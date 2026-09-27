"""27/09/2026: aula-guia aplicável, orçamento de narrativa e fonte recente.

Pedido do dono: a aula vira guia de como fazer, a história só entra quando
carrega o procedimento e todo conceito se apoia em fonte recente e datada. Cada
regra tem configuração lida por código, validador e teste; os exemplos de
`examples/` servem de antes e depois. Sem a configuração, nada muda.
"""

from __future__ import annotations

import sys
from datetime import date
from pathlib import Path

import pytest
import yaml

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.clients import load_client  # noqa: E402
from src.clients.context import (  # noqa: E402
    FontesRecentesConfig,
    GuiaAplicavelConfig,
    NarrativaConfig,
)
from src.validators import rules_loader  # noqa: E402
from src.validators.fontes_recentes_checker import (  # noqa: E402
    check_fontes_recentes,
    data_de_referencia,
    idade_em_meses,
    ler_data,
)
from src.validators.guia_aplicavel_checker import (  # noqa: E402
    check_guia_aplicavel,
    instrucao_para_prompt,
    medir,
)
from src.validators.narrativa_checker import check_narrativa  # noqa: E402
from src.validators.narrativa_checker import medir as medir_narrativa  # noqa: E402

REGRAS = PROJECT_ROOT / "config" / "quality_rules.yaml"
EXEMPLOS = PROJECT_ROOT / "examples"
GUIA = (EXEMPLOS / "aula_guia_referencia.md").read_text(encoding="utf-8")
ANTES = (EXEMPLOS / "aula_narrativa_antes.md").read_text(encoding="utf-8")
REFERENCIA = date(2026, 9, 27)

LIGADO_GUIA = GuiaAplicavelConfig(enabled=True, tipo_de_aula="pratica")
LIGADO_NARRATIVA = NarrativaConfig(enabled=True, parcela_max=0.2, abertura_sem_narrativa=True)
LIGADO_FONTES = FontesRecentesConfig(
    enabled=True, janela_meses=12, parcela_min_recente=0.5, estado_atual_max_meses=18
)


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


def _regras(achados) -> set[str]:
    return {a.regra for a in achados}


# ── configuração por cliente ────────────────────────────────────────────


def test_default_liga_as_tres_regras_com_os_numeros_do_client_yaml() -> None:
    c = load_client("default")
    dados = yaml.safe_load(
        (PROJECT_ROOT / "config" / "clients" / "default" / "client.yaml").read_text(
            encoding="utf-8"
        )
    )
    assert c.guia_aplicavel.enabled and c.narrativa.enabled and c.fontes_recentes.enabled
    assert c.narrativa.parcela_max == dados["narrativa"]["parcela_max"]
    assert c.fontes_recentes.janela_meses == dados["fontes_recentes"]["janela_meses"]
    assert (
        c.fontes_recentes.estado_atual_max_meses
        == dados["fontes_recentes"]["estado_atual_max_meses"]
    )
    assert c.guia_aplicavel.severidade == "aviso"


def test_template_deixa_as_tres_regras_desligadas() -> None:
    c = load_client("_template")
    assert not c.guia_aplicavel.enabled
    assert not c.narrativa.enabled
    assert not c.fontes_recentes.enabled


def test_curso_sobrepoe_a_recencia_do_cliente_chave_a_chave() -> None:
    curso = LIGADO_FONTES.sobreposto_por({"janela_meses": 6, "data_de_referencia": "2026-01-31"})
    assert curso.janela_meses == 6
    assert curso.parcela_min_recente == LIGADO_FONTES.parcela_min_recente
    assert data_de_referencia(curso, REFERENCIA) == date(2026, 1, 31)
    assert LIGADO_FONTES.sobreposto_por(None) is LIGADO_FONTES


# ── A e B: aula-guia e completude do como fazer ─────────────────────────


def test_aula_guia_de_referencia_passa_na_completude() -> None:
    m = medir(GUIA)
    assert m.passos >= 3 and not m.passos_sem_imperativo
    assert check_guia_aplicavel(GUIA, LIGADO_GUIA) == []


