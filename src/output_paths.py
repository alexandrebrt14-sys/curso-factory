"""Proteção dos intermediários quando o portal configurado é reconhecido."""

from __future__ import annotations

import json
from pathlib import Path


def validate_intermediate_output(target: Path, *, landing_root: Path | None = None) -> None:
    """Recusa intermediários nas pastas públicas/geradas do portal conhecido.

    Não infere a identidade pelo nome da pasta nem restringe exports TSX.
    Sem os três marcadores do portal, não impõe uma regra a outro projeto.
    """
    if landing_root is None:
        from src.config import LANDING_PAGE_DIR

        landing_root = LANDING_PAGE_DIR
    root = landing_root.expanduser().resolve()
    try:
        package = json.loads((root / "package.json").read_text(encoding="utf-8-sig"))
    except (OSError, ValueError):
        return
    if (
        not isinstance(package, dict)
        or package.get("name") != "alexandrecaramaschi-com"
        or not (root / "next.config.ts").is_file()
        or not (root / "src" / "app" / "educacao").is_dir()
    ):
        return

    destination = target.expanduser().resolve()
    for reserved in (root / "public", root / "src" / "generated"):
        if destination.is_relative_to(reserved.resolve()):
            raise ValueError(
                f"Destino intermediário reservado ao portal: {destination}. "
                "Use output/ do curso-factory; entregue apenas conteúdo revisado "
                "pelo contrato docs/PUBLICACAO_CONTEUDO_MIDIA.md."
            )
