#!/usr/bin/env python3
"""Convert curso-factory draft JSONs to landing-page-geo page.tsx files.

Reads the draft content from the pipeline output, parses the markdown into
Step/Section structures, and generates page.tsx files following the existing
seo-geo-advogados pattern.
"""

import json
import re
import sys
import os
import unicodedata

sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

# ── Course metadata ──
COURSES = {
    "automacao-n8n-make": {
        "draft_file": "output/drafts/automacao-com-n8n-e-make_20260330_121843.json",
        "target_dir": "/c/Sandyboxclaude/landing-page-geo/src/app/educacao/automacao-n8n-make",
        "course_id": "automacao-n8n-make",
        "title": "Automacao com n8n e Make: Fluxos Inteligentes com IA",
        "title_display": "Automa\u00e7\u00e3o com n8n e Make: Fluxos Inteligentes com IA",
        "description": "Criar automa\u00e7\u00f5es visuais conectando APIs, LLMs, bancos de dados e servi\u00e7os. Webhooks, triggers e integra\u00e7\u00f5es reais.",
        "badge_color": "#EA580C",
        "level": "Intermedi\u00e1rio",
        "duration": "~200 min",
        "modules_count": 10,
        "storage_key": "automacao-n8n-make-course-progress",
        "tags": "n8n, Make, Automa\u00e7\u00e3o, Webhooks, IA",
        "badge_text": "Curso de automa\u00e7\u00e3o no-code/low-code",
        "hero_desc": "10 m\u00f3dulos pr\u00e1ticos para criar fluxos de automa\u00e7\u00e3o conectando APIs, LLMs, bancos de dados e servi\u00e7os. Com n8n, Make, webhooks, triggers e integra\u00e7\u00f5es reais de mercado.",
        "completion_text": "Voc\u00ea completou todos os m\u00f3dulos do curso Automa\u00e7\u00e3o com n8n e Make. Agora voc\u00ea sabe criar fluxos inteligentes conectando APIs, LLMs e servi\u00e7os, com deploy e monitoramento em produ\u00e7\u00e3o.",
        "intro_text": "Ao final deste curso, voc\u00ea saber\u00e1 criar automa\u00e7\u00f5es visuais sem c\u00f3digo usando n8n e Make, integrar APIs REST, LLMs e bancos de dados, configurar webhooks e triggers, e fazer deploy de fluxos em produ\u00e7\u00e3o.",
        "intro_features": [
            ("workflow", "Fluxos visuais sem c\u00f3digo"),
            ("zap", "Integra\u00e7\u00e3o com LLMs"),
            ("globe", "Webhooks e APIs REST"),
        ],
        "prerequisites": [
            ("targetSm", "Profissionais de marketing, opera\u00e7\u00f5es ou TI"),
            ("trendUp", "Interesse em automa\u00e7\u00e3o de processos"),
            ("users", "N\u00e3o \u00e9 necess\u00e1rio saber programar"),
            ("zap", "Conta gratuita no n8n ou Make"),
        ],
        "faq": [
            ("Preciso saber programar?", "N\u00e3o. O n8n e o Make s\u00e3o ferramentas no-code/low-code. O curso ensina a criar fluxos visuais sem escrever c\u00f3digo. Os m\u00f3dulos que envolvem APIs mostram como configurar tudo pela interface visual."),
            ("Quanto custa?", "100% gratuito. Sem taxas ocultas. O curso faz parte do material educacional da Brasil GEO."),
            ("Qual a diferen\u00e7a entre n8n e Make?", "O n8n \u00e9 open-source e pode ser auto-hospedado, oferecendo mais controle. O Make tem interface mais visual e integra\u00e7\u00f5es prontas. O curso cobre ambos para voc\u00ea escolher o melhor para cada caso."),
            ("Preciso de conta paga?", "N\u00e3o. Tanto o n8n (cloud tier gratuito ou self-hosted) quanto o Make (plano gratuito) permitem seguir todos os exerc\u00edcios do curso."),
            ("Quanto tempo levo para completar?", "No seu ritmo. O conte\u00fado total \u00e9 de aproximadamente 200 minutos. O progresso \u00e9 salvo automaticamente no seu navegador."),
        ],
        "author_desc": "Este curso faz parte do material educacional da Brasil GEO, empresa brasileira especializada em Generative Engine Optimization. O conte\u00fado cobre as ferramentas de automa\u00e7\u00e3o mais usadas no mercado com exemplos pr\u00e1ticos de integra\u00e7\u00e3o com LLMs.",
    },
    "llm-finops": {
        "draft_file": "output/drafts/llm-finops_20260330_112812.json",
        "target_dir": "/c/Sandyboxclaude/landing-page-geo/src/app/educacao/llm-finops",
        "course_id": "llm-finops",
        "title": "LLM FinOps: Custos, Otimizacao e Governanca de IA",
        "title_display": "LLM FinOps: Custos, Otimiza\u00e7\u00e3o e Governan\u00e7a de IA",
        "description": "Gest\u00e3o de custos com LLMs, cache sem\u00e2ntico, roteamento inteligente, budget guards, dashboards e relat\u00f3rios para C-Level.",
        "badge_color": "#EA580C",
        "level": "Avan\u00e7ado",
        "duration": "~211 min",
        "modules_count": 10,
        "storage_key": "llm-finops-course-progress",
        "tags": "FinOps, LLM, Custos, Governan\u00e7a, Otimiza\u00e7\u00e3o",
        "badge_text": "Curso de gest\u00e3o de custos de IA",
        "hero_desc": "10 m\u00f3dulos pr\u00e1ticos com c\u00f3digo Python e TypeScript para monitorar, otimizar e governar gastos com LLMs. Cache sem\u00e2ntico, roteamento inteligente, budget guards e relat\u00f3rios para C-Level.",
        "completion_text": "Voc\u00ea completou todos os m\u00f3dulos do curso LLM FinOps. Agora voc\u00ea sabe monitorar custos de LLMs em tempo real, implementar cache sem\u00e2ntico e roteamento inteligente, criar budget guards e apresentar relat\u00f3rios ao C-Level.",
        "intro_text": "Ao final deste curso, voc\u00ea saber\u00e1 calcular custos de chamadas LLM, implementar cache sem\u00e2ntico e roteamento inteligente, criar budget guards e circuit breakers, e montar relat\u00f3rios de ROI para o C-Level.",
        "intro_features": [
            ("barChart", "Monitoramento de custos"),
            ("shield", "Budget guards"),
            ("layers", "Relat\u00f3rios C-Level"),
        ],
        "prerequisites": [
            ("targetSm", "Desenvolvedores, tech leads ou gestores de IA"),
            ("trendUp", "Familiaridade b\u00e1sica com APIs de LLM"),
            ("users", "Conhecimento b\u00e1sico de Python ou TypeScript"),
            ("zap", "Acesso a pelo menos uma API de LLM"),
        ],
        "faq": [
            ("Preciso de conhecimento t\u00e9cnico?", "Sim, conhecimento b\u00e1sico de programa\u00e7\u00e3o (Python ou TypeScript) \u00e9 recomendado. Os exemplos de c\u00f3digo s\u00e3o detalhados e comentados."),
            ("Quanto custa?", "100% gratuito. Sem taxas ocultas. O curso faz parte do material educacional da Brasil GEO."),
            ("Funciona com qualquer provedor de LLM?", "Sim. Os conceitos e t\u00e9cnicas se aplicam a OpenAI, Anthropic, Google, Groq e qualquer outro provedor. Os exemplos cobrem m\u00faltiplos provedores."),
            ("Quanto tempo levo para completar?", "No seu ritmo. O conte\u00fado total \u00e9 de aproximadamente 211 minutos. O progresso \u00e9 salvo automaticamente no seu navegador."),
            ("Serve para empresas pequenas?", "Sim. Mesmo startups que gastam US$ 500/m\u00eas com LLMs podem economizar 30-50% aplicando as t\u00e9cnicas deste curso. Para empresas que gastam US$ 10.000+/m\u00eas, o impacto \u00e9 ainda maior."),
        ],
        "author_desc": "Este curso faz parte do material educacional da Brasil GEO, empresa brasileira especializada em Generative Engine Optimization. O conte\u00fado integra pr\u00e1ticas reais de gest\u00e3o de custos com LLMs aplicadas no dia a dia da opera\u00e7\u00e3o.",
    },
    "mcp-avancado": {
        "draft_file": "output/drafts/mcp-avancado_20260330_111825.json",
        "target_dir": "/c/Sandyboxclaude/landing-page-geo/src/app/educacao/mcp-avancado",
        "course_id": "mcp-avancado",
        "title": "MCP Avancado: Servidores, Protocolos e Integracoes",
        "title_display": "MCP Avan\u00e7ado: Servidores, Protocolos e Integra\u00e7\u00f5es",
        "description": "Model Context Protocol em profundidade: criar servidores MCP, recursos, tools, sampling, integra\u00e7\u00f5es com browsers e IDEs.",
        "badge_color": "#7C3AED",
        "level": "Avan\u00e7ado",
        "duration": "~245 min",
        "modules_count": 12,
        "storage_key": "mcp-avancado-course-progress",
        "tags": "MCP, Protocolo, Servidores, Integra\u00e7\u00e3o",
        "badge_text": "Curso avan\u00e7ado de Model Context Protocol",
        "hero_desc": "12 m\u00f3dulos pr\u00e1ticos para dominar o Model Context Protocol: criar servidores MCP, expor resources e tools, configurar transport layers, integrar com IDEs e browsers, e fazer deploy em produ\u00e7\u00e3o.",
        "completion_text": "Voc\u00ea completou todos os m\u00f3dulos do curso MCP Avan\u00e7ado. Agora voc\u00ea sabe criar servidores MCP, expor resources e tools, configurar transporte e autentica\u00e7\u00e3o, integrar com IDEs e browsers, e fazer deploy em produ\u00e7\u00e3o.",
        "intro_text": "Ao final deste curso, voc\u00ea saber\u00e1 criar servidores MCP com TypeScript SDK, expor resources e tools para LLMs, configurar transport layers, integrar com VS Code e Chrome, e orquestrar m\u00faltiplos servidores.",
        "intro_features": [
            ("code", "Servidores MCP com TypeScript"),
            ("layers", "Resources, Tools e Prompts"),
            ("globe", "Integra\u00e7\u00e3o IDE + Browser"),
        ],
        "prerequisites": [
            ("targetSm", "Desenvolvedores com experi\u00eancia em TypeScript/Node.js"),
            ("trendUp", "Conhecimento b\u00e1sico do MCP (ver curso MCP com Chrome)"),
            ("users", "Familiaridade com APIs REST e JSON"),
            ("zap", "Node.js 20+ e VS Code instalados"),
        ],
        "faq": [
            ("Preciso fazer o curso MCP com Chrome primeiro?", "Recomendado, mas n\u00e3o obrigat\u00f3rio. O m\u00f3dulo 1 revisa os fundamentos do MCP. Se voc\u00ea j\u00e1 conhece o protocolo, pode come\u00e7ar direto."),
            ("Quanto custa?", "100% gratuito. Sem taxas ocultas. O curso faz parte do material educacional da Brasil GEO."),
            ("Qual linguagem \u00e9 usada?", "TypeScript \u00e9 a linguagem principal, usando o MCP SDK oficial. Exemplos em Python s\u00e3o fornecidos quando relevante."),
            ("Quanto tempo levo para completar?", "No seu ritmo. O conte\u00fado total \u00e9 de aproximadamente 245 minutos. O progresso \u00e9 salvo automaticamente no seu navegador."),
            ("Serve para criar integrações comerciais?", "Sim. O curso cobre autentica\u00e7\u00e3o OAuth, seguran\u00e7a, deploy em Docker e monitoramento, tudo necess\u00e1rio para servidores MCP em produ\u00e7\u00e3o."),
        ],
        "author_desc": "Este curso faz parte do material educacional da Brasil GEO, empresa brasileira especializada em Generative Engine Optimization. O conte\u00fado cobre o Model Context Protocol em profundidade com exemplos pr\u00e1ticos de integra\u00e7\u00e3o.",
    },
    "prompt-engineering-avancado": {
        "draft_file": "output/drafts/prompt-engineering-avancado_20260330_113510.json",
        "target_dir": "/c/Sandyboxclaude/landing-page-geo/src/app/educacao/prompt-engineering-avancado",
        "course_id": "prompt-engineering-avancado",
        "title": "Prompt Engineering Avancado: Tecnicas Profissionais",
        "title_display": "Prompt Engineering Avan\u00e7ado: T\u00e9cnicas Profissionais",
        "description": "Chain-of-thought, few-shot, constitutional AI, prompt chaining, avalia\u00e7\u00e3o sistem\u00e1tica e otimiza\u00e7\u00e3o de custos.",
        "badge_color": "#DB2777",
        "level": "Avan\u00e7ado",
        "duration": "~240 min",
        "modules_count": 12,
        "storage_key": "prompt-engineering-avancado-course-progress",
        "tags": "Prompt Engineering, Chain-of-Thought, Few-Shot, Avalia\u00e7\u00e3o",
        "badge_text": "Curso avan\u00e7ado de prompt engineering",
        "hero_desc": "12 m\u00f3dulos pr\u00e1ticos com t\u00e9cnicas profissionais de prompt engineering: chain-of-thought, few-shot, role prompting, structured output, RAG, prompt chaining, avalia\u00e7\u00e3o sistem\u00e1tica e otimiza\u00e7\u00e3o de custos.",
        "completion_text": "Voc\u00ea completou todos os m\u00f3dulos do curso Prompt Engineering Avan\u00e7ado. Agora voc\u00ea domina t\u00e9cnicas profissionais de engenharia de prompts, sabe avaliar qualidade sistematicamente e otimizar custos em produ\u00e7\u00e3o.",
        "intro_text": "Ao final deste curso, voc\u00ea saber\u00e1 aplicar chain-of-thought, few-shot learning, role prompting, structured output, prompt chaining e RAG. Al\u00e9m disso, dominar\u00e1 avalia\u00e7\u00e3o sistem\u00e1tica e otimiza\u00e7\u00e3o de custos.",
        "intro_features": [
            ("brain", "T\u00e9cnicas avan\u00e7adas de prompt"),
            ("code", "Structured output"),
            ("barChart", "Avalia\u00e7\u00e3o e m\u00e9tricas"),
        ],
        "prerequisites": [
            ("targetSm", "Desenvolvedores, product managers ou analistas de dados"),
            ("trendUp", "Experi\u00eancia b\u00e1sica com LLMs (ChatGPT, Claude, Gemini)"),
            ("users", "Conhecimento b\u00e1sico de programa\u00e7\u00e3o \u00e9 recomendado"),
            ("zap", "Acesso a pelo menos uma API de LLM"),
        ],
        "faq": [
            ("Preciso saber programar?", "Recomendado, mas n\u00e3o obrigat\u00f3rio. Os m\u00f3dulos conceituais s\u00e3o acess\u00edveis sem c\u00f3digo. Os m\u00f3dulos pr\u00e1ticos usam Python com exemplos detalhados."),
            ("Quanto custa?", "100% gratuito. Sem taxas ocultas. O curso faz parte do material educacional da Brasil GEO."),
            ("Funciona com qualquer LLM?", "Sim. As t\u00e9cnicas se aplicam a OpenAI, Anthropic, Google e outros. Exemplos cobrem m\u00faltiplos modelos."),
            ("Quanto tempo levo para completar?", "No seu ritmo. O conte\u00fado total \u00e9 de aproximadamente 240 minutos. O progresso \u00e9 salvo automaticamente no seu navegador."),
            ("Qual a diferen\u00e7a para o curso b\u00e1sico de Claude Code?", "O curso de Claude Code ensina a usar a ferramenta. Este curso ensina as t\u00e9cnicas de engenharia de prompts que se aplicam a qualquer LLM, com foco em produ\u00e7\u00e3o e escala."),
        ],
        "author_desc": "Este curso faz parte do material educacional da Brasil GEO, empresa brasileira especializada em Generative Engine Optimization. O conte\u00fado cobre t\u00e9cnicas profissionais de prompt engineering validadas em produ\u00e7\u00e3o.",
    },
}

