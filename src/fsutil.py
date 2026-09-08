"""Utilidades de arquivo compartilhadas: JSON atômico e leitura tolerante.

Três módulos (cost_tracker, cache, orchestrator) gravavam JSON com
``open(path, "w")`` direto. Um Ctrl-C ou queda de energia no meio da escrita
deixava um arquivo truncado, e cada módulo reagia de um jeito: o ledger de
custos zerava o histórico inteiro na chamada seguinte; o checkpoint do curso
derrubava todo ``create`` daquele slug com ``JSONDecodeError``. Aqui fica a
regra única: escrever em arquivo temporário ao lado e trocar com
``os.replace`` (atômico no mesmo sistema de arquivos); ao ler, um arquivo
corrompido é posto de lado com sufixo ``.corrupt-<carimbo>`` em vez de ser
apagado ou sobrescrito.
"""

from __future__ import annotations

import json
import logging
import os
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


def write_json_atomic(path: Path, data: Any, *, indent: int | None = 2) -> None:
    """Grava ``data`` como JSON em ``path`` sem deixar arquivo parcial para trás."""
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(f".{path.name}.{os.getpid()}.tmp")
    try:
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=indent, ensure_ascii=False, default=str)
        os.replace(tmp, path)
    finally:
        tmp.unlink(missing_ok=True)


def quarantine_corrupt(path: Path) -> Path | None:
    """Renomeia um arquivo ilegível para ``<nome>.corrupt-<carimbo>`` e devolve o destino.

    Preserva evidência para diagnóstico em vez de descartar dado. Devolve
    ``None`` quando o rename não foi possível (o arquivo fica no lugar).
    """
    stamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
    dest = path.with_name(f"{path.name}.corrupt-{stamp}")
    try:
        os.replace(path, dest)
    except OSError as exc:
        logger.error("Não consegui isolar %s: %s", path, exc)
        return None
    logger.error("Arquivo JSON corrompido isolado em %s", dest)
    return dest


def read_json_or_none(path: Path, *, quarantine: bool = True) -> Any | None:
    """Lê JSON de ``path``. Arquivo ausente, ilegível ou corrompido devolve ``None``.

    Com ``quarantine=True`` o arquivo corrompido é renomeado (ver
    :func:`quarantine_corrupt`), de modo que a próxima gravação não apague a
    evidência nem herde o lixo.
    """
    if not path.exists():
        return None
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError as exc:
        logger.error("JSON inválido em %s: %s", path, exc)
        if quarantine:
            quarantine_corrupt(path)
        return None
    except OSError as exc:
        logger.error("Falha ao ler %s: %s", path, exc)
        return None
