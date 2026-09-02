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
        self.course_id = ""
        #: Rastreador que recebe uma entrada por chamada, como o cliente real.
        self.tracker = None
        #: Simula a cadeia de fallback: provider declarado -> provider que atendeu.
        self.fallback: dict[str, str] = {}

    def set_course_context(self, course_id: str) -> None:
        self.course_id = course_id

    def call(self, provider: str, prompt: str, **kwargs) -> str:
        self.chamadas.append((provider, prompt))
        if self.tracker is not None:
            atendeu = self.fallback.get(provider, provider)
            self.tracker.track(atendeu, 100, 100, f"modelo-{atendeu}", 0.01, course_id=self.course_id)
        if provider == "perplexity":
            return "PESQUISA " + ("dado relevante. " * 800)
        if provider == "openai":
            if "AULAS DA TRILHA" in prompt or "TRACK LESSONS" in prompt:
                return (
                    "## O que você vai saber fazer\n\nMedir o tempo de resposta do seu WhatsApp.\n\n"
                    "## Antes de começar\n\nTer o WhatsApp Business instalado.\n\n"
                    "## Glossário\n\n**taxa de resposta**: de cada 100 mensagens, quantas foram respondidas.\n\n"
                    "## Perguntas frequentes\n\n**Preciso de chatbot?**\n\nNão. Comece pela saudação automática.\n\n"
                    "## Fontes\n\nOctadesk, CX Trends, maio de 2025.\n"
                )
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
    """Dublê antigo: só `is_over_budget`. Prova que o orquestrador ainda o aceita."""

    def is_over_budget(self, provider: str) -> bool:
        return False

    def report(self) -> str:
        return "sem custo"


class _LedgerFalso:
    """Dublê novo: ledger em memória com a API de orçamento e procedência."""

    def __init__(self, teto_sessao: float = 100.0) -> None:
        self.entradas: list[dict] = []
        self.teto_sessao = teto_sessao

    def track(self, provider, tokens_in, tokens_out, model, custo_usd, course_id="") -> None:
        self.entradas.append({"provider": provider, "model": model, "custo_usd": custo_usd, "course_id": course_id})

    def pode_chamar(self, provider: str, course_id: str = "") -> tuple[bool, str]:
        total = sum(e["custo_usd"] for e in self.entradas)
        if total >= self.teto_sessao:
            return False, f"orçamento da sessão esgotado (USD {total:.2f})"
        return True, ""

    def is_over_budget(self, provider: str) -> bool:
        return not self.pode_chamar(provider)[0]

    def indice_atual(self) -> int:
        return len(self.entradas)

    def entradas_desde(self, indice: int, course_id: str = "") -> list[dict]:
        return [e for e in self.entradas[indice:] if not course_id or e["course_id"] == course_id]

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
    # O único aviso admissível é o do quality gate (wave 2), que só relata.
    assert not [a for a in resultado.to_dict()["avisos"] if "Quality gate" not in a]


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


def _orquestrador_com_ledger(tmp_path, monkeypatch, ledger):
    import src.orchestrator as mod

    monkeypatch.setattr(mod, "DRAFTS_DIR", tmp_path)
    cliente = _ClienteFalso()
    cliente.tracker = ledger
    monkeypatch.setattr("src.llm_client.make_llm_client", lambda tracker: cliente)
    orq = Orchestrator(cost_tracker=ledger)
    orq.client = cliente
    for agente in (orq.researcher, orq.writer, orq.analyzer, orq.classifier, orq.reviewer):
        agente.client = cliente
    return orq, cliente


def test_procedencia_registra_o_modelo_que_atendeu_cada_etapa(tmp_path, monkeypatch) -> None:
    orq, cliente = _orquestrador_com_ledger(tmp_path, monkeypatch, _LedgerFalso())
    resultado = orq.run(_curso())

    assert resultado.sucesso, resultado.erros
    assert set(resultado.provedores) == {"research", "draft", "analyze", "classify", "review"}
    assert resultado.provedores["research"] == {"perplexity/modelo-perplexity": 1}
    # 2 planejamentos + 6 aulas + 2 fechamentos de trilha no writer
    assert resultado.provedores["draft"] == {"openai/modelo-openai": 10}
    assert resultado.provedores["review"] == {"anthropic/modelo-anthropic": 6}
    assert not [a for a in resultado.avisos if "fallback" in a]
    assert resultado.to_dict()["provedores"]["classify"] == {"google/modelo-google": 1}


def test_fallback_aparece_no_resultado_como_aviso(tmp_path, monkeypatch) -> None:
    orq, cliente = _orquestrador_com_ledger(tmp_path, monkeypatch, _LedgerFalso())
    cliente.fallback = {"openai": "anthropic", "perplexity": "google"}
    resultado = orq.run(_curso())

    assert resultado.sucesso, resultado.erros
    assert resultado.provedores["draft"] == {"anthropic/modelo-anthropic": 10}
    assert resultado.provedores["research"] == {"google/modelo-google": 1}
    avisos = [a for a in resultado.avisos if "rodou em fallback" in a]
    assert len(avisos) == 2
    assert any("'draft'" in a and "declarada em openai" in a for a in avisos)
    assert any("'research'" in a and "declarada em perplexity" in a for a in avisos)


