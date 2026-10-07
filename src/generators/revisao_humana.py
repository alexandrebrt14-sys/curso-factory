"""Checklist de revisão humana dos metadados que a fábrica gera (07/10/2026).

Por que existe. Em 01/10/2026 o Google revisou a orientação sobre conteúdo
feito com IA generativa e passou a chamar de crítica a verificação manual antes
de publicar, alcançando título, meta description, dados estruturados e texto
alternativo de imagem (developers.google.com/search/docs/fundamentals/
using-gen-ai-content). Em 06/10/2026 alertou contra informação de autoria
enganosa. A fábrica gera exatamente esses campos: `titulo_seo`, `descricao`,
`keywords_seo`, o JSON-LD `Course` e `FAQPage` do `page.tsx` e a legenda que vira
`alt` de cada figura. Até esta data eles saíam sem nenhum registro de revisão.

O que faz. `checklist_revisao_humana` devolve um Markdown com cada campo gerado,
transcrito, para a pessoa responsável conferir antes do PR na landing, e com a
data da próxima revisão do curso publicado. `TsxGenerator.write` grava esse
arquivo ao lado do `page.tsx`. Nada aqui reprova a geração: o arquivo é
pendência de publicação, e quem publica sem marcar os itens assume o risco
documentado pela orientação do Google.

Cadência. Profound (30/09/2026): a citação mediana em IA perde metade da
participação de pico em 11 dias. O número de dias vem de
`config/quality_rules.yaml > validation.revisao_publicacao.cadencia_revisao_dias`.
"""

from __future__ import annotations

from datetime import date, timedelta

from src.models import CourseDefinition, SectionType
from src.validators.rules_loader import validation_section

#: Nome do arquivo gravado ao lado do page.tsx.
REVISAO_ARQUIVO = "REVISAO_HUMANA.md"

#: Igual ao valor de `quality_rules.yaml` em 07/10/2026; só entra se a chave
#: sumir. Origem: Profound, 30/09/2026 (meia-vida de 11 dias; 78% das páginas
#: caem à metade em duas semanas).
_CADENCIA_FALLBACK_DIAS = 14


def cadencia_revisao_dias() -> int:
    """Dias entre revisões do curso publicado, lidos do YAML."""
    valor = validation_section("revisao_publicacao").get("cadencia_revisao_dias")
    try:
        dias = int(valor)
    except (TypeError, ValueError):
        return _CADENCIA_FALLBACK_DIAS
    return dias if dias > 0 else _CADENCIA_FALLBACK_DIAS


def pendencias_de_autoria(course: CourseDefinition) -> list[str]:
    """Lacunas de autoria que impedem publicar sem decisão humana.

    Autor vazio faria o JSON-LD sair com instrutor sem nome, e preencher no
    improviso é o que o Google chamou de autoria enganosa em 06/10/2026.
    """
    pendencias: list[str] = []
    if not course.autor_nome.strip():
        pendencias.append(
            "Autor vazio: informe a pessoa real que escreveu ou revisou o curso. "
            "Sem ela, o page.tsx sai sem instrutor no JSON-LD; nunca preencha com "
            "nome genérico ou persona."
        )
    if course.autor_nome.strip() and not course.autor_credencial.strip():
        pendencias.append(
            f"Credencial vazia para {course.autor_nome}: use a credencial canônica do "
            "client.yaml ou deixe sem cargo; não invente título."
        )
    return pendencias


def _figuras(course: CourseDefinition) -> list[tuple[str, str]]:
    itens: list[tuple[str, str]] = []
    for step in course.steps:
        for section in step.content:
            if section.type is SectionType.FIGURE:
                itens.append((step.title, (section.label or "").strip()))
    return itens


def checklist_revisao_humana(course: CourseDefinition, hoje: date | None = None) -> str:
    """Markdown com cada metadado gerado, para conferência humana antes de publicar."""
    hoje = hoje or date.today()
    dias = cadencia_revisao_dias()
    proxima = hoje + timedelta(days=dias)

    linhas: list[str] = [
        f"# Revisão humana antes de publicar: {course.titulo}",
        "",
        "Cada campo abaixo foi gerado pela fábrica e vai para o código da página. "
        "Desde 01/10/2026 a orientação do Google sobre conteúdo feito com IA pede "
        "verificação humana também de título, meta description, dados estruturados "
        "e texto alternativo. Marque o item só depois de conferir o texto contra as "
        "aulas publicadas.",
        "",
        "## Título e descrição",
        "",
        f"- [ ] Título da aba (`titulo_seo`): {course.titulo_seo or course.titulo}",
        f"- [ ] Meta description (`descricao`, {len(course.descricao.strip())} caracteres): "
        f"{course.descricao.strip()}",
    ]
    if course.descricao_curta.strip():
        linhas.append(
            f"- [ ] Subtítulo do topo (`descricao_curta`): {course.descricao_curta.strip()}"
        )
    if course.keywords_seo:
        linhas.append(f"- [ ] Palavras-chave (`keywords_seo`): {', '.join(course.keywords_seo)}")

    linhas += [
        "",
        "## Dados estruturados (JSON-LD)",
        "",
        "Os dados estruturados descrevem o que está visível na página e servem à busca "
        "clássica. Nenhum estudo mostrou que eles aumentem a citação em IA; campo que "
        "promete o que a página não mostra sai.",
        "",
        "- [ ] `Course.name` e `Course.description` iguais ao título e à descrição acima",
    ]
    if course.autor_nome.strip():
        cred = f" ({course.autor_credencial.strip()})" if course.autor_credencial.strip() else ""
        linhas.append(
            f"- [ ] `Course.instructor`: {course.autor_nome.strip()}{cred} escreveu ou revisou "
            "este curso de fato"
        )
    if course.faq:
        linhas.append(
            f"- [ ] `FAQPage` com {len(course.faq)} pergunta(s), cada resposta visível na página:"
        )
        for item in course.faq:
            linhas.append(f"  - {item.pergunta.strip()}")
    else:
        linhas.append("- [ ] Sem perguntas frequentes: o page.tsx não emite `FAQPage`")

    figuras = _figuras(course)
    linhas += ["", "## Texto alternativo das figuras", ""]
    if figuras:
        for titulo_aula, legenda in figuras:
            linhas.append(f"- [ ] {titulo_aula}: {legenda or '(legenda vazia)'}")
    else:
        linhas.append("- Nenhuma figura neste curso.")

    pendencias = pendencias_de_autoria(course)
    linhas += ["", "## Autoria", ""]
    if pendencias:
        linhas += [f"- [ ] PENDENTE: {p}" for p in pendencias]
    else:
        linhas.append(
            "- [ ] Nenhuma byline, selo de revisão por especialista ou fala atribuída a "
            "pessoa que não participou de fato (alerta do Google de 06/10/2026)"
        )

    linhas += [
        "",
        "## Depois de publicar",
        "",
        f"- [ ] Próxima revisão até {proxima.strftime('%d/%m/%Y')} (cadência de {dias} dias). "
        "A citação mediana em IA perde metade do peso em 11 dias (Profound, 30/09/2026); "
        "revise fatos, datas e fontes, e só mude a data com mudança editorial real.",
        "- [ ] Meça presença em resposta de IA em várias rodadas e por motor, em português "
        "no Google Brasil: 67% das URLs citadas trocaram no mesmo motor de um dia para o "
        "outro (arXiv 2609.22655, 19/09/2026). Impressão em IA não vira visita "
        "automaticamente no cálculo (arXiv 2608.18352, 18/08/2026).",
        "",
    ]
    return "\n".join(linhas)
