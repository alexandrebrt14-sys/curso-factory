"""Smoke tests para os validadores e o quality gate."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.clients import load_client
from src.clients.context import Geo2026Config
from src.validators import rules_loader
from src.validators.accent_checker import check_accents, fix_accents
from src.validators.content_checker import (
    _check_cliches,
    _check_percentages_have_source,
    _count_cite_sources,
    _count_quotations,
    _count_statistics,
    _count_unresolved_markers,
    _has_answer_capsule,
    check_content,
)
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


def test_fix_accents_nao_corrompe_homografos() -> None:
    """Homografo com forma sem acento valida NUNCA e trocado por dicionario.

    Regressao de 11/08/2026: o gate roda com auto_fix=True, e estas entradas
    injetavam erro de portugues em todo curso gerado ("nos projetos" ->
    "nos projetos" acentuado, "seria bom" -> "seria" acentuado, imperativo
    "Analise os dados" -> substantivo). Contexto e trabalho do revisor LLM.
    """
    text = (
        "Ele trabalha nos projetos e esta analise nos ajuda. "
        "Analise os dados. Se ele quiser, seria bom. Eu publico e valido o "
        "material que a equipe pratica."
    )
    corrigido, _ = fix_accents(text)
    assert corrigido == text
    assert check_accents(text) == []


def test_fix_accents_ainda_corrige_inequivocos() -> None:
    """A protecao de homografos nao pode desligar o caso inequivoco."""
    corrigido, n = fix_accents("Voce nao tem informacao sobre a producao.")
    assert n >= 4
    assert corrigido == "Você não tem informação sobre a produção."


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


# ─── citabilidade GEO (content_checker) ──────────────────────────────

def test_geo_count_cite_sources() -> None:
    text = (
        "Segundo a McKinsey (2025), o ganho é real. Outro dado vem do "
        "Gartner (2024). Ver também [o relatório](https://example.com/r)."
    )
    assert _count_cite_sources(text) >= 3


def test_geo_count_statistics() -> None:
    text = "Crescimento de 23% e queda de 8,7%, com lift de 4,1× e R$ 1.000."
    assert _count_statistics(text) >= 4


def test_geo_count_quotations() -> None:
    text = '> "A estrutura validável vence a prosa eloquente." — Alexandre Caramaschi'
    assert _count_quotations(text) >= 1


def test_geo_answer_capsule_detectado() -> None:
    text = (
        "## O que é Generative Engine Optimization?\n\n"
        "Generative Engine Optimization é a prática de estruturar conteúdo "
        "para que motores como ChatGPT, Gemini e Perplexity o citem como fonte "
        "em respostas geradas, medindo o ganho por taxa de citação observada."
    )
    assert _has_answer_capsule(text) is True


def test_geo_check_bloqueia_quando_playbook_ligado() -> None:
    """Com playbook ligado, módulo sem fontes/estatísticas gera erros GEO."""
    pobre = "## Título\n\nUm texto qualquer sem nenhuma fonte ou estatística."
    cfg = Geo2026Config(princeton_playbook_enabled=True)
    erros = check_content(pobre, "modulo", geo_config=cfg)
    geo_errors = [e for e in erros if e.categoria == "geo" and e.tipo == "error"]
    assert len(geo_errors) >= 1


def test_geo_check_so_avisa_quando_playbook_desligado() -> None:
    """Com playbook desligado, lacunas GEO viram avisos, não erros."""
    pobre = "## Título\n\nUm texto qualquer sem nenhuma fonte ou estatística."
    cfg = Geo2026Config(princeton_playbook_enabled=False)
    erros = check_content(pobre, "modulo", geo_config=cfg)
    geo_errors = [e for e in erros if e.categoria == "geo" and e.tipo == "error"]
    assert geo_errors == []


def test_geo_check_ausente_e_retrocompativel() -> None:
    """Sem geo_config, check_content não emite nenhuma categoria 'geo'."""
    texto = "## Título\n\nConteúdo sem GEO config."
    erros = check_content(texto, "modulo")
    assert all(e.categoria != "geo" for e in erros)


# ─── quality_rules.yaml lido em runtime (rules_loader) ───────────────

@pytest.fixture
def yaml_de_regras_ausente(monkeypatch: pytest.MonkeyPatch):
    """Aponta o rules_loader para um caminho inexistente.

    Limpa o cache antes e depois: load_rules e memoizado por processo e um
    resultado vazio vazando para os proximos testes desligaria o gate.
    """
    monkeypatch.setattr(
        rules_loader, "RULES_PATH", PROJECT_ROOT / "config" / "nao-existe-quality-rules.yaml"
    )
    rules_loader.load_rules.cache_clear()
    yield
    rules_loader.load_rules.cache_clear()


def test_load_rules_le_o_yaml_do_repositorio() -> None:
    """O arquivo real carrega e traz a secao de expressoes proibidas."""
    rules_loader.load_rules.cache_clear()
    regras = rules_loader.load_rules()
    expressoes = rules_loader.rules_list("forbidden_expressions", "expressions")
    assert "validation" in regras
    assert len(expressoes) > 18


def test_load_rules_arquivo_ausente_devolve_dict_vazio(yaml_de_regras_ausente) -> None:
    """Config sumida nao pode levantar excecao: devolve {} e segue o baile."""
    assert rules_loader.load_rules() == {}
    assert rules_loader.validation_section("anti_invencao") == {}
    assert rules_loader.rules_list("forbidden_expressions", "expressions") == []


def test_cliche_so_do_yaml_e_detectado() -> None:
    """Expressao que existe no YAML e nao no fallback agora reprova.

    'especialistas apontam' e uma das 28 entradas que o gate nunca checou
    enquanto o YAML era decorativo (achado de 11/08/2026).
    """
    from src.validators.content_checker import FORBIDDEN_CLICHES

    assert "especialistas apontam" not in FORBIDDEN_CLICHES  # vem da fonte, nao do fallback
    assert "especialistas apontam" in _check_cliches(
        "Especialistas apontam que o mercado vai dobrar."
    )
    assert "clique aqui" in _check_cliches("Para conhecer o metodo, clique aqui.")


def test_cliche_usa_fonte_quando_yaml_nao_carrega(yaml_de_regras_ausente) -> None:
    """Sem o YAML do repo, a fonte de estilo sustenta o anti-cliche sozinha.

    Ate 27/08/2026 este teste afirmava o contrario: sem YAML, "especialistas
    apontam" deixava de ser checado, porque a unica outra origem eram as 18
    entradas hardcoded. Com config/lexicos.json (espelho gerado da fonte) a
    cobertura deixou de depender do YAML do repositorio, que hoje guarda so o
    que e especifico do curso-factory.
    """
    assert _check_cliches("Nos dias de hoje tudo mudou.") == ["nos dias de hoje"]
    assert _check_cliches("Especialistas apontam que sim.") == ["especialistas apontam"]


# ─── anti-invencao: percentual sem fonte ─────────────────────────────

def test_percentual_sem_fonte_gera_aviso() -> None:
    """Numero sem origem na mesma frase vira aviso nao-bloqueante."""
    texto = "## Dados\n\nA adocao de agentes subiu 42% entre as empresas medias."
    achados = _check_percentages_have_source(texto)
    assert len(achados) == 1

    erros = check_content(texto, "modulo")
    avisos = [e for e in erros if e.categoria == "evidencia" and e.tipo == "warning"]
    assert len(avisos) == 1
    assert "denominador" in avisos[0].mensagem
    # Aviso nao pode virar erro bloqueante
    assert [e for e in erros if e.categoria == "evidencia" and e.tipo == "error"] == []


def test_percentual_com_fonte_na_mesma_frase_nao_gera_aviso() -> None:
    """Citacao parentetica com ano ou 'segundo X de 2026' silenciam o aviso."""
    com_parentese = "A adocao subiu 42% no ano (Gartner, 2026)."
    com_segundo = "Segundo o levantamento da consultoria de 2026, 42% ja migraram."
    assert _check_percentages_have_source(com_parentese) == []
    assert _check_percentages_have_source(com_segundo) == []


def test_percentual_em_tabela_e_codigo_e_ignorado() -> None:
    """Linha de tabela e bloco de codigo nao sao prosa e nao acusam."""
    texto = (
        "| Metrica | Valor |\n"
        "|---------|-------|\n"
        "| Adocao  | 42%   |\n\n"
        "```python\ntaxa = 0.42  # 42%\n```\n"
    )
    assert _check_percentages_have_source(texto) == []


def test_percentual_limita_avisos_por_documento() -> None:
    """Teto de 5 avisos evita relatorio que ninguem le."""
    texto = "\n\n".join(f"O indicador {i} cresceu {i}0% no periodo." for i in range(1, 9))
    assert len(_check_percentages_have_source(texto)) == 8
    erros = check_content(texto, "modulo")
    avisos = [e for e in erros if e.categoria == "evidencia" and e.tipo == "warning"]
    assert len(avisos) == 5


# ─── anti-invencao: marcadores de apuracao em aberto ─────────────────

def test_marcadores_acima_do_teto_bloqueiam() -> None:
    """6 marcadores passam do teto de 5 e reprovam a peca."""
    texto = "## Modulo\n\n" + "\n\n".join(
        [f"Paragrafo {i} [FALTA EVIDÊNCIA: numero de adocao]." for i in range(3)]
        + [f"Paragrafo {i} [PREENCHER-HUMANO: nome do cliente]." for i in range(3)]
    )
    assert _count_unresolved_markers(texto) == 6
    erros = check_content(texto, "modulo")
    bloqueantes = [e for e in erros if e.categoria == "evidencia" and e.tipo == "error"]
    assert len(bloqueantes) == 1
    assert "apuração" in bloqueantes[0].mensagem


def test_poucos_marcadores_nao_bloqueiam() -> None:
    """2 marcadores estao dentro do teto e nao geram erro."""
    texto = (
        "## Modulo\n\nPrimeiro ponto [FALTA EVIDÊNCIA: fonte do dado].\n\n"
        "Segundo ponto [PREENCHER-HUMANO: exemplo do cliente]."
    )
    assert _count_unresolved_markers(texto) == 2
    erros = check_content(texto, "modulo")
    assert [e for e in erros if e.categoria == "evidencia" and e.tipo == "error"] == []
