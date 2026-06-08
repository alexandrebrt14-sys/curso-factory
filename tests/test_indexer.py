"""Tests para o parser de TypeScript do course_indexer.

Cobre `parse_courses_from_tsx` e os extratores de campo (`_extract_str`,
`_extract_int`, `_extract_tags`) — antes sem qualquer cobertura, apesar de
serem a porta de entrada de dados do indexador (regex frágil sobre TSX).
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.indexer.course_indexer import (  # noqa: E402
    _extract_int,
    _extract_str,
    _extract_tags,
    parse_courses_from_tsx,
)

# ─── Fixture: um page.tsx mínimo com dois cursos e ruído em volta ──────────
SAMPLE_TSX = '''
import { Foo } from "bar";

const courses: CourseData[] = [
  {
    id: "geo-101",
    title: "Fundamentos de GEO",
    description: "Uma introdução prática à otimização para motores generativos.",
    href: "/educacao/geo-101",
    modules: 8,
    duration: "4h",
    level: "iniciante",
    tags: ["geo", "seo", "iniciante"],
  },
  {
    id: "geo-202",
    title: "GEO Avançado",
    description:
      "Estratégias de citabilidade e earned media para LLMs.",
    href: "/educacao/geo-202",
    modules: 12,
    duration: "6h",
    level: "avancado",
    tags: ["geo", "avancado"],
  },
];

const faqItems = [
  { q: "O que é GEO?", a: "Generative Engine Optimization." },
];
'''


def _write_sample(tmp_path: Path, content: str = SAMPLE_TSX) -> Path:
    p = tmp_path / "page.tsx"
    p.write_text(content, encoding="utf-8")
    return p


# ─── _extract_str / _extract_int / _extract_tags ──────────────────────────

def test_extract_str_basico() -> None:
    obj = 'id: "geo-101", title: "Fundamentos"'
    assert _extract_str(obj, "id") == "geo-101"
    assert _extract_str(obj, "title") == "Fundamentos"


def test_extract_str_campo_ausente_retorna_vazio() -> None:
    assert _extract_str('id: "x"', "inexistente") == ""


def test_extract_int_basico_e_ausente() -> None:
    assert _extract_int("modules: 12", "modules") == 12
    assert _extract_int("modules: 12", "duration") == 0


def test_extract_tags_basico_e_vazio() -> None:
    assert _extract_tags('tags: ["a", "b", "c"]', "tags") == ["a", "b", "c"]
    assert _extract_tags("semtags: 1", "tags") == []


# ─── parse_courses_from_tsx ────────────────────────────────────────────────

def test_parse_courses_extrai_dois_cursos(tmp_path: Path) -> None:
    cursos = parse_courses_from_tsx(_write_sample(tmp_path))
    assert len(cursos) == 2
    assert {c.id for c in cursos} == {"geo-101", "geo-202"}


def test_parse_courses_campos_corretos(tmp_path: Path) -> None:
    cursos = parse_courses_from_tsx(_write_sample(tmp_path))
    primeiro = next(c for c in cursos if c.id == "geo-101")
    assert primeiro.title == "Fundamentos de GEO"
    assert primeiro.modules == 8
    assert primeiro.duration == "4h"
    assert primeiro.level == "iniciante"
    assert primeiro.tags == ["geo", "seo", "iniciante"]


def test_parse_courses_descricao_multilinha(tmp_path: Path) -> None:
    """A descrição do segundo curso está quebrada em duas linhas no TSX."""
    cursos = parse_courses_from_tsx(_write_sample(tmp_path))
    segundo = next(c for c in cursos if c.id == "geo-202")
    assert "earned media" in segundo.description


def test_parse_courses_array_ausente_retorna_vazio(tmp_path: Path) -> None:
    cursos = parse_courses_from_tsx(_write_sample(tmp_path, "const outraCoisa = 1;"))
    assert cursos == []


def test_parse_courses_objeto_sem_id_e_ignorado(tmp_path: Path) -> None:
    tsx = (
        'const courses: CourseData[] = [\n'
        '  { title: "Sem id", modules: 3 },\n'
        '  { id: "valido", title: "Tem id", modules: 5, tags: [] },\n'
        '];\n'
    )
    cursos = parse_courses_from_tsx(_write_sample(tmp_path, tsx))
    assert [c.id for c in cursos] == ["valido"]
