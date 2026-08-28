"""Parser de Markdown → CourseSections / Módulos.

Fonte única de verdade para parsing editorial usado por:
- `src/generators/schema_builder.py` (pipeline happy-path, Markdown revisto)
- `src/converters/draft_to_course.py` (recovery de drafts órfãos)

Funções públicas:
- `slugify(valor)` → ASCII kebab-case (sem acentos)
- `short_id(valor, max_len=24)` → slug truncado para step_id
- `extract_module_blocks(md)` → lista de (título, conteúdo) por heading
- `parse_module_to_sections(md)` → lista de CourseSection validáveis

## Promoção a bloco visual

O modelo já escreve tabela, lista de passos e imagem em Markdown. Sem promoção,
tudo isso vira bloco `text` e não conta como alívio visual na doutrina
(`docs/DOUTRINA_VISUAL_CURSOS.md`), com os caracteres da tabela ainda pesando no
teto de parágrafo. Este parser promove três construções:

- tabela em Markdown → `dataTable`
- lista numerada de procedimento → `stepGuide` (critério em `_try_step_guide`)
- imagem com legenda → `figure`

Duas regras valem para toda promoção:

1. **Nada se perde.** A promoção troca as linhas originais por um marcador na
   posição exata, então a prosa que vinha antes e a que vinha depois continuam
   como blocos `text`, na ordem.
2. **Falha volta a ser texto.** Se a carga não passar pela validação do
   `CourseSection`, o trecho permanece como `text`. Bloco visual a menos é um
   defeito de cobertura; conteúdo a menos é perda irrecuperável.
"""

from __future__ import annotations

import re
import unicodedata

from pydantic import ValidationError

from src.models import CourseSection, SectionType

# Regex compartilhados
H1_RE = re.compile(r"^#\s+(.+?)\s*$", re.MULTILINE)
H2_RE = re.compile(r"^##\s+(.+?)\s*$", re.MULTILINE)
CODE_FENCE_RE = re.compile(r"```([a-zA-Z0-9_+-]*)\n(.*?)```", re.DOTALL)

# Prefixos de blockquote especiais (DICA/AVISO/CHECKPOINT) para schema_builder
_SPECIAL_QUOTES = {
    "DICA": SectionType.TIP,
    "AVISO": SectionType.WARNING,
    "CHECKPOINT": SectionType.CHECKPOINT,
}

# ─── Promoção a bloco visual: padrões ────────────────────────────────

#: Marcador que segura a posição de um bloco visual no texto.
_VISUAL_PLACEHOLDER = "[VISUAL_BLOCK_{}]"
#: Reconhece marcador de código ou de bloco visual dentro de um chunk.
_ANY_PLACEHOLDER_RE = re.compile(r"(\[(?:CODE|VISUAL)_BLOCK_\d+\])")

#: Célula da linha de separação de tabela: `---`, `:---`, `---:`, `:---:`.
_TABLE_SEP_CELL_RE = re.compile(r"^:?-{1,}:?$")
#: Linha em negrito curta que costuma titular a tabela logo abaixo.
_BOLD_TITLE_RE = re.compile(r"^\*\*(.+?)\*\*:?$")
#: `Fonte: ...` logo depois da tabela, com ou sem negrito.
_SOURCE_RE = re.compile(r"^\**\s*Fonte\s*:?\**\s*:?\s*(.+?)\s*$", re.IGNORECASE)
#: Linha que contém somente uma imagem Markdown.
_IMAGE_ONLY_RE = re.compile(r"^!\[(.*?)\]\(\s*([^)\s]+)(?:\s+\"[^\"]*\")?\s*\)$")
#: Item de lista numerada: `1. texto` ou `1) texto`.
_ORDERED_ITEM_RE = re.compile(r"^\s{0,3}(\d{1,2})[.)]\s+(.+?)\s*$")
#: Heading de qualquer nível.
_HEADING_RE = re.compile(r"^\s{0,3}#{1,6}\s+(.+?)\s*$")
#: Rótulo em negrito no começo do item: `**Abra o painel**: detalhe`.
_BOLD_LABEL_RE = re.compile(r"^\*\*(.+?)\*\*\s*[:.–-]?\s*(.*)$")

