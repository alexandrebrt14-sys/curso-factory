"""Parsers compartilhados do curso-factory.

Centraliza funções de parsing reutilizadas entre geradores e conversores.
Antes da refatoração 2026-04-19, `schema_builder.py` e `draft_to_course.py`
tinham implementações paralelas divergentes de slugify, split por headings
e parsing de markdown em CourseSections.
"""

from src.parsers.markdown_parser import (
    extract_module_blocks,
    parse_module_to_sections,
    short_id,
    slugify,
)

__all__ = [
    "extract_module_blocks",
    "parse_module_to_sections",
    "short_id",
    "slugify",
]
