"""Contrato A2A (Agent-to-Agent) para comércio agêntico.

A2A é o protocolo de troca de mensagens entre agentes — usado, por
exemplo, quando o agente do aluno conversa com o agente do produtor de
curso para descobrir oferta, preço e capacidades antes de comprar.

Este módulo expõe:

- Constantes com os endpoints HTTP canônicos que o servidor A2A futuro
  deverá expor.
- Função `a2a_course_info` que devolve um dict serializável como
  JSON-LD (Schema.org Course com extensões `agent_capabilities`).

Referência: arXiv:2505.02279 (MCP/A2A/ANP survey) e schema.org/Course.
"""

from __future__ import annotations

from typing import Any

from src.models import CourseDefinition

# ---------------------------------------------------------------------------
# Endpoints HTTP canônicos do servidor A2A futuro.
# ---------------------------------------------------------------------------

A2A_ENDPOINT_PURCHASE = "/api/agentic/purchase"
A2A_ENDPOINT_ENROLL = "/api/agentic/enroll"
A2A_ENDPOINT_COURSE_INFO = "/api/agentic/course-info"

A2A_ENDPOINTS: dict[str, str] = {
    "purchase": A2A_ENDPOINT_PURCHASE,
    "enroll": A2A_ENDPOINT_ENROLL,
    "course_info": A2A_ENDPOINT_COURSE_INFO,
}


def _build_offer(course: CourseDefinition, price_brl: float | None) -> dict[str, Any]:
    """Monta o bloco `offers` do JSON-LD.

    Quando `price_brl` é None, devolve oferta como "free of charge"
    (price 0). Caso contrário, oferta paga em BRL.
    """
    if price_brl is None:
        return {
            "@type": "Offer",
            "price": "0",
            "priceCurrency": "BRL",
            "availability": "https://schema.org/InStock",
            "url": f"{course.canonical_url}{A2A_ENDPOINT_ENROLL}",
            "category": "free",
        }
    # Formatação determinística com 2 casas para JSON-LD.
    formatted_price = f"{float(price_brl):.2f}"
    return {
        "@type": "Offer",
        "price": formatted_price,
        "priceCurrency": "BRL",
        "availability": "https://schema.org/InStock",
        "url": f"{course.canonical_url}{A2A_ENDPOINT_PURCHASE}",
        "category": "paid",
    }


def a2a_course_info(
    course: CourseDefinition,
    price_brl: float | None = None,
) -> dict[str, Any]:
    """Retorna dict JSON-LD descrevendo o curso para outros agentes.

    O documento retornado segue Schema.org (`@type: Course`) com extensões
    proprietárias `agent_capabilities` e `agent_endpoints` que listam o
    contrato A2A esperado.

    Strings JSON-LD ficam em inglês para compatibilidade máxima com
    crawlers (ver convenção do curso-factory para Schema.org).

    Args:
        course: Definição validada do curso.
        price_brl: Preço em BRL. None → oferta gratuita.

    Returns:
        Dict pronto para `json.dumps`.
    """
    provider_name = course.company_name or course.autor_nome or ""

    payload: dict[str, Any] = {
        "@context": "https://schema.org",
        "@type": "Course",
        "name": course.titulo,
        "description": course.descricao,
        "url": course.canonical_url,
        "inLanguage": "pt-BR",
        "provider": {
            "@type": "Organization",
            "name": provider_name,
            "url": (course.dominio or "").rstrip("/"),
        },
        "offers": _build_offer(course, price_brl),
        "agent_capabilities": [
            "list_modules",
            "get_module_content",
            "get_quiz",
            "submit_quiz_answer",
            "get_skills_taught",
            "purchase",
            "enroll",
        ],
        "agent_endpoints": {
            "purchase": f"{course.canonical_url}{A2A_ENDPOINT_PURCHASE}",
            "enroll": f"{course.canonical_url}{A2A_ENDPOINT_ENROLL}",
            "course_info": f"{course.canonical_url}{A2A_ENDPOINT_COURSE_INFO}",
        },
    }

    if course.autor_nome:
        payload["instructor"] = {
            "@type": "Person",
            "name": course.autor_nome,
            "description": course.autor_credencial or "",
        }

    return payload
