"""Carregador de config/providers.yaml.

Fonte de verdade para pricing, endpoints, modelos padrão e fallback dos LLMs.
Carregado uma vez no import; consumido por llm_client.py.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

_ROOT = Path(__file__).resolve().parents[1]
_PROVIDERS_YAML = _ROOT / "config" / "providers.yaml"


@dataclass(frozen=True)
class ProviderConfig:
    """Configuração imutável de um provider LLM."""
    name: str
    endpoint: str
    default_model: str
    price_input: float  # USD por 1K tokens
    price_output: float
    fallback: str | None
    protocol: str  # "openai_compat" | "anthropic" | "google"
    #: Cadeia completa de fallback, na ordem (wave 6). Quando o YAML só traz
    #: `fallback`, a cadeia é esse único salto.
    fallback_chain: tuple[str, ...] = ()


def _load() -> dict[str, ProviderConfig]:
    if not _PROVIDERS_YAML.exists():
        raise FileNotFoundError(
            f"config/providers.yaml não encontrado em {_PROVIDERS_YAML}"
        )
    with _PROVIDERS_YAML.open("r", encoding="utf-8") as f:
        raw: dict[str, Any] = yaml.safe_load(f) or {}
    providers_raw = raw.get("providers", {})
    out: dict[str, ProviderConfig] = {}
    for name, cfg in providers_raw.items():
        pricing = cfg.get("pricing", {})
        cadeia = cfg.get("fallback_chain") or ([cfg["fallback"]] if cfg.get("fallback") else [])
        out[name] = ProviderConfig(
            name=name,
            endpoint=cfg["endpoint"],
            default_model=cfg.get("default_model", ""),
            price_input=float(pricing.get("input", 0.0)),
            price_output=float(pricing.get("output", 0.0)),
            fallback=(cadeia[0] if cadeia else None),
            protocol=cfg.get("protocol", "openai_compat"),
            fallback_chain=tuple(p for p in cadeia if p and p != name),
        )
    return out


PROVIDERS: dict[str, ProviderConfig] = _load()


def get_provider(name: str) -> ProviderConfig:
    """Retorna config do provider ou levanta KeyError com mensagem clara."""
    if name not in PROVIDERS:
        raise KeyError(
            f"Provider '{name}' não configurado em config/providers.yaml. "
            f"Disponíveis: {sorted(PROVIDERS.keys())}"
        )
    return PROVIDERS[name]


# Compatibilidade com imports legados de llm_client.py
PRICING: dict[str, tuple[float, float]] = {
    name: (cfg.price_input, cfg.price_output) for name, cfg in PROVIDERS.items()
}

DEFAULT_MODELS: dict[str, str] = {
    name: cfg.default_model for name, cfg in PROVIDERS.items()
}

ENDPOINTS: dict[str, str] = {
    name: cfg.endpoint for name, cfg in PROVIDERS.items()
}

FALLBACK_MAP: dict[str, str] = {
    name: cfg.fallback for name, cfg in PROVIDERS.items() if cfg.fallback
}

#: Cadeia completa por provedor, na ordem em que o cliente tenta (wave 6).
FALLBACK_CHAINS: dict[str, tuple[str, ...]] = {
    name: cfg.fallback_chain for name, cfg in PROVIDERS.items()
}
