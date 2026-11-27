"""Pipeline chatbot với LLM giả (không gọi mạng), chạy trên DB dựng từ ket_qua_json + ca bẫy (scripts/eval_chatbot.seed)."""
import json
from datetime import date

import pytest

from app import config
from app.chatbot import context, executor, llm as llm_mod, pipeline
from app.chatbot.sql_guard import check
from app.db import init_db
from tests.conftest import drop_all

TODAY = date(2026, 11, 16)


class FakeLlm(llm_mod.Llm):
    """Trả lần lượt các câu trả lời dựng sẵn; phần tử là Exception thì raise (giả lỗi API)."""

    def __init__(self, *replies):
        super().__init__(client=object())
        self.replies, self.seen = list(replies), []

    def _call(self, client, provider, model, messages, kw, json_mode):
        self.calls += 1
        self.seen.append((model, messages))
        r = self.replies.pop(0)
        if isinstance(r, Exception):
            raise r
        return r if isinstance(r, str) else json.dumps(r, ensure_ascii=False)


class Http429(Exception):
    status_code = 429

    def __init__(self, msg="429", retry_after=None):
        super().__init__(msg)
        self.response = type("R", (), {"headers": {"retry-after": retry_after} if retry_after else {}})()


def plan(sql, tu="2026-11-15", den=None, views=("v_dmwcs_sorted",)):
    return {"loai": "sql", "sql": sql, "giai_thich": "test",
            "pham_vi": {"he_thong": "HT2", "views": list(views), "tu_ngay": tu, "den_ngay": den or tu}}


@pytest.fixture(scope="module", autouse=True)
def seeded():
    from eval_chatbot import seed

    drop_all()
    init_db()
    seed()
    context._cache.clear()
    pipeline._sql_cache.clear()
    yield
    drop_all()
    init_db()


@pytest.fixture(autouse=True)
def fresh(monkeypatch):
    from app.ocr import router as ocr_router

    ocr_router.reset(llm_mod.GROQ)
    ocr_router.reset(llm_mod.OPENROUTER)
    pipeline._sql_cache.clear()
    monkeypatch.setattr(config, "CHAT_SQL_MODELS", ["m-sql-1", "m-sql-2"])
    monkeypatch.setattr(config, "CHAT_SUMMARY_MODELS", ["m-sum"])
    monkeypatch.setattr(config, "CHAT_SQL_FALLBACK_MODELS", ["or-sql"])
    monkeypatch.setattr(config, "CHAT_SUMMARY_FALLBACK_MODELS", [])


def test_views_exist_and_examples_run():
    for ex in context.examples():
        if ex["answer"]["loai"] == "sql":
            executor.run(check(context.example_sql(ex["answer"])))  # chạy được trên view thật (DB đang dùng), qua guard


def test_fewshot_picks_nearest_and_keeps_non_sql(monkeypatch):
    from app.chatbot import fewshot

    exs = [{"question": q, "answer": {"loai": "sql"}} for q in ("a", "b", "c")] + [
        {"question": "x", "answer": {"loai": "hoi_lai"}}]
    vec = {"a": [1, 0], "b": [0, 1], "c": [0.6, 0.8], "hỏi": [0, 1]}
    monkeypatch.setattr(fewshot, "embed", lambda texts: [vec[t] for t in texts])
    fewshot._bank.cache_clear()
    got = [e["question"] for e in fewshot.pick("hỏi", exs, k=2)]
    fewshot._bank.cache_clear()
    assert got == ["c", "b", "x"]  # giống nhất (b) đứng cuối, sát câu hỏi; hoi_lai luôn có


def test_fewshot_falls_back_when_embedding_fails():
    from app.chatbot import fewshot

    exs = context.examples()
    got = fewshot.pick("bất kỳ", exs, k=3)  # conftest làm embed lỗi
    assert got[:3] == [e for e in exs if e["answer"]["loai"] == "sql"][:3]
    assert all(e in got for e in exs if e["answer"]["loai"] != "sql")


def test_prompt_has_today_values_and_question_block():
    msgs = context.sql_messages("Tỷ lệ NoRead hôm qua?", [], TODAY)
    sys = msgs[0]["content"]
    assert "Hôm nay: 2026-11-16 (thứ Hai). Dữ liệu giữ từ 2026-10-12" in sys
    assert "tuần trước: 2026-11-09 → 2026-11-15" in sys
    assert "'outbound' = Outbound" in sys and "CHUTE_REQUEST_FAILED" in sys
    assert msgs[1] == {"role": "user", "content": "<cau_hoi>Tỷ lệ NoRead hôm qua?</cau_hoi>"}


