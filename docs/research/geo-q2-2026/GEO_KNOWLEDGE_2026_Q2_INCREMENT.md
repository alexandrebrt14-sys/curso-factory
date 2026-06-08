# GEO Knowledge Q2 2026 — Incremento canônico para curso-factory

> Atualização 2026-05-17 sobre KB de 13-mai. Foco: novidades Q1-Q2 2026 aplicáveis especificamente ao repositório `curso-factory` (pipeline Python multi-LLM que gera cursos completos para Semijoias-Educa, Brasil GEO Academy e cursos futuros de marketing GEO/AI). Use este documento como contexto enriquecido em qualquer prompt/task neste repo.

## 0. Sumário executivo · ações imediatas

- **Criar curso novo "GEO 2026 Estado da Arte" na Brasil GEO Academy** com 8 módulos baseados nos papers Q1-Q2 2026 (`AgenticGEO`, `CASTER`, `AdaptOrch`, `DAAO`), publicação prevista para 2026-06-15. Fonte: https://arxiv.org/html/2603.20213v1
- **Atualizar `docs/GEO_KNOWLEDGE_BASE_2026.md` (versão 13-mai)** incorporando seção sobre AgenticGEO, ColPali, GraphRAG e métricas Citation Drift; abrir PR canônico em 2026-05-20. Fonte: https://microsoft.github.io/graphrag/
- **Refatorar o orchestrator multi-LLM do `curso-factory`** para suportar roteamento custo-aware (padrão `RouteLLM` + `MoA`), permitindo que cada etapa do pipeline (ementa, aula, exercício, revisão) use o modelo ideal por custo/qualidade. Fonte: https://arxiv.org/abs/2404.06801
- **Adicionar Claude Opus 4.7, GPT-5.5 e Gemini 3.1 Flash ao pool de geradores** do `curso-factory`, com fallback hierárquico Opus 4.7 → GPT-5.5 → Sonnet 4.6 → Haiku 4.5 para tarefas de raciocínio profundo (síntese de módulo). Fonte: https://www.anthropic.com/news/claude-opus-4-7
- **Publicar lab prático "llms.txt + MCP + discovery files"** como módulo gratuito da Brasil GEO Academy, com repositório template no GitHub e validador automatizado em Python. Fonte: https://www.solumize.com/blog/aeo-vs-seo-vs-geo-differences-2026
- **Implementar pipeline de embeddings BGE-M3 self-hosted** para o RAG interno do `curso-factory` (corpus de papers, transcrições, livros didáticos), reduzindo custo de OpenAI `text-embedding-3-large` em ~85%. Fonte: https://huggingface.co/BAAI/bge-m3
- **Instituir KPIs canônicos AECR/AIGVR/SoM nos cursos gerados** mensurando citação de Semijoias-Educa e Brasil GEO Academy em ChatGPT, Perplexity, Google AI Overviews e Claude via Profound ou Ahrefs Brand Radar. Fonte: https://ahrefs.com/brand-radar
- **Criar módulo "Vector Embeddings e RAG para Criadores de Curso"** ensinando docentes do Semijoias-Educa a construir bases vetoriais de seu próprio conteúdo, com Qdrant local + BGE-M3. Fonte: https://qdrant.tech/pricing/
- **Adotar `Rolling Baselines` no dashboard interno** do `curso-factory` para medir visibilidade dos cursos publicados em janelas móveis de 4 semanas (anti-padrão de medição fixa). Fonte: https://goodzinking.com/en/continuous-geo-monitoring.html
- **Atualizar `docs/SEO_KNOWLEDGE_BASE_2026.md`** com seção dedicada ao guia oficial do Google "AEO/GEO ainda é SEO" e cross-link com a KB de GEO. Fonte: https://www.searchenginejournal.com/googles-new-ai-search-guide-calls-aeo-and-geo-still-seo/575026/

## 1. Mudanças no estado da arte (2026 Q1-Q2) relevantes para este repo

### 1.1 AgenticGEO e o novo paradigma de geração de conteúdo educacional

