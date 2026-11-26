"""Few-shot động (mục 3 #12): chọn K ví dụ SQL gần câu hỏi nhất theo embedding (Cloudflare Workers AI, bge-m3).
Ví dụ hỏi lại/từ chối luôn được đưa vào. Embedding lỗi hoặc chưa cấu hình -> K ví dụ đầu file, chatbot vẫn chạy."""
import logging
import math
import os
from functools import lru_cache

from app import config

log = logging.getLogger("chatbot.fewshot")


@lru_cache
def _client():
    from openai import OpenAI

    account, key = os.environ.get("CLOUDFLARE_ACCOUNT_ID"), config.api_key("cloudflare")
    if not (config.CHAT_EMBED_MODEL and account and key):
        raise RuntimeError("chưa cấu hình CHAT_EMBED_MODEL / CLOUDFLARE_API_KEY / CLOUDFLARE_ACCOUNT_ID")
    return OpenAI(base_url=f"https://api.cloudflare.com/client/v4/accounts/{account}/ai/v1", api_key=key,
                  max_retries=0, timeout=10)


def embed(texts: list[str]) -> list[list[float]]:
    resp = _client().embeddings.create(model=config.CHAT_EMBED_MODEL, input=texts)
    return [d.embedding for d in resp.data]


@lru_cache
def _bank(questions: tuple[str, ...]) -> list[list[float]]:
    # shortcut: embed lại cả kho mỗi lần khởi động (1 request, vài chục câu); kho lên hàng nghìn câu thì lưu vector ra file
    return embed(list(questions))


def _cos(a: list[float], b: list[float]) -> float:
    return sum(x * y for x, y in zip(a, b)) / (math.sqrt(sum(x * x for x in a) * sum(y * y for y in b)) or 1)


def pick(question: str, examples: list[dict], k: int | None = None) -> list[dict]:
    """K ví dụ SQL giống câu hỏi nhất (giống nhất đứng cuối, sát câu hỏi) + mọi ví dụ hỏi lại/từ chối."""
    k = config.CHAT_FEWSHOT_K if k is None else k
    sql = [e for e in examples if e["answer"]["loai"] == "sql"]
    chosen = sql[:k]
    if len(sql) > k:
        try:
            q, bank = embed([question])[0], _bank(tuple(e["question"] for e in sql))
            top = sorted(zip(sql, bank), key=lambda p: _cos(q, p[1]), reverse=True)[:k]
            chosen = [e for e, _ in reversed(top)]
        except Exception as e:  # embedding chỉ để chọn ví dụ, lỗi không được làm hỏng câu trả lời
            log.warning("Few-shot động lỗi, dùng %d ví dụ đầu: %s", k, str(e)[:200])
    return chosen + [e for e in examples if e["answer"]["loai"] != "sql"]
