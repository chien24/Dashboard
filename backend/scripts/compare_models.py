"""So sánh độ chính xác các model OCR (không fallback): mỗi ảnh chạy qua từng model.

    cd backend
    python scripts/compare_models.py ../sample_dashboar/HT2/bcr_rate --bao-cao bcr_rate --gt ../ket_qua_json/HT2 --sleep 4
    python scripts/compare_models.py ../sample_dashboar/HT1 --models gemini:gemini-3.6-flash,nvidia:meta/llama-3.2-90b-vision-instruct

--gt: thư mục JSON đúng, tên file trùng tên ảnh (ví dụ ../ket_qua_json/HT1, đã đối chiếu tay). Không có --gt thì so với
kết quả Gemini (model đầu tiên trong danh sách) của cùng ảnh.
Kết quả: results/<model>/<ảnh>.json và results/summary.csv. OpenRouter free chỉ ~50 request/ngày: lọc bằng --models.
"""
import argparse
import csv
import json
import re
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from app import config  # noqa: E402
from app.ocr import router  # noqa: E402
from app.ocr.prompts import prompt_for  # noqa: E402
from app.schemas import SCHEMAS  # noqa: E402
from ocr_folder import collect_images, resolve_screen  # noqa: E402

ALL_MODELS = [(p["provider"], m) for p in config.PROVIDER_CHAIN for m in p["models"]]


def call(provider: str, model: str, image_path: str, screen: str) -> dict:
    """Gọi đúng 1 provider/model qua router (không fallback). Kết quả dạng {provider, model, data, latency_s, error}."""
    t0 = time.perf_counter()
    try:
        r = router.run(image_path, SCHEMAS[screen], prompt_for(screen), provider, model)
        return {**r, "latency_s": r["attempts"][-1]["latency_s"], "error": None}
    except router.AllProvidersFailed as e:
        return {"provider": provider, "model": model, "data": None, "attempts": e.attempts,
                "latency_s": round(time.perf_counter() - t0, 2), "error": str(e)}
BO_QUA = {"file", "loai", "model", "model_lan_2", "canh_bao", "canh_bao_ocr"}  # không phải số liệu đọc từ ảnh


def flatten(v, path: str = "") -> dict:
    """JSON lồng nhau -> {đường dẫn: giá trị lá}, bỏ các trường metadata."""
    if isinstance(v, dict):
        return {p: x for k, val in v.items() if k not in BO_QUA
                for p, x in flatten(val, f"{path}.{k}" if path else k).items()}
    if isinstance(v, list):
        return {p: x for i, val in enumerate(v) for p, x in flatten(val, f"{path}[{i}]").items()}
    return {path: v}


def norm(v):
    """So số sau khi bỏ phân cách hàng nghìn (. , khoảng trắng) và %: '5 987.75' = 5987.75, '77.079' = 77079."""
    if isinstance(v, bool) or v is None:
        return v
    if isinstance(v, (int, float)):
        return float(v)
    s = re.sub(r"[\s%]", "", str(v))
    if re.fullmatch(r"-?\d{1,3}([.,]\d{3})+", s):  # chỉ toàn nhóm 3 chữ số -> dấu là phân cách hàng nghìn
        s = re.sub(r"[.,]", "", s)
    try:
        return float(s.replace(",", "."))
    except ValueError:
        return str(v).strip()


def compare(got: dict | None, ref: dict | None) -> tuple[int, int, list[str]]:
    """(số trường khớp, tổng số trường của bản chuẩn, danh sách trường lệch)."""
    if not ref:
        return 0, 0, []
    r, g = flatten(ref), flatten(got or {})
    lech = [k for k in r if norm(g.get(k)) != norm(r[k])] + [k for k in g if k not in r]
    return sum(norm(g.get(k)) == norm(r[k]) for k in r), len(r), lech


def safe(name: str) -> str:
    return re.sub(r"[^\w.-]+", "_", name)


