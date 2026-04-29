"""Memória de conversa do Tutor IA runtime.

V0: armazenamento em RAM por (student_id, course_slug). Cada par mantém
uma lista ordenada de turnos (pergunta + resposta + timestamp).

Estrutura preparada para virar adapter Supabase sem quebrar a API pública:
basta criar `SupabaseTutorMemory` herdando de `BaseTutorMemory` e
sobrescrevendo `add` / `history` / `clear` para fazer round-trip à tabela
`edu_tutor_memory` (a ser criada no schema da landing-page-geo).

Razão para começar em RAM: V0 do tutor é stateless do lado do servidor,
e queremos validar UX antes de comprometer schema no Supabase. Quando o
endpoint /api/tutor/<course_slug> for promovido a produção, esta classe
vira o adapter padrão e a versão Supabase entra atrás de feature flag.
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class TutorTurn:
    """Um turno de conversa: pergunta do aluno + resposta do tutor."""

    question: str
    answer: str
    timestamp: float = field(default_factory=time.time)

    def as_dict(self) -> dict[str, str]:
        """Serializa o turno para uso em prompts ou APIs."""
        return {
            "question": self.question,
            "answer": self.answer,
            "timestamp": str(self.timestamp),
        }


class TutorMemory:
    """Memória de conversa em RAM, escopada por (student_id, course_slug).

    Não é thread-safe nem persistente. Apropriada para V0 e testes. Para
    produção, substituir por adapter Supabase mantendo a mesma interface
    (add / history / clear).

    Atributos:
        student_id: identificador único do aluno (UUID, e-mail ou similar).
        course_slug: slug do curso (ex.: "ia-aplicada-marketing-2026").
        max_turns: limite duro de turnos guardados em memória. Quando
            atingido, o turno mais antigo é descartado (FIFO).
    """

    DEFAULT_MAX_TURNS = 50

    def __init__(
        self,
        student_id: str,
        course_slug: str,
        max_turns: Optional[int] = None,
    ) -> None:
        if not student_id:
            raise ValueError("student_id obrigatório.")
        if not course_slug:
            raise ValueError("course_slug obrigatório.")

        self.student_id = student_id
        self.course_slug = course_slug
        self.max_turns = max_turns or self.DEFAULT_MAX_TURNS
        self._turns: list[TutorTurn] = []

    def add(self, question: str, answer: str) -> TutorTurn:
        """Registra um turno (pergunta + resposta) ao final da memória.

        Returns:
            O TutorTurn recém-criado. Útil para logging.
        """
        turn = TutorTurn(question=question, answer=answer)
        self._turns.append(turn)
        # Aplica janela FIFO se exceder max_turns.
        if len(self._turns) > self.max_turns:
            overflow = len(self._turns) - self.max_turns
            self._turns = self._turns[overflow:]
        return turn

    def history(self, limit: int = 10) -> list[dict[str, str]]:
        """Retorna os últimos `limit` turnos como lista de dicts.

        Args:
            limit: número máximo de turnos a devolver. Default 10.

        Returns:
            Lista ordenada do mais antigo ao mais recente, no formato
            esperado por Tutor.respond(student_history=...).
        """
        if limit <= 0:
            return []
        recent = self._turns[-limit:]
        return [t.as_dict() for t in recent]

    def clear(self) -> None:
        """Limpa toda a memória da conversa para este (student, course)."""
        self._turns = []

    def __len__(self) -> int:
        """Total de turnos registrados (não limitado por `limit` de history)."""
        return len(self._turns)

    def __repr__(self) -> str:
        return (
            f"TutorMemory(student_id={self.student_id!r}, "
            f"course_slug={self.course_slug!r}, turns={len(self._turns)})"
        )
