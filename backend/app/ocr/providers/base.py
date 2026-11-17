"""Exception chuẩn + lớp provider gốc. Mỗi provider map lỗi gốc về 1 exception chuẩn để router quyết định đổi model / provider."""
import base64
import io
import json
import mimetypes
import re
from pathlib import Path

from pydantic import BaseModel, ValidationError

from app import config
from app.ocr.prompts import HAU_TO_MO


class OcrError(Exception):
    pass


class QuotaExceeded(OcrError):
    """429 / RESOURCE_EXHAUSTED: đổi model, model vào cooldown."""


class AuthError(OcrError):
    """401/403/402, key sai/hết hạn/hết credit: bỏ cả provider."""


class ProviderUnavailable(OcrError):
    """Timeout, lỗi mạng, 5xx: thử lại rồi đổi provider."""


class ModelNotFound(OcrError):
    """404, model bị gỡ: đổi model, model bị disabled."""


class BadOutput(OcrError):
    """Không parse được JSON / sai schema: thử lại 1 lần rồi đổi model."""


def map_error(status: int | None, msg: str) -> OcrError:
    """HTTP status + thông báo lỗi gốc -> exception chuẩn."""
    m = msg.lower()
    if status == 429 or "resource_exhausted" in m or "quota" in m or "rate limit" in m:
        return QuotaExceeded(msg)
    if status in (401, 402, 403) or "api key" in m or "api_key_invalid" in m or "permission_denied" in m:
        return AuthError(msg)  # Gemini báo key sai bằng 400 "API key not valid"
    if status == 404 or "not_found" in m or "does not exist" in m:
        return ModelNotFound(msg)
    if status is None or status >= 500 or status == 408 or "timeout" in m or "deadline" in m:
        return ProviderUnavailable(msg)
    return BadOutput(msg)  # 400/413/422 còn lại: yêu cầu bị từ chối với model này


def extract_json(text: str | None):
    """Bỏ <think>…</think> và code fence, rồi lấy khối {...} hoặc [...] đầu tiên parse được."""
    t = re.sub(r"<think>.*?</think>", "", text or "", flags=re.S)
    t = re.sub(r"```(?:json)?", "", t)
    dec = json.JSONDecoder()
    for i, ch in enumerate(t):
        if ch in "{[":
            try:
                return dec.raw_decode(t, i)[0]
            except json.JSONDecodeError:
                continue
    raise BadOutput("Không tìm thấy JSON trong câu trả lời")


def validate_output(schema: type[BaseModel], data) -> dict:
    try:
        return schema.model_validate(data).model_dump()
    except ValidationError as e:
        err = e.errors()[0]
        raise BadOutput(f"Sai schema: {e.error_count()} lỗi, ví dụ {err['loc']}: {err['msg']}")


def image_data_url(path: str | Path, shrink: bool = False) -> str:
    """Ảnh -> data URL base64. shrink: nén JPEG q85, cạnh dài <= 2048px (khi API chê ảnh quá lớn)."""
    p = Path(path)
    if not shrink:
        mime = mimetypes.guess_type(p.name)[0] or "image/jpeg"
        return f"data:{mime};base64,{base64.b64encode(p.read_bytes()).decode()}"
    from PIL import Image

    im = Image.open(p).convert("RGB")
    im.thumbnail((2048, 2048))
    buf = io.BytesIO()
    im.save(buf, "JPEG", quality=85)
    return f"data:image/jpeg;base64,{base64.b64encode(buf.getvalue()).decode()}"


class BaseProvider:
    """1 lần gọi = 1 model. Trả dict đã validate theo schema; lỗi thì raise 1 exception chuẩn ở trên."""
    name = ""

    def __init__(self, api_key: str):
        self.api_key = api_key

    def ocr(self, image_path: str | Path, schema: type[BaseModel], prompt: str, model: str) -> dict:
        raise NotImplementedError


class OpenAICompatProvider(BaseProvider):
    """NVIDIA NIM và OpenRouter: OpenAI SDK chat.completions, ảnh base64, temperature=0, prompt kèm JSON schema."""
    base_url = ""
    extra_body: dict | None = None
    extra_headers: dict | None = None

    def __init__(self, api_key: str):
        super().__init__(api_key)
        from openai import OpenAI

        self.client = OpenAI(base_url=self.base_url, api_key=api_key, max_retries=0, timeout=config.TIMEOUT_S)

    def ocr(self, image_path, schema, prompt, model):
        schema_txt = json.dumps(schema.model_json_schema(), ensure_ascii=False)
        text = f"{prompt}\n\nTrả về đúng 1 object JSON theo JSON Schema sau:\n{schema_txt}{HAU_TO_MO}"
        shrink, json_mode = False, True
        while True:
            kwargs = dict(model=model, temperature=0, max_tokens=4096, extra_body=self.extra_body,
                          extra_headers=self.extra_headers,
                          messages=[{"role": "user", "content": [
                              {"type": "text", "text": text},
                              {"type": "image_url", "image_url": {"url": image_data_url(image_path, shrink)}}]}])
            if json_mode:
                kwargs["response_format"] = {"type": "json_object"}
            try:
                resp = self.client.chat.completions.create(**kwargs)
                break
            except Exception as e:
                status, msg = getattr(e, "status_code", None), str(e)
                if json_mode and status in (400, 422):
                    json_mode = False  # có thể model không hỗ trợ json_object -> gọi lại 1 lần không có tham số này
                    continue
                if not shrink and (status == 413 or "too large" in msg.lower()):
                    shrink = True  # ảnh quá lớn -> nén rồi thử lại 1 lần
                    continue
                raise map_error(status, f"{type(e).__name__}: {msg[:300]}") from e
        self.last_model = resp.model or model  # model thực sự trả lời
        content = resp.choices[0].message.content if resp.choices else None  # thinking: chỉ lấy content
        return validate_output(schema, extract_json(content))
