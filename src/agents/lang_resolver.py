"""Resolução de prompts traduzidos com cascata de fallback.

Wave 8 — Multi-idioma. Permite que cada agente carregue o prompt na
língua escolhida, caindo de volta para PT-BR (canônico) e finalmente para
o prompt raiz quando o idioma alvo não tiver tradução.

NOTA DE INTEGRAÇÃO: este módulo NÃO modifica `src/agents/base.py` na Wave 8.
A integração com `Agent._load_prompt_template` ficou documentada em
`curso-factory.wiki/Multi-Language.md` e será aplicada numa wave futura,
quando o pipeline aceitar `editorial.language` no `client.yaml`.

Cascata::

    1. src/templates/prompts/<language>/<prompt_file>
    2. src/templates/prompts/pt-br/<prompt_file>
    3. src/templates/prompts/<prompt_file>            (fallback global)

Uso típico::

    from src.agents.lang_resolver import resolve_prompt_path

    path = resolve_prompt_path("draft.md", "en")
    template = path.read_text(encoding="utf-8")
"""

from __future__ import annotations

from pathlib import Path

from src.i18n.constants import DEFAULT_LANGUAGE

# Diretório raiz dos prompts. Espelha PROMPTS_DIR de `src/agents/base.py`,
# mas é resolvido de forma independente para evitar import circular.
PROMPTS_DIR = Path(__file__).resolve().parent.parent / "templates" / "prompts"


def resolve_prompt_path(prompt_file: str, language: str = DEFAULT_LANGUAGE) -> Path:
    """Resolve o caminho do prompt seguindo a cascata de idiomas.

    Args:
        prompt_file: Nome do arquivo de prompt (ex.: ``"draft.md"``).
        language: Código do idioma alvo (ex.: ``"en"``, ``"pt-br"``). Quando
            não suportado ou inexistente, cai automaticamente para
            ``DEFAULT_LANGUAGE`` e, em seguida, para o prompt raiz.

    Returns:
        ``Path`` absoluto do prompt encontrado.

    Raises:
        FileNotFoundError: se nenhum dos três níveis da cascata existir.
    """
    if not prompt_file:
        raise FileNotFoundError("prompt_file vazio: nada a resolver.")

    # Normaliza o código para casar com a estrutura de pastas (lower-case).
    lang = (language or DEFAULT_LANGUAGE).strip().lower()

    candidates: list[Path] = []

    # 1) Idioma alvo
    candidates.append(PROMPTS_DIR / lang / prompt_file)

    # 2) PT-BR (default canônico) — só se o alvo era diferente
    if lang != DEFAULT_LANGUAGE:
        candidates.append(PROMPTS_DIR / DEFAULT_LANGUAGE / prompt_file)

    # 3) Fallback global (raiz) — comportamento legado da curso-factory
    candidates.append(PROMPTS_DIR / prompt_file)

    for candidate in candidates:
        if candidate.is_file():
            return candidate

    tried = "\n  ".join(str(c) for c in candidates)
    raise FileNotFoundError(
        f"Prompt '{prompt_file}' não encontrado para idioma '{lang}'.\n"
        f"Caminhos tentados:\n  {tried}"
    )
