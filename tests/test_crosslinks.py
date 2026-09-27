"""27/09/2026: crosslinks por aula, opt-in por cliente, conferidos contra o catálogo."""

from __future__ import annotations

import json
import sys
from dataclasses import replace
from pathlib import Path

import pytest
import yaml

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.clients import load_client  # noqa: E402
from src.clients import loader as client_loader  # noqa: E402
from src.clients.context import CrosslinksConfig  # noqa: E402
from src.validators import rules_loader  # noqa: E402
from src.validators.content_checker import check_content  # noqa: E402
from src.validators.crosslink_checker import (  # noqa: E402
    check_crosslinks_aula,
    check_crosslinks_curso,
    instrucao_para_prompt,
)
from src.validators.quality_gate import QualityGate  # noqa: E402

CATALOGO = PROJECT_ROOT / "config" / "clients" / "default" / "crosslinks_catalogo.json"
DESTINOS = [d["caminho"] for d in json.loads(CATALOGO.read_text(encoding="utf-8"))["destinos"]]
REGRAS = PROJECT_ROOT / "config" / "quality_rules.yaml"


def _config(**extra) -> CrosslinksConfig:
    base = CrosslinksConfig(
        enabled=True,
        min_por_aula=2,
        max_por_aula=4,
        min_destinos_distintos_no_curso=3,
        prefixos_validos=["/educacao/"],
        catalogo=CATALOGO,
    )
    return replace(base, **extra)


def _aula(links: list[tuple[str, str]], titulo: str = "Aula 1.1: Montar a agenda") -> str:
    prosa = " ".join(
        f'O curso "{ancora}" mostra o passo que esta aula não cobre, em [{ancora}]({caminho}).'
        for ancora, caminho in links
    )
    return (
        f"# {titulo}\n\nMonte a agenda do salão sem perder horário.\n\n"
        "A agenda cheia some quando ninguém confirma o horário na véspera.\n\n"
        "Quem confirma na véspera perde menos clientes e sabe quem vem.\n\n"
        "O custo aparece no fim do mês, quando a cadeira ficou vazia.\n\n"
        f"## Por que confirmar muda o caixa\n\n{prosa}\n"
    )


def _regras(achados) -> list[str]:
    return [a.regra for a in achados]


def test_duas_rotas_do_catalogo_passam() -> None:
    texto = _aula([("Setup", DESTINOS[0]), ("IA local", DESTINOS[1])])
    assert check_crosslinks_aula(texto, _config()) == []


def test_abaixo_do_piso_e_erro() -> None:
    achados = check_crosslinks_aula(_aula([("Setup", DESTINOS[0])]), _config())
    assert _regras(achados) == ["crosslink-piso"]
    assert achados[0].tipo == "error"


def test_piso_vem_da_configuracao_do_cliente() -> None:
    texto = _aula([("Setup", DESTINOS[0]), ("IA local", DESTINOS[1])])
    assert check_crosslinks_aula(texto, _config(min_por_aula=3))
    assert check_crosslinks_aula(texto, _config(min_por_aula=2)) == []


def test_acima_do_teto_e_aviso() -> None:
    links = [(f"Curso {i}", DESTINOS[i]) for i in range(5)]
    achados = check_crosslinks_aula(_aula(links), _config())
    assert _regras(achados) == ["crosslink-teto"]
    assert achados[0].tipo == "warning"


def test_rota_imaginada_reprova() -> None:
    texto = _aula([("Setup", DESTINOS[0]), ("Inventado", "/educacao/curso-que-nao-existe")])
    regras = _regras(check_crosslinks_aula(texto, _config()))
    assert "crosslink-destino" in regras and "crosslink-piso" in regras


@pytest.mark.parametrize("ancora", ["clique aqui", "Saiba mais.", "aqui", "neste link"])
def test_ancora_generica_reprova(ancora: str) -> None:
    texto = _aula([(ancora, DESTINOS[0]), ("IA local", DESTINOS[1])])
    achados = check_crosslinks_aula(texto, _config())
    assert "crosslink-ancora" in _regras(achados)


def test_link_na_abertura_e_aviso() -> None:
    texto = _aula([("Setup", DESTINOS[0]), ("IA local", DESTINOS[1])]).replace(
        "A agenda cheia some", f"A [agenda do curso de setup]({DESTINOS[2]}) cheia some"
    )
    assert "crosslink-abertura" in _regras(check_crosslinks_aula(texto, _config()))


def test_link_em_codigo_e_imagem_nao_contam() -> None:
    texto = _aula([]) + f"\n```\n[a]({DESTINOS[0]})\n```\n\n![figura]({DESTINOS[1]})\n"
    assert _regras(check_crosslinks_aula(texto, _config())) == ["crosslink-piso"]


def test_mesmo_destino_em_aulas_seguidas_reprova() -> None:
    a1 = _aula([("Setup", DESTINOS[0]), ("IA local", DESTINOS[1])], "Aula 1.1: A")
    a2 = _aula([("Setup", DESTINOS[0]), ("Outro", DESTINOS[2])], "Aula 1.2: B")
    achados = check_crosslinks_curso([("Aula 1.1: A", a1), ("Aula 1.2: B", a2)], _config())
    assert "crosslink-sequencia" in _regras(achados)