def test_aula_narrativa_antiga_nao_ensina_a_fazer() -> None:
    regras = _regras(check_guia_aplicavel(ANTES, LIGADO_GUIA))
    assert {
        "guia-sem-procedimento",
        "guia-sem-decisao",
        "guia-sem-criterio-de-pronto",
        "guia-sem-aplicacao",
    } <= regras


def test_passo_sem_imperativo_e_apontado() -> None:
    texto = GUIA.replace("1. Abra as configurações", "1. As configurações")
    achados = check_guia_aplicavel(texto, LIGADO_GUIA)
    assert any(a.regra == "passo-sem-imperativo" and "1" in a.mensagem for a in achados)


def test_bloco_de_passos_fora_de_lista_numerada_conta_como_procedimento() -> None:
    texto = "# Aula\n\nSubtítulo curto.\n\nAbertura.\n\n" + "\n\n".join(
        f"**Passo {i}.** Anote o valor {i}." for i in range(1, 5)
    )
    assert medir(texto).passos == 4


def test_aula_conceitual_pede_orientacao_de_aplicacao_e_aceita_decisao() -> None:
    conceitual = GuiaAplicavelConfig(enabled=True, tipo_de_aula="conceitual")
    so_conceito = "# Aula\n\nSubtítulo curto.\n\nA ideia é esta. Ela vale para lojas.\n"
    assert "guia-sem-aplicacao" in _regras(check_guia_aplicavel(so_conceito, conceitual))
    com_decisao = so_conceito + (
        "\nSe a loja vende pela internet, use o conceito no carrinho. "
        "Está pronto quando o carrinho mostra o total.\n"
    )
    assert check_guia_aplicavel(com_decisao, conceitual) == []


def test_severidade_erro_do_client_yaml_reprova() -> None:
    erro = GuiaAplicavelConfig(enabled=True, tipo_de_aula="pratica", severidade="erro")
    assert {a.tipo for a in check_guia_aplicavel(ANTES, erro)} == {"error"}
    assert {a.tipo for a in check_guia_aplicavel(ANTES, LIGADO_GUIA)} == {"warning"}


def test_piso_do_yaml_muda_o_veredito(regras_trocadas) -> None:
    regras_trocadas(lambda v: v["guia_aplicavel"]["tipos_de_aula"]["pratica"].update(passos_min=9))
    assert "guia-sem-procedimento" in _regras(check_guia_aplicavel(GUIA, LIGADO_GUIA))


def test_sem_configuracao_nada_e_medido(regras_trocadas) -> None:
    assert check_guia_aplicavel(ANTES, None) == []
    assert check_guia_aplicavel(ANTES, GuiaAplicavelConfig()) == []
    regras_trocadas(lambda v: v.pop("guia_aplicavel"))
    assert check_guia_aplicavel(ANTES, LIGADO_GUIA) == []
    assert instrucao_para_prompt(LIGADO_GUIA) == ""


def test_molde_do_prompt_sai_do_esqueleto_do_yaml_e_os_pisos_so_com_cliente_ligado() -> None:
    esqueleto = yaml.safe_load(REGRAS.read_text(encoding="utf-8"))["validation"]["guia_aplicavel"][
        "esqueleto"
    ]
    desligado = instrucao_para_prompt(None)
    ligado = instrucao_para_prompt(LIGADO_GUIA)
    for parte in esqueleto:
        assert parte["parte"] in desligado
    assert "verificador automático" not in desligado
    assert "verificador automático" in ligado


# ── C: orçamento de narrativa ───────────────────────────────────────────


def test_aula_narrativa_antiga_estoura_o_orcamento_e_abre_em_cena() -> None:
    m = medir_narrativa(ANTES)
    assert "Cláudia" in m.personagens and m.abertura_narrativa
    assert {"narrativa-acima-do-teto", "narrativa-na-abertura"} <= _regras(
        check_narrativa(ANTES, LIGADO_NARRATIVA)
    )


def test_aula_guia_fica_dentro_do_orcamento() -> None:
    m = medir_narrativa(GUIA)
    assert m.parcela <= LIGADO_NARRATIVA.parcela_max
    assert not m.abertura_narrativa
    assert check_narrativa(GUIA, LIGADO_NARRATIVA) == []


