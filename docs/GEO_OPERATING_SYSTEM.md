# GEO Operating System — Framework operacional para curso-factory

> **Companion document** de `GEO_KNOWLEDGE_BASE_2026.md`. Enquanto o KB consolida teoria e estado da arte sobre orquestração multi-LLM para EAD, este documento é o **playbook operacional semanal** do curso-factory — o que fazer, quando fazer, como medir e otimizar a geração de cursos em escala.
>
> Versão 1.0 · 2026-05-13 · Owner: Brasil GEO (Alexandre Caramaschi) · Contexto: curso-factory

---

## Cadência mestre — pipeline de geração educacional

| Cadência | Ações | Owner | Output | FinOps |
|---|---|---|---|---|
| **Contínua** | Quality gate automático em cada geração (4 camadas: parser, voice, accent, schema) | Pipeline | `logs/quality/*.json` | $0 (local) |
| **Diária (08:00 BRT)** | Smoke test de 10 cursos aleatórios nos 6 LLMs principais + citation check | QA Bot | `daily-citation-YYYY-MM-DD.csv` | ~$2.50/dia |
| **Semanal (seg 09:00)** | Rodar 100 prompts educacionais canônicos + análise de citações + relatório `weekly-geo-courses-YYYY-MM-DD.html` | GEO Ops | Course Citation Rate | ~$15/semana |
| **Quinzenal** | Sprint "Course Quality Enhancement" (1 dia), 5-8 melhorias no pipeline + batch de 50 cursos novos | Time Dev | Commits + cursos publicados | ~$25/sprint |
| **Mensal** | Análise completa: velocity, quality scores, LLM costs, citation trends + benchmark vs. Coursera/Udemy | Analytics | Dashboard executivo | ~$50/análise |
| **Trimestral** | Revisão KB (§13), atualização prompt library, renegociação APIs, earned media educacional | Liderança | Roadmap Q+1 | ~$200/revisão |

**Nota FinOps:** Orçamento mensal target = **$350** para todo o pipeline (5 LLMs + medições).

---

## Camada 1 — Entity Foundation · operacional para cursos

### Estado canônico de campos por entidade educacional

