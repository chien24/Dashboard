"""Hàng đợi OCR: OCR_CONCURRENCY luồng đọc job theo thứ tự (free tier giới hạn rate nên mặc định 1)."""
import logging
import queue
import threading
from pathlib import Path

from sqlalchemy import select

from app import config
from app.db import SessionLocal
from app.models import Job, Upload, now
from app.ocr import pipeline
from app.services.ingest import ingest

log = logging.getLogger("worker")
_q: queue.Queue[int] = queue.Queue()
_started = False


def enqueue(job_id: int):
    _q.put(job_id)


def _set(job_id: int, **kw):
    with SessionLocal() as db:
        job = db.get(Job, job_id)
        for k, v in kw.items():
            setattr(job, k, v)
        db.commit()


def run_job(job_id: int):
    with SessionLocal() as db:
        job = db.get(Job, job_id)
        if not job or job.status != "pending":
            return
        up = db.get(Upload, job.upload_id)
        job.status = "running"
        db.commit()
        loai, only_p, only_m, path, name = job.loai_hint, job.only_provider, job.only_model, up.stored_path, up.original_name
    try:
        r = pipeline.process(Path(path), loai, only_p, only_m, on_progress=lambda s: _set(job_id, progress=s))
        with SessionLocal() as db:
            rep = ingest(db, r, upload_id=up.id, source_name=name)
            rid = rep.id
        _set(job_id, status="done", report_id=rid, progress=f"xong · {r['provider']}/{r['model']}", finished_at=now())
    except Exception as e:  # lỗi 1 job không được làm chết luồng worker
        log.exception("Job %s lỗi", job_id)
        _set(job_id, status="failed", error=f"{type(e).__name__}: {e}"[:2000], finished_at=now())


def _loop():
    while True:
        run_job(_q.get())


def start():
    """Khởi động worker; job đang dở khi app tắt (running) được chạy lại."""
    global _started
    if _started:
        return
    _started = True
    with SessionLocal() as db:
        for job in db.scalars(select(Job).where(Job.status.in_(["pending", "running"])).order_by(Job.id)):
            job.status = "pending"
            _q.put(job.id)
        db.commit()
    for _ in range(max(1, config.OCR_CONCURRENCY)):
        threading.Thread(target=_loop, daemon=True).start()
