#!/usr/bin/env python
"""Valida um curso em JSON no formato do portal /educacao antes do PR lá.

Uso:
    python scripts/validar_curso_json.py <curso.json> [outro.json ...] [--json]
    python scripts/validar_curso_json.py output/cursos-json/<slug>.json

Reproduz, fora do portal, o que `src/lib/educacao/conteudo/schema.ts` e os
gates do `landing-page-geo` cobrariam: estrutura estrita, ids únicos em ASCII,
tamanho por capítulo (teto de 900 KB de HTML por página), bloco de código com
linguagem, acentos (até 20), zero emoji e o sidecar de glossário quando existe
ao lado (`<slug>.glossario.json`). Sai com 1 se algum curso reprovar.

Limites em `config/quality_rules.yaml > validation.curso_json`; a conta que os
justifica está em `docs/portal-educacao-estado-20261014.md`.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.validators.curso_json_checker import formatar, validar_arquivo


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("arquivos", nargs="+", help="um ou mais <slug>.json no formato do portal")
    parser.add_argument(
        "--json", action="store_true", help="imprime o resultado em JSON em vez de texto"
    )
    parser.add_argument(
        "--capitulo-aberto-erro",
        type=int,
        default=None,
        help="sobrescreve o teto de caracteres do capítulo aberto (padrão do YAML)",
    )
    parser.add_argument(
        "--min-capitulos", type=int, default=None, help="piso de capítulos do contrato (ex.: 25)"
    )
    parser.add_argument(
        "--midia-cap1", action="store_true", help="exige mediaPlayer (NotebookLM) no capítulo 1"
    )
    parser.add_argument(
        "--glossario", action="store_true", help="exige o sidecar <slug>.glossario.json com termos"
    )
    parser.add_argument(
        "--guia-por-capitulo",
        action="store_true",
        help="avisa capítulo sem guia prático com prompt e saída",
    )
    parser.add_argument(
        "--contrato-completo",
        action="store_true",
        help="atalho: --min-capitulos 25 --midia-cap1 --glossario --guia-por-capitulo",
    )
    args = parser.parse_args(argv)

    limites = {"capitulo_aberto_erro_chars": args.capitulo_aberto_erro}
    contrato = {
        "min_capitulos": args.min_capitulos or (25 if args.contrato_completo else None),
        "midia_capitulo_1": args.midia_cap1 or args.contrato_completo,
        "glossario_obrigatorio": args.glossario or args.contrato_completo,
        "guia_por_capitulo": args.guia_por_capitulo or args.contrato_completo,
    }
    saida: list[dict] = []
    reprovados = 0
    for nome in args.arquivos:
        caminho = Path(nome)
        res = validar_arquivo(caminho, limites=limites, contrato=contrato)
        if not res.aprovado:
            reprovados += 1
        if args.json:
            saida.append(
                {
                    "arquivo": str(caminho),
                    "aprovado": res.aprovado,
                    "erros": [a.__dict__ for a in res.erros],
                    "avisos": [a.__dict__ for a in res.avisos],
                    "medidas": res.medidas,
                }
            )
        else:
            print(formatar(res, nome=caminho.name))
    if args.json:
        print(json.dumps(saida, ensure_ascii=False, indent=2))
    return 1 if reprovados else 0


if __name__ == "__main__":
    sys.exit(main())
