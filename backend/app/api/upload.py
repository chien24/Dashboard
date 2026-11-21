"""POST /api/upload (nhiều ảnh), GET /api/jobs/{id}."""
import hashlib
from pathlib import Path

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from app import config
from app.db import get_db
from app.models import Job, Report, Upload, now
from app.schemas import LOAI
from app.services import worker

router = APIRouter(prefix="/api", tags=["upload"])
EXT = {".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".png": "image/png", ".webp": "image/webp"}
MAX_PIXELS = 50_000_000  # ảnh chụp màn hình 4K mới ~8 MP; chặn ảnh nén nhỏ nhưng giải mã ra hàng trăm MB RAM


def image_info(path: Path) -> tuple[int, int]:
    """Kiểm tra file đúng là ảnh (không tin đuôi file) và lấy kích thước."""
    from PIL import Image

    try:
        with Image.open(path) as im:
            im.verify()
        with Image.open(path) as im:
            if im.width * im.height > MAX_PIXELS:
                raise ValueError("quá nhiều điểm ảnh")
            im.load()  # giải mã hết: verify() không phát hiện ảnh bị cắt dở, ảnh đó lọt vào OCR rồi lỗi ở mọi provider
            return im.size
    except Exception:
        raise HTTPException(400, f"File không phải ảnh hợp lệ hoặc bị hỏng: {path.name}")


def new_job(db, upload_id: int, loai: str | None, only_provider=None, only_model=None) -> Job:
    job = Job(upload_id=upload_id, loai_hint=loai, only_provider=only_provider, only_model=only_model, status="pending")
    db.add(job)
    db.commit()
    worker.enqueue(job.id)
    return job


@router.post("/upload")
async def upload(files: list[UploadFile] = File(...), loai: str | None = Form(None), force: bool = Form(False),
                 db=Depends(get_db)):
    """Nhận nhiều ảnh, trả [{job_id, upload_id, duplicate, report_id}] ngay; OCR chạy nền theo hàng đợi.
    Ảnh trùng (cùng sha256) không OCR lại, trừ khi force=true."""
    loai = loai or None
    if loai and loai not in LOAI:
        raise HTTPException(400, f"loai phải là một trong {LOAI}")
    out = []
    limit = config.MAX_UPLOAD_MB * 1024 * 1024

    def duplicate(name, up):
        rep = db.scalar(select(Report).where(Report.upload_id == up.id).order_by(Report.id.desc()))
        job = db.scalar(select(Job).where(Job.upload_id == up.id).order_by(Job.id.desc()))
        return {"file": name, "upload_id": up.id, "duplicate": True,
                "job_id": job.id if job else None, "report_id": rep.id if rep else None}

    for f in files:
        ext = Path(f.filename or "").suffix.lower()
        if ext not in EXT:
            raise HTTPException(400, f"Chỉ nhận ảnh {', '.join(EXT)}: {f.filename}")
        if (f.size or 0) > limit:  # chặn trước khi đọc cả file vào RAM
            raise HTTPException(413, f"{f.filename} lớn hơn {config.MAX_UPLOAD_MB} MB")
        body = await f.read()
        if len(body) > limit:
            raise HTTPException(413, f"{f.filename} lớn hơn {config.MAX_UPLOAD_MB} MB")
        sha = hashlib.sha256(body).hexdigest()
        up = db.scalar(select(Upload).where(Upload.sha256 == sha))
        if up and not Path(up.stored_path).exists():  # lần trước OCR thất bại nên file đã bị xóa: ghi lại rồi OCR như ảnh mới
            Path(up.stored_path).parent.mkdir(parents=True, exist_ok=True)
            Path(up.stored_path).write_bytes(body)
        elif up and not force:
            out.append(duplicate(f.filename, up))
            continue
        if not up:
            d = config.UPLOAD_DIR / now().strftime("%Y/%m/%d")
            d.mkdir(parents=True, exist_ok=True)
            path = d / f"{sha}{ext}"
            path.write_bytes(body)
            try:
                w, h = image_info(path)
            except HTTPException:
                path.unlink(missing_ok=True)
                raise
            up = Upload(original_name=f.filename, stored_path=str(path), sha256=sha, mime=EXT[ext],
                        size_bytes=len(body), width=w, height=h)
            db.add(up)
            try:
                db.commit()
            except IntegrityError:  # request khác vừa ghi cùng ảnh (sha256 unique): coi như ảnh trùng, giữ file (cùng tên, cùng nội dung)
                db.rollback()
                out.append(duplicate(f.filename, db.scalar(select(Upload).where(Upload.sha256 == sha))))
                continue
        job = new_job(db, up.id, loai)
        out.append({"file": f.filename, "upload_id": up.id, "duplicate": False, "job_id": job.id, "report_id": None})
    return out


@router.get("/jobs/{job_id}")
def get_job(job_id: int, db=Depends(get_db)):
    job = db.get(Job, job_id)
    if not job:
        raise HTTPException(404, "Không có job này")
    return {"id": job.id, "upload_id": job.upload_id, "status": job.status, "progress": job.progress,
            "error": job.error, "report_id": job.report_id, "loai_hint": job.loai_hint,
            "created_at": job.created_at, "finished_at": job.finished_at}
