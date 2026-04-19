"""Parser de Markdown → CourseSections / Módulos.

Fonte única de verdade para parsing editorial usado por:
- `src/generators/schema_builder.py` (pipeline happy-path, Markdown revisto)
- `src/converters/draft_to_course.py` (recovery de drafts órfãos)

Funções públicas:
- `slugify(valor)` → ASCII kebab-case (sem acentos)
- `short_id(valor, max_len=24)` → slug truncado para step_id
- `extract_module_blocks(md)` → lista de (título, conteúdo) por heading
- `parse_module_to_sections(md)` → lista de CourseSection validáveis
"""

from __future__ import annotations

import re
import unicodedata

from src.models import CourseSection, SectionType

# Regex compartilhados
H1_RE = re.compile(r"^#\s+(.+?)\s*$", re.MULTILINE)
H2_RE = re.compile(r"^##\s+(.+?)\s*$", re.MULTILINE)
CODE_FENCE_RE = re.compile(r"```([a-zA-Z0-9_+-]*)\n(.*?)```", re.DOTALL)

# Prefixos de blockquote especiais (DICA/AVISO/CHECKPOINT) para schema_builder
_SPECIAL_QUOTES = {
    "DICA": SectionType.TIP,
    "AVISO": SectionType.WARNING,
    "CHECKPOINT": SectionType.CHECKPOINT,
}


def slugify(valor: str) -> str:
    """Converte título PT-BR em slug ASCII kebab-case sem acentos."""
    nfkd = unicodedata.normalize("NFKD", valor)
    ascii_str = "".join(c for c in nfkd if not unicodedata.combining(c))
    slug = re.sub(r"[^a-zA-Z0-9\s-]", "", ascii_str)
    slug = re.sub(r"[\s_]+", "-", slug.strip().lower())
    slug = re.sub(r"-+", "-", slug)
    return slug.strip("-")


def short_id(valor: str, max_len: int = 24) -> str:
    """Versão curta do slug (para ids de step)."""
    slug = slugify(valor)
    if len(slug) <= max_len:
        return slug
    return slug[:max_len].rstrip("-")


def extract_module_blocks(markdown: str) -> list[tuple[str, str]]:
    """Splita markdown em blocos por heading nível 1 ou 2.

    Preferência: H2 (padrão dos drafts). Fallback: H1. Sem headings, retorna
    o markdown inteiro como 1 único módulo.
    """
    if not markdown.strip():
        return []

    primary_re = H2_RE if H2_RE.search(markdown) else H1_RE
    matches = list(primary_re.finditer(markdown))

    if not matches:
        return [("Modulo Unico", markdown.strip())]

    blocks: list[tuple[str, str]] = []
    for i, match in enumerate(matches):
        title = match.group(1).strip()
        title = re.sub(r"\*\*(.+?)\*\*", r"\1", title)
        title = re.sub(r"\*(.+?)\*", r"\1", title)
        start = match.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(markdown)
        content = markdown[start:end].strip()
        if title and content:
            blocks.append((title, content))

    return blocks


def _detect_special_quote(line: str) -> tuple[SectionType, str] | None:
    """Detecta `> DICA: ...`, `> AVISO: ...`, `> CHECKPOINT: ...`."""
    stripped = line.strip()
    if not stripped.startswith(">"):
        return None
    content = stripped[1:].strip()
    for prefix, stype in _SPECIAL_QUOTES.items():
        if content.startswith(f"{prefix}:"):
            return stype, content[len(prefix) + 1 :].strip()
    return None


