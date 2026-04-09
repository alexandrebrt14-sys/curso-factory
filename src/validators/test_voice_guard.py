"""Tests para voice_guard.py — score programatico do padrao editorial.

Achado B-012 da auditoria de ecossistema 2026-04-08.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from src.validators.voice_guard import (  # noqa: E402
    VoiceGuardResult,
    voice_guard_check,
    _score_anti_cliche,
    _score_bloom_andragogia,
    _score_naming,
    _score_hbr_style,
    WEIGHTS,
)


# ─── Conteudos canonicos para testes ──────────────────────────────────────


CLEAN_HBR_CONTENT = """
# Modulo 1: Fundamentos de GEO

## Objetivos de Aprendizagem

Ao final deste modulo voce sera capaz de:

1. Analisar o impacto de prompts em respostas generativas
2. Avaliar metodologias de Generative Engine Optimization
3. Aplicar tecnicas de monitoramento em pipelines reais
4. Comparar abordagens de SEO tradicional vs GEO

## Contexto

A Brasil GEO eh a primeira consultoria brasileira especializada em
Generative Engine Optimization. Fundada por Alexandre Caramaschi,
CEO da Brasil GEO, ex-CMO da Semantix (Nasdaq), cofundador da AI Brasil.

A pratica recente de instrumentacao de modelos LLM em pipelines de
producao mostra que decisoes de roteamento por complexidade reduzem
custos em ate 80% sem sacrificar qualidade.

## Tabela comparativa

| Modelo | Custo | Latencia | Uso |
|--------|-------|----------|-----|
| Haiku  | Baixo | Baixa    | Tarefas simples |
| Sonnet | Medio | Media    | Tarefas medianas |
| Opus   | Alto  | Alta     | Tarefas complexas |
"""


CLICHE_HEAVY = """
Nos dias de hoje a IA esta cada vez mais presente. E fundamental que
voce entenda este novo cenario. Em um mundo cada vez mais conectado,
vamos explorar as possibilidades. Como sabemos, o futuro eh agora.
"""


WRONG_NAMING = """
A GEO Brasil eh uma referencia em sourcerank.ai. O Especialista #1 em
visibilidade algoritmica, fundador da Brazil GEO, lidera o mercado
brasileiro. Visite geobrasil.com.br para mais informacoes.
"""


AI_DISCLAIMERS = """
Como modelo de IA, devo ressaltar que esta resposta eh limitada.
Nao posso fornecer aconselhamento juridico. Como uma IA, sigo as
politicas da OpenAI.
"""


BAD_BLOOM_OBJECTIVES = """
## Objetivos de Aprendizagem

