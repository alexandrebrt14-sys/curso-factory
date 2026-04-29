"""Geradores de Schema.org/JSON-LD expandido para a página do curso.

Estes dicts são consumidos pelos templates Jinja2 da landing-page-geo
(via patch sugerido em `Agentic-Layer.md`) e injetados em
`<script type="application/ld+json">`. Todas as chaves seguem o
vocabulário Schema.org em inglês para compatibilidade com crawlers.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from src.models import CourseDefinition, StepDefinition

if TYPE_CHECKING:
    from src.clients.context import ClientContext


def _duration_to_iso8601(duration: str) -> str:
    """Converte 'NN min' em ISO 8601 'PTNNM'.

    Quando a string vier mal-formada, retorna 'PT0M' como degradação
    silenciosa (validador Pydantic já protege em `StepDefinition`).
    """
    try:
        minutes = int(str(duration).strip().replace(" min", "").strip())
    except (TypeError, ValueError):
        minutes = 0
    return f"PT{minutes}M"


def _provider_block(course: CourseDefinition) -> dict[str, Any]:
    """Bloco `provider` (Organization) reutilizado em vários JSON-LD."""
    return {
        "@type": "Organization",
        "name": course.company_name or course.autor_nome or "",
        "description": course.company_description or "",
        "url": (course.dominio or "").rstrip("/"),
    }


def _instructor_block(course: CourseDefinition) -> dict[str, Any]:
    """Bloco `instructor` (Person) baseado em autor_nome/credencial."""
    return {
        "@type": "Person",
        "name": course.autor_nome or "",
        "description": course.autor_credencial or "",
    }


def course_jsonld(course: CourseDefinition) -> dict[str, Any]:
    """Schema.org `Course` expandido.

    Inclui `provider`, `instructor`, `teaches` (skills declarados) e
    `educationalCredentialAwarded` quando o curso tiver tags/keywords
    apontando para uma certificação implícita.

    Args:
        course: Definição validada do curso.

    Returns:
        Dict JSON-LD.
    """
    teaches = course.keywords_seo or course.tags or []
    teaches = [t for t in teaches if isinstance(t, str) and t.strip()]

    payload: dict[str, Any] = {
        "@context": "https://schema.org",
        "@type": "Course",
        "name": course.titulo,
        "description": course.descricao,
        "url": course.canonical_url,
        "inLanguage": "pt-BR",
        "provider": _provider_block(course),
        "instructor": _instructor_block(course),
        "teaches": teaches,
        "educationalLevel": course.nivel_display or course.nivel.value,
        "timeRequired": _duration_to_iso8601(
            f"{course.duracao_total_minutos} min"
        ),
        "courseCode": course.slug,
        "educationalCredentialAwarded": (
            f"Certificado de conclusão — {course.titulo}"
        ),
        "hasCourseInstance": [
            {
                "@type": "CourseInstance",
                "courseMode": "online",
                "inLanguage": "pt-BR",
            }
        ],
    }

    if course.faq:
        # FAQ aninhado como hasPart simplificado — a página principal
        # geralmente emite um FAQPage separado.
        payload["hasPart"] = [
            {
                "@type": "Question",
                "name": item.pergunta,
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": item.resposta,
                },
            }
            for item in course.faq
        ]

    return payload


def learning_resource_jsonld(step: StepDefinition) -> dict[str, Any]:
    """Schema.org `LearningResource` para um step/módulo individual.

    Args:
        step: Definição validada do step.

    Returns:
        Dict JSON-LD.
    """
    return {
        "@context": "https://schema.org",
        "@type": "LearningResource",
        "name": step.title,
        "description": step.description,
        "identifier": step.id,
        "timeRequired": _duration_to_iso8601(step.duration),
        "learningResourceType": "module",
        "inLanguage": "pt-BR",
        "educationalUse": "instruction",
    }


def organization_jsonld(client_context: "ClientContext") -> dict[str, Any]:
    """Schema.org `Organization` para o cliente/tenant.

    Útil para emitir um bloco JSON-LD único na home da landing page de
    cada cliente.

    Args:
        client_context: ClientContext do tenant.

    Returns:
        Dict JSON-LD.
    """
    company_name = client_context.company.name or client_context.author.name or ""
    payload: dict[str, Any] = {
        "@context": "https://schema.org",
        "@type": "Organization",
        "name": company_name,
        "description": client_context.company.description or "",
        "url": (client_context.domain.canonical_url or "").rstrip("/"),
    }

    if client_context.author.name:
        payload["founder"] = {
            "@type": "Person",
            "name": client_context.author.name,
            "description": client_context.author.credential or "",
        }

    return payload
