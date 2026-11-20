"""Xóa dữ liệu cũ hơn RETENTION_DAYS (mặc định 35 ngày). dry_run=True: chỉ liệt kê, không xóa."""
import logging
from datetime import timedelta
from pathlib import Path

from sqlalchemy import delete, select, text

from app import config
from app.models import ChatConversation, DmwcsCapacityDaily, Job, Report, Upload, now

log = logging.getLogger("retention")


def cleanup(db, dry_run: bool = False) -> dict:
    cutoff = now().date() - timedelta(days=config.RETENTION_DAYS)
    reports = db.scalars(select(Report).where(Report.report_date < cutoff)).all()
    caps = db.scalars(select(DmwcsCapacityDaily).where(DmwcsCapacityDaily.ngay < cutoff)).all()
    jobs = db.scalars(select(Job).where(Job.created_at < now() - timedelta(days=config.RETENTION_DAYS))).all()
    # log chatbot có kết quả truy vấn = dữ liệu vận hành, xóa cùng hạn
    convs = db.scalars(select(ChatConversation.id).where(
        ChatConversation.updated_at < now() - timedelta(days=config.RETENTION_DAYS))).all()
    gone = {r.id for r in reports}
    # upload không còn report nào sau khi xóa (và không còn job đang chờ)
    uploads = [u for u in db.scalars(select(Upload)).all()
               if all(r.id in gone for r in u.reports) and (u.reports or u.uploaded_at.date() < cutoff)]
    out = {"cutoff": str(cutoff), "dry_run": dry_run,
           "reports": [{"id": r.id, "loai": r.loai, "report_date": str(r.report_date), "file": r.source_name} for r in reports],
           "capacity_days": [str(c.ngay) for c in caps],
           "uploads": [{"id": u.id, "file": u.original_name, "path": u.stored_path} for u in uploads],
           "jobs": len(jobs), "chat_conversations": len(convs)}
    if dry_run:
        return out
    files = 0
    for u in uploads:
        p = Path(u.stored_path)
        if p.exists():
            p.unlink()
            files += 1
    db.execute(delete(DmwcsCapacityDaily).where(DmwcsCapacityDaily.ngay < cutoff))
    db.execute(delete(Job).where(Job.id.in_([j.id for j in jobs])))
    db.execute(delete(Report).where(Report.id.in_(gone)))  # ON DELETE CASCADE sang bảng chi tiết
    db.execute(delete(Upload).where(Upload.id.in_([u.id for u in uploads])))
    db.execute(delete(ChatConversation).where(ChatConversation.id.in_(convs)))  # CASCADE sang chat_messages, chat_feedback
    db.commit()
    if db.bind.dialect.name == "sqlite":
        db.execute(text("PRAGMA optimize"))
    out["files_deleted"] = files
    log.info("Retention: xóa %d report, %d ngày capacity, %d upload (%d file), %d job, %d hội thoại chat",
             len(reports), len(caps), len(uploads), files, len(jobs), len(convs))
    return out


def vacuum(engine):
    if engine.dialect.name == "sqlite":
        with engine.connect().execution_options(isolation_level="AUTOCOMMIT") as c:  # VACUUM không chạy trong transaction
            c.exec_driver_sql("VACUUM")
