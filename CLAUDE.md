# curso-factory — Instruções Claude Code

## REGRA #0 — IDIOMA

Todo conteúdo gerado pelo orquestrador em PT-BR com acentuação completa. Exceção: código, commits, docstrings, identifiers técnicos.

## REGRA #1 — Contexto enriquecido GEO/SEO 2026 (mandatório)

Em **toda** decisão de arquitetura do orquestrador, escolha de prompts por agente (Perplexity research, GPT-4o writer, Gemini analyzer, Groq classifier, Claude reviewer), quality gate, FinOps por LLM, ou design de pipeline para novo segmento: ler primeiro os 4 documentos canônicos abaixo, na ordem.

**Spine didática (taxonomia canônica de aula):**
- [`docs/GEO_50_CONCEITOS_CANONICAL.md`](docs/GEO_50_CONCEITOS_CANONICAL.md) — V1, 17-05-2026. **Referência obrigatória ao planejar nova trilha de GEO/SEO em qualquer vertical** (joalheria, fintech, jurídico, saúde, educação). Cada um dos 50 conceitos é candidato a virar 1 aula HBR-grade; verticais reaproveitam a mesma taxonomia adaptando exemplos. Em criação de aula, os conceitos **4, 5, 6, 7, 8** são base (estrutura editorial — title, meta, H1, H2/H3, conteúdo visível) e **11, 12, 24, 25** são GEO-core (answer capsules, FAQ visível, citabilidade GEO, recuperabilidade generativa). Aulas com tema cruzando o **conceito 26 (pseudo-GEO)** viram automaticamente aula de "anti-padrão a evitar", nunca aula prescritiva de "como conseguir citação garantida". O documento traz a tabela síntese de mapeamento por uso (auditoria técnica, conteúdo, GEO/AISO, local, autoridade, conversão, governança, priorização) e a lista de anti-padrões proibidos da Brasil GEO.

**Camada teoria (KB):**
- [`docs/GEO_KNOWLEDGE_BASE_2026.md`](docs/GEO_KNOWLEDGE_BASE_2026.md) — V1, 13-05-2026. Estado da arte 2025-2026 adaptado a EAD: papers fundadores (Aggarwal 2023, Chen 2025), KPIs base, framework operacional 5 camadas, vendor stack inicial. **§11 é a aplicação específica deste repo.**
- [`docs/GEO_KNOWLEDGE_BASE_2026_V2.md`](docs/GEO_KNOWLEDGE_BASE_2026_V2.md) — V2, 17-05-2026 (delta). 10 papers acadêmicos publicados em 2026 verificados via arxiv.org (VMAO arXiv:2603.11445, ReaLM-Retrieve arXiv:2604.26649, AIO measurement arXiv:2605.14021 etc), vendor landscape pós-funding Q1/Q2 2026 (Profound Série C $96M @ $1B, Bluefish $43M, Peec $21M), framework de 14 KPIs canônicos com fonte primária + **alerta crítico: AIGVR/AECR/CTAM/RTAS/Brand Echo NÃO têm fonte primária verificável, não usar**.
- [`docs/SEO_KNOWLEDGE_BASE_2026.md`](docs/SEO_KNOWLEDGE_BASE_2026.md) — novo, 17-05-2026. Updates do Google 2026 (March 2026 Core Update com volatilidade Semrush 8.7/10, February 2026 Discover Update, March 2026 Spam Update), AI Overviews evolução (expansão para 100 idiomas, ads dentro de AIO, opt-out 19-mar-2026, litígios Penske/Leovy/CE antitrust), E-E-A-T 2026 (Author Entity, Experience como diferenciador, Disconnected Entity Hypothesis), técnico (Core Web Vitals composite, Information Gain, MUVERA, hreflang). 80 fontes validadas.
- [`docs/AI_DISCOVERY_STANDARDS_2026.md`](docs/AI_DISCOVERY_STANDARDS_2026.md) — novo, 17-05-2026. Catálogo canônico de 45+ AI crawlers (ClaudeBot, Perplexity-User que ignora robots.txt, Google-Extended etc), status real llms.txt em 2026 (10,1% adoção mas 0,001% das citações LLM), IETF AIPREF (`draft-ietf-aipref-vocab-06`), C2PA spec 2.3, Schema.org 30.0 (não adicionou `Agent`/`AIPolicy`/`GenerativeAI`), MCP ecosystem (registry oficial 6.8k stars, 7.700 servers em marketplaces). Templates prontos de robots.txt, llms.txt, llms-full.txt, JSON-LD Course.

