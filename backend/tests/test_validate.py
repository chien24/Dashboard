"""Kiểm tra số học, chuẩn hóa tên, parse JSON. Không cần API key."""
import copy
import json

import pytest
from conftest import FIXTURES

from app.ocr.providers.base import AuthError, BadOutput, ModelNotFound, ProviderUnavailable, QuotaExceeded, extract_json, map_error
from app.schemas import Capacity, to_number
from app.services.normalize import abnormal_type, day_chuyen_key, model_notes, no_chute_bi_cat, report_times
from app.services.validate import VALIDATORS, diff_numbers
from ocr_folder import resolve_screen

META = {"file", "loai", "model", "model_lan_2", "canh_bao"}


def records():
    for name in ("1.json", "2.json", "3.json", "tong_hop_scada.json"):
        recs = json.loads((FIXTURES / name).read_text(encoding="utf-8"))
        yield from recs if isinstance(recs, list) else [recs]


def data_of(rec):
    return {k: v for k, v in rec.items() if k not in META}


# ---------------------------------------------------------------- 4 file mẫu: không cảnh báo sai
@pytest.mark.parametrize("rec", list(records()), ids=lambda r: f"{r['loai']}-{r['file']}")
def test_file_mau_khong_canh_bao(rec):
    assert VALIDATORS[rec["loai"]](data_of(rec)) == []


def test_scada_tong_tren_100_la_binh_thuong():
    scada = [r for r in records() if r["loai"] == "scada"]
    assert all(sum(x["ty_le"] for x in r["phan_bo_bat_thuong"]) > 100 for r in scada)  # 102–107% trên dữ liệu mẫu
    assert all(VALIDATORS["scada"](data_of(r)) == [] for r in scada)


def test_scada_bia_so_cho_tron_100_bi_nghi_ngo():
    # ảnh Inbound 03/11: lần OCR cũ đọc 3261 (56.55%) thay vì 3678 (63.78%) để tổng tròn 100%
    inbound = next(data_of(r) for r in records() if r["loai"] == "scada" and r["day_chuyen"] == "Inbound")
    inbound["phan_bo_bat_thuong"][3].update(so_luong=3261, ty_le=56.55)
    assert any("Nghi ngờ" in e for e in VALIDATORS["scada"](inbound))


@pytest.mark.parametrize("loai, sua, tu_khoa", [
    ("dmwcs_sorted", {"total": 108958}, "khác Total"),
    ("dmwcs_sorted", {"pie_correct_pct": 88.5}, "nhãn 'Correct'"),
    ("dmwcs_sorted", {"no_read": {"so_luong": 10053, "ty_le": 83.5}}, "no_read"),
    ("dmwcs_bcr_rate", {"bcr": [{"bcr_no": 1, "total": 10, "success": 9, "failed": 0, "rate": 90.0}]}, "BCR 1: SUCCESS + FAILED"),
    ("dmwcs_bcr_rate", {"bcr": [{"bcr_no": 1, "total": 10, "success": 9, "failed": 1, "rate": 91.0}]}, "BCR 1: SUCCESS / TOTAL"),
    ("dmwcs_capacity", {"cong_suat_theo_ngay": [{"ngay": "2026-11-05", "cong_suat": 0}]}, "Có 1 điểm"),
])
def test_vi_pham_co_canh_bao(loai, sua, tu_khoa):
    d = copy.deepcopy(data_of(next(r for r in records() if r["loai"] == loai)))
    d.update(sua)
    assert any(tu_khoa in e for e in VALIDATORS[loai](d)), VALIDATORS[loai](d)


def test_scada_khung_gio_max_va_goi_theo_luoi():
    d = data_of(next(r for r in records() if r["loai"] == "scada"))
    errs = VALIDATORS["scada"]({**d, "cong_suat_max_den": d["cong_suat_max_tu"], "so_luong_goi_theo_luoi": 10**9})
    assert any("59 phút" in e for e in errs) and any("Số lượng đã quét" in e for e in errs)


