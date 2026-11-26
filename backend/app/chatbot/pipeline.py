"""Điều phối 1 câu hỏi (mục 4): LLM 1 sinh SQL -> sql_guard -> chạy read-only -> checks -> LLM 2 tóm tắt."""
import json
import logging
import math
import sqlite3
import time
from datetime import date

from app import config
from app.chatbot import checks, context, docs, executor
from app.chatbot.llm import AllModelsFailed, Llm
from app.chatbot.sql_guard import GuardError, check, wrap_limit
from app.models import now
from app.ocr.providers.base import BadOutput, extract_json

log = logging.getLogger("chatbot")
LOAI = ("sql", "hoi_lai", "ngoai_pham_vi", "huong_dan")
KHONG_CO_DOCS = "Hướng dẫn sử dụng chưa nói tới việc này. Bạn thử hỏi cụ thể hơn: tên trang, tên nút hoặc thông báo đang thấy."
DEFAULT_ANSWER = "Đây là kết quả truy vấn."
CHUA_TRA_LOI = ("Mình chưa trả lời được câu này. Bạn thử diễn đạt lại cụ thể hơn: nêu hệ thống (HT1 SCADA hay HT2 DMWCS), "
                "chỉ số và ngày, ví dụ \"Tỷ lệ REJECT HT2 ngày 12/11\".")
SQL_CACHE_S = 600
_sql_cache: dict = {}  # (hôm nay, câu hỏi chuẩn hóa) -> (thời điểm, plan)


def parse_plan(text: str) -> dict:
    """JSON của LLM 1 -> plan đã kiểm cấu trúc; sai thì BadOutput (llm.chat nhắc lại / đổi model)."""
    p = extract_json(text)
    if not isinstance(p, dict) or p.get("loai") not in LOAI:
        raise BadOutput("JSON thiếu 'loai' hợp lệ (sql | hoi_lai | ngoai_pham_vi | huong_dan)")
    if p["loai"] == "huong_dan":
        return p
    if p["loai"] == "sql":
        if not isinstance(p.get("sql"), str) or not p["sql"].strip():
            raise BadOutput("loai = sql nhưng thiếu 'sql'")
        if not checks.scope(p.get("pham_vi"), date.today()):
            raise BadOutput("loai = sql nhưng thiếu pham_vi.tu_ngay / den_ngay dạng YYYY-MM-DD")
    elif not isinstance(p.get("cau_hoi_lai"), str) or not p["cau_hoi_lai"].strip():
        raise BadOutput(f"loai = {p['loai']} nhưng thiếu 'cau_hoi_lai'")
    return p


def _norm(q: str) -> str:
    return " ".join(q.lower().split())


def _jsonable(v):
    return None if isinstance(v, float) and not math.isfinite(v) else v


