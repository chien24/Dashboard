"""Hồi quy OCR: so JSON OCR với số liệu đối chiếu tay (hoi_quy/ky_vong.json).

Cần chạy OCR 6 ảnh mẫu trước (có gọi API):
    python scripts/ocr_folder.py ../sample_dashboar/HT1 --force
    python scripts/ocr_folder.py ../sample_dashboar/HT2/sorted/1.jpg --bao-cao sorted --force
    python scripts/ocr_folder.py ../sample_dashboar/HT2/capacity/2.jpg --bao-cao capacity --force
    python scripts/ocr_folder.py ../sample_dashboar/HT2/bcr_rate/3.jpg --bao-cao bcr_rate --force
Rồi (trong backend/):  pytest tests/test_hoi_quy.py -v        (đổi thư mục kết quả: đặt OCR_OUT=<thư mục>)
Ảnh chưa có JSON thì bị skip. Test so số OCR thô, KHÔNG áp overrides.json.
"""
import json
import os
from pathlib import Path

import pytest

from ocr_folder import system_dir

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]  # thư mục gốc dự án (chứa ket_qua_json)
KY_VONG = {k: v for k, v in json.loads((HERE / "hoi_quy" / "ky_vong.json").read_text(encoding="utf-8")).items()
           if not k.startswith("_")}
OUT = Path(os.environ.get("OCR_OUT", ROOT / "ket_qua_json"))


def actual(rec: dict, field: str):
    if field == "phan_bo_bat_thuong":
        return [[x["so_luong"], x["ty_le"]] for x in rec[field]]
    if field == "cong_suat_theo_ngay":
        return [[p["ngay"], p["cong_suat"]] for p in rec[field]]
    if field == "bcr":
        return [[r["bcr_no"], r["total"], r["success"], r["failed"], r["rate"]] for r in rec[field]]
    return rec.get(field)


def mismatches(rec: dict, ky_vong: dict) -> list[str]:
    errs = []
    for field, want in ky_vong.items():
        if field == "anh":
            continue
        if field == "no_chute_danh_sach_bat_dau":
            if not rec.get("no_chute_danh_sach", "").startswith(want):
                errs.append(f"no_chute_danh_sach: '{rec.get('no_chute_danh_sach')}' không bắt đầu bằng '{want}'")
        elif (got := actual(rec, field)) != want:
            errs.append(f"{field}: OCR {got} / ảnh {want}")
    return errs


@pytest.mark.parametrize("key", KY_VONG)
def test_ocr_khop_anh(key):
    loai, file = key.split("/")
    f = OUT / system_dir(loai) / f"{Path(file).stem}.json"
    if not f.exists():
        pytest.skip(f"chưa có {f}")
    rec = json.loads(f.read_text(encoding="utf-8"))
    assert rec["loai"] == loai and rec["file"] == file, f"{f} là {rec['loai']}/{rec['file']}"
    errs = mismatches(rec, KY_VONG[key])
    assert not errs, "\n".join(errs + [f"canh_bao: {rec['canh_bao']}"])
