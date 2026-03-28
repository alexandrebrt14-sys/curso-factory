"""Agente de pesquisa via Perplexity.

Busca dados atualizados sobre o tema do curso para
fundamentar a criação de conteúdo educacional.
"""

from __future__ import annotations

from src.agents.base import Agent


class Researcher(Agent):
    """Agente Perplexity para pesquisa de temas educacionais."""

    nome = "researcher"
    provider = "perplexity"
    model = "sonar-pro"

    TEMPLATE = (
        "Você é um pesquisador educacional especializado em cursos online.\n"
        "Pesquise dados atualizados, tendências e referências sobre o tema abaixo.\n"
        "Foque em:\n"
        "- Principais conceitos e fundamentos do tema\n"
        "- Dados e estatísticas recentes\n"
        "- Melhores práticas de ensino para o assunto\n"
        "- Referências acadêmicas e de mercado relevantes\n"
        "- Lacunas comuns em cursos existentes sobre o tema\n\n"
        "Responda em português do Brasil com acentuação correta.\n\n"
        "--- CONTEXTO DO CURSO ---\n{context}"
    )

    def build_prompt(self, context: str) -> str:
        return self.TEMPLATE.format(context=context)
