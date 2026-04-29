"""Testes do módulo de certificação — Wave 9.

Cobre geração determinística, verificação HMAC, renderização HTML,
validação do Skill Graph e edge cases (unicode, score abaixo do
threshold, QR code com lib ausente).
"""

from __future__ import annotations

from datetime import datetime, timezone

import pytest

from src.certification.certificate import (
    Certificate,
    generate_certificate,
    render_html,
    verify_certificate,
)
from src.certification.skill_graph import (
    Skill,
    find_courses_by_skill,
    validate_skills,
)
from src.models import CourseDefinition


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


def _make_course(slug: str = "geo-fundamentos") -> CourseDefinition:
    """CourseDefinition válido para os testes (descricao >= 20 chars)."""
    return CourseDefinition(
        slug=slug,
        titulo="Fundamentos de GEO para Executivos",
        descricao="Curso completo de Generative Engine Optimization para líderes de marketing.",
        autor_nome="Alexandre Caramaschi",
        autor_credencial="CEO da Brasil GEO, ex-CMO da Semantix (Nasdaq), cofundador da AI Brasil",
        dominio="https://alexandrecaramaschi.com",
        company_name="Brasil GEO",
        tags=["geo-ranking", "llm", "schema-org"],
    )


_FIXED_TS = datetime(2026, 4, 29, 12, 0, 0, tzinfo=timezone.utc)


# ---------------------------------------------------------------------------
# generate_certificate
# ---------------------------------------------------------------------------


def test_generate_certificate_id_deterministico():
    course = _make_course()
    cert_a = generate_certificate(
        "aluno@example.com", "João Silva", course, 0.85, "secret",
        issued_at=_FIXED_TS,
    )
    cert_b = generate_certificate(
        "ALUNO@example.com", "João Silva", course, 0.85, "secret",
        issued_at=_FIXED_TS,
    )
    # Email normalizado para lowercase => mesmo id e mesmo hash.
    assert cert_a.id == cert_b.id
    assert cert_a.id.startswith("geo-fundamentos-")
    assert len(cert_a.id.split("-")[-1]) == 12  # sufixo SHA-1[:12]


def test_generate_certificate_hash_deterministico():
    course = _make_course()
    cert_a = generate_certificate(
        "aluno@example.com", "João", course, 0.9, "secret",
        issued_at=_FIXED_TS,
    )
    cert_b = generate_certificate(
        "aluno@example.com", "João", course, 0.9, "secret",
        issued_at=_FIXED_TS,
    )
    assert cert_a.hash == cert_b.hash
    assert len(cert_a.hash) == 64  # SHA-256 hex


def test_generate_certificate_signature_diferente_de_hash():
    course = _make_course()
    cert = generate_certificate(
        "aluno@example.com", "João", course, 0.9, "secret",
        issued_at=_FIXED_TS,
    )
    assert cert.signature != cert.hash
    assert len(cert.signature) == 64  # HMAC-SHA256 hex


def test_generate_certificate_score_abaixo_do_threshold_levanta():
    course = _make_course()
    with pytest.raises(ValueError, match="reprovado"):
        generate_certificate(
            "aluno@example.com", "João", course, 0.5, "secret",
            issued_at=_FIXED_TS,
        )


def test_generate_certificate_threshold_customizado():
    course = _make_course()
    # Com pass_threshold=0.4, 0.5 passa.
    cert = generate_certificate(
        "aluno@example.com", "João", course, 0.5, "secret",
        pass_threshold=0.4, issued_at=_FIXED_TS,
    )
    assert cert.score == 0.5


def test_generate_certificate_score_fora_do_intervalo():
    course = _make_course()
    with pytest.raises(ValueError):
        generate_certificate(
            "aluno@example.com", "João", course, 1.5, "secret",
            issued_at=_FIXED_TS,
        )
    with pytest.raises(ValueError):
        generate_certificate(
            "aluno@example.com", "João", course, -0.1, "secret",
            issued_at=_FIXED_TS,
        )


def test_generate_certificate_secret_vazio():
    course = _make_course()
    with pytest.raises(ValueError, match="secret"):
        generate_certificate(
            "aluno@example.com", "João", course, 0.9, "",
            issued_at=_FIXED_TS,
        )


def test_generate_certificate_email_unicode_nao_quebra():
    """Email com chars unicode (raro mas permitido em RFC 6531)."""
    course = _make_course()
    cert = generate_certificate(
        "joão@exámple.com", "João Çávio", course, 0.95, "secret",
        issued_at=_FIXED_TS,
    )
    # Nome preserva acentuação PT-BR.
    assert cert.student_name == "João Çávio"
    # Email normalizado para lowercase.
    assert cert.student_email == "joão@exámple.com"
    assert verify_certificate(cert, "secret") is True


# ---------------------------------------------------------------------------
# verify_certificate
# ---------------------------------------------------------------------------


def test_verify_certificate_assinatura_correta():
    course = _make_course()
    cert = generate_certificate(
        "aluno@example.com", "João", course, 0.9, "my-secret",
        issued_at=_FIXED_TS,
    )
    assert verify_certificate(cert, "my-secret") is True


