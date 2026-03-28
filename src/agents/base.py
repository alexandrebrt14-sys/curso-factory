"""Classe base para todos os agentes do pipeline.

Cada agente encapsula um provider LLM, um modelo padrão e
um método execute() que faz a chamada via LLMClient.
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.llm_client import LLMClient

logger = logging.getLogger(__name__)


class Agent:
    """Agente base que executa prompts via LLMClient."""

    nome: str = "base"
    provider: str = "openai"
    model: str = ""

    def __init__(self, client: LLMClient) -> None:
        self.client = client

    def build_prompt(self, context: str) -> str:
        """Monta o prompt completo. Subclasses devem sobrescrever."""
        return context

    def execute(self, context: str) -> str:
        """Executa o agente: monta prompt e chama o LLM."""
        prompt = self.build_prompt(context)
        logger.info("Agente '%s' executando via %s/%s", self.nome, self.provider, self.model)
        kwargs = {}
        if self.model:
            kwargs["model"] = self.model
        result = self.client.call(self.provider, prompt, **kwargs)
        logger.info(
            "Agente '%s' concluído (%d caracteres de resposta)",
            self.nome, len(result),
        )
        return result