**Camada operação (OS):**
- [`docs/GEO_OPERATING_SYSTEM.md`](docs/GEO_OPERATING_SYSTEM.md) — playbook semanal completo. **Apêndice 17-05-2026** documenta os diffs operacionais derivados das 5 waves (KPIs canônicos substituindo acrônimos sem fonte, vendor stack atualizado, ajustes pós-March 2026 Core Update, removal de `Claude-Web`/`anthropic-ai` deprecados, preparação `/.well-known/ai-preferences` para Q3 2026).

**Incremento canônico pós Google I/O 2026:**
- [`docs/SEO_GEO_INCREMENT_20260520.md`](docs/SEO_GEO_INCREMENT_20260520.md) — novo, 20-05-2026. Síntese executável de 3 documentos canônicos sobre SEO+GEO+AEO+B2A pós Google I/O 2026 (15-mai-2026). Inclui: (a) **Master Prompt 5 Ondas** unificado e executável para auditoria de portal editorial (Fundação técnica → Arquitetura/Entidade → Conteúdo/Information Gain → Citabilidade/Schema → Autoridade/B2A); (b) **Stack técnico de 38 camadas** com 570+ itens mapeados por onda; (c) **Princeton GEO playbook** com lifts mensurados (Cite Sources +115%, Statistics +41%, Quotation +28% — Aggarwal et al. KDD 2024 arXiv:2311.09735); (d) **Two-Phase JSON-LD theory** que resolve o debate Ahrefs (upstream Knowledge Graph lê schema; runtime RAG lê apenas HTML visível); (e) **Entity Boundary Drift** com cosine similarity ≥0,95 entre canais; (f) **8 Query Fan-Out variant types** de Michael King (iPullRank); (g) **Camada ASO** (Agentic Search Optimization) e roadmap B2A com NLWeb/MCP/OpenAPI (Gartner 2026: 90% B2B intermediado por agentes em 2028, $15T); (h) **Catálogo de bots IA atualizado mai/2026** incluindo OAI-AdsBot novo, Pay-Per-Crawl HTTP 402 da Cloudflare, crawl-to-referral ratios benchmarks; (i) **Anti-padrões 2026** (llms.txt como requisito = falso pelo Google AI Optimization Guide; schema como silver bullet = falso pelo estudo Ahrefs; FAQ rich results descontinuados 7-mai-2026). Templates prontos em [`docs/templates/seo-geo-2026/`](docs/templates/seo-geo-2026/): `robots-2026.txt` (20+ user-agents), `news-article-schema.jsonld` (@graph aninhado com Wikidata), `paywall-schema.jsonld` (regras Google 2026), `breadcrumb-schema.jsonld`, `llms.txt.template` (defensivo, não obrigatório). Fontes preservadas em [`docs/research/seogeo-20260520/`](docs/research/seogeo-20260520/). **Quando usar:** auditar portal editorial cliente, criar curso "GEO/SEO 2026", ajustar prompt do `writer.py` com Princeton checklist obrigatória (Cite Sources ≥3, Stats ≥5, Quotes ≥1).

**Pesquisa bruta:**
- [`docs/research/geo-knowledge-2026/`](docs/research/geo-knowledge-2026/) — Perplexity sonar-pro de 13-05-2026.
- [`docs/research/geo-seo-2026-wave/`](docs/research/geo-seo-2026-wave/) — 5 waves Perplexity sonar-deep-research de 17-05-2026 (papers 2026, SEO updates, vendor landscape, discovery standards, measurement frameworks), com WebFetch validation em ~50 URLs primárias.
- [`docs/research/geo-q2-2026/`](docs/research/geo-q2-2026/) — **incremento canônico 17-05-2026 (noite)** com 4 artefatos:
  - `GEO_KNOWLEDGE_2026_Q2_INCREMENT.md` — doc canônico específico para curso-factory (mudanças metodológicas Q1-Q2 2026, novos módulos de curso a produzir, KPIs canônicos para EAD, 7 artefatos educacionais). Gerado por Claude Opus 4.7 sobre síntese Gemini 2.5 Pro de 5 sonar-pro + 5 sonar-deep + 1 GPT-4o web_search.
  - `SYNTHESIS_STATE_OF_ART_2026.md` — síntese geral (8 seções, papers AgenticGEO/AdaptOrch/MoA/DAAO, vendor stack, Citation Drift Profound, lançamentos LLM Q1-Q2).
  - `CITATIONS_POOL.md` — **325 URLs verificáveis** consolidados.
  - `raw/` — 10 JSONs originais das waves para auditoria.

