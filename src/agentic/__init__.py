"""Camada de Agent Legibility do curso-factory (Wave 10 — quickwin).

Este módulo expõe contratos para tornar os cursos "legíveis" por agentes
de IA: arquivos `llms.txt` por curso, schemas MCP/A2A esperados pelo
servidor agêntico futuro e geradores de Schema.org expandido.

V0 deste pacote: apenas estrutura/contrato. Nenhum servidor MCP roda
ainda; os dataclasses servem como referência canônica para a Wave 10
e como entrada para os templates Jinja2 da landing-page-geo.

Uso típico:
    from src.agentic import generate_llms_txt, write_llms_txt
    from src.agentic import mcp_manifest, a2a_course_info, course_jsonld
"""

from src.agentic.a2a_schema import (
    A2A_ENDPOINT_COURSE_INFO,
    A2A_ENDPOINT_ENROLL,
    A2A_ENDPOINT_PURCHASE,
    A2A_ENDPOINTS,
    a2a_course_info,
)
from src.agentic.llms_txt import generate_llms_txt, write_llms_txt
from src.agentic.mcp_schema import (
    MCP_ENDPOINTS,
    MCPEndpoint,
    mcp_manifest,
)
from src.agentic.schema_org import (
    course_jsonld,
    learning_resource_jsonld,
    organization_jsonld,
)

__all__ = [
    "A2A_ENDPOINT_COURSE_INFO",
    "A2A_ENDPOINT_ENROLL",
    "A2A_ENDPOINT_PURCHASE",
    "A2A_ENDPOINTS",
    "MCP_ENDPOINTS",
    "MCPEndpoint",
    "a2a_course_info",
    "course_jsonld",
    "generate_llms_txt",
    "learning_resource_jsonld",
    "mcp_manifest",
    "organization_jsonld",
    "write_llms_txt",
]