O paper `arXiv:2603.20213` (26-mar-2026) propõe um sistema agentic que co-evolui estratégias de otimização e um "crítico" que emula o motor generativo, alcançando ganhos de visibilidade de ~46% sobre baselines tradicionais. Para o `curso-factory`, isso significa **repensar a arquitetura do pipeline**: cada aula gerada deve passar por uma etapa de "crítica simulada" que avalie sua probabilidade de ser citada por LLMs como ChatGPT e Perplexity quando o aluno fizer perguntas sobre o tópico fora da plataforma.

Aplicação concreta: adicionar um agente `geo_critic.py` ao pipeline que recebe a aula gerada, simula 10-20 prompts típicos do nicho (ex.: "como soldar prata 950" para Semijoias-Educa) e devolve um score de "citation-readiness" antes da publicação. Fontes: https://arxiv.org/html/2603.20213v1 · https://arxiv.org/abs/2509.08919 · https://foundationinc.co/lab/geo-metrics

### 1.2 Orquestração multi-LLM custo-aware (CASTER, AdaptOrch, DAAO)

Três papers de 2026 Q1 redefinem como sistemas multi-LLM devem operar: `CASTER` (`arXiv:2601.19793`, 30-jan-2026) introduz steering custo-aware; `AdaptOrch` (`arXiv:2602.16873`, 25-fev-2026) implementa seleção dinâmica de modelos; `DAAO` (`arXiv:2509.11079`, set-2025) propõe orquestração adaptativa em tempo real. O `curso-factory` hoje usa orquestração estática (escolha hard-coded por etapa). Migrar para orquestração adaptativa permitiria reduzir o custo médio por curso completo gerado em ~40-60%, mantendo qualidade equivalente.

Aplicação concreta: criar módulo `orchestrator/adaptive_router.py` que classifica cada tarefa (geração de ementa = raciocínio alto → Opus 4.7; geração de exercício múltipla escolha = média → GPT-5.5; revisão ortográfica = baixa → Haiku 4.5 ou Gemini 3.1 Flash). Fontes: https://arxiv.org/abs/2601.19793 · https://arxiv.org/abs/2602.16873 · https://arxiv.org/abs/2509.11079

### 1.3 RAG evolui de busca vetorial simples para GraphRAG e ColPali

O estado da arte em RAG migrou para abordagens específicas por domínio: `GraphRAG` (Microsoft) usa grafos de conhecimento para queries multi-hop; `ColPali` permite retrieval em PDFs com layout visual preservado; `LightRAG` simplifica grafos pesados; `Agentic RAG` (survey `arXiv:2502.11947`) torna o processo iterativo. Para o `curso-factory`, isso impacta diretamente como construímos a base de conhecimento usada para gerar conteúdo factualmente correto.

Aplicação concreta: para Semijoias-Educa (corpus com muitos PDFs técnicos de gemologia, catálogos de pedras, manuais de equipamentos), adotar `ColPali` em vez do pipeline atual de OCR + chunking textual. Para Brasil GEO Academy (corpus com papers acadêmicos e entidades conectadas), adotar `GraphRAG` para perguntas como "qual a relação entre `AdaptOrch` e `MoA`?". Fontes: https://microsoft.github.io/graphrag/ · https://github.com/illuin-tech/colpali · https://arxiv.org/abs/2502.11947

### 1.4 Lançamentos Q1-Q2 2026 expandem o pool de modelos disponíveis

Em apenas 4 meses, foram lançados: `Claude Opus 4.7` (abr-2026, foco em agentic reasoning), `GPT-5.5` (abr-2026, melhoria em codificação e tool use), `Gemma 4` (família open weights até 256k contexto), `Llama 4` (até 10M de contexto, Scout/Maverick), `Qwen 3.6-Plus` (1M contexto), `GLM-5.1` (744B MoE com licença MIT) e `Mistral 3` (mai-2026). O `curso-factory` precisa atualizar sua matriz de modelos suportados, especialmente para tarefas que se beneficiam de contexto massivo (ex.: ingerir um livro completo de joalheria como contexto para gerar um módulo de 12 aulas).

