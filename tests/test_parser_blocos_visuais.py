"""Testes da promoção de Markdown a bloco visual no parser.

O que se cobra aqui: a tabela vira `dataTable`, a lista de procedimento vira
`stepGuide` e a imagem legendada vira `figure`. Acima de tudo, nada se perde
no caminho. Tabela torta, imagem sem legenda e lista que não é procedimento
precisam sobreviver como texto em vez de derrubar a geração.
"""

from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.models import SectionType
from src.parsers import parse_module_to_sections

# ─── Auxiliares ──────────────────────────────────────────────────────

MD_TABELA = (
    "Prosa antes da tabela, que precisa sobreviver inteira.\n"
    "\n"
    "| Critério | Opção A | Opção B |\n"
    "|---|:---:|---|\n"
    "| Custo | Alto | Baixo |\n"
    "| Prazo | Curto | Longo |\n"
    "\n"
    "Prosa depois da tabela, que também precisa sobreviver.\n"
)


def _tipos(secoes) -> list[str]:
    return [s.type.value for s in secoes]


# ─── Tabela → dataTable ──────────────────────────────────────────────

def test_tabela_vira_data_table_entre_duas_prosas() -> None:
    secoes = parse_module_to_sections(MD_TABELA, add_checkpoint_if_missing=False)
    uteis = [s for s in secoes if s.type in (SectionType.TEXT, SectionType.DATA_TABLE)]

    assert _tipos(uteis) == ["text", "dataTable", "text"]
    assert "antes da tabela" in uteis[0].value
    assert "depois da tabela" in uteis[2].value

    tabela = uteis[1]
    assert tabela.value == ""
    assert tabela.data["columns"] == ["Critério", "Opção A", "Opção B"]
    assert tabela.data["rows"] == [
        ["Custo", "Alto", "Baixo"],
        ["Prazo", "Curto", "Longo"],
    ]


def test_tabela_absorve_titulo_em_negrito_e_fonte() -> None:
    md = (
        "**Comparativo de custo mensal**\n"
        "| Plano | Preço |\n"
        "|---|---|\n"
        "| Básico | R$ 90 |\n"
        "| Pleno | R$ 240 |\n"
        "Fonte: tabela pública de preços, agosto de 2026.\n"
    )
    secoes = parse_module_to_sections(md, add_checkpoint_if_missing=False)
    tabelas = [s for s in secoes if s.type == SectionType.DATA_TABLE]

    assert len(tabelas) == 1
    assert tabelas[0].data["title"] == "Comparativo de custo mensal"
    assert "agosto de 2026" in tabelas[0].data["source"]
    # O título em negrito foi consumido pela tabela, não sobrou como prosa.
    textos = " ".join(s.value for s in secoes if s.type == SectionType.TEXT)
    assert "Comparativo de custo mensal" not in textos


def test_tabela_com_celula_vazia_e_aceita() -> None:
    md = (
        "| Item | Nota |\n"
        "|---|---|\n"
        "| Alfa |  |\n"
        "| Beta | Boa |\n"
    )
    secoes = parse_module_to_sections(md, add_checkpoint_if_missing=False)
    tabelas = [s for s in secoes if s.type == SectionType.DATA_TABLE]
    assert len(tabelas) == 1
    assert tabelas[0].data["rows"][0] == ["Alfa", ""]


def test_tabela_torta_nao_derruba_e_nao_perde_conteudo() -> None:
    """Linha curta e linha longa: o parser normaliza sem descartar célula."""
    md = (
        "Introdução.\n"
        "\n"
        "| Critério | Opção A | Opção B |\n"
        "|---|---|---|\n"
        "| Custo | Alto |\n"
        "| Prazo | Curto | Longo | Extra |\n"
        "\n"
        "Fecho.\n"
    )
    secoes = parse_module_to_sections(md, add_checkpoint_if_missing=False)
    tabelas = [s for s in secoes if s.type == SectionType.DATA_TABLE]

    assert len(tabelas) == 1
    rows = tabelas[0].data["rows"]
    assert rows[0] == ["Custo", "Alto", ""]
    assert rows[1] == ["Prazo", "Curto", "Longo Extra"]

    tudo = " ".join(s.value for s in secoes) + repr(tabelas[0].data)
    assert "Introdução" in tudo
    assert "Fecho" in tudo
    assert "Extra" in tudo


def test_tabela_de_coluna_unica_continua_texto() -> None:
    md = "Lista simples.\n\n| Item |\n|---|\n| Alfa |\n"
    secoes = parse_module_to_sections(md, add_checkpoint_if_missing=False)
    assert SectionType.DATA_TABLE not in [s.type for s in secoes]
    textos = " ".join(s.value for s in secoes if s.type == SectionType.TEXT)
    assert "Alfa" in textos


# ─── CRLF ────────────────────────────────────────────────────────────

def test_crlf_produz_o_mesmo_resultado_que_lf() -> None:
    lf = parse_module_to_sections(MD_TABELA, add_checkpoint_if_missing=False)
    crlf = parse_module_to_sections(
        MD_TABELA.replace("\n", "\r\n"), add_checkpoint_if_missing=False
    )
    assert [s.model_dump() for s in lf] == [s.model_dump() for s in crlf]


def test_crlf_preserva_code_fence_e_tabela_juntos() -> None:
    md = (
        "Texto.\r\n"
        "\r\n"
        "```python\r\n"
        "x = 42\r\n"
        "```\r\n"
        "\r\n"
        "| A | B |\r\n"
        "|---|---|\r\n"
        "| 1 | 2 |\r\n"
    )
    secoes = parse_module_to_sections(md, add_checkpoint_if_missing=False)
    tipos = _tipos(secoes)
    assert "code" in tipos
    assert "dataTable" in tipos
    assert tipos.index("code") < tipos.index("dataTable")


