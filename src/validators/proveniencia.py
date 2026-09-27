"""Tabela de proveniência: as frases da aula que precisam de fonte, para conferência.

Pedido do dono em 27/09/2026, depois de duas execuções em que "nunca invente"
no prompt não impediu fabricação: cada número, data, versão e nome de produto
da aula sai com a fonte primária que foi aberta, registrada fora da página.
Sem proveniência, o fato sai do texto.

O formato de retorno do pipeline não muda: o redator devolve só a aula, e o
revisor devolve a aula e o relatório no contrato existente. A tabela é montada
depois, a partir do texto final, por este módulo. Ela lista cada frase com
número, data, versão ou nome de produto, com as colunas de fonte, trecho lido e
data de acesso em branco para quem confere preencher, e os crosslinks da aula.
É arquivo de trabalho: nunca vai para a página.

Onde aparece:

- `result.etapas["proveniencia"]`, gravada pelo orquestrador ao fim do pipeline;
- `python cli.py proveniencia <arquivo.md> [--saida tabela.md]`, para rascunho
  escrito fora do pipeline.

Os padrões de cada tipo e os rótulos de exemplo vivem em
`config/quality_rules.yaml > validation.proveniencia`. Sem a seção, nada é
extraído.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from functools import lru_cache

from src.validators.mascaras import CODIGO_CERCADO_RE, CODIGO_INLINE_RE
from src.validators.rules_loader import rules_list, validation_section

SECAO = "proveniencia"

_FIM_DE_FRASE_RE = re.compile(r"(?<=[.!?])\s+(?=[A-ZÀ-Ú\"“(])")
_LINK_RE = re.compile(r"(?<!!)\[([^\]\n]+)\]\(\s*([^)\s]+)")
_CABECALHO_AULA_RE = re.compile(r"^#\s+(.+?)\s*$", re.MULTILINE)
_SEPARADOR_DE_TABELA_RE = re.compile(r"^\|[\s:|-]+\|$")


@dataclass
class FraseFactual:
    linha: int
    frase: str
    tipos: list[str] = field(default_factory=list)
    exemplo: bool = False


@lru_cache(maxsize=16)
def _compilar(padroes: tuple[tuple[str, str], ...]) -> tuple[tuple[str, re.Pattern[str]], ...]:
    saida = []
    for tipo, expressao in padroes:
        try:
            saida.append((tipo, re.compile(expressao)))
        except re.error:
            continue
    return tuple(saida)


def _padroes() -> tuple[tuple[str, re.Pattern[str]], ...]:
    secao = validation_section(SECAO)
    if not secao or not bool(secao.get("enabled", True)):
        return ()
    brutos = secao.get("padroes")
    if not isinstance(brutos, dict):
        return ()
    pares = tuple(
        (str(tipo), str(expr)) for tipo, expr in brutos.items() if isinstance(expr, str) and expr
    )
    return _compilar(pares)


def _rotulos_de_exemplo() -> list[str]:
    return [r.lower() for r in rules_list(SECAO, "rotulos_de_exemplo")]


def _linhas_de_leitura(texto: str) -> list[tuple[int, str]]:
    """Linhas de texto de leitura, sem código, cabeçalho de aula nem separador de tabela."""

    def _branco(m: re.Match[str]) -> str:
        return re.sub(r"[^\n]", " ", m.group(0))

    limpo = CODIGO_INLINE_RE.sub(_branco, CODIGO_CERCADO_RE.sub(_branco, texto or ""))
    saida = []
    for numero, linha in enumerate(limpo.splitlines(), 1):
        s = linha.strip()
        if not s or s.startswith("# ") or _SEPARADOR_DE_TABELA_RE.match(s):
            continue
        saida.append((numero, s))
    return saida


def frases_para_conferencia(texto: str) -> list[FraseFactual]:
    """Frases (ou linhas de tabela) com número, data, versão ou nome de produto."""
    padroes = _padroes()
    if not padroes:
        return []
    rotulos = _rotulos_de_exemplo()
    achadas: list[FraseFactual] = []
    for numero, linha in _linhas_de_leitura(texto):
        pedacos = [linha] if linha.startswith("|") else _FIM_DE_FRASE_RE.split(linha)
        for pedaco in pedacos:
            frase = _LINK_RE.sub(lambda m: m.group(1), pedaco).strip(" |-*>")
            tipos = [tipo for tipo, rx in padroes if rx.search(frase)]
            if not tipos:
                continue
            exemplo = any(r in frase.lower() for r in rotulos)
            achadas.append(FraseFactual(numero, frase, tipos, exemplo))
    return achadas


def _celula(texto: str) -> str:
    return texto.replace("|", "/").replace("\n", " ").strip()


def tabela_de_proveniencia(texto: str) -> str:
    """Tabela Markdown de bastidor, uma seção por aula, com frases e crosslinks."""
    if not _padroes():
        return ""
    inicios = [(m.start(), m.group(1)) for m in _CABECALHO_AULA_RE.finditer(texto or "")]
    if not inicios:
        inicios = [(0, "Texto")]
    partes = [
        "# Proveniência (arquivo de trabalho, não vai para a página)",
        "",
        "Cada frase abaixo só fica na aula com a fonte primária aberta: URL, trecho lido e data "
        "de acesso. Frase sem fonte sai do texto. Exemplo rotulado dispensa fonte.",
    ]
    for k, (inicio, titulo) in enumerate(inicios):
        fim = inicios[k + 1][0] if k + 1 < len(inicios) else len(texto)
        bloco = texto[inicio:fim]
        if titulo.startswith("Trilha "):
            continue
        frases = frases_para_conferencia(bloco)
        links = _LINK_RE.findall(bloco)
        partes += ["", f"## {titulo}", ""]
        if frases:
            partes += [
                "| Frase da aula | Tipo | URL primária | Trecho lido | Data de acesso |",
                "|---|---|---|---|---|",
            ]
            for f in frases:
                url = "exemplo rotulado, sem fonte" if f.exemplo else ""
                partes.append(f"| {_celula(f.frase)} | {', '.join(f.tipos)} | {url} |  |  |")
        else:
            partes.append("Nenhuma frase com número, data, versão ou nome de produto.")
        internos = [(a, c) for a, c in links if c.startswith("/")]
        if internos:
            partes += ["", "| Crosslink (texto do link) | Caminho |", "|---|---|"]
            partes += [f"| {_celula(a)} | {c} |" for a, c in internos]
    return "\n".join(partes) + "\n"
