"""Agente de pesquisa via Perplexity.

Busca dados atualizados sobre o tema do curso para
fundamentar a criação de conteúdo educacional.

Prompt externo: src/templates/prompts/research.md
"""

from __future__ import annotations

from src.agents.base import Agent


class Researcher(Agent):
    """Agente Perplexity para pesquisa de temas educacionais."""

    nome = "researcher"
    provider = "perplexity"
    model = "sonar-pro"
    prompt_file = "research.md"

    # Fallback inline caso o arquivo externo não exista
    TEMPLATE = (
        "Você é um pesquisador educacional com rigor acadêmico, especializado em fundamentar "
        "cursos online de alto padrão (Harvard Business Review, MIT Sloan, HSM Management).\n\n"
        "Pesquise e forneça:\n"
        "1. FUNDAMENTAÇÃO: conceitos-chave, frameworks teóricos, autores de referência\n"
        "2. DADOS DE MERCADO: tamanho, crescimento, ticket médio, concorrentes (com tabelas)\n"
        "3. EVIDÊNCIAS: pesquisas acadêmicas, estudos de caso reais, estatísticas com fontes\n"
        "4. TENDÊNCIAS 2025-2026: metodologias (andragogia, microlearning), ferramentas emergentes\n"
        "5. ANÁLISE COMPETITIVA: 5+ cursos concorrentes com preço, avaliação, pontos fortes/fracos\n"
        "6. CASOS PARA EXERCÍCIOS: 3-5 casos reais verificáveis para uso como exemplos didáticos\n\n"
        "FORMATO: Markdown estruturado com tabelas comparativas e referências completas.\n"
        "IDIOMA: Português do Brasil com acentuação completa e ortografia correta.\n\n"
        "--- CONTEXTO DO CURSO ---\n{context}"
    )

    def build_prompt(self, context: str) -> str:
        template = self._load_prompt_template()
        if template:
            return template.replace("{context}", context)
        return self.TEMPLATE.format(context=context)