#: Vocabulário que caracteriza procedimento. Sem uma destas marcas na linha
#: introdutória, a lista numerada continua sendo prosa.
_PROCEDIMENTO_KEYWORDS = (
    "passo a passo",
    "passos",
    "etapas",
    "etapa",
    "procedimento",
    "roteiro",
    "checklist",
    "tutorial",
    "como fazer",
    "como configurar",
    "como criar",
    "como instalar",
    "como publicar",
    "faca assim",
    "siga",
    "execute",
    "configure",
    "instale",
    "implemente",
    "na pratica",
)

#: Teto de caracteres do rótulo de um passo antes de partir em rótulo e detalhe.
_STEP_LABEL_MAX = 90


def slugify(valor: str) -> str:
    """Converte título PT-BR em slug ASCII kebab-case sem acentos."""
    nfkd = unicodedata.normalize("NFKD", valor)
    ascii_str = "".join(c for c in nfkd if not unicodedata.combining(c))
    slug = re.sub(r"[^a-zA-Z0-9\s-]", "", ascii_str)
    slug = re.sub(r"[\s_]+", "-", slug.strip().lower())
    slug = re.sub(r"-+", "-", slug)
    return slug.strip("-")


def short_id(valor: str, max_len: int = 24) -> str:
    """Versão curta do slug (para ids de step)."""
    slug = slugify(valor)
    if len(slug) <= max_len:
        return slug
    return slug[:max_len].rstrip("-")


def _normalizar_quebras(texto: str) -> str:
    """Reduz CRLF e CR isolado a LF.

    Markdown vindo de arquivo gravado no Windows chega com `\\r\\n`, e o `\\r`
    residual já derrubou parser neste ecossistema: a cerca de código deixa de
    casar e o bloco inteiro vira prosa sem ninguém reclamar.
    """
    return texto.replace("\r\n", "\n").replace("\r", "\n")


def _sem_acentos_minusculo(valor: str) -> str:
    """Normaliza para comparação de vocabulário, sem acento e em minúsculas."""
    nfkd = unicodedata.normalize("NFKD", valor)
    return "".join(c for c in nfkd if not unicodedata.combining(c)).lower()


def extract_module_blocks(markdown: str) -> list[tuple[str, str]]:
    """Splita markdown em blocos por heading nível 1 ou 2.

    Preferência: H2 (padrão dos drafts). Fallback: H1. Sem headings, retorna
    o markdown inteiro como 1 único módulo.
    """
    markdown = _normalizar_quebras(markdown)
    if not markdown.strip():
        return []

    primary_re = H2_RE if H2_RE.search(markdown) else H1_RE
    matches = list(primary_re.finditer(markdown))

    if not matches:
        return [("Modulo Unico", markdown.strip())]

    blocks: list[tuple[str, str]] = []
    for i, match in enumerate(matches):
        title = match.group(1).strip()
        title = re.sub(r"\*\*(.+?)\*\*", r"\1", title)
        title = re.sub(r"\*(.+?)\*", r"\1", title)
        start = match.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(markdown)
        content = markdown[start:end].strip()
        if title and content:
            blocks.append((title, content))

    return blocks


def _detect_special_quote(line: str) -> tuple[SectionType, str] | None:
    """Detecta `> DICA: ...`, `> AVISO: ...`, `> CHECKPOINT: ...`."""
    stripped = line.strip()
    if not stripped.startswith(">"):
        return None
    content = stripped[1:].strip()
    for prefix, stype in _SPECIAL_QUOTES.items():
        if content.startswith(f"{prefix}:"):
            return stype, content[len(prefix) + 1 :].strip()
    return None


