"""Didática das superfícies que a régua de forma não mede (22/09/2026).

Pedido do dono: a aula passa na régua de máquina (extensão, parágrafo, frase,
jargão glosado, peso visual) e ainda assim sai picada, com registro de ficha
técnica nas superfícies que o redator não reescreve. A auditoria de 22/09/2026
sobre o curso de frontends e sobre os portais mediu cinco defeitos que nenhum
verificador da casa cobrava:

1. **Fichas de recurso** num registro diferente da aula: sem "você", nome de
   API cru sem glosa, terceiro parágrafo aberto sempre por "Confira" ou "Teste"
   e conferência que é fuga ("confira na versão instalada").
2. **Paredão por acúmulo**: dezenas de fichas de mesma forma, uma atrás da
   outra, sem frase que ligue uma à seguinte.
3. **Capítulo colado**: aulas justapostas sob um subtítulo, sem frase de
   passagem; e fecho que resume em vez de mandar fazer.
4. **Tique de promessa**: descrição que começa sempre com "Você sai" e empilha
   quatro promessas numa corrente de vírgulas; título de aula que é índice de
   técnico (dois-pontos, substantivos empilhados, jargão que a aula ainda vai
   ensinar).
5. **Cadência de parágrafo**: centenas de parágrafos abrindo com "O" ou "A" e
   parágrafos vizinhos abrindo com a mesma palavra, o que a fonte já proíbe
   (§3 da diretriz) e nenhum gate media.

Este módulo mede os cinco. Quase tudo é AVISO, porque didática se julga lendo;
vira ERRO só o que é tique comprovado: três parágrafos seguidos com a mesma
primeira palavra, a mesma fórmula de subtítulo em três módulos do mesmo curso
e a conferência de ficha que manda o aluno "consultar a documentação".

Os números vivem em `config/quality_rules.yaml > validation.didatica`, lidos
em runtime; a janela de glosa e o teto de palavras do título vêm de
`config/lexicos.json` (`limiares`), espelho da fonte de estilo. Nenhum literal
aqui é a régua: as constantes `_PADRAO_*` são fallback para configuração
ausente, como nos demais validadores.

Superfícies:

- `check_didatica(texto)` mede o Markdown de UMA aula (título H1, subtítulo,
  parágrafos, fecho, jargão, versões).
- `check_subtitulos(descricoes)` mede a lista de subtítulos de um módulo ou
  curso e pega a fórmula repetida.
- `check_fichas(fichas)` mede uma sequência de fichas (explicação, exemplo,
  conferência), o que no `landing-page-geo` é o bloco `resourceLesson` e aqui
  é qualquer sequência de blocos auxiliares (tip, warning, stepGuide).
- `check_didatica_definicao(course)` roda as três sobre o `CourseDefinition`
  montado, antes de renderizar.
"""

from __future__ import annotations

import re
import unicodedata
from collections import Counter
from dataclasses import dataclass, field
from typing import Any

from src.validators.lexicos_loader import carregar_lexicos
from src.validators.rules_loader import validation_section

# ─── Resultado ──────────────────────────────────────────────────────────


@dataclass
class AchadoDidatica:
    """Um achado de didática. `regra` é a chave curta que o relatório mostra."""

    regra: str
    mensagem: str
    tipo: str = "warning"


@dataclass
class ResultadoDidatica:
    achados: list[AchadoDidatica] = field(default_factory=list)

    @property
    def aprovado(self) -> bool:
        return not any(a.tipo == "error" for a in self.achados)

    @property
    def avisos(self) -> list[AchadoDidatica]:
        return [a for a in self.achados if a.tipo == "warning"]

    @property
    def erros(self) -> list[AchadoDidatica]:
        return [a for a in self.achados if a.tipo == "error"]


# ─── Configuração (fallbacks; o YAML vence) ──────────────────────────────

