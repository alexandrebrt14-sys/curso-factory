"""Saída de referência do pipeline: prova de que refatoração pura não muda nada.

Capturada em 27/09/2026, antes da rodada de refatoração, com o pipeline inteiro
rodando sobre um cliente LLM falso (nenhuma chamada paga). Guarda cada prompt
enviado a cada etapa, na ordem, e o relatório do quality gate. Uma refatoração
que se declara pura precisa manter os dois arquivos idênticos; uma mudança de
comportamento intencional regrava a referência no mesmo commit, e o diff do
arquivo mostra ao revisor exatamente o que mudou nos prompts e no gate.

Para regravar: `REGRAVAR_REFERENCIA=1 python -m pytest tests/test_saida_de_referencia.py`.
"""

from __future__ import annotations

import os
import re
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.models import Course, Module, NivelCurso  # noqa: E402
from src.orchestrator import Orchestrator  # noqa: E402

REFERENCIA = PROJECT_ROOT / "tests" / "fixtures" / "referencia"


class _Rastreador:
    def track(self, *a, **k) -> None:
        return None

    def is_over_budget(self, provider: str) -> bool:
        return False

    def report(self) -> str:
        return ""


class _ClienteFalso:
    """Responde de forma determinística e registra cada prompt."""

    def __init__(self) -> None:
        self.chamadas: list[tuple[str, str]] = []

    def set_course_context(self, course_id: str) -> None:
        return None

    def call(self, provider: str, prompt: str, **kwargs) -> str:
        self.chamadas.append((provider, prompt))
        if provider == "perplexity":
            return "PESQUISA: o tempo de resposta do WhatsApp decide a venda. " * 20
        if provider == "openai":
            if "AULAS DA TRILHA" in prompt:
                return "## Fontes\n\nOctadesk, CX Trends, maio de 2025.\n"
            if "Planeje de" in prompt:
                return "1. Por que o cliente some | tempo de resposta\n2. Responder em cinco minutos | roteiro\n"
            m = re.search(r"Esta aula: \*\*([^*]+)\*\*", prompt)
            titulo = m.group(1) if m else "aula"
            return (
                f"Responda o cliente antes que ele desista ({titulo}).\n\n"
                + ("A oficina perde a venda quando a resposta demora. " * 6)
                + "\n\n## Por que responder rápido muda o seu resultado\n\n"
                + ("Texto explicativo com frase direta e exemplo do balcão. " * 30)
                + "\n\n## Como a oficina do bairro fechou a venda\n\n"
                + ("A oficina respondeu em cinco minutos e fechou a venda de R$ 300. " * 20)
                + "\n\nAbra o WhatsApp e anote o horário da próxima mensagem sem resposta."
            )
        if provider == "google":
            if "classificar" in prompt or "Classificações obrigatórias" in prompt:
                return '{"nivel": "iniciante", "tags": ["whatsapp"]}'
            return '{"score": 80, "aprovado": true}'
        texto = prompt.split("--- AULA PARA REVISÃO ---", 1)[-1].strip()
        return texto + "\n\n---\nREVISÃO CONCLUÍDA\nAprovado para publicação: sim\n---"


def _rodar(tmp_path, monkeypatch) -> tuple[str, str]:
    cliente = _ClienteFalso()
    monkeypatch.setattr("src.llm_client.make_llm_client", lambda tracker: cliente)
    orq = Orchestrator(cost_tracker=_Rastreador(), drafts_dir=tmp_path)
    for agente in (orq.researcher, orq.writer, orq.analyzer, orq.classifier, orq.reviewer):
        agente.client = cliente
    orq.client = cliente
    curso = Course(
        id="whatsapp-que-vende",
        titulo="WhatsApp que vende",
        descricao="Responder rápido e fechar venda",
        nivel=NivelCurso.INICIANTE,
        tags=["whatsapp", "vendas"],
        modulos=[Module(titulo="Resposta rápida", descricao="tempo de resposta", ordem=1)],
    )
    resultado = orq.run(curso)
    assert resultado.sucesso, resultado.erros
    prompts = "\n\n======== CHAMADA ========\n\n".join(
        f"[{provider}]\n{prompt}" for provider, prompt in cliente.chamadas
    )
    gate = resultado.etapas.get("gate_report", "")
    return prompts + "\n", gate + "\n"


def _comparar(nome: str, atual: str) -> None:
    arquivo = REFERENCIA / nome
    if os.environ.get("REGRAVAR_REFERENCIA"):
        REFERENCIA.mkdir(parents=True, exist_ok=True)
        arquivo.write_text(atual, encoding="utf-8", newline="\n")
    esperado = arquivo.read_text(encoding="utf-8")
    assert atual == esperado, (
        f"A saída de {nome} mudou. Se a mudança é intencional, regrave a referência "
        f"(REGRAVAR_REFERENCIA=1) no mesmo commit e explique no commit o que mudou."
    )


def test_prompts_e_gate_do_pipeline_batem_com_a_referencia(tmp_path, monkeypatch) -> None:
    prompts, gate = _rodar(tmp_path, monkeypatch)
    _comparar("prompts_do_pipeline.txt", prompts)
    _comparar("relatorio_do_gate.txt", gate)


def test_prompt_de_aula_guarda_o_prefixo_estavel_para_o_cache(tmp_path, monkeypatch) -> None:
    """Regras e pesquisa primeiro, o que muda por aula no fim (27/09/2026).

    O cache automático de prompt só aproveita prefixo idêntico. Com as
    variáveis da aula no topo, cada aula pagava de novo as regras e a pesquisa.
    Aqui se prova que duas aulas do mesmo curso compartilham tudo até
    "--- ESTA AULA ---", e que nenhuma variável da aula aparece antes disso.
    """
    prompts, _ = _rodar(tmp_path, monkeypatch)
    chamadas = prompts.split("\n\n======== CHAMADA ========\n\n")
    aulas = [c for c in chamadas if c.startswith("[openai]") and "--- ESTA AULA ---" in c]
    assert len(aulas) >= 2
    corte = aulas[0].index("--- ESTA AULA ---")
    assert aulas[1][:corte] == aulas[0][:corte]
    assert "Esta aula: **" not in aulas[0][:corte]
    assert corte > 0.8 * len(aulas[0])
