"""OCR N lần (mặc định 2) -> so sánh từng trường số -> validate -> cảnh báo + status. Giữ kết quả lần 1."""
from app import config
from app.ocr import router
from app.ocr.classify import classify
from app.ocr.prompts import LAN_2, prompt_for
from app.schemas import SCHEMAS
from app.services.normalize import model_notes
from app.services.validate import VALIDATORS, diff_numbers


def process(image_path, loai: str | None = None, only_provider=None, only_model=None, on_progress=None) -> dict:
    """-> dict để ingest: loai, data, raw_json_1/2, provider, model, model_lan_2, canh_bao, status, attempts.
    Lần 1 lỗi hết chuỗi -> router.AllProvidersFailed."""
    attempts = []
    progress = on_progress or (lambda s: None)
    if not loai:
        progress("đang nhận diện loại ảnh")
        loai, a = classify(image_path, on_try=lambda p, m: progress(f"nhận diện loại · {p}/{m}"))
        attempts += a
    schema, prompt = SCHEMAS[loai], prompt_for(loai)
    runs, loi_lan_sau = [], []
    for i in range(config.OCR_PASSES):
        try:
            r = router.run(image_path, schema, prompt + (LAN_2 if i else ""), only_provider, only_model,
                           on_try=lambda p, m, i=i: progress(f"lần {i + 1}/{config.OCR_PASSES} · {p}/{m}"))
        except router.AllProvidersFailed as e:
            attempts += e.attempts
            if i == 0:
                raise
            loi_lan_sau.append(f"Không đọc được lần {i + 1} nên chưa đối chiếu: {e}"[:300])
            continue
        attempts += r["attempts"]
        runs.append(r)
    return build(loai, runs, attempts, loi_lan_sau)


def build(loai: str, runs: list[dict], attempts: list[dict], loi_them: list[str] = ()) -> dict:
    raws = [dict(r["data"]) for r in runs]
    data = {k: v for k, v in raws[0].items() if k != "canh_bao_ocr"}
    notes = [f"OCR lần {i + 1}: {n}" for i, raw in enumerate(raws) for n in model_notes(loai, raw.get("canh_bao_ocr") or [])]
    lech = [f"Lệch giữa lần 1 và lần {i + 2} (lần 1 / lần {i + 2}) {e}"
            for i, raw in enumerate(raws[1:]) for e in diff_numbers(data, {k: v for k, v in raw.items() if k != "canh_bao_ocr"})]
    # Lệch giữa các lần đọc / sai số học -> can_kiem_tra. Ghi chú của model (vd 'NoChute bị cắt') chỉ là cảnh báo.
    loi = [*loi_them, *lech, *VALIDATORS[loai](data)]
    return {
        "loai": loai, "data": data,
        "raw_json_1": raws[0], "raw_json_2": raws[1] if len(raws) > 1 else None,
        "provider": runs[0]["provider"], "model": runs[0]["model"],
        "model_lan_2": f"{runs[1]['provider']}:{runs[1]['model']}" if len(runs) > 1 else None,
        "canh_bao": notes + loi, "status": "can_kiem_tra" if loi else "ok", "attempts": attempts,
    }
