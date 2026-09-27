"""27/09/2026: a aula não narra a própria apuração; padrões lidos do YAML."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest
import yaml

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.validators import rules_loader  # noqa: E402
from src.validators.content_checker import (  # noqa: E402
    _check_bastidor,
    check_content,
    instrucao_de_apuracao,
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


@pytest.mark.parametrize(
    "frase",
    [
        "O preço de R$ 49 foi confirmado na fonte primária antes de entrar aqui.",
        "Verificamos o número com o fornecedor.",
        "O prazo foi conferido em 27 de setembro.",
        "Não há fonte para o dado de 2024, então ele ficou de fora.",
        "Descartamos por falta de certeza o número do segundo trimestre.",
        "Não foi possível verificar a data de lançamento.",
        "O placar não pôde ser checado.",
        "Segundo o que apuramos, o plano custa R$ 20.",
    ],
)
def test_frase_que_narra_a_apuracao_e_bastidor(frase: str) -> None:
    assert _check_bastidor(frase)


def test_mencao_entre_aspas_passa() -> None:
    assert _check_bastidor('Evite escrever "confirmado na fonte primária" na aula.') == []


def test_fato_limpo_passa() -> None:
    assert _check_bastidor("O plano custa R$ 20 por mês e cobre três usuários.") == []


def test_expressao_contida_na_do_lexico_conta_uma_vez() -> None:
    """ "verificamos" (YAML) dentro de "verificamos que" (fonte) é uma cobrança só."""
    achados = _check_bastidor("Verificamos que o prazo é de dez dias.")
    assert len(achados) == 1


def test_check_content_reprova_como_bastidor() -> None:
    erros = check_content("Verificamos o preço antes de publicar.", "aula")
    assert any(e.tipo == "error" and "Bastidor" in e.mensagem for e in erros)


def test_padrao_novo_no_yaml_passa_a_reprovar(regras_trocadas) -> None:
    frase = "O número foi auditado por nós na planilha."
    assert _check_bastidor(frase) == []

    regras_trocadas(
        lambda v: v["apuracao_narrada"]["padroes"].append("re:\\bauditad[oa] por n[óo]s\\b")
    )
    assert _check_bastidor(frase)


def test_sem_secao_o_bastidor_fica_como_antes(regras_trocadas) -> None:
    """Retrocompatibilidade: sem a seção, só o léxico da fonte cobra."""
    regras_trocadas(lambda v: v.pop("apuracao_narrada"))
    assert _check_bastidor("O prazo foi conferido em 27 de setembro.") == []
    assert _check_bastidor("Verificamos que o prazo é de dez dias.")  # léxico da fonte
    assert instrucao_de_apuracao() == ""


def test_instrucao_do_prompt_lista_os_literais_do_yaml() -> None:
    bloco = instrucao_de_apuracao()
    dados = yaml.safe_load(REGRAS.read_text(encoding="utf-8"))
    for item in dados["validation"]["apuracao_narrada"]["padroes"]:
        if not item.startswith("re:"):
            assert f'"{item}"' in bloco
    assert "{exemplos}" not in bloco


def test_prompts_pt_br_e_raiz_trazem_o_lugar_do_bloco() -> None:
    prompts = PROJECT_ROOT / "src" / "templates" / "prompts"
    for nome in ("draft.md", "review.md"):
        for pasta in (prompts, prompts / "pt-br"):
            assert "{bloco_apuracao}" in (pasta / nome).read_text(encoding="utf-8")
