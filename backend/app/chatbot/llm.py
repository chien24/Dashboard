"""Client LLM cho chatbot (mục 8). Groq là provider chính; OpenRouter chỉ dùng khi mọi model Groq đều lỗi hoặc đang
cooldown. Cả hai tương thích OpenAI API (SDK openai). Cooldown/disabled lưu chung bảng model_status với router OCR,
provider = 'groq-chat' / 'openrouter-chat' để không lẫn trạng thái OCR. Token đã dùng ghi vào chat_token_usage."""
import logging
import math
import re
from datetime import datetime, timedelta

from sqlalchemy import select
from sqlalchemy.dialects.sqlite import insert

from app import config
from app.db import SessionLocal
from app.models import ChatTokenUsage, ModelStatus, now
from app.ocr.providers.base import AuthError, BadOutput, ModelNotFound, QuotaExceeded, map_error
from app.ocr.router import is_blocked, mark

log = logging.getLogger("chatbot.llm")
GROQ, OPENROUTER = "groq-chat", "openrouter-chat"
NHAC_JSON = "Câu trả lời trước không phải JSON hợp lệ. Chỉ trả về đúng 1 object JSON theo định dạng đã nêu, không thêm chữ nào."


def providers() -> list[tuple[str, str, str | None, dict[str, list[str]]]]:
    """(tên trong model_status, base_url, api key, {vai trò: danh sách model}) theo thứ tự thử."""
    return [
        (GROQ, config.GROQ_BASE_URL, config.GROQ_API_KEY,
         {"sql": config.CHAT_SQL_MODELS, "summary": config.CHAT_SUMMARY_MODELS}),
        (OPENROUTER, config.OPENROUTER_BASE_URL, config.OPENROUTER_API_KEY,
         {"sql": config.CHAT_SQL_FALLBACK_MODELS, "summary": config.CHAT_SUMMARY_FALLBACK_MODELS}),
    ]


def params(provider: str, model: str, role: str) -> dict:
    """Tham số gọi theo vai trò; thinking theo từng họ model (Groq: gpt-oss có low/medium/high, Qwen chỉ none/default)."""
    p = {"temperature": 0, "max_tokens": 1500} if role == "sql" else {"temperature": 0.2, "max_tokens": 600}
    if provider == GROQ:
        effort = config.CHAT_SQL_REASONING_EFFORT if role == "sql" else "low"
        if "qwen" in model:
            p["reasoning_effort"] = "none" if role == "summary" or effort == "none" else "default"
            p["extra_body"] = {"reasoning_format": "hidden"}  # content không lẫn <think>, dùng được với json_object
        elif "gpt-oss" in model:
            p["reasoning_effort"] = effort
            p["extra_body"] = {"include_reasoning": False}
    elif role == "summary":
        p["extra_body"] = {"reasoning": {"enabled": False}}
    return p


class AllModelsFailed(Exception):
    def __init__(self, errors: list[str], retry_at: datetime | None, quota: bool):
        self.errors, self.retry_at, self.quota = errors, retry_at, quota
        super().__init__("Tất cả model chatbot đều lỗi: " + (" | ".join(errors) or "không có model nào dùng được"))


class NoKey(Exception):
    pass


def strip_think(text: str | None) -> str:
    return re.sub(r"<think>.*?</think>", "", text or "", flags=re.S).strip()


def retry_after(e: Exception) -> datetime | None:
    """Header retry-after (giây) của lỗi 429 -> thời điểm hết cooldown."""
    resp = getattr(e, "response", None)
    try:
        s = float(resp.headers.get("retry-after"))
    except (AttributeError, TypeError, ValueError):
        return None
    return now() + timedelta(seconds=max(1, math.ceil(s)))


def next_retry_at(pairs: list[tuple[str, str]]) -> datetime | None:
    """cooldown_until gần nhất trong chuỗi, để báo người dùng 'thử lại sau X phút'."""
    with SessionLocal() as db:
        rows = db.execute(select(ModelStatus.provider, ModelStatus.model, ModelStatus.cooldown_until)
                          .where(ModelStatus.state == "cooldown")).all()
    return min((t for p, m, t in rows if t and (p, m) in pairs), default=None)


