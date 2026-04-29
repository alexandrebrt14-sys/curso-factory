"""Exemplo de endpoint web do Tutor IA runtime — NÃO usar em produção.

Este arquivo demonstra como expor o `Tutor` (src/agents/tutor.py) atrás de
uma API HTTP simples usando FastAPI. É um STUB educacional para o time
front-end / DevOps planejar o deploy real.

Para produção, considere ainda:
- Autenticação por JWT do aluno (Supabase Auth).
- Rate limit por student_id (token bucket Redis).
- Persistência em Supabase em vez de TutorMemory em RAM.
- Telemetria de custo via CostTracker, com budget guard por aluno.
- CORS restrito ao domínio do cliente (alexandrecaramaschi.com etc).
- Streaming de resposta (Server-Sent Events) para UX percebida melhor.

Requirements de exemplo (NÃO instalar automaticamente):

    fastapi==0.115.0
    uvicorn[standard]==0.32.0
    pydantic==2.9.0

Como rodar localmente (depois de instalar manualmente):

    pip install fastapi 'uvicorn[standard]' pydantic
    uvicorn examples.tutor_api:app --reload --port 8001

E testar:

    curl -X POST http://localhost:8001/api/tutor/exemplo-curso \\
        -H "Content-Type: application/json" \\
        -d '{"question":"O que é prompt caching?","mode":"explain_like_5","student_id":"aluno-123"}'
"""

from __future__ import annotations

import logging
from typing import Optional

# Imports do FastAPI são lazy — o stub não deve quebrar `pytest tests/`
# em ambientes onde fastapi não está instalado.
try:
    from fastapi import FastAPI, HTTPException
    from pydantic import BaseModel
except ImportError as exc:  # pragma: no cover — apenas guarda o stub
    raise ImportError(
        "examples/tutor_api.py exige FastAPI e Pydantic. Instale com:\n"
        "    pip install fastapi 'uvicorn[standard]' pydantic\n"
        "Este é apenas um EXEMPLO — não use em produção."
    ) from exc

from src.agents.tutor import Tutor, TutorMode
from src.agents.tutor_memory import TutorMemory

logger = logging.getLogger(__name__)

app = FastAPI(
    title="Tutor IA — Curso Factory (exemplo)",
    description=(
        "Endpoint stub para demonstrar como expor o Tutor IA runtime. "
        "NÃO USE EM PRODUÇÃO sem implementar autenticação, rate limit, "
        "persistência e budget guard."
    ),
    version="0.1.0",
)


# Memória global em RAM, indexada por (student_id, course_slug). Em produção
# substituir por adapter Supabase.
_MEMORIES: dict[tuple[str, str], TutorMemory] = {}


def _get_memory(student_id: str, course_slug: str) -> TutorMemory:
    """Recupera ou cria memória para o par aluno/curso."""
    key = (student_id, course_slug)
    if key not in _MEMORIES:
        _MEMORIES[key] = TutorMemory(student_id=student_id, course_slug=course_slug)
    return _MEMORIES[key]


class TutorRequest(BaseModel):
    """Payload aceito pelo endpoint POST /api/tutor/<course_slug>."""

    question: str
    mode: str  # "explain_like_5" | "practical_example" | "quiz_me"
    student_id: str
    course_context: Optional[str] = None  # opcional; em prod, vem de busca vetorial


class TutorResponse(BaseModel):
    """Resposta retornada pelo endpoint."""

    answer: str
    mode: str
    history_length: int


@app.post("/api/tutor/{course_slug}", response_model=TutorResponse)
def tutor_endpoint(course_slug: str, payload: TutorRequest) -> TutorResponse:
    """Endpoint principal — recebe pergunta do aluno e devolve resposta do tutor.

    Em STUB usa Tutor(dry_run=True) para evitar custo. Em produção remover
    dry_run e injetar LLMClient real.
    """
    try:
        mode = TutorMode(payload.mode)
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail=(
                f"mode inválido: {payload.mode!r}. "
                f"Valores aceitos: {[m.value for m in TutorMode]}."
            ),
        )

    memory = _get_memory(payload.student_id, course_slug)

    # IMPORTANTE: dry_run=True. Em produção: tutor = Tutor(client=LLMClient()).
    tutor = Tutor(dry_run=True, persona="curiosa-paciente")

    course_ctx = payload.course_context or f"Curso: {course_slug} (contexto não informado)"
    history = memory.history(limit=10)

    answer = tutor.respond(
        question=payload.question,
        mode=mode,
        course_context=course_ctx,
        student_history=history,
    )
    memory.add(payload.question, answer)

    return TutorResponse(
        answer=answer,
        mode=mode.value,
        history_length=len(memory),
    )


@app.get("/health")
def health() -> dict[str, str]:
    """Healthcheck simples para load balancer."""
    return {"status": "ok", "stub": "true"}
