"""Testes para os modulos de humanizacao (PRs 2, 5, 6, 8).

Cobre stylometry_checker, disclosure_checker, detection_tracker e
integracao no quality_gate (camadas 5 e 6).
"""

from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.clients import load_client
from src.clients.context import (
    DisclosureConfig,
    VoiceSample,
    VoiceSamplesConfig,
)
from src.detection_tracker import DetectionEntry, DetectionTracker
from src.validators.disclosure_checker import (
    build_disclosure_block,
    disclosure_check,
)
from src.validators.quality_gate import QualityGate
from src.validators.stylometry_checker import (
    compute_burstiness,
    compute_burstiness_goh,
    compute_repetition_score,
    compute_type_token_ratio,
    stylometry_check,
)


# ─── stylometry_checker — fórmulas isoladas ──────────────────────────


def test_burstiness_zero_quando_todas_iguais() -> None:
    """Lengths idênticas → desvio-padrão zero → burstiness = 0."""
    assert compute_burstiness([10, 10, 10, 10]) == 0.0


def test_burstiness_positiva_para_lengths_variados() -> None:
    """Lengths diferentes → CV > 0."""
    b = compute_burstiness([4, 10, 25, 30, 5])
    assert b > 0.3


def test_burstiness_goh_no_intervalo_canonico() -> None:
    """Goh-Barabasi B = (sigma - mu) / (sigma + mu) ∈ [-1, +1]."""
    b = compute_burstiness_goh([4, 10, 25, 30, 5, 8, 22, 18])
    assert -1.0 <= b <= 1.0


def test_burstiness_amostra_pequena_retorna_zero() -> None:
    """N < 3 deve retornar 0 (insuficiente)."""
    assert compute_burstiness([10]) == 0.0
    assert compute_burstiness([10, 20]) == 0.0


def test_type_token_ratio_vocabulario_repetitivo() -> None:
    words = ["o", "o", "o", "o", "o"]
    assert compute_type_token_ratio(words) == 1 / 5


def test_type_token_ratio_vocabulario_unico() -> None:
    words = ["um", "dois", "tres", "quatro", "cinco"]
    assert compute_type_token_ratio(words) == 1.0


def test_repetition_score_baixo_em_texto_natural() -> None:
    words = "o gato subiu no telhado da casa azul que fica na esquina".split()
    score = compute_repetition_score(words)
    assert score == 0.0  # nenhum bigrama repete


def test_repetition_score_alto_em_boilerplate() -> None:
    # ≥10 palavras (limite minimo da funcao) com bigrama "o gato" repetido
    words = (
        "o gato gosta o gato corre o gato dorme e o gato pula"
    ).split()
    score = compute_repetition_score(words)
    assert score > 0.0


# ─── stylometry_check — integração ─────────────────────────────────


def _sample_text_humano_like() -> str:
    """Texto curto com cadencia variada (faixas alternadas)."""
    return (
        "Em 2024, a Stone reportou reducao de 23% no tempo de aprovacao. "
        "O dado importa. "
        "Mostra que o ganho de IA generativa em PMEs brasileiras saiu da promessa. "
        "Entrou no balanco. "
        "Pelo menos para quem mediu antes de adotar a tecnologia de forma sistematica. "
        "Os 23 pontos vieram de 3 mil contratos auditados pelo time interno."
    )


def _sample_text_llm_uniforme() -> str:
    """Texto com cadencia uniforme — todas frases 16-20 palavras."""
    return (
        "A inteligencia artificial generativa transforma a forma como empresas "
        "brasileiras tomam decisoes operacionais durante o ano corrente. "
        "Os modelos de linguagem natural permitem analise de grandes volumes "
        "de texto com latencia reduzida e custo marginal muito pequeno. "
        "Empresas que adotam essa tecnologia conseguem ganhos mensuraveis em "
        "produtividade e velocidade de resposta ao mercado consumidor brasileiro. "
        "A adocao em larga escala ainda enfrenta barreiras culturais e tecnicas "
        "que requerem investimento continuo em treinamento e infraestrutura."
    )


