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

logger = logging.getLogger(__name__)

# Regex para identificar headings (# Title, ## Module 1, etc)
H1_RE = re.compile(r"^#\s+(.+?)\s*$", re.MULTILINE)
H2_RE = re.compile(r"^##\s+(.+?)\s*$", re.MULTILINE)

# Regex para code fences ```lang\n...code...\n```
CODE_FENCE_RE = re.compile(r"```([a-zA-Z0-9_+-]*)\n(.*?)```", re.DOTALL)


# ---------------------------------------------------------------------------
# Helpers de slug e nomenclatura
# ---------------------------------------------------------------------------


def _slugify(value: str) -> str:
    """Converte titulo para slug ASCII kebab-case sem acentos.

    Reusa a regra do CourseDefinition que proibe acentos no slug.
    """
    import unicodedata

    nfkd = unicodedata.normalize("NFKD", value)
    ascii_str = "".join(c for c in nfkd if not unicodedata.combining(c))
    slug = re.sub(r"[^a-zA-Z0-9\s-]", "", ascii_str)
    slug = re.sub(r"[\s_]+", "-", slug.strip().lower())
    slug = re.sub(r"-+", "-", slug)
    return slug.strip("-")


def _short_id(value: str, max_len: int = 24) -> str:
    """Versao curta do slug para usar como id de step."""
    slug = _slugify(value)
    if len(slug) <= max_len:
        return slug
    return slug[:max_len].rstrip("-")


# ---------------------------------------------------------------------------
# Extracao de modulos do markdown
# ---------------------------------------------------------------------------


def _extract_module_blocks(markdown: str) -> list[tuple[str, str]]:
    """Splita markdown em blocos por heading nivel 1 ou 2.

    Returns:
        Lista de tuplas (titulo, conteudo). Conteudo nao inclui o heading.
    """
    if not markdown.strip():
        return []

    # Tenta H2 primeiro (mais comum em drafts), fallback H1
    primary_re = H2_RE if H2_RE.search(markdown) else H1_RE
    matches = list(primary_re.finditer(markdown))

    if not matches:
        # Sem headings — trata o draft inteiro como 1 unico modulo
        return [("Modulo Unico", markdown.strip())]

    blocks: list[tuple[str, str]] = []
    for i, match in enumerate(matches):
        title = match.group(1).strip()
        # Remove markdown bold/italic do titulo
        title = re.sub(r"\*\*(.+?)\*\*", r"\1", title)
        title = re.sub(r"\*(.+?)\*", r"\1", title)
        start = match.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(markdown)
        content = markdown[start:end].strip()
        if title and content:
            blocks.append((title, content))

    return blocks


def _parse_module_to_sections(content: str) -> list[CourseSection]:
    """Quebra o conteudo de um modulo em CourseSections.

    Heuristica:
    - Detecta code fences (```lang\\n...```) -> CODE sections
    - Linhas que comecam com '> ' -> TIP sections (block quotes)
    - Texto restante -> TEXT sections (1 por chunk de paragrafos)
    - Sempre adiciona um CHECKPOINT sintetico no final (obrigatorio pelo schema)
    """
    sections: list[CourseSection] = []

    # 1. Extrair code blocks primeiro (e remover do texto)
    code_blocks: list[CourseSection] = []
    def _code_replace(match: re.Match) -> str:
        lang = match.group(1) or "text"
        code = match.group(2).strip()
        if code:
            code_blocks.append(
                CourseSection(
                    type=SectionType.CODE,
                    value=code,
                    language=lang,
                )
            )
        return f"\n[CODE_BLOCK_{len(code_blocks) - 1}]\n"

    text_no_code = CODE_FENCE_RE.sub(_code_replace, content)

    # 2. Extrair blockquotes como TIPs
    tip_blocks: list[CourseSection] = []
    lines = text_no_code.splitlines()
    cleaned_lines: list[str] = []
    current_quote: list[str] = []

    for line in lines:
        if line.lstrip().startswith(">"):
            current_quote.append(line.lstrip()[1:].strip())
        else:
            if current_quote:
                quote_text = " ".join(current_quote).strip()
                if quote_text:
                    tip_blocks.append(
                        CourseSection(type=SectionType.TIP, value=quote_text)
                    )
                current_quote = []
            cleaned_lines.append(line)
    if current_quote:
        quote_text = " ".join(current_quote).strip()
        if quote_text:
            tip_blocks.append(
                CourseSection(type=SectionType.TIP, value=quote_text)
            )

    text_clean = "\n".join(cleaned_lines)

    # 3. Quebrar texto em chunks de paragrafos. Tamanho razoavel ~1500 chars.
    paragraphs = [p.strip() for p in re.split(r"\n\s*\n", text_clean) if p.strip()]
    chunk_size = 1500
    current_chunk: list[str] = []
    current_len = 0
    text_chunks: list[str] = []

    for p in paragraphs:
        if current_len + len(p) > chunk_size and current_chunk:
            text_chunks.append("\n\n".join(current_chunk))
            current_chunk = [p]
            current_len = len(p)
        else:
            current_chunk.append(p)
            current_len += len(p)
    if current_chunk:
        text_chunks.append("\n\n".join(current_chunk))

    # 4. Substituir placeholders [CODE_BLOCK_N] de volta pelo code section
    final_text_sections: list[CourseSection] = []
    for chunk in text_chunks:
        if not chunk.strip():
            continue
        # Verifica se o chunk inteiro eh apenas um placeholder
        placeholder_match = re.match(r"^\s*\[CODE_BLOCK_(\d+)\]\s*$", chunk)
        if placeholder_match:
            idx = int(placeholder_match.group(1))
            if 0 <= idx < len(code_blocks):
                sections.append(code_blocks[idx])
                code_blocks[idx] = None  # type: ignore  # marca consumido
            continue

        # Senao: text section, mas substitui placeholders inline
        for idx, code in enumerate(code_blocks):
            if code is not None:
                placeholder = f"[CODE_BLOCK_{idx}]"
                if placeholder in chunk:
                    # Salva texto ate o placeholder, depois codigo, depois resto
                    parts = chunk.split(placeholder, 1)
                    if parts[0].strip():
                        final_text_sections.append(
                            CourseSection(type=SectionType.TEXT, value=parts[0].strip())
                        )
                    sections.extend(final_text_sections)
                    final_text_sections = []
                    sections.append(code)
                    code_blocks[idx] = None  # type: ignore
                    chunk = parts[1] if len(parts) > 1 else ""

        if chunk.strip():
            final_text_sections.append(
                CourseSection(type=SectionType.TEXT, value=chunk.strip())
            )

    sections.extend(final_text_sections)

    # 5. Anexar code blocks que sobraram (nao consumidos pelos chunks de texto)
    for code in code_blocks:
        if code is not None:
            sections.append(code)

    # 6. Intercalar tips
    sections.extend(tip_blocks)

    # 7. Garantir minimo de 3 sections + 1 checkpoint (validacao Pydantic)
    has_checkpoint = any(s.type == SectionType.CHECKPOINT for s in sections)
    if not has_checkpoint:
        sections.append(
            CourseSection(
                type=SectionType.CHECKPOINT,
                value=(
                    "Verifique seu entendimento: revise os conceitos centrais "
                    "deste modulo antes de avancar para o proximo."
                ),
            )
        )

    # Se ainda nao temos 3 sections, adicionar TIPs padrao
    while len(sections) < 3:
        sections.append(
            CourseSection(
                type=SectionType.TIP,
                value="Reflita sobre como aplicar este conteudo ao seu contexto profissional.",
            )
        )

    return sections


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
