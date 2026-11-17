"""OCR cả thư mục ảnh ra JSON (công cụ dòng lệnh cũ, nay dùng pipeline/router mới). Không ghi vào DB.

    cd backend
    python scripts/ocr_folder.py ../sample_dashboar/HT1
    python scripts/ocr_folder.py ../sample_dashboar/HT2/sorted --bao-cao sorted
    python scripts/ocr_folder.py anh.png --he-thong HT2 --bao-cao capacity --force

Loại ảnh chọn theo thư mục cha HT1 (scada) / HT2 (+ --bao-cao). Kết quả: <out>/HT1|HT2/<tên ảnh>.json.
Muốn đưa vào dashboard: python scripts/import_json.py <out>
"""
import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.ocr import pipeline  # noqa: E402
from app.schemas import LOAI  # noqa: E402

IMAGE_EXT = {".jpg", ".jpeg", ".png", ".webp"}
SYSTEM_DIRS = {"HT1": "scada", "HT2": "dmwcs"}  # tên thư mục -> hệ thống


def system_dir(loai: str) -> str:
    return "HT1" if loai == "scada" else "HT2"


def resolve_screen(path, bao_cao: str | None = None, he_thong: str | None = None) -> str | None:
    """Thư mục cha (gần nhất trước) quyết định hệ thống; ngoài HT1/HT2 thì dùng he_thong.
    None nếu không xác định được; ValueError nếu ảnh HT2 mà thiếu/sai --bao-cao."""
    he = next((SYSTEM_DIRS[p.upper()] for p in reversed(Path(path).absolute().parent.parts) if p.upper() in SYSTEM_DIRS), None)
    he = he or SYSTEM_DIRS.get((he_thong or "").upper())
    if he is None:
        return None
    if he in LOAI:
        return he
    bao_caos = [k.split("_", 1)[1] for k in LOAI if k.startswith(he + "_")]
    if bao_cao in bao_caos:
        return f"{he}_{bao_cao}"
    loi = "thiếu --bao-cao" if not bao_cao else f"--bao-cao {bao_cao} không có cho hệ thống này"
    raise ValueError(f"Ảnh {path} thuộc hệ thống {he} nhưng {loi} (chọn: {', '.join(bao_caos)}).\n"
                     f"Ví dụ:  python scripts/ocr_folder.py {Path(path).parent} --bao-cao {bao_caos[0]}")


def collect_images(inputs: list[str]) -> list[Path]:
    files = []
    for item in inputs:
        p = Path(item)
        if p.is_dir():
            files += sorted(f for f in p.rglob("*") if f.suffix.lower() in IMAGE_EXT)
        elif p.suffix.lower() in IMAGE_EXT and p.exists():
            files.append(p)
        else:
            print(f"! Bỏ qua '{item}': không tồn tại hoặc không phải ảnh", file=sys.stderr)
    return files


def to_record(img: Path, r: dict) -> dict:
    """Kết quả pipeline -> JSON dạng cũ (file, loai, model, model_lan_2, canh_bao, ...dữ liệu)."""
    model = r["model"] if r["provider"] == "gemini" else f"{r['provider']}:{r['model']}"
    return {"file": img.name, "loai": r["loai"], "model": model, "model_lan_2": r["model_lan_2"],
            "canh_bao": r["canh_bao"], **r["data"]}


def main():
    for s in (sys.stdout, sys.stderr):
        s.reconfigure(encoding="utf-8", line_buffering=True)
    ap = argparse.ArgumentParser(description="OCR ảnh SCADA (HT1) / DMWCS (HT2) -> JSON")
    ap.add_argument("inputs", nargs="+")
    ap.add_argument("-o", "--out", default="../ket_qua_json")
    ap.add_argument("--force", action="store_true", help="Chạy lại cả ảnh đã có JSON")
    ap.add_argument("--bao-cao", choices=sorted(k.split("_", 1)[1] for k in LOAI if "_" in k))
    ap.add_argument("--he-thong", type=str.upper, choices=list(SYSTEM_DIRS))
    a = ap.parse_args()
    da_doc = loi = bo_qua = 0
    for img in collect_images(a.inputs):
        try:
            loai = resolve_screen(img, a.bao_cao, a.he_thong)
        except ValueError as e:
            sys.exit(f"Lỗi: {e}")
        if not loai:
            print(f"! Bỏ qua {img}: không nằm trong HT1/HT2 (dùng --he-thong)", file=sys.stderr)
            bo_qua += 1
            continue
        out = Path(a.out) / system_dir(loai) / f"{img.stem}.json"
        if out.exists() and not a.force:
            bo_qua += 1
            continue
        print(f"- Đang đọc: {img}  [{loai}]")
        try:
            r = pipeline.process(img, loai, on_progress=lambda s: print(f"  · {s}"))
        except Exception as e:
            print(f"  x {e}", file=sys.stderr)
            loi += 1
            continue
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(to_record(img, r), ensure_ascii=False, indent=2), encoding="utf-8")
        for c in r["canh_bao"]:
            print(f"  ! {c}", file=sys.stderr)
        da_doc += 1
    print(f"\nXong. Đã đọc: {da_doc} | lỗi: {loi} | bỏ qua: {bo_qua} | kết quả: {a.out}")


if __name__ == "__main__":
    main()