def test_teto_do_client_yaml_muda_o_veredito() -> None:
    folgado = NarrativaConfig(enabled=True, parcela_max=0.95)
    assert "narrativa-acima-do-teto" not in _regras(check_narrativa(ANTES, folgado))


def test_narrativa_no_presente_escapa_do_medidor() -> None:
    """Limite declarado: o medidor lê pretérito, cena e personagem; o presente passa."""
    presente = (
        "# Aula\n\nSubtítulo curto.\n\n"
        + "\n\n".join(
            "A Marta abre a agenda, olha os pedidos e responde a cada cliente." for _ in range(6)
        )
        + "\n"
    )
    assert check_narrativa(presente, LIGADO_NARRATIVA) == []


def test_narrativa_desligada_ou_sem_secao_nao_mede(regras_trocadas) -> None:
    assert check_narrativa(ANTES, None) == []
    assert check_narrativa(ANTES, NarrativaConfig()) == []
    regras_trocadas(lambda v: v.pop("orcamento_narrativa"))
    assert check_narrativa(ANTES, LIGADO_NARRATIVA) == []


# ── D: fonte recente e datada ───────────────────────────────────────────


@pytest.mark.parametrize(
    ("texto", "esperado"),
    [
        ("Microsoft, blog, 13 de julho de 2026.", date(2026, 7, 13)),
        ("FIDO Alliance, relatório, maio de 2026.", date(2026, 5, 1)),
        ("Relatório, 2026-08-14.", date(2026, 8, 14)),
        ("Relatório, 14/08/2026.", date(2026, 8, 14)),
        ("W3C, norma, 2019.", date(2019, 1, 1)),
        ("Sem data nenhuma. https://exemplo.com/2026/07/13/post", None),
    ],
)
def test_datas_em_formatos_do_yaml(texto, esperado) -> None:
    assert ler_data(texto) == esperado


def test_idade_em_meses_completos() -> None:
    assert idade_em_meses(date(2026, 7, 13), REFERENCIA) == 2
    assert idade_em_meses(date(2025, 9, 28), REFERENCIA) == 11
    assert idade_em_meses(date(2025, 3, 1), REFERENCIA) == 18


def test_aula_guia_tem_fontes_recentes_e_a_origem_fica_fora_da_conta() -> None:
    assert check_fontes_recentes(GUIA, LIGADO_FONTES, REFERENCIA) == []


def test_aula_antiga_tem_fonte_sem_data_pouco_recente_e_estado_atual_antigo() -> None:
    regras = _regras(check_fontes_recentes(ANTES, LIGADO_FONTES, REFERENCIA))
    assert {"fonte-sem-data", "fontes-pouco-recentes", "estado-atual-com-fonte-antiga"} <= regras


def test_a_data_de_referencia_e_injetada_e_decide_o_veredito() -> None:
    """O mesmo texto, lido em 2028, deixa de ter fontes recentes."""
    assert check_fontes_recentes(GUIA, LIGADO_FONTES, REFERENCIA) == []
    depois = check_fontes_recentes(GUIA, LIGADO_FONTES, date(2028, 9, 27))
    assert "fontes-pouco-recentes" in _regras(depois)


def test_tabela_de_proveniencia_preenchida_entra_na_conta() -> None:
    tabela = (
        "| Frase da aula | Tipo | URL primária | Data de publicação | Trecho lido | Data de acesso |\n"
        "|---|---|---|---|---|---|\n"
        "| Hoje o limite é de 200 mil tokens. | numero | https://exemplo.com/a | março de 2024 "
        "| trecho | 27/09/2026 |\n"
    )
    achados = check_fontes_recentes("# Aula\n\nTexto.\n", LIGADO_FONTES, REFERENCIA, tabela)
    assert "estado-atual-com-fonte-antiga" in _regras(achados)


