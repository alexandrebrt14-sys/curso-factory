"""Abertura direta e sem distração (R1 a R9, 08/09/2026).

Pedido do dono dos repositórios, literal: toda página, artigo, aula ou capítulo
começa com título, subtítulo e parágrafos diretos ao ponto; some o excesso de
botões, os percursos alternativos, o "mockup no seu negócio", o exercício
"faça agora", o card "checkpoint", o marcador "requer verificação" e qualquer
menção à LGPD; fontes verificadas ficam só no rodapé, em corpo pequeno.

As nove regras, numeradas como no mandato e na decisão
`wiki/decisions/abertura-direta-sem-distracao-20260908.md`:

- R1 abertura mínima: H1, subtítulo de uma frase, parágrafos. Nada entre eles.
- R2 sem CTA antes do corpo (cobrado no template, ver `tests/`).
- R3 sem percursos alternativos ("escolha seu caminho", "se você é X", "para quem é").
- R4 uma única descrição por página (cobrado no template).
- R5 sem "mockup no seu negócio" e variantes.
- R6 sem exercício "faça agora" e variantes.
- R7 fontes só no rodapé, curtas, uma por linha.
- R8 sem card "checkpoint" e variantes.
- R9 sem "requer verificação" e sem LGPD no texto de leitura.

Duas superfícies são medidas:

1. **Markdown** da aula ou da trilha (`check_abertura`), chamado por
   `content_checker.check_content` e, por ele, pelo `QualityGate`, pelo
   orquestrador ao fim do pipeline e por `python cli.py validate`.
2. **CourseDefinition** já montado (`check_abertura_definicao`), chamado por
   `TsxGenerator.render_page` antes de escrever o arquivo. Aqui a régua morde a
   publicação: bloco proibido no conteúdo levanta `AberturaError` e o curso
   não vira TSX.

Menção entre aspas não conta para R5, R6 e R8: a aula que ensina a NÃO escrever
"faça agora" precisa poder citar a expressão. R9 vale mesmo entre aspas, porque
a proibição do dono é à menção, e não ao uso.

Léxico em três camadas, somadas: os padrões deste módulo, as famílias do bloco
`aberturaEDistracao` da fonte de estilo (espelho `config/lexicos.json`, fonte
1.6.0 de 08/09/2026, lidas por `lexicos_loader.familias_de_abertura`) e o que
`validation.abertura.termos` do YAML acrescentar. Nada aqui remove termo da
fonte.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from src.validators.lexicos_loader import familias_de_abertura
from src.validators.rules_loader import validation_section

if TYPE_CHECKING:
    from src.models import CourseDefinition


@dataclass
class AchadoAbertura:
    """Um achado do gate de abertura e distração."""

    regra: str  # "R1", "R3", "R5", "R6", "R7", "R8", "R9"
    mensagem: str
    tipo: str = "error"


@dataclass
class ResultadoAbertura:
    achados: list[AchadoAbertura] = field(default_factory=list)

    @property
    def aprovado(self) -> bool:
        return not any(a.tipo == "error" for a in self.achados)


# ─── Padrões ───────────────────────────────────────────────────────────

#: Teto de palavras do subtítulo (uma frase que cabe numa linha de celular).
SUBTITULO_MAX_PALAVRAS = 30

#: Cabeçalho de qualquer nível.
_HEADING_RE = re.compile(r"^\s{0,3}(#{1,6})\s+(.+?)\s*$")
#: Linha que começa com rótulo em negrito (`**Faça agora:**`, `**Fonte:**`).
_ROTULO_NEGRITO_RE = re.compile(r"^\s*\*\*([^*]{2,80})\*\*\s*[:.]?")
#: Blockquote com prefixo (`> CHECKPOINT: ...`).
_QUOTE_ROTULO_RE = re.compile(r"^\s*>\s*([A-ZÀ-Ú][A-ZÀ-Ú \-]{2,30}):")
#: Fim de frase para contar frases do subtítulo.
_FIM_DE_FRASE_RE = re.compile(r"[.!?](?=\s|$)")
#: Trecho entre aspas: menção, não uso.
_MENCAO_RE = re.compile(r"[\"“„”']([^\"“„”'\n]{2,80})[\"“„”']")
#: Linha de fonte solta no corpo da aula.
_LINHA_DE_FONTE_RE = re.compile(r"^\s*\**\s*Fontes?\s*\**\s*:", re.IGNORECASE)
#: Cabeçalho "Fontes" (ou variantes) em qualquer nível.
_H_FONTES_RE = re.compile(
    r"^\s{0,3}#{1,6}\s+(?:Fontes?|Refer[êe]ncias|Sources|Fuentes)\b", re.IGNORECASE
)
#: Fronteira de trilha e de aula, como o orquestrador emite.
_TRILHA_H1_RE = re.compile(r"^#\s+Trilha\s+\d+\s*[:.\-]", re.MULTILINE)
_H1_RE = re.compile(r"^#\s+(?!#)(.+?)\s*$", re.MULTILINE)
#: Marcador de apuração pendente: bastidor que nunca vai ao publicado.
_MARCADOR_PENDENTE_RE = re.compile(
    r"\[\s*(?:FALTA\s+EVID[ÊE]NCIA|PREENCHER-HUMANO|MISSING\s+EVIDENCE|FALTA\s+EVIDENCIA)\s*:",
    re.IGNORECASE,
)

#: Padrões padrão por regra. A seção `validation.abertura` de
#: `config/quality_rules.yaml` pode ACRESCENTAR termos; nunca remover.
_PADROES_PADRAO: dict[str, list[str]] = {
    # R3: percurso alternativo, só em cabeçalho ou rótulo.
    "R3": [
        r"escolha\s+(?:o\s+)?seu\s+caminho",
        r"se\s+voc[êe]\s+[ée]\b.{0,40}\bv[áa]\s+para",
        r"comece\s+por\s+aqui",
        r"para\s+quem\s+[ée]\s+(?:este|esta|o|a)\b",
        r"choose\s+your\s+path",
        r"elige\s+tu\s+camino",
    ],
    # R5: mockup no seu negócio. `mockup`/`maquete` valem em qualquer linha;
    # "no seu negócio" só em cabeçalho ou rótulo (a prosa pode dizer "um dado
    # do próprio negócio").
    "R5_qualquer": [
        r"\bmock-?ups?\b",
        r"\bmaquetes?\b",
        r"\b(?:aplique|simule|monte|fa[çc]a)\s+(?:isso\s+)?no\s+seu\s+neg[óo]cio",
    ],
    "R5_rotulo": [
        r"\bno\s+seu\s+neg[óo]cio\b",
        r"\bin\s+your\s+business\b",
        r"\ben\s+tu\s+negocio\b",
    ],
    # R6: exercício "faça agora" e variantes, em cabeçalho ou rótulo.
    "R6": [
        r"\bfa[çc]a\s+agora\b",
        r"\bexerc[íi]cios?\b",
        r"\bm[ãa]o\s+na\s+massa\b",
        r"\bsua\s+vez\b",
        r"\bpratique\b",
        r"\btarefa\b",
        r"\bdesafio\b",
        r"\bchecklist\s+de\s+a[çc][ãa]o\b",
        r"\batividade\s+pr[áa]tica\b",
        r"\bresultado\s+esperado\b",
        r"\bse\s+travar\b",
        r"\bdo\s+it\s+now\b",
        r"\bexercises?\b",
        r"\bexpected\s+result\b",
        r"\bif\s+stuck\b",
        r"\bhazlo\s+ahora\b",
        r"\bejercicios?\b",
        r"\bresultado\s+esperado\b",
        r"\bsi\s+te\s+trabas\b",
    ],
    # R8: checkpoint e variantes, em cabeçalho, rótulo ou blockquote rotulado.
    "R8": [
        r"\bcheck-?points?\b",
        r"\bponto\s+de\s+verifica[çc][ãa]o\b",
        r"\brecapitulando\b",
        r"\bresumo\s+do\s+cap[íi]tulo\b",
        r"\bvoc[êe]\s+aprendeu\b",
        r"\bquiz(?:zes)?\b",
        r"\bo\s+que\s+voc[êe]\s+(?:vai\s+)?aprend(?:e|eu|er|er[áa])\b",
    ],
    # R9: verificação explícita e LGPD, em qualquer linha, mesmo entre aspas.
    "R9": [
        r"\brequer\s+verifica[çc][ãa]o\b",
        r"\ba\s+verificar\b",
        r"\[\s*verificar\s*\]",
        r"\bdado\s+n[ãa]o\s+confirmado\b",
        r"\bfonte\s+pendente\b",
        r"\bLGPD\b",
        r"\bLei\s+Geral\s+de\s+Prote[çc][ãa]o\s+de\s+Dados\b",
        r"\b13\.709\b",
        r"\bneeds\s+verification\b",
        r"\brequiere\s+verificaci[óo]n\b",
    ],
}


#: Famílias da fonte de estilo (bloco `aberturaEDistracao`, 1.6.0) somadas a
#: cada chave. Lista da fonte é literal; string é expressão regular. As formas
#: "falta evidência" de `verificacaoExplicita` ficam de fora da medição de
#: Markdown, porque o rascunho em revisão tolera o marcador `[FALTA EVIDÊNCIA:`
#: (camada anti-invenção); no publicado ele é barrado por
#: `check_abertura_definicao`.
_FAMILIAS_DA_FONTE: dict[str, tuple[str, ...]] = {
    "R3": ("percursoAlternativo",),
    "R5_qualquer": ("mockup", "noSeuNegocioInstrucao"),
    "R5_rotulo": ("noSeuNegocio",),
    "R6": ("exercicioForte", "exercicioRotulo"),
    "R8": ("checkpointForte", "checkpointRotulo"),
    "R9": ("verificacaoExplicita", "lgpd"),
}
_EXCLUIR_DA_FONTE = ("falta evidência", "falta evidencia")


def _literal(termo: str) -> str:
    return r"(?<!\w)" + re.escape(termo) + r"(?!\w)"


def _termos_da_fonte(chave: str) -> list[str]:
    familias = familias_de_abertura()
    termos: list[str] = []
    for nome in _FAMILIAS_DA_FONTE.get(chave, ()):
        bruto = familias.get(nome)
        if isinstance(bruto, list):
            termos.extend(
                _literal(t.strip())
                for t in bruto
                if isinstance(t, str) and t.strip() and t.strip().lower() not in _EXCLUIR_DA_FONTE
            )
        elif isinstance(bruto, str) and bruto.strip():
            termos.append(bruto)
    return termos


def _subtitulo_max_palavras() -> int:
    """Teto do subtítulo: a fonte (`subtituloMaxPalavras`) vence o padrão do módulo."""
    valor = familias_de_abertura().get("subtituloMaxPalavras")
    try:
        return int(valor) if valor else SUBTITULO_MAX_PALAVRAS
    except (TypeError, ValueError):
        return SUBTITULO_MAX_PALAVRAS


def _padroes(chave: str) -> list[re.Pattern[str]]:
    """Padrões da regra: os do módulo, mais a fonte de estilo, mais o YAML."""
    termos = list(_PADROES_PADRAO.get(chave, [])) + _termos_da_fonte(chave)
    try:
        secao = validation_section("abertura") or {}
        extra = secao.get("termos", {}) if isinstance(secao, dict) else {}
        if isinstance(extra, dict):
            for t in extra.get(chave, []) or []:
                if isinstance(t, str) and t.strip():
                    termos.append(re.escape(t.strip()) if not t.startswith("re:") else t[3:])
    except Exception:  # noqa: BLE001 - configuração ausente nunca derruba o gate
        pass
    compilados: list[re.Pattern[str]] = []
    for t in termos:
        try:
            compilados.append(re.compile(t, re.IGNORECASE | re.MULTILINE))
        except re.error:
            continue
    return compilados


def _ligado() -> bool:
    try:
        secao = validation_section("abertura") or {}
    except Exception:  # noqa: BLE001
        return True
    return bool(secao.get("enabled", True)) if isinstance(secao, dict) else True


def _sem_mencoes(texto: str) -> str:
    return _MENCAO_RE.sub(" ", texto)


def _sem_codigo(texto: str) -> str:
    """Apaga blocos de código: não são texto de leitura."""
    return re.sub(r"```[\s\S]*?```", "", texto)


def _eh_paragrafo_liso(linha: str) -> bool:
    """Linha de prosa: nem cabeçalho, nem lista, nem tabela, nem citação, nem imagem."""
    s = linha.strip()
    if not s:
        return False
    if s.startswith(("#", "-", "*", "+", "|", ">", "!", "<", "```", "[", "---")):
        return False
    if re.match(r"^\d{1,2}[.)]\s", s):
        return False
    return True


def _blocos(texto: str) -> list[str]:
    """Divide em blocos separados por linha em branco, sem os vazios."""
    return [b.strip() for b in re.split(r"\n\s*\n", texto) if b.strip()]


# ─── R1: abertura mínima ─────────────────────────────────────────────────


def _check_r1(texto: str) -> list[AchadoAbertura]:
    """H1, depois subtítulo de uma frase, depois parágrafo. Nada no meio."""
    achados: list[AchadoAbertura] = []
    m = _H1_RE.search(texto)
    if not m:
        return achados
    corpo = texto[m.end() :]
    blocos = _blocos(_sem_codigo(corpo))
    if len(blocos) < 2:
        achados.append(
            AchadoAbertura(
                "R1",
                "Abertura incompleta: depois do H1 precisam vir o subtítulo (uma frase) "
                "e ao menos um parágrafo antes de qualquer seção.",
            )
        )
        return achados

    subtitulo = blocos[0]
    linhas_sub = subtitulo.splitlines()
    if not all(_eh_paragrafo_liso(ln) for ln in linhas_sub) or len(linhas_sub) > 1:
        achados.append(
            AchadoAbertura(
                "R1",
                f"O primeiro bloco depois do H1 precisa ser o subtítulo em uma frase, "
                f"em linha própria; veio: '{subtitulo[:60]}'. Sem cabeçalho, lista, tabela, "
                f"citação, imagem ou card antes do subtítulo.",
            )
        )
        return achados
    frases = len(_FIM_DE_FRASE_RE.findall(subtitulo)) or 1
    palavras = len(subtitulo.split())
    teto = _subtitulo_max_palavras()
    if frases > 1 or palavras > teto:
        achados.append(
            AchadoAbertura(
                "R1",
                f"Subtítulo com {frases} frase(s) e {palavras} palavra(s); o subtítulo é UMA "
                f"frase de até {teto} palavras: '{subtitulo[:60]}'.",
            )
        )

    primeiro = blocos[1]
    if not all(_eh_paragrafo_liso(ln) for ln in primeiro.splitlines()):
        achados.append(
            AchadoAbertura(
                "R1",
                f"O primeiro elemento depois do subtítulo precisa ser um parágrafo; veio: "
                f"'{primeiro.splitlines()[0][:60]}'. Cabeçalho, lista, tabela, card, TOC, "
                f"'o que você vai aprender' e 'para quem é' não abrem a aula.",
            )
        )
    return achados


# ─── R3, R5, R6, R8: blocos de distração ─────────────────────────────────


def _linhas_rotuladas(texto: str) -> list[str]:
    """Cabeçalhos, rótulos em negrito no começo da linha e blockquotes rotulados."""
    rotulos: list[str] = []
    for linha in _sem_codigo(texto).splitlines():
        mh = _HEADING_RE.match(linha)
        if mh:
            rotulos.append(mh.group(2))
            continue
        mb = _ROTULO_NEGRITO_RE.match(linha)
        if mb:
            rotulos.append(mb.group(1))
            continue
        mq = _QUOTE_ROTULO_RE.match(linha)
        if mq:
            rotulos.append(mq.group(1))
    return rotulos


def _check_rotulos(texto: str, regra: str, chave: str, explicacao: str) -> list[AchadoAbertura]:
    achados: list[AchadoAbertura] = []
    padroes = _padroes(chave)
    vistos: set[str] = set()
    for rotulo in _linhas_rotuladas(texto):
        limpo = _sem_mencoes(rotulo)
        for p in padroes:
            m = p.search(limpo)
            if m and m.group(0).lower() not in vistos:
                vistos.add(m.group(0).lower())
                achados.append(
                    AchadoAbertura(
                        regra,
                        f"{explicacao}: '{rotulo.strip()[:70]}'.",
                    )
                )
                break
    return achados


def _check_qualquer_linha(
    texto: str, regra: str, chave: str, explicacao: str, respeita_mencao: bool = True
) -> list[AchadoAbertura]:
    achados: list[AchadoAbertura] = []
    corpo = _sem_codigo(texto)
    if respeita_mencao:
        corpo = _sem_mencoes(corpo)
    vistos: set[str] = set()
    for p in _padroes(chave):
        for m in p.finditer(corpo):
            chave_vista = m.group(0).lower()
            if chave_vista in vistos:
                continue
            vistos.add(chave_vista)
            achados.append(AchadoAbertura(regra, f"{explicacao}: '{m.group(0)}'."))
            break
    return achados


def _check_r3(texto: str) -> list[AchadoAbertura]:
    return _check_rotulos(
        texto,
        "R3",
        "R3",
        "Percurso alternativo no topo ou em seção (um único caminho linear)",
    )


def _check_r5(texto: str) -> list[AchadoAbertura]:
    achados = _check_qualquer_linha(
        texto,
        "R5",
        "R5_qualquer",
        "Bloco 'mockup no seu negócio' ou variante",
    )
    achados += _check_rotulos(
        texto,
        "R5",
        "R5_rotulo",
        "Seção 'no seu negócio' (remova o bloco e a instrução)",
    )
    return achados


def _check_r6(texto: str) -> list[AchadoAbertura]:
    return _check_rotulos(
        texto,
        "R6",
        "R6",
        "Exercício 'faça agora' ou variante (conteúdo é leitura, não workbook)",
    )


def _check_r8(texto: str) -> list[AchadoAbertura]:
    return _check_rotulos(
        texto,
        "R8",
        "R8",
        "Card 'checkpoint' ou variante",
    )


def _check_r9(texto: str) -> list[AchadoAbertura]:
    """Vale mesmo entre aspas: a proibição do dono é à menção."""
    return _check_qualquer_linha(
        texto,
        "R9",
        "R9",
        "Marcador de verificação ou menção à LGPD visível ao leitor (verificação é bastidor)",
        respeita_mencao=False,
    )


# ─── R7: fontes só no rodapé ────────────────────────────────────────────

FONTE_MAX_PALAVRAS = 25


def _check_r7_aula(texto: str) -> list[AchadoAbertura]:
    """Na aula, nenhuma linha de fonte e nenhum cabeçalho 'Fontes'."""
    achados: list[AchadoAbertura] = []
    for linha in _sem_codigo(texto).splitlines():
        if _H_FONTES_RE.match(linha) or _LINHA_DE_FONTE_RE.match(linha):
            achados.append(
                AchadoAbertura(
                    "R7",
                    f"Fonte no meio da aula: '{linha.strip()[:70]}'. A fonte vai para o bloco "
                    f"'Fontes' do rodapé da trilha, em uma linha curta.",
                )
            )
            break
    return achados


def _check_r7_trilha(texto: str) -> list[AchadoAbertura]:
    """Na trilha, 'Fontes' é o ÚLTIMO H2 e cada fonte é uma linha curta."""
    achados: list[AchadoAbertura] = []
    corpo = _sem_codigo(texto)
    h2s = [(m.start(), m.group(2)) for m in re.finditer(r"^(##)\s+(.+?)\s*$", corpo, re.MULTILINE)]
    idx_fontes = [
        i
        for i, (_, t) in enumerate(h2s)
        if re.match(r"(?:Fontes?|Sources|Fuentes|Refer[êe]ncias)\b", t, re.I)
    ]
    if not idx_fontes:
        return achados
    if idx_fontes[-1] != len(h2s) - 1 or len(idx_fontes) > 1:
        achados.append(
            AchadoAbertura(
                "R7",
                "O bloco 'Fontes' precisa ser o último H2 da trilha, e único.",
            )
        )
    inicio = h2s[idx_fontes[-1]][0]
    bloco = corpo[inicio:].splitlines()[1:]
    for linha in bloco:
        s = linha.strip().lstrip("-*0123456789.) ").strip()
        if not s:
            continue
        if s.startswith(">") or s.startswith("|"):
            achados.append(
                AchadoAbertura(
                    "R7",
                    "Fonte em card, citação ou tabela; no rodapé a fonte é texto e link, uma linha.",
                )
            )
            break
        if len(s.split()) > FONTE_MAX_PALAVRAS:
            achados.append(
                AchadoAbertura(
                    "R7",
                    f"Fonte com comentário longo ({len(s.split())} palavras): '{s[:60]}'. "
                    f"Nome da fonte, título e data, no máximo {FONTE_MAX_PALAVRAS} palavras.",
                )
            )
            break
    return achados


# ─── Entrada pública: Markdown ──────────────────────────────────────────


def check_abertura(texto: str, unidade: str = "aula") -> ResultadoAbertura:
    """Mede uma unidade de Markdown contra R1, R3, R5, R6, R7, R8 e R9.

    Args:
        texto: o Markdown da aula, da trilha ou do texto solto.
        unidade: `"aula"` (padrão), `"trilha"` ou `"texto"`. A trilha não tem
            abertura (é fechamento de módulo), então R1 não vale nela e R7 é
            medido pela posição do bloco 'Fontes'. Texto sem H1 não recebe R1.
    """
    resultado = ResultadoAbertura()
    if not _ligado() or not texto or not texto.strip():
        return resultado
    texto = texto.replace("\r\n", "\n")
    eh_trilha = unidade == "trilha" or bool(_TRILHA_H1_RE.match(texto.lstrip()))

    if not eh_trilha:
        resultado.achados += _check_r1(texto)
        resultado.achados += _check_r7_aula(texto)
    else:
        resultado.achados += _check_r7_trilha(texto)
    resultado.achados += _check_r3(texto)
    resultado.achados += _check_r5(texto)
    resultado.achados += _check_r6(texto)
    resultado.achados += _check_r8(texto)
    resultado.achados += _check_r9(texto)
    return resultado


# ─── Entrada pública: CourseDefinition (publicação) ─────────────────────


class AberturaError(ValueError):
    """O curso montado carrega bloco proibido ou abertura fora da ordem.

    Levantado por `TsxGenerator.render_page` antes de escrever o arquivo, no
    mesmo lugar em que a régua de peso visual morde: curso com card checkpoint,
    exercício "faça agora", "requer verificação" ou LGPD não vira TSX.
    """

    def __init__(self, achados: list[str]) -> None:
        self.achados = achados
        corpo = "\n".join(f"  - {a}" for a in achados)
        super().__init__(
            f"Abertura e distração reprovadas em {len(achados)} ponto(s) (R1 a R9):\n"
            f"{corpo}\n"
            "Regras: wiki/decisions/abertura-direta-sem-distracao-20260908.md"
        )


def _texto_da_secao(secao) -> str:
    """Tudo que a seção mostra ao leitor: value, label e os campos de texto do payload."""
    partes: list[str] = [secao.value or "", secao.label or ""]

    def _coleta(obj) -> None:
        if isinstance(obj, str):
            partes.append(obj)
        elif isinstance(obj, dict):
            for v in obj.values():
                _coleta(v)
        elif isinstance(obj, (list, tuple)):
            for v in obj:
                _coleta(v)

    _coleta(secao.data)
    return "\n".join(p for p in partes if p)


def check_abertura_definicao(course: CourseDefinition) -> list[str]:
    """Mede o curso montado. Devolve mensagens; vazio é aprovado.

    O que se cobra aqui, além dos padrões R5/R6/R8/R9 sobre o texto de cada
    seção: nenhum marcador de apuração pendente (`[FALTA EVIDÊNCIA:`) chega ao
    publicado; nenhuma seção do tipo checkpoint; nenhuma linha "Fonte:" em
    prosa (as fontes são hasteadas para o rodapé pelo gerador); cada módulo tem
    subtítulo (`description`) e abre com prosa (a primeira seção é `text`).
    """
    from src.models import SectionType

    if not _ligado():
        return []
    mensagens: list[str] = []
    for step in course.steps:
        rotulo = step.id
        if not (step.description or "").strip():
            mensagens.append(
                f"{rotulo}: módulo sem subtítulo (description). R1 pede título, subtítulo e parágrafo."
            )
        if step.content and step.content[0].type is not SectionType.TEXT:
            mensagens.append(
                f"{rotulo}: o módulo abre com bloco '{step.content[0].type.value}'. R1: o primeiro "
                f"elemento depois do subtítulo é um parágrafo."
            )
        for i, secao in enumerate(step.content):
            if secao.type.value == "checkpoint":
                mensagens.append(f"{rotulo}[{i}]: bloco checkpoint (R8).")
            texto = _texto_da_secao(secao)
            if not texto.strip():
                continue
            if _MARCADOR_PENDENTE_RE.search(texto):
                mensagens.append(
                    f"{rotulo}[{i}]: marcador de apuração pendente no conteúdo publicado (R9). "
                    f"Verificação é bastidor: resolva ou corte antes de publicar."
                )
            if secao.type is SectionType.TEXT:
                for linha in texto.splitlines():
                    if _LINHA_DE_FONTE_RE.match(linha) or _H_FONTES_RE.match(linha):
                        mensagens.append(
                            f"{rotulo}[{i}]: 'Fonte:' dentro da prosa (R7); a fonte vai ao rodapé."
                        )
                        break
            for achado in (
                _check_r5(texto)
                + _check_r6(texto)
                + _check_r8(texto)
                + _check_r9(texto)
                + _check_r3(texto)
            ):
                mensagens.append(f"{rotulo}[{i}]: [{achado.regra}] {achado.mensagem}")
    for k, fonte in enumerate(course.fontes):
        if len(fonte.split()) > FONTE_MAX_PALAVRAS:
            mensagens.append(
                f"fontes[{k}]: fonte com {len(fonte.split())} palavras; no rodapé a fonte é nome, "
                f"título e data, até {FONTE_MAX_PALAVRAS} palavras (R7)."
            )
        if _check_r9(fonte):
            mensagens.append(f"fontes[{k}]: menção proibida (R9) na fonte.")
    return mensagens


def format_report(resultado: ResultadoAbertura) -> str:
    if not resultado.achados:
        return "Abertura e distração (R1 a R9): todas as verificações passaram."
    linhas = [f"Abertura e distração (R1 a R9): {len(resultado.achados)} achado(s):"]
    for a in resultado.achados:
        linhas.append(f"    [{a.regra}] {a.mensagem}")
    return "\n".join(linhas)
