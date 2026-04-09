"""Orquestrador do pipeline de criação de cursos em 5 etapas.

Etapas:
1. Research (Perplexity) — busca dados atualizados sobre o tema
2. Draft (GPT-4o) — gera conteúdo dos módulos
3. Analyze (Gemini) — revisa qualidade e coerência
4. Classify (Groq) — classifica nível, tags, pré-requisitos
5. Review (Claude) — revisão final com foco em acentuação PT-BR
"""

from __future__ import annotations

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any

from src.config import OUTPUT_DIR
from src.cost_tracker import CostTracker
from src.llm_client import LLMClient
from src.models import Course
from src.agents.researcher import Researcher
from src.agents.writer import Writer
from src.agents.analyzer import Analyzer
from src.agents.classifier import Classifier
from src.agents.reviewer import Reviewer

logger = logging.getLogger(__name__)

DRAFTS_DIR = OUTPUT_DIR / "drafts"


class PipelineResult:
    """Resultado completo de uma execução do pipeline."""

    def __init__(self, course_id: str) -> None:
        self.course_id = course_id
        self.etapas: dict[str, str] = {}
        self.erros: list[str] = []
        self.sucesso: bool = False

    def to_dict(self) -> dict[str, Any]:
        return {
            "course_id": self.course_id,
            "timestamp": datetime.utcnow().isoformat(),
            "etapas": self.etapas,
            "erros": self.erros,
            "sucesso": self.sucesso,
        }


