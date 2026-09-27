"""Crosslinks por aula para outros cursos do portal (pedido do dono, 27/09/2026).

Toda aula liga para cursos do portal que completam o que ela ensina, dentro da
prosa e no fecho, com texto de link que diz o que o leitor encontra lá. O
destino sai do catálogo do portal, nunca da memória de quem escreve: rota
imaginada é defeito e reprova a aula.

A regra é OPT-IN POR CLIENTE. Piso, teto, prefixos válidos e catálogo vêm do
bloco `crosslinks` do `client.yaml` (`ClientContext.crosslinks`); a forma
(âncora genérica, parágrafos de abertura sem link, texto da instrução do
prompt) vem de `config/quality_rules.yaml > validation.crosslinks`. Com o bloco
do cliente ausente ou `enabled: false`, nada aqui roda e o prompt não muda.

Duas medidas:

- `check_crosslinks_aula`: uma aula. Destino fora do catálogo, âncora genérica
  e menos destinos que o piso são erro; mais que o teto e link na abertura são
  aviso.
- `check_crosslinks_curso`: a sequência de aulas. O mesmo destino em duas aulas
  seguidas é erro; o curso inteiro abaixo do piso de destinos distintos é erro.

Só contam links relativos cujo caminho começa por um prefixo válido. Link
dentro de bloco de código não conta; imagem não é link.
"""

from __future__ import annotations

import json
import logging
import re
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Any

import yaml

from src.validators.mascaras import sem_codigo
from src.validators.rules_loader import rules_list, validation_section

logger = logging.getLogger(__name__)

SECAO = "crosslinks"

#: Link Markdown que não é imagem: `[âncora](destino "título opcional")`.
_LINK_RE = re.compile(r"(?<!!)\[([^\]\n]+)\]\(\s*([^)\s]+)(?:\s+\"[^\"]*\")?\s*\)")
_H1_RE = re.compile(r"^#\s+(?!#)", re.MULTILINE)
_HEADING_RE = re.compile(r"^\s{0,3}#{1,6}\s")
_PONTUACAO_RE = re.compile(r"[^\w\s]")


@dataclass(frozen=True)
class LinkInterno:
    ancora: str
    caminho: str
    fragmento: str
    posicao: int


@dataclass
class AchadoCrosslink:
    regra: str
    mensagem: str
    tipo: str = "error"


def _ligado(config: Any) -> bool:
    return bool(config is not None and getattr(config, "enabled", False))


def _normalizar(caminho: str) -> str:
    return caminho.rstrip("/") or "/"


def extrair_links(texto: str, prefixos: list[str]) -> list[LinkInterno]:
    """Links internos da aula cujo caminho começa por um dos prefixos."""
    links: list[LinkInterno] = []
    for m in _LINK_RE.finditer(sem_codigo(texto or "")):
        destino = m.group(2).strip()
        if not destino.startswith("/"):
            continue
        caminho, _, fragmento = destino.partition("#")
        caminho = caminho.split("?", 1)[0]
        if not any(caminho.startswith(p) for p in prefixos):
            continue
        links.append(LinkInterno(m.group(1).strip(), _normalizar(caminho), fragmento, m.start()))
    return links


@lru_cache(maxsize=8)
def _ler_catalogo(caminho: str, _mtime: float) -> dict[str, dict]:
    arquivo = Path(caminho)
    texto = arquivo.read_text(encoding="utf-8")
    dados = json.loads(texto) if arquivo.suffix == ".json" else yaml.safe_load(texto)
    destinos = dados.get("destinos") if isinstance(dados, dict) else dados
    saida: dict[str, dict] = {}
    for item in destinos or []:
        if isinstance(item, dict) and isinstance(item.get("caminho"), str):
            saida[_normalizar(item["caminho"])] = item
    return saida


