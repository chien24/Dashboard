"""Lớp 2 (mục 9): SQL do LLM viết là không đáng tin. Chỉ cho 1 câu SELECT (WITH/UNION được) trên 7 view."""
import sqlglot
from sqlglot import exp

VIEWS = frozenset({"v_scada_summary", "v_scada_abnormal", "v_dmwcs_sorted", "v_dmwcs_no_chute",
                   "v_dmwcs_capacity", "v_dmwcs_bcr", "v_report_quality"})
BAD_FUNCS = frozenset({"load_extension", "readfile", "writefile", "edit", "fts3_tokenizer", "zipfile", "sqlar_compress",
                       "sqlar_uncompress"})
BAD_NODES = (exp.Insert, exp.Update, exp.Delete, exp.Drop, exp.Create, exp.Alter, exp.Command, exp.Pragma,
             exp.Attach, exp.Detach, exp.Transaction, exp.Commit, exp.Rollback)


class GuardError(Exception):
    pass


def _base_tables() -> set[str]:
    from app import models  # noqa: F401  đăng ký bảng
    from app.db import Base
    return set(Base.metadata.tables)


def check(sql: str) -> str:
    """Trả SQL đã bỏ dấu ';' cuối nếu hợp lệ; không hợp lệ -> GuardError (lý do tiếng Việt, gửi lại cho LLM sửa)."""
    sql = (sql or "").strip().rstrip(";").strip()
    if not sql:
        raise GuardError("SQL rỗng")
    try:
        stmts = [s for s in sqlglot.parse(sql, read="sqlite") if s is not None]
    except sqlglot.errors.SqlglotError as e:
        raise GuardError(f"SQL không parse được: {str(e)[:300]}")
    if len(stmts) != 1:
        raise GuardError(f"Chỉ được 1 câu lệnh, đang có {len(stmts)}")
    st = stmts[0]
    if not isinstance(st, exp.Query):
        raise GuardError(f"Chỉ được SELECT, không được {st.key.upper()}")
    if bad := next(st.find_all(*BAD_NODES), None):
        raise GuardError(f"Không được dùng {bad.key.upper()}")

    ctes = {c.alias_or_name.lower() for c in st.find_all(exp.CTE)}
    if clash := ctes & (_base_tables() | VIEWS):
        raise GuardError(f"Tên CTE trùng tên bảng/view: {', '.join(sorted(clash))}")
    for t in st.find_all(exp.Table):
        name = (t.name or "").lower()
        if t.args.get("db") or t.args.get("catalog"):
            raise GuardError(f"Không được chỉ định schema: {t.sql()}")
        if name not in VIEWS and name not in ctes:
            raise GuardError(f"Chỉ được truy vấn 7 view {', '.join(sorted(VIEWS))}; không được dùng '{t.sql() or name}'")
    for f in st.find_all(exp.Func):
        name = f.sql(dialect="sqlite").split("(", 1)[0].strip().lower()  # tên đúng như SQLite sẽ chạy
        if name in BAD_FUNCS or name.startswith(("sqlite_", "pragma_")):
            raise GuardError(f"Không được dùng hàm {name}")
    return sql


def wrap_limit(sql: str, max_rows: int) -> str:
    """Bọc giới hạn dòng; xuống dòng để comment '--' cuối câu không nuốt dấu ')'."""
    return f"SELECT * FROM (\n{sql}\n) LIMIT {max_rows + 1}"
