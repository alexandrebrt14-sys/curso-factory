"""Testes para CostTracker e Cache (FinOps + persistência LLM)."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import src.cache as cache_mod
import src.cost_tracker as cost_tracker

# ─── CostTracker ─────────────────────────────────────────────────────

@pytest.fixture
def isolated_costs(tmp_path, monkeypatch):
    """Redireciona o log de custos para tmp_path para isolar dos dados reais."""
    fake_costs = tmp_path / "costs.json"
    monkeypatch.setattr(cost_tracker, "COSTS_FILE", fake_costs)
    return fake_costs


def test_cost_tracker_track_persiste(isolated_costs) -> None:
    tracker = cost_tracker.CostTracker()
    tracker.track("openai", 100, 200, "gpt-4o", 0.01, course_id="curso-x")
    assert isolated_costs.exists()
    assert tracker.get_session_total()["openai"] == 0.01


def test_cost_tracker_get_course_total(isolated_costs) -> None:
    tracker = cost_tracker.CostTracker()
    tracker.track("openai", 100, 200, "gpt-4o", 0.05, course_id="curso-A")
    tracker.track("anthropic", 50, 80, "claude", 0.10, course_id="curso-A")
    tracker.track("openai", 100, 200, "gpt-4o", 0.02, course_id="curso-B")

    total_a = tracker.get_course_total("curso-A")
    assert total_a["openai"] == 0.05
    assert total_a["anthropic"] == 0.10

    total_b = tracker.get_course_total("curso-B")
    assert total_b["openai"] == 0.02
    assert "anthropic" not in total_b


def test_cost_tracker_check_before_call_bloqueia_acima_budget(
    isolated_costs, monkeypatch
) -> None:
    """Acima de CLAUDE_BUDGET_PER_COURSE, check_before_call retorna False."""
    monkeypatch.setattr(cost_tracker, "CLAUDE_BUDGET_PER_COURSE", 1.0)
    monkeypatch.setattr(cost_tracker, "TOTAL_BUDGET_PER_COURSE", 100.0)
    tracker = cost_tracker.CostTracker()
    tracker.track("anthropic", 1000, 1000, "claude", 1.50, course_id="caro")
    assert tracker.check_before_call("anthropic", course_id="caro") is False


def test_pode_chamar_ignora_teto_diario_e_respeita_curso_e_sessao(
    isolated_costs, monkeypatch
) -> None:
    """O teto diário por provedor não barra; o do curso e o da sessão barram, com motivo."""
    monkeypatch.setattr(cost_tracker, "DAILY_BUDGET_PER_PROVIDER", 0.05)
    monkeypatch.setattr(cost_tracker, "CLAUDE_BUDGET_PER_COURSE", 1.0)
    monkeypatch.setattr(cost_tracker, "TOTAL_BUDGET_PER_COURSE", 2.0)
    monkeypatch.setattr(cost_tracker, "SESSION_BUDGET_TOTAL", 3.0)
    tracker = cost_tracker.CostTracker()
    tracker.track("anthropic", 1000, 1000, "claude", 0.50, course_id="c1")
    # acima do teto diário (0,05), abaixo do teto do curso: pode
    assert tracker.is_over_budget("anthropic") is True
    assert tracker.pode_chamar("anthropic", "c1") == (True, "")
    tracker.track("anthropic", 1000, 1000, "claude", 0.60, course_id="c1")
    ok, motivo = tracker.pode_chamar("anthropic", "c1")
    assert ok is False and "Claude do curso" in motivo
    assert tracker.pode_chamar("google", "c1") == (True, "")
    tracker.track("google", 1000, 1000, "gemini", 1.00, course_id="c1")
    ok, motivo = tracker.pode_chamar("google", "c1")
    assert ok is False and "total do curso" in motivo
    tracker.track("google", 1000, 1000, "gemini", 1.00, course_id="c2")
    ok, motivo = tracker.pode_chamar("google", "c2")
    assert ok is False and "sessão" in motivo


def test_entradas_desde_mede_o_consumo_de_uma_etapa(isolated_costs) -> None:
    tracker = cost_tracker.CostTracker()
    tracker.track("openai", 1, 1, "gpt", 0.01, course_id="c1")
    marca = tracker.indice_atual()
    tracker.track("anthropic", 1, 1, "claude", 0.02, course_id="c1")
    tracker.track("anthropic", 1, 1, "claude", 0.02, course_id="outro")
    novas = tracker.entradas_desde(marca, "c1")
    assert [e["provider"] for e in novas] == ["anthropic"]
    assert len(tracker.entradas_desde(marca)) == 2


def test_cost_tracker_report_sem_entries() -> None:
    """Sem dados na sessão atual, report() retorna a string conhecida."""
    tracker = cost_tracker.CostTracker(session_id="sess_inexistente_xyz")
    assert "Nenhum custo" in tracker.report()


# ─── Cache ───────────────────────────────────────────────────────────

@pytest.fixture
def isolated_cache(tmp_path, monkeypatch):
    monkeypatch.setattr(cache_mod, "CACHE_DIR", tmp_path / ".cache")
    return tmp_path / ".cache"


def test_cache_set_get_roundtrip(isolated_cache) -> None:
    c = cache_mod.Cache(ttl=3600)
    c.set("prompt foo", "openai", "gpt-4o", "resposta foo")
    assert c.get("prompt foo", "openai", "gpt-4o") == "resposta foo"


def test_cache_miss_quando_modelo_diferente(isolated_cache) -> None:
    c = cache_mod.Cache(ttl=3600)
    c.set("prompt foo", "openai", "gpt-4o", "resposta foo")
    assert c.get("prompt foo", "openai", "gpt-4o-mini") is None


def test_cache_clear_remove_tudo(isolated_cache) -> None:
    c = cache_mod.Cache(ttl=3600)
    c.set("a", "openai", "m", "v1")
    c.set("b", "openai", "m", "v2")
    removidos = c.clear()
    assert removidos == 2
    assert c.get("a", "openai", "m") is None


def test_cache_expira_apos_ttl(isolated_cache) -> None:
    c = cache_mod.Cache(ttl=0)  # expira instantaneamente
    c.set("p", "openai", "m", "v")
    # Com ttl=0, qualquer get subsequente já deve considerar expirado
    assert c.get("p", "openai", "m") is None
