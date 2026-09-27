"""27/09/2026: peso visual por aula declarado pelo cliente ou pelo curso."""

from __future__ import annotations

import sys
from pathlib import Path

import yaml

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.clients import load_client  # noqa: E402
from src.clients import loader as client_loader  # noqa: E402
from src.clients.context import VisualConfig  # noqa: E402
from src.models import Course  # noqa: E402
from src.validators import rules_loader  # noqa: E402
from src.validators.content_checker import check_content  # noqa: E402
from src.validators.peso_visual_aula import (  # noqa: E402
    check_peso_visual_aula,
    instrucao_para_prompt,
    medir,
)

PARAGRAFO = (
    "A agenda do salão enche na sexta e esvazia na terça, e a dona só percebe no fim do mês, "
    "quando soma as cadeiras vazias e vê quanto deixou de faturar."
)
TABELA = (
    "| Critério | Agenda de papel | Agenda no celular |\n|---|---|---|\n| Lembrete | não | sim |\n"
)
PASSOS = (
    "Siga os passos para confirmar a agenda:\n\n"
    "1. Abra a agenda da semana.\n2. Marque quem não confirmou.\n3. Envie o lembrete na véspera.\n"
)
FIGURA = "![A agenda confirmada na véspera perde menos horários](agenda.svg)\n"


def _aula(*blocos: str) -> str:
    corpo = "\n\n".join(blocos)
    return f"# Aula 1.1: Confirmar a agenda\n\nConfirme a agenda sem perder horário.\n\n{corpo}\n"


def test_conta_pecas_tipos_e_ritmo_como_o_parser_emite() -> None:
    m = medir(_aula(PARAGRAFO, TABELA, PARAGRAFO, PASSOS, PARAGRAFO, FIGURA))
    assert m.pecas == 3
    assert m.tipos == {"dataTable", "stepGuide", "figure"}
    assert m.maior_sequencia_de_paragrafos == 1


def test_abaixo_do_piso_e_erro() -> None:
    cfg = VisualConfig(min_por_aula=5, max_por_aula=7, min_tipos_por_aula=3)
    achados = check_peso_visual_aula(_aula(PARAGRAFO, TABELA, PARAGRAFO), cfg)
    regras = {a.regra: a.tipo for a in achados}
    assert regras["visual-piso"] == "error"
    assert regras["visual-tipos"] == "warning"


def test_sequencia_longa_de_paragrafos_e_aviso() -> None:
    cfg = VisualConfig(max_paragrafos_sem_peca=3)
    texto = _aula(PARAGRAFO, PARAGRAFO, PARAGRAFO, PARAGRAFO, TABELA)
    assert [a.regra for a in check_peso_visual_aula(texto, cfg)] == ["visual-ritmo"]
    assert check_peso_visual_aula(_aula(PARAGRAFO, PARAGRAFO, TABELA, PARAGRAFO), cfg) == []


def test_acima_do_teto_declarado_e_aviso() -> None:
    cfg = VisualConfig(max_por_aula=2)
    achados = check_peso_visual_aula(_aula(PARAGRAFO, TABELA, PASSOS, FIGURA), cfg)
    assert [(a.regra, a.tipo) for a in achados] == [("visual-teto", "warning")]


def test_sem_declaracao_vale_o_teto_do_espelho() -> None:
    """Retrocompatibilidade: sem bloco `visual`, o aviso antigo de teto continua igual."""
    muitas = _aula(PARAGRAFO, TABELA, TABELA, TABELA, TABELA, FIGURA)
    antigos = [e for e in check_content(muitas, "aula") if "apoios visuais" in e.mensagem]
    assert antigos and antigos[0].tipo == "warning"
    assert check_peso_visual_aula(muitas, VisualConfig()) == []
    assert instrucao_para_prompt(VisualConfig()) == ""


def test_declarado_troca_o_teto_do_espelho_pela_regra_do_curso() -> None:
    muitas = _aula(PARAGRAFO, TABELA, TABELA, TABELA, TABELA, FIGURA)
    cfg = VisualConfig(min_por_aula=5, max_por_aula=7)
    erros = check_content(muitas, "aula", visual_config=cfg)
    assert not [e for e in erros if "apoios visuais" in e.mensagem]
    assert not [e for e in erros if e.categoria == "peso visual"]
    poucas = check_content(_aula(PARAGRAFO, TABELA), "aula", visual_config=cfg)
    assert any(e.categoria == "peso visual" and e.tipo == "error" for e in poucas)


