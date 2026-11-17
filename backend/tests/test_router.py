"""Router fallback với provider giả: 429 -> đổi model, 401 -> đổi provider, timeout -> retry rồi đổi provider."""
from datetime import timedelta

import pytest
from sqlalchemy import select

from app import config
from app.db import SessionLocal
from app.models import ModelStatus, now
from app.ocr import router
from app.ocr.providers.base import AuthError, BadOutput, ModelNotFound, ProviderUnavailable, QuotaExceeded
from app.schemas import Classify


class Fake:
    """Provider giả: script[(provider, model)] = danh sách exception lần lượt; hết danh sách thì thành công."""

    def __init__(self, name, script, calls):
        self.name, self.script, self.calls = name, script, calls

    def ocr(self, image_path, schema, prompt, model):
        self.calls.append((self.name, model))
        errs = self.script.get((self.name, model), [])
        if errs:
            raise errs.pop(0)
        return {"loai": "scada"}


@pytest.fixture
def chain(clean_db, monkeypatch):
    monkeypatch.setattr(config, "PROVIDER_CHAIN", [
        {"provider": "gemini", "models": ["g1", "g2"]},
        {"provider": "nvidia", "models": ["n1", "n2"]},
        {"provider": "openrouter", "models": ["o1"]},
    ])
    for k in config.KEYS.values():
        monkeypatch.setenv(k, "x")
    calls, sleeps = [], []

    def run(script, **kw):
        return router.run("a.jpg", Classify, "p", provider_factory=lambda n: Fake(n, script, calls),
                          sleep=sleeps.append, **kw)
    return run, calls, sleeps


def state(provider, model):
    with SessionLocal() as db:
        return db.scalar(select(ModelStatus).where(ModelStatus.provider == provider, ModelStatus.model == model))


def test_429_doi_model_va_cooldown(chain):
    run, calls, _ = chain
    r = run({("gemini", "g1"): [QuotaExceeded("429 Too Many Requests")]})
    assert (r["provider"], r["model"]) == ("gemini", "g2") and calls == [("gemini", "g1"), ("gemini", "g2")]
    st = state("gemini", "g1")
    assert st.state == "cooldown" and now() < st.cooldown_until <= now() + timedelta(seconds=61)
    calls.clear()
    run({})
    assert calls == [("gemini", "g2")]  # g1 đang cooldown -> bỏ qua


def test_429_theo_ngay_cooldown_toi_nua_dem(chain):
    run, _, _ = chain
    run({("gemini", "g1"): [QuotaExceeded("Quota exceeded for requests per day")]})
    cd = state("gemini", "g1").cooldown_until
    assert (cd.hour, cd.minute, cd.date()) == (0, 0, now().date() + timedelta(days=1))


def test_401_doi_provider_va_disabled(chain):
    run, calls, _ = chain
    r = run({("gemini", "g1"): [AuthError("API key not valid")]})
    assert r["provider"] == "nvidia" and ("gemini", "g2") not in calls
    states = {(s["provider"], s["model"]): s["state"] for s in router.provider_states()}
    assert states[("gemini", "g1")] == states[("gemini", "g2")] == "disabled"
    assert [a["error"] is None for a in r["attempts"]] == [False, True]
    router.reset("gemini")
    assert router.provider_states()[0]["state"] == "active"


def test_timeout_retry_2_lan_roi_doi_provider(chain):
    run, calls, sleeps = chain
    r = run({("gemini", "g1"): [ProviderUnavailable("timeout")] * 3})
    assert r["provider"] == "nvidia" and sleeps == [1, 3]
    assert calls == [("gemini", "g1")] * 3 + [("nvidia", "n1")]


def test_404_disable_model_bad_output_thu_lai_1_lan(chain):
    run, calls, _ = chain
    r = run({("gemini", "g1"): [ModelNotFound("404")], ("gemini", "g2"): [BadOutput("x"), BadOutput("y")]})
    assert state("gemini", "g1").state == "disabled"
    assert calls == [("gemini", "g1"), ("gemini", "g2"), ("gemini", "g2"), ("nvidia", "n1")] and r["model"] == "n1"


def test_het_chuoi_va_thieu_key(chain, monkeypatch):
    run, _, _ = chain
    monkeypatch.delenv("NVIDIA_API_KEY")
    with pytest.raises(router.AllProvidersFailed) as e:
        run({("gemini", "g1"): [AuthError("401")], ("openrouter", "o1"): [AuthError("401")]})
    assert {a["provider"] for a in e.value.attempts} == {"gemini", "openrouter"}  # nvidia không có key -> không gọi


def test_chi_dinh_provider_model(chain):
    run, calls, _ = chain
    r = run({}, only_provider="nvidia", only_model="n2")
    assert calls == [("nvidia", "n2")] and r["model"] == "n2"