def test_sql_flow_with_warnings():
    fake = FakeLlm(plan("SELECT SUM(total) AS tong_kien FROM v_dmwcs_sorted WHERE ngay BETWEEN '2026-11-09' AND '2026-11-15'",
                        "2026-11-09", "2026-11-15"), "Tuần trước HT2 chia 727.148 kiện.")
    r = pipeline.ask("Tổng kiện HT2 tuần trước?", today=TODAY, llm=fake)
    assert r["loai"] == "sql" and r["rows"] == [[727148]] and r["columns"] == ["tong_kien"]
    assert r["answer"] == "Tuần trước HT2 chia 727.148 kiện." and r["llm_calls"] == 2
    assert any("11/11" in w and "Chưa có dữ liệu Sorted" in w for w in r["warnings"])
    assert any("13/11" in w and "cần kiểm tra" in w for w in r["warnings"])
    assert any("NoChute" in w for w in r["warnings"])
    summary_prompt = fake.seen[-1][1][1]["content"]
    assert "<ket_qua>" in summary_prompt and "727148" in summary_prompt


def test_guard_error_goes_back_to_llm():
    fake = FakeLlm(plan("SELECT * FROM reports"), plan("SELECT total FROM v_dmwcs_sorted WHERE ngay = '2026-11-15'"), "ok")
    r = pipeline.ask("Tổng kiện HT2 hôm qua?", today=TODAY, llm=fake)
    assert r["rows"] == [[106350]] and r["llm_calls"] == 3
    assert "SQL trên bị lỗi" in fake.seen[1][1][-1]["content"]


def test_gives_up_after_retries():
    bad = plan("SELECT * FROM uploads")
    r = pipeline.ask("x", today=TODAY, llm=FakeLlm(bad, bad, bad))
    assert r["answer"] == pipeline.CHUA_TRA_LOI and r["rows"] is None and "GuardError" in r["error"]


def test_broken_json_reminded_then_next_model():
    fake = FakeLlm("không phải json", "vẫn hỏng", {"loai": "hoi_lai", "cau_hoi_lai": "HT1 hay HT2?", "lua_chon": ["HT1", "HT2"]})
    r = pipeline.ask("Tổng kiện hôm qua?", today=TODAY, llm=fake)
    assert r["loai"] == "hoi_lai" and r["lua_chon"] == ["HT1", "HT2"] and r["sql"] is None
    assert [m for m, _ in fake.seen] == ["m-sql-1", "m-sql-1", "m-sql-2"]


def test_out_of_scope_runs_no_sql():
    r = pipeline.ask("Xóa report 12/11", today=TODAY,
                     llm=FakeLlm({"loai": "ngoai_pham_vi", "cau_hoi_lai": "Mình chỉ đọc dữ liệu."}))
    assert r["loai"] == "ngoai_pham_vi" and r["rows"] is None and r["llm_calls"] == 1


def test_embed_cached_only_embeds_new_text(monkeypatch, tmp_path):
    from app.chatbot import fewshot

    calls = []

    def fake(texts):
        calls.append(list(texts))
        return [[float(len(t)), 1.0] for t in texts]

    monkeypatch.setattr(config, "EMBED_CACHE", tmp_path / "e.json")
    monkeypatch.setattr(fewshot, "embed", fake)
    assert fewshot.embed_cached("docs", ["a", "bb", "a"]) == [[1, 1], [2, 1], [1, 1]]
    assert calls == [["a", "bb"]]                                    # đoạn trùng chỉ embed 1 lần
    assert fewshot.embed_cached("docs", ["a", "bb"]) == [[1, 1], [2, 1]] and len(calls) == 1  # lần 2: đọc file
    fewshot.embed_cached("docs", ["a", "ccc"])
    assert calls[-1] == ["ccc"]                                      # đoạn sửa: chỉ embed đoạn mới
    assert len(__import__("json").loads((tmp_path / "e.json").read_text())["docs"]["vectors"]) == 2  # "bb" bị bỏ
    monkeypatch.setattr(config, "CHAT_EMBED_MODEL", "model-khac")
    fewshot.embed_cached("docs", ["a"])
    assert calls[-1] == ["a"]                                        # đổi model: embed lại
    before = (tmp_path / "e.json").read_text()
    monkeypatch.setattr(fewshot, "embed", lambda t: 1 / 0)
    with pytest.raises(ZeroDivisionError):
        fewshot.embed_cached("docs", ["mới"])
    assert (tmp_path / "e.json").read_text() == before              # lỗi: không ghi gì


