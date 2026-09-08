"""Constrói CourseDefinition a partir dos outputs do pipeline multi-LLM.

Recebe o slug, a definição YAML, o conteúdo revisado (markdown) e
o resultado da classificação para montar o modelo final validado.
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any

from src.models import (
    CourseDefinition,
    CourseSection,
    FAQItem,
    NivelCurso,
    SectionType,
    StepDefinition,
)
from src.parsers import (
    extract_module_blocks,
    extrair_fontes,
    extrair_subtitulo,
    parse_module_to_sections,
)

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
        client: ClientContext | None = None,
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
        steps, fontes = self._parse_markdown_to_steps(reviewed_content)

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
        # Schema exige >= 30 min; clamp para o piso legal sem inflar artificialmente.
        duracao_total = max(30, duracao_total)

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
            fontes=fontes,
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

    def _parse_markdown_to_steps(self, markdown: str) -> tuple[list[StepDefinition], list[str]]:
        """Converte markdown revisado em StepDefinitions via parser compartilhado.

        Delega a extração de módulos e parsing de seções para
        `src.parsers.markdown_parser`, garantindo paridade com o conversor
        de drafts órfãos. Devolve também as fontes hasteadas das trilhas
        (`## Fontes`), que o template desenha uma vez no rodapé (R7).
        """
        if not markdown or not markdown.strip():
            return [], []

        blocks = extract_module_blocks(markdown)
        if not blocks:
            return [], []

        steps: list[StepDefinition] = []
        fontes: list[str] = []
        for idx, (title, content) in enumerate(blocks):
            content, fontes_do_bloco = extrair_fontes(content)
            fontes.extend(f for f in fontes_do_bloco if f not in fontes)
            subtitulo, corpo = extrair_subtitulo(content)
            sections = parse_module_to_sections(corpo or content)
            if not sections:
                logger.warning("Bloco '%s' sem seção de conteúdo; pulado", title)
                continue
            steps.append(self._build_step(idx, title, sections, subtitulo))

        logger.info("Markdown parseado: %d steps extraídos, %d fonte(s)", len(steps), len(fontes))
        return steps, fontes

    @staticmethod
    def _build_step(
        index: int, title: str, sections: list[CourseSection], subtitulo: str = ""
    ) -> StepDefinition:
        """Monta um StepDefinition a partir do título, subtítulo e seções.

        O `description` é o subtítulo (R1): a frase única que o redator escreve
        logo abaixo do H1. Quando a unidade não traz subtítulo no formato, a
        primeira linha de prosa faz as vezes dele, como antes de 08/09/2026.
        """
        # Gera ID kebab-case a partir do índice
        step_id = f"step-{index:02d}"

        # Estima duração baseado no volume de conteúdo
        total_chars = sum(len(s.value) for s in sections)
        estimated_minutes = max(5, min(60, total_chars // 200))

        description = subtitulo.strip() if subtitulo and len(subtitulo.strip()) >= 5 else title
        if not subtitulo:
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