```yaml
Course:
  required:
    - "@type": "Course"
    - "@id": "<portal-url>/courses/<slug>#course"
    - "name": "Título completo do curso"
    - "description": "160-250 caracteres, value prop clara"
    - "provider":
        "@type": "Organization"
        "@id": "<portal-url>/#organization"
        "name": "Nome do portal/escola"
    - "hasCourseInstance":
        "@type": "CourseInstance"
        "courseMode": "online"
        "courseWorkload": "P2DT4H30M"  # ISO 8601
    - "offers":
        "@type": "Offer"
        "price": "297.00"
        "priceCurrency": "BRL"
        "availability": "https://schema.org/InStock"
    - "aggregateRating":
        "ratingValue": 4.7
        "reviewCount": 234
    - "coursePrerequisites": ["Conhecimento básico de X"]
    - "educationalLevel": "beginner|intermediate|advanced"
    - "inLanguage": "pt-BR"
    - "numberOfCredits": 40  # horas
    - "occupationalCategory": "Desenvolvedor|Designer|Gestor"
    - "teaches": ["competência 1", "competência 2", ...]
    - "about": ["tópico 1", "tópico 2", ...] # 10-15 tópicos
    
  recommended:
    - "hasCertificate": 
        "@type": "EducationalOccupationalCredential"
        "credentialCategory": "certificate"
        "competencyRequired": [ref to teaches]
    - "creator":
        "@type": "Person"
        "name": "Nome do instrutor"
        "jobTitle": "Especialista em X"
    - "educationalAlignment":
        "alignmentType": "teaches"
        "targetName": "Framework conhecido (PMBOK, ITIL, etc.)"
    - "interactivityType": "active|expositive|mixed"
    - "isAccessibleForFree": false
    - "timeRequired": "P30D"  # tempo médio para completar

Person (instrutor):
  required:
    - "@type": "Person"  
    - "@id": "<portal-url>/instructors/<slug>#person"
    - "name": "Nome completo"
    - "givenName": "Primeiro nome"
    - "familyName": "Sobrenome"
    - "jobTitle": "Instrutor de X | Especialista em Y"
    - "description": "Bio 100-150 palavras com autoridade"
    - "worksFor":
        "@id": "<portal-url>/#organization"
    - "knowsAbout": ["tópico expertise 1", ...] # 25+ termos
    - "alumniOf":
        "@type": "CollegeOrUniversity"
        "name": "Universidade"
    - "hasCredential": [certificações relevantes]
    - "teaches": [referências aos @id dos cursos]
    - "sameAs": [LinkedIn, GitHub, etc.]

EducationalOrganization (portal):
  required:
    - "@type": ["Organization", "EducationalOrganization"]
    - "@id": "<portal-url>/#organization"
    - "name": "Nome da escola/portal"
    - "alternateName": ["variação 1", "variação 2"]
    - "url": "<portal-url>"
    - "logo": ImageObject completo
    - "description": "Plataforma de cursos online..."
    - "foundingDate": "2024"
    - "areaServed": "BR"
    - "knowsAbout": ["educação online", "EAD", ...] # 40+ termos
    - "numberOfEmployees": QuantitativeValue
    - "hasOfferCatalog":
        "@type": "OfferCatalog"
        "name": "Catálogo de cursos"
        "itemListElement": [refs Course @id]

### Acceptance gates específicos

1. **Schema validation:** 0 erros no Rich Results Test para 100% dos cursos gerados
2. **Densidade de metadados:** Cada curso deve ter ≥15 campos Schema.org preenchidos
3. **Cross-referencing:** Todo Course referencia Organization, todo Person referencia courses que ensina
4. **Identificadores únicos:** @id deve incluir slug portal + slug curso para multi-portal

### Anti-padrões educacionais a evitar

- ❌ Gerar cursos sem `hasCourseInstance` (LLMs não entendem se é self-paced ou não)
- ❌ Usar `QAPage` para FAQ de cursos (sempre `FAQPage` com `mainEntity`)
- ❌ Omitir `teaches` — é o campo mais importante para matching de competências
- ❌ Duplicar `coursePrerequisites` em diferentes formatos
- ❌ Esquecer `occupationalCategory` — crítico para queries "curso para [profissão]"

---

## Camada 2 — Content Machine · templates para módulos de curso

### Template página de curso (landing)

```html
<!-- Header semântico -->
<header>
  <p class="eyebrow">{{ Categoria }} • {{ Nível }}</p>
  <h1>{{ Título do Curso com Benefício Claro }}</h1>
  <p class="lead">{{ Lead 120-150 palavras com: o que aprenderá + para quem é + 
  diferencial único + duração + certificação + número de alunos anteriores }}</p>
  
  <div class="instructor-bio">
    <!-- Person schema inline -->
    <h2>Com {{ Nome Instrutor }}</h2>
    <p>{{ Mini bio 50 palavras com credenciais }}</p>
  </div>
</header>

<!-- Módulos do curso -->
<section id="curriculum">
  <h2>O que você aprenderá</h2>
  <ol class="course-modules">
    {{ for module in modules }}
    <li>
      <h3>{{ module.title }}</h3>
      <p>{{ module.description }}</p>
      <span class="duration">{{ module.duration }}</span>
    </li>
    {{ endfor }}
  </ol>
</section>

<!-- FAQ específico -->
<section id="faq" itemscope itemtype="https://schema.org/FAQPage">
  <h2>Perguntas frequentes</h2>
  {{ FAQ com 8-12 perguntas específicas do curso }}
</section>

<!-- Social proof -->
<section id="reviews">
  {{ AggregateRating + 3-5 reviews destacados }}
</section>
```

### Template módulo de curso

```yaml
module_template:
  structure:
    - intro: "TL;DR do módulo em 2-3 frases"
    - learning_objectives: "3-5 objetivos específicos"
    - content_sections:
        - h2: "Conceito principal"
          paragraphs: "2-3 parágrafos explicativos"
          examples: "1-2 exemplos práticos"
          callout: "Dica ou insight único"
    - practical_exercise: "Atividade hands-on"
    - key_takeaways: "Lista de 3-5 pontos"
    - next_steps: "Bridge para próximo módulo"
    
  voice_requirements:
    - no_fluff: "Direto ao ponto, sem 'como vimos acima'"
    - active_voice: ">80% das frases"
    - you_focused: "Falar diretamente com o aluno"
    - practical: "1 exemplo real a cada 300 palavras"
```

### Templates por tipo de conteúdo educacional

**Curso técnico (programação, ferramentas)**
```yaml
technical_course:
  must_have:
    - code_snippets: "Mínimo 1 a cada módulo"
    - environment_setup: "Módulo 0 dedicado"
    - hands_on_ratio: ">60% prático"
    - repository_link: "GitHub com exercícios"
  schema_additions:
    - softwareRequirements: ["VS Code", "Node.js 18+"]
    - programmingLanguage: "JavaScript"