def test_fontes_desligadas_ou_sem_secao_nao_medem(regras_trocadas) -> None:
    assert check_fontes_recentes(ANTES, None, REFERENCIA) == []
    assert check_fontes_recentes(ANTES, FontesRecentesConfig(), REFERENCIA) == []
    regras_trocadas(lambda v: v.pop("fontes_recentes"))
    assert check_fontes_recentes(ANTES, LIGADO_FONTES, REFERENCIA) == []


def test_janela_do_client_yaml_muda_o_veredito() -> None:
    longa = FontesRecentesConfig(enabled=True, janela_meses=40, parcela_min_recente=0.5)
    assert "fontes-pouco-recentes" not in _regras(check_fontes_recentes(ANTES, longa, REFERENCIA))


# ── integração com o gate e os prompts ──────────────────────────────────


def test_gate_do_default_emite_as_tres_categorias_como_aviso() -> None:
    from src.validators.quality_gate import QualityGate

    achados = QualityGate.check_guia(ANTES, "aula", load_client("default"), referencia=REFERENCIA)
    assert {a.categoria for a in achados} == {"guia aplicável", "narrativa", "fontes recentes"}
    assert {a.tipo for a in achados} == {"warning"}


def test_gate_de_cliente_sem_os_blocos_fica_como_antes() -> None:
    from src.validators.quality_gate import QualityGate

    for cliente in ("_template", "acme", "herreira"):
        assert QualityGate.check_guia(ANTES, "aula", load_client(cliente)) == [], cliente


def test_prompts_da_redacao_e_da_revisao_recebem_os_blocos(monkeypatch) -> None:
    from src.agents.reviewer import Reviewer
    from src.agents.writer import Writer
    from src.models import Course
    from src.orchestrator import Orchestrator

    orq = Orchestrator.__new__(Orchestrator)
    orq.client_context = load_client("default")
    curso = Course(
        id="curso-x",
        titulo="Curso X de teste",
        fontes_recentes={"data_de_referencia": "2026-09-27"},
    )
    blocos = orq._blocos_guia(curso)
    assert all(blocos.values())
    assert "27/09/2026" in blocos["bloco_fontes_recentes"]
    for agente in (Writer(client=None), Reviewer(client=None)):
        prompt = agente.build_prompt("pesquisa", **blocos)
        assert "{bloco_molde_da_aula}" not in prompt
        assert "{bloco_narrativa}" not in prompt
        assert "{bloco_fontes_recentes}" not in prompt
        assert "Critério de pronto e próximo passo" in prompt

    orq.client_context = load_client("_template")
    desligado = orq._blocos_guia(Course(id="curso-y", titulo="Curso Y de teste"))
    assert desligado["bloco_narrativa"] == "" and desligado["bloco_fontes_recentes"] == ""
    assert desligado["bloco_molde_da_aula"]


def test_pesquisa_pede_data_por_fonte_e_janela_do_cliente() -> None:
    from src.agents.researcher import Researcher
    from src.models import Course
    from src.orchestrator import Orchestrator

    orq = Orchestrator.__new__(Orchestrator)
    orq.client_context = load_client("default")
    curso = Course(
        id="curso-x",
        titulo="Curso X de teste",
        fontes_recentes={"data_de_referencia": "2026-09-27"},
    )
    prompt = Researcher(client=None).build_prompt("ctx", **orq._research_vars(curso))
    assert "data de publicação" in prompt
    assert "27/09/2026" in prompt and "{bloco_fontes_recentes_pesquisa}" not in prompt
    assert "2024–2026" not in prompt


def test_prompts_pt_br_nao_exigem_mais_caso_contado_nem_fecho_pelo_personagem() -> None:
    pasta = PROJECT_ROOT / "src" / "templates" / "prompts" / "pt-br"
    vetadas = (
        "um caso do seu ramo, do começo ao fim",
        "contado inteiro",
        "contado por inteiro",
        "Fecho pelo exemplo",
        "dito pelo exemplo do H2 2",
        "cena de duas frases",
        "contados do começo ao fim",
        "aulas_sem_exemplo_inteiro",
    )
    for nome in ("draft.md", "review.md", "analyze.md", "research.md", "expand.md"):
        texto = (pasta / nome).read_text(encoding="utf-8")
        for frase in vetadas:
            assert frase not in texto, (nome, frase)
