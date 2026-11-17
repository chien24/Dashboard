"""Chuẩn hóa: thời gian, tên dây chuyền, tên loại bất thường SCADA, cảnh báo của model."""
import difflib
import json
import re
import unicodedata
from datetime import date, datetime
from functools import lru_cache
from pathlib import Path

ABNORMAL_FILE = Path(__file__).resolve().parents[1] / "ocr" / "abnormal_types.json"


def parse_dt(s) -> datetime | None:
    """'2026-11-03 00:00', '2026-11-09 00:00:00', '2026-11-05' -> datetime (giờ địa phương, naive)."""
    try:
        return datetime.fromisoformat(str(s).strip())
    except ValueError:
        return None


def report_times(loai: str, d: dict) -> tuple[datetime | None, datetime | None, date]:
    """(thoi_gian_tu, thoi_gian_den, report_date). Capacity: report_date = den_ngay; còn lại: ngày của thoi_gian_tu."""
    if loai == "dmwcs_capacity":
        tu, den = parse_dt(d["tu_ngay"]), parse_dt(d["den_ngay"])
        if not den:
            raise ValueError(f"den_ngay không hợp lệ: {d['den_ngay']!r}")
        return tu, den, den.date()
    tu, den = parse_dt(d["thoi_gian_tu"]), parse_dt(d["thoi_gian_den"])
    if not tu:
        raise ValueError(f"thoi_gian_tu không hợp lệ: {d['thoi_gian_tu']!r}")
    return tu, den, tu.date()


def day_chuyen_key(s: str) -> str:
    """Chữ thường, gộp khoảng trắng: 'CBs2  1st layer' và 'CBS2 1st layer' -> 'cbs2 1st layer'."""
    return " ".join(s.lower().split())


def _plain(s: str) -> str:
    s = unicodedata.normalize("NFD", s.replace("đ", "d").replace("Đ", "D"))
    return " ".join("".join(c for c in s if unicodedata.category(c) != "Mn").lower().split())


def _wild_eq(a: str, b: str) -> bool:
    """So từng ký tự; '?' ở bên nào cũng khớp 1 ký tự bất kỳ (lỗi font của SCADA)."""
    return len(a) == len(b) and all(x == y or "?" in (x, y) for x, y in zip(a, b))


@lru_cache
def _types() -> dict:
    return {k: v for k, v in json.loads(ABNORMAL_FILE.read_text(encoding="utf-8")).items() if not k.startswith("_")}


def abnormal_type(raw: str) -> tuple[str, str]:
    """Tên OCR -> (loai_key, loai_vi). Không khớp -> ('UNKNOWN', raw)."""
    p = _plain(raw)
    types = _types()
    for key, t in types.items():
        if any(_wild_eq(p, _plain(v)) for v in t["bien_the"]):
            return key, t["vi"]
    # gần đúng: bỏ '?' rồi so độ giống, lấy biến thể giống nhất nếu >= 0.8
    q = p.replace("?", "")
    best = max(((difflib.SequenceMatcher(None, q, _plain(v).replace("?", "")).ratio(), key)
                for key, t in types.items() for v in t["bien_the"]), default=(0, None))
    if best[0] >= 0.8:
        return best[1], types[best[1]]["vi"]
    return "UNKNOWN", raw


# Model hay tự báo "tổng % vượt 100%" cho SCADA; điều đó là bình thường nên bỏ cảnh báo này.
_VUOT_100 = re.compile(r"(vượt|quá|lớn hơn|hơn|>|exceed).{0,40}100\s*%|100\s*%.{0,20}(vượt|quá)", re.I)


def model_notes(loai: str, notes: list[str]) -> list[str]:
    return [n for n in notes if not (loai == "scada" and _VUOT_100.search(n))]


def no_chute_bi_cat(canh_bao: list[str]) -> bool:
    return any("nochute" in c.lower().replace(" ", "") and re.search(r"cắt|che|cut|trunc", c, re.I) for c in canh_bao)
