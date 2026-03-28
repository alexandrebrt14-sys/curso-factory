"""Verificador de acentuação PT-BR.

Detecta palavras comuns que DEVEM ter acento mas aparecem sem.
Ignora URLs, slugs, blocos de código e nomes de variáveis.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field


@dataclass
class AccentError:
    """Erro de acentuação encontrado."""
    linha: int
    palavra_errada: str
    correcao: str
    contexto: str


# Mapeamento de palavras sem acento → forma correta
# Apenas palavras que NUNCA existem sem acento no contexto educacional
ACCENT_MAP: dict[str, str] = {
    "nao": "não",
    "voce": "você",
    "tambem": "também",
    "ate": "até",
    "ja": "já",
    "so": "só",
    "apos": "após",
    "entao": "então",
    "producao": "produção",
    "informacao": "informação",
    "educacao": "educação",
    "solucao": "solução",
    "aplicacao": "aplicação",
    "funcao": "função",
    "avaliacao": "avaliação",
    "classificacao": "classificação",
    "publicacao": "publicação",
    "introducao": "introdução",
    "conclusao": "conclusão",
    "secao": "seção",
    "licao": "lição",
    "atencao": "atenção",
    "compreensao": "compreensão",
    "sera": "será",
    "esta": "está",
    "conteudo": "conteúdo",
    "modulo": "módulo",
    "topico": "tópico",
    "pratica": "prática",
    "tecnica": "técnica",
    "basico": "básico",
    "logica": "lógica",
    "pagina": "página",
    "codigo": "código",
    "metodo": "método",
    "numero": "número",
    "unico": "único",
    "valido": "válido",
    "analise": "análise",
    "possivel": "possível",
    "disponivel": "disponível",
    "util": "útil",
    "facil": "fácil",
    "dificil": "difícil",
    "necessario": "necessário",
    "obrigatorio": "obrigatório",
}

# Padrões que indicam contexto a ignorar (URLs, código, slugs)
IGNORE_PATTERNS = [
    re.compile(r"https?://\S+"),
    re.compile(r"`[^`]+`"),
    re.compile(r"```[\s\S]*?```", re.MULTILINE),
    re.compile(r"\[.*?\]\(.*?\)"),  # Links Markdown
    re.compile(r"<[^>]+>"),  # Tags HTML
]


def _mask_ignored(text: str) -> str:
    """Substitui regiões a ignorar por espaços para preservar posições."""
    masked = text
    for pattern in IGNORE_PATTERNS:
        masked = pattern.sub(lambda m: " " * len(m.group()), masked)
    return masked


def check_accents(text: str) -> list[AccentError]:
    """Verifica acentuação PT-BR no texto.

    Retorna lista de erros encontrados com linha, palavra e correção.
    """
    erros: list[AccentError] = []
    linhas = text.split("\n")

    for num_linha, linha in enumerate(linhas, start=1):
        masked = _mask_ignored(linha)
        palavras = re.findall(r"\b([a-zA-Z]+)\b", masked)
        for palavra in palavras:
            lower = palavra.lower()
            if lower in ACCENT_MAP:
                ctx_start = max(0, linha.lower().find(lower) - 20)
                ctx_end = min(len(linha), linha.lower().find(lower) + len(lower) + 20)
                erros.append(AccentError(
                    linha=num_linha,
                    palavra_errada=palavra,
                    correcao=ACCENT_MAP[lower],
                    contexto=linha[ctx_start:ctx_end].strip(),
                ))

    return erros


def format_report(erros: list[AccentError]) -> str:
    """Formata relatório de erros de acentuação."""
    if not erros:
        return "Acentuação: nenhum erro encontrado."
    linhas = [f"Acentuação: {len(erros)} erro(s) encontrado(s):\n"]
    for e in erros:
        linhas.append(
            f"  Linha {e.linha}: '{e.palavra_errada}' → '{e.correcao}' "
            f"(contexto: ...{e.contexto}...)"
        )
    return "\n".join(linhas)
