"""Tutor IA conversacional runtime — 6º agente do projeto curso-factory.

Diferente dos 5 agentes do pipeline (Researcher, Writer, Analyzer, Classifier,
Reviewer), o Tutor NÃO gera o curso. Ele conversa com o aluno em tempo real,
DEPOIS que o curso já foi publicado, dentro da página do curso.

Inspirações: Coursera Coach, Duolingo Max (Explain My Answer), Khanmigo.

Três modos de uso:
- EXPLAIN_LIKE_5: explica em linguagem simples com analogia concreta.
- PRACTICAL_EXAMPLE: gera exemplo aplicado ao contexto do aluno.
- QUIZ_ME: faz pergunta aberta de Bloom 3+ sem dar a resposta.

Uso típico (produção):

    from src.llm_client import LLMClient
    from src.agents.tutor import Tutor, TutorMode

    tutor = Tutor(client=LLMClient(), persona="curiosa-paciente")
    resposta = tutor.respond(
        question="Como funciona prompt caching na prática?",
        mode=TutorMode.PRACTICAL_EXAMPLE,
        course_context="Curso: Engenharia de Prompts...",
        student_history=[],
    )

Uso em testes / CI sem chave de API:

    tutor = Tutor(dry_run=True)
    resposta = tutor.respond(question="...", mode=TutorMode.QUIZ_ME,
                              course_context="...")
    # retorna resposta canned realista, não chama LLM
"""

from __future__ import annotations

import logging
from enum import Enum
from typing import TYPE_CHECKING, Optional

from src.agents.base import Agent, _safe_substitute

if TYPE_CHECKING:
    from src.llm_client import LLMClient

logger = logging.getLogger(__name__)


class TutorMode(str, Enum):
    """Três modos de interação suportados pelo tutor.

    Os valores são strings para facilitar serialização em JSON e querystring
    de endpoint web.
    """

    EXPLAIN_LIKE_5 = "explain_like_5"
    PRACTICAL_EXAMPLE = "practical_example"
    QUIZ_ME = "quiz_me"


# Respostas canned realistas usadas em dry_run / CI.
# Cobertura mínima: cada modo retorna texto coerente em PT-BR sem chamar LLM.
_DRY_RUN_RESPONSES: dict[TutorMode, str] = {
    TutorMode.EXPLAIN_LIKE_5: (
        "Imagine que você está organizando uma estante de livros. Quando você "
        "coloca cada livro no mesmo lugar todas as vezes, achar um livro depois "
        "fica fácil — você vai direto naquela prateleira sem pensar.\n\n"
        "**Prompt caching** funciona parecido: o sistema guarda partes do "
        "contexto que você usa toda hora (instruções, exemplos longos, "
        "documentação) num lugar de acesso rápido. Da próxima vez que você "
        "fizer uma pergunta nova reutilizando aquele contexto, o modelo não "
        "precisa reler tudo do zero — ele já sabe onde está.\n\n"
        "O ganho prático: respostas mais rápidas e custo menor em chamadas "
        "repetidas. É exatamente o que acontece quando você sabe de cor onde "
        "fica o livro favorito da estante."
    ),
    TutorMode.PRACTICAL_EXAMPLE: (
        "**Cenário:** você é gerente de produto numa fintech e precisa "
        "classificar 5 mil tickets de suporte por categoria todo dia.\n\n"
        "Aplicação passo a passo:\n\n"
        "1. Monte um system prompt com as 12 categorias e 3 exemplos de cada "
        "uma — total de cerca de 8 mil tokens.\n"
        "2. Marque esse bloco como `cache_control: ephemeral` na chamada à API.\n"
        "3. Para cada ticket novo, envie só o texto do ticket no campo `user`.\n"
        "4. As primeiras chamadas pagam o custo de escrita do cache. A partir "
        "da segunda, o system prompt é lido do cache por cerca de 10% do "
        "preço normal.\n"
        "5. Meça o cache hit rate na resposta da API (`cache_read_input_tokens`) "
        "para confirmar economia.\n\n"
        "**Resultado observável:** custo unitário por ticket cai entre 60% e "
        "80%, e a latência média da chamada cai pela metade.\n\n"
        "**Variação:** o mesmo padrão funciona para revisão de contratos, "
        "moderação de conteúdo e qualquer pipeline de classificação em "
        "volume com instruções fixas longas."
    ),
    TutorMode.QUIZ_ME: (
        "Você está consultando para uma startup que processa 50 mil chamadas "
        "ao Claude por dia, com prompt fixo de 12 mil tokens e variável de "
        "200 tokens. O CFO pede para cortar o custo de inferência pela "
        "metade sem sacrificar qualidade.\n\n"
        "Que combinação de prompt caching, escolha de modelo e design do "
        "pipeline você proporia, e qual seria o impacto esperado em cada uma "
        "das três alavancas?"
    ),
}


