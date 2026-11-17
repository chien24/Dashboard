"""Pydantic schema cho 4 loại output OCR (chuyển nguyên từ scada_ocr.py) và schema nhận diện loại ảnh.

Các schema này vừa gửi cho Gemini làm response_schema, vừa dùng để validate output của NVIDIA/OpenRouter
và dữ liệu sửa tay (PUT /api/reports/{id}).
"""
import re
from typing import Annotated, Literal

from pydantic import BaseModel, BeforeValidator, Field


def to_number(v):
    """Chuẩn hóa số đọc từ ảnh: '5 987.75' -> 5987.75, '83.23%' -> 83.23. Số thì giữ nguyên."""
    if isinstance(v, str):
        return float(re.sub(r"[\s,%]", "", v))  # dấu cách / dấu phẩy là phân cách hàng nghìn
    return v


Num = Annotated[float, BeforeValidator(to_number)]
Int = Annotated[int, BeforeValidator(to_number)]

# Trường model tự báo chỗ khó đọc; pipeline chuyển vào canh_bao rồi bỏ khỏi dữ liệu
CANH_BAO_OCR = "Chỗ mờ, bị che, bị cắt hoặc số trông bất thường khi đọc ảnh, mỗi chỗ 1 câu ngắn. Rỗng nếu không có"


# ---------------------------------------------------------------- HT1: SCADA
class LoaiBatThuong(BaseModel):
    loai: str = Field(description="Tên loại bất thường, chép nguyên văn như trên ảnh, kể cả ký tự '?' do lỗi font hoặc chữ tiếng Trung")
    so_luong: int
    ty_le: float = Field(description="Phần trăm, chỉ lấy số, bỏ dấu %")


class Scada(BaseModel):
    thoi_gian_tu: str = Field(description="Ô 'Thời gian quét' - mốc bắt đầu, dạng YYYY-MM-DD HH:MM")
    thoi_gian_den: str = Field(description="Ô 'Thời gian quét' - mốc kết thúc, dạng YYYY-MM-DD HH:MM")
    day_chuyen: str = Field(description="Ô 'dây chuyền sản xuất', ví dụ Outbound")
    so_luong_da_quet: int = Field(description="Thẻ 'Số lượng đã quét'")
    so_luong_goi_theo_luoi: int = Field(description="Thẻ 'Số lượng gói theo lưới'")
    so_buu_kien_bat_thuong: int = Field(description="Thẻ 'Số lượng bưu kiện bất thường'")
    ty_le_bat_thuong: float = Field(description="Thẻ 'Tỷ lệ bất thường', bỏ dấu %")
    thoi_gian_quet_trung_binh: float = Field(description="Thẻ 'Thời gian quét trung bình'")
    cong_suat_cao_nhat_1h: int = Field(description="Thẻ 'Công suất cao nhất trong một giờ' - số lớn")
    cong_suat_max_tu: str = Field(description="Dòng 'Thời gian xảy ra' dưới thẻ công suất - mốc đầu, YYYY-MM-DD HH:MM:SS")
    cong_suat_max_den: str = Field(description="Dòng 'Thời gian xảy ra' - mốc cuối, YYYY-MM-DD HH:MM:SS")
    phan_bo_bat_thuong: list[LoaiBatThuong] = Field(
        description="Chú thích (legend) bên phải biểu đồ tròn 'Phân bổ loại bất thường', theo đúng thứ tự từ trên xuống"
    )
    canh_bao_ocr: list[str] = Field(description=CANH_BAO_OCR)


# ---------------------------------------------------- HT2: DMWCS - Capacity
class DiemCongSuat(BaseModel):
    ngay: str = Field(description="Ngày ở trục X ngay bên dưới điểm, YYYY-MM-DD")
    cong_suat: Num = Field(description="Nhãn số in phía trên điểm, ví dụ '5 987.75' -> 5987.75")