def ask(question: str, history: list[dict] | None = None, today: date | None = None, llm: Llm | None = None) -> dict:
    """-> dict đúng dạng response của POST /api/chat (chưa có conversation_id/message_id) + llm_calls, error."""
    t0 = time.monotonic()
    today = today or now().date()
    history = (history or [])[-config.CHAT_HISTORY_TURNS:]
    llm = llm or Llm()
    out = {"loai": "sql", "answer": "", "sql": None, "columns": None, "rows": None, "row_count": 0, "truncated": False,
           "warnings": [], "chart": {"kieu": "none", "x": None, "y": []}, "lua_chon": None, "model_sql": None,
           "model_summary": None, "error": None}

    def done():
        out.update(latency_ms=int((time.monotonic() - t0) * 1000), llm_calls=llm.calls, tokens=llm.tokens)
        return out

    # ---- bước 2–3: ngữ cảnh + LLM 1 (câu hỏi đầu hội thoại giống hệt trong 10 phút -> dùng lại SQL)
    key = (today, _norm(question))
    cached = _sql_cache.get(key) if not history else None
    try:
        if cached and time.monotonic() - cached[0] < SQL_CACHE_S:
            plan, out["model_sql"] = cached[1], cached[2]
        else:
            messages = context.sql_messages(question, history, today)
            plan, out["model_sql"] = llm.chat("sql", messages, parse=parse_plan)
    except AllModelsFailed as e:
        return done() | _all_failed(e)

    if plan["loai"] == "huong_dan":  # hỏi cách dùng: trả lời theo docs/user-guide, không chạy SQL
        out["loai"] = "huong_dan"
        found = docs.search(question)
        if not found:
            out["answer"] = KHONG_CO_DOCS
            return done()
        try:
            out["answer"], out["model_summary"] = llm.chat("summary", docs.messages(question, found))
        except AllModelsFailed as e:
            return done() | _all_failed(e)
        out["answer"] = (out["answer"] or "").strip() or KHONG_CO_DOCS
        return done()

    for attempt in range(config.CHAT_SQL_RETRIES + 1):
        if plan["loai"] != "sql":
            out.update(loai=plan["loai"], answer=plan["cau_hoi_lai"].strip(),
                       lua_chon=[str(x) for x in plan.get("lua_chon") or []][:5] or None)
            return done()
        out["sql"] = plan["sql"].strip()
        if isinstance(plan.get("bieu_do"), dict):
            out["chart"] = plan["bieu_do"]
        warns, stop = checks.before_run(plan.get("pham_vi"), today)
        if stop:
            out.update(answer=stop, warnings=warns)
            return done()
        # ---- bước 4–5: kiểm tra + chạy; lỗi thì gửi lại cho LLM sửa (chung 1 bộ đếm)
        try:
            sql = check(plan["sql"])
            cols, rows, truncated = executor.run(wrap_limit(sql, config.CHAT_MAX_ROWS), max_rows=config.CHAT_MAX_ROWS)
            break
        except (GuardError, sqlite3.Error, executor.SqlTimeout) as e:
            err = f"{type(e).__name__}: {e}"
            log.info("SQL lỗi (lần %d): %s", attempt + 1, err)
            if attempt == config.CHAT_SQL_RETRIES:
                out.update(answer=CHUA_TRA_LOI, error=err[:1000])
                return done()
            messages = context.sql_messages(question, history, today) + [
                {"role": "assistant", "content": json.dumps(plan, ensure_ascii=False)},
                {"role": "user", "content": f"SQL trên bị lỗi: {err[:500]}\nSửa lại theo đúng luật, trả về JSON đầy đủ."}]
            try:
                plan, out["model_sql"] = llm.chat("sql", messages, parse=parse_plan)
            except AllModelsFailed as e2:
                return done() | _all_failed(e2)
    if not history:
        _sql_cache[key] = (time.monotonic(), plan, out["model_sql"])

    # ---- bước 6: cảnh báo
    rows = [[_jsonable(v) for v in r] for r in rows]
    warns += checks.after_run(plan.get("pham_vi"), today)
    out.update(columns=cols, rows=rows, row_count=len(rows), truncated=truncated, warnings=warns)
    if checks.is_empty(rows):
        out["answer"] = checks.empty_answer(plan.get("pham_vi"), today, context.db_values()["day_chuyen"])
        return done()

    # ---- bước 7: tóm tắt; lỗi thì vẫn trả bảng + SQL
    try:
        msgs = context.summary_messages(question, plan, cols, rows, len(rows), truncated, warns)
        out["answer"], out["model_summary"] = llm.chat("summary", msgs)
    except AllModelsFailed as e:
        log.warning("Tóm tắt lỗi: %s", e)
        out["error"] = f"tóm tắt: {e}"[:1000]
    out["answer"] = out["answer"] or DEFAULT_ANSWER
    return done()


def _all_failed(e: AllModelsFailed) -> dict:
    if e.quota:
        mins = max(1, math.ceil((e.retry_at - now()).total_seconds() / 60)) if e.retry_at else None
        msg = "Đã hết lượt hỏi miễn phí" + (f", thử lại sau khoảng {mins} phút." if mins else ", thử lại sau ít phút.")
    else:
        msg = "Chatbot chưa gọi được model nào. Báo quản trị kiểm tra API key và danh sách model trong .env."
    return {"loai": "loi", "answer": msg, "error": str(e)[:1000]}
