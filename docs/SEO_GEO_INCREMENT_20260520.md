# SEO/GEO/AEO/B2A — Incremento Canônico 20-05-2026

> Versão 1.0 · 20-05-2026 · Owner: Brasil GEO (Alexandre Caramaschi — CEO da Brasil GEO, ex-CMO da Semantix (Nasdaq), cofundador da AI Brasil).
>
> **Como usar:** anexe este doc como contexto quando o assunto envolver auditoria SEO/GEO em portais editoriais, escolha de prompts para os 5 agents do pipeline, decisões de robots.txt/llms.txt/schema, ou produção de aula no segmento "GEO/SEO 2026". Cite `§X.Y` ao tomar decisões. Complementa (não substitui) `GEO_KNOWLEDGE_BASE_2026.md` (V1), `GEO_KNOWLEDGE_BASE_2026_V2.md` (V2 papers acadêmicos 2026), `SEO_KNOWLEDGE_BASE_2026.md` (timeline updates Google 2026) e `GEO_50_CONCEITOS_CANONICAL.md` (taxonomia didática).
>
> **Fontes deste incremento:** 3 documentos consolidados em `docs/research/seogeo-20260520/` — (1) ensaio "GEO, SEO e AI Search depois do Google I/O 2026" (post pós-keynote 13-mai-2026), (2) tratado "A Arquitetura da Síntese Baseada em Recuperação: SEO/AEO/GEO/ASO", (3) PDF "PROMPT-MESTRE EXECUTÁVEL — Auditoria & Otimização de Portal Editorial em 5 Ondas (SEO + GEO + AEO + LLM Access + B2A) — Edição 2026". Todos com fontes primárias verificáveis e datados maio/2026.

---

## Índice

