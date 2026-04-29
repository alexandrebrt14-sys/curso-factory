"""Testes da camada de agent legibility (`src/agentic/`).

Cobre `llms.txt`, manifest MCP, payload A2A e geradores Schema.org.
Sem rede e sem dependência da landing-page-geo.
"""

from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

import pytest

# Garante que o diretório raiz do projeto está no sys.path.
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.agentic import (  # noqa: E402
    A2A_ENDPOINT_COURSE_INFO,
    A2A_ENDPOINT_ENROLL,
    A2A_ENDPOINT_PURCHASE,
    A2A_ENDPOINTS,
    MCP_ENDPOINTS,
    a2a_course_info,
    course_jsonld,
    generate_llms_txt,
    learning_resource_jsonld,
    mcp_manifest,
    organization_jsonld,
    write_llms_txt,
)
from src.clients import load_client  # noqa: E402
from src.clients.context import (  # noqa: E402
    Author,
    Branding,
    ClientContext,
    Company,
    Domain,
    Editorial,
    VoiceGuardConfig,
)
from src.models import (  # noqa: E402
    CourseDefinition,
    CourseSection,
    FAQItem,
    NivelCurso,
    SectionType,
    StepDefinition,
)


FIXTURES_DIR = Path(__file__).resolve().parent / "fixtures"


# ─── helpers ───────────────────────────────────────────────────────────────


def _load_sample_course() -> CourseDefinition:
    sample_path = FIXTURES_DIR / "sample_course.json"
    with open(sample_path, "r", encoding="utf-8") as fh:
        data = json.load(fh)
    return CourseDefinition(**data)


def _make_client(
    *,
    company_name: str = "Brasil GEO",
    author_name: str = "Alexandre Caramaschi",
    credential: str = "CEO da Brasil GEO, ex-CMO da Semantix (Nasdaq), cofundador da AI Brasil",
    canonical_url: str = "https://alexandrecaramaschi.com",
    client_id: str = "default",
) -> ClientContext:
    return ClientContext(
        id=client_id,
        author=Author(name=author_name, credential=credential),
        domain=Domain(canonical_url=canonical_url, educacao_path="/educacao"),
        company=Company(
            name=company_name,
            description=f"{company_name} — empresa de teste.",
        ),
        branding=Branding(),
        editorial=Editorial(),
        voice_guard=VoiceGuardConfig(enabled=False),
    )


def _make_acme_client() -> ClientContext:
    """Cliente alternativo para garantir que nada está hardcoded."""
    return _make_client(
        company_name="ACME Educação",
        author_name="Joana da Silva",
        credential="Diretora de Aprendizagem na ACME",
        canonical_url="https://acme.example.com",
        client_id="acme_test",
    )


def _make_minimal_course() -> CourseDefinition:
    """Curso edge: 1 step, sem skills/tags/keywords, fields opcionais vazios."""
    section_text = CourseSection(
        type=SectionType.TEXT,
        value="Conteúdo mínimo para validação do edge case.",
    )
    section_tip = CourseSection(
        type=SectionType.TIP,
        value="Dica curta para o edge case com acentuação válida.",
    )
    section_check = CourseSection(
        type=SectionType.CHECKPOINT,
        value="Você consegue rodar o pipeline mínimo sem quebrar?",
        label="CHECKPOINT",
    )
    step = StepDefinition(
        id="step-00",
        title="Único Módulo",
        duration="10 min",
        description="Edge case mínimo do curso",
        content=[section_text, section_tip, section_check],
    )
    return CourseDefinition(
        slug="curso-minimo",
        titulo="Curso Mínimo",
        descricao="Descrição mínima válida do curso para edge case com acentos.",
        nivel=NivelCurso.INICIANTE,
        steps=[step],
        autor_nome="",
        autor_credencial="",
        dominio="https://exemplo.test",
        company_name="",
    )


# ─── llms.txt ──────────────────────────────────────────────────────────────


def test_generate_llms_txt_atribuicao_e_modulos() -> None:
    """Inclui atribuição correta e lista todos os módulos do curso."""
    course = _load_sample_course()
    client = _make_client()

    out = generate_llms_txt(course, client)

    # Cabeçalho com título.
    assert out.startswith("# Teste de Geração")
    # Atribuição.
    assert "Autor: Alexandre Caramaschi" in out
    assert "ex-CMO da Semantix" in out
    assert "Empresa: Brasil GEO" in out
    assert "Domínio: https://alexandrecaramaschi.com" in out
    # Permissões padrão.
    assert "## Permissões para LLMs" in out
    assert "docs/knowledge/geo-aeo/" in out
    # Estrutura: lista os 2 módulos do sample.
    assert "Module 1: Introdução à Geração de Conteúdo" in out
    assert "Module 2: Validação e Qualidade" in out


