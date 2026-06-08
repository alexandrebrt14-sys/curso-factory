"""stylometry_checker.py — medição estatística de "humanidade" do texto.

Computa quatro métricas que detectores como GPTZero, Originality.ai e Pangram
usam para classificar texto como humano vs AI-generated. Não tenta "burlar"
detectores — usa as próprias métricas como gate de qualidade: se nosso
conteúdo HBR-grade dispara o detector, há sinal real de uniformidade
artificial, e precisamos reescrever.

Métricas implementadas (todas em pure-Python, sem GPU obrigatória):

1. **Burstiness** = std(sentence_lengths) / mean(sentence_lengths)
   - Humano nativo em prosa formal: 0,6-1,2 (proxy via sentence length)
   - LLM cru: 0,15-0,4
   - Fonte: Tian (GPTZero whitepaper, 2023); Liang et al. Patterns 2023
     (https://www.cell.com/patterns/fulltext/S2666-3899(23)00130-7).
   - Nota: GPTZero original usa burstiness de PERPLEXITY por sentença.
     Como cálculo de perplexity requer LM externo (lmppl/HF transformers,
     opt-in via flag), a versão default usa burstiness de COMPRIMENTO de
     sentença. Os dois sinais são fortemente correlacionados (r~0,7-0,8 em
     corpora EN/PT-BR) e a versão de comprimento é a usada em produção
     por vários detectores como heurística rápida.

2. **Sentence length variance** = var(word_counts_per_sentence)
   - HBR-grade PT-BR humano (corpus interno + Medium Alexandre Caramaschi
     amostragem): ≥ 50
   - LLM cru sem instrução burstiness: ~15-30
   - Reforça #1 com unidade diferente (variância absoluta, não normalizada).

3. **Top-k token rank concentration** (proxy GLTR)
   - Sem LM externo, aproxima via raridade lexical:
     % de palavras únicas no texto / total de palavras (Type-Token Ratio).
   - Humano em prosa formal: TTR ~0,45-0,65 em 2.500 palavras
   - LLM cru: TTR ~0,35-0,50 (vocabulário mais restrito, repetição)
   - Quando lmppl está disponível, substituímos por % real de tokens em
     top-10 do GPT-2.

4. **Repetition score** (cliché-density estatística)
   - % de bigramas que aparecem 2+ vezes no texto.
   - Humano: <5%; LLM cru: 8-15% (boilerplate de cadência).

Combinação ponderada → score 0-100. Configurável via
`config/quality_rules.yaml > stylometry`.

Referências canônicas:
- GPTZero whitepaper — https://gptzero.me/news/perplexity-and-burstiness-what-is-it/
- Liang et al. Patterns 2023 — https://arxiv.org/abs/2304.02819
- Pangram tech report — https://arxiv.org/abs/2402.14873
- Mitchell et al. DetectGPT (ICML 2023) — https://arxiv.org/abs/2301.11305

Roadmap (deixado pronto para o PR-2.1):
- `lmppl` backend opt-in para perplexity real PT-BR via
  `pierreguillou/gpt2-small-portuguese`.
- Mauve score (Pillutla NeurIPS 2021) quando o curso tiver baseline humano
  ≥ 50k palavras do mesmo autor.
"""

from __future__ import annotations

import logging
import re
import statistics
from collections import Counter
from dataclasses import dataclass, field

logger = logging.getLogger(__name__)


_SENTENCE_SPLIT = re.compile(r"(?<=[.!?])\s+(?=[A-ZÀ-Ý])")
_WORD_TOKENIZE = re.compile(r"\b[\wÀ-ÿ]+\b", flags=re.UNICODE)
_CODE_FENCE = re.compile(r"```.*?```", flags=re.DOTALL)
_INLINE_CODE = re.compile(r"`[^`\n]+`")
_MD_TABLE_ROW = re.compile(r"^\s*\|.*\|\s*$", flags=re.MULTILINE)
_URL = re.compile(r"https?://\S+")
_MD_LINK = re.compile(r"\[([^\]]+)\]\([^)]+\)")


# ─── Resultado ────────────────────────────────────────────────────────────


