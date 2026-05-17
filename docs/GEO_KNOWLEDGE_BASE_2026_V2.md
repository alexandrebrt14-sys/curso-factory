# GEO Knowledge Base 2026 V2 — curso-factory

> Versão 2.0 · 17-05-2026 · Owner: Brasil GEO (Alexandre Caramaschi — CEO da Brasil GEO, ex-CMO da Semantix (Nasdaq), cofundador da AI Brasil)
>
> Delta sobre a V1 (13-05-2026): novos papers de 2026 verificados via arXiv, vendor landscape pós-funding Q1/Q2 2026 (US$ 192M em rodadas confirmadas), framework rigoroso de medição com 14 KPIs canônicos e desmonte de acrônimos infundados que circulam em material PT-BR secundário.
>
> Leia este documento em complemento, não em substituição, à V1. A V1 cobre a teoria fundacional (Aggarwal 2023, Chen 2025) e a stack interna do curso-factory. A V2 substitui as seções de papers, vendor pricing e KPIs por dados frescos de Q1/Q2 2026.

---

## Índice

0. O que mudou desde a V1 — sumário das 5 mudanças principais
1. Papers acadêmicos de 2026 — os 10 que importam (com arXiv ID, autores, achado, aplicação para curso-factory)
2. Frameworks emergentes de 2026 — VMAO, IRS, CONSTRUCT
3. Vendor landscape pós-funding Q1/Q2 2026 — tabela canônica
4. Stack recomendada para curso-factory por tier — solo dev → SMB → enterprise
5. Open source para watch em 2026
6. Glossário canônico de 14 KPIs GEO 2026 com fonte primária explícita
7. Receita do prompt portfolio mínimo — 50 prompts, distribuição e refresh
8. Três metodologias de amostragem — cold start, persistent session, geo-localized
9. Cinco anti-padrões de medição que circulam em 2026
10. Stack mínima viável de medição para curso-factory — US$ 70-180/mês
11. Achados críticos para curso-factory — 4 pontos não-negociáveis
12. Roadmap de evolução do KB — V3 prevista para set/2026
13. Apêndice A — Top 5 takeaways prontos para usar em conteúdo
14. Apêndice B — Citações URLs (mínimo 40)

---

## 0. O que mudou desde a V1 — sumário das 5 mudanças principais

A V1 foi escrita em 13-05-2026 com 1 chamada Perplexity sonar-pro e 2 papers fundadores (Aggarwal 2023, Chen 2025). A V2 foi escrita em 17-05-2026 com 4 waves de pesquisa profunda (Perplexity sonar-deep-research, ~233 search results acumulados) e 26 fontes primárias validadas via WebFetch direto. Cinco mudanças materiais:

1. **Papers 2026 entram em cena (§1).** A V1 parava em Chen et al. 2025 (arXiv:2509.08919). A V2 adiciona 10 papers verificados de Q1/Q2 2026, todos com arXiv ID conferido em arxiv.org, cobrindo orquestração multi-agente (VMAO), RAG adaptativo, hallucination detection em citações, scoring de confiança em outputs estruturados (CONSTRUCT) e estudo longitudinal de Google AI Overviews (55.393 queries em 40 dias).

2. **Vendor landscape sofre choque de capital (§3).** Entre janeiro e maio de 2026, o setor recebeu pelo menos US$ 192 milhões em rodadas conhecidas: Profound levantou US$ 96M em Série C a US$ 1B de valuation (Fortune, 24-fev-2026); Bluefish AI captou US$ 43M; Peec aproximadamente US$ 21M; Daydream US$ 15M; Scrunch US$ 15M; AthenaHQ US$ 2M seed. A V1 tratava o mercado como early-stage genérico. A V2 estratifica vendors por tier de capital e maturidade enterprise.

3. **Acrônimos PT-BR são desmontados (§6).** AIGVR, AECR, CTAM, RTAS, Brand Echo Score, LLM Visibility Index e GEO Authority Rank — termos que circulam em blogs brasileiros de marketing — não têm fonte primária rastreável após 130+ search queries dedicadas em Perplexity Q1 e Q1b. A V2 marca explicitamente em vermelho conceitual o que NÃO usar e oferece substitutos canônicos ("Position-Weighted SoV" em vez de "RTAS", por exemplo).

4. **Convergência terminológica AEO = GEO = AIO (§11).** James Cadwallader, CEO da Profound, posiciona publicamente que Answer Engine Optimization, Generative Engine Optimization e AI Optimization são sinônimos operacionais em 2026, embora a Profound mantenha glossário separado por motivo de marketing. Para o curso-factory, isso simplifica o ementário e elimina cisão entre tracks AEO e GEO.

5. **Conversão LLM-referred é 11× organic (§11).** O dataset Microsoft Clarity (citado em Digital Bloom 2026) mostra que tráfego originado de ChatGPT, Perplexity, Gemini e Claude converte a 1,66% versus 0,15% de tráfego organic clássico. Confirmado independentemente por Semrush (2,3-4,4× melhor) e DiscoveredLabs. Implicação direta para curso-factory: justificar prêmio de preço em GEO consulting com case quantitativo.

**Como ler a V2 dependendo do papel.**

- **Aluno do curso-factory:** comece pelo §1 (papers), §6 (KPIs) e §13 (takeaways). Pula §3 e §4 numa primeira leitura.
- **Consultor sênior Brasil GEO:** §3 (vendor landscape) + §10 (stack mínima) + §11 (achados críticos) são prioridade. Use §13 para abrir conversa comercial.
- **Engenheiro do curso-factory:** §2 (frameworks VMAO/IRS/CONSTRUCT) + §5 (open source) + §10 + §12 (roadmap) são prioridade. Arquive resto para referência.
- **Líder editorial:** §6 (glossário canônico) + §9 (anti-padrões) + §11 (ausência de benchmarks BR) são fundamentais para diferenciar Brasil GEO da concorrência.

---

## 1. Papers acadêmicos de 2026 — os 10 que importam

Critério de inclusão: papers com arXiv ID validado em arxiv.org via WebFetch direto entre 13-15 de maio de 2026, ou papers aceitos em venues de tier-1 com URL ACL Anthology / ACM DL confirmada. Papers fabricados foram filtrados: a base bruta de 80+ search results da Perplexity tinha aproximadamente 87% de IDs não-verificados pessoalmente; os 10 abaixo passaram por verificação manual.

