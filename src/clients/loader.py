"""Loader de ClientContext a partir de config/clients/<id>/client.yaml."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

import yaml

from src.clients.context import (
    AgenticConfig,
    Author,
    Branding,
    CertificationConfig,
    ClientContext,
    Company,
    Domain,
    Editorial,
    EngagementConfig,
    TutorConfig,
    VoiceGuardCanonical,
    VoiceGuardConfig,
    VoiceGuardForbidden,
)

_ROOT = Path(__file__).resolve().parents[2]
_CLIENTS_DIR = _ROOT / "config" / "clients"


def _resolve_path(raw: str | None, base: Path) -> Path | None:
    """Resolve path relativo a `base` (raiz do repo)."""
    if not raw:
        return None
    p = Path(raw)
    if p.is_absolute():
        return p
    return (base / p).resolve()


def load_client(client_id: str = "default") -> ClientContext:
    """Carrega ClientContext do YAML em config/clients/<client_id>/client.yaml.

    Falha com FileNotFoundError se o YAML não existir.
    """
    yaml_path = _CLIENTS_DIR / client_id / "client.yaml"
    if not yaml_path.exists():
        raise FileNotFoundError(
            f"Cliente '{client_id}' não encontrado. Esperado em {yaml_path}. "
            f"Clientes disponíveis: {list_clients() or 'nenhum'}."
        )

    with yaml_path.open("r", encoding="utf-8") as f:
        data: dict[str, Any] = yaml.safe_load(f) or {}

    author_d = data.get("author", {})
    author = Author(
        name=author_d.get("name", ""),
        credential=author_d.get("credential", ""),
        title_seo_suffix=author_d.get("title_seo_suffix", ""),
    )

    domain_d = data.get("domain", {})
    domain = Domain(
        canonical_url=domain_d.get("canonical_url", ""),
        educacao_path=domain_d.get("educacao_path", "/educacao"),
    )

    company_d = data.get("company", {})
    company = Company(
        name=company_d.get("name", ""),
        description=company_d.get("description", ""),
    )

    branding_d = data.get("branding", {})
    branding = Branding(
        hero_gradient_from=branding_d.get("hero_gradient_from", "#032d60"),
        hero_gradient_to=branding_d.get("hero_gradient_to", "#0176d3"),
        badge_color=branding_d.get("badge_color", "#0176d3"),
    )

    ed_d = data.get("editorial", {})
    editorial = Editorial(
        style=ed_d.get("style", "business"),
        reference_publications=list(ed_d.get("reference_publications", [])),
        bloom_min_level=int(ed_d.get("bloom_min_level", 3)),
        knowles_min_principles=int(ed_d.get("knowles_min_principles", 4)),
        words_per_module_min=int(ed_d.get("words_per_module_min", 2500)),
        words_per_module_max=int(ed_d.get("words_per_module_max", 4000)),
    )

    vg_d = data.get("voice_guard", {})
    canonical_d = vg_d.get("canonical", {})
    forbidden_d = vg_d.get("forbidden", {})
    voice_guard = VoiceGuardConfig(
        enabled=bool(vg_d.get("enabled", True)),
        min_score=int(vg_d.get("min_score", 70)),
        canonical=VoiceGuardCanonical(
            company=canonical_d.get("company", ""),
            founder=canonical_d.get("founder", ""),
            credential_fragments=list(canonical_d.get("credential_fragments", [])),
            domains=list(canonical_d.get("domains", [])),
        ),
        forbidden=VoiceGuardForbidden(
            titles=list(forbidden_d.get("titles", [])),
            company_names=list(forbidden_d.get("company_names", [])),
            domains=list(forbidden_d.get("domains", [])),
            rhetoric_openers=list(forbidden_d.get("rhetoric_openers", [])),
            ai_disclaimers=list(forbidden_d.get("ai_disclaimers", [])),
        ),
    )

    landing_page_dir = _resolve_path(data.get("landing_page_dir"), _ROOT)
    educacao_dir = _resolve_path(data.get("educacao_dir"), _ROOT)

    output_d = data.get("output", {})
    output_base_dir = _resolve_path(output_d.get("base_dir", "output"), _ROOT) or _ROOT / "output"

    # Waves 6-10 features (todas opcionais, default off; ligar no client.yaml)
    features_d = data.get("features", {})

    eng_d = features_d.get("engagement", {})
    engagement = EngagementConfig(
        gamification_enabled=bool(eng_d.get("gamification_enabled", False)),
        streak_enabled=bool(eng_d.get("streak_enabled", True)),
        badges_enabled=bool(eng_d.get("badges_enabled", True)),
        leagues_enabled=bool(eng_d.get("leagues_enabled", False)),
        srs_enabled=bool(eng_d.get("srs_enabled", True)),
        srs_interval_initial_days=int(eng_d.get("srs_interval_initial_days", 1)),
        quiz_pass_threshold=float(eng_d.get("quiz_pass_threshold", 0.7)),
    )

    tut_d = features_d.get("tutor", {})
    tutor = TutorConfig(
        enabled=bool(tut_d.get("enabled", False)),
        persona=tut_d.get("persona", "curiosa-paciente"),
        name=tut_d.get("name", ""),
        model=tut_d.get("model", "claude-haiku-4-5-20251001"),
        budget_per_user_per_month=float(tut_d.get("budget_per_user_per_month", 2.0)),
        daily_budget=float(tut_d.get("daily_budget", 10.0)),
    )

    cert_d = features_d.get("certification", {})
    certification = CertificationConfig(
        enabled=bool(cert_d.get("enabled", False)),
        pass_threshold=float(cert_d.get("pass_threshold", 0.7)),
        blockchain_opt_in=bool(cert_d.get("blockchain_opt_in", False)),
        linkedin_integration=bool(cert_d.get("linkedin_integration", False)),
    )

    ag_d = features_d.get("agentic", {})
    agentic = AgenticConfig(
        enabled=bool(ag_d.get("enabled", False)),
        emit_llms_txt=bool(ag_d.get("emit_llms_txt", True)),
        mcp_server=bool(ag_d.get("mcp_server", False)),
        a2a_endpoints=bool(ag_d.get("a2a_endpoints", False)),
    )

    # Wave 8 — idioma default do cliente
    client_language = ed_d.get("language", "pt-br")

    return ClientContext(
        id=data.get("id", client_id),
        author=author,
        domain=domain,
        company=company,
        branding=branding,
        editorial=editorial,
        voice_guard=voice_guard,
        landing_page_dir=landing_page_dir,
        educacao_dir=educacao_dir,
        output_base_dir=output_base_dir,
        tutor=tutor,
        engagement=engagement,
        certification=certification,
        agentic=agentic,
        language=client_language,
    )


def list_clients() -> list[str]:
    """Retorna IDs dos clientes configurados (exclui _template e diretórios ocultos)."""
    if not _CLIENTS_DIR.exists():
        return []
    return sorted(
        p.name
        for p in _CLIENTS_DIR.iterdir()
        if p.is_dir()
        and not p.name.startswith("_")
        and not p.name.startswith(".")
        and (p / "client.yaml").exists()
    )


def get_client_from_env(default: str = "default") -> ClientContext:
    """Lê CURSO_FACTORY_CLIENT do env, senão carrega `default`."""
    client_id = os.environ.get("CURSO_FACTORY_CLIENT", default)
    return load_client(client_id)
