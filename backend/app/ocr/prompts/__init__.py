"""Prompt OCR (chuyển nguyên từ code cũ) để trong file .txt cùng thư mục, sửa được mà không cần sửa code."""
from pathlib import Path

_D = Path(__file__).parent


def _read(name: str) -> str:
    return (_D / f"{name}.txt").read_text(encoding="utf-8")


QUY_TAC_CHUNG = _read("quy_tac_chung")  # nối sau prompt của mọi loại
LAN_2 = _read("lan_2")                  # nối thêm ở lần OCR thứ 2
HAU_TO_MO = _read("hau_to_mo")          # chỉ cho model mã nguồn mở (NVIDIA, OpenRouter)
PROMPTS = {k: _read(k) for k in ("scada", "dmwcs_sorted", "dmwcs_capacity", "dmwcs_bcr_rate", "classify")}


def prompt_for(loai: str) -> str:
    """Prompt đầy đủ cho 1 loại; 'classify' không cần quy tắc chép số."""
    return PROMPTS[loai] + ("" if loai == "classify" else QUY_TAC_CHUNG)
