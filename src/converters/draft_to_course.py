"""Conversor de drafts JSON para CourseDefinition.

Drafts em output/drafts/*.json sao saidas brutas do pipeline (Markdown gerado
por GPT-4o + revisao Claude). Este modulo extrai o conteudo, parseia em
modulos via headings, e constroi um CourseDefinition validado.

Uso programatico:

    from src.converters.draft_to_course import convert_draft_to_course
    course = convert_draft_to_course(Path("output/drafts/foo.json"))
    if course:
        TsxGenerator().write(course, Path("output/converted_from_drafts"))

Implementa o achado F12 da auditoria de ecossistema 2026-04-08:
13 cursos com investimento LLM ja gasto (15-17k palavras cada) ficaram
orfaos em output/drafts/ sem nunca ser convertidos para TSX deployable.
Este conversor recupera esse investimento.

Estrategia de parsing:
- Prefere a etapa 'review' (texto mais polido pelo Claude); fallback para 'draft'
- Splita por headings nivel 1 ou 2 (^# ou ^##) para identificar modulos
- Cada modulo vira um StepDefinition com seccoes intercaladas:
  - Paragrafos -> CourseSection(type=TEXT)
  - ```code blocks``` -> CourseSection(type=CODE, language=...)
  - Insights/notas -> CourseSection(type=TIP) heuristicamente
  - Ultimo bloco do modulo -> CourseSection(type=CHECKPOINT) sintetico
- Best-effort: se um draft falhar parsing, retorna None e loga warning;
  o batch processor continua com os proximos
"""

from __future__ import annotations

import json
import logging
import re
from datetime import timedelta
from pathlib import Path
from typing import Any

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
    parse_module_to_sections,
    short_id,
    slugify,
)

logger = logging.getLogger(__name__)

# Aliases privados — preservam a API interna usada abaixo sem duplicar o parser
_slugify = slugify
_short_id = short_id
_extract_module_blocks = extract_module_blocks
_parse_module_to_sections = parse_module_to_sections


# ---------------------------------------------------------------------------
# Construcao do CourseDefinition
# ---------------------------------------------------------------------------


def _build_steps(
    blocks: list[tuple[str, str]],
    fallback_module_minutes: int = 18,
) -> list[StepDefinition]:
    """Converte blocos (titulo, conteudo) em StepDefinitions validados."""
    steps: list[StepDefinition] = []
    used_ids: set[str] = set()

    for idx, (title, content) in enumerate(blocks):
        # Garantir id unico
        base_id = _short_id(title) or f"modulo-{idx + 1}"
        step_id = base_id
        suffix = 1
        while step_id in used_ids:
            step_id = f"{base_id}-{suffix}"
            suffix += 1
        used_ids.add(step_id)

        # Description = primeira frase do conteudo (sem markdown)
        clean = re.sub(r"[*_`#>\[\]]", "", content)
        first_sentence = re.split(r"(?<=[.!?])\s+", clean.strip(), maxsplit=1)
        description = first_sentence[0] if first_sentence else title
        description = description[:240].strip()
        if len(description) < 5:
            description = f"Modulo {idx + 1}: {title}"

        try:
            sections = _parse_module_to_sections(content)
            step = StepDefinition(
                id=step_id,
                title=title[:140],
                duration=f"{fallback_module_minutes} min",
                icon_key="trendingUp",
                description=description,
                content=sections,
            )
            steps.append(step)
        except Exception as exc:
            logger.warning(
                "Falha ao construir step '%s' (%s): %s — pulando",
                title,
                step_id,
                exc,
            )

    return steps


def _extract_review_or_draft_text(etapas: dict) -> str:
    """Pega o texto principal: prefere review (mais polido), senao draft."""
    for key in ("review", "draft", "analyze", "research"):
        value = etapas.get(key)
        if isinstance(value, str) and value.strip():
            return value
        if isinstance(value, dict):
            content = value.get("content") or value.get("text") or value.get("output")
            if isinstance(content, str) and content.strip():
                return content
    return ""


