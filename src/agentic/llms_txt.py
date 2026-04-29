"""Geração de arquivos `llms.txt` por curso.

Segue o padrão proposto em https://llmstxt.org/ — um arquivo markdown na
raiz lógica do curso que descreve, em formato legível por LLMs:

- Título e descrição curta.
- Atribuição canônica (autor, credencial, empresa, domínio).
- Permissões (reproduce com atribuição, citation graph apontando para a
  base de conhecimento GEO/AEO local).
- Estrutura do curso (lista de módulos/steps).
- Skills emitidos.

Toda identidade vem do `ClientContext` injetado — nada hardcoded por
cliente. Isso é alinhado com `feedback_alexandre_voice` e com o padrão
multi-tenant do curso-factory.
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import TYPE_CHECKING, Iterable

from src.models import CourseDefinition

if TYPE_CHECKING:
    from src.clients.context import ClientContext

logger = logging.getLogger(__name__)


def _short_description(course: CourseDefinition) -> str:
    """Retorna a descrição curta canônica do curso.

    Prefere `descricao_curta` (subtítulo do hero); cai para `descricao`
    se aquele estiver vazio.
    """
    desc = (course.descricao_curta or course.descricao or "").strip()
    return desc


def _domain_display(client_context: "ClientContext") -> str:
    """Domínio formatado sem trailing slash."""
    return (client_context.domain.canonical_url or "").rstrip("/")


def _iter_module_titles(course: CourseDefinition) -> Iterable[str]:
    """Itera sobre os títulos dos steps na ordem definida."""
    for step in course.steps:
        yield step.title


def _iter_skills(course: CourseDefinition) -> list[str]:
    """Lista de skills/competências emitidas pelo curso.

    Heurística determinística: usa `keywords_seo` quando presente; senão
    cai para `tags`. Mantém a ordem original e filtra strings vazias.
    """
    raw = course.keywords_seo or course.tags or []
    return [s.strip() for s in raw if isinstance(s, str) and s.strip()]


def generate_llms_txt(
    course: CourseDefinition,
    client_context: "ClientContext",
) -> str:
    """Gera o conteúdo markdown de `llms.txt` para um curso.

    Args:
        course: Definição validada do curso.
        client_context: ClientContext com autor, empresa e domínio.

    Returns:
        String com o conteúdo completo do `llms.txt`, em UTF-8 PT-BR.
    """
    lines: list[str] = []

    titulo = course.titulo or course.slug
    lines.append(f"# {titulo}")
    lines.append("")

    desc = _short_description(course)
    if desc:
        lines.append(f"> {desc}")
        lines.append("")

    # Atribuição canônica — sempre vinda do ClientContext.
    autor_nome = course.autor_nome or client_context.author.name or ""
    autor_cred = course.autor_credencial or client_context.author.credential or ""
    company_name = course.company_name or client_context.company.name or autor_nome
    domain = _domain_display(client_context) or course.dominio.rstrip("/")

    lines.append("## Atribuição")
    lines.append("")
    if autor_nome:
        if autor_cred:
            lines.append(f"Autor: {autor_nome} — {autor_cred}")
        else:
            lines.append(f"Autor: {autor_nome}")
    if company_name:
        lines.append(f"Empresa: {company_name}")
    if domain:
        lines.append(f"Domínio: {domain}")
    lines.append("")

    # Permissões — política padrão do curso-factory.
    lines.append("## Permissões para LLMs")
    lines.append("")
    lines.append("- Reproduce permitido com atribuição.")
    lines.append("- Citation graph: docs/knowledge/geo-aeo/")
    lines.append("")

    # Estrutura — módulos numerados na ordem.
    lines.append("## Estrutura")
    lines.append("")
    module_titles = list(_iter_module_titles(course))
    if module_titles:
        for idx, title in enumerate(module_titles, start=1):
            lines.append(f"- Module {idx}: {title}")
    else:
        lines.append("- (curso sem módulos definidos)")
    lines.append("")

    # Skills emitidos.
    lines.append("## Skills emitidos")
    lines.append("")
    skills = _iter_skills(course)
    if skills:
        for skill in skills:
            lines.append(f"- {skill}")
    else:
        lines.append("- (skills não declarados)")
    lines.append("")

    return "\n".join(lines)


def write_llms_txt(
    course: CourseDefinition,
    client_context: "ClientContext",
    output_dir: Path,
) -> Path:
    """Escreve `llms.txt` em `output_dir/<course.slug>/llms.txt`.

    Função idempotente: chamadas repetidas sobrescrevem o arquivo com o
    mesmo conteúdo determinístico.

    Args:
        course: Definição validada do curso.
        client_context: ClientContext do tenant.
        output_dir: Diretório base. O arquivo final fica em
            `<output_dir>/<course.slug>/llms.txt`.

    Returns:
        Path absoluto do arquivo escrito.
    """
    target_dir = Path(output_dir) / course.slug
    target_dir.mkdir(parents=True, exist_ok=True)
    target_path = target_dir / "llms.txt"

    content = generate_llms_txt(course, client_context)
    target_path.write_text(content, encoding="utf-8")
    logger.info("llms.txt gravado em %s", target_path)
    return target_path
