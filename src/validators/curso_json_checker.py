"""Validação de um curso em JSON no formato do portal /educacao (14/10/2026).

Desde a reorganização do `landing-page-geo` (PR #1409, piloto; #1421 e #1425,
primeiros cursos migrados), o conteúdo de cada curso mora em
`src/content/cursos/<slug>.json`: um array de `Step`, validado no portal pelo
schema zod de `src/lib/educacao/conteudo/schema.ts`. Este módulo espelha esse
schema (`config/schema-curso.json`) e acrescenta os limites que o portal cobra
depois, no CI ou no gate pós-build, para que a reprovação apareça aqui, antes
do PR lá:

- estrutura e campos (objetos estritos: campo desconhecido reprova);
- ids únicos, em ASCII minúsculo com hífen (o id vira âncora e URL do capítulo);
- tamanho por capítulo e do curso, derivado do teto de 900 KB de HTML por
  página (`scripts/gate-peso-html-cursos.mjs`) e das medidas dos cursos migrados;
- bloco `code` com `language` conhecida pelo realce (Shiki) do portal;
- acentuação PT-BR em texto de leitura (até 20 ocorrências, como no portal);
- zero emoji (mesmas faixas de `scripts/ci/lint-emoji.mjs`);
- ícone conhecido, apoios visuais por capítulo e padrões de escrita proibidos
  pelo dono (12/10/2026), como aviso.

Os números vivem em `config/quality_rules.yaml > validation.curso_json`.
"""

from __future__ import annotations

import json
import re
import unicodedata
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from src.validators.accent_checker import check_accents
from src.validators.rules_loader import validation_section

SCHEMA_PATH = Path(__file__).resolve().parent.parent.parent / "config" / "schema-curso.json"

#: Tipos de seção do portal, na ordem de `SECTION_TYPES` (schema.ts, 14/10/2026).
SECTION_TYPES: tuple[str, ...] = (
    "text", "code", "warning", "tip", "checkpoint", "figure", "callout", "diagram", "flow",
    "mockup", "prompt", "matrix", "comparison", "statGrid", "useCase", "metaphor", "glossary",
    "quote", "bullets", "timeline", "dataTable", "resourceLesson", "checklist", "calculator",
    "decisionCase", "quizInline", "accordion", "template", "sourceNote", "fontes", "tabs",
    "slides", "tipCard", "stepGuide", "codeDownload", "mediaPlayer", "visualLab",
    "frontendLab", "liveLab",
)  # fmt: skip

#: Figuras (imagem ou SVG). O teto editorial `tetos.D.figuras_max` conta só
#: figuras; tabela, comparativo e passo a passo são apoio sem cota (draft.md).
FIGURAS: frozenset[str] = frozenset({"figure", "diagram", "mockup"})

STEP_CAMPOS = {
    "legacyIds",
    "id",
    "title",
    "duration",
    "icon",
    "description",
    "content",
    "faq",
    "contentDeferred",
}
STEP_OBRIGATORIOS = ("id", "title", "duration", "icon", "description", "content")
SECTION_CAMPOS = {"type", "value", "language", "codeHtml", "label", "title", "data"}
ID_RE = re.compile(r"^[a-z0-9-]+$")

# Faixas de scripts/ci/lint-emoji.mjs. Na faixa U+2600–U+27BF o portal isenta
# sinais tipográficos de uso corrente em prosa e interface; a lista abaixo é a
# interseção segura (setas e marcas de verificação em texto). Qualquer um deles
# seguido de U+FE0F volta a reprovar.
_EMOJI_RE = re.compile("[\U0001f300-\U0001faff]|️")
_DINGBATS_RE = re.compile("[☀-➿]")
_DINGBATS_ISENTOS = frozenset("✓✔✗✘✦✳✴➔➡✖✅")

DEFAULTS: dict[str, Any] = {
    "capitulo_aberto_aviso_chars": 60_000,
    "capitulo_aberto_erro_chars": 72_000,
    "capitulo_aviso_chars": 80_000,
    "capitulo_erro_chars": 110_000,
    "curso_aviso_chars": 1_200_000,
    "arquivo_aviso_bytes": 1_500_000,
    "acentos_max_ocorrencias": 20,
    "acentos_max_ocorrencias_pr_grande": 80,
    "acentos_pr_grande_linhas": 1000,
    "figuras_max_por_capitulo": 3,
    "linguagens_de_codigo": [
        "bash",
        "sh",
        "shell",
        "console",
        "terminal",
        "javascript",
        "js",
        "typescript",
        "ts",
        "tsx",
        "jsx",
        "json",
        "yaml",
        "yml",
        "markdown",
        "md",
        "html",
        "htm",
        "css",
        "python",
        "sql",
        "toml",
        "csv",
        "text",
    ],  # fmt: skip
    "icones": [],
    "padroes_de_escrita_proibidos": [],
}


