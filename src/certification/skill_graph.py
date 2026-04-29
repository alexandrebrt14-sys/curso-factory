"""Skill Graph — vocabulário controlado de habilidades.

Wave 9 V0 — armazenamento in-memory. A persistência (Postgres,
ArangoDB, RDF) e o casamento com vagas LinkedIn/InfoJobs ficam para
Waves seguintes.

Cada ``Skill`` carrega URI ``schema.org/Skill`` para garantir
interoperabilidade com Schema.org markup nos cursos publicados.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel, Field

if TYPE_CHECKING:
    from src.models import CourseDefinition


# URIs aceitos como tipo Schema.org válido para skills.
_VALID_SCHEMA_URIS = {
    "https://schema.org/Skill",
    "https://schema.org/DefinedTerm",
    "https://schema.org/Intangible",
}


class Skill(BaseModel):
    """Habilidade canônica do Skill Graph.

    O ``id`` é um slug ASCII kebab-case (ex.: ``geo-ranking``).
    O ``label`` é a forma humana com acentuação PT-BR.
    """

    id: str = Field(
        ...,
        pattern=r"^[a-z0-9-]+$",
        description="Slug ASCII kebab-case da habilidade",
    )
    label: str = Field(
        ...,
        min_length=1,
        description="Nome humano da habilidade (PT-BR com acentos)",
    )
    schema_org_uri: str = Field(
        default="https://schema.org/Skill",
        description="URI Schema.org para markup estruturado",
    )
    description: str = Field(default="", description="Descrição curta da habilidade")


def validate_skills(skills: list[Skill]) -> list[str]:
    """Valida uma lista de skills e retorna problemas detectados.

    Args:
        skills: Lista de objetos ``Skill`` a validar.

    Returns:
        Lista de strings descrevendo problemas. Vazia se tudo OK.

    Verificações:
        - URI deve estar em ``_VALID_SCHEMA_URIS``.
        - Label não pode ser apenas whitespace.
        - IDs devem ser únicos no conjunto.
    """
    issues: list[str] = []
    seen_ids: set[str] = set()

    for skill in skills:
        if skill.schema_org_uri not in _VALID_SCHEMA_URIS:
            issues.append(
                f"Skill '{skill.id}': URI inválido '{skill.schema_org_uri}'. "
                f"Aceitos: {sorted(_VALID_SCHEMA_URIS)}"
            )

        if not skill.label.strip():
            issues.append(f"Skill '{skill.id}': label vazio ou apenas whitespace")

        if skill.id in seen_ids:
            issues.append(f"Skill '{skill.id}': ID duplicado no conjunto")
        seen_ids.add(skill.id)

    return issues


def find_courses_by_skill(
    skill_id: str,
    courses: list["CourseDefinition"],
) -> list["CourseDefinition"]:
    """Filtra cursos cujas tags incluem o ``skill_id`` (V0 in-memory).

    A V0 usa ``CourseDefinition.tags`` como proxy do mapeamento
    skill -> curso. Versões futuras (Wave 10+) terão tabela de
    associação ``skills_courses`` persistente.
    """
    if not skill_id or not skill_id.strip():
        return []

    skill_id_norm = skill_id.strip().lower()
    return [
        course for course in courses
        if any(tag.strip().lower() == skill_id_norm for tag in course.tags)
    ]
