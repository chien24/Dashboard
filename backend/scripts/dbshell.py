"""Xem database trong terminal, CHỈ ĐỌC (cần tài khoản web). Xem HUONG_DAN_LOG_DB.md.

    cd backend
    py scripts/dbshell.py info              # file DB đang mở, số báo cáo / ảnh / job
    py scripts/dbshell.py tables            # các bảng, view và số dòng
    py scripts/dbshell.py schema reports    # cột của 1 bảng / view
    py scripts/dbshell.py jobs -n 10        # job OCR gần nhất
    py scripts/dbshell.py reports -n 10     # báo cáo gần nhất
    py scripts/dbshell.py providers         # trạng thái provider/model OCR (cooldown, lỗi)
    py scripts/dbshell.py sql "SELECT loai, COUNT(*) FROM reports GROUP BY loai"

Mở SQLite ở chế độ readonly: lệnh ghi/sửa/xóa đều bị từ chối, không đổi được dữ liệu.
"""
import argparse
import sqlite3
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app import terminal  # noqa: E402
from app.chatbot import executor  # noqa: E402

CELL = 60


def table(cols, rows, truncated=False, more="-n"):
    if not cols:
        return print("(không có cột)")
    cells = [[("" if v is None else str(v)).replace("\n", " ")[:CELL] for v in r] for r in rows]
    w = [max([len(c)] + [len(r[i]) for r in cells]) for i, c in enumerate(cols)]
    line = lambda vals: "  ".join(v.ljust(w[i]) for i, v in enumerate(vals)).rstrip()  # noqa: E731
    print(line(cols))
    print("  ".join("-" * x for x in w))
    for r in cells:
        print(line(r))
    print(f"({len(rows)} dòng{f', còn nữa, tăng {more} để xem nhiều hơn' if truncated else ''})")


def q(sql, params=(), max_rows=None, timeout=30):
    return executor.run(sql, params, max_rows=max_rows, timeout_s=timeout)


def cmd_info(_):
    p = executor.db_path().resolve()
    print(f"File: {p}")
    if not p.exists():
        sys.exit("Chưa có file DB ở đường dẫn trên. Kiểm tra DATABASE_URL và thư mục đang đứng (phải cd backend).")
    st = p.stat()
    print(f"Dung lượng: {st.st_size / 1024 / 1024:.1f} MB · sửa lúc {datetime.fromtimestamp(st.st_mtime):%Y-%m-%d %H:%M:%S}")
    one = lambda sql: q(sql)[1][0]  # noqa: E731
    n, tu, den = one("SELECT COUNT(*), MIN(report_date), MAX(report_date) FROM reports")
    print(f"Báo cáo: {n}" + (f" (ngày {tu} → {den})" if n else ""))
    print(f"Ảnh đã tải: {one('SELECT COUNT(*) FROM uploads')[0]}")
    jobs = q("SELECT status, COUNT(*) FROM jobs GROUP BY status ORDER BY status")[1]
    print("Job: " + (", ".join(f"{s} {c}" for s, c in jobs) or "0"))
    print(f"Hội thoại chatbot: {one('SELECT COUNT(*) FROM chat_conversations')[0]}")


def cmd_tables(_):
    names = q("SELECT name, type FROM sqlite_master WHERE type IN ('table','view') AND name NOT LIKE 'sqlite_%' "
              "ORDER BY type, name")[1]
    table(["ten", "loai", "so_dong"], [[n, t, q(f'SELECT COUNT(*) FROM "{n}"')[1][0][0]] for n, t in names])


def cmd_schema(a):
    if not q("SELECT 1 FROM sqlite_master WHERE name = ?", (a.name,))[1]:
        sys.exit(f"Không có bảng / view '{a.name}'. Xem danh sách: py scripts/dbshell.py tables")
    cols, rows, _ = q(f'PRAGMA table_info("{a.name}")')
    table(["cot", "kieu", "bat_buoc", "mac_dinh", "khoa_chinh"], [[r[1], r[2], r[3], r[4], r[5]] for r in rows])


def cmd_jobs(a):
    table(*q("SELECT j.id, j.status, j.loai_hint, u.original_name AS file, j.progress, j.report_id, j.created_at, "
             "j.finished_at, substr(j.error, 1, 80) AS error FROM jobs j LEFT JOIN uploads u ON u.id = j.upload_id "
             "ORDER BY j.id DESC", max_rows=a.n))


def cmd_reports(a):
    table(*q("SELECT id, loai, report_date, status, source_name, model, created_at FROM reports ORDER BY id DESC",
             max_rows=a.n))


def cmd_providers(_):
    table(*q("SELECT * FROM model_status ORDER BY provider, model"))


def cmd_sql(a):
    table(*q(a.query, max_rows=a.max, timeout=a.timeout), more="--max")


def main(argv=None):
    ap = argparse.ArgumentParser(description="Xem database OCR Dashboard, chỉ đọc (cần tài khoản web).")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("info", help="file DB đang mở và số liệu tổng quát").set_defaults(fn=cmd_info)
    sub.add_parser("tables", help="các bảng, view và số dòng").set_defaults(fn=cmd_tables)
    s = sub.add_parser("schema", help="cột của 1 bảng / view")
    s.add_argument("name")
    s.set_defaults(fn=cmd_schema)
    for name, fn in (("jobs", cmd_jobs), ("reports", cmd_reports)):
        s = sub.add_parser(name, help=f"{name} gần nhất")
        s.add_argument("-n", type=int, default=20)
        s.set_defaults(fn=fn)
    sub.add_parser("providers", help="trạng thái provider/model OCR").set_defaults(fn=cmd_providers)
    s = sub.add_parser("sql", help="chạy 1 câu SELECT (readonly)")
    s.add_argument("query")
    s.add_argument("--max", type=int, default=200, help="số dòng tối đa in ra (mặc định 200)")
    s.add_argument("--timeout", type=float, default=30, help="giây tối đa cho 1 truy vấn (mặc định 30)")
    s.set_defaults(fn=cmd_sql)
    args = ap.parse_args(argv)
    terminal.start("dbshell.py")
    if args.cmd != "info" and not executor.db_path().exists():
        sys.exit(f"Chưa có file DB: {executor.db_path().resolve()}")
    try:
        args.fn(args)
    except sqlite3.OperationalError as e:
        msg = str(e)
        if "readonly" in msg or "read-only" in msg:
            sys.exit(f"Lỗi: {msg}. DB mở ở chế độ readonly, lệnh này không sửa được dữ liệu.")
        sys.exit(f"Lỗi SQL: {msg}")
    except (sqlite3.Error, executor.SqlTimeout) as e:
        sys.exit(f"Lỗi SQL: {e}")


if __name__ == "__main__":
    main()