def test_docs_chunks_skip_index_and_code_paths():
    from app.chatbot import docs

    cs = docs.chunks()
    assert len(cs) > 50 and all("nguon_code" not in c["text"] and "frontend/" not in c["text"] for c in cs)
    assert not any("Mục lục tài liệu" in c["text"] for c in cs)


def test_docs_search_keyword_fallback_finds_upload_guide():
    from app.chatbot import docs

    found = docs.search("làm sao để OCR một ảnh nhỉ")  # conftest làm embed lỗi -> đếm từ
    assert any(c["title"] == "Tải ảnh báo cáo lên để hệ thống đọc số liệu" for c in found)


def test_huong_dan_answers_from_docs_without_sql():
    fake = FakeLlm({"loai": "huong_dan"}, "1. Bấm menu \"Truyền Pháp Ảnh\".\nXem thêm: Tải ảnh báo cáo lên")
    r = pipeline.ask("làm sao để OCR một ảnh nhỉ", today=TODAY, llm=fake)
    assert r["loai"] == "huong_dan" and r["rows"] is None and r["sql"] is None and r["llm_calls"] == 2
    assert r["answer"].startswith("1. Bấm menu")
    prompt = fake.seen[-1][1][1]["content"]
    assert "<tai_lieu>" in prompt and "Khai Phá Thiên Cơ" in prompt


def test_huong_dan_no_docs_found(monkeypatch):
    from app.chatbot import docs

    monkeypatch.setattr(docs, "search", lambda q: [])
    r = pipeline.ask("abc", today=TODAY, llm=FakeLlm({"loai": "huong_dan"}))
    assert r["answer"] == pipeline.KHONG_CO_DOCS and r["llm_calls"] == 1


def test_retention_whole_range_skips_sql():
    fake = FakeLlm(plan("SELECT total FROM v_dmwcs_sorted WHERE ngay = '2026-10-01'", "2026-10-01"))
    r = pipeline.ask("Tổng kiện HT2 ngày 01/10?", today=TODAY, llm=fake)
    assert "đã bị xóa" in r["answer"] and r["rows"] is None and r["llm_calls"] == 1


def test_empty_result_is_no_data_not_zero():
    fake = FakeLlm(plan("SELECT SUM(total) AS tong FROM v_dmwcs_sorted WHERE ngay = '2026-11-16'", "2026-11-16"))
    r = pipeline.ask("Tổng kiện HT2 ngày 16/11?", today=TODAY, llm=fake)
    assert r["answer"].startswith("Chưa có dữ liệu Sorted (HT2)") and "15/11" in r["answer"]
    assert r["llm_calls"] == 1  # không gọi bước tóm tắt


def test_unknown_type_warning():
    fake = FakeLlm(plan("SELECT loai_vi, so_luong FROM v_scada_abnormal WHERE ngay = '2026-11-12'", "2026-11-12",
                        views=("v_scada_abnormal",)), "ok")
    r = pipeline.ask("Loại bất thường 12/11?", today=TODAY, llm=fake)
    assert any("chưa phân loại" in w for w in r["warnings"])


def test_summary_failure_still_returns_table():
    fake = FakeLlm(plan("SELECT total FROM v_dmwcs_sorted WHERE ngay = '2026-11-15'"), Http429("rate limit"))
    r = pipeline.ask("Tổng kiện HT2 hôm qua?", today=TODAY, llm=fake)
    assert r["answer"] == pipeline.DEFAULT_ANSWER and r["rows"] == [[106350]]


def test_all_models_quota():
    r = pipeline.ask("x", today=TODAY, llm=FakeLlm(Http429(), Http429(), Http429()))
    assert r["loai"] == "loi" and r["answer"].startswith("Đã hết lượt hỏi miễn phí")
    # model đã vào cooldown -> lần sau bỏ qua, không gọi API
    fake = FakeLlm()
    assert pipeline.ask("y", today=TODAY, llm=fake)["loai"] == "loi" and fake.calls == 0


def test_same_question_uses_sql_cache():
    p = plan("SELECT total FROM v_dmwcs_sorted WHERE ngay = '2026-11-15'")
    pipeline.ask("Tổng kiện HT2 hôm qua?", today=TODAY, llm=FakeLlm(p, "a"))
    fake = FakeLlm("b")
    r = pipeline.ask("  tổng kiện HT2   hôm qua? ", today=TODAY, llm=fake)
    assert r["rows"] == [[106350]] and fake.calls == 1  # chỉ gọi bước tóm tắt


