"""Bảng ORM (mục 4 đặc tả). Mọi trường số là cột riêng; raw JSON của 2 lần OCR lưu ở reports."""
from datetime import date, datetime

from sqlalchemy import JSON, Boolean, Date, DateTime, Float, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base


def now():
    from app.config import TZ
    return datetime.now(TZ).replace(tzinfo=None)  # lưu giờ địa phương dạng naive


def fk(table: str, nullable=False):
    return mapped_column(ForeignKey(f"{table}.id", ondelete="CASCADE"), nullable=nullable, index=True)


class Upload(Base):
    __tablename__ = "uploads"
    id: Mapped[int] = mapped_column(primary_key=True)
    original_name: Mapped[str] = mapped_column(String)
    stored_path: Mapped[str] = mapped_column(String)
    sha256: Mapped[str] = mapped_column(String, unique=True)
    mime: Mapped[str | None] = mapped_column(String)
    size_bytes: Mapped[int | None]
    width: Mapped[int | None]
    height: Mapped[int | None]
    uploaded_at: Mapped[datetime] = mapped_column(DateTime, default=now)
    reports: Mapped[list["Report"]] = relationship(back_populates="upload", passive_deletes=True)


class Job(Base):
    __tablename__ = "jobs"
    id: Mapped[int] = mapped_column(primary_key=True)
    upload_id: Mapped[int] = fk("uploads")
    loai_hint: Mapped[str | None] = mapped_column(String)
    only_provider: Mapped[str | None] = mapped_column(String)  # OCR lại bằng provider/model chỉ định
    only_model: Mapped[str | None] = mapped_column(String)
    status: Mapped[str] = mapped_column(String, default="pending", index=True)  # pending/running/done/failed
    progress: Mapped[str | None] = mapped_column(String)  # "lần 1/2 · cloudflare/@cf/qwen/qwen3.8-27b" cho trang upload
    error: Mapped[str | None] = mapped_column(Text)
    report_id: Mapped[int | None] = mapped_column(ForeignKey("reports.id", ondelete="SET NULL"))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=now)
    finished_at: Mapped[datetime | None] = mapped_column(DateTime)


class Report(Base):
    __tablename__ = "reports"
    id: Mapped[int] = mapped_column(primary_key=True)
    upload_id: Mapped[int | None] = fk("uploads", nullable=True)  # None: import từ JSON cũ, không có ảnh
    source_name: Mapped[str | None] = mapped_column(String)  # tên ảnh gốc ('1.jpg'), cả khi import
    loai: Mapped[str] = mapped_column(String, index=True)
    provider: Mapped[str | None] = mapped_column(String)
    model: Mapped[str | None] = mapped_column(String)
    model_lan_2: Mapped[str | None] = mapped_column(String)
    status: Mapped[str] = mapped_column(String, default="ok")  # ok / can_kiem_tra / da_sua_tay
    canh_bao: Mapped[list] = mapped_column(JSON, default=list)
    thoi_gian_tu: Mapped[datetime | None] = mapped_column(DateTime)
    thoi_gian_den: Mapped[datetime | None] = mapped_column(DateTime)
    report_date: Mapped[date] = mapped_column(Date, index=True)
    data: Mapped[dict] = mapped_column(JSON)  # dữ liệu đang dùng (lần 1, hoặc bản sửa tay)
    raw_json_1: Mapped[dict | None] = mapped_column(JSON)
    raw_json_2: Mapped[dict | None] = mapped_column(JSON)
    attempts: Mapped[list | None] = mapped_column(JSON)
    ocr_version: Mapped[str | None] = mapped_column(String)  # bản OCR đang dùng '<report_id>:<lần>'; None = mặc định / sửa tay
    created_at: Mapped[datetime] = mapped_column(DateTime, default=now)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=now, onupdate=now)
    upload: Mapped[Upload | None] = relationship(back_populates="reports")


class ScadaSummary(Base):
    __tablename__ = "scada_summary"
    __table_args__ = (UniqueConstraint("day_chuyen_key", "thoi_gian_tu", "thoi_gian_den"),)
    id: Mapped[int] = mapped_column(primary_key=True)
    report_id: Mapped[int] = fk("reports")
    day_chuyen: Mapped[str] = mapped_column(String)
    day_chuyen_key: Mapped[str] = mapped_column(String, index=True)
    thoi_gian_tu: Mapped[datetime] = mapped_column(DateTime)
    thoi_gian_den: Mapped[datetime] = mapped_column(DateTime)
    so_luong_da_quet: Mapped[int]
    so_luong_goi_theo_luoi: Mapped[int]
    so_buu_kien_bat_thuong: Mapped[int]
    ty_le_bat_thuong: Mapped[float] = mapped_column(Float)
    thoi_gian_quet_trung_binh: Mapped[float] = mapped_column(Float)
    cong_suat_cao_nhat_1h: Mapped[int]
    cong_suat_max_tu: Mapped[datetime | None] = mapped_column(DateTime)
    cong_suat_max_den: Mapped[datetime | None] = mapped_column(DateTime)


class ScadaAbnormal(Base):
    __tablename__ = "scada_abnormal"
    id: Mapped[int] = mapped_column(primary_key=True)
    report_id: Mapped[int] = fk("reports")
    loai_raw: Mapped[str] = mapped_column(String)
    loai_key: Mapped[str] = mapped_column(String, index=True)
    loai_vi: Mapped[str] = mapped_column(String)
    so_luong: Mapped[int]
    ty_le: Mapped[float] = mapped_column(Float)


