"""Tự nhận diện loại ảnh khi người dùng không chọn (tốn thêm 1 lần gọi API)."""
from app.ocr import router
from app.ocr.prompts import prompt_for
from app.schemas import Classify


def classify(image_path, on_try=None) -> tuple[str, list[dict]]:
    """-> (loai, attempts). Ảnh không thuộc 4 loại -> ValueError."""
    r = router.run(image_path, Classify, prompt_for("classify"), on_try=on_try)
    loai = r["data"]["loai"]
    if loai == "khac":
        raise ValueError("Không nhận diện được loại màn hình. Hãy chọn loại khi upload.")
    return loai, r["attempts"]