**Wave Maio 2026 Pós-IO (24-05-2026)** — adiciona aos anteriores sem substituir:
- [`docs/research/geo-wave-maio-posio-2026/WAVE_MAIO_2026_POSIO_CANONICAL.md`](docs/research/geo-wave-maio-posio-2026/WAVE_MAIO_2026_POSIO_CANONICAL.md) — **doc canônico de 511 linhas** cobrindo delta 17-mai → 24-mai-2026 com foco didático: (a) Google I/O 2026 (Gemini 3.5 Flash default em AI Mode 1B MAU, AIO+AI Mode unificados) e Google Marketing Live 2026 (AI Mode Ads, Ask Advisor, AP2/UCP/Universal Cart) — vira 2 aulas do módulo novo "GEO/SEO 2026 Pós-IO"; (b) **AutoGEO ICLR'26** (Wu/Zhong/Kim/Xiong CMU, +50,99% lift) — vira aula obrigatória + bloco no prompt do `writer.py` (Cite Sources ≥3 + AutoGEO 5 regras); (c) Coluna Diogo Cortiz UOL 24-mai (Dilema da Inovação aplicado ao Google) — framing executivo para abertura do curso; (d) 6 novos arXiv IDs (Citation Absorption Rate, 7 failure types, Semantic Entropy Drift, LLM2Vec-Gen, limites teóricos embeddings) — viram conteúdo de aulas avançadas; (e) glossário 2026 (CAR, CSR, Citation Drift, Owned Content Share 4,3%, Failure Type, Semantic Entropy Drift); (f) 3 camadas canônicas de KPI (Visibilidade → Infraestrutura → Negócio) — vira spine de 3 aulas; (g) **Perplexity Comet + ChatGPT Atlas** agentic-browsers — vira módulo novo "Agentic Browsers: nova superfície de descoberta"; (h) anti-padrões reforçados (Cortiz: olhar para tecnologia esquecendo comportamento); (i) `client.yaml` schema expandido com bloco `geo_2026_pos_io.{autogeo_enabled, citation_absorption_tracking, ai_mode_ads_module_included, cortiz_framing_in_intro}`; (j) **24 URLs verificáveis** adicionais. Inclui apêndice §10 com achados complementares do orchestrator 5 LLMs (raw em [`raw/orchestrator_5llm_20260524_213700.json`](docs/research/geo-wave-maio-posio-2026/raw/orchestrator_5llm_20260524_213700.json)). **§6.3 é a aplicação específica deste repo** (4 entregáveis 60 dias, métrica de sucesso: primeiro cliente externo compra módulo "GEO/SEO 2026 Pós-IO" como módulo opcional em portal próprio até 23-jul-2026).

**Complementa** (não substitui) `docs/knowledge/geo-aeo/` — corpus de 30 instruções operacionais + 25 papers da onda 2026-04-25.

Citar `§X.Y` dos KBs/INCREMENT/WAVE ao tomar decisões. Atualizar trimestralmente (próxima: agosto/2026).

## 2026-05-20 — Incremento canônico pós Google I/O 2026 (SEO+GEO+AEO+B2A)

