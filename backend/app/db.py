"""Engine SQLAlchemy, session và init_db(). SQLite mặc định; Docker dùng PostgreSQL (DATABASE_URL=postgresql+psycopg://...)."""
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
    eng = eng or engine
    Base.metadata.create_all(eng)
    from sqlalchemy import inspect, text
    if "ocr_version" not in {c["name"] for c in inspect(eng).get_columns("reports")}:  # DB cũ: create_all không thêm cột
        with eng.begin() as c:
            c.execute(text("ALTER TABLE reports ADD COLUMN ocr_version VARCHAR"))
    if "title" not in {c["name"] for c in inspect(eng).get_columns("chat_conversations")}:
        with eng.begin() as c:
            c.execute(text("ALTER TABLE chat_conversations ADD COLUMN title VARCHAR"))
    # create_all không tạo view: view của chatbot viết riêng cho từng loại DB (cùng tên cột)
    views = Path(__file__).parent / "chatbot" / ("views_postgres.sql" if eng.dialect.name == "postgresql" else "views.sql")
    conn = eng.raw_connection()
    try:
        if eng.dialect.name == "sqlite":
            conn.executescript(views.read_text(encoding="utf-8"))
        else:
            with conn.cursor() as cur:
                cur.execute(views.read_text(encoding="utf-8"))  # psycopg chạy được nhiều câu khi không có tham số
            conn.commit()
    finally:
        conn.close()


def get_db():
    """Dependency FastAPI: 1 session cho mỗi request."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
