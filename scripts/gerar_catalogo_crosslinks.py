"""Gera o catálogo de destinos de crosslink a partir do catálogo do portal.

O destino real de um crosslink sai do código do portal, nunca da memória de
quem escreve: rota imaginada é defeito. Este script lê o catálogo de cursos
publicados da landing (`src/data/educacao-courses.ts`) e grava um JSON com
caminho, nome, nome curto e tags de cada curso, que o
`src/validators/crosslink_checker.py` usa para conferir cada link interno da
aula e o orquestrador usa para sugerir destinos ao redator.

Uso (leitura apenas no repositório de origem):

    python scripts/gerar_catalogo_crosslinks.py \\
        ../landing-page-geo/src/data/educacao-courses.ts \\
        config/clients/default/crosslinks_catalogo.json

O arquivo gerado registra a origem e o commit do arquivo lido, para que a
defasagem apareça no diff quando o catálogo for regerado.
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
from datetime import date
from pathlib import Path

_BLOCO_RE = re.compile(r"\{\s*\n\s*id:\s*\"([^\"]+)\"(.*?)\n  \},?", re.S)


def _campo(corpo: str, nome: str) -> str:
    m = re.search(rf"\b{nome}:\s*\n?\s*\"((?:[^\"\\]|\\.)*)\"", corpo)
    return m.group(1).replace('\\"', '"') if m else ""


def _tags(corpo: str) -> list[str]:
    m = re.search(r"\btags:\s*\[([^\]]*)\]", corpo, re.S)
    return re.findall(r"\"([^\"]+)\"", m.group(1)) if m else []


def _commit(origem: Path) -> str:
    try:
        saida = subprocess.run(
            ["git", "-C", str(origem.parent), "log", "-1", "--format=%h %cs", "--", origem.name],
            capture_output=True,
            text=True,
            check=True,
        )
        return saida.stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        return ""


def extrair(texto: str) -> list[dict]:
    destinos = []
    for id_curso, corpo in _BLOCO_RE.findall(texto):
        caminho = _campo(corpo, "href")
        if not caminho:
            continue
        destinos.append(
            {
                "id": id_curso,
                "caminho": caminho,
                "nome": _campo(corpo, "title"),
                "nome_curto": _campo(corpo, "shortTitle"),
                "tags": _tags(corpo),
            }
        )
    return destinos


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print(__doc__)
        return 2
    origem, destino = Path(argv[0]), Path(argv[1])
    destinos = extrair(origem.read_text(encoding="utf-8"))
    if not destinos:
        print(f"Nenhum curso lido de {origem}; o catálogo não foi gravado.", file=sys.stderr)
        return 1
    dados = {
        "origem": "landing-page-geo/src/data/educacao-courses.ts",
        "commit_origem": _commit(origem),
        "gerado_em": date.today().isoformat(),
        "destinos": destinos,
    }
    destino.write_text(
        json.dumps(dados, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n"
    )
    print(f"{len(destinos)} destinos gravados em {destino}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