@dataclass
class Achado:
    """Um problema encontrado. `nivel` é "erro" (reprova) ou "aviso"."""

    nivel: str
    regra: str
    caminho: str
    mensagem: str

    def __str__(self) -> str:
        return f"[{self.nivel}] {self.regra} em {self.caminho}: {self.mensagem}"


@dataclass
class Resultado:
    achados: list[Achado] = field(default_factory=list)
    medidas: dict[str, Any] = field(default_factory=dict)

    @property
    def erros(self) -> list[Achado]:
        return [a for a in self.achados if a.nivel == "erro"]

    @property
    def avisos(self) -> list[Achado]:
        return [a for a in self.achados if a.nivel == "aviso"]

    @property
    def aprovado(self) -> bool:
        return not self.erros

    def erro(self, regra: str, caminho: str, mensagem: str) -> None:
        self.achados.append(Achado("erro", regra, caminho, mensagem))

    def aviso(self, regra: str, caminho: str, mensagem: str) -> None:
        self.achados.append(Achado("aviso", regra, caminho, mensagem))


def carregar_limites(sobrescrever: dict[str, Any] | None = None) -> dict[str, Any]:
    """Limites de `validation.curso_json`, com os defaults do módulo por baixo."""
    limites = dict(DEFAULTS)
    secao = validation_section("curso_json")
    for chave in DEFAULTS:
        if chave in secao and secao[chave] is not None:
            limites[chave] = secao[chave]
    if sobrescrever:
        limites.update({k: v for k, v in sobrescrever.items() if v is not None})
    return limites


def carregar_schema() -> dict[str, Any]:
    """Lê o espelho `config/schema-curso.json` (metadados de origem incluídos)."""
    return json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))


# ─── estrutura (espelho do zod) ──────────────────────────────────────


def _e_valor_json(valor: Any, caminho: str, res: Resultado) -> None:
    """`data` só aceita o que JSON.parse devolve; float não finito reprova."""
    if isinstance(valor, bool) or valor is None or isinstance(valor, str):
        return
    if isinstance(valor, int):
        return
    if isinstance(valor, float):
        if valor != valor or valor in (float("inf"), float("-inf")):
            res.erro("schema", caminho, "número não finito (NaN ou Infinity) não cabe em JSON")
        return
    if isinstance(valor, list):
        for i, item in enumerate(valor):
            _e_valor_json(item, f"{caminho}[{i}]", res)
        return
    if isinstance(valor, dict):
        for chave, item in valor.items():
            if not isinstance(chave, str):
                res.erro("schema", caminho, f"chave de objeto não é string: {chave!r}")
            _e_valor_json(item, f"{caminho}.{chave}", res)
        return
    res.erro("schema", caminho, f"valor de tipo {type(valor).__name__} não cabe em JSON")


def _checar_secao(secao: Any, caminho: str, res: Resultado) -> None:
    if not isinstance(secao, dict):
        res.erro("schema", caminho, "seção precisa ser objeto")
        return
    desconhecidos = sorted(set(secao) - SECTION_CAMPOS)
    if desconhecidos:
        res.erro(
            "schema",
            caminho,
            f"campo desconhecido em seção (objeto estrito): {', '.join(desconhecidos)}",
        )
    tipo = secao.get("type")
    if tipo not in SECTION_TYPES:
        res.erro("schema", f"{caminho}.type", f"tipo de seção inválido: {tipo!r}")
    if not isinstance(secao.get("value"), str):
        res.erro("schema", f"{caminho}.value", "value é obrigatório e precisa ser string")
    for campo in ("language", "codeHtml", "label", "title"):
        if campo in secao and not isinstance(secao[campo], str):
            res.erro("schema", f"{caminho}.{campo}", "precisa ser string quando presente")
    if "data" in secao:
        _e_valor_json(secao["data"], f"{caminho}.data", res)


