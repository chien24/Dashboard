"""Xem log backend trong terminal (cần tài khoản web). Xem HUONG_DAN_LOG_DB.md.

    cd backend
    py scripts/logs.py                      # 50 dòng cuối của log hôm nay
    py scripts/logs.py -n 200 --level WARNING
    py scripts/logs.py --grep "Job 12" --date 2026-11-25
    py scripts/logs.py -f                   # theo dõi trực tiếp, Ctrl+C để thoát
    py scripts/logs.py --list               # liệt kê các file log
"""
import argparse
import re
import sys
import time
from datetime import date, datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app import config, terminal  # noqa: E402
from app.logging_setup import log_file  # noqa: E402
from app.models import now  # noqa: E402

LEVELS = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
HEAD = re.compile(r"^\d{4}-\d\d-\d\d \d\d:\d\d:\d\d (\w+) ")  # đầu 1 bản ghi; dòng khác (traceback) thuộc bản ghi trước


def records(lines):
    """Gom dòng thành bản ghi: [(level, text)]; traceback nhiều dòng đi cùng dòng log của nó."""
    out = []
    for line in lines:
        if m := HEAD.match(line):
            out.append([m.group(1), line])
        elif out:
            out[-1][1] += line
        else:
            out.append(["INFO", line])
    return out


def keep(rec, level, grep):
    lv, text = rec
    return (LEVELS.index(lv) if lv in LEVELS else 1) >= LEVELS.index(level) and (not grep or grep in text.lower())


def show(lines, args):
    for _, text in [r for r in records(lines) if keep(r, args.level, args.grep)][-args.n:] if args.n else []:
        sys.stdout.write(text if text.endswith("\n") else text + "\n")
    sys.stdout.flush()


def follow(args):
    path, pos, buf = None, 0, ""
    print(f"Đang theo dõi log (Ctrl+C để thoát), thư mục {config.LOG_DIR}", file=sys.stderr)
    while True:
        p = log_file()
        if p != path:  # mới mở hoặc sang ngày mới
            path, pos, buf = p, (p.stat().st_size if p.exists() and path is None else 0), ""
            if pos:  # lần đầu: in N bản ghi cuối trước khi theo dõi
                show(p.read_text(encoding="utf-8", errors="replace").splitlines(keepends=True), args)
        if path.exists() and path.stat().st_size > pos:
            with path.open("rb") as f:
                f.seek(pos)
                chunk = f.read()
            pos += len(chunk)
            buf += chunk.decode("utf-8", errors="replace")
            *done, buf = buf.split("\n")  # phần chưa hết dòng để lần sau
            for r in records([x + "\n" for x in done]):
                if keep(r, args.level, args.grep):
                    sys.stdout.write(r[1])
            sys.stdout.flush()
        time.sleep(0.5)


def list_files():
    files = sorted(config.LOG_DIR.glob("backend-*.log"))
    if not files:
        print(f"Chưa có file log nào trong {config.LOG_DIR}")
    for p in files:
        st = p.stat()
        print(f"{p.name}  {st.st_size / 1024:8.1f} KB  sửa lúc {datetime.fromtimestamp(st.st_mtime):%Y-%m-%d %H:%M:%S}")


def main(argv=None):
    ap = argparse.ArgumentParser(description="Xem log backend OCR Dashboard (cần tài khoản web).")
    ap.add_argument("-n", type=int, default=50, help="số bản ghi cuối cần in (mặc định 50)")
    ap.add_argument("-f", "--follow", action="store_true", help="theo dõi log hôm nay trực tiếp")
    ap.add_argument("--list", action="store_true", help="liệt kê các file log")
    ap.add_argument("--date", type=date.fromisoformat, help="ngày cần xem, dạng YYYY-MM-DD (mặc định hôm nay)")
    ap.add_argument("--level", type=str.upper, choices=LEVELS, default="DEBUG", help="chỉ in từ mức này trở lên")
    ap.add_argument("--grep", type=str.lower, help="chỉ in bản ghi có chứa chữ này (không phân biệt hoa thường)")
    args = ap.parse_args(argv)
    terminal.start("logs.py")
    if args.list:
        return list_files()
    if args.follow:
        try:
            return follow(args)
        except KeyboardInterrupt:
            return
    p = log_file(args.date or now().date())
    if not p.exists():
        print(f"Chưa có log ngày {(args.date or now().date()):%d/%m/%Y} ({p}). Các file đang có:")
        return list_files()
    show(p.read_text(encoding="utf-8", errors="replace").splitlines(keepends=True), args)


if __name__ == "__main__":
    main()