# ── Icon sets per course ──
ICON_SETS = {
    "automacao-n8n-make": [
        "rocket", "workflow", "terminal", "code", "globe",
        "zap", "database", "layers", "shield", "barChart",
    ],
    "llm-finops": [
        "rocket", "barChart", "database", "cloud", "workflow",
        "shield", "zap", "layers", "globe", "terminal",
    ],
    "mcp-avancado": [
        "rocket", "code", "database", "layers", "terminal",
        "workflow", "globe", "shield", "zap", "barChart",
        "cloud", "server",
    ],
    "prompt-engineering-avancado": [
        "rocket", "brain", "code", "layers", "workflow",
        "terminal", "database", "globe", "zap", "barChart",
        "shield", "cloud",
    ],
}


def slugify(text: str) -> str:
    """Convert text to URL-safe slug."""
    text = unicodedata.normalize('NFKD', text)
    text = text.encode('ascii', 'ignore').decode('ascii')
    text = re.sub(r'[^\w\s-]', '', text.lower())
    text = re.sub(r'[-\s]+', '-', text).strip('-')
    return text


def parse_module_content(text: str) -> list:
    """Parse markdown text into Section objects for a course module."""
    sections = []
    lines = text.strip().split('\n')

    current_text = []
    in_code_block = False
    code_lines = []
    code_lang = ""

    def flush_text():
        nonlocal current_text
        if current_text:
            combined = '\n'.join(current_text).strip()
            if combined:
                sections.append({"type": "text", "value": combined})
            current_text = []

    i = 0
    while i < len(lines):
        line = lines[i]

        # Code blocks
        if line.strip().startswith('```'):
            if not in_code_block:
                flush_text()
                in_code_block = True
                code_lang = line.strip()[3:].strip() or "text"
                code_lines = []
            else:
                in_code_block = False
                sections.append({
                    "type": "code",
                    "value": '\n'.join(code_lines),
                    "language": code_lang,
                })
            i += 1
            continue

        if in_code_block:
            code_lines.append(line)
            i += 1
            continue

        # Skip markdown headers (## and ###) - they become part of text flow
        stripped = line.strip()
        if stripped.startswith('#'):
            # Convert headers to sub-heading format (line ending with :)
            header_text = re.sub(r'^#{1,4}\s*', '', stripped)
            # Skip numbered prefixes like "1. " "2. "
            header_text = re.sub(r'^\d+\.\s*', '', header_text)
            if header_text:
                flush_text()
                current_text.append(f"{header_text}:")
            i += 1
            continue

        # Blockquotes -> tips or warnings
        if stripped.startswith('> '):
            flush_text()
            quote_text = stripped[2:]
            # Collect multi-line blockquotes
            while i + 1 < len(lines) and lines[i+1].strip().startswith('> '):
                i += 1
                quote_text += ' ' + lines[i].strip()[2:]

            if any(w in quote_text.lower() for w in ['atenção', 'cuidado', 'aviso', 'nunca', 'jamais', 'proibido']):
                sections.append({"type": "warning", "value": quote_text})
            else:
                sections.append({"type": "tip", "value": quote_text})
            i += 1
            continue

        # Empty lines separate paragraphs
        if not stripped:
            if current_text:
                flush_text()
            i += 1
            continue

        # Regular text
        current_text.append(line)
        i += 1

    flush_text()

    # If no checkpoint at the end, add one from the last section
    if sections and sections[-1]["type"] != "checkpoint":
        # Look for "checkpoint" or "verificação" text in the last few sections
        for idx in range(len(sections)-1, max(len(sections)-3, -1), -1):
            if idx >= 0 and sections[idx]["type"] == "text":
                val = sections[idx]["value"].lower()
                if 'checkpoint' in val or 'verificação' in val or 'neste ponto' in val:
                    sections[idx]["type"] = "checkpoint"
                    break

    return sections


