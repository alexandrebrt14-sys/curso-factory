"""Testes para o conversor de drafts JSON → CourseDefinition + TSX."""

from __future__ import annotations

import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.clients import load_client
from src.converters.draft_to_course import (
    convert_draft_to_course,
    convert_drafts_directory,
)


_DRAFT_REVIEWED = """
## Módulo 1: Fundamentos

A Geração de Engenharia Otimizada (GEO) é uma disciplina emergente que aplica
princípios de SEO ao contexto de respostas geradas por LLMs.

> DICA: pense em entidades, não em palavras-chave.

```python
client.search("GEO basics")
```

## Módulo 2: Aplicação

Aplique os conceitos em três passos práticos.
""".strip()


def _write_draft(tmp_path: Path, slug: str, etapa: str = "review") -> Path:
    payload = {
        "course_id": slug,
        "etapas": {etapa: _DRAFT_REVIEWED},
        "erros": [],
        "sucesso": True,
    }
    p = tmp_path / f"{slug}_20260101_120000.json"
    p.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
    return p


def test_convert_draft_basico(tmp_path) -> None:
    draft = _write_draft(tmp_path, "geo-fundamentos")
    course = convert_draft_to_course(draft)
    assert course is not None
    assert course.slug == "geo-fundamentos"
    assert len(course.steps) == 2
    assert course.duracao_total_minutos >= 30


def test_convert_draft_injeta_cliente(tmp_path) -> None:
    draft = _write_draft(tmp_path, "geo-cliente-test")
    client = load_client("default")
    course = convert_draft_to_course(draft, client=client)
    assert course is not None
    assert course.autor_nome == client.author.name
    assert course.dominio == client.domain.canonical_url
    assert course.company_name


def test_convert_draft_arquivo_invalido(tmp_path) -> None:
    bad = tmp_path / "broken.json"
    bad.write_text("não é json válido {", encoding="utf-8")
    assert convert_draft_to_course(bad) is None


def test_convert_draft_sem_conteudo(tmp_path) -> None:
    p = tmp_path / "empty_20260101_120000.json"
    p.write_text(json.dumps({"course_id": "empty", "etapas": {}}), encoding="utf-8")
    assert convert_draft_to_course(p) is None


def test_convert_draft_fallback_etapa_draft(tmp_path) -> None:
    """Se 'review' não está, deve cair pra 'draft'."""
    draft = _write_draft(tmp_path, "fallback-test", etapa="draft")
    course = convert_draft_to_course(draft)
    assert course is not None
    assert len(course.steps) == 2


def test_convert_drafts_directory_batch(tmp_path) -> None:
    inp = tmp_path / "drafts"
    inp.mkdir()
    out = tmp_path / "out"

    _write_draft(inp, "curso-um")
    _write_draft(inp, "curso-dois")
    # Arquivo broken — deve ser contado como falha, sem matar o batch
    (inp / "broken_20260101.json").write_text("{ bad", encoding="utf-8")
    # Arquivo de checkpoint — deve ser ignorado
    (inp / "outro_checkpoint.json").write_text(
        json.dumps({"course_id": "x", "etapas": {}}), encoding="utf-8"
    )

    result = convert_drafts_directory(inp, out)
    assert result["converted"] == 2
    assert result["failed"] == 1
    assert (out / "curso-um" / "page.tsx").exists()
    assert (out / "curso-um" / "layout.tsx").exists()
    assert (out / "curso-dois" / "page.tsx").exists()


def test_convert_drafts_directory_inexistente(tmp_path) -> None:
    result = convert_drafts_directory(tmp_path / "no_such", tmp_path / "out")
    assert "error" in result
    assert result["converted"] == 0
