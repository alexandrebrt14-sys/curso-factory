"""Completude do como fazer: a aula ensina a fazer? (pedido do dono, 27/09/2026).

A aula passou a ser guia aplicável: resposta primeiro, porquê com fonte,
pré-requisitos, passos com verbo no imperativo, verificação e erro comum com
conserto, decisões "se isto, faça aquilo", exemplo curto amarrado aos passos,
critério de pronto. Este módulo mede o que é contável nisso:

- procedimento: a maior sequência de passos (lista numerada ou linhas "Passo 1.");
- verbo no imperativo abrindo cada passo (imperativos do espelho
  `config/lexicos.json > verbosDeAcao` somados aos do YAML);
- verificação ("deu certo", "você vê", "confira se"), erro comum com conserto,
  decisão condicional e critério de pronto, por marcadores;
- orientação de aplicação: procedimento com passos suficientes ou cada decisão
  condicional, para que a aula conceitual nunca fique com zero aplicação.

O que ele não mede: se o passo está certo, se a ordem faz sentido, se o
exemplo percorre os passos. Isso fica com o prompt e com a revisão.

Tudo vem de `config/quality_rules.yaml > validation.guia_aplicavel` (pisos por
tipo de aula e marcadores) e do bloco `guia_aplicavel` do `client.yaml` (liga,
tipo de aula e severidade). Sem o bloco do cliente, ou sem a seção do YAML,
nada é medido e o gate fica como antes.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from functools import lru_cache
from typing import Any

from src.validators.blocos_de_aula import Passo, ler_aula
from src.validators.rules_loader import validation_section

SECAO = "guia_aplicavel"


@dataclass
class AchadoGuia:
    regra: str
    mensagem: str
    tipo: str = "warning"


@dataclass
class MedidaGuia:
    passos: int = 0
    passos_sem_imperativo: list[int] = field(default_factory=list)
    verificacoes: int = 0
    erros_comuns: int = 0
    condicionais: int = 0
    criterio_de_pronto: bool = False

    @property
    def parcela_imperativa(self) -> float:
        if not self.passos:
            return 0.0
        return (self.passos - len(self.passos_sem_imperativo)) / self.passos


def _secao() -> dict[str, Any]:
    secao = validation_section(SECAO)
    return secao if isinstance(secao, dict) else {}


@lru_cache(maxsize=32)
def _compilar(padroes: tuple[str, ...]) -> tuple[re.Pattern[str], ...]:
    saida = []
    for p in padroes:
        try:
            saida.append(re.compile(p, re.IGNORECASE | re.MULTILINE))
        except re.error:
            continue
    return tuple(saida)


def _padroes(secao: dict[str, Any], chave: str) -> tuple[re.Pattern[str], ...]:
    valor = secao.get(chave)
    if not isinstance(valor, list):
        return ()
    return _compilar(tuple(str(v) for v in valor if isinstance(v, str) and v))


def _contar(padroes: tuple[re.Pattern[str], ...], texto: str) -> int:
    return sum(len(p.findall(texto)) for p in padroes)


def _bloco_de_passos(secao: dict[str, Any]) -> re.Pattern[str] | None:
    expr = secao.get("bloco_de_passos")
    if not isinstance(expr, str) or not expr:
        return None
    try:
        return re.compile(expr, re.IGNORECASE)
    except re.error:
        return None


def _imperativos(secao: dict[str, Any]) -> tuple[set[str], re.Pattern[str] | None]:
    from src.validators.lexicos_loader import carregar_lexicos

    extras = {str(v).lower() for v in secao.get("verbos_imperativos") or [] if isinstance(v, str)}
    espelho = carregar_lexicos().get("verbosDeAcao")
    rx = None
    if isinstance(espelho, str) and espelho:
        try:
            rx = re.compile(espelho, re.IGNORECASE)
        except re.error:
            rx = None
    return extras, rx


def _abre_com_imperativo(passo: Passo, secao: dict[str, Any]) -> bool:
    extras, rx = _imperativos(secao)
    antes = sorted(
        (str(v).lower() for v in secao.get("antes_do_verbo") or [] if isinstance(v, str)),
        key=len,
        reverse=True,
    )
    texto = re.sub(r"[*_`\[\]]", "", passo.texto).strip().lower()
    for _ in range(2):
        for prefixo in antes:
            if (
                texto == prefixo
                or texto.startswith(prefixo + " ")
                or texto.startswith(prefixo + ",")
            ):
                texto = texto[len(prefixo) :].lstrip(" ,")
                break
    m = re.match(r"[a-zà-úç]+", texto)
    if not m:
        return False
    palavra = m.group(0)
    if palavra in extras:
        return True
    return bool(rx and rx.fullmatch(palavra))


def pisos_do_tipo(tipo: str) -> dict[str, Any]:
    """Os pisos do tipo de aula no YAML; tipo desconhecido cai no primeiro declarado."""
    tipos = _secao().get("tipos_de_aula")
    if not isinstance(tipos, dict) or not tipos:
        return {}
    escolhido = tipos.get(tipo) if tipo else None
    if not isinstance(escolhido, dict):
        escolhido = next(iter(tipos.values()))
    return escolhido if isinstance(escolhido, dict) else {}


def medir(texto: str) -> MedidaGuia:
    """Conta passos, imperativos, verificações, erros comuns, condicionais e critério."""
    secao = _secao()
    aula = ler_aula(texto, _bloco_de_passos(secao))
    procedimento = aula.procedimento
    corpo = aula.corpo
    return MedidaGuia(
        passos=len(procedimento),
        passos_sem_imperativo=[
            p.numero for p in procedimento if not _abre_com_imperativo(p, secao)
        ],
        verificacoes=_contar(_padroes(secao, "verificacao"), corpo),
        erros_comuns=_contar(_padroes(secao, "erro_comum"), corpo),
        condicionais=_contar(_padroes(secao, "condicional"), corpo),
        criterio_de_pronto=_contar(_padroes(secao, "criterio_de_pronto"), corpo) > 0,
    )


def _ligado(config: Any) -> bool:
    return bool(config is not None and getattr(config, "enabled", False))


def _num(pisos: dict[str, Any], chave: str) -> float | None:
    try:
        valor = pisos.get(chave)
        return None if valor is None else float(valor)
    except (TypeError, ValueError):
        return None


def check_guia_aplicavel(texto: str, config: Any, tipo: str | None = None) -> list[AchadoGuia]:
    """Mede UMA aula contra os pisos do tipo. Cliente sem a regra ligada: vazio."""
    secao = _secao()
    if not _ligado(config) or not secao or not texto or not texto.strip():
        return []
    tipo_de_aula = tipo or getattr(config, "tipo_de_aula", "") or ""
    pisos = pisos_do_tipo(tipo_de_aula)
    if not pisos:
        return []
    nivel = "error" if getattr(config, "severidade", "aviso") == "erro" else "warning"
    m = medir(texto)
    achados: list[AchadoGuia] = []

    def _piso(chave: str) -> float | None:
        return _num(pisos, chave)

    passos_min = _piso("passos_min")
    if passos_min and m.passos < passos_min:
        achados.append(
            AchadoGuia(
                "guia-sem-procedimento",
                f"{m.passos} passo(s) em sequência; a aula ensina a fazer com ao menos "
                f"{passos_min:g}: lista numerada na ordem em que o aluno executa, um verbo por "
                f"passo, com o que fazer e como saber que deu certo.",
                nivel,
            )
        )
    parcela = _piso("imperativo_min_parcela")
    if parcela is not None and m.passos and m.parcela_imperativa < parcela:
        achados.append(
            AchadoGuia(
                "passo-sem-imperativo",
                f"Passo(s) {', '.join(str(n) for n in m.passos_sem_imperativo)} não abre(m) com "
                f"verbo no imperativo; cada passo começa pelo que o aluno faz (abra, anote, "
                f"escolha).",
                nivel,
            )
        )
    for chave, valor, regra, conserto in (
        (
            "verificacoes_min",
            m.verificacoes,
            "guia-sem-verificacao",
            "diga, no passo ou no fim, como o aluno sabe que deu certo (o que ele vê na tela, "
            "o número que aparece)",
        ),
        (
            "erros_comuns_min",
            m.erros_comuns,
            "guia-sem-erro-comum",
            "diga o erro mais comum no passo em que ele acontece, com o conserto na mesma frase",
        ),
        (
            "condicionais_min",
            m.condicionais,
            "guia-sem-decisao",
            'onde a resposta muda com a situação, escreva "se isto, faça aquilo" no lugar de '
            '"depende"',
        ),
    ):
        minimo = _piso(chave)
        if minimo and valor < minimo:
            achados.append(
                AchadoGuia(regra, f"{valor} ocorrência(s), piso {minimo:g}: {conserto}.", nivel)
            )
    aplicacao_min = _piso("aplicacao_min")
    passos_para_aplicacao = _num(secao, "passos_para_aplicacao") or 0
    aplicacao = m.condicionais + (
        1 if passos_para_aplicacao and m.passos >= passos_para_aplicacao else 0
    )
    if aplicacao_min and aplicacao < aplicacao_min:
        achados.append(
            AchadoGuia(
                "guia-sem-aplicacao",
                "A aula não traz orientação de aplicação: nem procedimento em passos, nem "
                'decisão "se isto, faça aquilo". Mesmo aula de conceito diz o que o aluno faz '
                "com ele.",
                nivel,
            )
        )
    if pisos.get("criterio_de_pronto") and not m.criterio_de_pronto:
        achados.append(
            AchadoGuia(
                "guia-sem-criterio-de-pronto",
                'O fecho não diz quando o aluno terminou ("está pronto quando", "deu certo '
                'quando"), com número, prazo ou condição observável.',
                nivel,
            )
        )
    return achados


def instrucao_para_prompt(config: Any = None, tipo: str | None = None) -> str:
    """Bloco `{bloco_molde_da_aula}`: o esqueleto do YAML e, com o cliente ligado, os pisos."""
    secao = _secao()
    modelo = secao.get("instrucao_prompt")
    esqueleto = secao.get("esqueleto")
    if not isinstance(modelo, str) or not isinstance(esqueleto, list) or not esqueleto:
        return ""
    linhas = []
    for i, parte in enumerate(esqueleto, 1):
        if isinstance(parte, dict) and parte.get("parte") and parte.get("instrucao"):
            linhas.append(f"{i}. {str(parte['parte']).strip()}: {str(parte['instrucao']).strip()}")
    if not linhas:
        return ""
    texto = modelo.strip().replace("{esqueleto}", "\n".join(linhas))
    if _ligado(config):
        pisos = pisos_do_tipo(tipo or getattr(config, "tipo_de_aula", "") or "")
        extra = pisos.get("instrucao") if pisos else None
        if isinstance(extra, str) and extra.strip():
            extra = extra.strip()
            for chave in ("passos_min", "verificacoes_min", "erros_comuns_min", "condicionais_min"):
                extra = extra.replace("{" + chave + "}", f"{_num(pisos, chave) or 0:g}")
            texto += "\n\n" + extra
    return texto


def instrucao_do_plano() -> str:
    """Frase que entra no prompt de planejamento de aulas; vazia sem a seção."""
    valor = _secao().get("instrucao_plano")
    return valor.strip() if isinstance(valor, str) else ""
