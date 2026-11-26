"""Xem / sửa file .env bằng terminal (cần tài khoản web). Xem HUONG_DAN_LOG_DB.md.

    cd backend
    py scripts/env.py list                       # mọi biến; biến bí mật chỉ hiện "có / trống" (--show để hiện)
    py scripts/env.py get LOG_LEVEL
    py scripts/env.py set LOG_LEVEL WARNING      # tự sao lưu .env trước khi sửa
    py scripts/env.py set AUTH_PASSWORD          # không ghi giá trị: hỏi ẩn (không lưu vào lịch sử lệnh)
    py scripts/env.py unset LOG_DIR              # xóa dòng của biến (về giá trị mặc định)

Sửa xong phải khởi động lại backend thì mới có tác dụng.
"""
import argparse
import getpass
import re
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app import config, terminal  # noqa: E402

LINE = re.compile(r"^\s*(?:export\s+)?([A-Za-z_][A-Za-z0-9_]*)\s*=(.*)$")
NAME = re.compile(r"^[A-Z_][A-Z0-9_]*$")
SECRET = re.compile(r"KEY|PASSWORD|SECRET|TOKEN|ACCOUNT_ID|AUTH_USER")  # tên đăng nhập = nửa tài khoản: che luôn
INT = lambda v: v.isdigit()  # noqa: E731
CHECK = {  # biến có giá trị cố định: kiểm trước khi ghi, gõ sai thì backend không khởi động được
    "LOG_LEVEL": ({"DEBUG", "INFO", "WARNING", "ERROR"}, "DEBUG / INFO / WARNING / ERROR"),
    "LOG_TO_FILE": ({"0", "1"}, "0 hoặc 1"),
    "LOG_ACCESS": ({"api", "all", "off"}, "api / all / off"),
    "LOG_RETENTION_DAYS": (INT, "số nguyên"), "RETENTION_DAYS": (INT, "số nguyên"),
    "CHAT_RETENTION_DAYS": (INT, "số nguyên"), "OCR_CONCURRENCY": (INT, "số nguyên"), "OCR_PASSES": (INT, "số nguyên"),
}


def env_path() -> Path:
    """Cùng thứ tự với config.py: backend/.env, không có thì .env ở thư mục cha."""
    p = config.BACKEND_DIR / ".env"
    return p if p.exists() else config.BACKEND_DIR.parent / ".env"


def read(p: Path) -> tuple[list[str], str]:
    text = p.read_bytes().decode("utf-8-sig")  # không dùng read_text: nó đổi \r\n thành \n, mất kiểu xuống dòng gốc
    return text.splitlines(), "\r\n" if "\r\n" in text else "\n"


def write(p: Path, lines: list[str], nl: str) -> Path:
    stamp, n = f"{p.name}.bak-{datetime.now():%Y%m%d-%H%M%S}", 1
    bak = p.with_name(stamp)
    while bak.exists():  # sửa 2 lần trong 1 giây: không ghi đè bản sao lưu trước
        n += 1
        bak = p.with_name(f"{stamp}-{n}")
    bak.write_bytes(p.read_bytes())
    tmp = p.with_name(p.name + ".tmp")
    tmp.write_text(nl.join(lines) + nl, encoding="utf-8", newline="")  # UTF-8 không BOM, giữ kiểu xuống dòng cũ
    tmp.replace(p)  # ghi file tạm rồi đổi tên: lỗi giữa chừng không làm hỏng .env
    return bak


def unquote(v: str) -> str:
    v = v.strip()
    if len(v) >= 2 and v[0] == v[-1] and v[0] in "\"'":
        return v[1:-1].replace('\\"', '"').replace("\\\\", "\\") if v[0] == '"' else v[1:-1]
    return v.split(" #", 1)[0].strip()  # ghi chú cuối dòng


def quote(v: str) -> str:
    if v and not re.search(r"[\s#\"'\\]", v):
        return v
    return '"' + v.replace("\\", "\\\\").replace('"', '\\"') + '"'


def shown(name: str, value: str, show: bool) -> str:
    if SECRET.search(name) and not show:
        return f"(có, {len(value)} ký tự)" if value else "(trống)"
    return value if value else "(trống)"


def values(lines):
    return {m.group(1): unquote(m.group(2)) for line in lines if (m := LINE.match(line))}