Aplicação concreta: introduzir suporte a `Llama 4 Scout` para tarefas long-context (geração de curso baseado em PDF de 800 páginas) e `GLM-5.1` para geração de exercícios de programação (modelo aberto, custo zero de API). Fontes: https://www.anthropic.com/news/claude-opus-4-7 · https://openai.com/index/introducing-gpt-5-5/ · https://ai.meta.com/blog/llama-4-multimodal-intelligence/ · https://fazm.ai/blog/new-llm-releases-april-2026

### 1.5 KPIs GEO se consolidam e plataformas amadurecem

A indústria adotou um conjunto canônico de métricas: `Share of Model (SoM)`, `Citation Rate`, `Citation Drift`, `Time-to-Citation`, `AECR (Answer Engine Citation Rate)` e `AIGVR (AI-Generated Visibility Rate)`. Plataformas como Profound (valuation US$ 1B), Ahrefs Brand Radar, SEMrush AI Toolkit e AthenaHQ se consolidaram como fontes confiáveis de medição. Isso impacta diretamente o `curso-factory` porque os cursos publicados (Semijoias-Educa, Brasil GEO Academy) precisam medir sua presença em LLMs como sinal de sucesso, não apenas tráfego orgânico clássico.

Aplicação concreta: criar dashboard `geo_metrics.py` que consume API da Profound (ou scraping controlado quando API não disponível) e gera relatório semanal de SoM e Citation Rate para os domínios dos cursos. Fontes: https://ahrefs.com/brand-radar · https://checkthat.ai/brands/bluefish-ai/alternatives · https://alexandrecaramaschi.com/artigos/roi-do-geo-em-90-dias-metricas-honestas-para-o-cmo

## 2. Stack canônico atualizado

| Componente | Versão 13-mai | Versão 17-mai | Razão da mudança | Fonte URL |
|---|---|---|---|---|
| LLM principal (raciocínio) | Claude Opus 4.6 | Claude Opus 4.7 | Lançamento abr-2026 com agentic reasoning aprimorado e codificação avançada | https://www.anthropic.com/news/claude-opus-4-7 |
| LLM secundário | GPT-5 | GPT-5.5 | Lançamento abr-2026 com melhor tool use e redução de alucinações | https://openai.com/index/introducing-gpt-5-5/ |
| LLM rápido/barato | Haiku 4.5 / Gemini 2.5 Flash | Haiku 4.5 / Gemini 3.1 Flash | Atualização Gemini mar-2026 (mais rápido, contexto ampliado) | https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-3-1-flash-lite/ |
| LLM long-context | Gemini 2.5 Pro (2M) | Llama 4 Scout (10M) / Qwen 3.6-Plus (1M) | Necessidade de ingerir corpus extensos (livros completos) em uma única chamada | https://ai.meta.com/blog/llama-4-multimodal-intelligence/ |
| Embeddings (paid) | OpenAI text-embedding-3-large | Voyage 3 / Cohere Embed v4 | Performance superior em MTEB e melhor custo-benefício para tarefas multilíngues PT-BR | https://docs.voyageai.com/ |
| Embeddings (self-host) | bge-large-en-v1.5 | BGE-M3 | Suporte multilíngue nativo (PT-BR), dense + sparse + multi-vector em um único modelo | https://huggingface.co/BAAI/bge-m3 |
| Vector DB local | ChromaDB | Qdrant | Filtragem avançada de payload, melhor performance em produção | https://qdrant.tech/pricing/ |
| Vector DB cloud | Pinecone | Pinecone Serverless + LanceDB (multimodal) | LanceDB necessário para corpus multimodal (PDFs com imagens em Semijoias-Educa) | https://lancedb.com/ |
| RAG framework | LlamaIndex + LangChain | LightRAG + Agentic RAG pattern | Simplificação de pipelines pesados de grafo, padrão iterativo de retrieve+reason | https://github.com/HKUDS/LightRAG |
| RAG multimodal | OCR + chunking textual | ColPali (late interaction multimodal) | Preserva layout visual de PDFs técnicos (catálogos de pedras, diagramas) | https://github.com/illuin-tech/colpali |
| Orquestração | Roteamento estático por etapa | Padrão RouteLLM + MoA (custo-aware) | Redução de custo ~40-60% mantendo qualidade equivalente | https://arxiv.org/abs/2404.06801 |
| Crítico/avaliador | LLM-as-judge simples | AgenticGEO critic loop | Simulação de motor generativo para validar "citation-readiness" | https://arxiv.org/html/2603.20213v1 |
| Discovery files | sitemap.xml + robots.txt | sitemap.xml + robots.txt + llms.txt + MCP manifest | Padrões emergentes 2026 para crawlers de IA | https://www.solumize.com/blog/aeo-vs-seo-vs-geo-differences-2026 |
| Métricas de sucesso | Tráfego orgânico + conversões | + SoM + Citation Rate + Citation Drift | Adoção de KPIs canônicos GEO 2026 | https://foundationinc.co/lab/geo-metrics |
| Monitoramento GEO | Manual (busca em ChatGPT) | Profound API / Ahrefs Brand Radar | Automação e cobertura multi-LLM (10+ modelos) | https://ahrefs.com/brand-radar |
| Benchmark de avaliação | Custom internal | GEO-Bench + Arena-Hard + MT-Bench | Padrões da indústria para avaliar saída de LLMs | https://arxiv.org/abs/2311.09735 |

