"""Aula abaixo do piso ganha uma passada de expansão (03/09/2026)."""

from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import src.orchestrator as mod  # noqa: E402
from src.models import Module  # noqa: E402
from src.orchestrator import _contar_palavras  # noqa: E402
from tests.test_orchestrator_aulas import _curso, orquestrador  # noqa: E402, F401

CURTA = (
    "Você vai aprender a cobrar certo.\n\n## Por que o preço muda o resultado\n\n"
    + ("Frase curta. " * 30)
    + "\n\n## Como fica no seu negócio\n\nA Ana cobrou certo.\n\n## Faça agora\n\n"
    "1. Abra a agenda.\n\n**Resultado esperado:** um preço anotado."
)
LONGA = CURTA.replace("Frase curta. " * 30, "Frase que explica a ideia por inteiro, com o exemplo do salão. " * 120)


def _aula(orq, respostas: list[str]) -> tuple[str, list[str]]:
    chamadas: list[str] = []
    fila = iter(respostas)

    def execute(contexto: str, **variaveis) -> str:
        chamadas.append(contexto)
        return next(fila)

    orq.writer.execute = execute
    modulo = Module(titulo="Preço", descricao="d", ordem=1)
    md = orq._draft_lesson(_curso(), modulo, 1, [{"titulo": "Cobre certo", "ideia": "preço"}], 0, "PESQUISA " * 400)
    return md, chamadas


def test_aula_curta_ganha_uma_passada_e_fica_com_a_versao_maior(orquestrador, monkeypatch) -> None:
    orq, _ = orquestrador
    monkeypatch.setattr(mod, "DRAFT_EXPANSAO_ABAIXO_DO_PISO", True)
    md, chamadas = _aula(orq, [CURTA, LONGA])
    assert len(chamadas) == 2
    assert "--- AULA CURTA ---" in chamadas[1] and "PESQUISA" in chamadas[1]
    assert "Frase curta." in chamadas[1]
    assert _contar_palavras(md) > 700
    assert any("foi expandida" in a for a in orq._avisos_pendentes)


def test_expansao_que_nao_cresce_mantem_o_primeiro_rascunho(orquestrador, monkeypatch) -> None:
    orq, _ = orquestrador
    monkeypatch.setattr(mod, "DRAFT_EXPANSAO_ABAIXO_DO_PISO", True)
    md, chamadas = _aula(orq, [CURTA, "Nada."])
    assert len(chamadas) == 2
    assert "Frase curta." in md
    assert any("não cresceu" in a for a in orq._avisos_pendentes)


def test_aula_no_alvo_nao_ganha_segunda_chamada(orquestrador, monkeypatch) -> None:
    orq, _ = orquestrador
    monkeypatch.setattr(mod, "DRAFT_EXPANSAO_ABAIXO_DO_PISO", True)
    _, chamadas = _aula(orq, [LONGA])
    assert len(chamadas) == 1
    assert orq._avisos_pendentes == []


def test_chave_desligada_nao_expande(orquestrador, monkeypatch) -> None:
    orq, _ = orquestrador
    monkeypatch.setattr(mod, "DRAFT_EXPANSAO_ABAIXO_DO_PISO", False)
    md, chamadas = _aula(orq, [CURTA])
    assert len(chamadas) == 1
    assert "Frase curta." in md


def test_nota_de_expansao_existe_nos_tres_idiomas() -> None:
    from src.agents.lang_resolver import resolve_prompt_path

    for lang, marca in (("pt-br", "--- AULA CURTA ---"), ("en", "--- SHORT LESSON ---"), ("es", "--- LECCIÓN CORTA ---")):
        texto = resolve_prompt_path("expand.md", lang).read_text(encoding="utf-8")
        assert marca in texto
        assert "{lesson_md}" in texto and "{palavras_piso}" in texto
