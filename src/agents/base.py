"""Classe base para todos os agentes do pipeline.

Cada agente encapsula um provider LLM, um modelo padrão e
um método execute() que faz a chamada via LLMClient.

Os prompts são carregados de arquivos externos em
src/templates/prompts/ para facilitar manutenção e versionamento.
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.llm_client import LLMClient

logger = logging.getLogger(__name__)

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

    def build_prompt(self, context: str) -> str:
        """Monta o prompt completo a partir do template externo.

        Se o arquivo externo existir, usa-o com {context} substituído.
        Caso contrário, subclasses podem sobrescrever com lógica própria.
        """
        template = self._load_prompt_template()
        if template:
            return template.replace("{context}", context)
        return context

    def execute(self, context: str) -> str:
        """Executa o agente: monta prompt e chama o LLM."""
        prompt = self.build_prompt(context)
        logger.info("Agente '%s' executando via %s/%s", self.nome, self.provider, self.model)
        logger.info("Prompt: %d caracteres", len(prompt))
        kwargs = {}
        if self.model:
            kwargs["model"] = self.model
        result = self.client.call(self.provider, prompt, **kwargs)
        logger.info(
            "Agente '%s' concluído (%d caracteres de resposta)",
            self.nome, len(result),
        )
        return result