def test_generate_llms_txt_no_hardcoded_brasil_geo() -> None:
    """Cliente alternativo não pode ter 'Brasil GEO' vazando."""
    course = _load_sample_course()
    # Sobrescreve identidade do course pelos campos do client alternativo.
    course = course.model_copy(
        update={
            "autor_nome": "Joana da Silva",
            "autor_credencial": "Diretora de Aprendizagem na ACME",
            "company_name": "ACME Educação",
            "dominio": "https://acme.example.com",
        }
    )
    acme = _make_acme_client()

    out = generate_llms_txt(course, acme)

    assert "ACME Educação" in out
    assert "Joana da Silva" in out
    assert "Brasil GEO" not in out
    assert "Alexandre Caramaschi" not in out


def test_generate_llms_txt_skills_listados() -> None:
    """Skills/keywords aparecem na seção 'Skills emitidos'."""
    course = _load_sample_course()
    client = _make_client()
    out = generate_llms_txt(course, client)

    assert "## Skills emitidos" in out
    # keywords_seo do fixture
    assert "- teste de geração" in out
    assert "- curso factory" in out


def test_write_llms_txt_path_e_idempotente() -> None:
    """Escreve no path correto e é idempotente entre chamadas."""
    course = _load_sample_course()
    client = _make_client()

    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        out_path = write_llms_txt(course, client, tmp_path)
        expected = tmp_path / course.slug / "llms.txt"
        assert out_path == expected
        assert out_path.exists()

        first = out_path.read_text(encoding="utf-8")

        # Idempotência: segunda chamada produz o mesmo conteúdo.
        out_path_2 = write_llms_txt(course, client, tmp_path)
        second = out_path_2.read_text(encoding="utf-8")
        assert first == second


def test_generate_llms_txt_curso_minimo_nao_quebra() -> None:
    """Edge: curso com 1 step, sem skills, sem company — não levanta."""
    course = _make_minimal_course()
    client = _make_client(company_name="", author_name="", credential="")

    out = generate_llms_txt(course, client)

    assert "# Curso Mínimo" in out
    assert "Module 1: Único Módulo" in out
    # Skills vazio cai para fallback.
    assert "(skills não declarados)" in out


# ─── MCP ───────────────────────────────────────────────────────────────────


def test_mcp_manifest_chaves_canonicas() -> None:
    """Manifest MCP tem chaves esperadas e versões do protocolo."""
    course = _load_sample_course()
    manifest = mcp_manifest(course)

    for key in ("name", "version", "endpoints", "protocol", "course"):
        assert key in manifest, f"Manifest sem chave '{key}'"

    assert manifest["name"] == f"curso-factory.mcp.{course.slug}"
    assert manifest["version"] == "1.0.0"
    assert manifest["protocol"].startswith("mcp/")
    assert manifest["course"]["slug"] == course.slug

    # Endpoints declarados são todos os 5 do contrato.
    endpoint_names = {ep["name"] for ep in manifest["endpoints"]}
    assert endpoint_names == {
        "list_modules",
        "get_module_content",
        "get_quiz",
        "submit_quiz_answer",
        "get_skills_taught",
    }


def test_mcp_endpoints_estrutura() -> None:
    """MCP_ENDPOINTS contém parâmetros e retornos descritos."""
    by_name = {ep.name: ep for ep in MCP_ENDPOINTS}
    assert "submit_quiz_answer" in by_name

    submit = by_name["submit_quiz_answer"]
    assert "quiz_id" in submit.parameters
    assert "answer" in submit.parameters
    assert submit.returns.get("type") == "QuizResult"

    # list_modules e get_skills_taught não recebem parâmetros.
    assert by_name["list_modules"].parameters == {}
    assert by_name["get_skills_taught"].parameters == {}


# ─── A2A ───────────────────────────────────────────────────────────────────