def test_stylometry_texto_curto_retorna_aviso() -> None:
    """< 5 sentencas → erro em vez de score zoado."""
    r = stylometry_check("Frase um. Frase dois.")
    assert r.aprovado is False
    assert any("5 sentencas" in e or "sentencas" in e for e in r.erros)


def test_stylometry_humano_like_burstiness_maior_que_llm() -> None:
    r_humano = stylometry_check(_sample_text_humano_like())
    r_llm = stylometry_check(_sample_text_llm_uniforme())
    # Texto com cadencia variada deve ter burstiness mais alta
    assert r_humano.burstiness > r_llm.burstiness


def test_stylometry_score_no_intervalo_zero_cem() -> None:
    r = stylometry_check(_sample_text_humano_like())
    assert 0 <= r.score <= 100


def test_stylometry_report_text_legivel() -> None:
    r = stylometry_check(_sample_text_humano_like())
    txt = r.report()
    assert "Stylometry Report" in txt
    assert "burstiness" in txt
    assert "Sentencas" in txt


def test_stylometry_ignora_blocos_de_codigo() -> None:
    """Codigo nao deve viesar TTR/burstiness."""
    text = _sample_text_humano_like() + "\n\n```python\nx = 1\ny = 2\nz = 3\n```\n"
    r_com = stylometry_check(text)
    r_sem = stylometry_check(_sample_text_humano_like())
    # Diferencas devem ser pequenas — codigo foi removido antes da medicao
    assert abs(r_com.burstiness - r_sem.burstiness) < 0.15


# ─── disclosure_checker ────────────────────────────────────────────


def test_disclosure_desabilitado_passa_sempre(monkeypatch) -> None:
    """Cliente com disclosure.enabled=False nao bloqueia nada."""
    client = load_client("default")
    client.disclosure = DisclosureConfig(enabled=False)
    r = disclosure_check("texto qualquer", client=client)
    assert r.aprovado is True


def test_disclosure_block_if_missing_false_emite_aviso() -> None:
    """block_if_missing=False → aprovado=True mas avisos populados."""
    client = load_client("default")
    # Configuracao default tem block_if_missing=False
    assert client.disclosure.block_if_missing is False
    r = disclosure_check("Texto sem disclosure algum.", client=client)
    assert r.aprovado is True  # nao bloqueia
    assert len(r.avisos) > 0   # mas avisa


def test_disclosure_block_if_missing_true_bloqueia() -> None:
    """Com block_if_missing=True, ausencia bloqueia."""
    client = load_client("default")
    client.disclosure = DisclosureConfig(
        enabled=True,
        required_by=["PL_2338_2023"],
        block_if_missing=True,
    )
    r = disclosure_check("Texto sem disclosure algum.", client=client)
    assert r.aprovado is False
    assert len(r.erros) > 0


def test_disclosure_detecta_bloco_canonico() -> None:
    """Texto com bloco padrao + autor + norma passa."""
    client = load_client("default")
    client.disclosure.block_if_missing = True
    bloco = build_disclosure_block(client)
    r = disclosure_check(bloco, client=client)
    # bloco padrao tem todos os marcadores
    assert r.tem_bloco_disclosure is True
    assert r.tem_autor_canonico is True


def test_build_disclosure_block_inclui_autor() -> None:
    client = load_client("default")
    block = build_disclosure_block(client)
    assert client.author.name in block
    assert "PL 2338" in block or "pl 2338" in block.lower()


def test_build_disclosure_block_vazio_se_desabilitado() -> None:
    client = load_client("default")
    client.disclosure = DisclosureConfig(enabled=False)
    assert build_disclosure_block(client) == ""


# ─── voice_samples (PR-5) ──────────────────────────────────────────


def test_voice_samples_config_default_desabilitado() -> None:
    client = load_client("default")
    assert client.voice_guard.voice_samples.enabled is False
    assert client.voice_guard.voice_samples.samples == []