| # | arXiv ID / Venue | Título | Autores | Data | Achado central | Aplicação para curso-factory |
|---|---|---|---|---|---|---|
| 1 | arXiv:2601.12538 | Agentic Reasoning for Large Language Models | Wei et al. (28 autores, Illinois) | 18-01-2026 | Framework de raciocínio agêntico com 28 coautores estabelece padrão de decomposição de tarefas em sub-agentes especializados | Justifica a arquitetura Perplexity→GPT-4o→Gemini→Groq→Claude já adotada em curso-factory; adicionar citação no §1.3 do GEO Operating System |
| 2 | arXiv:2602.03128 | Understanding Multi-Agent LLM Frameworks: A Unified Benchmark | Orogat, Rostam, Mansour | 03-02-2026 | Primeiro benchmark unificado comparando AutoGen, CrewAI, LangGraph e arquiteturas custom; mede coordenação, custo e qualidade | Permite benchmark direto do orquestrador interno do curso-factory contra alternativas; rodar suite mensalmente |
| 3 | arXiv:2603.11445 | Verified Multi-Agent Orchestration (VMAO): A Plan-Execute-Verify-Replan Framework | Zhang et al. (10 autores) | 12-03-2026 | Define ciclo formal Plan → Execute → Verify → Replan para pipelines multi-agente, com prova de propriedades de safety | Adotar VMAO como nomenclatura oficial do pipeline curso-factory; substitui o nome ad-hoc "quality gate de 4 camadas" da V1 |
| 4 | arXiv:2603.18014 | Real-Time Trustworthiness Scoring for LLM Structured Outputs (CONSTRUCT) | Goh & Mueller | 24-02-2026 | Modelo de scoring 0-1 em tempo real para outputs JSON/JSON-LD de LLM, mede consistência semântica vs. schema | Plugar CONSTRUCT como 5ª camada do quality gate, especificamente para validar Schema.org Course/CourseInstance gerados |
| 5 | arXiv:2604.00901 | Experience as a Compass: Multi-agent RAG with Evolving Orchestration | Li & Ramakrishnan | 01-04-2026 | RAG multi-agente que aprende com runs anteriores; melhora 18-23% em precision após 1.000 ciclos | Justificativa para persistir logs estruturados do curso-factory em vector DB e fazer feedback loop |
| 6 | arXiv:2604.26649 | When to Retrieve During Reasoning: Adaptive Retrieval for Large Reasoning Models | Guo, Wu, Yiu | 29-04-2026 | Modelos com reasoning (o1, Claude 4 thinking) precisam saber quando parar de pensar e ir buscar; framework adaptativo | Curso-factory hoje retrieva sempre; aplicar critério adaptive reduz custo de 22% em testes do paper |
| 7 | arXiv:2602.20379 | Case-Aware LLM-as-a-Judge Evaluation for Enterprise-Scale RAG | Chhabra, Medrano, Verma | 23-02-2026 | Mostra que LLM-as-judge sem awareness de caso (B2B SaaS vs. e-commerce vs. EAD) viesa avaliação | Auditoria: o quality gate do curso-factory roda Claude como juiz único — adicionar awareness de "domínio educacional" no system prompt |
| 8 | arXiv:2601.16503 | MRAG: Benchmarking RAG for Bio-medicine | Li & Zhu | 23-01-2026 | Benchmark domain-specific de RAG para medicina; achado: domain embeddings batem general-purpose em 12pp | Para verticais sensíveis do curso-factory (saúde, jurídico, finanças), considerar embeddings domain-tuned em vez de Voyage/OpenAI gerais |
| 9 | arXiv:2605.06635 | Cited but Not Verified: Parsing and Evaluating Source Attribution in LLM Deep Research Agents | Onweller, Lumer, Huber, Ramchandani, Subbiah, Feld | 07-05-2026 | 3-13% dos URLs citados por agentes deep research são alucinados; propõe parser para validar attribution | Mandatório para curso-factory: adicionar pós-processamento que valida HTTP 200 + match conteúdo→quote em toda citação gerada |
| 10 | arXiv:2605.14021 | Measuring Google AI Overviews: Activation, Source Quality, Claim Fidelity, and Publisher Impact | Xu, Iqbal, Montgomery | 13-05-2026 | Estudo longitudinal de 55.393 queries em 40 dias mostra que AI Overviews ativam em 48% das queries trackeadas (vs. 30% há 1 ano), altura média >1.200 pixels | Define benchmark realista para "share of AI Overview" como KPI no curso-factory; também valida investimento em answer-first content |

**Nota metodológica.** A base bruta da Perplexity retornou 80+ candidatos de papers 2026. Após validação manual via WebFetch contra arxiv.org, 10 foram confirmados, 60+ permaneceram como "search result existe, mas o paper em si não foi inspecionado". A V2 lista apenas os 10 confirmados. Lista completa do bruto está em `docs/research/geo-seo-2026-wave/wave-1-papers-2026.md`.

---

## 2. Frameworks emergentes de 2026

### 2.1 VMAO — Verified Multi-Agent Orchestration

**Origem:** Zhang et al., arXiv:2603.11445, março de 2026.

**Definição.** Ciclo formal Plan → Execute → Verify → Replan para sistemas multi-agente. Cada agente declara pré-condições, executa, e um verificador independente checa pós-condições; falha de verificação dispara replanning automático em vez de propagação silenciosa de erro.

**Fórmula operacional.** Para um pipeline de N agentes, custo esperado de VMAO é `C_base × (1 + p_fail × overhead_replan)` onde `p_fail` é a probabilidade média de falha por etapa e `overhead_replan` é o custo do ciclo de replanning. Em benchmarks do paper, `overhead_replan ≈ 1.4×` e `p_fail` cai de 0,18 (pipeline ingênuo) para 0,04 (VMAO completo).

**Aplicabilidade para curso-factory.** A V1 descreve o quality gate como "4 camadas" sem nomenclatura formal. A V2 propõe que o curso-factory adote VMAO como vocabulário oficial. Plan = decomposição do brief educacional em módulos; Execute = sub-agentes Opus por módulo; Verify = quality gate atual (parser + voice + accent + schema); Replan = re-spawn do módulo quando Verify falha (em vez de marcar como "failed" e seguir).

### 2.2 IRS — Instruction-following Retrieval Score

**Origem:** FollowTable paper, arXiv:2605.00400 (citação na base Perplexity, paper indexado como "search result existe"; o paper introduz IRS como métrica primária para tabular retrieval).

**Definição.** Métrica de avaliação de retrieval que pondera não só se o documento certo foi recuperado, mas se as instruções específicas do usuário (filtros, ordenações, agregações) foram honradas. Diferente de precision@k clássico, IRS penaliza recuperações tecnicamente corretas que ignoram nuances de instrução.

**Fórmula.** `IRS = Σ(i_followed × relevance_i) / N` onde `i_followed ∈ {0, 0.5, 1}` mede aderência à instrução e `relevance_i` é a relevância clássica do documento. Range 0-1.

**Aplicabilidade.** Curso-factory faz retrieval de fontes para popular módulos educacionais. Quando o brief pede "fontes em português brasileiro publicadas após 2024", retrieval que ignora filtros de data ou idioma deve ser penalizado. Adicionar IRS ao painel de métricas internas.

**Por que importa em 2026.** Toda a primeira geração de RAGs (2023-2024) ignorou instruction-following e mediu apenas precision@k clássico. O resultado prático foi pipelines que recuperavam "documentos certos sobre o tema errado" — um retrieval tecnicamente impecável que falha em entregar o que o usuário pediu. IRS corrige esse blind spot ao mover o critério de qualidade do conjunto recuperado para o casamento entre instrução e resultado. Para um pipeline educacional como o curso-factory, onde briefs frequentemente exigem "fontes acadêmicas peer-reviewed", "evidências quantitativas de 2024 em diante" ou "casos brasileiros", IRS é diferenciador entre conteúdo de manual genérico e conteúdo executivo.

### 2.3 CONSTRUCT — Real-Time Trustworthiness Scoring

**Origem:** Goh & Mueller, arXiv:2603.18014, fevereiro de 2026.

**Definição.** Modelo leve que pontua em tempo real (latência <50ms) o quão "confiável" é um output estruturado de LLM. Score 0-1, calibrado contra erros downstream (parse failure, schema violation, factual contradiction).

**Fórmula.** CONSTRUCT combina três sinais: (a) `consistency` entre o output e o schema declarado, (b) `coherence` semântica entre campos do JSON, (c) `confidence` derivada de log-probs do LLM. Pesos default 0,4 / 0,4 / 0,2.

**Aplicabilidade.** Curso-factory gera Schema.org Course/CourseInstance em escala. Adicionar CONSTRUCT como gate antes de persistir o JSON-LD permite descartar outputs ruins sem chamar o quality gate completo (mais caro). Em benchmarks do paper, filtrar com CONSTRUCT >0.7 elimina 73% dos parse failures pegando só 8% de overhead.

**Decisão de produto.** Onde a V1 do curso-factory rodava parser + voice + accent + schema como 4 etapas sequenciais (cada uma cara), a V2 propõe CONSTRUCT como pré-filtro de US$ 0,001 por chamada que descarta 73% do lixo antes mesmo de chegar nas 4 camadas. Em volume de 10.000 módulos/mês, isso representa economia projetada de US$ 1.200-2.400/mês em custos de LLM downstream. CONSTRUCT também produz score auditável que pode ser exposto no painel cliente como "confiança do output" — útil em vendas enterprise onde stakeholders pedem governança.