class Tutor(Agent):
    """Tutor IA runtime — agente conversacional pós-publicação do curso.

    Atributos:
        nome: identificador interno do agente.
        provider: provider LLM padrão (Anthropic — Haiku é o modelo recomendado
            por custo / latência para tutor).
        model: modelo padrão. Pode ser sobrescrito por client.yaml.
        prompt_file: arquivo de prompt em src/templates/prompts/.
        persona: tom da personalidade do tutor (configurável por cliente).
        dry_run: quando True, retorna respostas canned sem chamar LLM. Útil
            em testes e CI sem chave de API.
    """

    nome: str = "tutor"
    provider: str = "anthropic"
    model: str = "claude-haiku-4-5-20251001"
    prompt_file: str = "tutor.md"

    def __init__(
        self,
        client: Optional[LLMClient] = None,
        persona: str = "curiosa-paciente",
        dry_run: bool = False,
        model: Optional[str] = None,
    ) -> None:
        """Inicializa o tutor.

        Args:
            client: instância de LLMClient. Pode ser None quando dry_run=True.
            persona: tom da personalidade do tutor. Default "curiosa-paciente".
            dry_run: quando True, retorna respostas canned sem chamar LLM.
            model: sobrescreve o modelo padrão (ex.: vindo de client.yaml).
        """
        if not dry_run and client is None:
            raise ValueError(
                "Tutor exige LLMClient quando dry_run=False. "
                "Passe client=LLMClient() ou use dry_run=True para testes."
            )

        # Quando dry_run, não inicializa o pipeline da Agent base (que exige
        # client). Mantemos os atributos compatíveis com Agent.
        self.client = client  # type: ignore[assignment]
        self._prompt_template: Optional[str] = None
        self.persona = persona
        self.dry_run = dry_run
        if model:
            self.model = model

    def build_prompt(  # type: ignore[override]
        self,
        context: str = "",
        question: str = "",
        course_context: str = "",
        student_history: str = "",
        persona: Optional[str] = None,
        **template_vars: str,
    ) -> str:
        """Constrói o prompt final substituindo placeholders no tutor.md.

        Args:
            context: campo legado herdado de Agent.build_prompt — não usado
                pelo template tutor.md, mas preservado por compatibilidade.
            question: pergunta literal do aluno.
            course_context: resumo do curso + trechos relevantes de módulos.
            student_history: histórico recente da conversa em texto único.
            persona: sobrescreve self.persona apenas para esta chamada.
            **template_vars: variáveis adicionais aceitas pelo Agent base.

        Returns:
            Prompt pronto para enviar ao LLM.
        """
        template = self._load_prompt_template()
        if not template:
            # Fallback inline mínimo se o tutor.md não existir.
            template = (
                "Você é {persona}, tutor IA do curso.\n\n"
                "Curso: {course_context}\n\n"
                "Histórico: {student_history}\n\n"
                "Pergunta do aluno: {question}\n\n"
                "Responda em PT-BR, sem emojis, sem disclaimers de IA."
            )

        substitutions = {
            "context": context,
            "question": question,
            "course_context": course_context,
            "student_history": student_history,
            "persona": persona or self.persona,
        }
        substitutions.update(template_vars)
        return _safe_substitute(template, substitutions)

    def respond(
        self,
        question: str,
        mode: TutorMode,
        course_context: str,
        student_history: Optional[list[dict[str, str]]] = None,
    ) -> str:
        """Responde à pergunta do aluno no modo escolhido.

        Args:
            question: texto literal da pergunta do aluno.
            mode: TutorMode.EXPLAIN_LIKE_5, PRACTICAL_EXAMPLE ou QUIZ_ME.
            course_context: contexto do curso (resumo + módulos relevantes
                idealmente vindos de busca vetorial em edu_documents).
            student_history: histórico recente, lista de
                {"question": str, "answer": str}. Default lista vazia.

        Returns:
            Resposta do tutor em texto plano.
        """
        if not isinstance(mode, TutorMode):
            raise TypeError(
                f"mode deve ser TutorMode (recebeu {type(mode).__name__})."
            )

        history_str = self._format_history(student_history or [])

        # Modo dry_run: bypass completo do LLM. Útil em testes, CI e desenvolvimento.
        if self.dry_run:
            logger.info(
                "Tutor.respond [dry_run] persona=%s mode=%s",
                self.persona, mode.value,
            )
            return _DRY_RUN_RESPONSES[mode]

        # Modo real: monta prompt incluindo a instrução de modo e chama o LLM.
        mode_instruction = self._mode_instruction(mode)
        full_question = f"[MODO: {mode.value}] {mode_instruction}\n\n{question}"

        prompt = self.build_prompt(
            question=full_question,
            course_context=course_context,
            student_history=history_str,
            persona=self.persona,
        )

        logger.info(
            "Tutor.respond persona=%s mode=%s prompt_len=%d",
            self.persona, mode.value, len(prompt),
        )

        if self.client is None:
            raise RuntimeError(
                "Tutor sem LLMClient não pode responder fora de dry_run."
            )

        return self.client.call(self.provider, prompt, model=self.model)

    @staticmethod
    def _format_history(history: list[dict[str, str]]) -> str:
        """Serializa histórico em texto plano para injetar no prompt."""
        if not history:
            return "(sem histórico anterior nesta sessão)"

        linhas: list[str] = []
        for turn in history:
            q = turn.get("question", "").strip()
            a = turn.get("answer", "").strip()
            if q:
                linhas.append(f"Aluno: {q}")
            if a:
                linhas.append(f"Tutor: {a}")
        return "\n".join(linhas)

    @staticmethod
    def _mode_instruction(mode: TutorMode) -> str:
        """Mensagem curta enviada ao LLM para reforçar o modo escolhido."""
        if mode == TutorMode.EXPLAIN_LIKE_5:
            return (
                "Use o modo EXPLAIN_LIKE_5: linguagem simples, analogia "
                "cotidiana, sem infantilizar."
            )
        if mode == TutorMode.PRACTICAL_EXAMPLE:
            return (
                "Use o modo PRACTICAL_EXAMPLE: cenário concreto, passo a "
                "passo numerado, resultado observável."
            )
        if mode == TutorMode.QUIZ_ME:
            return (
                "Use o modo QUIZ_ME: faça uma pergunta aberta de Bloom 3+ "
                "e NÃO dê a resposta."
            )
        # Defensive: enum exhausted.
        return ""
