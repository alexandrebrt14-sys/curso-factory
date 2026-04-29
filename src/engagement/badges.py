"""Sistema de conquistas (badges) para reconhecer marcos do aluno.

Cada `BadgeDefinition` declara um critério como callable que recebe o
`student_state` (dicionário arbitrário com métricas como `modulos_concluidos`,
`cursos_concluidos`, `streak_atual`, `quizzes`, etc.) e devolve `True` se o
aluno conquistou a badge.

O `BadgeEvaluator` itera o catálogo e devolve as badges concedidas.

Catálogo padrão (`DEFAULT_BADGES`):
    - primeiro_modulo: concluiu 1+ módulo.
    - primeiro_curso_completo: concluiu 1+ curso.
    - streak_7: 7 dias consecutivos de atividade.
    - streak_30: 30 dias consecutivos de atividade.
    - perfeito_em_quiz: pelo menos um quiz com 100% de acerto.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable, Iterable


# Tipo do critério: recebe o estado e devolve True se a badge foi conquistada.
BadgeCriterion = Callable[[dict[str, Any]], bool]


@dataclass(frozen=True)
class BadgeDefinition:
    """Definição de uma conquista.

    Atributos:
        id: identificador estável (ASCII, snake_case).
        name: nome curto exibido ao aluno (PT-BR com acentos).
        description: descrição curta da conquista.
        icon: chave do ícone associado (ex: "trophy", "fire", "star").
        criteria: callable que avalia o estado do aluno.
    """

    id: str
    name: str
    description: str
    icon: str
    criteria: BadgeCriterion = field(repr=False)


# ─── Critérios reutilizáveis ────────────────────────────────────────────


def _modulos_concluidos_ge(threshold: int) -> BadgeCriterion:
    """Critério: número de módulos concluídos >= threshold."""

    def _check(state: dict[str, Any]) -> bool:
        return int(state.get("modulos_concluidos", 0)) >= threshold

    return _check


def _cursos_concluidos_ge(threshold: int) -> BadgeCriterion:
    """Critério: número de cursos concluídos >= threshold."""

    def _check(state: dict[str, Any]) -> bool:
        return int(state.get("cursos_concluidos", 0)) >= threshold

    return _check


def _streak_atual_ge(threshold: int) -> BadgeCriterion:
    """Critério: streak atual >= threshold."""

    def _check(state: dict[str, Any]) -> bool:
        return int(state.get("streak_atual", 0)) >= threshold

    return _check


def _algum_quiz_perfeito() -> BadgeCriterion:
    """Critério: pelo menos um quiz registrado com 100% de acerto."""

    def _check(state: dict[str, Any]) -> bool:
        quizzes = state.get("quizzes", []) or []
        for q in quizzes:
            if isinstance(q, dict) and float(q.get("accuracy", 0.0)) >= 1.0:
                return True
        return False

    return _check


# ─── Catálogo padrão ────────────────────────────────────────────────────


DEFAULT_BADGES: tuple[BadgeDefinition, ...] = (
    BadgeDefinition(
        id="primeiro_modulo",
        name="Primeiro módulo",
        description="Você concluiu o primeiro módulo de um curso. Bom começo!",
        icon="seedling",
        criteria=_modulos_concluidos_ge(1),
    ),
    BadgeDefinition(
        id="primeiro_curso_completo",
        name="Primeiro curso completo",
        description="Você terminou um curso inteiro. Marco importante.",
        icon="trophy",
        criteria=_cursos_concluidos_ge(1),
    ),
    BadgeDefinition(
        id="streak_7",
        name="Sequência de 7 dias",
        description="Sete dias consecutivos estudando. Hábito em formação.",
        icon="fire",
        criteria=_streak_atual_ge(7),
    ),
    BadgeDefinition(
        id="streak_30",
        name="Sequência de 30 dias",
        description="Trinta dias consecutivos. Disciplina de elite.",
        icon="flame",
        criteria=_streak_atual_ge(30),
    ),
    BadgeDefinition(
        id="perfeito_em_quiz",
        name="Quiz perfeito",
        description="Você acertou 100% de um quiz. Domínio comprovado.",
        icon="star",
        criteria=_algum_quiz_perfeito(),
    ),
)


# ─── Evaluator ──────────────────────────────────────────────────────────


class BadgeEvaluator:
    """Avalia o `student_state` contra um catálogo de badges.

    Use a instância sem argumentos para o catálogo padrão, ou passe
    `badges=` para um catálogo customizado.
    """

    def __init__(self, badges: Iterable[BadgeDefinition] | None = None) -> None:
        self._badges: tuple[BadgeDefinition, ...] = (
            tuple(badges) if badges is not None else DEFAULT_BADGES
        )

    @property
    def catalog(self) -> tuple[BadgeDefinition, ...]:
        """Devolve o catálogo de badges configurado (imutável)."""
        return self._badges

    def evaluate(self, student_state: dict[str, Any]) -> list[BadgeDefinition]:
        """Devolve a lista de badges que o aluno conquistou agora.

        Args:
            student_state: dicionário com métricas. Chaves esperadas (todas
                opcionais): `modulos_concluidos`, `cursos_concluidos`,
                `streak_atual`, `quizzes` (lista de dicts com `accuracy`).

        Returns:
            Lista de `BadgeDefinition` cujos critérios foram atingidos,
            preservando a ordem do catálogo.
        """
        if not isinstance(student_state, dict):
            raise TypeError("student_state precisa ser um dict")

        return [b for b in self._badges if b.criteria(student_state)]
