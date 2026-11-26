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


def test_doi_ten_va_xoa_hoi_thoai(clean_db):
    c = client()
    with SessionLocal() as db:
        a = ChatConversation(updated_at=now() - timedelta(days=2))
        db.add(a)
        db.flush()
        db.add(ChatMessage(conversation_id=a.id, role="user", content="NoRead hôm qua?"))
        db.commit()
        cid, t0 = a.id, a.updated_at
    title = lambda: c.get("/api/chat/conversations").json()[0]["title"]
    assert c.patch(f"/api/chat/conversations/{cid}", json={"title": "  Báo cáo NoRead "}).status_code == 200
    assert title() == "Báo cáo NoRead"
    with SessionLocal() as db:
        assert db.get(ChatConversation, cid).updated_at == t0  # đổi tên không đẩy lên đầu danh sách
    c.patch(f"/api/chat/conversations/{cid}", json={"title": ""})
    assert title() == "NoRead hôm qua?"                          # để trống: về tên mặc định
    assert c.delete(f"/api/chat/conversations/{cid}").status_code == 200
    assert c.get("/api/chat/conversations").json() == []
    with SessionLocal() as db:
        assert db.query(ChatMessage).count() == 0                # CASCADE xóa tin nhắn
    assert c.delete(f"/api/chat/conversations/{cid}").status_code == 404
    assert c.patch(f"/api/chat/conversations/{cid}", json={"title": "x"}).status_code == 404


def test_xoa_hoi_thoai_sau_30_ngay(clean_db):
    from app.services.retention import cleanup
    with SessionLocal() as db:
        db.add_all([ChatConversation(updated_at=now() - timedelta(days=31)), ChatConversation(updated_at=now() - timedelta(days=29))])
        db.commit()
        assert cleanup(db)["chat_conversations"] == 1
        assert db.query(ChatConversation).count() == 1


CAP = {"tu_ngay": "2026-11-15", "den_ngay": "2026-11-16",
       "cong_suat_theo_ngay": [{"ngay": "2026-11-15", "cong_suat": 5000.0}, {"ngay": "2026-11-16", "cong_suat": 6000.0}]}


def test_danh_dau_ban_ocr_dang_dung(clean_db):
    """2 lần OCR giống hệt nhau thì chỉ 1 bản 'Đang dùng'; sửa tay thì không bản nào; chọn bản nào thì đánh dấu bản đó."""
    c = client()
    with SessionLocal() as db:
        up = Upload(original_name="a.png", stored_path="x", sha256="h")
        db.add(up)
        db.flush()
        r = Report(upload_id=up.id, loai="dmwcs_capacity", report_date=date(2026, 11, 16), data=CAP,
                   raw_json_1={**CAP, "canh_bao_ocr": []}, raw_json_2={**CAP, "canh_bao_ocr": []})
        db.add(r)
        db.commit()
        rid = r.id
    get = lambda: c.get(f"/api/reports/{rid}").json()
    put = lambda data, **q: c.put(f"/api/reports/{rid}", json=data, params={"updated_at": get()["updated_at"], **q})

    assert get()["ocr_dang_dung"] == f"{rid}:1"                      # vừa OCR xong: dùng lần 1
    assert put(CAP, ocr_version=f"{rid}:2").json()["ocr_dang_dung"] == f"{rid}:2"
    assert put(CAP).json()["ocr_dang_dung"] == f"{rid}:2"            # bấm Lưu không đổi số: giữ đánh dấu
    sua = {**CAP, "cong_suat_theo_ngay": [CAP["cong_suat_theo_ngay"][0], {"ngay": "2026-11-16", "cong_suat": 6100}]}
    assert put(sua).json()["ocr_dang_dung"] is None                  # sửa số: bản sửa tay
    assert put(CAP, ocr_version="999:1").status_code == 422


def test_db_cu_duoc_them_cot_ocr_version(tmp_path):
    from sqlalchemy import inspect, text

    from app.db import init_db, make_engine
    eng = make_engine(f"sqlite:///{(tmp_path / 'cu.db').as_posix()}")
    init_db(eng)
    with eng.begin() as c:
        c.execute(text("ALTER TABLE reports DROP COLUMN ocr_version"))  # giả DB tạo trước khi có cột
    init_db(eng)
    assert "ocr_version" in {x["name"] for x in inspect(eng).get_columns("reports")}


def test_luu_lien_tiep_khong_bao_nham_may_khac(clean_db):
    """Lưu 2 lần liền không đổi số: lần sau dùng updated_at trả về từ lần trước, không được 409."""
    c = client()
    with SessionLocal() as db:
        r = Report(loai="dmwcs_capacity", report_date=date(2026, 11, 16), data=CAP)
        db.add(r)
        db.commit()
        rid = r.id
    t = c.get(f"/api/reports/{rid}").json()["updated_at"]
    for _ in range(3):
        res = c.put(f"/api/reports/{rid}", json=CAP, params={"updated_at": t})
        assert res.status_code == 200, res.text
        t = res.json()["updated_at"]
