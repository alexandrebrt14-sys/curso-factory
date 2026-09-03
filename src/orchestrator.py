"""Orquestrador do pipeline de criação de cursos em 5 etapas.

Etapas:
1. Research (Perplexity): busca dados atualizados sobre o tema
2. Draft (GPT-4o): gera o conteúdo, UMA AULA POR CHAMADA
3. Analyze (Gemini): revisa qualidade e coerência do rascunho
4. Classify (Groq): classifica nível, tags, pré-requisitos a partir do rascunho
5. Review (Claude): revisão final, UMA AULA POR CHAMADA, devolvendo o texto

Três defeitos corrigidos em 02/09/2026, todos medidos nos drafts de
`output/drafts/`:

- **Insumo errado.** As etapas eram encadeadas pela saída da anterior: a
  classificação recebia o JSON da análise e a revisão recebia o JSON da
  classificação. O revisor nunca via o curso e devolvia um relatório de
  ~1.000 palavras ("aguardando conteúdo completo dos módulos"), que o
  conversor preferia ao rascunho. Agora cada etapa recebe o rascunho.
- **Unidade grande demais por chamada.** O writer recebia um módulo inteiro
  (4 a 6 aulas) para escrever numa única resposta, com teto de 16.384 tokens
  de saída, e só 3.000 caracteres da pesquisa. Saía truncado e raso. Agora a
  unidade de geração é a aula, com a pesquisa inteira no prompt.
- **Revisão em bloco.** O revisor recebia o curso inteiro e não tinha como
  devolver 15 mil palavras revisadas em 16 mil tokens. Agora revisa aula a
  aula, e uma resposta que encolhe o texto (comentário no lugar do conteúdo)
  é descartada em favor do rascunho, com aviso no resultado.

Formato do rascunho montado: cada aula começa com `# Aula i.j: título` (H1)
e usa H2 para as próprias seções, como manda o molde D da fonte de estilo.
O parser (`src/parsers/markdown_parser.py`) reconhece esse H1 como fronteira
de unidade.
"""

from __future__ import annotations

import json
import logging
import re
from collections.abc import Callable
from datetime import UTC, datetime
from pathlib import Path
from typing import TYPE_CHECKING, Any

from src.agents.analyzer import Analyzer
from src.agents.classifier import Classifier
from src.agents.researcher import Researcher
from src.agents.reviewer import Reviewer
from src.agents.writer import Writer
from src.config import (
    CLASSIFY_CONTEXT_CHARS,
    DRAFT_RESEARCH_CONTEXT_CHARS,
    OUTPUT_DIR,
    REVIEW_ANALYSIS_CHARS,
    REVIEW_MIN_RATIO,
    TRAIL_LESSONS_CHARS,
    TRAIL_RESEARCH_CHARS,
)
from src.cost_tracker import CostTracker
from src.models import Course, Module

if TYPE_CHECKING:
    from src.clients.context import ClientContext

logger = logging.getLogger(__name__)

DRAFTS_DIR = OUTPUT_DIR / "drafts"

#: Cabeçalho que abre cada aula no rascunho montado.
AULA_H1_RE = re.compile(r"^#\s+Aula\s+(\d+)\.(\d+)\s*[:.\-]\s*(.+?)\s*$", re.MULTILINE)
#: Cabeçalho do fechamento da trilha (objetivos, pré-requisitos, glossário,
#: FAQ e fontes), emitido uma vez por módulo, depois da última aula.
TRILHA_H1_RE = re.compile(r"^#\s+Trilha\s+(\d+)\s*[:.\-]\s*(.+?)\s*$", re.MULTILINE)
#: Qualquer unidade do rascunho novo: aula ou fechamento da trilha.
UNIDADE_H1_RE = re.compile(r"^#\s+(?:Aula\s+\d+\.\d+|Trilha\s+\d+)\s*[:.\-]", re.MULTILINE)
#: Cabeçalho de módulo dos rascunhos antigos (antes de 02/09/2026).
MODULO_H1_RE = re.compile(r"^#\s+M[óo]dulo\s+\d+\s*[:.\-]", re.MULTILINE)
#: Marcador de módulo que o orquestrador emite antes da primeira aula de cada módulo.
MODULO_COMENTARIO_RE = re.compile(r"<!--\s*M[óo]dulo[^\n]*-->\s*$")
#: Bloco de relatório que o revisor anexa ao fim do texto revisado.
RELATORIO_REVISAO_RE = re.compile(
    r"\n-{3,}\s*\n\s*(?:REVIS[ÃA]O CONCLU[ÍI]DA|REVIEW COMPLETE|REVISI[ÓO]N CONCLUIDA)[\s\S]*$",
    re.IGNORECASE,
)
#: Linha de plano de aulas: `1. Título | ideia em uma frase`.
PLANO_LINHA_RE = re.compile(r"^\s*(\d{1,2})[.)]\s*(.+?)(?:\s*\|\s*(.+?))?\s*$")


