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


@pytest.fixture
def clean_db():
    """DB trống cho mỗi test."""
    Base.metadata.drop_all(engine)
    init_db()
    yield