Adicionado em `docs/SEO_GEO_INCREMENT_20260520.md` o material consolidado de 3 fontes canônicas datadas mai/2026 sobre o estado da arte SEO+GEO+AEO+B2A pós Google I/O 2026 (15-mai-2026). **Não substitui** os 5 docs canônicos existentes (`GEO_KNOWLEDGE_BASE_2026.md`, `_V2`, `SEO_KNOWLEDGE_BASE_2026.md`, `AI_DISCOVERY_STANDARDS_2026.md`, `GEO_50_CONCEITOS_CANONICAL.md`) — **complementa** com camada operacional: Master Prompt 5 Ondas executável, 38 camadas técnicas mapeadas, Princeton GEO playbook (lifts mensurados), Two-Phase JSON-LD theory, Entity Boundary Drift, 8 Query Fan-Out variant types de King, ASO/B2A com NLWeb+MCP, anti-padrões 2026 e templates prontos (robots.txt, JSON-LD, llms.txt).

**Como aplicar no pipeline:**
- `writer.py` (GPT-4o): incluir Princeton checklist obrigatória em módulos GEO/SEO — Cite Sources ≥3 outbound, Stats ≥5 com fonte+ano, Quotes ≥1 atribuída
- `analyzer.py` (Gemini): validar Two-Phase JSON-LD theory ao revisar páginas schema-related
- `classifier.py` (Groq): tags canônicas `geo-2026`, `aeo`, `aso`, `b2a`, `entity-drift`, `query-fan-out`
- `reviewer.py` (Claude): aplicar Anti-padrões §13 (llms.txt não é requisito; schema não é silver bullet; GEO ≠ substituto de SEO)
- `content_checker.py`: validações opcionais Cite Sources count, Statistics count, Quotation count, Compression Fidelity, Schema-content parity (bloqueante)
- `client.yaml`: campos `geo_2026.princeton_playbook_enabled`, `geo_2026.schema_authority_stack_enabled`, `geo_2026.b2a_pilot.{nlweb_endpoint,mcp_endpoint,openapi_spec_url}`

## 2026-04-29 — Refactor profundo em 5 waves (base reusável para outros segmentos)

Pivô para tornar o curso-factory base de arquitetura para portais educacionais em **outros segmentos**, sem fork. As waves:

1. **Auditoria** — mapa de bugs (4 subcomandos do CLI quebrados por imports inexistentes), código morto (`unified_finops.py`, `_build_writer_context`), duplicações de prompt e divergências entre CLAUDE.md e código real.
2. **Fundação** — CLI reescrito (`validate`, `cost-report`, `batch`, `cache-clear` agora funcionam; `cmd_cost_report` lê o log real do `CostTracker` em vez da API fictícia que existia antes). `writer.py` e `reviewer.py` adotam `**template_vars` para paridade com os outros 3 agents.
3. **Consolidação** — `unified_finops.py` removido (zero referências). `Cache` plugado no `LLMClient` (cache hit antes de circuit/retry). Defaults "Alexandre Caramaschi" / "Brasil GEO" removidos de `models.py:CourseDefinition` (`""` em vez de hardcode — quem instancia injeta via `ClientContext`). `SchemaBuilder` ganha clamp `max(30, duracao)`. Scripts ad-hoc movidos para `scripts/legacy/`.
4. **Testes** — bateria expandida de **24 → 74 testes**: `test_cli` (11), `test_parsers` (14), `test_converters` (7), `test_cost_cache` (8), `test_validators_smoke` (10). Cobre todos os 8 subcomandos, parser canônico, conversor de drafts, FinOps, accent_checker, quality_gate e voice_guard. Toda chamada `datetime.utcnow()` migrada para `datetime.now(timezone.utc)`.
5. **Docs** — `docs/ARCHITECTURE.md` reescrito como guia portal-agnóstico (camadas, o que é reusável, o que é segmento-específico, gaps conhecidos). Para novo portal: copiar `config/clients/_template/`, preencher YAML, eventualmente ajustar prompts.

**Estado final:** 74/74 pytest verde, 8/8 subcomandos do CLI funcionais, zero código morto detectado, zero default de identidade no model.

## 2026-04-25 — Base de conhecimento GEO/AEO/Agentic Commerce

Foi adicionada uma camada doutrinária permanente em [docs/knowledge/geo-aeo/](docs/knowledge/geo-aeo/) que sintetiza 25+ papers acadêmicos (2025–2026) em 30 instruções operacionais, 7 princípios mestres, 4 checklists e tabela de thresholds quantitativos.

**Quando usar.** Cursos sobre GEO, AEO, marketing por IA, comércio agêntico, MCP/A2A, RAG, knowledge graphs ou qualquer tema correlato devem usar este corpus como fonte primária. Cada agente do pipeline tem responsabilidades específicas:

