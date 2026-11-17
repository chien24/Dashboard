"""Ingest 4 file mẫu vào DB tạm: đủ mọi trường, ghi đè khi trùng, API dashboard trả đúng số."""
import copy
import json

import pytest
from conftest import FIXTURES
from fastapi.testclient import TestClient
from sqlalchemy import select

from app.db import SessionLocal
from app.models import (DmwcsBcr, DmwcsCapacityDaily, DmwcsNoChuteItem, DmwcsSorted, Report, ScadaAbnormal,
                        ScadaSummary)
from app.services.ingest import ingest
from import_json import import_paths, to_result

FILES = [FIXTURES / n for n in ("1.json", "2.json", "3.json", "tong_hop_scada.json")]


@pytest.fixture
def db(clean_db):
    them, bo_qua, loi = import_paths(FILES)
    assert (them, bo_qua, loi) == (7, 0, [])
    with SessionLocal() as s:
        yield s


def rec(name):
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))


def test_ingest_scada_du_truong(db):
    rows = {s.day_chuyen_key: s for s in db.scalars(select(ScadaSummary))}
    assert set(rows) == {"outbound", "inbound", "cbs1 2st layer", "cbs2 1st layer"}
    for r in rec("tong_hop_scada.json"):
        s = rows[r["day_chuyen"].lower()]
        for k in ("so_luong_da_quet", "so_luong_goi_theo_luoi", "so_buu_kien_bat_thuong", "ty_le_bat_thuong",
                  "thoi_gian_quet_trung_binh", "cong_suat_cao_nhat_1h"):
            assert getattr(s, k) == r[k], k
        assert str(s.cong_suat_max_tu) == r["cong_suat_max_tu"]
        ab = db.scalars(select(ScadaAbnormal).where(ScadaAbnormal.report_id == s.report_id).order_by(ScadaAbnormal.id)).all()
        assert [(a.loai_raw, a.so_luong, a.ty_le) for a in ab] == [(x["loai"], x["so_luong"], x["ty_le"]) for x in r["phan_bo_bat_thuong"]]
        assert "UNKNOWN" not in {a.loai_key for a in ab}
    assert {r.status for r in db.scalars(select(Report).where(Report.loai == "scada"))} == {"ok"}


def test_ingest_dmwcs_du_truong(db):
    r1 = rec("1.json")
    s = db.scalar(select(DmwcsSorted))
    assert (s.total, s.correct_chute, s.pda, s.reject_chute, s.sort_failed) == (108957, 81121, 15758, 12078, 716)
    assert (s.no_read_so_luong, s.no_read_ty_le, s.no_chute_ty_le) == (10053, 83.23, 2.19)
    assert s.no_chute_danh_sach == r1["no_chute_danh_sach"] and s.no_chute_bi_cat  # canh_bao báo dòng bị cắt
    items = db.scalars(select(DmwcsNoChuteItem).order_by(DmwcsNoChuteItem.id)).all()
    assert [i.chute_no for i in items] == [int(x) for x in r1["no_chute_danh_sach"].split("/")]
    assert [i.co_the_bi_cat for i in items] == [False] * (len(items) - 1) + [True]
    caps = db.scalars(select(DmwcsCapacityDaily).order_by(DmwcsCapacityDaily.ngay)).all()
    assert [(str(c.ngay), c.cong_suat) for c in caps] == [(p["ngay"], p["cong_suat"]) for p in rec("2.json")["cong_suat_theo_ngay"]]
    bcr = db.scalars(select(DmwcsBcr).order_by(DmwcsBcr.bcr_no)).all()
    assert [(b.bcr_no, b.total, b.success, b.failed, b.rate) for b in bcr] == \
           [(b["bcr_no"], b["total"], b["success"], b["failed"], b["rate"]) for b in rec("3.json")["bcr"]]


def test_import_lai_khong_tao_ban_sao(db):
    assert import_paths(FILES)[:2] == (0, 7)


def test_ghi_de_khi_trung(db):
    # sorted cùng khoảng thời gian -> chỉ còn bản mới trên dashboard, report cũ (raw) vẫn giữ
    moi = copy.deepcopy(rec("1.json"))
    moi.update(file="moi.jpg", total=108958, correct_chute=81122)
    rep = ingest(db, to_result(moi), source_name="moi.jpg")
    assert [s.report_id for s in db.scalars(select(DmwcsSorted))] == [rep.id]
    assert db.scalar(select(Report).where(Report.source_name == "1.json")) is None  # source_name là tên ảnh, không phải tên JSON
    assert len(db.scalars(select(Report).where(Report.loai == "dmwcs_sorted")).all()) == 2
    # capacity chồng ngày, ảnh mới (den_ngay muộn hơn) thắng, khác giá trị thì cảnh báo
    cap = {"file": "cap2.jpg", "loai": "dmwcs_capacity", "tu_ngay": "2026-11-10", "den_ngay": "2026-11-11",
           "cong_suat_theo_ngay": [{"ngay": "2026-11-10", "cong_suat": 5609.95}, {"ngay": "2026-11-11", "cong_suat": 5790.51}]}
    rep = ingest(db, to_result(cap), source_name="cap2.jpg")
    c10 = db.scalar(select(DmwcsCapacityDaily).where(DmwcsCapacityDaily.ngay == rep.report_date.replace(day=10)))
    assert (c10.cong_suat, c10.report_id) == (5609.95, rep.id)
    assert any("khác ảnh trước" in c for c in rep.canh_bao)


