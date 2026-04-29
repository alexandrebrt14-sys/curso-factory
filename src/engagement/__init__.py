"""Camada de engajamento do curso-factory — Wave 6.

Reúne quatro submódulos puros (sem rede, sem persistência server-side) que
implementam mecânicas inspiradas em Duolingo (SRS, streak, badges) e em
cohorts FIAP (microlearning + quizzes).

Exporta:
    - SRSCard, review, due_cards (algoritmo SM-2)
    - Streak, record_activity (contador diário com grace period opcional)
    - BadgeDefinition, BadgeEvaluator, DEFAULT_BADGES
    - QuizQuestion, QuizAttempt, score
"""

from __future__ import annotations

from src.engagement.badges import (
    DEFAULT_BADGES,
    BadgeDefinition,
    BadgeEvaluator,
)
from src.engagement.quiz import (
    QuizAttempt,
    QuizQuestion,
    score,
)
from src.engagement.srs import (
    SRSCard,
    due_cards,
    review,
)
from src.engagement.streak import (
    Streak,
    record_activity,
)

__all__ = [
    # SRS
    "SRSCard",
    "review",
    "due_cards",
    # Streak
    "Streak",
    "record_activity",
    # Badges
    "BadgeDefinition",
    "BadgeEvaluator",
    "DEFAULT_BADGES",
    # Quiz
    "QuizQuestion",
    "QuizAttempt",
    "score",
]