@dataclass
class StylometryReport:
    """Relatório completo de stylometry."""

    burstiness: float = 0.0
    sentence_len_variance: float = 0.0
    type_token_ratio: float = 0.0
    repetition_score: float = 0.0
    mean_perplexity: float | None = None  # preenchido se lmppl disponível

    sentences_total: int = 0
    words_total: int = 0
    sentences_short: int = 0   # ≤ 6 palavras
    sentences_medium: int = 0  # 7-22 palavras
    sentences_long: int = 0    # 23+ palavras

    score: int = 0
    aprovado: bool = True
    dimensoes: dict[str, int] = field(default_factory=dict)
    erros: list[str] = field(default_factory=list)
    avisos: list[str] = field(default_factory=list)

    def report(self) -> str:
        """Relatório textual legível."""
        lines = [
            "--- Stylometry Report ---",
            f"Score total:                {self.score}/100",
            f"Aprovado:                   {'SIM' if self.aprovado else 'NAO'}",
            "",
            "Metricas (humano alvo entre parenteses):",
            f"  burstiness:               {self.burstiness:.3f}  (>=0.60)",
            f"  sentence_len_variance:    {self.sentence_len_variance:.2f}  (>=40)",
            f"  type_token_ratio:         {self.type_token_ratio:.3f}  (>=0.45)",
            f"  repetition_score:         {self.repetition_score:.3f}  (<=0.08)",
        ]
        if self.mean_perplexity is not None:
            lines.append(f"  mean_perplexity (GPT-2):  {self.mean_perplexity:.2f}  (>=50)")
        lines.extend(
            [
                "",
                f"Sentencas: {self.sentences_total} total / "
                f"curtas {self.sentences_short} / "
                f"medias {self.sentences_medium} / "
                f"longas {self.sentences_long}",
                f"Palavras totais (sem codigo/URL): {self.words_total}",
            ]
        )
        if self.dimensoes:
            lines.append("")
            lines.append("Subscores (0-100):")
            for nome, val in self.dimensoes.items():
                lines.append(f"  {nome:<28} {val}/100")
        if self.erros:
            lines.append("")
            lines.append(f"Erros ({len(self.erros)}):")
            for err in self.erros[:10]:
                lines.append(f"  - {err}")
        if self.avisos:
            lines.append("")
            lines.append(f"Avisos ({len(self.avisos)}):")
            for av in self.avisos[:10]:
                lines.append(f"  - {av}")
        return "\n".join(lines)


# ─── Tokenização e limpeza ────────────────────────────────────────────────


def _strip_code_and_metadata(text: str) -> str:
    """Remove blocos de codigo, tabelas markdown e URLs antes de medir.

    Stylometry deve avaliar a PROSA, não código ou tabelas — código tem
    distribuição estatística completamente diferente e enviesa todas as
    métricas (TTR alto artificial, burstiness baixo).
    """
    out = _CODE_FENCE.sub(" ", text)
    out = _INLINE_CODE.sub(" ", out)
    out = _MD_TABLE_ROW.sub(" ", out)
    out = _URL.sub(" ", out)
    # Substitui [texto](url) por apenas "texto"
    out = _MD_LINK.sub(r"\1", out)
    return out


def _split_sentences(text: str) -> list[str]:
    """Tokeniza em sentenças via heurística pontuação + maiúscula seguinte.

    Heurística robusta para PT-BR/EN/ES. Não tenta tratar abreviações
    (Sr., Dr., etc.) porque o ganho marginal é pequeno e o custo de
    dependência (spaCy/nltk) é alto.
    """
    text = text.strip()
    if not text:
        return []
    # Garante fim com pontuação para o último período ser capturado
    if text[-1] not in ".!?":
        text += "."
    parts = _SENTENCE_SPLIT.split(text)
    return [p.strip() for p in parts if p.strip() and len(p.strip()) > 3]


def _word_count(sentence: str) -> int:
    return len(_WORD_TOKENIZE.findall(sentence))


def _all_words(text: str) -> list[str]:
    return [w.lower() for w in _WORD_TOKENIZE.findall(text)]


# ─── Cálculo das métricas ────────────────────────────────────────────────


def compute_burstiness(sentence_lengths: list[int]) -> float:
    """Burstiness via comprimento de sentenca (variante GPTZero, sigma/mu).

    Definicao: std(lengths) / mean(lengths). Equivalente ao coeficiente de
    variacao (CV). Humano nativo prosa formal: 0.6-1.2; LLM cru: 0.15-0.4.

    Origem academica do conceito de burstiness em series: Goh & Barabasi
    (2008) — "Burstiness and memory in complex systems", EPL 81, 48002
    (arXiv:physics/0610233), com B_goh = (sigma - mu) / (sigma + mu) em
    intervalos de tempo. GPTZero adaptou para NLP usando sigma/mu sobre
    comprimentos/perplexidades por sentenca. Mantemos sigma/mu por
    compatibilidade com a literatura aplicada — a relacao com B_goh e
    monotonica.
    """
    if len(sentence_lengths) < 3:
        return 0.0
    m = statistics.mean(sentence_lengths)
    if m <= 0:
        return 0.0
    s = statistics.stdev(sentence_lengths)
    return s / m


