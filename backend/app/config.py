"""Cấu hình đọc từ .env (tìm ở backend/.env, nếu không có thì thư mục cha)."""
import os
from pathlib import Path
from zoneinfo import ZoneInfo

from dotenv import load_dotenv

BACKEND_DIR = Path(__file__).resolve().parents[1]
load_dotenv(BACKEND_DIR / ".env") or load_dotenv(BACKEND_DIR.parent / ".env")


def _list(name: str, default: list[str]) -> list[str]:
    v = os.environ.get(name, "").strip()
    return [x.strip() for x in v.split(",") if x.strip()] if v else default


DATABASE_URL = os.environ.get("DATABASE_URL") or f"sqlite:///{BACKEND_DIR / 'data' / 'ocr.db'}"
UPLOAD_DIR = Path(os.environ.get("UPLOAD_DIR") or BACKEND_DIR / "data" / "uploads")
RETENTION_DAYS = int(os.environ.get("RETENTION_DAYS", 35))
TIMEZONE = os.environ.get("TIMEZONE", "Asia/Ho_Chi_Minh")
TZ = ZoneInfo(TIMEZONE)
OCR_CONCURRENCY = int(os.environ.get("OCR_CONCURRENCY", 1))
OCR_PASSES = int(os.environ.get("OCR_PASSES", 2))
MAX_UPLOAD_MB = float(os.environ.get("MAX_UPLOAD_MB", 10))
TIMEOUT_S = 120
# Tài khoản dùng chung (đổi trong .env khi deploy). SESSION_SECRET: chuỗi ngẫu nhiên dài để ký cookie phiên.
AUTH_USER = os.environ.get("AUTH_USER")
AUTH_PASSWORD = os.environ.get("AUTH_PASSWORD")
SESSION_SECRET = os.environ.get("SESSION_SECRET")

# Log (HUONG_DAN_LOG_DB.md). LOG_ACCESS: api = chỉ dòng truy cập /api/, all = mọi request, off = tắt dòng truy cập.
LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO").upper()
LOG_TO_FILE = os.environ.get("LOG_TO_FILE", "1") != "0"
LOG_DIR = Path(os.environ.get("LOG_DIR") or BACKEND_DIR / "data" / "logs")
LOG_RETENTION_DAYS = int(os.environ.get("LOG_RETENTION_DAYS", RETENTION_DAYS))
LOG_ACCESS = os.environ.get("LOG_ACCESS", "api").lower()

KEYS = {"cloudflare": "CLOUDFLARE_API_KEY", "nvidia": "NVIDIA_API_KEY", "openrouter": "OPEN_ROUTER_API_KEY"}

# Thứ tự ưu tiên provider -> model. Override danh sách model bằng CLOUDFLARE_MODELS / NVIDIA_MODELS / OPENROUTER_MODELS.
PROVIDER_CHAIN = [
    {"provider": "cloudflare", "models": _list("CLOUDFLARE_MODELS", ["@cf/mistralai/mistral-small-3.1-24b-instruct",
                                                                     "@cf/qwen/qwen3.8-27b",
                                                                     "@cf/meta/llama-4-scout-17b-16e-instruct"])},
    {"provider": "nvidia", "models": _list("NVIDIA_MODELS", ["nvidia/nemotron-3.5-parse",
                                                             "nvidia/nemotron-3.5-super-vl-120b-a12b",
                                                              "meta/llama-3.2-90b-vision-instruct"])},
    {"provider": "openrouter", "models": _list("OPENROUTER_MODELS", ["nvidia/nemotron-3.5-super-vl:free",
                                                                      "inclusionai/ling-3.2-flash:free"])},
]


def api_key(provider: str) -> str | None:
    if provider == "cloudflare" and not os.environ.get("CLOUDFLARE_ACCOUNT_ID"):
        return None  # thiếu account ID thì coi như chưa cấu hình
    return os.environ.get(KEYS[provider]) or None


# ---------------------------------------------------------------- chatbot (request/DAC_TA_CHATBOT.md mục 8)
# Groq là provider chính; OpenRouter chỉ dùng khi mọi model Groq đều lỗi hoặc đang cooldown.
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
GROQ_BASE_URL = os.environ.get("GROQ_BASE_URL", "https://api.groq.com/openai/v1")
CHAT_SQL_MODELS = _list("CHAT_SQL_MODELS", ["qwen/qwen3.8-27b", "openai/gpt-oss-120b", "openai/gpt-oss-20b"])
CHAT_SUMMARY_MODELS = _list("CHAT_SUMMARY_MODELS", ["qwen/qwen3.8-27b", "openai/gpt-oss-20b"])
CHAT_SQL_REASONING_EFFORT = os.environ.get("CHAT_SQL_REASONING_EFFORT", "low")
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY") or os.environ.get("OPEN_ROUTER_API_KEY")
OPENROUTER_BASE_URL = os.environ.get("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")
CHAT_SQL_FALLBACK_MODELS = _list("CHAT_SQL_FALLBACK_MODELS", ["nvidia/nemotron-3-ultra-550b-a55b:free",
                                                              "google/gemma-4-31b-it:free"])
CHAT_SUMMARY_FALLBACK_MODELS = _list("CHAT_SUMMARY_FALLBACK_MODELS", ["nvidia/nemotron-3.5-lightning:free"])
CHAT_SQL_RETRIES = int(os.environ.get("CHAT_SQL_RETRIES", 2))
CHAT_LLM_TIMEOUT_S = float(os.environ.get("CHAT_LLM_TIMEOUT_S", 60))
CHAT_SQL_TIMEOUT_S = float(os.environ.get("CHAT_SQL_TIMEOUT_S", 5))
CHAT_MAX_ROWS = int(os.environ.get("CHAT_MAX_ROWS", 200))
CHAT_SUMMARY_ROWS = int(os.environ.get("CHAT_SUMMARY_ROWS", 50))
CHAT_HISTORY_TURNS = int(os.environ.get("CHAT_HISTORY_TURNS", 6))
CHAT_RATE_LIMIT_PER_MIN = int(os.environ.get("CHAT_RATE_LIMIT_PER_MIN", 10))
CHAT_RETENTION_DAYS = int(os.environ.get("CHAT_RETENTION_DAYS", 30))  # hội thoại không dùng quá N ngày thì xóa
# Few-shot động (mục 3 #12): embedding qua Cloudflare Workers AI (dùng key OCR). Rỗng = tắt, dùng ví dụ cố định.
CHAT_EMBED_MODEL = os.environ.get("CHAT_EMBED_MODEL", "@cf/baai/bge-m3")
EMBED_CACHE = Path(os.environ.get("EMBED_CACHE") or BACKEND_DIR / "data" / "embeddings.json")  # vector đã embed (docs, few-shot)
CHAT_FEWSHOT_K = int(os.environ.get("CHAT_FEWSHOT_K", 6))  # số ví dụ SQL đưa vào prompt (+ ví dụ hỏi lại/từ chối luôn có)