def test_verify_certificate_assinatura_errada():
    course = _make_course()
    cert = generate_certificate(
        "aluno@example.com", "João", course, 0.9, "my-secret",
        issued_at=_FIXED_TS,
    )
    assert verify_certificate(cert, "wrong-secret") is False


def test_verify_certificate_hash_adulterado():
    course = _make_course()
    cert = generate_certificate(
        "aluno@example.com", "João", course, 0.9, "my-secret",
        issued_at=_FIXED_TS,
    )
    tampered = cert.model_copy(update={"score": 0.99})
    assert verify_certificate(tampered, "my-secret") is False


# ---------------------------------------------------------------------------
# render_html
# ---------------------------------------------------------------------------


def test_render_html_contem_dados_chave():
    course = _make_course()
    cert = generate_certificate(
        "aluno@example.com", "Maria José", course, 0.92, "secret",
        issued_at=_FIXED_TS,
    )
    html = render_html(cert, course)

    # Nome do aluno presente.
    assert "Maria José" in html
    # Slug do curso presente.
    assert "geo-fundamentos" in html
    # Score formatado em porcentagem.
    assert "92.0%" in html
    # Naming canônico vindo de course (não hardcode).
    assert "Brasil GEO" in html
    assert "Alexandre Caramaschi" in html
    # Hash visível no footer.
    assert cert.hash in html
    # URL de verificação canônica.
    assert f"/certificado/{cert.hash}" in html


def test_render_html_url_verificacao_usa_dominio_do_course():
    course = _make_course()
    cert = generate_certificate(
        "aluno@example.com", "João", course, 0.9, "secret",
        issued_at=_FIXED_TS,
    )
    html = render_html(cert, course)
    assert "https://alexandrecaramaschi.com/certificado/" in html


# ---------------------------------------------------------------------------
# Skill Graph
# ---------------------------------------------------------------------------


def test_validate_skills_uri_invalido():
    skills = [
        Skill(id="geo", label="GEO", schema_org_uri="https://exemplo.com/skill"),
    ]
    issues = validate_skills(skills)
    assert len(issues) == 1
    assert "URI inválido" in issues[0]


def test_validate_skills_id_duplicado():
    skills = [
        Skill(id="geo", label="GEO"),
        Skill(id="geo", label="GEO Duplicado"),
    ]
    issues = validate_skills(skills)
    assert any("duplicado" in i.lower() for i in issues)


def test_validate_skills_tudo_ok():
    skills = [
        Skill(id="geo-ranking", label="Ranking em LLMs"),
        Skill(id="schema-org", label="Schema.org markup"),
    ]
    assert validate_skills(skills) == []


def test_find_courses_by_skill_filtra():
    c1 = _make_course("geo-fundamentos")
    c2 = _make_course("python-basico")
    c2.tags = ["python", "iniciante"]
    courses = [c1, c2]

    encontrados = find_courses_by_skill("geo-ranking", courses)
    assert len(encontrados) == 1
    assert encontrados[0].slug == "geo-fundamentos"


def test_find_courses_by_skill_sem_match():
    c1 = _make_course()
    assert find_courses_by_skill("ruby-on-rails", [c1]) == []


def test_find_courses_by_skill_id_vazio():
    c1 = _make_course()
    assert find_courses_by_skill("", [c1]) == []
    assert find_courses_by_skill("   ", [c1]) == []


# ---------------------------------------------------------------------------
# QR code (skip se lib indisponível)
# ---------------------------------------------------------------------------


def test_qr_to_base64_png_funciona_ou_skip():
    """Testa qr_to_base64_png; faz skip elegante se lib ausente."""
    pytest.importorskip("qrcode", reason="lib qrcode não instalada — skip")
    from src.certification.qrcode_helper import qr_to_base64_png

    result = qr_to_base64_png("https://example.com/certificado/abc123")
    # Base64 PNG decodificável e não-vazio.
    assert isinstance(result, str)
    assert len(result) > 100
    import base64 as _b64
    decoded = _b64.b64decode(result)
    # Magic bytes PNG: 89 50 4E 47.
    assert decoded[:4] == b"\x89PNG"


def test_qr_to_base64_png_url_vazia_levanta():
    from src.certification.qrcode_helper import qr_to_base64_png
    with pytest.raises(ValueError):
        qr_to_base64_png("")


def test_render_html_sem_qrcode_lib_nao_quebra(monkeypatch):
    """Mesmo sem qrcode, render_html retorna HTML válido."""
    course = _make_course()
    cert = generate_certificate(
        "aluno@example.com", "João", course, 0.9, "secret",
        issued_at=_FIXED_TS,
    )

    # Força fallback: substitui qr_to_base64_png por raise.
    import src.certification.certificate as cert_mod

    def _fake_qr(url, size=200):
        raise RuntimeError("qrcode lib indisponível (mock)")

    monkeypatch.setattr(cert_mod, "qr_to_base64_png", _fake_qr)
    html = render_html(cert, course)
    # HTML continua bem formado e contém a URL textual de verificação.
    assert "<!DOCTYPE html>" in html
    assert f"/certificado/{cert.hash}" in html
