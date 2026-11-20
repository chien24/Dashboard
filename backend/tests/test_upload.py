"""Upload: chặn trùng theo sha256, chặn file không phải ảnh / quá lớn, header bảo mật. Không gọi OCR (worker không chạy)."""
import io

from fastapi.testclient import TestClient
from PIL import Image
from sqlalchemy.exc import IntegrityError

from app import config
from app.main import app

c = TestClient(app)  # không dùng `with`: không chạy worker/scheduler, job chỉ nằm ở trạng thái pending
c.post("/api/auth/login", json={"username": config.AUTH_USER, "password": config.AUTH_PASSWORD})


def png(color="red") -> bytes:
    buf = io.BytesIO()
    Image.new("RGB", (8, 8), color).save(buf, "PNG")
    return buf.getvalue()


def post(name, data, **form):
    return c.post("/api/upload", files=[("files", (name, data, "image/png"))], data=form)


def test_anh_trung_khong_ocr_lai(clean_db):
    a = post("a.png", png()).json()[0]
    b = post("ban_sao.png", png()).json()[0]  # khác tên, cùng nội dung
    assert not a["duplicate"] and b["duplicate"] and b["upload_id"] == a["upload_id"] and b["job_id"] == a["job_id"]
    f = post("a.png", png(), force="true").json()[0]  # bấm "OCR lại"
    assert not f["duplicate"] and f["upload_id"] == a["upload_id"] and f["job_id"] != a["job_id"]
    assert not post("khac.png", png("blue")).json()[0]["duplicate"]


def test_tu_choi_file_xau(clean_db, monkeypatch):
    files_before = set(config.UPLOAD_DIR.rglob("*.*"))
    assert post("x.png", b"khong phai anh").status_code == 400  # đúng đuôi nhưng không phải ảnh
    assert set(config.UPLOAD_DIR.rglob("*.*")) == files_before  # file hỏng đã bị xóa, không nằm lại trên đĩa
    assert post("x.exe", png()).status_code == 400
    monkeypatch.setattr(config, "MAX_UPLOAD_MB", 0.00001)
    assert post("to.png", png()).status_code == 413


def test_hai_request_cung_luc_cung_anh(clean_db, monkeypatch):
    """Request kia ghi cùng ảnh ngay trước lúc commit: phải trả "trùng", không lỗi 500."""
    first = post("a.png", png()).json()[0]
    from sqlalchemy.orm import Session
    real_commit, calls = Session.commit, []

    def commit_once_fails(self):
        calls.append(1)
        if len(calls) == 1:
            raise IntegrityError("INSERT", {}, Exception("UNIQUE constraint failed: uploads.sha256"))
        return real_commit(self)

    # giả lập: lần tra sha256 đầu không thấy (request kia chưa commit), lần commit đầu đụng unique
    real_scalar, seen = Session.scalar, []

    def scalar_miss_first(self, stmt, *a, **k):
        if not seen and "uploads.sha256" in str(stmt):
            seen.append(1)
            return None
        return real_scalar(self, stmt, *a, **k)

    monkeypatch.setattr(Session, "scalar", scalar_miss_first)
    monkeypatch.setattr(Session, "commit", commit_once_fails)
    r = post("b.png", png())
    assert seen and calls  # đã đi đúng nhánh: tra không thấy rồi commit đụng unique
    assert r.status_code == 200 and r.json()[0]["duplicate"] and r.json()[0]["upload_id"] == first["upload_id"]


def test_header_bao_mat():
    h = c.get("/html/index.html").headers
    assert h["x-content-type-options"] == "nosniff" and h["x-frame-options"] == "DENY" and h["cache-control"] == "no-cache"


def _report(upload_id: int) -> int:
    from datetime import date

    from app.db import SessionLocal
    from app.models import Report
    with SessionLocal() as db:
        r = Report(upload_id=upload_id, loai="dmwcs_capacity", report_date=date(2026, 11, 16), data={})
        db.add(r)
        db.commit()
        return r.id


def test_xoa_report_cuoi_cung_thi_xoa_anh(clean_db):
    """Xóa report rồi tải lại đúng ảnh đó: là ảnh mới (không báo trùng trỏ vào report đã xóa)."""
    from app.db import SessionLocal
    from app.models import Job, Upload
    a = post("a.png", png()).json()[0]
    with SessionLocal() as db:  # job chạy xong (test không chạy worker)
        db.get(Job, a["job_id"]).status = "done"
        db.commit()
        path = config.UPLOAD_DIR / db.get(Upload, a["upload_id"]).stored_path
    r1, r2 = _report(a["upload_id"]), _report(a["upload_id"])  # r2 = lần OCR lại

    assert c.delete(f"/api/reports/{r2}").json() == {"deleted": r2, "upload_deleted": False}  # còn r1
    b = post("a.png", png()).json()[0]
    assert b["duplicate"] and b["report_id"] == r1

    assert c.delete(f"/api/reports/{r1}").json()["upload_deleted"]
    assert not path.exists()
    with SessionLocal() as db:
        assert db.get(Upload, a["upload_id"]) is None and db.get(Job, a["job_id"]) is None
    assert not post("a.png", png()).json()[0]["duplicate"]


def test_xoa_report_khi_anh_dang_ocr_lai_thi_giu_anh(clean_db):
    a = post("a.png", png()).json()[0]  # job đang pending
    r = _report(a["upload_id"])
    assert not c.delete(f"/api/reports/{r}").json()["upload_deleted"]