def test_piso_de_destinos_do_curso() -> None:
    a1 = _aula([("Setup", DESTINOS[0]), ("IA local", DESTINOS[1])], "Aula 1.1: A")
    a2 = _aula([("Outro", DESTINOS[2]), ("Mais um", DESTINOS[3])], "Aula 1.2: B")
    aulas = [("Aula 1.1: A", a1), ("Aula 1.2: B", a2)]
    assert check_crosslinks_curso(aulas, _config(min_destinos_distintos_no_curso=4)) == []
    assert _regras(check_crosslinks_curso(aulas, _config(min_destinos_distintos_no_curso=5))) == [
        "crosslink-curso"
    ]


def test_desligado_nao_cobra_nem_instrui() -> None:
    """Retrocompatibilidade: bloco ausente ou desligado mantém o comportamento anterior."""
    texto = _aula([])
    assert check_crosslinks_aula(texto, CrosslinksConfig()) == []
    assert check_crosslinks_aula(texto, None) == []
    assert instrucao_para_prompt(CrosslinksConfig()) == ""
    assert "crosslinks" not in {e.categoria for e in check_content(texto, "aula")}


def test_ancoras_genericas_vem_do_yaml(tmp_path, monkeypatch) -> None:
    dados = yaml.safe_load(REGRAS.read_text(encoding="utf-8"))
    dados["validation"]["crosslinks"]["ancoras_genericas"].append("confira")
    destino = tmp_path / "quality_rules.yaml"
    destino.write_text(yaml.safe_dump(dados, allow_unicode=True), encoding="utf-8")
    texto = _aula([("confira", DESTINOS[0]), ("IA local", DESTINOS[1])])
    assert check_crosslinks_aula(texto, _config()) == []
    monkeypatch.setattr(rules_loader, "RULES_PATH", destino)
    rules_loader.load_rules.cache_clear()
    try:
        assert "crosslink-ancora" in _regras(check_crosslinks_aula(texto, _config()))
    finally:
        rules_loader.load_rules.cache_clear()


def test_cliente_default_liga_com_piso_2_e_teto_4() -> None:
    cfg = load_client("default").crosslinks
    assert cfg.enabled and cfg.min_por_aula == 2 and cfg.max_por_aula == 4
    assert cfg.catalogo is not None and Path(cfg.catalogo).is_file()


def test_cliente_sem_bloco_fica_desligado(tmp_path, monkeypatch) -> None:
    origem = PROJECT_ROOT / "config" / "clients" / "default" / "client.yaml"
    dados = yaml.safe_load(origem.read_text(encoding="utf-8"))
    dados.pop("crosslinks")
    (tmp_path / "semlinks").mkdir()
    (tmp_path / "semlinks" / "client.yaml").write_text(
        yaml.safe_dump(dados, allow_unicode=True), encoding="utf-8"
    )
    monkeypatch.setattr(client_loader, "_CLIENTS_DIR", tmp_path)
    assert load_client("semlinks").crosslinks.enabled is False


def test_template_documenta_e_deixa_desligado() -> None:
    template = PROJECT_ROOT / "config" / "clients" / "_template" / "client.yaml"
    dados = yaml.safe_load(template.read_text(encoding="utf-8"))
    assert "crosslinks" not in dados  # comentado: desligado por padrão
    assert "# crosslinks:" in template.read_text(encoding="utf-8")


def test_quality_gate_mede_aula_e_sequencia_com_o_cliente() -> None:
    gate = QualityGate(client=load_client("default"), auto_fix=False)
    a1 = _aula([("Setup", DESTINOS[0])], "Aula 1.1: A")
    a2 = _aula([("Setup", DESTINOS[0]), ("Outro", DESTINOS[2])], "Aula 1.2: B")
    r = gate.check_text(a1 + "\n\n" + a2, unidade="aula", geo=False)
    texto = "\n".join(r.erros)
    assert "crosslink-piso" in texto and "crosslink-sequencia" in texto


def test_instrucao_do_prompt_lista_destinos_e_exclui_o_proprio_curso() -> None:
    cfg = _config()
    proprio = DESTINOS[0].rsplit("/", 1)[-1]
    bloco = instrucao_para_prompt(cfg, tags=["IA"], excluir=proprio, anteriores={DESTINOS[1]})
    assert "de 2 a 4" in bloco
    assert f"{DESTINOS[0]}:" not in bloco
    assert DESTINOS[1] in bloco  # citado como destino da aula anterior
    assert "{destinos}" not in bloco and "{min}" not in bloco


def test_prompt_de_redacao_traz_o_lugar_do_bloco() -> None:
    prompts = PROJECT_ROOT / "src" / "templates" / "prompts"
    for pasta in (prompts, prompts / "pt-br"):
        assert "{bloco_crosslinks}" in (pasta / "draft.md").read_text(encoding="utf-8")
