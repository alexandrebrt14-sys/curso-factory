"""Técnicas de GEO e SEO do segundo semestre de 2026 nos algoritmos (07/10/2026).

Cada teste prende uma regra que mudou, com a fonte no docstring:

- a camada `erros_de_geo` não promete mais lift de citação, e estatísticas e
  falas viram aviso (arXiv 2609.07559, 07/09/2026);
- o `TsxGenerator.write` grava a checklist de revisão humana dos metadados
  gerados (Google Search Central, 01/10/2026) com a cadência de revisão
  (Profound, 30/09/2026);
- o JSON-LD não sai com `FAQPage` vazio nem com instrutor sem nome (alerta do
  Google contra autoria enganosa, 06/10/2026);
- os prompts cobram variantes da pergunta, seção que se sustenta sozinha e
  autoria real.
"""

from __future__ import annotations

import sys
from datetime import date
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.clients.context import Geo2026Config  # noqa: E402
from src.generators import TsxGenerator  # noqa: E402
from src.generators.revisao_humana import (  # noqa: E402
    REVISAO_ARQUIVO,
    cadencia_revisao_dias,
    checklist_revisao_humana,
    pendencias_de_autoria,
)
from src.models import CourseDefinition  # noqa: E402
from src.validators.content_checker import GEO_RESSALVA_CITACAO, erros_de_geo  # noqa: E402

PROMPTS = PROJECT_ROOT / "src" / "templates" / "prompts" / "pt-br"
POBRE = "## Título\n\n- item solto sem fonte nem número\n"

FIGURA = {
    "type": "figure",
    "value": '<svg viewBox="0 0 10 10"><title>Funil</title></svg>',
    "label": "Funil de atendimento do WhatsApp em três etapas",
}


def _curso(**extra) -> CourseDefinition:
    base = dict(
        slug="teste-geo-seo",
        titulo="Curso de teste de GEO e SEO",
        titulo_seo="Curso de teste de GEO e SEO | Exemplo",
        descricao="Descrição do curso de teste com mais de vinte caracteres para a página.",
        descricao_curta="Subtítulo do curso em uma frase.",
        keywords_seo=["geo", "seo"],
        steps=[
            {
                "id": "modulo-um",
                "title": "Módulo um",
                "duration": "10 min",
                "description": "Subtítulo do módulo em uma frase.",
                "content": [
                    {"type": "text", "value": "Texto do módulo com uma frase direta."},
                    FIGURA,
                ],
            }
        ],
        faq=[{"pergunta": "Quanto custa começar?", "resposta": "Nada além do tempo da equipe."}],
        autor_nome="Maria Silva",
        autor_credencial="Consultora",
        dominio="https://exemplo.com.br",
        company_name="Exemplo",
        company_description="Empresa de exemplo.",
    )
    base.update(extra)
    return CourseDefinition(**base)


# ─── Camada GEO: verificabilidade, sem promessa de citação ────────────


def test_mensagens_geo_nao_prometem_lift_de_citacao() -> None:
    cfg = Geo2026Config(princeton_playbook_enabled=True, min_quotations=1)
    erros = erros_de_geo(POBRE, cfg, "curso")
    assert len(erros) == 4
    for e in erros:
        assert "lift" not in e.mensagem.lower()
        for numero in ("+40%", "+32,8%", "+42,6%", "1,9×", "+115%"):
            assert numero not in e.mensagem


def test_estatisticas_e_falas_sao_sempre_aviso() -> None:
    cfg = Geo2026Config(princeton_playbook_enabled=True, min_quotations=1)
    erros = erros_de_geo(POBRE, cfg, "curso")
    por_tema = {e.mensagem.split(":", 1)[0]: e for e in erros}
    assert por_tema["Dados quantitativos"].tipo == "warning"
    assert por_tema["Citações diretas"].tipo == "warning"
    assert GEO_RESSALVA_CITACAO in por_tema["Dados quantitativos"].mensagem


def test_fontes_e_capsula_seguem_o_playbook() -> None:
    ligado = erros_de_geo(POBRE, Geo2026Config(princeton_playbook_enabled=True), "curso")
    desligado = erros_de_geo(POBRE, Geo2026Config(princeton_playbook_enabled=False), "curso")
    bloqueia = {e.mensagem.split(":", 1)[0] for e in ligado if e.tipo == "error"}
    assert bloqueia == {"Fontes atribuídas", "Cápsula de resposta ausente"}
    assert all(e.tipo == "warning" for e in desligado)


def test_capsula_explica_o_recorte_do_motor() -> None:
    erros = erros_de_geo(POBRE, Geo2026Config(princeton_playbook_enabled=True), "curso")
    msg = next(e.mensagem for e in erros if e.mensagem.startswith("Cápsula"))
    assert "se sustentar sozinha" in msg


