"""Generate clean TSX course from expanded Markdown modules.

v2: Proper section splitting, no raw Markdown in output,
subsection headers as standalone text lines, paragraph breaks preserved.
"""
import sys
import re
import json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.models import (
    CourseDefinition, StepDefinition, CourseSection, SectionType, FAQItem, NivelCurso
)
from src.generators.tsx_generator import TsxGenerator


def split_modules(filepath: Path) -> dict[int, str]:
    text = filepath.read_text(encoding="utf-8")
    modules = {}
    parts = re.split(r'(?=^# M[oó]dulo \d+)', text, flags=re.MULTILINE)
    for part in parts:
        match = re.match(r'^# M[oó]dulo (\d+)', part)
        if match:
            modules[int(match.group(1))] = part
    return modules


def clean_text(text: str) -> str:
    """Clean Markdown formatting from text."""
    # Remove bold markers
    text = re.sub(r'\*\*([^*]+)\*\*', r'\1', text)
    # Remove italic markers
    text = re.sub(r'\*([^*]+)\*', r'\1', text)
    # Remove horizontal rules
    text = re.sub(r'\n---\n', '\n', text)
    text = re.sub(r'^---$', '', text, flags=re.MULTILINE)
    # Remove ### and #### sub-headings markers but keep text
    text = re.sub(r'^#{3,4}\s+', '', text, flags=re.MULTILINE)
    # Clean up excessive blank lines
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()


def convert_bullets(text: str) -> str:
    """Convert - bullets to -- format (template convention)."""
    return re.sub(r'^- ', '-- ', text, flags=re.MULTILINE)


def split_into_paragraphs(text: str, max_chars: int = 600) -> list[str]:
    """Split text into paragraph-sized chunks."""
    paragraphs = re.split(r'\n\n+', text)
    chunks = []
    current = []
    current_len = 0

    for para in paragraphs:
        para = para.strip()
        if not para:
            continue

        if current_len + len(para) > max_chars and current:
            chunks.append('\n\n'.join(current))
            current = [para]
            current_len = len(para)
        else:
            current.append(para)
            current_len += len(para)

    if current:
        chunks.append('\n\n'.join(current))

    return chunks


def parse_module(md_text: str, module_num: int) -> list[CourseSection]:
    """Parse a module's Markdown into clean CourseSection list."""
    sections: list[CourseSection] = []

    # Split by ## subsection headers
    subsection_pattern = r'^## \d+\.\d+\s+'
    parts = re.split(r'(?=^## \d+\.\d+\s+)', md_text, flags=re.MULTILINE)

    for part in parts:
        part = part.strip()
        if not part or len(part) < 30:
            continue

        # Skip the module title header (# Modulo N: ...)
        if re.match(r'^# M[oó]dulo \d+', part):
            # Only skip the first line (module title)
            lines = part.split('\n', 1)
            if len(lines) > 1:
                part = lines[1].strip()
            else:
                continue
            if not part or len(part) < 30:
                continue

        # Extract subsection header if present
        header_match = re.match(r'^## \d+\.\d+\s+(.*?)$', part, re.MULTILINE)
        header = ""
        body = part
        if header_match:
            header = header_match.group(1).strip()
            body = part[header_match.end():].strip()

        # Clean the body
        body = clean_text(body)
        body = convert_bullets(body)

        if not body or len(body) < 20:
            continue

        # Determine section type
        is_exercise = bool(re.search(r'exerc[ií]cio|fixação', header.lower())) if header else False
        is_summary = bool(re.search(r'resumo', header.lower())) if header else False
        is_intro = bool(re.search(r'introdução|introducao', header.lower())) if header else False

        if is_exercise:
            # Exercises as tip
            exercise_text = header + '\n\n' + body if header else body
            sections.append(CourseSection(type=SectionType.TIP, value=exercise_text))
            continue

        if is_summary:
            summary_text = header + '\n\n' + body if header else body
            sections.append(CourseSection(type=SectionType.TEXT, value=summary_text))
            continue

        # Split body into paragraph-sized chunks
        chunks = split_into_paragraphs(body, max_chars=700)

        for idx, chunk in enumerate(chunks):
            # Add header to first chunk of this subsection
            if idx == 0 and header:
                chunk = header + '\n\n' + chunk

            # Check if this chunk contains warning-worthy content
            has_warning = any(w in chunk.lower() for w in [
                'erro mais comum', 'nunca copie', 'penaliza', 'cuidado',
                'não cometa', 'grave', 'fatal', 'destruir', 'aniquila'
            ])

            if has_warning and not is_intro:
                sections.append(CourseSection(type=SectionType.WARNING, value=chunk))
            else:
                sections.append(CourseSection(type=SectionType.TEXT, value=chunk))

    # Ensure minimum 3 sections
    while len(sections) < 3:
        sections.append(CourseSection(
            type=SectionType.TEXT,
            value=f"Conteúdo complementar do módulo {module_num}."
        ))

    # Add checkpoint
    sections.append(CourseSection(
        type=SectionType.CHECKPOINT,
        value=f"Você concluiu o Módulo {module_num}. Revise os exercícios práticos e aplique os conceitos no seu negócio antes de prosseguir para o próximo módulo."
    ))

    return sections