def _checar_step(step: Any, caminho: str, res: Resultado) -> None:
    if not isinstance(step, dict):
        res.erro("schema", caminho, "capítulo precisa ser objeto")
        return
    desconhecidos = sorted(set(step) - STEP_CAMPOS)
    if desconhecidos:
        res.erro(
            "schema",
            caminho,
            f"campo desconhecido em Step (objeto estrito): {', '.join(desconhecidos)}",
        )
    for campo in STEP_OBRIGATORIOS:
        if campo not in step:
            res.erro("schema", f"{caminho}.{campo}", "campo obrigatório ausente")
    for campo in ("id", "title", "icon"):
        valor = step.get(campo)
        if campo in step and (not isinstance(valor, str) or not valor):
            res.erro("schema", f"{caminho}.{campo}", "precisa ser string não vazia")
    for campo in ("duration", "description"):
        if campo in step and not isinstance(step[campo], str):
            res.erro("schema", f"{caminho}.{campo}", "precisa ser string")
    if "legacyIds" in step and not (
        isinstance(step["legacyIds"], list) and all(isinstance(x, str) for x in step["legacyIds"])
    ):
        res.erro("schema", f"{caminho}.legacyIds", "precisa ser lista de strings")
    if "contentDeferred" in step and not isinstance(step["contentDeferred"], bool):
        res.erro("schema", f"{caminho}.contentDeferred", "precisa ser booleano")
    if "faq" in step:
        if not isinstance(step["faq"], list):
            res.erro("schema", f"{caminho}.faq", "precisa ser lista")
        else:
            for i, item in enumerate(step["faq"]):
                if not isinstance(item, dict) or set(item) != {"q", "a"}:
                    res.erro("schema", f"{caminho}.faq[{i}]", "item de FAQ é exatamente {q, a}")
                elif not all(isinstance(item[k], str) for k in ("q", "a")):
                    res.erro("schema", f"{caminho}.faq[{i}]", "q e a precisam ser strings")
    conteudo = step.get("content")
    if not isinstance(conteudo, list):
        if "content" in step:
            res.erro("schema", f"{caminho}.content", "precisa ser lista de seções")
        return
    for i, secao in enumerate(conteudo):
        _checar_secao(secao, f"{caminho}.content[{i}]", res)


def checar_estrutura(curso: Any, res: Resultado) -> None:
    """Reprova o que o `CursoJsonSchema` do portal reprovaria."""
    if not isinstance(curso, list) or not curso:
        res.erro("schema", "(raiz)", "curso precisa ser um array com pelo menos um capítulo")
        return
    vistos: set[str] = set()
    for i, step in enumerate(curso):
        caminho = f"[{i}]"
        _checar_step(step, caminho, res)
        if isinstance(step, dict) and isinstance(step.get("id"), str):
            if step["id"] in vistos:
                res.erro("ids-unicos", f"{caminho}.id", f"id de capítulo repetido: {step['id']}")
            vistos.add(step["id"])


# ─── limites do portal ───────────────────────────────────────────────


def _chars_da_secao(secao: dict[str, Any]) -> int:
    n = len(secao.get("value") or "")
    if "data" in secao:
        n += len(json.dumps(secao["data"], ensure_ascii=False))
    for campo in ("label", "title"):
        n += len(secao.get(campo) or "")
    return n


def chars_do_capitulo(step: dict[str, Any]) -> int:
    """Caracteres de conteúdo do capítulo: `value`, `data`, rótulos, título e descrição."""
    conteudo = step.get("content") if isinstance(step.get("content"), list) else []
    n = sum(_chars_da_secao(s) for s in conteudo if isinstance(s, dict))
    n += len(step.get("title") or "") + len(step.get("description") or "")
    return n


def _textos_de_leitura(step: dict[str, Any]) -> list[tuple[str, str]]:
    """Pares (caminho, texto) do que o leitor vê, sem blocos de código."""
    pares = [("title", step.get("title") or ""), ("description", step.get("description") or "")]
    conteudo = step.get("content") if isinstance(step.get("content"), list) else []
    for i, secao in enumerate(conteudo):
        if not isinstance(secao, dict) or secao.get("type") == "code":
            continue
        if isinstance(secao.get("value"), str):
            pares.append((f"content[{i}].value", secao["value"]))
        if "data" in secao:
            pares.append((f"content[{i}].data", _strings_do_json(secao["data"])))
    for i, item in enumerate(step.get("faq") or []):
        if isinstance(item, dict):
            pares.append((f"faq[{i}]", f"{item.get('q', '')}\n{item.get('a', '')}"))
    return pares


