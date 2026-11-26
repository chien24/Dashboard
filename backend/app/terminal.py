"""Cổng vào cho lệnh terminal (scripts/logs.py, scripts/dbshell.py): phải nhập đúng tài khoản web (AUTH_USER / AUTH_PASSWORD)
mới chạy. Gõ tay: hỏi tên + mật khẩu (mật khẩu không hiện). Chạy qua pipe / tự động: đọc 2 dòng từ stdin (tên, mật khẩu).
Mỗi lần dùng (đúng / sai) ghi vào log của backend để biết ai đã xem gì. Không bao giờ ghi tên/mật khẩu đã nhập."""
import getpass
import logging
import secrets
import sys
import time

from app import config, logging_setup

log = logging.getLogger("terminal")
TRIES = 3


def _ok(user: str, password: str) -> bool:
    return secrets.compare_digest(user.encode(), config.AUTH_USER.encode()) & \
        secrets.compare_digest(password.encode(), config.AUTH_PASSWORD.encode())


def _ask(tty: bool) -> tuple[str, str]:
    if tty:
        return input("Tên đăng nhập: "), getpass.getpass("Mật khẩu: ")
    return sys.stdin.readline().rstrip("\r\n"), sys.stdin.readline().rstrip("\r\n")


def start(tool: str, log_args: list[str] | None = None) -> None:
    """Gọi đầu mỗi script. Sai TRIES lần (gõ tay) hoặc 1 lần (pipe) -> thoát mã 1.
    log_args: đối số ghi vào log (mặc định sys.argv[1:]); script có đối số bí mật thì truyền bản đã che."""
    for s in (sys.stdout, sys.stderr):  # pipe / chuyển hướng trên Windows mặc định cp1252: tiếng Việt thành '?'
        if hasattr(s, "reconfigure"):
            s.reconfigure(encoding="utf-8", errors="replace")
    if hasattr(sys.stdin, "reconfigure") and not sys.stdin.isatty():
        sys.stdin.reconfigure(encoding="utf-8-sig")  # PowerShell pipe sang lệnh ngoài kèm BOM UTF-8: bỏ BOM khỏi tên đăng nhập
    logging_setup.setup(console=False)
    if not (config.AUTH_USER and config.AUTH_PASSWORD):
        sys.exit("Chưa đặt AUTH_USER / AUTH_PASSWORD trong .env nên không cho chạy lệnh này.")
    tty = sys.stdin.isatty()
    tries = TRIES if tty else 1
    for i in range(1, tries + 1):
        if _ok(*_ask(tty)):
            log.info("Terminal %s: đăng nhập đúng, chạy: %s", tool,
                     " ".join(sys.argv[1:] if log_args is None else log_args)[:300])
            return
        log.warning("Terminal %s: đăng nhập sai (lần %d/%d)", tool, i, tries)
        time.sleep(1)  # làm chậm việc dò mật khẩu
        print("Sai tài khoản hoặc mật khẩu.", file=sys.stderr)
    sys.exit(1)
