"""CLI standalone para emitir certificados — Wave 9 V0.

Demonstra o fluxo completo: instancia ``CourseDefinition`` mínimo,
chama ``generate_certificate``, renderiza HTML e grava em
``output/certificates/<hash>.html``.

Uso::

    python examples/certify_cli.py \\
        --slug geo-fundamentos \\
        --email aluno@x.com \\
        --name "João Silva" \\
        --score 0.85 \\
        --secret "test-secret"

Saída: imprime o caminho do HTML gerado e o hash do certificado.

NÃO modifica ``cli.py``. Este é um script auxiliar isolado para
validação manual do módulo ``src.certification``.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

# Permite execução direta sem `pip install -e .`.
_REPO_ROOT = Path(__file__).resolve().parent.parent
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from src.certification.certificate import (  # noqa: E402
    generate_certificate,
    render_html,
    verify_certificate,
)
from src.models import CourseDefinition  # noqa: E402


def _load_course(slug: str, course_json: Path | None) -> CourseDefinition:
    """Carrega CourseDefinition de JSON ou monta um stub mínimo."""
    if course_json and course_json.exists():
        data = json.loads(course_json.read_text(encoding="utf-8"))
        # Garante que o slug do CLI sobrescreve o do JSON se diferentes.
        data["slug"] = slug
        return CourseDefinition(**data)

    # Stub mínimo válido (descrição precisa de >=20 chars).
    return CourseDefinition(
        slug=slug,
        titulo=f"Curso {slug.replace('-', ' ').title()}",
        descricao=f"Curso completo de {slug} com avaliação final e certificado verificável.",
        autor_nome="Alexandre Caramaschi",
        autor_credencial="CEO da Brasil GEO, ex-CMO da Semantix (Nasdaq), cofundador da AI Brasil",
        dominio="https://alexandrecaramaschi.com",
        company_name="Brasil GEO",
        company_description="Plataforma de educação executiva sobre Generative Engine Optimization.",
    )


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Emite certificado verificável e renderiza HTML.",
    )
    parser.add_argument("--slug", required=True, help="Slug do curso (ASCII kebab-case)")
    parser.add_argument("--email", required=True, help="Email do aluno")
    parser.add_argument("--name", required=True, help="Nome completo do aluno")
    parser.add_argument("--score", type=float, required=True, help="Score [0.0, 1.0]")
    parser.add_argument("--secret", required=True, help="Segredo HMAC do emissor")
    parser.add_argument(
        "--course-json",
        type=Path,
        default=None,
        help="Opcional: caminho de JSON com CourseDefinition completo",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=_REPO_ROOT / "output" / "certificates",
        help="Diretório de saída do HTML",
    )
    parser.add_argument(
        "--pass-threshold",
        type=float,
        default=0.7,
        help="Threshold mínimo de aprovação (default 0.7)",
    )

    args = parser.parse_args()

    course = _load_course(args.slug, args.course_json)

    try:
        certificate = generate_certificate(
            student_email=args.email,
            student_name=args.name,
            course=course,
            score=args.score,
            secret=args.secret,
            pass_threshold=args.pass_threshold,
        )
    except ValueError as exc:
        print(f"[ERRO] {exc}", file=sys.stderr)
        return 2

    if not verify_certificate(certificate, args.secret):
        print("[ERRO] Falha de auto-verificação imediata após emissão", file=sys.stderr)
        return 3

    html = render_html(certificate, course)

    args.output_dir.mkdir(parents=True, exist_ok=True)
    out_path = args.output_dir / f"{certificate.hash}.html"
    out_path.write_text(html, encoding="utf-8")

    print(f"Certificado gerado: {out_path}")
    print(f"ID:        {certificate.id}")
    print(f"Hash:      {certificate.hash}")
    print(f"Signature: {certificate.signature}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
