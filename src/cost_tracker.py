"""Rastreamento de custos em tempo real para chamadas LLM.

Mantém o ledger em ``output/costs.json`` (lista de entradas) e oferece
consultas por dia, por sessão e por curso, além da decisão de orçamento
(:meth:`CostTracker.pode_chamar`) que o orquestrador consulta antes de cada
chamada paga.
"""

from __future__ import annotations

import logging
from collections.abc import Callable
from datetime import UTC, datetime

from src.config import (
    CLAUDE_BUDGET_PER_COURSE,
    DAILY_BUDGET_PER_PROVIDER,
    OUTPUT_DIR,
    SESSION_BUDGET_TOTAL,
    TOTAL_BUDGET_PER_COURSE,
)
from src.fsutil import read_json_or_none, write_json_atomic

logger = logging.getLogger(__name__)

COSTS_FILE = OUTPUT_DIR / "costs.json"

Entry = dict


class CostTracker:
    """Rastreia custos de chamadas LLM com persistência em JSON."""

    def __init__(self, session_id: str | None = None) -> None:
        self.session_id = session_id or datetime.now(UTC).strftime("%Y%m%d_%H%M%S")
        self._entries: list[Entry] = []
        self._load()

    # ------------------------------------------------------------------ I/O
    def _load(self) -> None:
        """Carrega o ledger. Arquivo corrompido é isolado, nunca sobrescrito."""
        data = read_json_or_none(COSTS_FILE)
        if isinstance(data, list):
            self._entries = [e for e in data if isinstance(e, dict)]
        elif data is not None:
            logger.error("Ledger %s não é uma lista; começando vazio", COSTS_FILE)
            self._entries = []

    def _save(self) -> None:
        """Persiste o ledger. Falha de disco vira log, não interrompe o pipeline."""
        try:
            write_json_atomic(COSTS_FILE, self._entries)
        except OSError as exc:
            logger.error("Não consegui gravar o ledger de custos em %s: %s", COSTS_FILE, exc)

    def entries(self) -> list[Entry]:
        """Cópia das entradas do ledger (fonte única para relatórios)."""
        return list(self._entries)

    # ------------------------------------------------------------- registro
    def track(
        self,
        provider: str,
        tokens_in: int,
        tokens_out: int,
        model: str,
        custo_usd: float,
        course_id: str = "",
    ) -> None:
        """Registra uma chamada LLM com seu custo."""
        entry: Entry = {
            "timestamp": datetime.now(UTC).isoformat(),
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

    # ------------------------------------------------------------- consultas
    def _totals_by_provider(self, pred: Callable[[Entry], bool]) -> dict[str, float]:
        totais: dict[str, float] = {}
        for e in self._entries:
            if pred(e):
                p = str(e.get("provider", ""))
                totais[p] = totais.get(p, 0.0) + float(e.get("custo_usd", 0.0))
        return totais

    def get_daily_total(self, provider: str) -> float:
        """Custo total de hoje (dia UTC, mesmo fuso dos carimbos) para um provider."""
        hoje = datetime.now(UTC).date().isoformat()
        return sum(
            float(e.get("custo_usd", 0.0))
            for e in self._entries
            if e.get("provider") == provider and str(e.get("timestamp", "")).startswith(hoje)
        )

    def get_session_total(self) -> dict[str, float]:
        """Custo total da sessão atual por provider."""
        return self._totals_by_provider(lambda e: e.get("sessao") == self.session_id)

    def get_course_total(self, course_id: str) -> dict[str, float]:
        """Custos por provider para um curso específico."""
        return self._totals_by_provider(lambda e: e.get("course_id") == course_id)

    def indice_atual(self) -> int:
        """Posição do ledger, para medir o que uma etapa consumiu (`entradas_desde`)."""
        return len(self._entries)

    def entradas_desde(self, indice: int, course_id: str = "") -> list[Entry]:
        """Entradas registradas a partir de `indice`, filtradas por curso quando pedido."""
        novas = self._entries[indice:]
        if course_id:
            novas = [e for e in novas if e.get("course_id") == course_id]
        return list(novas)

    # ------------------------------------------------------------ orçamento
    def is_over_budget(self, provider: str) -> bool:
        """Verifica o teto diário do provider e o teto total da sessão."""
        daily = self.get_daily_total(provider)
        session_sum = sum(self.get_session_total().values())
        if daily >= DAILY_BUDGET_PER_PROVIDER:
            logger.warning("Provider %s excedeu orçamento diário: USD %.4f", provider, daily)
            return True
        if session_sum >= SESSION_BUDGET_TOTAL:
            logger.warning("Orçamento total da sessão excedido: USD %.4f", session_sum)
            return True
        return False

    def pode_chamar(self, provider: str, course_id: str = "") -> tuple[bool, str]:
        """Decide se a próxima chamada cabe no orçamento e diz qual limite barrou.

        Combina o teto por curso com o teto total da sessão. O teto DIÁRIO por
        provedor fica de fora de propósito: quando um provedor cai e a cadeia
        de fallback concentra tudo em outro, o teto diário do sobrevivente
        cortava o pipeline no meio (E2E de 02/09/2026: revisão interrompida na
        aula 2 com US$ 2,13 no Anthropic). O que protege o bolso é o teto por
        curso e o da sessão.

        Returns:
            (True, "") quando pode chamar; (False, motivo) quando não.
        """
        session_sum = sum(self.get_session_total().values())
        if session_sum >= SESSION_BUDGET_TOTAL:
            return (
                False,
                f"orçamento da sessão esgotado (USD {session_sum:.2f} >= {SESSION_BUDGET_TOTAL:.2f})",
            )
        if course_id:
            course_costs = self.get_course_total(course_id)
            total_course = sum(course_costs.values())
            claude_course = course_costs.get("anthropic", 0.0)
            if provider == "anthropic" and claude_course >= CLAUDE_BUDGET_PER_COURSE:
                return (
                    False,
                    f"orçamento Claude do curso esgotado (USD {claude_course:.2f} >= {CLAUDE_BUDGET_PER_COURSE:.2f})",
                )
            if total_course >= TOTAL_BUDGET_PER_COURSE:
                return (
                    False,
                    f"orçamento total do curso esgotado (USD {total_course:.2f} >= {TOTAL_BUDGET_PER_COURSE:.2f})",
                )
        return True, ""

    def check_before_call(self, provider: str, course_id: str = "") -> bool:
        """Forma booleana de :meth:`pode_chamar` (mantida por compatibilidade)."""
        ok, motivo = self.pode_chamar(provider, course_id)
        if not ok:
            logger.warning("Chamada a %s barrada: %s", provider, motivo)
        return ok

    # ------------------------------------------------------------- relatório
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
