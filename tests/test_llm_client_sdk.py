"""Backend SDK (B-019/D8) — factory + adapter drop-in.

O adapter delega ao geo_orchestrator_sdk.call_llm; aqui o call_llm e mockado
(sem rede). O import real do SDK e coberto quando GEO_ORCHESTRATOR_PATH/
~/geo-orchestrator existe; caso contrario os testes de adapter sao pulados
(CI sem o repo vizinho) — a factory legada roda sempre.
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path
from unittest.mock import patch

import pytest

from src.cost_tracker import CostTracker
from src.llm_client import LLMClient, make_llm_client

_SDK_ROOT = Path(
    os.environ.get("GEO_ORCHESTRATOR_PATH", str(Path.home() / "geo-orchestrator"))
)
_HAS_SDK = (_SDK_ROOT / "geo_orchestrator_sdk" / "__init__.py").exists()

needs_sdk = pytest.mark.skipif(
    not _HAS_SDK, reason="geo-orchestrator nao disponivel neste ambiente"
)


@dataclass
class _FakeResult:
    text: str = "resposta sdk"
    alias: str = "perplexity"
    model: str = "sonar-deep-research"
    provider: str = "perplexity"
    cost: float = 0.002
    tokens_input: int = 100
    tokens_output: int = 50
    citations: list = field(default_factory=list)
    fallback_used: bool = False


def test_factory_default_is_legacy(monkeypatch):
    monkeypatch.delenv("CURSO_FACTORY_LLM_BACKEND", raising=False)
    client = make_llm_client(use_cache=False)
    try:
        assert isinstance(client, LLMClient)
    finally:
        client.close()


def test_factory_unknown_value_is_legacy(monkeypatch):
    monkeypatch.setenv("CURSO_FACTORY_LLM_BACKEND", "banana")
    client = make_llm_client(use_cache=False)
    try:
        assert isinstance(client, LLMClient)
    finally:
        client.close()


@needs_sdk
def test_factory_sdk_backend(monkeypatch):
    monkeypatch.setenv("CURSO_FACTORY_LLM_BACKEND", "sdk")
    from src.llm_client_sdk import SDKLLMClient
    client = make_llm_client(use_cache=False)
    assert isinstance(client, SDKLLMClient)


@needs_sdk
class TestSDKAdapter:
    def _client(self, use_cache=False):
        from src.llm_client_sdk import SDKLLMClient
        tracker = CostTracker()
        c = SDKLLMClient(cost_tracker=tracker, use_cache=use_cache)
        return c, tracker

    def test_call_maps_provider_and_tracks_cost(self):
        c, tracker = self._client()
        captured = {}

        def fake_call_llm(prompt, *, task_type, alias, max_tokens):
            captured.update(task_type=task_type, alias=alias, max_tokens=max_tokens)
            return _FakeResult()

        c._call_llm = fake_call_llm
        c.set_course_context("curso-teste")
        with patch.object(tracker, "track") as track:
            out = c.call("perplexity", "pesquise algo", max_tokens=2048)
        assert out == "resposta sdk"
        # research herda a banda de 600s no lado do orquestrador
        assert captured == {"task_type": "research", "alias": "perplexity",
                            "max_tokens": 2048}
        kw = track.call_args.kwargs
        assert track.call_args.args[0] == "perplexity"
        assert kw.get("course_id") == "curso-teste"

    def test_legacy_kwargs_ignored_not_fatal(self):
        c, _ = self._client()
        c._call_llm = lambda prompt, **kw: _FakeResult()
        out = c.call("openai", "escreva", model="gpt-4o-custom",
                     max_retries=9, base_delay=1.0)
        assert out == "resposta sdk"

    def test_unknown_provider_raises(self):
        c, _ = self._client()
        with pytest.raises(ValueError, match="provider desconhecido"):
            c.call("cohere", "oi")

    def test_local_cache_hit_skips_sdk(self, tmp_path):
        from src.llm_client_sdk import SDKLLMClient
        from src.cache import Cache
        cache = Cache(ttl=3600)
        cache._dir = tmp_path  # isola do cache real em disco
        c = SDKLLMClient(cache=cache)
        calls = []

        def fake(prompt, **kw):
            calls.append(prompt)
            return _FakeResult()

        c._call_llm = fake
        a = c.call("google", "analise X")
        b = c.call("google", "analise X")
        assert a == b == "resposta sdk"
        assert len(calls) == 1, "segunda chamada devia vir do cache local"

    def test_provider_map_covers_legacy_surface(self):
        from src.llm_client_sdk import PROVIDER_TO_SDK
        for p in ("perplexity", "openai", "google", "anthropic", "groq"):
            assert p in PROVIDER_TO_SDK
        # timeouts herdados: research para o canal que estourava 60s
        assert PROVIDER_TO_SDK["perplexity"] == ("perplexity", "research")