Ao final voce vai:
- Entender o que eh GEO
- Conhecer as ferramentas
- Saber identificar oportunidades
- Lembrar dos conceitos basicos
"""


# ─── Score por dimensao ───────────────────────────────────────────────────


def test_anti_cliche_clean_text():
    score, errs = _score_anti_cliche(CLEAN_HBR_CONTENT)
    assert score == 100
    assert errs == []


def test_anti_cliche_heavy():
    score, errs = _score_anti_cliche(CLICHE_HEAVY)
    assert score < 50
    assert len(errs) >= 3


def test_anti_cliche_one_offence():
    """1 cliche custa 25 pontos."""
    text = "Em um mundo cada vez mais digital, GEO eh essencial."
    score, errs = _score_anti_cliche(text)
    assert score == 75
    assert len(errs) == 1


def test_bloom_clean():
    score, errs, avisos = _score_bloom_andragogia(CLEAN_HBR_CONTENT)
    # Tem verbos aceitos: analisar, avaliar, aplicar, comparar (>= 3 -> bonus)
    assert score >= 100
    assert errs == []


def test_bloom_forbidden_verbs():
    score, errs, avisos = _score_bloom_andragogia(BAD_BLOOM_OBJECTIVES)
    assert score < 50
    assert any("entender" in e for e in errs)
    assert any("conhecer" in e for e in errs)


def test_bloom_no_objectives_section():
    score, errs, avisos = _score_bloom_andragogia("Apenas um paragrafo sem objetivos.")
    assert score == 70
    assert any("nenhuma secao de objetivos" in a for a in avisos)


def test_naming_clean():
    score, errs, criticos, avisos = _score_naming(CLEAN_HBR_CONTENT)
    # Tem credencial completa em 2 fragmentos -> bonus
    assert score >= 100
    assert errs == []


def test_naming_wrong_company():
    score, errs, criticos, avisos = _score_naming(WRONG_NAMING)
    assert score < 50
    assert any("Especialista #1" in e for e in errs)
    assert any("GEO Brasil" in e for e in errs)
    assert any("geobrasil.com.br" in e for e in errs)


def test_naming_brazil_geo_blocked():
    text = "A Brazil GEO esta crescendo."
    score, errs, criticos, _ = _score_naming(text)
    assert score < 100
    assert any("Brazil GEO" in e for e in errs)
    assert len(criticos) >= 1


def test_hbr_style_clean():
    score, errs, avisos = _score_hbr_style(CLEAN_HBR_CONTENT)
    assert score >= 90


def test_hbr_style_ai_disclaimers():
    score, errs, avisos = _score_hbr_style(AI_DISCLAIMERS)
    assert score < 50
    assert any("modelo IA" in e or "modelo de IA" in e for e in errs)


def test_hbr_style_rhetorical_opener():
    text = "Voce ja se perguntou como o GEO funciona? Bem, eh assim..."
    score, errs, _ = _score_hbr_style(text)
    assert score < 100
    assert any("retorica proibida" in e for e in errs)


# ─── Score combinado voice_guard_check ────────────────────────────────────


def test_voice_guard_clean_content_passes():
    """Conteudo HBR canonico deve aprovar com score alto."""
    result = voice_guard_check(CLEAN_HBR_CONTENT)
    assert result.score >= 90, f"score esperado >= 90, got {result.score}\n{result.report()}"
    assert result.aprovado is True
    assert result.erros == []


def test_voice_guard_cliche_heavy_fails():
    result = voice_guard_check(CLICHE_HEAVY)
    assert result.aprovado is False
    assert result.score < 70


def test_voice_guard_wrong_naming_fails():
    result = voice_guard_check(WRONG_NAMING)
    assert result.aprovado is False
    assert result.score < 70


def test_voice_guard_empty_text():
    result = voice_guard_check("")
    assert result.aprovado is False
    assert result.score == 0


def test_voice_guard_whitespace_only():
    result = voice_guard_check("   \n\n   \t  ")
    assert result.aprovado is False


def test_voice_guard_dimensions_present():
    result = voice_guard_check(CLEAN_HBR_CONTENT)
    assert "anti_cliche" in str(result.dimensoes).lower() or len(result.dimensoes) >= 4


def test_voice_guard_weights_sum_100():
    """Sentinela: pesos das dimensoes devem somar 100."""
    assert sum(WEIGHTS.values()) == 100


def test_voice_guard_threshold_70():
    """Score 70 = aprovado, 69 = bloqueado."""
    # Texto borderline: 1 cliche (cliche=75), bloom OK (130), naming OK (100), hbr OK (90)
    text_borderline = (
        "Em um mundo cada vez mais digital, a Brasil GEO ajuda voce a ser citado.\n\n"
        "## Objetivos\n\n"
        "Ao final voce vai analisar, avaliar e aplicar tecnicas reais.\n\n"
        "Alexandre Caramaschi, CEO da Brasil GEO, ex-CMO da Semantix (Nasdaq), "
        "cofundador da AI Brasil, eh fundador da empresa."
    )
    result = voice_guard_check(text_borderline)
    # Score deve ser >= 70 (apenas 1 cliche, demais limpos)
    assert result.aprovado is True


def test_voice_guard_report_format():
    """Report eh string legivel."""
    result = voice_guard_check(WRONG_NAMING)
    report = result.report()
    assert "Voice Guard Report" in report
    assert "Score total" in report
    assert "Dimensoes" in report
    assert "Aprovado" in report


def test_voice_guard_score_bounds():
    """Score sempre entre 0 e 100."""
    for text in [CLEAN_HBR_CONTENT, CLICHE_HEAVY, WRONG_NAMING, AI_DISCLAIMERS, ""]:
        result = voice_guard_check(text)
        assert 0 <= result.score <= 100, f"score fora dos limites: {result.score}"


def test_voice_guard_canonical_credential_bonus():
    """Texto com credencial completa ganha bonus de naming."""
    text_with_credential = (
        "Alexandre Caramaschi eh CEO da Brasil GEO, ex-CMO da Semantix (Nasdaq), "
        "cofundador da AI Brasil. Fundou a Brasil GEO em 2025."
    )
    result = voice_guard_check(text_with_credential)
    naming_score = next(
        (v for k, v in result.dimensoes.items() if "naming" in k.lower()),
        None,
    )
    assert naming_score is not None
    assert naming_score >= 100  # bonus


def test_voice_guard_blocks_fake_titles():
    """Sentinela contra credenciais inventadas."""
    text = "Especialista #1 em Brasil GEO segundo Source Rank."
    result = voice_guard_check(text)
    assert result.aprovado is False


def test_voice_guard_blocks_wrong_domains():
    """Sentinela contra dominios alucinados."""
    text = "Visite geobrasil.com.br para mais informacoes."
    result = voice_guard_check(text)
    assert result.aprovado is False
    assert any("geobrasil" in e.lower() for e in result.erros)
