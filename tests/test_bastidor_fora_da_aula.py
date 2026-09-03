"""03/09/2026: a aula não fala de si; lei entra como fato; o relatório nunca vaza."""

from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.orchestrator import separar_relatorio_de_revisao  # noqa: E402
from src.validators.content_checker import (  # noqa: E402
    _COMENTARIO_SOLTO_RE,
    _RELATORIO_VAZADO_RE,
    _ROTULO_PESQUISA_RE,
    _check_bastidor,
    _check_muleta_legal,
)


def test_aula_que_fala_de_si_e_bastidor() -> None:
    t = "Esta aula foi escrita em linguagem simples e os dados foram verificados com a equipe."
    assert _check_bastidor(t)


def test_metodo_da_estimativa_e_bastidor() -> None:
    t = "Segundo nossa metodologia, a estimativa calculada é de três em cada dez clientes."
    assert _check_bastidor(t)


def test_mencao_entre_aspas_nao_e_bastidor() -> None:
    t = 'Tire da sua página frases como "dados verificados": o cliente quer o número.'
    assert _check_bastidor(t) == []


def test_autoapresentacao_e_aviso_nao_bastidor() -> None:
    from src.validators.content_checker import _check_autoapresentacao
    t = "Esta aula explica como montar a tabela de preços do salão em uma tarde."
    assert _check_autoapresentacao(t)
    assert _check_bastidor(t) == []


def test_fato_com_passo_passa() -> None:
    t = "Três em cada dez clientes voltam em 60 dias. Abra a agenda e marque quem sumiu."
    assert _check_bastidor(t) == []


def test_rotulo_da_pesquisa_vazado() -> None:
    assert _ROTULO_PESQUISA_RE.search("O mercado cresceu 12% em 2025 [Alta].")
    assert not _ROTULO_PESQUISA_RE.search("O mercado cresceu 12% em 2025.")


def test_comentario_solto_e_marcador_de_modulo() -> None:
    assert _COMENTARIO_SOLTO_RE.search("texto <!-- revisor: cortei o parágrafo --> texto")
    assert not _COMENTARIO_SOLTO_RE.search("<!-- Módulo 1: Fundamentos -->\n# Aula 1.1: X")


def test_relatorio_vazado_em_tres_idiomas() -> None:
    for marca in ("REVISÃO CONCLUÍDA", "REVIEW COMPLETE", "REVISIÓN CONCLUIDA"):
        assert _RELATORIO_VAZADO_RE.search(f"fim da aula\n---\n{marca}\nPalavras: 900")


def test_separar_relatorio_aceita_marcador_em_ingles_e_espanhol() -> None:
    for marca in ("REVISÃO CONCLUÍDA", "REVIEW COMPLETE", "REVISIÓN CONCLUIDA"):
        saida = f"# Aula 1.1: X\n\nprosa\n\n---\n{marca}\nAprovado: sim\n---"
        texto, relatorio = separar_relatorio_de_revisao(saida)
        assert texto == "# Aula 1.1: X\n\nprosa"
        assert marca in relatorio


def test_muleta_legal_avisa_e_lei_com_numero_passa() -> None:
    assert _check_muleta_legal("Guarde os dados de acordo com a LGPD e consulte um advogado.")
    assert _check_muleta_legal("A Lei 8.078, artigo 49, dá sete dias para desistir.") == []
