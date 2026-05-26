#!/usr/bin/env python3
"""Sync output/approved/ -> wiki/courses/ no padrao Karpathy K-13.

Varre cursos aprovados e cria pagina wiki esqueleto para cada slug sem
pagina correspondente. Idempotente: re-rodar nao destrui trabalho
manual; apenas atualiza campo `updated` no frontmatter de paginas
existentes e cria novas paginas para cursos novos.

Detalhes da decisao em wiki/decisions/ADR-002-sync-automatico-courses-wiki.md.

Uso:
  python scripts/wiki/sync-courses.py           # cria paginas faltantes
  python scripts/wiki/sync-courses.py --dry-run # apenas reporta o que faria
  python scripts/wiki/sync-courses.py --force-update  # atualiza updated de todas
"""

from __future__ import annotations

import argparse
import re
import sys
from datetime import date, datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
WIKI_DIR = REPO_ROOT / "wiki"
COURSES_DIR = WIKI_DIR / "courses"
LOG_FILE = WIKI_DIR / "log.md"
OUTPUT_APPROVED = REPO_ROOT / "output" / "approved"
OUTPUT_CLIENTS = REPO_ROOT / "output" / "clients"

UPDATED_LINE_RE = re.compile(r"^updated:\s*\d{4}-\d{2}-\d{2}\s*$", re.MULTILINE)

PAGE_TEMPLATE = """---
name: {slug}
type: course
status: approved
created: {today}
updated: {today}
client: {client}
slug: {slug}
output_path: {output_path}
tags:
  - tag-a-preencher
nivel: intermediario
related:
  - {client}
  - padrao-editorial-hsm-hbr
  - andragogia-knowles
  - taxonomia-bloom
  - quality-gate-5-camadas
---

# Curso: {title}

Pagina gerada automaticamente por `scripts/wiki/sync-courses.py` em
{today}. Detalhes do curso em `{output_path}`.

## Metadata

- **Cliente**: {client} (veja [[clients/{client}]]).
- **Slug**: `{slug}`.
- **Path aprovado**: `{output_path}`.

## Pipeline aplicado

5 LLMs canonicos:

1. [[entities/perplexity-sonar]] (research)
2. [[entities/gpt-4o-writer]] (draft)
3. Gemini 2.5 Pro (analyze)
4. Groq Llama 3.3 (classify)
5. [[entities/claude-reviewer]] (review)

Detalhes em [[concepts/quality-gate-5-camadas]].

## Enriquecimento manual recomendado

Esta pagina e um esqueleto. Editar manualmente para adicionar:

- Tags reais (substituir `tag-a-preencher`).
- Cross-links para conceitos editoriais especificos aplicados.
- Cross-links para paginas em `wiki/sources/` citadas no curso.
- Notas pedagogicas, decisoes editoriais e variantes para outras
  verticais.
- Cross-link para `[[overview/topologia-cobertura-cursos]]` quando
  apropriado.

A funcao do sync e garantir que a pagina exista; a funcao humana e
enriquece-la quando o curso merece destaque ou cross-reference.
"""


def find_approved_courses() -> list[tuple[str, str, Path]]:
    """Retorna [(client_id, slug, path)] de cursos aprovados."""
    approved = []
    if OUTPUT_APPROVED.exists():
        for entry in OUTPUT_APPROVED.iterdir():
            if entry.is_dir():
                approved.append(("default", entry.name, entry))
    if OUTPUT_CLIENTS.exists():
        for client_dir in OUTPUT_CLIENTS.iterdir():
            if not client_dir.is_dir():
                continue
            client_approved = client_dir / "approved"
            if not client_approved.exists():
                continue
            for entry in client_approved.iterdir():
                if entry.is_dir():
                    approved.append((client_dir.name, entry.name, entry))
    return approved


def slug_to_title(slug: str) -> str:
    return slug.replace("-", " ").title()


def page_exists(slug: str) -> bool:
    return (COURSES_DIR / f"{slug}.md").exists()


def create_page(client_id: str, slug: str, output_path: Path) -> None:
    target = COURSES_DIR / f"{slug}.md"
    rel_output = output_path.relative_to(REPO_ROOT).as_posix()
    today = date.today().isoformat()
    target.write_text(
        PAGE_TEMPLATE.format(
            slug=slug,
            client=client_id,
            today=today,
            output_path=rel_output,
            title=slug_to_title(slug),
        ),
        encoding="utf-8",
    )


def update_page_updated(slug: str) -> None:
    target = COURSES_DIR / f"{slug}.md"
    text = target.read_text(encoding="utf-8")
    today = date.today().isoformat()
    new_text = UPDATED_LINE_RE.sub(f"updated: {today}", text, count=1)
    if new_text != text:
        target.write_text(new_text, encoding="utf-8")


def append_log(created: list[str], updated: list[str]) -> None:
    desc = f"Sync output approved->wiki courses. Criadas: {len(created)}. Atualizadas: {len(updated)}."
    pages = " ".join(f"wiki/courses/{s}.md" for s in (created + updated))
    line = (
        f"{date.today().isoformat()} | sync | scripts/wiki/sync-courses.py | "
        f"{desc} | {pages}\n"
    )
    with LOG_FILE.open("a", encoding="utf-8") as f:
        f.write(line)


def main() -> int:
    parser = argparse.ArgumentParser(description="Sync output/approved -> wiki/courses")
    parser.add_argument("--dry-run", action="store_true", help="apenas reporta")
    parser.add_argument("--force-update", action="store_true", help="atualiza updated de todas paginas existentes")
    args = parser.parse_args()

    if not COURSES_DIR.exists():
        COURSES_DIR.mkdir(parents=True, exist_ok=True)

    approved = find_approved_courses()
    created: list[str] = []
    updated: list[str] = []

    for client_id, slug, path in approved:
        if not page_exists(slug):
            if args.dry_run:
                print(f"CREATE: wiki/courses/{slug}.md (cliente={client_id})")
            else:
                create_page(client_id, slug, path)
                print(f"Criado: wiki/courses/{slug}.md")
            created.append(slug)
        elif args.force_update:
            if args.dry_run:
                print(f"UPDATE: wiki/courses/{slug}.md")
            else:
                update_page_updated(slug)
                print(f"Atualizado: wiki/courses/{slug}.md")
            updated.append(slug)

    print(f"\nResumo: {len(approved)} cursos aprovados, "
          f"{len(created)} paginas criadas, {len(updated)} atualizadas.")

    if not args.dry_run and (created or updated):
        append_log(created, updated)
        print(f"Log apendado em wiki/log.md.")

    return 0


if __name__ == "__main__":
    sys.exit(main())
