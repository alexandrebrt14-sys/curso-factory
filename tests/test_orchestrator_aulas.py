"""Geração por aula, insumo correto por etapa e revisão que devolve texto.

Cobre os três defeitos corrigidos em 02/09/2026 no orquestrador:
o writer recebia um módulo inteiro (e 3.000 caracteres de pesquisa); a
classificação e a revisão recebiam a saída da etapa anterior em vez do
rascunho; a revisão em bloco devolvia comentário no lugar do texto.
"""

from __future__ import annotations

import re

import pytest

from src.converters.draft_to_course import _extract_review_or_draft_text
from src.models import Course, Module, NivelCurso, Step
from src.orchestrator import (
    Orchestrator,
    PipelineResult,
    dividir_em_unidades,
    separar_relatorio_de_revisao,
)
from src.parsers import extract_module_blocks


class _ClienteFalso:
    """Registra cada chamada e responde conforme o provider."""

    def __init__(self) -> None:
        self.chamadas: list[tuple[str, str]] = []
        self.revisao_encolhe = False

    def set_course_context(self, course_id: str) -> None:
        self.course_id = course_id

    def call(self, provider: str, prompt: str, **kwargs) -> str:
        self.chamadas.append((provider, prompt))
        if provider == "perplexity":
            return "PESQUISA " + ("dado relevante. " * 800)
        if provider == "openai":
            if "Planeje de" in prompt:
                return (
                    "1. Por que o cliente some | A ideia de tempo de resposta\n"
                    "2. Como responder em cinco minutos | Roteiro de resposta\n"
                    "3. Faça agora com o seu WhatsApp | Exercício aplicado\n"
                )
            m = re.search(r"Esta aula: \*\*([^*]+)\*\*", prompt)
            titulo = m.group(1) if m else "aula"
            return (
                f"Você vai aprender a responder mais rápido ({titulo}).\n\n"
                "## Por que responder rápido muda o seu resultado\n\n"
                + ("Texto explicativo com frase direta e exemplo do balcão. " * 40)
                + "\n\n## Como fica no seu negócio\n\n"
                + ("A oficina do bairro respondeu em cinco minutos e fechou a venda. " * 30)
                + "\n\n## Faça agora\n\n1. Abra o WhatsApp e anote o horário.\n"
                "2. Responda a última mensagem sem resposta.\n\n"
                "**Resultado esperado:** uma resposta enviada em menos de cinco minutos."
            )
        if provider == "google":
            # O mesmo provider atende a análise (gemini pro) e a classificação
            # (gemini flash) desde o alinhamento ao catálogo do geo-orchestrator.
            if "Classificações obrigatórias" in prompt or "classificar" in prompt:
                return '{"nivel": "iniciante", "tags": ["whatsapp"]}'
            return '{"score": 80, "aprovado": true, "melhorias_prioritarias": ["nada"]}'
        if provider == "anthropic":
            texto = prompt.split("--- AULA PARA REVISÃO ---", 1)[-1].strip()
            if self.revisao_encolhe:
                return "Revisado. Aprovado.\n\n---\nREVISÃO CONCLUÍDA\nAprovado para publicação: sim\n---"
            return texto.replace("Texto explicativo", "Texto revisado") + (
                "\n\n---\nREVISÃO CONCLUÍDA\nCorreções de acentuação: 0\n"
                "Aprovado para publicação: sim\n---"
            )
        raise AssertionError(f"provider inesperado: {provider}")


class _CostTrackerFalso:
    def is_over_budget(self, provider: str) -> bool:
        return False

    def report(self) -> str:
        return "sem custo"


@pytest.fixture
def orquestrador(tmp_path, monkeypatch):
    import src.orchestrator as mod

    monkeypatch.setattr(mod, "DRAFTS_DIR", tmp_path)
    cliente = _ClienteFalso()
    monkeypatch.setattr("src.llm_client.make_llm_client", lambda tracker: cliente)
    orq = Orchestrator(cost_tracker=_CostTrackerFalso())
    orq.client = cliente
    for agente in (orq.researcher, orq.writer, orq.analyzer, orq.classifier, orq.reviewer):
        agente.client = cliente
    return orq, cliente


def _curso(com_etapas: bool = False) -> Course:
    etapas = (
        [Step(titulo="Aula fixa A", conteudo="ideia A"), Step(titulo="Aula fixa B", conteudo="ideia B")]
        if com_etapas else []
    )
    return Course(
        id="whatsapp-que-vende",
        titulo="WhatsApp que vende",
        descricao="Responder rápido e fechar venda",
        nivel=NivelCurso.INICIANTE,
        modulos=[
            Module(titulo="Resposta rápida", descricao="tempo de resposta", ordem=1, etapas=etapas),
            Module(titulo="Mensagem que traz de volta", descricao="retorno", ordem=2),
        ],
    )


def test_draft_gera_uma_chamada_por_aula_com_pesquisa_inteira(orquestrador) -> None:
    orq, cliente = orquestrador
    pesquisa = "PESQUISA " + ("dado relevante. " * 800)
    draft = orq._draft_modules_iterative(_curso(), pesquisa)

    aulas = re.findall(r"^# Aula (\d+\.\d+): (.+)$", draft, flags=re.MULTILINE)
    assert [a[0] for a in aulas] == ["1.1", "1.2", "1.3", "2.1", "2.2", "2.3"]
    assert "<!-- Módulo 1: Resposta rápida -->" in draft

    chamadas_writer = [p for prov, p in cliente.chamadas if prov == "openai" and "Esta aula:" in p]
    assert len(chamadas_writer) == 6
    # A pesquisa inteira viaja no prompt (antes eram 3.000 caracteres).
    assert all(len(p.split("--- DADOS DA PESQUISA ---", 1)[1]) > 10000 for p in chamadas_writer)
    # O prompt carrega os tetos da aula lidos da fonte, não números fixos.
    assert "{palavras_alvo_min}" not in chamadas_writer[0]
    assert "Aulas anteriores do módulo: nenhuma" in chamadas_writer[0]
    assert "1.1 Por que o cliente some" in chamadas_writer[1]