_PADRAO_ABERTURAS = {
    "pares_iguais_aviso": 2,
    "serie_igual_erro": 3,
    "artigo_definido_max_fracao": 0.5,
    "minimo_de_paragrafos": 6,
}
_PADRAO_GLOSA = {"janela_caracteres": 140, "termos_extra": [], "max_achados": 8}
_PADRAO_FECHO = {"exigir_acao": True, "exigir_criterio": True}
_PADRAO_VERSOES = {"por_mil_palavras_aviso": 4}
_PADRAO_TITULO = {"max_palavras": 12}
_PADRAO_SUBTITULO = {
    "max_palavras": 25,
    "virgulas_max": 2,
    "formulas": [
        "Você sai",
        "Você vai sair",
        "Você descobre",
        "Você aprende",
        "Você vai aprender",
        "Você entende",
        "Nesta aula",
        "Neste módulo",
    ],
    "formula_repetida_erro": 3,
}
_PADRAO_FICHAS = {
    "voce_por_mil_min": 5,
    "abertura_repetida_max": 2,
    "seguidas_max": 6,
    "fuga": [
        "versão instalada",
        "documentação atual",
        "documentação oficial",
        "pode conter",
        "consulte a documentação",
        "verifique na documentação",
        "posteriores ao recorte",
        "podem ter mudado",
    ],
}


def _secao(chave: str, padrao: dict[str, Any]) -> dict[str, Any]:
    """Bloco `validation.didatica.<chave>` do YAML, com os padrões por baixo."""
    bruto = validation_section("didatica").get(chave)
    saida = dict(padrao)
    if isinstance(bruto, dict):
        saida.update({k: v for k, v in bruto.items() if v is not None})
    return saida


def _ligado() -> bool:
    return bool(validation_section("didatica").get("enabled", True))


def _limiar_da_fonte(chave: str, padrao: int) -> int:
    limiares = carregar_lexicos().get("limiares")
    if isinstance(limiares, dict):
        valor = limiares.get(chave)
        if isinstance(valor, int) and valor > 0:
            return valor
    return padrao


def _jargao_da_fonte() -> list[str]:
    jargao = carregar_lexicos().get("jargao")
    return sorted(jargao.keys(), key=len, reverse=True) if isinstance(jargao, dict) else []


# ─── Texto: utilitários ─────────────────────────────────────────────────

_H1_RE = re.compile(r"^#\s+(?P<titulo>.+?)\s*$", re.MULTILINE)
_HEADING_RE = re.compile(r"^#{1,6}\s")
_CODE_FENCE_RE = re.compile(r"```.*?```", re.DOTALL)
_MENCAO_RE = re.compile(r"[\"“«'‘][^\"”»'’\n]{0,200}[\"”»'’]")
_AULA_PREFIXO_RE = re.compile(r"^(?:Aula|Lesson|Lección)\s+[\d.]+\s*:\s*", re.IGNORECASE)
_PALAVRA_RE = re.compile(r"[\wÀ-ÿ-]+", re.UNICODE)

#: Sinais de que o termo foi glosado logo depois de aparecer.
_SINAL_DE_GLOSA_RE = re.compile(
    r"\(|:|\bou seja\b|\bisto é\b|\bque é\b|\bé o\b|\bé a\b|\bsignifica\b|\bquer dizer\b"
    r"|\bfunciona como\b|\bparecid[oa] com\b|\bé como\b|\bcomo se\b|\bpense (?:n[oa]|em)\b",
    re.IGNORECASE,
)

#: Versão de software ou de biblioteca em prosa: "v3", "3.2", "3.2.1", "versão 18".
_VERSAO_RE = re.compile(r"\bv\d+(?:\.\d+)*\b|\b\d+\.\d+(?:\.\d+)?\b|\bvers(?:ão|ion)\s+\d+", re.I)

#: Nome de API cru: CamelCase com duas maiúsculas ou identificador com ponto.
_API_CRUA_RE = re.compile(
    r"\b(?:[A-Z][a-z]+){2,}\b|\b[A-Z][A-Za-z]+\.[A-Z][A-Za-z]+\b|\b[a-z]+[A-Z][A-Za-z]+\b"
)

#: Fecho que resume em vez de mandar fazer.
_FECHO_RESUMO_RE = re.compile(
    r"^(?:em resumo|resumindo|recapitulando|nesta aula|neste capítulo|vimos que|você aprendeu|"
    r"como vimos|para resumir)\b",
    re.IGNORECASE,
)

