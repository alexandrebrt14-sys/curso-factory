"""Validador de qualidade de conteúdo educacional.

Verifica presença de tabelas, formatação rica, exercícios,
princípios andragógicos, contagem de palavras e hierarquia
de títulos — elementos obrigatórios do padrão editorial
HSM/HBR/MIT Sloan.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field


@dataclass
class ContentError:
    """Erro ou aviso de qualidade de conteúdo."""
    tipo: str  # "error" ou "warning"
    categoria: str
    mensagem: str
    modulo: str = ""


# Clichês proibidos
FORBIDDEN_CLICHES = [
    "nos dias de hoje",
    "é fundamental que",
    "não é segredo que",
    "o futuro é agora",
    "em um mundo cada vez mais",
    "vamos explorar",
    "como sabemos",
    "é importante ressaltar",
    "diante desse cenário",
    "nesse contexto",
    "vale a pena destacar",
    "em última análise",
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
    """Conta tabelas Markdown no texto."""
    # Padrão: linha com | que tem ao menos 2 colunas
    table_rows = re.findall(r"^\|.+\|.+\|", text, re.MULTILINE)
    # Agrupar linhas de tabela consecutivas
    # Uma tabela tem header + separator + rows
    separators = re.findall(r"^\|[\s:|-]+\|", text, re.MULTILINE)
    return len(separators)


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
    ]
    exercicios = []
    for pattern in patterns:
        exercicios.extend(re.findall(pattern, text))
    return exercicios


def _check_cliches(text: str) -> list[str]:
    """Encontra clichês proibidos no texto."""
    found = []
    text_lower = text.lower()
    for cliche in FORBIDDEN_CLICHES:
        if cliche.lower() in text_lower:
            found.append(cliche)
    return found


def _check_bloom_objectives(text: str) -> tuple[list[str], list[str]]:
    """Verifica verbos de Bloom nos objetivos de aprendizagem.

    Returns:
        Tupla com (verbos_proibidos_encontrados, verbos_aceitos_encontrados).
    """
    # Procurar seção de objetivos
    obj_match = re.search(
        r"(?:Objetivos?\s+de\s+Aprendizagem|OBJETIVOS?)[\s\S]*?(?=\n##|\n\*\*[A-Z]|\Z)",
        text,
        re.IGNORECASE,
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
    for level, text, raw in headings:
        if level > prev_level + 1:
            errors.append(
                f"Pulo de hierarquia: H{prev_level} → H{level} "
                f"(título: '{text[:50]}')"
            )
        prev_level = level
    return errors


def _check_paragraph_length(text: str) -> list[tuple[int, int]]:
    """Encontra parágrafos com mais de 5 linhas."""
    long_paragraphs = []
    paragraphs = text.split("\n\n")
    line_num = 1
    for para in paragraphs:
        lines = para.strip().split("\n")
        # Ignorar blocos de código, tabelas, listas
        if para.strip().startswith(("```", "|", "- ", "* ", "1.", ">", "#")):
            line_num += len(lines) + 1
            continue
        if len(lines) > 5:
            long_paragraphs.append((line_num, len(lines)))
        line_num += len(lines) + 1
    return long_paragraphs


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


def check_content(text: str, module_name: str = "") -> list[ContentError]:
    """Valida qualidade de conteúdo educacional.

    Verifica: tabelas, formatação, exercícios, andragogia,
    contagem de palavras, hierarquia de títulos, clichês,
    verbos de Bloom e emojis.

    Returns:
        Lista de erros e avisos encontrados.
    """
    erros: list[ContentError] = []
    mod = module_name or "módulo"

    # 1. Contagem de palavras
    word_count = _count_words(text)
    if word_count < 2500:
        erros.append(ContentError(
            tipo="error",
            categoria="profundidade",
            mensagem=f"Módulo com apenas {word_count} palavras (mínimo: 2.500). "
                     f"Conteúdo insuficiente para padrão editorial HSM/HBR.",
            modulo=mod,
        ))
    elif word_count < 3000:
        erros.append(ContentError(
            tipo="warning",
            categoria="profundidade",
            mensagem=f"Módulo com {word_count} palavras (recomendado: 3.000-4.000). "
                     f"Considere aprofundar a análise.",
            modulo=mod,
        ))
    elif word_count > 4500:
        erros.append(ContentError(
            tipo="warning",
            categoria="profundidade",
            mensagem=f"Módulo com {word_count} palavras (máximo recomendado: 4.000). "
                     f"Considere dividir em submódulos.",
            modulo=mod,
        ))

    # 2. Tabelas obrigatórias
    table_count = _find_tables(text)
    if table_count == 0:
        erros.append(ContentError(
            tipo="error",
            categoria="formatação",
            mensagem="Nenhuma tabela encontrada. "
                     "Cada módulo DEVE ter ao menos 1 tabela comparativa.",
            modulo=mod,
        ))
    elif table_count < 1:
        erros.append(ContentError(
            tipo="warning",
            categoria="formatação",
            mensagem=f"Apenas {table_count} tabela(s). Recomendado: 1-3 por módulo.",
            modulo=mod,
        ))

    # 3. Hierarquia de títulos
    headings = _find_headings(text)
    if len(headings) < 3:
        erros.append(ContentError(
            tipo="error",
            categoria="formatação",
            mensagem=f"Apenas {len(headings)} subtítulos. "
                     f"O módulo deve ter ao menos 5-7 seções semânticas (H2/H3).",
            modulo=mod,
        ))

    hierarchy_errors = _check_heading_hierarchy(headings)
    for err in hierarchy_errors:
        erros.append(ContentError(
            tipo="error",
            categoria="formatação",
            mensagem=err,
            modulo=mod,
        ))

    # 4. Blocos de citação para insights
    blockquote_count = _find_blockquotes(text)
    if blockquote_count == 0:
        erros.append(ContentError(
            tipo="error",
            categoria="formatação",
            mensagem="Nenhum bloco de citação (>) encontrado. "
                     "Use blocos de citação para insights centrais e conceitos memoráveis.",
            modulo=mod,
        ))

    # 5. Termos em negrito
    bold_count = _find_bold_terms(text)
    if bold_count < 3:
        erros.append(ContentError(
            tipo="warning",
            categoria="formatação",
            mensagem=f"Apenas {bold_count} termos em negrito. "
                     f"Destaque termos-chave e conceitos na primeira ocorrência.",
            modulo=mod,
        ))

    # 6. Exercícios
    exercises = _find_exercises(text)
    if len(exercises) < 3:
        erros.append(ContentError(
            tipo="error",
            categoria="exercícios",
            mensagem=f"Apenas {len(exercises)} exercício(s) detectado(s) "
                     f"(mínimo: 3 por módulo com progressão de complexidade).",
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
    if not bloom_aceitos and not bloom_proibidos:
        erros.append(ContentError(
            tipo="warning",
            categoria="andragogia",
            mensagem="Seção de Objetivos de Aprendizagem não encontrada ou sem verbos de Bloom.",
            modulo=mod,
        ))

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

    if len(missing_principles) >= 3:
        erros.append(ContentError(
            tipo="error",
            categoria="andragogia",
            mensagem=f"Princípios andragógicos ausentes ({len(missing_principles)}): "
                     f"{', '.join(missing_principles)}. "
                     f"O conteúdo deve aplicar os 6 princípios de Knowles.",
            modulo=mod,
        ))
    elif missing_principles:
        erros.append(ContentError(
            tipo="warning",
            categoria="andragogia",
            mensagem=f"Princípios andragógicos fracos: {', '.join(missing_principles)}. "
                     f"Reforce a aplicação desses princípios.",
            modulo=mod,
        ))

    # 10. Parágrafos longos
    long_paras = _check_paragraph_length(text)
    for line_num, line_count in long_paras[:3]:  # Limitar a 3 avisos
        erros.append(ContentError(
            tipo="warning",
            categoria="formatação",
            mensagem=f"Parágrafo com {line_count} linhas próximo à linha {line_num} "
                     f"(máximo: 5 linhas por parágrafo).",
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
