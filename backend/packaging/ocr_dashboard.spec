# PyInstaller spec: đóng gói backend + frontend + Python thành dist/OCRDashboard/OCRDashboard.exe
# Chạy qua packaging/build.bat (không gọi tay). KHÔNG gói .env, data/, ảnh upload, log: các thứ đó tạo lúc chạy.
from pathlib import Path

from PyInstaller.utils.hooks import collect_data_files, collect_submodules, copy_metadata

PACK = Path(SPECPATH).resolve()  # backend/packaging
BACKEND = PACK.parent
ROOT = BACKEND.parent

# Mọi file không phải .py trong backend/app (prompt .txt/.md/.yaml, abnormal_types.json, views.sql...), giữ nguyên
# đường dẫn tương đối để code đọc bằng Path(__file__).parent vẫn đúng.
datas = [
    (str(p), str(p.parent.relative_to(BACKEND)))
    for p in (BACKEND / "app").rglob("*")
    if p.is_file() and p.suffix not in (".py", ".pyc") and "__pycache__" not in p.parts
]
datas += [
    (str(ROOT / "frontend"), "frontend"),
    (str(BACKEND / ".env.example"), "."),  # mẫu để tạo .env lần chạy đầu (chỉ có tên biến, không có key)
]
if (ROOT / "docs" / "user-guide").is_dir():  # tài liệu hướng dẫn cho chatbot (nếu có)
    datas.append((str(ROOT / "docs" / "user-guide"), "docs/user-guide"))
datas += copy_metadata("apscheduler")  # APScheduler 3 tìm trigger "cron" qua entry point của gói
datas += collect_data_files("tzdata")  # Windows không có dữ liệu múi giờ: ZoneInfo("Asia/Ho_Chi_Minh") cần gói tzdata (+ hiddenimports)

# uvicorn import "app.main:app" bằng chuỗi nên PyInstaller không tự thấy -> liệt kê mọi module trong backend/app.
# Không dùng collect_submodules("app"): hàm đó chạy trước khi biết pathex nên không tìm ra package app.
APP_MODULES = [
    ".".join(p.relative_to(BACKEND).with_suffix("").parts).removesuffix(".__init__")
    for p in (BACKEND / "app").rglob("*.py")
    if "__pycache__" not in p.parts
]
hiddenimports = (
    APP_MODULES
    + collect_submodules("uvicorn")
    + collect_submodules("apscheduler")
    + collect_submodules("sqlglot")  # dialect được import lúc chạy
    + collect_submodules("tzdata")  # zoneinfo nạp tzdata gián tiếp, PyInstaller không tự thấy
    + ["logs", "dbshell", "env"]  # lệnh con: OCRDashboard.exe logs|db|env
)

a = Analysis(
    [str(BACKEND / "launcher.py")],
    pathex=[str(BACKEND), str(BACKEND / "scripts")],
    datas=datas,
    hiddenimports=hiddenimports,
    excludes=["pytest", "_pytest", "tkinter"],
    noarchive=False,
)
pyz = PYZ(a.pure)
exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="OCRDashboard",
    console=True,  # có cửa sổ console: thấy log, đóng cửa sổ = tắt web (giống start_backend.bat)
    upx=False,  # UPX hay bị antivirus báo nhầm
    icon=str(PACK / "icon.ico") if (PACK / "icon.ico").exists() else None,
)
coll = COLLECT(exe, a.binaries, a.datas, strip=False, upx=False, name="OCRDashboard")
