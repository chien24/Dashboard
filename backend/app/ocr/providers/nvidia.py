"""NVIDIA NIM. Chỉ dùng model có tag Free Endpoint. Mặc định tắt thinking."""
from app.ocr.providers.base import OpenAICompatProvider


class NvidiaProvider(OpenAICompatProvider):
    name = "nvidia"
    base_url = "https://integrate.api.nvidia.com/v1"
    extra_body = {"chat_template_kwargs": {"enable_thinking": False}}
