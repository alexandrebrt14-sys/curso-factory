"""voice_guard.py — score programático de conformidade editorial por cliente.

Achado B-012 da auditoria de ecossistema 2026-04-08; parametrizado por
cliente em 2026-04-19 (auditoria multi-tenancy).

Antes deste módulo, o padrão editorial Alexandre (HSM/HBR/MIT Sloan +
andragogia + Bloom + naming canônico Brasil GEO) era enforced apenas via
prompt do agente Reviewer. Sem barreira programática, conteúdo fora do
padrão podia passar pelo quality_gate sem alerta.

Este módulo é a barreira de código. Calcula um score de 0 a 100 combinando
4 dimensões ponderadas:

  - Anti-clichê editorial:    peso 30 (clichês proibidos NUNCA permitidos)
  - Andragogia + Bloom:       peso 30 (verbos nível 3-6, princípios Knowles)
  - Naming canônico:          peso 25 (nomes canônicos do cliente,
                                       anti-fake titles, anti-domínios)
  - Estilo HBR/MIT Sloan:     peso 15 (sem disclaimers, sem perguntas
                                       retóricas como abertura)

Score < min_score (padrão 70) -> aprovado=False (bloqueia publicação).
Score 70-84 -> aprovado=True com warnings.
Score 85+ -> aprovado=True clean.

As regras (naming canônico, lista negra, disclaimers) vêm do ClientContext
carregado de config/clients/<id>/client.yaml. Se chamado sem client
explícito, usa o cliente "default" (Brasil GEO / Alexandre Caramaschi) —
backward-compat com a versão pré-refactor.

Uso:
    from src.clients import load_client
    from src.validators.voice_guard import voice_guard_check

    client = load_client("minha_empresa")
    result = voice_guard_check(texto, client=client)
    if not result.aprovado:
        print(result.report())
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from src.validators.content_checker import (
    _check_bloom_objectives,
    _check_cliches,
)

if TYPE_CHECKING:
    from src.clients.context import ClientContext


# ─── Resultado ────────────────────────────────────────────────────────────


@dataclass
class VoiceGuardResult:
    """Resultado do voice_guard_check."""
    score: int  # 0 a 100
    aprovado: bool  # score >= min_score E sem erros críticos
    dimensoes: dict[str, int] = field(default_factory=dict)
    erros: list[str] = field(default_factory=list)
    erros_criticos: list[str] = field(default_factory=list)
    avisos: list[str] = field(default_factory=list)

    def report(self) -> str:
        """Relatório textual legível."""
        lines = [
            "--- Voice Guard Report ---",
            f"Score total:      {self.score}/100",
            f"Aprovado:         {'SIM' if self.aprovado else 'NAO'}",
            "",
            "Dimensoes (peso):",
        ]
        for nome, val in self.dimensoes.items():
            lines.append(f"  {nome:<28} {val}/100")
        if self.erros_criticos:
            lines.append("")
            lines.append(f"Erros CRITICOS ({len(self.erros_criticos)}) — bloqueiam aprovacao:")
            for err in self.erros_criticos[:10]:
                lines.append(f"  ! {err}")
        if self.erros:
            lines.append("")
            lines.append(f"Erros ({len(self.erros)}):")
            for err in self.erros[:10]:
                lines.append(f"  - {err}")
            if len(self.erros) > 10:
                lines.append(f"  ... e mais {len(self.erros) - 10} erros")
        if self.avisos:
            lines.append("")
            lines.append(f"Avisos ({len(self.avisos)}):")
            for av in self.avisos[:5]:
                lines.append(f"  - {av}")
        return "\n".join(lines)


# ─── Pesos ────────────────────────────────────────────────────────────────


WEIGHTS = {
    "anti_cliche": 30,
    "bloom_andragogia": 30,
    "naming": 25,
    "hbr_style": 15,
}


# ─── Cálculo por dimensão ────────────────────────────────────────────────


def _score_anti_cliche(text: str) -> tuple[int, list[str]]:
    """Cada clichê custa 25 pontos; 4+ zera."""
    cliches = _check_cliches(text)
    if not cliches:
        return 100, []
    penalty = min(100, len(cliches) * 25)
    score = max(0, 100 - penalty)
    erros = [f"cliche proibido: '{c}'" for c in cliches]
    return score, erros


def _score_bloom_andragogia(text: str) -> tuple[int, list[str], list[str]]:
    """Penaliza verbos Bloom proibidos (nivel 1-2) em objetivos."""
    proibidos, aceitos = _check_bloom_objectives(text)
    erros: list[str] = []
    avisos: list[str] = []

    if not proibidos and not aceitos:
        avisos.append("nenhuma secao de objetivos com verbos Bloom detectavel")
        return 70, erros, avisos

    score = 100
    for v in proibidos:
        erros.append(f"verbo Bloom proibido em objetivos: '{v}'")
        score -= 25

    if len(aceitos) >= 3:
        score = min(100, score + 10)

    return max(0, score), erros, avisos


def _score_naming(
    text: str, client: "ClientContext | None" = None
) -> tuple[int, list[str], list[str], list[str]]:
    """Score de naming canônico parametrizado por cliente.

    Bloqueios absolutos (qualquer ocorrência força aprovado=False):
    - Qualquer título proibido
    - Qualquer nome errado da empresa
    - Qualquer domínio proibido
    """
    if client is None:
        from src.clients import load_client
        client = load_client("default")

    erros: list[str] = []
    erros_criticos: list[str] = []
    avisos: list[str] = []
    score = 100
    text_lower = text.lower()
    vg = client.voice_guard

    for title in vg.forbidden.titles:
        if title.lower() in text_lower:
            err = f"titulo/credencial inventada proibida: '{title}'"
            erros_criticos.append(err)
            erros.append(err)
            score -= 40

    for company in vg.forbidden.company_names:
        canonical = vg.canonical.company or "[canonical company]"
        if company.lower() in text_lower:
            err = f"naming errado da empresa: '{company}' (use '{canonical}')"
            erros_criticos.append(err)
            erros.append(err)
            score -= 30

    for domain in vg.forbidden.domains:
        if domain.lower() in text_lower:
            err = f"dominio proibido/alucinado: '{domain}'"
            erros_criticos.append(err)
            erros.append(err)
            score -= 50

    canonical_company = (vg.canonical.company or "").lower()
    canonical_founder = (vg.canonical.founder or "").lower()

    # Aviso heurístico só se o cliente definiu naming canônico
    if canonical_company or canonical_founder:
        mentions_company_context = any(
            kw in text_lower
            for kw in ["consultoria", "geo", "empresa", "metodologia"]
        )
        has_canonical_company = bool(canonical_company and canonical_company in text_lower)
        has_canonical_founder = bool(canonical_founder and canonical_founder in text_lower)

        if mentions_company_context and not (has_canonical_company or has_canonical_founder):
            marcador = f"'{vg.canonical.company}' nem '{vg.canonical.founder}'".strip()
            avisos.append(
                f"texto menciona consultoria/empresa mas nao referencia {marcador}"
            )

    if vg.canonical.credential_fragments:
        full_credential_count = sum(
            1
            for fragment in vg.canonical.credential_fragments
            if fragment.lower() in text_lower
        )
        if full_credential_count >= 2:
            score = min(100, score + 5)

    return max(0, score), erros, erros_criticos, avisos


def _score_hbr_style(
    text: str, client: "ClientContext | None" = None
) -> tuple[int, list[str], list[str]]:
    """Score de estilo HBR/MIT Sloan parametrizado por cliente."""
    if client is None:
        from src.clients import load_client
        client = load_client("default")

    erros: list[str] = []
    avisos: list[str] = []
    score = 100
    vg = client.voice_guard

    for opener in vg.forbidden.rhetoric_openers:
        if re.search(rf"(?:^|\n)\s*{re.escape(opener)}", text, re.IGNORECASE):
            erros.append(f"abertura retorica proibida: '{opener}...'")
            score -= 15

    text_lower = text.lower()
    for disc in vg.forbidden.ai_disclaimers:
        if disc.lower() in text_lower:
            erros.append(f"disclaimer de modelo IA proibido: '{disc}'")
            score -= 25

    long_paragraphs = 0
    for para in text.split("\n\n"):
        if para.strip().startswith(("```", "|", "- ", "* ", "1.", ">", "#")):
            continue
        if len(para.strip().split("\n")) > 5:
            long_paragraphs += 1
    if long_paragraphs > 0:
        avisos.append(f"{long_paragraphs} paragrafo(s) com mais de 5 linhas")
        score -= long_paragraphs * 10

    return max(0, score), erros, avisos


# ─── Score combinado ──────────────────────────────────────────────────────


def voice_guard_check(
    text: str, client: "ClientContext | None" = None
) -> VoiceGuardResult:
    """Roda todas as 4 dimensões parametrizadas pelo cliente.

    Sem `client`, usa o cliente "default" (backward-compat com versão
    pré-refactor). Para rodar sob padrão editorial de outro cliente, passe
    o ClientContext correspondente.
    """
    if not text or not text.strip():
        return VoiceGuardResult(
            score=0,
            aprovado=False,
            erros=["texto vazio ou apenas whitespace"],
        )

    if client is None:
        # Import tardio para evitar ciclo
        from src.clients import load_client
        client = load_client("default")

    if not client.voice_guard.enabled:
        # Cliente com voice guard desabilitado passa sempre
        return VoiceGuardResult(
            score=100,
            aprovado=True,
            dimensoes={"voice_guard": 100},
            avisos=[f"voice guard desabilitado para cliente '{client.id}'"],
        )

    s_cliche, err_cliche = _score_anti_cliche(text)
    s_bloom, err_bloom, av_bloom = _score_bloom_andragogia(text)
    s_naming, err_naming, err_criticos_naming, av_naming = _score_naming(text, client)
    s_hbr, err_hbr, av_hbr = _score_hbr_style(text, client)

    weighted = (
        s_cliche * WEIGHTS["anti_cliche"]
        + s_bloom * WEIGHTS["bloom_andragogia"]
        + s_naming * WEIGHTS["naming"]
        + s_hbr * WEIGHTS["hbr_style"]
    ) / 100

    score = int(round(weighted))
    min_score = client.voice_guard.min_score
    aprovado = score >= min_score and len(err_criticos_naming) == 0

    return VoiceGuardResult(
        score=score,
        aprovado=aprovado,
        dimensoes={
            "anti_cliche (peso 30)": s_cliche,
            "bloom_andragogia (peso 30)": s_bloom,
            "naming canonico (peso 25)": s_naming,
            "hbr_style (peso 15)": s_hbr,
        },
        erros=err_cliche + err_bloom + err_naming + err_hbr,
        erros_criticos=err_criticos_naming,
        avisos=av_bloom + av_naming + av_hbr,
    )
