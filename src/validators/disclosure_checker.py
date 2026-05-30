"""disclosure_checker.py — verifica disclosure de IA conforme regulação.

Brasil 2026:
- **PL 2338/2023** (Marco Legal da IA) — aprovado no Senado dez/2024, em
  tramitação na Câmara, sanção esperada em 2026. Disclosure mandatório:
  usuário deve saber que interage com IA; identificação obrigatória de
  conteúdo gerado/manipulado por IA. URL Senado:
  https://www25.senado.leg.br/web/atividade/materias/-/materia/157233

- **CFP Posicionamento 03/07/2025** — IA generativa em prática clínica e
  conteúdo psicológico exige supervisão profissional e disclosure. Não
  substitui psicólogo registrado.

- **MEC Marco Referencial 2025-07** — IA na Educação Básica; orientações
  curriculares + princípios éticos. URL:
  https://www.gov.br/mec/pt-br/assuntos/noticias/2025/julho/

Google EEAT (Quality Rater Guidelines set/2025): Trust = componente mais
importante; disclosure explícito de uso de IA + autor humano verificável
fortalece o sinal Trust independentemente de "AI content per se".

Operação:
- O cliente declara em `client.yaml > disclosure` quais normas se aplicam.
- O bloco padrão de disclosure deve estar no rodapé do módulo.
- Se `block_if_missing=true` E o bloco não for encontrado, o módulo é
  rejeitado pelo quality gate.
- Em modo report-only (`block_if_missing=false`), emite warning.
"""

from __future__ import annotations

import logging
import re
from dataclasses import dataclass, field
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.clients.context import ClientContext, DisclosureConfig

logger = logging.getLogger(__name__)


# Marcadores aceitos para identificar bloco de disclosure no texto.
# Procuramos pelo menos UM destes na seção final do módulo.
_DISCLOSURE_MARKERS = [
    r"sobre a produ[çc][aã]o deste conte[uú]do",
    r"disclosure de uso de ia",
    r"este conte[uú]do foi (co-?)?produzido com",
    r"conformidade com (o |)pl 2338",
    r"co-?produzido com pipeline de ia",
    r"revisado por (?:especialista|psic[oó]logo|m[eé]dico|advogado)",
]

# Marcadores que indicam disclosure presente mas INCOMPLETO (sem autor humano).
_INCOMPLETE_MARKERS = [
    r"gerado por ia",
    r"este texto foi escrito por (?:um )?modelo",
]


@dataclass
class DisclosureCheckResult:
    aprovado: bool = True
    tem_bloco_disclosure: bool = False
    tem_autor_canonico: bool = False
    tem_credencial_revisor: bool = False
    tem_norma_citada: bool = False
    erros: list[str] = field(default_factory=list)
    avisos: list[str] = field(default_factory=list)

    def report(self) -> str:
        lines = [
            "--- Disclosure Check Report ---",
            f"Aprovado:                       {'SIM' if self.aprovado else 'NAO'}",
            f"Bloco de disclosure presente:   {'sim' if self.tem_bloco_disclosure else 'NAO'}",
            f"Autor canonico citado:          {'sim' if self.tem_autor_canonico else 'NAO'}",
            f"Credencial do revisor humano:   {'sim' if self.tem_credencial_revisor else 'NAO'}",
            f"Norma regulatoria citada:       {'sim' if self.tem_norma_citada else 'NAO'}",
        ]
        if self.erros:
            lines.append("")
            lines.append(f"Erros ({len(self.erros)}):")
            for e in self.erros[:10]:
                lines.append(f"  - {e}")
        if self.avisos:
            lines.append("")
            lines.append(f"Avisos ({len(self.avisos)}):")
            for a in self.avisos[:10]:
                lines.append(f"  - {a}")
        return "\n".join(lines)


