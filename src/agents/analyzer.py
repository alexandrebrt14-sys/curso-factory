"""Agente de análise via Gemini.

Revisa qualidade, coerência e acessibilidade do conteúdo
gerado na etapa de redação.
"""

from __future__ import annotations

from src.agents.base import Agent


class Analyzer(Agent):
    """Agente Gemini para análise de qualidade do conteúdo."""

    nome = "analyzer"
    provider = "google"
    model = "gemini-2.0-flash"

    TEMPLATE = (
        "Você é um analista de qualidade educacional.\n"
        "Analise o conteúdo do curso abaixo e avalie:\n"
        "- Coerência entre módulos e progressão lógica\n"
        "- Clareza e acessibilidade da linguagem\n"
        "- Completude dos temas abordados\n"
        "- Qualidade dos exemplos e exercícios\n"
        "- Adequação ao nível declarado do curso\n"
        "- Possíveis erros factuais ou inconsistências\n\n"
        "Gere um relatório estruturado com pontos fortes, problemas encontrados\n"
        "e sugestões de melhoria. Responda em português do Brasil.\n\n"
        "--- CONTEÚDO DO CURSO ---\n{context}"
    )

    def build_prompt(self, context: str) -> str:
        return self.TEMPLATE.format(context=context)