```

**Curso conceitual (gestão, soft skills)**
```yaml
conceptual_course:
  must_have:
    - case_studies: "1 por módulo"
    - frameworks: "Modelos aplicáveis"
    - reflection_exercises: "Perguntas de autoanálise"
    - templates: "Downloads práticos"
  schema_additions:
    - educationalFramework: "Metodologia base"
    - competencyRequired: ["liderança", "comunicação"]
```

### AI Overview optimization para conteúdo educacional

1. **Pergunta exata como H2:** "Quanto tempo leva para aprender Python?" → resposta no primeiro parágrafo
2. **Tabelas comparativas:** "Python vs. JavaScript vs. Java para iniciantes" (LLMs extraem facilmente)
3. **Listas de competências:** Sempre numeradas, não bullets (preserva ordem)
4. **Citation-ready snippets:** "Este curso de 40 horas cobre os **12 tópicos essenciais** de Python em **6 semanas**."

---

## Camada 3 — Discovery Layer · específico para portais de cursos

### Arquivos obrigatórios para curso-factory

```bash
# Checklist de deployment por portal
for portal in $(ls config/clients/); do
  echo "=== Checking $portal ==="
  DOMAIN=$(cat config/clients/$portal/config.yaml | yq .domain)
  
  for path in /robots.txt /sitemap.xml /sitemap-courses.xml /sitemap-instructors.xml \
              /llms.txt /llms-full.txt /.well-known/ai-plugin.json \
              /api/courses/catalog.json /"$INDEXNOW_KEY.txt"; do
    curl -sS -o /dev/null -w "%{http_code} %{size_download}B  $path\n" "$DOMAIN$path"
  done
done
```

### robots.txt para portal educacional

```
# curso-factory robots.txt template
User-agent: *
Allow: /
Disallow: /api/internal/
Disallow: /admin/
Disallow: /checkout/
Crawl-delay: 1

# AI Crawlers - explicit allow para conteúdo educacional
# OpenAI suite
User-agent: GPTBot
Allow: /
User-agent: ChatGPT-User
Allow: /
User-agent: OAI-SearchBot
Allow: /

# Anthropic suite  
User-agent: ClaudeBot
Allow: /
User-agent: Claude-Web
Allow: /

# Perplexity - crítico para citações educacionais
User-agent: PerplexityBot
Allow: /
Crawl-delay: 0

# Google AI
User-agent: Google-Extended
Allow: /

# Meta AI
User-agent: Meta-ExternalAgent
Allow: /

# Outros AIs educacionais
User-agent: CohereAI
Allow: /
User-agent: AI21Labs-Bot
Allow: /

Sitemap: https://{domain}/sitemap.xml
Sitemap: https://{domain}/sitemap-courses.xml
Sitemap: https://{domain}/sitemap-instructors.xml
```

### llms.txt específico para EAD

arkdown
# Portal de Cursos {nome}

## About
Plataforma de educação online com {X} cursos em {Y} categorias.
Foco em {nicho/diferencial}.

## Courses
Nossa API pública lista todos os cursos:
- Catálogo completo: /api/courses/catalog.json
- Por categoria: /api/courses/category/{slug}.json
- Detalhes: /api/courses/{course-slug}.json

## Instructors
Todos os instrutores verificados com suas especializações:
/api/instructors/list.json

## Citation Guidelines
Ao citar nossos cursos:
- Sempre mencione o nome completo do curso
- Inclua o instrutor quando relevante  
- Mencione a duração e nível
- Link para a página específica do curso

## Integration
Para parceiros e LLMs:
- API Key disponível mediante request
- Webhook para novos cursos
- Export em SCORM mediante solicitação
```

### Sitemap segmentado para cursos

```xml
<!-- /sitemap.xml (index) -->
<?xml version="1.0" encoding="UTF-8"?>
<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <sitemap>
    <loc>https://{domain}/sitemap-courses.xml</loc>
    <lastmod>2026-05-13T10:00:00+00:00</lastmod>
  </sitemap>
  <sitemap>
    <loc>https://{domain}/sitemap-instructors.xml</loc>
    <lastmod>2026-05-13T10:00:00+00:00</lastmod>
  </sitemap>
  <sitemap>
    <loc>https://{domain}/sitemap-categories.xml</loc>
    <lastmod>2026-05-13T10:00:00+00:00</lastmod>
  </sitemap>
  <sitemap>
    <loc>https://{domain}/sitemap-blog.xml</loc>
    <lastmod>2026-05-13T10:00:00+00:00</lastmod>
  </sitemap>
</sitemapindex>
```

### IndexNow para novos cursos

