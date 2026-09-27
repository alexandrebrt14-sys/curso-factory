"""Tamanho e ordem do curso, orientados pelos dados de uso do portal (27/09/2026).

Os dados de uso do portal /educacao mostraram três coisas que o planejamento de
aulas não levava em conta: curso curto termina e curso longo não; o aluno
abandona na teoria que chega cedo e no apêndice de instalação; e a rolagem dos
capítulos abandonados fica abaixo da metade da página. Daí saem as orientações
que entram no planejamento e na redação, e duas conferências baratas, sempre
como aviso: o curso fora da faixa de aulas e uma das primeiras aulas acima do
alvo de palavras.

Tudo vem de `config/quality_rules.yaml > validation.planejamento`. Sem a seção,
ou com `enabled: false`, nenhuma instrução entra nos prompts e nada é conferido.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from src.validators.rules_loader import validation_section

SECAO = "planejamento"


@dataclass
class AchadoPlanejamento:
    regra: str
    mensagem: str
    tipo: str = "warning"


def _secao() -> dict[str, Any]:
    secao = validation_section(SECAO)
    return secao if secao and bool(secao.get("enabled", True)) else {}


def _inteiro(valor: Any) -> int | None:
    try:
        return int(valor)
    except (TypeError, ValueError):
        return None


def _faixa(valor: Any) -> tuple[int, int] | None:
    if isinstance(valor, (list, tuple)) and len(valor) == 2:
        a, b = _inteiro(valor[0]), _inteiro(valor[1])
        if a is not None and b is not None:
            return a, b
    return None


def _texto(secao: dict[str, Any], chave: str) -> str:
    valor = secao.get(chave)
    return valor.strip() if isinstance(valor, str) else ""


def instrucao_do_plano(numero_modulo: int) -> str:
    """Parágrafo que entra no prompt de planejamento de aulas do módulo."""
    secao = _secao()
    texto = _texto(secao, "instrucao_plano")
    faixa = _faixa(secao.get("aulas_por_curso"))
    iniciais = _inteiro(secao.get("aulas_iniciais_curtas"))
    if not texto or faixa is None or iniciais is None:
        return ""
    return (
        texto.replace("{aulas_min}", str(faixa[0]))
        .replace("{aulas_max}", str(faixa[1]))
        .replace("{iniciais}", str(iniciais))
        .replace("{modulo}", str(numero_modulo))
    )


def instrucao_da_aula(posicao_no_curso: int) -> str:
    """Bloco `{bloco_ordem_do_curso}` do `draft.md` para a aula nesta posição."""
    secao = _secao()
    partes = [_texto(secao, "instrucao_aula")]
    iniciais = _inteiro(secao.get("aulas_iniciais_curtas"))
    palavras = _inteiro(secao.get("palavras_max_aulas_iniciais"))
    inicial = _texto(secao, "instrucao_aula_inicial")
    if inicial and iniciais and palavras and 1 <= posicao_no_curso <= iniciais:
        partes.append(inicial.replace("{palavras_max}", str(palavras)))
    return "\n\n".join(p for p in partes if p)


def teto_da_aula_inicial(posicao_no_curso: int) -> int | None:
    """Alvo máximo de palavras se a aula está entre as primeiras do curso; senão `None`."""
    secao = _secao()
    iniciais = _inteiro(secao.get("aulas_iniciais_curtas"))
    teto = _inteiro(secao.get("palavras_max_aulas_iniciais"))
    if iniciais and teto and 1 <= posicao_no_curso <= iniciais:
        return teto
    return None


def check_planejamento_curso(aulas: list[tuple[str, str]]) -> list[AchadoPlanejamento]:
    """Faixa de aulas do curso e extensão das primeiras aulas, como aviso."""
    secao = _secao()
    if not secao or len(aulas) < 2:
        return []
    from src.validators.content_checker import _count_words

    achados: list[AchadoPlanejamento] = []
    faixa = _faixa(secao.get("aulas_por_curso"))
    if faixa and not (faixa[0] <= len(aulas) <= faixa[1]):
        achados.append(
            AchadoPlanejamento(
                "curso-tamanho",
                f"O curso tem {len(aulas)} aulas; para tema amplo, o padrão é de {faixa[0]} a "
                f"{faixa[1]}. Curso curto termina, curso longo não: aula que não muda uma decisão "
                f"do aluno sai.",
            )
        )
    iniciais = _inteiro(secao.get("aulas_iniciais_curtas")) or 0
    teto = _inteiro(secao.get("palavras_max_aulas_iniciais"))
    if teto:
        for titulo, texto in aulas[:iniciais]:
            palavras = _count_words(texto)
            if palavras > teto:
                achados.append(
                    AchadoPlanejamento(
                        "aula-inicial-longa",
                        f"'{titulo}' tem {palavras} palavras; as {iniciais} primeiras aulas "
                        f"do curso ficam em até {teto}, curtas e práticas.",
                    )
                )
    return achados
