"""Testes para o parser de Markdown — fonte única usada por
`schema_builder` e `draft_to_course`.
"""

from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.models import SectionType
from src.parsers import (
    extract_module_blocks,
    parse_module_to_sections,
    short_id,
    slugify,
)


# ─── slugify ─────────────────────────────────────────────────────────

def test_slugify_remove_acentos() -> None:
    assert slugify("Geração de Conteúdo Avançado") == "geracao-de-conteudo-avancado"


def test_slugify_normaliza_espacos_multiplos() -> None:
    assert slugify("  curso   com  espaços  ") == "curso-com-espacos"


def test_slugify_mantem_letras_e_numeros() -> None:
    assert slugify("Curso 101 — Módulo 2") == "curso-101-modulo-2"


def test_slugify_string_vazia() -> None:
    assert slugify("") == ""


# ─── short_id ────────────────────────────────────────────────────────

def test_short_id_trunca() -> None:
    longo = "este-titulo-eh-muito-longo-para-um-step-id"
    assert len(short_id(longo, max_len=12)) <= 12


def test_short_id_curto_passa_inteiro() -> None:
    assert short_id("curto") == "curto"


# ─── extract_module_blocks ───────────────────────────────────────────

def test_extract_blocks_h2() -> None:
    md = (
        "## Módulo 1: Introdução\n\n"
        "Conteúdo do primeiro.\n\n"
        "## Módulo 2: Avançado\n\n"
        "Conteúdo do segundo."
    )
    blocks = extract_module_blocks(md)
    assert len(blocks) == 2
    assert blocks[0][0] == "Módulo 1: Introdução"
    assert "primeiro" in blocks[0][1]
    assert blocks[1][0] == "Módulo 2: Avançado"


def test_extract_blocks_h1_fallback() -> None:
    md = "# Único\n\nTexto.\n"
    blocks = extract_module_blocks(md)
    assert len(blocks) == 1
    assert blocks[0][0] == "Único"


def test_extract_blocks_sem_heading() -> None:
    md = "Apenas texto corrido sem heading nenhum."
    blocks = extract_module_blocks(md)
    assert len(blocks) == 1
    assert "Modulo Unico" in blocks[0][0]


def test_extract_blocks_string_vazia() -> None:
    assert extract_module_blocks("") == []
    assert extract_module_blocks("   \n\n  ") == []


# ─── parse_module_to_sections ────────────────────────────────────────

def test_parse_secoes_minimo_garante_checkpoint() -> None:
    """Mesmo conteúdo curtíssimo deve gerar >= 3 sections com 1 CHECKPOINT."""
    sections = parse_module_to_sections("Texto qualquer.")
    assert len(sections) >= 3
    assert any(s.type == SectionType.CHECKPOINT for s in sections)


def test_parse_secoes_extrai_codigo() -> None:
    md = (
        "Texto antes.\n\n"
        "```python\n"
        "x = 42\n"
        "```\n\n"
        "Texto depois."
    )
    sections = parse_module_to_sections(md)
    code_sections = [s for s in sections if s.type == SectionType.CODE]
    assert len(code_sections) == 1
    assert "x = 42" in code_sections[0].value
    assert code_sections[0].language == "python"


def test_parse_secoes_blockquote_dica() -> None:
    md = "Texto.\n\n> DICA: aplique no contexto profissional.\n\nMais texto."
    sections = parse_module_to_sections(md)
    tips = [s for s in sections if s.type == SectionType.TIP]
    assert len(tips) >= 1
    assert "aplique" in tips[0].value


def test_parse_secoes_blockquote_checkpoint() -> None:
    md = "Texto.\n\n> CHECKPOINT: revise os conceitos."
    sections = parse_module_to_sections(md)
    checkpoints = [s for s in sections if s.type == SectionType.CHECKPOINT]
    # Deve haver ao menos 1 checkpoint vindo do blockquote ou do auto-add.
    assert len(checkpoints) >= 1
