"""Testes da camada de engajamento (Wave 6).

Cobre SRS (SM-2), Streak, Badges e Quiz. Todos os testes são puros — não
dependem de rede, banco ou disco.
"""

from __future__ import annotations

import sys
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.engagement.badges import (
    DEFAULT_BADGES,
    BadgeDefinition,
    BadgeEvaluator,
)
from src.engagement.quiz import QuizAttempt, QuizQuestion, score
from src.engagement.srs import (
    DEFAULT_EASE_FACTOR,
    MIN_EASE_FACTOR,
    SRSCard,
    due_cards,
    review,
)
from src.engagement.streak import Streak, record_activity


# ─── SRS ────────────────────────────────────────────────────────────────


def test_srs_card_novo_tem_defaults_corretos() -> None:
    card = SRSCard(concept_id="conceito-x")
    assert card.concept_id == "conceito-x"
    assert card.ease_factor == DEFAULT_EASE_FACTOR
    assert card.interval_days == 0
    assert card.repetitions == 0
    assert card.next_review.tzinfo is not None


def test_srs_review_quality_5_avanca_intervalo() -> None:
    now = datetime(2026, 4, 29, 12, 0, tzinfo=timezone.utc)
    card = SRSCard(concept_id="ml-supervisionado", next_review=now)
    revisado = review(card, quality=5, now=now)

    # Primeiro acerto: intervalo vira 1 dia, repetitions = 1.
    assert revisado.repetitions == 1
    assert revisado.interval_days == 1
    assert revisado.ease_factor >= DEFAULT_EASE_FACTOR
    assert revisado.next_review == now + timedelta(days=1)


def test_srs_review_quality_5_segunda_vez_vai_para_6_dias() -> None:
    now = datetime(2026, 4, 29, 12, 0, tzinfo=timezone.utc)
    card = SRSCard(concept_id="srs-2", next_review=now)
    primeira = review(card, quality=5, now=now)
    segunda = review(primeira, quality=5, now=now + timedelta(days=1))

    assert segunda.repetitions == 2
    assert segunda.interval_days == 6


def test_srs_review_quality_0_zera_repeticoes_e_volta_em_1_dia() -> None:
    now = datetime(2026, 4, 29, 12, 0, tzinfo=timezone.utc)
    card = SRSCard(
        concept_id="conceito-dificil",
        repetitions=4,
        interval_days=20,
        ease_factor=2.6,
        next_review=now,
    )
    revisado = review(card, quality=0, now=now)

    assert revisado.repetitions == 0
    assert revisado.interval_days == 1
    # ease_factor cai mas nunca abaixo de 1.3
    assert revisado.ease_factor >= MIN_EASE_FACTOR
    assert revisado.ease_factor < 2.6


def test_srs_review_quality_invalida_lanca_value_error() -> None:
    card = SRSCard(concept_id="x")
    with pytest.raises(ValueError):
        review(card, quality=7)


def test_srs_due_cards_filtra_e_ordena_por_atraso() -> None:
    now = datetime(2026, 4, 29, 12, 0, tzinfo=timezone.utc)
    devido_antigo = SRSCard(concept_id="a", next_review=now - timedelta(days=5))
    devido_recente = SRSCard(concept_id="b", next_review=now - timedelta(hours=1))
    futuro = SRSCard(concept_id="c", next_review=now + timedelta(days=3))

    devidos = due_cards([futuro, devido_recente, devido_antigo], now=now)

    assert [c.concept_id for c in devidos] == ["a", "b"]


# ─── Streak ─────────────────────────────────────────────────────────────


def test_streak_primeira_atividade_inicia_em_1() -> None:
    s = Streak()
    novo = record_activity(s, date(2026, 4, 29))
    assert novo.current == 1
    assert novo.longest == 1
    assert novo.last_activity == date(2026, 4, 29)


def test_streak_mesmo_dia_nao_muda() -> None:
    s = Streak(current=3, longest=5, last_activity=date(2026, 4, 29))
    novo = record_activity(s, date(2026, 4, 29))
    assert novo.current == 3
    assert novo.longest == 5
    assert novo.last_activity == date(2026, 4, 29)


def test_streak_dia_seguinte_incrementa() -> None:
    s = Streak(current=3, longest=3, last_activity=date(2026, 4, 29))
    novo = record_activity(s, date(2026, 4, 30))
    assert novo.current == 4
    assert novo.longest == 4
    assert novo.last_activity == date(2026, 4, 30)


def test_streak_pulo_de_1_dia_reseta_para_1() -> None:
    s = Streak(current=10, longest=10, last_activity=date(2026, 4, 29))
    # Pulou 30 -> 1 de maio = gap de 2 dias.
    novo = record_activity(s, date(2026, 5, 1))
    assert novo.current == 1
    # longest preserva o histórico
    assert novo.longest == 10


def test_streak_pulo_de_3_dias_reseta() -> None:
    s = Streak(current=20, longest=20, last_activity=date(2026, 4, 29))
    novo = record_activity(s, date(2026, 5, 3))
    assert novo.current == 1
    assert novo.longest == 20