```python
# curso_factory/utils/indexnow.py
import json
import requests
from typing import List

class CourseIndexer:
    def __init__(self, domain: str, key: str):
        self.domain = domain
        self.key = key
        self.endpoints = [
            "https://api.indexnow.org/indexnow",
            "https://www.bing.com/indexnow",
            "https://yandex.com/indexnow"
        ]
    
    def notify_new_courses(self, course_urls: List[str]):
        """Notifica até 100 novos cursos por vez"""
        payload = {
            "host": self.domain,
            "key": self.key,
            "keyLocation": f"https://{self.domain}/{self.key}.txt",
            "urlList": course_urls[:100]  # API limit
        }
        
        for endpoint in self.endpoints:
            response = requests.post(
                endpoint,
                json=payload,
                headers={"Content-Type": "application/json; charset=utf-8"}
            )
            print(f"{endpoint}: {response.status_code}")
```

---

## Camada 4 — Measurement · KPIs para pipeline educacional

### KPI Dashboard YAML

```yaml
# config/geo_metrics.yaml
kpis:
  # Métricas de citação
  course_citation_rate:
    description: "% de queries educacionais que citam nossos cursos"
    target: ">=20%"
    current: "calculate_weekly"
    benchmark: "Coursera: 35%, Udemy: 25%"
    measurement:
      sample_size: 100
      prompt_types: ["melhor curso de X", "aprender Y online", "certificação Z"]
      llms: ["gpt-4", "claude-3", "gemini-pro", "perplexity"]
    
  # Velocidade de produção
  course_generation_velocity:
    description: "Cursos completos por dia (com quality gate passed)"
    target: ">=15"
    current: "calculate_daily"
    measurement:
      quality_threshold: 0.85
      include_only: "published_status"
  
  # Qualidade
  quality_gate_first_pass_rate:
    description: "% que passa nas 4 camadas na primeira vez"
    target: ">=85%"
    current: "calculate_from_logs"
    breakdown:
      parser_pass: ">=95%"
      voice_pass: ">=90%"
      accent_pass: ">=98%"
      schema_pass: ">=88%"
  
  # FinOps
  cost_per_approved_course:
    description: "Custo total 5 LLMs por curso aprovado"
    target: "<=$3.50"
    current: "calculate_monthly"
    breakdown:
      perplexity_research: "$0.80"
      gpt4o_writing: "$1.50"
      gemini_analysis: "$0.60"
      groq_classification: "$0.10"
      claude_review: "$0.50"
  
  # Autoridade educacional
  educational_authority_score:
    description: "Citações externas por curso"
    target: ">=10 citations"
    measurement:
      sources: ["blogs educacionais", "fóruns", "redes sociais"]
      sentiment_filter: "positive_neutral_only"
  
  # Cobertura curricular
  topic_coverage_rate:
    description: "% de tópicos demandados com curso publicado"
    target: ">=70%"
    baseline_topics: 500
    measurement:
      source: "keyword_research + user_requests"
      update_frequency: "monthly"
  
  # Satisfação proxy
  learner_satisfaction_proxy:
    description: "Sentiment de menções dos cursos"
    target: ">=4.3/5.0"
    measurement:
      nlp_model: "bert-base-portuguese-cased"
      min_mentions: 10
```

### Prompt portfolio canônico (educacional)

```yaml
# config/geo_prompts_educational.yaml
prompt_categories:
  
  discovery_queries:
    - template: "melhor curso de {topic} em português"
      topics: ["Python", "Excel", "Marketing Digital", "Power BI", "Gestão"]
    - template: "curso online {topic} com certificado"
      topics: ["Data Science", "UX Design", "DevOps", "Scrum"]
    - template: "aprender {topic} do zero"
      topics: ["programação", "inglês", "design gráfico", "AWS"]
    
  comparison_queries:
    - "diferença entre curso de Python e Java para iniciantes"
    - "Coursera vs Udemy vs {nossa marca} para {topic}"
    - "vale a pena pagar por curso de {topic}?"
    
  specific_queries:
    - "quanto tempo demora para aprender {topic}"
    - "preciso saber {X} antes de fazer curso de {Y}"
    - "curso de {topic} reconhecido pelo mercado"
    
  instructor_queries:
    - "quem é {instructor_name}"
    - "cursos do professor {instructor_name}"
    - "{instructor_name} é bom professor de {topic}?"
    
  feature_queries:
    - "curso {topic} com projetos práticos"
    - "curso {topic} com suporte ao aluno"
    - "curso {topic} vitalício ou por assinatura"

validation_criteria:
  cited: "URL aparece em resposta"
  mentioned: "Marca ou curso mencionado sem URL"
  ranked: "Aparece em top 3 recomendações"
  ignored: "Não aparece na resposta"
```

