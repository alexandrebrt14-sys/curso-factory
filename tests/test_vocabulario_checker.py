"""27/09/2026: palavras de uso exagerado, com limite por aula lido do YAML."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest
import yaml

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.validators import rules_loader  # noqa: E402
from src.validators.content_checker import check_content  # noqa: E402
from src.validators.vocabulario_checker import (  # noqa: E402
    carregar_config,
    check_vocabulario,
    contar,
    instrucao_para_prompt,
)

REGRAS = PROJECT_ROOT / "config" / "quality_rules.yaml"


@pytest.fixture
def regras_trocadas(tmp_path, monkeypatch):
    """Grava uma cópia do YAML com a seção alterada e aponta o loader para ela."""

    def _trocar(alterar) -> None:
        dados = yaml.safe_load(REGRAS.read_text(encoding="utf-8"))
        alterar(dados["validation"])
        destino = tmp_path / "quality_rules.yaml"
        destino.write_text(yaml.safe_dump(dados, allow_unicode=True), encoding="utf-8")
        monkeypatch.setattr(rules_loader, "RULES_PATH", destino)
        rules_loader.load_rules.cache_clear()

    yield _trocar
    rules_loader.load_rules.cache_clear()


def _achados(texto: str) -> list:
    return check_vocabulario(texto).achados


def test_uma_ocorrencia_por_familia_passa() -> None:
    texto = "A régua do salão mede o corte. O fecho travou uma vez e a dona foi honesta."
    assert _achados(texto) == []


def test_primeira_ocorrencia_alem_do_limite_e_aviso() -> None:
    texto = "A régua mede o corte. Outra régua mede a franja."
    achados = _achados(texto)
    assert [a.tipo for a in achados] == ["warning"]
    assert "regua" in achados[0].regra


def test_tres_alem_do_limite_e_erro() -> None:
    texto = " ".join(["O sistema travou de novo."] * 4)
    achados = _achados(texto)
    assert [a.tipo for a in achados] == ["error"]
    assert "parar" in achados[0].mensagem


def test_variacoes_contam_na_mesma_familia() -> None:
    config = carregar_config()
    texto = (
        "Travar, trava, travado e travando. Canônico e canônicas. Honestamente, com honestidade."
    )
    contagem = contar(texto, config)
    assert contagem["travar"] == 4
    assert contagem["canonico"] == 2
    assert contagem["honesto"] == 2


def test_codigo_arquivo_chave_link_e_mencao_ficam_fora() -> None:
    texto = (
        'Troque "régua" por critério.\n\n'
        "O arquivo regua.py e a chave `tetos.regua` ficam iguais, assim como validation.regua_max.\n\n"
        "Leia o [guia de medidas](/educacao/regua-de-precos).\n\n"
        "```python\nregua = 1\nregua = 2\n```\n"
    )
    assert contar(texto, carregar_config())["regua"] == 0


def test_limite_vem_do_yaml(regras_trocadas) -> None:
    """Com limite 0 no YAML, uma ocorrência só já vira aviso: o número não mora no código."""

    def limite_zero(v):
        v["palavras_de_uso_exagerado"]["limite_por_aula"] = 0

    regras_trocadas(limite_zero)
    achados = check_vocabulario("A régua mede o corte.").achados
    assert [a.tipo for a in achados] == ["warning"]


def test_familia_nova_no_yaml_passa_a_ser_contada(regras_trocadas) -> None:
    def acrescenta(v):
        v["palavras_de_uso_exagerado"]["familias"]["alavancar"] = {
            "formas": ["alavancar", "alavanca"],
            "trocas": ["aumentar"],
        }

    regras_trocadas(acrescenta)
    achados = check_vocabulario("Alavancar vendas. Alavanca o caixa.").achados
    assert any("alavancar" in a.regra for a in achados)


def test_sem_secao_nada_e_cobrado_nem_instruido(regras_trocadas) -> None:
    """Retrocompatibilidade: sem a seção, o checador e o prompt ficam como antes."""
    regras_trocadas(lambda v: v.pop("palavras_de_uso_exagerado"))
    texto = " ".join(["A régua mede."] * 6)
    assert check_vocabulario(texto).achados == []
    assert instrucao_para_prompt() == ""
    categorias = {e.categoria for e in check_content(texto, "aula")}
    assert "vocabulario" not in categorias


def test_secao_desligada_nao_cobra(regras_trocadas) -> None:
    regras_trocadas(lambda v: v["palavras_de_uso_exagerado"].update(enabled=False))
    assert check_vocabulario(" ".join(["A régua mede."] * 6)).achados == []


def test_check_content_emite_categoria_vocabulario() -> None:
    texto = " ".join(["O pedido travou no caixa."] * 5)
    erros = [e for e in check_content(texto, "aula") if e.categoria == "vocabulario"]
    assert erros and erros[0].tipo == "error"


def test_instrucao_do_prompt_sai_do_yaml() -> None:
    bloco = instrucao_para_prompt()
    config = carregar_config()
    assert str(config.limite_por_aula) in bloco
    for familia in config.familias:
        assert familia.rotulo in bloco
    assert "{familias}" not in bloco and "{limite}" not in bloco


def test_prompt_de_redacao_e_revisao_recebem_o_bloco() -> None:
    from src.agents.reviewer import Reviewer
    from src.agents.writer import Writer
    from src.orchestrator import Orchestrator

    blocos = Orchestrator._blocos_de_instrucao()
    assert blocos["bloco_vocabulario"]
    for agente in (Writer(client=None), Reviewer(client=None)):
        prompt = agente.build_prompt("pesquisa", **blocos)
        assert blocos["bloco_vocabulario"] in prompt
        assert "{bloco_vocabulario}" not in prompt
