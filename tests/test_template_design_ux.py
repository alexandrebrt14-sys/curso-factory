"""Camada de design, layout e experiência de uso do template (07/10/2026).

Critérios do `GUIA_DESIGN_LAYOUT_UX.md` que viraram template nesta rodada: alvo
de toque de 44 px nos botões principais (D18), anel de foco visível e acordeão
anunciado ao leitor de tela (D19), transições desligadas com movimento reduzido
(D40), figura por caminho de imagem com `alt`, dimensões e carregamento tardio
(D22) e aviso de descrição da página fora da faixa (D46). Nenhum item aqui cria
gate novo: o que o teste cobra é que o template continue emitindo o que o guia
diz que ele emite.
"""

from __future__ import annotations

import logging
import re
import sys
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.generators import TsxGenerator  # noqa: E402
from src.generators.tsx_generator import DESCRICAO_MAX_CHARS, DESCRICAO_MIN_CHARS  # noqa: E402
from src.models import CourseDefinition  # noqa: E402
from src.parsers import parse_module_to_sections  # noqa: E402

FOCO = (
    "focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--accent)]"
)
DESCRICAO_OK = (
    "Curso de teste da camada visual: página, capítulos em acordeão, peças visuais e "
    "metadados conferidos no celular de 390 pontos, nos dois temas."
)


def _curso(secoes: list[dict], descricao: str = DESCRICAO_OK) -> CourseDefinition:
    return CourseDefinition(
        slug="teste-design-ux",
        titulo="Teste da camada visual",
        descricao=descricao,
        descricao_curta="Subtítulo do curso em uma frase.",
        steps=[
            {
                "id": "capitulo-um",
                "title": "Capítulo um",
                "duration": "10 min",
                "description": "Subtítulo do capítulo em uma frase.",
                "content": secoes,
            }
        ],
        autor_nome="Maria Silva",
        autor_credencial="Consultora",
        dominio="https://exemplo.com.br",
        company_name="Exemplo",
        company_description="Empresa de exemplo.",
    )


@pytest.fixture(scope="module")
def tsx() -> str:
    secoes = [
        {"type": "text", "value": "Parágrafo de abertura direto ao ponto."},
        {
            "type": "figure",
            "value": "tempo-de-resposta.svg",
            "label": "O tempo cai de 4 h para 12 min.",
        },
    ]
    return TsxGenerator().render_page(_curso(secoes), cobrar_peso_visual=False)


def _bloco(tsx: str, inicio: str, fim: str) -> str:
    return tsx.split(inicio, 1)[1].split(fim, 1)[0]


# ─── D18 e D19: alvo de toque, foco visível e acordeão anunciado ───────


def test_cabecalho_do_capitulo_tem_44px_foco_e_estado_anunciado(tsx: str) -> None:
    cabecalho = _bloco(tsx, "{/* Header */}", "{/* Content */}")
    assert "min-h-[44px]" in cabecalho
    assert FOCO in cabecalho
    assert "aria-expanded={isOpen}" in cabecalho
    assert "aria-controls={`${step.id}-conteudo`}" in cabecalho
    # O conteúdo que o cabeçalho controla carrega o mesmo id.
    assert "id={`${step.id}-conteudo`}" in tsx


def test_botoes_principais_tem_44px_e_foco_visivel(tsx: str) -> None:
    concluir = _bloco(tsx, "{/* Único botão do módulo", "{/* ───────── FAQ DATA")
    assert "min-h-[44px]" in concluir and FOCO in concluir
    recomecar = tsx[
        tsx.index("onClick={resetProgress}") : tsx.index("Recomeçar do primeiro módulo")
    ]
    assert "min-h-[44px]" in recomecar and FOCO in recomecar
    faq = _bloco(tsx, "<summary", "</summary>")
    assert "min-h-[44px]" in faq and FOCO in faq


def test_botao_de_copiar_fica_acima_do_piso_de_24px(tsx: str) -> None:
    """Ação secundária numa barra de 40 px: 32 px fica acima do piso 2.5.8 da WCAG 2.2."""
    copiar = _bloco(tsx, "function CodeBlock(", "/* ───────── RICH TEXT RENDERER")
    assert "min-h-[32px]" in copiar
    assert FOCO in copiar


# ─── D40: movimento reduzido ───────────────────────────────────────────


def test_toda_transicao_do_template_desliga_com_movimento_reduzido(tsx: str) -> None:
    linhas = [
        linha
        for linha in tsx.splitlines()
        if re.search(r"\btransition-(all|colors|transform)\b", linha)
    ]
    assert linhas, "o template tem transições"
    sem_reducao = [
        linha.strip() for linha in linhas if "motion-reduce:transition-none" not in linha
    ]
    assert sem_reducao == [], sem_reducao


# ─── D22: figura por caminho vira <img> acessível ──────────────────────


def test_figura_por_caminho_sai_como_img_com_alt_dimensoes_e_lazy(tsx: str) -> None:
    figura = _bloco(tsx, "function FigureBlock(", "/* Tabela de dados.")
    assert 'markup.trim().startsWith("<")' in figura
    img = _bloco(figura, "<img", "/>")
    for atributo in (
        "src={markup}",
        'alt={caption || ""}',
        "width={1200}",
        "height={675}",
        'loading="lazy"',
        'decoding="async"',
    ):
        assert atributo in img, atributo
    # O SVG inline continua entrando pelo caminho antigo.
    assert "dangerouslySetInnerHTML" in figura
    # A figura promovida pelo parser chega ao TSX com o caminho e a legenda.
    assert 'value: "tempo-de-resposta.svg"' in tsx
    assert "O tempo cai de 4 h para 12 min." in tsx


def test_parser_promove_imagem_com_legenda_para_figure_com_caminho() -> None:
    secoes = parse_module_to_sections(
        "Prosa de abertura.\n\n![O tempo cai de 4 h para 12 min.](tempo.svg)\n\nMais prosa."
    )
    figuras = [s for s in secoes if s.type.value == "figure"]
    assert len(figuras) == 1
    assert figuras[0].value == "tempo.svg"
    assert figuras[0].label == "O tempo cai de 4 h para 12 min."


# ─── D46: descrição da página na faixa ─────────────────────────────────


def test_descricao_fora_da_faixa_avisa_sem_bloquear(caplog: pytest.LogCaptureFixture) -> None:
    gerador = TsxGenerator()
    curta = _curso([{"type": "text", "value": "Prosa."}], descricao="Descrição curta demais.")
    with caplog.at_level(logging.WARNING, logger="src.generators.tsx_generator"):
        saida = gerador.render_layout(curta)
    assert "description:" in saida
    assert any(
        f"fora da faixa de {DESCRICAO_MIN_CHARS} a {DESCRICAO_MAX_CHARS}" in r.getMessage()
        for r in caplog.records
    )


def test_descricao_na_faixa_nao_avisa(caplog: pytest.LogCaptureFixture) -> None:
    assert DESCRICAO_MIN_CHARS <= len(DESCRICAO_OK) <= DESCRICAO_MAX_CHARS
    with caplog.at_level(logging.WARNING, logger="src.generators.tsx_generator"):
        TsxGenerator().render_layout(_curso([{"type": "text", "value": "Prosa."}]))
    assert not [r for r in caplog.records if "fora da faixa" in r.getMessage()]
