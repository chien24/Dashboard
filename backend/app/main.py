"""App FastAPI: API + phục vụ frontend + ảnh upload + worker OCR + lịch xóa dữ liệu cũ.

Chạy:  cd backend && uvicorn app.main:app --reload   rồi mở http://localhost:8000
"""
import logging
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles

from app import config
from app.api import auth, dashboard, reports, system, upload
from app.db import SessionLocal, engine, init_db
from app.ocr.router import reset_provider_disabled_on_start
from app.services import retention, worker

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(name)s %(levelname)s %(message)s")
FRONTEND = Path(__file__).resolve().parents[2] / "frontend"


def _cleanup():
    with SessionLocal() as db:
        retention.cleanup(db)


@asynccontextmanager
async def lifespan(app: FastAPI):
    from apscheduler.schedulers.background import BackgroundScheduler

    init_db()
    config.UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    reset_provider_disabled_on_start()
    _cleanup()
    worker.start()
    sched = BackgroundScheduler(timezone=config.TIMEZONE)
    sched.add_job(_cleanup, "cron", hour=2, minute=0)
    sched.add_job(lambda: retention.vacuum(engine), "cron", day_of_week="sun", hour=3, minute=0)
    sched.start()
    yield
    sched.shutdown(wait=False)


app = FastAPI(title="OCR Dashboard CNKT3", lifespan=lifespan)
for r in (auth.router, upload.router, reports.router, dashboard.router, system.router):
    app.include_router(r)
PRIVATE = ("/api/", "/uploads/", "/docs", "/redoc", "/openapi.json")  # Swagger cũng cần đăng nhập: lộ sơ đồ API
PUBLIC = ("/api/auth/", "/api/system/health")


@app.middleware("http")
async def require_login(request, call_next):
    """Chưa đăng nhập: chặn mọi API dữ liệu và ảnh đã upload; HTML/CSS/JS vẫn tải được (trang hiện ô trống)."""
    p = request.url.path
    if not p.startswith(PRIVATE) or p.startswith(PUBLIC):
        return await call_next(request)
    if not auth.is_logged_in(request):
        return JSONResponse({"detail": "Cần đăng nhập"}, status_code=401)
    resp = await call_next(request)
    # private: proxy/CDN (Vercel, Cloudflare) không lưu; no-cache: trình duyệt hỏi lại server mỗi lần, đăng xuất rồi không mở lại được từ cache
    resp.headers["Cache-Control"] = "private, no-cache"
    return resp


@app.middleware("http")
async def security_headers(request, call_next):
    """nosniff: trình duyệt không đoán lại kiểu file (ảnh upload không bị chạy như HTML); DENY: trang không bị nhúng vào iframe lạ."""
    resp = await call_next(request)
    resp.headers.setdefault("X-Content-Type-Options", "nosniff")
    resp.headers.setdefault("X-Frame-Options", "DENY")
    resp.headers.setdefault("Referrer-Policy", "same-origin")
    return resp

config.UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=config.UPLOAD_DIR), name="uploads")


@app.get("/", include_in_schema=False)
def home():
    return RedirectResponse("/html/index.html")


class FrontendFiles(StaticFiles):
    """no-cache: trình duyệt luôn hỏi lại server (file không đổi thì chỉ nhận 304), nên sửa HTML/CSS/JS là thấy ngay."""

    def file_response(self, *args, **kwargs):
        resp = super().file_response(*args, **kwargs)
        resp.headers["Cache-Control"] = "no-cache"
        return resp


app.mount("/", FrontendFiles(directory=FRONTEND), name="frontend")  # mount cuối để không che /api
