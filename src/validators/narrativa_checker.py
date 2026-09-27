"""Orçamento de narrativa por aula (pedido do dono, 27/09/2026).

Caso, personagem e cena só entram quando carregam o procedimento. Este medidor
é determinístico e barato: para cada parágrafo de prosa da aula (fora
subtítulo, lista, tabela, citação, código e fontes), procura três marcas:

- pretérito em série: ao menos `preterito_em_serie_min` verbos no pretérito
  (terminação e formas irregulares do YAML, menos as exceções);
- cena: hora, dia da semana, "naquela manhã", fala de personagem;
- personagem: nome com inicial maiúscula, fora do começo de frase, que volta
  em ao menos `personagem_paragrafos_min` parágrafos e aparece junto de verbo
  no pretérito.

O parágrafo com pretérito em série, com cena ou com personagem e pretérito
conta como narrativo. Duas medidas saem daí, conforme o `client.yaml`:

- `narrativa-acima-do-teto`: parcela de parágrafos narrativos acima de
  `narrativa.parcela_max`, só a partir de `paragrafos_min_para_medir`;
- `narrativa-na-abertura`: o primeiro parágrafo depois do subtítulo é
  narrativo, ou traz as marcas `aberturaEmCena` do espelho da fonte.

O que ele NÃO mede, e por isso nasce como aviso: se o exemplo carrega um passo
do procedimento; se o relato histórico é necessário (a origem do conceito) ou
gratuito; narrativa escrita no presente ("a Marta abre a agenda"); e marca
comercial que volta com verbo no passado pode passar por personagem.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from functools import lru_cache
from typing import Any

from src.validators.blocos_de_aula import ler_aula
from src.validators.rules_loader import validation_section

SECAO = "orcamento_narrativa"

_COMECO_DE_FRASE_RE = re.compile(r"(?:^|[.!?:;]\s+|[\"“(]\s*)$")


@dataclass
class AchadoNarrativa:
    regra: str
    mensagem: str
    tipo: str = "warning"


@dataclass
class MedidaNarrativa:
    paragrafos: int = 0
    narrativos: list[int] = field(default_factory=list)
    personagens: list[str] = field(default_factory=list)
    abertura_narrativa: bool = False

    @property
    def parcela(self) -> float:
        return len(self.narrativos) / self.paragrafos if self.paragrafos else 0.0


def _secao() -> dict[str, Any]:
    secao = validation_section(SECAO)
    return secao if isinstance(secao, dict) else {}


@lru_cache(maxsize=32)
def _compilar(padroes: tuple[str, ...]) -> tuple[re.Pattern[str], ...]:
    saida = []
    for p in padroes:
        try:
            saida.append(re.compile(p, re.IGNORECASE))
        except re.error:
            continue
    return tuple(saida)


def _lista(secao: dict[str, Any], chave: str) -> list[str]:
    valor = secao.get(chave)
    return [str(v) for v in valor if isinstance(v, str) and v] if isinstance(valor, list) else []


def _inteiro(secao: dict[str, Any], chave: str) -> int | None:
    try:
        valor = secao.get(chave)
        return None if valor is None else int(valor)
    except (TypeError, ValueError):
        return None


class _Marcas:
    """Marcas de narrativa compiladas uma vez por medição, a partir do YAML."""

    def __init__(self, secao: dict[str, Any]) -> None:
        try:
            self.preterito = re.compile(str(secao.get("preterito") or r"(?!)"), re.IGNORECASE)
        except re.error:
            self.preterito = re.compile(r"(?!)")
        self.formas = {f.lower() for f in _lista(secao, "preterito_formas")}
        self.excecoes = {f.lower() for f in _lista(secao, "preterito_excecoes")}
        self.cena = _compilar(tuple(_lista(secao, "cena")))
        self.serie_min = _inteiro(secao, "preterito_em_serie_min")
        try:
            self.nome = re.compile(str(secao.get("personagem_nome") or r"(?!)"))
        except re.error:
            self.nome = re.compile(r"(?!)")
        self.ignorados = {n.lower() for n in _lista(secao, "nomes_ignorados")}

    def verbos_no_preterito(self, texto: str) -> int:
        n = 0
        for palavra in re.findall(r"[a-zà-úç]+", texto.lower()):
            if palavra in self.excecoes:
                continue
            if palavra in self.formas or self.preterito.fullmatch(palavra):
                n += 1
        return n

    def tem_cena(self, texto: str) -> bool:
        return any(p.search(texto) for p in self.cena)

    def nomes(self, texto: str) -> set[str]:
        achados = set()
        for m in self.nome.finditer(texto):
            nome = m.group(1) if m.groups() else m.group(0)
            if nome.lower() in self.ignorados:
                continue
            if _COMECO_DE_FRASE_RE.search(texto[: m.start()]):
                continue
            achados.add(nome)
        return achados


def _espelho_de_abertura() -> tuple[re.Pattern[str], ...]:
    from src.validators.lexicos_loader import carregar_lexicos

    valor = carregar_lexicos().get("aberturaEmCena")
    if not isinstance(valor, list):
        return ()
    return _compilar(tuple(str(v) for v in valor if isinstance(v, str) and v))


def medir(texto: str) -> MedidaNarrativa:
    """Parágrafos de prosa, quais são narrativos e se a abertura é narrativa."""
    secao = _secao()
    if not secao:
        return MedidaNarrativa()
    marcas = _Marcas(secao)
    paragrafos = ler_aula(texto).paragrafos
    medida = MedidaNarrativa(paragrafos=len(paragrafos))
    if not paragrafos:
        return medida

    minimo_de_paragrafos = _inteiro(secao, "personagem_paragrafos_min")
    ocorrencias: dict[str, int] = {}
    nomes_por_paragrafo = [marcas.nomes(p) for p in paragrafos]
    for nomes in nomes_por_paragrafo:
        for nome in nomes:
            ocorrencias[nome] = ocorrencias.get(nome, 0) + 1
    recorrentes = (
        {n for n, k in ocorrencias.items() if k >= minimo_de_paragrafos}
        if minimo_de_paragrafos
        else set()
    )

    personagens: set[str] = set()
    for i, paragrafo in enumerate(paragrafos):
        verbos = marcas.verbos_no_preterito(paragrafo)
        em_serie = bool(marcas.serie_min) and verbos >= (marcas.serie_min or 0)
        com_personagem = bool(nomes_por_paragrafo[i] & recorrentes) and verbos >= 1
        if com_personagem:
            personagens |= nomes_por_paragrafo[i] & recorrentes
        if em_serie or marcas.tem_cena(paragrafo) or com_personagem:
            medida.narrativos.append(i)
    medida.personagens = sorted(personagens)
    abertura = paragrafos[0]
    medida.abertura_narrativa = 0 in medida.narrativos or (
        bool(secao.get("usar_espelho_na_abertura"))
        and any(p.search(abertura) for p in _espelho_de_abertura())
    )
    return medida


def check_narrativa(texto: str, config: Any) -> list[AchadoNarrativa]:
    """Mede UMA aula contra o orçamento do cliente. Sem a regra ligada, vazio."""
    secao = _secao()
    if config is None or not getattr(config, "enabled", False) or not secao:
        return []
    if not texto or not texto.strip():
        return []
    nivel = "error" if getattr(config, "severidade", "aviso") == "erro" else "warning"
    m = medir(texto)
    achados: list[AchadoNarrativa] = []
    teto = getattr(config, "parcela_max", None)
    minimo = _inteiro(secao, "paragrafos_min_para_medir") or 0
    if teto is not None and m.paragrafos >= minimo and m.parcela > teto:
        quem = f" (personagem: {', '.join(m.personagens)})" if m.personagens else ""
        achados.append(
            AchadoNarrativa(
                "narrativa-acima-do-teto",
                f"{len(m.narrativos)} de {m.paragrafos} parágrafos de prosa contam história "
                f"({m.parcela:.0%}), acima do teto de {teto:.0%}{quem}. O exemplo percorre os "
                f"passos e é curto; a história que não mostra um passo sendo feito sai.",
                nivel,
            )
        )
    if getattr(config, "abertura_sem_narrativa", False) and m.abertura_narrativa:
        achados.append(
            AchadoNarrativa(
                "narrativa-na-abertura",
                "A abertura começa por cena ou história. A aula abre pela resposta: o que o "
                "aluno vai conseguir fazer e o que custa não fazer.",
                nivel,
            )
        )
    return achados


def instrucao_para_prompt(config: Any) -> str:
    """Bloco `{bloco_narrativa}` dos prompts. Vazio sem a regra ligada ou sem teto."""
    if config is None or not getattr(config, "enabled", False):
        return ""
    modelo = _secao().get("instrucao_prompt")
    teto = getattr(config, "parcela_max", None)
    if not isinstance(modelo, str) or not modelo.strip() or teto is None:
        return ""
    return modelo.strip().replace("{parcela}", f"{teto:.0%}")
