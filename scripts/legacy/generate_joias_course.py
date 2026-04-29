"""Script para gerar o curso SEO/GEO Revendedoras de Joias.

Le os modulos expandidos, monta CourseDefinition e gera TSX.
"""
import sys
import re
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.models import (
    CourseDefinition, StepDefinition, CourseSection, SectionType, FAQItem, NivelCurso
)
from src.generators.tsx_generator import TsxGenerator


def split_modules(filepath: Path) -> dict[int, str]:
    """Split Markdown file into modules by '# Modulo N' headers."""
    text = filepath.read_text(encoding="utf-8")
    modules = {}

    # Split by single # headers: '# Modulo N' or '# Módulo N'
    parts = re.split(r'(?=^# M[oó]dulo \d+)', text, flags=re.MULTILINE)

    for part in parts:
        match = re.match(r'^# M[oó]dulo (\d+)', part)
        if match:
            num = int(match.group(1))
            modules[num] = part

    return modules


def markdown_to_sections(md_text: str, module_num: int) -> list[CourseSection]:
    """Convert expanded Markdown into CourseSection list for TSX."""
    sections: list[CourseSection] = []

    # Split by ## subsection headers
    subsections = re.split(r'(?=^## \d+\.\d+)', md_text, flags=re.MULTILINE)

    for sub in subsections:
        sub = sub.strip()
        if not sub or len(sub) < 50:
            continue

        # Check if this is the exercise section
        if re.match(r'^## \d+\.\d+ Exerc[ií]cios', sub):
            # Add as tip
            sections.append(CourseSection(type=SectionType.TIP, value=sub))
            continue

        # Check if this is a summary
        if re.match(r'^## \d+\.\d+ Resumo', sub):
            sections.append(CourseSection(type=SectionType.TEXT, value=sub))
            continue

        # Split long subsections into paragraphs for better readability
        paragraphs = re.split(r'\n\n+', sub)
        current_block = []

        for para in paragraphs:
            para = para.strip()
            if not para:
                continue

            current_block.append(para)

            # Flush block every ~800 chars to keep sections readable
            block_text = "\n\n".join(current_block)
            if len(block_text) > 800:
                sections.append(CourseSection(type=SectionType.TEXT, value=block_text))
                current_block = []

        # Flush remaining
        if current_block:
            block_text = "\n\n".join(current_block)
            if len(block_text) > 30:
                sections.append(CourseSection(type=SectionType.TEXT, value=block_text))

    # Add warning for key concepts
    if len(sections) > 3:
        # Find a good section to convert to warning (something with "importante", "cuidado", "atenção")
        for i, s in enumerate(sections):
            if any(w in s.value.lower() for w in ["importante", "cuidado", "atenção", "erro", "nunca"]):
                sections[i] = CourseSection(type=SectionType.WARNING, value=s.value)
                break

    # Ensure minimum 3 sections
    while len(sections) < 3:
        sections.append(CourseSection(
            type=SectionType.TEXT,
            value=f"Conteúdo complementar do módulo {module_num}."
        ))

    # Add checkpoint at end
    sections.append(CourseSection(
        type=SectionType.CHECKPOINT,
        value=f"Você concluiu o Módulo {module_num}. Revise os exercícios práticos e aplique os conceitos no seu negócio antes de prosseguir para o próximo módulo."
    ))

    return sections


