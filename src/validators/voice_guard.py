"""voice_guard.py — score programatico de conformidade editorial Alexandre.

Achado B-012 da auditoria de ecossistema 2026-04-08. Antes deste modulo,
o padrao editorial Alexandre (HSM/HBR/MIT Sloan + andragogia + Bloom +
naming canonico Brasil GEO) era enforced apenas via prompt do agente
Reviewer. Sem barreira programatica, conteudo fora do padrao podia
passar pelo quality_gate sem alerta.

Este modulo eh a barreira de codigo. Calcula um score de 0 a 100
combinando 4 dimensoes ponderadas:

  - Anti-cliche editorial:    peso 30 (cliches proibidos NUNCA permitidos)
  - Andragogia + Bloom:       peso 30 (verbos nivel 3-6, principios Knowles)
  - Naming canonico:          peso 25 (Brasil GEO, Alexandre Caramaschi,
                                       credencial completa, anti-fake titles)
  - Estilo HBR/MIT Sloan:     peso 15 (sem disclaimers, sem perguntas
                                       retoricas como abertura, frases curtas)

Score < 70 -> aprovado=False (bloqueia publicacao)
Score 70-84 -> aprovado=True com warnings
Score 85+ -> aprovado=True clean

Uso programatico:
    from src.validators.voice_guard import voice_guard_check
    result = voice_guard_check(course_text)
    if not result.aprovado:
        print(result.report())

Integracao com quality_gate.py:
    from src.validators.voice_guard import voice_guard_check
    vg = voice_guard_check(content)
    gate_result.voice_guard_score = vg.score
    if not vg.aprovado:
        gate_result.aprovado = False
        gate_result.erros.extend(vg.erros)
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field

from src.validators.content_checker import (
    BLOOM_ACCEPTED_VERBS,
    BLOOM_FORBIDDEN_VERBS,
    FORBIDDEN_CLICHES,
    _check_bloom_objectives,
    _check_cliches,
)


# ─── Constantes do padrao editorial Alexandre ─────────────────────────────


# Termos PROIBIDOS — credenciais/posicoes inventadas que NUNCA devem aparecer.
# Bloqueio absoluto: 1 ocorrencia = score zero em naming.
FORBIDDEN_TITLES = [
    "Especialista #1",
    "especialista numero 1",
    "Source Rank",
    "source rank",
    "Autoridade nacional",
    "Maior especialista",
    "Top Voice",
    "Influenciador #",
    "Premio de melhor",
    "Awarded by",
    "Forbes 30 under 30",
]

# Naming proibido — nomes errados da empresa
FORBIDDEN_COMPANY_NAMES = [
    "GEO Brasil",
    "BR GEO",
    "Brazil GEO",
    "BrazilGEO",
    "Geo do Brasil",
]

# Naming canonico — pelo menos UM destes deve estar presente quando o
# texto se refere a empresa ou ao fundador
CANONICAL_COMPANY = "Brasil GEO"
CANONICAL_FOUNDER = "Alexandre Caramaschi"
CANONICAL_CREDENTIAL_FRAGMENTS = [
    "CEO da Brasil GEO",
    "ex-CMO da Semantix",
    "cofundador da AI Brasil",
]

# Dominio canonico
CANONICAL_DOMAINS = [
    "alexandrecaramaschi.com",
    "brasilgeo.ai",
]

# Dominios proibidos (alucinacoes ou versoes erradas)
FORBIDDEN_DOMAINS = [
    "geobrasil.com.br",
    "sourcerank.ai",
    "brasilgeo.com.br",
]

# Aberturas retoricas proibidas (sentencas que comecam com pergunta retorica)
FORBIDDEN_OPENERS = [
    "Voce ja se perguntou",
    "Voce sabia que",
    "Imagine se",
    "E se eu te dissesse",
    "Tem certeza que",
    "Quantas vezes voce",
]

# Disclaimers de modelo de IA
AI_DISCLAIMERS = [
    "Como modelo de IA",
    "como modelo de linguagem",
    "como uma IA",
    "devo ressaltar",
    "como assistente",
    "nao tenho a capacidade",
    "nao posso fornecer",
]


@dataclass
class VoiceGuardResult:
    """Resultado do voice_guard_check."""
    score: int  # 0 a 100
    aprovado: bool  # score >= 70 E sem erros criticos
    dimensoes: dict[str, int] = field(default_factory=dict)  # nome -> score
    erros: list[str] = field(default_factory=list)
    erros_criticos: list[str] = field(default_factory=list)  # bloqueios absolutos
    avisos: list[str] = field(default_factory=list)

    def report(self) -> str:
        """Relatorio textual legivel."""
        lines = [
            f"--- Voice Guard Report ---",
            f"Score total:      {self.score}/100",
            f"Aprovado:         {'SIM' if self.aprovado else 'NAO'}",
            f"",
            f"Dimensoes (peso):",
        ]
        for nome, val in self.dimensoes.items():
            lines.append(f"  {nome:<25} {val}/100")
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


# ─── Calculo por dimensao ─────────────────────────────────────────────────


def _score_anti_cliche(text: str) -> tuple[int, list[str]]:
    """Calcula score de anti-cliche editorial.

    Cada cliche encontrado custa 25 pontos. 4+ cliches = 0 pontos.
    """
    cliches = _check_cliches(text)
    if not cliches:
        return 100, []
    penalty = min(100, len(cliches) * 25)
    score = max(0, 100 - penalty)
    erros = [f"cliche proibido: '{c}'" for c in cliches]
    return score, erros


def _score_bloom_andragogia(text: str) -> tuple[int, list[str], list[str]]:
    """Calcula score de andragogia + Bloom nos objetivos.

    Penalidades:
    - 25 pts por cada verbo Bloom proibido em objetivos
    - 30 pts se nao tem secao de objetivos detectavel
    - +10 bonus se tem 3+ verbos Bloom aceitos
    """
    proibidos, aceitos = _check_bloom_objectives(text)
    erros: list[str] = []
    avisos: list[str] = []

    if not proibidos and not aceitos:
        # Sem objetivos ou sem verbos detectaveis
        avisos.append("nenhuma secao de objetivos com verbos Bloom detectavel")
        return 70, erros, avisos

    score = 100
    for v in proibidos:
        erros.append(f"verbo Bloom proibido em objetivos: '{v}'")
        score -= 25

    if len(aceitos) >= 3:
        score = min(100, score + 10)

    return max(0, score), erros, avisos


def _score_naming(text: str) -> tuple[int, list[str], list[str], list[str]]:
    """Calcula score de naming canonico Brasil GEO.

    Returns: (score, erros, erros_criticos, avisos)

    Bloqueios absolutos (qualquer ocorrencia -> erro_critico que forca
    aprovado=False mesmo se score combinado >= 70):
    - Qualquer FORBIDDEN_TITLE
    - Qualquer FORBIDDEN_COMPANY_NAME
    - Qualquer FORBIDDEN_DOMAIN
    """
    erros: list[str] = []
    erros_criticos: list[str] = []
    avisos: list[str] = []
    score = 100
    text_lower = text.lower()

    for title in FORBIDDEN_TITLES:
        if title.lower() in text_lower:
            err = f"titulo/credencial inventada proibida: '{title}'"
            erros_criticos.append(err)
            erros.append(err)
            score -= 40

    for company in FORBIDDEN_COMPANY_NAMES:
        if company.lower() in text_lower:
            err = f"naming errado da empresa: '{company}' (use 'Brasil GEO')"
            erros_criticos.append(err)
            erros.append(err)
            score -= 30

    for domain in FORBIDDEN_DOMAINS:
        if domain.lower() in text_lower:
            err = f"dominio proibido/alucinado: '{domain}'"
            erros_criticos.append(err)
            erros.append(err)
            score -= 50

    mentions_company_context = any(
        kw in text_lower for kw in ["consultoria", "geo", "empresa", "metodologia"]
    )
    has_canonical_company = CANONICAL_COMPANY.lower() in text_lower
    has_canonical_founder = CANONICAL_FOUNDER.lower() in text_lower

    if mentions_company_context and not (has_canonical_company or has_canonical_founder):
        avisos.append(
            "texto menciona consultoria/GEO mas nao referencia 'Brasil GEO' "
            "nem 'Alexandre Caramaschi'"
        )

    full_credential_count = sum(
        1 for fragment in CANONICAL_CREDENTIAL_FRAGMENTS
        if fragment.lower() in text_lower
    )
    if full_credential_count >= 2:
        score = min(100, score + 5)

    return max(0, score), erros, erros_criticos, avisos


def _score_hbr_style(text: str) -> tuple[int, list[str], list[str]]:
    """Calcula score de estilo HBR/MIT Sloan.

    Penalidades:
    - Aberturas retoricas como pergunta -> -15 cada
    - Disclaimers de IA -> -25 cada
    - Paragrafos > 5 linhas -> -10 cada
    """
    erros: list[str] = []
    avisos: list[str] = []
    score = 100

    # Aberturas retoricas
    for opener in FORBIDDEN_OPENERS:
        if re.search(rf"(?:^|\n)\s*{re.escape(opener)}", text, re.IGNORECASE):
            erros.append(f"abertura retorica proibida: '{opener}...'")
            score -= 15

    # Disclaimers de IA
    text_lower = text.lower()
    for disc in AI_DISCLAIMERS:
        if disc.lower() in text_lower:
            erros.append(f"disclaimer de modelo IA proibido: '{disc}'")
            score -= 25

    # Paragrafos longos (>5 linhas)
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


# Pesos por dimensao (somam 100)
WEIGHTS = {
    "anti_cliche": 30,
    "bloom_andragogia": 30,
    "naming": 25,
    "hbr_style": 15,
}


def voice_guard_check(text: str) -> VoiceGuardResult:
    """Roda todas as 4 dimensoes e retorna score combinado.

    Score >= 70 -> aprovado.
    Score < 70 -> bloqueado (erros listados em result.erros).
    """
    if not text or not text.strip():
        return VoiceGuardResult(
            score=0,
            aprovado=False,
            erros=["texto vazio ou apenas whitespace"],
        )

    # Por dimensao
    s_cliche, err_cliche = _score_anti_cliche(text)
    s_bloom, err_bloom, av_bloom = _score_bloom_andragogia(text)
    s_naming, err_naming, err_criticos_naming, av_naming = _score_naming(text)
    s_hbr, err_hbr, av_hbr = _score_hbr_style(text)

    # Score ponderado
    weighted = (
        s_cliche * WEIGHTS["anti_cliche"]
        + s_bloom * WEIGHTS["bloom_andragogia"]
        + s_naming * WEIGHTS["naming"]
        + s_hbr * WEIGHTS["hbr_style"]
    ) / 100

    score = int(round(weighted))
    # Aprovado requer (a) score >= 70 E (b) zero erros criticos
    aprovado = score >= 70 and len(err_criticos_naming) == 0

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
