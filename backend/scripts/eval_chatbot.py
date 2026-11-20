"""Bộ đánh giá chatbot (request/DAC_TA_CHATBOT.md mục 12). Gọi model THẬT qua OpenRouter.

    cd backend
    py scripts/eval_chatbot.py --build-db                       # dựng lại tests/chatbot/fixtures/chat_eval.db
    py scripts/eval_chatbot.py                                  # chạy 40 câu với chuỗi model trong .env
    py scripts/eval_chatbot.py --models a:free,b:free --sleep 4 # so sánh từng model sinh SQL
    py scripts/eval_chatbot.py --only q01,q31 --with-summary    # chạy vài câu, có cả bước tóm tắt

Chạy trên bản sao tạm của chat_eval.db nên không đụng DB thật. Kết quả: eval_results/<ngày>.csv
"""
import argparse
import csv
import json
import math
import os
import re
import shutil
import sys
import tempfile
import time
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path

BACKEND = Path(__file__).resolve().parents[1]
FIXTURE = BACKEND / "tests" / "chatbot" / "fixtures" / "chat_eval.db"
QUESTIONS = BACKEND / "tests" / "chatbot" / "eval_questions.yaml"
KET_QUA = BACKEND.parent / "ket_qua_json"
EVAL_TODAY = date(2026, 11, 16)


# ---------------------------------------------------------------- dữ liệu test
def seed():
    """Nạp ket_qua_json vào DB đang cấu hình, cộng ca bẫy: 1 report SCADA can_kiem_tra có loại UNKNOWN (12/11),
    report Sorted 13/11 can_kiem_tra, xóa Sorted 11/11 (ngày thiếu ảnh)."""
    import copy

    from sqlalchemy import delete, select, update

    from app.db import SessionLocal, init_db
    from app.models import Report
    from app.services.ingest import clear_details, ingest
    from import_json import import_paths

    init_db()
    them, _, loi = import_paths(sorted(p for p in KET_QUA.rglob("*.json") if not p.name.startswith("tong_hop")))
    assert them and not loi, loi
    rec = json.loads((KET_QUA / "HT1" / "1.json").read_text(encoding="utf-8"))
    data = {k: v for k, v in rec.items() if k not in {"file", "loai", "model", "model_lan_2", "canh_bao"}}
    d = copy.deepcopy(data)
    d.update(thoi_gian_tu="2026-11-12 00:00", thoi_gian_den="2026-11-12 23:59", so_luong_da_quet=70000,
             so_luong_goi_theo_luoi=68000, so_buu_kien_bat_thuong=3400, ty_le_bat_thuong=5.0,
             cong_suat_cao_nhat_1h=7000, cong_suat_max_tu="2026-11-12 20:00:00", cong_suat_max_den="2026-11-12 20:59:00",
             phan_bo_bat_thuong=[{"loai": "Không Có Mã Vạch", "so_luong": 1500, "ty_le": 44.12},
                                 {"loai": "Yêu c?u ?ng d?n th?t b?i", "so_luong": 1200, "ty_le": 35.29},
                                 {"loai": "Không có Báo cáo Phân lo?i", "so_luong": 100, "ty_le": 2.94},
                                 {"loai": "Lo?i l? XYZ chua co", "so_luong": 650, "ty_le": 19.12}])
    d.pop("canh_bao_ocr", None)
    with SessionLocal() as db:
        ingest(db, {"loai": "scada", "data": d, "provider": "gemini", "model": "test", "status": "can_kiem_tra",
                    "canh_bao": ["Lệch giữa lần 1 và lần 2 (test)"]}, source_name="outbound_1211.jpg")
        db.execute(update(Report).where(Report.loai == "dmwcs_sorted", Report.report_date == date(2026, 11, 13))
                   .values(status="can_kiem_tra"))
        gone = db.scalars(select(Report.id).where(Report.loai == "dmwcs_sorted",
                                                  Report.report_date == date(2026, 11, 11))).all()
        clear_details(db, gone)
        db.execute(delete(Report).where(Report.id.in_(gone)))
        db.commit()


