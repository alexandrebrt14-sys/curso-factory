"""Gate de qualidade que executa todos os validadores.

Se qualquer validador falhar, bloqueia o deploy e gera
relatório detalhado com o status de cada verificação.

Inclui: acentuação (detecção + auto-correção), HTML,
links e qualidade de conteúdo (tabelas, formatação,
exercícios, andragogia, Bloom, clichês).
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import TYPE_CHECKING

from src.models import QualityReport
from src.validators.accent_checker import (
    check_accents,
    fix_accents,
)
from src.validators.accent_checker import (
    format_report as accent_report,
)
from src.validators.content_checker import (
    check_content,
)
from src.validators.content_checker import (
    format_report as content_report,
)
from src.validators.disclosure_checker import disclosure_check
from src.validators.html_validator import format_report as html_report
from src.validators.html_validator import validate_html
from src.validators.link_checker import check_links
from src.validators.link_checker import format_report as link_report
from src.validators.stylometry_checker import stylometry_check
from src.validators.voice_guard import voice_guard_check

if TYPE_CHECKING:
    from src.clients.context import ClientContext

logger = logging.getLogger(__name__)


@dataclass
class GateResult:
    """Resultado consolidado do quality gate."""
    aprovado: bool = True
    acentuacao_ok: bool = True
    html_ok: bool = True
    links_ok: bool = True
    conteudo_ok: bool = True
    voice_guard_ok: bool = True
    stylometry_ok: bool = True
    disclosure_ok: bool = True
    erros: list[str] = field(default_factory=list)
    avisos: list[str] = field(default_factory=list)
    relatorios: list[str] = field(default_factory=list)
    texto_corrigido: str = ""
    acentos_corrigidos: int = 0
    voice_guard_score: int = 0
    stylometry_score: int = 0
    stylometry_burstiness: float = 0.0


class QualityGate:
    """Executa todos os validadores e decide se o conteúdo pode ser publicado.

    O gate executa 4 camadas de validação:
    1. Acentuação PT-BR (detecção + auto-correção)
    2. Qualidade de conteúdo (tabelas, formatação, exercícios, andragogia)
    3. Links (acentos em URLs, links internos)
    4. HTML (tags, acessibilidade, semântica) — apenas para conteúdo HTML

    Se auto_fix=True, o gate corrige automaticamente acentos e retorna
    o texto corrigido em GateResult.texto_corrigido.
    """

    def __init__(
        self,
        base_dir: Path | None = None,
        auto_fix: bool = True,
        client: ClientContext | None = None,
    ) -> None:
        self.base_dir = base_dir
        self.auto_fix = auto_fix
        if client is None:
            from src.clients import load_client
            client = load_client("default")
        self.client = client

    def check_text(
        self,
        text: str,
        curso_id: str = "unknown",
        module_name: str = "",
        unidade: str = "modulo",
        geo: bool = True,
    ) -> GateResult:
        """Valida texto puro (Markdown) com todas as verificações.

        Executa: acentuação, conteúdo, links.
        Se auto_fix=True, corrige acentos automaticamente.

        Args:
            unidade: `"aula"` ou `"modulo"`. O padrão é `"modulo"` porque o
                pipeline de geração ainda entrega módulos, e medi-los com a
                régua de uma aula (piso 900, erro 3.600) reprovaria todo o
                acervo. Quando o gerador passar a emitir aula, o chamador
                passa `unidade="aula"` e a régua fica a do molde D sem
                multiplicador. Ver `content_checker.tetos_da_unidade`.
        """
        result = GateResult()

        # 0. Auto-correção de acentos (se habilitada)
        working_text = text
        if self.auto_fix:
            working_text, num_correcoes = fix_accents(text)
            result.acentos_corrigidos = num_correcoes
            result.texto_corrigido = working_text
            if num_correcoes > 0:
                logger.info(
                    "Auto-correção: %d acento(s) corrigido(s) em '%s'",
                    num_correcoes,
                    curso_id,
                )
                result.relatorios.append(
                    f"Auto-correção: {num_correcoes} acento(s) corrigido(s) automaticamente."
                )

        # 1. Verificação de acentuação (no texto corrigido, para detectar residuais)
        accent_errors = check_accents(working_text)
        if accent_errors:
            result.acentuacao_ok = False
            result.aprovado = False
            for e in accent_errors:
                result.erros.append(
                    f"Acentuação: '{e.palavra_errada}' → '{e.correcao}' (linha {e.linha})"
                )
        result.relatorios.append(accent_report(accent_errors))

        # 2. Verificação de qualidade de conteúdo (inclui citabilidade GEO
        #    quando o cliente liga geo_2026 no client.yaml — ver
        #    docs/GEO_REDACAO_CHECKLIST_2026.md)
        geo_config = getattr(self.client, "geo", None) if geo else None
        content_errors = self._check_content_por_unidade(
            working_text, module_name, geo_config, unidade
        )
        blocking_errors = [e for e in content_errors if e.tipo == "error"]
        warnings = [e for e in content_errors if e.tipo == "warning"]

        if blocking_errors:
            result.conteudo_ok = False
            result.aprovado = False
            for e in blocking_errors:
                result.erros.append(f"Conteúdo [{e.categoria}]: {e.mensagem}")
        for e in warnings:
            result.avisos.append(f"Conteúdo [{e.categoria}]: {e.mensagem}")
        result.relatorios.append(content_report(content_errors))

        # 3. Verificação de links
        link_errors = check_links(working_text, self.base_dir)
        if link_errors:
            criticos = [e for e in link_errors if e.tipo == "accent_in_url"]
            avisos = [e for e in link_errors if e.tipo != "accent_in_url"]
            if criticos:
                result.links_ok = False
                result.aprovado = False
                for e in criticos:
                    result.erros.append(f"Link com acento: {e.url} (linha {e.linha})")
            for e in avisos:
                result.avisos.append(f"Link: [{e.tipo}] {e.url} (linha {e.linha})")
        result.relatorios.append(link_report(link_errors))

        # 4. Voice Guard (barreira programática de padrão editorial do cliente)
        vg = voice_guard_check(working_text, client=self.client)
        result.voice_guard_score = vg.score
        if not vg.aprovado:
            result.voice_guard_ok = False
            result.aprovado = False
            for e in vg.erros_criticos:
                result.erros.append(f"Voice Guard [crítico]: {e}")
            for e in vg.erros:
                if e not in vg.erros_criticos:
                    result.erros.append(f"Voice Guard: {e}")
        for a in vg.avisos:
            result.avisos.append(f"Voice Guard: {a}")
        result.relatorios.append(vg.report())

        # 5. Stylometry (medição estatística de "humanidade" — opt-in)
        # Default: report-only. Para bloquear, ajustar quality_rules.yaml.
        sty = stylometry_check(working_text, min_score=60)
        result.stylometry_score = sty.score
        result.stylometry_burstiness = sty.burstiness
        if not sty.aprovado:
            result.stylometry_ok = False
            # Não bloqueia o gate por default — apenas reporta como aviso até
            # calibração com baseline humano (ver PR-2.1 corpus_calibration).
            for e in sty.erros:
                result.avisos.append(f"Stylometry: {e}")
        for a in sty.avisos:
            result.avisos.append(f"Stylometry: {a}")
        result.relatorios.append(sty.report())

        # 6. Disclosure (PL 2338/CFP/MEC + EEAT Google) — controlado por cliente
        disc = disclosure_check(working_text, client=self.client)
        if not disc.aprovado:
            result.disclosure_ok = False
            result.aprovado = False
            for e in disc.erros:
                result.erros.append(f"Disclosure: {e}")
        for a in disc.avisos:
            result.avisos.append(f"Disclosure: {a}")
        result.relatorios.append(disc.report())

        logger.info(
            "Quality gate (texto) para '%s': %s (vg_score=%d, "
            "stylometry_score=%d, burstiness=%.2f, disclosure_ok=%s)",
            curso_id,
            "APROVADO" if result.aprovado else "REPROVADO",
            vg.score,
            sty.score,
            sty.burstiness,
            result.disclosure_ok,
        )
        return result

    @staticmethod
    def _check_content_por_unidade(text: str, module_name: str, geo_config, unidade: str):
        """Mede aula a aula quando o texto vem montado pelo orquestrador.

        O rascunho gerado desde 02/09/2026 traz `# Aula i.j: título` abrindo
        cada aula. Nesse caso a régua da aula (molde D) vale para cada bloco,
        sem o multiplicador de módulo, e o rótulo do achado carrega o título da
        aula. Texto sem esse cabeçalho é medido inteiro, na unidade pedida.
        """
        from src.orchestrator import AULA_H1_RE, TRILHA_H1_RE, dividir_em_unidades

        if TRILHA_H1_RE.match(text.lstrip()) or module_name.startswith("Trilha "):
            # Fechamento da trilha (objetivos, glossário, FAQ, fontes): não é
            # aula e a régua da aula o reprovaria pelo motivo errado. As
            # camadas de acento, link, voice guard e disclosure seguem valendo.
            return []
        if not AULA_H1_RE.search(text):
            return check_content(text, module_name, geo_config=geo_config, unidade=unidade)
        achados = []
        for titulo, bloco in dividir_em_unidades(text):
            if titulo.startswith("Trilha "):
                continue
            rotulo = f"{module_name} / {titulo}" if module_name else titulo
            # A régua da aula não carrega a camada GEO: fontes, estatísticas
            # e citação vivem no nível da trilha e do curso (molde D).
            achados.extend(check_content(bloco, rotulo, geo_config=None, unidade="aula"))
        if geo_config is not None:
            achados.extend(QualityGate.check_geo(text, module_name or "curso", geo_config))
        return achados

    @staticmethod
    def check_geo(text: str, rotulo: str = "curso", geo_config=None):
        """Camada de citabilidade GEO sobre o texto INTEIRO (curso ou trilha).

        Cite Sources, Statistics, Quotation e answer capsule são metas do
        conjunto, não de cada aula de mil palavras: cobradas por aula, elas
        reprovavam toda aula do molde novo (wave 5, 02/09/2026).
        """
        if geo_config is None:
            return []
        achados = check_content(text, rotulo, geo_config=geo_config, unidade="modulo")
        return [a for a in achados if a.categoria == "geo"]

    def check_html(
        self,
        html: str,
        curso_id: str = "unknown",
        module_name: str = "",
        unidade: str = "modulo",
    ) -> GateResult:
        """Valida HTML completo com todas as verificações."""
        result = self.check_text(html, curso_id, module_name, unidade=unidade)

        # 4. Verificação de HTML
        html_errors = validate_html(html)
        if html_errors:
            result.html_ok = False
            result.aprovado = False
            for e in html_errors:
                loc = f" (linha {e.linha})" if e.linha else ""
                result.erros.append(f"HTML [{e.tipo}]{loc}: {e.mensagem}")
        result.relatorios.append(html_report(html_errors))

        logger.info("Quality gate (HTML) para '%s': %s",
                     curso_id, "APROVADO" if result.aprovado else "REPROVADO")
        return result

    def to_quality_report(self, gate_result: GateResult, curso_id: str) -> QualityReport:
        """Converte GateResult para o modelo QualityReport."""
        return QualityReport(
            curso_id=curso_id,
            timestamp=datetime.now(UTC),
            acentuacao_ok=gate_result.acentuacao_ok,
            html_ok=gate_result.html_ok,
            links_ok=gate_result.links_ok,
            aprovado=gate_result.aprovado,
            erros=gate_result.erros,
            avisos=gate_result.avisos,
        )

    def full_report(self, gate_result: GateResult) -> str:
        """Gera relatório completo formatado."""
        status = "APROVADO" if gate_result.aprovado else "REPROVADO"
        linhas = [
            "=" * 60,
            f"  QUALITY GATE: {status}",
            "=" * 60,
            "",
        ]

        if gate_result.acentos_corrigidos > 0:
            linhas.append(
                f"  Auto-correção: {gate_result.acentos_corrigidos} acento(s) corrigido(s)"
            )
            linhas.append("")

        for rel in gate_result.relatorios:
            linhas.append(rel)
            linhas.append("")

        if gate_result.erros:
            linhas.append(f"Erros bloqueantes: {len(gate_result.erros)}")
        if gate_result.avisos:
            linhas.append(f"Avisos: {len(gate_result.avisos)}")

        linhas.append("=" * 60)
        return "\n".join(linhas)