class Capacity(BaseModel):
    tu_ngay: str = Field(description="Ô ngày thứ nhất cạnh nút Query, YYYY-MM-DD")
    den_ngay: str = Field(description="Ô ngày thứ hai cạnh nút Query, YYYY-MM-DD")
    cong_suat_theo_ngay: list[DiemCongSuat] = Field(
        description="Các điểm có nhãn số trên biểu đồ 'The Report of Capacity', thứ tự từ trái sang phải"
    )
    canh_bao_ocr: list[str] = Field(description=CANH_BAO_OCR)


# ------------------------------------------------------ HT2: DMWCS - Sorted
class SoLuongTyLe(BaseModel):
    so_luong: Int = Field(description="Số trước ngoặc, ví dụ '10053(83.23%)' -> 10053")
    ty_le: Num = Field(description="Số trong ngoặc, bỏ dấu %, ví dụ '10053(83.23%)' -> 83.23")


class Sorted(BaseModel):
    thoi_gian_tu: str = Field(description="Ô thời gian thứ nhất cạnh nút Query, YYYY-MM-DD HH:MM:SS")
    thoi_gian_den: str = Field(description="Ô thời gian thứ hai cạnh nút Query, YYYY-MM-DD HH:MM:SS")
    total: Int = Field(description="Dòng Total")
    correct_chute: Int = Field(description="Dòng CorrectChute")
    pda: Int = Field(description="Dòng PDA")
    reject_chute: Int = Field(description="Dòng RejectChute")
    no_read: SoLuongTyLe = Field(description="Dòng NoRead")
    no_post_office: SoLuongTyLe = Field(description="Dòng NoPostOffice")
    no_chute: SoLuongTyLe = Field(description="Dòng NoChute THỨ NHẤT, dạng '265(2.19%)'")
    no_chute_danh_sach: str = Field(
        description="Dòng NoChute THỨ HAI: danh sách số máng ngăn bằng '/', chép nguyên văn phần nhìn thấy, không đoán phần bị cắt"
    )
    sort_failed: Int = Field(description="Dòng SortFailed")
    pie_correct_pct: Num = Field(description="Nhãn 'Correct: x %' trên biểu đồ tròn, chỉ lấy số")
    pie_reject_pct: Num = Field(description="Nhãn 'Reject: y %' trên biểu đồ tròn, chỉ lấy số")
    canh_bao_ocr: list[str] = Field(description=CANH_BAO_OCR)


# ---------------------------------------------------- HT2: DMWCS - Bcr rate
class DongBcr(BaseModel):
    bcr_no: Int = Field(description="Cột BCR_NO")
    total: Int = Field(description="Cột TOTAL")
    success: Int = Field(description="Cột SUCCESS")
    failed: Int = Field(description="Cột FAILED")
    rate: Num = Field(description="Cột RATE, bỏ dấu %, ví dụ '89.20%' -> 89.20")


class BcrRate(BaseModel):
    thoi_gian_tu: str = Field(description="Ô thời gian thứ nhất cạnh nút Query, YYYY-MM-DD HH:MM:SS")
    thoi_gian_den: str = Field(description="Ô thời gian thứ hai cạnh nút Query, YYYY-MM-DD HH:MM:SS")
    bcr: list[DongBcr] = Field(description="Mọi dòng của bảng popup BCR_NO | TOTAL | SUCCESS | FAILED | RATE, từ trên xuống")
    canh_bao_ocr: list[str] = Field(description=CANH_BAO_OCR)


# ------------------------------------------------------------ nhận diện loại
LOAI = ("scada", "dmwcs_sorted", "dmwcs_capacity", "dmwcs_bcr_rate")


class Classify(BaseModel):
    loai: Literal["scada", "dmwcs_sorted", "dmwcs_capacity", "dmwcs_bcr_rate", "khac"]


SCHEMAS: dict[str, type[BaseModel]] = {
    "scada": Scada, "dmwcs_sorted": Sorted, "dmwcs_capacity": Capacity, "dmwcs_bcr_rate": BcrRate, "classify": Classify,
}