def build_db():
    FIXTURE.parent.mkdir(parents=True, exist_ok=True)
    tmp = Path(tempfile.mkdtemp()) / "build.db"
    os.environ["DATABASE_URL"] = f"sqlite:///{tmp.as_posix()}"
    seed()
    from app.db import engine
    engine.dispose()
    with __import__("sqlite3").connect(tmp) as c:  # gộp WAL vào file chính trước khi copy
        c.execute("PRAGMA wal_checkpoint(TRUNCATE)")
        c.execute("PRAGMA journal_mode=DELETE")
    shutil.copy(tmp, FIXTURE)
    print("Đã dựng", FIXTURE)


# ---------------------------------------------------------------- chấm điểm
def _norm(v):
    if isinstance(v, float):
        return round(v, 2)
    if isinstance(v, int) and not isinstance(v, bool):
        return round(float(v), 2)
    if isinstance(v, str) and re.fullmatch(r"-?\d+(\.\d+)?", v.strip()):
        return round(float(v), 2)
    return v


def same_result(ref_rows, bot_rows, ordered: bool, match: str = "rows") -> bool:
    """Mỗi dòng tham chiếu phải nằm trọn trong 1 dòng của bot (bot được trả thêm cột), cùng số dòng.
    Bỏ qua tên cột; bỏ qua thứ tự dòng nếu reference_sql không có ORDER BY.
    match='first': chỉ so N dòng đầu của bot; match='values': mọi giá trị tham chiếu có mặt đâu đó trong kết quả bot."""
    if match == "values":
        return not (Counter(_norm(v) for r in ref_rows for v in r) - Counter(_norm(v) for r in bot_rows for v in r))
    if match == "first":
        bot_rows = bot_rows[:len(ref_rows)]
    ref = [Counter(_norm(v) for v in r) for r in ref_rows]
    bot = [Counter(_norm(v) for v in r) for r in bot_rows]
    if len(ref) != len(bot):
        return False
    if ordered:
        return all(not (a - b) for a, b in zip(ref, bot))
    left = list(bot)
    for a in ref:
        hit = next((i for i, b in enumerate(left) if not (a - b)), None)
        if hit is None:
            return False
        left.pop(hit)
    return True