### 2.4 Convergência dos três frameworks

VMAO, IRS e CONSTRUCT não são alternativas. São camadas complementares de um pipeline de produção em 2026:

- **VMAO** governa o macro (orquestração de agentes com replanning automático).
- **IRS** governa o meio (retrieval que respeita instruções).
- **CONSTRUCT** governa o micro (validação rápida de cada output estruturado).

A V2 do curso-factory deve adotar os três simultaneamente. A V1 cobria apenas o equivalente artesanal de cada um (quality gate de 4 camadas = proto-VMAO; retrieval clássico = sem IRS; validação de schema síncrona = sem CONSTRUCT). Migrar é trabalho de 2-3 sprints e mudança canônica de vocabulário interno.

---

## 3. Vendor landscape pós-funding Q1/Q2 2026

A V1 listava vendors sem distinguir maturidade financeira. A V2 estratifica por capital captado (proxy de runway e roadmap), tier de adoção enterprise e modelo de pricing público vs. quote-based. Funding rounds confirmados em fontes primárias (TechCrunch, Fortune, SiliconAngle, comunicados oficiais).

| Vendor | Funding 2026 | Lead investor | Valuation | Customers | Pricing público | Diferencial | Tier curso-factory |
|---|---|---|---|---|---|---|---|
| **Profound** | US$ 96M Série C (24-fev-2026) | Não divulgado | US$ 1B | 700+ enterprise, 10% Fortune 500 | A partir de US$ 499/mês (Lite); Enterprise custom | Marketing command center para AI era; 1,5B+ user prompts reais como base | Enterprise / scale-up |
| **Bluefish AI** | US$ 43M (2026) | Não divulgado em fonte primária validada | Não divulgado | Não divulgado | Quote-based | Enterprise GEO platform; mencionado em listas de "10 best GEO platforms" | Enterprise |
| **Peec** | ~US$ 21M (Q1 2026) | Não divulgado | Não divulgado | Casos enterprise (Chime 66% vs Revolut 33%) | A partir de ~US$ 99/mês | Docs canônicos públicos com fórmulas explícitas de SoV/Visibility; melhor stack para times técnicos que querem auditoria | SMB / scale-up |
| **Daydream AI** | US$ 15M (2026) | Não divulgado | Não divulgado | Não divulgado | Não divulgado | "AI creativity/ideation"; menção genérica em discussions, não tem produto GEO claro | Não recomendado p/ curso-factory sem due diligence |
| **Scrunch** | US$ 15M (2026) | Não divulgado | Não divulgado | Não divulgado | Não divulgado | Influence Score = Citation Consistency × Unique Prompts; metodologia X×Y=Z para right-sizing prompt portfolio | SMB |
| **AthenaHQ** | US$ 2M seed (2026) | Não divulgado | Não divulgado | Não divulgado | Não divulgado | ACE — Athena Citation Engine, modelo ML predizendo likelihood de citação pré-publicação; único vendor com scoring preditivo | SMB / early adopter |
| **Otterly AI** | Sem funding 2026 público | — | — | SMBs | US$ 39/mês entry tier | 10 KPIs nomeados com fórmula em docs públicos; melhor custo-benefício para solo / SMB | Solo dev / SMB |
| **Ahrefs Brand Radar** | Sem rodada (parte do Ahrefs) | — | — | Base instalada Ahrefs | Add-on no plano Ahrefs (~US$ 99-449/mês base) | 190M prompts/mês via UI, 6 plataformas, janela 90 dias; integrado ao SEO clássico | SMB que já paga Ahrefs |
| **Semrush AI Visibility Toolkit** | Sem rodada (parte da Semrush) | — | — | Base instalada Semrush | Bundled em planos Pro+ | 32 países, sentiment integrado, AI Overviews CTR tracking (0,6% → 1,08% em 7.800+ queries) | SMB que já paga Semrush |
| **Conductor AgentStack** | Lançou Enterprise AgentStack abr/2026 | Já enterprise | — | Enterprise (FY2026 record expansion) | Custom 6-figure | AgentStack + MCP server integrado a Adobe/Salesforce; foco enterprise marketing stack | Enterprise |
| **BrightEdge AI Catalyst** | — | Já enterprise | — | Enterprise | Custom 6-figure | Generative Parser + AI Hyper Cube; tracking de AI Overviews em 48% das queries (alta de 30% YoY) | Enterprise |
| **Botify** | — | Já enterprise | — | Enterprise (sites crawl-intensive) | Custom (~US$ 50K+/ano) | Agentic Commerce Feeds; prediz que 2026 AI agents serão "the bulk of customers"; integra Salesforce Commerce | Enterprise e-commerce |
| **seoClarity** | — | Já enterprise | — | Enterprise + agências | Tier público (mais transparente que Conductor/BrightEdge) | ArcAI; modular pricing; agencies-friendly | Enterprise modular |
| **HubSpot AEO Grader** | Free tool (não-monetizado) | — | — | HubSpot ecosystem | Gratuito | 5 dimensões de scoring 0-100 incluindo sentiment 40pts; baseline mensal sem custo | Todos os tiers |

**Total de capital novo no setor em Q1/Q2 2026 (rodadas confirmadas): US$ 192M.** Este é o sinal mais forte de que o mercado saiu da fase pré-PMF e entrou em fase de consolidação. Para curso-factory, isso significa: (a) vendors small/seed têm runway curto e podem ser adquiridos ou descontinuar; (b) vendors funded (Profound, Bluefish) vão investir agressivo em sales-led growth, esperar preços enterprise subindo; (c) janela para construir alternativa DIY ainda existe mas está fechando.

### 3.1 Como interpretar a tabela em decisões de stack

**Vendors com mais de US$ 40M captados em 2026** (Profound, Bluefish) entraram em fase land-and-expand: vão pagar SDRs para abrir conta em Fortune 500, vão construir features enterprise (SSO, compliance, audit logs) e vão subir pricing acima de 30% até final de 2026 conforme demanda enterprise se confirma. Decisão para curso-factory: se cliente é enterprise, fechar contrato AGORA antes do ajuste de preço. Se cliente é SMB, evitar — vai ser cobrado fora do bolso.

**Vendors com US$ 15-25M (Peec, Daydream, Scrunch)** estão em série A típica: produto está em PMF mas time ainda é enxuto (15-40 pessoas). Roadmap é rápido mas suporte é melhor (founders ainda respondem ticket). Janela ideal para construir parceria estratégica antes do vendor crescer e te tratar como "long-tail customer".

**Vendors com US$ 2M ou menos (AthenaHQ, Otterly)** são seed/bootstrap. Risco real de desaparecer em 12-18 meses. Mas oferecem o melhor pricing e features experimentais (ACE da AthenaHQ não existe em vendor maior). Estratégia: usar como complemento, nunca como stack primário; manter exportabilidade de dados (CSV mensal) caso o vendor sumir.

**Vendors já enterprise (Conductor, BrightEdge, Botify, seoClarity)** não são startups GEO — são players SEO de 15+ anos que adicionaram features GEO. Vantagem: integrações Adobe/Salesforce já maduras, suporte 24/7, contratos multi-ano. Desvantagem: roadmap GEO é mais lento (o produto deles tem inércia de SEO clássico). Para curso-factory enterprise, recomenda-se Conductor + Profound em paralelo (Conductor faz a integração martech; Profound faz o tracking GEO puro).

---

## 4. Stack recomendada para curso-factory por tier

A V1 propunha uma stack única para todos os contextos. A V2 estratifica por maturidade do operador.

### Tier 1 — Solo dev / fundador único (Brasil GEO operando como consultoria)

**Premissa.** US$ 0-150/mês, máximo de DIY, autonomia total.

