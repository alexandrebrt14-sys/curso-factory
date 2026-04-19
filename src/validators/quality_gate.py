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
from datetime import datetime
from pathlib import Path
from typing import TYPE_CHECKING, Optional

from src.models import QualityReport
from src.validators.accent_checker import (
    check_accents,
    fix_accents,
    format_report as accent_report,
)
from src.validators.content_checker import (
    check_content,
    format_report as content_report,
)
from src.validators.html_validator import validate_html, format_report as html_report
from src.validators.link_checker import check_links, format_report as link_report
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
    erros: list[str] = field(default_factory=list)
    avisos: list[str] = field(default_factory=list)
    relatorios: list[str] = field(default_factory=list)
    texto_corrigido: str = ""
    acentos_corrigidos: int = 0
    voice_guard_score: int = 0


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
        base_dir: Optional[Path] = None,
        auto_fix: bool = True,
        client: "ClientContext | None" = None,
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
    ) -> GateResult:
        """Valida texto puro (Markdown) com todas as verificações.

        Executa: acentuação, conteúdo, links.
        Se auto_fix=True, corrige acentos automaticamente.
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

        # 2. Verificação de qualidade de conteúdo
        content_errors = check_content(working_text, module_name)
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

        logger.info("Quality gate (texto) para '%s': %s (vg_score=%d)",
                     curso_id,
                     "APROVADO" if result.aprovado else "REPROVADO",
                     vg.score)
        return result

    def check_html(
        self,
        html: str,
        curso_id: str = "unknown",
        module_name: str = "",
    ) -> GateResult:
        """Valida HTML completo com todas as verificações."""
        result = self.check_text(html, curso_id, module_name)

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
            timestamp=datetime.utcnow(),
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
