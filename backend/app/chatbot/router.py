"""POST /api/chat, GET /api/chat/conversations/{id}, POST /api/chat/feedback, GET /api/chat/usage.
Đăng nhập do middleware require_login của app chặn (mọi /api/ đều cần cookie phiên)."""
import time
from collections import defaultdict, deque
from datetime import datetime, time as dtime

from fastapi import APIRouter, Body, Depends, HTTPException, Request
from sqlalchemy import func, select

from app import config
from app.chatbot import pipeline
from app.db import get_db
from app.models import ChatConversation, ChatFeedback, ChatMessage, ChatTokenUsage, now

router = APIRouter(prefix="/api/chat", tags=["chat"])
MAX_LEN = 1000
# shortcut: rate limit theo IP trong RAM (mất khi restart, sau tunnel nhiều người có thể chung IP); cần chặt hơn thì đưa vào DB/proxy.
_hits: dict[str, deque] = defaultdict(deque)


def _rate_limit(ip: str):
    q, t = _hits[ip], time.monotonic()
    while q and q[0] < t - 60:
        q.popleft()
    if len(q) >= config.CHAT_RATE_LIMIT_PER_MIN:
        wait = int(60 - (t - q[0])) + 1
        raise HTTPException(429, {"message": f"Hỏi nhanh quá, chờ {wait} giây rồi hỏi tiếp", "retry_after": wait},
                            headers={"Retry-After": str(wait)})
    q.append(t)


def _history(db, conv_id: int) -> list[dict]:
    """N lượt gần nhất: câu hỏi + SQL + tóm tắt (không gửi lại rows)."""
    msgs = db.scalars(select(ChatMessage).where(ChatMessage.conversation_id == conv_id)
                      .order_by(ChatMessage.id.desc()).limit(config.CHAT_HISTORY_TURNS * 2)).all()[::-1]
    out, q = [], None
    for m in msgs:
        if m.role == "user":
            q = m.content
        elif q is not None:
            out.append({"question": q, "sql": m.sql, "summary": m.content})
            q = None
    return out


def _view(m: ChatMessage) -> dict:
    p = m.result_preview or {}
    return {"message_id": m.id, "role": m.role, "content": m.content, "loai": m.loai, "sql": m.sql,
            "columns": p.get("columns"), "rows": p.get("rows"), "row_count": p.get("row_count", 0),
            "truncated": p.get("truncated", False), "lua_chon": p.get("lua_chon"), "warnings": m.warnings or [],
            "model_sql": m.model_sql, "model_summary": m.model_summary, "latency_ms": m.latency_ms,
            "created_at": m.created_at}


@router.post("")
def chat(request: Request, message: str = Body(..., embed=True), conversation_id: int | None = Body(None, embed=True),
         db=Depends(get_db)):
    message = (message or "").strip()
    if not message:
        raise HTTPException(422, "Câu hỏi rỗng")
    if len(message) > MAX_LEN:
        raise HTTPException(422, f"Câu hỏi dài quá {MAX_LEN} ký tự")
    _rate_limit(request.client.host if request.client else "?")
    conv = db.get(ChatConversation, conversation_id) if conversation_id else None
    if conversation_id and not conv:
        raise HTTPException(404, "Không có cuộc trò chuyện này (có thể đã bị xóa theo chính sách lưu trữ)")
    if not conv:
        conv = ChatConversation(user=config.AUTH_USER)
        db.add(conv)
        db.flush()
    history = _history(db, conv.id)
    db.add(ChatMessage(conversation_id=conv.id, role="user", content=message))
    db.commit()  # lưu câu hỏi trước: LLM có lỗi lạ thì vẫn còn log

    r = pipeline.ask(message, history)  # endpoint def (không async) -> FastAPI chạy trong thread pool
    rows = r["rows"]
    msg = ChatMessage(
        conversation_id=conv.id, role="assistant", content=r["answer"], loai=r["loai"], sql=r["sql"],
        result_preview={"columns": r["columns"], "rows": rows[:config.CHAT_SUMMARY_ROWS] if rows else rows,
                        "row_count": r["row_count"], "truncated": r["truncated"], "lua_chon": r["lua_chon"]},
        warnings=r["warnings"], model_sql=r["model_sql"], model_summary=r["model_summary"], llm_calls=r["llm_calls"],
        latency_ms=r["latency_ms"], error=r["error"])
    db.add(msg)
    conv.updated_at = now()
    db.commit()
    r.pop("error")
    return {"conversation_id": conv.id, "message_id": msg.id, **r}


@router.get("/conversations/{conv_id}")
def conversation(conv_id: int, db=Depends(get_db)):
    conv = db.get(ChatConversation, conv_id)
    if not conv:
        raise HTTPException(404, "Không có cuộc trò chuyện này (có thể đã bị xóa theo chính sách lưu trữ)")
    msgs = db.scalars(select(ChatMessage).where(ChatMessage.conversation_id == conv_id).order_by(ChatMessage.id)).all()
    return {"conversation_id": conv.id, "created_at": conv.created_at, "messages": [_view(m) for m in msgs]}


@router.post("/feedback")
def feedback(message_id: int = Body(...), rating: str = Body(...), note: str | None = Body(None), db=Depends(get_db)):
    if rating not in ("up", "down"):
        raise HTTPException(422, "rating phải là 'up' hoặc 'down'")
    m = db.get(ChatMessage, message_id)
    if not m or m.role != "assistant":
        raise HTTPException(404, "Không có câu trả lời này")
    db.add(ChatFeedback(message_id=message_id, rating=rating, note=(note or "")[:1000] or None))
    db.commit()
    return {"ok": True}


@router.get("/usage")
def usage(db=Depends(get_db)):
    """Số câu hỏi, số lần gọi model và token theo model hôm nay (free tier Groq giới hạn token/ngày cho từng model)."""
    start = datetime.combine(now().date(), dtime.min)
    n, calls = db.execute(select(func.count(), func.coalesce(func.sum(ChatMessage.llm_calls), 0)).where(
        ChatMessage.role == "assistant", ChatMessage.created_at >= start)).one()
    models = db.execute(select(ChatTokenUsage.provider, ChatTokenUsage.model, ChatTokenUsage.requests,
                               ChatTokenUsage.prompt_tokens + ChatTokenUsage.completion_tokens)
                        .where(ChatTokenUsage.ngay == start.date())).all()
    return {"ngay": start.date(), "cau_hoi": n, "llm_calls": calls,
            "tokens": sum(m[3] for m in models),
            "theo_model": [{"provider": p, "model": m, "requests": r, "tokens": t} for p, m, r, t in models]}