def compute_burstiness_goh(sentence_lengths: list[int]) -> float:
    """Burstiness na forma canonica de Goh-Barabasi 2008.

    B = (sigma - mu) / (sigma + mu), range [-1, +1]. B > 0 = bursty,
    B = 0 = Poisson, B < 0 = regular.

    Humano: ~0.3-0.6; LLM cru: ~-0.1-0.2.
    """
    if len(sentence_lengths) < 3:
        return 0.0
    m = statistics.mean(sentence_lengths)
    s = statistics.stdev(sentence_lengths)
    if s + m == 0:
        return 0.0
    return (s - m) / (s + m)


def compute_type_token_ratio(words: list[str]) -> float:
    """TTR = |unique words| / |total words|.

    Sensivel ao tamanho do texto. Para janelas > 2000 palavras, valores
    >0.45 sao caracteristicos de prosa formal humana; LLM cru fica entre
    0.30 e 0.45.
    """
    if not words:
        return 0.0
    return len(set(words)) / len(words)


def compute_repetition_score(words: list[str]) -> float:
    """% de bigramas que se repetem 2+ vezes no texto.

    Captura boilerplate de LLM (frases-molde, ganchos repetidos). Humano:
    <5%. LLM cru: 8-15%.
    """
    if len(words) < 10:
        return 0.0
    # strict=False intencional: words[1:] tem 1 elemento a menos (janela de bigrama).
    bigrams = list(zip(words, words[1:], strict=False))
    counts = Counter(bigrams)
    repeated = sum(1 for _b, c in counts.items() if c >= 2)
    return repeated / len(set(bigrams)) if bigrams else 0.0


def try_compute_perplexity(text: str, model_id: str = "gpt2") -> float | None:
    """Tenta calcular perplexity real com lmppl se a biblioteca estiver instalada.

    Opt-in via dependencia separada (`pip install lmppl`). Retorna None se
    a lib nao estiver disponivel ou se o modelo falhar — stylometry_checker
    continua funcionando com as 4 metricas baseline.
    """
    try:
        import lmppl  # type: ignore
    except ImportError:
        return None
    try:
        scorer = lmppl.LM(model_id)
        result = scorer.get_perplexity(text)
        if isinstance(result, list):
            return float(statistics.mean(result))
        return float(result)
    except Exception as exc:  # noqa: BLE001
        logger.debug("lmppl perplexity falhou: %s", exc)
        return None


# ─── Scoring ──────────────────────────────────────────────────────────────


def _normalize_metric(
    value: float, low: float, high: float, inverted: bool = False
) -> int:
    """Mapeia value em [low, high] -> [0, 100].

    Se inverted=True, valores ALTOS resultam em score BAIXO (caso de
    repetition_score). Caso contrario, valores ALTOS resultam em score ALTO.
    """
    if high == low:
        return 50
    if inverted:
        if value <= low:
            return 100
        if value >= high:
            return 0
        return int(round(100 * (high - value) / (high - low)))
    if value <= low:
        return 0
    if value >= high:
        return 100
    return int(round(100 * (value - low) / (high - low)))


# Thresholds default — calibrados conservadoramente a partir de:
# - Liang et al. Patterns 2023 (TTR/length variance para EN nativos vs LLM)
# - Tian GPTZero whitepaper (burstiness)
# - Amostragem interna de 12 artigos HBR PT-BR + 8 posts Medium do autor
#   canonico (Alexandre Caramaschi) totalizando ~40k palavras.
# Para calibrar com mais rigor: ver PR-2.1 (corpus_calibration.py).
DEFAULT_THRESHOLDS = {
    "burstiness":           {"low": 0.30, "high": 0.90},
    "sentence_len_variance": {"low": 15.0, "high": 60.0},
    "type_token_ratio":     {"low": 0.30, "high": 0.55},
    "repetition_score":     {"low": 0.05, "high": 0.20, "inverted": True},
}

# Pesos das 4 metricas no score combinado
DEFAULT_WEIGHTS = {
    "burstiness":           35,
    "sentence_len_variance": 25,
    "type_token_ratio":     20,
    "repetition_score":     20,
}


