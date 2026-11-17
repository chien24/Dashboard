"""Dữ liệu cho chart. Bản ghi trả về giữ đúng dạng JSON OCR cũ (thêm report_id, status, khóa chuẩn hóa)
để frontend dùng lại logic của HTML mẫu. Chỉ trả report đang "giữ khóa" (đã ghi đè thì bản cũ không hiện)."""
from collections import defaultdict
from datetime import date, datetime

from fastapi import APIRouter, Depends, Query
from sqlalchemy import select

from app.db import get_db
from app.models import DmwcsBcr, DmwcsCapacityDaily, DmwcsSorted, Report, ScadaAbnormal, ScadaSummary
from app.services.normalize import day_chuyen_key

router = APIRouter(prefix="/api/dashboard", tags=["dashboard"])


def fmt(v):
    return v.isoformat(sep=" ") if isinstance(v, datetime) else (v.isoformat() if isinstance(v, date) else v)


def meta(r: Report) -> dict:
    return {"report_id": r.id, "file": r.source_name, "loai": r.loai, "status": r.status, "model": r.model,
            "model_lan_2": r.model_lan_2, "canh_bao": r.canh_bao or [],
            "thoi_gian_tu": fmt(r.thoi_gian_tu), "thoi_gian_den": fmt(r.thoi_gian_den)}


def in_range(q, col, from_, to):
    if from_:
        q = q.where(col >= from_)
    if to:
        q = q.where(col <= to)
    return q


FROM = Query(None, alias="from")


@router.get("/scada")
def scada(from_: date | None = FROM, to: date | None = None, day_chuyen: str | None = None, db=Depends(get_db)):
    q = in_range(select(ScadaSummary, Report).join(Report, Report.id == ScadaSummary.report_id), Report.report_date, from_, to)
    if day_chuyen:
        q = q.where(ScadaSummary.day_chuyen_key == day_chuyen_key(day_chuyen))
    rows = db.execute(q.order_by(Report.report_date, ScadaSummary.day_chuyen_key)).all()
    ab = defaultdict(list)
    for a in db.scalars(select(ScadaAbnormal).where(ScadaAbnormal.report_id.in_([r.id for _, r in rows])).order_by(ScadaAbnormal.id)):
        ab[a.report_id].append({"loai": a.loai_raw, "loai_key": a.loai_key, "loai_vi": a.loai_vi,
                                "so_luong": a.so_luong, "ty_le": a.ty_le})
    cols = ("day_chuyen", "day_chuyen_key", "so_luong_da_quet", "so_luong_goi_theo_luoi", "so_buu_kien_bat_thuong",
            "ty_le_bat_thuong", "thoi_gian_quet_trung_binh", "cong_suat_cao_nhat_1h", "cong_suat_max_tu", "cong_suat_max_den")
    return [{**meta(r), **{c: fmt(getattr(s, c)) for c in cols}, "phan_bo_bat_thuong": ab[r.id]} for s, r in rows]


@router.get("/scada/abnormal")
def scada_abnormal(from_: date | None = FROM, to: date | None = None, day_chuyen: str | None = None, db=Depends(get_db)):
    """Tổng hợp theo loai_key trong khoảng ngày."""
    q = in_range(select(ScadaAbnormal, ScadaSummary).join(ScadaSummary, ScadaSummary.report_id == ScadaAbnormal.report_id)
                 .join(Report, Report.id == ScadaAbnormal.report_id), Report.report_date, from_, to)
    if day_chuyen:
        q = q.where(ScadaSummary.day_chuyen_key == day_chuyen_key(day_chuyen))
    agg = {}
    for a, _ in db.execute(q):
        g = agg.setdefault(a.loai_key, {"loai_key": a.loai_key, "loai_vi": a.loai_vi, "so_luong": 0, "so_bao_cao": 0})
        g["so_luong"] += a.so_luong
        g["so_bao_cao"] += 1
    return sorted(agg.values(), key=lambda g: -g["so_luong"])


