"""Few-shot động (mục 3 #12): chọn K ví dụ SQL gần câu hỏi nhất theo embedding (Cloudflare Workers AI, bge-m3).
Ví dụ hỏi lại/từ chối luôn được đưa vào. Embedding lỗi hoặc chưa cấu hình -> K ví dụ đầu file, chatbot vẫn chạy."""
import hashlib
import json
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


def embed_cached(name: str, texts: list[str], batch: int = 50) -> list[list[float]]:
    """Như embed() nhưng nhớ vector trong config.EMBED_CACHE theo (kho `name`, model, sha1 nội dung):
    khởi động lại chỉ embed đoạn mới / đã sửa; đoạn không còn dùng thì bỏ khỏi file. Lỗi giữa chừng thì không ghi gì."""
    try:
        store = json.loads(config.EMBED_CACHE.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        store = {}
    old = store.get(name) or {}
    vecs = old.get("vectors", {}) if old.get("model") == config.CHAT_EMBED_MODEL else {}
    keys = [hashlib.sha1(t.encode("utf-8")).hexdigest() for t in texts]
    miss = list({k: i for i, k in enumerate(keys) if k not in vecs}.values())  # đoạn trùng nội dung chỉ embed 1 lần
    for s in range(0, len(miss), batch):
        part = miss[s:s + batch]
        for i, v in zip(part, embed([texts[i] for i in part])):
            vecs[keys[i]] = [round(x, 6) for x in v]  # 6 chữ số đủ cho cosine, file nhỏ hơn một nửa
    if miss or set(vecs) != set(keys):
        store[name] = {"model": config.CHAT_EMBED_MODEL, "vectors": {k: vecs[k] for k in keys}}
        config.EMBED_CACHE.parent.mkdir(parents=True, exist_ok=True)
        tmp = config.EMBED_CACHE.with_suffix(".tmp")
        tmp.write_text(json.dumps(store, separators=(",", ":")), encoding="utf-8")
        tmp.replace(config.EMBED_CACHE)  # ghi file tạm rồi đổi tên: tắt server giữa chừng không làm hỏng file cũ
    return [vecs[k] for k in keys]


@lru_cache
def _bank(questions: tuple[str, ...]) -> list[list[float]]:
    return embed_cached("fewshot", list(questions))


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