def carregar_catalogo(config: Any) -> dict[str, dict] | None:
    """Catálogo de destinos do cliente, ou `None` se não houver arquivo legível."""
    caminho = getattr(config, "catalogo", None)
    if not caminho:
        return None
    arquivo = Path(caminho)
    try:
        return _ler_catalogo(str(arquivo), arquivo.stat().st_mtime)
    except (OSError, ValueError, yaml.YAMLError, AttributeError) as exc:
        logger.warning("Catálogo de crosslinks ilegível em %s: %s", arquivo, exc)
        return None


def _ancoras_genericas() -> set[str]:
    return {_ancora_normalizada(a) for a in rules_list(SECAO, "ancoras_genericas")}


def _ancora_normalizada(ancora: str) -> str:
    return " ".join(_PONTUACAO_RE.sub(" ", ancora.lower()).split())


def _inteiro_do_yaml(chave: str) -> int:
    try:
        return max(0, int(validation_section(SECAO).get(chave, 0) or 0))
    except (TypeError, ValueError):
        return 0


def _trecho_de_abertura(texto: str, paragrafos: int) -> str:
    """Subtítulo e os N primeiros parágrafos depois do H1, antes da primeira seção."""
    if paragrafos <= 0:
        return ""
    corpo = sem_codigo(texto)
    m = _H1_RE.search(corpo)
    if m:
        corpo = corpo[m.end() :].split("\n", 1)[-1]
    blocos: list[str] = []
    for bloco in re.split(r"\n\s*\n", corpo):
        limpo = bloco.strip()
        if not limpo:
            continue
        if _HEADING_RE.match(limpo):
            break
        blocos.append(limpo)
    extra = 1 if m else 0  # o subtítulo não conta como parágrafo, mas também não leva link
    return "\n\n".join(blocos[: paragrafos + extra])


def check_crosslinks_aula(texto: str, config: Any) -> list[AchadoCrosslink]:
    """Mede os crosslinks de UMA aula. Sem configuração ligada, devolve vazio."""
    if not _ligado(config) or not texto or not texto.strip():
        return []
    prefixos = list(getattr(config, "prefixos_validos", []) or [])
    links = extrair_links(texto, prefixos)
    catalogo = carregar_catalogo(config)
    achados: list[AchadoCrosslink] = []

    if catalogo is None:
        achados.append(
            AchadoCrosslink(
                "crosslink-catalogo",
                "Catálogo de crosslinks do cliente ausente ou ilegível; os destinos não foram "
                "conferidos. Regere com scripts/gerar_catalogo_crosslinks.py.",
                "warning",
            )
        )
        validos = links
    else:
        validos = []
        for link in links:
            if link.caminho in catalogo:
                validos.append(link)
            else:
                achados.append(
                    AchadoCrosslink(
                        "crosslink-destino",
                        f"Destino fora do catálogo do portal: '{link.caminho}'. Rota imaginada "
                        f"reprova a aula; use um caminho do catálogo.",
                    )
                )

    genericas = _ancoras_genericas()
    for link in links:
        if _ancora_normalizada(link.ancora) in genericas:
            achados.append(
                AchadoCrosslink(
                    "crosslink-ancora",
                    f"Texto de link genérico: '{link.ancora}' ({link.caminho}). O texto do link "
                    f"diz o que o leitor encontra lá e cita o curso pelo nome.",
                )
            )

    distintos = {link.caminho for link in validos}
    minimo = int(getattr(config, "min_por_aula", 0) or 0)
    maximo = int(getattr(config, "max_por_aula", 0) or 0)
    if minimo and len(distintos) < minimo:
        achados.append(
            AchadoCrosslink(
                "crosslink-piso",
                f"{len(distintos)} curso(s) do portal ligado(s) na aula; o piso é {minimo} "
                f"cursos diferentes. O link entra na prosa, onde o assunto aparece, e no fecho.",
            )
        )
    if maximo and len(distintos) > maximo:
        achados.append(
            AchadoCrosslink(
                "crosslink-teto",
                f"{len(distintos)} cursos do portal ligados na aula; o teto é {maximo}, para o "
                f"link não competir com a leitura.",
                "warning",
            )
        )

    abertura = _trecho_de_abertura(texto, _inteiro_do_yaml("paragrafos_iniciais_sem_link"))
    if abertura and extrair_links(abertura, prefixos):
        achados.append(
            AchadoCrosslink(
                "crosslink-abertura",
                "Crosslink no subtítulo ou nos parágrafos de abertura; nada compete com a "
                "abertura (R2). Leve o link para o ponto da prosa em que o assunto aparece.",
                "warning",
            )
        )
    return achados


