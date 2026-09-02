"""Camada de resiliência do cliente LLM (wave 6, 02/09/2026).

Cobre os dois incidentes do teste ponta a ponta: cota esgotada tratada como
falha transitória (retry e circuito à toa) e HTTP 200 sem bloco de texto
derrubando a cadeia inteira. E prova o desenho novo: taxonomia de erro,
extração tolerante, cadeia de fallback por provedor, provedor morto na
sessão, erro de formato sem circuito.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import src.llm_client as lc  # noqa: E402
from src.llm_client import (  # noqa: E402
    AuthError,
    FallbackExhaustedError,
    LLMClient,
    ModelNotFoundError,
    QuotaExhaustedError,
    RateLimitError,
    RequestRejectedError,
    ResponseFormatError,
    TransientError,
    classificar_http,
    extrair_texto_anthropic,
    extrair_texto_google,
    extrair_texto_openai,
)

# ─── extração de texto ───────────────────────────────────────────────


def test_anthropic_concatena_blocos_de_texto_e_ignora_raciocinio() -> None:
    data = {"content": [{"type": "thinking", "thinking": "..."}, {"type": "text", "text": "a"}, {"type": "text", "text": "b"}],
            "stop_reason": "end_turn"}
    assert extrair_texto_anthropic("anthropic", data) == "ab"


def test_anthropic_sem_bloco_de_texto_e_erro_de_formato_com_diagnostico() -> None:
    data = {"content": [{"type": "thinking", "thinking": "..."}], "stop_reason": "max_tokens"}
    with pytest.raises(ResponseFormatError) as exc:
        extrair_texto_anthropic("anthropic", data)
    assert "thinking" in str(exc.value) and "max_tokens" in str(exc.value)


def test_openai_conteudo_vazio_por_raciocinio_ou_length() -> None:
    data = {"choices": [{"message": {"content": "", "reasoning": "pensando"}, "finish_reason": "length"}]}
    with pytest.raises(ResponseFormatError) as exc:
        extrair_texto_openai("groq", data)
    assert "max_tokens" in str(exc.value)
    assert extrair_texto_openai("openai", {"choices": [{"message": {"content": " ok "}}]}) == "ok"
    partes = {"choices": [{"message": {"content": [{"type": "text", "text": "x"}, {"type": "text", "text": "y"}]}}]}
    assert extrair_texto_openai("openai", partes) == "xy"


def test_google_ignora_partes_de_raciocinio_e_diagnostica_max_tokens() -> None:
    ok = {"candidates": [{"content": {"parts": [{"text": "pensando", "thought": True}, {"text": "resposta"}]}, "finishReason": "STOP"}]}
    assert extrair_texto_google("google", ok) == "resposta"
    vazio = {"candidates": [{"content": {}, "finishReason": "MAX_TOKENS"}]}
    with pytest.raises(ResponseFormatError) as exc:
        extrair_texto_google("google", vazio)
    assert "maxOutputTokens" in str(exc.value)
    bloqueado = {"promptFeedback": {"blockReason": "SAFETY"}, "candidates": []}
    with pytest.raises(RequestRejectedError):
        extrair_texto_google("google", bloqueado)


# ─── classificação de erro HTTP ──────────────────────────────────────


@pytest.mark.parametrize(
    ("status", "corpo", "classe"),
    [
        (429, '{"error":{"type":"insufficient_quota","code":"credit_balance_exhausted"}}', QuotaExhaustedError),
        (401, '{"error":{"message":"You exceeded your current quota","type":"insufficient_quota"}}', QuotaExhaustedError),
        (402, "payment required", QuotaExhaustedError),
        (401, '{"error":"invalid api key"}', AuthError),
        (404, '{"error":{"message":"The model llama-3.3-70b-versatile does not exist"}}', ModelNotFoundError),
        (400, '{"error":{"message":"model not found"}}', ModelNotFoundError),
        (429, '{"error":{"message":"Rate limit reached, retry in 2s"}}', RateLimitError),
        (503, "overloaded", TransientError),
        (400, '{"error":{"message":"max_tokens too large"}}', RequestRejectedError),
    ],
)
def test_classificar_http(status, corpo, classe) -> None:
    erro = classificar_http("openai", status, corpo)
    assert isinstance(erro, classe), erro
    assert erro.provider == "openai"


# ─── cliente com transporte falso ────────────────────────────────────


class _Ledger:
    def __init__(self) -> None:
        self.entradas = []

    def track(self, provider, tokens_in, tokens_out, model, custo_usd, course_id="") -> None:
        self.entradas.append(provider)


def _cliente(monkeypatch, respostas: dict, chaves=("openai", "anthropic", "google", "perplexity", "groq")):
    """`respostas[provider]` é uma lista de itens: string (sucesso) ou exceção a levantar, na ordem."""
    monkeypatch.setattr(lc, "get_api_key", lambda p: "chave" if p in chaves else (_ for _ in ()).throw(ValueError("sem chave")))
    monkeypatch.setattr(lc.time, "sleep", lambda s: None)
    client = LLMClient(cost_tracker=_Ledger(), use_cache=False)
    chamadas: list[str] = []

    def do_call(provider, prompt, **kw):
        chamadas.append(provider)
        fila = respostas.setdefault(provider, [])
        item = fila.pop(0) if fila else TransientError(provider, "fila vazia")
        if isinstance(item, Exception):
            raise item
        client._log_cost(provider, kw.get("model", "m"), 10, 10)
        return item

    monkeypatch.setattr(client, "_do_call", do_call)
    client.chamadas = chamadas
    return client


def test_cadeia_de_fallback_pula_quem_esta_morto_e_chega_ao_terceiro(monkeypatch) -> None:
    respostas = {
        "openai": [QuotaExhaustedError("openai", "sem crédito")],
        "anthropic": [ResponseFormatError("anthropic", "só thinking"), ResponseFormatError("anthropic", "só thinking")],
        "google": ["texto do gemini"],
    }
    client = _cliente(monkeypatch, respostas)
    assert client.call("openai", "escreva", model="gpt-5.5") == "texto do gemini"
    # openai morreu na primeira; anthropic tentou 2x (formato); google atendeu
    assert client.chamadas == ["openai", "anthropic", "anthropic", "google"]
    assert "sem crédito" in client.indisponivel("openai")
    # erro de formato NÃO abre o circuito da anthropic
    assert not client._get_circuit("anthropic").is_open
    # procedência: só o google foi cobrado
    assert client.cost_tracker.entradas == ["google"]


def test_provedor_morto_nao_e_chamado_de_novo_na_sessao(monkeypatch) -> None:
    respostas = {"openai": [QuotaExhaustedError("openai", "sem crédito")], "anthropic": ["a", "b"]}
    client = _cliente(monkeypatch, respostas)
    assert client.call("openai", "um") == "a"
    assert client.call("openai", "dois") == "b"
    assert client.chamadas.count("openai") == 1


def test_rate_limit_transitorio_faz_retry_e_abre_circuito_so_no_limiar(monkeypatch) -> None:
    respostas = {"openai": [RateLimitError("openai", "429"), RateLimitError("openai", "429"), "ok"]}
    client = _cliente(monkeypatch, respostas)
    assert client.call("openai", "p") == "ok"
    assert client.chamadas == ["openai", "openai", "openai"]
    assert not client._get_circuit("openai").is_open


def test_transitorio_persistente_abre_circuito_e_cai_no_fallback(monkeypatch) -> None:
    respostas = {"openai": [TransientError("openai", "503")] * 3, "anthropic": ["claude"]}
    client = _cliente(monkeypatch, respostas)
    assert client.call("openai", "p") == "claude"
    assert client._get_circuit("openai").is_open
    # com o circuito aberto, a chamada seguinte nem tenta a openai
    respostas["anthropic"].append("claude2")
    assert client.call("openai", "q") == "claude2"
    assert client.chamadas[-1] == "anthropic" and client.chamadas.count("openai") == 3


def test_cadeia_esgotada_traz_o_historico(monkeypatch) -> None:
    respostas = {
        "openai": [QuotaExhaustedError("openai", "sem crédito")],
        "anthropic": [AuthError("anthropic", "chave recusada")],
        "google": [ModelNotFoundError("google", "modelo indisponível")],
        "perplexity": [QuotaExhaustedError("perplexity", "quota")],
    }
    client = _cliente(monkeypatch, respostas)
    with pytest.raises(FallbackExhaustedError) as exc:
        client.call("openai", "p")
    msg = str(exc.value)
    for trecho in ("openai: sem crédito", "anthropic: chave recusada", "google: modelo", "perplexity: quota"):
        assert trecho in msg
    assert len(exc.value.tentativas) == 4


def test_sem_chave_pula_o_provedor_sem_chamar(monkeypatch) -> None:
    respostas = {"anthropic": ["claude"]}
    client = _cliente(monkeypatch, respostas, chaves=("anthropic",))
    assert client.call("openai", "p") == "claude"
    assert client.chamadas == ["anthropic"]
    assert client.indisponivel("openai") == "sem chave de API"


def test_pedido_rejeitado_nao_faz_retry_nem_abre_circuito(monkeypatch) -> None:
    respostas = {"openai": [RequestRejectedError("openai", "400")], "anthropic": ["claude"]}
    client = _cliente(monkeypatch, respostas)
    assert client.call("openai", "p") == "claude"
    assert client.chamadas == ["openai", "anthropic"]
    assert not client._get_circuit("openai").is_open


def test_modelo_do_pedido_nao_viaja_para_o_fallback(monkeypatch) -> None:
    modelos: list = []
    client = _cliente(monkeypatch, {})

    def do_call(provider, prompt, **kw):
        modelos.append((provider, kw.get("model")))
        if provider == "openai":
            raise QuotaExhaustedError(provider, "x")
        return "ok"

    monkeypatch.setattr(client, "_do_call", do_call)
    assert client.call("openai", "p", model="gpt-5.5") == "ok"
    assert modelos == [("openai", "gpt-5.5"), ("anthropic", None)]


def test_cadeias_do_yaml_cobrem_todos_os_provedores_sem_ciclo() -> None:
    from src.providers import FALLBACK_CHAINS, PROVIDERS

    for nome, cadeia in FALLBACK_CHAINS.items():
        assert nome not in cadeia
        assert len(cadeia) == len(set(cadeia))
        for p in cadeia:
            assert p in PROVIDERS, f"{nome}: fallback {p} não configurado"
    assert len(FALLBACK_CHAINS["openai"]) >= 2
    assert len(FALLBACK_CHAINS["perplexity"]) >= 2
