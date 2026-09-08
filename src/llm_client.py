"""Cliente HTTP unificado para os LLMs do pipeline.

Camada de resiliência (wave 6, 02/09/2026), redesenhada depois de dois
incidentes no mesmo dia:

- A OpenAI sem crédito respondia 429 em toda chamada, e o cliente gastava
  três tentativas com backoff (2 s + 4 s) em cada uma das dez chamadas do
  curso antes de cair no fallback. Cota esgotada não é falha transitória:
  agora o provedor é marcado indisponível para a sessão na primeira resposta
  e nunca mais é chamado.
- A Anthropic respondia HTTP 200 e o cliente quebrava em `content[0]["text"]`
  quando o primeiro bloco não era texto. O erro de formato contava como falha
  do provedor, abria o circuito por 60 s e, com o fallback de um salto só
  (openai > anthropic > openai), o pipeline morria com "cadeia esgotada" sem
  nunca tentar o Google. Agora a extração de texto é tolerante a blocos de
  raciocínio e a partes vazias, erro de formato não abre circuito, e o
  fallback é uma cadeia por provedor (`config/providers.yaml`), percorrida
  pulando quem está morto, com circuito aberto ou sem chave.

Taxonomia de erro, que decide o que fazer:

| Classe                 | Quando                                   | Reação                                  |
|------------------------|------------------------------------------|-----------------------------------------|
| QuotaExhaustedError    | 401/402/403/429 com cota ou crédito zero | sem retry; provedor morto na sessão     |
| AuthError              | 401/403 sem menção a cota                | sem retry; provedor morto na sessão     |
| ModelNotFoundError     | 404, ou 400 dizendo que o modelo não existe | sem retry; provedor morto na sessão  |
| RateLimitError         | 429 transitório                          | retry com backoff; conta no circuito    |
| TransientError         | 5xx, timeout, falha de transporte        | retry com backoff; conta no circuito    |
| RequestRejectedError   | 400 por pedido inválido, bloqueio de segurança | sem retry; não conta no circuito  |
| ResponseFormatError    | 200 sem texto utilizável                 | uma repetição; não conta no circuito    |
| FallbackExhaustedError | nenhum provedor da cadeia respondeu      | sobe ao orquestrador com o histórico    |
"""

from __future__ import annotations

import logging
import os
import time
from dataclasses import dataclass, field
from typing import Any

import httpx

from src.cache import Cache
from src.config import MAX_TOKENS_PER_CALL, get_api_key
from src.cost_tracker import CostTracker

# Pricing, endpoints, modelos padrão e cadeias de fallback vêm de
# config/providers.yaml via src.providers. Os dicts são re-exportados para
# compatibilidade com imports externos.
from src.providers import (
    DEFAULT_MODELS,
    ENDPOINTS,
    FALLBACK_CHAINS,
    FALLBACK_MAP,
    MAX_TOKENS_BY_PROVIDER,
    PRICING,
)

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Taxonomia de erro
# ---------------------------------------------------------------------------


class LLMError(RuntimeError):
    """Base de todo erro do cliente; carrega o provedor."""

    def __init__(self, provider: str, mensagem: str) -> None:
        super().__init__(f"{provider}: {mensagem}")
        self.provider = provider
        self.mensagem = mensagem


class QuotaExhaustedError(LLMError):
    """Cota ou crédito esgotado. Não adianta repetir nem esperar."""


class AuthError(LLMError):
    """Chave inválida ou sem permissão."""


class ModelNotFoundError(LLMError):
    """O modelo pedido não existe mais neste provedor."""


class RateLimitError(LLMError):
    """429 transitório: vale repetir com backoff."""


class TransientError(LLMError):
    """5xx, timeout ou falha de transporte: vale repetir com backoff."""


class RequestRejectedError(LLMError):
    """Pedido inválido ou bloqueado (400 de payload, filtro de segurança)."""


class ResponseFormatError(LLMError):
    """HTTP 200 sem texto utilizável (bloco de raciocínio só, saída truncada, vazio)."""


