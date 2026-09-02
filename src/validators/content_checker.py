"""Validador de qualidade de conteúdo educacional.

**A unidade de medida é a AULA** desde 27/08/2026. Até então era o módulo, com
piso de 2.500 palavras e uma bateria de pisos ("3+ exercícios", "5+
estatísticas", "1+ tabela", "1+ blockquote"). O resultado medido nos cursos
gerados foi previsível: o redator enchia a cota com abrangência, listava o
conceito sem explicá-lo e emendava exercício em cima de exercício. A régua nova
vem do tipo D ("aula/trilha") da tabela única de tetos da fonte de estilo
(`alexandrebrt14-sys/escrita-empreendedor`, `MOLDES_DE_PAGINA.md` seções 2, 3-D
e 6):

- palavras, H2, H3 por H2, apoios visuais e parágrafo: os números vivem em
  `tetos.D` de `config/lexicos.json` (a fonte é a única cópia);
- 1 exercício por aula; 1 fonte datada e 1 cápsula por trilha.

Nenhum desses números mora neste arquivo nem em `config/quality_rules.yaml`:
eles vêm de `config/lexicos.json` (`tetos.D`), espelho gerado da fonte, lido por
`src/validators/lexicos_loader.py`. As constantes `FALLBACK_*` abaixo só entram
em ação se o espelho sumir, e existem para que uma configuração corrompida não
desligue o gate em silêncio. A mensagem de erro interpola o valor carregado, e
não um literal, para que código e mensagem nunca divirjam do arquivo.

**Compatibilidade com "módulo".** O pipeline de geração ainda entrega uma peça
chamada módulo. `check_content(..., unidade="modulo")` mede essa peça como um
conjunto de 4 a 6 aulas (`content_quality.lessons_per_module` no YAML), ou seja
4×1.200 a 6×2.400 = 4.800-14.400 palavras, com piso 4×900 = 3.600 e erro
6×3.600 = 21.600. Os pisos de estrutura (H2, exercício) também escalam pelo
número de aulas. O padrão do parâmetro é `"aula"`.

As listas de expressão proibida e os tetos vêm da fonte; o que sobra em
`config/quality_rules.yaml` é só o que é específico do curso-factory.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

from src.validators.lexicos_loader import expressoes_vetadas, tetos_da_aula
from src.validators.rules_loader import rules_list, validation_section


@dataclass
class ContentError:
    """Erro ou aviso de qualidade de conteúdo."""
    tipo: str  # "error" ou "warning"
    categoria: str
    mensagem: str
    modulo: str = ""


# ─── Tetos da aula (tipo D da fonte) ──────────────────────────────────────
#
# Fallbacks: espelham `tetos.D` de config/lexicos.json na data acima. Só valem
# quando o espelho não carrega.
FALLBACK_PALAVRAS_PISO = 900
FALLBACK_PALAVRAS_ALVO = (1200, 2400)
FALLBACK_PALAVRAS_AVISO = 2400
FALLBACK_PALAVRAS_ERRO = 3600
FALLBACK_H2 = (2, 4)
FALLBACK_H3_POR_H2 = 2
FALLBACK_VISUAIS_MAX = 3
FALLBACK_PARAGRAFO = (15, 45)

#: Faixa de aulas por módulo, para o modo de compatibilidade.
FALLBACK_AULAS_POR_MODULO = (4, 6)


def _par(valor, padrao: tuple[int, int]) -> tuple[int, int]:
    """Normaliza um par vindo do JSON (lista de 2) para tupla de inteiros."""
    if isinstance(valor, (list, tuple)) and len(valor) == 2:
        try:
            return int(valor[0]), int(valor[1])
        except (TypeError, ValueError):
            return padrao
    return padrao


def _inteiro(valor, padrao: int) -> int:
    try:
        return int(valor)
    except (TypeError, ValueError):
        return padrao


def tetos_da_unidade(unidade: str = "aula") -> dict:
    """Devolve os tetos aplicáveis à unidade medida.

    Args:
        unidade: `"aula"` (padrão) ou `"modulo"`. No segundo caso os números da
            aula são multiplicados pela faixa de aulas por módulo, porque o
            pipeline atual ainda entrega módulos e medi-los com a régua de uma
            aula reprovaria todo curso existente.

    Returns:
        Dict com `piso`, `alvo` (par), `aviso`, `erro`, `h2` (par),
        `h3_por_h2`, `visuais_max`, `paragrafo` (par) e `exercicios_min`.
    """
    d = tetos_da_aula()
    palavras = d.get("palavras") if isinstance(d.get("palavras"), dict) else {}

    piso = _inteiro(palavras.get("piso"), FALLBACK_PALAVRAS_PISO)
    alvo = _par(palavras.get("alvo"), FALLBACK_PALAVRAS_ALVO)
    aviso = _inteiro(palavras.get("aviso"), FALLBACK_PALAVRAS_AVISO)
    erro = _inteiro(palavras.get("erro"), FALLBACK_PALAVRAS_ERRO)
    h2 = _par(d.get("h2"), FALLBACK_H2)
    h3_por_h2 = _inteiro(d.get("h3_por_h2"), FALLBACK_H3_POR_H2)
    visuais_max = _inteiro(d.get("figuras_max"), FALLBACK_VISUAIS_MAX)
    paragrafo = _par(d.get("paragrafo"), FALLBACK_PARAGRAFO)

    cq = validation_section("content_quality")
    exercicios_min = _inteiro(cq.get("min_exercises_per_lesson"), 1)

    if unidade == "modulo":
        minimo, maximo = _par(cq.get("lessons_per_module"), FALLBACK_AULAS_POR_MODULO)
        piso *= minimo
        alvo = (alvo[0] * minimo, alvo[1] * maximo)
        aviso = alvo[1]
        erro *= maximo
        h2 = (h2[0] * minimo, h2[1] * maximo)
        visuais_max *= maximo
        exercicios_min *= minimo

    return {
        "unidade": "módulo" if unidade == "modulo" else "aula",
        "piso": piso,
        "alvo": alvo,
        "aviso": aviso,
        "erro": erro,
        "h2": h2,
        "h3_por_h2": h3_por_h2,
        "visuais_max": visuais_max,
        "paragrafo": paragrafo,
        "exercicios_min": exercicios_min,
    }


#: Teto de palavras por parágrafo, lido da fonte. `voice_guard` importa daqui.
MIN_PARAGRAPH_WORDS, MAX_PARAGRAPH_WORDS = tetos_da_unidade()["paragrafo"]

# Clichês proibidos — FALLBACK RESIDUAL.
# A lista viva tem duas origens: `config/lexicos.json` (a fonte de estilo, com
# clichê de máquina, adjetivo vazio, atribuição vaga, escassez fabricada e
# conectivo de enchimento) e `validation.forbidden_expressions.expressions` em
# config/quality_rules.yaml, que guarda só o que é específico deste repositório.
# As entradas abaixo são as que nem a fonte nem o YAML cobrem por conta própria;
# sem elas, um espelho ausente desligaria parte do anti-clichê em silêncio.
FORBIDDEN_CLICHES = [
    "é fundamental que",
    "não é segredo que",
    "o futuro é agora",
    "vamos explorar",
    "como sabemos",
    "diante desse cenário",
    "vale a pena destacar",
    "grosso modo",
    "vamos aprender",
    "agora você vai entender",
    "como todos sabem",
    "desde os primórdios",
    "desde tempos imemoriais",
]

# Verbos de Bloom proibidos em objetivos (níveis inferiores)
BLOOM_FORBIDDEN_VERBS = [
    "entender", "conhecer", "saber", "compreender",
    "lembrar", "memorizar", "listar", "descrever",
    "identificar", "reconhecer", "definir", "citar",
]

# Verbos de Bloom aceitos (níveis superiores)
BLOOM_ACCEPTED_VERBS = [
    "analisar", "comparar", "diferenciar", "diagnosticar", "categorizar",
    "avaliar", "justificar", "priorizar", "recomendar", "defender",
    "criar", "projetar", "formular", "propor", "desenvolver",
    "aplicar", "implementar", "executar", "demonstrar", "calcular",
    "construir", "elaborar", "planejar", "sintetizar", "integrar",
]


def _count_words(text: str) -> int:
    """Conta palavras no texto, ignorando blocos de código e metadados."""
    # Remover blocos de código
    clean = re.sub(r"```[\s\S]*?```", "", text)
    # Remover metadados YAML
    clean = re.sub(r"^---[\s\S]*?---", "", clean)
    return len(clean.split())


def _find_tables(text: str) -> int:
    """Conta tabelas Markdown no texto.

    Uma tabela tem header + separador + linhas; conta-se pelos separadores
    (`| --- | --- |`), que aparecem exatamente uma vez por tabela.
    """
    separators = re.findall(r"^\|[\s:|-]+\|", text, re.MULTILINE)
    return len(separators)


#: Separador de parágrafo em Markdown: uma linha em branco.
SEP_PARAGRAFO = "\n\n"

def _find_figures(text: str) -> int:
    """Conta figuras Markdown (imagem com legenda) no texto."""
    return len(re.findall(r"!\[[^\]]*\]\(", text))


def _find_headings(text: str) -> list[tuple[int, str, str]]:
    """Encontra headings Markdown com nível e texto."""
    headings = []
    for match in re.finditer(r"^(#{2,4})\s+(.+)", text, re.MULTILINE):
        level = len(match.group(1))
        headings.append((level, match.group(2).strip(), match.group(0)))
    return headings


def _find_blockquotes(text: str) -> int:
    """Conta blocos de citação (>) no texto."""
    return len(re.findall(r"^>\s+", text, re.MULTILINE))


def _find_bold_terms(text: str) -> int:
    """Conta termos em negrito no texto."""
    return len(re.findall(r"\*\*[^*]+\*\*", text))


def _find_exercises(text: str) -> list[str]:
    """Encontra exercícios no texto."""
    # Procura por padrões comuns de exercício
    patterns = [
        r"(?:###?\s+)?(?:Exercício|exercício)\s*(?:\d+|:|\s*—)",
        r"(?:###?\s+)?(?:Atividade|atividade)\s*(?:\d+|:|\s*—)",
        r"\*\*(?:Exercício|Atividade|Desafio|Prática)\b[^*]*\*\*",
        r"(?:###?\s+)?\*\*(?:Nível\s+Bloom|Nível):",
        # Molde da aula (02/09/2026): o exercício é o H2 "Faça agora", com o
        # campo "Resultado esperado". Medido no E2E do mesmo dia: seis aulas
        # com o exercício completo reprovavam por "0 exercício(s)".
        r"^#{2,4}\s+Fa[çc]a agora\b",
        r"\*\*Resultado esperado\s*:",
    ]
    exercicios = []
    for pattern in patterns:
        exercicios.extend(re.findall(pattern, text, flags=re.MULTILINE | re.IGNORECASE))
    return exercicios


def _forbidden_expressions() -> list[str]:
    """Une as três origens de expressão vetada, sem repetir nenhuma.

    Ordem: primeiro a fonte de estilo (`config/lexicos.json`), depois o que é
    específico deste repositório (`validation.forbidden_expressions.expressions`
    em `config/quality_rules.yaml`), por fim o fallback residual do módulo. A
    dedup é case-insensitive e preserva a ordem. Sem o espelho e sem o YAML,
    sobra o fallback — reduzido, mas nunca vazio.
    """
    merged: list[str] = []
    vistos: set[str] = set()
    origens = [
        expressoes_vetadas(),
        rules_list("forbidden_expressions", "expressions"),
        FORBIDDEN_CLICHES,
    ]
    for origem in origens:
        for expr in origem:
            limpo = expr.strip()
            chave = limpo.lower()
            if not chave or chave in vistos:
                continue
            vistos.add(chave)
            merged.append(limpo)
    return merged


#: Trecho curto entre aspas retas ou curvas: menção de uma expressão.
_MENCAO_RE = re.compile(r"[\"“„”']([^\"“„”'\n]{2,80})[\"“„”']")


def _sem_mencoes(text: str) -> str:
    """Apaga o que está entre aspas, para o gate não punir a menção de um vício."""
    return _MENCAO_RE.sub(" ", text)


def _check_cliches(text: str) -> list[str]:
    """Encontra clichês proibidos no texto.

    A lista combina a fonte de estilo, o YAML de regras e o fallback do módulo,
    de modo que acrescentar uma expressão em `config/lexicos.json` (regerando o
    espelho) ou em `config/quality_rules.yaml` passa a reprovar conteúdo sem
    alterar código.
    """
    found = []
    # Expressão entre aspas é menção, não uso: a aula que ensina a NÃO
    # escrever "últimas vagas" precisa poder citar "últimas vagas". Medido
    # no E2E de 02/09/2026 (aula sobre gatilhos reprovada por ensinar o veto).
    text_lower = _sem_mencoes(text).lower()
    for cliche in _forbidden_expressions():
        if cliche.lower() in text_lower:
            found.append(cliche)
    # Uma ocorrência, uma cobrança. Unir três listas trouxe expressões que se
    # contêm ("em um mundo cada vez mais" contém o conectivo "cada vez mais"),
    # e sem esta poda o mesmo trecho de texto era penalizado duas vezes pelo
    # voice_guard, que desconta por achado. Fica a expressão mais longa, que é
    # a que descreve melhor o defeito.
    minusculas = [c.lower() for c in found]
    return [
        cliche
        for cliche, chave in zip(found, minusculas, strict=True)
        if not any(chave != outra and chave in outra for outra in minusculas)
    ]


def _check_bloom_objectives(text: str) -> tuple[list[str], list[str]]:
    """Verifica verbos de Bloom nos objetivos de aprendizagem.

    Returns:
        Tupla com (verbos_proibidos_encontrados, verbos_aceitos_encontrados).
    """
    # Procurar a SEÇÃO de objetivos: cabeçalho ou rótulo em negrito abrindo a
    # linha. Até 02/09/2026 a busca casava a palavra "objetivo" em qualquer
    # frase ("o objetivo da mensagem é...") e lia "entender" no parágrafo
    # seguinte como verbo de Bloom de um objetivo que não existia.
    obj_match = re.search(
        r"^(?:#{1,6}\s*|\*\*)\s*Objetivos?(?:\s+de\s+Aprendizagem)?\b[\s\S]*?(?=\n##|\n\*\*[A-Z]|\Z)",
        text,
        re.IGNORECASE | re.MULTILINE,
    )
    if not obj_match:
        return [], []

    obj_text = obj_match.group(0).lower()
    proibidos = [v for v in BLOOM_FORBIDDEN_VERBS if v in obj_text]
    aceitos = [v for v in BLOOM_ACCEPTED_VERBS if v in obj_text]
    return proibidos, aceitos


def _check_heading_hierarchy(headings: list[tuple[int, str, str]]) -> list[str]:
    """Verifica se a hierarquia de títulos é correta (sem pulos)."""
    errors = []
    prev_level = 1  # Assume H1 como contexto
    for level, text, _raw in headings:
        if level > prev_level + 1:
            errors.append(
                f"Pulo de hierarquia: H{prev_level} → H{level} "
                f"(título: '{text[:50]}')"
            )
        prev_level = level
    return errors


def _check_paragraph_length(text: str) -> list[tuple[int, int]]:
    """Encontra parágrafos fora da faixa de 15 a 45 palavras.

    A régua trocou de unidade em 27/08/2026. Contar LINHAS media a largura da
    janela de quem escreveu, não o fôlego do parágrafo: o mesmo texto dava 4
    linhas num editor e 9 em outro. A fonte de estilo mede palavras, e a faixa
    do tipo D é 15 a 45 (`tetos.D.paragrafo`). Abaixo de 15 o parágrafo é
    fragmento de texto fatiado, que é a assinatura de conteúdo de máquina;
    acima de 45 costuma empilhar dois assuntos.

    Returns:
        Lista de (número da linha, palavras no parágrafo), só para os que estão
        fora da faixa.
    """
    fora_da_faixa: list[tuple[int, int]] = []
    paragraphs = text.split(SEP_PARAGRAFO)
    line_num = 1
    for para in paragraphs:
        limpo = para.strip()
        lines = limpo.splitlines()
        # Ignorar blocos de código, tabelas, listas, citações e cabeçalhos
        if limpo.startswith(("```", "|", "- ", "* ", "1.", ">", "#")):
            line_num += len(lines) + 1
            continue
        palavras = len(limpo.split())
        if palavras and not (MIN_PARAGRAPH_WORDS <= palavras <= MAX_PARAGRAPH_WORDS):
            fora_da_faixa.append((line_num, palavras))
        line_num += len(lines) + 1
    return fora_da_faixa


def _has_emoji(text: str) -> bool:
    """Detecta emojis no texto."""
    emoji_pattern = re.compile(
        "["
        "\U0001F600-\U0001F64F"
        "\U0001F300-\U0001F5FF"
        "\U0001F680-\U0001F6FF"
        "\U0001F1E0-\U0001F1FF"
        "\U00002702-\U000027B0"
        "\U000024C2-\U0001F251"
        "\U0001f926-\U0001f937"
        "\U00010000-\U0010ffff"
        "\u200d\u2640-\u2642"
        "]+",
        flags=re.UNICODE,
    )
    return bool(emoji_pattern.search(text))


def _strip_noise(text: str) -> str:
    """Remove blocos de código e metadados YAML para contagem GEO."""
    clean = re.sub(r"```[\s\S]*?```", "", text)
    clean = re.sub(r"^---[\s\S]*?---", "", clean)
    return clean


def _count_cite_sources(text: str) -> int:
    """Conta fontes externas atribuídas (Cite Sources do playbook Princeton).

    Sinais: citação parentética com ano "(Gartner, 2025)", marcadores
    "Segundo X (ano)"/"de acordo com (ano)" e links markdown externos.
    """
    clean = _strip_noise(text)
    signals = 0
    # Citação parentética contendo um ano (1900-2099)
    signals += len(re.findall(r"\([^)]*\b(?:19|20)\d{2}\b[^)]*\)", clean))
    # Marcadores de atribuição seguidos (na mesma frase) de um ano
    signals += len(
        re.findall(
            r"(?:Segundo|segundo|De acordo com|de acordo com|Conforme|conforme)\b"
            r"[^.\n]{0,80}\b(?:19|20)\d{2}\b",
            clean,
        )
    )
    # Links markdown para fontes externas (http/https)
    signals += len(re.findall(r"\[[^\]]+\]\(https?://", clean))
    return signals


def _count_statistics(text: str) -> int:
    """Conta dados quantitativos com contexto (estatísticas)."""
    clean = _strip_noise(text)
    count = 0
    count += len(re.findall(r"\b\d{1,3}(?:[.,]\d+)?\s?%", clean))          # percentuais
    count += len(re.findall(r"\b\d+(?:[.,]\d+)?\s?[x×](?![\w.])", clean))  # multiplicadores (3x, 4,1×)
    count += len(re.findall(r"(?:R\$|US\$|€)\s?\d", clean))                # valores monetários
    count += len(re.findall(r"\bde\s+\d[\d.,]*\s*%?\s+para\s+\d", clean))  # "de X para Y"
    return count


def _count_quotations(text: str) -> int:
    """Conta citações diretas atribuídas (aspas + nome do autor)."""
    clean = _strip_noise(text)
    # Trecho entre aspas (retas ou tipográficas) seguido de atribuição com travessão/hífen
    pattern = r'["“][^"”\n]{12,}["”]\s*[—–-]\s*[A-ZÀ-Ú]'
    return len(re.findall(pattern, clean))


def _has_answer_capsule(text: str) -> bool:
    """Detecta ao menos um 'answer capsule' (parágrafo resposta-primeiro após heading).

    Capsule = parágrafo de prosa curto (≈20-70 palavras), auto-contido,
    imediatamente após um heading H2/H3, sem ser lista/tabela/citação/código.
    """
    clean = _strip_noise(text)
    lines = clean.split("\n")
    for i, line in enumerate(lines):
        if not re.match(r"^#{2,4}\s+\S", line):
            continue
        # Achar o próximo bloco não-vazio após o heading
        j = i + 1
        while j < len(lines) and not lines[j].strip():
            j += 1
        if j >= len(lines):
            continue
        para = lines[j].strip()
        if para.startswith(("-", "*", "|", ">", "#", "1.", "```")):
            continue
        words = len(para.split())
        if 18 <= words <= 75:
            return True
    return False


# ─── Anti-invenção (validation.anti_invencao em config/quality_rules.yaml) ──

# Defaults aplicados quando o YAML não carrega. Espelham o arquivo.
DEFAULT_REQUIRE_SOURCE_FOR_PERCENTAGES = True
DEFAULT_MAX_UNRESOLVED_MARKERS = 5

# Teto de avisos de percentual por documento. Acima disso o relatório vira
# ruído e o revisor para de ler antes de chegar ao que importa.
MAX_PERCENTAGE_WARNINGS = 5

# Marcadores que o redator deixa para o revisor humano resolver. A grafia sem
# acento entra porque o marcador é digitado à mão no meio do texto.
_UNRESOLVED_MARKER_RE = re.compile(
    r"\[\s*(?:FALTA\s+EVID[ÊE]NCIA|PREENCHER-HUMANO)\s*:",
    re.IGNORECASE,
)

# Sinais de que um percentual está ancorado em fonte verificável.
_SOURCE_SIGNAL_RE = re.compile(
    r"\([^)]*\b(?:19|20)\d{2}\b[^)]*\)"   # citação parentética: "(Gartner, 2026)"
    r"|\b(?:19|20)\d{2}\b"                # ano solto na frase
    r"|\bsegundo\b"
    r"|\bconforme\b"
    r"|\bde acordo com\b"
    r"|\bfontes?\b"
    r"|\barxiv\b",
    re.IGNORECASE,
)

# Fim de frase: .!? seguido de espaço ou fim, linha em branco, ou início de
# heading. O lookahead impede cortar decimal e separador de milhar
# ("23.5%", "1.000 respondentes").
_SENTENCE_BREAK_RE = re.compile(r"[.!?](?=\s|$)|\n[ \t]*\n|\n(?=[ \t]*#)")


def _mask_uncheckable(text: str) -> str:
    """Apaga o que não deve ser lido como prosa, preservando as posições.

    Saem blocos de código, código inline e linhas de tabela Markdown. O
    comprimento e as quebras de linha ficam iguais aos do original, para que o
    número de linha reportado continue batendo com o arquivo.
    """
    def _blank(match: re.Match[str]) -> str:
        return re.sub(r"[^\n]", " ", match.group(0))

    masked = re.sub(r"```[\s\S]*?```", _blank, text)
    masked = re.sub(r"`[^`\n]*`", _blank, masked)
    masked = re.sub(r"^[ \t]*\|.*$", _blank, masked, flags=re.MULTILINE)
    return masked


def _split_sentences(text: str) -> list[tuple[int, str]]:
    """Divide o texto em frases, devolvendo (posição inicial, frase)."""
    frases: list[tuple[int, str]] = []
    inicio = 0
    for match in _SENTENCE_BREAK_RE.finditer(text):
        frases.append((inicio, text[inicio:match.end()]))
        inicio = match.end()
    if inicio < len(text):
        frases.append((inicio, text[inicio:]))
    return frases


def _check_percentages_have_source(text: str) -> list[tuple[int, str]]:
    """Encontra percentuais sem sinal de fonte na mesma frase.

    Percentual solto é o vetor mais comum de invenção: o número parece
    apuração e some na revisão. A checagem é textual e conservadora — basta um
    sinal de atribuição (ano, "segundo", "conforme", "de acordo com", "fonte",
    citação parentética com ano, "arXiv") na mesma frase para o número passar.
    Blocos de código, código inline e linhas de tabela ficam de fora.

    Returns:
        Lista de (número da linha, trecho da frase) para cada percentual sem
        sinal de fonte, na ordem em que aparecem.
    """
    masked = _mask_uncheckable(text)
    achados: list[tuple[int, str]] = []
    for inicio, frase in _split_sentences(masked):
        if "%" not in frase or _SOURCE_SIGNAL_RE.search(frase):
            continue
        pos_pct = inicio + frase.index("%")
        linha = masked.count("\n", 0, pos_pct) + 1
        trecho = re.sub(r"\s+", " ", frase).strip()
        if len(trecho) > 100:
            trecho = trecho[:97] + "..."
        achados.append((linha, trecho))
    return achados


def _count_unresolved_markers(text: str) -> int:
    """Conta marcadores de apuração pendente deixados para o revisor humano."""
    return len(_UNRESOLVED_MARKER_RE.findall(text))


def check_content(
    text: str,
    module_name: str = "",
    geo_config=None,
    unidade: str = "aula",
) -> list[ContentError]:
    """Valida qualidade de conteúdo educacional contra os tetos do molde D.

    Args:
        text: o Markdown da unidade a medir.
        module_name: rótulo usado no relatório.
        geo_config: `Geo2026Config` do cliente, opcional. Quando presente, liga
            a camada de citabilidade GEO.
        unidade: `"aula"` (padrão) ou `"modulo"`. Ver `tetos_da_unidade`: no
            modo módulo os números da aula são multiplicados pela faixa de 4 a
            6 aulas, para que o pipeline atual, que ainda entrega módulos, não
            seja reprovado por medir a peça errada.

    Verifica: extensão, número de H2 e de H3 por H2, hierarquia de títulos,
    teto de apoios visuais, exercício aplicado, clichês, verbos de Bloom,
    andragogia, faixa de parágrafo, emojis e as duas regras de anti-invenção.

    Returns:
        Lista de erros e avisos encontrados.
    """
    erros: list[ContentError] = []
    tetos = tetos_da_unidade(unidade)
    nome_unidade = tetos["unidade"]
    mod = module_name or nome_unidade

    # 1. Extensão. Piso, alvo, aviso e erro vêm de `tetos.D` na fonte.
    word_count = _count_words(text)
    piso = tetos["piso"]
    alvo_min, alvo_max = tetos["alvo"]
    if word_count < piso:
        erros.append(ContentError(
            tipo="error",
            categoria="profundidade",
            mensagem=f"{nome_unidade.capitalize()} com {word_count} palavras, abaixo do "
                     f"piso de {piso}. Abaixo do piso a peça apresenta o conceito e não o "
                     f"explica: falta a narrativa (de onde vem a ideia, por que importa, o "
                     f"que muda, o erro comum) ou o exemplo contado por inteiro. "
                     f"Alvo: {alvo_min} a {alvo_max}.",
            modulo=mod,
        ))
    elif word_count < alvo_min:
        erros.append(ContentError(
            tipo="warning",
            categoria="profundidade",
            mensagem=f"{nome_unidade.capitalize()} com {word_count} palavras, abaixo do "
                     f"alvo de {alvo_min} a {alvo_max}. Verifique se a parte explicativa "
                     f"(cerca de 60% das palavras) está desenvolvida.",
            modulo=mod,
        ))
    elif word_count > tetos["erro"]:
        erros.append(ContentError(
            tipo="error",
            categoria="profundidade",
            mensagem=f"{nome_unidade.capitalize()} com {word_count} palavras, acima do teto "
                     f"de {tetos['erro']}. Uma ideia por aula: divida em duas.",
            modulo=mod,
        ))
    elif word_count > tetos["aviso"]:
        erros.append(ContentError(
            tipo="warning",
            categoria="profundidade",
            mensagem=f"{nome_unidade.capitalize()} com {word_count} palavras, acima do "
                     f"alvo de {alvo_min} a {alvo_max}. Confira se não entrou uma segunda "
                     f"ideia que merece aula própria.",
            modulo=mod,
        ))

    # 2. Apoios visuais: TETO, não piso. Tabela e figura entram só quando
    #    substituem texto; cobrá-los como obrigação produzia enfeite.
    headings = _find_headings(text)
    visuais = _find_tables(text) + _find_figures(text)
    if visuais > tetos["visuais_max"]:
        erros.append(ContentError(
            tipo="warning",
            categoria="formatação",
            mensagem=f"{visuais} apoios visuais, acima do teto de {tetos['visuais_max']} "
                     f"por {nome_unidade}. Apoio visual entra quando SUBSTITUI texto "
                     f"(comparação, sequência, conjunto de números); acima do teto ele "
                     f"passa a competir com a leitura.",
            modulo=mod,
        ))

    # 3. H2 e H3: 2 a 4 H2 por aula (explicar, exemplo, fazer agora), até 2 H3
    #    por H2. O piso antigo de "3+ headings" não dizia de que nível.
    h2 = [h for h in headings if h[0] == 2]
    h2_min, h2_max = tetos["h2"]
    if len(h2) < h2_min:
        erros.append(ContentError(
            tipo="error",
            categoria="formatação",
            mensagem=f"{len(h2)} H2 na {nome_unidade}, abaixo do mínimo de {h2_min}. "
                     f"A sequência do molde pede ao menos: explicar a ideia, exemplo do "
                     f"negócio do aluno e 'faça agora'.",
            modulo=mod,
        ))
    elif len(h2) > h2_max:
        erros.append(ContentError(
            tipo="warning",
            categoria="formatação",
            mensagem=f"{len(h2)} H2 na {nome_unidade}, acima do teto de {h2_max}. "
                     f"Mais seções do que isso costuma indicar duas ideias na mesma peça.",
            modulo=mod,
        ))

    h3_por_h2 = tetos["h3_por_h2"]
    contagem_h3 = 0
    for nivel, _titulo, _raw in headings:
        if nivel == 2:
            contagem_h3 = 0
        elif nivel == 3:
            contagem_h3 += 1
            if contagem_h3 > h3_por_h2:
                erros.append(ContentError(
                    tipo="warning",
                    categoria="formatação",
                    mensagem=f"Mais de {h3_por_h2} H3 sob o mesmo H2. "
                             f"Acima disso o H2 já é duas seções.",
                    modulo=mod,
                ))
                break

    for err in _check_heading_hierarchy(headings):
        erros.append(ContentError(
            tipo="error",
            categoria="formatação",
            mensagem=err,
            modulo=mod,
        ))

    # 4. Negrito deixou de ter piso em 02/09/2026: cobrar "3 termos em
    #    negrito" produzia destaque por cota, e destaque em excesso anula o
    #    destaque. A chave `min_bold_terms_per_lesson` só age se estiver
    #    presente no YAML com valor acima de zero.
    bold_minimo = _inteiro(
        validation_section("content_quality").get("min_bold_terms_per_lesson"), 0
    )
    if bold_minimo > 0:
        bold_count = _find_bold_terms(text)
        if bold_count < bold_minimo:
            erros.append(ContentError(
                tipo="warning",
                categoria="formatação",
                mensagem=f"Apenas {bold_count} termos em negrito (recomendado: {bold_minimo}).",
                modulo=mod,
            ))

    # 5. Exercício: 1 por aula ("faça agora", 5-15 min, com etapas numeradas e
    #    o resultado esperado). Era "mínimo 3 por módulo".
    exercises = _find_exercises(text)
    minimo_ex = tetos["exercicios_min"]
    if len(exercises) < minimo_ex:
        erros.append(ContentError(
            tipo="error",
            categoria="exercícios",
            mensagem=f"{len(exercises)} exercício(s) detectado(s) na {nome_unidade} "
                     f"(mínimo: {minimo_ex}). O exercício é o 'faça agora': 5 a 15 minutos, "
                     f"em etapas numeradas, com dado real do aluno e o resultado esperado.",
            modulo=mod,
        ))

    # 7. Clichês proibidos
    cliches = _check_cliches(text)
    for cliche in cliches:
        erros.append(ContentError(
            tipo="error",
            categoria="editorial",
            mensagem=f"Clichê proibido encontrado: '{cliche}'. "
                     f"Substitua por informação concreta.",
            modulo=mod,
        ))

    # 8. Verbos de Bloom nos objetivos
    bloom_proibidos, bloom_aceitos = _check_bloom_objectives(text)
    for verbo in bloom_proibidos:
        erros.append(ContentError(
            tipo="error",
            categoria="andragogia",
            mensagem=f"Verbo de Bloom nível inferior nos objetivos: '{verbo}'. "
                     f"Use verbos de níveis 3-6: analisar, avaliar, criar, aplicar.",
            modulo=mod,
        ))
    # Objetivos de aprendizagem vivem no nível da trilha (molde D, bloco 1:
    # "uma frase do que vai aprender", sem lista de objetivos por aula). Aula
    # sem seção de objetivos é o esperado, então não há aviso por ausência;
    # a checagem de verbos só age quando a seção existe.

    # 9. Indicadores de andragogia
    text_lower = text.lower()
    andragogy_markers = {
        "necessidade_saber": [
            "por que", "por quê", "razão", "motivo", "necessidade",
            "problema que", "problema real", "desafio que",
        ],
        "autoconceito": [
            "considere", "analise como", "avalie se", "na sua experiência",
            "como profissional", "na sua rotina", "na sua atuação",
        ],
        "experiencia_previa": [
            "se você já", "experiência prévia", "experiência profissional",
            "no seu dia a dia", "na sua rotina", "provavelmente já",
        ],
        "prontidao": [
            "aplique hoje", "aplicar imediatamente", "uso imediato",
            "pode aplicar", "aplicação prática", "na próxima",
        ],
        "orientacao_problemas": [
            "problema real", "cenário real", "caso real",
            "situação real", "desafio real", "estudo de caso",
        ],
    }

    missing_principles = []
    for principle, markers in andragogy_markers.items():
        if not any(m in text_lower for m in markers):
            missing_principles.append(principle.replace("_", " "))

    # Desde 02/09/2026 a andragogia nunca reprova: os marcadores são
    # lexicais ("se você já", "na sua rotina") e uma aula que aplica Knowles
    # com outras palavras reprovava por não usar a fórmula. O revisor humano
    # e o analyzer (Gemini) medem o princípio; o gate só aponta.
    if missing_principles:
        erros.append(ContentError(
            tipo="warning",
            categoria="andragogia",
            mensagem=f"Princípios andragógicos fracos: {', '.join(missing_principles)}. "
                     f"Reforce a aplicação desses princípios.",
            modulo=mod,
        ))

    # 10. Parágrafos fora da faixa de 15 a 45 palavras (`tetos.D.paragrafo`).
    for line_num, palavras in _check_paragraph_length(text)[:5]:
        lado = "curto" if palavras < MIN_PARAGRAPH_WORDS else "longo"
        erros.append(ContentError(
            tipo="warning",
            categoria="formatação",
            mensagem=f"Parágrafo {lado} com {palavras} palavras próximo à linha {line_num} "
                     f"(faixa: {MIN_PARAGRAPH_WORDS} a {MAX_PARAGRAPH_WORDS}). "
                     f"Parágrafo curto demais fatia o raciocínio; longo demais costuma "
                     f"empilhar dois assuntos.",
            modulo=mod,
        ))

    # 11. Emojis
    if _has_emoji(text):
        erros.append(ContentError(
            tipo="error",
            categoria="editorial",
            mensagem="Emojis detectados no conteúdo. Proibido em conteúdo educacional.",
            modulo=mod,
        ))

    # 12. Anti-invenção: percentual sem fonte na mesma frase (aviso).
    #     Não bloqueia porque a heurística é textual e o falso positivo é
    #     barato de dispensar; bloquear aqui reprovaria conteúdo correto que
    #     cita a fonte no parágrafo anterior.
    anti_invencao = validation_section("anti_invencao")
    if bool(anti_invencao.get(
        "require_source_for_percentages", DEFAULT_REQUIRE_SOURCE_FOR_PERCENTAGES
    )):
        for linha, trecho in _check_percentages_have_source(text)[:MAX_PERCENTAGE_WARNINGS]:
            erros.append(ContentError(
                tipo="warning",
                categoria="evidencia",
                mensagem=f"Percentual sem fonte na mesma frase (linha {linha}): "
                         f"\"{trecho}\". A conferência humana exige quatro coisas: "
                         f"origem, data, método e denominador.",
                modulo=mod,
            ))

    # 13. Anti-invenção: teto de marcadores de apuração em aberto (erro).
    marcadores = _count_unresolved_markers(text)
    teto_marcadores = anti_invencao.get(
        "fail_if_unresolved_markers_above", DEFAULT_MAX_UNRESOLVED_MARKERS
    )
    try:
        teto_marcadores = int(teto_marcadores)
    except (TypeError, ValueError):
        teto_marcadores = DEFAULT_MAX_UNRESOLVED_MARKERS
    if marcadores > teto_marcadores:
        erros.append(ContentError(
            tipo="error",
            categoria="evidencia",
            mensagem=f"{marcadores} marcadores de apuração em aberto "
                     f"([FALTA EVIDÊNCIA: / [PREENCHER-HUMANO:), acima do teto de "
                     f"{teto_marcadores}. Acima do teto a peça não está pronta para "
                     f"revisão: ela está pedindo apuração.",
            modulo=mod,
        ))

    # 14. Citabilidade GEO (opt-in via client.yaml geo_2026) — ver
    #     docs/GEO_REDACAO_CHECKLIST_2026.md. Severidade depende do playbook:
    #     habilitado = erro bloqueante; desabilitado = aviso não-bloqueante.
    if geo_config is not None:
        playbook = bool(getattr(geo_config, "princeton_playbook_enabled", False))
        geo_tipo = "error" if playbook else "warning"

        min_cite = int(getattr(geo_config, "min_cite_sources", 3))
        min_stats = int(getattr(geo_config, "min_statistics", 5))
        min_quotes = int(getattr(geo_config, "min_quotations", 1))
        require_capsule = bool(getattr(geo_config, "require_answer_capsule", True))

        n_cite = _count_cite_sources(text)
        if n_cite < min_cite:
            erros.append(ContentError(
                tipo=geo_tipo,
                categoria="geo",
                mensagem=f"Cite Sources: {n_cite} fonte(s) externa(s) atribuída(s) "
                         f"(mínimo GEO: {min_cite}). Lift de citação +40% (até +115% fora do top-1).",
                modulo=mod,
            ))

        n_stats = _count_statistics(text)
        if n_stats < min_stats:
            erros.append(ContentError(
                tipo=geo_tipo,
                categoria="geo",
                mensagem=f"Statistics: {n_stats} dado(s) quantitativo(s) "
                         f"(mínimo GEO: {min_stats}). Lift de citação +32,8%.",
                modulo=mod,
            ))

        n_quotes = _count_quotations(text)
        if n_quotes < min_quotes:
            erros.append(ContentError(
                tipo=geo_tipo,
                categoria="geo",
                mensagem=f"Quotation: {n_quotes} citação(ões) direta(s) atribuída(s) "
                         f"(mínimo GEO: {min_quotes}). Citação de especialista é o maior lift, +42,6%.",
                modulo=mod,
            ))

        if require_capsule and not _has_answer_capsule(text):
            erros.append(ContentError(
                tipo=geo_tipo,
                categoria="geo",
                mensagem="Answer capsule ausente: nenhum parágrafo resposta-primeiro "
                         "(40-60 palavras) detectado após um heading. Lift de citação 1,9×.",
                modulo=mod,
            ))

    return erros


def format_report(erros: list[ContentError]) -> str:
    """Formata relatório de qualidade de conteúdo."""
    if not erros:
        return "Conteúdo: todas as verificações passaram."

    errors = [e for e in erros if e.tipo == "error"]
    warnings = [e for e in erros if e.tipo == "warning"]

    linhas = [f"Conteúdo: {len(errors)} erro(s), {len(warnings)} aviso(s):\n"]

    if errors:
        linhas.append("  ERROS (bloqueantes):")
        for e in errors:
            linhas.append(f"    [{e.categoria}] {e.mensagem}")

    if warnings:
        linhas.append("  AVISOS (não-bloqueantes):")
        for e in warnings:
            linhas.append(f"    [{e.categoria}] {e.mensagem}")

    return "\n".join(linhas)
