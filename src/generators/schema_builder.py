"""Constrói CourseDefinition a partir dos outputs do pipeline multi-LLM.

Recebe o slug, a definição YAML, o conteúdo revisado (markdown) e
o resultado da classificação para montar o modelo final validado.
"""

from __future__ import annotations

import logging
import re
from typing import TYPE_CHECKING, Any

from src.models import (
    CourseDefinition,
    CourseSection,
    FAQItem,
    NivelCurso,
    SectionType,
    StepDefinition,
)
from src.parsers import extract_module_blocks, parse_module_to_sections

if TYPE_CHECKING:
    from src.clients.context import ClientContext

logger = logging.getLogger(__name__)


class SchemaBuilder:
    """Monta um CourseDefinition completo a partir dos dados do pipeline."""

    def build(
        self,
        slug: str,
        yaml_def: dict[str, Any],
        reviewed_content: str,
        classify_result: dict[str, Any],
        client: "ClientContext | None" = None,
    ) -> CourseDefinition:
        """Constrói e valida um CourseDefinition.

        Args:
            slug: Identificador kebab-case do curso (ASCII apenas).
            yaml_def: Definição do curso vinda do courses.yaml.
            reviewed_content: Markdown revisado pelo agente de review (Claude).
            classify_result: Resultado da classificação (Groq): nível, tags, etc.

        Returns:
            CourseDefinition validado pelo Pydantic.
        """
        steps = self._parse_markdown_to_steps(reviewed_content)

        nivel_str = classify_result.get("nivel", yaml_def.get("nivel", "intermediario"))
        nivel_map = {
            "iniciante": NivelCurso.INICIANTE,
            "intermediario": NivelCurso.INTERMEDIARIO,
            "intermediário": NivelCurso.INTERMEDIARIO,
            "avancado": NivelCurso.AVANCADO,
            "avançado": NivelCurso.AVANCADO,
        }
        nivel = nivel_map.get(nivel_str.lower(), NivelCurso.INTERMEDIARIO)

        tags = classify_result.get("tags", yaml_def.get("tags", []))
        keywords_seo = classify_result.get(
            "keywords_seo", yaml_def.get("keywords_seo", [])
        )
        prerequisitos = classify_result.get(
            "prerequisitos", yaml_def.get("prerequisitos", [])
        )

        faq_raw = classify_result.get("faq", yaml_def.get("faq", []))
        faq_items = []
        for item in faq_raw:
            if isinstance(item, dict) and "pergunta" in item and "resposta" in item:
                faq_items.append(
                    FAQItem(pergunta=item["pergunta"], resposta=item["resposta"])
                )

        duracao_total = sum(
            int(s.duration.replace(" min", "")) for s in steps
        ) if steps else 180

        if client is None:
            from src.clients import load_client
            client = load_client("default")

        # Branding vem do cliente por padrão; YAML pode sobrescrever por curso
        hero_from = yaml_def.get("hero_gradient_from", client.branding.hero_gradient_from)
        hero_to = yaml_def.get("hero_gradient_to", client.branding.hero_gradient_to)
        badge = yaml_def.get("badge_color", client.branding.badge_color)

        course = CourseDefinition(
            slug=slug,
            titulo=yaml_def.get("titulo", yaml_def.get("nome", slug)),
            descricao=yaml_def.get("descricao", ""),
            nivel=nivel,
            tags=tags,
            keywords_seo=keywords_seo,
            prerequisitos_display=prerequisitos,
            steps=steps,
            faq=faq_items,
            duracao_total_minutos=duracao_total,
            duracao_display=f"~{duracao_total} min",
            hero_gradient_from=hero_from,
            hero_gradient_to=hero_to,
            badge_color=badge,
            # Autoria injetada do ClientContext
            autor_nome=client.author.name,
            autor_credencial=client.author.credential,
            dominio=client.domain.canonical_url,
            educacao_path=client.domain.educacao_path,
            company_name=client.company.name or client.author.name,
            company_description=(
                client.company.description
                or f"Curso produzido por {client.author.name}."
            ),
        )

        logger.info(
            "CourseDefinition construído: slug=%s, steps=%d, faq=%d",
            course.slug,
            len(course.steps),
            len(course.faq),
        )
        return course

    def _parse_markdown_to_steps(self, markdown: str) -> list[StepDefinition]:
        """Converte markdown revisado em StepDefinitions via parser compartilhado.

        Delega a extração de módulos e parsing de seções para
        `src.parsers.markdown_parser`, garantindo paridade com o conversor
        de drafts órfãos.
        """
        if not markdown or not markdown.strip():
            return []

        blocks = extract_module_blocks(markdown)
        if not blocks:
            return []

        steps: list[StepDefinition] = []
        for idx, (title, content) in enumerate(blocks):
            sections = parse_module_to_sections(content)
            steps.append(self._build_step(idx, title, sections))

        logger.info("Markdown parseado: %d steps extraídos", len(steps))
        return steps

    @staticmethod
    def _build_step(
        index: int, title: str, sections: list[CourseSection]
    ) -> StepDefinition:
        """Monta um StepDefinition a partir do título e seções coletadas."""
        # Gera ID kebab-case a partir do índice
        step_id = f"step-{index:02d}"

        # Estima duração baseado no volume de conteúdo
        total_chars = sum(len(s.value) for s in sections)
        estimated_minutes = max(5, min(60, total_chars // 200))

        # Gera descrição a partir do primeiro parágrafo de texto
        description = title
        for section in sections:
            if section.type == SectionType.TEXT:
                first_line = section.value.split("\n")[0].strip()
                if len(first_line) >= 5:
                    description = first_line[:120]
                    break

        return StepDefinition(
            id=step_id,
            title=title,
            duration=f"{estimated_minutes} min",
            description=description,
            content=sections,
        )