@router.get("/dmwcs/sorted")
def dmwcs_sorted(from_: date | None = FROM, to: date | None = None, db=Depends(get_db)):
    q = in_range(select(DmwcsSorted, Report).join(Report, Report.id == DmwcsSorted.report_id), Report.report_date, from_, to)
    out = []
    for s, r in db.execute(q.order_by(Report.report_date)):
        out.append({**meta(r), **{c: getattr(s, c) for c in ("total", "correct_chute", "pda", "reject_chute", "sort_failed",
                                                               "pie_correct_pct", "pie_reject_pct", "no_chute_danh_sach",
                                                               "no_chute_bi_cat")},
                    **{k: {"so_luong": getattr(s, f"{k}_so_luong"), "ty_le": getattr(s, f"{k}_ty_le")}
                       for k in ("no_read", "no_post_office", "no_chute")}})
    return out


@router.get("/dmwcs/capacity")
def dmwcs_capacity(from_: date | None = FROM, to: date | None = None, db=Depends(get_db)):
    """Mỗi ngày đúng 1 giá trị (đã chọn ảnh mới nhất lúc ghi)."""
    q = in_range(select(DmwcsCapacityDaily, Report).join(Report, Report.id == DmwcsCapacityDaily.report_id),
                 DmwcsCapacityDaily.ngay, from_, to)
    return [{"ngay": fmt(c.ngay), "cong_suat": c.cong_suat, "report_id": r.id, "file": r.source_name, "model": r.model,
             "model_lan_2": r.model_lan_2, "canh_bao": r.canh_bao or [], "status": r.status,
             "tu_ngay": fmt(r.thoi_gian_tu.date()) if r.thoi_gian_tu else None, "den_ngay": fmt(r.report_date)}
            for c, r in db.execute(q.order_by(DmwcsCapacityDaily.ngay))]


@router.get("/dmwcs/bcr")
def dmwcs_bcr(from_: date | None = FROM, to: date | None = None, bcr_no: int | None = None, db=Depends(get_db)):
    q = in_range(select(DmwcsBcr, Report).join(Report, Report.id == DmwcsBcr.report_id), Report.report_date, from_, to)
    if bcr_no is not None:
        q = q.where(DmwcsBcr.bcr_no == bcr_no)
    recs = {}
    for b, r in db.execute(q.order_by(Report.report_date, DmwcsBcr.bcr_no)):
        recs.setdefault(r.id, {**meta(r), "bcr": []})["bcr"].append(
            {c: getattr(b, c) for c in ("bcr_no", "total", "success", "failed", "rate")})
    return list(recs.values())


@router.get("/compare")
def compare(from_: date | None = FROM, to: date | None = None, db=Depends(get_db)):
    """SCADA cạnh DMWCS theo cùng ngày: tổng đã quét SCADA (và từng dây chuyền) so với Total/Correct/Reject DMWCS."""
    days = defaultdict(lambda: {"scada": {"so_luong_da_quet": 0, "day_chuyen": {}}, "dmwcs": None})
    q = in_range(select(ScadaSummary, Report).join(Report, Report.id == ScadaSummary.report_id), Report.report_date, from_, to)
    for s, r in db.execute(q):
        d = days[fmt(r.report_date)]["scada"]
        d["so_luong_da_quet"] += s.so_luong_da_quet
        d["day_chuyen"][s.day_chuyen] = s.so_luong_da_quet
    q = in_range(select(DmwcsSorted, Report).join(Report, Report.id == DmwcsSorted.report_id), Report.report_date, from_, to)
    for s, r in db.execute(q):
        days[fmt(r.report_date)]["dmwcs"] = {"total": s.total, "correct": s.correct_chute + s.pda, "reject": s.reject_chute}
    return [{"ngay": k, **v, "scada": v["scada"] if v["scada"]["day_chuyen"] else None} for k, v in sorted(days.items())]