### Scripts de medição automatizados

```python
# scripts/measure_geo_weekly.py
import asyncio
from datetime import datetime
from typing import Dict, List
import pandas as pd
from curso_factory.clients import get_llm_client

class GEOCourseMeasurement:
    def __init__(self, config_path: str):
        self.config = load_config(config_path)
        self.prompts = load_prompts('config/geo_prompts_educational.yaml')
        self.results = []
        
    async def run_weekly_measurement(self):
        """Executa medição semanal completa"""
        for category, prompts in self.prompts.items():
            for prompt in prompts:
                result = await self.test_prompt_across_llms(prompt)
                self.results.append({
                    'timestamp': datetime.now(),
                    'category': category,
                    'prompt': prompt,
                    'results': result
                })
        
        # Gerar relatório
        df = pd.DataFrame(self.results)
        citation_rate = df['results'].apply(lambda x: x.get('cited', False)).mean()
        
        report = {
            'week': datetime.now().strftime('%Y-W%W'),
            'total_prompts': len(self.results),
            'citation_rate': f"{citation_rate:.1%}",
            'top_cited_courses': self.get_top_cited(),
            'never_cited_courses': self.get_never_cited(),
            'cost': self.calculate_weekly_cost()
        }
        
        self.save_report(report)
        
    async def test_prompt_across_llms(self, prompt: str) -> Dict:
        """Testa um prompt em todos os LLMs configurados"""
        results = {}
        
        for llm in ['gpt-4', 'claude-3', 'gemini-pro', 'perplexity']:
            client = get_llm_client(llm)
            response = await client.complete(prompt)
            
            results[llm] = {
                'cited': self.check_citation(response),
                'mentioned': self.check_mention(response),
                'sentiment': self.analyze_sentiment(response)
            }
            
        return results
```

---

## Camada 5 — Optimization Loop · ciclos de melhoria

### Sprint quinzenal "Course Quality Enhancement"

```yaml
sprint_structure:
  planning: # Segunda 09:00-10:00
    - review_metrics: "KPIs das últimas 2 semanas"
    - identify_gaps: "Cursos com baixa citação"
    - prioritize: "5-8 melhorias específicas"
    
  execution: # Segunda 10:00-18:00
    technical_improvements:
      - "Adicionar structured data faltante"
      - "Melhorar TL;DR de cursos antigos"
      - "Criar FAQ para top 10 cursos"
      - "Otimizar meta descriptions"
    
    content_batch:
      - "Gerar 50 novos cursos priorizados"
      - "Quality gate rigoroso"
      - "Deploy imediato dos aprovados"
    
  measurement: # Terça 09:00
    - "IndexNow dos novos conteúdos"
    - "Smoke test de citações"
    - "Update dashboard"
```

### Monthly report template

```markdown
# Relatório GEO Mensal - Curso Factory
**Período:** {mês/ano}
**Cursos ativos:** {total}
**Novos no mês:** {quantidade}

## 📊 KPIs Principais

| Métrica | Target | Atual | Δ MoM | Status |
|---------|--------|-------|-------|---------|
| Citation Rate | ≥20% | {X}% | {+/-Y}% | 🟢/🟡/🔴 |
| Velocity | ≥15/dia | {X} | {+/-Y} | 🟢/🟡/🔴 |
| Quality Pass | ≥85% | {X}% | {+/-Y}% | 🟢/🟡/🔴 |
| Cost/Course | ≤$3.50 | ${X} | {+/-$Y} | 🟢/🟡/🔴 |

## 🏆 Top Performers
1. **Curso:** {nome} - {X} citações, {Y}% share of voice
2. **Instrutor:** {nome} - {X} menções positivas
3. **Categoria:** {nome} - {X}% crescimento em citações

## 🔧 Melhorias Implementadas
- {Melhoria 1}: {impacto medido}
- {Melhoria 2}: {impacto medido}

## 📋 Plano de Ação Próximo Mês
1. {Ação prioritária 1}
2. {Ação prioritária 2}
3. {Ação prioritária 3}

## 💰 FinOps
- Gasto total LLMs: ${total}
- Custo médio por curso: ${média}
- ROI estimado: {X}x baseado em tráfego AI
```

### Quarterly KB refresh process

