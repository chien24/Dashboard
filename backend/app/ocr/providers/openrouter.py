"""OpenRouter. Không dùng 'openrouter/free' (chọn model ngẫu nhiên). Free tier ~20 request/phút, ~50 request/ngày."""
from app.ocr.providers.base import OpenAICompatProvider


class OpenRouterProvider(OpenAICompatProvider):
    name = "openrouter"
    base_url = "https://openrouter.ai/api/v1"
    extra_headers = {"X-OpenRouter-Title": "OCR Dashboard"}
