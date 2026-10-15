"""Conferência da pasta do curso que a fábrica entrega ao portal /educacao.

Reproduz, em segundos e sem build, as regras que o portal passou a exigir nas
Etapas 3 e 4 da reorganização do landing-page-geo (14 e 15/10/2026). Cada regra
nasceu de um curso que travou na migração:

- P1 página de servidor: `page.tsx` com "use client" não pode ler o JSON do
  disco (o `next build` quebra com "node:fs" no pacote do navegador). Treze
  cursos ficaram fora da Etapa 4 por isso.
- P2 steps.ts fino: o conteúdo mora em `src/content/cursos/<slug>.json`; o
  `steps.ts` só chama `carregarCurso(slug)`.
- P3 conteúdo sob demanda: a página serve o capítulo aberto e entrega os
  demais por `deferStepContent` e pela rota `[curso]/[capitulo]/conteudo.json`
  (PR #1464). Sem isso o HTML passa do teto de 900 KB.
- P4 JSON fora do grafo de tipos: nenhum arquivo do curso importa o JSON do
  conteúdo; JSON acima de 1 MB no `import` pesa no tsc de todo PR.
- P5 sem `url: undefined` no TypeScript que sobrar: o JSON não guarda chave
  indefinida e o payload do servidor muda (achado na migração do
  frontends-com-vibecoding, #1472).

Uso: `python scripts/conferir_pagina_portal.py <pasta-do-curso-no-portal>`.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

_USE_CLIENT = re.compile(r"""^\s*(['"])use client\1\s*;?\s*$""", re.MULTILINE)
_CARREGAR = re.compile(r"\bcarregarCurso\s*\(")
_CONTEUDO_INLINE = re.compile(r"\bcontent\s*:\s*\[")
_SOB_DEMANDA = re.compile(r"\b(deferStepContent|courseContentJsonPath)\b")
_IMPORT_JSON_CURSO = re.compile(r"""from\s+['"][^'"]*content/cursos/[^'"]+\.json['"]""")
_URL_UNDEFINED = re.compile(r"\burl\s*:\s*undefined\b")


@dataclass
class Achado:
    regra: str
    arquivo: str
    mensagem: str


@dataclass
class Resultado:
    erros: list[Achado] = field(default_factory=list)

    @property
    def aprovado(self) -> bool:
        return not self.erros


def conferir_pasta(pasta: Path) -> Resultado:
    """Confere `page.tsx`, `steps.ts` e os demais `.ts`/`.tsx` da pasta do curso."""
    res = Resultado()
    page = pasta / "page.tsx"
    steps = pasta / "steps.ts"

    if not page.is_file():
        res.erros.append(Achado("P0", str(page), "page.tsx ausente"))
    else:
        texto = page.read_text(encoding="utf-8")
        if _USE_CLIENT.search(texto):
            res.erros.append(
                Achado(
                    "P1",
                    page.name,
                    'página com "use client": o portal lê o JSON do disco no servidor; '
                    "mova a interação para um componente cliente filho",
                )
            )
        if not _SOB_DEMANDA.search(texto):
            res.erros.append(
                Achado(
                    "P3",
                    page.name,
                    "página sem conteúdo sob demanda (deferStepContent ou courseContentJsonPath); "
                    "o HTML carregaria todos os capítulos",
                )
            )

    if not steps.is_file():
        res.erros.append(Achado("P0", str(steps), "steps.ts ausente"))
    else:
        texto = steps.read_text(encoding="utf-8")
        if not _CARREGAR.search(texto):
            res.erros.append(
                Achado(
                    "P2",
                    steps.name,
                    "steps.ts não chama carregarCurso(slug); o conteúdo deve vir do JSON",
                )
            )
        if _CONTEUDO_INLINE.search(texto):
            res.erros.append(
                Achado(
                    "P2",
                    steps.name,
                    "steps.ts com conteúdo escrito no arquivo (content: [...]); mova para o JSON",
                )
            )

    for arq in sorted(pasta.rglob("*.ts*")):
        if arq.suffix not in {".ts", ".tsx"}:
            continue
        texto = arq.read_text(encoding="utf-8")
        nome = str(arq.relative_to(pasta))
        if _IMPORT_JSON_CURSO.search(texto):
            res.erros.append(
                Achado(
                    "P4",
                    nome,
                    "import do JSON do curso no código; use carregarCurso (leitura em tempo de execução)",
                )
            )
        if _URL_UNDEFINED.search(texto):
            res.erros.append(
                Achado(
                    "P5",
                    nome,
                    "url: undefined; omita a chave (o JSON não guarda chave indefinida)",
                )
            )
    return res


def formatar(res: Resultado, nome: str) -> str:
    if res.aprovado:
        return f"{nome}: página do portal OK (P1 a P5)"
    linhas = [f"{nome}: {len(res.erros)} problema(s)"]
    linhas += [f"  [{a.regra}] {a.arquivo}: {a.mensagem}" for a in res.erros]
    return "\n".join(linhas)
