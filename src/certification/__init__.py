"""Módulo de certificação verificável e Skill Graph.

Wave 9 — Certificação + Skill Graph + Career Integration.

Inspirado em Coursera Professional Certificates, FIAP Trampoo e
LinkedIn Learning. Fornece:

- Geração de certificado determinístico com hash SHA-256 e
  assinatura HMAC-SHA256 verificável.
- Renderização HTML autossuficiente com QR code embutido.
- Skill Graph mínimo (V0) baseado em ``schema.org/Skill``.

Importação canônica::

    from src.certification.certificate import (
        Certificate,
        generate_certificate,
        verify_certificate,
        render_html,
    )
    from src.certification.skill_graph import (
        Skill,
        validate_skills,
        find_courses_by_skill,
    )
"""

from __future__ import annotations

from src.certification.certificate import (
    Certificate,
    generate_certificate,
    render_html,
    verify_certificate,
)
from src.certification.skill_graph import (
    Skill,
    find_courses_by_skill,
    validate_skills,
)

__all__ = [
    "Certificate",
    "generate_certificate",
    "verify_certificate",
    "render_html",
    "Skill",
    "validate_skills",
    "find_courses_by_skill",
]