## 3. Roadmap operacional próximos 60 dias

| Ação | Esforço | Owner | Prazo | Métrica de sucesso |
|---|---|---|---|---|
| Refatorar orchestrator para roteamento custo-aware (RouteLLM + MoA) | 5 dias-dev | Eng. Backend | 2026-05-30 | Redução ≥40% no custo médio por curso gerado |
| Criar curso "GEO 2026 Estado da Arte" (8 módulos, 56 aulas) | 12 dias | Líder Conteúdo + curso-factory | 2026-06-15 | Curso publicado com ≥80% de aulas "citation-ready" (score AgenticGEO) |
| Implementar `geo_critic.py` (loop crítico AgenticGEO) | 4 dias-dev | Eng. ML | 2026-06-05 | Score médio de citation-readiness ≥0.7 em amostra de 50 aulas |
| Migrar embeddings para BGE-M3 self-hosted | 3 dias-dev | Eng. Infra | 2026-05-28 | Custo de embeddings reduzido ≥80%; MTEB-pt mantido |
| Adicionar Llama 4 Scout (long-context) ao pool de modelos | 2 dias-dev | Eng. Backend | 2026-06-01 | Geração de curso a partir de PDF ≥500 páginas em uma única chamada |
| Implementar ColPali para Semijoias-Educa (PDFs técnicos) | 6 dias-dev | Eng. ML | 2026-06-20 | Precisão de retrieval ≥85% em queries sobre figuras/tabelas |
| Adotar GraphRAG para Brasil GEO Academy (papers + entidades) | 7 dias-dev | Eng. ML | 2026-06-25 | Suporte a queries multi-hop em corpus de 200+ papers |
| Publicar lab "llms.txt + MCP + discovery files" como módulo gratuito | 4 dias | Líder Conteúdo | 2026-06-10 | ≥500 alunos inscritos em 30 dias |
| Criar dashboard `geo_metrics.py` (SoM, Citation Rate, Drift) | 5 dias-dev | Eng. Data | 2026-06-15 | Dashboard em produção com dados semanais de 4 LLMs |
| Atualizar `docs/GEO_KNOWLEDGE_BASE_2026.md` (PR canônico) | 2 dias | Doc Owner | 2026-05-20 | PR mergeado com revisão de 2 reviewers |
| Atualizar `docs/SEO_KNOWLEDGE_BASE_2026.md` (cross-link GEO) | 1 dia | Doc Owner | 2026-05-22 | Seção "AEO/GEO ainda é SEO" incorporada |
| Criar módulo "Vector Embeddings e RAG para Criadores de Curso" | 8 dias | Líder Conteúdo | 2026-07-05 | Módulo com lab prático Qdrant+BGE-M3 publicado |
| Integrar Profound API (ou Ahrefs Brand Radar) | 3 dias-dev | Eng. Data | 2026-06-10 | Ingestão automatizada semanal de métricas SoM por curso |
| Lab prático configurando `llms.txt` para sites dos 2 cursos atuais | 1 dia | Eng. Infra | 2026-05-25 | Arquivos `llms.txt` válidos em semijoias-educa.com.br e brasilgeoacademy.com.br |
| Criar template de "Glossário Citável" por curso | 2 dias | Líder Conteúdo | 2026-06-30 | Template aplicado em 3 cursos; ≥30 termos definidos por curso |

