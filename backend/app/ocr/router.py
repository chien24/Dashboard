"""Chuỗi fallback provider -> model (mục 3.2 đặc tả). Trạng thái cooldown/disabled lưu ở bảng model_status.

| Lỗi                 | Hành động                                                        |
| QuotaExceeded       | đổi model; model cooldown 60s, hoặc tới 00:00 hôm sau nếu theo ngày |
| AuthError           | bỏ cả provider; provider disabled tới khi restart / reset         |
| ProviderUnavailable | thử lại 2 lần (1s, 3s), vẫn lỗi thì đổi provider                  |
| ModelNotFound       | đổi model; model disabled                                         |
| BadOutput           | thử lại 1 lần cùng model, vẫn sai thì đổi model                   |
"""
import time
from datetime import datetime, timedelta

from sqlalchemy import select

from app import config
from app.db import SessionLocal
from app.models import ModelStatus, now
from app.ocr.providers.base import AuthError, BadOutput, ModelNotFound, ProviderUnavailable, QuotaExceeded

RETRY_UNAVAILABLE_S = (1, 3)
PROVIDER = "*"  # model_status.model = '*' : trạng thái của cả provider


class AllProvidersFailed(Exception):
    def __init__(self, attempts: list[dict]):
        self.attempts = attempts
        detail = " | ".join(f"{a['provider']}/{a['model']}: {a['error'][:100]}" for a in attempts if a.get("error"))
        super().__init__("Tất cả provider/model đều lỗi: " + (detail or "không có provider nào có API key"))


def make_provider(name: str):
    from app.ocr.providers.gemini import GeminiProvider
    from app.ocr.providers.nvidia import NvidiaProvider
    from app.ocr.providers.openrouter import OpenRouterProvider

    return {"gemini": GeminiProvider, "nvidia": NvidiaProvider, "openrouter": OpenRouterProvider}[name](config.api_key(name))


# ---------------------------------------------------------------- model_status
def _status(db, provider: str, model: str) -> ModelStatus:
    st = db.scalar(select(ModelStatus).where(ModelStatus.provider == provider, ModelStatus.model == model))
    if not st:
        st = ModelStatus(provider=provider, model=model, state="active", fail_count=0)
        db.add(st)
    return st


def is_blocked(provider: str, model: str) -> str | None:
    """Lý do bỏ qua (provider disabled, model disabled/cooldown chưa hết) hoặc None."""
    with SessionLocal() as db:
        for m in (PROVIDER, model):
            st = db.scalar(select(ModelStatus).where(ModelStatus.provider == provider, ModelStatus.model == m))
            if not st or st.state == "active":
                continue
            if st.state == "disabled":
                return f"{'provider' if m == PROVIDER else 'model'} disabled: {st.last_error or ''}"[:200]
            if st.state == "cooldown" and st.cooldown_until and st.cooldown_until > now():
                return f"cooldown tới {st.cooldown_until:%Y-%m-%d %H:%M:%S}"
    return None


def cooldown_until(msg: str, fail_count: int) -> datetime:
    """429 theo ngày (thông báo có 'per day'/'daily', hoặc 429 liên tiếp >= 3 lần) -> tới 00:00 hôm sau; còn lại 60s."""
    m = msg.lower()
    if "per day" in m or "daily" in m or "perday" in m or fail_count >= 3:
        return datetime.combine(now().date() + timedelta(days=1), datetime.min.time())
    return now() + timedelta(seconds=60)


def mark(provider: str, model: str, state: str, error: str | None = None, until: datetime | None = None):
    """Ghi trạng thái. state='ok': thành công -> reset fail_count. until: hết cooldown lúc nào (vd từ header retry-after)."""
    with SessionLocal() as db:
        st = _status(db, provider, model)
        if state == "ok":
            st.state, st.fail_count, st.cooldown_until = "active", 0, None
        elif state == "cooldown":
            st.fail_count = (st.fail_count or 0) + 1
            st.state, st.last_error = "cooldown", error
            st.cooldown_until = until or cooldown_until(error or "", st.fail_count)
        else:
            st.state, st.last_error = state, error
            st.fail_count = (st.fail_count or 0) + 1
        db.commit()


def reset(provider: str | None = None):
    """Gỡ cooldown/disabled (tất cả, hoặc 1 provider)."""
    with SessionLocal() as db:
        q = select(ModelStatus)
        if provider:
            q = q.where(ModelStatus.provider == provider)
        for st in db.scalars(q):
            st.state, st.cooldown_until, st.fail_count = "active", None, 0
        db.commit()


