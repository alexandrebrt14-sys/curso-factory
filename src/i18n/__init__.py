"""Pacote de internacionalização (i18n) da curso-factory.

Expõe constantes de idiomas suportados e utilitários de validação.
A pasta `src/templates/prompts/<lang>/` contém os prompts traduzidos.

Cascata de resolução (ver `src/agents/lang_resolver.py`):

    1. src/templates/prompts/<language>/<prompt_file>
    2. src/templates/prompts/pt-br/<prompt_file>
    3. src/templates/prompts/<prompt_file>          (fallback global)

Uso típico::

    from src.i18n import SUPPORTED_LANGUAGES, DEFAULT_LANGUAGE, is_supported

    if not is_supported(lang):
        lang = DEFAULT_LANGUAGE
"""

from __future__ import annotations

from src.i18n.constants import (
    DEFAULT_LANGUAGE,
    SUPPORTED_LANGUAGES,
    is_supported,
)

__all__ = ["DEFAULT_LANGUAGE", "SUPPORTED_LANGUAGES", "is_supported"]