- **Pesquisa (Perplexity)** → fontes-âncora aceitas em `50-fontes-e-links.md`. Toda afirmação factual deve casar com pelo menos um paper deste catálogo.
- **Redação (GPT-4o)** → princípios de `00-principios-mestres.md`, estrutura TL;DR/BLUF de `31-checklist-reescrita.md`, densidade de entidades 1/100 palavras (Instrução 17).
- **Análise (Gemini)** → verificar os 16 pilares de `30-checklist-auditoria-geo16.md` em cada módulo.
- **Classificação (Groq)** → tags com termos canônicos do `02-glossario.md`.
- **Revisão (Claude)** → varredura final contra `01-anti-patterns.md`.

**Princípio operacional.** Em conflito entre uma diretiva tática e um princípio mestre, **prevalece o princípio mestre**. A tese central: *GEO técnico é necessário, não suficiente. Estrutura validável vence prosa eloquente. Mídia conquistada explica a maior parte da variância de citação. Agent legibility é a nova SEO.*

**Manutenção.** Revisão trimestral. Novos papers entram simultaneamente em `2X-papers-bloco-*.md`, `40-thresholds-quantitativos.md` e `50-fontes-e-links.md`.

## 2026-04-19 — Refactor multi-tenant (Ondas 1-5)

### Mudança estrutural: ClientContext
- **Antes:** credencial Alexandre, domínio `alexandrecaramaschi.com`, padrão HSM/HBR/MIT Sloan e regras do voice guard estavam **hardcoded** em `models.py`, `voice_guard.py`, `pyproject.toml`, etc. Rodar a fábrica para outro cliente exigia fork.
- **Depois:** tudo que varia por cliente vem de `config/clients/<id>/client.yaml`. O framework carrega o YAML em um `ClientContext` (`src/clients/context.py`) e injeta em CourseFactory, Orchestrator, SchemaBuilder, QualityGate e voice_guard_check.
- **Cliente `default`** preserva 100% do comportamento pré-refactor (Brasil GEO). Qualquer `<id>` diferente escreve em `output/clients/<id>/`.
- **CLI:** `python cli.py create "Curso" --client minhaempresa` ou `export CURSO_FACTORY_CLIENT=<id>`.
- **Como listar:** `python cli.py clients`.
- **Playbook completo:** [docs/MULTI-CLIENT.md](docs/MULTI-CLIENT.md).

### Consolidação técnica
- **Parser compartilhado** `src/parsers/markdown_parser.py`: fonte única de `slugify`, `extract_module_blocks`, `parse_module_to_sections`. Antes, `schema_builder.py` e `draft_to_course.py` tinham implementações paralelas divergentes.
- **Providers em YAML** `config/providers.yaml` + `src/providers.py`: pricing, endpoints, default_model e fallback. `llm_client.py` só orquestra — mudança de preço/modelo é edição YAML.
- **Voice Guard no QualityGate**: agora é a 4ª camada bloqueante. Score < `client.voice_guard.min_score` (padrão 70) ou erro crítico → `aprovado=False`.

### Limpeza
- `.gitignore` exclui `output/`, `*.egg-info/`, `.pytest_cache/`, `.mypy_cache/`.
- `tests/fixtures/sample_course.json`: `nivel` corrigido de `intermediario` → `intermediário` (5/5 testes voltaram a verde).
- `src/indexer/course_indexer.py`: removido hardcode `C:/Sandyboxclaude/...`; lê `LANDING_PAGE_DIR` do env ou derive de path relativo.

### Commits da refatoração
- `d3c1077` — refactor: multi-tenancy via ClientContext + limpeza de fundação
- `203f126` — refactor: consolidação técnica (markdown_parser, providers.yaml, voice_guard em QualityGate)

### Regra para trabalhos futuros
Ao tocar em qualquer lógica sensível a autor/domínio/padrão editorial: passe pelo `ClientContext`, **não** hardcode. Se precisar de uma constante que varia por cliente, é campo de YAML.

## 2026-04-09 — Mudanças da auditoria de ecossistema (Wave D)

