"""Abertura direta e sem distração (R1 a R9, 08/09/2026).

Pedido do dono: toda aula começa com título, subtítulo e parágrafos; nada de
"faça agora", "mockup no seu negócio", "checkpoint", "requer verificação" ou
LGPD; fontes só no rodapé, em corpo pequeno. Cada regra é cobrada em duas
superfícies: o Markdown (pelo `content_checker`, e por ele pelo `QualityGate`
e pelo orquestrador) e o `CourseDefinition` montado (pelo `TsxGenerator`, que
recusa publicar). O template também é medido, porque é nele que o topo carregado
morava: rótulo antes do H1, barra de estatísticas, índice lateral, card "o que
você vai aprender" e "Fonte:" dentro de tabela.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.clients import load_client  # noqa: E402
from src.generators.tsx_generator import TsxGenerator  # noqa: E402
from src.models import CourseDefinition  # noqa: E402
from src.parsers import extrair_fontes, extrair_subtitulo, parse_module_to_sections  # noqa: E402
from src.validators.abertura_checker import (  # noqa: E402
    AberturaError,
    check_abertura,
    check_abertura_definicao,
)
from src.validators.content_checker import check_content  # noqa: E402
from src.validators.quality_gate import QualityGate  # noqa: E402

PROSA = " ".join(["palavra"] * 30) + "."

AULA_OK = (
    "# Aula 1.1: Responder em cinco minutos\n\n"
    "Você vai responder o cliente antes que ele desista.\n\n"
    f"{PROSA}\n\n{PROSA}\n\n"
    "## Por que a demora custa a venda\n\n"
    f"{PROSA}\n\n"
    "## Como a oficina do Sérgio parou de perder orçamento\n\n"
    f"{PROSA}\n\n{PROSA}\n"
)


def _regras(texto: str, unidade: str = "aula") -> list[str]:
    return [a.regra for a in check_abertura(texto, unidade).achados]


def _mensagens(texto: str, unidade: str = "aula") -> list[str]:
    return [a.mensagem for a in check_abertura(texto, unidade).achados]


# ─── R1: abertura mínima ─────────────────────────────────────────────────


def test_r1_aula_com_subtitulo_e_paragrafo_passa() -> None:
    assert _regras(AULA_OK) == []


def test_r1_aula_que_abre_com_h2_reprova() -> None:
    texto = "# Aula 1.1: X\n\n## Por que\n\n" + PROSA
    assert "R1" in _regras(texto)


@pytest.mark.parametrize("bloco", [
    "- item um\n- item dois",
    "| a | b |\n|---|---|\n| 1 | 2 |",
    "> citação em destaque",
    "![legenda](fig.svg)",
    "1. passo um\n2. passo dois",
])
def test_r1_nada_antes_do_subtitulo(bloco: str) -> None:
    texto = f"# Aula 1.1: X\n\n{bloco}\n\nSubtítulo depois.\n\n{PROSA}"
    assert "R1" in _regras(texto)


def test_r1_subtitulo_com_duas_frases_reprova() -> None:
    texto = f"# Aula 1.1: X\n\nPrimeira frase. Segunda frase.\n\n{PROSA}"
    msgs = _mensagens(texto)
    assert any("Subtítulo" in m and "frase" in m for m in msgs)


def test_r1_o_primeiro_elemento_depois_do_subtitulo_e_paragrafo() -> None:
    texto = f"# Aula 1.1: X\n\nSubtítulo em uma frase.\n\n## O que você vai aprender\n\n{PROSA}"
    regras = _regras(texto)
    assert "R1" in regras
    # "O que você vai aprender" como seção também é R8.
    assert "R8" in regras


def test_r1_nao_vale_para_texto_sem_h1_nem_para_trilha() -> None:
    assert "R1" not in _regras("Só prosa, sem cabeçalho.\n\n" + PROSA)
    trilha = "# Trilha 1: X\n\n## Glossário\n\n**termo**: glosa\n\n## Fontes\n\nOctadesk, CX Trends, maio de 2025.\n"
    assert _regras(trilha) == []


# ─── R3, R5, R6, R8, R9 ─────────────────────────────────────────────────


@pytest.mark.parametrize("cabecalho,regra", [
    ("## Escolha seu caminho", "R3"),
    ("## Se você é dono de salão, vá para a aula 3", "R3"),
    ("## Aplique no seu negócio", "R5"),
    ("## Como fica no seu negócio", "R5"),
    ("## Faça agora", "R6"),
    ("### Exercício 1: monte a tabela", "R6"),
    ("## Mão na massa", "R6"),
    ("## Sua vez", "R6"),
    ("## Desafio da semana", "R6"),
    ("## Checkpoint", "R8"),
    ("## Recapitulando", "R8"),
    ("## Quiz rápido", "R8"),
    ("## Resumo do capítulo", "R8"),
])
def test_bloco_proibido_em_cabecalho_reprova(cabecalho: str, regra: str) -> None:
    texto = AULA_OK + f"\n{cabecalho}\n\n{PROSA}\n"
    assert regra in _regras(texto), _mensagens(texto)


@pytest.mark.parametrize("rotulo,regra", [
    ("**Resultado esperado:** uma resposta enviada.", "R6"),
    ("**Se travar:** peça ajuda.", "R6"),
    ("> CHECKPOINT: revise os conceitos.", "R8"),
    ("> EXERCÍCIO: abra a agenda.", "R6"),
])
def test_bloco_proibido_em_rotulo_ou_citacao_reprova(rotulo: str, regra: str) -> None:
    texto = AULA_OK + f"\n{rotulo}\n"
    assert regra in _regras(texto), _mensagens(texto)


def test_r5_mockup_e_maquete_valem_em_qualquer_linha() -> None:
    assert "R5" in _regras(AULA_OK + "\nMonte um mockup da sua página.\n")
    assert "R5" in _regras(AULA_OK + "\nFaça uma maquete do fluxo.\n")


def test_prosa_pode_dizer_do_proprio_negocio_sem_reprovar() -> None:
    """R5 reprova a SEÇÃO 'no seu negócio', não a prosa que fala do negócio dele."""
    texto = AULA_OK + "\nAnote um dado do seu negócio: quantos clientes voltaram no mês.\n"
    assert "R5" not in _regras(texto)


def test_mencao_entre_aspas_nao_reprova_r6_nem_r8() -> None:
    texto = AULA_OK + '\n## Por que tirar o "faça agora" e o "checkpoint" da página\n\n' + PROSA
    regras = _regras(texto)
    assert "R6" not in regras and "R8" not in regras


@pytest.mark.parametrize("trecho", [
    "Este número requer verificação.",
    "Dado a verificar com a equipe.",
    "Taxa de 12% [verificar].",
    "Fonte pendente para o dado de 2025.",
    "Guarde os dados conforme a LGPD.",
    "A Lei Geral de Proteção de Dados manda pedir consentimento.",
    "Veja a Lei 13.709 antes de mandar mensagem.",
    'Ele disse: "isso é assunto de LGPD".',
])
def test_r9_verificacao_e_lgpd_reprovam_mesmo_entre_aspas(trecho: str) -> None:
    assert "R9" in _regras(AULA_OK + f"\n{trecho}\n")


# ─── R7: fontes só no rodapé ────────────────────────────────────────────


def test_r7_fonte_no_meio_da_aula_reprova() -> None:
    assert "R7" in _regras(AULA_OK + "\nFonte: IBGE, Pnad 2025.\n")
    assert "R7" in _regras(AULA_OK + "\n**Fonte:** IBGE, Pnad 2025.\n")
    assert "R7" in _regras(AULA_OK + "\n## Fontes\n\nIBGE, 2025.\n")


def test_r7_trilha_com_fontes_por_ultimo_e_curtas_passa() -> None:
    trilha = (
        "# Trilha 1: X\n\n## O que você vai saber fazer\n\nMedir o tempo de resposta.\n\n"
        "## Glossário\n\n**termo**: glosa\n\n## Fontes\n\n"
        "Octadesk, CX Trends, maio de 2025. https://octadesk.com/cx\n"
        "Booksy, relatório interno, 2024.\n"
    )
    assert _regras(trilha, "trilha") == []


def test_r7_trilha_com_fontes_fora_do_fim_reprova() -> None:
    trilha = (
        "# Trilha 1: X\n\n## Fontes\n\nOctadesk, CX Trends, maio de 2025.\n\n"
        "## Glossário\n\n**termo**: glosa\n"
    )
    assert "R7" in _regras(trilha, "trilha")


def test_r7_fonte_com_comentario_longo_reprova() -> None:
    longa = " ".join(["comentário"] * 30)
    trilha = f"# Trilha 1: X\n\n## Glossário\n\n**t**: g\n\n## Fontes\n\nOctadesk, 2025, {longa}\n"
    assert "R7" in _regras(trilha, "trilha")


# ─── Integração: content_checker e QualityGate ─────────────────────────


def test_check_content_emite_categoria_abertura_bloqueante() -> None:
    texto = AULA_OK.replace("## Por que a demora custa a venda", "## Faça agora")
    erros = check_content(texto, "aula")
    achados = [e for e in erros if e.categoria == "abertura"]
    assert achados and all(e.tipo == "error" for e in achados)
    assert any("[R6]" in e.mensagem for e in achados)


def test_aula_limpa_nao_recebe_achado_de_abertura() -> None:
    erros = check_content(AULA_OK, "aula")
    assert [e for e in erros if e.categoria == "abertura"] == []


def test_quality_gate_reprova_checkpoint_e_mede_a_trilha() -> None:
    gate = QualityGate(client=load_client("default"), auto_fix=False)
    texto = (
        "<!-- Módulo 1: X -->\n\n" + AULA_OK + "\n> CHECKPOINT: revise.\n\n"
        "# Trilha 1: X\n\n## Fontes\n\nOctadesk, 2025.\n\n## Glossário\n\n**t**: g\n"
    )
    r = gate.check_text(texto, curso_id="t", unidade="aula", geo=False)
    assert not r.aprovado
    assert any("[R8]" in e for e in r.erros)
    # A trilha é medida também: "Fontes" fora do fim reprova por R7.
    assert any("[R7]" in e and "último H2" in e for e in r.erros)
    # O achado carrega o rótulo da trilha no relatório de conteúdo.
    achados = check_content(texto.split("# Trilha 1: X", 1)[0], "x")
    assert not any("[R7]" in e.mensagem for e in achados)


def test_quality_gate_aprova_a_trilha_bem_formada() -> None:
    gate = QualityGate(client=load_client("default"), auto_fix=False)
    trilha = "# Trilha 1: X\n\n## Glossário\n\n**t**: g\n\n## Fontes\n\nOctadesk, CX Trends, maio de 2025.\n"
    r = gate.check_text(trilha, curso_id="t", module_name="Trilha 1: X", unidade="aula", geo=False)
    assert [e for e in r.erros if "[R" in e] == []


# ─── Parser: subtítulo, fontes, checkpoint descartado ──────────────────


def test_parser_extrai_subtitulo_e_fontes() -> None:
    sub, corpo = extrair_subtitulo("Você vai responder mais rápido.\n\n" + PROSA)
    assert sub == "Você vai responder mais rápido."
    assert corpo.startswith("palavra")
    sub2, corpo2 = extrair_subtitulo("## Sem subtítulo\n\n" + PROSA)
    assert sub2 == "" and corpo2.startswith("## Sem")

    md = "## Glossário\n\n**t**: g\n\n## Fontes\n\n- Octadesk, 2025.\n- Booksy, 2024.\n"
    sem, fontes = extrair_fontes(md)
    assert fontes == ["Octadesk, 2025.", "Booksy, 2024."]
    assert "Fontes" not in sem and "Glossário" in sem


def test_parser_descarta_checkpoint_e_nao_fabrica_secao() -> None:
    secoes = parse_module_to_sections("Prosa.\n\n> CHECKPOINT: revise.\n\n> DICA: confira.")
    assert [s.type.value for s in secoes] == ["text", "tip"]


# ─── CourseDefinition e TSX: a publicação morde ────────────────────────


def _curso(secoes: list[dict], **extra) -> CourseDefinition:
    return CourseDefinition(
        slug="teste-abertura",
        titulo="Curso de teste da abertura",
        descricao="Descrição do curso com mais de vinte caracteres.",
        descricao_curta="Subtítulo do curso em uma frase.",
        steps=[{
            "id": "modulo-um",
            "title": "Módulo um",
            "duration": "10 min",
            "description": "Subtítulo do módulo em uma frase.",
            "content": secoes,
        }],
        autor_nome="Maria Silva",
        autor_credencial="Consultora",
        dominio="https://exemplo.com.br",
        company_name="Exemplo",
        company_description="Empresa de exemplo.",
        **extra,
    )


TABELA = {"type": "dataTable", "value": "", "data": {
    "columns": ["Régua", "Número"], "rows": [["Operador", "400"], ["Documento", "250"]],
    "source": "IBGE, Pnad, 2025 https://www.ibge.gov.br/pnad"}}


def test_definicao_reprova_marcador_pendente_e_termos_proibidos() -> None:
    curso = _curso([
        {"type": "text", "value": "Parágrafo de abertura [FALTA EVIDÊNCIA: taxa de retorno]."},
        {"type": "tip", "value": "Faça agora: abra a agenda e conforme a LGPD peça consentimento."},
    ])
    msgs = check_abertura_definicao(curso)
    assert any("apuração pendente" in m for m in msgs)
    assert any("[R9]" in m for m in msgs)


def test_render_page_levanta_abertura_error() -> None:
    curso = _curso([{"type": "text", "value": "Este número requer verificação antes de publicar."}])
    with pytest.raises(AberturaError) as exc:
        TsxGenerator().render_page(curso, cobrar_peso_visual=False)
    assert "[R9]" in str(exc.value)
    assert "abertura-direta-sem-distracao" in str(exc.value)


def test_definicao_exige_prosa_na_primeira_secao() -> None:
    curso = _curso([TABELA, {"type": "text", "value": "Prosa depois da tabela."}])
    assert any("R1" in m for m in check_abertura_definicao(curso))


@pytest.fixture(scope="module")
def tsx() -> str:
    curso = _curso(
        [{"type": "text", "value": "Parágrafo de abertura direto ao ponto."}, TABELA],
        fontes=["Octadesk, CX Trends, maio de 2025."],
        prerequisitos_display=["Ter o WhatsApp Business instalado"],
    )
    return TsxGenerator().render_page(curso, cobrar_peso_visual=False)


def test_template_abre_com_h1_subtitulo_e_modulos_nessa_ordem(tsx: str) -> None:
    """R1 e R2 no template: H1 antes do subtítulo, subtítulo antes dos módulos, sem botão no meio."""
    corpo = tsx[tsx.index('<main id="main-content">'):]
    i_h1 = corpo.index("<h1")
    i_sub = corpo.index("Subtítulo do curso em uma frase.")
    i_steps = corpo.index("<StepCard")
    assert i_h1 < i_sub < i_steps
    topo = corpo[:i_steps]
    assert "<button" not in topo and "<nav" not in topo and "<aside" not in topo


def test_template_nao_emite_os_blocos_do_topo_carregado(tsx: str) -> None:
    assert "O que você vai aprender" not in tsx
    assert "sf-label" not in tsx  # rótulo que vinha ANTES do H1
    assert "Tempo estimado: ~" not in tsx  # barra de estatísticas do hero
    assert "sticky top-[57px]" not in tsx  # barra de progresso fixa
    assert "Pré-requisitos</h5>" not in tsx  # card lateral
    assert 'case "checkpoint"' not in tsx  # R8
    assert "Checkpoint</span>" not in tsx


def test_template_descricao_aparece_uma_vez_no_topo(tsx: str) -> None:
    """R4: a descrição do curso não se repete em card visível; o JSON-LD não conta."""
    visivel = tsx[tsx.index('<main id="main-content">'):tsx.index("<Footer")]
    assert visivel.count("Descrição do curso com mais de vinte caracteres.") == 1


def test_template_fontes_so_no_rodape_e_pequenas(tsx: str) -> None:
    """R7: nenhum 'Fonte:' dentro de bloco; um bloco 'Fontes' depois do FAQ, antes do Footer, em 0.8rem."""
    assert "Fonte: {" not in tsx
    assert "BlockFootnote source=" not in tsx
    inicio = tsx.index('aria-label="Fontes"')
    assert inicio > tsx.index("Perguntas frequentes")
    assert inicio < tsx.index("<Footer")
    bloco = tsx[inicio:tsx.index("</section>", inicio)]
    assert "text-[0.8rem]" in bloco
    assert "Octadesk, CX Trends, maio de 2025." in bloco
    # O `source` da tabela subiu para o rodapé, e a URL virou link.
    assert "IBGE, Pnad, 2025" in bloco
    assert re.search(r'<a href="https://www\.ibge\.gov\.br/pnad"[^>]*>https://www\.ibge\.gov\.br/pnad</a>', bloco)
    # Pré-requisitos viraram uma linha discreta no rodapé, não card no topo.
    assert "Antes de começar:" in tsx and tsx.index("Antes de começar:") > tsx.index("Perguntas frequentes")


def test_curso_sem_fontes_nao_desenha_o_bloco() -> None:
    curso = _curso([{"type": "text", "value": "Parágrafo de abertura direto ao ponto."}])
    saida = TsxGenerator().render_page(curso, cobrar_peso_visual=False)
    assert 'aria-label="Fontes"' not in saida


def test_step_definition_nao_exige_mais_checkpoint_nem_tres_secoes() -> None:
    curso = _curso([{"type": "text", "value": "Uma seção basta."}])
    assert len(curso.steps[0].content) == 1
