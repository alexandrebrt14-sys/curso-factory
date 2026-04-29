"""Testes da Wave 8 — Multi-idioma.

Cobre:
- Constantes e validação em ``src/i18n``.
- Cascata de resolução em ``src/agents/lang_resolver``.
- Estrutura de pastas ``src/templates/prompts/{en,es,pt-br}/``.
- Translator em modo dry-run.

Nenhum teste daqui aciona LLM real.
"""

from __future__ import annotations

import sys
from pathlib import Path
from unittest.mock import MagicMock

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.agents.lang_resolver import (  # noqa: E402
    PROMPTS_DIR,
    resolve_prompt_path,
)
from src.agents.translator import Translator  # noqa: E402
from src.i18n import (  # noqa: E402
    DEFAULT_LANGUAGE,
    SUPPORTED_LANGUAGES,
    is_supported,
)


REQUIRED_PROMPTS: tuple[str, ...] = (
    "research.md",
    "draft.md",
    "analyze.md",
    "classify.md",
    "review.md",
    "translate.md",
)


# ─── Constantes de idioma ────────────────────────────────────────────────


def test_supported_languages_minimum_set() -> None:
    """SUPPORTED_LANGUAGES contém pelo menos pt-br, en e es."""
    assert "pt-br" in SUPPORTED_LANGUAGES
    assert "en" in SUPPORTED_LANGUAGES
    assert "es" in SUPPORTED_LANGUAGES
    assert DEFAULT_LANGUAGE == "pt-br"


def test_is_supported_truthy_for_known_codes() -> None:
    """is_supported aceita os 3 idiomas e é case-insensitive."""
    assert is_supported("en") is True
    assert is_supported("EN") is True
    assert is_supported(" pt-br ") is True
    assert is_supported("es") is True


def test_is_supported_falsy_for_unknown_or_invalid() -> None:
    """Idiomas não suportados ou inputs inválidos retornam False."""
    assert is_supported("ja") is False
    assert is_supported("fr") is False
    assert is_supported("") is False
    assert is_supported(None) is False  # type: ignore[arg-type]


# ─── Estrutura de pastas e prompts traduzidos ────────────────────────────


def test_en_folder_has_six_prompts() -> None:
    """A pasta src/templates/prompts/en/ contém os 6 prompts esperados."""
    en_dir = PROMPTS_DIR / "en"
    assert en_dir.is_dir(), f"Pasta não existe: {en_dir}"
    for fname in REQUIRED_PROMPTS:
        path = en_dir / fname
        assert path.is_file(), f"Falta prompt EN: {path}"


def test_es_folder_has_six_prompts() -> None:
    """A pasta src/templates/prompts/es/ contém os 6 prompts esperados."""
    es_dir = PROMPTS_DIR / "es"
    assert es_dir.is_dir(), f"Pasta não existe: {es_dir}"
    for fname in REQUIRED_PROMPTS:
        path = es_dir / fname
        assert path.is_file(), f"Falta prompt ES: {path}"


def test_translated_prompts_are_non_empty() -> None:
    """Nenhum prompt traduzido pode estar vazio (mínimo 200 chars)."""
    for lang in ("en", "es"):
        for fname in REQUIRED_PROMPTS:
            path = PROMPTS_DIR / lang / fname
            content = path.read_text(encoding="utf-8")
            assert content.strip(), f"Prompt vazio: {path}"
            assert len(content) > 200, (
                f"Prompt suspeitamente curto em {path}: {len(content)} chars"
            )


# ─── Resolução com cascata ───────────────────────────────────────────────


def test_resolve_prompt_path_returns_target_language_when_present() -> None:
    """Idioma alvo presente: resolve direto para a pasta do idioma."""
    path = resolve_prompt_path("draft.md", "en")
    assert path == PROMPTS_DIR / "en" / "draft.md"
    assert path.is_file()


def test_resolve_prompt_path_falls_back_to_pt_br_for_unsupported() -> None:
    """Idioma não suportado (ja) cai para pt-br ou raiz, nunca falha."""
    path = resolve_prompt_path("draft.md", "ja")
    # Aceita tanto pt-br/ quanto raiz (cascata 2 ou 3).
    expected_pt_br = PROMPTS_DIR / "pt-br" / "draft.md"
    expected_root = PROMPTS_DIR / "draft.md"
    assert path in (expected_pt_br, expected_root)
    assert path.is_file()


def test_resolve_prompt_path_pt_br_explicit() -> None:
    """pt-br explícito resolve para a pasta pt-br/."""
    path = resolve_prompt_path("research.md", "pt-br")
    # Deve resolver dentro do diretório pt-br/ (criado na Wave 8).
    assert path == PROMPTS_DIR / "pt-br" / "research.md"
    assert path.is_file()


def test_resolve_prompt_path_raises_when_nothing_matches() -> None:
    """Arquivo inexistente em qualquer cascata levanta FileNotFoundError."""
    with pytest.raises(FileNotFoundError):
        resolve_prompt_path("does_not_exist_anywhere.md", "en")


# ─── Translator (dry-run) ────────────────────────────────────────────────


def test_translator_dry_run_returns_non_empty_string() -> None:
    """Translator em dry-run retorna resposta sem tocar o LLM."""
    fake_client = MagicMock()
    translator = Translator(client=fake_client, dry_run=True)

    result = translator.translate(
        content="# Módulo 1\n\nConteúdo de exemplo em PT-BR.",
        source_lang="pt-br",
        target_lang="en",
    )

    assert isinstance(result, str)
    assert result.strip()
    assert "pt-br" in result
    assert "en" in result
    # Não pode ter chamado o cliente LLM em dry-run.
    fake_client.call.assert_not_called()


def test_translator_real_mode_calls_llm() -> None:
    """Translator fora de dry-run delega ao LLMClient.call."""
    fake_client = MagicMock()
    fake_client.call.return_value = "translated content"
    translator = Translator(client=fake_client, dry_run=False)

    result = translator.translate(
        content="conteúdo",
        source_lang="pt-br",
        target_lang="es",
    )

    assert result == "translated content"
    fake_client.call.assert_called_once()
    # Verifica que o provider correto foi usado.
    args, kwargs = fake_client.call.call_args
    assert args[0] == "anthropic"
    # Verifica que o prompt construído inclui marcadores de idioma.
    prompt_arg = args[1]
    assert "pt-br" in prompt_arg
    assert "es" in prompt_arg
    assert "conteúdo" in prompt_arg
