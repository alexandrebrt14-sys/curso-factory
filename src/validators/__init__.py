"""Validadores do quality gate: acentuação, conteúdo, links, voz, estilometria,
disclosure, densidade visual, abertura (R1 a R9) e HTML.

Superfície estável para quem consome o pacote de fora. Os módulos internos
continuam importáveis pelo caminho completo.
"""

from src.validators.abertura_checker import check_abertura, check_abertura_definicao
from src.validators.accent_checker import AccentError, check_accents, fix_accents
from src.validators.content_checker import ContentError, check_content
from src.validators.disclosure_checker import DisclosureCheckResult, disclosure_check
from src.validators.html_validator import HTMLError, validate_html
from src.validators.link_checker import LinkError, check_links
from src.validators.quality_gate import GateResult, QualityGate
from src.validators.stylometry_checker import StylometryReport, stylometry_check
from src.validators.visual_density import check_visual_density
from src.validators.voice_guard import VoiceGuardResult, voice_guard_check

__all__ = [
    "AccentError",
    "ContentError",
    "DisclosureCheckResult",
    "GateResult",
    "HTMLError",
    "LinkError",
    "QualityGate",
    "StylometryReport",
    "VoiceGuardResult",
    "check_abertura",
    "check_abertura_definicao",
    "check_accents",
    "check_content",
    "check_links",
    "check_visual_density",
    "disclosure_check",
    "fix_accents",
    "stylometry_check",
    "validate_html",
    "voice_guard_check",
]