#: Verbos no imperativo (2ª pessoa formal, que é o "você" do leitor) que abrem
#: uma instrução de fecho. Lista fechada de propósito: heurística por sufixo
#: pegaria substantivo ("compra", "conta", "marca").
_IMPERATIVOS = frozenset(
    """abra anote liste calcule publique meça compare escolha teste confira registre defina monte
    envie mande marque separe escreva comece use troque peça ligue agende revise crie some olhe
    veja pergunte conte guarde mantenha pare corte reserve rode instale configure copie cole
    grave salve imprima leia responda ajuste corrija apague repita observe acompanhe verifique
    confirme decida escolha aplique preencha divida multiplique subtraia reduza aumente fixe
    combine junte tire coloque ponha deixe faça vá volte siga entre abra feche mude limite
    priorize desenhe esboce planeje experimente prove compare ordene classifique nomeie
    descreva explique treine pratique ensaie""".split()
)

#: Sinal de critério: número, prazo, condição ou comparação que diz quando o
#: aluno acertou.
_CRITERIO_RE = re.compile(
    r"\d|\bR\$|%|\b(?:dia|dias|semana|semanas|mês|meses|hora|horas|minuto|minutos)\b|\bat[ée]\b|"
    r"\bquando\b|\bse\b|\bantes de\b|\bdepois de\b|\bpelo menos\b|\bno m[áa]ximo\b|\bmais de\b|"
    r"\bmenos de\b|\bmetade\b|\bdobro\b|\bo mesmo\b|\bmaior\b|\bmenor\b|\bigual\b",
    re.IGNORECASE,
)

#: Verbos que costumam nomear o resultado num título de aula. Um título com
#: verbo promete o que o aluno vai conseguir; sem verbo é rótulo de índice.
_VERBOS_DE_TITULO = frozenset(
    """muda decide entra sai faz vira para evita custa cabe cai sobe ganha perde vale traz leva
    escolhe mede conta paga cobra vende compra responde atende fecha abre nasce morre começa
    termina chega volta funciona quebra resolve troca corta cresce encolhe pesa importa serve
    basta falha acerta erra dura fica passa manda pede recebe mostra prova decidir escolher medir
    contar pagar cobrar vender comprar responder atender fechar abrir começar terminar chegar
    voltar funcionar quebrar resolver trocar cortar crescer pesar servir bastar falhar acertar
    errar durar ficar passar mandar pedir receber mostrar provar montar publicar calcular anotar
    listar comparar testar conferir registrar definir enviar marcar separar escrever usar
    ligar agendar revisar criar somar olhar ver perguntar guardar manter parar reservar rodar
    instalar configurar copiar gravar salvar ler ajustar corrigir repetir observar acompanhar
    verificar confirmar aplicar preencher dividir reduzir aumentar fixar combinar juntar tirar
    colocar deixar fazer ir seguir entrar mudar limitar priorizar desenhar planejar experimentar
    ordenar nomear descrever explicar treinar praticar transformar evitar ganhar perder parar
    saber conseguir precisar poder dever querer descobrir aprender entender""".split()
)

_ARTIGOS_DEFINIDOS = frozenset({"o", "a", "os", "as"})


def _sem_acento(texto: str) -> str:
    return "".join(
        c for c in unicodedata.normalize("NFD", texto) if unicodedata.category(c) != "Mn"
    )


def _contar_palavras(texto: str) -> int:
    return len(_PALAVRA_RE.findall(texto))


def _primeira_palavra(paragrafo: str) -> str:
    limpo = paragrafo.lstrip("*_>` ").strip()
    m = _PALAVRA_RE.search(limpo)
    return m.group(0).lower() if m else ""


def _paragrafos_de_prosa(texto: str) -> list[str]:
    """Blocos de prosa lisa: sem cabeçalho, lista, tabela, citação nem código."""
    corpo = _CODE_FENCE_RE.sub("", texto)
    saida: list[str] = []
    for bloco in re.split(r"\n\s*\n", corpo):
        limpo = bloco.strip()
        if not limpo:
            continue
        primeira = limpo.splitlines()[0].lstrip()
        if primeira.startswith(("|", "- ", "-- ", "* ", ">", "!", "<", "---")) or _HEADING_RE.match(
            primeira
        ):
            continue
        if re.match(r"^\d+[.)]\s", primeira):
            continue
        saida.append(limpo)
    return saida


