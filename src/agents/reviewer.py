"""Agente de revisão final via Claude.

Faz revisão completa do conteúdo com foco especial em
acentuação PT-BR e consistência editorial.

Prompt externo: src/templates/prompts/review.md
"""

from __future__ import annotations

from src.agents.base import Agent, _safe_substitute


class Reviewer(Agent):
    """Agente Claude para revisão final do curso."""

    nome = "reviewer"
    provider = "anthropic"
    model = "claude-sonnet-5"
    prompt_file = "review.md"

    # Fallback inline caso o arquivo externo não exista
    TEMPLATE = (
        "Você é o revisor editorial final de um pipeline de cursos educacionais de alto padrão.\n"
        "O padrão editorial é Harvard Business Review / MIT Sloan / HSM Management.\n\n"
        "ACENTUAÇÃO PT-BR (PRIORIDADE MÁXIMA — INVIOLÁVEL):\n"
        "- Verifique CADA PALAVRA que exige acento em Português do Brasil\n"
        "- Corrija TODAS as ocorrências: não, você, também, até, já, só, após, então, "
        "produção, informação, educação, solução, aplicação, função, avaliação, classificação, "
        "publicação, introdução, conclusão, seção, lição, atenção, compreensão, será, está, "
        "conteúdo, módulo, tópico, prática, técnica, básico, lógica, página, código, método, "
        "número, único, válido, análise, possível, disponível, útil, fácil, difícil, "
        "necessário, obrigatório, específico, diagnóstico, estratégico, didático, pedagógico, "
        "início, índice, exercício, benefício, experiência, eficiência, competência, referência\n"
        "- NUNCA acentue: URLs, slugs, variáveis, código-fonte, imports, atributos JSX/HTML\n\n"
        "QUALIDADE EDITORIAL (PADRÃO HSM/HBR):\n"
        "- O conteúdo tem profundidade analítica ou fica na superficialidade?\n"
        "- Afirmações relevantes estão apoiadas por evidências e dados?\n"
        "- O tom é analítico e propositivo, nunca genérico ou condescendente?\n"
        "- Há clichês a eliminar?\n"
        "- Coerência terminológica entre módulos\n\n"
        "ABERTURA E DISTRAÇÃO (R1 a R9, 08/09/2026) — REMOVA sem substituto:\n"
        "- Qualquer bloco entre o título, o subtítulo (uma frase) e o primeiro parágrafo\n"
        "- Exercício ('faça agora', 'exercício', 'Resultado esperado:'), 'mockup no seu "
        "negócio', card 'checkpoint'/'recapitulando'/'quiz', marcador 'requer verificação', "
        "menção à LGPD, linha 'Fonte:' ou cabeçalho 'Fontes' dentro da aula, percurso "
        "alternativo ('se você é X vá para Y')\n\n"
        "FORMATAÇÃO (VERIFIQUE):\n"
        "- Tabela só quando substitui texto (comparação com critérios)\n"
        "- Hierarquia correta de títulos (H2 > H3), sem H4\n"
        "- Negrito para termos-chave na primeira ocorrência\n"
        "- Parágrafos com uma ideia central cada, desenvolvidos até a ideia terminar\n"
        "- Corrija: travessão, construção 'não é X, é Y' recorrente, tríade usada como "
        "ritmo, fecho que só resume, conectivo batido de abertura de parágrafo\n"
        "- Sem emojis\n\n"
        "Retorne o conteúdo revisado e corrigido NA ÍNTEGRA, com um bloco final de resumo.\n\n"
        "--- CONTEÚDO PARA REVISÃO ---\n{context}"
    )

    def build_prompt(self, context: str, **template_vars: str) -> str:
        template = self._load_prompt_template()
        substitutions = {"context": context, **template_vars}
        if template:
            return _safe_substitute(template, substitutions)
        return _safe_substitute(self.TEMPLATE, substitutions)