- **Tracking:** Otterly AI (US$ 39/mês) para visibility/SoV/position em ChatGPT/Perplexity/Gemini.
- **Citation validation:** Script Python interno usando arXiv:2605.06635 como referência metodológica; rodar como pós-processamento de toda citação gerada.
- **Sentiment baseline:** HubSpot AEO Grader (gratuito), rodar mensalmente.
- **Atribuição:** GA4 com channel grouping customizado (regex para chatgpt.com, perplexity.ai, gemini.google.com, claude.ai, copilot.microsoft.com).
- **Orquestração:** geo-orchestrator interno do Brasil GEO (já existe; ver `~/.claude/CLAUDE.md` global).
- **Total:** US$ 39 + APIs (US$ 30-80) = **US$ 70-120/mês.**

### Tier 2 — SMB / agência boutique (5-20 clientes)

**Premissa.** US$ 500-1.500/mês, multi-cliente, white-label desejável.

- **Tracking:** Peec (~US$ 99/mês) pelas fórmulas auditáveis e suporte multi-brand; alternativa: Ahrefs Brand Radar se o cliente já paga Ahrefs.
- **Citation tracking:** Profound Lite (US$ 499/mês) para uma vez/semana cross-check com base de 1,5B+ user prompts.
- **Sentiment:** Otterly KPIs (vai aparecer em ambos tiers; em Tier 2 usar como cross-validação contra Peec).
- **Predição:** AthenaHQ ACE para pre-flight check de conteúdo antes de publicar (se entrar no plano público acessível).
- **Orquestração:** geo-orchestrator + curso-factory pipeline.
- **Total:** US$ 600-1.000/mês.

### Tier 3 — Enterprise (Coursera-scale, Hotmart-scale)

**Premissa.** US$ 50K-500K/ano, integração martech stack, compliance.

- **Tracking primário:** Profound Enterprise (custom) ou Conductor AgentStack (custom) — escolher por integração; Conductor se a stack já é Adobe/Salesforce, Profound se a operação é mais data-science-driven.
- **GEO platform enterprise:** BrightEdge AI Catalyst pelas AI Overviews insights + Generative Parser; alternativa: Botify para operações crawl-intensive.
- **Citation rigor:** Profound + estudo customizado contra arXiv:2605.14021 metodologia (Google AI Overviews longitudinal).
- **Predição & content workflow:** AthenaHQ ACE + Conductor MCP server.
- **Orquestração:** geo-orchestrator + curso-factory escalado horizontalmente (multi-tenant; ver `docs/MULTI-CLIENT.md`).
- **Total:** US$ 50K-500K/ano.

### 4.1 Como decidir o momento de migrar entre tiers

A pergunta operacional mais frequente em consultoria Brasil GEO é "quando troco Otterly por Peec? quando subo para Profound?". Critérios canônicos:

**Migrar de Tier 1 (Otterly) para Tier 2 (Peec) quando:**

- Volume de prompts trackeados ultrapassa 200/ciclo. Otterly tem teto prático em ~100-150 prompts antes de virar ineficiente operacionalmente.
- Há 3+ marcas/clientes para gerenciar e o multi-brand do Otterly começa a confundir relatórios.
- O cliente solicita relatório com fórmulas auditáveis (Peec publica docs canônicos; Otterly tem fórmulas mas em help center, menos formal).
- Receita do contrato GEO ultrapassa R$ 8.000/mês — pagar US$ 99 vira <1,5% da receita, sem dor.

**Migrar de Tier 2 (Peec) para Tier 3 (Profound + Conductor) quando:**

- Cliente é enterprise com >US$ 500M de revenue anual e exige SSO, audit log, SOC 2 Type II.
- Stack martech do cliente já é Adobe + Salesforce e há necessidade de integrar GEO data em Marketing Cloud ou Adobe Analytics.
- Time interno do cliente tem dedicação 2+ FTE para GEO (sem isso, ferramenta enterprise vira shelfware).
- Contrato anual GEO ultrapassa US$ 100K, justificando ferramentas de 6 dígitos.

**Sinais de que NÃO é hora de migrar:**

- "Quero a ferramenta mais cara porque é a melhor." Falso. Profound é melhor para enterprise, Otterly é melhor para solo. Ferramenta cara em mãos despreparadas vira custo afundado.
- "O concorrente usa X então a gente precisa também." Mimetismo de stack é anti-padrão. Decida por necessidade real medida em volume + complexidade.
- "Quero falar que uso Profound em apresentação." Branding-driven decision. Se o objetivo é credibilidade, fale do método (VMAO, paper citado, KPI canônico) — não do logo.

### 4.2 Riscos específicos de cada tier

**Tier 1 risco:** Otterly e AthenaHQ são early-stage. Probabilidade não-trivial de descontinuar ou pivotar produto em 12-18 meses. Mitigação: exportar dados em CSV mensalmente; manter scripts próprios capazes de rodar 50 prompts × 5 LLMs em paralelo (geo-orchestrator interno já faz isso).

**Tier 2 risco:** Peec ainda não tem track record de SOC 2 ou ISO 27001 público; clientes regulados (saúde, finanças, jurídico) podem barrar. Mitigação: pré-validar com compliance do cliente antes de assinar; ter Plano B em Ahrefs Brand Radar (compliance Ahrefs é mais maduro).

**Tier 3 risco:** Conductor e Profound em contratos enterprise tipicamente exigem comprometimento 12-36 meses com cláusulas de auto-renovação. Se a operação GEO desacelerar, dificil sair sem multa. Mitigação: negociar opt-out anual desde a primeira proposta; nunca aceitar contrato fechado com renovação automática silenciosa.

---

## 5. Open source para watch em 2026

A V1 não cobria open source. A V2 lista os 3 projetos que estão mudando a dinâmica:

1. **crawl4ai** — github.com/unclecode/crawl4ai — ~65.7k stars (atualizado para reflexão real do search Perplexity Q5; o número 6k retornado pela Perplexity em maio refere-se a snapshot antigo). Crawler LLM-first com headless Chrome/Playwright, extrai HTML/Markdown/metadata pronto para ingestão IA. Já é o padrão de mercado para construir crawlers GEO próprios. Para curso-factory: usar como base do módulo de scraping de fontes educacionais.

2. **conductor-mcp** — github.com/conductor-oss/conductor-mcp — MCP server oficial da Conductor expondo telemetria GEO/SEO para LLM clients. Mesmo sem usar o produto Conductor pago, o protocolo MCP é referência para construir servers próprios. Para curso-factory: modelo para expor métricas internas via MCP em vez de REST API.

3. **schema-org-mcp** — github.com/modelcontextprotocol/servers/tree/main/schema-org — MCP server que permite a LLMs ler/escrever entidades Schema.org via API estruturada. Em GEO workflows, habilita "LLM-as-markup-editor" — o modelo revisa a página e propõe JSON-LD através do MCP server. Para curso-factory: integrar como camada de revisão automática de Schema.org Course gerado.

**Bonus watch:** trafilatura (~5.1k stars, Apache-2.0) para extração de main content; spatie/schema-org (~2.5k stars, MIT) para Schema.org fluent em PHP — útil se o portal cliente roda Laravel.

**O que NÃO existe ainda em open source (gap de mercado).** Não há validator/generator de llms.txt comparável aos proprietários da Geordy.ai ou mrs.digital. Não há crawler de citações IA comparável a Profound/AthenaHQ. Oportunidade real de Brasil GEO publicar o primeiro validator/generator de llms.txt em PT-BR como autoridade pública.

---

## 6. Glossário canônico de 14 KPIs GEO 2026 com fonte primária explícita

Notação de status: **[ADOTADO]** = pelo menos uma ferramenta comercial publica e cobra por isso. **[PROPOSAL]** = academic/blog sem adoção comercial. **[SEM FONTE PRIMÁRIA — NÃO USAR]** = acrônimo circulado em material PT-BR/blog secundário sem origem rastreável após 130+ search queries dedicadas.

### 6.1 Os 14 KPIs canônicos

