"""Rastreamento de custos em tempo real para chamadas LLM.

Mantém log JSON em output/costs.json e oferece métodos para
consultar totais diários, por sessão e verificar orçamento.
"""

from __future__ import annotations

import json
import logging
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Optional

from src.config import (
    OUTPUT_DIR, DAILY_BUDGET_PER_PROVIDER, SESSION_BUDGET_TOTAL,
    CLAUDE_BUDGET_PER_COURSE, TOTAL_BUDGET_PER_COURSE,
)

logger = logging.getLogger(__name__)

COSTS_FILE = OUTPUT_DIR / "costs.json"


class CostTracker:
    """Rastreia custos de chamadas LLM com persistência em JSON."""

    def __init__(self, session_id: Optional[str] = None) -> None:
        self.session_id = session_id or datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        self._entries: list[dict] = []
        self._load()

    def _load(self) -> None:
        """Carrega entradas existentes do arquivo JSON."""
        if COSTS_FILE.exists():
            try:
                with open(COSTS_FILE, "r", encoding="utf-8") as f:
                    self._entries = json.load(f)
            except (json.JSONDecodeError, OSError):
                self._entries = []

    def _save(self) -> None:
        """Persiste todas as entradas no arquivo JSON."""
        COSTS_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(COSTS_FILE, "w", encoding="utf-8") as f:
            json.dump(self._entries, f, indent=2, ensure_ascii=False, default=str)

    def track(
        self, provider: str, tokens_in: int, tokens_out: int,
        model: str, custo_usd: float, course_id: str = ""
    ) -> None:
        """Registra uma chamada LLM com seu custo."""
        entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "provider": provider,
            "model": model,
            "tokens_in": tokens_in,
            "tokens_out": tokens_out,
            "custo_usd": round(custo_usd, 6),
            "sessao": self.session_id,
            "course_id": course_id,
        }
        self._entries.append(entry)
        self._save()

    def get_daily_total(self, provider: str) -> float:
        """Retorna o custo total do dia para um provider específico."""
        hoje = date.today().isoformat()
        return sum(
            e["custo_usd"]
            for e in self._entries
            if e["provider"] == provider and e["timestamp"].startswith(hoje)
        )

    def get_session_total(self) -> dict[str, float]:
        """Retorna o custo total da sessão atual por provider."""
        totais: dict[str, float] = {}
        for e in self._entries:
            if e["sessao"] == self.session_id:
                totais[e["provider"]] = totais.get(e["provider"], 0.0) + e["custo_usd"]
        return totais

    def is_over_budget(self, provider: str) -> bool:
        """Verifica se o provider excedeu o orçamento diário."""
        daily = self.get_daily_total(provider)
        session_totals = self.get_session_total()
        session_sum = sum(session_totals.values())
        if daily >= DAILY_BUDGET_PER_PROVIDER:
            logger.warning("Provider %s excedeu orçamento diário: USD %.4f", provider, daily)
            return True
        if session_sum >= SESSION_BUDGET_TOTAL:
            logger.warning("Orçamento total da sessão excedido: USD %.4f", session_sum)
            return True
        return False

    def get_course_total(self, course_id: str) -> dict[str, float]:
        """Retorna custos por provider para um curso específico."""
        totais: dict[str, float] = {}
        for e in self._entries:
            if e.get("course_id") == course_id:
                p = e["provider"]
                totais[p] = totais.get(p, 0.0) + e["custo_usd"]
        return totais

    def check_before_call(self, provider: str, course_id: str = "") -> bool:
        """Verifica se a próxima chamada está dentro do budget.

        Returns True se está OK, False se deve bloquear.
        Aplica limites:
        - Claude: máx $5.00 por curso
        - Total: máx $10.00 por curso
        """
        if not course_id:
            return not self.is_over_budget(provider)

        course_costs = self.get_course_total(course_id)
        total_course = sum(course_costs.values())
        claude_course = course_costs.get("anthropic", 0.0)

        if provider == "anthropic" and claude_course >= CLAUDE_BUDGET_PER_COURSE:
            logger.warning(
                "Budget Claude excedido para curso %s: USD %.2f >= %.2f",
                course_id, claude_course, CLAUDE_BUDGET_PER_COURSE,
            )
            return False

        if total_course >= TOTAL_BUDGET_PER_COURSE:
            logger.warning(
                "Budget total excedido para curso %s: USD %.2f >= %.2f",
                course_id, total_course, TOTAL_BUDGET_PER_COURSE,
            )
            return False

        return True

    def report(self) -> str:
        """Gera relatório formatado dos custos da sessão."""
        totais = self.get_session_total()
        if not totais:
            return "Nenhum custo registrado nesta sessão."
        linhas = [
            "--- Relatório de Custos ---",
            f"{'Provider':<15} {'Custo (USD)':>12}",
            "-" * 28,
        ]
        total_geral = 0.0
        for provider, custo in sorted(totais.items()):
            linhas.append(f"{provider:<15} {custo:>12.4f}")
            total_geral += custo
        linhas.append("-" * 28)
        linhas.append(f"{'TOTAL':<15} {total_geral:>12.4f}")
        linhas.append(f"Orçamento sessão: USD {SESSION_BUDGET_TOTAL:.2f}")
        return "\n".join(linhas)