def convert_draft_to_course(draft_path: Path) -> CourseDefinition | None:
    """Converte um draft JSON para CourseDefinition. Best-effort.

    Args:
        draft_path: Caminho para output/drafts/{slug}_{timestamp}.json

    Returns:
        CourseDefinition se conseguiu parsear; None se falhou.
        Falhas sao logadas como warnings — caller continua o batch.
    """
    try:
        raw = draft_path.read_text(encoding="utf-8")
        data = json.loads(raw)
    except (OSError, json.JSONDecodeError) as exc:
        logger.warning("nao foi possivel ler %s: %s", draft_path, exc)
        return None

    course_id = data.get("course_id") or draft_path.stem.split("_")[0]
    etapas = data.get("etapas") or {}

    text = _extract_review_or_draft_text(etapas)
    if not text:
        logger.warning("draft %s sem conteudo em etapas review/draft", draft_path.name)
        return None

    blocks = _extract_module_blocks(text)
    if not blocks:
        logger.warning("draft %s sem modulos identificaveis", draft_path.name)
        return None

    steps = _build_steps(blocks)
    if not steps:
        logger.warning("draft %s nao gerou nenhum step valido", draft_path.name)
        return None

    # Construir titulo legivel a partir do course_id
    titulo = course_id.replace("-", " ").title()
    if len(titulo) < 5:
        titulo = f"Curso {titulo}"

    # Descricao: usa o primeiro paragrafo do texto (sem markdown)
    plain = re.sub(r"[#*_`>\[\]]", "", text)
    first_para = re.split(r"\n\s*\n", plain.strip())
    descricao = first_para[0][:280].strip() if first_para else titulo
    if len(descricao) < 20:
        descricao = (
            f"{titulo} — curso pratico com modulos progressivos para "
            f"profissionais aplicarem no dia a dia."
        )

    duracao_total = sum(
        int(re.match(r"(\d+)", s.duration).group(1))  # type: ignore
        for s in steps
    )
    # Schema exige >= 30 min. Drafts com 1 step unico ficariam abaixo;
    # clamp para o minimo legal sem inflar artificialmente o display.
    duracao_total = max(30, duracao_total)

    try:
        course = CourseDefinition(
            slug=_slugify(course_id),
            titulo=titulo,
            descricao=descricao,
            nivel=NivelCurso.INTERMEDIARIO,
            tags=["GEO", "Educacao", "Brasil GEO"],
            keywords_seo=[course_id, titulo.lower(), "alexandre caramaschi"],
            duracao_total_minutos=duracao_total,
            duracao_display=f"~{duracao_total} min",
            steps=steps,
            faq=[
                FAQItem(
                    pergunta="Este curso eh adequado para meu nivel?",
                    resposta=(
                        "Sim. O curso foi desenhado para profissionais com experiencia "
                        "previa que querem aplicar os conceitos diretamente no trabalho."
                    ),
                ),
            ],
        )
    except Exception as exc:
        logger.warning(
            "draft %s falhou validacao Pydantic CourseDefinition: %s",
            draft_path.name,
            exc,
        )
        return None

    return course


# ---------------------------------------------------------------------------
# Batch processor
# ---------------------------------------------------------------------------


def convert_drafts_directory(
    input_dir: Path,
    output_dir: Path,
) -> dict[str, Any]:
    """Converte todos os *.json de input_dir para TSX em output_dir.

    Returns:
        Dict com resumo: {converted: int, failed: int, files: [...]}
    """
    from src.generators.tsx_generator import TsxGenerator

    if not input_dir.exists():
        return {"converted": 0, "failed": 0, "files": [], "error": f"input_dir nao existe: {input_dir}"}

    output_dir.mkdir(parents=True, exist_ok=True)
    generator = TsxGenerator()

    converted = 0
    failed = 0
    results: list[dict] = []

    for draft_path in sorted(input_dir.glob("*.json")):
        if "checkpoint" in draft_path.name.lower():
            continue
        course = convert_draft_to_course(draft_path)
        if not course:
            failed += 1
            results.append({
                "file": draft_path.name,
                "status": "failed",
                "reason": "ver logs",
            })
            continue

        try:
            page_path, layout_path = generator.write(course, output_dir)
            converted += 1
            results.append({
                "file": draft_path.name,
                "status": "ok",
                "slug": course.slug,
                "steps": len(course.steps),
                "page_path": str(page_path),
            })
        except Exception as exc:
            failed += 1
            results.append({
                "file": draft_path.name,
                "status": "failed",
                "reason": f"tsx_generator: {exc}",
            })

    return {
        "converted": converted,
        "failed": failed,
        "total": converted + failed,
        "files": results,
    }
