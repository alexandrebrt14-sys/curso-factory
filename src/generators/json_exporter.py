"""Exporta um `CourseDefinition` no formato JSON do portal /educacao (14/10/2026).

Desde a reorganização do `landing-page-geo` (PR #1409), o conteúdo de um curso
mora em `src/content/cursos/<slug>.json` (array de `Step`), com o glossário por
aula num sidecar `<slug>.glossario.json`. O `page.tsx` do portal deixa de
carregar conteúdo; `steps.ts` vira montagem fina (`carregarCurso(slug)` e, se
houver, os guias práticos em TypeScript). Esta é a saída final do curso-factory
para o portal; o `page.tsx`/`layout.tsx` do `TsxGenerator` segue disponível só
para o esqueleto da página e para a revisão local.

O que sai daqui:

- `<slug>.json`: um `Step` por módulo, com as chaves na ordem do portal
  (`id`, `title`, `duration`, `icon`, `description`, `content`, `faq`), sem
  campo opcional vazio (o schema é estrito e `language: null` reprova);
- `<slug>.glossario.json`: `{ id da aula: [{term, def}] }`, vazio quando o
  curso não declara termos (`CourseDefinition` ainda não os carrega);
- `<slug>.midia.json`: manifesto das figuras e imagens do curso (origem, texto
  alternativo, dimensões quando vêm no HTML), insumo do contrato de mídia
  (`docs/PUBLICACAO_CONTEUDO_MIDIA.md`); a fábrica não envia mídia ao R2;
- `<slug>.steps.ts`: montagem fina de referência para `src/app/educacao/<slug>/`.

Depois de gravar, `scripts/validar_curso_json.py` roda sobre o resultado.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from src.fsutil import write_json_atomic
from src.models import CourseDefinition, CourseSection, StepDefinition

#: Chaves de ícone da fábrica que têm outro nome em courseIcons.tsx do portal.
ICONES_DO_PORTAL = {"trendingUp": "trendUp"}

_IMG_RE = re.compile(r"<img\b[^>]*>", re.IGNORECASE)
_ATTR_RE = re.compile(r'(\w+)\s*=\s*"([^"]*)"')


def secao_para_portal(secao: CourseSection) -> dict[str, Any]:
    """`CourseSection` -> seção do portal: só os campos preenchidos."""
    saida: dict[str, Any] = {"type": secao.type.value, "value": secao.value or ""}
    if secao.language:
        saida["language"] = secao.language
    if secao.label:
        saida["label"] = secao.label
    if secao.data is not None:
        saida["data"] = secao.data
    return saida


def step_para_portal(
    step: StepDefinition, faq: list[dict[str, str]] | None = None
) -> dict[str, Any]:
    """`StepDefinition` -> `Step` do portal (`icon_key` vira `icon`)."""
    saida: dict[str, Any] = {
        "id": step.id,
        "title": step.title,
        "duration": step.duration,
        "icon": ICONES_DO_PORTAL.get(step.icon_key, step.icon_key),
        "description": step.description,
        "content": [secao_para_portal(s) for s in step.content],
    }
    if faq:
        saida["faq"] = faq
    return saida


def curso_para_portal(course: CourseDefinition) -> list[dict[str, Any]]:
    """Lista ordenada de `Step` do portal. A ordem do array é a ordem de leitura.

    A FAQ do curso (`CourseDefinition.faq`) vai no último capítulo, que é onde
    o portal a lê quando o curso não tem FAQ por aula; as fontes do rodapé
    (R7) viram um bloco `fontes` no último capítulo, como os guias práticos
    fazem no portal (`guias/aplicar.ts`).
    """
    steps = [step_para_portal(s) for s in course.steps]
    if not steps:
        return steps
    if course.fontes:
        steps[-1]["content"].append(
            {
                "type": "fontes",
                "value": "",
                "data": {"items": [{"source": f} for f in course.fontes]},
            }
        )
    if course.faq:
        steps[-1]["faq"] = [{"q": f.pergunta, "a": f.resposta} for f in course.faq]
    return steps


def manifesto_de_midia(course: CourseDefinition) -> list[dict[str, Any]]:
    """Figuras e imagens do curso, para o inventário de mídia do portal."""
    itens: list[dict[str, Any]] = []
    for step in course.steps:
        for i, secao in enumerate(step.content):
            if secao.type.value not in {"figure", "diagram", "mockup"}:
                continue
            item: dict[str, Any] = {
                "capitulo": step.id,
                "bloco": i,
                "tipo": secao.type.value,
                "legenda": secao.label or (secao.data or {}).get("caption") or "",
                "inline_svg": secao.value.lstrip().lower().startswith("<svg"),
            }
            if secao.data and isinstance(secao.data, dict):
                for chave in ("src", "alt", "width", "height"):
                    if chave in secao.data:
                        item[chave] = secao.data[chave]
            m = _IMG_RE.search(secao.value or "")
            if m:
                attrs = dict(_ATTR_RE.findall(m.group(0)))
                for chave in ("src", "alt", "width", "height"):
                    if chave in attrs:
                        item[chave] = attrs[chave]
            itens.append(item)
    return itens


def steps_ts_de_referencia(slug: str) -> str:
    """`steps.ts` fino: o portal lê o JSON do disco; nada de conteúdo em TS."""
    return (
        "/**\n"
        f' * steps.ts do curso "{slug}": montagem fina gerada pelo curso-factory.\n'
        " * O conteúdo mora em src/content/cursos/<slug>.json (fonte única); para editar\n"
        " * um capítulo, edite o JSON. Guias práticos em TypeScript, quando existirem,\n"
        " * entram aqui por aplicarGuias(), como no piloto #1409.\n"
        " */\n"
        'import type { Step } from "@/types/course-page";\n'
        'import { carregarCurso } from "@/lib/educacao/conteudo/carregar";\n\n'
        f'export const SLUG_DO_CURSO = "{slug}";\n\n'
        "export const STEPS_SEM_GUIAS: Step[] = carregarCurso(SLUG_DO_CURSO);\n"
        "export const STEPS: Step[] = STEPS_SEM_GUIAS;\n"
    )


def exportar_curso_json(
    course: CourseDefinition,
    target_dir: Path,
    *,
    glossario: dict[str, list[dict[str, str]]] | None = None,
) -> dict[str, Path]:
    """Grava `<slug>.json`, `<slug>.glossario.json`, `<slug>.midia.json` e
    `<slug>.steps.ts` em `target_dir`. Devolve os caminhos por nome."""
    target_dir = Path(target_dir)
    target_dir.mkdir(parents=True, exist_ok=True)
    slug = course.slug
    caminhos = {
        "curso": target_dir / f"{slug}.json",
        "glossario": target_dir / f"{slug}.glossario.json",
        "midia": target_dir / f"{slug}.midia.json",
        "steps": target_dir / f"{slug}.steps.ts",
    }
    steps = curso_para_portal(course)
    # Mesma gravação do portal: indentação de 2 espaços, UTF-8 sem escapar
    # acento, quebra de linha final (o git diff lê uma linha por campo).
    caminhos["curso"].write_text(
        json.dumps(steps, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    ids = {s["id"] for s in steps}
    termos = {aula: lista for aula, lista in (glossario or {}).items() if aula in ids}
    write_json_atomic(caminhos["glossario"], termos)
    write_json_atomic(caminhos["midia"], manifesto_de_midia(course))
    caminhos["steps"].write_text(steps_ts_de_referencia(slug), encoding="utf-8")
    return caminhos