def _titulo_e_subtitulo(texto: str) -> tuple[str | None, str | None]:
    """H1 (sem o prefixo 'Aula i.j:') e a primeira linha lisa depois dele."""
    m = _H1_RE.search(texto)
    if not m:
        return None, None
    titulo = _AULA_PREFIXO_RE.sub("", m.group("titulo").strip())
    resto = texto[m.end() :]
    for bloco in re.split(r"\n\s*\n", resto):
        limpo = bloco.strip()
        if limpo and not _HEADING_RE.match(limpo):
            return titulo, limpo.splitlines()[0].strip()
    return titulo, None


# ─── 1. Cadência de abertura de parágrafo ───────────────────────────────


def check_aberturas_de_paragrafo(texto: str) -> list[AchadoDidatica]:
    """Parágrafos vizinhos com a mesma primeira palavra e excesso de artigo definido."""
    cfg = _secao("aberturas", _PADRAO_ABERTURAS)
    paragrafos = _paragrafos_de_prosa(texto)
    achados: list[AchadoDidatica] = []
    if len(paragrafos) < 2:
        return achados

    primeiras = [_primeira_palavra(p) for p in paragrafos]
    pares = 0
    serie = 1
    maior_serie = 1
    palavra_da_serie = ""
    for anterior, atual in zip(primeiras, primeiras[1:], strict=False):
        if atual and atual == anterior:
            pares += 1
            serie += 1
            if serie > maior_serie:
                maior_serie = serie
                palavra_da_serie = atual
        else:
            serie = 1

    serie_erro = int(cfg["serie_igual_erro"])
    if maior_serie >= serie_erro:
        achados.append(
            AchadoDidatica(
                "abertura-em-serie",
                f'{maior_serie} parágrafos seguidos começam com "{palavra_da_serie}". A fonte '
                f"proíbe parágrafos vizinhos com a mesma construção (§3): mude a entrada de "
                f"alguns deles (oração subordinada, adjunto de tempo, o dado que puxa a frase).",
                tipo="error",
            )
        )
    elif pares >= int(cfg["pares_iguais_aviso"]):
        achados.append(
            AchadoDidatica(
                "abertura-repetida",
                f"{pares} pares de parágrafos vizinhos começam com a mesma palavra. Mesma cadência "
                f"em série é a sensação de texto picado: varie a entrada de metade deles.",
            )
        )

    minimo = int(cfg["minimo_de_paragrafos"])
    if len(paragrafos) >= minimo:
        com_artigo = sum(1 for p in primeiras if p in _ARTIGOS_DEFINIDOS)
        fracao = com_artigo / len(paragrafos)
        if fracao > float(cfg["artigo_definido_max_fracao"]):
            achados.append(
                AchadoDidatica(
                    "abertura-por-artigo",
                    f"{com_artigo} de {len(paragrafos)} parágrafos abrem com artigo definido "
                    f'("O", "A", "Os", "As"). Sujeito antes de tudo em todo parágrafo é a '
                    f"cadência de máquina; comece alguns pela condição, pelo número ou pelo verbo.",
                )
            )
    return achados


# ─── 2. Jargão sem glosa ────────────────────────────────────────────────


