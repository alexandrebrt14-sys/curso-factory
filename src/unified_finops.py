"""Adapter curso-factory -> geo-finops calls.db unificado.

Espelha o cost_tracker existente (output/costs.json) para o calls.db central.
"""

from __future__ import annotations

import logging
import sys
from pathlib import Path

logger = logging.getLogger(__name__)

_GEO_FINOPS_PATH = Path("C:/Sandyboxclaude/geo-finops")
if _GEO_FINOPS_PATH.exists() and str(_GEO_FINOPS_PATH) not in sys.path:
    sys.path.insert(0, str(_GEO_FINOPS_PATH))

try:
    from geo_finops import track_call as _track_call
    _AVAILABLE = True
except ImportError:
    _AVAILABLE = False
    _track_call = None


PROJECT_NAME = "curso-factory"


def record(
    provider: str,
    model: str,
    tokens_in: int,
    tokens_out: int,
    custo_usd: float,
    sessao: str | None = None,
    course_id: str | None = None,
    timestamp: str | None = None,
) -> None:
    """Espelha cost_tracker.record() para o calls.db unificado."""
    if not _AVAILABLE:
        return
    try:
        _track_call(
            project=PROJECT_NAME,
            model_id=model,
            tokens_in=tokens_in,
            tokens_out=tokens_out,
            cost_usd=custo_usd,
            run_id=sessao,
            task_type=course_id or "course_generation",
            success=True,
            provider=provider,
            timestamp=timestamp,
        )
    except Exception as exc:
        logger.error("curso-factory unified adapter falhou: %s", exc)
