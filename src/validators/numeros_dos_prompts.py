"""Números que os prompts citam, lidos da mesma configuração que os validadores usam.

Até 27/09/2026 os prompts traziam os números escritos à mão ("até 12 palavras",
"até 25 palavras", "acima de 350 palavras", "até 28", "até 60", "3 marcadores"),
enquanto os validadores liam os mesmos números do espelho `config/lexicos.json`
e de `config/quality_rules.yaml`. Duas cópias do mesmo número divergem em
silêncio, que é o defeito que a casa já pagou em 11/08/2026. Agora o prompt só
marca o lugar (`{glosa_max_palavras}`, `{frase_max_palavras}`...) e este módulo
entrega o valor, para redação, revisão, análise e fechamento de trilha.

Origem de cada número:

| Variável | Origem |
|---|---|
| `glosa_max_palavras` | `lexicos.json > limiares.glosaMaxPalavras` |
| `titulo_max_palavras` | `lexicos.json > limiares.h1MaxPalavras` |
| `subtitulo_max_palavras` | `lexicos.json > aberturaEDistracao.subtituloMaxPalavras` |
| `h3_acima_de_palavras` | `lexicos.json > limiares.h3SoAcimaDePalavras` |
| `frase_max_palavras` | `lexicos.json > limiares.fraseMaxPalavras` |
| `frase_tolerancia_palavras` | `lexicos.json > limiares.fraseToleranciaPalavras` |
| `marcadores_max_aula` | `quality_rules.yaml > validation.anti_invencao.marcadores_por_aula_no_rascunho` |
| `fonte_max_palavras` | `quality_rules.yaml > validation.abertura.fonte_max_palavras` |

Os fallbacks abaixo são iguais aos valores da configuração em 27/09/2026 e só
entram se a chave sumir, para que o prompt nunca saia com a variável crua.
"""

from __future__ import annotations

from src.validators.lexicos_loader import carregar_lexicos, familias_de_abertura
from src.validators.rules_loader import validation_section

_FALLBACK: dict[str, int] = {
    "glosa_max_palavras": 12,
    "titulo_max_palavras": 12,
    "subtitulo_max_palavras": 25,
    "h3_acima_de_palavras": 350,
    "frase_max_palavras": 28,
    "frase_tolerancia_palavras": 60,
    "marcadores_max_aula": 3,
    "fonte_max_palavras": 25,
}

_DOS_LIMIARES = {
    "glosa_max_palavras": "glosaMaxPalavras",
    "titulo_max_palavras": "h1MaxPalavras",
    "h3_acima_de_palavras": "h3SoAcimaDePalavras",
    "frase_max_palavras": "fraseMaxPalavras",
    "frase_tolerancia_palavras": "fraseToleranciaPalavras",
}

_DO_YAML = {
    "marcadores_max_aula": ("anti_invencao", "marcadores_por_aula_no_rascunho"),
    "fonte_max_palavras": ("abertura", "fonte_max_palavras"),
}


def _positivo(valor) -> int | None:
    try:
        convertido = int(valor)
    except (TypeError, ValueError):
        return None
    return convertido if convertido > 0 else None


def numero(chave: str) -> int:
    """O número da chave, da configuração; o fallback só se ela sumir."""
    valor = None
    if chave in _DOS_LIMIARES:
        limiares = carregar_lexicos().get("limiares")
        if isinstance(limiares, dict):
            valor = _positivo(limiares.get(_DOS_LIMIARES[chave]))
    elif chave == "subtitulo_max_palavras":
        valor = _positivo(familias_de_abertura().get("subtituloMaxPalavras"))
    elif chave in _DO_YAML:
        secao, campo = _DO_YAML[chave]
        valor = _positivo(validation_section(secao).get(campo))
    return valor if valor is not None else _FALLBACK[chave]


def numeros_dos_prompts() -> dict[str, str]:
    """Todas as variáveis numéricas dos prompts, em string, prontas para substituir."""
    return {chave: str(numero(chave)) for chave in _FALLBACK}