def build_course() -> CourseDefinition:
    """Build complete CourseDefinition from expanded modules."""

    drafts = Path(__file__).resolve().parent.parent / "output" / "drafts"

    mods_1_4 = split_modules(drafts / "modulos-1-4-expanded.md")
    mods_5_8 = split_modules(drafts / "modulos-5-8-expanded.md")
    all_mods = {**mods_1_4, **mods_5_8}

    print(f"Módulos encontrados: {sorted(all_mods.keys())}")
    for k, v in all_mods.items():
        print(f"  Módulo {k}: {len(v)} chars")

    module_defs = [
        {
            "id": "fundamentos-mercado-psicologia",
            "title": "Fundamentação, Inteligência de Mercado e Psicologia do Consumidor Joalheiro",
            "duration": "60 min",
            "icon_key": "trendingUp",
            "description": "Motivadores emocionais, tendências 2025-2026, economia da revenda e vocabulário semântico do setor joalheiro.",
        },
        {
            "id": "seo-classico-ecommerce",
            "title": "A Fundação Inabalável do SEO Clássico em E-commerce de Acessórios",
            "duration": "60 min",
            "icon_key": "search",
            "description": "Auditoria técnica on-page, pesquisa de palavras-chave, otimização de conteúdo e monitoramento com Google Search Console.",
        },
        {
            "id": "geo-aeo-nova-fronteira",
            "title": "A Nova Fronteira — Dominando GEO e AEO",
            "duration": "60 min",
            "icon_key": "megaphone",
            "description": "GEO vs SEO, RAG, conteúdo answer-first, otimização de entidades e linguagem para LLMs.",
        },
        {
            "id": "eeat-confianca",
            "title": "A Engenharia da Confiança — E-E-A-T para Revendedoras Autônomas",
            "duration": "60 min",
            "icon_key": "handshake",
            "description": "Experiência, Especialização, Autoridade e Confiabilidade aplicados ao comércio de joias.",
        },
        {
            "id": "busca-visual-google-lens",
            "title": "Otimização de Busca Visual, Multimodalidade e Google Lens",
            "duration": "60 min",
            "icon_key": "barChart",
            "description": "SEO visual, alt text semântico, Product Schema, Google Merchant Center e direção de arte.",
        },
        {
            "id": "seo-local-goiania",
            "title": "Hegemonia Geográfica e SEO Local (Estudo de Caso: Goiânia)",
            "duration": "60 min",
            "icon_key": "briefcase",
            "description": "Google Business Profile, consistência NAP, link building local e captação de reviews.",
        },
        {
            "id": "social-commerce-whatsapp",
            "title": "Social Commerce, Catálogos e o Ecossistema do WhatsApp Business",
            "duration": "60 min",
            "icon_key": "shoppingCart",
            "description": "SEO no catálogo WhatsApp, scripts de conversão, Status estratégico e integração com Instagram.",
        },
        {
            "id": "stack-ia-kpis",
            "title": "Stack Tecnológico, Automação com IA e KPIs da Era Generativa",
            "duration": "60 min",
            "icon_key": "database",
            "description": "IA como assistente, ferramentas SEO/GEO, novos KPIs generativos e plano de execução contínua.",
        },
    ]

    steps = []
    for i, mdef in enumerate(module_defs, 1):
        md_content = all_mods.get(i, "")
        if not md_content:
            print(f"  AVISO: Módulo {i} não encontrado nos arquivos expandidos!")
            md_content = f"Conteúdo do módulo {i} será adicionado em breve."

        content_sections = markdown_to_sections(md_content, i)
        print(f"  Módulo {i}: {len(content_sections)} seções geradas")

        steps.append(StepDefinition(
            id=mdef["id"],
            title=mdef["title"],
            duration=mdef["duration"],
            icon_key=mdef["icon_key"],
            description=mdef["description"],
            content=content_sections,
        ))

    faq = [
        FAQItem(
            pergunta="O que é GEO e por que revendedoras de joias precisam disso?",
            resposta="GEO (Generative Engine Optimization) é a otimização de conteúdo para ser citado em respostas de IAs como ChatGPT, Perplexity e Google AI Overviews. Revendedoras precisam porque o tráfego vindo de IAs converte de 4,4 a 23 vezes mais que o tráfego orgânico tradicional, e ignorar esse canal significa perder vendas de alta intenção."
        ),
        FAQItem(
            pergunta="Preciso de site próprio ou funciona só com WhatsApp e Instagram?",
            resposta="O curso ensina a otimizar ambos os cenários. O WhatsApp Business tem um catálogo indexável que funciona como motor de busca interno. Porém, ter um site próprio (mesmo simples, em Nuvemshop ou Shopify) potencializa drasticamente o SEO clássico, os dados estruturados e a visibilidade em IAs generativas."
        ),
        FAQItem(
            pergunta="Quanto tempo leva para ver resultados com SEO em semijoias?",
            resposta="SEO clássico costuma mostrar resultados mensuráveis entre 3 e 6 meses. GEO pode gerar citações em IAs em semanas se o conteúdo for bem estruturado com FAQs, entidades claras e dados factuais. SEO local (Google Business Profile) pode gerar resultados em poucas semanas com avaliações e consistência NAP."
        ),
        FAQItem(
            pergunta="Como fazer minha marca ser citada pelo ChatGPT e Perplexity?",
            resposta="Você precisa criar conteúdo answer-first: FAQs rigorosas, definições diretas, dados estruturados (Schema.org) e entidades claras. Os LLMs usam RAG para selecionar fontes, priorizando conteúdo factual, sem ambiguidades e com autoridade demonstrada via E-E-A-T."
        ),
        FAQItem(
            pergunta="SEO local funciona para quem vende apenas online, sem loja física?",
            resposta="Sim, parcialmente. Mesmo sem loja física, você pode otimizar para buscas regionais criando conteúdo localizado e participando de diretórios e associações locais. Para quem tem ponto de venda ou atende em uma região específica, o SEO local com Google Business Profile é indispensável."
        ),
        FAQItem(
            pergunta="Qual a diferença entre SEO clássico e GEO na prática?",
            resposta="SEO clássico otimiza para você aparecer nos resultados do Google e receber cliques. GEO otimiza para você ser citado e recomendado dentro das respostas de IAs. O SEO foca em palavras-chave e backlinks; o GEO foca em entidades, dados estruturados e conteúdo modular em formato de pergunta e resposta."
        ),
        FAQItem(
            pergunta="Como otimizar imagens de joias para o Google Lens?",
            resposta="Use formato WebP com compressão abaixo de 100kb, alt text descritivo em linguagem natural (não keyword stuffing), e implemente Product Schema com name, brand, offers e aggregateRating. Fotos com fundo limpo, boa iluminação e detalhes de textura performam melhor em busca visual."
        ),
    ]

    course = CourseDefinition(
        slug="seo-geo-revendedoras-joias",
        titulo="SEO e GEO para Revendedoras de Joias e Semijoias: Autoridade e Vendas na Era da IA",
        titulo_seo="SEO e GEO para Revendedoras de Joias e Semijoias | Curso Completo | Alexandre Caramaschi",
        descricao="Curso completo que une SEO clássico e GEO (Generative Engine Optimization) para revendedoras de joias e semijoias. Da pesquisa de palavras-chave à citação em ChatGPT e Perplexity, passando por E-E-A-T, busca visual, SEO local, WhatsApp Business e métricas da era generativa.",
        descricao_curta="Domine SEO clássico e GEO para capturar tráfego orgânico e generativo no mercado joalheiro brasileiro de USD 15 bilhões.",
        nivel=NivelCurso.INTERMEDIARIO,
        nivel_display="Intermediário",
        tags=["SEO", "GEO", "Joias", "Semijoias", "E-commerce", "WhatsApp Business", "E-E-A-T", "Busca Visual", "SEO Local"],
        keywords_seo=["seo semijoias", "geo joias", "como vender joias online", "otimizacao busca visual joias", "whatsapp business semijoias", "eeat joias", "seo local joalheria", "revendedora semijoias", "curso seo joias"],
        duracao_total_minutos=480,
        duracao_display="~480 min",
        steps=steps,
        prerequisitos_display=["Acesso à internet e computador ou celular", "Conta no WhatsApp Business (gratuita)", "Conhecimento básico de redes sociais"],
        faq=faq,
        hero_gradient_from="#4A1942",
        hero_gradient_to="#D4AF37",
        autor_nome="Alexandre Caramaschi",
        autor_credencial="CEO da Brasil GEO, ex-CMO da Semantix (Nasdaq), cofundador da AI Brasil",
        dominio="https://alexandrecaramaschi.com",
        badge_color="#D4AF37",
    )

    return course


def main():
    course = build_course()
    gen = TsxGenerator()

    # Generate to deployed output
    target = Path(__file__).resolve().parent.parent / "output" / "deployed"
    page_path, layout_path = gen.write(course, target)

    print(f"\npage.tsx gerado: {page_path} ({page_path.stat().st_size} bytes)")
    print(f"layout.tsx gerado: {layout_path} ({layout_path.stat().st_size} bytes)")
    print(f"Slug: {course.slug}")
    print(f"Steps: {len(course.steps)}")
    total_sections = sum(len(s.content) for s in course.steps)
    print(f"Total seções: {total_sections}")
    print(f"FAQ: {len(course.faq)}")

    # Copy to landing-page-geo
    landing = Path("C:/Sandyboxclaude/landing-page-geo/src/app/educacao") / course.slug
    landing.mkdir(parents=True, exist_ok=True)

    page_content = page_path.read_text(encoding="utf-8")
    (landing / "page.tsx").write_text(page_content, encoding="utf-8")

    layout_content = layout_path.read_text(encoding="utf-8")
    (landing / "layout.tsx").write_text(layout_content, encoding="utf-8")

    print(f"Copiado para: {landing}")


if __name__ == "__main__":
    main()