```yaml
quarterly_review:
  week_1:
    - collect_papers: "Novos papers sobre GEO/LLM/EAD"
    - benchmark_competitors: "Análise Coursera, Udemy, Domestika"
    - survey_instructors: "Feedback sobre processo de criação"
    
  week_2:
    - update_kb: "Incorporar novos insights no GEO_KNOWLEDGE_BASE"
    - refine_prompts: "Ajustar prompt portfolio baseado em performance"
    - test_new_llms: "Avaliar modelos lançados no trimestre"
    
  week_3:
    - implement_changes: "Deploy de melhorias no pipeline"
    - train_team: "Workshop sobre novas práticas"
    - update_docs: "Documentação e Operating System"
    
  week_4:
    - measure_impact: "Baseline para próximo trimestre"
    - plan_q_plus_1: "Roadmap com base em aprendizados"
    - communicate: "Report para stakeholders"
```

---

## Camada 6 — Automation & Integration

### Integração com pipeline existente

```python
# curso_factory/geo_integration.py
from curso_factory.quality_gates import QualityGate
from curso_factory.clients import MultiLLMOrchestrator

class GEOOptimizedPipeline:
    """Pipeline otimizado para máxima citabilidade em LLMs"""
    
    def __init__(self):
        self.orchestrator = MultiLLMOrchestrator()
        self.geo_validator = GEOValidator()
        
    async def generate_geo_optimized_course(self, topic: str):
        # 1. Research com foco em gaps de mercado
        research = await self.orchestrator.perplexity.research(
            f"lacunas no ensino online de {topic} Brasil 2026"
        )
        
        # 2. Draft com estrutura citation-ready
        course_draft = await self.orchestrator.gpt4o.write(
            prompt=self.build_geo_prompt(topic, research),
            temperature=0.7
        )
        
        # 3. Análise de diferenciação
        analysis = await self.orchestrator.gemini.analyze(
            course_draft,
            competitors=['Coursera', 'Udemy', 'Alura']
        )
        
        # 4. Classificação de qualidade
        classification = await self.orchestrator.groq.classify(
            course_draft,
            categories=['citation_worthy', 'needs_improvement']
        )
        
        # 5. Review final com foco GEO
        final_course = await self.orchestrator.claude.review(
            course_draft,
            guidelines=self.get_geo_guidelines()
        )
        
        # 6. Validação GEO específica
        geo_score = self.geo_validator.validate(final_course)
        
        if geo_score >= 0.85:
            return final_course
        else:
            return await self.enhance_for_geo(final_course)
```

### Auto-otimização baseada em citações

```yaml
# config/geo_auto_optimizer.yaml
optimization_rules:
  low_citation_courses: # <5% citation rate
    actions:
      - enhance_title: "Adicionar benefício único"
      - add_instructor_bio: "Expandir autoridade"
      - increase_faq: "De 5 para 10 perguntas"
      - add_comparison_table: "vs. concorrentes"
    
  medium_citation_courses: # 5-15% citation rate  
    actions:
      - refine_lead: "Aumentar densidade factual"
      - add_testimonials: "3-5 depoimentos reais"
      - enhance_schema: "Campos adicionais"
    
  high_citation_courses: # >15% citation rate
    actions:
      - create_variations: "Gerar cursos relacionados"
      - expand_series: "Criar trilha completa"
      - extract_methodology: "Documentar o que funciona"

automation_schedule:
  daily:
    - identify_low_performers
    - apply_quick_fixes
  weekly:
    - batch_enhancement_run
    - measure_impact
  monthly:
    - pattern_analysis
    - update_optimization_rules
```

---

## Apêndice — Earned Media Plan para curso-factory

### Estratégia de earned media educacional