def _strings_do_json(valor: Any) -> str:
    if isinstance(valor, str):
        return valor
    if isinstance(valor, list):
        return "\n".join(_strings_do_json(v) for v in valor)
    if isinstance(valor, dict):
        return "\n".join(_strings_do_json(v) for v in valor.values())
    return ""


_TOKEN_TECNICO_RE = re.compile(r"\S*[/_.\\-]\S*|`[^`]*`|https?://\S+")


def _sem_html(texto: str) -> str:
    """Tira tags (SVG inline e `<img>` chegam como HTML em `value`)."""
    return re.sub(r"<[^>]+>", " ", texto)


def _so_leitura(texto: str) -> str:
    """Mascara o que o guarda do portal também ignora: slug, caminho, id com
    hífen, URL e código entre crases. Sobra o texto de leitura."""
    return _TOKEN_TECNICO_RE.sub(" ", _sem_html(texto))


def _acentos(texto: str):
    """Palavras sem acento no texto de leitura; sigla em caixa alta (AI, SO) não conta."""
    return [e for e in check_accents(_so_leitura(texto)) if not e.palavra_errada.isupper()]


def _tem_emoji(texto: str) -> bool:
    if _EMOJI_RE.search(texto):
        return True
    for m in _DINGBATS_RE.finditer(texto):
        if m.group(0) not in _DINGBATS_ISENTOS:
            return True
    return False


def _sem_acento(texto: str) -> str:
    return "".join(
        c for c in unicodedata.normalize("NFD", texto) if unicodedata.category(c) != "Mn"
    )