# ─── Promoção: helpers ───────────────────────────────────────────────


def _secao_segura(**kwargs) -> CourseSection | None:
    """Monta um `CourseSection` e devolve `None` se a carga não passar.

    Todo caminho de promoção passa por aqui. Deixar a exceção subir mataria a
    geração inteira por causa de uma tabela torta.
    """
    try:
        return CourseSection(**kwargs)
    except (ValidationError, ValueError):
        return None


def _celulas_da_linha(linha: str) -> list[str]:
    """Quebra uma linha de tabela Markdown em células já limpas."""
    bruto = linha.strip()
    if bruto.startswith("|"):
        bruto = bruto[1:]
    if bruto.endswith("|"):
        bruto = bruto[:-1]
    return [c.strip() for c in bruto.split("|")]


def _eh_linha_de_tabela(linha: str) -> bool:
    """Linha de corpo de tabela: tem barra e não está vazia."""
    return "|" in linha and bool(linha.strip())


def _eh_separador_de_tabela(linha: str, n_colunas: int) -> bool:
    """Reconhece `|---|---|` e as variações com alinhamento (`:---:`)."""
    if "|" not in linha or "-" not in linha:
        return False
    celulas = _celulas_da_linha(linha)
    if len(celulas) != n_colunas:
        return False
    return all(_TABLE_SEP_CELL_RE.match(c) for c in celulas)


def _normalizar_linha(celulas: list[str], n_colunas: int) -> list[str]:
    """Ajusta uma linha torta ao número de colunas, sem descartar conteúdo.

    Linha curta ganha células vazias. Linha longa tem o excedente juntado na
    última célula, porque cortar célula é perder o que o autor escreveu.
    """
    if len(celulas) == n_colunas:
        return celulas
    if len(celulas) < n_colunas:
        return celulas + [""] * (n_colunas - len(celulas))
    mantidas = celulas[: n_colunas - 1]
    excedente = " ".join(c for c in celulas[n_colunas - 1 :] if c)
    return mantidas + [excedente]


def _try_data_table(
    linhas: list[str], inicio: int, saida: list[str]
) -> tuple[CourseSection, int] | None:
    """Tenta ler uma tabela Markdown a partir de `linhas[inicio]`.

    Devolve a seção `dataTable` e o índice da primeira linha ainda não
    consumida. `saida` são as linhas já emitidas: se a última delas for um
    negrito curto, ela é adotada como `title` e retirada dali.
    """
    if inicio + 1 >= len(linhas):
        return None
    cabecalho = linhas[inicio]
    if not _eh_linha_de_tabela(cabecalho):
        return None
    colunas = _celulas_da_linha(cabecalho)
    if len(colunas) < 2:
        return None
    if not _eh_separador_de_tabela(linhas[inicio + 1], len(colunas)):
        return None

    rows: list[list[str]] = []
    i = inicio + 2
    while i < len(linhas) and _eh_linha_de_tabela(linhas[i]):
        rows.append(_normalizar_linha(_celulas_da_linha(linhas[i]), len(colunas)))
        i += 1
    if not rows:
        return None

    # `Fonte:` logo depois da tabela, tolerando uma linha em branco no meio.
    source: str | None = None
    j = i
    if j < len(linhas) and not linhas[j].strip():
        j += 1
    if j < len(linhas):
        match_fonte = _SOURCE_RE.match(linhas[j].strip())
        if match_fonte:
            source = match_fonte.group(1).strip().strip("*").strip()
            i = j + 1

    # Título vindo do negrito curto imediatamente acima.
    title: str | None = None
    corte = len(saida)
    k = len(saida) - 1
    while k >= 0 and not saida[k].strip():
        k -= 1
    if k >= 0:
        match_titulo = _BOLD_TITLE_RE.match(saida[k].strip())
        if match_titulo and len(match_titulo.group(1)) <= 80:
            title = match_titulo.group(1).strip()
            corte = k

    data: dict = {"columns": colunas, "rows": rows}
    if title:
        data["title"] = title
    if source:
        data["source"] = source

    secao = _secao_segura(type=SectionType.DATA_TABLE, value="", data=data)
    if secao is None:
        return None
    if title:
        del saida[corte:]
    return secao, i