def deduplicate_modules(titles_and_contents: list) -> list:
    """Remove duplicate modules (same title), keeping the longer content."""
    seen = {}
    for title, content in titles_and_contents:
        # Normalize title for comparison
        norm_title = title.strip().lower()
        if norm_title not in seen:
            seen[norm_title] = (title, content)
        else:
            # Keep the one with more content
            existing = seen[norm_title]
            if len(content) > len(existing[1]):
                seen[norm_title] = (title, content)
    return list(seen.values())


def extract_modules_from_draft(draft_text: str, target_count: int) -> list:
    """Extract modules from draft markdown text."""
    # Split by module headers
    parts = re.split(r'^# Módulo \d+:\s*', draft_text, flags=re.MULTILINE)

    modules_raw = []
    for part in parts[1:]:  # Skip empty first part
        lines = part.strip().split('\n')
        if not lines:
            continue
        title = lines[0].strip()
        # Skip if title is just a repeat of itself (some drafts have # Title again)
        content_start = 1
        if content_start < len(lines) and lines[content_start].strip() == '':
            content_start += 1
        # Check if next line is a duplicate title
        if content_start < len(lines):
            next_line = lines[content_start].strip()
            if next_line.startswith('#') and re.sub(r'^#+\s*', '', next_line).strip().lower() == title.lower():
                content_start += 1

        content = '\n'.join(lines[content_start:])
        modules_raw.append((title, content))

    # Deduplicate
    modules = deduplicate_modules(modules_raw)

    # Trim to target count if needed
    if len(modules) > target_count:
        modules = modules[:target_count]

    return modules


def escape_tsx_string(s: str) -> str:
    """Escape a string for use in TSX."""
    s = s.replace('\\', '\\\\')
    s = s.replace('"', '\\"')
    s = s.replace('\n', '\\n')
    s = s.replace('\r', '')
    # Convert markdown bold to ** format (kept as-is for FormattedText)
    return s


def generate_step_data(modules: list, course_meta: dict, icon_set: list) -> str:
    """Generate the STEPS array as TypeScript code."""
    lines = []
    lines.append("const STEPS: Step[] = [")

    for idx, (title, content) in enumerate(modules):
        step_id = slugify(title)
        if not step_id:
            step_id = f"modulo-{idx+1}"

        # Parse content into sections
        sections = parse_module_content(content)

        # Ensure we have at least some content
        if not sections:
            sections = [{"type": "text", "value": f"Conte\u00fado do m\u00f3dulo: {title}"}]

        # Ensure checkpoint at the end
        has_checkpoint = any(s["type"] == "checkpoint" for s in sections)
        if not has_checkpoint:
            sections.append({
                "type": "checkpoint",
                "value": f"Voc\u00ea concluiu o m\u00f3dulo sobre {title.lower()} e est\u00e1 pronto para avan\u00e7ar ao pr\u00f3ximo t\u00f3pico.",
            })

        duration = f"{18 + (idx % 5) * 2} min"
        icon_key = icon_set[idx % len(icon_set)]

        # Build description from first text section
        desc = ""
        for s in sections:
            if s["type"] == "text":
                desc = s["value"][:150].split('\n')[0]
                if len(desc) > 120:
                    desc = desc[:117] + "..."
                break
        if not desc:
            desc = title

        lines.append(f"  {{")
        lines.append(f'    id: "{step_id}",')
        lines.append(f'    title: "{escape_tsx_string(title)}",')
        lines.append(f'    duration: "{duration}",')
        lines.append(f'    icon: "{str(idx+1).zfill(2)}",')
        lines.append(f'    description: "{escape_tsx_string(desc)}",')
        lines.append(f"    content: [")

        for section in sections:
            stype = section["type"]
            sval = escape_tsx_string(section["value"])
            if stype == "code":
                lang = section.get("language", "text")
                lines.append(f'      {{ type: "code", value: "{sval}", language: "{lang}" }},')
            else:
                lines.append(f'      {{ type: "{stype}", value: "{sval}" }},')

        lines.append(f"    ],")
        lines.append(f"  }},")

    lines.append("];")
    return '\n'.join(lines)


