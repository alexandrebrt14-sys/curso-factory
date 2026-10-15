"""Confere a pasta de um curso no portal /educacao (regras P1 a P5).

Uso:
    python scripts/conferir_pagina_portal.py D:/caminho/landing-page-geo/src/app/educacao/<slug>

Sai 0 quando a pasta segue o contrato das Etapas 3 e 4 (página de servidor,
steps.ts fino, conteúdo sob demanda, JSON fora do grafo de tipos) e 1 quando não.
Detalhe das regras em docs/portal-educacao-estado-20261014.md, seção 8.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.validators.pagina_portal_checker import conferir_pasta, formatar  # noqa: E402


def main(argv: list[str] | None = None) -> int:
    args = sys.argv[1:] if argv is None else argv
    if len(args) != 1:
        print(__doc__)
        return 2
    pasta = Path(args[0])
    if not pasta.is_dir():
        print(f"pasta não encontrada: {pasta}")
        return 2
    res = conferir_pasta(pasta)
    print(formatar(res, pasta.name))
    return 0 if res.aprovado else 1


if __name__ == "__main__":
    raise SystemExit(main())
