"""Ajustes do checker vindos do segundo teste real (wave 7, 02/09/2026).

O redator varia a forma do exercício (H2 com título próprio, "resultado
esperado" em prosa) e as fontes vivem no rodapé da trilha. O gate precisa
reconhecer as duas coisas em vez de reprovar pelo motivo errado.
"""

from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.providers import MAX_TOKENS_BY_PROVIDER  # noqa: E402
from src.validators.content_checker import (  # noqa: E402
    _count_cite_sources,
    _find_exercises,
)


def test_exercicio_com_titulo_proprio_e_passos_numerados_e_reconhecido() -> None:
    texto = (
        "# Aula 1.4: Etiquetas\n\n## Por que organizar muda o resultado\n\nprosa\n\n"
        "## Crie três etiquetas para agrupar os contatos da semana\n\n"
        "Separe dez minutos com o celular na mão.\n\n"
        "1. Abra o WhatsApp Business e toque em Etiquetas.\n"
        "2. Crie a segunda etiqueta para quem agendou.\n"
        "3. Abra as conversas dos últimos sete dias.\n"
    )
    assert _find_exercises(texto)


def test_resultado_esperado_em_prosa_conta() -> None:
    texto = "## Faça agora\n\nSiga os passos.\n\nO resultado esperado é que você tenha um script novo."
    assert len(_find_exercises(texto)) >= 1


def test_lista_de_dois_itens_sem_rotulo_nao_e_exercicio() -> None:
    texto = "## Como fica\n\n1. primeiro\n2. segundo\n\nprosa"
    assert _find_exercises(texto) == []


def test_fontes_do_rodape_da_trilha_contam_como_cite_sources() -> None:
    trilha = (
        "# Trilha 1: X\n\n## Glossário\n\n**termo**: glosa\n\n## Fontes\n\n"
        "Harvard Business Review, The Short Life of Online Sales Leads, março de 2011.\n"
        "Octadesk, CX Trends, maio de 2025.\n"
        "Booksy, relatório interno, 2024.\n"
        "Linha sem ano não conta.\n"
    )
    assert _count_cite_sources(trilha) == 3


def test_teto_de_saida_por_provedor_vem_do_yaml() -> None:
    assert MAX_TOKENS_BY_PROVIDER["anthropic"] >= 32000
    assert MAX_TOKENS_BY_PROVIDER["google"] >= 32000
