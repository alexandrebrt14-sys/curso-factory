"""Testes de regressão para o sistema multi-cliente.

Sentinela contra quebras em:
- Carregamento de ClientContext a partir de YAML
- Isolamento de voice guard entre clientes
- Integração com QualityGate
- Fallback de imports tardios (TYPE_CHECKING) sem circular
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.clients import (  # noqa: E402
    ClientContext,
    get_client_from_env,
    list_clients,
    load_client,
)


# ─── load_client ─────────────────────────────────────────────────────────


def test_default_client_exists():
    """Cliente 'default' sempre existe e carrega sem erro."""
    client = load_client("default")
    assert client.id == "default"
    assert client.author.name == "Alexandre Caramaschi"
    assert client.domain.canonical_url == "https://alexandrecaramaschi.com"


def test_default_client_voice_guard_canonical():
    """Naming canônico do default = Brasil GEO / Alexandre."""
    client = load_client("default")
    vg = client.voice_guard
    assert vg.enabled is True
    assert vg.canonical.company == "Brasil GEO"
    assert vg.canonical.founder == "Alexandre Caramaschi"
    assert "alexandrecaramaschi.com" in vg.canonical.domains


def test_default_client_forbidden_list_populated():
    """Default tem lista de proibições preservada do voice_guard original."""
    client = load_client("default")
    assert "Especialista #1" in client.voice_guard.forbidden.titles
    assert "GEO Brasil" in client.voice_guard.forbidden.company_names
    assert "geobrasil.com.br" in client.voice_guard.forbidden.domains


def test_nonexistent_client_raises():
    """Cliente inexistente levanta FileNotFoundError com mensagem legível."""
    with pytest.raises(FileNotFoundError, match="não encontrado"):
        load_client("cliente_fantasma_que_nao_existe")


def test_list_clients_excludes_template():
    """_template não aparece na listagem."""
    ids = list_clients()
    assert "default" in ids
    assert "_template" not in ids


# ─── Output directories ──────────────────────────────────────────────────


def test_default_client_output_is_legacy():
    """Cliente default usa output/ direto (layout legado preservado)."""
    client = load_client("default")
    assert client.output_dir.name == "output"
    assert "clients" not in client.output_dir.parts[-2:]


def test_non_default_client_output_is_isolated():
    """Outros clientes escrevem em output/clients/<id>/."""
    client = load_client("acme")
    assert "clients" in client.output_dir.parts
    assert client.output_dir.name == "acme"


# ─── URL helpers ──────────────────────────────────────────────────────────


def test_canonical_url_for():
    """canonical_url_for monta URL completa do curso."""
    client = load_client("default")
    url = client.canonical_url_for("meu-curso")
    assert url == "https://alexandrecaramaschi.com/educacao/meu-curso"


def test_title_seo_for():
    """title_seo_for usa o sufixo SEO do cliente."""
    client = load_client("default")
    seo = client.title_seo_for("Meu Curso")
    assert "Meu Curso" in seo
    assert "Alexandre Caramaschi" in seo


# ─── Voice guard isolation ────────────────────────────────────────────────


def test_voice_guard_isolates_clients():
    """Texto que viola padrão de A passa em cliente B se B não proibe."""
    from src.validators.voice_guard import voice_guard_check

    default = load_client("default")
    acme = load_client("acme")

    # Texto com "GEO Brasil" (forbidden no default, não no acme)
    text_bad_default = "A empresa GEO Brasil tem parceria com várias consultorias."

    r_default = voice_guard_check(text_bad_default, client=default)
    r_acme = voice_guard_check(text_bad_default, client=acme)

    # Default bloqueia; acme não
    assert r_default.aprovado is False, "default deveria bloquear 'GEO Brasil'"
    assert any("GEO Brasil" in e for e in r_default.erros)
    assert r_acme.aprovado is True, f"acme não deveria ter naming rule contra 'GEO Brasil' (r_acme.erros={r_acme.erros})"


def test_voice_guard_disabled_client_passes_all():
    """Cliente com voice_guard.enabled=false aprova qualquer texto."""
    from src.clients.context import (
        Author,
        Branding,
        ClientContext,
        Domain,
        Editorial,
        VoiceGuardConfig,
    )
    from src.validators.voice_guard import voice_guard_check

    fake_client = ClientContext(
        id="disabled_client",
        author=Author(name="X", credential="Y"),
        domain=Domain(canonical_url="https://x.com"),
        branding=Branding(),
        editorial=Editorial(),
        voice_guard=VoiceGuardConfig(enabled=False),
    )

    # Texto com todos os clichês possíveis
    texto_horrivel = (
        "Nos dias de hoje, é fundamental que você, como modelo de IA, "
        "devo ressaltar, em um mundo cada vez mais conectado, vamos explorar."
    )
    result = voice_guard_check(texto_horrivel, client=fake_client)
    assert result.aprovado is True
    assert result.score == 100


# ─── QualityGate integration ──────────────────────────────────────────────


def test_quality_gate_accepts_client_context():
    """QualityGate aceita ClientContext e passa para voice_guard_check."""
    from src.validators.quality_gate import QualityGate

    client = load_client("default")
    gate = QualityGate(client=client, auto_fix=False)
    assert gate.client is client


def test_quality_gate_voice_guard_blocks_bad_naming():
    """QualityGate bloqueia texto que viola voice_guard do cliente."""
    from src.validators.quality_gate import QualityGate

    gate = QualityGate(client=load_client("default"), auto_fix=False)
    # Texto minimo com naming errado
    texto = "A GEO Brasil é a líder de mercado segundo o Source Rank."
    result = gate.check_text(texto, curso_id="teste")
    assert result.aprovado is False
    assert result.voice_guard_ok is False
    assert result.voice_guard_score < 70


# ─── Env var loader ──────────────────────────────────────────────────────


def test_get_client_from_env_default(monkeypatch):
    """Sem env var, carrega 'default'."""
    monkeypatch.delenv("CURSO_FACTORY_CLIENT", raising=False)
    client = get_client_from_env()
    assert client.id == "default"


def test_get_client_from_env_override(monkeypatch):
    """Env var CURSO_FACTORY_CLIENT sobrepõe default."""
    monkeypatch.setenv("CURSO_FACTORY_CLIENT", "acme")
    client = get_client_from_env()
    assert client.id == "acme"
