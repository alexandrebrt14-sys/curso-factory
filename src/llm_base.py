"""Base comum dos clientes LLM (transporte próprio e SDK do orquestrador).

Os dois backends (`LLMClient`, com httpx e resiliência própria, e
`SDKLLMClient`, que delega ao geo_orchestrator_sdk) expõem a mesma
superfície para os agentes: `call(provider, prompt, **kwargs)`, os atalhos
`call_<provider>()`, `set_course_context()`, `close()` e uso como context
manager. Antes cada um reimplementava tudo isso; aqui fica uma vez só, e a
factory `make_llm_client()` pode prometer `BaseLLMClient` no retorno.
"""

from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from typing import Any

from src.cache import Cache
from src.cost_tracker import CostTracker

logger = logging.getLogger(__name__)

#: Provedores que o pipeline conhece pelo nome curto.
PROVIDER_NAMES: tuple[str, ...] = ("perplexity", "openai", "google", "groq", "anthropic")


class BaseLLMClient(ABC):
    """Contrato que o orquestrador e os agentes usam, independente do transporte."""

    def __init__(
        self,
        cost_tracker: CostTracker | None = None,
        cache: Cache | None = None,
        use_cache: bool = True,
    ) -> None:
        self.cost_tracker = cost_tracker or CostTracker()
        self.cache = cache if cache is not None else (Cache() if use_cache else None)
        # course_id ativo, setado pelo Orchestrator: toda chamada é tagueada
        # no CostTracker com o curso (achado F32 da auditoria 2026-04-08).
        self.current_course_id: str = ""

    # --- ciclo de vida ------------------------------------------------------

    def set_course_context(self, course_id: str) -> None:
        """Define o curso ativo para fins de tracking de custo."""
        self.current_course_id = course_id or ""

    def close(self) -> None:  # noqa: B027 - opcional: só transportes com conexão sobrescrevem
        """Libera recursos do transporte. Idempotente; a base não tem o que fechar."""

    def __enter__(self) -> BaseLLMClient:
        return self

    def __exit__(self, *exc_info: object) -> None:
        self.close()

    # --- chamada ------------------------------------------------------------

    @abstractmethod
    def call(self, provider: str, prompt: str, **kwargs: Any) -> str:
        """Envia `prompt` ao `provider` e devolve o texto da resposta."""

    def _cache_get(self, prompt: str, provider: str, model: str) -> str | None:
        if self.cache is None:
            return None
        return self.cache.get(prompt, provider, model)

    def _cache_set(self, prompt: str, provider: str, model: str, result: str) -> None:
        if self.cache is not None:
            self.cache.set(prompt, provider, model, result)

    def _registrar_custo(
        self,
        provider: str,
        model: str,
        tokens_in: int,
        tokens_out: int,
        custo: float,
        *,
        rotulo: str = "LLM",
        detalhe: str = "",
    ) -> None:
        """Grava a chamada no ledger local por curso e loga a linha padrão."""
        self.cost_tracker.track(
            provider,
            tokens_in,
            tokens_out,
            model,
            custo,
            course_id=self.current_course_id,
        )
        logger.info(
            "%s %s/%s: %d tok_in, %d tok_out, USD %.4f (curso=%s%s)",
            rotulo,
            provider,
            model,
            tokens_in,
            tokens_out,
            custo,
            self.current_course_id or "n/a",
            detalhe,
        )

    # --- atalhos por provedor -----------------------------------------------

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


__all__ = ["PROVIDER_NAMES", "BaseLLMClient"]
