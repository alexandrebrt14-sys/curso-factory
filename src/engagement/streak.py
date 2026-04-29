"""Contador de streak diário inspirado no Duolingo.

Mantém duas métricas:
    - `current`: dias consecutivos de atividade até o presente.
    - `longest`: melhor sequência histórica do aluno.

Regras de transição (com `today` representando a data da nova atividade):
    - Mesmo dia que `last_activity`: nada muda.
    - `today == last_activity + 1 dia`: incrementa `current`.
    - `today` está dentro do `grace_period_days` após `last_activity + 1`:
      preserva o `current` mas atualiza `last_activity` (perdão configurável).
    - Caso contrário: reset para `current = 1`.

`longest` é atualizado sempre que `current` ultrapassa o valor anterior.
"""

from __future__ import annotations

from datetime import date, timedelta

from pydantic import BaseModel, Field


class Streak(BaseModel):
    """Estado da sequência de atividades do aluno.

    Atributos:
        current: dias consecutivos atualmente registrados.
        longest: maior sequência histórica.
        last_activity: data da última atividade contabilizada.
    """

    current: int = Field(default=0, ge=0, description="Streak atual em dias")
    longest: int = Field(default=0, ge=0, description="Melhor streak histórica")
    last_activity: date | None = Field(default=None, description="Data da última atividade")


def record_activity(
    streak: Streak,
    today: date,
    grace_period_days: int = 0,
) -> Streak:
    """Registra atividade no dia `today` e devolve um novo `Streak`.

    Args:
        streak: estado atual.
        today: data da atividade que está sendo registrada.
        grace_period_days: tolerância em dias após o gap natural de 1 dia.
            Default 0 (regra clássica). Com `grace_period_days=1`, pular
            um único dia ainda preserva a streak.

    Returns:
        Novo `Streak` com `current`, `longest` e `last_activity` atualizados.

    Raises:
        ValueError: se `grace_period_days < 0` ou se `today` for anterior
            à `last_activity` registrada.
    """
    if grace_period_days < 0:
        raise ValueError("grace_period_days precisa ser >= 0")

    if streak.last_activity is None:
        # Primeira atividade do aluno: streak começa em 1.
        new_current = 1
        new_longest = max(streak.longest, new_current)
        return streak.model_copy(
            update={
                "current": new_current,
                "longest": new_longest,
                "last_activity": today,
            }
        )

    if today < streak.last_activity:
        raise ValueError(
            f"today ({today}) é anterior à última atividade ({streak.last_activity})"
        )

    delta = (today - streak.last_activity).days

    if delta == 0:
        # Mesmo dia: nada muda.
        return streak.model_copy()

    # `delta == 1` é o caso natural; `1 < delta <= 1 + grace` ainda preserva.
    if delta == 1 or 1 < delta <= 1 + grace_period_days:
        new_current = streak.current + 1
    else:
        # Pulo grande: reset para 1 (a atividade de hoje conta).
        new_current = 1

    new_longest = max(streak.longest, new_current)

    return streak.model_copy(
        update={
            "current": new_current,
            "longest": new_longest,
            "last_activity": today,
        }
    )
