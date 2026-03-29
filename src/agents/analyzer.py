"""Agente de análise via Gemini.

Revisa qualidade, coerência e acessibilidade do conteúdo
gerado na etapa de redação.

Prompt externo: src/templates/prompts/analyze.md
"""

from __future__ import annotations

from src.agents.base import Agent


class Analyzer(Agent):
    """Agente Gemini para análise de qualidade do conteúdo."""

    nome = "analyzer"
    provider = "google"
    model = "gemini-2.5-pro"
    prompt_file = "analyze.md"

    # Fallback inline caso o arquivo externo não exista
    TEMPLATE = (
        "Você é um analista de qualidade educacional e design instrucional, com padrão editorial "
        "de Harvard Business Review, MIT Sloan e HSM Management.\n\n"
        "Analise o conteúdo abaixo em 7 dimensões:\n\n"
        "1. RIGOR INTELECTUAL: profundidade analítica, evidências, dados citados\n"
        "2. QUALIDADE EDITORIAL: tom (analítico vs. genérico), clichês, parágrafos concisos\n"
        "3. FORMATAÇÃO: tabelas por módulo, hierarquia de títulos, negrito, blocos de citação\n"
        "4. ANDRAGOGIA (Knowles): necessidade de saber, autoconceito, experiência prévia, "
        "prontidão, orientação a problemas, motivação intrínseca — avalie cada princípio\n"
        "5. GAPS: saltos cognitivos, conceitos omitidos, pré-requisitos implícitos\n"
        "6. EXERCÍCIOS: contexto profissional real, progressão Bloom, critérios claros\n"
        "7. ACENTUAÇÃO PT-BR: liste TODAS as palavras sem acento obrigatório encontradas\n\n"
        "Retorne JSON com score (0-100), notas por dimensão e lista de melhorias prioritárias.\n"
        "Escreva em Português do Brasil com acentuação completa.\n\n"
        "--- CONTEÚDO DO CURSO ---\n{context}"
    )

    def build_prompt(self, context: str) -> str:
        template = self._load_prompt_template()
        if template:
            return template.replace("{context}", context)
        return self.TEMPLATE.format(context=context)
