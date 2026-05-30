"""detection_tracker.py — persiste historico de scores de stylometry/disclosure.

Analogo ao cost_tracker.py. Cada vez que o quality_gate roda em um modulo,
escreve uma linha JSONL em output/.detection/history.jsonl com:
- timestamp
- curso_id + module_name
- stylometry_score, burstiness, sentence_len_variance, ttr, repetition_score
- voice_guard_score
- disclosure_ok
- pangram_score (None ate PR-3 ligar Pangram API)
- aprovado final do gate
- pipeline_version (string semver do curso-factory)
- client_id

Comando CLI `python cli.py detection-report --since YYYY-MM-DD` agrega:
- por cliente
- por curso
- tendencia de score ao longo do tempo
- drift: detecta quando algum LLM da banca muda cadencia (ex: Claude 4.6 -> 4.7
  mudou comprimento de sentenca median).

Util para:
- Auditar regressao de qualidade quando o pipeline atualiza modelo
- Provar para Google EEAT que ha mensuracao continua
- Calibrar thresholds via Bloco 5 do dossie cientifico (corpus_calibration)
"""

from __future__ import annotations

import json
import logging
import statistics
from collections import defaultdict
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional

logger = logging.getLogger(__name__)

_DEFAULT_HISTORY_PATH = Path("output/.detection/history.jsonl")


@dataclass
class DetectionEntry:
    """Linha JSONL no historico de deteccao."""
    ts: str
    course_id: str
    module_name: str
    client_id: str
    stylometry_score: int
    burstiness: float
    sentence_len_variance: float
    type_token_ratio: float
    repetition_score: float
    mean_perplexity: Optional[float]
    voice_guard_score: int
    disclosure_ok: bool
    pangram_score: Optional[float]  # ai_likelihood 0-1; None se nao rodou
    aprovado_gate: bool
    pipeline_version: str
    extra: dict[str, Any] = field(default_factory=dict)


class DetectionTracker:
    """Persiste e consulta historico de stylometry/disclosure."""

    def __init__(self, path: Optional[Path] = None) -> None:
        self.path = path or _DEFAULT_HISTORY_PATH
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def record(self, entry: DetectionEntry) -> None:
        """Append-only no JSONL."""
        with self.path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(asdict(entry), ensure_ascii=False) + "\n")

    def record_from_gate(
        self,
        gate_result,
        course_id: str,
        module_name: str,
        client_id: str,
        pipeline_version: str = "unknown",
        pangram_score: Optional[float] = None,
    ) -> None:
        """Atalho: extrai campos de um GateResult e persiste."""
        # Re-import tardio para evitar ciclo (gate importa tracker via cli)
        entry = DetectionEntry(
            ts=datetime.now(timezone.utc).isoformat(),
            course_id=course_id,
            module_name=module_name,
            client_id=client_id,
            stylometry_score=getattr(gate_result, "stylometry_score", 0),
            burstiness=float(getattr(gate_result, "stylometry_burstiness", 0.0)),
            sentence_len_variance=0.0,  # nao exposto direto pelo GateResult; OK ficar 0
            type_token_ratio=0.0,
            repetition_score=0.0,
            mean_perplexity=None,
            voice_guard_score=getattr(gate_result, "voice_guard_score", 0),
            disclosure_ok=bool(getattr(gate_result, "disclosure_ok", True)),
            pangram_score=pangram_score,
            aprovado_gate=bool(gate_result.aprovado),
            pipeline_version=pipeline_version,
        )
        self.record(entry)

    def load_entries(
        self, since: Optional[datetime] = None, client_id: Optional[str] = None
    ) -> list[dict]:
        """Carrega todas as entradas (filtro opcional por data e cliente)."""
        if not self.path.exists():
            return []
        out: list[dict] = []
        with self.path.open("r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    d = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if since:
                    ts_str = d.get("ts", "")
                    try:
                        ts = datetime.fromisoformat(ts_str)
                    except ValueError:
                        continue
                    if ts < since:
                        continue
                if client_id and d.get("client_id") != client_id:
                    continue
                out.append(d)
        return out

    def report_text(
        self, since: Optional[datetime] = None, client_id: Optional[str] = None
    ) -> str:
        """Agregado por curso/cliente com medianas e tendencias."""
        entries = self.load_entries(since=since, client_id=client_id)
        if not entries:
            return "Nenhum registro de deteccao encontrado."

        lines = [
            "=" * 70,
            f"  Detection Report — {len(entries)} registros",
            "=" * 70,
            "",
        ]
        if since:
            lines.append(f"Desde: {since.isoformat()}")
        if client_id:
            lines.append(f"Cliente: {client_id}")
        lines.append("")

        # Agregado global
        sty_scores = [e.get("stylometry_score", 0) for e in entries]
        bursts = [float(e.get("burstiness", 0.0)) for e in entries]
        vg_scores = [e.get("voice_guard_score", 0) for e in entries]
        approved = sum(1 for e in entries if e.get("aprovado_gate"))

        def med(xs):
            return statistics.median(xs) if xs else 0.0

        lines.append("Global:")
        lines.append(
            f"  stylometry_score   mediana={med(sty_scores):.1f}  "
            f"min={min(sty_scores) if sty_scores else 0}  "
            f"max={max(sty_scores) if sty_scores else 0}"
        )
        lines.append(
            f"  burstiness         mediana={med(bursts):.3f}  "
            f"min={min(bursts) if bursts else 0:.3f}  "
            f"max={max(bursts) if bursts else 0:.3f}"
        )
        lines.append(
            f"  voice_guard_score  mediana={med(vg_scores):.1f}"
        )
        lines.append(
            f"  aprovados_gate:    {approved}/{len(entries)} "
            f"({100 * approved / len(entries):.1f}%)"
        )

        # Por cliente
        by_client: dict[str, list[dict]] = defaultdict(list)
        for e in entries:
            by_client[e.get("client_id", "?")].append(e)
        if len(by_client) > 1:
            lines.append("")
            lines.append("Por cliente:")
            for cid in sorted(by_client.keys()):
                sub = by_client[cid]
                sub_sty = [e.get("stylometry_score", 0) for e in sub]
                sub_appr = sum(1 for e in sub if e.get("aprovado_gate"))
                lines.append(
                    f"  {cid:<25} n={len(sub):<4} "
                    f"sty_median={med(sub_sty):>5.1f}  "
                    f"aprov={sub_appr}/{len(sub)}"
                )

        # Por curso (top 10 por volume)
        by_course: dict[str, list[dict]] = defaultdict(list)
        for e in entries:
            by_course[e.get("course_id", "?")].append(e)
        top = sorted(by_course.items(), key=lambda kv: -len(kv[1]))[:10]
        if top:
            lines.append("")
            lines.append("Top 10 cursos por volume:")
            for cid, sub in top:
                sub_sty = [e.get("stylometry_score", 0) for e in sub]
                sub_appr = sum(1 for e in sub if e.get("aprovado_gate"))
                lines.append(
                    f"  {cid:<40} n={len(sub):<4} "
                    f"sty_median={med(sub_sty):>5.1f}  "
                    f"aprov={sub_appr}/{len(sub)}"
                )

        return "\n".join(lines)
