"""LGPD nos prompts: orientação, não remoção (11/10/2026, decisão do dono).

O #98 tirou a menção à lei de dados do gate que reprova (`R9_lgpd` virou
aviso), mas os prompts dos agentes e os templates seguiam mandando remover o
nome da lei ou reprovar a aula por ele. Aqui se cobra a orientação nova:
evitar menção desnecessária, citar com precisão quando citar, e nunca tratar
a menção como motivo para reprovar.
"""

from __future__ import annotations

from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parent.parent

ARQUIVOS = [
    "src/agents/reviewer.py",
    "src/agents/writer.py",
    "src/agents/analyzer.py",
    "src/orchestrator.py",
    *sorted(
        str(p.relative_to(PROJECT_ROOT)).replace("\\", "/")
        for p in (PROJECT_ROOT / "src" / "templates" / "prompts").rglob("*.md")
    ),
]

#: Frases que mandavam remover ou proibir a menção à lei de dados.
ORDENS_DE_REMOCAO = (
    "QUALQUER menção à LGPD",
    "nem LGPD",
    "sem LGPD",
    "nem menção à LGPD",
    "menção à LGPD, linha",
    "'checkpoint' ou LGPD",
    "o nome da lei sai",
    "não é\n  nomeada",
    "é nomeada de forma nenhuma",
    "ANY mention of the data protection law",
    "the name goes",
    "is never named",
    "law by name",
    "the data protection law named",
    "CUALQUIER mención a la ley de protección",
    "el nombre\n  sale",
    "no se nombra",
    "por su nombre",
    "la ley de protección de datos nombrada",
)


@pytest.mark.parametrize("rel", ARQUIVOS)
def test_prompt_nao_manda_remover_lgpd(rel: str) -> None:
    texto = (PROJECT_ROOT / rel).read_text(encoding="utf-8")
    achados = [f for f in ORDENS_DE_REMOCAO if f in texto]
    assert achados == [], f"{rel}: {achados}"


@pytest.mark.parametrize(
    "rel",
    [
        "src/agents/reviewer.py",
        "src/agents/writer.py",
        "src/agents/analyzer.py",
        "src/templates/prompts/pt-br/draft.md",
        "src/templates/prompts/pt-br/review.md",
        "src/templates/prompts/pt-br/analyze.md",
        "src/templates/prompts/en/draft.md",
        "src/templates/prompts/en/review.md",
        "src/templates/prompts/en/analyze.md",
        "src/templates/prompts/es/draft.md",
        "src/templates/prompts/es/review.md",
        "src/templates/prompts/es/analyze.md",
    ],
)
def test_prompt_orienta_mencao_precisa_sem_reprovar(rel: str) -> None:
    # Espaços e quebras de linha normalizados: a orientação pode vir quebrada.
    texto = " ".join((PROJECT_ROOT / rel).read_text(encoding="utf-8").split())
    assert any(
        f in texto
        for f in (
            "não é motivo para reprovar",
            "not a reason to fail",
            "no es motivo para reprobar",
            "não reprova",
        )
    ), rel
    assert any(f in texto for f in ("com precisão", "con precisión", "precisely")), rel
