"""Lớp 1 + 3 (mục 9): kết nối chỉ đọc riêng cho chatbot, có timeout.
SQLite: mở file mode=ro + query_only, timeout bằng progress handler.
PostgreSQL: role chỉ SELECT trên 7 view (CHAT_DATABASE_URL), transaction READ ONLY, statement_timeout."""
import sqlite3
import time
from datetime import date, datetime
from decimal import Decimal
from pathlib import Path

from app import config


class SqlError(Exception):
    """Lỗi khi chạy SQL (cú pháp, ghi vào DB chỉ đọc...): pipeline gửi lại cho LLM sửa."""


class SqlTimeout(SqlError):
    pass


def db_path() -> Path:
    url = config.DATABASE_URL
    if not url.startswith("sqlite:///"):
        raise RuntimeError("DATABASE_URL không phải SQLite")
    return Path(url.split("///", 1)[1])


def connect() -> sqlite3.Connection:
    conn = sqlite3.connect(f"{db_path().resolve().as_uri()}?mode=ro", uri=True, check_same_thread=False)
    conn.execute("PRAGMA query_only = ON")
    return conn


def _value(v):
    """Postgres trả Decimal / date / datetime: đổi về dạng SQLite trả (float, chuỗi) để JSON hóa và hiển thị như cũ."""
    if isinstance(v, Decimal):
        return float(v)
    if isinstance(v, (date, datetime)):
        return str(v)
    return v


def _run_postgres(url: str, sql: str, params, max_rows, timeout_s):
    import psycopg
    from sqlalchemy.engine import make_url

    dsn = make_url(url).set(drivername="postgresql").render_as_string(hide_password=False)
    if params:  # checks.py viết tham số kiểu "?" (SQLite); "%" có sẵn (LIKE '%x%') phải nhân đôi cho psycopg
        sql = sql.replace("%", "%%").replace("?", "%s")
    try:
        with psycopg.connect(dsn, connect_timeout=5, options=f"-c default_transaction_read_only=on "
                                                              f"-c statement_timeout={max(1, int(timeout_s * 1000))}") as conn:
            cur = conn.execute(sql, params or None)
            rows = cur.fetchmany(max_rows + 1) if max_rows else cur.fetchall()
            cols = [d.name for d in cur.description or []]
            conn.rollback()
    except psycopg.errors.QueryCanceled as e:
        raise SqlTimeout(f"Truy vấn chạy quá {timeout_s:g} giây") from e
    except psycopg.Error as e:
        raise SqlError(str(e).strip()) from e
    return cols, [[_value(v) for v in r] for r in rows]


def _run_sqlite(sql: str, params, max_rows, timeout_s):
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
            raise SqlError(str(e)) from e
        except sqlite3.Error as e:
            raise SqlError(str(e)) from e
        cols = [d[0] for d in cur.description or []]
    finally:
        conn.close()
    return cols, [list(r) for r in rows]


def run(sql: str, params=(), max_rows: int | None = None, timeout_s: float | None = None, url: str | None = None):
    """-> (columns, rows, truncated). max_rows: lấy tối đa max_rows + 1 dòng để biết có bị cắt.
    url: mặc định CHAT_DATABASE_URL (Postgres: role chỉ đọc 7 view); dbshell truyền DATABASE_URL để xem mọi bảng."""
    timeout_s = config.CHAT_SQL_TIMEOUT_S if timeout_s is None else timeout_s
    url = url or config.CHAT_DATABASE_URL
    if url.startswith("postgresql"):
        cols, rows = _run_postgres(url, sql, params, max_rows, timeout_s)
    else:
        cols, rows = _run_sqlite(sql, params, max_rows, timeout_s)
    truncated = bool(max_rows) and len(rows) > max_rows
    if truncated:
        rows = rows[:max_rows]
    return cols, rows, truncated