class PipelineResult:
    """Resultado completo de uma execução do pipeline."""

    def __init__(self, course_id: str) -> None:
        self.course_id = course_id
        self.etapas: dict[str, str] = {}
        self.erros: list[str] = []
        self.avisos: list[str] = []
        #: Por etapa, quantas chamadas cada "provedor/modelo" de fato atendeu.
        #: É o que diz se a etapa rodou no modelo declarado ou em fallback.
        self.provedores: dict[str, dict[str, int]] = {}
        #: Veredito do quality gate por aula, gravado ao fim do pipeline:
        #: `{titulo: {"aprovado": bool, "erros": [...], "avisos": n}}`.
        self.gate: dict[str, dict[str, Any]] = {}
        self.sucesso: bool = False

    def to_dict(self) -> dict[str, Any]:
        return {
            "course_id": self.course_id,
            "timestamp": datetime.now(UTC).isoformat(),
            "etapas": self.etapas,
            "erros": self.erros,
            "avisos": self.avisos,
            "provedores": self.provedores,
            "gate": self.gate,
            "sucesso": self.sucesso,
        }

    @property
    def gate_aprovado(self) -> bool | None:
        """True se toda aula passou, False se alguma reprovou, None se o gate não rodou."""
        if not self.gate:
            return None
        return all(v.get("aprovado") for v in self.gate.values())


def dividir_em_unidades(texto: str) -> list[tuple[str, str]]:
    """Divide o rascunho montado em (título, texto) por aula.

    Reconhece `# Aula i.j: título`; para rascunho antigo, `# Módulo n:`. Sem
    nenhum dos dois, devolve o texto inteiro como uma unidade. O texto de cada
    unidade inclui o próprio cabeçalho, para que o revisor o veja e devolva.
    """
    texto = texto.replace("\r\n", "\n")
    padrao = UNIDADE_H1_RE if AULA_H1_RE.search(texto) else MODULO_H1_RE
    inicios = [m.start() for m in padrao.finditer(texto)]
    if not inicios:
        return [("", texto.strip())] if texto.strip() else []
    # O marcador `<!-- Módulo i: ... -->` que antecede uma aula viaja com ela,
    # para que o texto revisado continue idêntico em estrutura ao rascunho.
    ajustados: list[int] = []
    for ini in inicios:
        antes = texto[:ini].rstrip()
        m = MODULO_COMENTARIO_RE.search(antes)
        ajustados.append(m.start() if m and not texto[m.end():ini].strip() else ini)
    unidades: list[tuple[str, str]] = []
    for k, ini in enumerate(ajustados):
        fim = ajustados[k + 1] if k + 1 < len(ajustados) else len(texto)
        bloco = texto[ini:fim].strip().rstrip("-").strip()
        titulo = ""
        for linha in bloco.splitlines():
            if linha.startswith("# "):
                titulo = linha[2:].strip()
                break
        unidades.append((titulo, bloco))
    return unidades


def separar_relatorio_de_revisao(saida: str) -> tuple[str, str]:
    """Separa o texto revisado do bloco `REVISÃO CONCLUÍDA` que o fecha."""
    m = RELATORIO_REVISAO_RE.search(saida)
    if not m:
        return saida.strip(), ""
    return saida[: m.start()].strip(), saida[m.start():].strip().strip("-").strip()


def _contar_palavras(texto: str) -> int:
    return len(texto.split())