def check_glosa_de_jargao(
    texto: str, termos_extra: list[str] | None = None
) -> list[AchadoDidatica]:
    """Primeira aparição de termo técnico sem sinal de glosa na janela da fonte.

    A lista de termos é o `jargao` do espelho da fonte (com a glosa-padrão de
    cada um) mais `didatica.glosa.termos_extra` do YAML e o que o chamador
    passar. Glosa reconhecida: parêntese, dois-pontos, "ou seja", "isto é",
    "que é", "funciona como", "parecido com", "é como".
    """
    cfg = _secao("glosa", _PADRAO_GLOSA)
    janela = _limiar_da_fonte("glosaJanelaCaracteres", int(cfg["janela_caracteres"]))
    termos = list(_jargao_da_fonte())
    for t in list(cfg.get("termos_extra") or []) + list(termos_extra or []):
        if isinstance(t, str) and t and t not in termos:
            termos.append(t)

    prosa = "\n".join(_paragrafos_de_prosa(texto))
    prosa_plana = _sem_acento(prosa).lower()
    achados: list[AchadoDidatica] = []
    sem_glosa: list[str] = []
    for termo in termos:
        alvo = _sem_acento(termo).lower()
        m = re.search(r"(?<![\w-])" + re.escape(alvo) + r"(?![\w-])", prosa_plana)
        if not m:
            continue
        trecho = prosa[m.end() : m.end() + janela]
        if not _SINAL_DE_GLOSA_RE.search(trecho):
            sem_glosa.append(termo)
    teto = int(cfg["max_achados"])
    if sem_glosa:
        lista = ", ".join(f'"{t}"' for t in sem_glosa[:teto])
        extra = f" (e mais {len(sem_glosa) - teto})" if len(sem_glosa) > teto else ""
        achados.append(
            AchadoDidatica(
                "jargao-sem-glosa",
                f"Termo técnico sem glosa na primeira aparição: {lista}{extra}. A glosa tem até "
                f'12 palavras e uma analogia do cotidiano do aluno, no molde "spring: jeito de '
                f'animar que imita uma mola".',
            )
        )
    return achados


# ─── 3. Fecho com ação e critério ───────────────────────────────────────


def check_fecho(texto: str) -> list[AchadoDidatica]:
    """O último parágrafo manda fazer (imperativo) e diz como saber se acertou."""
    cfg = _secao("fecho", _PADRAO_FECHO)
    paragrafos = _paragrafos_de_prosa(texto)
    if not paragrafos:
        return []
    fecho = paragrafos[-1]
    achados: list[AchadoDidatica] = []
    if _FECHO_RESUMO_RE.match(fecho.lstrip("*_ ")):
        achados.append(
            AchadoDidatica(
                "fecho-resumo",
                "O último parágrafo resume o que foi lido. O fecho mostra a consequência pelo "
                "exemplo e diz o que o aluno faz a seguir (R8: sem recapitulação).",
            )
        )
    palavras = {w.lower() for w in _PALAVRA_RE.findall(fecho)}
    if cfg.get("exigir_acao") and not (palavras & _IMPERATIVOS):
        achados.append(
            AchadoDidatica(
                "fecho-sem-acao",
                "O último parágrafo não traz verbo no imperativo (abra, anote, calcule, publique...). "
                "O fecho entrega a ação de hoje, em prosa.",
            )
        )
    if cfg.get("exigir_criterio") and not _CRITERIO_RE.search(fecho):
        achados.append(
            AchadoDidatica(
                "fecho-sem-criterio",
                "O último parágrafo manda fazer sem dizer como saber se deu certo: acrescente o "
                'número, o prazo ou a condição que o aluno confere ("quando três clientes '
                'responderem", "em uma semana", "se o custo passar de R$ 40").',
            )
        )
    return achados


# ─── 4. Enxurrada de versão ─────────────────────────────────────────────


def check_enxurrada_de_versao(texto: str) -> list[AchadoDidatica]:
    """Número de versão por mil palavras acima do teto: minúcia que não decide nada."""
    cfg = _secao("versoes", _PADRAO_VERSOES)
    prosa = "\n".join(_paragrafos_de_prosa(texto))
    n_palavras = _contar_palavras(prosa)
    if n_palavras < 200:
        return []
    versoes = _VERSAO_RE.findall(prosa)
    por_mil = len(versoes) * 1000 / n_palavras
    teto = float(cfg["por_mil_palavras_aviso"])
    if por_mil > teto:
        exemplos = ", ".join(dict.fromkeys(versoes[:5]))
        return [
            AchadoDidatica(
                "enxurrada-de-versao",
                f"{len(versoes)} números de versão em {n_palavras} palavras ({por_mil:.1f} por mil; "
                f"teto {teto:g}): {exemplos}. Versão só entra quando muda a decisão do aluno; o "
                f"resto vai para a lista de fontes.",
            )
        ]
    return []


# ─── 5. Título e subtítulo ──────────────────────────────────────────────