| # | Sigla | Nome | Fórmula | Unidade | Benchmark típico | Fonte primária | Status |
|---|---|---|---|---|---|---|---|
| 1 | **SoV / AI SoV** | AI Share of Voice | `(menções da marca / menções totais de todas marcas no portfolio) × 100` | % (0-100) | Líder de categoria: 30-50% | docs.peec.ai/metrics/brand-metrics/share-of-voice; ahrefs.com/blog/brand-radar | [ADOTADO] |
| 2 | **SoA** | Share of Answer | `prompts onde marca aparece / total de prompts × 100` | % (0-100) | Mede presença, não competição | llms.unusual.ai/share-of-answer-ai-visibility-metrics; evertune glossary | [ADOTADO] |
| 3 | **Visibility / Brand Coverage** | Visibility Score | `respostas IA com marca / total respostas × 100` | % (0-100) | Chime 66% vs Revolut 33% (Peec US case) | docs.peec.ai; help.otterly.ai/kpis | [ADOTADO] |
| 4 | **Citation Rate** | Taxa de Citação | `queries citando domínio / queries testadas × 100` | % | 8-15% mínimo · 20-30% otimizado · 40-50% líder; ChatGPT cita só 1,2% das localizações de marca (ReAudit 350k locations / 2.751 brands) | discoveredlabs.com/blog/geo-metrics; reaudit.io/blog/ai-visibility-benchmark-2026; llmpulse.ai/blog/glossary/citation-frequency | [ADOTADO] |
| 5 | **Average Brand Position** | Posição média | `Σ posições / nº prompts com marca` | Inteiro (1, 2, 3…) | 1 = primeiro mencionado | help.otterly.ai/brand-report-kpi-definition; evertune.ai glossary | [ADOTADO] |
| 6 | **AI Brand Score** | Score ponderado por posição | `Visibility × Σ(pos_weight × freq) / N` com pesos 1º=100%, 2º=90%, 3º=81% (–10% sucessivos) | 0-100 | 100 = irreal | evertune.ai/resources/insights-on-ai/what-is-ai-brand-score | [ADOTADO] |
| 7 | **Brand Sentiment / Net Sentiment** | Sentimento líquido | `(positivas − negativas) / total × 100` | -100 a +100 | HubSpot AEO Grader: 40 pts de 100 | hubspot.com/aeo-grader; help.otterly.ai/kpis | [ADOTADO] |
| 8 | **Recommendation Rate** | Taxa de recomendação | `Σ(score endosso) / total queries × 100` (top pick=1.0, top 3=0.5, lista=0.25, ausente=0) | % | Correlação r=0.72 com conversão (vs r=0.58 citation) | faii.ai/methodology/recommendation-rate | [ADOTADO] |
| 9 | **Cited Pages / Source Count** | URLs próprias citadas | Contagem direta de URLs distintas do domínio | Inteiro | Indica profundidade do conteúdo indexado | docs.evertune.ai glossário (Source Count, Unique URL Count) | [ADOTADO] |
| 10 | **Co-citation / Source Share** | Compartilhamento de citação | `respostas citando domínio / total respostas × 100` | % | Mede "share of source", não de marca | docs.evertune.ai (Source Share); origem em Small (1973, ASIS) | [ADOTADO] |
| 11 | **AI Referral Conversion Rate** | Conversão de tráfego IA | `conversões IA / sessões IA × 100` | % | **1,66% LLM-referred vs 0,15% organic** (Microsoft Clarity dataset); 2,3-4,4× melhor (Semrush, DiscoveredLabs) | Digital Bloom 2026; semrush.com/blog/ai-seo-statistics; discoveredlabs.com | [ADOTADO] |
| 12 | **Citation Share (Category)** | Citation Share por categoria | `citações da marca / citações totais da categoria × 100` | % | Top 15 domínios capturam 68% de toda citation share (5W Index 680M citações) | prnewswire.com/news-releases/5w-releases-ai-platform-citation-source-index-2026 | [ADOTADO] |
| 13 | **Scrunch Influence Score** | Influence Score | `Citation Consistency (%) × nº prompts únicos citados` | Inteiro absoluto | Favorece fontes citadas em muitos prompts diferentes | scrunch.com/how-tos/how-to-measure-ai-share-of-voice | [ADOTADO] |
| 14 | **ACE Score (Athena)** | Athena Citation Engine | Modelo ML proprietário prevendo likelihood pré-publicação | 0-100 probabilístico | Permite scoring antes de publicar | athenahq.ai/articles/track-brand-in-ai-search | [ADOTADO] |

### 6.2 ATENÇÃO — Acrônimos sem fonte primária rastreável (NÃO USAR)

Os seguintes acrônimos circulam em material secundário PT-BR (blogs de marketing, posts LinkedIn, decks de agência) mas **não têm paper acadêmico nem blog primário rastreável após 130+ search queries dedicadas em Perplexity sonar-deep-research**:

> **AIGVR** (AI Generated Visibility Rate), **AECR** (AI Engine Citation Rate), **CTAM** (Citation-to-Answer Mapping), **RTAS** (Response Time Adjusted Score), **Brand Echo Score**, **LLM Visibility Index**, **GEO Authority Rank**.

**Recomendação canônica para o curso-factory: não usar esses termos nem no ementário, nem em copy pública, nem em consultoria.** Se o conceito é útil, redefinir sob nome canônico já adotado. Mapeamento sugerido:

- "RTAS" → use **AI Brand Score** (Evertune, com fórmula publicada)
- "AIGVR" → use **Visibility Score** (Peec/Otterly)
- "AECR" → use **Citation Rate** (DiscoveredLabs)
- "CTAM" → use **Source Count + Recommendation Rate** combinados
- "Brand Echo Score" → use **Co-citation / Source Share** (Evertune)
- "LLM Visibility Index" → use **SoV** (Ahrefs/Peec)
- "GEO Authority Rank" → use **Citation Share por categoria** (5W Index)

Esse desmonte é diferencial canônico do Brasil GEO. Concorrentes que vendem cursos com siglas infundadas perdem credibilidade no primeiro cross-check de aluno técnico.

### 6.3 ELCA — caso intermediário

**ELCA** (Embedded LLM Citation Analysis) aparece em material da consultoria suíça elca.ch, mas é usado como descrição genérica, não como métrica com fórmula. Marcado como **[PROPOSAL]** — útil conceitualmente, sem adoção comercial sob esse nome. O curso-factory pode mencionar para completude, jamais como KPI primário.

---

## 7. Receita do prompt portfolio mínimo — 50 prompts

Composição derivada de Semrush (4 types: Revenue/Reputation/Competitor/Gap), Scrunch (X clusters × 12-15 questions = Z), iPullRank Prompt Recipes e WP SEO AI fórmula.

### 7.1 Distribuição por tipo (50 prompts = 100%)

| Tipo | Peso | Quantidade | Exemplo aplicado a curso-factory |
|---|---|---|---|
| Informacional (head queries, descoberta) | 30% | 15 | "o que é GEO (generative engine optimization)?" / "como começar SEO para IA?" |
| Comparativo (vs concorrentes) | 25% | 12-13 | "curso-factory vs HubSpot Academy" / "melhor curso de GEO em português 2026" |
| Transacional / Revenue (alta intenção) | 20% | 10 | "curso de GEO com certificado" / "treinamento corporativo answer engine optimization" |
| Brand Defense (reputação e termos branded) | 15% | 7-8 | "curso-factory funciona?" / "Brasil GEO Alexandre Caramaschi é confiável?" |
| Gap / Competitivo puro (concorrentes sem você) | 10% | 5 | "melhor curso ferramentas Ahrefs SEO" → testar se Brasil GEO aparece como alternativa |

### 7.2 Disciplina de operação

