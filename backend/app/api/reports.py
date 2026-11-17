"""CRUD report: danh sách, chi tiết, sửa tay, xóa, OCR lại."""
from datetime import date
from pathlib import Path

from fastapi import APIRouter, Body, Depends, HTTPException, Query
from sqlalchemy import func, select

from app import config
from app.api.upload import new_job
from app.db import get_db
from app.models import DmwcsBcr, DmwcsCapacityDaily, DmwcsSorted, Report, ScadaSummary
from app.ocr.providers.base import BadOutput, validate_output
from app.schemas import SCHEMAS
from app.services.ingest import write_details
from app.services.normalize import abnormal_type, day_chuyen_key, report_times
from app.services.validate import VALIDATORS

router = APIRouter(prefix="/api/reports", tags=["reports"])
HE = {"ht1": ["scada"], "ht2": ["dmwcs_sorted", "dmwcs_capacity", "dmwcs_bcr_rate"]}


def dang_dung(db, ids: list[int]) -> set[int]:
    """Report còn dòng chi tiết = đang hiện trên dashboard; bị ảnh mới hơn ghi đè thì mất dòng chi tiết."""
    out = set()
    for t in (ScadaSummary, DmwcsSorted, DmwcsBcr, DmwcsCapacityDaily):
        out |= set(db.scalars(select(t.report_id).where(t.report_id.in_(ids))))
    return out


def image_url(rep: Report) -> str | None:
    if not rep.upload:
        return None
    try:
        return "/uploads/" + Path(rep.upload.stored_path).resolve().relative_to(config.UPLOAD_DIR.resolve()).as_posix()
    except ValueError:
        return None


def summary(rep: Report) -> dict:
    return {"id": rep.id, "loai": rep.loai, "file": rep.source_name, "status": rep.status, "report_date": rep.report_date,
            "thoi_gian_tu": rep.thoi_gian_tu, "thoi_gian_den": rep.thoi_gian_den, "provider": rep.provider,
            "model": rep.model, "model_lan_2": rep.model_lan_2, "so_canh_bao": len(rep.canh_bao or []),
            "upload_id": rep.upload_id, "created_at": rep.created_at}


def get_or_404(db, rid: int) -> Report:
    rep = db.get(Report, rid)
    if not rep:
        raise HTTPException(404, "Không có report này")
    return rep


@router.get("")
def list_reports(loai: str | None = None, from_: date | None = Query(None, alias="from"), to: date | None = None, status: str | None = None,
                 day_chuyen: str | None = None, q: str | None = None, he: str | None = None,
                 limit: int = 50, offset: int = 0, db=Depends(get_db)):
    """Lọc theo loai hoặc he (ht1 = SCADA, ht2 = DMWCS), khoảng ngày (from_/to theo report_date), status, day_chuyen,
    q = một phần tên file (không phân biệt hoa thường); phân trang limit/offset."""
    text, q = q, select(Report)
    if loai:
        q = q.where(Report.loai == loai)
    if he:
        if he not in HE:
            raise HTTPException(400, f"he phải là một trong {list(HE)}")
        q = q.where(Report.loai.in_(HE[he]))
    if text and text.strip():
        q = q.where(func.lower(Report.source_name).contains(text.strip().lower(), autoescape=True))
    if from_:
        q = q.where(Report.report_date >= from_)
    if to:
        q = q.where(Report.report_date <= to)
    if status:
        q = q.where(Report.status == status)
    if day_chuyen:
        q = q.where(Report.id.in_(select(ScadaSummary.report_id).where(ScadaSummary.day_chuyen_key == day_chuyen_key(day_chuyen))))
    total = db.scalar(select(func.count()).select_from(q.subquery()))
    rows = db.scalars(q.order_by(Report.report_date.desc(), Report.id.desc()).limit(min(limit, 500)).offset(offset)).all()
    active = dang_dung(db, [r.id for r in rows])
    return {"total": total, "items": [{**summary(r), "dang_dung": r.id in active,
                                       "day_chuyen": (r.data or {}).get("day_chuyen")} for r in rows]}


@router.get("/{rid}")
def get_report(rid: int, db=Depends(get_db)):
    rep = get_or_404(db, rid)
    out = {**summary(rep), "data": rep.data, "canh_bao": rep.canh_bao, "raw_json_1": rep.raw_json_1,
           "raw_json_2": rep.raw_json_2, "attempts": rep.attempts, "image_url": image_url(rep),
           "dang_dung": rep.id in dang_dung(db, [rep.id])}
    if rep.loai == "scada":  # tên loại bất thường đã chuẩn hóa (abnormal_types.json), để hiển thị cạnh nhãn OCR gốc
        out["bat_thuong"] = [{**p, **dict(zip(("loai_key", "loai_vi"), abnormal_type(p["loai"])))}
                             for p in (rep.data or {}).get("phan_bo_bat_thuong", [])]
    return out


@router.put("/{rid}")
def edit_report(rid: int, data: dict = Body(...), db=Depends(get_db)):
    """Sửa tay khi OCR sai: validate schema + số học lại, status = da_sua_tay. raw_json giữ nguyên."""
    rep = get_or_404(db, rid)
    data = {k: v for k, v in data.items() if k != "canh_bao_ocr"}
    try:
        clean = validate_output(SCHEMAS[rep.loai], {**data, "canh_bao_ocr": []})
        report_times(rep.loai, clean)
    except (BadOutput, ValueError) as e:
        raise HTTPException(422, str(e))
    clean.pop("canh_bao_ocr")
    rep.data = clean
    rep.thoi_gian_tu, rep.thoi_gian_den, rep.report_date = report_times(rep.loai, clean)
    rep.canh_bao = ["Đã sửa tay"] + VALIDATORS[rep.loai](clean)
    rep.status = "da_sua_tay"
    write_details(db, rep)
    db.commit()
    return get_report(rid, db)


@router.delete("/{rid}")
def delete_report(rid: int, db=Depends(get_db)):
    db.delete(get_or_404(db, rid))  # ON DELETE CASCADE xóa dòng chi tiết
    db.commit()
    return {"deleted": rid}


@router.post("/{rid}/reocr")
def reocr(rid: int, provider: str | None = Body(None, embed=True), model: str | None = Body(None, embed=True),
          db=Depends(get_db)):
    """OCR lại ảnh của report (tùy chọn chỉ định provider/model). Kết quả là report mới, ghi đè dữ liệu dashboard."""
    rep = get_or_404(db, rid)
    if not rep.upload_id:
        raise HTTPException(400, "Report import từ JSON, không có ảnh gốc để OCR lại")
    if provider and provider not in config.KEYS:
        raise HTTPException(400, f"provider phải là một trong {list(config.KEYS)}")
    job = new_job(db, rep.upload_id, rep.loai, provider, model)
    return {"job_id": job.id}