def grade(q: dict, r: dict) -> tuple[bool, str]:
    from app.chatbot import executor

    want = q.get("expect_loai", "sql")
    if r["loai"] != want:
        return False, f"loai {r['loai']} ≠ {want}"
    for s in q.get("expect_answer_contains") or []:
        if s.lower() not in (r["answer"] or "").lower():
            return False, f"câu trả lời thiếu '{s}'"
    for s in q.get("expect_warning_contains") or []:
        if not any(s.lower() in w.lower() for w in r["warnings"]):
            return False, f"thiếu cảnh báo '{s}'"
    if want == "sql" and q.get("reference_sql"):
        if r["rows"] is None:
            return False, f"không chạy được SQL: {r.get('error') or r['answer']}"
        _, ref, _ = executor.run(q["reference_sql"])
        if not same_result(ref, r["rows"], "order by" in q["reference_sql"].lower(), q.get("match", "rows")):
            return False, f"kết quả khác reference ({len(r['rows'])} / {len(ref)} dòng)"
    return True, ""


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("--build-db", action="store_true")
    ap.add_argument("--models", help="Danh sách model sinh SQL, ngăn bằng dấu phẩy; mỗi model chạy riêng cả bộ")
    ap.add_argument("--only", help="Chỉ chạy các id, ngăn bằng dấu phẩy")
    ap.add_argument("--with-summary", action="store_true", help="Gọi cả bước tóm tắt (tốn thêm 1 lượt/câu)")
    ap.add_argument("--sleep", type=float, default=0, help="Nghỉ giữa các câu (free tier ~20 request/phút)")
    a = ap.parse_args()
    sys.path.insert(0, str(BACKEND))
    if a.build_db or not FIXTURE.exists():
        build_db()
        if a.build_db:
            return
    work = Path(tempfile.mkdtemp()) / "eval.db"
    shutil.copy(FIXTURE, work)
    os.environ["DATABASE_URL"] = f"sqlite:///{work.as_posix()}"

    import yaml

    from app import config
    from app.chatbot import pipeline
    from app.db import init_db

    init_db()
    qs = yaml.safe_load(QUESTIONS.read_text(encoding="utf-8"))
    if a.only:
        ids = set(a.only.split(","))
        qs = [q for q in qs if q["id"] in ids]
    if not a.with_summary:
        config.CHAT_SUMMARY_MODELS, config.CHAT_SUMMARY_FALLBACK_MODELS = [], []  # chấm SQL không cần tóm tắt
    models = a.models.split(",") if a.models else [None]
    out_rows, stats = [], defaultdict(lambda: Counter())
    for m in models:
        if m:  # đo riêng 1 model: tắt dự phòng để kết quả không lẫn model khác
            config.CHAT_SQL_MODELS, config.CHAT_SQL_FALLBACK_MODELS = [m], []
        label = m or "chuỗi .env"
        for q in qs:
            today = date.fromisoformat(str(q.get("today") or EVAL_TODAY))
            history = [{"question": h["question"], "sql": h.get("sql"), "summary": h.get("summary", "")}
                       for h in q.get("history") or []]
            for _ in range(4):  # free tier: 429 -> chờ đúng retry-after rồi hỏi lại, không tính là sai
                pipeline._sql_cache.clear()
                r = pipeline.ask(q["question"], history, today=today)
                if r["loai"] != "loi" or "hết lượt" not in r["answer"]:
                    break
                wait = wait_cooldown()
                print(f"   … 429, chờ {wait:.0f} giây")
            ok, why = grade(q, r)
            first_ok = r["llm_calls"] <= 1 + (1 if a.with_summary and r["rows"] else 0)
            print(f"{'✅' if ok else '❌'} {q['id']} [{label}] {q['question']} · {r['tokens']} token · {r['latency_ms']} ms"
                  + (f" — {why}" if why else ""))
            data_q = q.get("expect_loai", "sql") == "sql" and bool(q.get("reference_sql"))
            for tag in ["_tong"] + (["_cau_du_lieu"] if data_q else []) + list(q.get("tags") or []):
                stats[(label, tag)].update(n=1, dung=int(ok), sql_lan_dau=int(first_ok))
            out_rows.append({"model": label, "id": q["id"], "question": q["question"], "tags": " ".join(q.get("tags") or []),
                             "dung": int(ok), "ly_do": why, "loai": r["loai"], "model_sql": r["model_sql"],
                             "llm_calls": r["llm_calls"], "tokens": r["tokens"], "latency_ms": r["latency_ms"],
                             "sql": r["sql"] or "", "answer": r["answer"], "error": r.get("error") or ""})
            time.sleep(a.sleep)
    res = BACKEND / "eval_results"
    res.mkdir(exist_ok=True)
    suffix = "_".join(re.sub(r"[^\w.-]+", "-", x) for x in models if x) or "chuoi-env"
    path = res / f"{date.today().isoformat()}_{suffix}.csv"
    with path.open("w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=list(out_rows[0]))
        w.writeheader()
        w.writerows(out_rows)
    print("\nModel | nhóm | đúng / tổng | SQL hợp lệ ngay lần đầu")
    for (label, tag), c in sorted(stats.items()):
        print(f"{label} | {tag} | {c['dung']}/{c['n']} | {c['sql_lan_dau']}/{c['n']}")
    for label in dict.fromkeys(r["model"] for r in out_rows):
        rows = [r for r in out_rows if r["model"] == label]
        lat, tok = sorted(r["latency_ms"] for r in rows), [r["tokens"] for r in rows]
        c = stats[(label, "_cau_du_lieu")]
        print(f"TONG KET {label}: execution accuracy {c['dung']}/{c['n']} = {100 * c['dung'] / max(1, c['n']):.1f}% · "
              f"đúng tất cả {stats[(label, '_tong')]['dung']}/{len(rows)} · token/câu TB {sum(tok) / len(tok):.0f} "
              f"(max {max(tok)}) · latency p50 {lat[len(lat) // 2]} ms, p95 {lat[min(len(lat) - 1, math.ceil(len(lat) * 0.95) - 1)]} ms")
    print("Đã lưu", path)


def wait_cooldown() -> float:
    """Ngủ tới khi model gần nhất hết cooldown (tối đa 90 giây)."""
    from app.chatbot.llm import next_retry_at, providers
    from app.models import now

    pairs = [(p, m) for p, _, _, ms in providers() for m in ms["sql"]]
    at = next_retry_at(pairs)
    s = min(90.0, max(3.0, (at - now()).total_seconds() + 1)) if at else 10.0
    time.sleep(s)
    return s

if __name__ == "__main__":
    main()
