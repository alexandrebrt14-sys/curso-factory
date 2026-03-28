"""Pipeline de criação de cursos para uso via CLI.

Encapsula o Orchestrator e o CostTracker para execução simplificada
de cursos a partir de nome e configuração opcional.
"""

from __future__ import annotations

import logging
from typing import Any

from src.cost_tracker import CostTracker
from src.models import Course, NivelCurso
from src.orchestrator import Orchestrator, PipelineResult

logger = logging.getLogger(__name__)


class CourseFactory:
    """Fábrica de cursos que orquestra o pipeline completo via CLI.

    Uso típico:
        factory = CourseFactory()
        result = factory.run("Meu Curso de GEO", {"nivel": "intermediario"})
    """

    def __init__(self) -> None:
        self.cost_tracker = CostTracker()
        self.orchestrator = Orchestrator(cost_tracker=self.cost_tracker)

    def run(
        self,
        nome: str,
        course_config: dict[str, Any] | None = None,
    ) -> PipelineResult:
        """Executa o pipeline completo para criar um curso.

        Args:
            nome: Nome do curso em PT-BR (ex: "GEO para Iniciantes").
            course_config: Configuração opcional com campos do Course:
                - nivel: "iniciante" | "intermediario" | "avancado"
                - descricao: descrição do curso
                - tags: lista de tags
                - pre_requisitos: lista de pré-requisitos
                - modulos: lista de módulos pré-definidos

        Returns:
            PipelineResult com status, etapas concluídas e erros.
        """
        config = course_config or {}

        slug = self._generate_slug(nome)

        nivel_str = config.get("nivel", "intermediario")
        nivel_map = {
            "iniciante": NivelCurso.INICIANTE,
            "intermediario": NivelCurso.INTERMEDIARIO,
            "intermediário": NivelCurso.INTERMEDIARIO,
            "avancado": NivelCurso.AVANCADO,
            "avançado": NivelCurso.AVANCADO,
        }
        nivel = nivel_map.get(nivel_str.lower(), NivelCurso.INTERMEDIARIO)

        course = Course(
            id=slug,
            titulo=nome,
            descricao=config.get("descricao", f"Curso completo sobre {nome}"),
            nivel=nivel,
            tags=config.get("tags", []),
            pre_requisitos=config.get("pre_requisitos", []),
        )

        logger.info(
            "Iniciando pipeline para curso: '%s' (slug: %s, nível: %s)",
            nome,
            slug,
            nivel.value,
        )
        logger.info("Orçamento da sessão: %s", self.cost_tracker.report())

        result = self.orchestrator.run(course)

        if result.sucesso:
            logger.info("Curso '%s' criado com sucesso", nome)
        else:
            logger.error(
                "Curso '%s' falhou com %d erros", nome, len(result.erros)
            )

        return result

    @staticmethod
    def _generate_slug(nome: str) -> str:
        """Gera slug kebab-case ASCII a partir do nome do curso.

        Remove acentos, converte para minúsculas e substitui espaços por hífens.
        """
        import unicodedata

        # Normaliza e remove acentos
        nfkd = unicodedata.normalize("NFKD", nome)
        ascii_only = nfkd.encode("ascii", "ignore").decode("ascii")

        # Converte para kebab-case
        slug = ascii_only.lower().strip()
        slug = slug.replace(" ", "-")

        # Remove caracteres não permitidos
        slug = "".join(c for c in slug if c.isalnum() or c == "-")

        # Remove hífens duplicados e nas bordas
        while "--" in slug:
            slug = slug.replace("--", "-")
        slug = slug.strip("-")

        return slug