## 4. KPIs e medições aplicáveis

Para o `curso-factory` e os sites educacionais que ele alimenta, adotamos o seguinte conjunto canônico de KPIs:

- **Citation Rate (CR)** · Fórmula: `(respostas em que o domínio do curso é citado) / (total de prompts testados)`. Baseline atual: desconhecido (será medido em 2026-05-25). Target Q3 2026: ≥15% em Semijoias-Educa e ≥25% em Brasil GEO Academy. Fonte: https://foundationinc.co/lab/geo-metrics

- **Share of Model (SoM)** · Fórmula: `(menções da marca em respostas LLM) / (menções totais de marcas concorrentes para o cluster de prompts)`. Baseline: Semijoias-Educa ~3% (estimado), Brasil GEO Academy ~8% (estimado). Target Q3 2026: ≥10% Semijoias-Educa, ≥20% Brasil GEO Academy. Fonte: https://alexandrecaramaschi.com/artigos/roi-do-geo-em-90-dias-metricas-honestas-para-o-cmo

- **AECR (Answer Engine Citation Rate)** · Fórmula igual ao CR, porém segmentada por motor (Google AI Overviews, ChatGPT, Perplexity, Claude). Baseline a ser estabelecido em 2026-06-01. Target Q3 2026: AECR ≥10% em pelo menos 3 motores. Fonte: conceito derivado de https://www.solumize.com/blog/aeo-vs-seo-vs-geo-differences-2026

- **AIGVR (AI-Generated Visibility Rate)** · Fórmula: `(menções da marca em qualquer resposta gerada por IA) / (total de respostas geradas para prompts do cluster)`. Funcionalmente similar a CR agregado multi-LLM. Target Q3 2026: ≥20% para Brasil GEO Academy. Fonte: https://athenahq.ai/athena-state-of-ai-full-report

- **Citation Drift** · Fórmula: `% de domínios citados que mudam entre janelas mensais consecutivas`. Métrica de estabilidade. Baseline da indústria: 40-59%. Target Q3 2026: monitorar e estabilizar abaixo de 35% para nossos cursos. Fonte: https://checkthat.ai/brands/bluefish-ai/alternatives

- **Time-to-Citation (TTC)** · Fórmula: `(data da primeira citação por LLM) - (data de publicação do conteúdo)`. Baseline atual: desconhecido. Target Q3 2026: TTC mediano ≤45 dias para conteúdo otimizado via `curso-factory`. Fonte: https://www.inboundcycle.com/pt/blog-de-inbound-marketing/metricas-geo/

- **Citation Share (Anchor Coverage)** · Fórmula: `(fontes do nosso domínio citadas em uma resposta) / (total de fontes citadas na resposta)`. Target Q3 2026: ≥25% quando citados. Fonte: https://authoritytech.io/blog/share-of-citation

- **CTAM (Cost To Acquire Mention)** · Fórmula: `(custo total de produção do curso via curso-factory) / (número de menções únicas adquiridas em LLMs nos 90 dias seguintes)`. Baseline a estabelecer. Target Q3 2026: CTAM ≤ R$ 50 por menção. Fonte: conceito derivado, sem paper formal

- **RTAS (Response Time for Agentic System)** · Fórmula: `tempo médio (segundos) para o pipeline curso-factory gerar uma aula completa após o trigger`. Baseline atual: ~180s/aula. Target Q3 2026: ≤90s/aula após adoção de roteamento adaptativo. Fonte: conceito derivado, sem paper formal