def _split_label_detail(texto: str) -> tuple[str, str | None]:
    """Parte o texto de um passo em rótulo e detalhe.

    Prioridade: negrito no começo, depois dois-pontos com prefixo curto, depois
    a primeira frase quando o item é longo demais para virar rótulo.
    """
    texto = texto.strip()
    match_bold = _BOLD_LABEL_RE.match(texto)
    if match_bold:
        label = match_bold.group(1).strip()
        detail = match_bold.group(2).strip()
        if len(label) >= 3:
            return label, detail or None

    if ":" in texto:
        prefixo, resto = texto.split(":", 1)
        prefixo = prefixo.strip()
        resto = resto.strip()
        if 3 <= len(prefixo) <= _STEP_LABEL_MAX and resto:
            return prefixo, resto

    if len(texto) <= _STEP_LABEL_MAX:
        return texto, None

    corte = texto.find(". ")
    if 3 <= corte <= _STEP_LABEL_MAX:
        return texto[:corte].strip(), texto[corte + 1 :].strip()
    return texto[:_STEP_LABEL_MAX].rstrip(), texto[_STEP_LABEL_MAX:].strip() or None


def _intro_de_procedimento(saida: list[str]) -> tuple[str, int] | None:
    """Procura, nas linhas já emitidas, a introdução que autoriza `stepGuide`.

    Aceita heading de qualquer nível ou linha terminada em dois-pontos, desde
    que o texto traga vocabulário de procedimento. Devolve o título e o índice
    de corte em `saida`.
    """
    k = len(saida) - 1
    while k >= 0 and not saida[k].strip():
        k -= 1
    if k < 0:
        return None

    linha = saida[k].strip()
    match_heading = _HEADING_RE.match(linha)
    if match_heading:
        bruto = match_heading.group(1).strip()
    elif linha.endswith(":"):
        bruto = linha[:-1].strip()
    else:
        return None

    titulo = re.sub(r"\*\*(.+?)\*\*", r"\1", bruto).strip().strip("*").strip()
    normalizado = _sem_acentos_minusculo(titulo)
    if not any(p in normalizado for p in _PROCEDIMENTO_KEYWORDS):
        return None
    if len(titulo) < 3:
        return None
    return titulo, k


def _try_step_guide(
    linhas: list[str], inicio: int, saida: list[str]
) -> tuple[CourseSection, int] | None:
    """Tenta promover uma lista numerada a `stepGuide`.

    Critério, deliberadamente conservador: na dúvida, o trecho segue como
    prosa, porque promover errado carimba de procedimento o que era só uma
    enumeração:

    1. **Três itens, no mínimo**, numerados em sequência começando em `1`. Dois
       itens não sustentam um passo a passo e sequência quebrada (1, 2, 4) indica
       que a leitura do bloco está errada.
    2. **Introdução explícita** na linha imediatamente anterior: heading de
       qualquer nível ou linha terminada em dois-pontos.
    3. **Vocabulário de procedimento** nessa introdução (`passo a passo`,
       `etapas`, `como configurar`, `checklist`, `siga`, `execute`, ...). Sem
       isso, uma lista de argumentos sob "Três motivos para migrar" viraria um
       guia de execução, o que é falso.
    4. Cada item precisa render um rótulo com pelo menos três caracteres.

    Uma lista numerada solta, sem introdução, ou com introdução genérica, fica
    exatamente como está.
    """
    itens: list[str] = []
    i = inicio
    esperado = 1
    while i < len(linhas):
        match_item = _ORDERED_ITEM_RE.match(linhas[i])
        if not match_item:
            break
        if int(match_item.group(1)) != esperado:
            break
        itens.append(match_item.group(2).strip())
        esperado += 1
        i += 1

    if len(itens) < 3:
        return None

    intro = _intro_de_procedimento(saida)
    if intro is None:
        return None
    titulo, corte = intro

    steps: list[dict] = []
    for item in itens:
        label, detail = _split_label_detail(item)
        if len(label) < 3:
            return None
        passo: dict = {"label": label}
        if detail:
            passo["detail"] = detail
        steps.append(passo)

    secao = _secao_segura(
        type=SectionType.STEP_GUIDE,
        value="",
        data={"title": titulo, "steps": steps},
    )
    if secao is None:
        return None
    del saida[corte:]
    return secao, i


