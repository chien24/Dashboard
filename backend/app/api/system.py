"""Health, trạng thái provider, retention thủ công."""
from fastapi import APIRouter, Depends
from sqlalchemy import text

from app.db import get_db
from app.ocr import router as ocr_router
from app.services.retention import cleanup

router = APIRouter(prefix="/api/system", tags=["system"])


@router.get("/health")
def health(db=Depends(get_db)):
    db.execute(text("SELECT 1"))
    return {"ok": True}


@router.get("/providers")
def providers():
    """Trạng thái từng provider/model: active / cooldown / disabled / no_key."""
    return ocr_router.provider_states()


@router.post("/providers/reset")
def providers_reset(provider: str | None = None):
    ocr_router.reset(provider)
    return ocr_router.provider_states()


@router.post("/cleanup")
def run_cleanup(dry_run: bool = True, db=Depends(get_db)):
    """Xóa dữ liệu cũ hơn RETENTION_DAYS. Mặc định dry_run=true: chỉ liệt kê."""
    return cleanup(db, dry_run=dry_run)