def test_streak_grace_period_perdoa_um_pulo() -> None:
    s = Streak(current=5, longest=5, last_activity=date(2026, 4, 29))
    # Com grace=1, pular 1 dia ainda incrementa (gap de 2 dias).
    novo = record_activity(s, date(2026, 5, 1), grace_period_days=1)
    assert novo.current == 6
    assert novo.longest == 6


def test_streak_longest_atualiza_quando_current_supera() -> None:
    s = Streak(current=4, longest=4, last_activity=date(2026, 4, 29))
    novo = record_activity(s, date(2026, 4, 30))
    assert novo.current == 5
    assert novo.longest == 5


# ─── Badges ─────────────────────────────────────────────────────────────


def test_badge_definition_e_imutavel() -> None:
    b = BadgeDefinition(
        id="teste",
        name="Teste",
        description="badge de teste",
        icon="star",
        criteria=lambda s: True,
    )
    assert b.id == "teste"
    with pytest.raises(Exception):
        b.id = "outro"  # type: ignore[misc]


def test_badge_evaluator_concede_primeiro_modulo_e_streak_7() -> None:
    evaluator = BadgeEvaluator()
    state = {
        "modulos_concluidos": 2,
        "cursos_concluidos": 0,
        "streak_atual": 7,
        "quizzes": [{"accuracy": 0.8}],
    }
    concedidas = evaluator.evaluate(state)
    ids = {b.id for b in concedidas}
    assert "primeiro_modulo" in ids
    assert "streak_7" in ids
    assert "primeiro_curso_completo" not in ids
    assert "streak_30" not in ids
    assert "perfeito_em_quiz" not in ids


def test_badge_evaluator_concede_quiz_perfeito_e_curso_completo() -> None:
    evaluator = BadgeEvaluator()
    state = {
        "modulos_concluidos": 8,
        "cursos_concluidos": 1,
        "streak_atual": 30,
        "quizzes": [{"accuracy": 0.6}, {"accuracy": 1.0}],
    }
    concedidas = evaluator.evaluate(state)
    ids = {b.id for b in concedidas}
    # Estado completo deve disparar todas as 5 badges padrão.
    assert ids == {b.id for b in DEFAULT_BADGES}


def test_badge_evaluator_estado_vazio_nao_concede_nada() -> None:
    evaluator = BadgeEvaluator()
    concedidas = evaluator.evaluate({})
    assert concedidas == []


def test_badge_evaluator_aceita_catalogo_customizado() -> None:
    custom = BadgeDefinition(
        id="custom_x",
        name="Custom",
        description="só para o teste",
        icon="bolt",
        criteria=lambda s: s.get("xp", 0) >= 100,
    )
    evaluator = BadgeEvaluator(badges=[custom])
    assert evaluator.evaluate({"xp": 50}) == []
    assert evaluator.evaluate({"xp": 150}) == [custom]


# ─── Quiz ───────────────────────────────────────────────────────────────


def test_quiz_question_valida_correct_index_dentro_do_range() -> None:
    q = QuizQuestion(
        id="q1",
        prompt="Qual é a capital do Brasil?",
        options=["São Paulo", "Brasília", "Rio de Janeiro"],
        correct_index=1,
        explanation="Brasília é a capital federal desde 1960.",
    )
    assert q.options[q.correct_index] == "Brasília"


def test_quiz_question_correct_index_fora_do_range_falha() -> None:
    with pytest.raises(Exception):
        QuizQuestion(
            id="q1",
            prompt="Pergunta de teste",
            options=["A", "B"],
            correct_index=5,
        )


def test_quiz_score_acertos_e_acuracia() -> None:
    attempts = [
        QuizAttempt(question_id="q1", selected_index=1, correct=True),
        QuizAttempt(question_id="q2", selected_index=0, correct=True),
        QuizAttempt(question_id="q3", selected_index=2, correct=False),
        QuizAttempt(question_id="q4", selected_index=1, correct=False),
    ]
    resultado = score(attempts)
    assert resultado["total"] == 4
    assert resultado["correct"] == 2
    assert resultado["accuracy"] == 0.5
    assert resultado["weak_concepts"] == ["q3", "q4"]


def test_quiz_score_lista_vazia_devolve_zero_e_acuracia_zero() -> None:
    resultado = score([])
    assert resultado["total"] == 0
    assert resultado["correct"] == 0
    assert resultado["accuracy"] == 0.0
    assert resultado["weak_concepts"] == []


def test_quiz_score_weak_concepts_sem_duplicatas() -> None:
    attempts = [
        QuizAttempt(question_id="q1", selected_index=0, correct=False),
        QuizAttempt(question_id="q1", selected_index=1, correct=False),
        QuizAttempt(question_id="q2", selected_index=2, correct=True),
    ]
    resultado = score(attempts)
    # q1 aparece só uma vez mesmo com dois erros.
    assert resultado["weak_concepts"] == ["q1"]
    assert resultado["total"] == 3
    assert resultado["correct"] == 1
