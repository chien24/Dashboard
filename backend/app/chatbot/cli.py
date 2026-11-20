"""Chạy thử chatbot từ terminal (gọi model thật, đọc DB theo DATABASE_URL).

    cd backend && py -m app.chatbot.cli "Tỷ lệ NoRead hôm qua?" --today 2026-11-16
    cd backend && py -m app.chatbot.cli            # hỏi liên tục, giữ lịch sử để hỏi nối tiếp; Enter trống để thoát
"""
import argparse
import json
import sys
from datetime import date

from app.chatbot import pipeline


def show(r: dict):
    print(f"\n[{r['loai']}] {r['answer']}")
    if r.get("lua_chon"):
        print("Lựa chọn:", " | ".join(r["lua_chon"]))
    for w in r["warnings"]:
        print("  ⚠", w)
    if r["sql"]:
        print("SQL:\n" + r["sql"])
    if r["columns"]:
        print(" | ".join(r["columns"]))
        for row in r["rows"][:20]:
            print(" | ".join("" if v is None else str(v) for v in row))
        if r["row_count"] > 20 or r["truncated"]:
            print(f"... {r['row_count']} dòng" + (" (bị cắt)" if r["truncated"] else ""))
    print(f"model: {r['model_sql']} / {r['model_summary']} · {r['llm_calls']} lần gọi · {r['latency_ms']} ms"
          + (f" · lỗi: {r['error']}" if r.get("error") else ""))


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("question", nargs="?")
    ap.add_argument("--today", type=date.fromisoformat, help="Cố định 'hôm nay' (YYYY-MM-DD)")
    ap.add_argument("--json", action="store_true", help="In nguyên JSON trả về")
    a = ap.parse_args()
    from app.db import init_db
    init_db()  # tạo view + bảng chat nếu app chưa chạy lần nào sau khi cập nhật
    history = []
    while True:
        q = a.question or input("\nHỏi: ").strip()
        if not q:
            return
        r = pipeline.ask(q, history, today=a.today)
        print(json.dumps(r, ensure_ascii=False, indent=2, default=str)) if a.json else show(r)
        history.append({"question": q, "sql": r["sql"], "summary": r["answer"]})
        if a.question:
            return


if __name__ == "__main__":
    main()
