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

    def run(self, course: Course) -> PipelineResult:
        """Executa o pipeline completo para um curso."""
        result = PipelineResult(course.id)
        DRAFTS_DIR.mkdir(parents=True, exist_ok=True)

        etapas = [
            ("research", self.researcher, self._build_research_context(course)),
            ("draft", self.writer, None),
            ("analyze", self.analyzer, None),
            ("classify", self.classifier, None),
            ("review", self.reviewer, None),
        ]

        context = ""
        for nome, agente, ctx_inicial in etapas:
            # Verifica orçamento antes de cada etapa
            if self.cost_tracker.is_over_budget(agente.provider):
                msg = f"Orçamento excedido para {agente.provider}. Pipeline interrompido na etapa '{nome}'."
                logger.error(msg)
                result.erros.append(msg)
                break

            logger.info("Iniciando etapa: %s (provider: %s)", nome, agente.provider)
            prompt_context = ctx_inicial if ctx_inicial else context

            try:
                output = agente.execute(prompt_context)
                result.etapas[nome] = output
                context = output  # Passa output como contexto para a próxima etapa
                logger.info("Etapa '%s' concluída com sucesso", nome)
            except Exception as exc:
                msg = f"Erro na etapa '{nome}': {exc}"
                logger.error(msg)
                result.erros.append(msg)
                break
        else:
            result.sucesso = True

        # Salva resultado em output/drafts/
        self._save_result(course.id, result)
        logger.info("Pipeline %s para curso '%s'",
                     "concluído com sucesso" if result.sucesso else "interrompido com erros",
                     course.id)
        logger.info(self.cost_tracker.report())
        return result

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

    def _save_result(self, course_id: str, result: PipelineResult) -> None:
        """Salva o resultado do pipeline em JSON."""
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        filename = f"{course_id}_{timestamp}.json"
        path = DRAFTS_DIR / filename
        with open(path, "w", encoding="utf-8") as f:
            json.dump(result.to_dict(), f, indent=2, ensure_ascii=False)
        logger.info("Resultado salvo em: %s", path)
