"""Testes da camada `visual_density` (src/validators/visual_density.py).

O teste que mais importa aqui é `test_numeros_saem_do_yaml_e_o_veredito_muda`:
ele grava um YAML de regras com outros limites, aponta o `rules_loader` para
ele e prova que o veredito acompanha a configuração. Enquanto esse teste
existir, ninguém consegue promover o limite de volta a constante de código sem
ficar vermelho.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.models import CourseSection, SectionType
from src.validators import rules_loader
from src.validators.visual_density import CATEGORIA, check_visual_density


# ─── Fábricas de blocos ──────────────────────────────────────────────

def bloco_texto(texto: str) -> CourseSection:
    """Bloco de prosa."""
    return CourseSection(type=SectionType.TEXT, value=texto)


def bloco_figura(n: int = 1) -> CourseSection:
    """Bloco visual do tipo `figure`, com SVG no `value` e legenda no `label`."""
    return CourseSection(
        type=SectionType.FIGURE,
        value=f"<svg role='img' aria-label='diagrama {n}'></svg>",
        label=f"Figura {n}: fluxo do processo",
    )


def bloco_tabela() -> CourseSection:
    """Bloco visual do tipo `dataTable`."""
    return CourseSection(
        type=SectionType.DATA_TABLE,
        value="",
        data={
            "columns": ["Critério", "Antes", "Depois"],
            "rows": [["Custo", "R$ 10", "R$ 4"]],
        },
    )


def bloco_codigo(tamanho: int) -> CourseSection:
    """Bloco de código, que não pode inflar o denominador de prosa."""
    return CourseSection(
        type=SectionType.CODE,
        value="x = 1  # " + ("a" * tamanho),
        language="python",
    )


def prosa(tamanho: int, semente: str = "palavra ") -> str:
    """Devolve um parágrafo de prosa com o tamanho pedido, em caracteres.

    Termina em ponto final para que o `strip()` do checador não devolva um
    caractere a menos e as asserções de tamanho batam na unidade.
    """
    return (semente * (tamanho // len(semente) + 1))[:tamanho - 1] + "."


def tres_visuais() -> list[CourseSection]:
    """Os três blocos visuais que cumprem o piso padrão."""
    return [bloco_figura(1), bloco_figura(2), bloco_tabela()]


def mensagens(erros) -> str:
    """Junta as mensagens dos achados, para asserção de conteúdo."""
    return " || ".join(e.mensagem for e in erros)


@pytest.fixture(autouse=True)
def yaml_do_repositorio():
    """Garante que cada teste começa lendo o YAML real, sem cache sujo."""
    rules_loader.load_rules.cache_clear()
    yield
    rules_loader.load_rules.cache_clear()


@pytest.fixture
def yaml_customizado(monkeypatch: pytest.MonkeyPatch, tmp_path: Path):
    """Devolve uma função que instala um YAML de regras temporário."""
    def instalar(corpo: str) -> Path:
        caminho = tmp_path / "quality_rules.yaml"
        caminho.write_text(corpo, encoding="utf-8")
        monkeypatch.setattr(rules_loader, "RULES_PATH", caminho)
        rules_loader.load_rules.cache_clear()
        return caminho

    yield instalar
    rules_loader.load_rules.cache_clear()


# ─── 1. Teto de parágrafo ────────────────────────────────────────────

def test_paragrafo_acima_do_teto_reprova_e_nomeia_modulo_e_tamanho() -> None:
    """Parágrafo de 1.500 caracteres reprova, com módulo e medida na mensagem."""
    sections = [bloco_texto(prosa(1500)), *tres_visuais()]
    erros = check_visual_density(sections, "Módulo 3: precificação")

    tetos = [e for e in erros if "max_paragraph_chars" in e.mensagem]
    assert len(tetos) == 1
    achado = tetos[0]
    assert achado.tipo == "error"
    assert achado.categoria == CATEGORIA
    assert achado.modulo == "Módulo 3: precificação"
    assert "Módulo 3: precificação" in achado.mensagem
    assert "1500" in achado.mensagem
    assert "1200" in achado.mensagem
    # A mensagem precisa dizer qual peça resolve.
    assert "stepGuide" in achado.mensagem


def test_teto_e_do_paragrafo_e_nao_do_bloco() -> None:
    """Bloco de 2.400 caracteres em dois parágrafos de 1.200 passa no teto."""
    bloco = bloco_texto(prosa(1150) + "\n\n" + prosa(1150))
    erros = check_visual_density([bloco, *tres_visuais()], "módulo")
    assert not [e for e in erros if "max_paragraph_chars" in e.mensagem]

    # O mesmo volume num parágrafo só reprova.
    unico = bloco_texto(prosa(2300))
    erros = check_visual_density([unico, *tres_visuais()], "módulo")
    assert [e for e in erros if "max_paragraph_chars" in e.mensagem]


def test_codigo_e_figura_nao_entram_no_teto_nem_no_denominador() -> None:
    """Bloco de código e SVG de figura não contam como prosa."""
    sections = [bloco_texto(prosa(400)), bloco_codigo(5000), *tres_visuais()]
    erros = check_visual_density(sections, "módulo")
    assert erros == []


# ─── 2. Piso de blocos visuais ───────────────────────────────────────

def test_dois_blocos_visuais_nao_cumprem_o_piso_de_tres() -> None:
    # Prosa acima do corte de 800: só então o piso de três se aplica.
    sections = [bloco_texto(prosa(900)), bloco_figura(1), bloco_tabela()]
    erros = check_visual_density(sections, "Módulo 1")

    pisos = [e for e in erros if "min_visual_blocks_per_module" in e.mensagem]
    assert len(pisos) == 1
    assert pisos[0].tipo == "error"
    assert "Módulo 1" in pisos[0].mensagem
    assert "2 bloco(s) visual(is)" in pisos[0].mensagem
    assert "Faltam 1" in pisos[0].mensagem


def test_tabela_dentro_de_bloco_de_texto_nao_da_credito_de_piso() -> None:
    """Markdown de tabela dentro de um `text` não conta como bloco visual."""
    tabela_md = "| Critério | Antes | Depois |\n| --- | --- | --- |\n| Custo | 10 | 4 |"
    sections = [bloco_texto(f"{prosa(900)}\n\n{tabela_md}"), bloco_figura(1), bloco_figura(2)]
    erros = check_visual_density(sections, "módulo")
    pisos = [e for e in erros if "min_visual_blocks_per_module" in e.mensagem]
    assert len(pisos) == 1
    assert "2 bloco(s) visual(is)" in pisos[0].mensagem


# ─── 3. Densidade ────────────────────────────────────────────────────

def test_modulo_longo_com_tres_visuais_falha_na_densidade() -> None:
    """20 mil caracteres de prosa pedem 8 blocos visuais, não 3."""
    paragrafos = "\n\n".join(prosa(1000) for _ in range(20))
    erros = check_visual_density([bloco_texto(paragrafos), *tres_visuais()], "Módulo 7")

    densidade = [e for e in erros if "chars_per_visual_block" in e.mensagem]
    assert len(densidade) == 1
    assert densidade[0].tipo == "warning"
    assert "Módulo 7" in densidade[0].mensagem
    assert "20000 caracteres de prosa" in densidade[0].mensagem
    assert "pede 8" in densidade[0].mensagem


def test_modulo_curto_com_tres_visuais_passa() -> None:
    """Módulo curto com o piso cumprido não gera nenhum achado."""
    erros = check_visual_density([bloco_texto(prosa(900)), *tres_visuais()], "Módulo 2")
    assert erros == []


# ─── 4. Os números saem do YAML ──────────────────────────────────────

YAML_APERTADO = """
validation:
  visual_density:
    enabled: true
    required_for_new_course: true
    max_paragraph_chars: 300
    min_visual_blocks_per_module: 5
    chars_per_visual_block: 200
