"""Certificado verificável — geração, assinatura e renderização HTML.

Wave 9 — Certificação. Cada certificado emitido é determinístico:
- ``id`` derivado do slug do curso e SHA-1 do email do aluno.
- ``hash`` SHA-256 sobre tupla canônica ``id|email|score|issued_at``.
- ``signature`` HMAC-SHA256 do hash, com ``secret`` privado do emissor.

A verificação recalcula o HMAC e compara em tempo constante. O
``blockchain_tx`` é opcional (placeholder para integração futura com
camada on-chain — ainda não implementada nesta V0).
"""

from __future__ import annotations

import hashlib
import hmac
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from jinja2 import Environment, FileSystemLoader, select_autoescape
from pydantic import BaseModel, Field

from src.certification.qrcode_helper import qr_to_base64_png
from src.models import CourseDefinition


# Diretório padrão dos templates (compartilhado com o gerador TSX).
_DEFAULT_TEMPLATE_DIR = Path(__file__).resolve().parent.parent / "templates"
_DEFAULT_TEMPLATE_NAME = "certificate.html.j2"


def _now_utc() -> datetime:
    """UTC wall-clock determinístico."""
    return datetime.now(timezone.utc)


class Certificate(BaseModel):
    """Certificado emitido para um aluno em um curso."""

    id: str = Field(..., description="ID único derivado de slug + email")
    course_slug: str = Field(..., description="Slug do curso certificado")
    student_email: str = Field(..., description="Email do aluno (chave de identidade)")
    student_name: str = Field(..., min_length=1, description="Nome completo do aluno")
    issued_at: datetime = Field(default_factory=_now_utc, description="Timestamp de emissão UTC")
    score: float = Field(..., ge=0.0, le=1.0, description="Score normalizado [0.0, 1.0]")
    hash: str = Field(..., description="SHA-256 determinístico")
    signature: str = Field(..., description="HMAC-SHA256 do hash (hex)")
    blockchain_tx: Optional[str] = Field(
        default=None,
        description="Transação on-chain (placeholder V0 — não implementado)",
    )


def _student_id_suffix(email: str) -> str:
    """Calcula sufixo determinístico de 12 hex chars a partir do email.

    Normaliza para lowercase + strip antes do SHA-1 para garantir
    estabilidade entre re-emissões com casing diferente.
    """
    normalized = email.strip().lower().encode("utf-8")
    return hashlib.sha1(normalized).hexdigest()[:12]


def _compute_hash(cert_id: str, email: str, score: float, issued_at: datetime) -> str:
    """Hash SHA-256 sobre tupla canônica.

    Score formatado com 6 casas decimais para evitar drift de
    representação float entre re-execuções.
    """
    canonical = f"{cert_id}|{email.strip().lower()}|{score:.6f}|{issued_at.isoformat()}"
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def _compute_signature(payload_hash: str, secret: str) -> str:
    """HMAC-SHA256 do hash, com segredo do emissor."""
    return hmac.new(
        secret.encode("utf-8"),
        payload_hash.encode("utf-8"),
        hashlib.sha256,
    ).hexdigest()


def generate_certificate(
    student_email: str,
    student_name: str,
    course: CourseDefinition,
    score: float,
    secret: str,
    *,
    pass_threshold: float = 0.7,
    issued_at: Optional[datetime] = None,
) -> Certificate:
    """Gera certificado verificável para um aluno aprovado.

    Args:
        student_email: Email do aluno (será normalizado para lowercase).
        student_name: Nome completo (preserva acentuação PT-BR).
        course: Definição completa do curso (slug, autor, dominio).
        score: Pontuação final normalizada em ``[0.0, 1.0]``.
        secret: Segredo HMAC privado do emissor (NUNCA compartilhar).
        pass_threshold: Limiar mínimo de aprovação (default 0.7).
        issued_at: Override de timestamp para testes determinísticos.

    Returns:
        ``Certificate`` populado com hash e signature.

    Raises:
        ValueError: Se score fora do intervalo, abaixo do threshold,
            email vazio, ou secret vazio.
    """
    if not student_email or not student_email.strip():
        raise ValueError("student_email não pode ser vazio")
    if not student_name or not student_name.strip():
        raise ValueError("student_name não pode ser vazio")
    if not secret or not secret.strip():
        raise ValueError("secret não pode ser vazio (necessário para HMAC)")
    if not 0.0 <= score <= 1.0:
        raise ValueError(f"score deve estar em [0.0, 1.0], recebido {score!r}")
    if score < pass_threshold:
        raise ValueError(
            f"Aluno reprovado: score {score:.2f} < pass_threshold {pass_threshold:.2f}"
        )

    cert_id = f"{course.slug}-{_student_id_suffix(student_email)}"
    timestamp = issued_at or _now_utc()
    payload_hash = _compute_hash(cert_id, student_email, score, timestamp)
    signature = _compute_signature(payload_hash, secret)

    return Certificate(
        id=cert_id,
        course_slug=course.slug,
        student_email=student_email.strip().lower(),
        student_name=student_name.strip(),
        issued_at=timestamp,
        score=score,
        hash=payload_hash,
        signature=signature,
    )


def verify_certificate(certificate: Certificate, secret: str) -> bool:
    """Verifica se a assinatura HMAC do certificado é válida.

    Recalcula hash e signature a partir dos campos do certificado e
    compara em tempo constante (``hmac.compare_digest``). Retorna
    ``False`` se hash foi adulterado, signature inválida, ou secret
    incorreto.
    """
    if not secret:
        return False

    expected_hash = _compute_hash(
        certificate.id,
        certificate.student_email,
        certificate.score,
        certificate.issued_at,
    )
    if not hmac.compare_digest(expected_hash, certificate.hash):
        return False

    expected_signature = _compute_signature(certificate.hash, secret)
    return hmac.compare_digest(expected_signature, certificate.signature)


def _build_verification_url(certificate: Certificate, course: CourseDefinition) -> str:
    """Monta URL pública canônica para verificação do certificado."""
    base = course.dominio.rstrip("/") if course.dominio else ""
    return f"{base}/certificado/{certificate.hash}"


def render_html(
    certificate: Certificate,
    course: CourseDefinition,
    template_path: Optional[Path] = None,
) -> str:
    """Renderiza certificado HTML autossuficiente (sem CSS externo).

    Args:
        certificate: Certificado emitido por ``generate_certificate``.
        course: Mesma definição usada na emissão (autor, company).
        template_path: Override do template Jinja2. Se ``None``, usa
            ``src/templates/certificate.html.j2``.

    Returns:
        HTML completo pronto para salvar em ``output/certificates/``.
    """
    if template_path is None:
        template_dir = _DEFAULT_TEMPLATE_DIR
        template_name = _DEFAULT_TEMPLATE_NAME
    else:
        template_dir = template_path.parent
        template_name = template_path.name

    env = Environment(
        loader=FileSystemLoader(str(template_dir)),
        autoescape=select_autoescape(["html", "xml", "j2"]),
    )
    template = env.get_template(template_name)

    verification_url = _build_verification_url(certificate, course)

    # QR code é opcional — se a lib não estiver disponível ou falhar,
    # o template recebe string vazia e não quebra.
    qr_base64 = ""
    try:
        qr_base64 = qr_to_base64_png(verification_url)
    except (RuntimeError, ValueError):
        qr_base64 = ""

    return template.render(
        certificate=certificate,
        course=course,
        verification_url=verification_url,
        qr_base64=qr_base64,
        score_pct=f"{certificate.score * 100:.1f}",
        issued_at_display=certificate.issued_at.strftime("%d/%m/%Y"),
    )