def test_voice_samples_config_aceita_amostras() -> None:
    vs = VoiceSamplesConfig(
        enabled=True,
        samples=[
            VoiceSample(path="a.md", length_words=1000, tags=["x"]),
            VoiceSample(path="b.md", length_words=500),
        ],
        anchor_strategy="concat",
        anchor_max_words=1500,
    )
    assert vs.enabled is True
    assert len(vs.samples) == 2
    assert vs.samples[0].length_words == 1000


# ─── detection_tracker (PR-8) ──────────────────────────────────────


def test_detection_tracker_persiste_e_le() -> None:
    tmp = Path(tempfile.mkdtemp()) / "history.jsonl"
    t = DetectionTracker(path=tmp)
    entry = DetectionEntry(
        ts="2026-05-17T15:00:00+00:00",
        course_id="c1",
        module_name="m1",
        client_id="default",
        stylometry_score=75,
        burstiness=0.85,
        sentence_len_variance=120.0,
        type_token_ratio=0.5,
        repetition_score=0.04,
        mean_perplexity=None,
        voice_guard_score=88,
        disclosure_ok=True,
        pangram_score=None,
        aprovado_gate=True,
        pipeline_version="5.2",
    )
    t.record(entry)
    entries = t.load_entries()
    assert len(entries) == 1
    assert entries[0]["stylometry_score"] == 75
    assert entries[0]["course_id"] == "c1"


def test_detection_tracker_filtro_por_cliente() -> None:
    tmp = Path(tempfile.mkdtemp()) / "history.jsonl"
    t = DetectionTracker(path=tmp)
    for cid in ["default", "acme", "default"]:
        t.record(DetectionEntry(
            ts="2026-05-17T15:00:00+00:00",
            course_id="c", module_name="m", client_id=cid,
            stylometry_score=70, burstiness=0.7,
            sentence_len_variance=0.0, type_token_ratio=0.0,
            repetition_score=0.0, mean_perplexity=None,
            voice_guard_score=80, disclosure_ok=True,
            pangram_score=None, aprovado_gate=True,
            pipeline_version="5.2",
        ))
    only_default = t.load_entries(client_id="default")
    only_acme = t.load_entries(client_id="acme")
    assert len(only_default) == 2
    assert len(only_acme) == 1


def test_detection_tracker_report_text_legivel() -> None:
    tmp = Path(tempfile.mkdtemp()) / "history.jsonl"
    t = DetectionTracker(path=tmp)
    # Sem entradas
    assert "Nenhum registro" in t.report_text()
    # Com entrada
    t.record(DetectionEntry(
        ts="2026-05-17T15:00:00+00:00",
        course_id="c1", module_name="m1", client_id="default",
        stylometry_score=80, burstiness=0.9,
        sentence_len_variance=120.0, type_token_ratio=0.55,
        repetition_score=0.05, mean_perplexity=None,
        voice_guard_score=85, disclosure_ok=True,
        pangram_score=None, aprovado_gate=True,
        pipeline_version="5.2",
    ))
    rpt = t.report_text()
    assert "Detection Report" in rpt
    assert "mediana" in rpt.lower()


def test_detection_tracker_record_from_gate() -> None:
    """Atalho record_from_gate extrai campos de um GateResult."""
    from src.validators.quality_gate import GateResult
    tmp = Path(tempfile.mkdtemp()) / "history.jsonl"
    t = DetectionTracker(path=tmp)
    gr = GateResult(
        aprovado=True,
        stylometry_score=72,
        stylometry_burstiness=0.78,
        voice_guard_score=85,
        disclosure_ok=True,
    )
    t.record_from_gate(gr, course_id="cx", module_name="mx", client_id="default")
    entries = t.load_entries()
    assert len(entries) == 1
    assert entries[0]["stylometry_score"] == 72
    assert entries[0]["burstiness"] == pytest.approx(0.78)


# ─── quality_gate camadas 5 + 6 integradas ────────────────────────


def test_quality_gate_inclui_stylometry_score() -> None:
    client = load_client("default")
    gate = QualityGate(client=client, auto_fix=True)
    r = gate.check_text(_sample_text_humano_like(), curso_id="t1", module_name="m1")
    # camada 5 deve preencher os campos
    assert r.stylometry_score >= 0
    assert r.stylometry_burstiness >= 0