- **Pickup Rate** · Fórmula: `% de conteúdos publicados nos últimos 60 dias que foram citados por ao menos 1 LLM`. Target Q3 2026: ≥40%. Fonte: conceito derivado, sem paper formal

- **Citation-readiness score (interno, AgenticGEO)** · Fórmula: score 0-1 gerado pelo `geo_critic.py` que simula prompts e mede probabilidade de citação. Target Q3 2026: ≥0.7 médio em aulas publicadas. Fonte: https://arxiv.org/html/2603.20213v1

Toda métrica deve usar **Rolling Baselines** (média móvel de 4 semanas) em vez de comparação fixa, conforme padrão consolidado em 2026. Fonte: https://goodzinking.com/en/continuous-geo-monitoring.html

## 5. Anti-padrões a evitar

1. **Gerar aulas sem etapa de "crítica simulada" (AgenticGEO critic loop)** · Publicar conteúdo direto do gerador para o site, sem validar citation-readiness, replica o anti-padrão "publish-and-forget". Em um ambiente com Citation Drift de 40-59%, isso garante baixa visibilidade duradoura. Justificativa: o paper AgenticGEO demonstra ganhos de ~46% quando se adota crítico simulado. Fonte: https://arxiv.org/html/2603.20213v1

2. **Roteamento estático de LLM por etapa do pipeline** · Hard-coding "ementa sempre usa GPT-5.5, exercício sempre Sonnet 4.6" desperdiça orçamento e perde qualidade. CASTER e AdaptOrch mostram que roteamento adaptativo reduz custo 40-60% mantendo qualidade. Justificativa: a complexidade da tarefa varia drasticamente entre aulas (ex.: aula introdutória vs. aula técnica avançada). Fontes: https://arxiv.org/abs/2601.19793 · https://arxiv.org/abs/2602.16873

3. **Tratar o `curso-factory` como ferramenta de SEO clássico** · Otimizar títulos para keywords e meta-descriptions sem considerar clareza factual, estrutura citável e dados estruturados é equivalente a "fazer SEO para um buscador que não existe mais". Justificativa: o paper original de GEO (`arXiv:2311.09735`) e o guia oficial do Google ("AEO/GEO ainda é SEO") deixam claro que o foco mudou para "ser fonte da verdade". Fonte: https://www.searchenginejournal.com/googles-new-ai-search-guide-calls-aeo-and-geo-still-seo/575026/

4. **Otimizar cursos apenas para um único LLM (ex.: só ChatGPT)** · Concentrar a estratégia em um único motor ignora a fragmentação do mercado e a alta volatilidade. Um update de modelo pode apagar visibilidade da noite para o dia. Justificativa: dados da Profound mostram Citation Drift de 40-59% mensal. Fonte: https://checkthat.ai/brands/bluefish-ai/alternatives

5. **Usar OCR + chunking textual para PDFs do Semijoias-Educa** · O corpus de gemologia e joalheria depende fortemente de figuras (cortes de pedras, diagramas de soldagem, ilustrações de técnicas). OCR descarta essa informação. Justificativa: ColPali preserva layout visual e late interaction, alcançando precisão superior em corpora multimodais técnicos. Fonte: https://github.com/illuin-tech/colpali

6. **Medir sucesso dos cursos apenas por tráfego orgânico/conversões** · Em um mundo com zero-click searches dominantes, o conteúdo do curso pode estar moldando a percepção do usuário (via citação em LLMs) sem gerar clique direto. Ignorar SoM e Citation Rate subestima drasticamente o ROI real do `curso-factory`. Justificativa: relatórios da BrightEdge e SparkToro mostram crescimento de AI search visits e mudança do funil. Fontes: https://www.brightedge.com/resources/research-reports/ai-search-visits-in-surging-2025 · https://sparktoro.com/blog/new-research-search-happens-everywhere-an-analysis-of-41-websites-with-significant-search-activity/

