"""Constantes de idioma suportadas pela curso-factory.

Wave 8 — Multi-idioma (inspirado em Coursera, 50+ idiomas).
A primeira leva inclui pt-br (canônico), en (inglês americano padrão) e
es (espanhol padrão neutro). Novos idiomas devem ser adicionados em
SUPPORTED_LANGUAGES e ter seus prompts traduzidos em
`src/templates/prompts/<código>/`.
"""

from __future__ import annotations

# Lista canônica de códigos de idioma suportados pelo pipeline.
# Os códigos seguem BCP 47 simplificado (lower-case, hífen quando aplicável).
SUPPORTED_LANGUAGES: list[str] = ["pt-br", "en", "es"]

# Idioma padrão do projeto. Toda a base PT-BR é canônica e funciona como
# último fallback antes do diretório raiz `prompts/`.
DEFAULT_LANGUAGE: str = "pt-br"


def is_supported(lang: str) -> bool:
    """Retorna True se o idioma é oficialmente suportado.

    A comparação é case-insensitive e tolera espaços laterais. Códigos
    desconhecidos retornam False — o caller deve cair no DEFAULT_LANGUAGE.

    Args:
        lang: Código do idioma (ex.: "en", "pt-br", "ES").

    Returns:
        True se `lang` está em SUPPORTED_LANGUAGES.
    """
    if not isinstance(lang, str):
        return False
    return lang.strip().lower() in SUPPORTED_LANGUAGES
