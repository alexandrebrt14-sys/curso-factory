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


def test_default_client_company_populated():
    """Default tem seção company com nome e descrição preenchidos."""
    client = load_client("default")
    assert client.company.name == "Brasil GEO"
    assert "Brasil GEO" in client.company.description
    assert len(client.company.description) > 50


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


# ─── Template Jinja2 não contém hardcodes do cliente default ───────────


def test_page_template_has_no_client_hardcodes():
    """Sentinela: page.tsx.j2 não pode ter 'Brasil GEO' ou
    'alexandrecaramaschi.com' hardcoded. Tudo deve vir de variáveis Jinja2.
    """
    template_path = ROOT / "src" / "templates" / "page.tsx.j2"
    assert template_path.exists()
    content = template_path.read_text(encoding="utf-8")

    # Sentinela: nenhuma string do cliente default pode aparecer literalmente
    forbidden = ["Brasil GEO", "alexandrecaramaschi.com", "Alexandre Caramaschi"]
    for term in forbidden:
        assert term not in content, (
            f"page.tsx.j2 contém hardcode '{term}'. "
            f"Use variável Jinja2 ({{{{company_name}}}}, {{{{dominio}}}} ou {{{{autor_nome}}}}) em vez disso."
        )


def test_tsx_render_isolates_clients_no_leaks():
    """Renderização TSX de um curso sob cliente B não pode vazar dados do A.

    Sentinela E2E contra regressão: durante o refactor 2026-04-19 descobriu-se
    que `{% raw %}` blocks no page.tsx.j2 estavam impedindo interpolação
    Jinja2 de variáveis dentro do JSON-LD (bug pré-existente). Este teste
    garante que variáveis críticas sejam interpoladas de fato.
    """
    from src.generators.schema_builder import SchemaBuilder
    from src.generators.tsx_generator import TsxGenerator

    acme = load_client("acme")
    sb = SchemaBuilder()
    lorem = ("Paragrafo profundo com conteudo educacional detalhado. " * 50)
    md = (
        "## Modulo Um\n\n" + lorem + "\n\n> CHECKPOINT: Revise.\n\n" + lorem +
        "\n\n## Modulo Dois\n\n" + lorem + "\n\n> CHECKPOINT: Aplique.\n\n" + lorem
    )
    yaml_d = {
        "titulo": "Curso ACME",
        "descricao": "Descricao vinte caracteres minimo para validacao.",
    }
    course = sb.build("curso-acme", yaml_d, md, {}, client=acme)

    gen = TsxGenerator()
    page = gen.render_page(course)
    layout = gen.render_layout(course)

    # Nenhum dado do cliente default pode vazar
    for term in ["Brasil GEO", "alexandrecaramaschi.com", "Alexandre Caramaschi"]:
        assert term not in page, f"page.tsx vaza default: {term!r}"
        assert term not in layout, f"layout.tsx vaza default: {term!r}"

    # Dados do ACME devem estar presentes
    assert "Maria Silva" in page
    assert "ACME Consultoria" in page
    assert "acme-consultoria.com.br" in page
    assert "acme-consultoria.com.br" in layout

    # Path customizado do cliente aplicado
    assert "/cursos" in page
    assert 'href="/cursos"' in page

    # Bug de duplicação de protocolo (https://https://) corrigido
    assert "https://https://" not in page
    assert "https://https://" not in layout

    # Variáveis Jinja2 que deveriam ser interpoladas e ficaram literais (bug raw)
    import re
    unrendered = [m.group() for m in re.finditer(r"\{\{\s+[a-z_]+\s+\}\}", page)]
    assert not unrendered, (
        f"Variáveis Jinja2 não renderizadas em page.tsx: {unrendered}. "
        f"Provavelmente algum {{% raw %}} bloqueando — use {{{{ '{{' }}}} em vez."
    )


def test_course_definition_injects_company_from_client():
    """SchemaBuilder injeta company_name e company_description do ClientContext."""
    from src.generators.schema_builder import SchemaBuilder

    client = load_client("default")
    sb = SchemaBuilder()

    # Markdown com bastante texto (>6000 chars) para cada step
    # produzir duração suficiente (min 30 min total)
    lorem = (
        "Este é um parágrafo longo que simula conteúdo educacional real "
        "com profundidade analítica, dados de mercado e aplicações práticas "
        "para o profissional que está aprendendo o tema em questão. "
    ) * 30
    md = (
        f"## Módulo Um\n\n{lorem}\n\n"
        f"> CHECKPOINT: Revise os conceitos.\n\n"
        f"{lorem}\n\n"
        f"## Módulo Dois\n\n{lorem}\n\n"
        f"> CHECKPOINT: Aplique em seu contexto.\n\n"
        f"{lorem}\n"
    )
    yaml_def = {
        "titulo": "Curso de Teste",
        "descricao": "Descrição com pelo menos vinte caracteres para passar na validação Pydantic.",
    }

    course = sb.build("curso-teste", yaml_def, md, {}, client=client)
    # Os campos vêm do ClientContext, não dos defaults do Pydantic
    assert course.autor_nome == client.author.name
    assert course.dominio == client.domain.canonical_url
    assert course.company_name == client.company.name
    assert course.company_description == client.company.description