class DmwcsSorted(Base):
    __tablename__ = "dmwcs_sorted"
    id: Mapped[int] = mapped_column(primary_key=True)
    report_id: Mapped[int] = fk("reports")
    total: Mapped[int]
    correct_chute: Mapped[int]
    pda: Mapped[int]
    reject_chute: Mapped[int]
    no_read_so_luong: Mapped[int]
    no_read_ty_le: Mapped[float] = mapped_column(Float)
    no_post_office_so_luong: Mapped[int]
    no_post_office_ty_le: Mapped[float] = mapped_column(Float)
    no_chute_so_luong: Mapped[int]
    no_chute_ty_le: Mapped[float] = mapped_column(Float)
    no_chute_danh_sach: Mapped[str] = mapped_column(Text)
    no_chute_bi_cat: Mapped[bool] = mapped_column(Boolean, default=False)
    sort_failed: Mapped[int]
    pie_correct_pct: Mapped[float] = mapped_column(Float)
    pie_reject_pct: Mapped[float] = mapped_column(Float)


class DmwcsNoChuteItem(Base):
    __tablename__ = "dmwcs_no_chute_items"
    id: Mapped[int] = mapped_column(primary_key=True)
    report_id: Mapped[int] = fk("reports")
    chute_no: Mapped[int]
    co_the_bi_cat: Mapped[bool] = mapped_column(Boolean, default=False)


class DmwcsCapacityDaily(Base):
    __tablename__ = "dmwcs_capacity_daily"
    id: Mapped[int] = mapped_column(primary_key=True)
    report_id: Mapped[int] = fk("reports")
    ngay: Mapped[date] = mapped_column(Date, unique=True)
    cong_suat: Mapped[float] = mapped_column(Float)


class DmwcsBcr(Base):
    __tablename__ = "dmwcs_bcr"
    __table_args__ = (UniqueConstraint("report_id", "bcr_no"),)
    id: Mapped[int] = mapped_column(primary_key=True)
    report_id: Mapped[int] = fk("reports")
    bcr_no: Mapped[int]
    total: Mapped[int]
    success: Mapped[int]
    failed: Mapped[int]
    rate: Mapped[float] = mapped_column(Float)


class ModelStatus(Base):
    """Trạng thái provider/model cho router. model='*' là trạng thái của cả provider."""
    __tablename__ = "model_status"
    __table_args__ = (UniqueConstraint("provider", "model"),)
    id: Mapped[int] = mapped_column(primary_key=True)
    provider: Mapped[str] = mapped_column(String)
    model: Mapped[str] = mapped_column(String)
    state: Mapped[str] = mapped_column(String, default="active")  # active / cooldown / disabled
    cooldown_until: Mapped[datetime | None] = mapped_column(DateTime)
    last_error: Mapped[str | None] = mapped_column(Text)
    fail_count: Mapped[int] = mapped_column(Integer, default=0)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=now, onupdate=now)


# ---------------------------------------------------------------- chatbot (request/DAC_TA_CHATBOT.md mục 10)
class ChatConversation(Base):
    __tablename__ = "chat_conversations"
    id: Mapped[int] = mapped_column(primary_key=True)
    user: Mapped[str | None] = mapped_column(String)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=now)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=now, onupdate=now, index=True)


class ChatMessage(Base):
    __tablename__ = "chat_messages"
    id: Mapped[int] = mapped_column(primary_key=True)
    conversation_id: Mapped[int] = fk("chat_conversations")
    role: Mapped[str] = mapped_column(String)  # user / assistant
    content: Mapped[str] = mapped_column(Text)
    loai: Mapped[str | None] = mapped_column(String)  # sql / hoi_lai / ngoai_pham_vi / loi
    sql: Mapped[str | None] = mapped_column(Text)
    result_preview: Mapped[dict | None] = mapped_column(JSON)  # columns, rows (≤ 50), row_count, truncated, lua_chon
    warnings: Mapped[list | None] = mapped_column(JSON)
    model_sql: Mapped[str | None] = mapped_column(String)
    model_summary: Mapped[str | None] = mapped_column(String)
    llm_calls: Mapped[int | None]
    latency_ms: Mapped[int | None]
    error: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=now, index=True)


class ChatFeedback(Base):
    __tablename__ = "chat_feedback"
    id: Mapped[int] = mapped_column(primary_key=True)
    message_id: Mapped[int] = fk("chat_messages")
    rating: Mapped[str] = mapped_column(String)  # up / down
    note: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=now)


class ChatTokenUsage(Base):
    """Token đã dùng theo ngày + provider + model (free tier Groq giới hạn token/phút và /ngày cho từng model)."""
    __tablename__ = "chat_token_usage"
    __table_args__ = (UniqueConstraint("ngay", "provider", "model"),)
    id: Mapped[int] = mapped_column(primary_key=True)
    ngay: Mapped[date] = mapped_column(Date, index=True)
    provider: Mapped[str] = mapped_column(String)
    model: Mapped[str] = mapped_column(String)
    requests: Mapped[int] = mapped_column(Integer, default=0)
    prompt_tokens: Mapped[int] = mapped_column(Integer, default=0)
    completion_tokens: Mapped[int] = mapped_column(Integer, default=0)
