"""Gerador de arquivos TSX (page.tsx e layout.tsx) via templates Jinja2.

Usa templates em src/templates/ para gerar arquivos determinísticos
a partir de um CourseDefinition validado pelo Pydantic.
"""

from __future__ import annotations

import logging
from pathlib import Path

from jinja2 import Environment, FileSystemLoader

from src.models import CourseDefinition

logger = logging.getLogger(__name__)

TEMPLATES_DIR = Path(__file__).resolve().parent.parent / "templates"


def _js_escape(value: str) -> str:
    """Escapa caracteres problemáticos para uso em strings JavaScript/TSX.

    Trata: barra invertida, aspas duplas e quebras de linha.
    """
    if not isinstance(value, str):
        return str(value)
    return (
        value
        .replace("\\", "\\\\")
        .replace('"', '\\"')
        .replace("\n", "\\n")
    )


def _pascal_case(value: str) -> str:
    """Converte kebab-case para PascalCase.

    Exemplo: 'meu-curso-legal' -> 'MeuCursoLegal'
    """
    return "".join(part.capitalize() for part in value.split("-"))


class TsxGenerator:
    """Gera arquivos page.tsx e layout.tsx a partir de CourseDefinition."""

    def __init__(self) -> None:
        self.env = Environment(
            loader=FileSystemLoader(str(TEMPLATES_DIR)),
            keep_trailing_newline=True,
            trim_blocks=True,
            lstrip_blocks=True,
        )
        self.env.filters["js_escape"] = _js_escape
        self.env.filters["pascal_case"] = _pascal_case

    def render_page(self, course: CourseDefinition) -> str:
        """Renderiza page.tsx a partir do template page.tsx.j2.

        Flattena os steps e suas seções para o contexto do template.
        """
        template = self.env.get_template("page.tsx.j2")

        flat_steps = []
        for step in course.steps:
            flat_step = {
                "id": step.id,
                "title": step.title,
                "duration": step.duration,
                "icon_key": step.icon_key,
                "description": step.description,
                "content": [
                    {
                        "type": section.type.value,
                        "value": section.value,
                        "language": section.language or "",
                        "label": section.label or "",
                    }
                    for section in step.content
                ],
            }
            flat_steps.append(flat_step)

        context = {
            "slug": course.slug,
            "titulo": course.titulo,
            "titulo_seo": course.titulo_seo,
            "descricao": course.descricao,
            "descricao_curta": course.descricao_curta,
            "nivel_display": course.nivel_display,
            "duracao_display": course.duracao_display,
            "duracao_total_minutos": course.duracao_total_minutos,
            "tags": course.tags,
            "keywords_seo": course.keywords_seo,
            "steps": flat_steps,
            "prerequisitos_display": course.prerequisitos_display,
            "faq": [
                {"pergunta": f.pergunta, "resposta": f.resposta}
                for f in course.faq
            ],
            "hero_gradient_from": course.hero_gradient_from,
            "hero_gradient_to": course.hero_gradient_to,
            "autor_nome": course.autor_nome,
            "autor_credencial": course.autor_credencial,
            "dominio": course.dominio,
            "educacao_path": course.educacao_path,
            "canonical_url": course.canonical_url,
            "company_name": course.company_name,
            "company_description": course.company_description,
            "local_storage_key": course.local_storage_key,
            "component_name": course.component_name,
            "badge_color": course.badge_color,
            "breadcrumb_label": course.breadcrumb_label,
        }

        return template.render(context)

    def render_layout(self, course: CourseDefinition) -> str:
        """Renderiza layout.tsx a partir do template layout.tsx.j2."""
        template = self.env.get_template("layout.tsx.j2")

        context = {
            "slug": course.slug,
            "titulo_seo": course.titulo_seo,
            "descricao": course.descricao,
            "keywords_seo": course.keywords_seo,
            "dominio": course.dominio,
            "educacao_path": course.educacao_path,
            "canonical_url": course.canonical_url,
            "autor_nome": course.autor_nome,
            "autor_credencial": course.autor_credencial,
            "company_name": course.company_name,
        }

        return template.render(context)

    def write(
        self, course: CourseDefinition, target_dir: Path
    ) -> tuple[Path, Path]:
        """Gera e escreve page.tsx e layout.tsx no diretório alvo.

        Cria target_dir/slug/ se não existir.
        Retorna tupla (page_path, layout_path).
        """
        course_dir = target_dir / course.slug
        course_dir.mkdir(parents=True, exist_ok=True)

        page_content = self.render_page(course)
        page_path = course_dir / "page.tsx"
        page_path.write_text(page_content, encoding="utf-8")
        logger.info("page.tsx gerado: %s", page_path)

        layout_content = self.render_layout(course)
        layout_path = course_dir / "layout.tsx"
        layout_path.write_text(layout_content, encoding="utf-8")
        logger.info("layout.tsx gerado: %s", layout_path)

        return page_path, layout_path
