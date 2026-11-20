"""sql_guard phải chặn mọi thứ ngoài 1 câu SELECT trên 7 view (mục 12)."""
import sqlite3

import pytest

from app.chatbot import executor
from app.chatbot.sql_guard import GuardError, check, wrap_limit

BLOCKED = [
    "INSERT INTO reports(loai) VALUES ('x')",
    "UPDATE reports SET status = 'ok'",
    "DELETE FROM reports",
    "DROP TABLE reports",
    "DROP VIEW v_dmwcs_sorted",
    "CREATE TABLE x (a int)",
    "ATTACH DATABASE 'x.db' AS x",
    "PRAGMA table_info(reports)",
    "SELECT 1; DELETE FROM reports",
    "SELECT * FROM v_dmwcs_sorted; SELECT * FROM v_dmwcs_bcr",
    "SELECT * FROM reports",
    "SELECT * FROM uploads",
    "SELECT * FROM sqlite_master",
    "SELECT * FROM main.v_dmwcs_sorted",
    "SELECT * FROM v_dmwcs_sorted WHERE report_id IN (SELECT id FROM reports)",
    "SELECT * FROM v_dmwcs_sorted s JOIN (SELECT * FROM (SELECT * FROM jobs)) j ON 1",
    "WITH x AS (SELECT * FROM model_status) SELECT * FROM x",
    "WITH reports AS (SELECT 1) SELECT * FROM reports",
    "WITH x AS (SELECT 1) DELETE FROM reports",
    "SELECT load_extension('evil')",
    "SELECT readfile('C:/secret.txt')",
    "SELECT * FROM pragma_table_info('reports')",
    "SELECT sqlite_version()",
    "",
]
ALLOWED = [
    "SELECT * FROM v_dmwcs_sorted",
    "select ngay, total from V_DMWCS_SORTED where ngay between '2026-11-09' and '2026-11-15';",
    "WITH t AS (SELECT ngay, SUM(total) s FROM v_dmwcs_sorted GROUP BY ngay) SELECT * FROM t ORDER BY ngay",
    "SELECT ngay FROM v_scada_summary UNION ALL SELECT ngay FROM v_dmwcs_sorted",
    "SELECT SUM(trang_thai = 'can_kiem_tra') AS n FROM v_report_quality -- ghi chú cuối",
]


@pytest.mark.parametrize("sql", BLOCKED)
def test_blocked(sql):
    with pytest.raises(GuardError):
        check(sql)


@pytest.mark.parametrize("sql", ALLOWED)
def test_allowed(sql):
    assert check(sql)


def test_wrap_keeps_trailing_comment_harmless():
    assert "\n) LIMIT 201" in wrap_limit(check(ALLOWED[-1]), 200)


def test_executor_is_read_only(clean_db):
    with pytest.raises(sqlite3.OperationalError):
        executor.run("DELETE FROM reports")  # lớp 1 vẫn chặn kể cả khi sql_guard bị lọt


def test_executor_truncates(clean_db):
    cols, rows, truncated = executor.run("WITH RECURSIVE n(i) AS (SELECT 1 UNION ALL SELECT i + 1 FROM n LIMIT 300) "
                                         "SELECT i FROM n", max_rows=200)
    assert cols == ["i"] and len(rows) == 200 and truncated


def test_executor_timeout(clean_db):
    slow = "WITH RECURSIVE n(i) AS (SELECT 1 UNION ALL SELECT i + 1 FROM n) SELECT COUNT(*) FROM n"
    with pytest.raises(executor.SqlTimeout):
        executor.run(slow, timeout_s=0.3)