def check_titulo(titulo: str) -> list[AchadoDidatica]:
    """Título como promessa do aluno, não índice de técnico."""
    cfg = _secao("titulo", _PADRAO_TITULO)
    limpo = _AULA_PREFIXO_RE.sub("", titulo.strip())
    if not limpo:
        return []
    achados: list[AchadoDidatica] = []
    teto = _limiar_da_fonte("h1MaxPalavras", int(cfg["max_palavras"]))
    n = _contar_palavras(limpo)
    if n > teto:
        achados.append(
            AchadoDidatica("titulo-longo", f'Título com {n} palavras (teto {teto}): "{limpo}".')
        )
    if ":" in limpo:
        achados.append(
            AchadoDidatica(
                "titulo-com-dois-pontos",
                f'Título com dois-pontos é rótulo de índice ("{limpo}"). Diga o que o aluno vai '
                f"conseguir fazer, com verbo.",
            )
        )
    palavras = [w.lower() for w in _PALAVRA_RE.findall(limpo)]
    if palavras and not any(w in _VERBOS_DE_TITULO for w in palavras):
        achados.append(
            AchadoDidatica(
                "titulo-sem-verbo",
                f'Título sem verbo ("{limpo}"): substantivos empilhados pressupõem o conceito que a '
                f'aula ainda vai ensinar. Nomeie o resultado: "Como a oficina parou de perder '
                f'orçamento", "Escolher a base do site sem pagar duas vezes".',
            )
        )
    return achados


def check_subtitulo(subtitulo: str) -> list[AchadoDidatica]:
    """Subtítulo em uma promessa: sem fórmula fixa, sem corrente de vírgulas."""
    cfg = _secao("subtitulo", _PADRAO_SUBTITULO)
    limpo = subtitulo.strip()
    if not limpo:
        return []
    achados: list[AchadoDidatica] = []
    n = _contar_palavras(limpo)
    teto = int(cfg["max_palavras"])
    if n > teto:
        achados.append(
            AchadoDidatica(
                "subtitulo-longo",
                f"Subtítulo com {n} palavras (teto {teto}). Ninguém lê até o fim no celular.",
            )
        )
    virgulas = limpo.count(",")
    if virgulas > int(cfg["virgulas_max"]):
        achados.append(
            AchadoDidatica(
                "subtitulo-promessas-empilhadas",
                f"Subtítulo com {virgulas} vírgulas: promessas empilhadas numa corrente. Uma "
                f"promessa por subtítulo; as outras são das aulas seguintes.",
            )
        )
    for formula in cfg.get("formulas") or []:
        if _sem_acento(limpo).lower().startswith(_sem_acento(str(formula)).lower()):
            achados.append(
                AchadoDidatica(
                    "subtitulo-formula",
                    f'Subtítulo começa com a fórmula "{formula}". A promessa muda de forma a cada '
                    f"aula: comece pelo resultado, pelo problema ou pela decisão.",
                )
            )
            break
    return achados


def check_subtitulos(descricoes: list[str]) -> list[AchadoDidatica]:
    """Fórmula de abertura repetida entre os subtítulos de um módulo ou curso."""
    cfg = _secao("subtitulo", _PADRAO_SUBTITULO)
    aberturas = Counter()
    for d in descricoes:
        palavras = _PALAVRA_RE.findall(d or "")
        if len(palavras) >= 2:
            aberturas[" ".join(w.lower() for w in palavras[:2])] += 1
    teto = int(cfg["formula_repetida_erro"])
    achados: list[AchadoDidatica] = []
    for abertura, n in aberturas.most_common():
        if n >= teto:
            achados.append(
                AchadoDidatica(
                    "subtitulo-formula-repetida",
                    f'{n} subtítulos começam com "{abertura}". Fórmula repetida vira tique e toda '
                    f"promessa do curso fica com a mesma cara.",
                    tipo="error",
                )
            )
    return achados


# ─── 6. Fichas (recurso, caso, dica) ────────────────────────────────────


@dataclass
class Ficha:
    """Uma ficha auxiliar: nome, explicação, exemplo e conferência (qualquer um vazio)."""

    nome: str = ""
    explicacao: str = ""
    exemplo: str = ""
    conferencia: str = ""

    @property
    def texto(self) -> str:
        return "\n".join(p for p in (self.explicacao, self.exemplo, self.conferencia) if p)


