"""Gerador de arquivos TSX (page.tsx e layout.tsx) via templates Jinja2.

Usa templates em src/templates/ para gerar arquivos determinísticos
a partir de um CourseDefinition validado pelo Pydantic.
"""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any

from jinja2 import Environment, FileSystemLoader, select_autoescape

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


def _js_json(value: Any) -> str:
    """Serializa a carga de um bloco visual como literal JavaScript no TSX.

    A acentuação fica literal (`ensure_ascii=False`) porque o arquivo gerado é
    UTF-8 e texto de leitura humana não deve virar sequência de escape. Aspas,
    barras invertidas e quebras de linha ficam por conta do `json.dumps`. O
    sinal de menor vira escape para que payload nenhum consiga abrir marcação
    dentro do arquivo gerado.
    """
    if value is None:
        return "undefined"
    return json.dumps(value, ensure_ascii=False).replace("<", "\\u003c")


def _peso_visual_obrigatorio() -> bool:
    """Lê do YAML se a régua de peso visual reprova a geração.

    Vem de `validation.visual_density.required_for_new_course`. Quando a
    camada não existe, está desligada ou o arquivo some, devolve False: a
    ausência de configuração não pode derrubar geração que já funcionava.
    """
    try:
        from src.validators.rules_loader import validation_section

        camada = validation_section("visual_density") or {}
    except Exception:  # noqa: BLE001 - configuração ausente nunca derruba build
        return False
    if not camada.get("enabled", True):
        return False
    return bool(camada.get("required_for_new_course", False))


class VisualDensityError(ValueError):
    """Um ou mais módulos reprovaram na régua de peso visual.

    Existe como classe própria para que quem chama consiga distinguir o curso
    que nasceu como coluna de texto de qualquer outro erro de renderização, e
    decidir entre consertar o conteúdo e renderizar em modo legado.
    """

    def __init__(self, achados: list[str]) -> None:
        self.achados = achados
        corpo = "\n".join(f"  - {a}" for a in achados)
        super().__init__(
            f"Peso visual reprovado em {len(achados)} ponto(s). "
            "Nenhum curso nasce como coluna de texto:\n"
            f"{corpo}\n"
            "Doutrina e catálogo de peças: docs/DOUTRINA_VISUAL_CURSOS.md"
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
            # Templates são código (.tsx.j2) — select_autoescape mantém escape
            # OFF para eles e ON caso um dia se renderize .html/.xml. Valores
            # dinâmicos em contexto JS já passam pelo filtro `js_escape`.
            autoescape=select_autoescape(["html", "xml"]),
            keep_trailing_newline=True,
            trim_blocks=True,
            lstrip_blocks=True,
        )
        self.env.filters["js_escape"] = _js_escape
        self.env.filters["js_json"] = _js_json
        self.env.filters["pascal_case"] = _pascal_case

    def render_page(self, course: CourseDefinition, *, cobrar_peso_visual: bool | None = None) -> str:
        """Renderiza page.tsx a partir do template page.tsx.j2.

        Flattena os steps e suas seções para o contexto do template.

        Antes de renderizar, cobra a régua de peso visual de cada módulo. É
        aqui que ela morde, e não numa etapa opcional depois: curso que nasce
        como coluna de texto não chega a virar arquivo. O padrão vem de
        `validation.visual_density.required_for_new_course` no
        `config/quality_rules.yaml`; passe `cobrar_peso_visual=False` para
        renderizar um curso legado sem reprovar, caso em que os achados saem
        apenas no log.

        Raises:
            VisualDensityError: quando a cobrança está ligada e algum módulo
                reprova. A mensagem nomeia o módulo, a regra, o número medido
                e a peça que resolve.
        """
        self._cobrar_peso_visual(course, cobrar_peso_visual)
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
                        # Carga dos blocos visuais. Sem ela o bloco renderiza
                        # nada e não avisa.
                        "data": section.data,
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

    def _cobrar_peso_visual(
        self, course: CourseDefinition, cobrar: bool | None
    ) -> None:
        """Roda a régua de peso visual em cada módulo antes de renderizar.

        Quando `cobrar` é None, a decisão vem do YAML. Achado de severidade
        `error` reprova; `warning` sai no log e deixa passar, que é como o
        curso legado atravessa sem virar refém.
        """
        from src.validators.visual_density import check_visual_density

        if cobrar is None:
            cobrar = _peso_visual_obrigatorio()

        reprovas: list[str] = []
        for step in course.steps:
            achados = check_visual_density(
                step.content, module_name=step.id, curso_novo=cobrar
            )
            for a in achados:
                if a.tipo == "error":
                    reprovas.append(a.mensagem)
                else:
                    logger.warning("peso visual (%s): %s", step.id, a.mensagem)

        if reprovas:
            raise VisualDensityError(reprovas)

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