class FallbackExhaustedError(LLMError):
    """Nenhum provedor da cadeia respondeu; `tentativas` guarda o histórico."""

    def __init__(self, provider: str, tentativas: list[str]) -> None:
        self.tentativas = tentativas
        super().__init__(provider, "cadeia de fallback esgotada: " + "; ".join(tentativas))


#: Sinais no corpo da resposta de que o problema é cota ou crédito.
_SINAIS_DE_COTA = (
    "insufficient_quota", "credit_balance_exhausted", "exceeded your current quota",
    "no credits remaining", "billing", "insufficient credits", "quota exceeded",
    "out of credits", "plan and billing", "credit balance",
)
_SINAIS_DE_MODELO = (
    "model not found", "does not exist", "not found for model", "unknown model",
    "model_not_found", "is not supported", "decommissioned", "has been deprecated",
    "no longer supported", "invalid model",
)


def classificar_http(provider: str, status: int, corpo: str) -> LLMError:
    """Traduz status e corpo de uma resposta HTTP de erro na classe certa."""
    texto = (corpo or "")[:600]
    baixo = texto.lower()
    resumo = texto.replace("\n", " ")[:200]
    if any(s in baixo for s in _SINAIS_DE_COTA) and status in (401, 402, 403, 429):
        return QuotaExhaustedError(provider, f"cota ou crédito esgotado (HTTP {status}): {resumo}")
    if status == 402:
        return QuotaExhaustedError(provider, f"pagamento exigido (HTTP 402): {resumo}")
    if status in (401, 403):
        return AuthError(provider, f"chave recusada (HTTP {status}): {resumo}")
    if status == 404 or (status == 400 and any(s in baixo for s in _SINAIS_DE_MODELO)):
        return ModelNotFoundError(provider, f"modelo indisponível (HTTP {status}): {resumo}")
    if status == 429:
        return RateLimitError(provider, f"limite de taxa (HTTP 429): {resumo}")
    if status >= 500:
        return TransientError(provider, f"erro do servidor (HTTP {status}): {resumo}")
    return RequestRejectedError(provider, f"pedido rejeitado (HTTP {status}): {resumo}")


# ---------------------------------------------------------------------------
# Extração de texto por protocolo (tolerante a bloco de raciocínio e a vazio)
# ---------------------------------------------------------------------------


def extrair_texto_openai(provider: str, data: dict) -> str:
    """`choices[0].message.content`; vazio com finish_reason=length é truncamento."""
    choices = data.get("choices") or []
    if not choices:
        raise ResponseFormatError(provider, f"resposta sem choices: {str(data)[:160]}")
    choice = choices[0]
    message = choice.get("message") or {}
    texto = message.get("content")
    if isinstance(texto, list):  # alguns provedores devolvem partes
        texto = "".join(p.get("text", "") for p in texto if isinstance(p, dict))
    texto = (texto or "").strip()
    if not texto:
        motivo = choice.get("finish_reason")
        if motivo == "length" or message.get("reasoning"):
            raise ResponseFormatError(
                provider,
                "resposta sem texto: a saída foi consumida pelo raciocínio ou truncada "
                f"(finish_reason={motivo}); aumente max_tokens ou troque o modelo",
            )
        raise ResponseFormatError(provider, f"resposta vazia (finish_reason={motivo})")
    return texto


def extrair_texto_anthropic(provider: str, data: dict) -> str:
    """Concatena todos os blocos `text`; bloco de raciocínio não é texto."""
    blocos = data.get("content") or []
    textos = [b.get("text", "") for b in blocos if isinstance(b, dict) and b.get("type") == "text"]
    texto = "".join(textos).strip()
    stop = data.get("stop_reason")
    if not texto:
        tipos = [b.get("type") for b in blocos if isinstance(b, dict)]
        raise ResponseFormatError(
            provider, f"resposta sem bloco de texto (blocos={tipos}, stop_reason={stop})"
        )
    if stop == "max_tokens":
        logger.warning("%s: saída truncada em max_tokens; o texto pode estar incompleto", provider)
    return texto


