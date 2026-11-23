"""Cloudflare Workers AI qua endpoint OpenAI-compatible (/ai/v1). Cần CLOUDFLARE_API_KEY + CLOUDFLARE_ACCOUNT_ID."""
import os

from app.ocr.providers.base import OpenAICompatProvider


class CloudflareProvider(OpenAICompatProvider):
    name = "cloudflare"

    def __init__(self, api_key: str):
        self.base_url = f"https://api.cloudflare.com/client/v4/accounts/{os.environ['CLOUDFLARE_ACCOUNT_ID']}/ai/v1"
        super().__init__(api_key)
