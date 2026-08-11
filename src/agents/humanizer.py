"""Humanizer — agente de pos-processamento com detector-in-the-loop.

Roda DEPOIS do reviewer (Claude). Multi-pass adversarial editing inspirado em:
- Krishna et al. *Paraphrasing evades detectors* (DIPPER, NeurIPS 2023) —
  https://arxiv.org/abs/2303.13408
- *Adversarial Paraphrasing — universal humanization attack* (2025) —
  https://arxiv.org/abs/2506.07001

Implementacao V1 (sem detector externo):
- Mede stylometry interno (burstiness, sentence variance, TTR, repetition)
  via src.validators.stylometry_checker
- Se score < target_score, dispara reescrita instruida com diagnostico
  especifico (qual metrica esta ruim e como corrigir)
- Itera ate target_score OU max_iters (default 2)
- Cada pass roda Claude Opus pelo prompt `humanize.md`

Implementacao V2 (futura — PR-3 + PR-4 combinados):
- Substituir signal interno por API Pangram/Originality (custo $0.99/100 scans)
- Adicionar RADAR-style proxy interno (2 LMs PT-BR pequenos como Binoculars)
  para reduzir dependencia de API paga (Hu et al. NeurIPS 2023 —
  https://arxiv.org/abs/2307.03838)

Opt-in via client.yaml:
    pipeline:
      humanize_enabled: true
      humanize_target_stylometry_score: 75
      humanize_max_iters: 2

Default OFF. Quando OFF, o pipeline termina no reviewer como hoje.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from src.agents.base import Agent, _safe_substitute
from src.validators.stylometry_checker import StylometryReport, stylometry_check

if TYPE_CHECKING:
    from src.clients.context import ClientContext
    from src.llm_client import LLMClient

logger = logging.getLogger(__name__)


@dataclass
class HumanizerResult:
    """Resultado de um run do Humanizer."""

    texto_final: str = ""
    iters_realizadas: int = 0
    score_inicial: int = 0
    score_final: int = 0
    burstiness_inicial: float = 0.0
    burstiness_final: float = 0.0
    convergiu: bool = False  # True se atingiu target_score
    historico_scores: list[int] = field(default_factory=list)
    motivo_parada: str = ""

    def report(self) -> str:
        lines = [
            "--- Humanizer Report ---",
            f"Iters:           {self.iters_realizadas}",
            f"Score:           {self.score_inicial} -> {self.score_final}",
            f"Burstiness:      {self.burstiness_inicial:.3f} -> {self.burstiness_final:.3f}",
            f"Convergiu:       {'SIM' if self.convergiu else 'NAO'}",
            f"Historico:       {self.historico_scores}",
            f"Motivo parada:   {self.motivo_parada}",
        ]
        return "\n".join(lines)


class Humanizer(Agent):
    """Agente Claude que reescreve texto orientado por signal de stylometry.

    Diferente dos outros agentes do pipeline, NAO executa contra fixture
    estatica — recebe um texto + relatorio de stylometry e devolve uma
    versao reescrita com instrucoes cirurgicas baseadas no diagnostico.
    """

    nome = "humanizer"
    provider = "anthropic"
    model = "claude-opus-4-7"
    prompt_file = "humanize.md"

    # Fallback inline (mantem o agente operavel se humanize.md nao existir)
    TEMPLATE = (
        "Voce e um editor de prosa de alto padrao. Recebe um texto que ja\n"
        "passou por revisao editorial mas tem cadencia uniforme, paragrafos\n"
        "simetricos e aberturas repetidas, padrao tipico de LLM. Sua tarefa:\n"
        "reescrever a estrutura desses trechos SEM mudar conteudo factual.\n\n"
        "DIAGNOSTICO STYLOMETRIA:\n{diagnostic}\n\n"
        "REGRAS INVIOLAVEIS:\n"
        "1. NAO mude numeros, datas, citacoes, nomes proprios, blocos de\n"
        "   codigo, tabelas, marcadores [FALTA EVIDENCIA: ...] nem termos\n"
        "   tecnicos canonicos.\n"
        "2. NAO mude o sentido logico de nenhum paragrafo e nao corte\n"
        "   informacao.\n"
        "3. NAO insira hedges ('talvez', 'pode ser') onde o texto original\n"
        "   afirma com convicao.\n"
        "4. NAO use travessao nem hifen como recurso estilistico.\n"
        "5. NAO aplique cota de ritmo: nada de uma frase curta por paragrafo\n"
        "   nem de alternancia programada curta/longa. O comprimento vem do\n"
        "   conteudo.\n"
        "6. NAO troque termo tecnico por sinonimo para variar vocabulario.\n\n"
        "O QUE REESCREVER: blocos com frases todas do mesmo tamanho;\n"
        "paragrafos vizinhos que abrem com a mesma construcao; simetria de\n"
        "secao e triades de ritmo; conectivos de abertura ('alem disso',\n"
        "'nesse contexto', 'vale destacar'), que saem por subtracao; fechos\n"
        "que apenas resumem o que foi dito; listas cujos itens tem relacao de\n"
        "causa entre si, que voltam a ser prosa.\n\n"
        "Devolva o texto reescrito NA INTEGRA. Sem preambulo, sem epilogo,\n"
        "sem 'aqui esta o texto reescrito:'. Apenas o texto.\n\n"
        "--- TEXTO ORIGINAL ---\n{context}"
    )

    def build_prompt(
        self,
        context: str,
        diagnostic: str = "",
        **template_vars: str,
    ) -> str:
        template = self._load_prompt_template()
        substitutions = {
            "context": context,
            "diagnostic": diagnostic,
            **template_vars,
        }
        if template:
            return _safe_substitute(template, substitutions)
        return _safe_substitute(self.TEMPLATE, substitutions)

    def _build_diagnostic(self, report: StylometryReport) -> str:
        """Gera diagnostico a partir do StylometryReport.

        O diagnostico aponta ONDE o texto esta uniforme e manda reescrever a
        estrutura daquele trecho. Nao prescreve cota de frase curta nem troca
        de termo por sinonimo: as duas "correcoes" melhoram a metrica e pioram
        o texto (staccato de manchete e incoerencia terminologica), conforme
        DIRETRIZ_EDITORIAL.md secoes 4 e 6.
        """
        lines = []
        if report.burstiness < 0.6:
            lines.append(
                f"- burstiness={report.burstiness:.2f} (referencia humana >= 0.60). "
                "Cadencia uniforme: localize os blocos em que quase todas as frases "
                "tem tamanho parecido e reescreva-os deixando o conteudo governar o "
                "comprimento (periodo longo para raciocinio com causa e ressalva, "
                "frase curta quando houver o que enfatizar). Nao distribua frase "
                "curta por cota."
            )
        if report.sentence_len_variance < 40:
            lines.append(
                f"- variancia de comprimento={report.sentence_len_variance:.1f} "
                "(referencia >= 40). Funda em periodos os trechos que fatiam um "
                "unico raciocinio e desenvolva os argumentos que hoje estao "
                "resumidos em uma frase."
            )
        if report.type_token_ratio < 0.40:
            lines.append(
                f"- type_token_ratio={report.type_token_ratio:.2f} "
                "(referencia >= 0.45). Vocabulario restrito por repeticao de "
                "construcoes de apoio. Acrescente informacao concreta (dado, caso, "
                "consequencia) ou reformule a construcao. PROIBIDO trocar o termo "
                "tecnico canonico por sinonimo."
            )
        if report.repetition_score > 0.10:
            lines.append(
                f"- repetition_score={report.repetition_score:.2f} "
                "(referencia <= 0.08). Bigramas boilerplate em excesso: varie as "
                "construcoes-molde que se repetem ('temos que', 'e importante', "
                "'isso significa que') mantendo a terminologia tecnica."
            )
        if report.sentences_short == 0:
            lines.append(
                "- nenhuma sentenca curta (<=6 palavras) no modulo inteiro. "
                "Verifique se algum fechamento de bloco ganharia forca em frase "
                "seca; se nenhum ganhar, deixe como esta."
            )
        if not lines:
            lines.append("- score ja satisfatorio; reescrita marginal apenas.")
        return "\n".join(lines)

    def run_iterative(
        self,
        text: str,
        target_score: int = 75,
        max_iters: int = 2,
    ) -> HumanizerResult:
        """Multi-pass: reescreve ate target_score OU max_iters atingido.

        Retorna HumanizerResult com texto final, historico de scores e
        diagnostico de convergencia. NAO levanta excecao em falha de LLM —
        retorna o melhor texto obtido ate o ponto.
        """
        initial = stylometry_check(text)
        result = HumanizerResult(
            texto_final=text,
            iters_realizadas=0,
            score_inicial=initial.score,
            score_final=initial.score,
            burstiness_inicial=initial.burstiness,
            burstiness_final=initial.burstiness,
            historico_scores=[initial.score],
        )

        if initial.score >= target_score:
            result.convergiu = True
            result.motivo_parada = "score inicial ja atende target"
            return result

        current_text = text
        current_report = initial

        for i in range(max_iters):
            diagnostic = self._build_diagnostic(current_report)
            prompt = self.build_prompt(current_text, diagnostic=diagnostic)
            try:
                rewritten = self.client.call(
                    self.provider,
                    prompt,
                    model=self.model,
                )
            except Exception as exc:  # noqa: BLE001
                logger.warning("Humanizer pass %d falhou: %s", i + 1, exc)
                result.motivo_parada = f"falha LLM na iter {i + 1}: {exc}"
                break

            if not rewritten or len(rewritten) < len(current_text) * 0.5:
                # Output suspeito (texto muito curto) — preserva versao anterior
                logger.warning(
                    "Humanizer pass %d retornou texto suspeito (len=%d vs "
                    "original=%d) — preservando versao anterior",
                    i + 1, len(rewritten or ""), len(current_text),
                )
                result.motivo_parada = (
                    f"output truncado na iter {i + 1} — preservada versao anterior"
                )
                break

            new_report = stylometry_check(rewritten)
            result.iters_realizadas = i + 1
            result.historico_scores.append(new_report.score)

            if new_report.score > current_report.score:
                # Aceita o pass (melhorou)
                current_text = rewritten
                current_report = new_report
                result.texto_final = rewritten
                result.score_final = new_report.score
                result.burstiness_final = new_report.burstiness
            else:
                # Pass nao melhorou — para antes de degradar mais
                result.motivo_parada = (
                    f"score nao melhorou na iter {i + 1} "
                    f"({new_report.score} <= {current_report.score})"
                )
                break

            if new_report.score >= target_score:
                result.convergiu = True
                result.motivo_parada = f"target {target_score} atingido"
                break

        if not result.motivo_parada:
            result.motivo_parada = f"max_iters={max_iters} atingido sem convergir"

        return result


def humanize_if_enabled(
    text: str,
    client: ClientContext,
    llm_client: LLMClient,
) -> tuple[str, HumanizerResult | None]:
    """Roda o humanizer se o cliente tiver opt-in. Retorna (texto, resultado_ou_None).

    Atalho para uso em src.agents.pipeline (etapa 6 opcional).

    Configuracao no client.yaml:
        pipeline:
          humanize_enabled: true
          humanize_target_stylometry_score: 75
          humanize_max_iters: 2

    Se nao houver bloco `pipeline` ou `humanize_enabled` for False, retorna
    o texto original sem alteracao e None como segundo elemento.
    """
    # Le configuracao via getattr para nao forcar schema rigido no ClientContext
    # (o usuario pode adicionar bloco `pipeline` opcionalmente no YAML)
    pipeline_cfg = getattr(client, "pipeline", None)
    if not pipeline_cfg or not getattr(pipeline_cfg, "humanize_enabled", False):
        return text, None

    target = int(getattr(pipeline_cfg, "humanize_target_stylometry_score", 75))
    max_iters = int(getattr(pipeline_cfg, "humanize_max_iters", 2))

    humanizer = Humanizer(llm_client)
    result = humanizer.run_iterative(text, target_score=target, max_iters=max_iters)
    logger.info(
        "Humanizer: score %d -> %d em %d iters (convergiu=%s)",
        result.score_inicial,
        result.score_final,
        result.iters_realizadas,
        result.convergiu,
    )
    return result.texto_final, result