def test_etapas_do_modulo_no_yaml_viram_aulas_sem_planejamento(orquestrador) -> None:
    orq, cliente = orquestrador
    curso = _curso(com_etapas=True)
    aulas = orq._plan_lessons(curso, curso.modulos[0], 1, "pesquisa")
    assert [a["titulo"] for a in aulas] == ["Aula fixa A", "Aula fixa B"]
    assert not [p for prov, p in cliente.chamadas if "Planeje de" in p]


def test_plano_ilegivel_vira_aula_unica(orquestrador) -> None:
    orq, cliente = orquestrador
    cliente.call = lambda provider, prompt, **kw: "não sei planejar"  # type: ignore[assignment]
    curso = _curso()
    aulas = orq._plan_lessons(curso, curso.modulos[1], 2, "pesquisa")
    assert aulas == [{"titulo": "Mensagem que traz de volta", "ideia": "retorno"}]


def test_pipeline_entrega_o_rascunho_a_analise_classificacao_e_revisao(orquestrador) -> None:
    orq, cliente = orquestrador
    resultado = orq.run(_curso())

    assert resultado.sucesso, resultado.erros
    draft = resultado.etapas["draft"]
    prompt_analise = next(p for prov, p in cliente.chamadas if prov == "google" and "classificar" not in p)
    prompt_classificacao = next(p for prov, p in cliente.chamadas if prov == "google" and "classificar" in p)
    prompts_revisao = [p for prov, p in cliente.chamadas if prov == "anthropic"]

    assert "# Aula 1.1:" in prompt_analise and "# Aula 2.3:" in prompt_analise
    assert "# Aula 1.1:" in prompt_classificacao
    # A revisão é aula a aula, e cada chamada recebe a aula, não o JSON anterior.
    assert len(prompts_revisao) == 6
    assert all("# Aula" in p and '"nivel"' not in p.split("--- AULA PARA REVISÃO ---")[-1] for p in prompts_revisao)
    assert "melhorias_prioritarias" in prompts_revisao[0]  # pista da análise
    # O texto revisado volta inteiro e sem o bloco de relatório.
    revisado = resultado.etapas["review"]
    assert "Texto revisado" in revisado and "REVISÃO CONCLUÍDA" not in revisado
    assert len(revisado.split()) >= len(draft.split()) * 0.9
    assert "REVISÃO CONCLUÍDA" in resultado.etapas["review_report"]
    assert resultado.to_dict()["avisos"] == []


def test_revisao_que_encolhe_mantem_o_rascunho_e_avisa(orquestrador) -> None:
    orq, cliente = orquestrador
    cliente.revisao_encolhe = True
    curso = _curso()
    draft = orq._draft_modules_iterative(curso, "pesquisa")
    resultado = PipelineResult(curso.id)

    revisado = orq._review_iterative(curso, draft, "", resultado)

    assert revisado.split() == draft.split()
    assert len(resultado.avisos) == 6
    assert "rascunho original foi mantido" in resultado.avisos[0]


def test_dividir_em_unidades_reconhece_aula_e_modulo_antigo() -> None:
    novo = "<!-- Módulo 1: X -->\n\n# Aula 1.1: Primeira\n\ncorpo\n\n# Aula 1.2: Segunda\n\ncorpo 2"
    assert [t for t, _ in dividir_em_unidades(novo)] == ["Aula 1.1: Primeira", "Aula 1.2: Segunda"]
    antigo = "# Módulo 1: A\n\n## Seção\n\ntexto\n\n---\n\n# Módulo 2: B\n\ntexto"
    assert [t for t, _ in dividir_em_unidades(antigo)] == ["Módulo 1: A", "Módulo 2: B"]
    assert dividir_em_unidades("só prosa") == [("", "só prosa")]
    assert dividir_em_unidades("   ") == []


def test_separar_relatorio_de_revisao() -> None:
    saida = "# Aula 1.1: T\n\ntexto\n\n---\nREVISÃO CONCLUÍDA\nAprovado: sim\n---"
    texto, relatorio = separar_relatorio_de_revisao(saida)
    assert texto == "# Aula 1.1: T\n\ntexto"
    assert relatorio.startswith("REVISÃO CONCLUÍDA")
    assert separar_relatorio_de_revisao("sem relatório") == ("sem relatório", "")


def test_conversor_prefere_rascunho_quando_a_revisao_e_comentario() -> None:
    draft = "# Aula 1.1: T\n\n" + ("palavra " * 500)
    etapas = {"draft": draft, "review": "Revisado. Aprovado para publicação: sim."}
    assert _extract_review_or_draft_text(etapas) == draft
    revisao_inteira = draft.replace("palavra", "revista")
    assert _extract_review_or_draft_text({"draft": draft, "review": revisao_inteira}) == revisao_inteira


def test_parser_trata_cada_aula_como_unidade() -> None:
    md = (
        "<!-- Módulo 1: X -->\n\n"
        "# Aula 1.1: Primeira\n\n## Por que\n\ntexto\n\n## Faça agora\n\n1. passo\n\n"
        "# Aula 1.2: Segunda\n\n## Por que\n\ntexto 2"
    )
    blocos = extract_module_blocks(md)
    assert [t for t, _ in blocos] == ["Aula 1.1: Primeira", "Aula 1.2: Segunda"]
    assert "## Faça agora" in blocos[0][1]
    assert "<!--" not in blocos[0][1]