def generate_step_icons_map(modules: list, icon_set: list) -> str:
    """Generate the STEP_ICONS mapping."""
    lines = []
    lines.append("const STEP_ICONS: Record<string, keyof typeof icons> = {")
    for idx, (title, _) in enumerate(modules):
        step_id = slugify(title)
        if not step_id:
            step_id = f"modulo-{idx+1}"
        icon_key = icon_set[idx % len(icon_set)]
        lines.append(f'  "{step_id}": "{icon_key}",')
    lines.append("};")
    return '\n'.join(lines)


def generate_page_tsx(course_key: str, modules: list) -> str:
    """Generate the complete page.tsx file."""
    meta = COURSES[course_key]
    icon_set = ICON_SETS[course_key]

    first_step_id = slugify(modules[0][0]) if modules else "modulo-1"

    step_data = generate_step_data(modules, meta, icon_set)
    step_icons = generate_step_icons_map(modules, icon_set)

    badge_color = meta["badge_color"]

    # Build FAQ JSON-LD
    faq_jsonld = []
    for q, a in meta["faq"]:
        faq_jsonld.append(f'''                  {{
                    "@type": "Question",
                    name: "{escape_tsx_string(q)}",
                    acceptedAnswer: {{
                      "@type": "Answer",
                      text: "{escape_tsx_string(a)}",
                    }},
                  }}''')

    faq_items = []
    for q, a in meta["faq"]:
        faq_items.append(f'''                    {{
                        q: "{escape_tsx_string(q)}",
                        a: "{escape_tsx_string(a)}",
                      }}''')

    intro_features = []
    for icon_name, label in meta["intro_features"]:
        intro_features.append(f'''                    <div className="flex items-center gap-3 text-sm text-[#DBEAFE] bg-white/5 rounded-lg px-3 py-2.5">
                      <span className="text-[#93C5FD]">{{icons.{icon_name}}}</span>
                      {label}
                    </div>''')

    prereq_items = []
    for icon_name, label in meta["prerequisites"]:
        prereq_items.append(f'''                      <li className="flex items-start gap-2">
                        <span className="mt-0.5 flex-shrink-0">{{icons.{icon_name}}}</span>
                        {label}
                      </li>''')

    # Function name from course_id
    func_name = ''.join(word.capitalize() for word in course_key.replace('-', ' ').split()) + "CoursePage"

    tsx = f'''"use client";

import {{ useState }} from "react";
import useProgress from "@/hooks/useProgress";
import Topbar from "@/components/Topbar";
import Breadcrumbs from "@/components/Breadcrumbs";
import Footer from "@/components/Footer";
import CourseEnhancements from "@/components/CourseEnhancements";

/* ───────── TYPES ───────── */
interface Step {{
  id: string;
  title: string;
  duration: string;
  icon: string;
  description: string;
  content: Section[];
}}

interface Section {{
  type: "text" | "code" | "warning" | "tip" | "checkpoint";
  value: string;
  language?: string;
  label?: string;
}}

/* ───────── LUCIDE ICONS (enterprise style) ───────── */
const icons: Record<string, React.ReactNode> = {{
  rocket: (
    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.75" strokeLinecap="round" strokeLinejoin="round">
      <path d="M4.5 16.5c-1.5 1.26-2 5-2 5s3.74-.5 5-2c.71-.84.7-2.13-.09-2.91a2.18 2.18 0 0 0-2.91-.09z"/><path d="m12 15-3-3a22 22 0 0 1 2-3.95A12.88 12.88 0 0 1 22 2c0 2.72-.78 7.5-6 11a22.35 22.35 0 0 1-4 2z"/><path d="M9 12H4s.55-3.03 2-4c1.62-1.08 5 0 5 0"/><path d="M12 15v5s3.03-.55 4-2c1.08-1.62 0-5 0-5"/>
    </svg>
  ),
  cloud: (
    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.75" strokeLinecap="round" strokeLinejoin="round">
      <path d="M17.5 19H9a7 7 0 1 1 6.71-9h1.79a4.5 4.5 0 1 1 0 9Z"/>
    </svg>
  ),
  code: (
    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.75" strokeLinecap="round" strokeLinejoin="round">
      <path d="m18 16 4-4-4-4"/><path d="m6 8-4 4 4 4"/><path d="m14.5 4-5 16"/>
    </svg>
  ),
  shield: (
    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.75" strokeLinecap="round" strokeLinejoin="round">
      <path d="M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1.17 1.17 0 0 1 1.52 0C14.51 3.81 17 5 19 5a1 1 0 0 1 1 1z"/>
    </svg>
  ),
  zap: (
    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.75" strokeLinecap="round" strokeLinejoin="round">
      <path d="M4 14a1 1 0 0 1-.78-1.63l9.9-10.2a.5.5 0 0 1 .86.46l-1.92 6.02A1 1 0 0 0 13 10h7a1 1 0 0 1 .78 1.63l-9.9 10.2a.5.5 0 0 1-.86-.46l1.92-6.02A1 1 0 0 0 11 14z"/>
    </svg>
  ),
  database: (
    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.75" strokeLinecap="round" strokeLinejoin="round">
      <ellipse cx="12" cy="5" rx="9" ry="3"/><path d="M3 5V19A9 3 0 0 0 21 19V5"/><path d="M3 12A9 3 0 0 0 21 12"/>
    </svg>
  ),
  globe: (
    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.75" strokeLinecap="round" strokeLinejoin="round">
      <circle cx="12" cy="12" r="10"/><path d="M12 2a14.5 14.5 0 0 0 0 20 14.5 14.5 0 0 0 0-20"/><path d="M2 12h20"/>
    </svg>
  ),
  workflow: (
    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.75" strokeLinecap="round" strokeLinejoin="round">
      <rect x="3" y="3" width="8" height="8" rx="2"/><rect x="13" y="13" width="8" height="8" rx="2"/><path d="M7 11v4a2 2 0 0 0 2 2h4"/><path d="M17 7h-4a2 2 0 0 0-2 2v4"/>
    </svg>
  ),
  barChart: (
    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.75" strokeLinecap="round" strokeLinejoin="round">
      <line x1="12" y1="20" x2="12" y2="10"/><line x1="18" y1="20" x2="18" y2="4"/><line x1="6" y1="20" x2="6" y2="16"/>
    </svg>
  ),
  layers: (
    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.75" strokeLinecap="round" strokeLinejoin="round">
      <path d="m12.83 2.18a2 2 0 0 0-1.66 0L2.6 6.08a1 1 0 0 0 0 1.83l8.58 3.91a2 2 0 0 0 1.66 0l8.58-3.9a1 1 0 0 0 0-1.83Z"/><path d="m22.18 12.09-8.58 3.91a2 2 0 0 1-1.66 0L2.6 12.09"/><path d="m22.18 16.59-8.58 3.91a2 2 0 0 1-1.66 0L2.6 16.59"/>
    </svg>
  ),
  terminal: (
    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.75" strokeLinecap="round" strokeLinejoin="round">
      <polyline points="4 17 10 11 4 5"/><line x1="12" y1="19" x2="20" y2="19"/>
    </svg>
  ),
  server: (
    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.75" strokeLinecap="round" strokeLinejoin="round">
      <rect width="20" height="8" x="2" y="2" rx="2" ry="2"/><rect width="20" height="8" x="2" y="14" rx="2" ry="2"/><line x1="6" x2="6.01" y1="6" y2="6"/><line x1="6" x2="6.01" y1="18" y2="18"/>
    </svg>
  ),
  brain: (
    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.75" strokeLinecap="round" strokeLinejoin="round">
      <path d="M12 5a3 3 0 1 0-5.997.125 4 4 0 0 0-2.526 5.77 4 4 0 0 0 .556 6.588A4 4 0 1 0 12 18Z"/><path d="M12 5a3 3 0 1 1 5.997.125 4 4 0 0 1 2.526 5.77 4 4 0 0 1-.556 6.588A4 4 0 1 1 12 18Z"/><path d="M15 13a4.5 4.5 0 0 1-3-4 4.5 4.5 0 0 1-3 4"/><path d="M12 18v-5.5"/>
    </svg>
  ),
  /* ── Utility icons ── */
  clock: (
    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.75" strokeLinecap="round" strokeLinejoin="round">
      <circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/>
    </svg>
  ),
  bookOpen: (
    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.75" strokeLinecap="round" strokeLinejoin="round">
      <path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"/><path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"/>
    </svg>
  ),
  graduationCapSm: (
    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.75" strokeLinecap="round" strokeLinejoin="round">
      <path d="M22 10v6M2 10l10-5 10 5-10 5z"/><path d="M6 12v5c0 1 4 3 6 3s6-2 6-3v-5"/>
    </svg>
  ),
  layersSm: (
    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.75" strokeLinecap="round" strokeLinejoin="round">
      <path d="m12.83 2.18a2 2 0 0 0-1.66 0L2.6 6.08a1 1 0 0 0 0 1.83l8.58 3.91a2 2 0 0 0 1.66 0l8.58-3.9a1 1 0 0 0 0-1.83Z"/><path d="m22.18 12.09-8.58 3.91a2 2 0 0 1-1.66 0L2.6 12.09"/><path d="m22.18 16.59-8.58 3.91a2 2 0 0 1-1.66 0L2.6 16.59"/>
    </svg>
  ),
  targetSm: (
    <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="var(--accent)" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/>
    </svg>
  ),
  trendUp: (
    <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="var(--accent)" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <polyline points="22 7 13.5 15.5 8.5 10.5 2 17"/><polyline points="16 7 22 7 22 13"/>
    </svg>
  ),
  users: (
    <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="var(--accent)" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/>
    </svg>
  ),
  check: (
    <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round">
      <polyline points="20 6 9 17 4 12"/>
    </svg>
  ),
  checkLg: (
    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round">
      <polyline points="20 6 9 17 4 12"/>
    </svg>
  ),
  checkCircleLg: (
    <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="white" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
      <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/>
    </svg>
  ),
  chevronDown: (
    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="var(--text-muted)" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <polyline points="6 9 12 15 18 9"/>
    </svg>
  ),
  chevronDownSm: (
    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="var(--text-muted)" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <polyline points="6 9 12 15 18 9"/>
    </svg>
  ),
  chevronRight: (
    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <polyline points="9 18 15 12 9 6"/>
    </svg>
  ),
  alertTriangle: (
    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#f57f17" strokeWidth="1.75" strokeLinecap="round" strokeLinejoin="round">
      <path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3Z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/>
    </svg>
  ),
  lightbulb: (
    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="{badge_color}" strokeWidth="1.75" strokeLinecap="round" strokeLinejoin="round">
      <path d="M15 14c.2-1 .7-1.7 1.5-2.5 1-.9 1.5-2.2 1.5-3.5A6 6 0 0 0 6 8c0 1 .2 2.2 1.5 3.5.7.7 1.3 1.5 1.5 2.5"/><path d="M9 18h6"/><path d="M10 22h4"/>
    </svg>
  ),
  circleCheck: (
    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="var(--success)" strokeWidth="1.75" strokeLinecap="round" strokeLinejoin="round">
      <circle cx="12" cy="12" r="10"/><path d="m9 12 2 2 4-4"/>
    </svg>
  ),
  clipboard: (
    <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <rect x="9" y="9" width="13" height="13" rx="2"/><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/>
    </svg>
  ),
  clipboardCheck: (
    <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <polyline points="20 6 9 17 4 12"/>
    </svg>
  ),
  messageCircleQuestion: (
    <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="{badge_color}" strokeWidth="1.75" strokeLinecap="round" strokeLinejoin="round">
      <path d="M7.9 20A9 9 0 1 0 4 16.1L2 22Z"/><path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"/><path d="M12 17h.01"/>
    </svg>
  ),
}};

{step_icons}

/* ───────── DATA ───────── */
{step_data}

/* ───────── COMPONENT: FormattedText ───────── */
function FormattedText({{ value }}: {{ value: string }}) {{
  const elements: React.ReactNode[] = [];
  const lines = value.split("\\n");

  function renderInline(text: string) {{
    const parts: React.ReactNode[] = [];
    const regex = /\\*\\*(.+?)\\*\\*/g;
    let lastIndex = 0;
    let match;
    let k = 0;
    while ((match = regex.exec(text)) !== null) {{
      if (match.index > lastIndex) parts.push(text.slice(lastIndex, match.index));
      parts.push(<strong key={{k++}} className="font-semibold text-[var(--text)]">{{match[1]}}</strong>);
      lastIndex = regex.lastIndex;
    }}
    if (lastIndex < text.length) parts.push(text.slice(lastIndex));
    return parts;
  }}

  let bulletBuf: string[] = [];
  let numBuf: string[] = [];
  let tableBuf: string[][] = [];
  let tableHeader: string[] = [];

  const flushBullets = () => {{
    if (!bulletBuf.length) return;
    elements.push(
      <ul key={{`bl-${{elements.length}}`}} className="my-3 space-y-2 pl-1">
        {{bulletBuf.map((b, i) => (
          <li key={{i}} className="flex items-start gap-2 text-[15px] leading-relaxed">
            <span className="mt-[7px] w-1.5 h-1.5 rounded-full flex-shrink-0" style={{{{ background: "{badge_color}" }}}} />
            <span className="text-justify">{{renderInline(b)}}</span>
          </li>
        ))}}
      </ul>
    );
    bulletBuf = [];
  }};

  const flushNums = () => {{
    if (!numBuf.length) return;
    elements.push(
      <ol key={{`ol-${{elements.length}}`}} className="my-3 space-y-2 pl-1 list-none counter-reset-item">
        {{numBuf.map((n, i) => (
          <li key={{i}} className="flex items-start gap-3 text-[15px] leading-relaxed">
            <span className="font-bold text-sm mt-0.5 flex-shrink-0" style={{{{ color: "{badge_color}" }}}}>{{String(i + 1).padStart(2, "0")}}</span>
            <span className="text-justify">{{renderInline(n)}}</span>
          </li>
        ))}}
      </ol>
    );
    numBuf = [];
  }};

  const flushTable = () => {{
    if (!tableBuf.length) return;
    elements.push(
      <div key={{`tb-${{elements.length}}`}} className="my-4 overflow-x-auto rounded-[var(--radius)] border border-[var(--border)]">
        <table className="w-full text-sm">
          <thead>
            <tr className="bg-[var(--bg-muted)]">
              {{tableHeader.map((h, i) => (
                <th key={{i}} className="px-4 py-2.5 text-left font-bold text-xs uppercase tracking-wider text-[var(--text-muted)]">
                  {{h}}
                </th>
              ))}}
            </tr>
          </thead>
          <tbody>
            {{tableBuf.map((row, ri) => (
              <tr key={{ri}} className={{ri % 2 === 0 ? "" : "bg-[var(--bg-muted)]/50"}}>
                {{row.map((cell, ci) => (
                  <td key={{ci}} className="px-4 py-2.5 text-[var(--text)] border-t border-[var(--border-light)]">
                    {{renderInline(cell)}}
                  </td>
                ))}}
              </tr>
            ))}}
          </tbody>
        </table>
      </div>
    );
    tableBuf = [];
    tableHeader = [];
  }};

  for (let j = 0; j < lines.length; j++) {{
    const line = lines[j];
    const trimmed = line.trim();

    if (!trimmed) {{
      flushBullets();
      flushNums();
      continue;
    }}

    /* Table row */
    if (trimmed.startsWith("|") && trimmed.endsWith("|")) {{
      flushBullets();
      flushNums();
      const cells = trimmed.split("|").filter(Boolean).map((c) => c.trim());
      if (cells.every((c) => /^[-:]+$/.test(c))) {{ j++; continue; }}
      if (!tableHeader.length) {{ tableHeader = cells; }} else {{ tableBuf.push(cells); }}
      continue;
    }} else {{
      flushTable();
    }}

    /* Bullet */
    if (trimmed.startsWith("-- ")) {{
      flushNums();
      flushTable();
      bulletBuf.push(trimmed.slice(3));
      continue;
    }}

    /* Numbered */
    const numMatch = trimmed.match(/^(\\d+)\\.\\s+(.+)/);
    if (numMatch) {{
      flushBullets();
      flushTable();
      numBuf.push(numMatch[2]);
      continue;
    }}

    flushBullets();
    flushNums();
    flushTable();

    /* Sub-heading */
    if (trimmed.endsWith(":") && trimmed.length < 120 && !trimmed.startsWith("--")) {{
      elements.push(
        <h4
          key={{`h-${{j}}`}}
          className="font-bold text-[var(--text)] mt-6 mb-2 pb-2 border-b border-[var(--border-light)] text-base"
        >
          {{trimmed.slice(0, -1)}}
        </h4>
      );
      continue;
    }}

    /* Regular paragraph */
    elements.push(
      <p key={{`p-${{j}}`}} className="mb-3 text-justify leading-[1.75]">
        {{renderInline(trimmed)}}
      </p>
    );
  }}

  flushTable();
  flushBullets();
  flushNums();

  return <div className="text-[var(--text)] text-[15px]">{{elements}}</div>;
}}

/* ───────── COMPONENT: CodeBlock ───────── */
function CodeBlock({{ code, language }}: {{ code: string; language?: string }}) {{
  const [copied, setCopied] = useState(false);
  const copy = () => {{
    navigator.clipboard.writeText(code);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  }};
  return (
    <div className="my-4 rounded-[var(--radius)] overflow-hidden border border-[var(--border)] bg-[#1e1e2e]">
      <div className="flex items-center justify-between px-4 py-2 bg-[#181825] border-b border-[#313244]">
        <span className="text-xs text-[#a6adc8] font-mono">{{language || "code"}}</span>
        <button onClick={{copy}} className="flex items-center gap-1.5 text-xs text-[#a6adc8] hover:text-white transition-colors">
          {{copied ? icons.clipboardCheck : icons.clipboard}}
          {{copied ? "Copiado" : "Copiar"}}
        </button>
      </div>
      <pre className="p-4 overflow-x-auto text-sm leading-relaxed">
        <code className="text-[#cdd6f4] font-mono whitespace-pre">{{code}}</code>
      </pre>
    </div>
  );
}}

/* ───────── COMPONENT: StepCard ───────── */
function StepCard({{
  step,
  index,
  isOpen,
  isCompleted,
  onToggle,
  onComplete,
}}: {{
  step: Step;
  index: number;
  isOpen: boolean;
  isCompleted: boolean;
  onToggle: () => void;
  onComplete: () => void;
}}) {{
  return (
    <div
      id={{step.id}}
      className={{`rounded-[var(--radius-lg)] border transition-all duration-300 ${{
        isOpen
          ? "border-[{badge_color}] shadow-lg"
          : isCompleted
          ? "border-[var(--success)] bg-[var(--success-light)]/30"
          : "border-[var(--border)] hover:border-[{badge_color}]/50"
      }}`}}
    >
      <button
        onClick={{onToggle}}
        className="w-full flex items-center gap-4 p-5 sm:p-6 text-left group"
      >
        <div
          className={{`flex-shrink-0 w-12 h-12 rounded-xl flex items-center justify-center transition-all duration-200 ${{
            isCompleted
              ? "bg-[var(--success)] text-white shadow-[0_2px_8px_rgba(46,132,74,0.3)]"
              : isOpen
              ? "bg-[{badge_color}] text-white shadow-[0_2px_8px_rgba(0,0,0,0.15)]"
              : "bg-[var(--bg-muted)] text-[var(--text-muted)] group-hover:bg-[{badge_color}]/10 group-hover:text-[{badge_color}]"
          }}`}}
        >
          {{isCompleted ? icons.checkLg : (icons[STEP_ICONS[step.id]] || <span className="text-sm font-bold">{{String(index + 1).padStart(2, "0")}}</span>)}}
        </div>
        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-2 mb-1 flex-wrap">
            <h3 className={{`font-bold text-lg ${{isCompleted ? "text-[var(--success)]" : "text-[var(--text)]"}}`}}>
              {{step.title}}
            </h3>
            <span className="text-xs font-medium text-[var(--text-light)] bg-[var(--bg-muted)] px-2 py-0.5 rounded-full">
              {{step.duration}}
            </span>
          </div>
          <p className="text-sm text-[var(--text-muted)] line-clamp-1">{{step.description}}</p>
        </div>
        <span className={{`flex-shrink-0 transition-transform duration-300 ${{isOpen ? "rotate-180" : ""}}`}}>
          {{icons.chevronDown}}
        </span>
      </button>

      {{isOpen && (
        <div className="px-5 sm:px-6 pb-6 border-t border-[var(--border-light)]">
          <div className="pt-5 pl-0 sm:pl-16 space-y-4">
            {{step.content.map((section, i) => {{
              switch (section.type) {{
                case "text":
                  return <FormattedText key={{i}} value={{section.value}} />;
                case "code":
                  return <CodeBlock key={{i}} code={{section.value}} language={{section.language}} />;
                case "warning":
                  return (
                    <div key={{i}} className="flex gap-3 p-4 rounded-[var(--radius)] bg-[#fff8e1] border border-[#ffe082]">
                      <span className="flex-shrink-0 mt-0.5">{{icons.alertTriangle}}</span>
                      <p className="text-sm text-[#5d4037] leading-relaxed text-justify">{{section.value}}</p>
                    </div>
                  );
                case "tip":
                  return (
                    <div key={{i}} className="flex gap-3 p-4 rounded-[var(--radius)] bg-[{badge_color}]/5 border border-[{badge_color}]/20">
                      <span className="flex-shrink-0 mt-0.5">{{icons.lightbulb}}</span>
                      <p className="text-sm text-[var(--text)] leading-relaxed text-justify">{{section.value}}</p>
                    </div>
                  );
                case "checkpoint":
                  return (
                    <div key={{i}} className="flex gap-3 p-4 rounded-[var(--radius)] bg-[var(--success-light)] border border-[var(--success)]/20">
                      <span className="flex-shrink-0 mt-0.5">{{icons.circleCheck}}</span>
                      <div>
                        <span className="text-xs font-bold text-[var(--success)] uppercase tracking-wider block mb-1">Checkpoint</span>
                        <p className="text-sm text-[var(--success)] leading-relaxed">{{section.value}}</p>
                      </div>
                    </div>
                  );
                default:
                  return null;
              }}
            }})}}

            <div className="pt-4 flex items-center gap-3">
              <button
                onClick={{onComplete}}
                className={{`inline-flex items-center gap-2 px-5 py-2.5 rounded-[var(--radius)] font-semibold text-sm transition-all ${{
                  isCompleted
                    ? "bg-[var(--success-light)] text-[var(--success)] border border-[var(--success)]/30"
                    : "bg-[{badge_color}] text-white hover:opacity-90"
                }}`}}
                style={{isCompleted ? {{}} : {{ color: "#fff" }}}}
              >
                {{isCompleted ? (
                  <>
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round"><polyline points="20 6 9 17 4 12"/></svg>
                    Concluido
                  </>
                ) : (
                  <>
                    Marcar como concluido
                    {{icons.chevronRight}}
                  </>
                )}}
              </button>
            </div>
          </div>
        </div>
      )}}
    </div>
  );
}}

/* ───────── MAIN PAGE ───────── */
export default function {func_name}() {{
  const [openStep, setOpenStep] = useState<string | null>("{first_step_id}");
  const {{ completedModules, completeModule, progress }} = useProgress("{meta['course_id']}", "{meta['storage_key']}", STEPS.length);
  const completed = new Set(completedModules);

  const toggleStep = (id: string) => {{
    const newOpen = openStep === id ? null : id;
    setOpenStep(newOpen);
    if (newOpen) {{
      const step = STEPS.find((s) => s.id === newOpen);
      const index = STEPS.findIndex((s) => s.id === newOpen);
      if (step) {{
        localStorage.setItem("last_course_visited", JSON.stringify({{
          courseId: "{meta['course_id']}",
          courseTitle: "{escape_tsx_string(meta['title_display'])}",
          moduleTitle: step.title,
          moduleIndex: index + 1,
          totalModules: STEPS.length,
          timestamp: Date.now(),
        }}));
      }}
    }}
  }};

  const completeStep = (id: string) => {{
    if (completed.has(id)) return;
    completeModule(id);
    const currentIndex = STEPS.findIndex((s) => s.id === id);
    if (currentIndex < STEPS.length - 1) {{
      const nextStep = STEPS[currentIndex + 1];
      setOpenStep(nextStep.id);
      localStorage.setItem("last_course_visited", JSON.stringify({{
        courseId: "{meta['course_id']}",
        courseTitle: "{escape_tsx_string(meta['title_display'])}",
        moduleTitle: nextStep.title,
        moduleIndex: currentIndex + 2,
        totalModules: STEPS.length,
        timestamp: Date.now(),
      }}));
    }}
  }};

  const resetProgress = () => {{
    setOpenStep("{first_step_id}");
    localStorage.removeItem("{meta['storage_key']}");
    window.location.reload();
  }};

  return (
    <>
      <Topbar />
      <Breadcrumbs
        items={{[
          {{ label: "Inicio", href: "/" }},
          {{ label: "Educacao", href: "/educacao" }},
          {{ label: "{escape_tsx_string(meta['title_display'])}" }},
        ]}}
      />

      <main id="main-content">
        {{/* Hero */}}
        <section className="py-16 sm:py-20 px-6 bg-gradient-to-b from-[{badge_color}]/5 via-[{badge_color}]/10 to-white">
          <div className="max-w-[var(--max)] mx-auto">
            <div className="max-w-3xl">
              <span className="inline-block text-xs font-bold uppercase tracking-wider text-[{badge_color}] bg-[{badge_color}]/10 px-3 py-1 rounded-full mb-3">
                {meta['badge_text']}
              </span>
              <h1 className="text-[clamp(28px,4vw,44px)] font-extrabold text-[var(--text)] leading-[1.1] mb-5">
                {meta['title_display']}
              </h1>
              <p className="text-lg text-[var(--text-muted)] leading-relaxed mb-8 max-w-2xl">
                {meta['hero_desc']}
              </p>

              <div className="flex flex-wrap gap-6 text-sm">
                <div className="flex items-center gap-2 text-[var(--text-muted)]">
                  {{icons.clock}}
                  <span>Tempo estimado: {meta['duration']}</span>
                </div>
                <div className="flex items-center gap-2 text-[var(--text-muted)]">
                  {{icons.bookOpen}}
                  <span>{{STEPS.length}} modulos</span>
                </div>
                <div className="flex items-center gap-2 text-[var(--text-muted)]">
                  {{icons.graduationCapSm}}
                  <span>Nivel: {meta['level']}</span>
                </div>
                <div className="flex items-center gap-2 text-[var(--text-muted)]">
                  {{icons.layersSm}}
                  <span>{meta['tags']}</span>
                </div>
              </div>
            </div>
          </div>
        </section>

        {{/* Progress bar */}}
        <div className="sticky top-[57px] z-[5] bg-white/95 backdrop-blur-sm border-b border-[var(--border)]">
          <div className="max-w-[var(--max)] mx-auto px-6 py-3">
            <div className="flex items-center justify-between gap-4">
              <div className="flex items-center gap-3 flex-1">
                <span className="text-sm font-semibold text-[var(--text)] whitespace-nowrap">
                  {{completed.size}}/{{STEPS.length}} concluidos
                </span>
                <div className="flex-1 h-2 bg-[var(--bg-muted)] rounded-full overflow-hidden">
                  <div
                    className="h-full rounded-full transition-all duration-500 ease-out"
                    style={{{{
                      width: `${{progress}}%`,
                      background: progress === 100
                        ? "var(--success)"
                        : "{badge_color}",
                    }}}}
                  />
                </div>
                <span className="text-sm font-bold text-[{badge_color}] whitespace-nowrap">
                  {{progress}}%
                </span>
              </div>
              {{completed.size > 0 && (
                <button
                  onClick={{resetProgress}}
                  className="text-xs text-[var(--text-light)] hover:text-[var(--text)] transition-colors"
                >
                  Resetar
                </button>
              )}}
            </div>
          </div>
        </div>

        {{/* Course sidebar + content */}}
        <section className="py-12 px-6">
          <div className="max-w-[var(--max)] mx-auto">
            <div className="grid grid-cols-1 lg:grid-cols-[280px_1fr] gap-8">
              {{/* Sidebar */}}
              <aside className="hidden lg:block">
                <div className="sticky top-[110px]">
                  <h4 className="font-bold text-[var(--text)] text-sm mb-4 uppercase tracking-wider">
                    Modulos
                  </h4>
                  <nav className="space-y-1">
                    {{STEPS.map((step, i) => (
                      <button
                        key={{step.id}}
                        onClick={{() => {{
                          setOpenStep(step.id);
                          localStorage.setItem("last_course_visited", JSON.stringify({{
                            courseId: "{meta['course_id']}",
                            courseTitle: "{escape_tsx_string(meta['title_display'])}",
                            moduleTitle: step.title,
                            moduleIndex: i + 1,
                            totalModules: STEPS.length,
                            timestamp: Date.now(),
                          }}));
                          document.getElementById(step.id)?.scrollIntoView({{ behavior: "smooth", block: "center" }});
                        }}}}
                        className={{`w-full text-left flex items-center gap-3 px-3 py-2.5 rounded-[var(--radius)] text-sm transition-colors ${{
                          openStep === step.id
                            ? "bg-[{badge_color}]/10 text-[{badge_color}] font-semibold"
                            : completed.has(step.id)
                            ? "text-[var(--success)] hover:bg-[var(--success-light)]"
                            : "text-[var(--text-muted)] hover:bg-[var(--bg-muted)] hover:text-[var(--text)]"
                        }}`}}
                      >
                        <span className={{`flex-shrink-0 w-7 h-7 rounded-lg flex items-center justify-center transition-all ${{
                          completed.has(step.id)
                            ? "bg-[var(--success)] text-white"
                            : openStep === step.id
                            ? "bg-[{badge_color}] text-white"
                            : "bg-[var(--bg-muted)] text-[var(--text-muted)]"
                        }}`}}>
                          {{completed.has(step.id) ? (
                            icons.check
                          ) : (
                            <span className="[&>svg]:w-3.5 [&>svg]:h-3.5">{{icons[STEP_ICONS[step.id]] || String(i + 1).padStart(2, "0")}}</span>
                          )}}
                        </span>
                        <span className="truncate">{{step.title}}</span>
                      </button>
                    ))}}
                  </nav>

                  <div className="mt-8 p-4 rounded-[var(--radius)] bg-[var(--bg-muted)] border border-[var(--border-light)]">
                    <h5 className="font-bold text-sm text-[var(--text)] mb-2">Pre-requisitos</h5>
                    <ul className="text-xs text-[var(--text-muted)] space-y-2">
{chr(10).join(prereq_items)}
                    </ul>
                  </div>
                </div>
              </aside>

              {{/* Steps list */}}
              <div className="space-y-4">
                {{/* Intro card */}}
                <div className="p-6 rounded-[var(--radius-lg)] bg-gradient-to-br from-[{badge_color}]/80 to-[{badge_color}] text-white mb-6">
                  <h2 className="text-xl font-bold mb-3">O que voce vai aprender</h2>
                  <p className="text-sm text-white/80 leading-relaxed mb-4">
                    {meta['intro_text']}
                  </p>
                  <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
{chr(10).join(intro_features)}
                  </div>
                </div>

                {{/* Steps */}}
                {{STEPS.map((step, i) => (
                  <StepCard
                    key={{step.id}}
                    step={{step}}
                    index={{i}}
                    isOpen={{openStep === step.id}}
                    isCompleted={{completed.has(step.id)}}
                    onToggle={{() => toggleStep(step.id)}}
                    onComplete={{() => completeStep(step.id)}}
                  />
                ))}}

                {{/* Completion card */}}
                {{completed.size === STEPS.length && (
                  <div className="p-8 rounded-[var(--radius-lg)] bg-gradient-to-br from-[var(--success-light)] to-white border-2 border-[var(--success)] text-center">
                    <div className="w-16 h-16 mx-auto mb-4 rounded-2xl bg-[var(--success)] flex items-center justify-center shadow-[0_4px_16px_rgba(46,132,74,0.3)]">
                      {{icons.checkCircleLg}}
                    </div>
                    <h2 className="text-2xl font-bold text-[var(--success)] mb-2">Curso concluido com sucesso!</h2>
                    <p className="text-[var(--text-muted)] mb-6 max-w-lg mx-auto">
                      Parabens! {meta['completion_text']}
                    </p>
                    <div className="flex flex-wrap items-center justify-center gap-3">
                      <a href="/educacao" className="sf-btn-primary" style={{{{ color: "#fff" }}}}>
                        Explorar outros cursos
                      </a>
                      <a href="/conteudos" className="sf-btn-outline">
                        Ler artigos tecnicos
                      </a>
                    </div>
                  </div>
                )}}

                {{/* FAQ section */}}
                <div className="mt-12 pt-12 border-t border-[var(--border)]">
                  <div className="flex items-center gap-3 mb-6">
                    <span className="text-[{badge_color}]">{{icons.messageCircleQuestion}}</span>
                    <h2 className="text-2xl font-bold text-[var(--text)]">Perguntas frequentes</h2>
                  </div>
                  <div className="space-y-3">
                    {{[
{','.join(faq_items)}
                    ].map((faq, i) => (
                      <details key={{i}} className="group rounded-[var(--radius)] border border-[var(--border)] overflow-hidden">
                        <summary className="flex items-center justify-between p-4 cursor-pointer hover:bg-[var(--bg-muted)] transition-colors">
                          <span className="font-semibold text-[var(--text)] text-[15px] pr-4">{{faq.q}}</span>
                          <span className="flex-shrink-0 transition-transform group-open:rotate-180">
                            {{icons.chevronDownSm}}
                          </span>
                        </summary>
                        <div className="px-4 pb-4 text-sm text-[var(--text-muted)] leading-relaxed">
                          {{faq.a}}
                        </div>
                      </details>
                    ))}}
                  </div>
                </div>

                {{/* Author section */}}
                <div className="mt-12 p-6 rounded-[var(--radius-lg)] bg-[var(--bg-muted)] border border-[var(--border-light)] flex flex-col sm:flex-row items-start gap-5">
                  <div className="w-14 h-14 rounded-full bg-[{badge_color}] flex items-center justify-center text-white font-bold text-lg flex-shrink-0">
                    AC
                  </div>
                  <div>
                    <h3 className="font-bold text-[var(--text)] mb-1">Alexandre Caramaschi</h3>
                    <p className="text-xs text-[{badge_color}] font-semibold mb-2">
                      CEO da Brasil GEO, ex-CMO da Semantix (Nasdaq), cofundador da AI Brasil
                    </p>
                    <p className="text-sm text-[var(--text-muted)] leading-relaxed">
                      {meta['author_desc']}
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>
      </main>

      <CourseEnhancements
        courseId="{meta['course_id']}"
        courseName="{escape_tsx_string(meta['title_display'])}"
        completedCount={{completed.size}}
        totalModules={{STEPS.length}}
      />
      <Footer />

      {{/* JSON-LD */}}
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{{{
          __html: JSON.stringify({{
            "@context": "https://schema.org",
            "@graph": [
              {{
                "@type": "Course",
                name: "{escape_tsx_string(meta['title_display'])}",
                description: "{escape_tsx_string(meta['description'])}",
                provider: {{
                  "@type": "Organization",
                  name: "Brasil GEO",
                  url: "https://brasilgeo.ai",
                }},
                instructor: {{
                  "@type": "Person",
                  name: "Alexandre Caramaschi",
                  url: "https://alexandrecaramaschi.com",
                  jobTitle: "CEO da Brasil GEO",
                }},
                educationalLevel: "{meta['level']}",
                inLanguage: "pt-BR",
                numberOfCredits: STEPS.length,
                timeRequired: "PT{meta['duration'].replace('~', '').replace(' min', '')}M",
                hasCourseInstance: {{
                  "@type": "CourseInstance",
                  courseMode: "online",
                  courseWorkload: "PT{meta['duration'].replace('~', '').replace(' min', '')}M",
                }},
              }},
              {{
                "@type": "FAQPage",
                mainEntity: [
{(','+chr(10)).join(faq_jsonld)},
                ],
              }},
              {{
                "@type": "BreadcrumbList",
                itemListElement: [
                  {{ "@type": "ListItem", position: 1, name: "Inicio", item: "https://alexandrecaramaschi.com" }},
                  {{ "@type": "ListItem", position: 2, name: "Educacao", item: "https://alexandrecaramaschi.com/educacao" }},
                  {{ "@type": "ListItem", position: 3, name: "{escape_tsx_string(meta['title_display'])}" }},
                ],
              }},
            ],
          }}),
        }}}}
      />
    </>
  );
}}
'''
    return tsx