def _try_figure(linha: str) -> CourseSection | None:
    """Promove `![legenda](caminho)` a `figure`.

    Imagem sem legenda não é promovida: o `CourseSection` recusa figura muda, e
    o certo nesse caso é a imagem continuar no texto em vez de sumir.
    """
    match_img = _IMAGE_ONLY_RE.match(linha.strip())
    if not match_img:
        return None
    legenda = match_img.group(1).strip()
    caminho = match_img.group(2).strip()
    if not legenda or not caminho:
        return None
    return _secao_segura(type=SectionType.FIGURE, value=caminho, label=legenda)


def _extrair_blocos_visuais(texto: str) -> tuple[str, list[CourseSection]]:
    """Troca construções visuais por marcadores, preservando a posição.

    O que não vira bloco visual sai daqui intacto, linha por linha.
    """
    linhas = texto.split("\n")
    saida: list[str] = []
    blocos: list[CourseSection] = []

    def _marcar(secao: CourseSection) -> None:
        blocos.append(secao)
        saida.append("")
        saida.append(_VISUAL_PLACEHOLDER.format(len(blocos) - 1))
        saida.append("")

    i = 0
    while i < len(linhas):
        linha = linhas[i]

        tabela = _try_data_table(linhas, i, saida)
        if tabela is not None:
            secao, proximo = tabela
            _marcar(secao)
            i = proximo
            continue

        guia = _try_step_guide(linhas, i, saida)
        if guia is not None:
            secao, proximo = guia
            _marcar(secao)
            i = proximo
            continue

        figura = _try_figure(linha)
        if figura is not None:
            _marcar(figura)
            i += 1
            continue

        saida.append(linha)
        i += 1

    return "\n".join(saida), blocos