def checar_limites(curso: list[dict[str, Any]], res: Resultado, limites: dict[str, Any]) -> None:
    """Tamanho, ids, linguagem, acentos, emoji, ícone, visuais e escrita."""
    linguagens = {str(x).lower() for x in limites["linguagens_de_codigo"]}
    icones = {str(x) for x in limites["icones"]}
    proibidos = [str(p).lower() for p in limites["padroes_de_escrita_proibidos"]]
    acentos_total = 0
    total_chars = 0
    por_capitulo: list[dict[str, Any]] = []

    for i, step in enumerate(curso):
        if not isinstance(step, dict):
            continue
        caminho = f"[{i}]"
        sid = step.get("id") if isinstance(step.get("id"), str) else ""

        if sid and not ID_RE.match(sid):
            res.erro(
                "id-ascii",
                f"{caminho}.id",
                f"id '{sid}' precisa ser ASCII minúsculo com hífen: ele vira âncora e URL do capítulo",
            )
        if icones and isinstance(step.get("icon"), str) and step["icon"] not in icones:
            res.aviso(
                "icone",
                f"{caminho}.icon",
                f"ícone '{step['icon']}' não está em courseIcons.tsx (lista de 14/10/2026)",
            )
        if isinstance(step.get("duration"), str) and not re.match(r"^\d+ min$", step["duration"]):
            res.aviso(
                "duration",
                f"{caminho}.duration",
                f"duração '{step['duration']}' fora do formato 'NN min'",
            )

        n = chars_do_capitulo(step)
        total_chars += n
        por_capitulo.append({"id": sid, "chars": n})
        if i == 0:
            if n > limites["capitulo_aberto_erro_chars"]:
                res.erro(
                    "peso-capitulo-aberto",
                    caminho,
                    f"{n:,} caracteres no capítulo que a página entrega aberto; acima de "
                    f"{limites['capitulo_aberto_erro_chars']:,} a página passa do teto de 900 KB de HTML".replace(
                        ",", "."
                    ),
                )
            elif n > limites["capitulo_aberto_aviso_chars"]:
                res.aviso(
                    "peso-capitulo-aberto",
                    caminho,
                    f"{n:,} caracteres no capítulo aberto (aviso a partir de {limites['capitulo_aberto_aviso_chars']:,})".replace(
                        ",", "."
                    ),
                )
        else:
            if n > limites["capitulo_erro_chars"]:
                res.erro(
                    "peso-capitulo",
                    caminho,
                    f"{n:,} caracteres; acima de {limites['capitulo_erro_chars']:,} a URL do capítulo e o conteudo.json ficam pesados demais".replace(
                        ",", "."
                    ),
                )
            elif n > limites["capitulo_aviso_chars"]:
                res.aviso(
                    "peso-capitulo",
                    caminho,
                    f"{n:,} caracteres (aviso a partir de {limites['capitulo_aviso_chars']:,})".replace(
                        ",", "."
                    ),
                )

        conteudo = step.get("content") if isinstance(step.get("content"), list) else []
        visuais = 0
        for j, secao in enumerate(conteudo):
            if not isinstance(secao, dict):
                continue
            cam = f"{caminho}.content[{j}]"
            tipo = secao.get("type")
            if tipo == "code":
                lang = secao.get("language")
                if not lang:
                    res.erro(
                        "code-language",
                        cam,
                        "bloco de código sem `language`; o realce do portal precisa dela",
                    )
                elif str(lang).lower() not in linguagens:
                    res.aviso(
                        "code-language",
                        cam,
                        f"linguagem '{lang}' não está na lista do realce; o Shiki trata como texto sem cor",
                    )
            if tipo in FIGURAS:
                visuais += 1
            if tipo == "codeHtml" or "codeHtml" in secao:
                res.aviso(
                    "code-html", cam, "codeHtml é acrescentado pelo servidor; não emita no JSON"
                )
        if visuais > limites["figuras_max_por_capitulo"]:
            res.aviso(
                "figuras",
                caminho,
                f"{visuais} figuras no capítulo; o teto editorial (tetos.D.figuras_max) é {limites['figuras_max_por_capitulo']}",
            )
        if step.get("contentDeferred") is not None:
            res.aviso(
                "content-deferred",
                f"{caminho}.contentDeferred",
                "marca do corpo sob demanda é acrescentada pelo servidor; não emita no JSON",
            )

        for cam, texto in _textos_de_leitura(step):
            limpo = _sem_html(texto)
            if _tem_emoji(limpo):
                res.erro(
                    "emoji",
                    f"{caminho}.{cam}",
                    "emoji em texto de leitura (gate lint-emoji do portal)",
                )
            ocorrencias = _acentos(texto)
            if ocorrencias:
                acentos_total += len(ocorrencias)
                exemplo = ocorrencias[0]
                res.aviso(
                    "acentos",
                    f"{caminho}.{cam}",
                    f"{len(ocorrencias)} palavra(s) sem acento, ex.: '{exemplo.palavra_errada}' -> '{exemplo.correcao}'",
                )
            baixo = _sem_acento(limpo.lower())
            for padrao in proibidos:
                if _sem_acento(padrao) in baixo:
                    res.aviso(
                        "escrita",
                        f"{caminho}.{cam}",
                        f'padrão proibido pela regra de escrita de 12/10/2026: "{padrao}"',
                    )

    # Mesma regra do portal (11/10/2026): 20 ocorrências; 80 quando a mudança
    # verificada tem 1.000 linhas ou mais, o que todo curso novo tem.
    linhas = limites.get("_linhas_do_arquivo") or 0
    teto_acentos = (
        limites["acentos_max_ocorrencias_pr_grande"]
        if linhas >= limites["acentos_pr_grande_linhas"]
        else limites["acentos_max_ocorrencias"]
    )
    res.medidas["acentos_teto"] = teto_acentos
    if acentos_total > teto_acentos:
        res.erro(
            "acentos",
            "(curso)",
            f"{acentos_total} palavras sem acento; o portal reprova acima de {teto_acentos}",
        )
    if total_chars > limites["curso_aviso_chars"]:
        res.aviso(
            "peso-curso",
            "(curso)",
            f"{total_chars:,} caracteres no curso inteiro (aviso a partir de {limites['curso_aviso_chars']:,})".replace(
                ",", "."
            ),
        )

    res.medidas.update(
        {
            "capitulos": len(curso),
            "chars_total": total_chars,
            "chars_capitulo_aberto": por_capitulo[0]["chars"] if por_capitulo else 0,
            "chars_capitulo_max": max((c["chars"] for c in por_capitulo), default=0),
            "acentos": acentos_total,
            "por_capitulo": por_capitulo,
        }
    )