def build_course() -> CourseDefinition:
    drafts = Path(__file__).resolve().parent.parent / "output" / "drafts"

    mods_1_4 = split_modules(drafts / "modulos-1-4-expanded.md")
    mods_5_8 = split_modules(drafts / "modulos-5-8-expanded.md")
    all_mods = {**mods_1_4, **mods_5_8}

    print(f"Módulos encontrados: {sorted(all_mods.keys())}")

    module_defs = [
        {"id": "fundamentos-mercado-psicologia", "title": "Fundamentação, Inteligência de Mercado e Psicologia do Consumidor Joalheiro", "duration": "60 min", "icon_key": "trendingUp", "description": "Motivadores emocionais, tendências 2025-2026, economia da revenda e vocabulário semântico do setor joalheiro."},
        {"id": "seo-classico-ecommerce", "title": "A Fundação Inabalável do SEO Clássico em E-commerce de Acessórios", "duration": "60 min", "icon_key": "search", "description": "Auditoria técnica on-page, pesquisa de palavras-chave, otimização de conteúdo e monitoramento com Google Search Console."},
        {"id": "geo-aeo-nova-fronteira", "title": "A Nova Fronteira — Dominando GEO e AEO", "duration": "60 min", "icon_key": "megaphone", "description": "GEO vs SEO, RAG, conteúdo answer-first, otimização de entidades e linguagem para LLMs."},
        {"id": "eeat-confianca", "title": "A Engenharia da Confiança — E-E-A-T para Revendedoras Autônomas", "duration": "60 min", "icon_key": "handshake", "description": "Experiência, Especialização, Autoridade e Confiabilidade aplicados ao comércio de joias."},
        {"id": "busca-visual-google-lens", "title": "Otimização de Busca Visual, Multimodalidade e Google Lens", "duration": "60 min", "icon_key": "barChart", "description": "SEO visual, alt text semântico, Product Schema, Google Merchant Center e direção de arte."},
        {"id": "seo-local-goiania", "title": "Hegemonia Geográfica e SEO Local (Estudo de Caso: Goiânia)", "duration": "60 min", "icon_key": "briefcase", "description": "Google Business Profile, consistência NAP, link building local e captação de reviews."},
        {"id": "social-commerce-whatsapp", "title": "Social Commerce, Catálogos e o Ecossistema do WhatsApp Business", "duration": "60 min", "icon_key": "shoppingCart", "description": "SEO no catálogo WhatsApp, scripts de conversão, Status estratégico e integração com Instagram."},
        {"id": "stack-ia-kpis", "title": "Stack Tecnológico, Automação com IA e KPIs da Era Generativa", "duration": "60 min", "icon_key": "database", "description": "IA como assistente, ferramentas SEO/GEO, novos KPIs generativos e plano de execução contínua."},
    ]

    steps = []
    for i, mdef in enumerate(module_defs, 1):
        md_content = all_mods.get(i, "")
        if not md_content:
            print(f"  AVISO: Módulo {i} não encontrado!")
            continue

        content_sections = parse_module(md_content, i)
        print(f"  Módulo {i}: {len(content_sections)} seções ({sum(len(s.value) for s in content_sections)} chars)")

        steps.append(StepDefinition(
            id=mdef["id"],
            title=mdef["title"],
            duration=mdef["duration"],
            icon_key=mdef["icon_key"],
            description=mdef["description"],
            content=content_sections,
        ))

    faq = [
        FAQItem(pergunta="O que é GEO e por que revendedoras de joias precisam disso?", resposta="GEO (Generative Engine Optimization) é a otimização de conteúdo para ser citado em respostas de IAs como ChatGPT, Perplexity e Google AI Overviews. Revendedoras precisam porque o tráfego vindo de IAs converte de 4,4 a 23 vezes mais que o tráfego orgânico tradicional, e ignorar esse canal significa perder vendas de alta intenção."),
        FAQItem(pergunta="Preciso de site próprio ou funciona só com WhatsApp e Instagram?", resposta="O curso ensina a otimizar ambos os cenários. O WhatsApp Business tem um catálogo indexável que funciona como motor de busca interno. Porém, ter um site próprio (mesmo simples, em Nuvemshop ou Shopify) potencializa drasticamente o SEO clássico, os dados estruturados e a visibilidade em IAs generativas."),
        FAQItem(pergunta="Quanto tempo leva para ver resultados com SEO em semijoias?", resposta="SEO clássico costuma mostrar resultados mensuráveis entre 3 e 6 meses. GEO pode gerar citações em IAs em semanas se o conteúdo for bem estruturado com FAQs, entidades claras e dados factuais. SEO local (Google Business Profile) pode gerar resultados em poucas semanas com avaliações e consistência NAP."),
        FAQItem(pergunta="Como fazer minha marca ser citada pelo ChatGPT e Perplexity?", resposta="Você precisa criar conteúdo answer-first: FAQs rigorosas, definições diretas, dados estruturados (Schema.org) e entidades claras. Os LLMs usam RAG para selecionar fontes, priorizando conteúdo factual, sem ambiguidades e com autoridade demonstrada via E-E-A-T."),
        FAQItem(pergunta="SEO local funciona para quem vende apenas online, sem loja física?", resposta="Sim, parcialmente. Mesmo sem loja física, você pode otimizar para buscas regionais criando conteúdo localizado e participando de diretórios e associações locais. Para quem tem ponto de venda ou atende em uma região específica, o SEO local com Google Business Profile é indispensável."),
        FAQItem(pergunta="Qual a diferença entre SEO clássico e GEO na prática?", resposta="SEO clássico otimiza para você aparecer nos resultados do Google e receber cliques. GEO otimiza para você ser citado e recomendado dentro das respostas de IAs. O SEO foca em palavras-chave e backlinks; o GEO foca em entidades, dados estruturados e conteúdo modular em formato de pergunta e resposta."),
        FAQItem(pergunta="Como otimizar imagens de joias para o Google Lens?", resposta="Use formato WebP com compressão abaixo de 100kb, alt text descritivo em linguagem natural (não keyword stuffing), e implemente Product Schema com name, brand, offers e aggregateRating. Fotos com fundo limpo, boa iluminação e detalhes de textura performam melhor em busca visual."),
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


def post_process_tsx(filepath: Path):
    """Fix remaining Jinja2 variables not rendered by template."""
    content = filepath.read_text(encoding="utf-8")

    replacements = {
        '{{ hero_gradient_from }}': '#4A1942',
        '{{ hero_gradient_to }}': '#D4AF37',
        '{{ titulo | js_escape }}': 'SEO e GEO para Revendedoras de Joias e Semijoias: Autoridade e Vendas na Era da IA',
        '{{ descricao | js_escape }}': 'Curso completo que une SEO clássico e GEO (Generative Engine Optimization) para revendedoras de joias e semijoias. Da pesquisa de palavras-chave à citação em ChatGPT e Perplexity, passando por E-E-A-T, busca visual, SEO local, WhatsApp Business e métricas da era generativa.',
        '{{ nivel_display | js_escape }}': 'Intermediário',
        '{{ steps | length }}': '8',
        '{{ duracao_total_minutos }}': '480',
        '{{ autor_nome | js_escape }}': 'Alexandre Caramaschi',
        '{{ autor_credencial | js_escape }}': 'CEO da Brasil GEO, ex-CMO da Semantix (Nasdaq), cofundador da AI Brasil',
        '{{ dominio }}': 'alexandrecaramaschi.com',
        '{{ canonical_url }}': 'https://alexandrecaramaschi.com/educacao/seo-geo-revendedoras-joias',
        '{{ descricao_curta | js_escape }}': 'Domine SEO clássico e GEO para capturar tráfego orgânico e generativo no mercado joalheiro brasileiro de USD 15 bilhões.',
        '{{ breadcrumb_label | js_escape }}': 'SEO e GEO para Revendedoras de Joias e Semijoias: Autoridade e Vendas na Era da IA',
        '{{ badge_color }}': '#D4AF37',
        '{{ duracao_display }}': '~480 min',
        '{{ local_storage_key }}': 'seo-geo-revendedoras-joias-course-progress',
        '{{ autor_nome[:2] | upper }}': 'AL',
    }

    for k, v in replacements.items():
        content = content.replace(k, v)

    # Handle FAQ loop
    faq_items = [
        ('O que é GEO e por que revendedoras de joias precisam disso?', 'GEO (Generative Engine Optimization) é a otimização de conteúdo para ser citado em respostas de IAs como ChatGPT, Perplexity e Google AI Overviews. Revendedoras precisam porque o tráfego vindo de IAs converte de 4,4 a 23 vezes mais que o tráfego orgânico tradicional, e ignorar esse canal significa perder vendas de alta intenção.'),
        ('Preciso de site próprio ou funciona só com WhatsApp e Instagram?', 'O curso ensina a otimizar ambos os cenários. O WhatsApp Business tem um catálogo indexável que funciona como motor de busca interno. Porém, ter um site próprio (mesmo simples, em Nuvemshop ou Shopify) potencializa drasticamente o SEO clássico, os dados estruturados e a visibilidade em IAs generativas.'),
        ('Quanto tempo leva para ver resultados com SEO em semijoias?', 'SEO clássico costuma mostrar resultados mensuráveis entre 3 e 6 meses. GEO pode gerar citações em IAs em semanas se o conteúdo for bem estruturado com FAQs, entidades claras e dados factuais. SEO local (Google Business Profile) pode gerar resultados em poucas semanas com avaliações e consistência NAP.'),
        ('Como fazer minha marca ser citada pelo ChatGPT e Perplexity?', 'Você precisa criar conteúdo answer-first: FAQs rigorosas, definições diretas, dados estruturados (Schema.org) e entidades claras. Os LLMs usam RAG para selecionar fontes, priorizando conteúdo factual, sem ambiguidades e com autoridade demonstrada via E-E-A-T.'),
        ('SEO local funciona para quem vende apenas online, sem loja física?', 'Sim, parcialmente. Mesmo sem loja física, você pode otimizar para buscas regionais criando conteúdo localizado e participando de diretórios e associações locais. Para quem tem ponto de venda ou atende em uma região específica, o SEO local com Google Business Profile é indispensável.'),
        ('Qual a diferença entre SEO clássico e GEO na prática?', 'SEO clássico otimiza para você aparecer nos resultados do Google e receber cliques. GEO otimiza para você ser citado e recomendado dentro das respostas de IAs. O SEO foca em palavras-chave e backlinks; o GEO foca em entidades, dados estruturados e conteúdo modular em formato de pergunta e resposta.'),
        ('Como otimizar imagens de joias para o Google Lens?', 'Use formato WebP com compressão abaixo de 100kb, alt text descritivo em linguagem natural (não keyword stuffing), e implemente Product Schema com name, brand, offers e aggregateRating. Fotos com fundo limpo, boa iluminação e detalhes de textura performam melhor em busca visual.'),
    ]

    faq_schema = ''
    for q, a in faq_items:
        faq_schema += f'''                  {{
                    "@type": "Question",
                    name: "{q}",
                    acceptedAnswer: {{
                      "@type": "Answer",
                      text: "{a}",
                    }},
                  }},\n'''

    faq_pattern = r'\{%\s*for item in faq\s*%\}.*?\{%\s*endfor\s*%\}'
    content = re.sub(faq_pattern, faq_schema.rstrip(), content, flags=re.DOTALL)

    filepath.write_text(content, encoding="utf-8")
    print(f"Post-processed: {filepath}")


def main():
    course = build_course()
    gen = TsxGenerator()

    # Generate
    target = Path(__file__).resolve().parent.parent / "output" / "deployed"
    page_path, layout_path = gen.write(course, target)

    # Post-process to fix Jinja2 remnants
    post_process_tsx(page_path)

    print(f"\npage.tsx: {page_path} ({page_path.stat().st_size:,} bytes)")
    print(f"layout.tsx: {layout_path}")
    print(f"Steps: {len(course.steps)}, Seções: {sum(len(s.content) for s in course.steps)}")

    # Copy to landing-page-geo
    landing = Path("C:/Sandyboxclaude/landing-page-geo/src/app/educacao") / course.slug
    landing.mkdir(parents=True, exist_ok=True)

    (landing / "page.tsx").write_text(page_path.read_text(encoding="utf-8"), encoding="utf-8")
    (landing / "layout.tsx").write_text(layout_path.read_text(encoding="utf-8"), encoding="utf-8")

    print(f"Copiado para: {landing}")


if __name__ == "__main__":
    main()