def parse_module_to_sections(
    content: str,
    chunk_size: int = 1500,
    add_checkpoint_if_missing: bool = True,
    min_sections: int = 3,
) -> list[CourseSection]:
    """Converte conteúdo de um módulo em CourseSections.

    Estratégia:
    1. Normaliza quebras de linha (CRLF vira LF)
    2. Extrai code fences e guarda marcadores
    3. Extrai blockquotes especiais (DICA/AVISO/CHECKPOINT) e genéricos (TIP)
    4. Promove tabela, lista de procedimento e imagem legendada a bloco visual,
       deixando um marcador na posição original
    5. Quebra texto restante em chunks
    6. Reinsere code fences e blocos visuais onde aparecem os marcadores
    7. Garante ≥1 CHECKPOINT e ≥min_sections sections (validação Pydantic)
    """
    content = _normalizar_quebras(content)
    sections: list[CourseSection] = []

    code_blocks: list[CourseSection | None] = []

    def _code_replace(match: re.Match) -> str:
        lang = match.group(1) or "text"
        code = match.group(2).strip()
        if not code:
            return ""
        code_blocks.append(
            CourseSection(type=SectionType.CODE, value=code, language=lang)
        )
        return f"\n[CODE_BLOCK_{len(code_blocks) - 1}]\n"

    text_no_code = CODE_FENCE_RE.sub(_code_replace, content)

    # Blockquotes
    quote_sections: list[CourseSection] = []
    lines = text_no_code.splitlines()
    cleaned_lines: list[str] = []
    current_quote_lines: list[str] = []

    def _flush_quote() -> None:
        if not current_quote_lines:
            return
        joined = " ".join(current_quote_lines).strip()
        if not joined:
            return
        # Verifica se é um quote especial (DICA:/AVISO:/CHECKPOINT:)
        matched_type: SectionType | None = None
        for prefix, stype in _SPECIAL_QUOTES.items():
            if joined.startswith(f"{prefix}:"):
                matched_type = stype
                joined = joined[len(prefix) + 1 :].strip()
                quote_sections.append(
                    CourseSection(type=stype, value=joined, label=prefix)
                )
                break
        if matched_type is None:
            quote_sections.append(CourseSection(type=SectionType.TIP, value=joined))

    for line in lines:
        if line.lstrip().startswith(">"):
            current_quote_lines.append(line.lstrip()[1:].strip())
        else:
            _flush_quote()
            current_quote_lines = []
            cleaned_lines.append(line)
    _flush_quote()

    text_clean = "\n".join(cleaned_lines)

    # Promoção a bloco visual
    text_clean, visual_blocks_raw = _extrair_blocos_visuais(text_clean)
    visual_blocks: list[CourseSection | None] = list(visual_blocks_raw)

    # Chunks de texto
    paragraphs = [p.strip() for p in re.split(r"\n\s*\n", text_clean) if p.strip()]
    text_chunks: list[str] = []
    current_chunk: list[str] = []
    current_len = 0
    for p in paragraphs:
        if current_len + len(p) > chunk_size and current_chunk:
            text_chunks.append("\n\n".join(current_chunk))
            current_chunk = [p]
            current_len = len(p)
        else:
            current_chunk.append(p)
            current_len += len(p)
    if current_chunk:
        text_chunks.append("\n\n".join(current_chunk))

    def _resgatar(marcador: str) -> CourseSection | None:
        """Consome o bloco de um marcador, uma vez só."""
        familia, _, resto = marcador.strip("[]").partition("_BLOCK_")
        try:
            idx = int(resto)
        except ValueError:
            return None
        pool = code_blocks if familia == "CODE" else visual_blocks
        if 0 <= idx < len(pool) and pool[idx] is not None:
            secao = pool[idx]
            pool[idx] = None
            return secao
        return None

    # Reinsere code blocks e blocos visuais na posição original
    for chunk in text_chunks:
        if not chunk.strip():
            continue
        for parte in _ANY_PLACEHOLDER_RE.split(chunk):
            if not parte.strip():
                continue
            if _ANY_PLACEHOLDER_RE.fullmatch(parte.strip()):
                secao = _resgatar(parte.strip())
                if secao is not None:
                    sections.append(secao)
                continue
            sections.append(
                CourseSection(type=SectionType.TEXT, value=parte.strip())
            )

    # Blocos não consumidos (marcador perdido em corte de chunk)
    for pendente in (*code_blocks, *visual_blocks):
        if pendente is not None:
            sections.append(pendente)

    # Quotes ao final
    sections.extend(quote_sections)

    # Garantias mínimas para validação Pydantic de StepDefinition
    has_checkpoint = any(s.type == SectionType.CHECKPOINT for s in sections)
    if add_checkpoint_if_missing and not has_checkpoint:
        sections.append(
            CourseSection(
                type=SectionType.CHECKPOINT,
                value=(
                    "Verifique seu entendimento: revise os conceitos centrais "
                    "deste módulo antes de avançar para o próximo."
                ),
                label="CHECKPOINT",
            )
        )

    while len(sections) < min_sections:
        sections.append(
            CourseSection(
                type=SectionType.TIP,
                value="Reflita sobre como aplicar este conteúdo ao seu contexto profissional.",
            )
        )

    return sections
