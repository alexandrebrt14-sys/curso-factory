"""Testes do Tutor IA runtime (Wave 7) — agente conversacional.

Garantem que:
- Inicialização funciona em dry_run (sem chave de API, essencial em CI).
- Os 3 modos retornam strings não-vazias coerentes em PT-BR.
- TutorMemory cumpre add / history / clear / limit.
- Persona é injetada no prompt construído.
- Prompt template é carregado de tutor.md.

Não dependem de LLM real nem rede.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.agents.tutor import Tutor, TutorMode  # noqa: E402
from src.agents.tutor_memory import TutorMemory, TutorTurn  # noqa: E402


# ─── Tutor: inicialização ─────────────────────────────────────────────────


def test_tutor_inicializa_em_dry_run_sem_client():
    """Em dry_run, Tutor pode ser criado sem LLMClient."""
    tutor = Tutor(dry_run=True)
    assert tutor.dry_run is True
    assert tutor.persona == "curiosa-paciente"
    assert tutor.client is None


def test_tutor_exige_client_fora_de_dry_run():
    """Sem dry_run e sem client deve dar ValueError claro."""
    with pytest.raises(ValueError, match="dry_run"):
        Tutor(dry_run=False)


def test_tutor_persona_customizavel():
    """Persona é configurável via construtor."""
    tutor = Tutor(dry_run=True, persona="analitico-objetivo")
    assert tutor.persona == "analitico-objetivo"


def test_tutor_model_override():
    """Parâmetro model sobrescreve o default."""
    tutor = Tutor(dry_run=True, model="claude-sonnet-4-6")
    assert tutor.model == "claude-sonnet-4-6"


# ─── Tutor: respond() em dry_run ──────────────────────────────────────────


@pytest.mark.parametrize(
    "mode",
    [TutorMode.EXPLAIN_LIKE_5, TutorMode.PRACTICAL_EXAMPLE, TutorMode.QUIZ_ME],
)
def test_tutor_respond_dry_run_retorna_string_nao_vazia(mode):
    """Cada um dos 3 modos retorna texto coerente em dry_run."""
    tutor = Tutor(dry_run=True)
    resposta = tutor.respond(
        question="Como funciona prompt caching?",
        mode=mode,
        course_context="Curso de exemplo sobre engenharia de prompts.",
        student_history=[],
    )
    assert isinstance(resposta, str)
    assert len(resposta) > 50, f"Resposta vazia ou muito curta para {mode}"
    # Sem disclaimers de IA proibidos.
    assert "como modelo de linguagem" not in resposta.lower()
    assert "como uma ia" not in resposta.lower()


def test_tutor_respond_quiz_me_termina_com_pergunta():
    """Modo QUIZ_ME deve devolver uma pergunta (texto contém '?')."""
    tutor = Tutor(dry_run=True)
    resposta = tutor.respond(
        question="Quero treinar minha intuição em FinOps de LLM.",
        mode=TutorMode.QUIZ_ME,
        course_context="Curso de FinOps aplicado a LLMs.",
    )
    assert "?" in resposta


def test_tutor_respond_modo_invalido_levanta():
    """Passar string em vez de TutorMode deve falhar com TypeError."""
    tutor = Tutor(dry_run=True)
    with pytest.raises(TypeError, match="TutorMode"):
        tutor.respond(
            question="...",
            mode="explain_like_5",  # type: ignore[arg-type]
            course_context="...",
        )


def test_tutor_respond_aceita_history_none():
    """student_history=None deve ser tratado como lista vazia."""
    tutor = Tutor(dry_run=True)
    resposta = tutor.respond(
        question="Teste",
        mode=TutorMode.EXPLAIN_LIKE_5,
        course_context="Curso de teste.",
        student_history=None,
    )
    assert isinstance(resposta, str) and resposta


# ─── Tutor: build_prompt() ────────────────────────────────────────────────


def test_tutor_build_prompt_injeta_persona():
    """Persona aparece literalmente no prompt construído."""
    tutor = Tutor(dry_run=True, persona="mentora-direta")
    prompt = tutor.build_prompt(
        question="Por que cache importa?",
        course_context="Curso X.",
        student_history="(vazio)",
    )
    assert "mentora-direta" in prompt


def test_tutor_build_prompt_injeta_question_e_course_context():
    """Variáveis question e course_context são substituídas."""
    tutor = Tutor(dry_run=True)
    prompt = tutor.build_prompt(
        question="MINHA_PERGUNTA_UNICA",
        course_context="MEU_CURSO_UNICO",
        student_history="(vazio)",
    )
    assert "MINHA_PERGUNTA_UNICA" in prompt
    assert "MEU_CURSO_UNICO" in prompt


def test_tutor_prompt_template_carregado_de_arquivo():
    """O arquivo tutor.md em src/templates/prompts/ é carregado de fato."""
    template_path = (
        ROOT / "src" / "templates" / "prompts" / "tutor.md"
    )
    assert template_path.exists(), "tutor.md ausente — Wave 7 incompleta."

    tutor = Tutor(dry_run=True)
    template = tutor._load_prompt_template()
    assert "{persona}" in template
    assert "{question}" in template
    assert "{course_context}" in template
    # Sentinela: deve mencionar os 3 modos.
    assert "EXPLAIN_LIKE_5" in template
    assert "PRACTICAL_EXAMPLE" in template
    assert "QUIZ_ME" in template


# ─── TutorMemory ──────────────────────────────────────────────────────────


def test_tutor_memory_add_history_clear():
    """Fluxo básico: add registra, history retorna, clear apaga."""
    mem = TutorMemory(student_id="aluno-1", course_slug="curso-x")
    assert len(mem) == 0
    assert mem.history() == []

    mem.add("Pergunta A?", "Resposta A.")
    mem.add("Pergunta B?", "Resposta B.")

    hist = mem.history()
    assert len(hist) == 2
    assert hist[0]["question"] == "Pergunta A?"
    assert hist[1]["answer"] == "Resposta B."

    mem.clear()
    assert len(mem) == 0
    assert mem.history() == []


def test_tutor_memory_respeita_limit():
    """history(limit=N) devolve no máximo N turnos, mais recentes primeiro
    em ordem cronológica crescente."""
    mem = TutorMemory(student_id="aluno-1", course_slug="curso-x")
    for i in range(5):
        mem.add(f"P{i}?", f"R{i}.")

    hist = mem.history(limit=3)
    assert len(hist) == 3
    # Os 3 últimos: P2, P3, P4.
    assert hist[0]["question"] == "P2?"
    assert hist[2]["question"] == "P4?"


def test_tutor_memory_limit_zero_retorna_vazio():
    """limit=0 ou negativo devolve lista vazia (defensive)."""
    mem = TutorMemory(student_id="x", course_slug="y")
    mem.add("Q", "A")
    assert mem.history(limit=0) == []
    assert mem.history(limit=-5) == []


def test_tutor_memory_max_turns_aplica_fifo():
    """Quando excede max_turns, o mais antigo é descartado."""
    mem = TutorMemory(student_id="x", course_slug="y", max_turns=3)
    for i in range(5):
        mem.add(f"P{i}?", f"R{i}.")
    # Apenas os 3 últimos devem sobrar (P2, P3, P4).
    assert len(mem) == 3
    hist = mem.history(limit=10)
    assert hist[0]["question"] == "P2?"
    assert hist[-1]["question"] == "P4?"


def test_tutor_memory_exige_ids_nao_vazios():
    """student_id e course_slug vazios devem dar ValueError."""
    with pytest.raises(ValueError, match="student_id"):
        TutorMemory(student_id="", course_slug="curso")
    with pytest.raises(ValueError, match="course_slug"):
        TutorMemory(student_id="aluno", course_slug="")


def test_tutor_turn_serializa_dict():
    """TutorTurn.as_dict() devolve campos esperados pelo prompt."""
    turn = TutorTurn(question="Q", answer="A", timestamp=1234567890.0)
    d = turn.as_dict()
    assert d["question"] == "Q"
    assert d["answer"] == "A"
    assert d["timestamp"] == "1234567890.0"


# ─── TutorMode enum ───────────────────────────────────────────────────────


def test_tutor_mode_values_estaveis():
    """Valores do enum são strings estáveis (compatíveis com JSON)."""
    assert TutorMode.EXPLAIN_LIKE_5.value == "explain_like_5"
    assert TutorMode.PRACTICAL_EXAMPLE.value == "practical_example"
    assert TutorMode.QUIZ_ME.value == "quiz_me"


def test_tutor_mode_construct_from_string():
    """TutorMode('explain_like_5') reconstrói o enum corretamente."""
    assert TutorMode("explain_like_5") == TutorMode.EXPLAIN_LIKE_5
    assert TutorMode("quiz_me") == TutorMode.QUIZ_ME
