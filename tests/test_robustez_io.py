"""Robustez de I/O: JSON atômico, ledger e checkpoint corrompidos, drafts por cliente.

Cobre o que a refatoração de 08/09/2026 prometeu: arquivo corrompido nunca é
sobrescrito nem apaga histórico; gravação interrompida nunca deixa JSON
parcial; cada cliente grava os rascunhos no próprio diretório.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import src.cost_tracker as cost_tracker
from src.fsutil import quarantine_corrupt, read_json_or_none, write_json_atomic

# ─── fsutil ──────────────────────────────────────────────────────────


def test_write_json_atomic_nao_deixa_temporario(tmp_path: Path) -> None:
    alvo = tmp_path / "sub" / "dados.json"
    write_json_atomic(alvo, {"a": 1, "b": [1, 2]})
    assert json.loads(alvo.read_text(encoding="utf-8")) == {"a": 1, "b": [1, 2]}
    assert [p.name for p in alvo.parent.iterdir()] == ["dados.json"]


def test_write_json_atomic_preserva_anterior_se_serializacao_falhar(tmp_path: Path) -> None:
    alvo = tmp_path / "dados.json"
    write_json_atomic(alvo, {"ok": True})

    class _Insersializavel:
        pass

    # default=str converte objetos; força a falha com um ciclo.
    ciclo: list = []
    ciclo.append(ciclo)
    with pytest.raises(ValueError):
        write_json_atomic(alvo, ciclo)
    assert json.loads(alvo.read_text(encoding="utf-8")) == {"ok": True}
    assert [p.name for p in tmp_path.iterdir()] == ["dados.json"]


def test_read_json_or_none_isola_corrompido(tmp_path: Path) -> None:
    alvo = tmp_path / "dados.json"
    alvo.write_text('{"truncado": ', encoding="utf-8")
    assert read_json_or_none(alvo) is None
    assert not alvo.exists()
    isolados = list(tmp_path.glob("dados.json.corrupt-*"))
    assert len(isolados) == 1
    assert isolados[0].read_text(encoding="utf-8") == '{"truncado": '


def test_read_json_or_none_sem_quarentena(tmp_path: Path) -> None:
    alvo = tmp_path / "dados.json"
    alvo.write_text("nao é json", encoding="utf-8")
    assert read_json_or_none(alvo, quarantine=False) is None
    assert alvo.exists()


def test_read_json_or_none_ausente(tmp_path: Path) -> None:
    assert read_json_or_none(tmp_path / "nada.json") is None


def test_quarantine_corrupt_devolve_destino(tmp_path: Path) -> None:
    alvo = tmp_path / "x.json"
    alvo.write_text("{", encoding="utf-8")
    dest = quarantine_corrupt(alvo)
    assert dest is not None and dest.exists() and not alvo.exists()


# ─── CostTracker ─────────────────────────────────────────────────────


@pytest.fixture
def ledger(tmp_path, monkeypatch) -> Path:
    fake = tmp_path / "costs.json"
    monkeypatch.setattr(cost_tracker, "COSTS_FILE", fake)
    return fake


def test_ledger_corrompido_e_isolado_e_nao_sobrescrito(ledger: Path) -> None:
    ledger.write_text('[{"provider": "openai", "custo_usd": 1.0', encoding="utf-8")
    tracker = cost_tracker.CostTracker()
    assert tracker.entries() == []
    tracker.track("openai", 1, 1, "gpt", 0.001)
    # O arquivo novo tem só a entrada nova; o corrompido sobrevive ao lado.
    assert len(json.loads(ledger.read_text(encoding="utf-8"))) == 1
    assert len(list(ledger.parent.glob("costs.json.corrupt-*"))) == 1


def test_ledger_com_formato_errado_comeca_vazio(ledger: Path) -> None:
    ledger.write_text('{"nao": "lista"}', encoding="utf-8")
    tracker = cost_tracker.CostTracker()
    assert tracker.entries() == []


def test_entries_devolve_copia(ledger: Path) -> None:
    tracker = cost_tracker.CostTracker()
    tracker.track("openai", 1, 1, "gpt", 0.001)
    copia = tracker.entries()
    copia.clear()
    assert len(tracker.entries()) == 1


def test_get_daily_total_usa_dia_utc(ledger: Path, monkeypatch) -> None:
    tracker = cost_tracker.CostTracker()
    tracker.track("openai", 1, 1, "gpt", 0.5)
    # A entrada acabou de ser carimbada em UTC: tem de contar como "hoje".
    assert tracker.get_daily_total("openai") == pytest.approx(0.5)


def test_entrada_antiga_sem_campos_nao_derruba_totais(ledger: Path) -> None:
    ledger.write_text(json.dumps([{"timestamp": "2026-01-01T00:00:00+00:00"}]), encoding="utf-8")
    tracker = cost_tracker.CostTracker()
    assert tracker.get_session_total() == {}
    assert tracker.get_daily_total("openai") == 0.0


def test_check_before_call_equivale_a_pode_chamar(ledger: Path, monkeypatch) -> None:
    monkeypatch.setattr(cost_tracker, "TOTAL_BUDGET_PER_COURSE", 0.05)
    tracker = cost_tracker.CostTracker()
    tracker.track("openai", 1, 1, "gpt", 0.06, course_id="c")
    assert tracker.pode_chamar("openai", "c")[0] is False
    assert tracker.check_before_call("openai", "c") is False
    assert tracker.check_before_call("openai", "outro") is True


# ─── Orchestrator: checkpoint e drafts por cliente ───────────────────


def _orquestrador(tmp_path, monkeypatch, client_context=None):
    from src.orchestrator import Orchestrator

    class _Cliente:
        def set_course_context(self, cid):
            pass

        def close(self):
            self.fechado = True

    cliente = _Cliente()
    monkeypatch.setattr("src.llm_client.make_llm_client", lambda tracker: cliente)
    kwargs = {"cost_tracker": cost_tracker.CostTracker()}
    if client_context is not None:
        kwargs["client_context"] = client_context
    else:
        kwargs["drafts_dir"] = tmp_path
    return Orchestrator(**kwargs), cliente


def test_checkpoint_corrompido_e_isolado_e_pipeline_recomeca(tmp_path, monkeypatch, ledger) -> None:
    orq, _ = _orquestrador(tmp_path, monkeypatch)
    cp = orq._checkpoint_path("curso-x")
    cp.write_text('{"etapas": {"research": "ok"', encoding="utf-8")
    assert orq._load_checkpoint("curso-x") is None
    assert not cp.exists()
    assert len(list(tmp_path.glob("curso-x_checkpoint.json.corrupt-*"))) == 1


def test_checkpoint_valido_e_retomado(tmp_path, monkeypatch, ledger) -> None:
    from src.orchestrator import PipelineResult

    orq, _ = _orquestrador(tmp_path, monkeypatch)
    r = PipelineResult("curso-y")
    r.etapas["research"] = "pesquisa"
    orq._save_checkpoint("curso-y", r, context="ctx")
    carregado = orq._load_checkpoint("curso-y")
    assert carregado is not None
    result, context = carregado
    assert result.etapas == {"research": "pesquisa"}
    assert context == "ctx"
    assert [p.name for p in tmp_path.iterdir()] == ["curso-y_checkpoint.json"]


def test_drafts_dir_segue_o_cliente(tmp_path, monkeypatch, ledger) -> None:
    from src.clients import load_client

    acme = load_client("acme")
    monkeypatch.setattr(acme, "output_base_dir", tmp_path)
    orq, _ = _orquestrador(tmp_path, monkeypatch, client_context=acme)
    assert orq.drafts_dir == tmp_path / "clients" / "acme" / "drafts"
    assert orq.drafts_dir == acme.output_dir / "drafts"


def test_orchestrator_close_fecha_o_cliente(tmp_path, monkeypatch, ledger) -> None:
    orq, cliente = _orquestrador(tmp_path, monkeypatch)
    with orq:
        pass
    assert getattr(cliente, "fechado", False) is True


# ─── accent_checker: blocos de código e contexto ─────────────────────


def test_check_accents_ignora_bloco_de_codigo_inteiro() -> None:
    from src.validators.accent_checker import check_accents

    texto = "Voce sabe.\n```\nvoce = 1\n```\nProducao alta."
    erros = check_accents(texto)
    linhas = sorted(e.linha for e in erros)
    assert linhas == [1, 5]


def test_check_accents_contexto_da_ocorrencia_certa() -> None:
    from src.validators.accent_checker import check_accents

    texto = "voce primeiro e depois " + ("x " * 30) + "voce de novo"
    erros = [e for e in check_accents(texto) if e.palavra_errada == "voce"]
    assert len(erros) == 2
    assert "de novo" in erros[1].contexto
    assert "de novo" not in erros[0].contexto


# ─── draft_to_course: duração sem dígito ─────────────────────────────


def test_minutos_tolera_rotulo_sem_numero() -> None:
    from src.converters.draft_to_course import DEFAULT_MODULE_MINUTES, _minutos

    assert _minutos("25 min", 18) == 25
    assert _minutos("aprox. meia hora", 18) == 18
    assert _minutos("", 18) == 18
    assert DEFAULT_MODULE_MINUTES == 18


# ─── quality_gate: texto_corrigido sem auto_fix ──────────────────────


def test_texto_corrigido_e_o_input_sem_auto_fix() -> None:
    from src.validators.quality_gate import QualityGate

    texto = "# Título\n\nUm parágrafo curto de teste."
    r = QualityGate(auto_fix=False).check_text(texto, curso_id="t")
    assert r.texto_corrigido == texto