def disclosure_check(
    text: str, client: "ClientContext | None" = None
) -> DisclosureCheckResult:
    """Verifica se o texto tem o bloco de disclosure exigido pelo cliente.

    Retorna sempre um DisclosureCheckResult; campos `aprovado` e `erros`
    refletem decisão final considerando `block_if_missing` do cliente.
    """
    result = DisclosureCheckResult()

    if client is None:
        from src.clients import load_client
        client = load_client("default")

    disc: "DisclosureConfig" = client.disclosure
    if not disc.enabled:
        # Cliente não exige disclosure — passa direto
        return result

    text_lower = text.lower()

    # 1. Busca por marcadores de disclosure
    for marker in _DISCLOSURE_MARKERS:
        if re.search(marker, text_lower):
            result.tem_bloco_disclosure = True
            break

    # 2. Verifica autor canônico
    author_name = (client.author.name or "").lower()
    if author_name and author_name in text_lower:
        result.tem_autor_canonico = True

    # 3. Verifica credencial do autor (fragmentos canônicos do voice_guard)
    if client.voice_guard.canonical.credential_fragments:
        full_count = sum(
            1
            for frag in client.voice_guard.canonical.credential_fragments
            if frag.lower() in text_lower
        )
        if full_count >= 1:
            result.tem_credencial_revisor = True

    # 4. Verifica que pelo menos UMA norma exigida está citada
    if disc.required_by:
        for norma in disc.required_by:
            # Normas vêm em formato PL_2338_2023, MEC_Marco_Referencial_2025
            # — buscamos a parte humana (pl 2338, mec, cfp).
            humanized = norma.lower().replace("_", " ")
            short_keys = ["pl 2338", "cfp", "mec", "lgpd", "anpd"]
            for k in short_keys:
                if k in humanized and k in text_lower:
                    result.tem_norma_citada = True
                    break
            if result.tem_norma_citada:
                break

    # 5. Verifica disclosure incompleto (presente mas sem autor humano)
    for incomplete in _INCOMPLETE_MARKERS:
        if re.search(incomplete, text_lower) and not result.tem_autor_canonico:
            result.avisos.append(
                f"disclosure incompleto: '{incomplete}' presente mas sem "
                f"citacao explicita do autor canonico '{client.author.name}'"
            )

    # 6. Reviewer extra (psicólogo CRP, médico CRM, advogado OAB) — se exigido
    for extra in disc.reviewer_extra:
        role = extra.get("role", "")
        field_id = extra.get("field_in_template", "")
        # Sinaliza ausência por busca da role; threshold leve (regulador exige
        # mas conteudo pode ainda nao ter sido revisado humanamente).
        if role and role.lower() not in text_lower:
            result.avisos.append(
                f"disclosure exige revisao humana por '{role}' (campo "
                f"'{field_id}') — verificar antes de publicacao"
            )

    # 7. Decisão final
    erros_estruturais: list[str] = []
    if not result.tem_bloco_disclosure:
        erros_estruturais.append(
            "bloco de disclosure ausente — exigido por "
            f"{', '.join(disc.required_by) if disc.required_by else 'cliente'}"
        )
    if not result.tem_autor_canonico:
        erros_estruturais.append(
            f"autor canonico '{client.author.name}' nao citado no texto"
        )
    if disc.required_by and not result.tem_norma_citada:
        erros_estruturais.append(
            "nenhuma das normas regulatorias exigidas foi citada: "
            f"{', '.join(disc.required_by)}"
        )

    if disc.block_if_missing:
        result.erros.extend(erros_estruturais)
        result.aprovado = len(erros_estruturais) == 0
    else:
        # Modo report-only: avisos em vez de erros bloqueantes
        for e in erros_estruturais:
            result.avisos.append(f"[report-only] {e}")
        result.aprovado = True

    return result


def format_report(result: DisclosureCheckResult) -> str:
    return result.report()


def build_disclosure_block(client: "ClientContext | None" = None) -> str:
    """Gera o bloco padronizado de disclosure para inserir no rodape do modulo.

    O `reviewer.py` (Claude) pode chamar isto para inserir o bloco quando
    detectar ausência. Tambem pode ser usado em templates Jinja2.
    """
    if client is None:
        from src.clients import load_client
        client = load_client("default")

    disc = client.disclosure
    if not disc.enabled:
        return ""

    author = client.author.name or "[autor]"
    credential = client.author.credential or ""
    models = ", ".join(disc.pipeline_models) if disc.pipeline_models else "modelos de IA"
    normas_human = []
    for n in disc.required_by:
        if "PL_2338" in n:
            normas_human.append("PL 2338/2023 (Marco Legal da IA, Brasil)")
        elif "CFP" in n:
            normas_human.append("Posicionamento CFP de 03/07/2025")
        elif "MEC" in n:
            normas_human.append("Marco Referencial MEC IA na Educacao")
        elif "LGPD" in n:
            normas_human.append("LGPD art. 20")
        else:
            normas_human.append(n.replace("_", " "))
    normas_str = "; ".join(normas_human) if normas_human else "regulacao aplicavel"

    extra_lines = []
    for extra in disc.reviewer_extra:
        role = extra.get("role", "")
        if role:
            extra_lines.append(f"Revisão técnica adicional por {role}.")

    bloco = (
        f"> **Sobre a producao deste conteudo**: Co-produzido com pipeline "
        f"de IA ({models}) e revisado por {author}"
        + (f" ({credential})" if credential else "")
        + f". Disclosure conforme {normas_str}."
    )
    if extra_lines:
        bloco += "\n>\n> " + " ".join(extra_lines)
    return bloco
