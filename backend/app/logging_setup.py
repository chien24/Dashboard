"""Log ra console + file theo ngày (LOG_DIR/backend-YYYY-MM-DD.log, UTF-8), xóa file cũ quá LOG_RETENTION_DAYS ngày.
Gắn cả vào logger của uvicorn (uvicorn tự cấu hình trước khi import app, không propagate lên root)."""
import logging
from datetime import timedelta

from app import config
from app.models import now

FMT = logging.Formatter("%(asctime)s %(levelname)s %(name)s: %(message)s", "%Y-%m-%d %H:%M:%S")
log = logging.getLogger("app")


def log_file(day=None):
    return config.LOG_DIR / f"backend-{(day or now().date()).isoformat()}.log"


class DailyFile(logging.FileHandler):
    """Sang ngày mới thì mở file mới và dọn file quá hạn (tên file theo ngày để logs.py lọc theo ngày dễ)."""

    def __init__(self):
        config.LOG_DIR.mkdir(parents=True, exist_ok=True)
        self.day = now().date()
        super().__init__(log_file(self.day), encoding="utf-8")
        self.cleanup()

    def emit(self, record):
        if (d := now().date()) != self.day:
            self.acquire()
            try:
                self.close()
                self.day, self.baseFilename = d, str(log_file(d).resolve())
                self.stream = self._open()
            finally:
                self.release()
            self.cleanup()
        super().emit(record)

    def cleanup(self):
        cut = log_file(self.day - timedelta(days=config.LOG_RETENTION_DAYS)).name
        for p in config.LOG_DIR.glob("backend-*.log"):
            if p.name < cut:  # tên chứa ngày ISO: so chuỗi = so ngày
                p.unlink(missing_ok=True)


class ApiOnly(logging.Filter):
    """LOG_ACCESS=api: chỉ giữ dòng truy cập /api/ (bỏ HTML/CSS/JS/ảnh cho log gọn). args uvicorn: (ip, method, path, ...)."""

    def filter(self, record):
        args = record.args if isinstance(record.args, tuple) else ()
        return len(args) > 2 and str(args[2]).startswith("/api/")


def setup(console: bool = True):
    """console=False: lệnh terminal (scripts/) chỉ ghi file để lưu vết ai đã dùng, không in log ra màn hình."""
    root = logging.getLogger()
    root.setLevel(config.LOG_LEVEL)
    if not any(getattr(h, "_ocr", False) for h in root.handlers):  # gọi lại (reload, test) không gắn handler 2 lần
        handlers = [logging.StreamHandler()] if console else []
        if config.LOG_TO_FILE:
            handlers.append(DailyFile())
        for h in handlers:
            h._ocr = True
            h.setFormatter(FMT)
            root.addHandler(h)
        file_h = handlers[-1] if config.LOG_TO_FILE else None
        if file_h and console:  # uvicorn có handler console riêng, propagate=False: chỉ thêm file (uvicorn.error đẩy lên "uvicorn")
            for name in ("uvicorn", "uvicorn.access"):
                if not (lg := logging.getLogger(name)).propagate:
                    lg.addHandler(file_h)
            log.info("Ghi log vào %s", file_h.baseFilename)
    if config.LOG_LEVEL != "DEBUG":  # thư viện HTTP ghi mỗi request kèm URL (có account ID Cloudflare): chỉ giữ cảnh báo/lỗi
        for name in ("httpx", "httpx2", "httpcore"):
            logging.getLogger(name).setLevel(logging.WARNING)
    access = logging.getLogger("uvicorn.access")
    access.disabled = config.LOG_ACCESS == "off"
    if config.LOG_ACCESS == "api" and not any(isinstance(f, ApiOnly) for f in access.filters):
        access.addFilter(ApiOnly())
