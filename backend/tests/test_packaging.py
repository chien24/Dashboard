"""Bản đóng gói (launcher.py + app/config.py khi chạy từ OCRDashboard.exe). Không cần PyInstaller để chạy test này."""
import os
import re
import subprocess
import sys
from pathlib import Path

BACKEND = Path(__file__).resolve().parents[1]


def run_py(code_or_args: list[str], home: Path, extra_env: dict | None = None) -> subprocess.CompletedProcess:
    env = {"PATH": os.environ.get("PATH", ""), "OCR_DASHBOARD_HOME": str(home), "PYTHONIOENCODING": "utf-8",
           "OPEN_BROWSER": "0", **(extra_env or {})}
    if os.name == "nt":
        env["SYSTEMROOT"] = os.environ.get("SYSTEMROOT", "")
    return subprocess.run([sys.executable, *code_or_args], cwd=BACKEND, env=env, capture_output=True, text=True,
                          encoding="utf-8", timeout=60, stdin=subprocess.DEVNULL)


def test_frozen_paths(tmp_path):
    """Giả lập chạy từ exe: .env và data ở LOCALAPPDATA\\OCRDashboard, tài nguyên ở sys._MEIPASS."""
    code = ("import sys; sys.frozen = True; sys._MEIPASS = r'%s'\n"
            "from app import config as c\n"
            "print(c.APP_HOME); print(c.ENV_FILE); print(c.RESOURCE_DIR); print(c.DATABASE_URL); print(c.UPLOAD_DIR)"
            % (tmp_path / "meipass"))
    # PYTHONIOENCODING: thư mục tạm có thể chứa chữ có dấu (user "Chiến"), pipe mặc định cp1252 thì print lỗi
    env = {"PATH": os.environ.get("PATH", ""), "LOCALAPPDATA": str(tmp_path / "local"), "PYTHONIOENCODING": "utf-8"}
    if os.name == "nt":
        env["SYSTEMROOT"] = os.environ.get("SYSTEMROOT", "")
    r = subprocess.run([sys.executable, "-c", code], cwd=BACKEND, env=env, capture_output=True, text=True,
                       encoding="utf-8", timeout=60)
    assert r.returncode == 0, r.stderr
    out = r.stdout.splitlines()
    home = tmp_path / "local" / "OCRDashboard"
    assert out[0] == str(home)
    assert out[1] == str(home / ".env")
    assert out[2] == str(tmp_path / "meipass")
    assert out[3] == f"sqlite:///{home / 'data' / 'ocr.db'}"
    assert out[4] == str(home / "data" / "uploads")


def test_source_paths_unchanged():
    """Chạy từ source vẫn dùng backend/.env và backend/data như trước."""
    from app import config

    assert not config.FROZEN
    assert config.ENV_FILE == BACKEND / ".env"
    assert config.DATA_DIR == BACKEND / "data"
    assert config.RESOURCE_DIR == BACKEND.parent


def test_first_run_creates_only_env(tmp_path):
    home = tmp_path / "home"
    r = run_py(["launcher.py"], home)
    assert r.returncode == 0, r.stderr
    assert "Lần chạy đầu" in r.stdout
    assert (home / ".env").read_text(encoding="utf-8") == (BACKEND / ".env.example").read_text(encoding="utf-8")
    assert sorted(p.name for p in home.iterdir()) == [".env"]  # chưa tạo data/


def test_missing_login_does_not_start(tmp_path):
    home = tmp_path / "home"
    home.mkdir()
    (home / ".env").write_text("AUTH_USER=admin\nAUTH_PASSWORD=\n", encoding="utf-8")
    r = run_py(["launcher.py"], home)
    assert "AUTH_PASSWORD" in r.stdout and "còn thiếu" in r.stdout
    assert not (home / "data").exists()


def test_config_command_keeps_existing_env(tmp_path):
    home = tmp_path / "home"
    home.mkdir()
    (home / ".env").write_text("AUTH_USER=giu-nguyen\n", encoding="utf-8")
    run_py(["launcher.py", "config"], home)
    assert (home / ".env").read_text(encoding="utf-8") == "AUTH_USER=giu-nguyen\n"


def test_env_example_has_no_secret_values():
    """.env.example được gói vào bộ cài: không bao giờ được chứa key/mật khẩu thật."""
    secret = re.compile(r"KEY|PASSWORD|SECRET|TOKEN|ACCOUNT_ID|AUTH_USER")
    names = set()
    for line in (BACKEND / ".env.example").read_text(encoding="utf-8").splitlines():
        m = re.match(r"^([A-Z_][A-Z0-9_]*)=(.*)$", line)
        if m:
            names.add(m.group(1))
            if secret.search(m.group(1)):
                assert m.group(2).strip() == "", f"{m.group(1)} trong .env.example phải để trống"
    for need in ("AUTH_USER", "AUTH_PASSWORD", "SESSION_SECRET", "CLOUDFLARE_ACCOUNT_ID", "CLOUDFLARE_API_KEY",
                 "NVIDIA_API_KEY", "OPEN_ROUTER_API_KEY", "GROQ_API_KEY"):
        assert need in names, f".env.example thiếu {need}"
