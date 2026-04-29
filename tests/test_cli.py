"""Testes de smoke para o CLI.

Garante que cada subcomando do CLI carrega o módulo certo (sem ImportError),
processa argumentos corretamente e retorna o exit code esperado em casos
sem rede (não chama LLMs reais).
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import cli  # noqa: E402


def _run(args: list[str]) -> int:
    """Executa o CLI com argv simulado e retorna exit code."""
    parser = cli.build_parser()
    parsed = parser.parse_args(args)
    return parsed.func(parsed)


# ─── parser e ajuda ──────────────────────────────────────────────────

def test_parser_has_all_commands() -> None:
    parser = cli.build_parser()
    help_text = parser.format_help()
    for cmd in [
        "create",
        "clients",
        "validate",
        "cost-report",
        "batch",
        "emit-catalog",
        "drafts-to-tsx",
        "cache-clear",
    ]:
        assert cmd in help_text, f"Subcomando '{cmd}' deveria estar registrado"


def test_parser_requires_command() -> None:
    parser = cli.build_parser()
    with pytest.raises(SystemExit):
        parser.parse_args([])


# ─── clients ──────────────────────────────────────────────────────────

def test_cmd_clients_lista_default(capsys) -> None:
    rc = _run(["clients"])
    captured = capsys.readouterr()
    assert rc == 0
    assert "default" in captured.out
    assert "voice_guard" in captured.out


# ─── validate ────────────────────────────────────────────────────────

def test_cmd_validate_path_inexistente(capsys) -> None:
    rc = _run(["validate", "C:/nao_existe_xyz_fictpath"])
    captured = capsys.readouterr()
    assert rc == 1
    assert "não encontrado" in captured.err or "nao encontrado" in captured.err.lower()


def test_cmd_validate_arquivo_aprovado(tmp_path, capsys) -> None:
    """Texto canônico-PT em diretório vazio (sem .md) sai limpo."""
    rc = _run(["validate", str(tmp_path)])
    out = capsys.readouterr().out
    assert rc == 0
    assert "Nenhum arquivo .md" in out


# ─── cost-report ─────────────────────────────────────────────────────

def test_cmd_cost_report_executa(capsys) -> None:
    rc = _run(["cost-report"])
    out = capsys.readouterr().out
    assert rc == 0
    # Sem entries vira mensagem genérica; com entries vira tabela —
    # ambos os caminhos devem retornar 0.
    assert "Curso Factory" in out or "Nenhum custo" in out


# ─── drafts-to-tsx ───────────────────────────────────────────────────

def test_cmd_drafts_to_tsx_input_inexistente(tmp_path, capsys) -> None:
    rc = _run([
        "drafts-to-tsx",
        "--input", str(tmp_path / "nao_existe"),
        "--output", str(tmp_path / "out"),
    ])
    out = capsys.readouterr().out
    assert rc == 1
    assert "ERRO" in out or "nao existe" in out


def test_cmd_drafts_to_tsx_input_vazio(tmp_path, capsys) -> None:
    """Diretório existe mas sem arquivos: 0 conversões, exit 0."""
    inp = tmp_path / "drafts"
    inp.mkdir()
    rc = _run([
        "drafts-to-tsx",
        "--input", str(inp),
        "--output", str(tmp_path / "out"),
    ])
    out = capsys.readouterr().out
    assert rc == 0
    assert "Convertidos: 0" in out


# ─── emit-catalog ────────────────────────────────────────────────────

def test_cmd_emit_catalog(tmp_path) -> None:
    rc = _run(["emit-catalog", "--output-dir", str(tmp_path)])
    catalog = tmp_path / "course_catalog.json"
    assert rc == 0
    assert catalog.exists()
    data = json.loads(catalog.read_text(encoding="utf-8"))
    assert "courses" in data
    assert "course_count" in data


# ─── batch ───────────────────────────────────────────────────────────

def test_cmd_batch_arquivo_inexistente(capsys) -> None:
    rc = _run(["batch", "C:/nao_existe_yaml.yaml"])
    err = capsys.readouterr().err
    assert rc == 1
    assert "não encontrado" in err or "nao encontrado" in err.lower()


# ─── client desconhecido ─────────────────────────────────────────────

def test_cmd_create_cliente_inexistente(capsys) -> None:
    """Cliente bobo: o CLI deve avisar e retornar exit 1, sem chamar LLM."""
    rc = _run(["create", "Curso Bobo", "--client", "cliente_inexistente_xyz"])
    err = capsys.readouterr().err
    assert rc == 1
    assert "ERRO" in err