## 6. Artefatos a produzir

Os seguintes artefatos canônicos devem ser criados no repositório `curso-factory` nos próximos 30 dias:

1. **`docs/GEO_KNOWLEDGE_BASE_2026.md` (atualização)** · Incorporar seções sobre AgenticGEO, ColPali, GraphRAG, Citation Drift e KPIs canônicos (SoM, AECR, AIGVR). Adicionar tabela de papers Q1-Q2 2026. Prazo: 2026-05-20.

2. **`docs/SEO_KNOWLEDGE_BASE_2026.md` (atualização)** · Cross-link com KB de GEO; adicionar seção "AEO/GEO ainda é SEO" baseada no guia oficial Google; incluir tabela de Schema.org relevante para conteúdo educacional (Course, LearningResource, HowTo, FAQPage). Prazo: 2026-05-22.

3. **`orchestrator/adaptive_router.py`** · Módulo Python que implementa roteamento custo-aware (padrão RouteLLM + MoA) com classificação dinâmica de complexidade de tarefa e seleção de LLM (Opus 4.7 / GPT-5.5 / Sonnet 4.6 / Haiku 4.5 / Gemini 3.1 Flash / Llama 4 Scout). Inclui telemetria de custo por execução. Prazo: 2026-05-30.

4. **`agents/geo_critic.py`** · Agente "crítico" inspirado em AgenticGEO que recebe aula gerada, simula prompts típicos do nicho via LLM-as-judge e devolve score de citation-readiness 0-1. Bloqueia publicação se score <0.5. Prazo: 2026-06-05.

5. **`rag/colpali_pipeline.py`** · Pipeline ColPali multimodal para ingestão de PDFs técnicos do Semijoias-Educa (catálogos de pedras, manuais de equipamentos, diagramas). Substitui OCR + chunking textual atual. Prazo: 2026-06-20.

6. **`rag/graphrag_pipeline.py`** · Pipeline GraphRAG para Brasil GEO Academy (papers + entidades), permitindo queries multi-hop sobre o corpus de pesquisa acadêmica. Prazo: 2026-06-25.

7. **`courses/geo-2026-estado-da-arte/`** · Curso completo "GEO 2026 Estado da Arte" com 8 módulos: (1) Fundamentos GEO/AEO; (2) Papers Q1-Q2 2026 (AgenticGEO, CASTER, AdaptOrch, DAAO); (3) Stack canônico 2026; (4) Profound dashboard prático; (5) Ahrefs Brand Radar e tracking de AI Overviews; (6) Vector embeddings e RAG; (7) KPIs canônicos (AECR/AIGVR/SoM); (8) Lab `llms.txt` + MCP + discovery files. Prazo: 2026-06-15.

8. **`courses/embeddings-rag-para-criadores/`** · Módulo "Vector Embeddings e RAG para Criadores de Curso" ensinando docentes a construir bases vetoriais de seu próprio conteúdo, com lab Qdrant local + BGE-M3 self-hosted. Prazo: 2026-07-05.

9. **`dashboards/geo_metrics.py`** · Dashboard interno que ingere dados de Profound API (ou Ahrefs Brand Radar) e calcula semanalmente SoM, Citation Rate, AECR, Citation Drift, Time-to-Citation e Pickup Rate para os domínios dos cursos. Usa Rolling Baselines (4 semanas). Prazo: 2026-06-15.

10. **`templates/llms_txt_template.md` + `templates/mcp_manifest_template.json`** · Templates canônicos para `llms.txt` e manifest MCP, aplicados nos sites Semijoias-Educa e Brasil GEO Academy, com validador automatizado em Python (`tools/validate_discovery_files.py`). Prazo: 2026-05-25.

11. **`templates/glossario_citavel_template.md`** · Template de "Glossário Citável" por curso, com seções estruturadas (Termo, Definição canônica de 1-2 sentenças, Sinônimos, Fontes). Aplicar em 3 cursos iniciais. Prazo: 2026-06-30.

