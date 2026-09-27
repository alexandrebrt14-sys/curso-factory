"""Máscaras de texto de leitura, compartilhadas pelos validadores de vocabulário.

Contar palavra em aula exige tirar da contagem o que não é texto de leitura:
bloco de código, código inline, menção entre aspas, nome de arquivo e chave de
configuração. Cada máscara troca o trecho por espaços do mesmo tamanho, para que
posição e número de linha continuem batendo com o original.

As expressões ficam compiladas uma vez, no import. Nenhuma delas é regra
editorial: são a mecânica de separar leitura de aparato. As regras (quais
palavras, qual limite, qual severidade) vivem em `config/quality_rules.yaml`.
"""

from __future__ import annotations

import re

#: Bloco de código cercado por crase tripla.
CODIGO_CERCADO_RE = re.compile(r"```[\s\S]*?```")
#: Código inline entre crases simples.
CODIGO_INLINE_RE = re.compile(r"`[^`\n]*`")
#: Trecho curto entre aspas retas, curvas ou angulares: menção, não uso.
MENCAO_RE = re.compile(r"[\"“„”«]([^\"“„”«»\n]{1,120})[\"”»]")
#: Nome de arquivo, caminho ou chave pontuada: `regua.py`, `a/b/c`, `tetos.D.figuras_max`.
IDENTIFICADOR_RE = re.compile(r"(?<![\w./\\-])[\w-]*(?:[./\\_][\w-]+)+")
#: Destino de link Markdown: `](caminho)`. O texto âncora continua sendo leitura.
DESTINO_DE_LINK_RE = re.compile(r"\]\([^)\n]*\)")


def _apagar(match: re.Match[str]) -> str:
    return re.sub(r"[^\n]", " ", match.group(0))


def sem_codigo(texto: str) -> str:
    """Apaga blocos de código e código inline, preservando posições."""
    return CODIGO_INLINE_RE.sub(_apagar, CODIGO_CERCADO_RE.sub(_apagar, texto))


def sem_mencoes(texto: str) -> str:
    """Apaga o que está entre aspas, preservando posições."""
    return MENCAO_RE.sub(_apagar, texto)


def sem_identificadores(texto: str) -> str:
    """Apaga nome de arquivo, caminho, chave de configuração e destino de link."""
    return IDENTIFICADOR_RE.sub(_apagar, DESTINO_DE_LINK_RE.sub(_apagar, texto))


def texto_de_leitura(texto: str, respeitar_mencao: bool = True) -> str:
    """O que o aluno lê como prosa: sem código, sem identificador e, por padrão, sem menção."""
    limpo = sem_identificadores(sem_codigo(texto))
    return sem_mencoes(limpo) if respeitar_mencao else limpo