def checar_glossario(glossario: Any, curso: list[dict[str, Any]], res: Resultado) -> None:
    """Sidecar `<slug>.glossario.json`: id da aula -> [{term, def}], só ids do curso."""
    if not isinstance(glossario, dict):
        res.erro("glossario", "(glossário)", "o sidecar precisa ser um objeto id da aula -> termos")
        return
    ids = {s.get("id") for s in curso if isinstance(s, dict)}
    for aula, termos in glossario.items():
        if aula not in ids:
            res.erro("glossario", f"(glossário).{aula}", "termos de aula que não existe no curso")
        if not isinstance(termos, list):
            res.erro("glossario", f"(glossário).{aula}", "precisa ser lista de {term, def}")
            continue
        for i, termo in enumerate(termos):
            if not isinstance(termo, dict) or set(termo) != {"term", "def"}:
                res.erro("glossario", f"(glossário).{aula}[{i}]", "termo é exatamente {term, def}")
            elif not (
                isinstance(termo["term"], str)
                and termo["term"]
                and isinstance(termo["def"], str)
                and termo["def"]
            ):
                res.erro(
                    "glossario",
                    f"(glossário).{aula}[{i}]",
                    "term e def precisam ser strings não vazias",
                )


# ─── contrato de qualidade do curso (14/10/2026) ─────────────────────

#: Rótulo que os guias práticos levam no portal (PR #1332: abas "Funções",
#: "Casos de uso" e "Aplicações" por capítulo, com prompt e saída).
_GUIA_RE = re.compile(r"guia pr[aá]tico", re.IGNORECASE)
_PROMPT_E_SAIDA_RE = re.compile(r"prompt.*sa[ií]da|sa[ií]da.*prompt", re.IGNORECASE | re.DOTALL)
_EXEMPLO_REAL = frozenset({"useCase", "decisionCase", "stepGuide", "dataTable", "statGrid"})


def checar_contrato(
    curso: list[dict[str, Any]],
    glossario: Any | None,
    res: Resultado,
    *,
    min_capitulos: int | None = None,
    midia_capitulo_1: bool = False,
    glossario_obrigatorio: bool = False,
    guia_por_capitulo: bool = False,
) -> None:
    """Requisitos de qualidade além do formato, os mesmos que o portal e o
    curso-factory já cobram: piso de capítulos do contrato, mídia do capítulo 1
    (NotebookLM: `mediaPlayer`), glossário por aula, guia prático com prompt e
    saída por capítulo, figura e exemplo real em cada capítulo.
    """
    if min_capitulos and len(curso) < min_capitulos:
        res.erro(
            "contrato-capitulos",
            "(curso)",
            f"{len(curso)} capítulos; o contrato pede pelo menos {min_capitulos}",
        )
    primeiro = curso[0] if curso and isinstance(curso[0], dict) else {}
    tipos_cap1 = {s.get("type") for s in primeiro.get("content", []) if isinstance(s, dict)}
    if midia_capitulo_1 and "mediaPlayer" not in tipos_cap1:
        res.erro(
            "contrato-midia-cap1",
            "[0]",
            "o capítulo 1 precisa do bloco mediaPlayer (vídeo e podcast do NotebookLM)",
        )
    if glossario_obrigatorio:
        if not isinstance(glossario, dict) or not glossario:
            res.erro(
                "contrato-glossario",
                "(glossário)",
                "sidecar <slug>.glossario.json ausente ou vazio",
            )
        else:
            sem_termos = [
                s.get("id") for s in curso if isinstance(s, dict) and not glossario.get(s.get("id"))
            ]
            if sem_termos:
                res.aviso(
                    "contrato-glossario",
                    "(glossário)",
                    f"{len(sem_termos)} capítulo(s) sem termo no glossário: {', '.join(map(str, sem_termos[:5]))}",
                )
    for i, step in enumerate(curso):
        if not isinstance(step, dict):
            continue
        conteudo = [s for s in step.get("content", []) if isinstance(s, dict)]
        tipos = {s.get("type") for s in conteudo}
        texto = "\n".join(_strings_do_json(s) for s in conteudo)
        if guia_por_capitulo:
            tem_guia = any(
                _GUIA_RE.search(
                    (s.get("label") or "")
                    + " "
                    + (s.get("title") or "")
                    + " "
                    + (s.get("value") or "")[:200]
                )
                for s in conteudo
            )
            if not tem_guia:
                res.aviso(
                    "contrato-guia",
                    f"[{i}]",
                    "capítulo sem guia prático (bloco rotulado 'Guia prático', com prompt e saída)",
                )
            elif not _PROMPT_E_SAIDA_RE.search(texto):
                res.aviso(
                    "contrato-guia", f"[{i}]", "guia prático sem prompt e saída reproduzíveis"
                )
        if not (tipos & FIGURAS):
            res.aviso(
                "contrato-figura",
                f"[{i}]",
                "capítulo sem figura (SVG autoral ou imagem com legenda que afirma)",
            )
        if not (tipos & _EXEMPLO_REAL):
            res.aviso(
                "contrato-exemplo",
                f"[{i}]",
                "capítulo sem exemplo real (useCase, decisionCase, stepGuide, dataTable ou statGrid)",
            )


