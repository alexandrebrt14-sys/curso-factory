"""Backend LLM via geo_orchestrator_sdk — B-019/D8 (strangler pattern).

O curso-factory sempre chamou as APIs LLM direto (httpx proprio) — bypass do
orquestrador: sem banda de timeout por task_type, sem fallback chain canonica,
sem FinOps unificado (o incidente de timeout do research em sonar-pro nasceu
desse bypass). Este adapter implementa a MESMA interface do LLMClient legado
(`call(provider, prompt, **kwargs) -> str` + atalhos + course context) mas
delega ao `geo_orchestrator_sdk.call_llm`, herdando:

- banda de timeout por task_type (research 600s, writing 420s...);
- fallback chain canonica do orquestrador + circuit breaker;
- FinOps global (mesmo ledger diario SQLite dos runs do orquestrador),
   alem do cost_tracker LOCAL por course_id (dupla contabilidade mantida).

ATIVACAO (opt-in, rollout seguro — zero mudanca sem a env):

    CURSO_FACTORY_LLM_BACKEND=sdk

O caminho do repo do orquestrador vem de GEO_ORCHESTRATOR_PATH (default:
~/geo-orchestrator). A troca acontece na factory `make_llm_client()` em
llm_client.py — os agents nao mudam (mesma interface).

Diferencas deliberadas vs legado (documentadas, nao acidentais):
- `model=` custom e IGNORADO com log: o catalog do orquestrador e a SoT de
  modelos (sempre a versao canonica mais atual de cada provider).
- retry/backoff por chamada sao do orquestrador (LLMClient interno), nao os
  `max_retries/base_delay` locais — aceitos e ignorados com log.
- cache local do curso-factory continua valendo (envolve o adapter no mesmo
  ponto do fluxo: aqui dentro, antes de delegar).
"""

from __future__ import annotations

import logging
import sys
from typing import Any

from src.cache import Cache
from src.config import GEO_ORCHESTRATOR_PATH, MAX_TOKENS_PER_CALL
from src.cost_tracker import CostTracker
from src.llm_base import BaseLLMClient

logger = logging.getLogger(__name__)

# provider (curso-factory) -> (alias canonico, task_type) no orquestrador.
# task_type governa a BANDA DE TIMEOUT e a fallback chain herdadas.
PROVIDER_TO_SDK: dict[str, tuple[str, str]] = {
    "perplexity": ("perplexity", "research"),  # sonar-deep-research, 600s
    "openai": ("gpt4o", "writing"),  # gpt-5.5, 420s
    "google": ("gemini", "analysis"),  # gemini pro, 360s
    "anthropic": ("claude", "review"),  # opus, 360s
    # groq foi removido do orquestrador (Sprint 16); o equivalente bulk
    # canonico e o gemini_flash. Mantido para compat com fluxos legados.
    "groq": ("gemini_flash", "classification"),
}


def _ensure_sdk_on_path() -> None:
    """Adiciona o repo do geo-orchestrator ao sys.path (path-based install)."""
    root = GEO_ORCHESTRATOR_PATH
    if not (root / "geo_orchestrator_sdk" / "__init__.py").exists():
        raise ImportError(
            f"geo_orchestrator_sdk nao encontrado em {root} — defina "
            "GEO_ORCHESTRATOR_PATH apontando para o clone do geo-orchestrator."
        )
    if str(root) not in sys.path:
        sys.path.insert(0, str(root))


class SDKLLMClient(BaseLLMClient):
    """Backend que delega ao geo_orchestrator_sdk.

    Mesma superfície do `LLMClient` (herdada de `BaseLLMClient`): call(),
    atalhos call_<provider>(), set_course_context(), close(), context manager
    e cost_tracker local. Não há circuito nem cadeia própria: isso é do
    orquestrador.
    """

    def __init__(
        self,
        cost_tracker: CostTracker | None = None,
        cache: Cache | None = None,
        use_cache: bool = True,
    ) -> None:
        _ensure_sdk_on_path()
        from geo_orchestrator_sdk import call_llm  # noqa: PLC0415

        super().__init__(cost_tracker=cost_tracker, cache=cache, use_cache=use_cache)
        self._call_llm = call_llm
        logger.info("LLM backend: geo_orchestrator_sdk (CURSO_FACTORY_LLM_BACKEND=sdk)")

    def close(self) -> None:
        """No-op: o SDK fecha o ConnectionPool por chamada (lição F3)."""

    def call(self, provider: str, prompt: str, **kwargs: Any) -> str:
        if provider not in PROVIDER_TO_SDK:
            raise ValueError(
                f"provider desconhecido: {provider!r} (validos: {sorted(PROVIDER_TO_SDK)})"
            )
        alias, task_type = PROVIDER_TO_SDK[provider]

        # Compat: kwargs do backend legado que o SDK governa internamente.
        for ignored in ("model", "max_retries", "base_delay", "_fallback_depth"):
            if ignored in kwargs:
                logger.debug(
                    "SDK backend ignora kwarg %r=%r (governado pelo orquestrador)",
                    ignored,
                    kwargs.pop(ignored),
                )
        max_tokens = int(kwargs.pop("max_tokens", MAX_TOKENS_PER_CALL))
        if kwargs:
            logger.debug("SDK backend: kwargs nao mapeados ignorados: %s", sorted(kwargs))

        # Cache local do curso-factory (mesma posição do fluxo legado).
        cached = self._cache_get(prompt, provider, alias)
        if cached is not None:
            return cached

        result = self._call_llm(prompt, task_type=task_type, alias=alias, max_tokens=max_tokens)

        # Dupla contabilidade: FinOps global já registrado pelo SDK; aqui o
        # ledger LOCAL por curso (relatórios por course_id continuam íntegros).
        self._registrar_custo(
            provider,
            f"{result.alias}/{result.model}",
            result.tokens_input,
            result.tokens_output,
            result.cost,
            rotulo="LLM(sdk)",
            detalhe=", fallback" if result.fallback_used else "",
        )

        self._cache_set(prompt, provider, alias, result.text)
        return result.text
