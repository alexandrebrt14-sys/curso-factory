"""27/09/2026: tabela de proveniência como entrega de bastidor, fora da página."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest
import yaml

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.validators import rules_loader  # noqa: E402
from src.validators.proveniencia import (  # noqa: E402
    frases_para_conferencia,
    tabela_de_proveniencia,
)

REGRAS = PROJECT_ROOT / "config" / "quality_rules.yaml"

AULA = """# Aula 1.1: Escolher o computador

Escolha o computador sem pagar duas vezes.

O Mac Mini M4 custa R$ 7.999 desde março de 2026. Suponha uma pousada com 8 quartos.
O Ollama 0.12 roda modelos locais. A dona decide olhando o caixa do mês.

```bash
ollama run modelo:7b
```

| Opção | Preço |
|---|---|
| Mac Mini | R$ 7.999 |

Leia "[IA Local na Prática](/educacao/orquestracao-llm-local-desktop)" para instalar.
"""


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


def test_extrai_frases_com_numero_data_versao_e_produto() -> None:
    frases = {f.frase: f for f in frases_para_conferencia(AULA)}
    preco = frases["O Mac Mini M4 custa R$ 7.999 desde março de 2026."]
    assert {"numero", "data", "produto"} <= set(preco.tipos)
    assert "versao" not in preco.tipos  # separador de milhar não é versão
    assert "versao" in frases["O Ollama 0.12 roda modelos locais."].tipos
    assert "A dona decide olhando o caixa do mês." not in frases


def test_exemplo_rotulado_dispensa_fonte() -> None:
    frases = {f.frase: f for f in frases_para_conferencia(AULA)}
    assert frases["Suponha uma pousada com 8 quartos."].exemplo is True
    assert "exemplo rotulado" in tabela_de_proveniencia(AULA)


def test_codigo_fica_fora_e_celula_de_tabela_entra() -> None:
    frases = [f.frase for f in frases_para_conferencia(AULA)]
    assert not any("ollama run" in f for f in frases)
    assert any(f.startswith("Mac Mini") and "R$ 7.999" in f for f in frases)


def test_tabela_traz_colunas_de_fonte_e_os_crosslinks() -> None:
    tabela = tabela_de_proveniencia(AULA)
    assert (
        "| Frase da aula | Tipo | URL primária | Data de publicação | Trecho lido | Data de acesso |"
        in tabela
    )
    assert "## Aula 1.1: Escolher o computador" in tabela
    assert "/educacao/orquestracao-llm-local-desktop" in tabela


def test_padroes_vem_do_yaml(regras_trocadas) -> None:
    regras_trocadas(lambda v: v["proveniencia"]["padroes"].update(marca="\\bcaixa\\b"))
    frases = {f.frase: f for f in frases_para_conferencia(AULA)}
    assert frases["A dona decide olhando o caixa do mês."].tipos == ["marca"]


def test_sem_secao_nada_e_extraido(regras_trocadas) -> None:
    regras_trocadas(lambda v: v.pop("proveniencia"))
    assert frases_para_conferencia(AULA) == []
    assert tabela_de_proveniencia(AULA) == ""


def test_cli_grava_a_tabela(tmp_path) -> None:
    import argparse

    from cli import cmd_proveniencia

    origem = tmp_path / "aula.md"
    origem.write_text(AULA, encoding="utf-8")
    saida = tmp_path / "tabela.md"
    assert cmd_proveniencia(argparse.Namespace(path=str(origem), saida=str(saida))) == 0
    assert "Frase da aula" in saida.read_text(encoding="utf-8")


def test_orquestrador_grava_a_tabela_sem_mudar_o_texto() -> None:
    from src.orchestrator import Orchestrator, PipelineResult

    resultado = PipelineResult("curso-x")
    resultado.etapas["review"] = AULA
    Orchestrator._registrar_proveniencia(None, resultado)
    assert resultado.etapas["review"] == AULA
    assert "Frase da aula" in resultado.etapas["proveniencia"]
