"""Agentes do pipeline (um por etapa) e a fachada `CourseFactory`.

`Tutor`/`TutorMemory` (runtime de tutoria) e `Translator` (multi-idioma)
ficam fora da fachada: são importados pelo caminho completo por quem os usa
(`examples/tutor_api.py`, testes).
"""

from src.agents.analyzer import Analyzer
from src.agents.base import Agent
from src.agents.classifier import Classifier
from src.agents.humanizer import Humanizer, HumanizerResult, humanize_if_enabled
from src.agents.researcher import Researcher
from src.agents.reviewer import Reviewer
from src.agents.writer import Writer


def __getattr__(name: str):
    # `CourseFactory` importa o orquestrador, que importa os agentes: carregar
    # aqui de forma preguiçosa evita o ciclo no import do pacote.
    if name == "CourseFactory":
        from src.agents.pipeline import CourseFactory

        return CourseFactory
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


__all__ = [
    "Agent",
    "Analyzer",
    "Classifier",
    "CourseFactory",
    "Humanizer",
    "HumanizerResult",
    "Researcher",
    "Reviewer",
    "Writer",
    "humanize_if_enabled",
]
