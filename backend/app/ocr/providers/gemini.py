"""Gemini qua google-genai, giữ cách gọi của code cũ: response_schema = pydantic schema, ảnh độ phân giải cao."""
import mimetypes
from pathlib import Path

from app import config
from app.ocr.providers.base import BadOutput, BaseProvider, map_error


class GeminiProvider(BaseProvider):
    name = "gemini"

    def __init__(self, api_key: str):
        super().__init__(api_key)
        from google import genai
        from google.genai import types

        self.types = types
        self.client = genai.Client(api_key=api_key, http_options=types.HttpOptions(timeout=config.TIMEOUT_S * 1000))

    def ocr(self, image_path, schema, prompt, model):
        t = self.types
        p = Path(image_path)
        image = t.Part.from_bytes(data=p.read_bytes(), mime_type=mimetypes.guess_type(p.name)[0] or "image/jpeg")
        cfg = t.GenerateContentConfig(response_mime_type="application/json", response_schema=schema,
                                      media_resolution=t.MediaResolution.MEDIA_RESOLUTION_HIGH)  # chữ chú thích rất nhỏ
        try:
            resp = self.client.models.generate_content(model=model, contents=[image, prompt], config=cfg)
        except Exception as e:
            raise map_error(getattr(e, "code", None), f"{type(e).__name__}: {str(e)[:300]}") from e
        self.last_model = model
        try:
            data = resp.parsed if isinstance(resp.parsed, schema) else schema.model_validate_json(resp.text)
        except Exception as e:
            raise BadOutput(f"Gemini trả JSON sai schema: {str(e)[:200]}") from e
        return data.model_dump()
