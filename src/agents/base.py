"""Classe base para todos os agentes do pipeline.

Cada agente encapsula um provider LLM, um modelo padrão e
um método execute() que faz a chamada via LLMClient.

Os prompts são carregados de arquivos externos em
src/templates/prompts/ para facilitar manutenção e versionamento.
"""

from __future__ import annotations

import logging
import re
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.llm_client import LLMClient

logger = logging.getLogger(__name__)


def _safe_substitute(template: str, substitutions: dict) -> str:
    """Replace only known named placeholders in a template string.

    Unlike str.format_map(), this function does not raise KeyError for unknown
    or literal {curly braces} (e.g. JSON examples inside markdown code blocks).
    It replaces only the keys listed in *substitutions* and leaves every other
    {…} token untouched.

    Args:
        template: Raw template string that may contain {placeholder} tokens and
            literal curly braces in code/JSON examples.
        substitutions: Mapping of placeholder name → replacement value.

    Returns:
        Template with known placeholders substituted.
    """
    def replace_match(match: re.Match) -> str:
        key = match.group(1)
        if key in substitutions:
            return substitutions[key]
        # Not a known placeholder — return the original {key} unchanged.
        return match.group(0)

    # Match {identifier} tokens only (letters, digits, underscores).
    return re.sub(r"\{([A-Za-z_][A-Za-z0-9_]*)\}", replace_match, template)


PROMPTS_DIR = Path(__file__).resolve().parent.parent / "templates" / "prompts"


class Agent:
    """Agente base que executa prompts via LLMClient."""

    nome: str = "base"
    provider: str = "openai"
    model: str = ""
    prompt_file: str = ""  # Nome do arquivo .md em templates/prompts/

    def __init__(self, client: LLMClient) -> None:
        self.client = client
        self._prompt_template: str | None = None

    def _load_prompt_template(self) -> str:
        """Carrega o prompt do arquivo externo em templates/prompts/."""
        if self._prompt_template is not None:
            return self._prompt_template

        if not self.prompt_file:
            self._prompt_template = ""
            return ""

        path = PROMPTS_DIR / self.prompt_file
        if not path.exists():
            logger.warning(
                "Arquivo de prompt não encontrado: %s. Usando prompt inline.",
                path,
            )
            self._prompt_template = ""
            return ""

        self._prompt_template = path.read_text(encoding="utf-8")
        logger.info(
            "Prompt carregado de %s (%d caracteres)",
            path.name,
            len(self._prompt_template),
        )
        return self._prompt_template

    def build_prompt(self, context: str, **template_vars: str) -> str:
        """Build the full prompt from the external template.

        If the external template file exists, substitutes all named placeholders
        using template_vars, with {context} as the fallback for agents that only
        use that single variable.  Subclasses may override with custom logic.

        Args:
            context: The pipeline context string passed through each step.
            **template_vars: Named variables expected by the external template
                (e.g. course_name, course_description, target_modules,
                draft_content, content).  When provided, these are substituted
                into the template in addition to — or instead of — {context}.
        """
        template = self._load_prompt_template()
        if template:
            # Build the substitution mapping: always include {context} so that
            # templates that use it (draft.md, review.md) keep working, plus
            # any extra named variables the caller supplies.
            substitutions = {"context": context}
            substitutions.update(template_vars)
            # Use _safe_substitute instead of str.format_map() to avoid
            # KeyError on literal {curly braces} in JSON/code examples inside
            # the .md templates (e.g., the JSON output schema in analyze.md).
            return _safe_substitute(template, substitutions)
        return context

    def execute(self, context: str, **template_vars: str) -> str:
        """Execute the agent: build the prompt and call the LLM.

        Args:
            context: Pipeline context string.
            **template_vars: Extra named variables forwarded to build_prompt()
                so that templates with named placeholders receive their values.
        """
        prompt = self.build_prompt(context, **template_vars)
        logger.info("Agente '%s' executando via %s/%s", self.nome, self.provider, self.model)
        logger.info("Prompt: %d caracteres", len(prompt))
        llm_kwargs: dict = {}
        if self.model:
            llm_kwargs["model"] = self.model
        result = self.client.call(self.provider, prompt, **llm_kwargs)
        logger.info(
            "Agente '%s' concluído (%d caracteres de resposta)",
            self.nome, len(result),
        )
        return result