### NOVO: course_id propagado em cost_tracker (F32)
- **Commit:** `72ee757` — `feat(cost-tracker): propaga course_id em todas chamadas LLM`
- **Antes:** `cost_tracker.track()` sempre recebia `course_id=""`, tornando IMPOSSÍVEL responder "qual curso custou X" no `cost-report` ou aplicar budget guard granular por curso.
- **Depois:** `LLMClient.set_course_context(course_id)` é chamado pelo `Orchestrator.run()` no início. Todas as chamadas LLM subsequentes propagam automaticamente.
- **Como usar:** `python cli.py cost-report` agora pode agrupar por `course_id`. `cost_tracker.get_course_total('llm-finops')` retorna dados precisos por curso.
- **Compat backward:** se `set_course_context` não for chamado, comportamento idêntico ao anterior.

## 2026-04-09 — Mudanças da auditoria de ecossistema (Wave A-C)

### 1. CLI `drafts-to-tsx` (F12)
- **Commit:** `bc2f36e` — `feat(cli): drafts-to-tsx`
- **Arquivos:** `cli.py` (+novo subcomando), `src/converters/__init__.py`, `src/converters/draft_to_course.py`
- **Uso:** `python cli.py drafts-to-tsx [--input output/drafts] [--output output/converted_from_drafts]`
- **Resultado da execução desta sessão:** **12/12 drafts órfãos convertidos** para TSX deployable. Output em `output/converted_from_drafts/` com `page.tsx` + `layout.tsx` válidos por curso.
- **Próximo passo do owner:** revisar manualmente cada `output/converted_from_drafts/{slug}/page.tsx`, decidir quais publicar, mover aprovados para `output/deployed/`, commit final.
- **Cursos liberados:** automacao-com-n8n (×2), deploy-moderno, geo-para-educacao-financeira-40 e -sub-18, llm-finops (×2), mcp-avancado (×2), prompt-engineering-avancado, seo-e-geo-para-advogados, seo-e-geo-para-revendedoras-de-joias.
- **Conversor é best-effort:** parseia markdown da etapa `review` (preferida) ou `draft` (fallback), splita por headings, gera CourseSections (TEXT, CODE, TIP, CHECKPOINT). Cursos com 1 step só (sem headings claros) são clamped para 30 min mínimo.

### 2. Pre-commit secret_guard (F44)
- **Commit:** `8638b3f` — `sec(precommit): instala secret_guard`
- **Arquivos:** `.tools/secret_guard.py`, `.githooks/pre-commit`
- **Já ativado** localmente

### Achados pendentes neste repo

- **F13 (CRÍTICO):** ~~`voice_guard.py` programático ainda não existe.~~ **RESOLVIDO** na onda 2026-04-09 (B-012) e depois parametrizado por ClientContext em 2026-04-19.
- **F38 → BAIXO:** `curso-factory` chama LLMs direto em vez de usar `geo-orchestrator`. Crosscheck Gemini concordou que esse achado estava superdimensionado. Migração para SDK fica para uma onda futura.

## Regras Fundamentais

### Idioma
- TODO texto de curso DEVE ser em Português do Brasil com acentuação completa
- NUNCA: "nao", "voce", "producao" — SEMPRE: "não", "você", "produção"
- Exceção: código, variáveis, commits, nomes de arquivo em inglês

### Nomenclatura (cliente `default`)
- Credencial canônica: "Alexandre Caramaschi — CEO da Brasil GEO, ex-CMO da Semantix (Nasdaq), cofundador da AI Brasil"
- NUNCA usar: "Especialista #1", "GEO Brasil", "Source Rank"
- Domínios válidos: alexandrecaramaschi.com, brasilgeo.ai
- NUNCA referenciar: geobrasil.com.br, sourcerank.ai

**Importante:** essas regras valem para o cliente `default`. Ao trabalhar com outro cliente (`--client <id>`), as regras de naming vêm do `config/clients/<id>/client.yaml`. Não misture: jamais hardcode credencial Alexandre no código — tudo passa pelo `ClientContext`.

### Sem Emojis
- Proibido emojis em qualquer conteúdo de curso ou documentação

## Arquitetura do Pipeline

