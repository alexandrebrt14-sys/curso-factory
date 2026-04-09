"""Cliente HTTP unificado para os 5 LLMs do pipeline.

Implementa circuit breaker, retry com backoff exponencial,
fallback entre providers e rate limiting por token bucket.
"""

from __future__ import annotations

import logging
import time
from dataclasses import dataclass, field
from typing import Any, Optional

import httpx

from src.config import get_api_key, MAX_TOKENS_PER_CALL
from src.cost_tracker import CostTracker

logger = logging.getLogger(__name__)

# Preços aproximados por 1K tokens (input, output) em USD
PRICING: dict[str, tuple[float, float]] = {
    "perplexity": (0.001, 0.001),
    "openai": (0.005, 0.015),
    "google": (0.00025, 0.0005),
    "groq": (0.0001, 0.0002),
    "anthropic": (0.015, 0.075),  # Claude Opus 4.6
}

# Mapeamento provider → modelo padrão
DEFAULT_MODELS: dict[str, str] = {
    "perplexity": "sonar-pro",
    "openai": "gpt-4o",
    "google": "gemini-2.0-flash",
    "groq": "llama-3.3-70b-versatile",
    "anthropic": "claude-opus-4-6",
}

# Endpoints base
ENDPOINTS: dict[str, str] = {
    "perplexity": "https://api.perplexity.ai/chat/completions",
    "openai": "https://api.openai.com/v1/chat/completions",
    "google": "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent",
    "groq": "https://api.groq.com/openai/v1/chat/completions",
    "anthropic": "https://api.anthropic.com/v1/messages",
}

# Fallback: se o provider primário falhar, tentar o secundário
FALLBACK_MAP: dict[str, str] = {
    "openai": "anthropic",
    "anthropic": "openai",
    "google": "openai",
    "groq": "openai",
    "perplexity": "google",
}


@dataclass
class CircuitState:
    """Estado do circuit breaker para um provider."""
    failures: int = 0
    open_until: float = 0.0
    threshold: int = 3
    cooldown: float = 60.0

    @property
    def is_open(self) -> bool:
        if self.failures >= self.threshold and time.time() < self.open_until:
            return True
        if self.failures >= self.threshold and time.time() >= self.open_until:
            # Half-open: reseta para permitir uma tentativa
            self.failures = 0
        return False

    def record_failure(self) -> None:
        self.failures += 1
        if self.failures >= self.threshold:
            self.open_until = time.time() + self.cooldown
            logger.warning("Circuit breaker aberto por %.0fs", self.cooldown)

    def record_success(self) -> None:
        self.failures = 0


@dataclass
class TokenBucket:
    """Rate limiter simples baseado em token bucket."""
    capacity: int = 10
    tokens: float = 10.0
    refill_rate: float = 1.0  # tokens por segundo
    last_refill: float = field(default_factory=time.time)

    def consume(self) -> bool:
        now = time.time()
        elapsed = now - self.last_refill
        self.tokens = min(self.capacity, self.tokens + elapsed * self.refill_rate)
        self.last_refill = now
        if self.tokens >= 1.0:
            self.tokens -= 1.0
            return True
        return False

    def wait_and_consume(self) -> None:
        while not self.consume():
            time.sleep(0.1)