class Orchestrator:
    """Orquestra as 5 etapas do pipeline de criação de cursos."""

    def __init__(self, cost_tracker: CostTracker | None = None) -> None:
        self.cost_tracker = cost_tracker or CostTracker()
        self.client = LLMClient(self.cost_tracker)
        self.researcher = Researcher(self.client)
        self.writer = Writer(self.client)
        self.analyzer = Analyzer(self.client)
        self.classifier = Classifier(self.client)
        self.reviewer = Reviewer(self.client)

    def _checkpoint_path(self, course_id: str) -> Path:
        return DRAFTS_DIR / f"{course_id}_checkpoint.json"

    def _save_checkpoint(self, course_id: str, result: PipelineResult, context: str) -> None:
        """Salva checkpoint incremental após cada etapa concluída."""
        data = result.to_dict()
        data["_context"] = context
        path = self._checkpoint_path(course_id)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        logger.info("Checkpoint salvo: %s (%d etapas)", path.name, len(result.etapas))

    def _load_checkpoint(self, course_id: str) -> tuple[PipelineResult, str] | None:
        """Carrega checkpoint se existir, para resume após desconexão."""
        path = self._checkpoint_path(course_id)
        if not path.exists():
            return None
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        result = PipelineResult(course_id)
        result.etapas = data.get("etapas", {})
        result.erros = []  # Limpa erros anteriores para retry
        context = data.get("_context", "")
        logger.info("Checkpoint carregado: %d etapas concluídas anteriormente", len(result.etapas))
        return result, context

    def _build_template_vars(self, nome: str, course: Course, context: str) -> dict:
        """Return the named template variables required by each step's .md prompt.

        Each external prompt template uses specific named placeholders instead of
        the generic {context} variable.  This method maps step names to their
        expected variable sets so the orchestrator can forward them to execute().

        Args:
            nome: Pipeline step name ('research', 'analyze', 'classify', etc.).
            course: The Course object being processed.
            context: The accumulated pipeline context at this point in the run.

        Returns:
            Dict of keyword arguments to pass to agent.execute().
        """
        if nome == "research":
            # research.md: {course_name}, {course_description}, {target_modules}
            modulos_list = ""
            if course.modulos:
                lines = [f"  - {m.titulo}: {m.descricao}" for m in course.modulos]
                modulos_list = "\n".join(lines)
            else:
                modulos_list = "A definir conforme pesquisa"
            return {
                "course_name": course.titulo,
                "course_description": course.descricao or f"Curso completo sobre {course.titulo}",
                "target_modules": modulos_list,
            }

        if nome == "analyze":
            # analyze.md: {course_name}, {draft_content}
            return {
                "course_name": course.titulo,
                "draft_content": context,
            }

        if nome == "classify":
            # classify.md: {course_name}, {content}
            return {
                "course_name": course.titulo,
                "content": context,
            }

        # draft.md and review.md use {context} only — no extra vars needed.
        return {}

    def run(self, course: Course) -> PipelineResult:
        """Executa o pipeline completo para um curso, com resume de checkpoint."""
        DRAFTS_DIR.mkdir(parents=True, exist_ok=True)

        # Achado F32 — propaga course_id para todas as chamadas LLM, fazendo
        # com que o cost_tracker registre cada call sob o curso correto
        # (antes ficava com course_id="" tornando impossivel rastrear
        # custo por curso).
        self.client.set_course_context(course.id)

        # Tenta carregar checkpoint para resume
        checkpoint = self._load_checkpoint(course.id)
        if checkpoint:
            result, context = checkpoint
            logger.info("Retomando pipeline de checkpoint com etapas: %s", list(result.etapas.keys()))
        else:
            result = PipelineResult(course.id)
            context = ""

        etapas = [
            ("research", self.researcher, self._build_research_context(course)),
            ("draft", self.writer, None),  # Draft handled specially below
            ("analyze", self.analyzer, None),
            ("classify", self.classifier, None),
            ("review", self.reviewer, None),
        ]

        for nome, agente, ctx_inicial in etapas:
            # Pula etapas já concluídas (resume)
            if nome in result.etapas:
                context = result.etapas[nome]
                logger.info("Etapa '%s' já concluída (checkpoint), pulando", nome)
                continue

            # Verifica orçamento antes de cada etapa
            if self.cost_tracker.is_over_budget(agente.provider):
                msg = f"Orçamento excedido para {agente.provider}. Pipeline interrompido na etapa '{nome}'."
                logger.error(msg)
                result.erros.append(msg)
                break

            logger.info("Iniciando etapa: %s (provider: %s)", nome, agente.provider)

            # ── Draft: gerar módulo a módulo para obter conteúdo completo ──
            if nome == "draft" and course.modulos and len(course.modulos) > 1:
                try:
                    all_modules = self._draft_modules_iterative(course, context)
                    result.etapas[nome] = all_modules
                    context = all_modules
                    logger.info("Etapa 'draft' concluída: %d módulos gerados", len(course.modulos))
                    self._save_checkpoint(course.id, result, context)
                    continue
                except Exception as exc:
                    msg = f"Erro na etapa 'draft' (iterativo): {exc}"
                    logger.error(msg)
                    result.erros.append(msg)
                    self._save_checkpoint(course.id, result, context)
                    break

            # Se a etapa tem contexto inicial E há contexto do pipeline anterior, combina ambos
            if ctx_inicial and context:
                prompt_context = ctx_inicial + "\n\n--- CONTEXTO ANTERIOR DO PIPELINE ---\n" + context
            elif ctx_inicial:
                prompt_context = ctx_inicial
            else:
                prompt_context = context

            # Build named template vars so external .md templates receive their
            # expected placeholders (course_name, draft_content, content, etc.)
            # instead of leaving them unfilled in the sent prompt.
            template_vars = self._build_template_vars(nome, course, context)

            try:
                output = agente.execute(prompt_context, **template_vars)
                result.etapas[nome] = output
                context = output
                logger.info("Etapa '%s' concluída com sucesso", nome)
                # Salva checkpoint após cada etapa
                self._save_checkpoint(course.id, result, context)
            except Exception as exc:
                msg = f"Erro na etapa '{nome}': {exc}"
                logger.error(msg)
                result.erros.append(msg)
                # Salva checkpoint mesmo com erro para preservar etapas anteriores
                self._save_checkpoint(course.id, result, context)
                break
        else:
            result.sucesso = True

        # Salva resultado final
        self._save_result(course.id, result)
        # Remove checkpoint se pipeline concluiu com sucesso
        cp = self._checkpoint_path(course.id)
        if result.sucesso and cp.exists():
            cp.unlink()
            logger.info("Checkpoint removido (pipeline concluído com sucesso)")
        logger.info("Pipeline %s para curso '%s'",
                     "concluído com sucesso" if result.sucesso else "interrompido com erros",
                     course.id)
        logger.info(self.cost_tracker.report())
        return result

    def _draft_modules_iterative(self, course: Course, research_context: str) -> str:
        """Gera conteúdo módulo a módulo para garantir profundidade.

        Em vez de pedir todos os módulos numa única call (que gera apenas 1),
        chama o writer N vezes — uma para cada módulo — passando o contexto
        de pesquisa e os módulos anteriores como referência.
        """
        all_output: list[str] = []

        for i, modulo in enumerate(course.modulos, 1):
            logger.info("Draft módulo %d/%d: %s", i, len(course.modulos), modulo.titulo)

            # Contexto específico para este módulo
            prev_titles = [m.titulo for m in course.modulos[:i - 1]]
            next_titles = [m.titulo for m in course.modulos[i:]]

            prompt = (
                f"INSTRUÇÃO: Gere o conteúdo COMPLETO do Módulo {i} abaixo.\n"
                f"Este é o módulo {i} de {len(course.modulos)} do curso '{course.titulo}'.\n"
                f"Nível: {course.nivel.value}\n\n"
                f"MÓDULO A GERAR:\n"
                f"  Título: {modulo.titulo}\n"
                f"  Conteúdo esperado: {modulo.descricao or 'conforme pesquisa'}\n\n"
            )

            if prev_titles:
                prompt += "Módulos anteriores (já escritos): " + ", ".join(prev_titles) + "\n"
            if next_titles:
                prompt += "Próximos módulos (ainda não escritos): " + ", ".join(next_titles) + "\n"

            prompt += (
                "\nGere 2.500-4.000 palavras seguindo a estrutura obrigatória:\n"
                "1. Abertura com Impacto (250-350 palavras)\n"
                "2. Fundamentação Conceitual (800-1.200 palavras)\n"
                "3. Análise de Caso (400-600 palavras)\n"
                "4. Quadro Comparativo (tabela obrigatória)\n"
                "5. Exercícios Práticos (mínimo 3)\n"
                "6. Síntese Executiva (200-250 palavras)\n\n"
                "IMPORTANTE: Português do Brasil com acentuação COMPLETA.\n"
            )

            if research_context:
                prompt += "\n--- DADOS DA PESQUISA ---\n" + research_context[:3000]

            if self.cost_tracker.is_over_budget(self.writer.provider):
                logger.warning("Orçamento excedido no módulo %d. Parando draft.", i)
                break

            output = self.writer.execute(prompt)
            all_output.append(f"# Módulo {i}: {modulo.titulo}\n\n{output}")
            logger.info("Módulo %d gerado: %d palavras", i, len(output.split()))

        return "\n\n---\n\n".join(all_output)

    def _build_research_context(self, course: Course) -> str:
        """Monta o contexto inicial para a etapa de pesquisa."""
        modulos_txt = ""
        if course.modulos:
            modulos_txt = "\nMódulos planejados:\n"
            for m in course.modulos:
                modulos_txt += f"  - {m.titulo}: {m.descricao}\n"
        return (
            f"Curso: {course.titulo}\n"
            f"Descrição: {course.descricao}\n"
            f"Nível: {course.nivel.value}\n"
            f"Tags: {', '.join(course.tags)}\n"
            f"{modulos_txt}"
        )

    def _build_writer_context(self, course: Course) -> str:
        """Monta contexto para o redator com estrutura obrigatória dos módulos."""
        modulos_txt = ""
        if course.modulos:
            modulos_txt = "\n\nESTRUTURA OBRIGATÓRIA DOS MÓDULOS (gere TODOS, sem pular nenhum):\n"
            for i, m in enumerate(course.modulos, 1):
                modulos_txt += f"\nMódulo {i}: {m.titulo}\n"
                if m.descricao:
                    modulos_txt += f"  Conteúdo esperado: {m.descricao}\n"
        return (
            f"INSTRUÇÕES: Gere o conteúdo COMPLETO de TODOS os {len(course.modulos)} módulos listados abaixo.\n"
            f"Cada módulo deve ter: objetivos, conteúdo principal detalhado, exemplos práticos, resumo e exercícios.\n"
            f"NÃO resuma nem pule módulos. Gere o conteúdo integral de cada um.\n"
            f"IMPORTANTE: Todo o texto DEVE usar Português do Brasil com acentuação completa e ortografia correta.\n"
            f"\nCurso: {course.titulo}\n"
            f"Descrição: {course.descricao}\n"
            f"Nível: {course.nivel.value}\n"
            f"{modulos_txt}"
        )

    def _save_result(self, course_id: str, result: PipelineResult) -> None:
        """Salva o resultado do pipeline em JSON."""
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        filename = f"{course_id}_{timestamp}.json"
        path = DRAFTS_DIR / filename
        with open(path, "w", encoding="utf-8") as f:
            json.dump(result.to_dict(), f, indent=2, ensure_ascii=False)
        logger.info("Resultado salvo em: %s", path)