# ---------------------------------------------------------------- chuẩn hóa
@pytest.mark.parametrize("raw, key", [
    ("Không có Báo cáo Phân lo?i", "NO_SORT_REPORT"), ("Không có Báo cáo Phân loại", "NO_SORT_REPORT"),
    ("Yêu c?u ?ng d?n th?t b?i", "CHUTE_REQUEST_FAILED"), ("Yêu cầu ?ng đơn th?t b?i", "CHUTE_REQUEST_FAILED"),
    ("Yêu cầu ?ng đến thất bại", "CHUTE_REQUEST_FAILED"), ("Yêu cầu ?ng đ?n th?t b?i", "CHUTE_REQUEST_FAILED"),
    ("Không Có Mã Vạch", "NO_BARCODE"), ("Khóa Ô Phân Loại Quá Vòng", "CHUTE_LOCK_OVER_LOOP"),
    ("Khóa Ở Phân Loại Quá Vòng", "CHUTE_LOCK_OVER_LOOP"),
    ("物理设备异常", "PHYSICAL_DEVICE_ERROR"), ("格口设备异常", "CHUTE_DEVICE_ERROR"),
    ("Hoàn toàn lạ", "UNKNOWN"),
])
def test_abnormal_type(raw, key):
    assert abnormal_type(raw)[0] == key


def test_chuan_hoa_khac():
    assert day_chuyen_key("CBs2  1st layer") == day_chuyen_key("CBS2 1st layer") == "cbs2 1st layer"
    tu, den, rd = report_times("scada", {"thoi_gian_tu": "2026-11-03 00:00", "thoi_gian_den": "2026-11-03 23:59"})
    assert (tu.hour, str(rd)) == (0, "2026-11-03")
    assert str(report_times("dmwcs_capacity", {"tu_ngay": "2026-11-05", "den_ngay": "2026-11-10"})[2]) == "2026-11-10"
    assert model_notes("scada", ["Tổng tỷ lệ phần trăm ở chú thích biểu đồ tròn vượt quá 100%", "Lỗi font '?'"]) == ["Lỗi font '?'"]
    assert no_chute_bi_cat(["OCR lần 1: Dòng NoChute thứ hai bị cắt chữ ở mép phải"])
    assert to_number("5 987.75") == 5987.75 and to_number("83.23%") == 83.23


# ---------------------------------------------------------------- parse output model / map lỗi
@pytest.mark.parametrize("text", ['{"a": 1}', 'Kết quả:\n```json\n{"a": 1}\n```', '<think>{x}</think>{"a": 1}'])
def test_extract_json(text):
    assert extract_json(text) == {"a": 1}


def test_extract_json_loi():
    with pytest.raises(BadOutput):
        extract_json("không có json")


@pytest.mark.parametrize("status, msg, cls", [
    (429, "Too Many Requests", QuotaExceeded), (None, "429 RESOURCE_EXHAUSTED quota", QuotaExceeded),
    (400, "API key not valid. Please pass a valid API key.", AuthError), (401, "Unauthorized", AuthError),
    (402, "Payment required", AuthError), (404, "model not found", ModelNotFound),
    (503, "UNAVAILABLE", ProviderUnavailable), (None, "ReadTimeout", ProviderUnavailable), (504, "DEADLINE", ProviderUnavailable),
])
def test_map_error(status, msg, cls):
    assert isinstance(map_error(status, msg), cls)


def test_schema_nhan_chuoi_so():
    c = Capacity.model_validate({"tu_ngay": "2026-11-05", "den_ngay": "2026-11-05", "canh_bao_ocr": [],
                                 "cong_suat_theo_ngay": [{"ngay": "2026-11-05", "cong_suat": "5 987.75"}]})
    assert c.cong_suat_theo_ngay[0].cong_suat == 5987.75


def test_diff_numbers():
    assert diff_numbers({"a": [{"x": 3678}]}, {"a": [{"x": 3261}, {"x": 2}]}) == ["a[0].x: 3678 / 3261", "a[1].x: — / 2"]


def test_resolve_screen(tmp_path):
    assert resolve_screen(tmp_path / "HT1" / "a.jpg") == "scada"
    assert resolve_screen(tmp_path / "HT2" / "bcr_rate" / "a.jpg", "bcr_rate") == "dmwcs_bcr_rate"
    assert resolve_screen(tmp_path / "x.png") is None
    with pytest.raises(ValueError, match="--bao-cao"):
        resolve_screen(tmp_path / "HT2" / "a.jpg")
