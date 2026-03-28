"""Configuracao central do curso-factory.

Carrega variaveis de ambiente e definicoes de cursos a partir de
.env e config/courses.yaml. Define constantes de limites FinOps.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

import yaml
from dotenv import load_dotenv

# Raiz do projeto (dois niveis acima de src/)
ROOT_DIR = Path(__file__).resolve().parent.parent
CONFIG_DIR = ROOT_DIR / "config"
OUTPUT_DIR = ROOT_DIR / "output"
CACHE_DIR = ROOT_DIR / ".cache"

# Carrega .env da raiz do projeto
load_dotenv(ROOT_DIR / ".env")

# --- Chaves de API ---
OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
ANTHROPIC_API_KEY: str = os.getenv("ANTHROPIC_API_KEY", "")
GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY", "")
GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
PERPLEXITY_API_KEY: str = os.getenv("PERPLEXITY_API_KEY", "")

# --- Limites FinOps (em USD) ---
DAILY_BUDGET_PER_PROVIDER: float = float(os.getenv("DAILY_BUDGET_PER_PROVIDER", "2.00"))
SESSION_BUDGET_TOTAL: float = float(os.getenv("SESSION_BUDGET_TOTAL", "5.00"))
MAX_TOKENS_PER_CALL: int = int(os.getenv("MAX_TOKENS_PER_CALL", "4096"))

# --- Budget per course (AAA quality) ---
CLAUDE_BUDGET_PER_COURSE: float = float(os.getenv("CLAUDE_BUDGET_PER_COURSE", "5.00"))
TOTAL_BUDGET_PER_COURSE: float = float(os.getenv("TOTAL_BUDGET_PER_COURSE", "10.00"))

# --- Landing page integration ---
LANDING_PAGE_DIR: Path = Path(os.getenv(
    "LANDING_PAGE_DIR",
    str(ROOT_DIR.parent / "landing-page-geo")
))
EDUCACAO_DIR: Path = LANDING_PAGE_DIR / "src" / "app" / "educacao"

# --- Cache ---
CACHE_TTL_SECONDS: int = int(os.getenv("CACHE_TTL_SECONDS", "3600"))

# --- Modelo Claude (AAA = Opus) ---
CLAUDE_MODEL: str = os.getenv("CLAUDE_MODEL", "claude-opus-4-6")


def load_courses() -> list[dict[str, Any]]:
    """Carrega a lista de cursos definidos em config/courses.yaml."""
    courses_path = CONFIG_DIR / "courses.yaml"
    if not courses_path.exists():
        return []
    with open(courses_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    if data is None:
        return []
    return data.get("courses", data) if isinstance(data, dict) else data


def get_api_key(provider: str) -> str:
    """Retorna a chave de API para o provider indicado."""
    keys = {
        "openai": OPENAI_API_KEY,
        "anthropic": ANTHROPIC_API_KEY,
        "google": GOOGLE_API_KEY,
        "groq": GROQ_API_KEY,
        "perplexity": PERPLEXITY_API_KEY,
    }
    key = keys.get(provider.lower(), "")
    if not key:
        raise ValueError(f"Chave de API nao configurada para o provider: {provider}")
    return key