def test_curso_sobrepoe_o_cliente_campo_a_campo() -> None:
    cliente = VisualConfig(min_por_aula=1, max_por_aula=3)
    curso = VisualConfig.de_dict({"min_por_aula": 5, "min_tipos_por_aula": 3})
    final = cliente.sobreposto_por(curso)
    assert (final.min_por_aula, final.max_por_aula, final.min_tipos_por_aula) == (5, 3, 3)
    assert cliente.sobreposto_por(None) is cliente


def test_bloco_do_client_yaml_e_lido(tmp_path, monkeypatch) -> None:
    origem = PROJECT_ROOT / "config" / "clients" / "default" / "client.yaml"
    dados = yaml.safe_load(origem.read_text(encoding="utf-8"))
    assert not load_client("default").visual.declarado
    dados["visual"] = {"min_por_aula": 5, "max_por_aula": 7, "max_paragrafos_sem_peca": 3}
    (tmp_path / "visual").mkdir()
    (tmp_path / "visual" / "client.yaml").write_text(
        yaml.safe_dump(dados, allow_unicode=True), encoding="utf-8"
    )
    monkeypatch.setattr(client_loader, "_CLIENTS_DIR", tmp_path)
    cfg = load_client("visual").visual
    assert (cfg.min_por_aula, cfg.max_por_aula, cfg.max_paragrafos_sem_peca) == (5, 7, 3)
    assert cfg.min_tipos_por_aula is None


def test_curso_declara_visual_e_o_redator_recebe(tmp_path, monkeypatch) -> None:
    from src.orchestrator import Orchestrator

    orq = Orchestrator.__new__(Orchestrator)
    orq.client_context = load_client("default")
    sem = Course(id="curso-x", titulo="Curso X de teste")
    assert Orchestrator._variaveis_de_peso_visual(orq, sem) == {"bloco_peso_visual": ""}
    com = Course(
        id="curso-x", titulo="Curso X de teste", visual={"min_por_aula": 5, "max_por_aula": 7}
    )
    variaveis = Orchestrator._variaveis_de_peso_visual(orq, com)
    assert variaveis["figuras_max"] == "7"
    assert "de 5 a 7" in variaveis["bloco_peso_visual"]


def test_instrucao_do_prompt_vem_do_yaml(tmp_path, monkeypatch) -> None:
    regras = PROJECT_ROOT / "config" / "quality_rules.yaml"
    dados = yaml.safe_load(regras.read_text(encoding="utf-8"))
    dados["validation"]["peso_visual"]["instrucao_prompt"] = "Piso {min}, teto {max}."
    destino = tmp_path / "quality_rules.yaml"
    destino.write_text(yaml.safe_dump(dados, allow_unicode=True), encoding="utf-8")
    monkeypatch.setattr(rules_loader, "RULES_PATH", destino)
    rules_loader.load_rules.cache_clear()
    try:
        assert (
            instrucao_para_prompt(VisualConfig(min_por_aula=5, max_por_aula=7)) == "Piso 5, teto 7."
        )
    finally:
        rules_loader.load_rules.cache_clear()


def test_courses_yaml_leva_o_bloco_ate_o_curso() -> None:
    sys.path.insert(0, str(PROJECT_ROOT))
    from cli import _course_config_from_yaml

    cfg = _course_config_from_yaml({"nivel": "iniciante", "visual": {"min_por_aula": 5}})
    assert cfg["visual"] == {"min_por_aula": 5}
    assert _course_config_from_yaml({"nivel": "iniciante"})["visual"] is None


def test_prompt_de_redacao_traz_o_lugar_do_bloco() -> None:
    prompts = PROJECT_ROOT / "src" / "templates" / "prompts"
    for pasta in (prompts, prompts / "pt-br"):
        assert "{bloco_peso_visual}" in (pasta / "draft.md").read_text(encoding="utf-8")