"""

YAML_FROUXO = """
validation:
  visual_density:
    enabled: true
    required_for_new_course: true
    max_paragraph_chars: 5000
    min_visual_blocks_per_module: 1
    chars_per_visual_block: 100000
"""


def test_numeros_saem_do_yaml_e_o_veredito_muda(yaml_customizado) -> None:
    """O mesmo módulo passa com um YAML e reprova com outro.

    Prova mecânica de que teto, piso e densidade são lidos da configuração.
    Se alguém devolver qualquer um dos três a constante de código, este teste
    fica vermelho no mesmo instante.
    """
    sections = [bloco_texto(prosa(900)), *tres_visuais()]

    yaml_customizado(YAML_FROUXO)
    assert check_visual_density(sections, "módulo") == []

    yaml_customizado(YAML_APERTADO)
    erros = check_visual_density(sections, "módulo")
    texto = mensagens(erros)
    # Teto de 300: o parágrafo de 900 agora estoura.
    assert "acima do teto de 300" in texto
    # Piso de 5: os 3 visuais agora faltam.
    assert "piso de 5" in texto
    # Densidade de 1 bloco a cada 200 caracteres: 900 de prosa pedem 5.
    assert "a cada 200 caracteres" in texto
    assert "pede 5" in texto


def test_valor_ilegivel_no_yaml_cai_no_fallback_sem_explodir(yaml_customizado) -> None:
    """Limite escrito como texto não derruba o checador."""
    yaml_customizado(
        "validation:\n"
        "  visual_density:\n"
        "    enabled: true\n"
        "    max_paragraph_chars: muito\n"
        "    min_visual_blocks_per_module: 3\n"
        "    chars_per_visual_block: 2500\n"
    )
    erros = check_visual_density([bloco_texto(prosa(1500)), *tres_visuais()], "módulo")
    assert "acima do teto de 1200" in mensagens(erros)


# ─── 5. Camada ausente ou desligada ──────────────────────────────────

def test_camada_ausente_nao_derruba_e_avisa(yaml_customizado) -> None:
    yaml_customizado("validation:\n  content_quality:\n    enabled: true\n")
    erros = check_visual_density([bloco_texto(prosa(9000))], "Módulo 4")
    assert all(e.tipo == "warning" for e in erros)
    assert len(erros) == 1
    assert "NÃO foi cobrada" in erros[0].mensagem
    assert "Módulo 4" in erros[0].mensagem


def test_camada_desligada_nao_cobra_e_diz_no_relatorio(yaml_customizado) -> None:
    yaml_customizado(
        "validation:\n  visual_density:\n    enabled: false\n    max_paragraph_chars: 10\n"
    )
    erros = check_visual_density([bloco_texto(prosa(9000))], "Módulo 5")
    assert len(erros) == 1
    assert erros[0].tipo == "warning"
    assert "desligada" in erros[0].mensagem


def test_yaml_inexistente_nao_derruba(monkeypatch: pytest.MonkeyPatch) -> None:
    """Config sumida degrada com aviso, sem levantar exceção."""
    monkeypatch.setattr(
        rules_loader, "RULES_PATH", PROJECT_ROOT / "config" / "nao-existe-quality-rules.yaml"
    )
    rules_loader.load_rules.cache_clear()
    erros = check_visual_density([bloco_texto(prosa(9000))], "módulo")
    rules_loader.load_rules.cache_clear()
    assert len(erros) == 1
    assert erros[0].tipo == "warning"


# ─── Curso legado ────────────────────────────────────────────────────

def test_curso_legado_recebe_aviso_no_lugar_de_erro() -> None:
    """Com `required_for_new_course: true`, o acervo publicado não fica refém."""
    sections = [bloco_texto(prosa(1500)), bloco_figura(1)]

    novos = check_visual_density(sections, "módulo", curso_novo=True)
    assert any(e.tipo == "error" for e in novos)

    legados = check_visual_density(sections, "módulo", curso_novo=False)
    assert all(e.tipo == "warning" for e in legados)
    # A dívida continua registrada, com a mesma contagem.
    assert len(legados) == len(novos)


def test_blocos_como_dicionario_sao_medidos_igual() -> None:
    """Curso carregado de JSON chega como dicionário e vale a mesma régua."""
    sections = [
        {"type": "text", "value": prosa(1500)},
        {"type": "figure", "value": "<svg></svg>", "label": "Figura 1"},
    ]
    erros = check_visual_density(sections, "módulo")
    texto = mensagens(erros)
    assert "acima do teto de 1200" in texto
    assert "1 bloco(s) visual(is)" in texto


# ─── 6. O corte que separa capítulo de trecho de apoio ────────────────

def test_modulo_curto_nao_responde_pelo_piso_de_tres() -> None:
    """Abertura e encerramento não são capítulo, e não pedem três peças.

    Exigir três figuras num módulo de meia página produz enfeite, não leitura.
    O corte é `min_prose_chars_for_floor`, e é o mesmo que o portão
    `gate-peso-visual.mjs` do landing-page-geo usa.
    """
    sections = [bloco_texto(prosa(400))]
    erros = check_visual_density(sections, "abertura")

    pisos = [e for e in erros if "min_visual_blocks_per_module" in e.mensagem]
    assert pisos == [], "módulo curto não deveria responder pelo piso"


def test_modulo_longo_sem_peca_ainda_responde_pelo_piso() -> None:
    """Passado o corte, o piso volta a valer, mesmo sem nenhuma peça."""
    sections = [bloco_texto(prosa(900))]
    erros = check_visual_density(sections, "capítulo")

    pisos = [e for e in erros if "min_visual_blocks_per_module" in e.mensagem]
    assert len(pisos) == 1
    assert pisos[0].tipo == "error"


def test_o_corte_sai_do_yaml(tmp_path, monkeypatch) -> None:
    """Mudar `min_prose_chars_for_floor` no YAML muda o veredito.

    Sem este teste o corte volta a ser constante fixa na primeira refatoração,
    que é exatamente como `max_paragraph_lines` apodreceu.
    """
    from src.validators import rules_loader

    def com_corte(valor: int):
        caminho = tmp_path / f"regras_{valor}.yaml"
        caminho.write_text(
            "validation:\n"
            "  visual_density:\n"
            "    enabled: true\n"
            "    required_for_new_course: true\n"
            "    max_paragraph_chars: 1200\n"
            "    min_visual_blocks_per_module: 3\n"
            f"    min_prose_chars_for_floor: {valor}\n"
            "    chars_per_visual_block: 2500\n",
            encoding="utf-8",
        )
        return caminho

    sections = [bloco_texto(prosa(600))]

    for corte, espera_piso in ((300, True), (5000, False)):
        monkeypatch.setattr(rules_loader, "RULES_PATH", com_corte(corte))
        rules_loader.load_rules.cache_clear()
        erros = check_visual_density(sections, "módulo")
        pisos = [e for e in erros if "min_visual_blocks_per_module" in e.mensagem]
        assert bool(pisos) is espera_piso, (
            f"com corte em {corte} o piso deveria "
            f"{'valer' if espera_piso else 'ficar de fora'}"
        )

    rules_loader.load_rules.cache_clear()


# ─── 7. A costura: a régua morde na geração ──────────────────────────

def _curso_de_prova(secoes: list) -> "object":
    """Monta um CourseDefinition mínimo em volta das seções dadas."""
    from src.models import CourseDefinition

    return CourseDefinition(
        slug="prova-peso-visual",
        titulo="Curso de prova do peso visual",
        descricao="Curso mínimo para exercitar a cobrança na geração do TSX.",
        steps=[{
            "id": "capitulo-um",
            "title": "Capítulo de prova",
            "duration": "12 min",
            "description": "Exercita a cobrança de peso visual",
            "content": secoes,
        }],
    )


def test_geracao_reprova_curso_que_nasce_como_coluna_de_texto() -> None:
    """Sem este teste a costura some numa refatoração e ninguém percebe.

    A régua só vale porque `TsxGenerator.render_page` a cobra antes de escrever
    o arquivo. Um checador que existe e não é chamado por pipeline nenhum é a
    mesma configuração declarativa que esta rodada veio consertar.
    """
    from src.generators.tsx_generator import TsxGenerator, VisualDensityError

    curso = _curso_de_prova([
        {"type": "text", "value": prosa(900)},
        {"type": "text", "value": prosa(900)},
        {"type": "checkpoint", "value": "Você consegue explicar o conceito central?"},
    ])

    with pytest.raises(VisualDensityError) as exc:
        TsxGenerator().render_page(curso)

    mensagem = str(exc.value)
    assert "capitulo-um" in mensagem
    assert "min_visual_blocks_per_module" in mensagem
    assert "DOUTRINA_VISUAL_CURSOS.md" in mensagem


def test_geracao_passa_quando_o_modulo_tem_as_pecas() -> None:
    from src.generators.tsx_generator import TsxGenerator

    curso = _curso_de_prova([
        {"type": "text", "value": prosa(900)},
        {"type": "figure", "value": "<svg role='img'></svg>", "label": "O funil"},
        {"type": "dataTable", "value": "", "data": {
            "columns": ["Régua", "Número"], "rows": [["Operador", "400"], ["Documento", "250"]]}},
        {"type": "stepGuide", "value": "", "data": {
            "title": "Instalar a medição",
            "steps": [{"label": "Criar o evento"}, {"label": "Conferir a taxa"}]}},
        {"type": "checkpoint", "value": "Você consegue nomear o evento perseguido?"},
    ])

    tsx = TsxGenerator().render_page(curso)
    assert 'case "dataTable"' in tsx
    assert "capitulo-um" in tsx


def test_modo_legado_renderiza_sem_reprovar() -> None:
    """Curso já publicado atravessa, com a dívida saindo no log."""
    from src.generators.tsx_generator import TsxGenerator

    curso = _curso_de_prova([
        {"type": "text", "value": prosa(900)},
        {"type": "text", "value": prosa(900)},
        {"type": "checkpoint", "value": "Você consegue explicar o conceito central?"},
    ])

    tsx = TsxGenerator().render_page(curso, cobrar_peso_visual=False)
    assert "capitulo-um" in tsx
