"""Điểm vào của bản đóng gói OCRDashboard.exe (PyInstaller, xem packaging/). Chạy từ source vẫn dùng uvicorn như cũ.

    OCRDashboard.exe              chạy web (lần đầu: tạo .env từ mẫu, mở Notepad để điền rồi thoát)
    OCRDashboard.exe config       mở .env bằng Notepad (chưa có thì tạo từ mẫu)
    OCRDashboard.exe logs ...     = py scripts/logs.py ...
    OCRDashboard.exe db ...       = py scripts/dbshell.py ...
    OCRDashboard.exe env ...      = py scripts/env.py ...

.env và data/ nằm ở %LOCALAPPDATA%\\OCRDashboard (config.APP_HOME), KHÔNG nằm trong thư mục cài:
gỡ hoặc cài bản mới không mất dữ liệu, và bộ cài không chứa key/mật khẩu nào.
Chạy thử từ source: cd backend && py launcher.py (dùng backend/.env và backend/data như bình thường).
"""
import os
import shutil
import socket
import subprocess
import sys
import threading
import time
import traceback
import urllib.request
import webbrowser
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent / "scripts"
sys.path.insert(0, str(SCRIPTS))  # để "import logs/dbshell/env" khi chạy từ source; bản đóng gói đã gói sẵn

from app import config  # noqa: E402  (đọc .env ngay khi import)

HOST = "127.0.0.1"  # chỉ nhận kết nối trong máy; người ngoài vào qua Cloudflare Tunnel
PORT = int(os.environ.get("PORT") or 8000)
TEMPLATE = config.RESOURCE_DIR / ".env.example" if config.FROZEN else config.BACKEND_DIR / ".env.example"
REQUIRED = {"AUTH_USER": "tên đăng nhập dashboard", "AUTH_PASSWORD": "mật khẩu đăng nhập dashboard"}
OCR_KEYS = ("CLOUDFLARE_API_KEY", "NVIDIA_API_KEY", "OPEN_ROUTER_API_KEY")


def pause():
    if config.FROZEN and interactive():
        input("\nNhấn Enter để đóng cửa sổ...")


def interactive() -> bool:
    """Người dùng mở từ shortcut/cửa sổ console. Chạy từ script/agent (stdin không phải bàn phím) thì không mở
    Notepad, không dừng chờ Enter."""
    return bool(sys.stdin) and sys.stdin.isatty()


def open_env():
    """Mở .env bằng Notepad khi có người ngồi trước máy; còn lại chỉ in đường dẫn."""
    if os.name == "nt" and interactive():
        subprocess.Popen(["notepad.exe", str(config.ENV_FILE)])
    else:
        print(f"Mở và sửa file: {config.ENV_FILE}")


def browser_enabled() -> bool:
    return (os.environ.get("OPEN_BROWSER") or "1") != "0"


def ensure_env() -> bool:
    """True nếu .env đã có. Chưa có: tạo từ mẫu, mở để điền, trả False (người dùng điền xong chạy lại)."""
    if config.ENV_FILE.exists():
        return True
    config.APP_HOME.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(TEMPLATE, config.ENV_FILE)
    print(f"Lần chạy đầu: đã tạo file cấu hình\n  {config.ENV_FILE}\n"
          "Điền API key và tài khoản đăng nhập (AUTH_USER, AUTH_PASSWORD), lưu lại rồi chạy OCR Dashboard lần nữa.")
    open_env()
    return False


def check_env() -> bool:
    missing = [f"  {k}  ({v})" for k, v in REQUIRED.items() if not (os.environ.get(k) or "").strip()]
    if missing:
        print(f"File {config.ENV_FILE} còn thiếu:\n" + "\n".join(missing) + "\nĐiền rồi lưu lại, sau đó chạy lại.")
        open_env()
        return False
    if not any((os.environ.get(k) or "").strip() for k in OCR_KEYS):
        print(f"Cảnh báo: chưa có API key OCR nào ({', '.join(OCR_KEYS)}): web vẫn chạy nhưng upload ảnh sẽ lỗi.")
    return True


def already_running() -> bool:
    try:
        with urllib.request.urlopen(f"http://{HOST}:{PORT}/api/system/health", timeout=2):
            return True
    except OSError:
        return False


def port_busy() -> bool:
    with socket.socket() as s:
        return s.connect_ex((HOST, PORT)) == 0


def open_browser_when_ready():
    url = f"http://localhost:{PORT}"
    for _ in range(120):  # đợi tối đa ~60 giây
        if already_running():
            print(f"\nOCR Dashboard đang chạy: {url}  (đóng cửa sổ này = tắt web)\n", flush=True)
            if browser_enabled():
                webbrowser.open(url)
            return
        time.sleep(0.5)


def serve():
    if not ensure_env() or not check_env():
        return pause()
    if port_busy():
        if already_running():
            print(f"OCR Dashboard đã chạy sẵn ở cửa sổ khác: mở http://localhost:{PORT}")
            if browser_enabled():
                webbrowser.open(f"http://localhost:{PORT}")
        else:
            print(f"Cổng {PORT} đang bị chương trình khác dùng. Tắt chương trình đó, hoặc đặt PORT=... trong .env "
                  "(nhớ sửa luôn cổng trong cấu hình Cloudflare Tunnel).")
        return pause()

    import uvicorn

    os.chdir(config.APP_HOME)  # DATABASE_URL / UPLOAD_DIR dạng ./data/... trong .env tính từ đây
    config.DATA_DIR.mkdir(parents=True, exist_ok=True)
    print(f"Cấu hình: {config.ENV_FILE}\nDữ liệu:  {config.DATA_DIR}", flush=True)
    threading.Thread(target=open_browser_when_ready, daemon=True).start()
    # truyền chuỗi "app.main:app" (không import trước) để uvicorn cấu hình logging trước khi import app,
    # app/logging_setup.py mới gắn được file log vào logger của uvicorn
    uvicorn.run("app.main:app", host=HOST, port=PORT)


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    cmd, args = (sys.argv[1], sys.argv[2:]) if len(sys.argv) > 1 else ("serve", [])
    if config.APP_HOME.is_dir():  # .env mẫu ghi DATABASE_URL=sqlite:///./data/ocr.db: mọi lệnh tính từ APP_HOME,
        os.chdir(config.APP_HOME)  # gõ "OCRDashboard.exe db info" ở thư mục nào cũng mở đúng DB
    try:
        if cmd == "serve":
            serve()
        elif cmd == "config":
            ensure_env() and open_env()
        elif cmd in ("logs", "db", "env"):
            import importlib

            importlib.import_module({"logs": "logs", "db": "dbshell", "env": "env"}[cmd]).main(args)
        else:
            print(__doc__)
    except KeyboardInterrupt:
        pass
    except SystemExit:
        raise
    except Exception:  # cửa sổ console không tự đóng mất, để còn đọc/chụp lỗi
        traceback.print_exc()
        print(f"\nLog chi tiết: {config.LOG_DIR}")
        pause()
        sys.exit(1)


if __name__ == "__main__":
    main()
