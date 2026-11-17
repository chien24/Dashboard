"""Engine SQLAlchemy, session và init_db(). SQLite mặc định; đổi DATABASE_URL để dùng PostgreSQL."""
from pathlib import Path

from sqlalchemy import create_engine, event
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app import config


class Base(DeclarativeBase):
    pass


def make_engine(url: str = config.DATABASE_URL):
    sqlite = url.startswith("sqlite")
    if sqlite and ":memory:" not in url:
        Path(url.split("///", 1)[1]).parent.mkdir(parents=True, exist_ok=True)
    eng = create_engine(url, connect_args={"check_same_thread": False} if sqlite else {})
    if sqlite:
        @event.listens_for(eng, "connect")
        def _pragma(conn, _):  # SQLite mặc định tắt khóa ngoại -> ON DELETE CASCADE không chạy nếu không bật
            cur = conn.cursor()
            cur.execute("PRAGMA foreign_keys=ON")
            cur.execute("PRAGMA journal_mode=WAL")  # worker OCR ghi trong lúc API đọc
            cur.close()
    return eng


engine = make_engine()
SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)


def init_db(eng=None):
    from app import models  # noqa: F401  đăng ký bảng
    Base.metadata.create_all(eng or engine)


def get_db():
    """Dependency FastAPI: 1 session cho mỗi request."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
