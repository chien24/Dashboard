"""Lớp 1 + 3 (mục 9): kết nối SQLite chỉ đọc riêng cho chatbot, timeout bằng progress handler."""
import sqlite3
import time
from pathlib import Path

from app import config


def db_path() -> Path:
    url = config.DATABASE_URL
    if not url.startswith("sqlite:///"):
        raise RuntimeError("Chatbot hiện chỉ hỗ trợ SQLite (Postgres: tạo role chatbot_ro chỉ SELECT trên 7 view)")
    return Path(url.split("///", 1)[1])


def connect() -> sqlite3.Connection:
    conn = sqlite3.connect(f"{db_path().resolve().as_uri()}?mode=ro", uri=True, check_same_thread=False)
    conn.execute("PRAGMA query_only = ON")
    return conn


class SqlTimeout(Exception):
    pass


def run(sql: str, params=(), max_rows: int | None = None, timeout_s: float | None = None):
    """-> (columns, rows, truncated). max_rows: lấy tối đa max_rows + 1 dòng để biết có bị cắt."""
    timeout_s = config.CHAT_SQL_TIMEOUT_S if timeout_s is None else timeout_s
    deadline = time.monotonic() + timeout_s
    conn = connect()
    try:
        conn.set_progress_handler(lambda: time.monotonic() > deadline, 10_000)  # trả True -> SQLite hủy truy vấn
        try:
            cur = conn.execute(sql, params)
            rows = cur.fetchmany(max_rows + 1) if max_rows else cur.fetchall()
        except sqlite3.OperationalError as e:
            if "interrupted" in str(e):
                raise SqlTimeout(f"Truy vấn chạy quá {timeout_s:g} giây") from e
            raise
        cols = [d[0] for d in cur.description or []]
    finally:
        conn.close()
    truncated = bool(max_rows) and len(rows) > max_rows
    if truncated:
        rows = rows[:max_rows]
    return cols, [list(r) for r in rows], truncated