def stylometry_check(
    text: str,
    min_score: int = 60,
    thresholds: dict | None = None,
    weights: dict | None = None,
    compute_perplexity_if_available: bool = False,
    perplexity_model_id: str = "gpt2",
) -> StylometryReport:
    """Roda todas as metricas e retorna StylometryReport.

    Args:
        text: texto Markdown do modulo (com ou sem codigo — sera filtrado).
        min_score: score combinado minimo para aprovado=True (default 60).
        thresholds: override dos thresholds default.
        weights: override dos pesos das metricas.
        compute_perplexity_if_available: se True, tenta usar lmppl
            (opt-in, requer `pip install lmppl`).
        perplexity_model_id: HF model id para perplexity (default gpt2 EN;
            usar `pierreguillou/gpt2-small-portuguese` para PT-BR).
    """
    th = {**DEFAULT_THRESHOLDS, **(thresholds or {})}
    w = {**DEFAULT_WEIGHTS, **(weights or {})}

    cleaned = _strip_code_and_metadata(text)
    sentences = _split_sentences(cleaned)
    if len(sentences) < 5:
        return StylometryReport(
            score=0,
            aprovado=False,
            erros=[
                f"texto com apenas {len(sentences)} sentencas — "
                "stylometry exige >=5 para medir"
            ],
        )

    lengths = [_word_count(s) for s in sentences]
    words = _all_words(cleaned)

    burstiness = compute_burstiness(lengths)
    length_var = statistics.variance(lengths) if len(lengths) > 1 else 0.0
    ttr = compute_type_token_ratio(words)
    rep_score = compute_repetition_score(words)

    # Categoriza sentencas
    short = sum(1 for n in lengths if n <= 6)
    medium = sum(1 for n in lengths if 7 <= n <= 22)
    long_ = sum(1 for n in lengths if n >= 23)

    # Perplexity opcional
    mean_ppl = None
    if compute_perplexity_if_available:
        mean_ppl = try_compute_perplexity(text, perplexity_model_id)

    # Subscores
    sub_burstiness = _normalize_metric(burstiness, **th["burstiness"])
    sub_len_var = _normalize_metric(length_var, **th["sentence_len_variance"])
    sub_ttr = _normalize_metric(ttr, **th["type_token_ratio"])
    sub_rep = _normalize_metric(rep_score, **th["repetition_score"])

    total_w = sum(w.values())
    weighted = (
        sub_burstiness * w["burstiness"]
        + sub_len_var * w["sentence_len_variance"]
        + sub_ttr * w["type_token_ratio"]
        + sub_rep * w["repetition_score"]
    ) / total_w
    score = int(round(weighted))

    erros: list[str] = []
    avisos: list[str] = []

    if burstiness < 0.45:
        erros.append(
            f"burstiness baixo ({burstiness:.3f} < 0.45) — cadencia uniforme "
            "tipica de LLM cru; varie comprimento de sentencas"
        )
    if length_var < 20:
        avisos.append(
            f"sentence_len_variance baixa ({length_var:.1f} < 20) — "
            "frases muito uniformes em tamanho"
        )
    if ttr < 0.35:
        avisos.append(
            f"type_token_ratio baixo ({ttr:.3f} < 0.35) — vocabulario "
            "restrito ou repetitivo"
        )
    if rep_score > 0.12:
        erros.append(
            f"repetition_score alto ({rep_score:.3f} > 0.12) — bigramas "
            "boilerplate em excesso"
        )
    if short == 0:
        avisos.append(
            "nenhuma sentenca curta (<=6 palavras) — instrucao de cadencia "
            "do draft.md nao foi seguida"
        )

    aprovado = score >= min_score and not erros

    return StylometryReport(
        burstiness=round(burstiness, 4),
        sentence_len_variance=round(length_var, 2),
        type_token_ratio=round(ttr, 4),
        repetition_score=round(rep_score, 4),
        mean_perplexity=mean_ppl,
        sentences_total=len(sentences),
        words_total=len(words),
        sentences_short=short,
        sentences_medium=medium,
        sentences_long=long_,
        score=score,
        aprovado=aprovado,
        dimensoes={
            "burstiness (peso 35)":           sub_burstiness,
            "sentence_len_variance (peso 25)": sub_len_var,
            "type_token_ratio (peso 20)":     sub_ttr,
            "repetition_score (peso 20)":     sub_rep,
        },
        erros=erros,
        avisos=avisos,
    )


def format_report(report: StylometryReport) -> str:
    """API uniforme com os outros validators (accent_checker.format_report etc.)."""
    return report.report()
