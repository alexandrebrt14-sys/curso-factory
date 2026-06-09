"""Render de video de abertura de curso (Remotion).

Aciona o subprojeto Node em `remotion/` via `npx remotion render`, passando os
campos do CourseDefinition como props. Mantido fora do pipeline de geracao de
conteudo: e um passo opcional de divulgacao, acionado por `python cli.py
render-video` ou quando o curso define `intro_video: True`.

Node-only: requer Node/npm instalados. Nao adiciona dependencia Python.
"""

from __future__ import annotations

import json
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.models import CourseDefinition

# Raiz do subprojeto Remotion (curso-factory/remotion).
REMOTION_DIR = Path(__file__).resolve().parents[2] / "remotion"
COMPOSITION_ID = "CourseIntro"


class VideoRenderError(RuntimeError):
    """Falha ao renderizar o video (Node ausente, deps faltando, render quebrou)."""


def _course_to_props(course: "CourseDefinition") -> dict:
    """Mapeia o CourseDefinition para as props da composicao CourseIntro."""
    return {
        "titulo": course.titulo,
        "nivel": course.nivel_display,
        "modulos": len(course.steps) or 0,
        "duracao": course.duracao_display,
        "corDestaque": course.hero_gradient_to,
    }


def _ensure_node() -> None:
    if shutil.which("npx") is None:
        raise VideoRenderError(
            "npx/Node nao encontrado no PATH. Instale Node 18+ para renderizar video."
        )


def _ensure_deps() -> None:
    """Instala as dependencias do subprojeto Remotion na primeira execucao."""
    if (REMOTION_DIR / "node_modules").is_dir():
        return
    print("[render-video] instalando dependencias do subprojeto Remotion...")
    result = subprocess.run(
        ["npm", "install"],
        cwd=REMOTION_DIR,
        capture_output=True,
        text=True,
        shell=False,
    )
    if result.returncode != 0:
        raise VideoRenderError(
            f"npm install falhou no subprojeto Remotion:\n{result.stderr[-2000:]}"
        )


def render_course_intro(
    course: "CourseDefinition",
    out_path: Path | str,
) -> Path:
    """Renderiza o MP4 de abertura a partir de um CourseDefinition."""
    return render_intro(_course_to_props(course), out_path, slug=course.slug)


def render_intro(
    props: dict,
    out_path: Path | str,
    slug: str = "intro",
) -> Path:
    """Renderiza a composicao CourseIntro com props arbitrarias.

    Args:
        props: campos da composicao (titulo, nivel, modulos, duracao, corDestaque).
        out_path: caminho do .mp4 de saida.
        slug: rotulo apenas para log.

    Raises:
        VideoRenderError: se Node faltar, deps falharem ou o render quebrar.
    """
    if not REMOTION_DIR.is_dir():
        raise VideoRenderError(f"Subprojeto Remotion nao encontrado em {REMOTION_DIR}")

    _ensure_node()
    _ensure_deps()

    out_path = Path(out_path).resolve()
    out_path.parent.mkdir(parents=True, exist_ok=True)

    # Props via arquivo temporario (evita problemas de escaping de JSON no shell).
    with tempfile.NamedTemporaryFile(
        "w", suffix=".json", delete=False, encoding="utf-8"
    ) as tmp:
        json.dump(props, tmp, ensure_ascii=False)
        props_file = Path(tmp.name)

    try:
        cmd = [
            "npx",
            "remotion",
            "render",
            "src/index.ts",
            COMPOSITION_ID,
            str(out_path),
            f"--props={props_file}",
        ]
        print(f"[render-video] {slug} -> {out_path}")
        result = subprocess.run(
            cmd,
            cwd=REMOTION_DIR,
            capture_output=True,
            text=True,
            shell=False,
        )
        if result.returncode != 0:
            raise VideoRenderError(
                f"remotion render falhou:\n{result.stderr[-2000:]}"
            )
    finally:
        props_file.unlink(missing_ok=True)

    if not out_path.is_file():
        raise VideoRenderError(f"Render terminou mas {out_path} nao existe.")
    return out_path
