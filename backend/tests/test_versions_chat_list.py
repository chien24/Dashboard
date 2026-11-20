"""OCR Version của report, danh sách hội thoại chatbot (mọi máy), xóa hội thoại sau 30 ngày không dùng."""
from datetime import date, timedelta

from app.db import SessionLocal
from app.models import ChatConversation, ChatMessage, Report, Upload, now
from tests.conftest import client


def test_versions_gom_moi_lan_ocr_cua_anh(clean_db):
    c = client()
    with SessionLocal() as db:
        up = Upload(original_name="a.png", stored_path="x", sha256="h")
        db.add(up)
        db.flush()
        mk = lambda d1, d2: Report(upload_id=up.id, loai="dmwcs_capacity", report_date=date(2026, 11, 16), data={"a": 1},
                                   raw_json_1={"a": d1, "canh_bao_ocr": ["mờ"]}, raw_json_2=d2 and {"a": d2})
        r1, r2 = mk(1, 2), mk(3, None)  # r2 = lần "OCR lại", lần 2 lỗi
        db.add_all([r1, r2])
        db.commit()
        ids = r1.id, r2.id
    v = c.get(f"/api/reports/{ids[1]}").json()["versions"]
    assert [(x["report_id"], x["lan"], x["data"]) for x in v] == [(ids[0], 1, {"a": 1}), (ids[0], 2, {"a": 2}), (ids[1], 1, {"a": 3})]


def test_danh_sach_hoi_thoai_moi_may(clean_db):
    c = client()
    with SessionLocal() as db:
        a, b, rong = ChatConversation(updated_at=now() - timedelta(days=2)), ChatConversation(), ChatConversation()
        db.add_all([a, b, rong])
        db.flush()
        db.add_all([ChatMessage(conversation_id=a.id, role="user", content="NoRead hôm qua?"),
                    ChatMessage(conversation_id=a.id, role="assistant", content="..."),
                    ChatMessage(conversation_id=a.id, role="user", content="còn tuần trước?"),
                    ChatMessage(conversation_id=b.id, role="user", content="Công suất AVG")])
        db.commit()
        ids = a.id, b.id
    r = c.get("/api/chat/conversations").json()
    assert [(x["conversation_id"], x["title"], x["so_cau_hoi"]) for x in r] == [(ids[1], "Công suất AVG", 1), (ids[0], "NoRead hôm qua?", 2)]


def test_xoa_hoi_thoai_sau_30_ngay(clean_db):
    from app.services.retention import cleanup
    with SessionLocal() as db:
        db.add_all([ChatConversation(updated_at=now() - timedelta(days=31)), ChatConversation(updated_at=now() - timedelta(days=29))])
        db.commit()
        assert cleanup(db)["chat_conversations"] == 1
        assert db.query(ChatConversation).count() == 1
