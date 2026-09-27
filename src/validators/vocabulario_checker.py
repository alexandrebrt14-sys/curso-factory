"""Palavras de uso exagerado por aula (pedido do dono, 27/09/2026).

O dono pediu, como regra permanente, menos repetição de quatro palavras que o
time usa entre si e que soam estranhas ao leitor: "travar", "canônico",
"régua" e "honesto", com as variações de cada uma. O limite vale por aula, em
toda superfície de leitura (título, subtítulo, prosa, legenda, célula de
tabela), e a palavra só cabe no sentido literal.

Tudo o que é regra mora em `config/quality_rules.yaml >
validation.palavras_de_uso_exagerado`: as famílias com as formas contadas, as
trocas sugeridas, o limite por aula, o excesso que vira aviso e o excesso que
vira erro, e o texto da instrução que entra nos prompts. Este módulo não traz
lista nem número próprio. Sem a seção, ou com `enabled: false`, nada é cobrado
e nenhuma instrução entra no prompt, que é o comportamento anterior a 27/09.

Fica fora da contagem o que não é leitura: bloco de código, código inline,
nome de arquivo, chave de configuração, destino de link e menção entre aspas
(a aula que ensina a trocar "régua" por "critério" precisa poder citar a
palavra). A máscara está em `src/validators/mascaras.py`.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from functools import lru_cache
from typing import Any

from src.validators.mascaras import texto_de_leitura
from src.validators.rules_loader import validation_section

SECAO = "palavras_de_uso_exagerado"


@dataclass(frozen=True)
class Familia:
    """Uma família de palavras contadas juntas."""

    nome: str
    rotulo: str
    formas: tuple[str, ...]
    trocas: tuple[str, ...]


@dataclass
class ConfigVocabulario:
    """A seção do YAML já validada. `None` quando ausente ou desligada."""

    limite_por_aula: int
    excesso_para_aviso: int
    excesso_para_erro: int
    familias: tuple[Familia, ...]
    instrucao_prompt: str = ""


@dataclass
class AchadoVocabulario:
    regra: str
    mensagem: str
    tipo: str = "warning"


@dataclass
class ResultadoVocabulario:
    contagens: dict[str, int] = field(default_factory=dict)
    achados: list[AchadoVocabulario] = field(default_factory=list)


def _inteiro(valor: Any) -> int | None:
    try:
        convertido = int(valor)
    except (TypeError, ValueError):
        return None
    return convertido if convertido >= 0 else None


def _textos(bruto: Any) -> tuple[str, ...]:
    if not isinstance(bruto, list):
        return ()
    return tuple(s.strip() for s in bruto if isinstance(s, str) and s.strip())


def carregar_config() -> ConfigVocabulario | None:
    """Lê a seção do YAML. Devolve `None` se faltar peça obrigatória.

    Obrigatórios: `limite_por_aula`, `excesso_para_aviso`, `excesso_para_erro`
    e ao menos uma família com formas. Faltando qualquer um, a regra não é
    cobrada: configuração pela metade não vira número inventado em código.
    """
    secao = validation_section(SECAO)
    if not secao or not bool(secao.get("enabled", True)):
        return None
    limite = _inteiro(secao.get("limite_por_aula"))
    aviso = _inteiro(secao.get("excesso_para_aviso"))
    erro = _inteiro(secao.get("excesso_para_erro"))
    if limite is None or aviso is None or erro is None:
        return None
    familias: list[Familia] = []
    brutas = secao.get("familias")
    if isinstance(brutas, dict):
        for nome, corpo in brutas.items():
            if not isinstance(corpo, dict):
                continue
            formas = _textos(corpo.get("formas"))
            if not formas:
                continue
            rotulo = str(corpo.get("rotulo") or ", ".join(formas[:3]))
            familias.append(Familia(str(nome), rotulo, formas, _textos(corpo.get("trocas"))))
    if not familias:
        return None
    instrucao = secao.get("instrucao_prompt")
    return ConfigVocabulario(
        limite_por_aula=limite,
        excesso_para_aviso=max(1, aviso),
        excesso_para_erro=max(1, erro),
        familias=tuple(familias),
        instrucao_prompt=instrucao.strip() if isinstance(instrucao, str) else "",
    )


@lru_cache(maxsize=32)
def _padrao(formas: tuple[str, ...]) -> re.Pattern[str]:
    """Uma expressão por família, compilada uma vez; a forma mais longa vence."""
    ordenadas = sorted(formas, key=len, reverse=True)
    corpo = "|".join(re.escape(f) for f in ordenadas)
    return re.compile(r"(?<!\w)(?:" + corpo + r")(?!\w)", re.IGNORECASE)


def contar(texto: str, config: ConfigVocabulario) -> dict[str, int]:
    """Ocorrências por família no texto de leitura da aula."""
    leitura = texto_de_leitura(texto or "")
    return {f.nome: len(_padrao(f.formas).findall(leitura)) for f in config.familias}


def check_vocabulario(texto: str, config: ConfigVocabulario | None = None) -> ResultadoVocabulario:
    """Mede UMA aula. Sem configuração, devolve resultado vazio."""
    config = config if config is not None else carregar_config()
    resultado = ResultadoVocabulario()
    if config is None or not texto or not texto.strip():
        return resultado
    resultado.contagens = contar(texto, config)
    for familia in config.familias:
        n = resultado.contagens.get(familia.nome, 0)
        excesso = n - config.limite_por_aula
        if excesso < config.excesso_para_aviso:
            continue
        tipo = "error" if excesso >= config.excesso_para_erro else "warning"
        trocas = ", ".join(familia.trocas) if familia.trocas else "diga o fato sem a palavra"
        resultado.achados.append(
            AchadoVocabulario(
                regra=f"uso-exagerado:{familia.nome}",
                mensagem=f"'{familia.rotulo}' aparece {n} vez(es) na aula; o limite é "
                f"{config.limite_por_aula}, só no sentido literal. Troque pelo sentido: {trocas}.",
                tipo=tipo,
            )
        )
    return resultado


def instrucao_para_prompt(config: ConfigVocabulario | None = None) -> str:
    """Bloco de instrução para `draft.md` e `review.md`, montado do YAML.

    O texto vem de `instrucao_prompt`, com `{limite}` e `{familias}` trocados
    pelos valores da configuração. Sem configuração ou sem texto, devolve
    vazio e o prompt segue como antes.
    """
    config = config if config is not None else carregar_config()
    if config is None or not config.instrucao_prompt:
        return ""
    linhas = [
        f"- {f.rotulo}: {', '.join(f.trocas)}" if f.trocas else f"- {f.rotulo}"
        for f in config.familias
    ]
    return config.instrucao_prompt.replace("{limite}", str(config.limite_por_aula)).replace(
        "{familias}", "\n".join(linhas)
    )