def record_usage(provider: str, model: str, prompt_tokens: int, completion_tokens: int):
    """Cộng dồn token theo ngày + provider + model (UPSERT nguyên tử, nhiều luồng gọi cùng lúc vẫn đúng)."""
    stmt = insert(ChatTokenUsage).values(ngay=now().date(), provider=provider, model=model, requests=1,
                                         prompt_tokens=prompt_tokens, completion_tokens=completion_tokens)
    stmt = stmt.on_conflict_do_update(index_elements=["ngay", "provider", "model"], set_={
        "requests": ChatTokenUsage.requests + 1,
        "prompt_tokens": ChatTokenUsage.prompt_tokens + stmt.excluded.prompt_tokens,
        "completion_tokens": ChatTokenUsage.completion_tokens + stmt.excluded.completion_tokens})
    with SessionLocal() as db:
        db.execute(stmt)
        db.commit()


class Llm:
    """1 đối tượng cho 1 câu hỏi; đếm số lần gọi API (calls) và token (tokens) để log."""

    def __init__(self, client=None):
        self._fixed_client = client  # test truyền client giả
        self._clients: dict[str, object] = {}
        self.calls = 0
        self.tokens = 0

    def client(self, provider: str, base_url: str, key: str | None):
        if self._fixed_client is not None:
            return self._fixed_client
        if provider not in self._clients:
            if not key:
                raise NoKey(f"chưa cấu hình API key của {provider}")
            from openai import OpenAI

            headers = {"HTTP-Referer": "https://localhost", "X-Title": "OCR Dashboard Chat"} if provider == OPENROUTER else None
            self._clients[provider] = OpenAI(base_url=base_url, api_key=key, max_retries=0,
                                             timeout=config.CHAT_LLM_TIMEOUT_S, default_headers=headers)
        return self._clients[provider]

    def _call(self, client, provider: str, model: str, messages: list[dict], kw: dict, json_mode: bool) -> str:
        kw = dict(model=model, messages=messages, **kw)
        if json_mode:
            kw["response_format"] = {"type": "json_object"}
        self.calls += 1
        resp = client.chat.completions.create(**kw)
        if u := getattr(resp, "usage", None):
            pt, ct = u.prompt_tokens or 0, u.completion_tokens or 0
            self.tokens += pt + ct
            log.info("LLM usage %s/%s: prompt=%d completion=%d", provider, model, pt, ct)
            try:
                record_usage(provider, model, pt, ct)
            except Exception:  # ghi thống kê lỗi không được làm hỏng câu trả lời
                log.exception("Không ghi được chat_token_usage")
        return resp.choices[0].message.content if resp.choices else ""

    def chat(self, role: str, messages: list[dict], parse=None):
        """-> (kết quả, 'provider:model'). parse(text) trả giá trị hoặc raise BadOutput: hỏng thì nhắc lại 1 lần cùng
        model, vẫn hỏng thì đổi model. 429 -> cooldown theo retry-after; 404 -> disabled; 401/402/403 -> bỏ cả provider."""
        errors, quota, pairs = [], False, []
        for provider, base_url, key, models in providers():
            for model in models[role]:
                pairs.append((provider, model))
                if why := is_blocked(provider, model):
                    errors.append(f"{provider}/{model}: bỏ qua ({why})")
                    quota = quota or "cooldown" in why
                    continue
                try:
                    client = self.client(provider, base_url, key)
                except NoKey as e:
                    errors.append(str(e))
                    break
                msgs, json_mode, reminded, skip_provider = list(messages), parse is not None, False, False
                while True:
                    try:
                        text = self._call(client, provider, model, msgs, params(provider, model, role), json_mode)
                    except Exception as e:
                        status = getattr(e, "status_code", None)
                        if json_mode and status in (400, 422) and "json" in str(e).lower():
                            json_mode = False  # model không hỗ trợ response_format -> parse lỏng
                            continue
                        err = map_error(status, f"{type(e).__name__}: {str(e)[:300]}")
                        errors.append(f"{provider}/{model}: {err}")
                        log.warning("chat %s %s/%s lỗi: %s", role, provider, model, err)
                        if isinstance(err, QuotaExceeded):
                            quota = True
                            mark(provider, model, "cooldown", str(err), until=retry_after(e))
                        elif isinstance(err, ModelNotFound):
                            mark(provider, model, "disabled", str(err))
                        elif isinstance(err, AuthError):
                            skip_provider = True  # key sai/hết credit: model khác cùng provider cũng vậy
                        break
                    mark(provider, model, "ok")
                    label = f"{provider.removesuffix('-chat')}:{model}"
                    if parse is None:
                        return strip_think(text), label
                    try:
                        return parse(text), label
                    except BadOutput as e:
                        if reminded:
                            errors.append(f"{provider}/{model}: {e}")
                            break
                        reminded = True
                        msgs += [{"role": "assistant", "content": (text or "")[:2000]}, {"role": "user", "content": NHAC_JSON}]
                if skip_provider:
                    break
        raise AllModelsFailed(errors, next_retry_at(pairs), quota)
