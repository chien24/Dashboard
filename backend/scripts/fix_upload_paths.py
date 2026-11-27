"""Sửa đường dẫn ảnh trong bảng uploads sau khi chép dữ liệu sang máy / thư mục khác (ví dụ từ Windows vào Docker).
Bảng uploads lưu đường dẫn đầy đủ của máy cũ (D:\\...\\data\\uploads\\2026\\11\\16\\<sha>.jpg) nên ảnh cũ không hiện.
Ảnh luôn nằm ở UPLOAD_DIR/YYYY/MM/DD/<tên>, nên chỉ cần ghép 4 phần cuối vào UPLOAD_DIR hiện tại. Cần tài khoản web.

    cd backend
    py scripts/fix_upload_paths.py            # chỉ xem sẽ đổi gì, không ghi
    py scripts/fix_upload_paths.py --apply    # ghi vào DB
Docker:  docker compose exec app python scripts/fix_upload_paths.py --apply
"""
import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app import config, terminal  # noqa: E402

TAIL = re.compile(r"(\d{4})/(\d\d)/(\d\d)/([^/]+)$")


def new_path(stored: str) -> Path | None:
    """Đường dẫn mới trong UPLOAD_DIR hiện tại; None nếu không đúng dạng .../YYYY/MM/DD/<tên>."""
    m = TAIL.search(stored.replace("\\", "/"))
    return config.UPLOAD_DIR.joinpath(*m.groups()) if m else None


def main(argv=None):
    ap = argparse.ArgumentParser(description="Sửa đường dẫn ảnh trong bảng uploads theo UPLOAD_DIR hiện tại.")
    ap.add_argument("--apply", action="store_true", help="ghi vào DB (không có thì chỉ in ra)")
    args = ap.parse_args(argv)
    terminal.start("fix_upload_paths.py")
    from app.db import SessionLocal
    from app.models import Upload

    changed = missing = bad = 0
    with SessionLocal() as db:
        for up in db.query(Upload).order_by(Upload.id):
            p = new_path(up.stored_path)
            if p is None:
                bad += 1
                print(f"[bỏ qua] upload {up.id}: không nhận ra dạng đường dẫn {up.stored_path}")
                continue
            if not p.exists():
                missing += 1  # ảnh OCR lỗi đã bị xóa, hoặc chưa chép thư mục uploads sang
            if str(p) != up.stored_path:
                changed += 1
                up.stored_path = str(p)
        if args.apply:
            db.commit()
    print(f"UPLOAD_DIR: {config.UPLOAD_DIR}")
    print(f"{'Đã sửa' if args.apply else 'Sẽ sửa'} {changed} dòng · bỏ qua {bad} · "
          f"{missing} ảnh không thấy file ở chỗ mới (ảnh OCR lỗi đã bị xóa, hoặc chưa chép uploads/)")
    if changed and not args.apply:
        print("Chưa ghi gì. Chạy lại với --apply để ghi vào DB.")


if __name__ == "__main__":
    main()