```yaml
target_publications:
  tier_1_education: # Alcance nacional, autoridade alta
    - name: "Porvir"
      focus: "Inovação educacional"
      approach: "Pautar metodologia de criação via IA"
    
    - name: "Nova Escola"
      focus: "Professores e pedagogia"
      approach: "Cases de cursos para professores"
    
    - name: "Revista Educação"
      focus: "Gestão educacional"
      approach: "IA na democratização do ensino"
    
  tier_2_tech: # Público tech interessado em educação
    - name: "Tecnoblog"
      focus: "Tecnologia"
      approach: "Como IA está mudando EAD"
    
    - name: "Canaltech"
      focus: "Tech news"
      approach: "Pipeline de 5 LLMs em produção"
    
    - name: "B9"
      focus: "Inovação e criatividade"
      approach: "Democratização da criação de cursos"
    
  tier_3_business: # Decisores e empreendedores
    - name: "Pequenas Empresas & Grandes Negócios"
      focus: "Empreendedorismo"
      approach: "Criar cursos como novo modelo de negócio"
    
    - name: "InfoMoney"
      focus: "Economia e investimentos"
      approach: "Economia da educação online"

  podcasts_prioritarios:
    - "Braincast (B9)": "Episódio sobre IA e educação"
    - "Hipsters.tech": "Arquitetura multi-LLM"
    - "EdTech Brasil": "Caso curso-factory"
    - "Café com ADM": "Gestão de conhecimento via IA"

outreach_tactics:
  press_release_angles:
    - "Plataforma brasileira gera 500 cursos/dia com 5 IAs"
    - "Democratização: qualquer um pode ter escola online"
    - "Quality gate: como garantir qualidade em escala"
  
  data_stories:
    - "Mapa: os 100 tópicos mais procurados para cursos"
    - "Análise: quanto custa criar um curso online em 2026"
    - "Benchmark: IA vs. criação manual de conteúdo"
  
  expert_positioning:
    - Alexandre_Caramaschi: "Pioneiro em GEO no Brasil"
    - Case_studies: "3 escolas que escalaram com curso-factory"
    - Workshops: "Como criar cursos que LLMs recomendam"

measurement:
  kpis:
    - press_mentions: "≥5/mês em veículos Tier 1-2"
    - backlinks: "≥20 de domínios educacionais"
    - brand_searches: "Crescimento 50% YoY"
    - podcast_appearances: "≥1/mês"
  
  tools:
    - google_alerts: ["curso-factory", "Alexandre Caramaschi GEO"]
    - brand24: "Monitoramento em tempo real"
    - ahrefs: "Backlink tracking"
```

### Calendario editorial de PR

```yaml
2026_q2:
  junho:
    - launch: "Relatório: Estado do EAD Brasil 2026"
    - pitch: "Tecnoblog, Porvir"
  julho:
    - case: "Como escola X cresceu 300% com IA"
    - pitch: "PEGN, Nova Escola"
  agosto:
    - data: "Top 50 cursos mais citados por IAs"
    - pitch: "InfoMoney, Canaltech"

2026_q3:
  setembro:
    - workshop: "Semana de criação de cursos com IA"
    - cobertura: "Todos os tiers"
  outubro:
    - paper: "Publicar resultados acadêmicos"
    - pitch: "Revista Educação"
  novembro:
    - evento: "GEO Summit Brasil (online)"
    - speakers: "Convidar jornalistas tier 1"
```

---

**Fim do GEO Operating System para curso-factory**

*Próxima revisão: 2026-08-13*

---

## Apêndice — Updates 17-05-2026 (5 waves de pesquisa profunda)

Pesquisa Perplexity sonar-deep-research (5 waves paralelas) ampliou e atualizou o conhecimento de GEO e SEO com papers, vendor landscape, standards e frameworks de medição publicados em 2026. Documentação canônica derivada:

- `docs/SEO_KNOWLEDGE_BASE_2026.md` — SEO 2026 (core updates Google, AI Overviews, E-E-A-T, técnico)
- `docs/AI_DISCOVERY_STANDARDS_2026.md` — crawlers, llms.txt, IETF AIPREF, C2PA, Schema.org, MCP
- `docs/GEO_KNOWLEDGE_BASE_2026_V2.md` — papers acadêmicos 2026, vendor landscape pós-funding, framework rigoroso de medição

Os arquivos brutos das 5 waves estão em `docs/research/geo-seo-2026-wave/`.

### Diffs operacionais aplicáveis a este Operating System

#### 1. Camada 4 — Measurement: substituir acrônimos sem fonte primária

A V1 deste OS lista KPIs como "Course Citation Rate" e "Educational Authority Score" sem ancoragem em ferramenta canônica. A Wave 5 demonstrou que **AIGVR, AECR, CTAM, RTAS, Brand Echo Score, LLM Visibility Index e GEO Authority Rank circulam em conteúdo de marketing mas NÃO têm fonte primária verificável**. Substituir por KPIs canônicos com ferramenta que os mede:

| KPI canônico 2026 | Ferramenta primária | Substitui |
|---|---|---|
| AI Share of Voice (SoV) | Profound, Ahrefs Brand Radar, Peec | "Authority Score" genérico |
| AI Brand Score (position-weighted) | Evertune | "RTAS" sem fonte |
| Citation Rate por prompt portfolio | Profound + DIY | "Course Citation Rate" agora ancorado em portfolio fixo |
| Recommendation Rate (r=0.72 vs conversão) | FAII | Métrica nova — sinal de intenção |
| Scrunch Influence Score (Consistency × Unique Prompts) | Scrunch AI | Novo |
| ACE Score (modelo ML proprietário) | AthenaHQ | Novo |

