"""Cobrança da camada `visual_density` de config/quality_rules.yaml.

A camada foi instalada em 17/08/2026 e nasceu declarativa: o `rules_loader`
carrega o YAML inteiro, mas nenhum validador lia `validation.visual_density`.
Este módulo fecha a lacuna. Os três números (teto de parágrafo, piso de blocos
visuais e caracteres de prosa por bloco visual) saem do YAML a cada chamada.
Nenhum deles é constante no código, de propósito: constante é exatamente o
defeito que fez `content_quality.max_paragraph_lines` divergir em silêncio da
`MAX_PARAGRAPH_LINES` do `content_checker`.

Por que módulo separado, e não dentro do `content_checker`: o `content_checker`
mede Markdown cru, uma string por módulo. A densidade visual só existe depois
que o Markdown virou lista de `CourseSection`: ela é uma propriedade da
composição de blocos, não do texto. Enfiar a régua lá exigiria reconstruir os
blocos a partir da string, que é a etapa do `markdown_parser`. O tipo de achado
(`ContentError`) e o formato do relatório continuam sendo os da casa, então o
`quality_gate` pluga este checador do mesmo jeito que pluga os outros.

O que NÃO conta como prosa no denominador nem responde pelo teto de parágrafo:

- Bloco de código e bloco de prompt. Código não é parede de texto: ele já tem
  respiro tipográfico próprio, e contá-lo empurraria o autor a quebrar função
  para caber na régua.
- Todo bloco visual, inclusive `figure`. O `value` de uma figura é o SVG ou a
  marcação da imagem, que mediria dezenas de milhares de caracteres de prosa
  inexistente.
- Trecho cercado por crase tripla dentro de um bloco de prosa, pelo mesmo
  motivo do bloco `code`.
- Linha de tabela Markdown dentro de um bloco de prosa. A tabela é trabalho
  visual feito; cobrar os caracteres dela como prosa é cobrar duas vezes pela
  mesma peça. O crédito de bloco visual, porém, só vem com o bloco `dataTable`:
  tabela escrita dentro de um `text` não conta para o piso.
- Parágrafo que é só heading. Título não é paredão.

Lista com marcador CONTA, tanto no denominador quanto no teto: mil e duzentos
caracteres de lista corrida são parede igual.
"""

from __future__ import annotations

import logging
import math
import re
from collections.abc import Iterable
from typing import Any

from src.models import VISUAL_SECTION_TYPES
from src.validators.content_checker import ContentError
from src.validators.rules_loader import validation_section

logger = logging.getLogger(__name__)

#: Categoria usada em todo `ContentError` emitido aqui.
CATEGORIA = "densidade visual"

#: Fallbacks usados só quando a chave existe no YAML mas veio ilegível
#: (texto onde devia haver número). Camada ausente ou desligada NÃO cai
#: aqui: ela sai sem cobrar, com aviso.
FALLBACK_MAX_PARAGRAPH_CHARS = 1200
FALLBACK_MIN_VISUAL_BLOCKS = 3
# Abaixo deste tanto de prosa o módulo não é capítulo e o piso não se aplica.
FALLBACK_MIN_PROSE_FOR_FLOOR = 800
FALLBACK_CHARS_PER_VISUAL_BLOCK = 2500

#: Tipos que nunca entram no denominador de prosa, além dos visuais.
#: A lista viva é `validation.visual_density.non_visual_types`.
FALLBACK_NON_PROSE_TYPES = frozenset({"code", "prompt", "sourceNote"})

_FENCED_CODE_RE = re.compile(r"```[\s\S]*?```")
_TABLE_LINE_RE = re.compile(r"^[ \t]*\|.*$", re.MULTILINE)
_HEADING_ONLY_RE = re.compile(r"^#{1,6}\s+\S")


def _inteiro(valor: Any, fallback: int) -> int:
    """Converte um valor do YAML em inteiro positivo, ou devolve o fallback."""
    try:
        convertido = int(valor)
    except (TypeError, ValueError):
        return fallback
    return convertido if convertido > 0 else fallback


def _tipo_do_bloco(section: Any) -> str:
    """Devolve o tipo do bloco como string, aceitando modelo ou dicionário.

    O gerador entrega `CourseSection`; um curso já publicado chega como JSON
    carregado, com o tipo em texto. Os dois precisam ser medidos pela mesma
    régua.
    """
    bruto = section.get("type") if isinstance(section, dict) else getattr(section, "type", None)
    return getattr(bruto, "value", bruto) if bruto is not None else ""