def test_quality_gate_inclui_disclosure_ok() -> None:
    client = load_client("default")
    gate = QualityGate(client=client, auto_fix=True)
    r = gate.check_text(_sample_text_humano_like(), curso_id="t1", module_name="m1")
    # campo existe e foi calculado
    assert isinstance(r.disclosure_ok, bool)


def test_quality_gate_stylometry_eh_report_only_por_default() -> None:
    """Score baixo de stylometry NAO deve bloquear (apenas avisar) sem opt-in explicito."""
    client = load_client("default")
    gate = QualityGate(client=client, auto_fix=True)
    # Texto repetitivo (boilerplate) — stylometry vai pontuar baixo
    txt = "O sistema. " * 30
    r = gate.check_text(txt, curso_id="t1", module_name="m1")
    # Independente do stylometry score, aprovacao do GATE depende de outras camadas
    # (content_check vai reprovar pelo word count baixo) — mas o motivo NAO pode
    # ser stylometry.
    motivos_stylometry = [e for e in r.erros if e.startswith("Stylometry:")]
    assert motivos_stylometry == []


# ─── humanizer (PR-4) ──────────────────────────────────────────────


def test_humanizer_diagnostic_builder_com_problemas() -> None:
    """_build_diagnostic deve listar problemas especificos."""
    from src.agents.humanizer import Humanizer
    from src.validators.stylometry_checker import StylometryReport
    h = Humanizer(client=None)  # type: ignore[arg-type]
    bad_report = StylometryReport(
        burstiness=0.30,
        sentence_len_variance=10.0,
        type_token_ratio=0.30,
        repetition_score=0.15,
        sentences_short=0,
        sentences_total=10,
        score=40,
    )
    diag = h._build_diagnostic(bad_report)
    assert "burstiness" in diag.lower()
    assert "type_token" in diag.lower()
    assert "repetition" in diag.lower()
    assert "ZERO frases curtas" in diag or "zero" in diag.lower()


def test_humanizer_diagnostic_builder_quando_ja_bom() -> None:
    """Sem problemas, diagnostico indica que score ja e satisfatorio."""
    from src.agents.humanizer import Humanizer
    from src.validators.stylometry_checker import StylometryReport
    h = Humanizer(client=None)  # type: ignore[arg-type]
    good_report = StylometryReport(
        burstiness=0.90,
        sentence_len_variance=60.0,
        type_token_ratio=0.55,
        repetition_score=0.04,
        sentences_short=3,
        sentences_total=10,
        score=85,
    )
    diag = h._build_diagnostic(good_report)
    assert "satisfat" in diag.lower() or "marginal" in diag.lower()


def test_humanizer_score_inicial_alto_nao_dispara_reescrita() -> None:
    """Se texto ja atende target, retorna sem chamar LLM."""
    from src.agents.humanizer import Humanizer
    h = Humanizer(client=None)  # type: ignore[arg-type]
    text = _sample_text_humano_like()
    # target absurdamente baixo para garantir convergencia inicial
    result = h.run_iterative(text, target_score=10, max_iters=2)
    assert result.iters_realizadas == 0
    assert result.convergiu is True
    assert "ja atende" in result.motivo_parada.lower() or "atende" in result.motivo_parada.lower()


def test_humanize_if_enabled_default_off() -> None:
    """Cliente default tem humanize_enabled=false — retorna texto original sem result."""
    from src.agents.humanizer import humanize_if_enabled
    client = load_client("default")
    text = "Texto qualquer."
    out, result = humanize_if_enabled(text, client=client, llm_client=None)  # type: ignore[arg-type]
    assert out == text
    assert result is None


def test_pipeline_config_default() -> None:
    client = load_client("default")
    assert client.pipeline.humanize_enabled is False
    assert client.pipeline.humanize_target_stylometry_score == 75
    assert client.pipeline.humanize_max_iters == 2