def _com_glosa(texto: str, inicio: int, janela: int) -> bool:
    return bool(_SINAL_DE_GLOSA_RE.search(texto[inicio : inicio + janela]))


def check_fichas(fichas: list[Ficha], ligacoes: int = 0) -> list[AchadoDidatica]:
    """Registro, abertura, API crua, fuga e acúmulo numa sequência de fichas.

    Args:
        fichas: as fichas na ordem em que o leitor as encontra.
        ligacoes: quantas frases de passagem existem entre elas (prosa que diz
            o que acabou de ser resolvido e por que a próxima ficha vem agora).
    """
    if not fichas:
        return []
    cfg = _secao("fichas", _PADRAO_FICHAS)
    janela = _limiar_da_fonte("glosaJanelaCaracteres", 140)
    achados: list[AchadoDidatica] = []

    texto_total = "\n".join(f.texto for f in fichas)
    n_palavras = _contar_palavras(texto_total)
    if n_palavras >= 150:
        n_voce = len(re.findall(r"\bvoc[êe]\b", texto_total, re.IGNORECASE))
        por_mil = n_voce * 1000 / n_palavras
        piso = float(cfg["voce_por_mil_min"])
        if por_mil < piso:
            achados.append(
                AchadoDidatica(
                    "ficha-registro-impessoal",
                    f'{n_voce} "você" em {n_palavras} palavras de ficha ({por_mil:.1f} por mil; '
                    f"piso {piso:g}). A aula fala com a pessoa; a ficha fala sobre o assunto. "
                    f"Reescreva no mesmo registro da aula: você, imperativo, exemplo do negócio.",
                )
            )

    teto_abertura = int(cfg["abertura_repetida_max"])
    for campo, rotulo in (("explicacao", "explicação"), ("conferencia", "conferência")):
        primeiras = Counter(
            _primeira_palavra(getattr(f, campo)) for f in fichas if getattr(f, campo)
        )
        for palavra, n in primeiras.most_common(1):
            if palavra and n > teto_abertura:
                achados.append(
                    AchadoDidatica(
                        "ficha-abertura-repetida",
                        f'{n} fichas abrem a {rotulo} com "{palavra}". Mesma palavra em série é '
                        f"paredão; varie a entrada ou ligue uma ficha à seguinte.",
                    )
                )

    fugas = [str(f).lower() for f in (cfg.get("fuga") or [])]
    for f in fichas:
        conf = _sem_acento(f.conferencia).lower()
        for fuga in fugas:
            if _sem_acento(fuga) in conf:
                achados.append(
                    AchadoDidatica(
                        "ficha-conferencia-de-fuga",
                        f'Conferência de "{f.nome or "ficha"}" manda o aluno "{fuga}". Isso não '
                        f"ensina, só se protege: diga o que ele vê na tela quando acertou.",
                        tipo="error",
                    )
                )
                break

    crus: list[str] = []
    for f in fichas:
        texto = f.texto
        for m in _API_CRUA_RE.finditer(texto):
            if not _com_glosa(texto, m.end(), janela):
                crus.append(m.group(0))
                break
    if crus:
        lista = ", ".join(dict.fromkeys(crus[:6]))
        achados.append(
            AchadoDidatica(
                "ficha-api-crua",
                f"Nome de API sem glosa na ficha: {lista}. Um dono de padaria não agarra isso sem "
                f"uma explicação prática logo em seguida, entre parênteses ou depois de dois-pontos.",
            )
        )

    teto_seguidas = int(cfg["seguidas_max"])
    seguidas = len(fichas) - ligacoes
    if seguidas > teto_seguidas:
        achados.append(
            AchadoDidatica(
                "fichas-em-paredao",
                f"{len(fichas)} fichas seguidas com {ligacoes} frase(s) de ligação (teto {teto_seguidas} "
                f"sem ligação). Depois de cada grupo, uma frase diz o que ficou resolvido, por que a "
                f"próxima vem agora e onde o leitor pode parar.",
            )
        )
    return achados


# ─── Superfície: Markdown de uma aula ───────────────────────────────────