def _valor_do_bloco(section: Any) -> str:
    """Devolve o `value` do bloco como string, aceitando modelo ou dicionário."""
    bruto = section.get("value") if isinstance(section, dict) else getattr(section, "value", "")
    return bruto if isinstance(bruto, str) else ""


def _tipos_visuais(regras: dict[str, Any]) -> set[str]:
    """Tipos que dão crédito de bloco visual.

    A base é `VISUAL_SECTION_TYPES` de `src/models.py`, que é o que o gerador
    sabe emitir. A ela se soma `visual_density.visual_block_types` do YAML, que
    lista também os tipos que só o motor da landing desenha hoje. A união evita
    duas listas divergindo, que é o defeito que esta rodada está consertando.
    """
    tipos = {t.value for t in VISUAL_SECTION_TYPES}
    do_yaml = regras.get("visual_block_types")
    if isinstance(do_yaml, list):
        tipos |= {t.strip() for t in do_yaml if isinstance(t, str) and t.strip()}
    return tipos


def _tipos_nao_prosa(regras: dict[str, Any]) -> set[str]:
    """Tipos cujo conteúdo fica fora do denominador de prosa."""
    do_yaml = regras.get("non_visual_types")
    if isinstance(do_yaml, list):
        declarados = {t.strip() for t in do_yaml if isinstance(t, str) and t.strip()}
        if declarados:
            return declarados
    return set(FALLBACK_NON_PROSE_TYPES)


def _limpar_prosa(texto: str) -> str:
    """Retira do texto o que não é prosa, preservando as quebras de linha."""
    def _apagar(match: re.Match[str]) -> str:
        return re.sub(r"[^\n]", "", match.group(0))

    limpo = _FENCED_CODE_RE.sub(_apagar, texto)
    return _TABLE_LINE_RE.sub("", limpo)


def _paragrafos(texto: str) -> list[str]:
    """Divide um bloco de prosa em parágrafos pela linha em branco.

    O teto é do parágrafo, não do bloco: um bloco com três parágrafos responde
    por cada um deles isoladamente.
    """
    paragrafos = []
    for bruto in re.split(r"\n[ \t]*\n", _limpar_prosa(texto)):
        limpo = bruto.strip()
        if not limpo or _HEADING_ONLY_RE.match(limpo):
            continue
        paragrafos.append(limpo)
    return paragrafos


