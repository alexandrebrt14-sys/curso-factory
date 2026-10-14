"""Curso em JSON do portal /educacao: validador, exportador e cache de pesquisa (14/10/2026).

O validador espelha `src/lib/educacao/conteudo/schema.ts` do landing-page-geo
(`config/schema-curso.json`) e os limites do portal (teto de 900 KB por página,
acentos, emoji, linguagem do bloco de código). Os testes usam um curso pequeno
no formato real e o resultado de `exportar_curso_json` sobre a fixture da fábrica.
"""

from __future__ import annotations

import copy
import json
import sys
import time
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import src.cache as cache_mod
from src.generators.json_exporter import curso_para_portal, exportar_curso_json, manifesto_de_midia
from src.models import CourseDefinition
from src.validators import curso_json_checker as checker
from src.validators.curso_json_checker import SECTION_TYPES, validar_arquivo, validar_curso

FIXTURES_DIR = Path(__file__).resolve().parent / "fixtures"
SCHEMA_PATH = PROJECT_ROOT / "config" / "schema-curso.json"


def _curso_minimo() -> list[dict]:
    return [
        {
            "id": "decisao-executiva",
            "title": "A decisão que antecede o curso",
            "duration": "12 min",
            "icon": "brain",
            "description": "O que decidir antes de abrir a primeira ferramenta.",
            "content": [
                {
                    "type": "text",
                    "value": "A autoridade temática é medida pela cobertura de um assunto.",
                },
                {"type": "code", "value": "print('olá')", "language": "python"},
                {
                    "type": "dataTable",
                    "value": "",
                    "data": {
                        "columns": ["Opção", "Custo"],
                        "rows": [["A", "R$ 10"], ["B", "R$ 20"]],
                    },
                },
            ],
            "faq": [
                {"q": "Vale para loja física?", "a": "Vale, com a mesma condição de cobertura."}
            ],
        },
        {
            "id": "mapa-de-demanda",
            "title": "Mapa de demanda",
            "duration": "18 min",
            "icon": "search",
            "description": "Como achar as perguntas que o cliente faz.",
            "content": [
                {
                    "type": "text",
                    "value": "Comece pelo Search Console e anote a origem de cada pergunta.",
                }
            ],
        },
    ]


# ─── schema espelhado ────────────────────────────────────────────────


def test_espelho_do_schema_registra_origem_e_tipos() -> None:
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    assert schema["origem"]["arquivo"] == "src/lib/educacao/conteudo/schema.ts"
    assert schema["origem"]["copiado_em"] == "2026-10-14"
    assert tuple(schema["$defs"]["sectionType"]["enum"]) == SECTION_TYPES
    assert len(SECTION_TYPES) == 39
    assert schema["$defs"]["step"]["additionalProperties"] is False
    assert schema["$defs"]["section"]["additionalProperties"] is False


def test_curso_minimo_passa_no_validador_e_no_jsonschema() -> None:
    curso = _curso_minimo()
    res = validar_curso(curso)
    assert res.aprovado, [str(a) for a in res.erros]
    assert res.medidas["capitulos"] == 2
    jsonschema = pytest.importorskip("jsonschema")
    jsonschema.validate(curso, json.loads(SCHEMA_PATH.read_text(encoding="utf-8")))


@pytest.mark.parametrize(
    ("mutacao", "regra"),
    [
        (lambda c: c[0].__setitem__("extra", 1), "schema"),
        (lambda c: c[0]["content"][0].__setitem__("foo", "x"), "schema"),
        (lambda c: c[0]["content"][0].__setitem__("type", "video"), "schema"),
        (lambda c: c[0].pop("icon"), "schema"),
        (lambda c: c[1].__setitem__("id", "decisao-executiva"), "ids-unicos"),
        (lambda c: c[1].__setitem__("id", "Decisão Executiva"), "id-ascii"),
        (lambda c: c[0]["content"][1].pop("language"), "code-language"),
        (
            lambda c: c[0]["content"][0].__setitem__("value", "Parabéns \U0001f389 pela aula"),
            "emoji",
        ),
        (lambda c: c[0]["content"][2].__setitem__("data", {"n": float("nan")}), "schema"),
    ],
)
def test_reprova_o_que_o_portal_reprova(mutacao, regra: str) -> None:
    curso = _curso_minimo()
    mutacao(curso)
    res = validar_curso(curso)
    assert not res.aprovado
    assert regra in {a.regra for a in res.erros}, [str(a) for a in res.erros]


def test_curso_vazio_ou_nao_lista_reprova() -> None:
    assert not validar_curso([]).aprovado
    assert not validar_curso({"id": "x"}).aprovado


