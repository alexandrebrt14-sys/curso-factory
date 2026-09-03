"""Leitura do léxico e dos tetos vindos da fonte única de estilo.

A fonte é o repositório `alexandrebrt14-sys/escrita-empreendedor`. O arquivo
`config/lexicos.json` deste repositório é um **espelho gerado**, não um
original: ele sai de

    python -m escrita.cli lexicos --json > config/lexicos.json

rodado dentro da fonte. Nada aqui é editado à mão. Quando a fonte muda, o
espelho é regerado e o hash em `DIRETRIZ_EDITORIAL.md` (ponteiro) é atualizado.

Por que existe: até 27/08/2026 o repositório mantinha cópia própria das listas
de clichê (18 entradas em `content_checker.FORBIDDEN_CLICHES`, 56 em
`config/quality_rules.yaml`) e cópia própria dos números de extensão. Duas
cópias da mesma regra divergem em silêncio — foi o que aconteceu com
"especialistas apontam", que existia no YAML e nunca era checada. A regra
transversal do `PLANO_DE_MIGRACAO.md` é: nenhum repositório mantém lista,
número ou regra que também exista na fonte.

O que este módulo entrega:

- `tetos_da_aula()` — o bloco `tetos["D"]` da fonte (o tipo D é a aula), que é
  de onde saem piso, alvo, aviso, erro, H2, H3 por H2, figuras e parágrafo.
- `expressoes_vetadas()` — a união das listas de expressão proibida da fonte
  (clichê de máquina, adjetivo vazio, atribuição vaga, escassez fabricada e
  conectivo de enchimento).

Contrato de robustez, igual ao do `rules_loader`: nada aqui levanta exceção.
Arquivo ausente ou JSON quebrado devolvem vazio com aviso no log, e o chamador
cai no fallback embutido em código. Validador que derruba o pipeline por causa
de configuração faltando é pior que validador conservador.
"""

from __future__ import annotations

import json
import logging
from functools import lru_cache
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
LEXICOS_PATH = ROOT_DIR / "config" / "lexicos.json"

#: Chaves da fonte que reúnem expressão proibida em prosa. `jargao` fica de
#: fora de propósito: jargão pede glosa, não proibição, e cobrá-lo aqui
#: reprovaria termo técnico legítimo de curso.
CHAVES_DE_EXPRESSAO_VETADA = (
    "clichesDeMaquina",
    "adjetivosVazios",
    "atribuicaoVaga",
    "escassezFabricada",
    "conectivosDeEnchimento",
)


@lru_cache(maxsize=1)
def carregar_lexicos() -> dict[str, Any]:
    """Carrega `config/lexicos.json`, com cache de processo.

    Returns:
        Dict com o léxico da fonte, ou `{}` quando o arquivo não existe, não é
        lido ou não é JSON válido com mapeamento no topo. Nunca levanta.
    """
    path = LEXICOS_PATH
    if not path.exists():
        logger.warning(
            "lexicos.json não encontrado em %s — os validadores seguem com os fallbacks "
            "embutidos no código. Regere com: python -m escrita.cli lexicos --json",
            path,
        )
        return {}

    try:
        with path.open("r", encoding="utf-8") as fh:
            dados = json.load(fh)
    except (OSError, ValueError) as exc:
        logger.warning(
            "Falha ao ler lexicos.json (%s) — os validadores seguem com os fallbacks "
            "embutidos no código.",
            exc,
        )
        return {}

    if not isinstance(dados, dict):
        logger.warning(
            "lexicos.json não tem um mapeamento no nível superior (tipo lido: %s).",
            type(dados).__name__,
        )
        return {}

    return dados


def tetos_da_aula() -> dict[str, Any]:
    """Devolve `tetos["D"]` da fonte — o molde da aula.

    O tipo D da tabela única de tetos (`MOLDES_DE_PAGINA.md`, seção 2) é a
    aula/trilha, que é a unidade de medida deste repositório desde 27/08/2026.

    Returns:
        Dict com as chaves `palavras`, `h2`, `h3_por_h2`, `figuras_max` e
        `paragrafo`, ou `{}` se o espelho não carregar.
    """
    tetos = carregar_lexicos().get("tetos")
    if not isinstance(tetos, dict):
        return {}
    aula = tetos.get("D")
    return aula if isinstance(aula, dict) else {}


#: Famílias da fonte que denunciam bastidor: o texto falando de si, da regra
#: seguida, da checagem feita ou do método da estimativa. Desde 03/09/2026 são
#: erro no checker; até então o prompt proibia e nenhum código conferia.
CHAVES_DE_BASTIDOR = (
    "bastidorDeVerificacao",
    "rotuloDeConfianca",
    "metalinguagemDeProcesso",
)


def _lista(chave: str) -> list[str]:
    bruto = carregar_lexicos().get(chave)
    if not isinstance(bruto, list):
        return []
    saida: list[str] = []
    vistos: set[str] = set()
    for item in bruto:
        if isinstance(item, str) and item.strip() and item.strip().lower() not in vistos:
            vistos.add(item.strip().lower())
            saida.append(item.strip())
    return saida


def expressoes_de_bastidor() -> list[str]:
    """União das famílias de bastidor da fonte. Vazia se o espelho não carregar."""
    saida: list[str] = []
    vistos: set[str] = set()
    for chave in CHAVES_DE_BASTIDOR:
        for item in _lista(chave):
            if item.lower() not in vistos:
                vistos.add(item.lower())
                saida.append(item)
    return saida


def regex_de_metalinguagem() -> str:
    """Padrão de autorreferência da fonte (`metalinguagemRx`), ou vazio."""
    rx = carregar_lexicos().get("metalinguagemRx")
    return rx if isinstance(rx, str) and rx.strip() else ""


def regex_de_autoapresentacao() -> str:
    """Padrão da página que se apresenta em vez de responder (`autoapresentacaoRx`)."""
    rx = carregar_lexicos().get("autoapresentacaoRx")
    return rx if isinstance(rx, str) and rx.strip() else ""


def expressoes_de_muleta_legal() -> list[str]:
    """Aviso legal genérico que a fonte manda trocar por fato com número."""
    return _lista("muletaLegal")


def expressoes_vetadas() -> list[str]:
    """Une as listas de expressão proibida da fonte, deduplicadas.

    Returns:
        Lista em minúsculas, sem repetição, na ordem das chaves de
        `CHAVES_DE_EXPRESSAO_VETADA`. Vazia se o espelho não carregar.
    """
    dados = carregar_lexicos()
    saida: list[str] = []
    vistos: set[str] = set()
    for chave in CHAVES_DE_EXPRESSAO_VETADA:
        bruto = dados.get(chave)
        if not isinstance(bruto, list):
            continue
        for item in bruto:
            if not isinstance(item, str):
                continue
            limpo = item.strip()
            if not limpo or limpo.lower() in vistos:
                continue
            vistos.add(limpo.lower())
            saida.append(limpo)
    return saida
