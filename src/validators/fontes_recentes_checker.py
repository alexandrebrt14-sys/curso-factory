"""Fonte recente e datada (pedido do dono, 27/09/2026).

Todo conceito central da aula se apoia em fonte primária com data de
publicação; em tema que muda rápido, a fonte é dos últimos meses; fonte antiga
só entra como origem do conceito, dita como tal. Este módulo lê:

- o bloco `## Fontes` (da aula ou do fechamento da trilha), uma fonte por linha;
- a tabela de proveniência preenchida (`proveniencia.py`), quando o chamador a
  entrega: as linhas com URL contam como fontes, e a coluna "Data de
  publicação" dá a idade de cada frase;
- a atribuição curta com data no corpo ("(Microsoft, julho de 2026)").

E confere, conforme o bloco `fontes_recentes` do `client.yaml` (ou do curso):

- `fonte-sem-data`: fonte sem data de publicação legível; ela conta como não recente;
- `fontes-pouco-recentes`: parcela de fontes com até `janela_meses` abaixo de
  `parcela_min_recente` (a fonte marcada como origem do conceito fica fora da conta);
- `estado-atual-com-fonte-antiga`: frase que afirma o estado atual ("hoje",
  "atualmente", "a versão atual") apoiada em fonte com mais de
  `estado_atual_max_meses`.

A data de referência nunca é lida do relógio aqui dentro: vem do parâmetro
`referencia`, que o chamador preenche com `data_de_referencia` da configuração
ou com a data da execução. Formatos de data, nomes de mês e marcadores vivem em
`config/quality_rules.yaml > validation.fontes_recentes`.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from datetime import date
from functools import lru_cache
from typing import Any

from src.validators.rules_loader import validation_section

SECAO = "fontes_recentes"

_URL_RE = re.compile(r"https?://\S+")
_FIM_DE_FRASE_RE = re.compile(r"(?<=[.!?])\s+(?=[A-ZÀ-Ú\"“(])")


@dataclass
class AchadoFonte:
    regra: str
    mensagem: str
    tipo: str = "warning"


@dataclass
class Fonte:
    texto: str
    data: date | None = None
    origem: bool = False
    url: str = ""


@dataclass
class MedidaFontes:
    fontes: list[Fonte] = field(default_factory=list)
    recentes: int = 0
    contadas: int = 0
    estado_atual_antigo: list[tuple[str, int]] = field(default_factory=list)

    @property
    def parcela(self) -> float:
        return self.recentes / self.contadas if self.contadas else 0.0


def _secao() -> dict[str, Any]:
    secao = validation_section(SECAO)
    return secao if isinstance(secao, dict) else {}


@lru_cache(maxsize=16)
def _compilar(padroes: tuple[str, ...]) -> tuple[re.Pattern[str], ...]:
    saida = []
    for p in padroes:
        try:
            saida.append(re.compile(p, re.IGNORECASE))
        except re.error:
            continue
    return tuple(saida)


def _lista(secao: dict[str, Any], chave: str) -> list[str]:
    valor = secao.get(chave)
    return [str(v) for v in valor if isinstance(v, str) and v] if isinstance(valor, list) else []


def ler_data(texto: str, secao: dict[str, Any] | None = None) -> date | None:
    """A data de publicação escrita no texto, pelo primeiro formato do YAML que casar."""
    secao = _secao() if secao is None else secao
    meses = {str(k).lower(): int(v) for k, v in (secao.get("meses") or {}).items()}
    try:
        mes_padrao = int(secao.get("mes_quando_so_ano"))
    except (TypeError, ValueError):
        return None
    limpo = _URL_RE.sub(" ", texto or "")
    for padrao in _compilar(tuple(_lista(secao, "formatos_de_data"))):
        for m in padrao.finditer(limpo):
            grupos = m.groupdict()
            try:
                ano = int(grupos["ano"])
                if grupos.get("mesnome"):
                    mes = meses.get(grupos["mesnome"].lower())
                    if mes is None:
                        continue
                elif grupos.get("mes"):
                    mes = int(grupos["mes"])
                else:
                    mes = mes_padrao
                dia = int(grupos["dia"]) if grupos.get("dia") else 1
                return date(ano, mes, dia)
            except (KeyError, TypeError, ValueError):
                continue
    return None


def idade_em_meses(publicada: date, referencia: date) -> int:
    """Meses completos entre a publicação e a referência (negativo vira zero)."""
    meses = (referencia.year - publicada.year) * 12 + (referencia.month - publicada.month)
    if referencia.day < publicada.day:
        meses -= 1
    return max(0, meses)


def _eh_origem(texto: str, secao: dict[str, Any]) -> bool:
    baixo = texto.lower()
    return any(m.lower() in baixo for m in _lista(secao, "marcadores_de_origem"))


def fontes_do_texto(texto: str, secao: dict[str, Any] | None = None) -> list[Fonte]:
    """Cada linha de cada bloco `## Fontes` do texto, com data e marca de origem."""
    from src.parsers.markdown_parser import extrair_fontes

    secao = _secao() if secao is None else secao
    saida: list[Fonte] = []
    resto = texto or ""
    while True:
        novo, linhas = extrair_fontes(resto)
        if not linhas:
            break
        for linha in linhas:
            url = _URL_RE.search(linha)
            saida.append(
                Fonte(
                    linha,
                    ler_data(linha, secao),
                    _eh_origem(linha, secao),
                    url.group(0) if url else "",
                )
            )
        if novo == resto:
            break
        resto = novo
    return saida


def linhas_da_proveniencia(tabela: str) -> list[dict[str, str]]:
    """Linhas preenchidas da tabela de proveniência, como dicionário por coluna."""
    saida: list[dict[str, str]] = []
    cabecalho: list[str] | None = None
    for linha in (tabela or "").splitlines():
        s = linha.strip()
        if not s.startswith("|"):
            cabecalho = None
            continue
        celulas = [c.strip() for c in s.strip("|").split("|")]
        if cabecalho is None:
            cabecalho = [c.lower() for c in celulas]
            continue
        if all(re.fullmatch(r":?-+:?", c) for c in celulas if c):
            continue
        if "frase da aula" not in cabecalho:
            continue
        saida.append(dict(zip(cabecalho, celulas, strict=False)))
    return saida


def _estado_atual(frase: str, secao: dict[str, Any]) -> bool:
    baixo = f" {frase.lower()} "
    return any(
        re.search(r"(?<![\wà-ú])" + re.escape(m.lower()) + r"(?![\wà-ú])", baixo)
        for m in _lista(secao, "marcadores_de_estado_atual")
    )


def medir(
    texto: str,
    referencia: date,
    janela_meses: int | None,
    tabela_proveniencia: str | None = None,
) -> MedidaFontes:
    """Fontes do texto e da tabela, quantas recentes e as alegações de estado atual."""
    secao = _secao()
    medida = MedidaFontes(fontes=fontes_do_texto(texto, secao))
    frases_datadas: list[tuple[str, date]] = []
    vistas = {f.url for f in medida.fontes if f.url}
    for linha in linhas_da_proveniencia(tabela_proveniencia or ""):
        url = linha.get("url primária", "")
        publicada = ler_data(linha.get("data de publicação", ""), secao)
        if url.startswith("http") and url not in vistas:
            vistas.add(url)
            medida.fontes.append(
                Fonte(url, publicada, _eh_origem(linha.get("frase da aula", ""), secao), url)
            )
        if publicada:
            frases_datadas.append((linha.get("frase da aula", ""), publicada))
    rx = secao.get("atribuicao_no_corpo")
    if isinstance(rx, str) and rx:
        try:
            atribuicao = re.compile(rx)
        except re.error:
            atribuicao = None
        if atribuicao:
            from src.validators.blocos_de_aula import sem_rodape_de_fontes

            corpo = sem_rodape_de_fontes(texto or "")
            for frase in _FIM_DE_FRASE_RE.split(corpo):
                for m in atribuicao.finditer(frase):
                    publicada = ler_data(m.group(2), secao)
                    if publicada:
                        frases_datadas.append((" ".join(frase.split()), publicada))
    for fonte in medida.fontes:
        if fonte.origem:
            continue
        medida.contadas += 1
        if (
            fonte.data
            and janela_meses is not None
            and idade_em_meses(fonte.data, referencia) <= janela_meses
        ):
            medida.recentes += 1
    for frase, publicada in frases_datadas:
        if _estado_atual(frase, secao):
            medida.estado_atual_antigo.append((frase, idade_em_meses(publicada, referencia)))
    return medida


def data_de_referencia(config: Any, padrao: date) -> date:
    """A data declarada na configuração; ilegível ou ausente, a que o chamador injeta."""
    bruto = getattr(config, "data_de_referencia", None)
    if bruto:
        try:
            return date.fromisoformat(str(bruto))
        except ValueError:
            pass
    return padrao


def check_fontes_recentes(
    texto: str,
    config: Any,
    referencia: date,
    tabela_proveniencia: str | None = None,
) -> list[AchadoFonte]:
    """Confere data, recência e estado atual das fontes. Sem a regra ligada, vazio.

    `referencia` é obrigatória: o validador nunca lê o relógio.
    """
    secao = _secao()
    if config is None or not getattr(config, "enabled", False) or not secao:
        return []
    nivel = "error" if getattr(config, "severidade", "aviso") == "erro" else "warning"
    janela = getattr(config, "janela_meses", None)
    m = medir(texto or "", referencia, janela, tabela_proveniencia)
    achados: list[AchadoFonte] = []
    sem_data = [f.texto for f in m.fontes if f.data is None]
    for texto_fonte in sem_data:
        achados.append(
            AchadoFonte(
                "fonte-sem-data",
                f'Fonte sem data de publicação: "{texto_fonte[:90]}". Registre dia, mês e ano (ou '
                f"mês e ano); sem data, ela conta como não recente.",
                nivel,
            )
        )
    parcela_min = getattr(config, "parcela_min_recente", None)
    if parcela_min is not None and janela is not None and m.contadas and m.parcela < parcela_min:
        achados.append(
            AchadoFonte(
                "fontes-pouco-recentes",
                f"{m.recentes} de {m.contadas} fontes têm até {janela} meses em "
                f"{referencia.strftime('%d/%m/%Y')} ({m.parcela:.0%}); o mínimo é {parcela_min:.0%}. "
                f"Procure a edição mais recente da fonte; a fonte antiga fica só como origem do "
                f"conceito, dita como tal.",
                nivel,
            )
        )
    teto = getattr(config, "estado_atual_max_meses", None)
    if teto is not None:
        for frase, idade in m.estado_atual_antigo:
            if idade > teto:
                achados.append(
                    AchadoFonte(
                        "estado-atual-com-fonte-antiga",
                        f'"{frase[:120]}" afirma o estado atual com fonte de {idade} meses; o '
                        f"teto é {teto}. Troque pela fonte mais recente ou date a afirmação no "
                        f"passado.",
                        nivel,
                    )
                )
    return achados


def instrucao_para_prompt(config: Any, referencia: date, chave: str = "instrucao_prompt") -> str:
    """Bloco `{bloco_fontes_recentes}` (ou o da pesquisa). Vazio sem a regra ligada."""
    if config is None or not getattr(config, "enabled", False):
        return ""
    modelo = _secao().get(chave)
    janela = getattr(config, "janela_meses", None)
    if not isinstance(modelo, str) or not modelo.strip() or janela is None:
        return ""
    parcela = getattr(config, "parcela_min_recente", None)
    teto = getattr(config, "estado_atual_max_meses", None)
    return (
        modelo.strip()
        .replace("{janela}", str(janela))
        .replace("{parcela}", f"{parcela:.0%}" if parcela is not None else "a maior parte")
        .replace("{estado_atual}", str(teto) if teto is not None else str(janela))
        .replace("{data_referencia}", referencia.strftime("%d/%m/%Y"))
    )