# ─── limites do portal ───────────────────────────────────────────────


def test_capitulo_aberto_acima_do_teto_reprova_e_os_demais_so_avisam() -> None:
    curso = _curso_minimo()
    curso[0]["content"][0]["value"] = "a" * 80_000
    res = validar_curso(curso)
    assert "peso-capitulo-aberto" in {a.regra for a in res.erros}

    curso = _curso_minimo()
    curso[1]["content"][0]["value"] = "a" * 90_000
    res = validar_curso(curso)
    assert res.aprovado
    assert "peso-capitulo" in {a.regra for a in res.avisos}


def test_acentos_contam_so_texto_de_leitura_e_respeitam_o_teto_de_pr_grande() -> None:
    curso = _curso_minimo()
    frase = "A publicacao do numero e a opcao do usuario. "
    curso[0]["content"][0]["value"] = frase * 8  # mais de 20 palavras sem acento
    curso[0]["content"][1]["value"] = "numero = opcao  # codigo nao conta"
    curso[0]["content"][2]["data"]["note"] = "veja /educacao/publicacao-numero e `opcao`"
    res = validar_curso(curso)
    assert 20 < res.medidas["acentos"] <= 32
    assert "acentos" in {a.regra for a in res.erros}

    res_grande = validar_curso(curso, linhas=1200)
    assert res_grande.medidas["acentos_teto"] == 80
    assert res_grande.aprovado


def test_sigla_em_caixa_alta_nao_conta_como_acento() -> None:
    curso = _curso_minimo()
    curso[0]["content"][0]["value"] = "Os AI Overviews mudaram a página de resultados."
    assert validar_curso(curso).medidas["acentos"] == 0


def test_avisos_de_qualidade_escrita_icone_figuras_e_contrato() -> None:
    curso = _curso_minimo()
    curso[0]["content"][0]["value"] = (
        "Não se trata de volume, trata-se de cobertura. Além disso, meça."
    )
    curso[0]["icon"] = "iconeInventado"
    curso[0]["content"].extend(
        {"type": "figure", "value": "<svg></svg>", "label": "f"} for _ in range(4)
    )
    res = validar_curso(
        curso,
        glossario={
            "decisao-executiva": [{"term": "cobertura", "def": "quantos subtemas o site responde"}]
        },
        contrato={
            "min_capitulos": 25,
            "midia_capitulo_1": True,
            "glossario_obrigatorio": True,
            "guia_por_capitulo": True,
        },
    )
    regras = {a.regra for a in res.avisos}
    assert {"escrita", "icone", "figuras", "contrato-guia", "contrato-glossario"} <= regras
    erros = {a.regra for a in res.erros}
    assert {"contrato-capitulos", "contrato-midia-cap1"} <= erros


def test_glossario_com_aula_inexistente_reprova() -> None:
    res = validar_curso(
        _curso_minimo(), glossario={"aula-que-nao-existe": [{"term": "a", "def": "b"}]}
    )
    assert "glossario" in {a.regra for a in res.erros}


# ─── arquivo real e script ───────────────────────────────────────────


def test_validar_arquivo_le_o_sidecar_ao_lado(tmp_path: Path) -> None:
    curso = tmp_path / "meu-curso.json"
    curso.write_text(json.dumps(_curso_minimo(), ensure_ascii=False, indent=2), encoding="utf-8")
    (tmp_path / "meu-curso.glossario.json").write_text(
        json.dumps({"mapa-de-demanda": [{"term": "demanda", "def": "o que as pessoas procuram"}]}),
        encoding="utf-8",
    )
    res = validar_arquivo(curso)
    assert res.aprovado, [str(a) for a in res.erros]
    assert res.medidas["bytes_arquivo"] > 0

    (tmp_path / "meu-curso.glossario.json").write_text(json.dumps({"x": []}), encoding="utf-8")
    assert not validar_arquivo(curso).aprovado


def test_script_sai_com_1_quando_reprova(tmp_path: Path, capsys) -> None:
    sys.path.insert(0, str(PROJECT_ROOT / "scripts"))
    import validar_curso_json

    bom = tmp_path / "bom.json"
    bom.write_text(json.dumps(_curso_minimo(), ensure_ascii=False), encoding="utf-8")
    assert validar_curso_json.main([str(bom)]) == 0
    assert "APROVADO" in capsys.readouterr().out

    ruim = copy.deepcopy(_curso_minimo())
    ruim[0]["content"][1].pop("language")
    arquivo = tmp_path / "ruim.json"
    arquivo.write_text(json.dumps(ruim, ensure_ascii=False), encoding="utf-8")
    assert validar_curso_json.main([str(arquivo), "--json"]) == 1
    saida = json.loads(capsys.readouterr().out)
    assert saida[0]["aprovado"] is False
    assert saida[0]["erros"][0]["regra"] == "code-language"


