"""Cache de resultados LLM para evitar reprocessamento.

Usa hash SHA256 do prompt como chave e armazena em .cache/
como arquivos JSON individuais. TTL configurável.
"""

from __future__ import annotations

import hashlib
import json
import logging
import time
from pathlib import Path
from typing import Optional

from src.config import CACHE_DIR, CACHE_TTL_SECONDS

logger = logging.getLogger(__name__)


class Cache:
    """Cache em disco baseado em hash SHA256 do prompt."""

    def __init__(self, ttl: Optional[int] = None) -> None:
        self.ttl = ttl if ttl is not None else CACHE_TTL_SECONDS
        self._dir = CACHE_DIR
        self._dir.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def _make_key(prompt: str, provider: str, model: str) -> str:
        """Gera chave SHA256 a partir do prompt, provider e modelo."""
        raw = f"{provider}:{model}:{prompt}"
        return hashlib.sha256(raw.encode("utf-8")).hexdigest()

    def _path(self, key: str) -> Path:
        return self._dir / f"{key}.json"

    def get(self, prompt: str, provider: str, model: str) -> Optional[str]:
        """Recupera resultado do cache se existir e não estiver expirado."""
        key = self._make_key(prompt, provider, model)
        path = self._path(key)
        if not path.exists():
            return None
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except (json.JSONDecodeError, OSError):
            return None

        created = data.get("created", 0)
        if time.time() - created > self.ttl:
            logger.debug("Cache expirado para chave %s", key[:12])
            path.unlink(missing_ok=True)
            return None

        logger.info("Cache hit para %s/%s (chave %s)", provider, model, key[:12])
        return data.get("result")

    def set(self, prompt: str, provider: str, model: str, result: str) -> None:
        """Armazena resultado no cache."""
        key = self._make_key(prompt, provider, model)
        path = self._path(key)
        data = {
            "provider": provider,
            "model": model,
            "created": time.time(),
            "prompt_preview": prompt[:200],
            "result": result,
        }
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        logger.debug("Cache gravado: chave %s", key[:12])

    def clear(self) -> int:
        """Remove todas as entradas do cache. Retorna quantidade removida."""
        count = 0
        for path in self._dir.glob("*.json"):
            path.unlink()
            count += 1
        logger.info("Cache limpo: %d entradas removidas", count)
        return count

    def clear_expired(self) -> int:
        """Remove apenas entradas expiradas. Retorna quantidade removida."""
        count = 0
        now = time.time()
        for path in self._dir.glob("*.json"):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                if now - data.get("created", 0) > self.ttl:
                    path.unlink()
                    count += 1
            except (json.JSONDecodeError, OSError):
                path.unlink(missing_ok=True)
                count += 1
        return count