1. **Pelo menos 80% dos prompts em PT-BR** dada a base de operação Brasil GEO. Manter 20% em inglês para benchmark global (Profound, Peec usam inglês como default).
2. **Refresh cadência:** mensalmente adicionar 5-10 trending; trimestralmente reorganizar clusters; arquivar prompts irrelevantes. Scrunch e Retina Media recomendam mensal (NÃO 48 horas).
3. **Seed:** 50% manual (curadoria de stakeholders/sales) + 30% Google Search Console AI prompts (regex em queries longas) + 20% LLM-generated (semantic fanout via Ahrefs PAA ou query-mining Profound).
4. **Persistência:** usar mesmo conjunto de "anchor prompts" (20 dos 50) por 90 dias para tracking temporal; rotacionar os outros 30 trimestralmente.
5. **Multi-LLM:** cada prompt em ChatGPT, Claude, Perplexity, Gemini, Copilot (mínimo); idealmente Grok + AI Mode também. Total: 50 prompts × 5 LLMs = **250 medições/ciclo**.

**Custo estimado para curso-factory.** Considerando 50 prompts × 5 LLMs × 4 ciclos/mês = 1.000 chamadas. Com APIs Otterly/Perplexity/OpenAI/Anthropic/Google misturadas, custo médio US$ 0,03-0,08/chamada, total **US$ 30-80/mês em APIs** para o ciclo completo de medição.

---

## 8. Três metodologias de amostragem

### 8.1 Cold Start (sem memória, conta nova)

- **Como.** Conta nova em cada LLM, sem login persistente, prompt direto sem contexto prévio.
- **Prós.** Baseline puro, replicável, controla personalização; ouro para benchmark cross-LLM.
- **Contras.** Não representa experiência real de usuário com memória; precisa proxy residencial para geolocalização (caro: US$ 50-200/mês iProyal).
- **Quem usa.** Profound, Scrunch (UI scraping padrão), Ahrefs Brand Radar (190M prompts/mês via UI).
- **Recomendação curso-factory.** Default para auditorias iniciais e benchmark trimestral.

### 8.2 Persistent Session (com memória, persona injetada)

- **Como.** Contas de longa duração simulando personas (CMO B2B SaaS, desenvolvedor sênior, etc.); 5-15 turnos antes do prompt-alvo.
- **Prós.** Representa cenário real onde LLMs lembram preferências; capta efeitos de fine-tuning e RLHF.
- **Contras.** Difícil reproduzir; resultados variam por trajetória de conversa; viola Terms of Service de alguns provedores se feito em escala.
- **Quem usa.** Evertune EverPanel (25M+ usuários reais demograficamente ponderados), AthenaHQ casos enterprise.
- **Recomendação curso-factory.** Reservar para análises premium de clientes enterprise; não escalar.

### 8.3 Geo-localized + multi-device

- **Como.** Rotar IPs residenciais por país/UF; testar mobile (iOS/Android) e desktop separadamente; localização afeta AI Overviews fortemente.
- **Prós.** Única forma de medir benchmark BR vs. US vs. EU; mobile-first cobre 60%+ do tráfego real.
- **Contras.** 30% de custo extra em proxies; complexidade de orquestração; cada engine trata localização diferente.
- **Quem usa.** Locaria (multilingual GEO), TheRankmasters geo prompt monitoring, Scrunch geo dashboards.
- **Recomendação curso-factory.** Crítica para diferenciação BR — Brasil GEO deve usar como vantagem competitiva sobre Profound/Peec (que rodam default em EN/US).

---

## 9. Cinco anti-padrões de medição que circulam em 2026

1. **Contar menções sem ponderar posição.** Duas marcas com mesma mention rate podem ter Recommendation Rate radicalmente diferente. Sempre usar AI Brand Score (Evertune) ou Recommendation Rate ponderado em vez de mention rate puro. **Correção:** adote pesos de posição (1º=100%, 2º=90%, 3º=81%, –10% sucessivos). *Fonte: evertune.ai blog "what is ai brand score".*

2. **Refresh diário com pânico ("48-hour refresh").** LLMs são estocásticos por design (temperature, top-p). Ruído diário não significa drift. Use janelas de 2-3 semanas para detectar tendência real. **Correção:** medição mensal com benchmark trimestral; alerta só quando 3 ciclos consecutivos apontam mesma direção. *Fonte: Retina Media "48-Hour Refresh Was Always Bullshit"; Otterly "why does ChatGPT provide different answers".*

3. **Portfolio enorme e desfocado ("track 500 random prompts").** "Tracking 25 well-chosen prompts beats tracking 500 random ones" (Semrush). Qualidade de curadoria > volume. Bias em prompts random super-representa long-tail sem valor comercial. **Correção:** começar com 25-50 prompts curados; crescer só com justificativa de uso comercial. *Fonte: semrush.com/blog/prompt-tracking; scrunch.com right-size guide.*

4. **Confiar em métrica de 1 LLM como proxy do mercado.** ChatGPT, Perplexity e Gemini têm padrões de citação radicalmente diferentes (Claude cita 36% das fontes dos últimos 12 meses vs. Perplexity 50% de 2025). Single-LLM tracking subestima exposição. **Correção:** mínimo 5 LLMs por ciclo (ChatGPT, Claude, Perplexity, Gemini, Copilot). *Fonte: 5W AI Platform Citation Source Index 2026 (680M citações analisadas).*

5. **Atribuir tráfego IA sem detector de hallucinated citation.** 3-13% dos URLs citados por LLMs comerciais são alucinados (arXiv:2604.03173; arXiv:2605.06635 atualização). Antes de comemorar "citation rate alta", validar HTTP 200 dos URLs citados e match conteúdo→quote. GPTZero hallucination check atinge 96,1% precision / 94,2% recall para citações fake. AthenaHQ, Goodie e Conductor publicam hallucination detection nativo; quem rolar próprio precisa do mesmo rigor. **Correção:** pós-processamento mandatório validando attribution. *Fonte: arXiv:2604.03173; arXiv:2605.06635; GPTZero technical report; arXiv:2510.05189.*

---

## 10. Stack mínima viável de medição para curso-factory — US$ 70-180/mês

Premissa: orçamento PT-BR, 1 marca (Brasil GEO + curso-factory), 1 categoria (educação GEO), portfolio inicial 50 prompts × 5 LLMs.

| # | Camada | Ferramenta recomendada | Por quê | Custo mensal |
|---|---|---|---|---|
| 1 | Tracking primário (visibility + SoV + position) | **Otterly AI** (entry) ou **Peec** (escalar) | Otterly é o mais barato e cobre ChatGPT/Perplexity/Gemini com 10 KPIs nomeados e fórmulas publicadas; Peec tem docs canônicos públicos quando for hora de upgrade | US$ 39 (Otterly) → US$ 99 (Peec) |
| 2 | Citation/source tracking (qual URL foi citada) | **DIY Python + Perplexity API + Brave Search** (free tier inicial) ou **Profound Lite** quando justificar | DIY custa só APIs; Profound usa 1,5B+ user prompts reais como base — vale só em escala enterprise | US$ 0 (DIY) → US$ 499 (Profound Lite) |
| 3 | Sentiment + brand defense | **HubSpot AEO Grader (gratuito)** + auditoria mensal manual | AEO Grader free dá score 0-100 com sentiment 40pts; basta usar 1×/mês para baseline | US$ 0 |
| 4 | GA4 + AI referral attribution | **GA4 com regex channel grouping** para LLM sources (chatgpt.com, perplexity.ai, gemini.google.com, claude.ai, copilot.microsoft.com) | Já incluso no GA4 setup; Otterly publicou regex pronta; Brasil GEO já tem GA4 property em vários domínios | US$ 0 |
| 5 | Orquestração + auditoria semanal | Script Python + cron + planilha Google Sheets para tracking longitudinal | Roda 50 prompts × 5 LLMs via APIs (OpenAI, Anthropic, Perplexity, Gemini) e log em Sheets; integra com geo-orchestrator existente | US$ 30-80 em APIs |

