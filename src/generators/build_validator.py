"""Validador de build Next.js para os arquivos TSX gerados.

Executa `npx next build` e verifica a sintaxe básica dos arquivos
TSX antes de submeter ao build completo.
"""

from __future__ import annotations

import logging
import subprocess
from pathlib import Path

logger = logging.getLogger(__name__)


class BuildValidator:
    """Valida arquivos TSX gerados via build Next.js e verificação de sintaxe."""

    def __init__(self, landing_page_dir: Path, timeout: int = 300) -> None:
        self.landing_page_dir = landing_page_dir
        self.timeout = timeout

    def validate(self) -> dict:
        """Executa `npx next build` e retorna resultado.

        Returns:
            Dicionário com:
            - ok: bool indicando se o build passou
            - exit_code: código de saída do processo
            - errors: lista de erros extraídos do output
        """
        result = {
            "ok": False,
            "exit_code": -1,
            "errors": [],
        }

        if not self.landing_page_dir.exists():
            result["errors"].append(
                f"Diretório da landing page não encontrado: {self.landing_page_dir}"
            )
            return result

        logger.info(
            "Iniciando build Next.js em: %s (timeout: %ds)",
            self.landing_page_dir,
            self.timeout,
        )

        try:
            proc = subprocess.run(
                ["npx", "next", "build"],
                cwd=str(self.landing_page_dir),
                capture_output=True,
                text=True,
                timeout=self.timeout,
                shell=True,
            )

            result["exit_code"] = proc.returncode

            if proc.returncode == 0:
                result["ok"] = True
                logger.info("Build Next.js concluído com sucesso")
            else:
                errors = self._extract_errors(proc.stderr + proc.stdout)
                result["errors"] = errors
                logger.error(
                    "Build Next.js falhou (exit_code=%d): %d erros",
                    proc.returncode,
                    len(errors),
                )

        except subprocess.TimeoutExpired:
            result["errors"].append(
                f"Build excedeu o timeout de {self.timeout} segundos"
            )
            logger.error("Build Next.js excedeu timeout de %ds", self.timeout)
        except FileNotFoundError:
            result["errors"].append(
                "Comando 'npx' não encontrado. Verifique se o Node.js está instalado."
            )
            logger.error("npx não encontrado no PATH")
        except OSError as exc:
            result["errors"].append(f"Erro ao executar build: {exc}")
            logger.error("Erro de OS ao executar build: %s", exc)

        return result

    @staticmethod
    def validate_tsx_syntax(content: str) -> list[str]:
        """Verificação rápida de sintaxe TSX antes do build completo.

        Checa:
        - Presença de "use client" (obrigatório para componentes interativos)
        - Presença de export default
        - Balanceamento de chaves { }
        - Balanceamento de parênteses ( )
        - Balanceamento de colchetes [ ]

        Args:
            content: Conteúdo do arquivo TSX como string.

        Returns:
            Lista de erros encontrados (vazia se tudo OK).
        """
        errors: list[str] = []

        if not content or not content.strip():
            errors.append("Conteúdo TSX está vazio")
            return errors

        # Verifica "use client"
        if '"use client"' not in content and "'use client'" not in content:
            errors.append(
                'Diretiva "use client" não encontrada. '
                "Necessária para componentes com interatividade."
            )

        # Verifica export default
        if "export default" not in content:
            errors.append(
                "Nenhum 'export default' encontrado. "
                "O componente principal precisa ser exportado."
            )

        # Balanceamento de chaves
        open_braces = content.count("{")
        close_braces = content.count("}")
        if open_braces != close_braces:
            errors.append(
                f"Chaves desbalanceadas: {open_braces} abertas vs "
                f"{close_braces} fechadas"
            )

        # Balanceamento de parênteses
        open_parens = content.count("(")
        close_parens = content.count(")")
        if open_parens != close_parens:
            errors.append(
                f"Parênteses desbalanceados: {open_parens} abertos vs "
                f"{close_parens} fechados"
            )

        # Balanceamento de colchetes
        open_brackets = content.count("[")
        close_brackets = content.count("]")
        if open_brackets != close_brackets:
            errors.append(
                f"Colchetes desbalanceados: {open_brackets} abertos vs "
                f"{close_brackets} fechados"
            )

        return errors

    @staticmethod
    def _extract_errors(output: str) -> list[str]:
        """Extrai mensagens de erro relevantes do output do build.

        Filtra linhas que contêm indicadores de erro do Next.js/TypeScript.
        """
        if not output:
            return ["Build falhou sem output de erro"]

        error_indicators = [
            "Error:",
            "error TS",
            "TypeError:",
            "SyntaxError:",
            "Module not found",
            "Cannot find module",
            "Unexpected token",
            "failed to compile",
            "Build error",
        ]

        errors: list[str] = []
        for line in output.split("\n"):
            stripped = line.strip()
            if any(indicator in stripped for indicator in error_indicators):
                if stripped not in errors:
                    errors.append(stripped)

        if not errors and output.strip():
            # Se não encontrou padrões específicos, retorna as últimas linhas
            last_lines = [
                l.strip() for l in output.strip().split("\n")[-5:] if l.strip()
            ]
            errors = last_lines

        return errors
