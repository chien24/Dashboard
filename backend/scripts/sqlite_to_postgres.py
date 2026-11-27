"""Chép toàn bộ dữ liệu từ file SQLite cũ (backend/data/ocr.db) sang DB đang cấu hình (DATABASE_URL, thường là
PostgreSQL trong Docker). Chỉ chép vào DB TRỐNG (chưa có báo cáo, ảnh, job, hội thoại) để không trộn / trùng dữ liệu.
Cần tài khoản web. Xem HUONG_DAN_DOCKER.md mục "Chuyển dữ liệu".

    docker compose run --rm -v "D:\\...\\backend\\data:/old:ro" backend python scripts/sqlite_to_postgres.py /old/ocr.db
Chép xong: chép thư mục uploads/ vào volume rồi chạy scripts/fix_upload_paths.py --apply (đường dẫn ảnh của máy cũ).
"""
import argparse
import shutil
import sqlite3
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from sqlalchemy import func, insert, select, text  # noqa: E402

from app import terminal  # noqa: E402

BATCH = 1000


def _open_readonly(p: Path) -> sqlite3.Connection:
    """mode=ro; DB chế độ WAL trong thư mục chỉ đọc (mount :ro) thì không tạo được file -shm -> mở immutable,
    nhưng chỉ khi không còn file -wal có dữ liệu chưa ghi vào DB (backend cũ còn chạy / tắt đột ngột)."""
    uri = p.resolve().as_uri()
    try:
        conn = sqlite3.connect(f"{uri}?mode=ro", uri=True)
        conn.execute("SELECT 1 FROM sqlite_master LIMIT 1")
        return conn
    except sqlite3.OperationalError:
        wal = p.with_name(p.name + "-wal")
        if wal.exists() and wal.stat().st_size:
            raise SystemExit(f"{wal.name} còn dữ liệu chưa ghi vào {p.name}: tắt hẳn backend cũ (start_backend.bat) "
                             "rồi chạy lại, hoặc mount thư mục cũ không có :ro")
        return sqlite3.connect(f"{uri}?immutable=1", uri=True)


def copy(src_path: Path, dst_engine) -> dict[str, int]:
    """-> {bảng: số dòng đã chép}. Bảng đích phải trống."""
    from app import models  # noqa: F401  đăng ký bảng
    from app.db import Base, init_db, make_engine

    # chép ra bản tạm (backup API: bản chụp nhất quán) rồi mới init_db: KHÔNG sửa file cũ, mount :ro vẫn chạy
    snap = Path(tempfile.mkdtemp(prefix="ocr_src_")) / "ocr.db"
    a = _open_readonly(src_path)
    b = sqlite3.connect(snap)
    try:
        a.backup(b)
    finally:
        a.close()
        b.close()
    src = make_engine(f"sqlite:///{snap.as_posix()}")
    init_db(src)  # SQLite cũ thiếu cột mới (ocr_version, title...) thì thêm trước khi đọc
    init_db(dst_engine)
    tables = Base.metadata.sorted_tables  # bảng cha trước bảng con (khóa ngoại)
    with dst_engine.connect() as d:
        if busy := [t.name for t in tables if d.execute(select(func.count()).select_from(t)).scalar()]:
            raise SystemExit(f"DB đích đã có dữ liệu ở bảng: {', '.join(busy)}. Chỉ chép vào DB trống.")
    done = {}
    with src.connect() as s, dst_engine.begin() as d:  # 1 transaction: lỗi giữa chừng thì DB đích vẫn trống
        for t in tables:
            n = 0
            for chunk in s.execute(select(t)).mappings().partitions(BATCH):
                d.execute(insert(t), [dict(r) for r in chunk])
                n += len(chunk)
            done[t.name] = n
        if dst_engine.dialect.name == "postgresql":  # id đã chép tay: dời bộ đếm id qua id lớn nhất
            for t in tables:
                if "id" in t.c:
                    d.execute(text(f"SELECT setval(pg_get_serial_sequence('{t.name}', 'id'), "
                                   f"COALESCE((SELECT MAX(id) FROM {t.name}), 1), "
                                   f"(SELECT MAX(id) FROM {t.name}) IS NOT NULL)"))
    src.dispose()
    shutil.rmtree(snap.parent, ignore_errors=True)
    return done


def main(argv=None):
    ap = argparse.ArgumentParser(description="Chép dữ liệu từ file SQLite cũ sang DB đang cấu hình (DB trống).")
    ap.add_argument("sqlite_file", type=Path, help="file ocr.db cũ")
    args = ap.parse_args(argv)
    terminal.start("sqlite_to_postgres.py")
    if not args.sqlite_file.is_file():
        sys.exit(f"Không thấy file {args.sqlite_file}")
    from app.db import engine

    for name, n in copy(args.sqlite_file, engine).items():
        print(f"{name:24} {n:6} dòng")
    print("Xong. Tiếp theo: chép uploads/ vào volume rồi chạy scripts/fix_upload_paths.py --apply")


if __name__ == "__main__":
    main()