class LLMClient:
    """Cliente unificado para múltiplos providers LLM."""

    def __init__(self, cost_tracker: Optional[CostTracker] = None) -> None:
        self.cost_tracker = cost_tracker or CostTracker()
        self._circuits: dict[str, CircuitState] = {}
        self._buckets: dict[str, TokenBucket] = {}
        self._http = httpx.Client(timeout=60.0)
        # course_id ativo — setado pelo Orchestrator antes de iniciar o
        # pipeline. Achado F32 da auditoria 2026-04-08: antes deste campo,
        # cost_tracker.track sempre recebia course_id="" e era impossivel
        # rastrear "qual curso custou X". Agora cada chamada LLM eh
        # automaticamente tagueada com o curso ativo.
        self.current_course_id: str = ""

    def set_course_context(self, course_id: str) -> None:
        """Define o curso ativo para fins de tracking de custo.

        Chamado pelo Orchestrator no inicio do pipeline. Todas as chamadas
        LLM subsequentes (via call/_log_cost) propagarao este course_id
        para o CostTracker, permitindo relatorios precisos por curso e
        budget guard granular.
        """
        self.current_course_id = course_id or ""

    def _get_circuit(self, provider: str) -> CircuitState:
        if provider not in self._circuits:
            self._circuits[provider] = CircuitState()
        return self._circuits[provider]

    def _get_bucket(self, provider: str) -> TokenBucket:
        if provider not in self._buckets:
            self._buckets[provider] = TokenBucket()
        return self._buckets[provider]

    def call(self, provider: str, prompt: str, **kwargs: Any) -> str:
        """Chamada genérica com circuit breaker, retry e fallback."""
        circuit = self._get_circuit(provider)
        if circuit.is_open:
            logger.warning("Circuito aberto para %s, tentando fallback", provider)
            return self._try_fallback(provider, prompt, **kwargs)

        bucket = self._get_bucket(provider)
        bucket.wait_and_consume()

        max_retries = kwargs.pop("max_retries", 3)
        base_delay = kwargs.pop("base_delay", 2.0)

        for attempt in range(max_retries):
            try:
                result = self._do_call(provider, prompt, **kwargs)
                circuit.record_success()
                return result
            except Exception as exc:
                circuit.record_failure()
                if attempt < max_retries - 1:
                    delay = base_delay * (2 ** attempt)
                    logger.warning(
                        "Tentativa %d/%d falhou para %s: %s. Aguardando %.1fs",
                        attempt + 1, max_retries, provider, exc, delay,
                    )
                    time.sleep(delay)
                else:
                    logger.error("Todas as tentativas falharam para %s", provider)

        return self._try_fallback(provider, prompt, **kwargs)

    def _try_fallback(self, provider: str, prompt: str, **kwargs: Any) -> str:
        fallback = FALLBACK_MAP.get(provider)
        if not fallback:
            raise RuntimeError(f"Sem fallback disponível para {provider}")
        logger.info("Usando fallback: %s → %s", provider, fallback)
        return self.call(fallback, prompt, **kwargs)

    def _do_call(self, provider: str, prompt: str, **kwargs: Any) -> str:
        """Executa a chamada HTTP real para o provider."""
        api_key = get_api_key(provider)
        model = kwargs.get("model", DEFAULT_MODELS.get(provider, ""))
        max_tokens = kwargs.get("max_tokens", MAX_TOKENS_PER_CALL)

        if provider == "anthropic":
            return self._call_anthropic(api_key, model, prompt, max_tokens)
        elif provider == "google":
            return self._call_google(api_key, model, prompt, max_tokens)
        else:
            # OpenAI-compatible: openai, perplexity, groq
            return self._call_openai_compat(provider, api_key, model, prompt, max_tokens)

    def _call_openai_compat(
        self, provider: str, api_key: str, model: str, prompt: str, max_tokens: int
    ) -> str:
        url = ENDPOINTS[provider]
        headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
        payload = {
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": max_tokens,
        }
        resp = self._http.post(url, headers=headers, json=payload)
        resp.raise_for_status()
        data = resp.json()
        text = data["choices"][0]["message"]["content"]
        tokens_in = data.get("usage", {}).get("prompt_tokens", 0)
        tokens_out = data.get("usage", {}).get("completion_tokens", 0)
        self._log_cost(provider, model, tokens_in, tokens_out)
        return text

    def _call_anthropic(self, api_key: str, model: str, prompt: str, max_tokens: int) -> str:
        url = ENDPOINTS["anthropic"]
        headers = {
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01",
            "Content-Type": "application/json",
        }
        payload = {
            "model": model,
            "max_tokens": max_tokens,
            "messages": [{"role": "user", "content": prompt}],
        }
        resp = self._http.post(url, headers=headers, json=payload)
        resp.raise_for_status()
        data = resp.json()
        text = data["content"][0]["text"]
        tokens_in = data.get("usage", {}).get("input_tokens", 0)
        tokens_out = data.get("usage", {}).get("output_tokens", 0)
        self._log_cost("anthropic", model, tokens_in, tokens_out)
        return text

    def _call_google(self, api_key: str, model: str, prompt: str, max_tokens: int) -> str:
        url = ENDPOINTS["google"].format(model=model) + f"?key={api_key}"
        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {"maxOutputTokens": max_tokens},
        }
        resp = self._http.post(url, json=payload)
        resp.raise_for_status()
        data = resp.json()
        text = data["candidates"][0]["content"]["parts"][0]["text"]
        usage = data.get("usageMetadata", {})
        tokens_in = usage.get("promptTokenCount", 0)
        tokens_out = usage.get("candidatesTokenCount", 0)
        self._log_cost("google", model, tokens_in, tokens_out)
        return text

    def _log_cost(self, provider: str, model: str, tokens_in: int, tokens_out: int) -> None:
        price_in, price_out = PRICING.get(provider, (0.0, 0.0))
        custo = (tokens_in / 1000 * price_in) + (tokens_out / 1000 * price_out)
        # Propaga course_id ativo (vazio se nao setado, mantendo compat)
        self.cost_tracker.track(
            provider, tokens_in, tokens_out, model, custo,
            course_id=self.current_course_id,
        )
        logger.info(
            "LLM %s/%s: %d tok_in, %d tok_out, USD %.4f (curso=%s)",
            provider, model, tokens_in, tokens_out, custo,
            self.current_course_id or "n/a",
        )

    # --- Métodos de conveniência por provider ---

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