def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.chdir(base_dir)

    for course_key, meta in COURSES.items():
        print(f"\n{'='*60}")
        print(f"Processing: {course_key}")
        print(f"{'='*60}")

        # Read draft
        draft_file = meta["draft_file"]
        if not os.path.exists(draft_file):
            print(f"  ERROR: Draft file not found: {draft_file}")
            continue

        with open(draft_file, encoding='utf-8') as f:
            data = json.load(f)

        if not data.get("sucesso"):
            print(f"  SKIP: Draft pipeline not successful")
            continue

        draft = data["etapas"].get("draft", "")
        if not draft:
            print(f"  SKIP: No draft content")
            continue

        # Extract modules
        modules = extract_modules_from_draft(draft, meta["modules_count"])
        print(f"  Extracted {len(modules)} modules (target: {meta['modules_count']})")
        for i, (title, content) in enumerate(modules):
            words = len(content.split())
            print(f"    {i+1}. {title} ({words} words)")

        # Generate page.tsx
        tsx_content = generate_page_tsx(course_key, modules)

        # Write to target
        target_dir = meta["target_dir"]
        # Convert /c/ to C:/ for Windows
        if sys.platform == 'win32':
            target_dir_win = target_dir.replace('/c/', 'C:/')
        else:
            target_dir_win = target_dir

        target_file = os.path.join(target_dir_win, "page.tsx")
        os.makedirs(os.path.dirname(target_file), exist_ok=True)

        with open(target_file, 'w', encoding='utf-8') as f:
            f.write(tsx_content)

        line_count = tsx_content.count('\n') + 1
        print(f"  Written: {target_file} ({line_count} lines)")


if __name__ == "__main__":
    main()