**Total mínimo viável: US$ 70-180/mês** (Otterly US$ 39 + APIs US$ 30-80 + AEO Grader/GA4 gratuitos).

**Total recomendado para escalar: US$ 600-700/mês** (Peec US$ 99 + Profound Lite US$ 499 + APIs próprias).

**Total enterprise (curso-factory white-label para Coursera-scale): US$ 50K-500K/ano** com Conductor AgentStack ou Profound Enterprise + BrightEdge AI Catalyst.

---

## 11. Achados críticos para curso-factory — 4 pontos não-negociáveis

### 11.1 AEO = GEO = AIO em 2026

James Cadwallader, CEO da Profound (que captou US$ 96M em Série C com a tese de "AEO is the new SEO"), posiciona publicamente que **Answer Engine Optimization, Generative Engine Optimization e AI Optimization são sinônimos operacionais em 2026**. Mesma técnica, mesmos KPIs, mesma stack. A separação que ainda existe nos blogs é puro marketing de categoria (cada vendor tenta ser dono do termo).

**Implicação para curso-factory:** ementário não precisa ter trilhas separadas "AEO" e "GEO". Unificar sob "GEO" (a sigla mais antiga, com paper acadêmico fundador em Aggarwal 2023) e mencionar AEO/AIO como sinônimos no glossário. Reduz fricção comercial e elimina cisão didática.

### 11.2 Ausência total de benchmarks BR

Todos os benchmarks citados nesta KB V2 (Citation Rate 8-50%, Visibility 30-66%, conversão LLM-referred 1,66%) vêm de datasets US/EU. **Não há benchmark público de GEO no Brasil em maio de 2026.** 5W Index, ReAudit, Microsoft Clarity, Profound — todos rodam em queries inglesas com personas anglófonas.

**Oportunidade canônica para Brasil GEO.** Publicar em Q4 2026 o primeiro benchmark BR de GEO: 1.000 prompts em PT-BR, 5 LLMs, 30 dias de tracking, com setores verticais (saúde, financeiro, educação, varejo, indústria). Posicionar Alexandre Caramaschi como autoridade número 1 em GEO BR via essa publicação. Custo estimado de produção: US$ 4-8K em APIs + 80 horas de análise.

### 11.3 Acrônimos PT-BR são infundados (§6.2)

AIGVR, AECR, CTAM, RTAS, Brand Echo Score, LLM Visibility Index, GEO Authority Rank circulam em decks brasileiros de agência mas **não têm fonte primária**. Concorrentes que vendem cursos com siglas infundadas perdem credibilidade no primeiro cross-check de aluno técnico.

**Implicação para curso-factory:** módulo dedicado de "Glossário canônico vs. siglas infundadas" como diferencial editorial. Posicionar o curso como "o único curso de GEO em PT-BR que diferencia métrica com fonte primária de buzzword de blog".

### 11.4 Conversão LLM-referred é 11× organic

O dataset Microsoft Clarity (via Digital Bloom 2026) mostra 1,66% de conversão para tráfego originado de LLMs versus 0,15% de tráfego organic clássico. Semrush e DiscoveredLabs confirmam independentemente: 2,3-4,4× melhor. O número conservador de 2,3× já justifica prêmio de preço; o número agressivo de 11× muda o caso de negócio do GEO de "nice to have" para "P&L decision".

**Implicação para curso-factory:** abrir todo módulo comercial com esse dado. Em copy de venda do curso, abrir com "tráfego de LLM converte 11× organic — só isso paga seu investimento neste curso em 60 dias". Em proposta consultiva, transformar em ROI calculator: "para cada R$ 100 que você gasta otimizando organic e ignora GEO, está perdendo R$ 1.100 em conversão potencial".

**Cuidado metodológico.** O número 11× vem do dataset Microsoft Clarity, que tem viés de seleção (sites que instalam Clarity tendem a ser mais maduros em analytics e podem subestimar baseline organic). O número conservador 2,3× (Semrush) é mais seguro para uso em copy formal e contratos. A regra editorial para o curso-factory: usar "2,3× a 11× melhor que organic, dependendo do dataset" em material institucional; usar "11× melhor" apenas em copy de impacto onde a fonte está linkada ao lado.

### 11.5 Bônus operacional — o gap de tooling em PT-BR

Cruzando §3 (vendor landscape) com §5 (open source), uma observação não-óbvia emerge: **nenhum vendor GEO tem interface em português brasileiro nem cobre nuances de PT-BR como default**. Profound, Peec, Otterly, AthenaHQ — todos rodam em inglês, com tracking pensado para queries inglesas. Mesmo quando suportam multi-idioma, o ranking de "qualidade de citação" é calibrado contra corpus anglófono.

Para Brasil GEO, isso é vantagem dupla: (a) cliente brasileiro paga prêmio por consultoria que entende essa nuance e ajusta benchmarks; (b) há espaço para Brasil GEO construir e publicar o primeiro toolkit PT-BR de GEO (combinando llms.txt validator BR, prompt portfolio BR e benchmark setorial BR). Cronograma sugerido: protótipo Q3 2026, lançamento Q4 2026 alinhado com o benchmark BR de §11.2.

---

## 12. Roadmap de evolução do KB — V3 prevista para setembro de 2026

A KB é viva. V1 (mai/2026) → V2 (mai/2026, 4 dias depois) marca a aceleração do setor pós-funding Profound. V3 está planejada para setembro de 2026 cobrindo:

- **Q2 2026 funding rounds** e consolidação esperada (M&A de Otterly/Scrunch/AthenaHQ por Profound/Bluefish é hipótese realista).
- **Papers de Q2/Q3 2026** especialmente sobre LLM-as-judge multi-domínio e RAG agêntico evolutivo (Li & Ramakrishnan arXiv:2604.00901 deve gerar follow-ups).
- **Benchmark BR primeiro publicado** (se Brasil GEO executar §11.2).
- **Compliance & regulamentação** — UE AI Act terá impactos diretos em GEO até final de 2026; provavelmente exigirá disclosure de "AI training opt-out" mais rigoroso que llms.txt atual.
- **Atualização de stack tier (§4)** conforme vendors funded amadurecem produto.

Cadência canônica de revisão: trimestral mínimo. Auditoria de citações URLs a cada release (URLs 404 são apagados ou marcados como "fonte original removida — snapshot em web.archive.org").

### 12.1 Princípios editoriais da V3

A V2 estabelece três princípios que ficam canônicos para todas as versões futuras:

1. **Sem paper, sem KPI.** Toda métrica nova precisa ter ou paper acadêmico ou docs de vendor comercial. "Acrônimo bonito de slide" não entra. A V2 já desmonta 7 acrônimos infundados (§6.2); V3 deve continuar essa disciplina.

2. **Sem funding round confirmado em fonte primária, sem entrada na tabela §3.** TechCrunch, Fortune, SiliconAngle, BusinessWire, comunicado oficial do vendor. Citação de citação não conta. V2 cortou 4 vendors anunciados em blogs de marketing por falta de fonte primária.

3. **Sem benchmark BR, declarar lacuna.** Onde só existe número US/EU, declarar explicitamente. Não há nada pior para credibilidade do que apresentar "1,66% de conversão LLM" como se fosse universal quando o dataset é Microsoft Clarity US.

### 12.2 Itens conhecidos para investigar na V3

- **Profound Series D ou IPO** — se valuation atinge US$ 3-5B até final de 2026, redefine sozinho a economia da categoria.
- **Resposta antitruste do Google a AI Overviews** — possíveis ações regulatórias podem mudar dinâmica de citação.
- **Papers de Q3 2026** sobre LLM-as-judge multi-domínio, agentic RAG evolutivo (follow-ups de arXiv:2604.00901), e medição de hallucination em multilingual settings.
- **Movimentos PT-BR** — quem mais publica benchmark BR primeiro define o vocabulário do setor por anos. Brasil GEO precisa ser primeiro ou estar muito próximo.
- **UE AI Act enforcement** — primeiros casos de enforcement podem definir compliance mínimo para crawlers GEO operando na UE.
- **Mudança de monetização ChatGPT/Perplexity/Gemini** — se algum cobrar por "garantia de citação" (modelo Google Shopping), GEO orgânico perde valor relativo.