def extrair_texto_google(provider: str, data: dict) -> str:
    """Partes de texto do primeiro candidato, sem as partes de raciocínio."""
    feedback = data.get("promptFeedback") or {}
    if feedback.get("blockReason"):
        raise RequestRejectedError(provider, f"prompt bloqueado: {feedback.get('blockReason')}")
    candidatos = data.get("candidates") or []
    if not candidatos:
        raise ResponseFormatError(provider, f"resposta sem candidates: {str(data)[:160]}")
    cand = candidatos[0]
    partes = (cand.get("content") or {}).get("parts") or []
    textos = [p["text"] for p in partes if isinstance(p, dict) and "text" in p and not p.get("thought")]
    texto = "\n".join(t for t in textos if t).strip()
    if not texto:
        motivo = cand.get("finishReason")
        if motivo == "MAX_TOKENS":
            raise ResponseFormatError(
                provider, "resposta sem texto: o raciocínio consumiu maxOutputTokens; aumente o teto"
            )
        if motivo in ("SAFETY", "RECITATION", "BLOCKLIST", "PROHIBITED_CONTENT"):
            raise RequestRejectedError(provider, f"resposta bloqueada ({motivo})")
        raise ResponseFormatError(provider, f"resposta vazia (finishReason={motivo})")
    return texto


# ---------------------------------------------------------------------------
# Circuito e rate limit
# ---------------------------------------------------------------------------


@dataclass
class CircuitState:
    """Circuit breaker de um provedor: só falha transitória conta."""
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


# ---------------------------------------------------------------------------
# Cliente
# ---------------------------------------------------------------------------


