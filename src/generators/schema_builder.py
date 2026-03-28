"""Constrói CourseDefinition a partir dos outputs do pipeline multi-LLM.

Recebe o slug, a definição YAML, o conteúdo revisado (markdown) e
o resultado da classificação para montar o modelo final validado.
"""

from __future__ import annotations

import logging
import re
from typing import Any

from src.models import (
    CourseDefinition,
    CourseSection,
    FAQItem,
    NivelCurso,
    SectionType,
    StepDefinition,
)

logger = logging.getLogger(__name__)


class SchemaBuilder:
    """Monta um CourseDefinition completo a partir dos dados do pipeline."""

    def build(
        self,
        slug: str,
        yaml_def: dict[str, Any],
        reviewed_content: str,
        classify_result: dict[str, Any],
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
            hero_gradient_from=yaml_def.get("hero_gradient_from", "#032d60"),
            hero_gradient_to=yaml_def.get("hero_gradient_to", "#0176d3"),
        )

        logger.info(
            "CourseDefinition construído: slug=%s, steps=%d, faq=%d",
            course.slug,
            len(course.steps),
            len(course.faq),
        )
        return course

    def _parse_markdown_to_steps(self, markdown: str) -> list[StepDefinition]:
        """Converte markdown revisado em lista estruturada de StepDefinition.

        Detecta os seguintes padrões:
        - ## Título (header = novo step)
        - ```linguagem ... ``` (bloco de código)
        - > DICA: ... (tip)
        - > AVISO: ... (warning)
        - > CHECKPOINT: ... (checkpoint)
        - Texto regular (text)
        """
        if not markdown or not markdown.strip():
            return []

        steps: list[StepDefinition] = []
        current_title: str | None = None
        current_sections: list[CourseSection] = []
        step_counter = 0

        lines = markdown.split("\n")
        i = 0

        while i < len(lines):
            line = lines[i]

            # Detecta header ## = novo step
            header_match = re.match(r"^##\s+(.+)$", line)
            if header_match:
                # Salva step anterior se existir
                if current_title is not None and current_sections:
                    steps.append(
                        self._build_step(step_counter, current_title, current_sections)
                    )
                step_counter += 1
                current_title = header_match.group(1).strip()
                current_sections = []
                i += 1
                continue

            # Detecta bloco de código
            code_match = re.match(r"^```(\w*)$", line)
            if code_match:
                language = code_match.group(1) or "text"
                code_lines: list[str] = []
                i += 1
                while i < len(lines) and not lines[i].startswith("```"):
                    code_lines.append(lines[i])
                    i += 1
                i += 1  # Pula o ``` de fechamento
                code_content = "\n".join(code_lines)
                if code_content.strip():
                    current_sections.append(
                        CourseSection(
                            type=SectionType.CODE,
                            value=code_content,
                            language=language,
                        )
                    )
                continue

            # Detecta blockquotes especiais
            tip_match = re.match(r"^>\s*DICA:\s*(.+)$", line)
            if tip_match:
                current_sections.append(
                    CourseSection(
                        type=SectionType.TIP,
                        value=tip_match.group(1).strip(),
                        label="DICA",
                    )
                )
                i += 1
                continue

            warning_match = re.match(r"^>\s*AVISO:\s*(.+)$", line)
            if warning_match:
                current_sections.append(
                    CourseSection(
                        type=SectionType.WARNING,
                        value=warning_match.group(1).strip(),
                        label="AVISO",
                    )
                )
                i += 1
                continue

            checkpoint_match = re.match(r"^>\s*CHECKPOINT:\s*(.+)$", line)
            if checkpoint_match:
                current_sections.append(
                    CourseSection(
                        type=SectionType.CHECKPOINT,
                        value=checkpoint_match.group(1).strip(),
                        label="CHECKPOINT",
                    )
                )
                i += 1
                continue

            # Texto regular (ignora linhas vazias isoladas)
            if line.strip():
                # Acumula texto consecutivo em uma única seção
                text_lines: list[str] = [line]
                i += 1
                while i < len(lines):
                    next_line = lines[i]
                    if (
                        next_line.startswith("##")
                        or next_line.startswith("```")
                        or next_line.startswith("> DICA:")
                        or next_line.startswith("> AVISO:")
                        or next_line.startswith("> CHECKPOINT:")
                        or not next_line.strip()
                    ):
                        break
                    text_lines.append(next_line)
                    i += 1
                text_content = "\n".join(text_lines)
                if text_content.strip():
                    current_sections.append(
                        CourseSection(type=SectionType.TEXT, value=text_content)
                    )
                continue

            i += 1

        # Salva último step
        if current_title is not None and current_sections:
            steps.append(
                self._build_step(step_counter, current_title, current_sections)
            )

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