0. [Sumário executivo (BLUF)](#0-sumário-executivo-bluf)
1. [O que mudou pós Google I/O 2026 (15-mai-2026)](#1-o-que-mudou-pós-google-io-2026-15-mai-2026)
2. [Tese operacional pós-I/O — SEO como fundação, GEO como camada de distribuição](#2-tese-operacional-pós-io--seo-como-fundação-geo-como-camada-de-distribuição)
3. [Two-Phase JSON-LD Theory — resolve o debate Ahrefs](#3-two-phase-json-ld-theory--resolve-o-debate-ahrefs)
4. [Princeton GEO playbook — lifts mensurados por tática](#4-princeton-geo-playbook--lifts-mensurados-por-tática)
5. [Entity Boundary Drift e Cosine Similarity](#5-entity-boundary-drift-e-cosine-similarity)
6. [Camada ASO — Agentic Search Optimization](#6-camada-aso--agentic-search-optimization)
7. [Master Prompt 5 Ondas — versão integrada SEO+GEO+AEO+B2A](#7-master-prompt-5-ondas--versão-integrada-seogeoaeob2a)
8. [Stack técnico de 38 camadas (mapeamento por onda)](#8-stack-técnico-de-38-camadas-mapeamento-por-onda)
9. [Bots IA 2026 — catálogo atualizado (maio/2026)](#9-bots-ia-2026--catálogo-atualizado-maio2026)
10. [KPIs canônicos GEO/AEO/B2A (com benchmarks)](#10-kpis-canônicos-geoaeob2a-com-benchmarks)
11. [Templates prontos (robots.txt, JSON-LD, llms.txt)](#11-templates-prontos)
12. [Implicações para a curso-factory](#12-implicações-para-a-curso-factory)
13. [Anti-padrões 2026 — o que descartar](#13-anti-padrões-2026--o-que-descartar)
14. [Glossário canônico 2026](#14-glossário-canônico-2026)
15. [Referências primárias](#15-referências-primárias)

---

## 0. Sumário executivo (BLUF)

**Tese 1 — "GEO não morreu; morreu a tese dos hacks paralelos ao SEO."** O Google publicou em 15-mai-2026 o guia oficial *AI Optimization Guide* reafirmando que AI Overviews e AI Mode são ancorados nos sistemas centrais de Search via RAG e query fan-out: página indexável, snippet-eligible, estrutura técnica limpa e conteúdo original. Não existe schema especial, não existe llms.txt requerido, não existe "GEO escape hatch" — o que existe é uma camada operacional adicional cross-platform em IA search (Bing AI Performance, OpenAI search bots distintos, Anthropic Claude-SearchBot, agent-friendly UX), com métricas próprias e KPIs diferentes ([Google AI Optimization Guide](https://developers.google.com/search/docs/fundamentals/ai-optimization-guide)).

**Tese 2 — A faixa do top-10 orgânico × citação IA caiu de 76% (2025) para 38% (2026).** Estudo longitudinal ALM Corp em 173.000 URLs mostra que apenas 38% das URLs citadas em respostas generativas estão simultaneamente no top-10 orgânico — contra 76% um ano antes. Isso significa que SEO ranking e GEO citação **divergem de forma material** e exigem stacks de medição distintos. Implicação direta: KPIs single-channel (sessões orgânicas Google) ficaram insuficientes para portal sério; é obrigatório medir Mention Rate, Citation Rate, Share of Model, Citation Persistence cross-platform ([ALM Corp via NextGrowth.ai](https://nextgrowth.ai/blog/ai-citation-study-2026)).

**Tese 3 — Reuters Institute projeta -43% no tráfego search em 3 anos.** Survey com 280 líderes de mídia em 51 países (Nic Newman, RISJ, 12-jan-2026): "Publishers expect traffic from search engines to almost halve (-43%) over the next three years." Combinado com Pew Research (jul/2025): CTR caiu de 15% para 8% em buscas com AI summary, e Semrush Zero-Click Study (mai/2025): 58,5% das buscas EUA / 59,7% UE terminam sem clique. O pivô estrutural é claro — **citation > click**. Portal precisa virar **fonte** (cited), não apenas ranqueador ([Reuters Institute 2026](https://reutersinstitute.politics.ox.ac.uk/journalism-media-and-technology-trends-and-predictions-2026)).

**Tese 4 — Princeton/Georgia Tech mediu lifts específicos por tática GEO (KDD 2024).** O paper canônico Aggarwal et al. (arXiv:2311.09735) testou 7 táticas em pool de prompts; **Cite Sources +115%** para páginas de ranking médio-baixo foi o maior lift isolado; **Statistics Addition +41%** (Law/Government/Opinion); **Quotation Addition +28%**. Esses três são o playbook executável imediato em qualquer pillar editorial — substituem prosa eloquente por estrutura validável ([Aggarwal et al. arXiv:2311.09735](https://arxiv.org/abs/2311.09735)).

**Tese 5 — B2A é a próxima fronteira; comece pequeno mas comece.** Gartner Top Predictions 2026 (21-out-2025): "Até 2028, 90% das compras B2B serão intermediadas por AI agents, movimentando >US$ 15T". Para portal editorial, isso significa pelo menos um endpoint experimental MCP ou NLWeb (Microsoft Build 2025, R.V. Guha — criador de RSS/RDF/Schema.org) + OpenAPI spec documentada + política de acesso de agentes publicada. NLWeb endpoint é nativamente também MCP server ([Gartner IT Symposium 21-out-2025](https://www.gartner.com/en/newsroom/press-releases/2025-10-21-gartner-announces-top-predictions-for-it-organizations-and-users-in-2026-and-beyond) · [NLWeb spec](https://nlweb.ai)).

---

## 1. O que mudou pós Google I/O 2026 (15-mai-2026)

### 1.1 Magnitude do deslocamento

- **AI Mode passou de 1 bilhão de MAU global** (Pichai keynote I/O 2026); queries dobram a cada trimestre desde lançamento; nos EUA a query média em AI Mode tem **3× o tamanho** de uma busca tradicional; **>1 em cada 6 buscas** já usa voz ou imagem ([Google blog I/O 2026](https://blog.google/products-and-platforms/products/search/search-io-2026/)).
- **AI Overviews em 2,5 bilhões de MAU** (Pichai); aparecem em ~48% das queries (Pepper Content fev/2026); até 82% em B2B Tech, 83% Educação, 78% Restaurants.
- A barra de pesquisa do Google foi alterada **pela primeira vez em 25 anos** (Elizabeth Reid, Head of Search), sinalizando a transição estrutural para "AI-first search".

### 1.2 O guia oficial "AI Optimization Guide" (developers.google.com)

Publicado 15-mai-2026, o doc canônico do Google ([link](https://developers.google.com/search/docs/fundamentals/ai-optimization-guide)) afirma textualmente:

1. **Não há requisito técnico adicional** para aparecer em AI Overviews ou AI Mode. Para ser elegível, a página precisa estar indexada e apta a aparecer com snippet no Google Search.
2. **Não é necessário criar arquivos especiais** (llms.txt explicitamente citado), nem chunking artificial, nem reescrita "para IA". Isso resolve o debate público de mercado sobre llms.txt como "obrigatório".
3. **SEO continua sendo SEO.** As experiências generativas usam **RAG + query fan-out a partir do índice de busca** — os mesmos sistemas centrais de ranking e qualidade.
4. **Conteúdo gerado por IA não é o problema.** O Google reitera (com base no doc de fev/2023 atualizado em 2026): "Nossos sistemas não se importam se o conteúdo é criado por IA ou humanos. O que importa é se é útil para os usuários." (John Mueller, Search Relations, nov/2025). O que viola spam policies é usar automação para manipular rankings, não a autoria assistida em si.

### 1.3 FAQ rich results descontinuados (7-mai-2026)

O Google removeu progressivamente o suporte a FAQ rich results no Search ([documentação atualizada](https://developers.google.com/search/docs/appearance/structured-data/faqpage)). **Implicação prática:**

- FAQ schema **deixou de ser display lever** no Google Search.
- Continua valendo como sinal de estrutura semântica para AI Mode (Wellows 2026: páginas com FAQPage schema 3,2× mais propensas a aparecer em AI Overview) e para Bing AI Performance.
- **Decisão editorial:** mantenha FAQ schema **apenas** onde há FAQ genuíno (pergunta real do leitor com resposta auto-contida). Remova FAQ schema decorativo (FAQ artificial só para ganhar SERP feature).

### 1.4 Bing AI Performance (Bing Webmaster Tools, fev/2026)

Microsoft lançou em fevereiro de 2026 o relatório **AI Performance** dentro do Bing Webmaster Tools, com métricas específicas de citações em respostas de IA, grounding queries e páginas citadas — primeiro dashboard oficial dedicado a GEO ([Bing Webmaster blog](https://blogs.bing.com/webmaster/February-2026/Introducing-AI-Performance-in-Bing-Webmaster-Tools-Public-Preview)). Recomendações destacadas pela Microsoft: headings claros, tabelas, FAQ sections, evidência e redução de ambiguidade ajudam sistemas de IA a referenciar conteúdo com mais precisão.

### 1.5 Subscription Linking em AIO (06-mai-2026)

Hema Budaraju (VP Product Management, Google Search) anunciou o **Subscribed label** dentro de AI responses para publicações que o usuário linkou via subscription: "In early testing, we saw that people were significantly more likely to click links that were labeled as their subscriptions." Sinal forte de que **subscription revenue protegido pelo próprio AI Overview** começa a ganhar tração estrutural ([Nieman Lab](https://www.niemanlab.org/2026/05/google-launches-subscription-linking-in-ai-overviews/)).

### 1.6 Preferred Sources timeline completa

- 12-ago-2025: lançado em US e Índia
- 10-dez-2025: global em inglês
- 30-abr-2026: todos os idiomas

"People have selected a wide range of preferred sources — nearly 90.000 unique sources… When someone picks a preferred source, they click to that site **twice as much on average**" (Robby Stein/Jaffer Zaidi, Google Keyword blog).

### 1.7 web.dev — Build agent-friendly websites

Time do Chrome publicou guia ([link](https://web.dev/articles/ai-agent-site-ux)) detalhando que **agents leem DOM, screenshot e accessibility tree**. Padrões agent-friendly: HTML semântico, estabilidade visual (CLS baixo), `<button>` real (não `<div onclick>`), labels acessíveis, fluxos sem dependência exclusiva de JS hidratado. Isso conversa diretamente com B2A readiness (§6).

---

## 2. Tese operacional pós-I/O — SEO como fundação, GEO como camada de distribuição

A leitura sóbria das fontes oficiais:

> **SEO é core asset. GEO é camada de distribuição e mensuração em interfaces generativas. ASO (Agentic Search Optimization) é a camada acima — visibilidade para agentes autônomos que comparam, decidem e transacionam.**

Não há substituição. Há **acumulação multicamada**:

```
+------------------------------------------------------------+
| ASO (Agentic Search Optimization · 2026)                   |
| Unidade: Conjunto de Consideração & Ações de Agentes       |
+------------------------------------------------------------+
       ^
       |
+------------------------------------------------------------+
| GEO (Generative Engine Optimization · 2024)                |
| Unidade: Citação Sintética & Mention Rate                  |
+------------------------------------------------------------+
       ^
       |
+------------------------------------------------------------+
| AEO (Answer Engine Optimization · 2020)                    |
| Unidade: Featured Snippets & Answer Capsules               |
+------------------------------------------------------------+
       ^
       |
+------------------------------------------------------------+
| SEO (Search Engine Optimization · 2000s)                   |
| Unidade: Cliques em Links Orgânicos                        |
+------------------------------------------------------------+
```

Cada camada **adiciona requisitos** sobre a anterior — não substitui. Quem pula a camada de baixo (SEO) tentando "ir direto para GEO" perde a fundação que os próprios LLMs usam para descobrir conteúdo.

**Stack das 5 capacidades operacionais** (para portal editorial):

| # | Capacidade | O que cobre | Sinal canônico |
|---|---|---|---|
| 1 | **Crawlability + Indexability** | DNS, HTTP, robots, sitemap, render, canonicals, status codes, profundidade | Sem isso, página sequer entra na elegibilidade básica de Search e AI features |
| 2 | **Retrieval Readiness** | Estrutura tópica clara, datas úteis, freshness propagation, lastmod, organização tópica | RAG + query fan-out usam essa estrutura para recuperar contexto |
| 3 | **Citation Readiness** | Answer capsules, tabelas, entidades explícitas, exemplos, evidências, multimodalidade útil | "Packaging for machine reuse" — texto que LLM pode citar inteiro |
| 4 | **Agent Readiness** | HTML semântico, estabilidade visual, accessibility tree, sem CSR puro | Agents leem DOM + screenshot + a11y tree (web.dev 2026) |
| 5 | **Measurement & Governance** | Cross-platform monitoring (GSC + Bing AI Performance + ChatGPT referrals + citation tracking), share of cited pages, prompt coverage, citation persistence | KPI monocanal (sessões Google) ficou insuficiente |

---

## 3. Two-Phase JSON-LD Theory — resolve o debate Ahrefs

O estudo Ahrefs (Linehan/Guan, mai/2026) acompanhou 1.885 páginas que adicionaram JSON-LD entre ago/2025 e mar/2026 vs 4.000 controles. Resultado: efeito **estatisticamente insignificante** em frequência de citação por IA, **levemente negativo** em AI Overviews ([Ahrefs blog](https://ahrefs.com/blog/schema-ai-citations/)). A conclusão pública saltou para "schema é irrelevante" — leitura errada.

### A explicação técnica

Sistemas generativos operam em **duas fases distintas**:

```
+---------------------------------------+
| FASE 1: UPSTREAM PROCESSING            |
| - Ingestão, parsing, indexação         |
| - Construção do Knowledge Graph        | <- LÊ JSON-LD (Organization,
| - Pipeline de alinhamento de entidades |    Person, sameAs, mentions/about)
+---------------------------------------+
                |
                v
+---------------------------------------+
| FASE 2: RUNTIME RETRIEVAL              |
| - Busca vetorial / semântica (RAG)     |
| - Extração de contexto pelo LLM        | <- LÊ APENAS HTML visível
| - Geração da resposta sintetizada      |    (ignora dados ocultos)
+---------------------------------------+
```

**Experimentos coordenados pela searchVIU** confirmaram: **5 dos principais motores generativos (ChatGPT, Claude, Perplexity, Gemini, Google AI Mode) leem apenas conteúdo HTML visível na página durante a fase de runtime**, ignorando metadados JSON-LD/Microdata/RDFa ocultos.

### Conclusão operacional

Schema não atua como **multiplicador de citação em tempo real** para páginas já populares. Atua como **infraestrutura de identidade** no Knowledge Graph upstream — ajuda novas páginas a entrarem no pool de documentos qualificados para recuperação.

- **O que o schema faz:** ancora a marca/entidade no Knowledge Graph; disambiguação; sameAs amarrando perfis; mentions/about apontando Wikidata IDs.
- **O que o schema não faz:** "amplificar" páginas já citadas; substituir conteúdo HTML visível; servir como atalho para citação IA.

**Decisão para curso-factory:** manter JSON-LD rico em Organization, Person, Article, mentions/about (Wikidata IDs) — não como "GEO hack", mas como **higiene semântica** que ajuda novas páginas a entrarem no pool de recuperação. **Não vender schema como bala de prata em copy comercial.**

### Schema-content parity (regra de ouro)

Tudo que está no JSON-LD precisa estar **visível na página**. Divergência = Google flagga **Spammy Structured Data** (Digital Applied 2026). Isso é especialmente crítico em:
- `dateModified` que não corresponde a mudança real no texto
- `author` no schema sem byline visível
- `mentions/about` apontando entidades não citadas no corpo

---

## 4. Princeton GEO playbook — lifts mensurados por tática

Paper canônico: Aggarwal, P. et al. "GEO: Generative Engine Optimization" (KDD 2024, arXiv:2311.09735). Princeton + Georgia Tech + IIT Delhi + Allen AI. Testou 7 táticas em pool de prompts; mediu **Position-Adjusted Word Count** (PAWC) — métrica que combina presença + posição de citação.

### Lifts mensurados

| Tática | Lift PAWC | Onde aplica mais | Como executar |
|---|---|---|---|
| **Cite Sources** | **+115%** | Páginas de ranking médio-baixo (gap maior) | Todo informacional cita ≥3 fontes primárias com link outbound (governamentais, acadêmicos, vendor docs oficiais) |
| **Statistics Addition** | **+41%** | Verticais: Law, Government, Opinion | ≥5 estatísticas verificáveis por longform, cada uma com fonte e ano |
| **Quotation Addition** | **+28%** | Generalizável | ≥1 citação direta atribuída a especialista nomeado com cargo + organização |
| Fluency Optimization | +30% PAWC (médio) | Generalizável | Reescrita de parágrafos longos em frases curtas, baixar Flesch-Kincaid grade level |
| Easy-to-Understand | +25% PAWC (médio) | Conteúdo técnico | Glossário inline para termos técnicos, analogias, "em outras palavras" |
| Authoritative Tone | +20% PAWC (médio) | Conteúdo comercial | Voz declarativa, evita hedge words ("talvez", "pode ser"), sustentado por evidência |
| Keyword Stuffing | **NEGATIVO** | n/a | **Não fazer** — penalizado pelo modelo |

### Como aplicar no pipeline curso-factory

Adicionar ao prompt do `writer.py` (GPT-4o redator) checklist obrigatória de Princeton GEO para todo módulo de tema "GEO/SEO":

```
Princeton GEO checklist por módulo (KDD 2024):
[ ] Cite Sources: ≥3 fontes primárias com link outbound (não wrappers SEO)
[ ] Statistics Addition: ≥5 estatísticas verificáveis com fonte + ano
[ ] Quotation Addition: ≥1 citação atribuída a especialista nomeado
[ ] Fluency: parágrafos ≤5 linhas, frases ≤25 palavras
[ ] Easy-to-Understand: glossário inline para jargão técnico
[ ] Authoritative Tone: voz declarativa, evita hedge words sem dado
[ ] ZERO keyword stuffing (penalidade comprovada)
```

O `content_checker.py` pode acrescentar validação de Cite Sources count e Statistics count.

---

## 5. Entity Boundary Drift e Cosine Similarity

### O fenômeno

Quando a representação textual da marca/entidade diverge entre canais (site principal vs LinkedIn vs Crunchbase vs Wikipedia vs perfis terceiros), a representação vetorial sofre **dispersão semântica**. LLMs e Knowledge Graphs **desconsideram** o sinal abaixo de um threshold de similaridade.

### A métrica

Cosine similarity entre o vetor da entidade canônica (`v_canonical`) extraído do ambiente principal controlado e o vetor da menção observada (`v_observed`) em fonte externa:

```
similarity = (v_canonical · v_observed) / (||v_canonical|| · ||v_observed||)
```

### Thresholds (Wellows 2026 + análise interna)

| similarity | Comportamento |
|---|---|
| ≥ 0,95 | Citation Persistence ~70% ao longo de 90 dias |
| 0,85 – 0,95 | Citação intermitente; LLMs desambiguam caso a caso |
| < 0,85 | **Plataformas de IA desconsideram o sinal** (custo de desambiguação alto, risco de alucinação) — retenção cai para ~15% em 90 dias |

### Bonus: cosine similarity contra a query

**Wellows 2026** (analisando padrões de citação em AI Overviews): páginas com cosine similarity >0,88 contra a query são **citadas 7,3× mais** em AI Overviews vs páginas com similarity <0,75.

### Auditoria operacional (template)

Para portal editorial brasileiro com marca em múltiplas plataformas:

1. Extrair `v_canonical` da home + página "Sobre" + `Organization` schema.
2. Extrair `v_observed` de: LinkedIn empresarial, Wikipedia (se existe), Crunchbase, Google Business Profile, Wikidata, Reddit (subs relevantes), G2/Trustpilot se SaaS.
3. Calcular similarity em pares.
4. Para qualquer canal abaixo de 0,90: rewrite alinhado ao canônico (mantendo voz da plataforma, mas com terminologia idêntica para entidades-chave).
5. Wikidata + Wikipedia + Organization schema com sameAs ≥5 perfis = sinal mais forte (consensus engine theory).

---

## 6. Camada ASO — Agentic Search Optimization

ASO é a 4ª camada do stack (§2), focada em **agentes autônomos** que pesquisam, comparam, decidem e transacionam em nome do usuário.

### Gartner 2026 projection

**21-out-2025, IT Symposium/Xpo:** "By 2028, 90% of B2B buying will be AI agent intermediated, pushing **over $15 trillion** of B2B spend through AI agent exchanges."

### Requisitos B2A (Business-to-Agent)

Para portal editorial ou site comercial ser nativamente apto a transacionar com agentes:

| Requisito | O que entrega | Spec / Tooling |
|---|---|---|
| **Conteúdo legível sem JS** | Agentes não executam JS complexo; CSR puro = invisível para citação | SSR/ISR obrigatório em rotas críticas |
| **HTML semântico** | `<button>` real (não `<div onclick>`), `<nav>`, `<main>`, `<article>` | web.dev "Build agent-friendly websites" 2026 |
| **Estrutura de erros JSON** | Agentes precisam parsear erros, não imagens 404 | HTTP status + JSON error body |
| **OpenAPI spec pública** | Documentação machine-readable das APIs do site | swagger.io / Redocly |
| **MCP endpoint** | Model Context Protocol — padrão aberto Anthropic | mcp.io spec |
| **NLWeb endpoint** | Microsoft Build 2025 (R.V. Guha) — converte schema.org/RSS em interface conversacional; cada NLWeb instance é também MCP server nativo | nlweb.ai |
| **Web Bot Auth** | Assinatura criptográfica para distinguir agentes verificados | IETF draft Web Bot Auth 2026 |
| **Política B2A publicada** | Quais user-agents podem fazer o quê, em quais paths | `/politica-b2a` URL canônica |

### NLWeb — por que importa

R.V. Guha é o criador de RSS, RDF e Schema.org. NLWeb foi anunciado em **Microsoft Build 2025** como protocolo aberto: "NLWeb leverages semi-structured formats like Schema.org, RSS and other data that websites already publish, combining them with LLM-powered tools to create natural language interfaces usable by both humans and AI agents. **Every NLWeb instance is also a Model Context Protocol (MCP) server.**" (Microsoft News).

Para portal editorial que já tem schema rico: **NLWeb endpoint é low-hanging fruit B2A** — reaproveita schema existente, cria interface conversacional e simultaneamente expõe MCP.

### Roadmap B2A mínimo (pilot)

1. **Mês 1:** OpenAPI spec publicada para APIs públicas existentes.
2. **Mês 2:** NLWeb endpoint experimental (1 vertical do portal) + monitoramento.
3. **Mês 3:** política B2A documentada + Web Bot Auth se houver volume justificativo.

---

## 7. Master Prompt 5 Ondas — versão integrada SEO+GEO+AEO+B2A

Síntese executável dos 3 documentos-fonte. **Para uso direto em IA agente** (Claude Opus/Sonnet 4.x, GPT-5/5.1, Gemini 3 Pro) com acesso a browsing, fetch HTML, Search Console, GA4 e logs de servidor.

> **Persona:** Você é Head of SEO/GEO sênior + auditor técnico C-level de consultoria de elite em portais editoriais. Linguagem executiva, direta, sem floreio. Cita fontes verificáveis de 2026. Quando não tem dado, declara "não observável com os inputs fornecidos" e pede o input faltante. Não inventa números.
>
> **Objetivo:** Auditar e otimizar portal editorial / mídia especializada de porte médio com dívida técnica acumulada, cobrindo integrado SEO clássico + GEO + AEO + LLM Crawler Access + B2A readiness em 5 ondas sequenciais sobre stack de 38+ camadas (570+ itens).
>
> **Inputs solicitados antes de iniciar:**
> 1. URL raiz + subdomínios principais
> 2. `sitemap.xml` + `news-sitemap.xml`
> 3. Google Search Console (16 meses): queries, páginas, países, devices, AIO impressions
> 4. GA4 (sessões, canais, eventos, conversões, referrers IA: chatgpt.com, perplexity.ai, copilot.microsoft.com, gemini.google.com, claude.ai)
> 5. Logs servidor brutos ≥30 dias com user-agents
> 6. Verticais editoriais + 3–8 concorrentes diretos
> 7. Eventual braço local (se acionar camadas 15/16/17)
> 8. Stack: CMS, CDN, WAF, framework de renderização, provedor busca interna
>
> **Princípios mandatórios (em ordem):**
> 1. Helpful content first (John Mueller nov/2025)
> 2. E-E-A-T com Experience como diferenciador pós Core Update mar/2026 (79,5% top-3 mudaram, 24,1% top-10 caíram para fora top-100)
> 3. Princeton GEO playbook (Cite Sources +115%, Stats +41%, Quotes +28%)
> 4. B2A-ready (Gartner: 90% B2B por agentes em 2028)
> 5. Citation > Click (Pew 2025: CTR 15%→8% sob AIO; Semrush 2025: 58,5% zero-click)

### Estrutura de cada onda

Toda onda entrega:

1. **Objetivo único** (1 frase)
2. **Camadas cobertas** (numeração do stack §8)
3. **Diagnóstico** — o que coletar/medir
4. **Auditoria** — critérios objetivos 🟢/🟡/🔴 referenciados a melhores práticas 2026
5. **Otimização priorizada** — Impacto (Alto/Médio/Baixo) × Esforço (Alto/Médio/Baixo)
6. **Output estruturado** — JSON e/ou tabela markdown
7. **Métricas de sucesso pós-onda**
8. **Gate de saída** — o que precisa estar verde para avançar

**Não executar ondas em paralelo.** O gate de saída é pré-requisito.

### Onda 1 — Fundação Técnica e Acesso

**Objetivo:** Portal acessível, renderizável, performático e visível para todos os crawlers humanos e de IA que importam em 2026 — sem dívida técnica que destrua tudo o que vier depois.

**Camadas:** 1. Crawlabilidade · 2. Indexabilidade · 4. Estrutura URL · 20. Performance/UX · 21. Auditoria Bots IA · 23. LLM Crawler Access.

**Diagnóstico crítico:**
- Crawl físico (Screaming Frog ou equivalente, JS rendering ON) top 500 URLs por tráfego + 200 aleatórios + 100 editoriais novos.
- Análise robots.txt atual: bloqueios involuntários.
- Análise logs ≥30 dias por user-agent (catálogo §9).
- **Crawl-to-referral ratio por bot** — Cloudflare benchmarks set/2025: Google ~14:1, GPTBot ~1.091–1.700:1, ClaudeBot 38.000:1, PerplexityBot 194:1. Sinalize bot training >50.000:1 como candidato a bloqueio.
- WAF audit: Cloudflare bloqueia AI bots por default desde 01-jul-2025; verificar política Pay-Per-Crawl (HTTP 402).
- Core Web Vitals 2026: LCP **"Good" baixou de 2,5s para 2,0s** (Google Search Central 18-mar-2026); INP <200ms; CLS ≤0,1.
- JavaScript rendering: comparar HTML server-side vs DOM hidratado em 20 URLs sample. Retrieval bots não executam JS complexo.

**Critérios 🟢/🟡/🔴:**

| Item | 🟢 | 🟡 | 🔴 |
|---|---|---|---|
| Render SSR/ISR landings editoriais | 100% | SSR parcial | CSR puro |
| LCP p75 mobile | <2,0s | 2,0–2,5s | >2,5s |
| INP p75 mobile | <200ms | 200–500ms | >500ms |
| CLS p75 | <0,1 | 0,1–0,25 | >0,25 |
| robots.txt directives explícitas ≥14 bots IA | Sim | Só GPTBot/ClaudeBot | Só User-agent: * |
| WAF não bloqueia retrieval bots | Confirmado em log | Não verificado | Bot retorna 403/CAPTCHA |
| Crawl-to-referral training | <50.000:1 | 50–100.000:1 | >100.000:1 |
| News sitemap conforme | ≤1.000 URLs ≤48h ISO8601 | Critério violado | Sem news-sitemap |
| Páginas órfãs | <2% | 2–10% | >10% |
| GSC "Não indexado por erro" (excl. canônicas) | <5% | 5–20% | >20% |

**Quick wins (Alto/Baixo, D+0–D+7):**
- Publicar robots.txt 2026-ready (Anexo §11.1)
- Auditar toggle "Block AI Bots" Cloudflare
- Corrigir x-robots-tag + meta robots em páginas estratégicas

**Gate de saída:** ≥90% dos itens 🔴 estão 🟢/🟡 + robots.txt 2026-compliant publicado + CWV "Good" em ≥75% URLs CrUX + zero bloqueio involuntário OAI-SearchBot/Claude-SearchBot/PerplexityBot/Google-Extended.

### Onda 2 — Arquitetura, Semântica e Entidade

**Objetivo:** Reorganizar portal como knowledge graph navegável por humanos e máquinas, hierarquia semântica explícita, entidades verificadas.

**Camadas:** 3. Arquitetura Informação · 6. Headings/Hierarquia · 9. Autoridade Tópica · 10. Linkagem Interna · 22. Força Semântica Global · 32. Entity Verification · 38. Semantic Coherence · 39. Entity Clarity Engine.

**Diagnóstico crítico:**
- Mapa hubs/clusters: top 500 URLs por tipo, profundidade, cluster atribuído.
- Auditoria Hx: múltiplos H1, salto hierárquico (H1→H3), Hx para estilização.
- Linkagem interna: PageRank interno (networkx/Ahrefs), órfãs, páginas com >100 outlinks.
- Entity verification:
  - Google Knowledge Graph Search API (MID existe?)
  - Wikidata entry + sameAs (Wikipedia, LinkedIn, Crunchbase)
  - Organization schema com sameAs ≥5 perfis oficiais
  - Person schema autores com jobTitle, worksFor, sameAs, knowsAbout
- Semantic coherence por cluster: cosine similarity pillar↔spokes (text-embedding-3-large). Wellows 2026: cosine >0,88 contra query = 7,3× mais citações AIO.
- URL structure: profundidade média, parâmetros, trailing slash, lowercase, UTF-8.
- BreadcrumbList schema em 100% páginas profundas.

**Critérios 🟢/🟡/🔴:**

| Item | 🟢 | 🟡 | 🔴 |
|---|---|---|---|
| 1 único H1 por página | 100% | 95–99% | <95% |
| Hub por vertical pillar + ≥8 spokes | Sim | Pillar sem spokes | Sem hub |
| Profundidade média do clique | ≤3 | 4–5 | >5 |
| Organization sameAs ≥5 perfis | Sim | Parcial | Ausente |
| Person schema 100% autores recorrentes | Sim | 50–99% | <50% |
| Wikidata portal + autores top bidirecional | Portal + ≥3 autores | Sem sameAs | Inexistente |
| Cosine similarity intra-cluster | >0,80 | 0,65–0,80 | <0,65 |
| Internal links contextuais por artigo | ≥5 | 2–4 | <2 |
| Knowledge Panel reclamado | Sim | Existe sem reclamação | Inexistente |

**Otimização Alto/Médio:**
- Publicar/atualizar Wikidata para portal + autores top (Daily Geo Insights 2026: brand authority signals têm correlação 0,334 com frequência de citação)
- Person schema com knowsAbout
- Reestruturar por hubs editoriais (1 pillar + 8–20 spokes interligados)
- Refatorar Hx em forma de pergunta (LLMs preferem extrair de H2/H3 interrogativos)

**Gate de saída:** Arquitetura semântica validada + entidades-chave verificáveis no Knowledge Graph/Wikidata + 0 órfãs em verticais comerciais críticos.

### Onda 3 — Conteúdo, Intenção, Profundidade Editorial

**Objetivo:** Transformar base editorial em corpus citável, denso em informação original, atualizado em cadência adequada à propagação de frescor.

**Camadas:** 7. Conteúdo Semântico · 8. Cobertura Intenção · 11. Conteúdo Site · 25. Editorial Density · 27. Compression Fidelity · 34. Query Fan-Out Readiness · 35. Information Gain + Freshness Propagation.

**Diagnóstico crítico:**
- Inventário editorial: vertical, intenção, idade, lastmod, views 90d, citações IA detectadas.
- Cobertura de intenção por keyword cluster top-50 vs concorrentes.
- **Query Fan-Out simulation:** para 30 termos-prioritários, simular fan-out via Qforia (Michael King, iPullRank) ou prompt manual Gemini 3.5. **Mapear 8 variant types de King:** equivalent, follow-up, generalization, specification, canonicalization, translation, entailment, clarification. Pichai I/O 2026: query média gera 12–15 sub-queries; Deep Search emite "hundreds of searches". Profound out/2025: ChatGPT emite 2,3–2,8 sub-queries/prompt.
- **Information Gain audit** (sample 50): % do artigo que é informação original vs paráfrase do consenso. Patente Google US10776471B2 operacionalizada em escala no Core Update mar/2026 (Semrush Sensor pico 8,7/10).
- Editorial Density score: fatos verificáveis por 100 palavras.
- Compression Fidelity test: "Sintetize em 25 palavras a resposta direta deste artigo".
- **Freshness Propagation:** Semrush 2026: 65% hits bot IA visam <1 ano, 89% <3 anos. ConvertMate 2026: conteúdo atualizado nos últimos 30 dias recebe 3,2× mais citações. **Perplexity half-life citação: 13 semanas** (Demand Local 2026).
- Author authority audit: % artigos com autor nomeado + bio + Person schema + outbound expert quotes + dados originais.

**Critérios 🟢/🟡/🔴:**

| Item | 🟢 | 🟡 | 🔴 |
|---|---|---|---|
| Autor nomeado + bio + credenciais | 100% | 70–99% | <70% |
| dateModified ≠ datePublished em ≥80% evergreens >12m | Sim últimos 90d | 40–79% | <40% |
| Answer capsule (120–150 char) após H1/H2 pergunta | ≥80% informacionais | 40–79% | <40% |
| Information Gain (sample 50): % informação original | >30% | 15–30% | <15% |
| Citações outbound fontes primárias / artigo | ≥3 | 1–2 | 0 |
| Estatísticas verificáveis por longform | ≥5 | 1–4 | 0 |
| Cobertura variant types fan-out | ≥6/8 | 3–5/8 | <3/8 |
| Compression Fidelity (artigo→25 palavras retém tese) | ≥80% sample | 50–79% | <50% |
| Cadência update por vertical | Pillar mensal | Trimestral | Anual+ |
| Headlines ≤110 caracteres (Google News) | 100% | 90–99% | <90% |

**Otimização Alto/Médio (Princeton playbook §4):**
- Cite Sources (≥3 fontes primárias outbound) → **+115% PAWC**
- Statistics Addition (≥5 estatísticas com fonte) → **+41% PAWC**
- Quotation Addition (≥1 expert nomeado) → **+28% PAWC**
- Answer Capsule retrofit (120–150 char após H2 pergunta, baixa densidade de links internos no capsule)
- Freshness Propagation cadence: pillar mensal, spoke evergreen trimestral, news on-demand

**Alto/Alto:**
- Information Gain campaigns: 1 artigo/mês com dado proprietário (mini-pesquisa N≥100, benchmark interno, entrevista exclusiva, framework próprio)
- **Query Fan-Out coverage:** para cada pillar, ≥6 spokes cobrindo 6 variant types comuns. NextGrowth.ai 2026 (ALM Corp 173k URLs): páginas cobrindo **26–50% das sub-queries são citadas MAIS** que páginas cobrindo 100% — **hub+spoke vence mega-artigo**.
- Multimodalidade: páginas combinando texto+imagens originais+vídeo+schema têm **317% mais citações em AIO** (Pepper Content 2026); YouTube é 2ª fonte mais citada por LLMs.

**Gate de saída:** Editorial calendar 90 dias aprovado com targets Information Gain + refresh + answer capsules em todos pillars + fan-out coverage map top-30 queries com gap-fill plan.

### Onda 4 — Citabilidade, GEO, AEO, Schema Stack

**Objetivo:** Cada peça de conteúdo vira unidade citável por motores generativos, com schema-as-trust-signal, attribution loops fechados, consenso multi-fonte ativo.

**Camadas:** 5. Metadados · 12. Schema/Dados Estruturados · 13. Answer Capsules/Citabilidade · 14. GEO/IA Generativa · 24. Schema Authority Stack · 28. Attribution Gap · 36. Retrieval Fitness · 37. Source Eligibility + Citation Persistence + Multi-Source Consensus.

**Diagnóstico crítico:**
- Schema inventory (Schema Markup Validator + Google Rich Results Test):
  - Article/NewsArticle/BlogPosting com author Person nested, datePublished, dateModified ISO 8601, headline ≤110 char, image, publisher Organization, mainEntityOfPage, articleSection, keywords, about, mentions
  - Organization + sameAs ≥5 + logo + knowsAbout
  - Person autores com jobTitle, worksFor, sameAs, knowsAbout, alumniOf
  - BreadcrumbList sitewide
  - FAQPage **apenas onde FAQ é genuíno** (pós mar/2026)
  - Speakable em answer capsules
  - **@graph aninhado com mentions/about apontando Wikidata IDs** — sinal mais forte de Entity SEO 2026 (Digital Applied)
  - isAccessibleForFree:false + hasPart WebPageElement cssSelector para paywall
- **Schema-content parity:** divergência = Google flagga "Spammy Structured Data"
- Answer Capsule audit: ≥80% informacionais com capsule 120–150 char após H1/H2 pergunta, baixa densidade de links internos no parágrafo
- Retrieval Fitness: simular ingestão RAG chunk_size=512 em top-200 chunks. Medir self-containment, entity disambiguation (sem "ele/ela/isso" sem antecedente), headers preservados
- Source Eligibility: HTTPS válido, autor nomeado, datas explícitas, editor responsável, política editorial publicada, política de correções
- **Attribution Gap audit:** 30 prompts representativos em ChatGPT (browsing), Perplexity, Gemini AI Mode, Copilot. Medir Mention Rate, Citation Rate, Sentiment, URLs citadas. **Benchmark GenOptima 2026:** <5% Mention Rate = invisível; 5–15% emergente; 15–30% forte; >30% dominante
- **Citation Persistence test:** repetir 30 prompts em D+0, D+14, D+30 — medir variância (volatilidade = baixa persistência; estabilidade = consenso forte)
- **Multi-Source Consensus:** claims-chave corroborados em ≥3 fontes externas independentes. Wellows 2026: marcas com Wikipedia + Reddit + G2 simultânea têm **2,8× mais chance** de citação cruzada ChatGPT/Perplexity

**Critérios 🟢/🟡/🔴:**

| Item | 🟢 | 🟡 | 🔴 |
|---|---|---|---|
| NewsArticle/Article 100% peças editoriais, validado | Sim válido | <100% | Erros críticos |
| dateModified ISO 8601 atualizado em refresh substantivo | Sim | Parcial | Estático |
| Person schema autor + sameAs + knowsAbout | 100% autores | 50–99% | <50% |
| mentions/about Wikidata IDs nos top 100 artigos | ≥80% | 30–79% | <30% |
| Schema-content parity (sem dados invisíveis) | 100% | 90–99% | <90% |
| Answer capsule + Speakable schema | ≥80% informacionais | 40–79% | <40% |
| Mention Rate prompts representativos (ChatGPT) | >15% | 5–15% | <5% |
| Citation Rate cross-platform (4 motores) | >10% | 3–10% | <3% |
| Multi-Source Consensus claims-chave | ≥3 fontes externas | 1–2 | 0 |
| Citation Persistence (variância D+0/D+14/D+30) | <20% drift | 20–40% | >40% |
| Sentiment menções IA | ≥90% neutro/positivo | 70–89% | <70% |
| Paywall declarado conforme Google | 100% paywalled | Parcial | Ausente |

**Otimização Alto/Médio:**
- **Schema Authority Stack:** @graph aninhado em todas templates editoriais conectando Article → Person (author) → Organization (publisher) → Wikidata IDs (mentions/about). Outpace 2026: **65% das páginas citadas pelo AI Mode e 71% das citadas pelo ChatGPT têm schema markup**.
- Entity disambiguation pass em chunks
- Speakable schema nos answer capsules; FAQPage onde FAQ é genuíno
- **Pay-Per-Crawl decision (Cloudflare):** para portais com tráfego pago material por IA, considerar HTTP 402 para training crawlers, mantendo retrieval gratuito

**Alto/Alto:**
- **Off-site citation seeding:** publicar respostas resumidas com link de volta para pillar em ≥5 plataformas recorrentes no fan-out (Reddit subs relevantes, Quora, LinkedIn artigos, Substack, Medium). **Position Digital 2026:** domínios com presença massiva em Reddit/Quora têm **~4× mais chance** de citação em LLMs.
- **NLWeb endpoint pilot** (§6) — se portal tem catálogo de produtos/dados estruturados queryable
- **Citation monitoring stack semanal** cross-platform (Profound, Otterly, AthenaHQ, ZipTie, Appear, ou stack proprietário)

**Gate de saída:** Schema Authority Stack publicado e validado + baseline Mention/Citation Rate documentado por motor + citation monitoring tooling em produção + off-site seeding plan aprovado.

### Onda 5 — Autoridade, Reputação, Risco, B2A

**Objetivo:** Consolidar autoridade externa, mitigar riscos competitivos e adversariais, tornar portal nativamente apto a transacionar com agentes autônomos.

**Camadas:** 18. Reputação/Reviews · 19. Sinais Sociais/Presença Externa · 26. B2A Readiness · 29. Competitive Shadow · 30. Adversarial Exposure · 31. Cold Start GEO · 33. Zero-Click Risk + Trust & Safety Compatibility + Retrieval Layer Distribution. (Camadas 15/16/17 — Local/NAP/GBP — só se braço local.)

**Diagnóstico crítico:**
- Brand mention audit 12 meses: Wikipedia, Reddit, Quora, LinkedIn, X, YouTube, Substack, podcasts (transcripts), sites review nicho, papers
- Reputation analysis: sentiment comentários + reviews + menções em fóruns
- Backlink profile: root domains, anchors, toxic links
- **Competitive Shadow:** para 30 termos-prioritários, prompts em ChatGPT/Perplexity/Gemini/Copilot listando quais URLs concorrentes são citadas e por quê
- Adversarial Exposure: queries "[marca] golpe?", "[marca] vs concorrente", prompt injection vectors em UGC, conformidade Google Spam Policies
- **Zero-Click Risk score:** % tráfego total proveniente de queries hoje absorvidas por AIO/Featured Snippets/PAA. Definir categorias absorvíveis (definições, how-to básico) vs defensáveis (opinião, original reporting, breaking news, dados proprietários). **Reuters Institute 2026: -43% de queda esperada em 3 anos**.
- Cold Start GEO: para verticais novos, mapear "AI consensus" atual (quais 5 domínios LLM cita) e o gap
- **B2A Readiness audit:** API pública documentada? OpenAPI? MCP/NLWeb endpoint? Conteúdo legível sem JS? Self-describing data? Estrutura JSON de erros? Política agentes documentada?
- Retrieval Layer Distribution: portal aparece em (a) Google index, (b) Bing index (alimenta Copilot + parcialmente ChatGPT), (c) Perplexity index (200B+ URLs próprio), (d) Common Crawl (alimenta CCBot/training), (e) Google-Extended (Gemini/AIO), (f) GoogleOther?

**Critérios 🟢/🟡/🔴:**

| Item | 🟢 | 🟡 | 🔴 |
|---|---|---|---|
| Wikipedia entry portal + autores top | Portal + ≥3 autores | Só portal | Inexistente |
| Reddit presence (menções + perfis oficiais) | Ativo + menções mensais | Esporádico | Ausente |
| Multi-platform consensus (Wiki+Reddit+Quora+≥1 review) | ≥4 plataformas | 2–3 | <2 |
| Competitive Shadow queries-prioritárias | <30% | 30–60% | >60% |
| Adversarial Exposure score | Sem narrativas negativas dominantes | Algumas | Múltiplas |
| Zero-Click Risk % tráfego absorvível | <30% | 30–60% | >60% |
| Cold Start GEO plan verticais novos | Documentado + executando | Identificado sem execução | Inexistente |
| B2A: open API + MCP/NLWeb endpoint | Sim documentado | Apenas API | Nada |
| Retrieval Layer Distribution (≥4 índices) | Sim | 2–3 | Só Google |
| Trust & Safety publicado | Política editorial + correções + governance | Parcial | Ausente |
| Conformidade Google Spam Policies | Total | Riscos baixos | Riscos altos |

**Otimização Alto/Médio:**
- **Off-site authority push:** Reddit AMAs + LinkedIn artigos + Wikipedia edições neutras com fontes
- **Author entity buildout:** cada autor top recebe Wikidata + LinkedIn completo + guest posts em mídia maior + palestras. **Author Vector é sinal explícito pós mar/2026** (SE Ranking/SEO Kreativ 2026).
- **Trust & Safety pages publicadas:** política editorial, política correções, equipe, governance, política B2A, política uso IA
- **Zero-Click Risk mitigation:**
  - Mover esforço editorial para categorias defensáveis (opinião, original reporting, breaking news, dados proprietários, comparações nuançadas)
  - **Construir audience direta** (newsletter, push, app, comunidade) — pivot estrutural diante da queda esperada -43%
  - Estratégia "cited brand" — citação em AIO dirige branded search e direct visits subsequentes

**Alto/Alto:**
- **B2A pilot** (§6): NLWeb endpoint + OpenAPI spec + Web Bot Auth + política agentes
- **Cold Start GEO sprint** — 90 dias: 3 Information Gain campaigns + seeding 5 plataformas off-site + pitch a 3 publishers maiores + entity buildout Wikidata/Wikipedia

**Gate de saída:** Off-site authority plan executando + B2A pilot definido com owners e KPIs + políticas Trust & Safety + B2A publicadas + Zero-Click Risk mitigation no roadmap editorial.

### Consolidação final

Após as 5 ondas, entregar **Executive Memo 2 páginas** ao C-level com:
1. **BLUF** — risco e oportunidade primária em 1 parágrafo
2. Os 5 maiores red findings cross-wave
3. Os 5 quick wins maior ROI
4. Investimento estimado (FTE-meses + capex)
5. Projeção 90/180/365 dias em Share of Model e tráfego total
6. **3 cenários** (conservador, base, agressivo) com decisões-chave:
   - opt-in/opt-out training crawlers (GPTBot, ClaudeBot, Google-Extended, Applebot-Extended)
   - Pay-Per-Crawl (HTTP 402) yes/no
   - B2A pilot scope (MCP/NLWeb/OpenAPI)

---

## 8. Stack técnico de 38 camadas (mapeamento por onda)

Taxonomia operacional consolidada (570+ itens avaliáveis):

| # | Camada | Foco | Onda |
|---|---|---|---|
| 1 | Crawlabilidade Técnica | DNS, HTTP, status codes, redirects, render | 1 |
| 2 | Indexabilidade | robots, canonical, x-robots-tag, sitemap | 1 |
| 3 | Arquitetura de Informação | Hubs, clusters, depth, hierarquia tópica | 2 |
| 4 | Estrutura de URL | Path design, slug, parâmetros, trailing slash | 1 |
| 5 | Metadados Essenciais | Title, description, OG, Twitter Cards | 4 |
| 6 | Headings e Hierarquia Semântica | H1 único, Hx hierarquia, interrogativos | 2 |
| 7 | Conteúdo Semântico | Densidade entidades, coerência tópica | 3 |
| 8 | Cobertura de Intenção | informational/commercial/transactional/navigational | 3 |
| 9 | Autoridade Tópica | Topical authority, depth por cluster | 2 |
| 10 | Linkagem Interna | PageRank interno, contextual, anchor descritivo | 2 |
| 11 | Conteúdo do Site | Inventário editorial, profundidade média | 3 |
| 12 | Schema e Dados Estruturados | JSON-LD validation, @graph, mentions/about | 4 |
| 13 | Answer Capsules & Citabilidade | 120–150 char após H2 pergunta | 4 |
| 14 | GEO e IA Generativa | Mention Rate, Citation Rate, Share of Model | 4 |
| 15 | Autoridade Local | Local SEO (opcional, só se braço local) | 5 opt |
| 16 | NAP / Citações Locais | (opcional) | 5 opt |
| 17 | Google Business Profile | (opcional) | 5 opt |
| 18 | Reputação e Reviews | Trustpilot, G2, Google reviews | 5 |
| 19 | Sinais Sociais e Presença Externa | Reddit, LinkedIn, Wikipedia, X, YouTube | 5 |
| 20 | Performance, UX, Experiência Técnica | CWV 2026: LCP <2,0s, INP <200ms, CLS <0,1 | 1 |
| 21 | Auditoria de Bots de IA | Catálogo §9, log analysis | 1 |
| 22 | Força Semântica Global | Cosine pillar↔spokes >0,80 | 2 |
| 23 | LLM Crawler Access | robots.txt, WAF policy, Pay-Per-Crawl | 1 |
| 24 | Schema Authority Stack | @graph aninhado, Wikidata IDs | 4 |
| 25 | Editorial Density | Fatos verificáveis / 100 palavras | 3 |
| 26 | B2A Readiness | NLWeb, MCP, OpenAPI, Web Bot Auth | 5 |
| 27 | Compression Fidelity | Resumo 25 palavras retém tese | 3 |
| 28 | Attribution Gap | Mention Rate × 30 prompts representativos | 4 |
| 29 | Competitive Shadow | Concorrente × query × motivo da citação | 5 |
| 30 | Adversarial Exposure | Spam policies, prompt injection UGC | 5 |
| 31 | Cold Start GEO | Verticais novos, mapping AI consensus atual | 5 |
| 32 | Entity Verification | Wikidata, Knowledge Graph, sameAs ≥5 | 2 |
| 33 | Zero-Click Risk | % tráfego absorvível por AIO/FS/PAA | 5 |
| 34 | Query Fan-Out Readiness | 8 variant types King, sub-query coverage | 3 |
| 35 | Information Gain | Patente Google US10776471B2 | 3 |
| 36 | Retrieval Fitness | Chunks self-contained, entidades disambiguadas | 4 |
| 37 | Source Eligibility | HTTPS, autor nomeado, política editorial pub | 4 |
| 38 | Semantic Coherence | Coerência multi-canal (site + perfis + Wiki) | 2 |
| 39 | Entity Clarity Engine | Drift de limite de entidade < 0,15 distance | 2 |

---

## 9. Bots IA 2026 — catálogo atualizado (maio/2026)

| User-Agent | Owner | Função | Recomendação portal editorial |
|---|---|---|---|
| Googlebot | Google | Search clássico | Allow |
| Googlebot-News | Google | Google News index | Allow |
| Bingbot | Microsoft | Bing + Copilot/ChatGPT parcial | Allow |
| **GPTBot** | OpenAI | **Training** ChatGPT/GPT-5+ (~1.091:1 ratio jul/2025) | Decisão política |
| **OAI-SearchBot** | OpenAI | **Live retrieval** ChatGPT Search | **Allow obrigatório** |
| ChatGPT-User (v1/2/3) | OpenAI | User-triggered fetch | Allow |
| **OAI-AdsBot** | OpenAI | Validação ChatGPT ads (lançado abr/2026) | Allow se monetiza |
| **ClaudeBot** | Anthropic | Training Claude (38.000:1 ratio jul/2025) | Decisão |
| **Claude-SearchBot** | Anthropic | **Retrieval Claude** | **Allow obrigatório** |
| Claude-User | Anthropic | User-triggered Claude | Allow |
| claude-web (legacy) | Anthropic | Legacy identifier | Allow |
| anthropic-ai | Anthropic | Training bulk | Decisão |
| **PerplexityBot** | Perplexity | Index Perplexity (200B+ URLs) | **Allow obrigatório** |
| Perplexity-User | Perplexity | User-triggered | Allow |
| **Google-Extended** | Google | Training Gemini/AI Overviews (não afeta Search) | Decisão |
| GoogleOther | Google | R&D / outros produtos | Allow |
| Google-NotebookLM, Google-Agent, Google-Read-Aloud, Google-CloudVertexBot | Google | Produtos específicos | Allow |
| Applebot | Apple | Search/Siri | Allow |
| Applebot-Extended | Apple | Training Apple Intelligence | Decisão |
| Meta-ExternalAgent | Meta | Meta AI (FB/IG/WhatsApp) | Decisão |
| Amazonbot | Amazon | Alexa + AI features | Allow |
| CCBot | Common Crawl | Alimenta open-source LLMs | Decisão |
| Bytespider | ByteDance | Training TikTok/Doubao (agressivo) | **Geralmente Block** |
| MistralAI-User | Mistral | User-triggered | Allow |
| DuckAssistBot | DuckDuckGo | DuckAssist | Allow |
| Diffbot / YouBot | Diffbot/You.com | Index | Allow |

### Crawl-to-referral ratio benchmarks (Cloudflare set/2025)

| Bot | Ratio | Tendência |
|---|---|---|
| Googlebot | ~14:1 | Estável |
| GPTBot | ~1.091–1.700:1 | Crescente |
| ClaudeBot | 38.000:1 (jul/2025) | Caiu 87% de 286.000:1 em jan/2025 após Claude ganhar web search em mar/2025 |
| Anthropic global | 73.000:1 (jun/2025) | — |
| PerplexityBot | 194:1 | Estável (motor de retrieval, não training) |

**Sinalize qualquer bot training >50.000:1** como candidato a bloqueio se ROI de tráfego não justificar custo de banda.

### Cloudflare Pay-Per-Crawl (HTTP 402, lançado 01-jul-2025)

> "Cloudflare, Inc. is now the first Internet infrastructure provider to block AI crawlers accessing content without permission or compensation, by default."

Para portais com tráfego material por IA, considerar HTTP 402 para training crawlers (GPTBot, ClaudeBot, CCBot, Google-Extended, Applebot-Extended, Meta-ExternalAgent), mantendo **retrieval gratuito** (OAI-SearchBot, Claude-SearchBot, PerplexityBot). Cloudflare atua como Merchant of Record.

---

## 10. KPIs canônicos GEO/AEO/B2A (com benchmarks)

### Tier 1 — SEO clássico (mantidos)

| KPI | Baseline | Target 90d | Fonte |
|---|---|---|---|
| Sessões orgânicas (Google) | X | +5% (defensivo sob AIO) | GSC + GA4 |
| Top-3 keywords não-brand | X | +10% | GSC |
| Indexação efetiva | X% | >95% URLs valiosas | GSC Coverage |
| CWV "Good" URLs CrUX p75 | X% | >75% | CrUX/PSI |
| Páginas com schema válido | X% | >95% | SMV/RRT |
| Featured snippets ganhos | X | +30% | SEMrush/Ahrefs |

### Tier 2 — GEO / AEO

| KPI | Baseline | Target 90d | Benchmark canônico |
|---|---|---|---|
| **Mention Rate ChatGPT** (30 prompts representativos) | X% | >15% | GenOptima: <5% invisível / 5–15% emergente / 15–30% forte / >30% dominante |
| **Citation Rate cross-platform** (4 motores: ChatGPT, Perplexity, Gemini AIO, Copilot) | X% | >10% | — |
| **Share of Model** vs concorrentes top-3 | X% | +50% | GenOptima KPI Framework 2026 |
| **Citation Persistence drift** (D+0 vs D+30) | X% | <30% | Estabilidade indica consenso forte |
| **Multi-Source Consensus** claims-chave | X | ≥3 fontes externas | Wellows 2026: Wiki+Reddit+G2 simultânea 2,8× mais citação cruzada |
| AI Overviews citation rate (queries-prioritárias) | X% | >20% | — |
| Tráfego referral IA (ChatGPT/Perplexity/Copilot/Gemini) | X | +100% (base baixa) | utm_source=chatgpt.com etc |

### Tier 3 — B2A (early stage)

| KPI | Baseline | Target 90d |
|---|---|---|
| Endpoints B2A publicados | 0 | ≥1 (NLWeb ou MCP) |
| OpenAPI spec coverage de APIs públicas | X% | 100% |
| Web Bot Auth implementado | Não | Pilot |
| Política B2A publicada | Não | Sim |

### Brand & autoridade externa

| KPI | Baseline | Target 90d |
|---|---|---|
| Brand mentions externas ≥4 plataformas | X | +25% YoY |
| Wikipedia entry portal + autores top | X | Portal + ≥3 autores |
| Backlinks referring domains 12m | X | Crescente, anchors descritivos |

---

## 11. Templates prontos

Versões completas em `docs/templates/seo-geo-2026/`:

### 11.1 `robots-2026.txt`

Template completo com 20+ user-agents (Search clássico + OpenAI retrieval/training/user + Anthropic + Perplexity + Google AI + Apple + Meta + Amazon + outros relevantes + Bytespider bloqueado). Decisão training (GPTBot, ClaudeBot, CCBot, Google-Extended, Applebot-Extended, Meta-ExternalAgent) por política editorial.

### 11.2 `news-article-schema.jsonld`

NewsArticle em formato @graph aninhado conectando Article → Person (author) → Organization (publisher) → Wikidata IDs em mentions/about. Inclui Speakable em answer capsules. Schema-content parity obrigatória.

### 11.3 `paywall-schema.jsonld`

Paywall declarado conforme Google Search Central 2026: isAccessibleForFree:false + hasPart WebPageElement cssSelector (apenas .class selectors, sem nesting).

### 11.4 `breadcrumb-schema.jsonld`

BreadcrumbList sitewide para páginas profundas.

### 11.5 `llms.txt.template`

Template llms.txt curado <200K tokens com seções: Sobre nós, Autores, Verticais e pillars, Dados proprietários, Optional. **ROI direto marginal hoje (OtterlyAI: 0,1% do tráfego de bot por llms.txt; Search Engine Land: 8 em 9 sites sem mudança mensurável)** — mas valor de opcionalidade baixo custo. Google AI Optimization Guide expressamente afirma que NÃO é necessário; trate como aposta defensiva, não como requisito.

---

## 12. Implicações para a curso-factory

### 12.1 Curso "GEO/SEO 2026" — material novo

Este incremento habilita aulas/módulos como:

| Módulo | Conteúdo central | Verbos Bloom |
|---|---|---|
| Two-Phase JSON-LD | Por que o estudo Ahrefs estava correto e errado simultaneamente | Analisar, diferenciar |
| Princeton GEO playbook | Cite Sources +115%, Stats +41%, Quotes +28% — táticas executáveis | Aplicar, implementar |
| Entity Boundary Drift | Cosine similarity ≥0,95 entre canais; auditoria multi-plataforma | Diagnosticar, calcular |
| Query Fan-Out 8 variant types | Mapear cobertura de sub-queries por pillar | Mapear, projetar |
| Master Prompt 5 Ondas | Execução completa SEO+GEO+AEO+B2A | Implementar, avaliar |
| Bots IA catálogo | Decisões robots.txt + Pay-Per-Crawl + WAF | Avaliar, decidir |
| B2A pilot | NLWeb + MCP + OpenAPI | Projetar, propor |

### 12.2 Pipeline (5 LLMs) — ajustes recomendados

| Agent | Prompt update sugerido |
|---|---|
| **Researcher (Perplexity)** | Incluir nas fontes-âncora: Google AI Optimization Guide (15-mai-2026), Bing AI Performance, Aggarwal et al. arXiv:2311.09735, Reuters Institute 2026, web.dev agent-friendly |
| **Writer (GPT-4o)** | Adicionar Princeton checklist obrigatória (Cite Sources ≥3, Stats ≥5, Quotes ≥1) em módulos GEO/SEO |
| **Analyzer (Gemini)** | Validar Two-Phase JSON-LD theory ao revisar conteúdo schema-related |
| **Classifier (Groq)** | Tags canônicas: `geo-2026`, `aeo`, `aso`, `b2a`, `entity-drift`, `query-fan-out` |
| **Reviewer (Claude)** | Checagem anti-padrão §13 (não vender llms.txt como bala de prata, não tratar schema como silver bullet, não prometer ranking ChatGPT) |

### 12.3 `content_checker.py` — validações novas (opt-in)

| Validação | Critério | Tipo |
|---|---|---|
| Cite Sources count | ≥3 outbound a fontes primárias | Aviso |
| Statistics count | ≥5 estatísticas com fonte e ano | Aviso |
| Quotation count | ≥1 citação direta atribuída | Aviso |
| Compression Fidelity | "Sintetize em 25 palavras" preserva tese | Manual |
| Schema-content parity | Tudo no JSON-LD aparece no HTML visível | Bloqueante |
| Answer capsule | 120–150 char após H1/H2 pergunta em informacional | Aviso |

### 12.4 Cliente template — `config/clients/_template/client.yaml`

Adicionar campos opcionais:

```yaml
geo_2026:
  princeton_playbook_enabled: true       # força checklist Cite Sources/Stats/Quotes
  schema_authority_stack_enabled: true   # exige @graph aninhado em Article
  citation_monitoring_endpoints: []      # lista de prompts a monitorar mensalmente
  b2a_pilot:
    nlweb_endpoint: null                 # URL se publicado
    mcp_endpoint: null
    openapi_spec_url: null
```

---

## 13. Anti-padrões 2026 — o que descartar

### 13.1 "llms.txt é requisito para AI Overviews"

**Falso.** Google AI Optimization Guide (15-mai-2026) afirma textualmente que **não é necessário**. OtterlyAI mediu 84 requests a llms.txt em 62.100 hits de bots IA — **0,1%**. Search Engine Land: 8 em 9 sites sem mudança mensurável. **Trate como opcionalidade defensiva, não como obrigação.**

### 13.2 "Schema é silver bullet de citação em IA"

**Falso.** Estudo Ahrefs (mai/2026) mostra que adicionar schema a páginas já citadas **não as amplifica**. Schema atua **upstream** (Knowledge Graph, entity disambiguation) — não como multiplicador em runtime. Vender schema como "GEO hack" é desalinhado das fontes oficiais e tecnicamente errado.

### 13.3 "GEO substitui SEO"

**Falso.** Google AI Optimization Guide: AI features são ancoradas em RAG + query fan-out **a partir do índice de Search**. Página não indexada = página invisível para AIO/AI Mode. SEO é o pré-requisito; GEO é camada cumulativa.

### 13.4 "Criar 100s de páginas para capturar variações de fan-out"

**Falso e perigoso.** NextGrowth.ai 2026 (ALM Corp 173k URLs): páginas cobrindo **26–50% das sub-queries são citadas MAIS** que páginas cobrindo 100%. **Hub+spoke vence mega-artigo.** Além disso, March 2026 Spam Update derrubou 50–80% do tráfego de sites com publicação massiva de AI sem revisão.

### 13.5 "FAQ schema em qualquer página ajuda em GEO"

**Parcialmente falso.** Google removeu rich result FAQ em 7-mai-2026. AI Mode ainda lê schema FAQ como trust signal **apenas onde FAQ é genuíno** (pergunta real do leitor com resposta auto-contida). FAQ schema decorativo em página de produto/serviço é spam estrutural.

### 13.6 "Bloquear todos os bots de IA com User-agent: * Disallow: /"

**Falso e contraproducente.** Bloquear retrieval bots (OAI-SearchBot, Claude-SearchBot, PerplexityBot) elimina chance de citação. A decisão correta é granular: liberar retrieval/user, decidir training caso a caso, considerar Pay-Per-Crawl (HTTP 402) para training se ROI justificar.

### 13.7 "AI content é penalizado pelo Google"

**Falso.** John Mueller (nov/2025): "Nossos sistemas não se importam se o conteúdo é criado por IA ou humanos. O que importa é se é útil para os usuários." O que viola spam policies é **automação para manipular rankings**, não autoria assistida. AI assistido + revisão humana + first-hand evidence + dados originais permanece intacto pós Core Update mar/2026.

### 13.8 "KPI único é tráfego orgânico Google"

**Insuficiente.** Reuters Institute 2026: -43% queda esperada em 3 anos. CTR caiu 15%→8% sob AIO (Pew 2025). 58,5% zero-click EUA (Semrush 2025). Portal sério precisa medir Mention Rate, Citation Rate, Share of Model, Citation Persistence cross-platform — não só sessões.

---

## 14. Glossário canônico 2026

| Termo | Definição | Fonte |
|---|---|---|
| **AI Overviews (AIO)** | Resumos AI no topo da SERP do Google. 2,5B MAU global. Aparecem em ~48% das queries (Pepper Content fev/2026); até 82% B2B Tech | Google I/O 2026, Pichai keynote |
| **AI Mode** | Modo conversacional do Google Search. 1B MAU em 1 ano; queries dobram a cada trimestre; default global usa Gemini 3.5 Flash desde I/O 2026 | Google blog I/O 2026 |
| **Query Fan-Out** | Decomposição de 1 query em sub-queries paralelas pelo AI Mode. Média 12–15; Deep Search emite "hundreds of searches" | Google I/O 2025/2026 |
| **8 Variant Types** | Tipos de sub-query no fan-out (Michael King iPullRank): equivalent, follow-up, generalization, specification, canonicalization, translation, entailment, clarification | iPullRank Qforia |
| **Information Gain** | Sinal Google operacionalizado em escala no Core Update mar/2026 — Semrush Sensor pico 8,7/10 | Patente US10776471B2 |
| **Answer Capsule** | Parágrafo auto-contido 120–150 char logo após heading-pergunta — formato preferido por LLMs. 72,4% das páginas citadas pelo ChatGPT contêm answer capsule curto | Search Engine Land 2026 |
| **Compression Fidelity** | Capacidade do conteúdo ser comprimido (e.g., "Sintetize em 25 palavras") sem perder a tese | Tratado seogeo 2026 |
| **Citation Persistence** | Estabilidade da citação ao longo do tempo (D+0/D+14/D+30 drift) | Master Prompt 2026 |
| **Multi-Source Consensus** | Corroboração de claim em ≥3 fontes externas independentes | Wellows 2026 |
| **Retrieval Fitness** | Quão bem o conteúdo é "chunkável" e self-contained para pipelines RAG | Master Prompt 2026 |
| **Share of Model (SoM) / Mention Rate / Citation Rate** | % de respostas IA que mencionam a marca vs concorrentes. <5% invisível / 5–15% emergente / 15–30% forte / >30% dominante | GenOptima KPI Framework 2026 |
| **Entity Boundary Drift** | Divergência semântica das menções da marca entre canais; cosine similarity <0,85 = LLM desconsidera sinal | Tratado seogeo 2026 |
| **MCP** (Model Context Protocol) | Padrão aberto Anthropic para agentes consumirem dados de sites | mcp.io |
| **NLWeb** | Projeto open-source Microsoft (R.V. Guha, Build 2025) — converte schema.org/RSS em interface conversacional; cada endpoint é também MCP server | nlweb.ai |
| **B2A** (Business-to-Agent) | Otimização para agentes autônomos. Gartner 2026: 90% B2B intermediado por agentes em 2028 ($15T) | Gartner IT Symposium out/2025 |
| **ASO** (Agentic Search Optimization) | Camada acima de GEO — visibilidade para agentes que comparam/decidem/transacionam | Jarred Smith 2026 |
| **Preferred Sources** | Feature Google: usuário escolhe fontes preferidas; cliques 2× em média | Google Keyword blog (Stein/Zaidi) |
| **Subscription Linking em AIO** | Subscribed label dentro de AI responses; mais cliques em early testing | Hema Budaraju 06-mai-2026 |
| **Pay-Per-Crawl** | HTTP 402 — Cloudflare como Merchant of Record para training crawlers | Cloudflare 01-jul-2025 |
| **Web Bot Auth** | Assinatura criptográfica para verificar bots oficiais | IETF draft 2026 |

---

## 15. Referências primárias

**Documentos canônicos Google (15-mai-2026 e correlatos):**

- Google. *AI Optimization Guide*. developers.google.com/search/docs/fundamentals/ai-optimization-guide
- Google. *AI Features and Your Website*. developers.google.com/search/docs/appearance/ai-features
- Google Blog. *Search's I/O 2026 updates: AI agents and more*. blog.google/products-and-platforms/products/search/search-io-2026/
- Google. *Top ways to ensure your content performs well in Google's AI experiences on Search* (mai/2025 atualizado 2026). developers.google.com/search/blog/2025/05/succeeding-in-ai-search
- Google. *Google Search's guidance about AI-generated content* (fev/2023, atualizado 2026). developers.google.com/search/blog/2023/02/google-search-and-ai-content
- Google. *FAQPage structured data* (atualizado 7-mai-2026). developers.google.com/search/docs/appearance/structured-data/faqpage

**Microsoft / Bing:**

- Bing Webmaster blog. *Introducing AI Performance in Bing Webmaster Tools (Public Preview)*. fev/2026. blogs.bing.com/webmaster/February-2026/Introducing-AI-Performance-in-Bing-Webmaster-Tools-Public-Preview
- Bing Webmaster blog. *Keeping Content Discoverable with Sitemaps in AI-Powered Search*. jul/2025. blogs.bing.com/webmaster/July-2025/Keeping-Content-Discoverable-with-Sitemaps-in-AI-Powered-Search
- Microsoft News. *NLWeb at Build 2025*. news.microsoft.com
- NLWeb spec. nlweb.ai

**web.dev:**

- *Build agent-friendly websites*. web.dev/articles/ai-agent-site-ux

**Cloudflare:**

- Cloudflare Press. *Cloudflare blocks AI crawlers by default*. 01-jul-2025.
- Cloudflare Blog. *Introducing pay per crawl*. 01-jul-2025.
- Cloudflare. *Crawlers, search, and AI bots*. set/2025 (benchmarks crawl-to-referral).

**Papers acadêmicos:**

- Aggarwal, P. et al. *GEO: Generative Engine Optimization*. KDD 2024. arXiv:2311.09735
- Patente Google US10776471B2. *Contextual Estimation of Link Information Gain*.

**Estudos longitudinais / dados de mercado 2026:**

- Ahrefs (Linehan/Guan). *Schema and AI Citations*. mai/2026. ahrefs.com/blog/schema-ai-citations/
- ALM Corp / NextGrowth.ai. *AI Citation Study 2026* (173k URLs longitudinal).
- Reuters Institute. *Journalism, Media, and Technology Trends and Predictions 2026*. Nic Newman, RISJ. 12-jan-2026. reutersinstitute.politics.ox.ac.uk
- Pew Research. *Click rate analysis with AI summaries*. 22-jul-2025.
- Semrush. *Zero-Click Searches Study* via Statista. 04-mai-2025.
- Pepper Content. *AI Overviews coverage by vertical 2026*. (citado no Master Prompt).
- Wellows. *AI Overviews citation patterns 2026*.
- Outpace. *Schema in AI Mode citations 2026* (65–71% citations têm schema).
- Position Digital. *Reddit/Quora presence and LLM citations*. 2026.
- Digital Applied. *Information Gain in March 2026 Core Update*. 2026.
- Daily Geo Insights. *Brand authority signals correlation 2026* (0,334).
- GenOptima. *Mention Rate Benchmarks 2026* (KPI framework).
- searchVIU. *Runtime vs upstream JSON-LD reading experiments*. 2026.

**Gartner:**

- Gartner. *Top Predictions for IT Organizations and Users in 2026 and Beyond*. IT Symposium/Xpo. 21-out-2025. gartner.com (90% B2B by AI agents 2028; $15T).

**Documentos seogeo originais (20-05-2026):**

- "GEO, SEO e AI Search depois do Google I/O 2026" — `docs/research/seogeo-20260520/doc1_io2026.md`
- "A Arquitetura da Síntese Baseada em Recuperação: SEO/AEO/GEO/ASO" — `docs/research/seogeo-20260520/doc2_otimizacao.md`
- "PROMPT-MESTRE EXECUTÁVEL — Auditoria & Otimização de Portal Editorial em 5 Ondas — Edição 2026" — `docs/research/seogeo-20260520/doc3_master_prompt.md`

---

> **Manutenção:** revisar trimestralmente (próxima revisão: agosto/2026). Novos benchmarks de Mention Rate / Citation Persistence / Crawl-to-referral entram aqui; novos updates Google entram em `SEO_KNOWLEDGE_BASE_2026.md`.
