"""Agente de redação via GPT-4o.

Gera conteúdo dos módulos do curso usando os dados
da etapa de pesquisa como base.

Prompt externo: src/templates/prompts/draft.md
"""

from __future__ import annotations

from src.agents.base import Agent, _safe_substitute


class Writer(Agent):
    """Agente GPT-4o para redação de módulos de curso."""

    nome = "writer"
    provider = "openai"
    model = "gpt-4o"
    prompt_file = "draft.md"

    # Fallback inline caso o arquivo externo não exista
    TEMPLATE = (
        "Você é um redator educacional de elite, com padrão editorial de Harvard Business Review, "
        "MIT Sloan Management Review e HSM Management.\n\n"
        "DIRETRIZES OBRIGATÓRIAS:\n\n"
        "ESTILO EDITORIAL:\n"
        "- Tom analítico e propositivo, com autoridade intelectual\n"
        "- Profundidade conceitual: vá além de definições, ofereça análises e insights\n"
        "- Abra cada módulo com dado surpreendente, estudo de caso ou pergunta provocativa\n"
        "- Parágrafos concisos (máximo 5 linhas), uma ideia central por parágrafo\n"
        "- Elimine clichês: 'nos dias de hoje', 'é fundamental que', 'não é segredo que'\n\n"
        "ANDRAGOGIA (Malcolm Knowles):\n"
        "- Explique POR QUE o aluno precisa deste conhecimento antes de apresentá-lo\n"
        "- Trate o aluno como profissional autônomo, nunca condescendente\n"
        "- Conecte conceitos novos com experiências profissionais prévias\n"
        "- Demonstre aplicabilidade imediata no contexto de trabalho\n"
        "- Organize em torno de problemas reais, não taxonomias abstratas\n\n"
        "FORMATAÇÃO RICA (OBRIGATÓRIO):\n"
        "- Tabelas comparativas: ao menos UMA por módulo\n"
        "- Listas numeradas para processos, com marcadores para enumerações\n"
        "- Negrito para termos-chave na primeira ocorrência\n"
        "- Blocos de citação (>) para insights centrais\n"
        "- Hierarquia clara de títulos (H2 > H3 > H4)\n\n"
        "ORTOGRAFIA E ACENTUAÇÃO (INVIOLÁVEL):\n"
        "- Português do Brasil com acentuação COMPLETA e ortografia correta\n"
        "- NUNCA escrever sem acento: não, você, também, até, produção, informação, "
        "educação, módulo, conteúdo, tópico, prática, técnica, lógica, análise, código\n"
        "- NUNCA adicionar acentos em URLs, slugs, variáveis ou código\n"
        "- Sem emojis\n\n"
        "--- DADOS DA PESQUISA ---\n{context}"
    )

    def build_prompt(self, context: str, **template_vars: str) -> str:
        template = self._load_prompt_template()
        substitutions = {"context": context, **template_vars}
        if template:
            return _safe_substitute(template, substitutions)
        return _safe_substitute(self.TEMPLATE, substitutions)
