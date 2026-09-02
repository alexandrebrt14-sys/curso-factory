"""Configuração central do curso-factory.

Carrega variáveis de ambiente e definições de cursos a partir de
.env e config/courses.yaml. Define constantes de limites FinOps.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

import yaml
from dotenv import load_dotenv

# Raiz do projeto (dois níveis acima de src/)
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
MAX_TOKENS_PER_CALL: int = int(os.getenv("MAX_TOKENS_PER_CALL", "16384"))

# --- Tamanho dos insumos por etapa (caracteres) ---
# A geração é por AULA desde 02/09/2026: cada chamada do writer recebe a
# pesquisa inteira até este teto (antes eram 3.000 caracteres, que deixavam o
# redator sem dado e produziam aula rasa). 40 mil caracteres cabem com folga
# no contexto do GPT-4o (128 mil tokens).
DRAFT_RESEARCH_CONTEXT_CHARS: int = int(os.getenv("DRAFT_RESEARCH_CONTEXT_CHARS", "40000"))
# A classificação (Groq, 128 mil tokens de contexto) não precisa do curso inteiro.
CLASSIFY_CONTEXT_CHARS: int = int(os.getenv("CLASSIFY_CONTEXT_CHARS", "60000"))
# Trecho do relatório da análise (Gemini) que acompanha cada aula na revisão.
REVIEW_ANALYSIS_CHARS: int = int(os.getenv("REVIEW_ANALYSIS_CHARS", "3000"))
# Revisão que devolve menos que esta fração das palavras recebidas é
# comentário, não revisão: o rascunho original é mantido.
REVIEW_MIN_RATIO: float = float(os.getenv("REVIEW_MIN_RATIO", "0.6"))

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
CLAUDE_MODEL: str = os.getenv("CLAUDE_MODEL", "claude-sonnet-5")


def load_courses() -> list[dict[str, Any]]:
    """Carrega a lista de cursos definidos em config/courses.yaml."""
    courses_path = CONFIG_DIR / "courses.yaml"
    if not courses_path.exists():
        return []
    with open(courses_path, encoding="utf-8") as f:
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
        raise ValueError(f"Chave de API não configurada para o provider: {provider}")
    return key
