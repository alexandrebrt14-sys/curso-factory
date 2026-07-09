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
import os
import sys
from pathlib import Path
from typing import Any

from src.cache import Cache
from src.cost_tracker import CostTracker

logger = logging.getLogger(__name__)

# provider (curso-factory) -> (alias canonico, task_type) no orquestrador.
# task_type governa a BANDA DE TIMEOUT e a fallback chain herdadas.
PROVIDER_TO_SDK: dict[str, tuple[str, str]] = {
    "perplexity": ("perplexity", "research"),    # sonar-deep-research, 600s
    "openai":     ("gpt4o", "writing"),          # gpt-5.5, 420s
    "google":     ("gemini", "analysis"),        # gemini pro, 360s
    "anthropic":  ("claude", "review"),          # opus, 360s
    # groq foi removido do orquestrador (Sprint 16); o equivalente bulk
    # canonico e o gemini_flash. Mantido para compat com fluxos legados.
    "groq":       ("gemini_flash", "classification"),
}


def _ensure_sdk_on_path() -> None:
    """Adiciona o repo do geo-orchestrator ao sys.path (path-based install)."""
    root = Path(
        os.environ.get("GEO_ORCHESTRATOR_PATH", str(Path.home() / "geo-orchestrator"))
    )
    if not (root / "geo_orchestrator_sdk" / "__init__.py").exists():
        raise ImportError(
            f"geo_orchestrator_sdk nao encontrado em {root} — defina "
            "GEO_ORCHESTRATOR_PATH apontando para o clone do geo-orchestrator."
        )
    if str(root) not in sys.path:
        sys.path.insert(0, str(root))


class SDKLLMClient:
    """Drop-in do LLMClient legado, delegando ao geo_orchestrator_sdk.

    Mesma superficie usada pelos agents: call(), atalhos call_<provider>(),
    set_course_context(), close(), context manager e cost_tracker local.
    """

    def __init__(
        self,
        cost_tracker: CostTracker | None = None,
        cache: Cache | None = None,
        use_cache: bool = True,
    ) -> None:
        _ensure_sdk_on_path()
        from geo_orchestrator_sdk import call_llm  # noqa: PLC0415

        self._call_llm = call_llm
        self.cost_tracker = cost_tracker or CostTracker()
        self.cache = cache if cache is not None else (Cache() if use_cache else None)
        self.current_course_id: str = ""
        logger.info("LLM backend: geo_orchestrator_sdk (CURSO_FACTORY_LLM_BACKEND=sdk)")

    # --- interface legada -------------------------------------------------

    def set_course_context(self, course_id: str) -> None:
        self.current_course_id = course_id or ""

    def close(self) -> None:
        """No-op: o SDK fecha o ConnectionPool por chamada (licao F3)."""

    def __enter__(self) -> "SDKLLMClient":
        return self

    def __exit__(self, *exc: object) -> None:
        self.close()

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
                    ignored, kwargs.pop(ignored),
                )
        max_tokens = int(kwargs.pop("max_tokens", 4096))
        if kwargs:
            logger.debug("SDK backend: kwargs nao mapeados ignorados: %s", sorted(kwargs))

        # Cache local do curso-factory (mesma posicao do fluxo legado).
        if self.cache is not None:
            cached = self.cache.get(prompt, provider, alias)
            if cached is not None:
                return cached

        result = self._call_llm(
            prompt, task_type=task_type, alias=alias, max_tokens=max_tokens
        )

        # Dupla contabilidade: FinOps global ja registrado pelo SDK; aqui o
        # ledger LOCAL por curso (relatorios por course_id continuam integros).
        self.cost_tracker.track(
            provider,
            result.tokens_input,
            result.tokens_output,
            result.model,
            result.cost,
            course_id=self.current_course_id,
        )
        logger.info(
            "LLM(sdk) %s->%s/%s: %d tok_in, %d tok_out, USD %.4f (curso=%s%s)",
            provider, result.alias, result.model,
            result.tokens_input, result.tokens_output, result.cost,
            self.current_course_id or "n/a",
            ", fallback" if result.fallback_used else "",
        )

        if self.cache is not None:
            self.cache.set(prompt, provider, alias, result.text)
        return result.text

    # --- atalhos legados ---------------------------------------------------

    def call_perplexity(self, prompt: str, **kwargs: Any) -> str:
        return self.call("perplexity", prompt, **kwargs)

    def call_openai(self, prompt: str, **kwargs: Any) -> str:
        return self.call("openai", prompt, **kwargs)

    def call_google(self, prompt: str, **kwargs: Any) -> str:
        return self.call("google", prompt, **kwargs)

    def call_groq(self, prompt: str, **kwargs: Any) -> str:
        return self.call("groq", prompt, **kwargs)

    def call_anthropic(self, prompt: str, **kwargs: Any) -> str:
        return self.call("anthropic", prompt, **kwargs)