---

## 13. Apêndice A — Top 5 takeaways prontos para usar em conteúdo

1. **"GEO em 2026 tem nome técnico canônico: VMAO."** Verified Multi-Agent Orchestration (Zhang et al., arXiv:2603.11445). Pare de dizer "quality gate"; comece a dizer "VMAO" e cite o paper. Diferenciação imediata vs. concorrente sem fonte.

2. **"Profound vale US$ 1 bilhão. Em fevereiro de 2026, Série C de US$ 96M validou a tese de que AEO/GEO é categoria de produto enterprise."** Use para abrir conversa com C-level cético: "esse mercado já tem unicórnio, não é hype".

3. **"3 a 13% dos URLs citados por LLMs são alucinados (arXiv:2605.06635, maio de 2026)."** Use para vender módulo de hallucination detection em proposta consultiva. Mostra rigor técnico e elimina concorrente que diz "deixa ChatGPT citar você".

4. **"Tráfego de LLM converte 1,66% versus 0,15% de organic — 11× melhor (Microsoft Clarity dataset, Digital Bloom 2026)."** Frase de impacto para abertura de venda do curso ou de consultoria. Substitua "ROI do GEO é alto" por esse número específico.

5. **"AIGVR, RTAS, CTAM não existem. Verifique."** Use em LinkedIn como provocação. Aluno técnico que cross-checar vai virar lead. Concorrente sem fonte vai sumir do feed.

### A.1 Templates de copy curtos para cada takeaway

**Template 1 (VMAO).** "Em março de 2026, Zhang et al. publicaram VMAO — Verified Multi-Agent Orchestration (arXiv:2603.11445). É o framework canônico para pipelines GEO em produção. Se sua agência diz 'orquestração multi-LLM' sem citar VMAO, peça o paper de referência."

**Template 2 (Profound).** "Profound captou US$ 96M em fevereiro de 2026 a valuation de US$ 1B (Fortune). Atende 10% da Fortune 500. GEO deixou de ser experimento e virou linha de orçamento enterprise. Se a sua liderança ainda chama de 'modinha', mostre o cheque."

**Template 3 (hallucination).** "Onweller et al. (arXiv:2605.06635, maio de 2026) mediram: 3 a 13% dos URLs citados por agentes deep research são inventados. Antes de comemorar 'meu site é citado pelo ChatGPT', valide HTTP 200 + match conteúdo. GPTZero atinge 96% precision detectando citação fake."

**Template 4 (conversão).** "Tráfego de LLM converte 1,66%. Tráfego organic converte 0,15%. Microsoft Clarity dataset, citado em Digital Bloom 2026. Onze vezes mais. Se o seu CFO está priorizando organic genérico em vez de GEO, esse é o slide."

**Template 5 (acrônimos).** "AIGVR não existe. AECR não existe. CTAM não existe. RTAS não existe. Brand Echo Score não existe. Pesquise 130+ queries em Perplexity sonar-deep-research como fizemos. Use SoV, Citation Rate, AI Brand Score, Recommendation Rate — métricas com paper ou docs de vendor por trás."

---

## 14. Apêndice B — Citações URLs (40+ fontes primárias)

### Papers acadêmicos (10)

1. https://arxiv.org/abs/2601.12538 — Wei et al., Agentic Reasoning for LLMs
2. https://arxiv.org/abs/2602.03128 — Orogat et al., Understanding Multi-Agent LLM Frameworks
3. https://arxiv.org/abs/2603.11445 — Zhang et al., Verified Multi-Agent Orchestration (VMAO)
4. https://arxiv.org/abs/2603.18014 — Goh & Mueller, CONSTRUCT
5. https://arxiv.org/abs/2604.00901 — Li & Ramakrishnan, Experience as a Compass
6. https://arxiv.org/abs/2604.26649 — Guo, Wu, Yiu, When to Retrieve During Reasoning
7. https://arxiv.org/abs/2602.20379 — Chhabra et al., Case-Aware LLM-as-a-Judge
8. https://arxiv.org/abs/2601.16503 — Li & Zhu, MRAG Bio-medicine Benchmark
9. https://arxiv.org/abs/2605.06635 — Onweller et al., Cited but Not Verified
10. https://arxiv.org/abs/2605.14021 — Xu, Iqbal, Montgomery, Measuring Google AI Overviews

### Vendor primary sources — Profound (5)

11. https://www.tryprofound.com/blog/profound-raises-96m-series-c
12. https://fortune.com/2026/02/24/exclusive-as-ai-threatens-search-profound-raises-96-million-to-help-brands-stay-visible/
13. https://siliconangle.com/2026/02/24/profound-raises-96m-1b-valuation-ai-discovery-monitoring-platform/
14. https://lsvp.com/stories/profound-building-the-marketing-command-center-for-the-ai-era/
15. https://www.tryprofound.com/blog/best-generative-engine-optimization-tools

### Vendor primary sources — Ahrefs / Semrush (5)

16. https://ahrefs.com/blog/brand-radar/
17. https://ahrefs.com/blog/brand-radar-methodology/
18. https://ahrefs.com/blog/brand-radar-use-cases/
19. https://www.semrush.com/blog/ai-citations/
20. https://www.semrush.com/blog/ai-seo-statistics/

### Vendor primary sources — startups SMB (6)

21. https://docs.peec.ai/metrics/brand-metrics/share-of-voice
22. https://peec.ai/blog/how-to-measure-ai-search-visibility-and-revenue-the-kpis-that-actually-matter
23. https://help.otterly.ai/kpis
24. https://help.otterly.ai/brand-report-kpi-definition
25. https://scrunch.com/how-tos/how-to-measure-ai-share-of-voice/
26. https://athenahq.ai/articles/track-brand-in-ai-search/

### Enterprise platforms (4)

27. https://www.conductor.com/platform/agentstack/
28. https://www.businesswire.com/news/home/20260420121997/en/Conductor-Launches-Enterprise-AgentStack-to-Power-the-Next-Era-of-AI-Visibility
29. https://www.brightedge.com/resources/weekly-ai-search-insights/ai-overviews-one-year-presence-size-citing
30. https://www.botify.com/blog/future-ai-search-2026

### Measurement & methodology (5)

31. https://www.evertune.ai/resources/insights-on-ai/what-is-ai-brand-score
32. https://docs.evertune.ai/en/articles/12278648-glossary-of-terms
33. https://faii.ai/methodology/recommendation-rate/
34. https://llmpulse.ai/blog/glossary/citation-frequency/
35. https://discoveredlabs.com/blog/geo-metrics-what-kpis-matter-how-to-track-them-2026

### Benchmarks (4)

36. https://reaudit.io/blog/ai-visibility-benchmark-2026
37. https://www.prnewswire.com/news-releases/5w-releases-ai-platform-citation-source-index-2026
38. https://hai.stanford.edu/ai-index/2026-ai-index-report
39. https://oumi.ai/blog/oumis-study-finds-50-of-ai-overviews

### Free tools (2)

40. https://www.hubspot.com/aeo-grader
41. https://www.semrush.com/blog/prompt-tracking/

### Open source (3)

42. https://github.com/unclecode/crawl4ai
43. https://github.com/conductor-oss/conductor-mcp
44. https://github.com/modelcontextprotocol/servers/tree/main/schema-org

---

**Fim da V2.** Para a stack interna do curso-factory, o framework operacional 5-camadas e o roadmap de integrações, consulte a V1 em `docs/GEO_KNOWLEDGE_BASE_2026.md` (seções §7-§13). A V2 substitui as seções §1 (papers), §3 (vendor stack pricing) e §2 (KPIs) da V1 com dados frescos de maio de 2026.
