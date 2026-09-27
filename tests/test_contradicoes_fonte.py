"""27/09/2026: contradições com a fonte de estilo corrigidas no curso-factory."""

from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.validators import lexicos_loader  # noqa: E402
from src.validators.content_checker import check_content  # noqa: E402

PROMPTS = PROJECT_ROOT / "src" / "templates" / "prompts"


def _aula_longa(com_tabela: bool) -> str:
    frase = "A dona do salão confere a agenda da semana antes de abrir as portas de manhã."
    paragrafo = " ".join([frase] * 5)
    corpo = "\n\n".join([paragrafo] * 14)
    tabela = "\n\n| Critério | Papel | Celular |\n|---|---|---|\n| Lembrete | não | sim |\n"
    return (
        "# Aula 1.1: Confirmar a agenda\n\nConfirme a agenda sem perder horário.\n\n"
        f"{paragrafo}\n\n## Por que confirmar\n\n{corpo}{tabela if com_tabela else ''}\n\n"
        f"## Como fica no salão\n\n{paragrafo}\n"
    )


def _aviso_sem_visual(texto: str) -> list:
    return [e for e in check_content(texto, "aula") if "nenhum apoio visual" in e.mensagem]


def test_c12_aula_longa_sem_apoio_recebe_aviso_do_limiar_da_fonte() -> None:
    avisos = _aviso_sem_visual(_aula_longa(com_tabela=False))
    assert avisos and avisos[0].tipo == "warning"
    limiar = lexicos_loader.carregar_lexicos()["limiares"]["semVisualAcimaDePalavras"]
    assert str(limiar) in avisos[0].mensagem
    assert _aviso_sem_visual(_aula_longa(com_tabela=True)) == []


def test_c12_sem_o_limiar_no_espelho_nada_muda(tmp_path, monkeypatch) -> None:
    import json

    dados = json.loads(lexicos_loader.LEXICOS_PATH.read_text(encoding="utf-8"))
    dados["limiares"].pop("semVisualAcimaDePalavras")
    espelho = tmp_path / "lexicos.json"
    espelho.write_text(json.dumps(dados, ensure_ascii=False), encoding="utf-8")
    monkeypatch.setattr(lexicos_loader, "LEXICOS_PATH", espelho)
    lexicos_loader.carregar_lexicos.cache_clear()
    try:
        assert _aviso_sem_visual(_aula_longa(com_tabela=False)) == []
    finally:
        lexicos_loader.carregar_lexicos.cache_clear()


def test_c2_molde_da_aula_tem_tres_h2_em_todos_os_idiomas() -> None:
    marcas = {"pt-br": "o normal são três", "en": "three is the norm", "es": "lo normal son tres"}
    for idioma, marca in marcas.items():
        for nome in ("draft.md", "review.md"):
            assert marca in (PROMPTS / idioma / nome).read_text(encoding="utf-8"), (idioma, nome)
    assert marcas["pt-br"] in (PROMPTS / "draft.md").read_text(encoding="utf-8")


def test_c1_fallback_inline_nao_pede_cena_nem_registro_hbr() -> None:
    from src.agents.reviewer import Reviewer
    from src.agents.writer import Writer

    for template in (Writer.TEMPLATE, Reviewer.TEMPLATE):
        assert "situação concreta" not in template
        assert "Harvard" not in template and "padrão HSM" not in template.lower()


def test_c8_credencial_sem_travessao_no_claude_md() -> None:
    texto = (PROJECT_ROOT / "CLAUDE.md").read_text(encoding="utf-8")
    assert "Alexandre Caramaschi — CEO" not in texto


def test_capsula_mensagem_e_codigo_usam_a_mesma_faixa() -> None:
    """Item 10 de 27/09/2026: a mensagem dizia 40-60 e o código aceitava 18 a 75."""
    from src.clients.context import Geo2026Config
    from src.validators.content_checker import CAPSULA_PALAVRAS

    cfg = Geo2026Config(princeton_playbook_enabled=True, require_answer_capsule=True)
    erros = check_content("## Título\n\n- item solto\n", "x", geo_config=cfg, unidade="modulo")
    msg = next(e.mensagem for e in erros if "capsule" in e.mensagem.lower())
    assert f"{CAPSULA_PALAVRAS[0]} a {CAPSULA_PALAVRAS[1]} palavras" in msg
