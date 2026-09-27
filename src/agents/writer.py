"""Agente de redação via GPT-4o.

Gera conteúdo dos módulos do curso usando os dados
da etapa de pesquisa como base.

Prompt externo: src/templates/prompts/pt-br/draft.md
"""

from __future__ import annotations

from src.agents.base import Agent, _safe_substitute


class Writer(Agent):
    """Agente GPT-4o para redação de módulos de curso."""

    nome = "writer"
    provider = "openai"
    model = "gpt-5.5"
    prompt_file = "draft.md"

    # Fallback inline caso o arquivo externo não exista
    # Fallback mínimo, só para o caso de o prompt externo sumir. As regras vivem
    # em src/templates/prompts/<idioma>/draft.md; aqui fica o suficiente para não
    # contradizê-las (até 27/09/2026 este texto pedia registro HBR e abertura em
    # cena, que a fonte de estilo proíbe).
    TEMPLATE = (
        "Você escreve UMA aula de curso para o dono de um pequeno negócio brasileiro, leigo "
        "em tecnologia, que lê no celular. Linguagem simples, frase direta, exemplo do ramo "
        "dele com nome de coisa real.\n\n"
        "- Abra com o subtítulo em UMA frase, em linha própria, e depois dois ou três "
        "parágrafos diretos ao ponto; sem cena, sem personagem, nada entre o título, o "
        "subtítulo e o primeiro parágrafo\n"
        "- Uma ideia só, explicada até o fim, com um caso do ramo do aluno contado inteiro, "
        "e um fecho com verbo no imperativo e critério de acerto\n"
        "- Nunca: exercício ou 'faça agora', 'mockup no seu negócio', card 'checkpoint', "
        "'requer verificação', menção à LGPD, linha 'Fonte:' no meio do texto, "
        "percurso alternativo, frase sobre a própria apuração\n"
        "- Todo número vem da pesquisa abaixo; o que não estiver lá não entra como fato\n"
        "- Sem travessão, sem 'não é X, é Y' como padrão, sem clichê, sem H4\n\n"
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
