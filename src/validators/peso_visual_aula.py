"""Peso visual por aula, declarado pelo cliente ou pelo curso (27/09/2026).

O padrão da casa é TETO de apoios visuais por aula (`tetos.D.figuras_max` do
espelho `config/lexicos.json`), medido pelo `content_checker` como aviso. O dono
pediu, para um curso, o contrário: de cinco a sete peças por aula, com três
tipos diferentes, e nenhuma sequência longa de parágrafos sem peça. Em vez de
mexer no espelho (que é gerado pela fonte de estilo e vale para todo mundo), o
cliente ou o curso declaram o bloco `visual` e este módulo mede a aula contra
ele. Sem bloco declarado, nada aqui roda e vale o teto do espelho, como antes.

As peças são contadas como o gerador vai emiti-las: o Markdown da aula passa
pelo mesmo `parse_module_to_sections` do pipeline, e conta como peça o bloco
cujo tipo está em `VISUAL_SECTION_TYPES` (`src/models.py`) ou em
`validation.visual_density.visual_block_types` do YAML. Do Markdown o parser
promove três tipos (tabela vira `dataTable`, lista de procedimento vira
`stepGuide`, imagem com legenda vira `figure`), então um piso de tipos acima de
três só se cumpre com autoria explícita ou na montagem da landing.

Severidades: abaixo do piso de peças, erro (o dono pediu que a aula reprove);
acima do teto, abaixo do piso de tipos e sequência longa de parágrafos, aviso.
O texto da instrução do prompt vem de
`config/quality_rules.yaml > validation.peso_visual.instrucao_prompt`.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any

from src.validators.rules_loader import rules_list, validation_section

_H1_RE = re.compile(r"^#\s+(?!#).*$", re.MULTILINE)
_HEADING_RE = re.compile(r"^\s{0,3}#{1,6}\s")


@dataclass
class MedidaVisual:
    pecas: int = 0
    tipos: set[str] = field(default_factory=set)
    maior_sequencia_de_paragrafos: int = 0


@dataclass
class AchadoVisual:
    regra: str
    mensagem: str
    tipo: str = "warning"


def _declarado(config: Any) -> bool:
    return bool(config is not None and getattr(config, "declarado", False))


def _tipos_visuais() -> set[str]:
    from src.models import VISUAL_SECTION_TYPES

    return {t.value for t in VISUAL_SECTION_TYPES} | set(
        rules_list("visual_density", "visual_block_types")
    )


def _paragrafos(valor: str) -> int:
    return sum(
        1
        for bloco in re.split(r"\n\s*\n", valor or "")
        if bloco.strip() and not _HEADING_RE.match(bloco.strip())
    )


def medir(texto: str) -> MedidaVisual:
    """Conta peças, tipos e a maior sequência de parágrafos sem peça na aula."""
    from src.models import SectionType
    from src.parsers.markdown_parser import extrair_subtitulo, parse_module_to_sections

    corpo = _H1_RE.sub("", texto or "", count=1).strip()
    _, corpo = extrair_subtitulo(corpo)
    visuais = _tipos_visuais()
    medida = MedidaVisual()
    corrente = 0
    for secao in parse_module_to_sections(corpo):
        tipo = secao.type.value
        if tipo in visuais:
            medida.pecas += 1
            medida.tipos.add(tipo)
            corrente = 0
        elif secao.type is SectionType.TEXT:
            corrente += _paragrafos(secao.value)
            medida.maior_sequencia_de_paragrafos = max(
                medida.maior_sequencia_de_paragrafos, corrente
            )
    return medida


def check_peso_visual_aula(texto: str, config: Any) -> list[AchadoVisual]:
    """Mede UMA aula contra o bloco `visual` declarado. Sem declaração, vazio."""
    if not _declarado(config) or not texto or not texto.strip():
        return []
    m = medir(texto)
    achados: list[AchadoVisual] = []
    minimo = config.min_por_aula
    maximo = config.max_por_aula
    tipos = config.min_tipos_por_aula
    seguidos = config.max_paragrafos_sem_peca
    if minimo is not None and m.pecas < minimo:
        achados.append(
            AchadoVisual(
                "visual-piso",
                f"{m.pecas} peça(s) visual(is) na aula; este curso pede ao menos {minimo}. "
                f"Cada peça carrega informação própria: comparação vira tabela, processo vira "
                f"passo a passo, conceito abstrato vira figura com legenda que afirma um fato.",
                "error",
            )
        )
    if maximo is not None and m.pecas > maximo:
        achados.append(
            AchadoVisual(
                "visual-teto",
                f"{m.pecas} peças visuais na aula, acima do teto de {maximo} deste curso; acima "
                f"dele a peça passa a competir com a leitura.",
            )
        )
    if tipos is not None and len(m.tipos) < tipos:
        achados.append(
            AchadoVisual(
                "visual-tipos",
                f"{len(m.tipos)} tipo(s) de peça na aula ({', '.join(sorted(m.tipos)) or 'nenhum'}); "
                f"este curso pede {tipos} tipos diferentes.",
            )
        )
    if seguidos is not None and m.maior_sequencia_de_paragrafos > seguidos:
        achados.append(
            AchadoVisual(
                "visual-ritmo",
                f"{m.maior_sequencia_de_paragrafos} parágrafos seguidos sem peça visual; este "
                f"curso pede uma peça a cada {seguidos} parágrafos, no máximo.",
            )
        )
    return achados


def instrucao_para_prompt(config: Any) -> str:
    """Bloco `{bloco_peso_visual}` do `draft.md`. Vazio sem declaração."""
    if not _declarado(config):
        return ""
    texto = validation_section("peso_visual").get("instrucao_prompt")
    if not isinstance(texto, str) or not texto.strip():
        return ""

    def _valor(v: int | None) -> str:
        return "sem limite" if v is None else str(v)

    return (
        texto.strip()
        .replace("{min}", _valor(config.min_por_aula))
        .replace("{max}", _valor(config.max_por_aula))
        .replace("{tipos}", _valor(config.min_tipos_por_aula))
        .replace("{paragrafos}", _valor(config.max_paragrafos_sem_peca))
    )