12. **`docs/ANTI_PADROES_GEO_2026.md`** · Documento canônico listando os 6 anti-padrões da seção 5 deste documento, com exemplos práticos e revisões trimestrais. Prazo: 2026-06-01.

## Apêndice — URLs canônicos

1. https://ahrefs.com/brand-radar
2. https://ahrefs.com/blog/ai-overviews-reduce-clicks-update/
3. https://ai.meta.com/blog/llama-4-multimodal-intelligence/
4. https://alexandrecaramaschi.com/artigos/roi-do-geo-em-90-dias-metricas-honestas-para-o-cmo
5. https://api-docs.deepseek.com/news/news260424
6. https://arxiv.org/abs/2004.12832
7. https://arxiv.org/abs/2210.07316
8. https://arxiv.org/abs/2212.10496
9. https://arxiv.org/abs/2306.05685
10. https://arxiv.org/abs/2311.09735
11. https://arxiv.org/abs/2404.06801
12. https://arxiv.org/abs/2406.04692
13. https://arxiv.org/abs/2406.11939
14. https://arxiv.org/abs/2502.11947
15. https://arxiv.org/abs/2509.08919
16. https://arxiv.org/abs/2509.11079
17. https://arxiv.org/abs/2511.16681
18. https://arxiv.org/abs/2601.19793
19. https://arxiv.org/abs/2602.16873
20. https://arxiv.org/abs/2603.20324
21. https://arxiv.org/html/2603.20213v1
22. https://athenahq.ai/athena-state-of-ai-full-report
23. https://authoritytech.io/blog/share-of-citation
24. https://backlinko.com/ai-statistics
25. https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-3-1-flash-lite/
26. https://checkthat.ai/brands/bluefish-ai/alternatives
27. https://docs.cohere.com/docs/embeddings
28. https://docs.mistral.ai/models/model-cards/pixtral-large-24-11
29. https://docs.voyageai.com/
30. https://docs.x.ai/developers/models/grok-4.3
31. https://fazm.ai/blog/new-llm-releases-april-2026
32. https://foundationinc.co/lab/geo-metrics
33. https://github.com/Alibaba-NLP/gte-Qwen
34. https://github.com/HKUDS/LightRAG
35. https://github.com/illuin-tech/colpali
36. https://github.com/pgvector/pgvector
37. https://github.com/stanford-futuredata/ColBERT
38. https://goodzinking.com/en/continuous-geo-monitoring.html
39. https://huggingface.co/BAAI/bge-m3
40. https://huggingface.co/Snowflake/snowflake-arctic-embed-l
41. https://huggingface.co/jinaai/jina-embeddings-v3
42. https://huggingface.co/nvidia/NV-Embed-v2
43. https://lancedb.com/
44. https://microsoft.github.io/graphrag/
45. https://milvus.io/pricing/
46. https://mistral.ai/news/codestral-2501
47. https://mistral.ai/news/mistral-3
48. https://openai.com/index/introducing-gpt-5-5/
49. https://platform.openai.com/docs/guides/embeddings
50. https://profound.ai/
51. https://qdrant.tech/pricing/
52. https://searchengineland.com/library/google/google-ai-overviews
53. https://sparktoro.com/blog/new-research-search-happens-everywhere-an-analysis-of-41-websites-with-significant-search-activity/
54. https://turbopuffer.com/
55. https://vespa.ai/
56. https://weaviate.io/pricing
57. https://www.anthropic.com/news/claude-haiku-4-5
58. https://www.anthropic.com/news/claude-opus-4-6
59. https://www.anthropic.com/news/claude-opus-4-7
60. https://www.anthropic.com/news/claude-sonnet-4-6
61. https://www.brightedge.com/resources/research-reports/ai-search-visits-in-surging-2025
62. https://www.inboundcycle.com/pt/blog-de-inbound-marketing/metricas-geo/
63. https://www.pinecone.io/pricing/
64. https://www.searchenginejournal.com/googles-new-ai-search-guide-calls-aeo-and-geo-still-seo/575026/
65. https://www.solumize.com/blog/aeo-vs-seo-vs-geo-differences-2026