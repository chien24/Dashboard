"""Import các file JSON OCR cũ (ket_qua_json/...) vào DB.

    cd backend && python scripts/import_json.py ../ket_qua_json

Nhận file 1 bản ghi hoặc mảng (tong_hop_*.json). Bản ghi trùng (cùng loai + file + thời gian) chỉ import 1 lần,
chạy lại script không tạo bản sao. Cảnh báo được tính lại bằng bộ kiểm tra hiện tại (bỏ cảnh báo sai kiểu cũ).
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from sqlalchemy import select  # noqa: E402

from app.db import SessionLocal, init_db  # noqa: E402
from app.models import Report  # noqa: E402
from app.ocr.providers.base import validate_output  # noqa: E402
from app.schemas import LOAI, SCHEMAS  # noqa: E402
from app.services.ingest import ingest  # noqa: E402
from app.services.normalize import model_notes, report_times  # noqa: E402
from app.services.validate import VALIDATORS  # noqa: E402

META = {"file", "loai", "model", "model_lan_2", "canh_bao", "report_id", "status"}


def to_result(rec: dict) -> dict:
    loai = rec["loai"]
    data = validate_output(SCHEMAS[loai], {**{k: v for k, v in rec.items() if k not in META}, "canh_bao_ocr": []})
    data.pop("canh_bao_ocr")
    old = rec.get("canh_bao") or []
    notes = model_notes(loai, [c for c in old if c.startswith("OCR lần")])
    loi = [c for c in old if c.startswith(("Lệch giữa", "Không đọc được lần"))] + VALIDATORS[loai](data)
    model = rec.get("model") or ""
    return {"loai": loai, "data": data, "raw_json_1": rec, "provider": model.split(":", 1)[0] if ":" in model else "gemini",
            "model": model.split(":", 1)[-1] or None, "model_lan_2": rec.get("model_lan_2"),
            "canh_bao": notes + loi, "status": "can_kiem_tra" if loi else "ok"}


def import_paths(paths: list[Path]) -> tuple[int, int, list[str]]:
    init_db()
    them = bo_qua = 0
    loi = []
    with SessionLocal() as db:
        for f in paths:
            try:
                recs = json.loads(f.read_text(encoding="utf-8"))
            except (OSError, ValueError) as e:
                loi.append(f"{f}: {e}")
                continue
            for rec in recs if isinstance(recs, list) else [recs]:
                if not isinstance(rec, dict) or rec.get("loai") not in LOAI:
                    continue
                try:
                    r = to_result(rec)
                    tu, _, _ = report_times(r["loai"], r["data"])
                except Exception as e:
                    loi.append(f"{f} ({rec.get('file')}): {e}")
                    continue
                if db.scalar(select(Report.id).where(Report.loai == r["loai"], Report.source_name == rec.get("file"),
                                                     Report.thoi_gian_tu == tu, Report.upload_id.is_(None))):
                    bo_qua += 1
                    continue
                ingest(db, r, source_name=rec.get("file"))
                them += 1
    return them, bo_qua, loi


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    paths = []
    for a in sys.argv[1:]:
        p = Path(a)
        paths += sorted(p.rglob("*.json")) if p.is_dir() else [p]
    them, bo_qua, loi = import_paths(paths)
    print(f"Đã import {them} bản ghi, bỏ qua {bo_qua} bản đã có.")
    for e in loi:
        print("  ! " + e)


if __name__ == "__main__":
    main()
