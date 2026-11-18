"""Test dùng DB SQLite tạm và thư mục upload tạm; không cần API key, không gọi mạng."""
import os
import tempfile
from pathlib import Path

_TMP = Path(tempfile.mkdtemp(prefix="ocr_test_"))
os.environ["DATABASE_URL"] = f"sqlite:///{(_TMP / 'test.db').as_posix()}"
os.environ["UPLOAD_DIR"] = str(_TMP / "uploads")

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


@pytest.fixture
def clean_db():
    """DB trống cho mỗi test."""
    Base.metadata.drop_all(engine)
    init_db()
    yield