def parse_module_to_sections(
    content: str,
    chunk_size: int = 1500,
    add_checkpoint_if_missing: bool = True,
    min_sections: int = 3,
) -> list[CourseSection]:
    """Converte conteúdo de um módulo em CourseSections.

    Estratégia:
    1. Extrai code fences e guarda placeholders
    2. Extrai blockquotes especiais (DICA/AVISO/CHECKPOINT) e genéricos (TIP)
    3. Quebra texto restante em chunks
    4. Reinsere code fences onde aparecem os placeholders
    5. Garante ≥1 CHECKPOINT e ≥min_sections sections (validação Pydantic)
    """
    sections: list[CourseSection] = []

    code_blocks: list[CourseSection | None] = []

    def _code_replace(match: re.Match) -> str:
        lang = match.group(1) or "text"
        code = match.group(2).strip()
        if not code:
            return ""
        code_blocks.append(
            CourseSection(type=SectionType.CODE, value=code, language=lang)
        )
        return f"\n[CODE_BLOCK_{len(code_blocks) - 1}]\n"

    text_no_code = CODE_FENCE_RE.sub(_code_replace, content)

    # Blockquotes
    quote_sections: list[CourseSection] = []
    lines = text_no_code.splitlines()
    cleaned_lines: list[str] = []
    current_quote_lines: list[str] = []

    def _flush_quote() -> None:
        if not current_quote_lines:
            return
        joined = " ".join(current_quote_lines).strip()
        if not joined:
            return
        # Verifica se é um quote especial (DICA:/AVISO:/CHECKPOINT:)
        matched_type: SectionType | None = None
        for prefix, stype in _SPECIAL_QUOTES.items():
            if joined.startswith(f"{prefix}:"):
                matched_type = stype
                joined = joined[len(prefix) + 1 :].strip()
                quote_sections.append(
                    CourseSection(type=stype, value=joined, label=prefix)
                )
                break
        if matched_type is None:
            quote_sections.append(CourseSection(type=SectionType.TIP, value=joined))

    for line in lines:
        if line.lstrip().startswith(">"):
            current_quote_lines.append(line.lstrip()[1:].strip())
        else:
            _flush_quote()
            current_quote_lines = []
            cleaned_lines.append(line)
    _flush_quote()

    text_clean = "\n".join(cleaned_lines)

    # Chunks de texto
    paragraphs = [p.strip() for p in re.split(r"\n\s*\n", text_clean) if p.strip()]
    text_chunks: list[str] = []
    current_chunk: list[str] = []
    current_len = 0
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

    # Reinsere code blocks
    final_text_sections: list[CourseSection] = []
    for chunk in text_chunks:
        if not chunk.strip():
            continue
        placeholder_match = re.match(r"^\s*\[CODE_BLOCK_(\d+)\]\s*$", chunk)
        if placeholder_match:
            idx = int(placeholder_match.group(1))
            if 0 <= idx < len(code_blocks) and code_blocks[idx] is not None:
                sections.append(code_blocks[idx])  # type: ignore[arg-type]
                code_blocks[idx] = None
            continue

        for idx, code in enumerate(code_blocks):
            if code is None:
                continue
            placeholder = f"[CODE_BLOCK_{idx}]"
            if placeholder in chunk:
                parts = chunk.split(placeholder, 1)
                if parts[0].strip():
                    final_text_sections.append(
                        CourseSection(type=SectionType.TEXT, value=parts[0].strip())
                    )
                sections.extend(final_text_sections)
                final_text_sections = []
                sections.append(code)
                code_blocks[idx] = None
                chunk = parts[1] if len(parts) > 1 else ""

        if chunk.strip():
            final_text_sections.append(
                CourseSection(type=SectionType.TEXT, value=chunk.strip())
            )

    sections.extend(final_text_sections)

    # Code blocks não consumidos
    for code in code_blocks:
        if code is not None:
            sections.append(code)

    # Quotes ao final
    sections.extend(quote_sections)

    # Garantias mínimas para validação Pydantic de StepDefinition
    has_checkpoint = any(s.type == SectionType.CHECKPOINT for s in sections)
    if add_checkpoint_if_missing and not has_checkpoint:
        sections.append(
            CourseSection(
                type=SectionType.CHECKPOINT,
                value=(
                    "Verifique seu entendimento: revise os conceitos centrais "
                    "deste módulo antes de avançar para o próximo."
                ),
                label="CHECKPOINT",
            )
        )

    while len(sections) < min_sections:
        sections.append(
            CourseSection(
                type=SectionType.TIP,
                value="Reflita sobre como aplicar este conteúdo ao seu contexto profissional.",
            )
        )

    return sections