5 LLMs com papéis fixos — NÃO interpretar como sub-agentes do Claude Code:
1. Perplexity (sonar-pro) → pesquisa, fundamentação acadêmica e análise competitiva
2. GPT-4o → redação de módulos com padrão editorial HSM/HBR/MIT Sloan e andragogia
3. Gemini (2.5-pro) → análise de qualidade pedagógica e andragógica em 7 dimensões
4. Groq (Llama 3.3) → classificação, tags e metadados
5. Claude (opus-4-6) → revisão final com correção ativa: acentuação PT-BR, qualidade editorial, formatação ($5 max/curso)

### Prompts Externos (IMPORTANTE)
- Os prompts dos 5 agentes ficam em `src/templates/prompts/*.md`
- Os agentes em `src/agents/` carregam automaticamente o prompt externo via `base.py`
- Para alterar o comportamento de um agente, edite o arquivo .md correspondente
- Se o arquivo .md não existir, o agente usa o TEMPLATE inline como fallback
- NUNCA duplicar instruções entre o prompt externo e o template inline

## Padrão Editorial — Regras de Qualidade

### Estilo HSM/HBR/MIT Sloan
- Tom analítico, direto, orientado por dados, sem jargão vazio
- Frases curtas. Parágrafos de 2-3 frases (máximo 5 linhas). Sem floreios
- Dados e estatísticas para sustentar argumentos — nunca afirmar sem evidência
- Evitar superlativos sem evidência ("o melhor", "revolucionário")

### Andragogia (6 Princípios de Knowles) — OBRIGATÓRIO
1. Necessidade de saber — POR QUE antes do COMO
2. Autoconceito — profissional autônomo, nunca condescendente
3. Experiência prévia — conectar com vivências profissionais
4. Prontidão — aplicabilidade imediata no trabalho
5. Orientação a problemas — problemas reais, não taxonomias
6. Motivação intrínseca — crescimento profissional e domínio

### Taxonomia de Bloom nos Objetivos
- ACEITOS (nível 3-6): analisar, comparar, diagnosticar, avaliar, justificar, criar, projetar, aplicar, implementar
- PROIBIDOS (nível 1-2): entender, conhecer, saber, compreender, lembrar, memorizar, listar, descrever, identificar

### Formatação Obrigatória por Módulo
- Ao menos 1 tabela comparativa (formato markdown com pipes)
- Ao menos 3 exercícios com contexto profissional e progressão Bloom
- Sub-headings (linha terminando com `:`) a cada 2-3 parágrafos
- Negrito em termos-chave na primeira ocorrência usando `**termo**`
- Blockquotes (`> `) para insights centrais — ao menos 1-2 por módulo
- Bullets com `-- ` (dois hífens), NUNCA `- ` (um hífen)
- Nunca mais de 3 parágrafos seguidos sem elemento visual
- 2.500-4.000 palavras por módulo

### Padrão de Layout (FormattedText — UX Microsoft Learn + Salesforce Trailhead)
O template `page.tsx.j2` inclui um componente `FormattedText` que renderiza:
- `**bold**` → `<strong>` com font-semibold
- Linha terminando com `:` → `<h4>` sub-heading com border-bottom
- `-- item` → bullet list com dot azul (accent color)
- `1. item` → ordered list com número azul
- `| col | col |` → `<table>` com header uppercase e zebra striping
- `> texto` → blockquote com borda lateral azul
- Parágrafos → text-justify com leading-[1.75]
- Warning/tip/checkpoint → text-justify aplicado

### Expressões Proibidas
- "nos dias de hoje", "é fundamental que", "não é segredo que"
- "o futuro é agora", "em um mundo cada vez mais", "vamos explorar"
- "como sabemos", "é importante ressaltar", "vale a pena destacar"
- "grosso modo", "vamos aprender", "agora você vai entender"

## Quality Gate — 5 Camadas de Validação