def test_a2a_course_info_jsonld_valido() -> None:
    """Payload A2A serializa como JSON e tem @context/@type corretos."""
    course = _load_sample_course()
    payload = a2a_course_info(course)

    # Serialização JSON funciona sem erro.
    serialized = json.dumps(payload, ensure_ascii=False)
    assert serialized
    parsed = json.loads(serialized)

    assert parsed["@context"] == "https://schema.org"
    assert parsed["@type"] == "Course"
    assert parsed["url"] == course.canonical_url
    # Capabilities canônicas.
    assert "list_modules" in parsed["agent_capabilities"]
    assert "purchase" in parsed["agent_capabilities"]
    # Endpoints batem com as constantes.
    assert parsed["agent_endpoints"]["purchase"].endswith(A2A_ENDPOINT_PURCHASE)
    assert parsed["agent_endpoints"]["enroll"].endswith(A2A_ENDPOINT_ENROLL)
    assert parsed["agent_endpoints"]["course_info"].endswith(
        A2A_ENDPOINT_COURSE_INFO
    )


def test_a2a_course_info_offer_paga_e_gratuita() -> None:
    """Oferta varia conforme price_brl."""
    course = _load_sample_course()

    free = a2a_course_info(course, price_brl=None)
    assert free["offers"]["price"] == "0"
    assert free["offers"]["category"] == "free"

    paid = a2a_course_info(course, price_brl=297.0)
    assert paid["offers"]["price"] == "297.00"
    assert paid["offers"]["priceCurrency"] == "BRL"
    assert paid["offers"]["category"] == "paid"


def test_a2a_endpoints_constants() -> None:
    """As constantes de endpoints estão expostas e batem com o dict."""
    assert A2A_ENDPOINTS["purchase"] == A2A_ENDPOINT_PURCHASE
    assert A2A_ENDPOINTS["enroll"] == A2A_ENDPOINT_ENROLL
    assert A2A_ENDPOINTS["course_info"] == A2A_ENDPOINT_COURSE_INFO


# ─── Schema.org ────────────────────────────────────────────────────────────


def test_course_jsonld_provider_instructor_teaches() -> None:
    """course_jsonld tem provider, instructor e teaches preenchidos."""
    course = _load_sample_course()
    payload = course_jsonld(course)

    assert payload["@type"] == "Course"
    assert payload["provider"]["@type"] == "Organization"
    assert payload["instructor"]["@type"] == "Person"
    assert isinstance(payload["teaches"], list)
    assert payload["teaches"]
    assert payload["timeRequired"].startswith("PT")
    assert payload["courseCode"] == course.slug
    assert "educationalCredentialAwarded" in payload


def test_learning_resource_jsonld_para_step() -> None:
    """LearningResource é gerado para um step individual."""
    course = _load_sample_course()
    step = course.steps[0]
    payload = learning_resource_jsonld(step)

    assert payload["@type"] == "LearningResource"
    assert payload["identifier"] == step.id
    assert payload["timeRequired"].startswith("PT")
    assert payload["inLanguage"] == "pt-BR"


def test_organization_jsonld_para_client() -> None:
    """organization_jsonld monta Organization com founder a partir do client."""
    client = load_client("default")
    payload = organization_jsonld(client)

    assert payload["@type"] == "Organization"
    assert payload["name"] == "Brasil GEO"
    assert payload["founder"]["name"] == "Alexandre Caramaschi"
    assert payload["url"].startswith("https://")


def test_course_jsonld_curso_minimo() -> None:
    """Edge: curso minimal não quebra os geradores Schema.org."""
    course = _make_minimal_course()
    payload = course_jsonld(course)
    assert payload["@type"] == "Course"
    assert payload["teaches"] == []
    # FAQ ausente → sem hasPart.
    assert "hasPart" not in payload


def test_course_jsonld_inclui_faq_quando_existe() -> None:
    """FAQs viram blocos Question/Answer dentro de hasPart."""
    course = _load_sample_course()
    # Garante que o fixture tem FAQ; senão o teste vira no-op.
    assert course.faq, "Fixture deveria ter FAQ definida"
    payload = course_jsonld(course)
    assert "hasPart" in payload
    assert all(item["@type"] == "Question" for item in payload["hasPart"])
    # Cada Question tem Answer aninhada.
    for item in payload["hasPart"]:
        assert item["acceptedAnswer"]["@type"] == "Answer"


# Sanity: verifica que FAQItem importado está em uso (lint).
def test_faq_item_imported() -> None:
    item = FAQItem(pergunta="Como funciona?", resposta="Funciona muito bem mesmo.")
    assert item.pergunta == "Como funciona?"
