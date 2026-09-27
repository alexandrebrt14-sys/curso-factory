"""27/09/2026: tamanho e ordem do curso, orientados pelos dados de uso do portal."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest
import yaml

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.validators import rules_loader  # noqa: E402
from src.validators.planejamento_checker import (  # noqa: E402
    check_planejamento_curso,
    instrucao_da_aula,
    instrucao_do_plano,
)

REGRAS = PROJECT_ROOT / "config" / "quality_rules.yaml"


@pytest.fixture
def regras_trocadas(tmp_path, monkeypatch):
    def _trocar(alterar) -> None:
        dados = yaml.safe_load(REGRAS.read_text(encoding="utf-8"))
        alterar(dados["validation"])
        destino = tmp_path / "quality_rules.yaml"
        destino.write_text(yaml.safe_dump(dados, allow_unicode=True), encoding="utf-8")
        monkeypatch.setattr(rules_loader, "RULES_PATH", destino)
        rules_loader.load_rules.cache_clear()

    yield _trocar
    rules_loader.load_rules.cache_clear()


def _aula(n: int, palavras: int) -> tuple[str, str]:
    titulo = f"Aula 1.{n}: Tema {n}"
    return titulo, f"# {titulo}\n\n" + " ".join(["palavra"] * palavras)


def _secao() -> dict:
    return yaml.safe_load(REGRAS.read_text(encoding="utf-8"))["validation"]["planejamento"]


def test_curso_na_faixa_com_aulas_iniciais_curtas_passa() -> None:
    s = _secao()
    minimo = s["aulas_por_curso"][0]
    aulas = [_aula(i, 500) for i in range(1, minimo + 1)]
    assert check_planejamento_curso(aulas) == []


def test_aula_inicial_acima_do_alvo_e_aviso() -> None:
    s = _secao()
    minimo = s["aulas_por_curso"][0]
    teto = s["palavras_max_aulas_iniciais"]
    aulas = [_aula(i, 500) for i in range(1, minimo + 1)]
    aulas[1] = _aula(2, teto + 50)
    aulas[s["aulas_iniciais_curtas"]] = _aula(s["aulas_iniciais_curtas"] + 1, teto + 500)
    achados = check_planejamento_curso(aulas)
    assert [(a.regra, a.tipo) for a in achados] == [("aula-inicial-longa", "warning")]
    assert "Aula 1.2" in achados[0].mensagem


def test_curso_fora_da_faixa_e_aviso() -> None:
    achados = check_planejamento_curso([_aula(i, 500) for i in range(1, 31)])
    assert [(a.regra, a.tipo) for a in achados] == [("curso-tamanho", "warning")]


def test_numeros_vem_do_yaml(regras_trocadas) -> None:
    def muda(v):
        v["planejamento"]["aulas_por_curso"] = [2, 3]
        v["planejamento"]["palavras_max_aulas_iniciais"] = 100

    regras_trocadas(muda)
    achados = check_planejamento_curso([_aula(1, 150), _aula(2, 50)])
    assert [a.regra for a in achados] == ["aula-inicial-longa"]
    assert "entre 2 e 3" in instrucao_do_plano(1)
    assert "100 palavras" in instrucao_da_aula(1)


def test_sem_secao_nada_muda(regras_trocadas) -> None:
    """Retrocompatibilidade: sem a seção, nenhum aviso e nenhum texto no prompt."""
    regras_trocadas(lambda v: v.pop("planejamento"))
    assert check_planejamento_curso([_aula(i, 5000) for i in range(1, 40)]) == []
    assert instrucao_do_plano(1) == ""
    assert instrucao_da_aula(1) == ""


def test_so_as_primeiras_aulas_recebem_a_instrucao_de_aula_curta() -> None:
    s = _secao()
    iniciais = s["aulas_iniciais_curtas"]
    primeira = instrucao_da_aula(1)
    depois = instrucao_da_aula(iniciais + 1)
    assert str(s["palavras_max_aulas_iniciais"]) in primeira
    assert str(s["palavras_max_aulas_iniciais"]) not in depois
    assert depois and depois in primeira  # a regra da tese na primeira metade vale para todas


def test_prompt_de_planejamento_recebe_a_ordem(monkeypatch) -> None:
    from src.clients import load_client
    from src.models import Course, Module
    from src.orchestrator import Orchestrator

    enviados: list[str] = []

    class _Cliente:
        def call(self, provider, prompt, **kw):
            enviados.append(prompt)
            return "1. Primeira aula | ideia"

    orq = Orchestrator.__new__(Orchestrator)
    orq.client_context = load_client("default")
    orq.client = _Cliente()
    from src.agents.writer import Writer

    orq.writer = Writer(client=None)
    curso = Course(id="curso-x", titulo="Curso X de teste")
    orq._plan_lessons(curso, Module(titulo="Módulo um", descricao="d"), 1, "pesquisa")
    s = _secao()
    assert f"entre {s['aulas_por_curso'][0]} e {s['aulas_por_curso'][1]} aulas" in enviados[0]


def test_gate_do_curso_emite_categoria_planejamento() -> None:
    from src.validators.quality_gate import QualityGate

    texto = "\n\n".join(b for _, b in [_aula(i, 50) for i in range(1, 4)])
    achados = QualityGate.check_curso(texto, "curso", client=None)
    assert any(a.categoria == "planejamento" and a.tipo == "warning" for a in achados)