def reset_provider_disabled_on_start():
    """'disabled tới khi restart': khởi động lại app thì provider bị AuthError được thử lại."""
    with SessionLocal() as db:
        for st in db.scalars(select(ModelStatus).where(ModelStatus.model == PROVIDER)):
            st.state = "active"
        db.commit()


# ---------------------------------------------------------------- chạy chuỗi
def chain(only_provider: str | None = None, only_model: str | None = None) -> list[tuple[str, list[str]]]:
    out = []
    for p in config.PROVIDER_CHAIN:
        if only_provider and p["provider"] != only_provider:
            continue
        out.append((p["provider"], [only_model] if only_model else p["models"]))
    return out


def run(image_path, schema, prompt: str, only_provider=None, only_model=None, on_try=None,
        sleep=time.sleep, provider_factory=make_provider) -> dict:
    """Trả {data, provider, model, attempts}. Lỗi hết chuỗi -> AllProvidersFailed(attempts).
    on_try(provider, model): báo tiến trình cho trang upload."""
    attempts = []
    for pname, models in chain(only_provider, only_model):
        if not config.api_key(pname):
            continue
        if (why := is_blocked(pname, PROVIDER)) and not only_provider:
            attempts.append({"provider": pname, "model": PROVIDER, "error": f"bỏ qua: {why}", "latency_s": 0})
            continue
        try:
            prov = provider_factory(pname)
        except Exception as e:
            attempts.append({"provider": pname, "model": PROVIDER, "error": f"Không khởi tạo được: {e}", "latency_s": 0})
            continue
        next_provider = False
        for model in models:
            if (why := is_blocked(pname, model)) and not only_model:
                attempts.append({"provider": pname, "model": model, "error": f"bỏ qua: {why}", "latency_s": 0})
                continue
            unavailable = bad = 0
            while True:
                if on_try:
                    on_try(pname, model)
                t0 = time.perf_counter()
                try:
                    data = prov.ocr(image_path, schema, prompt, model)
                except Exception as e:
                    err = f"{type(e).__name__}: {str(e)[:300]}"
                    attempts.append({"provider": pname, "model": model, "error": err,
                                     "latency_s": round(time.perf_counter() - t0, 2)})
                    if isinstance(e, QuotaExceeded):
                        mark(pname, model, "cooldown", err)
                        break  # -> model sau
                    if isinstance(e, ModelNotFound):
                        mark(pname, model, "disabled", err)
                        break
                    if isinstance(e, AuthError):
                        mark(pname, PROVIDER, "disabled", err)
                        next_provider = True
                        break
                    if isinstance(e, BadOutput):
                        bad += 1
                        if bad <= 1:
                            continue  # thử lại 1 lần cùng model
                        break
                    # ProviderUnavailable hoặc lỗi lạ không map được
                    unavailable += 1
                    if unavailable <= len(RETRY_UNAVAILABLE_S):
                        sleep(RETRY_UNAVAILABLE_S[unavailable - 1])
                        continue
                    next_provider = True
                    break
                actual = getattr(prov, "last_model", model)
                attempts.append({"provider": pname, "model": actual, "error": None,
                                 "latency_s": round(time.perf_counter() - t0, 2)})
                mark(pname, model, "ok")
                return {"data": data, "provider": pname, "model": actual, "attempts": attempts}
            if next_provider:
                break
    raise AllProvidersFailed(attempts)


def provider_states() -> list[dict]:
    """Cho /api/system/providers: mọi provider/model trong chuỗi kèm trạng thái."""
    with SessionLocal() as db:
        rows = {(s.provider, s.model): s for s in db.scalars(select(ModelStatus))}
    out = []
    for p in config.PROVIDER_CHAIN:
        name = p["provider"]
        prov = rows.get((name, PROVIDER))
        has_key = bool(config.api_key(name))
        for m in p["models"]:
            st = rows.get((name, m))
            state = "no_key" if not has_key else "disabled" if prov and prov.state == "disabled" else (st.state if st else "active")
            if state == "cooldown" and st.cooldown_until and st.cooldown_until <= now():
                state = "active"
            out.append({"provider": name, "model": m, "state": state,
                        "cooldown_until": st.cooldown_until.isoformat(sep=" ") if st and st.cooldown_until else None,
                        "last_error": (prov.last_error if prov and prov.state == "disabled" else st.last_error if st else None),
                        "fail_count": st.fail_count if st else 0})
    return out