# ─── Imagem → figure ─────────────────────────────────────────────────

def test_imagem_com_legenda_vira_figure() -> None:
    md = (
        "Antes da figura.\n"
        "\n"
        "![Fluxo de aprovação do artigo](/imagens/fluxo-aprovacao.png)\n"
        "\n"
        "Depois da figura.\n"
    )
    secoes = parse_module_to_sections(md, add_checkpoint_if_missing=False)
    figuras = [s for s in secoes if s.type == SectionType.FIGURE]

    assert len(figuras) == 1
    assert figuras[0].value == "/imagens/fluxo-aprovacao.png"
    assert figuras[0].label == "Fluxo de aprovação do artigo"
    assert _tipos(secoes)[:3] == ["text", "figure", "text"]


def test_imagem_sem_legenda_continua_no_texto() -> None:
    md = "Antes.\n\n![](/imagens/sem-legenda.png)\n\nDepois.\n"
    secoes = parse_module_to_sections(md, add_checkpoint_if_missing=False)

    assert SectionType.FIGURE not in [s.type for s in secoes]
    textos = " ".join(s.value for s in secoes if s.type == SectionType.TEXT)
    assert "/imagens/sem-legenda.png" in textos


# ─── Lista numerada → stepGuide ──────────────────────────────────────

def test_lista_de_procedimento_vira_step_guide() -> None:
    md = (
        "### Passo a passo para publicar o curso\n"
        "\n"
        "1. **Gere o rascunho**: rode o comando de geração no repositório.\n"
        "2. **Revise a acentuação**: confira o relatório do validador.\n"
        "3. **Publique**: abra o pull request e aguarde o portão.\n"
        "\n"
        "Depois disso, acompanhe a fila.\n"
    )
    secoes = parse_module_to_sections(md, add_checkpoint_if_missing=False)
    guias = [s for s in secoes if s.type == SectionType.STEP_GUIDE]

    assert len(guias) == 1
    guia = guias[0]
    assert guia.value == ""
    assert guia.data["title"] == "Passo a passo para publicar o curso"
    assert [p["label"] for p in guia.data["steps"]] == [
        "Gere o rascunho",
        "Revise a acentuação",
        "Publique",
    ]
    assert "comando de geração" in guia.data["steps"][0]["detail"]
    # A prosa posterior sobrevive.
    textos = " ".join(s.value for s in secoes if s.type == SectionType.TEXT)
    assert "acompanhe a fila" in textos


def test_lista_de_procedimento_com_intro_em_dois_pontos() -> None:
    md = (
        "Siga estas etapas para configurar o ambiente:\n"
        "\n"
        "1. Instale as dependências do projeto.\n"
        "2. Copie o arquivo de exemplo de variáveis.\n"
        "3. Rode a suíte de testes para conferir.\n"
    )
    secoes = parse_module_to_sections(md, add_checkpoint_if_missing=False)
    guias = [s for s in secoes if s.type == SectionType.STEP_GUIDE]
    assert len(guias) == 1
    assert guias[0].data["title"] == "Siga estas etapas para configurar o ambiente"
    assert len(guias[0].data["steps"]) == 3


def test_lista_numerada_sem_sinal_de_procedimento_continua_texto() -> None:
    """Enumeração de argumentos não é passo a passo. Na dúvida, não promove."""
    md = (
        "O mercado mudou em três frentes.\n"
        "\n"
        "1. A busca deixou de ser dez links azuis.\n"
        "2. O tráfego de referência caiu.\n"
        "3. A marca virou critério de citação.\n"
    )
    secoes = parse_module_to_sections(md, add_checkpoint_if_missing=False)

    assert SectionType.STEP_GUIDE not in [s.type for s in secoes]
    textos = " ".join(s.value for s in secoes if s.type == SectionType.TEXT)
    assert "dez links azuis" in textos
    assert "critério de citação" in textos


def test_lista_de_dois_itens_nao_vira_step_guide() -> None:
    md = (
        "Passo a passo mínimo:\n"
        "\n"
        "1. Abra o painel de controle.\n"
        "2. Salve a configuração.\n"
    )
    secoes = parse_module_to_sections(md, add_checkpoint_if_missing=False)
    assert SectionType.STEP_GUIDE not in [s.type for s in secoes]
    textos = " ".join(s.value for s in secoes if s.type == SectionType.TEXT)
    assert "Abra o painel de controle" in textos


def test_lista_numerada_sem_introducao_nenhuma_continua_texto() -> None:
    md = (
        "1. Abra o painel de controle.\n"
        "2. Ajuste o limite de requisições.\n"
        "3. Salve a configuração.\n"
    )
    secoes = parse_module_to_sections(md, add_checkpoint_if_missing=False)
    assert SectionType.STEP_GUIDE not in [s.type for s in secoes]
    textos = " ".join(s.value for s in secoes if s.type == SectionType.TEXT)
    assert "limite de requisições" in textos


# ─── Convivência com o comportamento existente ───────────────────────

def test_checkpoint_sintetico_continua_sendo_acrescentado() -> None:
    secoes = parse_module_to_sections(MD_TABELA)
    assert any(s.type == SectionType.CHECKPOINT for s in secoes)
    assert len(secoes) >= 3


def test_bloco_visual_convive_com_blockquote_especial() -> None:
    md = (
        "Abertura.\n"
        "\n"
        "| A | B |\n"
        "|---|---|\n"
        "| 1 | 2 |\n"
        "\n"
        "> DICA: confira a fonte antes de citar.\n"
    )
    secoes = parse_module_to_sections(md, add_checkpoint_if_missing=False)
    tipos = _tipos(secoes)
    assert "dataTable" in tipos
    assert "tip" in tipos
