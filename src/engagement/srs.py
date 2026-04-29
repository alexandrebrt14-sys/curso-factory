"""Spaced Repetition System (SM-2) para reforço de conceitos do curso.

Implementação de variante leve do algoritmo SM-2 (SuperMemo 2) usado pelo
Anki e Duolingo. Cada conceito vira um `SRSCard` que é revisado com uma
nota de qualidade (0-5). O algoritmo recalcula:

    - `ease_factor` (fator de facilidade, mínimo 1.3)
    - `interval_days` (próximo intervalo de revisão em dias)
    - `repetitions` (sequência atual de acertos consecutivos)
    - `next_review` (data/hora da próxima revisão sugerida)

Não persiste nada — devolve sempre uma nova instância imutável (`model_copy`
do Pydantic) para que o caller decida onde armazenar (Supabase, JSON local,
etc.). Sem rede, sem efeitos colaterais.
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Iterable

from pydantic import BaseModel, Field, field_validator


def _now_utc() -> datetime:
    """Wall-clock UTC; substitui datetime.utcnow() (deprecated em 3.12)."""
    return datetime.now(timezone.utc)


# Constantes do SM-2 clássico.
MIN_EASE_FACTOR: float = 1.3
DEFAULT_EASE_FACTOR: float = 2.5
QUALITY_PASS_THRESHOLD: int = 3  # nota >= 3 conta como acerto


class SRSCard(BaseModel):
    """Cartão de revisão associado a um conceito do curso.

    Atributos:
        concept_id: identificador do conceito/etapa (ex: slug do step).
        ease_factor: facilidade (>= 1.3). Cresce com acertos, cai com erros.
        interval_days: dias até a próxima revisão.
        repetitions: número de acertos consecutivos. Reseta para 0 em erro.
        next_review: timestamp UTC da próxima revisão sugerida.
    """

    concept_id: str = Field(..., min_length=1, description="ID do conceito/etapa")
    ease_factor: float = Field(default=DEFAULT_EASE_FACTOR, ge=MIN_EASE_FACTOR)
    interval_days: int = Field(default=0, ge=0, description="Dias até próxima revisão")
    repetitions: int = Field(default=0, ge=0, description="Acertos consecutivos")
    next_review: datetime = Field(default_factory=_now_utc)

    @field_validator("next_review")
    @classmethod
    def _ensure_tz(cls, v: datetime) -> datetime:
        """Garante que `next_review` sempre tenha timezone."""
        if v.tzinfo is None:
            return v.replace(tzinfo=timezone.utc)
        return v


def review(card: SRSCard, quality: int, now: datetime | None = None) -> SRSCard:
    """Aplica uma revisão SM-2 ao cartão e devolve uma nova instância.

    Args:
        card: cartão atual.
        quality: nota da resposta (0-5). Convenção SM-2:
            0 = blackout total
            1 = errou, lembrou ao ver a resposta
            2 = errou, mas a resposta pareceu fácil ao ver
            3 = acertou com dificuldade
            4 = acertou com hesitação
            5 = acertou com perfeição
        now: timestamp de referência (default: agora UTC).

    Returns:
        Novo `SRSCard` com `ease_factor`, `interval_days`, `repetitions`
        e `next_review` recalculados.

    Raises:
        ValueError: se `quality` estiver fora de [0, 5].
    """
    if not 0 <= quality <= 5:
        raise ValueError(f"quality precisa estar em [0, 5], recebido {quality}")

    reference = now or _now_utc()
    if reference.tzinfo is None:
        reference = reference.replace(tzinfo=timezone.utc)

    # Recalcula ease_factor pela fórmula SM-2.
    new_ef = card.ease_factor + (
        0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02)
    )
    new_ef = max(MIN_EASE_FACTOR, new_ef)

    if quality < QUALITY_PASS_THRESHOLD:
        # Falha: zera repetições e volta para revisão no dia seguinte.
        new_repetitions = 0
        new_interval = 1
    else:
        # Sucesso: avança a sequência.
        new_repetitions = card.repetitions + 1
        if new_repetitions == 1:
            new_interval = 1
        elif new_repetitions == 2:
            new_interval = 6
        else:
            # Intervalo cresce multiplicando pelo ease_factor.
            new_interval = max(1, round(card.interval_days * new_ef))

    next_review = reference + timedelta(days=new_interval)

    return card.model_copy(
        update={
            "ease_factor": round(new_ef, 4),
            "interval_days": new_interval,
            "repetitions": new_repetitions,
            "next_review": next_review,
        }
    )


def due_cards(cards: Iterable[SRSCard], now: datetime | None = None) -> list[SRSCard]:
    """Filtra cartões com revisão devida (next_review <= now).

    Args:
        cards: iterável de cartões.
        now: timestamp de referência (default: agora UTC).

    Returns:
        Lista de cartões cuja revisão já está devida, ordenados pelo mais
        atrasado primeiro (next_review crescente).
    """
    reference = now or _now_utc()
    if reference.tzinfo is None:
        reference = reference.replace(tzinfo=timezone.utc)

    devidos = [c for c in cards if c.next_review <= reference]
    devidos.sort(key=lambda c: c.next_review)
    return devidos
