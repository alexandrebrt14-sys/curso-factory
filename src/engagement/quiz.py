"""Modelo de quiz para microlearning e checkpoints de módulo.

Estruturas Pydantic puras (sem rede). O `score()` agrega tentativas e
identifica conceitos fracos para alimentar o SRS.
"""

from __future__ import annotations

from datetime import datetime, timezone

from pydantic import BaseModel, Field, field_validator, model_validator


def _now_utc() -> datetime:
    """Wall-clock UTC; substitui datetime.utcnow() (deprecated em 3.12)."""
    return datetime.now(timezone.utc)


class QuizQuestion(BaseModel):
    """Uma pergunta de múltipla escolha.

    Atributos:
        id: identificador estável (slug do conceito; ASCII).
        prompt: enunciado em PT-BR com acentos.
        options: lista de alternativas (mínimo 2).
        correct_index: índice (0-based) da alternativa correta.
        explanation: justificativa exibida após a resposta.
    """

    id: str = Field(..., min_length=1, description="ID estável do conceito")
    prompt: str = Field(..., min_length=5, description="Enunciado PT-BR")
    options: list[str] = Field(..., min_length=2, description="Alternativas")
    correct_index: int = Field(..., ge=0, description="Índice da resposta correta")
    explanation: str = Field(default="", description="Justificativa pós-resposta")

    @model_validator(mode="after")
    def _correct_index_valido(self) -> "QuizQuestion":
        if self.correct_index >= len(self.options):
            raise ValueError(
                f"correct_index ({self.correct_index}) fora do range "
                f"de options (len={len(self.options)})"
            )
        return self

    @field_validator("options")
    @classmethod
    def _options_nao_vazias(cls, v: list[str]) -> list[str]:
        if any(not str(opt).strip() for opt in v):
            raise ValueError("Nenhuma alternativa pode ser vazia")
        return v


class QuizAttempt(BaseModel):
    """Tentativa registrada de um aluno em uma pergunta.

    Atributos:
        question_id: ID da `QuizQuestion`.
        selected_index: índice escolhido pelo aluno.
        correct: verdadeiro se acertou.
        timestamp: momento da resposta (UTC).
    """

    question_id: str = Field(..., min_length=1)
    selected_index: int = Field(..., ge=0)
    correct: bool = Field(...)
    timestamp: datetime = Field(default_factory=_now_utc)

    @field_validator("timestamp")
    @classmethod
    def _ensure_tz(cls, v: datetime) -> datetime:
        if v.tzinfo is None:
            return v.replace(tzinfo=timezone.utc)
        return v


def score(attempts: list[QuizAttempt]) -> dict:
    """Agrega tentativas e devolve métricas + conceitos fracos.

    Args:
        attempts: lista de `QuizAttempt`. Pode incluir múltiplas tentativas
            para a mesma pergunta — a contagem usa todas.

    Returns:
        Dicionário com:
            - `total` (int): número de tentativas.
            - `correct` (int): número de tentativas corretas.
            - `accuracy` (float): proporção de acertos em [0.0, 1.0].
              Devolve 0.0 se `attempts` for vazio.
            - `weak_concepts` (list[str]): IDs de perguntas com pelo menos
              uma tentativa errada, sem duplicatas, ordenados pelo primeiro
              erro registrado.
    """
    total = len(attempts)
    correct = sum(1 for a in attempts if a.correct)
    accuracy = (correct / total) if total > 0 else 0.0

    weak_seen: set[str] = set()
    weak_concepts: list[str] = []
    for a in attempts:
        if not a.correct and a.question_id not in weak_seen:
            weak_seen.add(a.question_id)
            weak_concepts.append(a.question_id)

    return {
        "total": total,
        "correct": correct,
        "accuracy": accuracy,
        "weak_concepts": weak_concepts,
    }
