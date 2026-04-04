# Artefato canônico — consumido por landing-page-geo via worker, não por escrita direta
"""Emite o catálogo canônico de cursos como artefato JSON.

Lê os metadados dos cursos a partir de config/courses.yaml e dos diretórios
em output/approved/ e output/deployed/, e grava output/course_catalog.json.

A landing-page-geo NÃO é referenciada aqui. O artefato gerado é consumido
por um processo externo (worker, CI/CD) que conhece a estrutura da landing page.
"""

from __future__ import annotations

import json
import logging
from datetime import datetime, timezone
from pathlib import Path

logger = logging.getLogger(__name__)

# Raiz do projeto (dois níveis acima deste arquivo: src/generators/ -> src/ -> raiz)
_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
_OUTPUT_DIR = _PROJECT_ROOT / "output"
_CONFIG_DIR = _PROJECT_ROOT / "config"


class MetadataSync:
    """Gera o artefato course_catalog.json a partir de metadados internos do curso-factory."""

    def __init__(self, output_dir: Path | None = None) -> None:
        """
        Args:
            output_dir: Diretório de saída onde course_catalog.json será gravado.
                        Padrão: output/ na raiz do projeto.
        """
        self.output_dir = output_dir if output_dir is not None else _OUTPUT_DIR
        self.catalog_path = self.output_dir / "course_catalog.json"

    def sync(self) -> dict:
        """Varre metadados internos e grava output/course_catalog.json.

        Não acessa nenhum caminho externo ao curso-factory. A landing page
        consome este artefato via worker independente.

        Returns:
            Dicionário com status da operação:
            - ok: bool indicando sucesso
            - course_count: número de cursos incluídos no catálogo
            - catalog_path: caminho absoluto do artefato gerado
            - errors: lista de erros, se houver
        """
        result: dict = {
            "ok": False,
            "course_count": 0,
            "catalog_path": str(self.catalog_path),
            "errors": [],
        }

        # Garante que o diretório de saída existe
        try:
            self.output_dir.mkdir(parents=True, exist_ok=True)
        except OSError as exc:
            result["errors"].append(f"Não foi possível criar output_dir: {exc}")
            return result

        courses = self._collect_courses()
        result["course_count"] = len(courses)
        logger.info("Cursos coletados para o catálogo: %d", len(courses))

        catalog = {
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "course_count": len(courses),
            "courses": courses,
        }

        # Escrita atômica: grava em .tmp e renomeia
        tmp_path = self.catalog_path.with_suffix(".json.tmp")
        try:
            tmp_path.write_text(
                json.dumps(catalog, ensure_ascii=False, indent=2),
                encoding="utf-8",
            )
            tmp_path.replace(self.catalog_path)
            logger.info("course_catalog.json gravado em: %s", self.catalog_path)
        except OSError as exc:
            result["errors"].append(f"Erro ao gravar course_catalog.json: {exc}")
            if tmp_path.exists():
                tmp_path.unlink(missing_ok=True)
            return result

        result["ok"] = True
        return result

    # ------------------------------------------------------------------
    # Métodos internos — sem referência a caminhos externos
    # ------------------------------------------------------------------

    def _collect_courses(self) -> list[dict]:
        """Coleta metadados de cursos a partir de courses.yaml e dos diretórios output/.

        Prioridade de dados: deployed > approved > courses.yaml.

        Returns:
            Lista de dicts com metadados canônicos de cada curso.
        """
        # 1. Base: courses.yaml
        base_courses = self._load_yaml_courses()

        # 2. Enriquece com status de output/
        deployed_slugs = self._list_slugs(self.output_dir / "deployed")
        approved_slugs = self._list_slugs(self.output_dir / "approved")

        enriched: list[dict] = []
        for course in base_courses:
            slug = course.get("slug", "")
            status = "planejado"
            if slug in deployed_slugs:
                status = "deployed"
            elif slug in approved_slugs:
                status = "approved"

            enriched.append({
                "slug": slug,
                "nome": course.get("nome", ""),
                "nivel": course.get("nivel", ""),
                "modulos": course.get("modulos", 0),
                "descricao": str(course.get("descricao", "")).strip(),
                "tags": course.get("tags", []),
                "prerequisitos": course.get("prerequisitos", []),
                "duracao_estimada": course.get("duracao_estimada", ""),
                "prioridade": course.get("prioridade", ""),
                "status": status,
            })

        return enriched

    def _load_yaml_courses(self) -> list[dict]:
        """Carrega a lista de cursos de config/courses.yaml."""
        courses_path = _CONFIG_DIR / "courses.yaml"
        if not courses_path.exists():
            logger.warning("courses.yaml não encontrado: %s", courses_path)
            return []
        try:
            import yaml  # import local para não exigir yaml em contextos sem config
            with open(courses_path, "r", encoding="utf-8") as fh:
                data = yaml.safe_load(fh)
            if not data:
                return []
            return data.get("courses", data) if isinstance(data, dict) else list(data)
        except Exception as exc:  # noqa: BLE001
            logger.error("Erro ao carregar courses.yaml: %s", exc)
            return []

    def _list_slugs(self, directory: Path) -> set[str]:
        """Retorna os slugs (nomes de subdiretórios) presentes em um diretório output/."""
        if not directory.is_dir():
            return set()
        return {entry.name for entry in directory.iterdir() if entry.is_dir()}