def main():
    for s in (sys.stdout, sys.stderr):
        s.reconfigure(encoding="utf-8", line_buffering=True)
    ap = argparse.ArgumentParser(description="So sánh model OCR")
    ap.add_argument("images", help="Thư mục ảnh (hoặc 1 ảnh)")
    ap.add_argument("--gt", help="Thư mục ground truth JSON, tên trùng tên ảnh")
    ap.add_argument("--bao-cao", help="Loại báo cáo cho ảnh HT2")
    ap.add_argument("--he-thong", type=str.upper)
    ap.add_argument("--models", help="Danh sách provider:model ngăn bằng dấu phẩy (mặc định: tất cả)")
    ap.add_argument("--sleep", type=float, default=0, help="Nghỉ giữa các request (giây) để không vượt rate limit")
    ap.add_argument("-o", "--out", default="../results")
    a = ap.parse_args()

    models = ALL_MODELS if not a.models else [tuple(x.strip().split(":", 1)) for x in a.models.split(",")]
    out = Path(a.out)
    rows = []
    for img in collect_images([a.images]):
        try:
            screen = resolve_screen(img, a.bao_cao, a.he_thong)
        except ValueError as e:
            sys.exit(f"Lỗi: {e}")
        if not screen:
            print(f"! Bỏ qua {img}: không nằm trong HT1/HT2 (dùng --he-thong)", file=sys.stderr)
            continue
        gt_file = Path(a.gt) / f"{img.stem}.json" if a.gt else None
        ref = json.loads(gt_file.read_text(encoding="utf-8")) if gt_file and gt_file.exists() else None
        if ref and ref.get("loai", screen) != screen:
            print(f"! {gt_file} là loại {ref['loai']}, ảnh là {screen}: bỏ ground truth", file=sys.stderr)
            ref = None
        nguon = "ground truth" if ref else "Gemini"
        for i, (provider, model) in enumerate(models):
            if i and a.sleep:
                time.sleep(a.sleep)
            print(f"- {img.name} [{screen}] -> {provider}/{model}")
            try:
                r = call(provider, model, str(img), screen)
            except Exception as e:  # 1 lượt lỗi (vd ảnh bị chuyển chỗ giữa chừng) không được làm dừng cả lần so sánh
                r = {"provider": provider, "model": model, "data": None, "latency_s": None,
                     "error": f"{type(e).__name__}: {str(e)[:300]}"}
            d = out / safe(f"{provider}_{model}")
            d.mkdir(parents=True, exist_ok=True)
            (d / f"{img.stem}.json").write_text(json.dumps(r, ensure_ascii=False, indent=2), encoding="utf-8")
            if ref is None and provider == "gemini" and r["data"]:
                ref = r["data"]  # không có ground truth: lấy kết quả Gemini đầu tiên làm chuẩn
            khop, tong, lech = compare(r["data"], ref)
            rows.append({"anh": str(img), "loai": screen, "provider": provider, "model_yeu_cau": model,
                         "model_tra_loi": r["model"], "latency_s": r["latency_s"], "parse_ok": r["data"] is not None,
                         "so_sanh_voi": nguon if ref is not r["data"] else "(chính nó)",
                         "truong_khop": khop, "tong_truong": tong, "truong_lech": "; ".join(lech), "loi": r["error"] or ""})
            print(f"  {'OK' if r['data'] else 'LỖI'} {r['latency_s']}s · khớp {khop}/{tong}" + (f" · {r['error'][:120]}" if r["error"] else ""))
    out.mkdir(exist_ok=True)
    if rows:
        with (out / "summary.csv").open("w", newline="", encoding="utf-8-sig") as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0]))
            w.writeheader()
            w.writerows(rows)
    print(f"\nXong: {len(rows)} lượt. Tổng hợp: {out / 'summary.csv'}")


if __name__ == "__main__":
    main()