def cmd_list(p, a):
    for name, v in values(read(p)[0]).items():
        print(f"{name} = {shown(name, v, a.show)}")


def cmd_get(p, a):
    vals = values(read(p)[0])
    if a.name not in vals:
        sys.exit(f"{a.name} chưa có trong {p.name} (backend dùng giá trị mặc định).")
    print(shown(a.name, vals[a.name], a.show))


def cmd_set(p, a):
    value = a.value
    if value is None:
        if not sys.stdin.isatty():
            sys.exit("Thiếu giá trị. Ghi: py scripts/env.py set TÊN GIÁ_TRỊ")
        value = getpass.getpass(f"Giá trị mới cho {a.name} (không hiện khi gõ): ")
        if value != getpass.getpass("Nhập lại lần nữa: "):
            sys.exit("Hai lần nhập không giống nhau, không sửa gì.")
    if "\n" in value or "\r" in value:
        sys.exit("Giá trị không được xuống dòng.")
    if a.name in CHECK:
        ok, hint = CHECK[a.name]
        if not (ok(value) if callable(ok) else value in ok):
            sys.exit(f"{a.name} chỉ nhận: {hint}. Không sửa gì.")
    if a.name == "AUTH_PASSWORD" and len(value) < 8:
        sys.exit("Mật khẩu đăng nhập phải từ 8 ký tự. Không sửa gì.")
    lines, nl = read(p)
    new, hit = f"{a.name}={quote(value)}", False
    for i, line in enumerate(lines):
        if (m := LINE.match(line)) and m.group(1) == a.name:
            lines[i], hit = new, True
    if not hit:
        lines.append(new)
    bak = write(p, lines, nl)
    print(f"Đã {'sửa' if hit else 'thêm'} {a.name} = {shown(a.name, value, False)} trong {p}")
    print(f"Bản sao lưu: {bak.name}. Khởi động lại backend để có tác dụng.")


def cmd_unset(p, a):
    lines, nl = read(p)
    keep = [x for x in lines if not ((m := LINE.match(x)) and m.group(1) == a.name)]
    if len(keep) == len(lines):
        sys.exit(f"{a.name} không có trong {p.name}, không sửa gì.")
    bak = write(p, keep, nl)
    print(f"Đã xóa {a.name} khỏi {p}. Bản sao lưu: {bak.name}. Khởi động lại backend để có tác dụng.")


def name_arg(s: str) -> str:
    if not NAME.match(s):
        raise argparse.ArgumentTypeError("tên biến chỉ gồm chữ IN HOA, số và dấu _, ví dụ LOG_LEVEL")
    return s


def main(argv=None):
    ap = argparse.ArgumentParser(description="Xem / sửa file .env của OCR Dashboard (cần tài khoản web).")
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("list", help="liệt kê các biến")
    s.add_argument("--show", action="store_true", help="hiện cả giá trị bí mật (KEY / PASSWORD / SECRET / TOKEN / ACCOUNT_ID / AUTH_USER)")
    s.set_defaults(fn=cmd_list)
    s = sub.add_parser("get", help="xem giá trị 1 biến")
    s.add_argument("name", type=name_arg)
    s.add_argument("--show", action="store_true", help="hiện cả giá trị bí mật")
    s.set_defaults(fn=cmd_get)
    s = sub.add_parser("set", help="đặt giá trị 1 biến (thêm mới nếu chưa có)")
    s.add_argument("name", type=name_arg)
    s.add_argument("value", nargs="?", help="bỏ trống để nhập ẩn (nên dùng cho mật khẩu / khóa API)")
    s.set_defaults(fn=cmd_set)
    s = sub.add_parser("unset", help="xóa dòng của 1 biến")
    s.add_argument("name", type=name_arg)
    s.set_defaults(fn=cmd_unset)
    args = ap.parse_args(argv)
    log_args = [args.cmd] + ([args.name] if hasattr(args, "name") else [])
    if args.cmd == "set":  # giá trị của biến bí mật không bao giờ vào log
        log_args.append("***" if SECRET.search(args.name) else "(nhập ẩn)" if args.value is None else args.value)
    terminal.start("env.py", log_args)
    p = env_path()
    if not p.exists():
        sys.exit(f"Không tìm thấy file .env ({config.BACKEND_DIR / '.env'} hoặc {p}).")
    args.fn(p, args)


if __name__ == "__main__":
    main()