# ─── entrada única ───────────────────────────────────────────────────


def validar_curso(
    curso: Any,
    *,
    glossario: Any | None = None,
    tamanho_arquivo: int | None = None,
    linhas: int | None = None,
    limites: dict[str, Any] | None = None,
    contrato: dict[str, Any] | None = None,
) -> Resultado:
    """Valida um curso já carregado (lista de Steps) e, se houver, o glossário.

    `linhas` é o número de linhas do arquivo gravado (indentação de 2 espaços,
    como o portal grava): decide se vale o teto de acentos de PR grande. Sem
    ele, vale o teto de 20.
    """
    lim = carregar_limites(limites)
    if linhas is not None:
        lim["_linhas_do_arquivo"] = linhas
    res = Resultado()
    checar_estrutura(curso, res)
    if isinstance(curso, list) and curso:
        checar_limites(curso, res, lim)
        if glossario is not None:
            checar_glossario(glossario, curso, res)
        if contrato:
            checar_contrato(curso, glossario, res, **contrato)
    if tamanho_arquivo is not None:
        res.medidas["bytes_arquivo"] = tamanho_arquivo
        if tamanho_arquivo > lim["arquivo_aviso_bytes"]:
            res.aviso(
                "peso-arquivo",
                "(arquivo)",
                f"{tamanho_arquivo:,} bytes de JSON (aviso a partir de {lim['arquivo_aviso_bytes']:,})".replace(
                    ",", "."
                ),
            )
    return res


def validar_arquivo(
    caminho: Path, *, limites: dict[str, Any] | None = None, contrato: dict[str, Any] | None = None
) -> Resultado:
    """Valida `<slug>.json` e, se existir ao lado, `<slug>.glossario.json`."""
    caminho = Path(caminho)
    try:
        bruto = caminho.read_bytes()
        curso = json.loads(bruto.decode("utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        res = Resultado()
        res.erro("arquivo", str(caminho), f"não consegui ler o JSON: {exc}")
        return res
    glossario = None
    sidecar = caminho.with_name(caminho.name[: -len(".json")] + ".glossario.json")
    if sidecar.is_file():
        try:
            glossario = json.loads(sidecar.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            res = Resultado()
            res.erro("glossario", str(sidecar), f"não consegui ler o sidecar: {exc}")
            return res
    linhas = bruto.count(b"\n") + 1
    return validar_curso(
        curso,
        glossario=glossario,
        tamanho_arquivo=len(bruto),
        linhas=linhas,
        limites=limites,
        contrato=contrato,
    )


def formatar(res: Resultado, *, nome: str = "") -> str:
    """Relatório em texto, erros antes dos avisos, com as medidas no fim."""
    linhas: list[str] = []
    titulo = f"Curso {nome}" if nome else "Curso"
    linhas.append(
        f"{titulo}: {'APROVADO' if res.aprovado else 'REPROVADO'} ({len(res.erros)} erro(s), {len(res.avisos)} aviso(s))"
    )
    for a in res.erros + res.avisos:
        linhas.append(f"  {a}")
    m = res.medidas
    if m:
        linhas.append(
            "  medidas: {cap} capítulos; {tot} caracteres; capítulo aberto {ab}; maior capítulo {mx}; {ac} palavras sem acento".format(
                cap=m.get("capitulos", 0),
                tot=f"{m.get('chars_total', 0):,}".replace(",", "."),
                ab=f"{m.get('chars_capitulo_aberto', 0):,}".replace(",", "."),
                mx=f"{m.get('chars_capitulo_max', 0):,}".replace(",", "."),
                ac=m.get("acentos", 0),
            )
        )
        if "bytes_arquivo" in m:
            linhas.append(f"  arquivo: {m['bytes_arquivo']:,} bytes".replace(",", "."))
    return "\n".join(linhas)
