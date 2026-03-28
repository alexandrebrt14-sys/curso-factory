"""Agente de redação via GPT-4o.

Gera conteúdo dos módulos do curso usando os dados
da etapa de pesquisa como base.
"""

from __future__ import annotations

from src.agents.base import Agent


class Writer(Agent):
    """Agente GPT-4o para redação de módulos de curso."""

    nome = "writer"
    provider = "openai"
    model = "gpt-4o"

    TEMPLATE = (
        "Você é um redator educacional especializado em criar cursos online de alta qualidade.\n"
        "Com base na pesquisa abaixo, redija o conteúdo completo dos módulos do curso.\n"
        "Diretrizes:\n"
        "- Linguagem clara, acessível e engajante\n"
        "- Estruture cada módulo com: objetivos, conteúdo principal, exemplos práticos, resumo\n"
        "- Inclua exercícios de fixação ao final de cada módulo\n"
        "- Use formatação Markdown para organização\n"
        "- Português do Brasil com acentuação completa e correta\n"
        "- Sem emojis\n\n"
        "--- DADOS DA PESQUISA ---\n{context}"
    )

    def build_prompt(self, context: str) -> str:
        return self.TEMPLATE.format(context=context)
