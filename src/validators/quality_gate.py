"""Gate de qualidade que executa todos os validadores.

Se qualquer validador falhar, bloqueia o deploy e gera
relatório detalhado com o status de cada verificação.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Optional

from src.models import QualityReport
from src.validators.accent_checker import check_accents, format_report as accent_report
from src.validators.html_validator import validate_html, format_report as html_report
from src.validators.link_checker import check_links, format_report as link_report

logger = logging.getLogger(__name__)


@dataclass
class GateResult:
    """Resultado consolidado do quality gate."""
    aprovado: bool = True
    acentuacao_ok: bool = True
    html_ok: bool = True
    links_ok: bool = True
    erros: list[str] = field(default_factory=list)
    avisos: list[str] = field(default_factory=list)
    relatorios: list[str] = field(default_factory=list)


class QualityGate:
    """Executa todos os validadores e decide se o conteúdo pode ser publicado."""

    def __init__(self, base_dir: Optional[Path] = None) -> None:
        self.base_dir = base_dir

    def check_text(self, text: str, curso_id: str = "unknown") -> GateResult:
        """Valida texto puro (Markdown) com verificação de acentuação e links."""
        result = GateResult()

        # 1. Verificação de acentuação
        accent_errors = check_accents(text)
        if accent_errors:
            result.acentuacao_ok = False
            result.aprovado = False
            for e in accent_errors:
                result.erros.append(
                    f"Acentuação: '{e.palavra_errada}' → '{e.correcao}' (linha {e.linha})"
                )
        result.relatorios.append(accent_report(accent_errors))

        # 2. Verificação de links
        link_errors = check_links(text, self.base_dir)
        if link_errors:
            # Acentos em URLs são erro crítico; links quebrados são aviso
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

        logger.info("Quality gate (texto) para '%s': %s",
                     curso_id, "APROVADO" if result.aprovado else "REPROVADO")
        return result

    def check_html(self, html: str, curso_id: str = "unknown") -> GateResult:
        """Valida HTML completo com todas as verificações."""
        result = self.check_text(html, curso_id)

        # 3. Verificação de HTML
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
            "=" * 50,
            f"  QUALITY GATE: {status}",
            "=" * 50,
            "",
        ]
        for rel in gate_result.relatorios:
            linhas.append(rel)
            linhas.append("")

        if gate_result.erros:
            linhas.append(f"Erros bloqueantes: {len(gate_result.erros)}")
        if gate_result.avisos:
            linhas.append(f"Avisos: {len(gate_result.avisos)}")

        linhas.append("=" * 50)
        return "\n".join(linhas)