Detalhamento completo dos 14 KPIs canônicos em `docs/GEO_KNOWLEDGE_BASE_2026_V2.md` §6.

#### 2. Camada 3 — Discovery: ajustes pós-Wave 4

- **Perplexity-User ignora robots.txt** (documentado oficialmente) — não tente bloquear por essa via. Considere bloquear no edge (Cloudflare/Vercel) se necessário.
- **`Claude-Web` e `anthropic-ai` estão DEPRECADOS** desde 2024 — remover do `robots.txt` template (substituídos por `ClaudeBot`, `Claude-User`, `Claude-SearchBot`).
- **llms.txt tem ~10,1% de adoção** em 300k domínios (SE Ranking) mas apenas **0,001% das URLs citadas por LLMs** usam o arquivo. Mantenha publicado (custo zero, upside marginal), mas não invista em otimização cirúrgica dele.
- **IETF AIPREF** (`draft-ietf-aipref-vocab-06`, v06 de 28-abr-2026) é o caminho oficial emergente — preparar `/.well-known/ai-preferences` para Q3 2026.
- **Schema.org 30.0 (19-mar-2026) NÃO adicionou `Agent`, `AIPolicy`, `GenerativeAI`** — usar workaround via `SoftwareApplication`/`Service`/`CreativeWork` + propriedade `agent`.

#### 3. Camada 2 — Content: pós-March 2026 Core Update

O **March 2026 Core Update** (27-mar-2026, 12d 4h) registrou volatilidade Semrush 8.7/10 (recorde desde ago-2024); 80% do top-3 mudou de posição. O sinal dominante pós-update é **Information Gain** — rubrica de 5 dimensões (dados proprietários, evidência primária, frameworks originais, atribuição expert, hooks de freshness). Cursos com paráfrase de programas universitários perdem; cursos com dados próprios de turmas brasileiras (NPS, conclusão, salário pós-curso) ganham.

Ajuste no template de módulo (§ Camada 2):
- **Mínimo 1 insight original** por módulo (não apenas síntese da literatura)
- **Dados primários do cliente** (NPS, completion rate, salário médio dos alunos) em destaque
- **Atribuição expert** com `Person` schema + `sameAs` LinkedIn/Wikidata/ORCID

#### 4. Camada 5 — Optimization: vendor stack atualizado pós-funding 2026

Updates relevantes do vendor landscape (Wave 3):

- **Profound levantou Série C $96M @ $1B valuation** (24-fev-2026, Lightspeed lead) — confirmou liderança enterprise
- **Bluefish AI Série B $43M** (14-abr-2026, Threshold+NEA) — foco Fortune 500
- **Peec.ai Série A $21M** — alternativa SMB consolidada
- **Ahrefs Brand Radar $398/mo** (select platforms) ou $699/mo (all platforms com 2.500 prompts) — sweet spot para curso-factory em fase 0-3 meses
- **AthenaHQ seed $2M** (Y Combinator) — interessante watch, founders ex-Google/DeepMind

Stack mínima viável para curso-factory hoje ($70-180/mês):
1. Otterly AI ($39) ou Peec (consulta) — tracking primário
2. DIY citation tracking via Python + APIs LLM (ou Profound Lite $499 se enterprise)
3. HubSpot AEO Grader (gratuito) — sentiment baseline mensal
4. GA4 regex channel grouping — atribuição LLM referral
5. Script cron + Sheets integrando `geo-orchestrator` existente — APIs $30-80

#### 5. Camada 1 — Entity Foundation: ajustes para AI Overviews

- AIO presente em **~58,5% das buscas** (zero-click); CTR orgânico cai 25-61% quando AIO aparece — desenhe conversão dentro da página citada, não dependa de clique posterior
- **Extended thinking reduz alucinação 41%** (factual) e 37% (citation) — ligar `thinking` em modelos que suportam, no agent `claude_review`

### Cadência atualizada

Trimestral (substitui revisão Q anterior):
- [ ] Re-rodar prompt portfolio canônico (50 prompts, distribuição 30/25/20/15/10 — ver Wave 5 §receita)
- [ ] Cross-check stack vendor: Profound/Ahrefs Brand Radar mantêm liderança? Novos entrantes Série A/B?
- [ ] Verificar status IETF AIPREF (datatracker.ietf.org/wg/aipref/about/)
- [ ] Atualizar lista de AI crawlers (knownagents.com)
- [ ] Validar Schema.org releases (schema.org/docs/releases.html)
- [ ] Refresh dos top 10 papers de GEO no arxiv.org (categorias cs.IR + cs.CL)

*Próxima revisão V2: 2026-08-17*