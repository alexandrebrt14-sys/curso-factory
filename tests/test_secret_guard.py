"""Testes do pre-commit secret_guard (.tools/secret_guard.py) — issue #17.

As chaves falsas sao construidas em runtime por concatenacao para que este
proprio arquivo nunca contenha um literal que casaria com os padroes de
segredo (senao o gitleaks do CI e o proprio guard bloqueariam o commit).
"""

from __future__ import annotations

import importlib.util
import subprocess
import sys
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parent.parent
GUARD_PATH = PROJECT_ROOT / ".tools" / "secret_guard.py"


def _load_guard():
    spec = importlib.util.spec_from_file_location("secret_guard", GUARD_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


guard = _load_guard()

# Chaves falsas montadas em runtime (nunca literais completos no source)
FAKE_OPENAI_PROJ = "sk-" + "proj-" + "Ab1" * 20
FAKE_ANTHROPIC = "sk-" + "ant-" + "api03-" + "Xy9" * 20
FAKE_GOOGLE = "AIza" + "B" * 35
FAKE_GITHUB_PAT = "ghp" + "_" + "C1d2" * 9
FAKE_AWS = "AKIA" + "ABCDEFGHIJKLMNOP"


class TestScanContent:
    def test_detecta_chave_openai_project(self):
        findings = guard.scan_content(f"OPENAI_API_KEY={FAKE_OPENAI_PROJ}")
        assert findings, "chave sk-proj falsa deveria ser detectada"

    def test_detecta_chave_anthropic(self):
        findings = guard.scan_content(f"key = '{FAKE_ANTHROPIC}'")
        assert findings

    def test_detecta_chave_google(self):
        findings = guard.scan_content(f"GOOGLE_API_KEY={FAKE_GOOGLE}")
        assert findings

    def test_detecta_github_pat(self):
        findings = guard.scan_content(f"token: {FAKE_GITHUB_PAT}")
        assert findings

    def test_detecta_aws_access_key(self):
        findings = guard.scan_content(f"aws_access_key_id = {FAKE_AWS}")
        assert findings

    def test_snippet_e_redacted(self):
        findings = guard.scan_content(f"OPENAI_API_KEY={FAKE_OPENAI_PROJ}")
        for _label, redacted, _context in findings:
            assert FAKE_OPENAI_PROJ not in redacted, "segredo completo nao pode aparecer no log"

    def test_placeholder_nao_dispara(self):
        content = "ANTHROPIC_API_KEY=" + "sk-" + "ant-" + "api03-" + "X" * 54
        findings = guard.scan_content(content)
        assert findings == [], "placeholder uppercase do .env.example nao deveria disparar"

    def test_conteudo_limpo_nao_dispara(self):
        findings = guard.scan_content("def soma(a, b):\n    return a + b\n")
        assert findings == []


class TestEnvFileBlocked:
    @pytest.mark.parametrize(
        "filename",
        [".env", ".env.local", ".env.production", "subdir/.env"],
    )
    def test_bloqueia_env(self, filename):
        blocked, reason = guard.is_env_file_blocked(filename)
        assert blocked, f"{filename} deveria ser bloqueado ({reason})"

    @pytest.mark.parametrize(
        "filename",
        [".env.example", ".env.sample", ".env.template", "config/app.yaml"],
    )
    def test_permite_exemplos_e_arquivos_normais(self, filename):
        blocked, _reason = guard.is_env_file_blocked(filename)
        assert not blocked, f"{filename} nao deveria ser bloqueado"


class TestCliFileMode:
    """Integracao: invoca o guard como o hook faria, em modo --file."""

    def _run(self, path: Path) -> subprocess.CompletedProcess:
        return subprocess.run(
            [sys.executable, str(GUARD_PATH), "--file", str(path)],
            capture_output=True,
            text=True,
            check=False,
        )

    def test_arquivo_com_segredo_retorna_1(self, tmp_path):
        alvo = tmp_path / "config.py"
        alvo.write_text(f'OPENAI_API_KEY = "{FAKE_OPENAI_PROJ}"\n', encoding="utf-8")
        result = self._run(alvo)
        assert result.returncode == 1
        assert "SEGREDO DETECTADO" in result.stderr

    def test_arquivo_limpo_retorna_0(self, tmp_path):
        alvo = tmp_path / "app.py"
        alvo.write_text("print('sem segredos aqui')\n", encoding="utf-8")
        result = self._run(alvo)
        assert result.returncode == 0
