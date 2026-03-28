"""Sincroniza metadados da landing page com os cursos gerados.

Lê o layout.tsx da seção /educacao, conta os diretórios de curso
que possuem page.tsx e atualiza as contagens no arquivo.
"""

from __future__ import annotations

import logging
from pathlib import Path

logger = logging.getLogger(__name__)


class MetadataSync:
    """Sincroniza contadores e metadados na landing page de educação."""

    def __init__(self, landing_page_dir: Path) -> None:
        self.landing_page_dir = landing_page_dir
        self.educacao_dir = landing_page_dir / "src" / "app" / "educacao"
        self.layout_path = self.educacao_dir / "layout.tsx"

    def sync(self) -> dict:
        """Lê layout.tsx, conta cursos com page.tsx e atualiza contagem.

        Usa find-and-replace em linhas específicas (título/descrição)
        para atualização atômica sem regex no arquivo inteiro.

        Returns:
            Dicionário com status da sincronização:
            - ok: bool indicando sucesso
            - course_count: número de cursos encontrados
            - updated_lines: número de linhas atualizadas
            - errors: lista de erros, se houver
        """
        result = {
            "ok": False,
            "course_count": 0,
            "updated_lines": 0,
            "errors": [],
        }

        # Verifica se o diretório de educação existe
        if not self.educacao_dir.exists():
            result["errors"].append(
                f"Diretório de educação não encontrado: {self.educacao_dir}"
            )
            return result

        # Conta diretórios de curso que possuem page.tsx
        course_count = 0
        if self.educacao_dir.is_dir():
            for entry in self.educacao_dir.iterdir():
                if entry.is_dir() and (entry / "page.tsx").exists():
                    course_count += 1

        result["course_count"] = course_count
        logger.info("Cursos encontrados com page.tsx: %d", course_count)

        # Verifica se layout.tsx existe
        if not self.layout_path.exists():
            result["errors"].append(
                f"layout.tsx não encontrado: {self.layout_path}"
            )
            return result

        # Lê conteúdo atual do layout.tsx
        content = self.layout_path.read_text(encoding="utf-8")
        original_content = content
        updated_lines = 0

        # Padrões de contagem para find-and-replace
        # Busca padrões como "X cursos" ou "X curso" em títulos/descrições
        count_patterns = self._find_count_patterns(content)

        for old_text, new_text in count_patterns:
            if old_text in content:
                content = content.replace(old_text, new_text, 1)
                if old_text != new_text:
                    updated_lines += 1
                    logger.info("Atualizado: '%s' -> '%s'", old_text, new_text)

        result["updated_lines"] = updated_lines

        # Escreve de volta apenas se houve mudança
        if content != original_content:
            # Escrita atômica: escreve em arquivo temporário e renomeia
            tmp_path = self.layout_path.with_suffix(".tsx.tmp")
            try:
                tmp_path.write_text(content, encoding="utf-8")
                tmp_path.replace(self.layout_path)
                logger.info(
                    "layout.tsx atualizado com %d alterações", updated_lines
                )
            except OSError as exc:
                result["errors"].append(f"Erro ao escrever layout.tsx: {exc}")
                if tmp_path.exists():
                    tmp_path.unlink()
                return result
        else:
            logger.info("layout.tsx já está atualizado, nenhuma alteração necessária")

        result["ok"] = True
        return result

    def _find_count_patterns(
        self, content: str
    ) -> list[tuple[str, str]]:
        """Identifica padrões de contagem no conteúdo para substituição.

        Busca linhas que contêm contagens de cursos e gera pares
        (texto_antigo, texto_novo) para substituição.

        Returns:
            Lista de tuplas (old_text, new_text).
        """
        course_count = 0
        if self.educacao_dir.is_dir():
            for entry in self.educacao_dir.iterdir():
                if entry.is_dir() and (entry / "page.tsx").exists():
                    course_count += 1

        patterns: list[tuple[str, str]] = []

        # Procura por padrões comuns de contagem em cada linha
        for line in content.split("\n"):
            stripped = line.strip()

            # Padrão: "N cursos disponíveis" ou "N cursos gratuitos" etc.
            for i in range(200):
                old_count = f"{i} curso"
                if old_count in stripped and f"{course_count} curso" not in stripped:
                    # Verifica se é "cursos" (plural) ou "curso" (singular)
                    if f"{i} cursos" in stripped:
                        new_word = "cursos" if course_count != 1 else "curso"
                        old_fragment = f"{i} cursos"
                        new_fragment = f"{course_count} {new_word}"
                    else:
                        new_word = "curso" if course_count == 1 else "cursos"
                        old_fragment = f"{i} curso"
                        new_fragment = f"{course_count} {new_word}"
                    patterns.append((old_fragment, new_fragment))
                    break

        return patterns
