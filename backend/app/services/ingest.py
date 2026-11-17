"""Ghi kết quả đã chuẩn hóa vào DB.

Ghi đè khi trùng: report mới "chiếm" khóa (scada: dây chuyền + ca; sorted/bcr: khoảng thời gian), dòng chi tiết
của report cũ bị xóa nhưng report cũ (raw JSON) vẫn giữ. Capacity: mỗi ngày 1 dòng, lấy ảnh có den_ngay muộn hơn.
"""
from sqlalchemy import delete, select

from app.models import (DmwcsBcr, DmwcsCapacityDaily, DmwcsNoChuteItem, DmwcsSorted, Report, ScadaAbnormal,
                        ScadaSummary)
from app.services.normalize import abnormal_type, day_chuyen_key, no_chute_bi_cat, parse_dt, report_times

DETAIL_TABLES = (ScadaSummary, ScadaAbnormal, DmwcsSorted, DmwcsNoChuteItem, DmwcsBcr, DmwcsCapacityDaily)
CAPACITY_KHAC = "Công suất AVG"  # tiền tố cảnh báo khi ảnh capacity mới khác ảnh cũ


def clear_details(db, report_ids):
    ids = list(report_ids)
    if ids:
        for t in DETAIL_TABLES:
            db.execute(delete(t).where(t.report_id.in_(ids)))


def ingest(db, r: dict, upload_id: int | None = None, source_name: str | None = None) -> Report:
    """r: kết quả của pipeline.process (hoặc import JSON). Commit và trả Report."""
    tu, den, rd = report_times(r["loai"], r["data"])
    rep = Report(upload_id=upload_id, source_name=source_name, loai=r["loai"], provider=r.get("provider"),
                 model=r.get("model"), model_lan_2=r.get("model_lan_2"), status=r.get("status", "ok"),
                 canh_bao=list(r.get("canh_bao") or []), thoi_gian_tu=tu, thoi_gian_den=den, report_date=rd,
                 data=r["data"], raw_json_1=r.get("raw_json_1"), raw_json_2=r.get("raw_json_2"), attempts=r.get("attempts"))
    db.add(rep)
    db.flush()
    write_details(db, rep)
    db.commit()
    return rep


def write_details(db, rep: Report):
    """(Ghi lại) bảng chi tiết của 1 report từ rep.data. Dùng cả khi sửa tay."""
    d = rep.data
    clear_details(db, [rep.id])
    if rep.loai == "scada":
        key = day_chuyen_key(d["day_chuyen"])
        old = db.scalars(select(ScadaSummary.report_id).where(
            ScadaSummary.day_chuyen_key == key, ScadaSummary.thoi_gian_tu == rep.thoi_gian_tu,
            ScadaSummary.thoi_gian_den == rep.thoi_gian_den)).all()
        clear_details(db, old)
        db.add(ScadaSummary(
            report_id=rep.id, day_chuyen=d["day_chuyen"], day_chuyen_key=key,
            thoi_gian_tu=rep.thoi_gian_tu, thoi_gian_den=rep.thoi_gian_den,
            cong_suat_max_tu=parse_dt(d["cong_suat_max_tu"]), cong_suat_max_den=parse_dt(d["cong_suat_max_den"]),
            **{k: d[k] for k in ("so_luong_da_quet", "so_luong_goi_theo_luoi", "so_buu_kien_bat_thuong",
                                 "ty_le_bat_thuong", "thoi_gian_quet_trung_binh", "cong_suat_cao_nhat_1h")}))
        for x in d["phan_bo_bat_thuong"]:
            key_, vi = abnormal_type(x["loai"])
            if key_ == "UNKNOWN" and not any(x["loai"] in c for c in rep.canh_bao):
                rep.canh_bao = [*rep.canh_bao, f"Loại bất thường chưa có trong abnormal_types.json: '{x['loai']}'"]
            db.add(ScadaAbnormal(report_id=rep.id, loai_raw=x["loai"], loai_key=key_, loai_vi=vi,
                                 so_luong=x["so_luong"], ty_le=x["ty_le"]))
    elif rep.loai in ("dmwcs_sorted", "dmwcs_bcr_rate"):
        table = DmwcsSorted if rep.loai == "dmwcs_sorted" else DmwcsBcr
        old = db.scalars(select(Report.id).where(
            Report.loai == rep.loai, Report.id != rep.id, Report.thoi_gian_tu == rep.thoi_gian_tu,
            Report.thoi_gian_den == rep.thoi_gian_den, Report.id.in_(select(table.report_id)))).all()
        clear_details(db, old)
        if rep.loai == "dmwcs_bcr_rate":
            for b in d["bcr"]:
                db.add(DmwcsBcr(report_id=rep.id, **{k: b[k] for k in ("bcr_no", "total", "success", "failed", "rate")}))
        else:
            cat = no_chute_bi_cat(rep.canh_bao)
            db.add(DmwcsSorted(
                report_id=rep.id, no_chute_danh_sach=d["no_chute_danh_sach"], no_chute_bi_cat=cat,
                **{k: d[k] for k in ("total", "correct_chute", "pda", "reject_chute", "sort_failed",
                                     "pie_correct_pct", "pie_reject_pct")},
                **{f"{k}_{f}": d[k][f] for k in ("no_read", "no_post_office", "no_chute") for f in ("so_luong", "ty_le")}))
            items = [x for x in d["no_chute_danh_sach"].split("/") if x.strip().isdigit()]
            for i, x in enumerate(items):
                db.add(DmwcsNoChuteItem(report_id=rep.id, chute_no=int(x), co_the_bi_cat=cat and i == len(items) - 1))
    elif rep.loai == "dmwcs_capacity":
        canh_bao = [c for c in rep.canh_bao if not c.startswith(CAPACITY_KHAC)]
        for p in d["cong_suat_theo_ngay"]:
            ngay = parse_dt(p["ngay"])
            if not ngay:
                continue  # validate đã cảnh báo ngày sai định dạng
            ngay = ngay.date()
            cur = db.scalar(select(DmwcsCapacityDaily).where(DmwcsCapacityDaily.ngay == ngay))
            if cur:
                cur_rep = db.get(Report, cur.report_id)
                if cur_rep.report_date > rep.report_date:
                    continue  # ảnh đang dùng có khoảng truy vấn mới hơn -> giữ
                if cur.cong_suat != p["cong_suat"]:
                    canh_bao.append(f"{CAPACITY_KHAC} ngày {ngay:%d/%m} khác ảnh trước ({cur.cong_suat} ở report "
                                    f"#{cur.report_id}): dùng {p['cong_suat']} của ảnh này")
                db.delete(cur)
                db.flush()
            db.add(DmwcsCapacityDaily(report_id=rep.id, ngay=ngay, cong_suat=p["cong_suat"]))
        rep.canh_bao = canh_bao
    db.flush()
