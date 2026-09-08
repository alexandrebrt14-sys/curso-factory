"""Leitura em runtime de config/quality_rules.yaml.

Até 11/08/2026 esse YAML era decorativo: nenhum módulo do repositório o lia.
A consequência prática aparecia em `forbidden_expressions.expressions`, que
tinha 46 entradas enquanto o gate rodava com as 18 hardcoded em
`content_checker.FORBIDDEN_CLICHES` — expressões como "especialistas apontam"
e "estudos indicam" nunca chegaram a ser checadas. As chaves
`anti_invencao.require_source_for_percentages` e
`anti_invencao.fail_if_unresolved_markers_above` também não existiam em código.

Este módulo fecha a lacuna. Editar uma lista no YAML passa a mudar o
comportamento da validação, sem tocar em Python.

Contrato de robustez: nada aqui levanta exceção. Arquivo ausente, YAML
quebrado ou estrutura inesperada devolvem `{}` com aviso no log, e o chamador
cai no fallback embutido. Validador que derruba o pipeline por causa de config
faltando é pior que validador conservador.

Uso:
    from src.validators.rules_loader import load_rules, validation_section

    teto = validation_section("anti_invencao").get("fail_if_unresolved_markers_above", 5)
"""

from __future__ import annotations

import logging
from functools import lru_cache
from pathlib import Path
from typing import Any

import yaml

logger = logging.getLogger(__name__)

# Raiz do projeto (três níveis acima de src/validators/), no mesmo padrão de
# src/config.py::ROOT_DIR.
ROOT_DIR = Path(__file__).resolve().parent.parent.parent
RULES_PATH = ROOT_DIR / "config" / "quality_rules.yaml"


@lru_cache(maxsize=1)
def load_rules() -> dict[str, Any]:
    """Carrega config/quality_rules.yaml como dict, com cache de processo.

    O resultado é memoizado: o YAML é lido uma vez por processo. Testes que
    trocam `RULES_PATH` precisam chamar `load_rules.cache_clear()` antes e
    depois da troca.

    Returns:
        Dict com o conteúdo do YAML, ou `{}` quando o arquivo não existe,
        não é lido, não é YAML válido ou não tem mapeamento no topo.
        Nunca levanta exceção.
    """
    path = RULES_PATH
    if not path.exists():
        logger.warning(
            "quality_rules.yaml não encontrado em %s — validadores seguem com os fallbacks "
            "embutidos no código.",
            path,
        )
        return {}

    try:
        with path.open("r", encoding="utf-8") as fh:
            data = yaml.safe_load(fh)
    except (OSError, yaml.YAMLError) as exc:
        logger.warning(
            "Falha ao ler quality_rules.yaml (%s) — validadores seguem com os fallbacks "
            "embutidos no código.",
            exc,
        )
        return {}

    if not isinstance(data, dict):
        logger.warning(
            "quality_rules.yaml não tem um mapeamento no nível superior (tipo lido: %s) — "
            "validadores seguem com os fallbacks embutidos no código.",
            type(data).__name__,
        )
        return {}

    return data


def validation_section(name: str) -> dict[str, Any]:
    """Devolve `validation.<name>` do YAML, ou `{}` se ausente/malformado.

    Args:
        name: nome da subseção sob `validation` (ex.: "anti_invencao").
    """
    validation = load_rules().get("validation")
    if not isinstance(validation, dict):
        return {}
    section = validation.get(name)
    return section if isinstance(section, dict) else {}


def rules_list(section: str, key: str) -> list[str]:
    """Devolve uma lista de strings de `validation.<section>.<key>`.

    Itens não-string e strings vazias são descartados, para que um YAML
    editado à mão nunca quebre o validador que consome a lista.
    """
    raw = validation_section(section).get(key)
    if not isinstance(raw, list):
        return []
    return [item.strip() for item in raw if isinstance(item, str) and item.strip()]
