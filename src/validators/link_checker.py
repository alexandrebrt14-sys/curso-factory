"""Validador de links e hrefs.

Verifica se links internos existem e se URLs não contêm
caracteres acentuados (regra crítica após incidente 2026-03-27
onde 55 hrefs foram corrompidos por acentuação indevida).
"""

from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass
from pathlib import Path
from typing import Optional


@dataclass
class LinkError:
    """Erro de validação de link."""
    tipo: str
    url: str
    mensagem: str
    linha: int = 0


# Regex para extrair URLs de href, src e links Markdown
HREF_PATTERN = re.compile(r'(?:href|src)=["\']([^"\']+)["\']', re.IGNORECASE)
MARKDOWN_LINK_PATTERN = re.compile(r'\[.*?\]\(([^)]+)\)')


def _has_accented_chars(text: str) -> bool:
    """Verifica se o texto contém caracteres acentuados."""
    nfkd = unicodedata.normalize("NFKD", text)
    for char in nfkd:
        if unicodedata.category(char) == "Mn":  # Marca de combinação (acento)
            return True
    return False


def _extract_urls(text: str) -> list[tuple[str, int]]:
    """Extrai todas as URLs do texto com seus números de linha."""
    urls: list[tuple[str, int]] = []
    for num_linha, linha in enumerate(text.split("\n"), start=1):
        for match in HREF_PATTERN.finditer(linha):
            urls.append((match.group(1), num_linha))
        for match in MARKDOWN_LINK_PATTERN.finditer(linha):
            urls.append((match.group(1), num_linha))
    return urls


def check_links(
    text: str,
    base_dir: Optional[Path] = None,
) -> list[LinkError]:
    """Valida todos os links encontrados no texto.

    Verificações:
    1. URLs não contêm caracteres acentuados (CRÍTICO)
    2. Links internos apontam para arquivos existentes
    3. URLs têm formato válido
    """
    errors: list[LinkError] = []
    urls = _extract_urls(text)

    for url, linha in urls:
        # Verificação crítica: acentos em URLs
        if _has_accented_chars(url):
            errors.append(LinkError(
                tipo="accent_in_url",
                url=url,
                mensagem=(
                    "URL contém caracteres acentuados. "
                    "Isso corrompe o link (ref: incidente 2026-03-27 com 55 hrefs corrompidos)"
                ),
                linha=linha,
            ))
            continue

        # Links internos (não começam com http/https/mailto/#)
        if not re.match(r"^(https?://|mailto:|#|javascript:)", url):
            if base_dir:
                target = base_dir / url
                if not target.exists():
                    errors.append(LinkError(
                        tipo="broken_internal",
                        url=url,
                        mensagem=f"Link interno aponta para arquivo inexistente: {target}",
                        linha=linha,
                    ))

        # URLs com espaços (geralmente erro)
        if " " in url and not url.startswith("mailto:"):
            errors.append(LinkError(
                tipo="invalid_url",
                url=url,
                mensagem="URL contém espaços não codificados",
                linha=linha,
            ))

    return errors


def format_report(errors: list[LinkError]) -> str:
    """Formata relatório de validação de links."""
    if not errors:
        return "Links: validação aprovada."
    linhas = [f"Links: {len(errors)} erro(s) encontrado(s):\n"]
    for e in errors:
        loc = f" (linha {e.linha})" if e.linha else ""
        linhas.append(f"  [{e.tipo}]{loc}: {e.url}")
        linhas.append(f"    {e.mensagem}")
    return "\n".join(linhas)
