"""Agente de classificação via Groq.

Classifica nível, tags, pré-requisitos e duração estimada
do curso com base no conteúdo analisado.

Prompt externo: src/templates/prompts/classify.md
"""

from __future__ import annotations

from src.agents.base import Agent


class Classifier(Agent):
    """Agente Groq para classificação de metadados do curso."""

    nome = "classifier"
    provider = "groq"
    model = "llama-3.3-70b-versatile"
    prompt_file = "classify.md"

    # Fallback inline caso o arquivo externo não exista
    TEMPLATE = (
        "Você é um classificador de conteúdo educacional.\n"
        "Com base no conteúdo e análise abaixo, determine:\n\n"
        "1. NÍVEL: iniciante, intermediário ou avançado\n"
        "2. TAGS: até 10 palavras-chave relevantes para indexação\n"
        "3. PRÉ-REQUISITOS: conhecimentos necessários para acompanhar o curso\n"
        "4. DURAÇÃO ESTIMADA: em horas, considerando leitura e exercícios\n"
        "5. PÚBLICO-ALVO: perfil dos alunos ideais\n\n"
        "Responda em formato JSON válido com as chaves:\n"
        "nivel, tags, pre_requisitos, duracao_horas, publico_alvo\n\n"
        "Responda em português do Brasil com acentuação correta.\n\n"
        "--- CONTEÚDO E ANÁLISE ---\n{context}"
    )

    def build_prompt(self, context: str) -> str:
        template = self._load_prompt_template()
        if template:
            return template.replace("{context}", context)
        return self.TEMPLATE.format(context=context)