def destinos_da_aula(texto: str, config: Any) -> set[str]:
    """Caminhos distintos ligados pela aula (válidos ou não)."""
    prefixos = list(getattr(config, "prefixos_validos", []) or [])
    return {link.caminho for link in extrair_links(texto, prefixos)}


def check_crosslinks_curso(aulas: list[tuple[str, str]], config: Any) -> list[AchadoCrosslink]:
    """Mede a sequência de aulas: repetição em aulas seguidas e piso do curso."""
    if not _ligado(config) or len(aulas) < 2:
        return []
    achados: list[AchadoCrosslink] = []
    anteriores: set[str] = set()
    titulo_anterior = ""
    todos: set[str] = set()
    for titulo, texto in aulas:
        atuais = destinos_da_aula(texto, config)
        repetidos = sorted(atuais & anteriores)
        if repetidos:
            achados.append(
                AchadoCrosslink(
                    "crosslink-sequencia",
                    f"'{titulo}' repete o destino da aula anterior ('{titulo_anterior}'): "
                    f"{', '.join(repetidos)}. Varie o curso de destino entre aulas seguidas.",
                )
            )
        todos |= atuais
        anteriores, titulo_anterior = atuais, titulo
    piso = int(getattr(config, "min_destinos_distintos_no_curso", 0) or 0)
    if piso and len(todos) < piso:
        achados.append(
            AchadoCrosslink(
                "crosslink-curso",
                f"O curso liga para {len(todos)} curso(s) distinto(s) do portal; o piso é {piso}.",
            )
        )
    return achados


def destinos_sugeridos(
    config: Any, tags: list[str] | tuple[str, ...] = (), excluir: str = ""
) -> list[dict]:
    """Destinos do catálogo em ordem de afinidade de tag, sem o próprio curso."""
    catalogo = carregar_catalogo(config) or {}
    alvo = {t.lower() for t in tags}
    itens = [
        item
        for caminho, item in catalogo.items()
        if not (excluir and caminho.rstrip("/").endswith("/" + excluir))
    ]
    itens.sort(key=lambda i: -len(alvo & {str(t).lower() for t in i.get("tags", [])}))
    limite = _inteiro_do_yaml("max_destinos_no_prompt")
    return itens[:limite] if limite else itens


def instrucao_para_prompt(
    config: Any,
    tags: list[str] | tuple[str, ...] = (),
    excluir: str = "",
    anteriores: set[str] | frozenset[str] = frozenset(),
) -> str:
    """Bloco `{bloco_crosslinks}` do `draft.md`. Vazio quando a regra está desligada."""
    if not _ligado(config):
        return ""
    texto = validation_section(SECAO).get("instrucao_prompt")
    destinos = destinos_sugeridos(config, tags, excluir)
    if not isinstance(texto, str) or not texto.strip() or not destinos:
        return ""
    linhas = [
        f"- {d['caminho']}: {d.get('nome') or d.get('nome_curto') or d['caminho']}"
        for d in destinos
    ]
    aviso = (
        "A aula anterior já ligou para "
        + ", ".join(sorted(anteriores))
        + "; escolha outros destinos."
        if anteriores
        else ""
    )
    return (
        texto.strip()
        .replace("{min}", str(getattr(config, "min_por_aula", 0)))
        .replace("{max}", str(getattr(config, "max_por_aula", 0)))
        .replace("{anteriores}", aviso)
        .replace("{destinos}", "\n".join(linhas))
    )