def check_visual_density(
    sections: Iterable[Any],
    module_name: str = "",
    curso_novo: bool = True,
) -> list[ContentError]:
    """Cobra a camada `visual_density` sobre os blocos de um módulo.

    Três regras, com os três números lidos de
    `validation.visual_density` em config/quality_rules.yaml:

    1. `max_paragraph_chars`: teto de caracteres por parágrafo de prosa.
       Reprova: paredão é defeito objetivo, o autor vê o número e quebra o
       parágrafo ou promove o trecho a bloco visual.
    2. `min_visual_blocks_per_module`: piso de blocos visuais no módulo.
       Reprova: a contagem é determinística, sem heurística no meio, e um
       módulo sem nenhum alívio visual é exatamente o curso que a doutrina
       proíbe de nascer.
    3. `chars_per_visual_block`: um bloco visual a cada N caracteres de prosa.
       Avisa apenas: o denominador depende do critério de exclusão descrito no
       docstring do módulo, e um módulo denso de propósito, com prosa que não
       se deixa tabular, não deve ser barrado por uma divisão.

    Args:
        sections: blocos do módulo, como `CourseSection` ou dicionários.
        module_name: nome do módulo, que entra em toda mensagem.
        curso_novo: quando `required_for_new_course` é verdadeiro no YAML e
            este parâmetro é falso, os achados saem como aviso em vez de erro.
            É assim que o acervo já publicado não fica refém da régua nova: a
            dívida aparece no relatório, contada e nomeada, sem bloquear
            republicação de curso legado.

    Returns:
        Lista de `ContentError` no formato da casa. Camada ausente, malformada
        ou desligada devolve um único aviso dizendo que nada foi cobrado.
    """
    mod = module_name or "módulo"
    regras = validation_section("visual_density")

    if not regras:
        return [ContentError(
            tipo="warning",
            categoria=CATEGORIA,
            mensagem=(
                f"A camada 'visual_density' não foi encontrada em "
                f"config/quality_rules.yaml: a densidade visual do módulo '{mod}' "
                f"NÃO foi cobrada. Restaure a seção para voltar a medir teto de "
                f"parágrafo, piso de blocos visuais e densidade."
            ),
            modulo=mod,
        )]

    if not bool(regras.get("enabled", True)):
        return [ContentError(
            tipo="warning",
            categoria=CATEGORIA,
            mensagem=(
                f"A camada 'visual_density' está desligada (enabled: false) em "
                f"config/quality_rules.yaml: a densidade visual do módulo '{mod}' "
                f"NÃO foi cobrada."
            ),
            modulo=mod,
        )]

    teto_paragrafo = _inteiro(
        regras.get("max_paragraph_chars"), FALLBACK_MAX_PARAGRAPH_CHARS
    )
    piso_visual = _inteiro(
        regras.get("min_visual_blocks_per_module"), FALLBACK_MIN_VISUAL_BLOCKS
    )
    chars_por_visual = _inteiro(
        regras.get("chars_per_visual_block"), FALLBACK_CHARS_PER_VISUAL_BLOCK
    )

    # Curso legado só é cobrado como aviso quando a régua é declarada
    # obrigatória apenas para curso novo.
    so_para_curso_novo = bool(regras.get("required_for_new_course", True))
    severidade = "warning" if (so_para_curso_novo and not curso_novo) else "error"
    if severidade == "warning":
        logger.info(
            "Módulo '%s' medido como curso legado: achados de densidade visual "
            "saem como aviso (required_for_new_course: true).",
            mod,
        )

    visuais = _tipos_visuais(regras)
    fora_da_prosa = _tipos_nao_prosa(regras) | visuais

    erros: list[ContentError] = []
    blocos_visuais = 0
    chars_prosa = 0
    estouros: list[tuple[int, int, str]] = []  # (posição do bloco, tamanho, trecho)

    for indice, section in enumerate(sections, start=1):
        tipo = _tipo_do_bloco(section)
        if tipo in visuais:
            blocos_visuais += 1
        if tipo in fora_da_prosa:
            continue
        for paragrafo in _paragrafos(_valor_do_bloco(section)):
            chars_prosa += len(paragrafo)
            if len(paragrafo) > teto_paragrafo:
                estouros.append((indice, len(paragrafo), paragrafo[:60].replace("\n", " ")))

    # 1. Teto de parágrafo.
    for indice, tamanho, trecho in estouros:
        erros.append(ContentError(
            tipo=severidade,
            categoria=CATEGORIA,
            mensagem=(
                f"Módulo '{mod}': parágrafo do bloco {indice} com {tamanho} caracteres, "
                f"acima do teto de {teto_paragrafo} (max_paragraph_chars). "
                f"Começa em \"{trecho}...\". Quebre o parágrafo na virada de assunto "
                f"ou promova o trecho a bloco visual: enumeração vira 'stepGuide', "
                f"contraste vira 'comparison', série de números vira 'statGrid'."
            ),
            modulo=mod,
        ))

    # 2. Piso de blocos visuais, só para módulo que é capítulo de verdade.
    #
    # Abaixo de `min_prose_chars_for_floor` o módulo é abertura, encerramento ou
    # trecho de apoio, e cobrar três peças ali produz enfeite em vez de leitura.
    # A densidade da regra 3 continua valendo em qualquer tamanho, e é ela que
    # pega o módulo longo que se escondeu atrás de duas figuras.
    piso_a_partir_de = _inteiro(
        regras.get("min_prose_chars_for_floor"), FALLBACK_MIN_PROSE_FOR_FLOOR
    )
    if chars_prosa >= piso_a_partir_de and blocos_visuais < piso_visual:
        faltam = piso_visual - blocos_visuais
        erros.append(ContentError(
            tipo=severidade,
            categoria=CATEGORIA,
            mensagem=(
                f"Módulo '{mod}': {blocos_visuais} bloco(s) visual(is) para um piso de "
                f"{piso_visual} (min_visual_blocks_per_module). Faltam {faltam}. "
                f"Acrescente 'dataTable', 'comparison', 'statGrid', 'stepGuide', "
                f"'timeline' ou 'figure'. Tabela escrita dentro de um bloco 'text' "
                f"não conta para o piso."
            ),
            modulo=mod,
        ))

    # 3. Densidade: um bloco visual a cada N caracteres de prosa.
    exigidos = math.ceil(chars_prosa / chars_por_visual) if chars_prosa else 0
    if blocos_visuais < exigidos:
        erros.append(ContentError(
            tipo="warning",
            categoria=CATEGORIA,
            mensagem=(
                f"Módulo '{mod}': {chars_prosa} caracteres de prosa para "
                f"{blocos_visuais} bloco(s) visual(is); a régua de um bloco a cada "
                f"{chars_por_visual} caracteres (chars_per_visual_block) pede "
                f"{exigidos}. Acrescente {exigidos - blocos_visuais} bloco(s) visual(is) "
                f"ou reduza a prosa do módulo."
            ),
            modulo=mod,
        ))

    return erros