### Camada 1: Acentuação (accent_checker.py)
- 300+ mapeamentos de palavras sem acento → forma correta
- `check_accents()`: detecta erros com linha, palavra e contexto
- `fix_accents()`: corrige automaticamente, preservando URLs/código/variáveis
- Rastreamento de blocos de código (```) para não alterar código

### Camada 2: Conteúdo (content_checker.py)
- Contagem de palavras (2.500-4.000)
- Presença de tabelas (mínimo 1 por módulo)
- Hierarquia de títulos sem pulos
- Blocos de citação para insights
- Exercícios (mínimo 3)
- Clichês proibidos (18 expressões)
- Verbos de Bloom nos objetivos
- Princípios andragógicos (5 indicadores)
- Parágrafos longos (máximo 5 linhas)
- Emojis (proibidos)

### Camada 3: Links (link_checker.py)
- Acentos em URLs = ERRO CRÍTICO (incidente 2026-03-27: 55 hrefs corrompidos)
- Verificação de links internos

### Camada 4: HTML (html_validator.py)
- Fechamento de tags, elementos obrigatórios, acessibilidade

### Camada 5: FinOps (cost_tracker.py)
- Budget guard: $5 max Claude, $10 max total por curso
- Cache obrigatório: SHA-256, TTL 24h

### Auto-correção de Acentos
- O quality gate (`auto_fix=True` por padrão) corrige acentos automaticamente
- O texto corrigido é retornado em `GateResult.texto_corrigido`
- Correções residuais são detectadas e reportadas

## Regras Anti-Retrabalho

### NUNCA usar heredocs para conteúdo grande
- Heredocs >50 linhas QUEBRAM no shell
- SEMPRE usar templates Jinja2 em src/templates/
- SEMPRE gerar arquivos via Python (Write tool ou script)

### NUNCA usar scripts de substituição por regex
- Scripts que leem template e substituem trechos são FRÁGEIS
- SEMPRE gerar o arquivo completo de uma vez (geração atômica)

### Validação ANTES de deploy
- Rodar quality_gate.py com todas as 5 camadas
- Se qualquer camada bloqueante falhar, NÃO fazer deploy
- Auto-correção de acentos é aplicada automaticamente

### FinOps
- Budget guard ativo: $5 max Claude, $10 max total por curso
- Cache obrigatório — nunca reprocessar conteúdo já aprovado
- Verificar custo antes de executar pipeline completo
- API keys: fonte de verdade em geo-orchestrator/.env

## Estrutura de Arquivos

- config/courses.yaml — definição dos cursos
- config/quality_rules.yaml — regras de qualidade
- src/agents/ — um agente por LLM (carrega prompt de templates/prompts/)
- src/templates/prompts/ — prompts externos de alta densidade (.md)
- src/templates/ — templates Jinja2 para TSX (NUNCA heredoc)
- src/validators/ — 5 validadores (acentos, conteúdo, HTML, links, quality gate)
- src/generators/ — geradores de TSX (Jinja2, schema builder, metadata sync, build validator)
- src/schemas/ — JSON Schema para CourseDefinition
- output/drafts/ — rascunhos
- output/approved/ — aprovados
- output/deployed/ — em produção
- tests/ — testes unitários dos geradores

## Comandos CLI

```bash
python cli.py clients                                # Lista clientes em config/clients/
python cli.py create "Nome do Curso"                 # Cria curso sob cliente default
python cli.py create "Nome do Curso" --client acme   # Cria sob cliente específico
python cli.py validate output/drafts/                # Valida rascunhos
python cli.py cost-report                            # Relatório de custos
python cli.py batch config/courses.yaml              # Criação em lote
python cli.py batch config/courses.yaml --client X   # Lote sob cliente X
```

## Workflow de Criação de Curso

1. Definir curso em courses.yaml (nome, nível, módulos, descrição)
2. Executar `python cli.py create "Nome"`
3. Pipeline automático: Research → Draft → Analyze → Classify → Review
4. Quality Gate automático (5 camadas: acentos + conteúdo + links + HTML + FinOps)
5. Auto-correção de acentos aplicada
6. Se aprovado → output/approved/
7. Deploy manual ou via script

## Credencial do Autor (cliente `default`)
- Nome: Alexandre Caramaschi
- Título: CEO da Brasil GEO, ex-CMO da Semantix (Nasdaq), cofundador da AI Brasil
- URL: https://alexandrecaramaschi.com
- NUNCA usar: "Especialista #1", credenciais inventadas

**Para outro cliente:** consulte `config/clients/<id>/client.yaml` → seção `author:` e `voice_guard.canonical:`. O voice guard bloqueia textos que violem o naming canônico do cliente ativo.