class LLMClient:
    """Cliente unificado para múltiplos providers LLM."""

    def __init__(
        self,
        cost_tracker: CostTracker | None = None,
        cache: Cache | None = None,
        use_cache: bool = True,
    ) -> None:
        self.cost_tracker = cost_tracker or CostTracker()
        self.cache = cache if cache is not None else (Cache() if use_cache else None)
        self._circuits: dict[str, CircuitState] = {}
        self._buckets: dict[str, TokenBucket] = {}
        #: Provedores mortos nesta sessão (cota, chave, modelo): motivo por nome.
        self._indisponiveis: dict[str, str] = {}
        # Timeout de leitura configurável via env (HTTP_TIMEOUT). 600 s: o prompt
        # de research em sonar-deep-research passa de minutos, e geração densa
        # de aula não pode cair em fallback por pressa.
        self._http = httpx.Client(timeout=float(os.getenv("HTTP_TIMEOUT", "600")))
        # course_id ativo, setado pelo Orchestrator: toda chamada é tagueada
        # no CostTracker com o curso (achado F32 da auditoria 2026-04-08).
        self.current_course_id: str = ""

    # --- ciclo de vida ------------------------------------------------------

    def set_course_context(self, course_id: str) -> None:
        """Define o curso ativo para fins de tracking de custo."""
        self.current_course_id = course_id or ""

    def close(self) -> None:
        """Fecha o cliente HTTP subjacente. Idempotente."""
        http = getattr(self, "_http", None)
        if http is not None:
            http.close()

    def __enter__(self) -> LLMClient:
        return self

    def __exit__(self, *exc_info: object) -> None:
        self.close()

    def __del__(self) -> None:
        try:
            self.close()
        except Exception:  # noqa: BLE001
            pass

    # --- estado por provedor ------------------------------------------------

    def _get_circuit(self, provider: str) -> CircuitState:
        if provider not in self._circuits:
            self._circuits[provider] = CircuitState()
        return self._circuits[provider]

    def _get_bucket(self, provider: str) -> TokenBucket:
        if provider not in self._buckets:
            self._buckets[provider] = TokenBucket()
        return self._buckets[provider]

    def marcar_indisponivel(self, provider: str, motivo: str) -> None:
        """Tira o provedor da sessão: cota, chave ou modelo não se resolvem repetindo."""
        if provider not in self._indisponiveis:
            logger.error("%s fora da sessão: %s", provider, motivo)
        self._indisponiveis[provider] = motivo

    def indisponivel(self, provider: str) -> str:
        """Motivo para não chamar o provedor agora, ou string vazia se pode."""
        if provider in self._indisponiveis:
            return self._indisponiveis[provider]
        if provider not in ENDPOINTS:
            return "provedor não configurado"
        try:
            get_api_key(provider)
        except ValueError:
            return "sem chave de API"
        if self._get_circuit(provider).is_open:
            return "circuito aberto"
        return ""

    def cadeia(self, provider: str) -> list[str]:
        """O provedor pedido seguido da cadeia de fallback dele, sem repetição."""
        ordem = [provider] + list(FALLBACK_CHAINS.get(provider, ()))
        vistos: list[str] = []
        for p in ordem:
            if p not in vistos:
                vistos.append(p)
        return vistos

    # --- chamada ------------------------------------------------------------

    def call(self, provider: str, prompt: str, **kwargs: Any) -> str:
        """Chamada com cache, cadeia de fallback, circuito por provedor e retry por classe de erro.

        Percorre `cadeia(provider)`: pula quem está morto na sessão, com
        circuito aberto ou sem chave; em cada provedor vivo aplica a política
        de retry da classe de erro; se todos falharem, levanta
        `FallbackExhaustedError` com o histórico, que o orquestrador registra
        como erro da etapa.
        """
        kwargs.pop("_fallback_depth", None)  # compat com chamadores antigos
        model_for_cache = kwargs.get("model") or DEFAULT_MODELS.get(provider, "")
        if self.cache is not None:
            cached = self.cache.get(prompt, provider, model_for_cache)
            if cached is not None:
                return cached

        tentativas: list[str] = []
        for prov in self.cadeia(provider):
            motivo = self.indisponivel(prov)
            if motivo:
                tentativas.append(f"{prov}: {motivo}")
                continue
            kw = dict(kwargs)
            if prov != provider:
                # O modelo pedido pertence ao provedor original; o fallback usa o seu padrão.
                kw.pop("model", None)
                logger.info("Usando fallback: %s > %s", provider, prov)
            try:
                result = self._chamar_com_retry(prov, prompt, **kw)
            except LLMError as exc:
                tentativas.append(f"{prov}: {exc.mensagem}")
                continue
            if self.cache is not None and prov == provider:
                self.cache.set(prompt, provider, model_for_cache, result)
            return result

        raise FallbackExhaustedError(provider, tentativas)

    def _chamar_com_retry(self, provider: str, prompt: str, **kwargs: Any) -> str:
        """Política de retry por classe de erro num único provedor."""
        circuit = self._get_circuit(provider)
        self._get_bucket(provider).wait_and_consume()
        max_retries = int(kwargs.pop("max_retries", 3))
        base_delay = float(kwargs.pop("base_delay", 2.0))
        tentativas_formato = 0
        tentativas_transitorias = 0

        while True:
            try:
                result = self._do_call(provider, prompt, **kwargs)
                circuit.record_success()
                return result
            except (QuotaExhaustedError, AuthError, ModelNotFoundError) as exc:
                self.marcar_indisponivel(provider, exc.mensagem)
                raise
            except RequestRejectedError:
                raise
            except ResponseFormatError as exc:
                tentativas_formato += 1
                if tentativas_formato > 1:
                    raise
                logger.warning("%s: %s. Repetindo uma vez.", provider, exc.mensagem)
            except (RateLimitError, TransientError) as exc:
                circuit.record_failure()
                tentativas_transitorias += 1
                if tentativas_transitorias >= max_retries:
                    logger.error("Todas as tentativas falharam para %s: %s", provider, exc.mensagem)
                    raise
                delay = base_delay * (2 ** (tentativas_transitorias - 1))
                logger.warning(
                    "Tentativa %d/%d falhou para %s: %s. Aguardando %.1fs",
                    tentativas_transitorias, max_retries, provider, exc.mensagem, delay,
                )
                time.sleep(delay)

    def _do_call(self, provider: str, prompt: str, **kwargs: Any) -> str:
        """Executa a chamada HTTP real, traduzindo falhas na taxonomia."""
        api_key = get_api_key(provider)
        model = kwargs.get("model", DEFAULT_MODELS.get(provider, ""))
        # Teto de saída: o do chamador, senão o do provedor (providers.yaml),
        # senão o global. Modelo que raciocina dentro do teto precisa de folga.
        max_tokens = kwargs.get("max_tokens") or MAX_TOKENS_BY_PROVIDER.get(provider) or MAX_TOKENS_PER_CALL
        try:
            if provider == "anthropic":
                return self._call_anthropic(api_key, model, prompt, max_tokens)
            if provider == "google":
                return self._call_google(api_key, model, prompt, max_tokens)
            return self._call_openai_compat(provider, api_key, model, prompt, max_tokens)
        except httpx.HTTPStatusError as exc:
            raise classificar_http(provider, exc.response.status_code, exc.response.text) from exc
        except httpx.TimeoutException as exc:
            raise TransientError(provider, f"timeout: {exc}") from exc
        except httpx.TransportError as exc:
            raise TransientError(provider, f"falha de transporte: {exc}") from exc
        except LLMError:
            raise
        except (KeyError, IndexError, TypeError, ValueError) as exc:
            raise ResponseFormatError(provider, f"resposta com formato inesperado: {exc!r}") from exc

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
        text = extrair_texto_openai(provider, data)
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
        text = extrair_texto_anthropic("anthropic", data)
        tokens_in = data.get("usage", {}).get("input_tokens", 0)
        tokens_out = data.get("usage", {}).get("output_tokens", 0)
        self._log_cost("anthropic", model, tokens_in, tokens_out)
        return text

    def _call_google(self, api_key: str, model: str, prompt: str, max_tokens: int) -> str:
        url = ENDPOINTS["google"].format(model=model) + f"?key={api_key}"
        # Modelos com raciocínio consomem o teto de saída antes do texto
        # (gotcha conhecido: "thinking come maxOutputTokens"). Folga de 4x nos
        # modelos pro e 2x nos flash, com piso de 8.192.
        fator = 4 if "pro" in model else 2
        effective_max = max(8192, max_tokens * fator)
        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {"maxOutputTokens": effective_max},
        }
        resp = self._http.post(url, json=payload)
        resp.raise_for_status()
        data = resp.json()
        text = extrair_texto_google("google", data)
        usage = data.get("usageMetadata", {})
        tokens_in = usage.get("promptTokenCount", 0)
        tokens_out = usage.get("candidatesTokenCount", 0)
        self._log_cost("google", model, tokens_in, tokens_out)
        return text

    def _log_cost(self, provider: str, model: str, tokens_in: int, tokens_out: int) -> None:
        price_in, price_out = PRICING.get(provider, (0.0, 0.0))
        custo = (tokens_in / 1000 * price_in) + (tokens_out / 1000 * price_out)
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