# ─── Revisão humana dos metadados e cadência ──────────────────────────


def test_cadencia_vem_do_yaml() -> None:
    assert cadencia_revisao_dias() == 14


def test_checklist_transcreve_cada_metadado_gerado() -> None:
    curso = _curso()
    md = checklist_revisao_humana(curso, hoje=date(2026, 10, 7))
    assert curso.titulo_seo in md
    assert curso.descricao in md
    assert "geo, seo" in md
    assert "Quanto custa começar?" in md
    assert FIGURA["label"] in md
    assert "Maria Silva (Consultora)" in md
    assert "21/10/2026" in md  # 07/10 + 14 dias
    assert "01/10/2026" in md


def test_autor_vazio_vira_pendencia() -> None:
    curso = _curso(autor_nome="", autor_credencial="")
    pendencias = pendencias_de_autoria(curso)
    assert len(pendencias) == 1 and pendencias[0].startswith("Autor vazio")
    assert "PENDENTE: Autor vazio" in checklist_revisao_humana(curso)
    assert pendencias_de_autoria(_curso()) == []


def test_write_grava_checklist_ao_lado_do_page(tmp_path, monkeypatch) -> None:
    monkeypatch.setattr("src.generators.tsx_generator._peso_visual_obrigatorio", lambda: False)
    gen = TsxGenerator()
    page_path, _layout = gen.write(_curso(), tmp_path)
    checklist = page_path.parent / REVISAO_ARQUIVO
    assert checklist.exists()
    assert gen.ultimo_checklist_revisao == checklist
    assert "Revisão humana antes de publicar" in checklist.read_text(encoding="utf-8")


# ─── JSON-LD: só o que existe de verdade ──────────────────────────────


def test_jsonld_sem_faq_nao_emite_faqpage() -> None:
    gen = TsxGenerator()
    com = gen.render_page(_curso(), cobrar_peso_visual=False)
    sem = gen.render_page(_curso(faq=[]), cobrar_peso_visual=False)
    assert '"@type": "FAQPage"' in com
    assert '"@type": "FAQPage"' not in sem


def test_jsonld_sem_autor_nao_emite_instrutor() -> None:
    gen = TsxGenerator()
    com = gen.render_page(_curso(), cobrar_peso_visual=False)
    sem = gen.render_page(_curso(autor_nome="", autor_credencial=""), cobrar_peso_visual=False)
    assert "instructor:" in com
    assert "instructor:" not in sem


# ─── Prompts ──────────────────────────────────────────────────────────


def _prompt(nome: str) -> str:
    return (PROMPTS / nome).read_text(encoding="utf-8")


def test_redacao_e_revisao_cobram_recorte_variantes_e_autoria() -> None:
    for nome in ("draft.md", "review.md"):
        texto = _prompt(nome)
        assert "se sustenta sozinha" in texto
        assert "formas diferentes com que o aluno faria a mesma pergunta" in texto
        assert "Autoria enganosa" in texto
        assert "arXiv 2609.07559" in texto


def test_pesquisa_registra_limites_de_geo_com_data() -> None:
    texto = _prompt("research.md")
    for marca in (
        "variantes da pergunta",
        "arXiv 2609.23162",
        "arXiv 2609.07559",
        "arXiv 2609.22655",
        "arXiv 2609.24407",
    ):
        assert marca in texto


def test_faq_da_trilha_cobre_variantes_sem_prometer_citacao() -> None:
    texto = _prompt("trail.md")
    assert "formas diferentes da mesma dúvida" in texto
    assert "nenhum estudo mostrou que ele aumente a citação" in texto


def test_tag_citation_ready_sem_contagem_de_estatistica() -> None:
    texto = _prompt("classify.md")
    assert "Statistics ≥5" not in texto
    assert "não prevê citação" in texto


# ─── Regra 46 da fonte 1.10.0: promessa de citação ────────────────────


def test_promessa_de_citacao_vira_aviso() -> None:
    from src.validators.content_checker import erros_de_promessa_de_citacao

    achados = erros_de_promessa_de_citacao("Este método garante citação no ChatGPT.", "x")
    assert achados and all(e.tipo == "warning" for e in achados)
    assert achados[0].categoria == "promessa-de-citacao"


def test_promessa_negada_ou_entre_aspas_nao_conta() -> None:
    from src.validators.content_checker import promessas_de_citacao

    assert promessas_de_citacao("Nenhuma agência garante citação no ChatGPT.") == []
    assert promessas_de_citacao('Fuja de quem vende "citação garantida" no Google.') == []


def test_alavanca_dada_como_causa_vira_aviso() -> None:
    from src.validators.content_checker import promessas_de_citacao

    assert promessas_de_citacao("Estatísticas aumentam a chance de citação da página.")
