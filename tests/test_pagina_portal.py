"""Regras P1 a P5 da pasta do curso no portal (Etapas 3 e 4, 14 e 15/10/2026)."""

from __future__ import annotations

from pathlib import Path

from src.validators.pagina_portal_checker import conferir_pasta

PAGE_OK = """import CoursePage from "@/components/course/CoursePage";
import { STEPS } from "./steps";
import { courseContentJsonPath, deferStepContent } from "@/lib/course-deferred-content";
export default function Page() { return null; }
"""
STEPS_OK = """import { carregarCurso } from "@/lib/educacao/conteudo/carregar";
export const STEPS = carregarCurso("exemplo");
"""


def _pasta(
    tmp_path: Path, page: str = PAGE_OK, steps: str = STEPS_OK, extra: dict[str, str] | None = None
) -> Path:
    (tmp_path / "page.tsx").write_text(page, encoding="utf-8")
    (tmp_path / "steps.ts").write_text(steps, encoding="utf-8")
    for nome, texto in (extra or {}).items():
        (tmp_path / nome).write_text(texto, encoding="utf-8")
    return tmp_path


def _regras(tmp_path: Path, **kw) -> set[str]:
    return {a.regra for a in conferir_pasta(_pasta(tmp_path, **kw)).erros}


def test_pasta_no_contrato_passa(tmp_path):
    assert conferir_pasta(_pasta(tmp_path)).aprovado


def test_p1_pagina_de_cliente_reprova(tmp_path):
    assert "P1" in _regras(tmp_path, page='"use client";\n' + PAGE_OK)


def test_p1_ignora_use_client_em_comentario(tmp_path):
    assert "P1" not in _regras(tmp_path, page='// sem "use client" aqui de propósito\n' + PAGE_OK)


def test_p2_steps_sem_carregar_reprova(tmp_path):
    assert "P2" in _regras(tmp_path, steps="export const STEPS = [];\n")


def test_p2_conteudo_inline_reprova(tmp_path):
    steps = STEPS_OK + 'export const X = [{ id: "a", content: [ { type: "p" } ] }];\n'
    assert "P2" in _regras(tmp_path, steps=steps)


def test_p3_pagina_sem_sob_demanda_reprova(tmp_path):
    page = 'import { STEPS } from "./steps";\nexport default function Page() { return null; }\n'
    assert "P3" in _regras(tmp_path, page=page)


def test_p4_import_do_json_reprova(tmp_path):
    extra = {"glossario.ts": 'import dados from "@/content/cursos/exemplo.json";\n'}
    assert "P4" in _regras(tmp_path, extra=extra)


def test_p5_url_undefined_reprova(tmp_path):
    extra = {"fontes.ts": 'export const F = [{ title: "x", url: undefined }];\n'}
    assert "P5" in _regras(tmp_path, extra=extra)


def test_paginas_ausentes(tmp_path):
    assert {a.regra for a in conferir_pasta(tmp_path).erros} == {"P0"}
