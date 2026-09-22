"""Didática das superfícies que a régua de forma não mede (22/09/2026).

O que se cobra aqui é o vínculo entre o defeito medido na auditoria e o achado
do gate: cadência de abertura de parágrafo, jargão sem glosa, fecho com ação e
critério, enxurrada de versão, título como promessa, subtítulo sem fórmula e
fichas no registro da aula. Os números vêm de `validation.didatica` do YAML e
de `limiares` do espelho; os testes trocam a configuração para provar que o
veredito acompanha.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.generators.tsx_generator import TsxGenerator  # noqa: E402
from src.models import CourseDefinition  # noqa: E402
from src.validators import rules_loader  # noqa: E402
from src.validators.content_checker import check_content  # noqa: E402
from src.validators.didatica_checker import (  # noqa: E402
    Ficha,
    check_didatica,
    check_didatica_definicao,
    check_fichas,
    check_subtitulo,
    check_subtitulos,
    check_titulo,
    format_report,
)

ENCHIMENTO = " ".join(["palavra"] * 25) + "."


def _aula(paragrafos: list[str], titulo: str = "Como a oficina parou de perder orçamento") -> str:
    corpo = "\n\n".join(paragrafos)
    return (
        f"# Aula 1.1: {titulo}\n\n"
        "Você responde o orçamento antes de o cliente desistir.\n\n"
        f"{corpo}\n"
    )


def _regras(texto: str) -> list[str]:
    return [a.regra for a in check_didatica(texto).achados]


# ─── Cadência de abertura ───────────────────────────────────────────────


def test_tres_paragrafos_com_a_mesma_entrada_reprovam() -> None:
    texto = _aula([f"O cliente {ENCHIMENTO}", f"O dono {ENCHIMENTO}", f"O caixa {ENCHIMENTO}"])
    resultado = check_didatica(texto)
    assert "abertura-em-serie" in [a.regra for a in resultado.erros]


def test_dois_pares_repetidos_so_avisam() -> None:
    texto = _aula(
        [
            f"O cliente {ENCHIMENTO}",
            f"O dono {ENCHIMENTO}",
            f"Quando chove, {ENCHIMENTO}",
            f"Depois disso, {ENCHIMENTO}",
            f"Depois da venda, {ENCHIMENTO}",
        ]
    )
    resultado = check_didatica(texto)
    assert "abertura-repetida" in [a.regra for a in resultado.avisos]
    assert resultado.aprovado


def test_maioria_por_artigo_definido_avisa() -> None:
    texto = _aula([f"{art} {ENCHIMENTO}" for art in ("O", "A", "Os", "Em", "As", "O", "Se", "A")])
    assert "abertura-por-artigo" in _regras(texto)


def test_entradas_variadas_passam_limpas() -> None:
    texto = _aula(
        [
            f"Quando o orçamento demora, {ENCHIMENTO}",
            f"O cliente {ENCHIMENTO}",
            f"Em três dias {ENCHIMENTO}",
            f"Anote o valor e confira em uma semana se {ENCHIMENTO}",
        ]
    )
    assert not any(r.startswith("abertura") for r in _regras(texto))


# ─── Jargão, fecho, versão ─────────────────────────────────────────────


def test_jargao_da_fonte_sem_glosa_avisa_e_com_glosa_passa() -> None:
    sem = _aula(
        [f"O funil da loja encolheu. {ENCHIMENTO}", f"Anote hoje o total em 7 dias. {ENCHIMENTO}"]
    )
    com = _aula(
        [
            f"O funil (o caminho do cliente, de ouvi falar até paguei) encolheu. {ENCHIMENTO}",
            f"Anote hoje o total em 7 dias. {ENCHIMENTO}",
        ]
    )
    assert "jargao-sem-glosa" in _regras(sem)
    assert "jargao-sem-glosa" not in _regras(com)


def test_fecho_sem_acao_e_sem_criterio_avisa() -> None:
    texto = _aula(
        [f"Quando chove, {ENCHIMENTO}", "A loja vendeu bem e todos ficaram contentes com isso."]
    )
    regras = _regras(texto)
    assert "fecho-sem-acao" in regras
    assert "fecho-sem-criterio" in regras


def test_fecho_com_imperativo_e_criterio_passa() -> None:
    texto = _aula(
        [
            f"Quando chove, {ENCHIMENTO}",
            "Abra a agenda hoje e anote quantos orçamentos saíram em 7 dias.",
        ]
    )
    regras = _regras(texto)
    assert "fecho-sem-acao" not in regras
    assert "fecho-sem-criterio" not in regras


def test_fecho_que_resume_avisa() -> None:
    texto = _aula([f"Quando chove, {ENCHIMENTO}", "Em resumo, anote hoje o que saiu em 7 dias."])
    assert "fecho-resumo" in _regras(texto)


def test_enxurrada_de_versao_avisa() -> None:
    versoes = " ".join(f"React {i}.{i} e Next 1{i}.0 mudaram." for i in range(8))
    texto = _aula([f"Quando chove, {versoes} {ENCHIMENTO}"] + [f"Se der, {ENCHIMENTO}"] * 6)
    assert "enxurrada-de-versao" in _regras(texto)


# ─── Título e subtítulo ────────────────────────────────────────────────


@pytest.mark.parametrize(
    "titulo, regra",
    [
        ("DESIGN.md: o sistema de design escrito para o agente ler", "titulo-com-dois-pontos"),
        ("A escada de movimento e o radar do trimestre", "titulo-sem-verbo"),
        (
            "Astro ou Next.js pelo tipo de página e o custo da troca em cada base do site",
            "titulo-longo",
        ),
    ],
)
def test_titulo_indice_de_tecnico_avisa(titulo: str, regra: str) -> None:
    assert regra in [a.regra for a in check_titulo(titulo)]


def test_titulo_como_promessa_passa() -> None:
    assert check_titulo("Aula 2.3: Escolher a base do site sem pagar duas vezes") == []


def test_subtitulo_com_formula_e_promessas_empilhadas_avisa() -> None:
    sub = (
        "Você sai com o framework escolhido pelo tipo de página, a peça de cada camada definida, "
        "o radar do trimestre lido pelos rótulos novo, atualização e alerta, e o custo escrito"
    )
    regras = [a.regra for a in check_subtitulo(sub)]
    assert {"subtitulo-formula", "subtitulo-promessas-empilhadas", "subtitulo-longo"} <= set(regras)


def test_formula_repetida_entre_subtitulos_reprova() -> None:
    achados = check_subtitulos(
        ["Você sai com o site no ar", "Você sai com a base escolhida", "Você sai com o custo"]
    )
    assert [a.tipo for a in achados] == ["error"]
    assert (
        check_subtitulos(["Você sai com o site no ar", "O custo cabe no bolso", "Escolha a base"])
        == []
    )


# ─── Fichas ────────────────────────────────────────────────────────────


def _ficha_tecnica(i: int) -> Ficha:
    return Ficha(
        nome=f"Recurso {i}",
        explicacao="Num projeto novo, o Dialog.Root abre a caixa e a equipe mantém a composição dos componentes.",
        exemplo="A loja escolhe esse caminho quando a identidade visual exige liberdade na composição.",
        conferencia="Confira as APIs na versão instalada; a documentação atual pode conter mudanças.",
    )


def test_fichas_em_registro_tecnico_reprovam_por_fuga_e_avisam_o_resto() -> None:
    achados = check_fichas([_ficha_tecnica(i) for i in range(8)])
    regras = {a.regra for a in achados}
    assert "ficha-conferencia-de-fuga" in {a.regra for a in achados if a.tipo == "error"}
    assert {
        "ficha-registro-impessoal",
        "ficha-abertura-repetida",
        "ficha-api-crua",
        "fichas-em-paredao",
    } <= regras


def test_fichas_no_registro_da_aula_passam() -> None:
    fichas = [
        Ficha(
            nome="Diálogo",
            explicacao="Você abre a caixa de confirmação com Dialog.Root (a moldura que segura a janela).",
            exemplo="Na padaria, você confirma o pedido antes de cobrar, e o cliente vê o total.",
            conferencia="Clique em cancelar: o pedido precisa continuar na tela, sem cobrar.",
        ),
        Ficha(
            nome="Tema",
            explicacao="Você guarda as cores num tema (a lata de tinta com etiqueta) e troca uma vez.",
            exemplo="Quando você muda o azul da marca, todos os botões mudam juntos.",
            conferencia="Troque a cor e abra três páginas: as três precisam mostrar o azul novo.",
        ),
    ]
    assert check_fichas(fichas, ligacoes=1) == []


# ─── Integração: gate e gerador ────────────────────────────────────────


def test_check_content_emite_categoria_didatica() -> None:
    texto = _aula([f"O cliente {ENCHIMENTO}", f"O dono {ENCHIMENTO}", f"O caixa {ENCHIMENTO}"])
    categorias = {e.categoria for e in check_content(texto, "aula")}
    assert "didatica" in categorias


def test_desligar_no_yaml_silencia_o_gate(tmp_path, monkeypatch) -> None:
    yaml = tmp_path / "quality_rules.yaml"
    yaml.write_text("validation:\n  didatica:\n    enabled: false\n", encoding="utf-8")
    monkeypatch.setattr(rules_loader, "RULES_PATH", yaml)
    rules_loader.load_rules.cache_clear()
    try:
        texto = _aula([f"O cliente {ENCHIMENTO}", f"O dono {ENCHIMENTO}", f"O caixa {ENCHIMENTO}"])
        assert check_didatica(texto).achados == []
    finally:
        rules_loader.load_rules.cache_clear()


def test_numero_do_yaml_muda_o_veredito(tmp_path, monkeypatch) -> None:
    yaml = tmp_path / "quality_rules.yaml"
    yaml.write_text(
        "validation:\n  didatica:\n    aberturas:\n      serie_igual_erro: 5\n", encoding="utf-8"
    )
    monkeypatch.setattr(rules_loader, "RULES_PATH", yaml)
    rules_loader.load_rules.cache_clear()
    try:
        texto = _aula([f"O cliente {ENCHIMENTO}", f"O dono {ENCHIMENTO}", f"O caixa {ENCHIMENTO}"])
        assert check_didatica(texto).aprovado
    finally:
        rules_loader.load_rules.cache_clear()


def _curso(descricoes: list[str]) -> CourseDefinition:
    steps = [
        {
            "id": f"modulo-{i}",
            "title": "Escolher a base do site sem pagar duas vezes",
            "duration": "8 min",
            "description": d,
            "content": [
                {
                    "type": "text",
                    "value": f"Quando chove, {ENCHIMENTO}\n\nAnote hoje o que saiu em 7 dias.",
                }
            ],
        }
        for i, d in enumerate(descricoes)
    ]
    return CourseDefinition(
        slug="curso-teste",
        titulo="Curso de teste",
        descricao="Descrição do curso de teste com mais de vinte caracteres.",
        steps=steps,
    )


def test_definicao_aponta_formula_repetida_e_o_gerador_nao_recusa() -> None:
    curso = _curso(["Você sai com o site", "Você sai com a base", "Você sai com o custo"])
    mensagens = check_didatica_definicao(curso)
    assert any("subtitulo-formula-repetida" in m for m in mensagens)
    gerador = TsxGenerator()
    tsx = gerador.render_page(curso, cobrar_peso_visual=False)
    assert "curso-teste" in tsx
    assert gerador.achados_didatica == mensagens


def test_format_report_lista_erros_e_avisos() -> None:
    texto = _aula([f"O cliente {ENCHIMENTO}", f"O dono {ENCHIMENTO}", f"O caixa {ENCHIMENTO}"])
    relatorio = format_report(check_didatica(texto))
    assert relatorio.startswith("Didática: 1 erro(s)")
    assert "[error] abertura-em-serie" in relatorio


# ─── Orquestrador: título proposto pelo redator ────────────────────────


def test_orquestrador_extrai_titulo_proposto_no_topo() -> None:
    from src.orchestrator import Orchestrator

    titulo, corpo = Orchestrator._extrair_titulo_proposto(
        "TÍTULO: Escolher a base do site sem pagar duas vezes\n\nVocê decide a base em uma tarde.\n\nProsa."
    )
    assert titulo == "Escolher a base do site sem pagar duas vezes"
    assert corpo.startswith("Você decide a base em uma tarde.")


def test_orquestrador_ignora_titulo_fora_do_topo() -> None:
    from src.orchestrator import Orchestrator

    texto = "Você decide a base em uma tarde.\n\nTítulo: isso é prosa.\n"
    assert Orchestrator._extrair_titulo_proposto(texto) == (None, texto)