# ---------------------------------------------------------------------------
# Factory de backend (B-019/D8 — strangler pattern, 2026-07-09)
# ---------------------------------------------------------------------------

def make_llm_client(
    cost_tracker: CostTracker | None = None,
    cache: Cache | None = None,
    use_cache: bool = True,
):
    """Retorna o cliente LLM do backend ativo.

    CURSO_FACTORY_LLM_BACKEND=sdk -> SDKLLMClient (geo_orchestrator_sdk):
    herda banda de timeout por task_type, fallback chain canônica, circuit
    breaker e FinOps unificado do orquestrador. Qualquer outro valor (ou
    ausente) -> LLMClient próprio, com a camada de resiliência deste módulo.
    """
    if os.getenv("CURSO_FACTORY_LLM_BACKEND", "").strip().lower() == "sdk":
        from src.llm_client_sdk import SDKLLMClient
        return SDKLLMClient(cost_tracker=cost_tracker, cache=cache, use_cache=use_cache)
    return LLMClient(cost_tracker=cost_tracker, cache=cache, use_cache=use_cache)


__all__ = [
    "AuthError", "CircuitState", "FALLBACK_MAP", "FallbackExhaustedError", "LLMClient",
    "LLMError", "ModelNotFoundError", "QuotaExhaustedError", "RateLimitError",
    "RequestRejectedError", "ResponseFormatError", "TokenBucket", "TransientError",
    "classificar_http", "extrair_texto_anthropic", "extrair_texto_google",
    "extrair_texto_openai", "make_llm_client",
]
