"""Contrato MCP (Model Context Protocol) para o servidor agêntico futuro.

Este módulo NÃO inicia servidor algum. Define apenas as estruturas de
dados e o manifest que o servidor MCP — quando existir — deverá expor.
Serve como referência canônica para:

1. Documentação (Wiki `Agentic-Layer`).
2. Geração de Schema.org/JSON-LD apontando para os endpoints corretos.
3. Testes de contrato (parse + chaves esperadas).

Referência: https://modelcontextprotocol.io/ e survey arXiv:2505.02279
("MCP/A2A/ANP: a protocol survey for agent legibility").
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from src.models import CourseDefinition


@dataclass
class MCPEndpoint:
    """Descrição declarativa de um endpoint MCP.

    Atributos:
        name: Nome do método (snake_case).
        description: Descrição curta em PT-BR para legibilidade humana.
        parameters: Schema dos parâmetros aceitos. Mapping nome→tipo+meta.
        returns: Schema do retorno. Mapping com `type` e `description`.
    """

    name: str
    description: str
    parameters: dict[str, Any] = field(default_factory=dict)
    returns: dict[str, Any] = field(default_factory=dict)

    def to_manifest_entry(self) -> dict[str, Any]:
        """Serializa para o formato esperado dentro do `endpoints` do manifest."""
        return {
            "name": self.name,
            "description": self.description,
            "parameters": self.parameters,
            "returns": self.returns,
        }


# ---------------------------------------------------------------------------
# Endpoints canônicos — espelham o contrato esperado pelo agente do aluno.
# ---------------------------------------------------------------------------

MCP_ENDPOINTS: list[MCPEndpoint] = [
    MCPEndpoint(
        name="list_modules",
        description="Lista todos os módulos do curso com título, ordem e duração.",
        parameters={},
        returns={
            "type": "array<ModuleInfo>",
            "description": (
                "Lista de objetos com campos id, title, order, duration_minutes."
            ),
        },
    ),
    MCPEndpoint(
        name="get_module_content",
        description="Retorna o conteúdo textual completo de um módulo.",
        parameters={
            "module_id": {
                "type": "string",
                "description": "ID kebab-case do módulo (ex.: 'step-01').",
                "required": True,
            },
        },
        returns={
            "type": "string",
            "description": "Markdown PT-BR do módulo solicitado.",
        },
    ),
    MCPEndpoint(
        name="get_quiz",
        description="Retorna o quiz vinculado a um módulo, se existir.",
        parameters={
            "module_id": {
                "type": "string",
                "description": "ID kebab-case do módulo.",
                "required": True,
            },
        },
        returns={
            "type": "Quiz | null",
            "description": (
                "Objeto Quiz com perguntas e opções; null se o módulo "
                "não tiver quiz."
            ),
        },
    ),
    MCPEndpoint(
        name="submit_quiz_answer",
        description="Submete a resposta de um quiz e devolve o resultado.",
        parameters={
            "quiz_id": {
                "type": "string",
                "description": "ID do quiz (formato 'quiz-<module_id>').",
                "required": True,
            },
            "answer": {
                "type": "integer",
                "description": "Índice da alternativa escolhida (0-based).",
                "required": True,
            },
        },
        returns={
            "type": "QuizResult",
            "description": (
                "Objeto com campos correct (bool), explanation (str) e "
                "next_module_id (str | null)."
            ),
        },
    ),
    MCPEndpoint(
        name="get_skills_taught",
        description="Lista as skills/competências emitidas pelo curso.",
        parameters={},
        returns={
            "type": "array<Skill>",
            "description": (
                "Lista de skills no formato {name, level, evidence_url}."
            ),
        },
    ),
]


def mcp_manifest(course: CourseDefinition) -> dict[str, Any]:
    """Monta o manifest MCP standard para um curso.

    O manifest é o documento que o servidor MCP futuro publicará no
    endpoint `/.well-known/mcp.json` (ou equivalente). Aqui é gerado
    estaticamente a partir do `CourseDefinition` para que possa ser
    incluído em artefatos de build.

    Args:
        course: Definição validada do curso.

    Returns:
        Dict serializável como JSON, com chaves canônicas:
            - `name`: identificador do servidor MCP do curso.
            - `version`: versão do contrato.
            - `description`: descrição curta.
            - `course`: bloco com slug/título/canonical_url.
            - `endpoints`: lista de endpoints (ver MCP_ENDPOINTS).
            - `protocol`: marcador de versão do MCP.
    """
    return {
        "name": f"curso-factory.mcp.{course.slug}",
        "version": "1.0.0",
        "protocol": "mcp/1.0",
        "description": (
            course.descricao_curta
            or course.descricao
            or f"Servidor MCP do curso {course.titulo}."
        ),
        "course": {
            "slug": course.slug,
            "title": course.titulo,
            "canonical_url": course.canonical_url,
            "duration_display": course.duracao_display,
        },
        "endpoints": [ep.to_manifest_entry() for ep in MCP_ENDPOINTS],
    }