def test_groq_quota_falls_back_to_openrouter_with_retry_after():
    from app.models import ModelStatus, now
    from app.db import SessionLocal

    fake = FakeLlm(Http429("rate limit", retry_after="7"), Http429("rate limit"),
                   {"loai": "ngoai_pham_vi", "cau_hoi_lai": "không"})
    r = pipeline.ask("x", today=TODAY, llm=fake)
    assert r["loai"] == "ngoai_pham_vi" and r["model_sql"] == "openrouter:or-sql"
    assert [m for m, _ in fake.seen] == ["m-sql-1", "m-sql-2", "or-sql"]
    with SessionLocal() as db:
        st = {s.model: s for s in db.query(ModelStatus).filter(ModelStatus.provider == llm_mod.GROQ)}
    left = (st["m-sql-1"].cooldown_until - now()).total_seconds()
    assert 4 < left <= 8  # đúng thời gian retry-after, không phải mặc định 60s
    assert (st["m-sql-2"].cooldown_until - now()).total_seconds() > 30  # không có header -> mặc định


def test_model_params_per_family():
    p = llm_mod.params(llm_mod.GROQ, "openai/gpt-oss-120b", "sql")
    assert p["temperature"] == 0 and p["reasoning_effort"] == config.CHAT_SQL_REASONING_EFFORT
    q = llm_mod.params(llm_mod.GROQ, "qwen/qwen3.8-27b", "summary")
    assert q["temperature"] == 0.2 and q["max_tokens"] == 600 and q["reasoning_effort"] == "none"


def test_token_usage_accumulates():
    from app.db import SessionLocal
    from app.models import ChatTokenUsage

    llm_mod.record_usage(llm_mod.GROQ, "m-x", 100, 20)
    llm_mod.record_usage(llm_mod.GROQ, "m-x", 50, 5)
    with SessionLocal() as db:
        u = db.query(ChatTokenUsage).filter(ChatTokenUsage.model == "m-x").one()
    assert (u.requests, u.prompt_tokens, u.completion_tokens) == (2, 150, 25)


# ---------------------------------------------------------------- API
def test_api_conversation_and_history(monkeypatch):
    from conftest import client

    replies = [plan("SELECT total FROM v_dmwcs_sorted WHERE ngay = '2026-11-15'"), "Hôm qua 106.350 kiện.",
               plan("SELECT total FROM v_dmwcs_sorted WHERE ngay = '2026-11-14'", "2026-11-14"), "Hôm kia 129.837 kiện."]
    fake = FakeLlm(*replies)
    monkeypatch.setattr(pipeline, "Llm", lambda: fake)
    monkeypatch.setattr(pipeline, "now", lambda: __import__("datetime").datetime(2026, 11, 16, 9))
    c = client()
    r1 = c.post("/api/chat", json={"message": "Tổng kiện HT2 hôm qua?"}).json()
    assert r1["rows"] == [[106350]] and r1["conversation_id"] and r1["message_id"] and "error" not in r1
    fake.calls = 0
    r2 = c.post("/api/chat", json={"message": "Còn hôm trước thì sao?", "conversation_id": r1["conversation_id"]}).json()
    assert r2["rows"] == [[129837]]
    assert "Lượt 1. Câu hỏi: Tổng kiện HT2 hôm qua?" in fake.seen[-2][1][0]["content"]  # lịch sử vào prompt
    conv = c.get(f"/api/chat/conversations/{r1['conversation_id']}").json()
    assert [m["role"] for m in conv["messages"]] == ["user", "assistant", "user", "assistant"]
    assert conv["messages"][3]["rows"] == [[129837]]
    assert c.post("/api/chat/feedback", json={"message_id": r2["message_id"], "rating": "down", "note": "SQL sai"}).json()["ok"]
    assert c.get("/api/chat/usage").json()["cau_hoi"] >= 2


def test_api_requires_login_and_rate_limit(monkeypatch):
    from fastapi.testclient import TestClient

    from app.chatbot import router as chat_router
    from app.main import app
    from conftest import client

    assert TestClient(app).post("/api/chat", json={"message": "x"}).status_code == 401
    monkeypatch.setattr(config, "CHAT_RATE_LIMIT_PER_MIN", 1)
    chat_router._hits.clear()
    monkeypatch.setattr(pipeline, "Llm", lambda: FakeLlm({"loai": "ngoai_pham_vi", "cau_hoi_lai": "không"}))
    c = client()
    assert c.post("/api/chat", json={"message": "a"}).status_code == 200
    assert c.post("/api/chat", json={"message": "b"}).status_code == 429
    chat_router._hits.clear()