# ─── exportador ──────────────────────────────────────────────────────


def _fixture() -> CourseDefinition:
    dados = json.loads((FIXTURES_DIR / "sample_course.json").read_text(encoding="utf-8"))
    return CourseDefinition(**dados)


def test_exportador_emite_steps_na_ordem_do_portal_sem_opcional_vazio() -> None:
    steps = curso_para_portal(_fixture())
    assert list(steps[0].keys())[:6] == [
        "id",
        "title",
        "duration",
        "icon",
        "description",
        "content",
    ]
    assert steps[0]["icon"] == "trendUp"  # trendingUp da fábrica vira a chave do portal
    for step in steps:
        for secao in step["content"]:
            assert "language" not in secao or secao["language"]
            assert secao.get("label") != ""
            assert "codeHtml" not in secao
    # fontes do rodapé viram bloco `fontes` no último capítulo; FAQ vai junto
    assert steps[-1]["content"][-1]["type"] == "fontes"
    assert steps[-1]["faq"][0]["q"]
    assert validar_curso(steps).aprovado


def test_exportador_grava_os_quatro_arquivos_e_filtra_glossario(tmp_path: Path) -> None:
    course = _fixture()
    caminhos = exportar_curso_json(
        course,
        tmp_path,
        glossario={
            course.steps[0].id: [{"term": "pipeline", "def": "sequência de etapas"}],
            "orfao": [],
        },
    )
    assert caminhos["curso"].name == f"{course.slug}.json"
    assert json.loads(caminhos["glossario"].read_text(encoding="utf-8")) == {
        course.steps[0].id: [{"term": "pipeline", "def": "sequência de etapas"}]
    }
    assert caminhos["curso"].read_text(encoding="utf-8").endswith("]\n")
    assert "carregarCurso(SLUG_DO_CURSO)" in caminhos["steps"].read_text(encoding="utf-8")
    assert json.loads(caminhos["midia"].read_text(encoding="utf-8")) == manifesto_de_midia(course)
    assert validar_arquivo(caminhos["curso"]).aprovado


def test_manifesto_de_midia_le_img_e_svg() -> None:
    course = _fixture()
    dados = course.model_dump()
    dados["steps"][0]["content"].append(
        {
            "type": "figure",
            "value": '<img src="/educacao/x/fig.webp" alt="Funil de três etapas" width="960" height="540">',
            "label": "Funil",
        }
    )
    dados["steps"][0]["content"].append(
        {"type": "figure", "value": "<svg role='img'></svg>", "label": "Mapa"}
    )
    itens = manifesto_de_midia(CourseDefinition(**dados))
    assert itens[0]["src"] == "/educacao/x/fig.webp" and itens[0]["alt"] == "Funil de três etapas"
    assert itens[0]["width"] == "960" and itens[0]["inline_svg"] is False
    assert itens[1]["inline_svg"] is True


# ─── cache de pesquisa por tópico ────────────────────────────────────


@pytest.fixture
def cache_isolado(tmp_path, monkeypatch):
    monkeypatch.setattr(cache_mod, "CACHE_DIR", tmp_path)
    return tmp_path


def test_pesquisa_tem_ttl_proprio_mais_longo(cache_isolado, monkeypatch) -> None:
    cache = cache_mod.Cache(ttl=10, ttl_por_provider={"perplexity": 1000})
    assert cache.ttl_de("perplexity") == 1000
    assert cache.ttl_de("openai") == 10
    cache.set("tema", "perplexity", "sonar", "pesquisa")
    cache.set("tema", "openai", "gpt", "redacao")
    agora = time.time()
    monkeypatch.setattr(cache_mod.time, "time", lambda: agora + 100)
    assert cache.get("tema", "perplexity", "sonar") == "pesquisa"
    assert cache.get("tema", "openai", "gpt") is None


def test_ttl_padrao_de_pesquisa_vem_da_configuracao(cache_isolado) -> None:
    cache = cache_mod.Cache()
    assert cache.ttl_de("perplexity") == cache_mod.CACHE_TTL_PESQUISA_SECONDS
    assert cache.ttl_de("perplexity") >= cache.ttl


def test_checker_defaults_batem_com_o_yaml() -> None:
    limites = checker.carregar_limites()
    assert limites["capitulo_aberto_erro_chars"] == 72_000
    assert limites["acentos_max_ocorrencias"] == 20
    assert "python" in limites["linguagens_de_codigo"]
    assert "trendUp" in limites["icones"]