def test_api_dashboard_va_sua_tay(db):
    c = TestClient(__import__("app.main", fromlist=["app"]).app)  # không dùng `with`: không chạy worker/scheduler
    scada = c.get("/api/dashboard/scada", params={"from": "2026-11-01", "to": "2026-11-30"}).json()
    assert len(scada) == 4 and all(r["phan_bo_bat_thuong"] for r in scada)
    assert c.get("/api/dashboard/scada", params={"day_chuyen": "CBS2 1st layer"}).json()[0]["so_luong_da_quet"] == 27648
    assert len(c.get("/api/dashboard/dmwcs/capacity").json()) == 6
    assert [b["rate"] for b in c.get("/api/dashboard/dmwcs/bcr").json()[0]["bcr"]] == [89.2, 88.9, 100.0, 88.13, 78.34]
    rid = c.get("/api/reports", params={"loai": "dmwcs_sorted"}).json()["items"][0]["id"]
    data = c.get(f"/api/reports/{rid}").json()["data"]
    r = c.put(f"/api/reports/{rid}", json={**data, "total": 1}).json()
    assert r["status"] == "da_sua_tay" and any("khác Total" in w for w in r["canh_bao"])
    assert c.get("/api/dashboard/dmwcs/sorted").json()[0]["total"] == 1
    assert c.put(f"/api/reports/{rid}", json={**data, "total": "abc"}).status_code == 422


def test_lich_su_tim_kiem(db):
    c = TestClient(__import__("app.main", fromlist=["app"]).app)
    moi = copy.deepcopy(rec("1.json"))
    moi.update(file="Sorted_Moi.jpg", total=108958)
    ingest(db, to_result(moi), source_name="Sorted_Moi.jpg")  # ghi đè bản sorted cũ trên dashboard
    tim = c.get("/api/reports", params={"q": "sorted_moi"}).json()  # không phân biệt hoa thường, tìm chung 2 hệ thống
    assert tim["total"] == 1 and tim["items"][0]["dang_dung"]
    ht2 = c.get("/api/reports", params={"he": "ht2"}).json()["items"]
    assert {i["loai"] for i in ht2} == {"dmwcs_sorted", "dmwcs_capacity", "dmwcs_bcr_rate"}
    assert [i["dang_dung"] for i in ht2 if i["loai"] == "dmwcs_sorted"].count(False) == 1  # bản cũ bị thay
    ht1 = c.get("/api/reports", params={"he": "ht1", "from": "2026-11-01", "to": "2026-11-30"}).json()["items"]
    assert ht1 and all(i["loai"] == "scada" and i["day_chuyen"] for i in ht1)
    assert c.get("/api/reports", params={"q": "%"}).json()["total"] == 0  # ký tự đặc biệt của LIKE không bị hiểu là "mọi thứ"
    assert c.get("/api/reports", params={"he": "ht9"}).status_code == 400
    d = c.get(f"/api/reports/{ht1[0]['id']}").json()
    assert d["bat_thuong"] and all(p["loai_key"] != "UNKNOWN" for p in d["bat_thuong"])


def test_retention_35_ngay(db):
    from datetime import timedelta

    from app.models import now
    from app.services.retention import cleanup

    cu = copy.deepcopy(rec("3.json"))
    ngay = now().date() - timedelta(days=40)
    cu.update(file="cu.jpg", thoi_gian_tu=f"{ngay} 00:00:00", thoi_gian_den=f"{ngay + timedelta(days=1)} 00:00:00")
    rep = ingest(db, to_result(cu), source_name="cu.jpg")
    xem = cleanup(db, dry_run=True)
    assert [r["id"] for r in xem["reports"]] == [rep.id] and db.get(Report, rep.id)  # dry_run không xóa
    cleanup(db, dry_run=False)
    db.expire_all()
    assert db.get(Report, rep.id) is None and not db.scalars(select(DmwcsBcr).where(DmwcsBcr.report_id == rep.id)).all()
    assert all(str(r.report_date) >= xem["cutoff"] for r in db.scalars(select(Report)))  # chỉ còn report trong hạn
