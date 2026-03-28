"""Validador de HTML gerado pelo pipeline.

Verifica tags fechadas, atributos válidos, elementos obrigatórios
e acessibilidade básica.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from html.parser import HTMLParser


@dataclass
class HTMLError:
    """Erro de validação HTML."""
    tipo: str
    mensagem: str
    linha: int = 0


REQUIRED_ELEMENTS = {"html", "head", "title", "body", "main", "h1"}
VOID_ELEMENTS = {
    "area", "base", "br", "col", "embed", "hr", "img", "input",
    "link", "meta", "param", "source", "track", "wbr",
}


class _HTMLChecker(HTMLParser):
    """Parser interno que rastreia tags abertas e elementos encontrados."""

    def __init__(self) -> None:
        super().__init__()
        self.stack: list[tuple[str, int]] = []
        self.found_elements: set[str] = set()
        self.errors: list[HTMLError] = []
        self.has_lang: bool = False
        self.img_without_alt: list[int] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        line, _ = self.getpos()
        self.found_elements.add(tag)

        if tag == "html":
            attr_dict = dict(attrs)
            if "lang" in attr_dict:
                self.has_lang = True

        if tag == "img":
            attr_dict = dict(attrs)
            if "alt" not in attr_dict:
                self.img_without_alt.append(line)

        if tag not in VOID_ELEMENTS:
            self.stack.append((tag, line))

    def handle_endtag(self, tag: str) -> None:
        if tag in VOID_ELEMENTS:
            return
        line, _ = self.getpos()
        if not self.stack:
            self.errors.append(HTMLError("tag_extra", f"Tag de fechamento sem abertura: </{tag}>", line))
            return
        open_tag, open_line = self.stack[-1]
        if open_tag == tag:
            self.stack.pop()
        else:
            self.errors.append(HTMLError(
                "tag_mismatch",
                f"Esperado </{open_tag}> (aberto na linha {open_line}), encontrado </{tag}>",
                line,
            ))


def validate_html(html: str) -> list[HTMLError]:
    """Valida HTML e retorna lista de erros encontrados."""
    errors: list[HTMLError] = []
    checker = _HTMLChecker()

    try:
        checker.feed(html)
    except Exception as exc:
        errors.append(HTMLError("parse_error", f"Erro ao analisar HTML: {exc}"))
        return errors

    errors.extend(checker.errors)

    # Tags não fechadas
    for tag, line in checker.stack:
        errors.append(HTMLError("tag_unclosed", f"Tag não fechada: <{tag}>", line))

    # Elementos obrigatórios ausentes
    for elem in REQUIRED_ELEMENTS:
        if elem not in checker.found_elements:
            errors.append(HTMLError("missing_element", f"Elemento obrigatório ausente: <{elem}>"))

    # Acessibilidade: atributo lang em <html>
    if "html" in checker.found_elements and not checker.has_lang:
        errors.append(HTMLError("accessibility", "Atributo 'lang' ausente em <html>"))

    # Acessibilidade: imagens sem alt
    for line in checker.img_without_alt:
        errors.append(HTMLError("accessibility", f"Imagem sem atributo 'alt'", line))

    return errors


def format_report(errors: list[HTMLError]) -> str:
    """Formata relatório de validação HTML."""
    if not errors:
        return "HTML: validação aprovada."
    linhas = [f"HTML: {len(errors)} erro(s) encontrado(s):\n"]
    for e in errors:
        loc = f" (linha {e.linha})" if e.linha else ""
        linhas.append(f"  [{e.tipo}]{loc}: {e.mensagem}")
    return "\n".join(linhas)
