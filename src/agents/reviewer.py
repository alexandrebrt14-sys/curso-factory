"""Agente de revisão final via Claude.

Faz revisão completa do conteúdo com foco especial em
acentuação PT-BR e consistência editorial.
"""

from __future__ import annotations

from src.agents.base import Agent


class Reviewer(Agent):
    """Agente Claude para revisão final do curso."""

    nome = "reviewer"
    provider = "anthropic"
    model = "claude-opus-4-6"

    TEMPLATE = (
        "Você é um revisor editorial especializado em conteúdo educacional em português do Brasil.\n"
        "Faça a revisão final do conteúdo abaixo com atenção especial a:\n\n"
        "ACENTUAÇÃO (PRIORIDADE MÁXIMA):\n"
        "- Verifique TODAS as palavras que exigem acento em PT-BR\n"
        "- Corrija: nao→não, voce→você, e→é (quando verbo), producao→produção\n"
        "- NUNCA adicione acentos em URLs, slugs, nomes de variáveis ou código\n\n"
        "CONSISTÊNCIA EDITORIAL:\n"
        "- Uniformidade no tratamento (você/tu)\n"
        "- Coerência terminológica entre módulos\n"
        "- Formatação Markdown consistente\n"
        "- Sem emojis no conteúdo\n\n"
        "QUALIDADE GERAL:\n"
        "- Fluidez e naturalidade do texto\n"
        "- Precisão das informações\n"
        "- Clareza das instruções em exercícios\n\n"
        "Retorne o conteúdo revisado e corrigido na íntegra.\n\n"
        "--- CONTEÚDO PARA REVISÃO ---\n{context}"
    )

    def build_prompt(self, context: str) -> str:
        return self.TEMPLATE.format(context=context)
