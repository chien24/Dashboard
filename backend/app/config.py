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

KEYS = {"gemini": "GEMINI_API_KEY", "nvidia": "NVIDIA_API_KEY", "openrouter": "OPEN_ROUTER_API_KEY"}

# Thứ tự ưu tiên provider -> model. Override danh sách model bằng GEMINI_MODELS / NVIDIA_MODELS / OPENROUTER_MODELS.
PROVIDER_CHAIN = [
    {"provider": "gemini", "models": _list("GEMINI_MODELS", ["gemini-3.8-flash", "gemini-3.6-flash", "gemini-3.5-flash-lite"])},
    {"provider": "nvidia", "models": _list("NVIDIA_MODELS", ["nvidia/nemotron-3.5-parse",
                                                             "nvidia/nemotron-3.5-super-vl-120b-a12b",
                                                              "meta/llama-3.2-90b-vision-instruct"])},
    {"provider": "openrouter", "models": _list("OPENROUTER_MODELS", ["google/gemma-4-31b-it:free",
                                                                      "nvidia/nemotron-3.5-super-vl:free",
                                                                      "inclusionai/ling-3.2-flash:free"])},
]


def api_key(provider: str) -> str | None:
    return os.environ.get(KEYS[provider]) or None
