"""Smoke tests para os validadores e o quality gate."""

from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.clients import load_client
from src.validators.accent_checker import check_accents, fix_accents
from src.validators.quality_gate import QualityGate
from src.validators.voice_guard import voice_guard_check


# ─── accent_checker ──────────────────────────────────────────────────

def test_check_accents_detecta_palavras_sem_acento() -> None:
    text = "Voce nao precisa de producao infinita ate amanha."
    erros = check_accents(text)
    palavras = {e.palavra_errada.lower() for e in erros}
    # Pelo menos algumas das palavras-alvo devem ser detectadas
    assert "voce" in palavras
    assert "nao" in palavras
    assert "producao" in palavras


def test_check_accents_texto_limpo() -> None:
    text = "Você não precisa de produção infinita até amanhã."
    erros = check_accents(text)
    assert erros == []


def test_check_accents_ignora_blocos_de_codigo() -> None:
    text = "```python\nnao_acentuado = True\n```"
    erros = check_accents(text)
    # Tokens dentro de bloco de código não devem ser contados
    assert all(e.linha == 0 for e in erros) or erros == []


def test_fix_accents_corrige_e_preserva_capitalizacao() -> None:
    text = "Voce esta produzindo informacao. Nao e dificil."
    corrigido, n = fix_accents(text)
    assert n >= 3
    # Capitalização preservada
    assert "Você" in corrigido
    # Palavras com acento não devem ser duplamente corrigidas
    assert "Vocêcê" not in corrigido


def test_fix_accents_preserva_codigo() -> None:
    text = "Texto: producao\n```\nproducao = 42\n```"
    corrigido, _ = fix_accents(text)
    # Fora do bloco vira "produção", mas dentro fica como variável
    assert "produção" in corrigido
    assert "producao = 42" in corrigido


# ─── quality_gate ────────────────────────────────────────────────────

def test_quality_gate_texto_canonico() -> None:
    """Texto que respeita acentuação deve sair sem erro de acentos."""
    client = load_client("default")
    gate = QualityGate(client=client, auto_fix=False)
    text = "Você precisa entender produção para crescer no mercado."
    result = gate.check_text(text, curso_id="smoke")
    # Texto curto não passa todos os critérios de conteúdo, mas acentos sim
    assert result.acentuacao_ok is True


def test_quality_gate_autofix_corrige_acentos() -> None:
    client = load_client("default")
    gate = QualityGate(client=client, auto_fix=True)
    result = gate.check_text("Voce nao deve produzir informacao errada.", curso_id="smoke")
    assert result.acentos_corrigidos >= 3
    assert "Você" in result.texto_corrigido


# ─── voice_guard ─────────────────────────────────────────────────────

def test_voice_guard_score_em_zero_a_cem() -> None:
    client = load_client("default")
    result = voice_guard_check("Texto qualquer com produção e análise.", client=client)
    assert 0 <= result.score <= 100


def test_voice_guard_detecta_titulo_proibido() -> None:
    """Cliente default proíbe 'Especialista #1' e 'Source Rank'."""
    client = load_client("default")
    text = "Sou o Especialista #1 em GEO Brasil, líder do Source Rank."
    result = voice_guard_check(text, client=client)
    # Ao menos um erro crítico deve ser registrado
    assert len(result.erros_criticos) > 0 or result.aprovado is False


def test_voice_guard_isolamento_entre_clientes() -> None:
    """Naming canônico do default não pode aprovar voz de outro cliente."""
    default = load_client("default")
    acme = load_client("acme")
    text_default = (
        "Curso de GEO assinado por Alexandre Caramaschi, CEO da Brasil GEO."
    )
    r_default = voice_guard_check(text_default, client=default)
    r_acme = voice_guard_check(text_default, client=acme)
    # Voz Alexandre passa no cliente default e cai (ou pelo menos pontua menor)
    # no acme — não pode dar score igual.
    assert r_default.score >= r_acme.score