class Orchestrator:
    """Orquestra as 5 etapas do pipeline de criação de cursos."""

    def __init__(
        self,
        cost_tracker: CostTracker | None = None,
        client_context: ClientContext | None = None,
    ) -> None:
        self.cost_tracker = cost_tracker or CostTracker()
        if client_context is None:
            from src.clients import load_client
            client_context = load_client("default")
        self.client_context = client_context
        # B-019/D8: factory decide o backend: legado (default) ou
        # geo_orchestrator_sdk via CURSO_FACTORY_LLM_BACKEND=sdk (herda
        # timeout por task_type, fallback chain e FinOps do orquestrador).
        from src.llm_client import make_llm_client
        self.client = make_llm_client(self.cost_tracker)
        self.researcher = Researcher(self.client)
        self.writer = Writer(self.client)
        self.analyzer = Analyzer(self.client)
        self.classifier = Classifier(self.client)
        self.reviewer = Reviewer(self.client)

    # ── checkpoint ──────────────────────────────────────────────────────

    def _checkpoint_path(self, course_id: str) -> Path:
        return DRAFTS_DIR / f"{course_id}_checkpoint.json"

    def _save_checkpoint(self, course_id: str, result: PipelineResult, context: str = "") -> None:
        """Salva checkpoint incremental após cada etapa concluída."""
        data = result.to_dict()
        data["_context"] = context
        path = self._checkpoint_path(course_id)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        logger.info("Checkpoint salvo: %s (%d etapas)", path.name, len(result.etapas))

    def _load_checkpoint(self, course_id: str) -> tuple[PipelineResult, str] | None:
        """Carrega checkpoint se existir, para resume após desconexão."""
        path = self._checkpoint_path(course_id)
        if not path.exists():
            return None
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        result = PipelineResult(course_id)
        result.etapas = data.get("etapas", {})
        result.avisos = list(data.get("avisos", []))
        result.provedores = dict(data.get("provedores", {}))
        result.erros = []  # Limpa erros anteriores para retry
        context = data.get("_context", "")
        logger.info("Checkpoint carregado: %d etapas concluídas anteriormente", len(result.etapas))
        return result, context

    # ── orçamento e procedência ─────────────────────────────────────────

    def _pode_chamar(self, provider: str, course_id: str = "") -> tuple[bool, str]:
        """Orçamento por curso e por sessão (`CostTracker.pode_chamar`).

        Rastreador sem esse método (dublês antigos) cai no `is_over_budget`.
        """
        pode = getattr(self.cost_tracker, "pode_chamar", None)
        if pode is None:
            if self.cost_tracker.is_over_budget(provider):
                return False, f"orçamento excedido para {provider}"
            return True, ""
        return pode(provider, course_id)

    def _marca(self) -> int:
        indice = getattr(self.cost_tracker, "indice_atual", None)
        return indice() if indice else -1

    def _procedencia(self, marca: int, course_id: str) -> dict[str, int]:
        """`{"provedor/modelo": chamadas}` registrados desde a marca."""
        if marca < 0:
            return {}
        entradas = self.cost_tracker.entradas_desde(marca, course_id)
        usados: dict[str, int] = {}
        for e in entradas:
            chave = f"{e.get('provider')}/{e.get('model')}"
            usados[chave] = usados.get(chave, 0) + 1
        return usados

    def _registrar_procedencia(
        self, result: PipelineResult, nome: str, provider_declarado: str, usados: dict[str, int]
    ) -> None:
        if not usados:
            return
        result.provedores[nome] = usados
        fora = {k: n for k, n in usados.items() if not k.startswith(provider_declarado + "/")}
        if fora and sum(fora.values()) * 2 >= sum(usados.values()):
            aviso = (
                f"Etapa '{nome}' rodou em fallback: declarada em {provider_declarado}, "
                f"atendida por {', '.join(f'{k} ({n})' for k, n in usados.items())}."
            )
            logger.warning(aviso)
            result.avisos.append(aviso)

    # ── tetos da aula, lidos da fonte de estilo ─────────────────────────

    @staticmethod
    def _tetos_da_aula() -> dict[str, str]:
        """Números do molde D como variáveis de template, todos em string.

        Vêm de `config/lexicos.json` (espelho da fonte de estilo) via
        `content_checker.tetos_da_unidade("aula")`. O prompt de redação não
        carrega número nenhum: quem muda a régua na fonte muda o prompt.
        """
        from src.validators.content_checker import tetos_da_unidade

        t = tetos_da_unidade("aula")
        alvo_min, alvo_max = t["alvo"]
        h2_min, h2_max = t["h2"]
        par_min, par_max = t["paragrafo"]
        return {
            "palavras_piso": str(t["piso"]),
            "palavras_alvo_min": str(alvo_min),
            "palavras_alvo_max": str(alvo_max),
            "palavras_aviso": str(t["aviso"]),
            "palavras_erro": str(t["erro"]),
            "h2_min": str(h2_min),
            "h2_max": str(h2_max),
            "h3_por_h2": str(t["h3_por_h2"]),
            "figuras_max": str(t["visuais_max"]),
            "paragrafo_min": str(par_min),
            "paragrafo_max": str(par_max),
            "minutos_alvo": str(max(5, round(alvo_max / 180))),
        }

    # ── etapas ──────────────────────────────────────────────────────────

    def _step_research(self, course: Course) -> str:
        return self.researcher.execute(
            self._build_research_context(course),
            **self._research_vars(course),
        )

    def _step_draft(self, course: Course, research: str) -> str:
        return self._draft_modules_iterative(course, research)

    def _step_analyze(self, course: Course, draft: str) -> str:
        return self.analyzer.execute(
            draft, course_name=course.titulo, draft_content=draft
        )

    def _step_classify(self, course: Course, draft: str) -> str:
        conteudo = draft[:CLASSIFY_CONTEXT_CHARS]
        return self.classifier.execute(
            conteudo, course_name=course.titulo, content=conteudo
        )

    def _step_review(
        self, course: Course, draft: str, analysis: str, result: PipelineResult
    ) -> str:
        return self._review_iterative(course, draft, analysis, result)

    def run(self, course: Course) -> PipelineResult:
        """Executa o pipeline completo para um curso, com resume de checkpoint."""
        DRAFTS_DIR.mkdir(parents=True, exist_ok=True)

        # Achado F32: propaga course_id para todas as chamadas LLM, fazendo
        # com que o cost_tracker registre cada call sob o curso correto.
        self.client.set_course_context(course.id)

        checkpoint = self._load_checkpoint(course.id)
        if checkpoint:
            result, _ = checkpoint
            logger.info("Retomando pipeline de checkpoint com etapas: %s", list(result.etapas.keys()))
        else:
            result = PipelineResult(course.id)

        etapas: list[tuple[str, str, Callable[[], str]]] = [
            ("research", self.researcher.provider,
             lambda: self._step_research(course)),
            ("draft", self.writer.provider,
             lambda: self._step_draft(course, result.etapas.get("research", ""))),
            ("analyze", self.analyzer.provider,
             lambda: self._step_analyze(course, result.etapas.get("draft", ""))),
            ("classify", self.classifier.provider,
             lambda: self._step_classify(course, result.etapas.get("draft", ""))),
            ("review", self.reviewer.provider,
             lambda: self._step_review(
                 course, result.etapas.get("draft", ""),
                 result.etapas.get("analyze", ""), result,
             )),
        ]

        for nome, provider, executar in etapas:
            if nome in result.etapas:
                logger.info("Etapa '%s' já concluída (checkpoint), pulando", nome)
                continue

            pode, motivo = self._pode_chamar(provider, course.id)
            if not pode:
                msg = f"{motivo}. Pipeline interrompido na etapa '{nome}'."
                logger.error(msg)
                result.erros.append(msg)
                break

            logger.info("Iniciando etapa: %s (provider: %s)", nome, provider)
            marca = self._marca()
            try:
                saida = executar()
                result.etapas[nome] = saida
                self._registrar_procedencia(result, nome, provider, self._procedencia(marca, course.id))
                logger.info("Etapa '%s' concluída (%d palavras)", nome, _contar_palavras(saida))
                self._save_checkpoint(course.id, result, saida)
            except Exception as exc:
                msg = f"Erro na etapa '{nome}': {exc}"
                logger.error(msg)
                result.erros.append(msg)
                self._registrar_procedencia(result, nome, provider, self._procedencia(marca, course.id))
                self._save_checkpoint(course.id, result)
                break
        else:
            result.sucesso = True

        if result.sucesso:
            self._quality_gate(course, result)

        self._save_result(course.id, result)
        cp = self._checkpoint_path(course.id)
        if result.sucesso and cp.exists():
            cp.unlink()
            logger.info("Checkpoint removido (pipeline concluído com sucesso)")
        logger.info("Pipeline %s para curso '%s'",
                     "concluído com sucesso" if result.sucesso else "interrompido com erros",
                     course.id)
        logger.info(self.cost_tracker.report())
        return result

    # ── draft: uma aula por chamada ─────────────────────────────────────

    def _aulas_por_modulo(self) -> tuple[int, int]:
        from src.validators.content_checker import FALLBACK_AULAS_POR_MODULO, _par
        from src.validators.rules_loader import validation_section

        cq = validation_section("content_quality")
        return _par(cq.get("lessons_per_module"), FALLBACK_AULAS_POR_MODULO)

    def _plan_lessons(
        self, course: Course, modulo: Module, numero: int, research_context: str
    ) -> list[dict[str, str]]:
        """Devolve a lista de aulas do módulo: `[{"titulo", "ideia"}, ...]`.

        Se o módulo já vem com etapas definidas no YAML, elas são as aulas.
        Senão, uma chamada curta ao writer planeja de N a M aulas (faixa de
        `content_quality.lessons_per_module`), uma ideia por aula. Se o plano
        não puder ser lido, o módulo inteiro vira uma aula única, para que o
        pipeline nunca pare por causa do planejamento.
        """
        if modulo.etapas:
            return [
                {"titulo": e.titulo, "ideia": e.conteudo.strip() or modulo.descricao}
                for e in modulo.etapas
            ]

        minimo, maximo = self._aulas_por_modulo()
        prompt = (
            f"Você planeja as aulas de um curso em português do Brasil, com "
            f"acentuação completa.\n\n"
            f"Curso: {course.titulo}\nNível: {course.nivel.value}\n"
            f"Módulo {numero}: {modulo.titulo}\n"
            f"Descrição do módulo: {modulo.descricao or 'conforme pesquisa'}\n\n"
            f"Planeje de {minimo} a {maximo} aulas para este módulo. Cada aula "
            f"ensina UMA ideia, explicada por inteiro, e termina com o aluno "
            f"fazendo algo com um dado do próprio negócio. As aulas se "
            f"encadeiam: a seguinte usa o que a anterior deixou pronto.\n\n"
            f"Responda SOMENTE com uma linha por aula, neste formato, sem "
            f"comentário antes ou depois:\n"
            f"1. Título da aula em até 10 palavras | a ideia única da aula em uma frase\n\n"
            f"--- DADOS DA PESQUISA ---\n{research_context[:12000]}"
        )
        # Falha de provedor sobe ao pipeline como erro da etapa: mascarar como
        # "aula única" só adiava o mesmo erro para a primeira aula (E2E de
        # 02/09/2026). O que vira aula única é plano ilegível, não provedor morto.
        resposta = self.client.call(self.writer.provider, prompt, model=self.writer.model)

        aulas: list[dict[str, str]] = []
        for linha in resposta.splitlines():
            m = PLANO_LINHA_RE.match(linha)
            if not m:
                continue
            titulo = m.group(2).strip().strip("*").strip()
            ideia = (m.group(3) or "").strip()
            if titulo:
                aulas.append({"titulo": titulo, "ideia": ideia})
        if not aulas:
            logger.warning("Plano de aulas ilegível para o módulo %d; aula única", numero)
            return [{"titulo": modulo.titulo, "ideia": modulo.descricao}]
        return aulas[:maximo]

    def _draft_lesson(
        self,
        course: Course,
        modulo: Module,
        numero_modulo: int,
        aulas: list[dict[str, str]],
        indice: int,
        research_context: str,
    ) -> str:
        """Escreve UMA aula, com a pesquisa inteira e o mapa das aulas vizinhas."""
        aula = aulas[indice]
        anteriores = [f"{numero_modulo}.{k + 1} {a['titulo']}" for k, a in enumerate(aulas[:indice])]
        seguintes = [f"{numero_modulo}.{k + 1} {a['titulo']}" for k, a in enumerate(aulas[indice + 1:], indice + 1)]
        variaveis = {
            "course_name": course.titulo,
            "course_level": course.nivel.value,
            "module_number": str(numero_modulo),
            "module_title": modulo.titulo,
            "module_description": modulo.descricao or "conforme pesquisa",
            "lesson_number": f"{numero_modulo}.{indice + 1}",
            "lesson_title": aula["titulo"],
            "lesson_idea": aula.get("ideia") or "a ideia central desta aula, explicada por inteiro",
            "lesson_position": f"aula {indice + 1} de {len(aulas)} do módulo {numero_modulo}",
            "previous_lessons": "; ".join(anteriores) or "nenhuma (esta abre o módulo)",
            "next_lessons": "; ".join(seguintes) or "nenhuma (esta fecha o módulo)",
            **self._tetos_da_aula(),
        }
        contexto = research_context[:DRAFT_RESEARCH_CONTEXT_CHARS]
        texto = self.writer.execute(contexto, **variaveis).strip()
        # Garante o cabeçalho da aula na primeira linha, e um só.
        texto = AULA_H1_RE.sub("", texto, count=1).strip() if AULA_H1_RE.match(texto) else texto
        texto = re.sub(r"^#\s+(?!#)", "## ", texto, count=1) if texto.startswith("# ") else texto
        return f"# Aula {numero_modulo}.{indice + 1}: {aula['titulo']}\n\n{texto}"

    def _draft_modules_iterative(self, course: Course, research_context: str) -> str:
        """Gera o curso aula a aula.

        Para cada módulo: planeja as aulas (ou usa as etapas do YAML), depois
        escreve cada aula numa chamada própria, com a pesquisa inteira. Curso
        sem módulos declarados vira um módulo com o título do curso.
        """
        modulos = course.modulos or [Module(titulo=course.titulo, descricao=course.descricao, ordem=1)]
        partes: list[str] = []

        for i, modulo in enumerate(modulos, 1):
            pode, motivo = self._pode_chamar(self.writer.provider, course.id)
            if not pode:
                logger.warning("%s antes do módulo %d. Parando draft.", motivo, i)
                break
            aulas = self._plan_lessons(course, modulo, i, research_context)
            logger.info("Módulo %d/%d '%s': %d aula(s) planejada(s)",
                        i, len(modulos), modulo.titulo, len(aulas))
            partes.append(f"<!-- Módulo {i}: {modulo.titulo} -->")
            partes_do_modulo: list[str] = []
            for j in range(len(aulas)):
                pode, motivo = self._pode_chamar(self.writer.provider, course.id)
                if not pode:
                    logger.warning("%s na aula %d.%d. Parando draft.", motivo, i, j + 1)
                    return "\n\n".join(partes)
                logger.info("Draft aula %d.%d: %s", i, j + 1, aulas[j]["titulo"])
                aula_md = self._draft_lesson(course, modulo, i, aulas, j, research_context)
                partes.append(aula_md)
                partes_do_modulo.append(aula_md)
                logger.info("Aula %d.%d gerada: %d palavras", i, j + 1, _contar_palavras(aula_md))
            pode, motivo = self._pode_chamar(self.writer.provider, course.id)
            if not pode:
                logger.warning("%s antes do fechamento da trilha %d. Parando draft.", motivo, i)
                return "\n\n".join(partes)
            trilha_md = self._close_trail(course, modulo, i, aulas, partes_do_modulo, research_context)
            if trilha_md:
                partes.append(trilha_md)
                logger.info("Trilha %d fechada: %d palavras", i, _contar_palavras(trilha_md))

        return "\n\n".join(partes)

    def _close_trail(
        self,
        course: Course,
        modulo: Module,
        numero_modulo: int,
        aulas: list[dict[str, str]],
        aulas_md: list[str],
        research_context: str,
    ) -> str:
        """Escreve o que vive no nível da trilha, uma vez, depois das aulas.

        O molde D manda objetivos, pré-requisitos, glossário, FAQ e fontes
        para o nível da trilha, e até a wave 5 (02/09/2026) o pipeline não os
        gerava em lugar nenhum. Sai como `# Trilha n: título`, unidade própria
        que a revisão pula e o gate mede sem a régua da aula.
        """
        from src.agents.base import _safe_substitute
        from src.agents.lang_resolver import resolve_prompt_path

        if not aulas_md:
            return ""
        try:
            template = resolve_prompt_path("trail.md", self.writer.language).read_text(encoding="utf-8")
        except FileNotFoundError:
            logger.warning("Prompt trail.md ausente; a trilha %d fica sem fechamento", numero_modulo)
            return ""
        lessons = "\n\n".join(aulas_md)[:TRAIL_LESSONS_CHARS]
        prompt = _safe_substitute(template, {
            "course_name": course.titulo,
            "course_level": course.nivel.value,
            "module_number": str(numero_modulo),
            "module_title": modulo.titulo,
            "module_description": modulo.descricao or "conforme pesquisa",
            "lesson_titles": "; ".join(f"{numero_modulo}.{k + 1} {a['titulo']}" for k, a in enumerate(aulas)),
            "lessons": lessons,
            "context": research_context[:TRAIL_RESEARCH_CHARS],
        })
        texto = self.client.call(self.writer.provider, prompt, model=self.writer.model).strip()
        texto = TRILHA_H1_RE.sub("", texto, count=1).strip() if TRILHA_H1_RE.match(texto) else texto
        return f"# Trilha {numero_modulo}: {modulo.titulo}\n\n{texto}"

    # ── review: uma aula por chamada, texto de volta ────────────────────

    def _review_iterative(
        self, course: Course, draft: str, analysis: str, result: PipelineResult
    ) -> str:
        """Revisa unidade a unidade e devolve o texto revisado inteiro.

        A saída de cada chamada é separada em texto e relatório. Se o texto
        devolvido tiver menos que `REVIEW_MIN_RATIO` das palavras da unidade
        recebida, a resposta é comentário e não revisão: a unidade original
        fica, e o resultado ganha um aviso. Os relatórios vão para
        `etapas["review_report"]`.
        """
        unidades = dividir_em_unidades(draft)
        if not unidades:
            return ""
        resumo_analise = (analysis or "")[:REVIEW_ANALYSIS_CHARS]
        revisadas: list[str] = []
        relatorios: list[str] = []

        for k, (titulo, texto) in enumerate(unidades, 1):
            if titulo.startswith("Trilha "):
                # O fechamento da trilha não é aula: o prompt de revisão cobra
                # exercício e exemplo, e reescrever glossário e fontes cria
                # risco de invenção. Passa como saiu do writer.
                revisadas.append(texto)
                continue
            pode, motivo = self._pode_chamar(self.reviewer.provider, course.id)
            if not pode:
                aviso = f"{motivo} na revisão da unidade {k}; as seguintes ficam sem revisão."
                logger.warning(aviso)
                result.avisos.append(aviso)
                revisadas.extend(t for _, t in unidades[k - 1:])
                break
            logger.info("Revisão %d/%d: %s", k, len(unidades), titulo or "(unidade sem título)")
            saida = self.reviewer.execute(
                texto,
                course_name=course.titulo,
                unit_title=titulo or f"unidade {k}",
                unit_position=f"{k} de {len(unidades)}",
                analysis_summary=resumo_analise,
            )
            texto_revisado, relatorio = separar_relatorio_de_revisao(saida)
            if relatorio:
                relatorios.append(f"[{titulo or k}] {relatorio}")
            originais, devolvidas = _contar_palavras(texto), _contar_palavras(texto_revisado)
            if originais and devolvidas < originais * REVIEW_MIN_RATIO:
                aviso = (
                    f"Revisão da unidade '{titulo or k}' devolveu {devolvidas} palavras para "
                    f"{originais} recebidas (abaixo de {REVIEW_MIN_RATIO:.0%}); "
                    f"o rascunho original foi mantido."
                )
                logger.warning(aviso)
                result.avisos.append(aviso)
                revisadas.append(texto)
                continue
            revisadas.append(texto_revisado)

        if relatorios:
            result.etapas["review_report"] = "\n\n".join(relatorios)
        return "\n\n".join(revisadas)

    # ── quality gate ao fim do pipeline ─────────────────────────────────

    def _quality_gate(self, course: Course, result: PipelineResult) -> None:
        """Roda o quality gate aula a aula sobre o texto final e grava o veredito.

        Só relata: o pipeline não reprova por causa do gate, porque o veredito
        vai para `result.gate` e para a etapa `gate_report`, e é o operador
        quem decide o que corrigir. Até 02/09/2026 (wave 2) o gate só rodava
        se alguém lembrasse de chamar `python cli.py validate` depois.
        """
        from src.validators.quality_gate import QualityGate

        final = result.etapas.get("review") or result.etapas.get("draft") or ""
        if not final.strip():
            return
        try:
            gate = QualityGate(client=self.client_context, auto_fix=False)
        except Exception as exc:  # pragma: no cover - dependência ausente
            logger.warning("Quality gate indisponível: %s", exc)
            return
        linhas: list[str] = []
        for titulo, bloco in dividir_em_unidades(final):
            rotulo = titulo or "unidade"
            try:
                r = gate.check_text(bloco, curso_id=course.id, module_name=rotulo, unidade="aula", geo=False)
            except Exception as exc:
                logger.warning("Quality gate falhou em '%s': %s", rotulo, exc)
                result.gate[rotulo] = {"aprovado": None, "erros": [f"gate falhou: {exc}"], "avisos": 0}
                continue
            result.gate[rotulo] = {
                "aprovado": bool(r.aprovado),
                "erros": list(r.erros),
                "avisos": len(r.avisos),
                "voice_guard_score": r.voice_guard_score,
            }
            linhas.append(f"{'OK  ' if r.aprovado else 'FAIL'} {rotulo}: {len(r.erros)} erro(s), {len(r.avisos)} aviso(s)")
            for e in r.erros:
                linhas.append(f"      - {e}")
        # Camada GEO (fontes, estatísticas, citação, cápsula) sobre o curso
        # inteiro: meta do conjunto, não de cada aula.
        geo_config = getattr(self.client_context, "geo", None)
        if geo_config is not None:
            try:
                geo_achados = gate.check_geo(final, "curso", geo_config)
            except Exception as exc:
                logger.warning("Camada GEO falhou: %s", exc)
                geo_achados = []
            erros_geo = [a.mensagem for a in geo_achados if a.tipo == "error"]
            result.gate["curso"] = {
                "aprovado": not erros_geo,
                "erros": erros_geo,
                "avisos": sum(1 for a in geo_achados if a.tipo == "warning"),
            }
            linhas.append(f"{'OK  ' if not erros_geo else 'FAIL'} curso (GEO): {len(erros_geo)} erro(s), "
                          f"{result.gate['curso']['avisos']} aviso(s)")
            for e in erros_geo:
                linhas.append(f"      - {e}")
        aprovadas = sum(1 for v in result.gate.values() if v.get("aprovado"))
        cabecalho = f"Quality gate: {aprovadas} de {len(result.gate)} unidade(s) aprovada(s)"
        result.etapas["gate_report"] = cabecalho + "\n" + "\n".join(linhas)
        if aprovadas < len(result.gate):
            result.avisos.append(f"{cabecalho}; veja etapas.gate_report antes de publicar.")
        logger.info(cabecalho)

    # ── contextos auxiliares ────────────────────────────────────────────

    def _research_vars(self, course: Course) -> dict[str, str]:
        if course.modulos:
            modulos_list = "\n".join(f"  - {m.titulo}: {m.descricao}" for m in course.modulos)
        else:
            modulos_list = "A definir conforme pesquisa"
        return {
            "course_name": course.titulo,
            "course_description": course.descricao or f"Curso completo sobre {course.titulo}",
            "target_modules": modulos_list,
        }

    def _build_template_vars(self, nome: str, course: Course, context: str) -> dict:
        """Compatibilidade: variáveis nomeadas por etapa (uso externo e testes)."""
        if nome == "research":
            return self._research_vars(course)
        if nome == "analyze":
            return {"course_name": course.titulo, "draft_content": context}
        if nome == "classify":
            return {"course_name": course.titulo, "content": context}
        return {}

    def _build_research_context(self, course: Course) -> str:
        """Monta o contexto inicial para a etapa de pesquisa."""
        modulos_txt = ""
        if course.modulos:
            modulos_txt = "\nMódulos planejados:\n"
            for m in course.modulos:
                modulos_txt += f"  - {m.titulo}: {m.descricao}\n"
        return (
            f"Curso: {course.titulo}\n"
            f"Descrição: {course.descricao}\n"
            f"Nível: {course.nivel.value}\n"
            f"Tags: {', '.join(course.tags)}\n"
            f"{modulos_txt}"
        )

    def _save_result(self, course_id: str, result: PipelineResult) -> None:
        """Salva o resultado do pipeline em JSON."""
        timestamp = datetime.now(UTC).strftime("%Y%m%d_%H%M%S")
        filename = f"{course_id}_{timestamp}.json"
        path = DRAFTS_DIR / filename
        with open(path, "w", encoding="utf-8") as f:
            json.dump(result.to_dict(), f, indent=2, ensure_ascii=False)
        logger.info("Resultado salvo em: %s", path)
