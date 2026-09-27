"""Blocos de uma aula em Markdown, para os medidores de guia e de narrativa (27/09/2026).

Mecânica pura, sem regra editorial: separa o texto em blocos (parágrafo de prosa,
lista numerada, lista, tabela, citação, cabeçalho), tira o H1, o subtítulo, o
código e o bloco de fontes do rodapé, e devolve os parágrafos de prosa e os
itens de lista numerada na ordem em que aparecem. Quais marcas contam, quantas
e com que severidade fica em `config/quality_rules.yaml`.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field

from src.validators.mascaras import CODIGO_CERCADO_RE, sem_codigo

_H1_RE = re.compile(r"^#\s+(?!#).*$", re.MULTILINE)
_CABECALHO_RE = re.compile(r"^\s{0,3}(#{1,6})\s+(.*)$")
_ITEM_NUMERADO_RE = re.compile(r"^\s{0,3}(\d+)[.)]\s+(.*)$")
_ITEM_RE = re.compile(r"^\s{0,3}(?:[-*+]|--)\s+")


@dataclass
class Passo:
    numero: int
    texto: str


@dataclass
class Aula:
    """A aula em partes: prosa em ordem, listas de passos, texto corrido para busca."""

    paragrafos: list[str] = field(default_factory=list)
    listas_de_passos: list[list[Passo]] = field(default_factory=list)
    corpo: str = ""

    @property
    def procedimento(self) -> list[Passo]:
        """A maior sequência de passos da aula (lista numerada ou bloco de passos)."""
        return max(self.listas_de_passos, key=len, default=[])


def sem_rodape_de_fontes(texto: str) -> str:
    """Corta todo bloco `## Fontes` (do cabeçalho até o próximo cabeçalho)."""
    from src.parsers.markdown_parser import extrair_fontes

    anterior = None
    while anterior != texto:
        anterior = texto
        texto, _ = extrair_fontes(texto)
    return texto


def _sem_subtitulo(corpo: str) -> str:
    from src.parsers.markdown_parser import extrair_subtitulo

    _, resto = extrair_subtitulo(corpo)
    return resto


def ler_aula(texto: str, bloco_de_passos: re.Pattern[str] | None = None) -> Aula:
    """Separa a aula em parágrafos de prosa e listas de passos.

    `bloco_de_passos`, quando dado, reconhece passo fora de lista numerada
    (linha que abre com "Passo 1."): grupo 1 é o número, grupo 2 o texto.
    """
    bruto = CODIGO_CERCADO_RE.sub("", texto or "")
    bruto = _H1_RE.sub("", bruto, count=1).strip()
    bruto = sem_rodape_de_fontes(_sem_subtitulo(bruto))
    aula = Aula(corpo=sem_codigo(bruto))
    corrente: list[Passo] = []

    def _fechar() -> None:
        nonlocal corrente
        if corrente:
            aula.listas_de_passos.append(corrente)
        corrente = []

    for bloco in re.split(r"\n\s*\n", bruto):
        linhas = [linha for linha in bloco.splitlines() if linha.strip()]
        if not linhas:
            continue
        primeira = linhas[0]
        numerado = _ITEM_NUMERADO_RE.match(primeira)
        passo_solto = bloco_de_passos.match(primeira) if bloco_de_passos else None
        if numerado or passo_solto:
            for linha in linhas:
                m = _ITEM_NUMERADO_RE.match(linha) or (
                    bloco_de_passos.match(linha) if bloco_de_passos else None
                )
                if m:
                    numero = int(m.group(1))
                    if corrente and numero != corrente[-1].numero + 1:
                        _fechar()
                    corrente.append(Passo(numero, m.group(2).strip()))
                elif corrente:
                    corrente[-1].texto += " " + linha.strip()
            continue
        if _CABECALHO_RE.match(primeira):
            _fechar()
            resto = [linha for linha in linhas[1:] if linha.strip()]
            if resto and not _CABECALHO_RE.match(resto[0]):
                aula.paragrafos.append(" ".join(s.strip() for s in resto))
            continue
        if _ITEM_RE.match(primeira) or primeira.lstrip().startswith(("|", ">", "![")):
            continue
        # Parágrafo de prosa entre passos não fecha a lista: a lista numerada do
        # Markdown recomeça a contagem, e o `1.` seguinte abre outra sequência.
        aula.paragrafos.append(" ".join(s.strip() for s in linhas))
    _fechar()
    return aula