def check_didatica(texto: str, unidade: str = "aula") -> ResultadoDidatica:
    """Mede o Markdown de uma aula. Para trilha, só jargão e cadência."""
    resultado = ResultadoDidatica()
    if not _ligado() or not texto.strip():
        return resultado
    corpo = texto
    resultado.achados.extend(check_aberturas_de_paragrafo(corpo))
    resultado.achados.extend(check_glosa_de_jargao(corpo))
    resultado.achados.extend(check_enxurrada_de_versao(corpo))
    if unidade == "aula":
        titulo, subtitulo = _titulo_e_subtitulo(corpo)
        if titulo:
            resultado.achados.extend(check_titulo(titulo))
        if subtitulo:
            resultado.achados.extend(check_subtitulo(subtitulo))
        resultado.achados.extend(check_fecho(corpo))
    return resultado


# ─── Superfície: CourseDefinition montado ───────────────────────────────

_TIPOS_DE_FICHA = frozenset({"tip", "warning", "stepGuide", "comparison"})


def _fichas_da_definicao(step) -> tuple[list[Ficha], int]:
    """Blocos auxiliares consecutivos viram fichas; prosa entre eles conta como ligação."""
    fichas: list[Ficha] = []
    ligacoes = 0
    anterior_era_ficha = False
    for secao in step.content:
        tipo = secao.type.value
        if tipo in _TIPOS_DE_FICHA:
            texto = secao.value or ""
            dados = secao.data or {}
            if tipo == "stepGuide":
                partes = [
                    f"{s.get('title', '')}. {s.get('description', '')}"
                    for s in dados.get("steps", [])
                    if isinstance(s, dict)
                ]
                texto = "\n".join(partes)
            elif tipo == "comparison":
                texto = " ".join(str(v) for v in dados.values() if isinstance(v, str))
            fichas.append(
                Ficha(
                    nome=secao.label
                    or (dados.get("title") if isinstance(dados, dict) else "")
                    or tipo,
                    explicacao=texto,
                )
            )
            anterior_era_ficha = True
        elif tipo == "text" and anterior_era_ficha and fichas:
            ligacoes += 1
            anterior_era_ficha = False
        else:
            anterior_era_ficha = False
    return fichas, ligacoes


def check_didatica_definicao(course) -> list[str]:
    """Mede o curso montado. Devolve mensagens rotuladas; vazio é aprovado.

    Título e subtítulo de cada módulo, fórmula repetida entre os subtítulos,
    cadência e fecho da prosa de cada módulo, jargão sem glosa e as fichas
    (blocos auxiliares em sequência). Nada aqui recusa a renderização: o
    gerador registra no log e segue. O que reprova o curso é o gate da aula.
    """
    if not _ligado():
        return []
    mensagens: list[str] = []
    for step in course.steps:
        rotulo = step.id
        for a in check_titulo(step.title):
            mensagens.append(f"{rotulo}: [{a.regra}] {a.mensagem}")
        for a in check_subtitulo(step.description or ""):
            mensagens.append(f"{rotulo}: [{a.regra}] {a.mensagem}")
        prosa = "\n\n".join(s.value for s in step.content if s.type.value == "text" and s.value)
        if prosa:
            for a in (
                check_aberturas_de_paragrafo(prosa)
                + check_glosa_de_jargao(prosa)
                + check_fecho(prosa)
            ):
                mensagens.append(f"{rotulo}: [{a.regra}] {a.mensagem}")
        fichas, ligacoes = _fichas_da_definicao(step)
        for a in check_fichas(fichas, ligacoes):
            mensagens.append(f"{rotulo}: [{a.regra}] {a.mensagem}")
    for a in check_subtitulos([s.description or "" for s in course.steps]):
        mensagens.append(f"curso: [{a.regra}] {a.mensagem}")
    return mensagens


def format_report(resultado: ResultadoDidatica) -> str:
    if not resultado.achados:
        return "Didática: nenhum achado."
    linhas = [f"Didática: {len(resultado.erros)} erro(s), {len(resultado.avisos)} aviso(s)"]
    for a in resultado.achados:
        linhas.append(f"  [{a.tipo}] {a.regra}: {a.mensagem}")
    return "\n".join(linhas)
