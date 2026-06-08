"""Testes de regressão para dois fixes de robustez.

1. Humanizer deve invocar `client.call(...)` — antes chamava
   `client.completion(...)`, método inexistente em LLMClient; o `except`
   genérico engolia o AttributeError e o humanizer falhava silenciosamente
   em toda execução com cliente real.
2. LLMClient deve fechar o httpx.Client (close / context manager), para não
   vazar conexões TCP ao processar muitos cursos no mesmo processo.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.agents.humanizer import Humanizer  # noqa: E402


class _FakeClient:
    """Cliente que só expõe `call` — espelha a interface real de LLMClient.

    Se o Humanizer tentar `completion(...)`, levanta AttributeError, que o
    teste detecta via `motivo_parada`.
    """

    def __init__(self, resposta: str) -> None:
        self.resposta = resposta
        self.chamadas: list[tuple[str, str]] = []

    def call(self, provider: str, prompt: str, **kwargs: object) -> str:
        self.chamadas.append((provider, prompt))
        return self.resposta


# Texto de cadência deliberadamente uniforme (todas as frases ~iguais),
# para garantir score de stylometry baixo e disparar a reescrita.
_TEXTO_UNIFORME = " ".join(
    ["Este é um parágrafo de teste com sentenças de comprimento parecido."] * 8
)


def test_humanizer_invoca_call_e_nao_completion() -> None:
    resposta = (
        "Frase curta. Agora uma sentença bem mais longa, com vírgulas, "
        "subordinadas e ritmo variável que quebra a monotonia anterior do "
        "texto original de teste. Curto de novo. E segue."
    ) * 3
    fake = _FakeClient(resposta)
    humanizer = Humanizer(client=fake)  # type: ignore[arg-type]

    result = humanizer.run_iterative(_TEXTO_UNIFORME, target_score=100, max_iters=1)

    # O fix garante que `call` foi de fato invocado (sem AttributeError).
    assert len(fake.chamadas) >= 1
    assert "falha LLM" not in result.motivo_parada
    assert result.iters_realizadas >= 1


def test_humanizer_provider_propagado_para_call() -> None:
    fake = _FakeClient(_TEXTO_UNIFORME + " Final curto.")
    humanizer = Humanizer(client=fake)  # type: ignore[arg-type]
    humanizer.run_iterative(_TEXTO_UNIFORME, target_score=100, max_iters=1)
    assert fake.chamadas[0][0] == humanizer.provider  # "anthropic"


def test_llm_client_close_e_context_manager() -> None:
    from src.llm_client import LLMClient

    class _FakeHttp:
        def __init__(self) -> None:
            self.closed = False

        def close(self) -> None:
            self.closed = True

    with LLMClient(use_cache=False) as client:
        fake_http = _FakeHttp()
        client._http = fake_http  # type: ignore[assignment]
    # Ao sair do `with`, __exit__ → close() deve ter fechado o http.
    assert fake_http.closed is True


def test_llm_client_close_idempotente() -> None:
    from src.llm_client import LLMClient

    client = LLMClient(use_cache=False)
    client.close()
    client.close()  # segunda chamada não deve levantar