def test_quality_gate_roda_ao_fim_e_grava_veredito_por_aula(tmp_path, monkeypatch) -> None:
    orq, cliente = _orquestrador_com_ledger(tmp_path, monkeypatch, _LedgerFalso())
    resultado = orq.run(_curso())

    assert resultado.sucesso, resultado.erros
    unidades = {t for t, _ in dividir_em_unidades(resultado.etapas["review"])}
    # 6 aulas + 2 fechamentos de trilha, mais a camada GEO do curso inteiro.
    assert len(unidades) == 8
    assert set(resultado.gate) == unidades | {"curso"}
    for nome, veredito in resultado.gate.items():
        assert veredito["aprovado"] in (True, False)
        assert isinstance(veredito["erros"], list)
        if nome != "curso":
            # A camada GEO não é cobrada por aula (fontes vivem na trilha).
            assert not any("[geo]" in e for e in veredito["erros"]), nome
    assert resultado.etapas["gate_report"].startswith("Quality gate: ")
    assert resultado.gate_aprovado in (True, False)
    if resultado.gate_aprovado is False:
        assert any("Quality gate" in a for a in resultado.avisos)
    assert resultado.to_dict()["gate"] == resultado.gate


def test_gate_nao_roda_quando_o_pipeline_falha(tmp_path, monkeypatch) -> None:
    orq, cliente = _orquestrador_com_ledger(tmp_path, monkeypatch, _LedgerFalso(teto_sessao=0.09))
    resultado = orq.run(_curso())
    assert not resultado.sucesso
    assert resultado.gate == {} and resultado.gate_aprovado is None
    assert "gate_report" not in resultado.etapas


def test_orcamento_da_sessao_interrompe_com_motivo(tmp_path, monkeypatch) -> None:
    # pesquisa (0,01) + planejamento e fechamento do módulo 1 + 6 aulas = 0,09;
    # o fechamento da trilha 2 e a análise não cabem.
    orq, cliente = _orquestrador_com_ledger(tmp_path, monkeypatch, _LedgerFalso(teto_sessao=0.09))
    resultado = orq.run(_curso())

    assert not resultado.sucesso
    assert "research" in resultado.etapas and "draft" in resultado.etapas
    assert "analyze" not in resultado.etapas
    assert any("orçamento da sessão esgotado" in e and "'analyze'" in e for e in resultado.erros)


def test_fechamento_da_trilha_vem_depois_das_aulas_e_nao_passa_pela_revisao(tmp_path, monkeypatch) -> None:
    orq, cliente = _orquestrador_com_ledger(tmp_path, monkeypatch, _LedgerFalso())
    resultado = orq.run(_curso())

    assert resultado.sucesso, resultado.erros
    draft = resultado.etapas["draft"]
    titulos = [t for t, _ in dividir_em_unidades(draft)]
    assert titulos == [
        "Aula 1.1: Por que o cliente some", "Aula 1.2: Como responder em cinco minutos",
        "Aula 1.3: Faça agora com o seu WhatsApp", "Trilha 1: Resposta rápida",
        "Aula 2.1: Por que o cliente some", "Aula 2.2: Como responder em cinco minutos",
        "Aula 2.3: Faça agora com o seu WhatsApp", "Trilha 2: Mensagem que traz de volta",
    ]
    trilha = dict(dividir_em_unidades(draft))["Trilha 1: Resposta rápida"]
    for secao in ("## O que você vai saber fazer", "## Glossário", "## Perguntas frequentes", "## Fontes"):
        assert secao in trilha
    # O prompt da trilha recebe as aulas do módulo e os títulos na ordem.
    prompt_trilha = next(p for prov, p in cliente.chamadas if prov == "openai" and "AULAS DA TRILHA" in p)
    assert "1.1 Por que o cliente some; 1.2 Como responder" in prompt_trilha
    assert "# Aula 1.3:" in prompt_trilha and "# Aula 2.1:" not in prompt_trilha
    # A revisão pula as trilhas (6 aulas revisadas, não 8) e o texto revisado as preserva.
    assert len([p for prov, p in cliente.chamadas if prov == "anthropic"]) == 6
    assert "# Trilha 2: Mensagem que traz de volta" in resultado.etapas["review"]
    # O gate não aplica a régua da aula ao fechamento da trilha.
    assert "Trilha 1: Resposta rápida" in resultado.gate
    assert not any("exercício" in e for e in resultado.gate["Trilha 1: Resposta rápida"]["erros"])


def test_parser_trata_a_trilha_como_bloco_proprio() -> None:
    md = "# Aula 1.1: Primeira\n\n## Por que\n\ntexto\n\n# Trilha 1: Módulo\n\n## Glossário\n\n**x**: y"
    blocos = extract_module_blocks(md)
    assert [t for t, _ in blocos] == ["Aula 1.1: Primeira", "Trilha 1: Módulo"]
    assert [t for t, _ in dividir_em_unidades(md)] == ["Aula 1.1: Primeira", "Trilha 1: Módulo"]


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
