"""Test dùng DB SQLite tạm và thư mục upload tạm; không cần API key, không gọi mạng.
Chạy trên PostgreSQL: đặt TEST_DATABASE_URL=postgresql+psycopg://... (DB riêng cho test: các test XÓA SẠCH bảng)."""
import os
import tempfile
from pathlib import Path

_TMP = Path(tempfile.mkdtemp(prefix="ocr_test_"))
os.environ["DATABASE_URL"] = os.environ.get("TEST_DATABASE_URL") or f"sqlite:///{(_TMP / 'test.db').as_posix()}"
os.environ.pop("CHAT_DATABASE_URL", None)  # test chạy SQL chatbot bằng chính DB test
os.environ["UPLOAD_DIR"] = str(_TMP / "uploads")
os.environ["EMBED_CACHE"] = str(_TMP / "embeddings.json")
os.environ["LOG_DIR"] = str(_TMP / "logs")  # test không ghi vào log thật

import pytest  # noqa: E402

from app.db import Base, engine, init_db  # noqa: E402

FIXTURES = Path(__file__).parent / "fixtures"


def client():
    """TestClient đã đăng nhập. Không dùng `with`: không chạy worker/scheduler."""
    from fastapi.testclient import TestClient

    from app import config
    from app.main import app

    c = TestClient(app)
    assert c.post("/api/auth/login", json={"username": config.AUTH_USER, "password": config.AUTH_PASSWORD}).status_code == 200
    return c


@pytest.fixture(autouse=True)
def no_embedding(monkeypatch):
    """Few-shot động không gọi Cloudflare trong test: embed lỗi -> fewshot dùng K ví dụ đầu."""
    from app.chatbot import fewshot

    def fail(texts):
        raise RuntimeError("test: tắt embedding")

    monkeypatch.setattr(fewshot, "embed", fail)


def drop_all():
    """Xóa mọi bảng. PostgreSQL không cho xóa bảng còn view phụ thuộc (SQLite thì cho): xóa 7 view trước."""
    from app.chatbot.sql_guard import VIEWS

    with engine.begin() as c:
        for v in sorted(VIEWS):  # SQLite không nhận nhiều view trong 1 câu DROP VIEW
            c.exec_driver_sql(f"DROP VIEW IF EXISTS {v}")
    Base.metadata.drop_all(engine)


@pytest.fixture
def clean_db():
    """DB trống cho mỗi test."""
    drop_all()
    init_db()
    yield
