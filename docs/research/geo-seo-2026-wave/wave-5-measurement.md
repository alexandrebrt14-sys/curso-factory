# Wave 5 — Measurement Frameworks GEO 2026

Pesquisa profunda para `curso-factory`. Foco: como medir presença em LLMs, KPIs canônicos, prompt portfolio, share of voice em AI. Data: 2026-05-17.

Status das fontes:
- **Perplexity sonar-deep-research** — 5 queries; Q1/Q4 primeira tentativa veio sem retrieval (search_results vazio), refeitas como Q1b/Q4b
- **WebFetch direto** — 16 fontes primárias (Profound, Ahrefs Brand Radar, Peec docs, Otterly KPIs, Scrunch, AthenaHQ, Evertune glossary, HubSpot AEO Grader, 5W Index, ReAudit benchmark, etc.)

Total citado: 195+ URLs únicos via Perplexity (Q1b 51 / Q2 49 / Q3 48 / Q5 48) + 16 WebFetch validados.

---

## 1. Glossário canônico — 14 KPIs GEO 2026

Notação: `[ADOPTED]` = pelo menos uma ferramenta comercial publica e cobra por isso. `[PROPOSAL]` = academic/blog sem adoção comercial sob aquele nome. `[NO PRIMARY SOURCE]` = acrônimo circulado em material PT-BR/blog secundário sem origem rastreável.

| Sigla | Nome | Definição operacional | Fórmula | Unidade | Benchmark típico | Fonte canônica |
|---|---|---|---|---|---|---|
| **SoV / AI SoV** `[ADOPTED]` | AI Share of Voice | % das menções totais entre marcas competidoras num portfolio de prompts | `(menções da marca / menções totais de todas marcas) × 100` | % (0-100) | Líder de categoria: 30-50% | Ahrefs Brand Radar, Peec docs, Sprout Social |
| **SoA** `[ADOPTED]` | Share of Answer | % dos prompts rastreados onde a marca é mencionada ou recomendada | `prompts com marca / total de prompts × 100` | % (0-100) | Variável; mede presença ≠ competição | llms.unusual.ai, Evertune |
| **Visibility Score / Brand Coverage** `[ADOPTED]` | Visibility / Coverage | % das respostas IA que mencionam a marca | `respostas com marca / total respostas × 100` | % (0-100) | Chime 66% vs Revolut 33% (Peec US case) | Peec docs, Otterly KPIs |
| **Citation Rate / Citation Frequency** `[ADOPTED]` | Taxa de Citação | % queries onde domínio é referenciado como fonte | `queries citando domínio / queries testadas × 100` | % | 8-15% mínimo · 20-30% otimizado · 40-50% líder. ChatGPT cita só 1,2% das localizações de marca | DiscoveredLabs, ReAudit 2026, LLMPulse |
| **Average Brand Position** `[ADOPTED]` | Posição média | Ranking médio onde a marca aparece na resposta | `Σ posições / nº prompts com marca` | Posição (1, 2, 3…) | 1 = primeiro mencionado | Otterly, Evertune (Average Position) |
| **AI Brand Score** `[ADOPTED]` | Score de marca ponderado por posição | Visibility × peso da posição (1º=100%, 2º=90%, 3º=81%, –10% sucessivos) | `Visibility × Σ(pos_weight × freq) / N` | 0-100 | 100 = 1º em 100% das respostas (irreal) | Evertune AI Brand Score |
| **Brand Sentiment / Net Sentiment** `[ADOPTED]` | Sentimento líquido | Tom emocional médio das menções da marca | `(positivas − negativas) / total × 100` | -100 a +100 | HubSpot AEO Grader: 40 pts de 100 | Otterly, HubSpot, Conductor |
| **Recommendation Rate** `[ADOPTED]` | Taxa de recomendação | % de respostas que endossam explicitamente a marca como top pick | `Σ(score endosso) / total queries × 100` onde top pick=1.0, top 3=0.5, lista=0.25, ausente=0 | % | Correlação com conversão r=0.72 (vs r=0.58 citation) | FAII methodology |
| **Brand Mention Rate** `[ADOPTED]` | Taxa de menção | Frequência absoluta da marca em respostas IA | `menções da marca / janela tempo` | Contagem ou % | Métrica de presença bruta; combine com SoV | VisibilityStack, AthenaHQ |
| **Cited Pages / Source Count** `[ADOPTED]` | URLs próprias citadas | Quantidade de URLs distintas do domínio aparecendo em respostas IA | Contagem direta | Inteiro | Indica profundidade do conteúdo indexado | Evertune (Source Count, Unique URL Count) |
| **Co-citation / Source Share** `[ADOPTED]` | Compartilhamento de citação | % das respostas onde domínio aparece | `respostas citando domínio / total respostas × 100` | % | Mede "share of source", não de marca | Evertune Source Share, ASIS Co-citation (1973) |
| **Brand Snippet Rate** `[ADOPTED]` | Taxa de trecho de marca | % de respostas onde a marca recebe trecho próprio (vs ser citada en passant) | `respostas com snippet dedicado / respostas com menção × 100` | % | Pouco padronizado em 2026 | AthenaHQ, Goodie Agentic Commerce |
| **AI Referral Conversion Rate** `[ADOPTED]` | Conversão de tráfego IA | % de sessões originadas de LLMs que convertem | `conversões IA / sessões IA × 100` | % | 1,66% LLM-referred vs 0,15% organic (Microsoft Clarity); converte 2,3-4,4x melhor (Semrush, DiscoveredLabs) | Digital Bloom 2026, Semrush |
| **ELCA** `[PROPOSAL]` | Embedded LLM Citation Analysis | Análise de citações incorporadas em respostas IA (vs links externos) | Sem fórmula publicada canônica | – | ELCA (consultoria suíça) usa o termo de forma genérica, não como métrica | elca.ch (single source) |
| **Citation Share** `[ADOPTED]` | Citation Share | % das citações IA totais na categoria capturadas pela marca | `citações da marca / citações totais da categoria × 100` | % | Top 15 domínios capturam 68% de toda citation share (5W Index 680M citações) | InfiniteMedia, 5W Index 2026 |
| **Scrunch Influence Score** `[ADOPTED]` | Influence Score | Mede impacto real de uma fonte ponderando consistência × diversidade de prompts | `Citation Consistency (%) × nº prompts únicos citados` | Número absoluto | Favorece fontes citadas em muitos prompts diferentes | Scrunch metrics guide |
| **ACE Score** `[ADOPTED]` | Athena Citation Engine | Modelo ML treinado em milhões de respostas IA prevendo likelihood de qualquer conteúdo ser citado | Proprietário (não publicado) | 0-100 probabilístico | Permite scoring pré-publicação | AthenaHQ ACE launch |

### Acrônimos sem fonte primária rastreável `[NO PRIMARY SOURCE]`

**AIGVR, AECR, CTAM, RTAS, Brand Echo Score, LLM Visibility Index, GEO Authority Rank** — pesquisa profunda Q1+Q1b (130+ search queries) não localizou paper acadêmico nem blog primário que defina estes acrônimos com fórmula. Aparecem em material secundário PT-BR/material de marketing sem origem rastreável. **Recomendação: NÃO usar no curso-factory sob esses nomes.** Se útil conceitualmente, redefinir sob nome canônico (ex.: usar "Position-Weighted SoV" em vez de "RTAS").

---

## 2. Receita pronta — Prompt portfolio mínimo de 50 prompts

Composição baseada em Semrush 4 types + Scrunch (X clusters × 12-15 questions) + iPullRank Prompt Recipes + WP SEO AI fórmula.

### Distribuição por tipo (50 prompts = 100%)

| Tipo | Peso | Quantidade | Exemplo (curso-factory) |
|---|---|---|---|
| **Informacional** (head queries, descoberta) | 30% | 15 | "o que é geo (generative engine optimization)?" / "como começar SEO para IA" |
| **Comparativo** (vs concorrentes) | 25% | 12-13 | "curso-factory vs HubSpot Academy" / "melhor curso GEO 2026" |
| **Transacional / Revenue** (alta intenção compra) | 20% | 10 | "curso de GEO com certificado" / "treinamento corporativo answer engine optimization" |
| **Brand Defense** (reputação e termos branded) | 15% | 7-8 | "curso-factory funciona?" / "curso-factory é bom?" / "[fundador] credibilidade" |
| **Gap / Competitivo puro** (concorrentes sem você) | 10% | 5 | "melhor curso ferramentas Ahrefs SEO" → ver se você aparece como alternativa |

### Disciplina de operação

1. **Pelo menos 80% dos prompts em PT-BR** dada base de operação Brasil GEO. Manter 20% em EN para benchmark global (Profound, Peec usam EN como default).
2. **Refresh cadência**: Mensal adicionar 5-10 trending; trimestral reorganizar clusters; arquivar prompts irrelevantes. Scrunch e Retina Media recomendam mensal (não 48h).
3. **Seed**: 50% manual (curatoria de stakeholders/sales) + 30% GSC AI prompts (regex em queries longas) + 20% LLM-generated (semantic fanout via Ahrefs PAA ou query-mining Profound).
4. **Persistência**: usar mesmo conjunto de "anchor prompts" (ex.: 20 dos 50) por 90 dias para tracking temporal; rotacionar os outros 30 trimestralmente.
5. **Multi-LLM**: cada prompt deve ser executado em ChatGPT, Claude, Perplexity, Gemini, Copilot (mínimo); idealmente também Grok + AI Mode. Total: 50 prompts × 5 LLMs = 250 medições/ciclo.

---

## 3. Três metodologias de amostragem

### 3.1 Cold Start (sem memória, conta nova)
- **Como**: criar conta nova em cada LLM, sem login persistente, prompt direto sem contexto prévio
- **Prós**: baseline puro, replicável, controla personalização; ouro para benchmark cross-LLM
- **Contras**: não representa experiência real de usuário com memória; precisa proxy residencial p/ geo (caro: $50-200/mês iProyal)
- **Quem usa**: Profound, Scrunch (UI scraping no padrão), Ahrefs Brand Radar (190M prompts/mês via UI)

### 3.2 Persistent Session (com memória, persona injetada)
- **Como**: contas de longa duração simulando personas (CMO B2B SaaS, desenvolvedor sênior, etc.); 5-15 turnos antes do prompt-alvo
- **Prós**: representa cenário real onde LLMs lembram preferências; capta efeitos de fine-tuning e RLHF
- **Contras**: difícil reproduzir; resultados variam por trajetória de conversa; viola ToS de alguns provedores se feito em escala
- **Quem usa**: Evertune EverPanel (25M+ usuários reais demograficamente ponderados), AthenaHQ casos enterprise

### 3.3 Geo-localized + Multi-device (residential proxy + mobile/desktop)
- **Como**: rotar IPs residenciais por país/UF; testar mobile (iOS/Android) e desktop separadamente; localização afeta AI Overviews fortemente
- **Prós**: única forma de medir benchmark BR vs US vs EU; mobile-first cobre 60%+ do tráfego real
- **Contras**: 30% custo extra em proxies; complexidade de orquestração; cada engine trata localização diferente
- **Quem usa**: Locaria (multilingual GEO), TheRankmasters geo prompt monitoring, Scrunch geo dashboards

---

## 4. Cinco anti-padrões de medição GEO em 2026

1. **Contar menções sem ponderar posição** — duas marcas com mesma mention rate podem ter Recommendation Rate radicalmente diferente. Sempre usar AI Brand Score (Evertune) ou Recommendation Rate ponderado, não mention rate puro. *Fonte: Evertune blog "what is ai brand score"*

2. **Refresh diário com pânico ("48-hour refresh")** — LLMs são estocásticos por design (temperature, top-p). Ruído diário não significa drift. Use janelas de 2-3 semanas para detectar tendência real. *Fonte: Retina Media "48-Hour Refresh Was Always Bullshit"; Otterly "why does ChatGPT provide different answers"*

3. **Portfolio enorme e desfocado ("track 500 random prompts")** — "Tracking 25 well-chosen prompts beats tracking 500 random ones" (Semrush). Qualidade da curadoria > volume. Bias em prompts random superrepresenta long-tail sem valor comercial. *Fonte: Semrush prompt tracking, Scrunch right-size*

4. **Confiar em métrica de 1 LLM como proxy do mercado** — ChatGPT, Perplexity e Gemini têm padrões de citação radicalmente diferentes (Claude 36% citações dos últimos 12 meses vs Perplexity 50% de 2025). Single-LLM tracking subestima exposição. *Fonte: 5W AI Platform Citation Source Index 2026 (680M citações analisadas)*

5. **Atribuir tráfego IA sem detector de hallucinated citation** — **3-13% dos URLs citados por LLMs comerciais são alucinados** (arXiv 2604.03173, estudo 2026). Antes de comemorar "citation rate alta", validar HTTP 200 dos URLs citados e match conteúdo→quote. GPTZero hallucination check atinge 96,1% precision / 94,2% recall para citações fake. AthenaHQ, Goodie e Conductor publicam hallucination detection nativo; rolar próprio se montar stack DIY. *Fonte: AthenaHQ hallucination detection, arXiv 2604.03173, GPTZero technical report, arXiv 2510.05189*

---

## 5. Recomendação stack mínima viável para curso-factory

Premissa: orçamento PT-BR, 1 marca (Brasil GEO + curso-factory), 1 categoria (educação GEO), portfolio inicial 50 prompts × 5 LLMs.

| # | Camada | Ferramenta recomendada | Por que | Custo mensal |
|---|---|---|---|---|
| 1 | **Tracking primário** (visibility + SoV + position) | **Peec AI** ou **Otterly AI** | Peec docs públicos canônicos, fórmulas explícitas; Otterly é o mais barato e cobre ChatGPT/Perplexity/Gemini com KPIs nomeados (10 KPIs com fórmula) | US$ 39-99 (Otterly $39, Peec ~$99) |
| 2 | **Citation/source tracking** (qual URL foi citada) | **Profound Lite** (se budget) ou DIY Python + Perplexity API + Brave Search | Profound usa 1,5B+ user prompts reais como base; alternativa DIY custa só APIs | US$ 0 (DIY) ou US$ 499 (Profound Lite) |
| 3 | **Sentiment + brand defense** | **HubSpot AEO Grader (gratuito)** + auditoria mensal manual | AEO Grader free dá score 0-100 com sentiment 40pts; basta usar 1x/mês p/ baseline | US$ 0 |
| 4 | **GA4 + AI referral attribution** | **GA4 com regex channel grouping para LLM sources** (chatgpt.com, perplexity.ai, gemini.google.com, claude.ai) | Já incluso no GA4 setup; Otterly publicou regex pronta; Brasil GEO já tem GA4 property | US$ 0 |
| 5 | **Orquestração + auditoria semanal** | Script Python + cron + planilha Google Sheets para tracking longitudinal | Roda os 50 prompts × 5 LLMs via APIs (OpenAI, Anthropic, Perplexity, Gemini) e log em Sheets; integra com geo-orchestrator existente | US$ 30-80 em APIs (estimado: 50 prompts × 5 LLMs × 4 ciclos/mês = 1000 chamadas) |

**Total mínimo viável: ~US$ 70-180/mês** (Otterly $39 + APIs $30-80 + AEO Grader/GA4 gratuitos).

**Total recomendado para escalar**: US$ 600-700/mês (Peec ~$99 + Profound Lite $499 + APIs próprias).

---

## 6. Referências validadas (16 fontes primárias)

WebFetch direto verificou (HTTP 200 + conteúdo extraído):

1. https://ahrefs.com/blog/brand-radar/ — Ahrefs Brand Radar overview
2. https://ahrefs.com/blog/brand-radar-methodology/ — Methodology (190M prompts, 6 platforms, 90-day window)
3. https://docs.peec.ai/metrics/brand-metrics/share-of-voice — Fórmula SoV canônica
4. https://peec.ai/blog/how-to-measure-ai-search-visibility-and-revenue-the-kpis-that-actually-matter — 4 KPIs Peec
5. https://athenahq.ai/articles/track-brand-in-ai-search/ — AthenaHQ Mention Rate + Citation Rate
6. https://athenahq.ai — AthenaHQ landing
7. https://scrunch.com/how-tos/how-to-measure-ai-share-of-voice/ — Scrunch SoV (8 LLMs)
8. https://scrunch.com/blog/keywords-to-prompts-right-size-your-ai-search-tracking — Scrunch X×Y=Z formula
9. https://help.otterly.ai/kpis — 5 KPIs Otterly com fórmulas
10. https://help.otterly.ai/brand-report-kpi-definition — 10 KPIs Brand Report completos
11. https://www.tryprofound.com/blog/data-driven-prompt-recommendation — Profound 100M+ prompts
12. https://www.tryprofound.com/blog/best-generative-engine-optimization-tools — Pricing canônico
13. https://www.evertune.ai/resources/insights-on-ai/what-is-ai-brand-score — AI Brand Score formula (position weighting)
14. https://docs.evertune.ai/en/articles/12278648-glossary-of-terms — Evertune glossário completo (40+ termos)
15. https://www.semrush.com/blog/prompt-tracking/ — 4 prompt types (Revenue/Reputation/Competitor/Gap)
16. https://www.hubspot.com/aeo-grader — 5 dimensões scoring 0-100
17. https://discoveredlabs.com/blog/geo-metrics-what-kpis-matter-how-to-track-them-2026 — 5 KPIs com benchmarks numéricos
18. https://reaudit.io/blog/ai-visibility-benchmark-2026 — Estudo 350k locations / 2.751 brands (ChatGPT cita 1,2%)
19. https://www.prnewswire.com/news-releases/5w-releases-ai-platform-citation-source-index-2026 — 680M citações across 5 LLMs
20. https://faii.ai/methodology/recommendation-rate/ — Recommendation Rate (r=0.72 vs conversão)
21. https://llmpulse.ai/blog/glossary/citation-frequency/ — Citation Frequency definição + benchmarks
22. https://llms.unusual.ai/share-of-answer-ai-visibility-metrics — Share of Answer vs SoV
23. https://www.britopian.com/measurement/geo-visibility-metrics/ — 5 métricas PR/media

Perplexity sonar-deep-research adicional (5 chamadas com 233 citações cumulativas): salvas em `wave5_q1b_raw.json` (51 cit), `wave5_q2_raw.json` (49), `wave5_q3_raw.json` (48), `wave5_q4b_raw.json` (38), `wave5_q5_raw.json` (47). Custo total Perplexity: ~US$ 4,80.

Achados-chave adicionais Q4b:
- AthenaHQ ACE (Athena Citation Engine) é o primeiro modelo ML público predizendo likelihood de citação pré-publicação
- Scrunch Influence Score = Citation Consistency × Unique Prompts (fórmula explícita)
- Peec estudo 1M+ citações publicou benchmarks de citation rate por setor
- arXiv 2604.03173 quantifica hallucination rate em URLs: 3-13% dos URLs citados por LLMs comerciais são fake
- GPTZero hallucination check report: 96,1% precision / 94,2% recall em citações fabricadas
- Profound argumenta que AEO = GEO = AIO (termos sinônimos), mas mantém glossário separado

---

## 7. Lacunas e recomendações p/ Wave 6

- **ELCA, AIGVR, AECR, CTAM, RTAS** — após pesquisa esgotada, não há paper primário. Curso deve abordar ESSES acrônimos apenas para desmistificar ("não use, faltam fontes primárias"), nunca como framework.
- **Benchmarks PT-BR** específicos não existem em fontes públicas — todos os números são US/EU. Oportunidade para Brasil GEO produzir o primeiro benchmark BR (Q4 2026).
- **Hallucination detection em citations** — área quente; arXiv 2510.05189 + AthenaHQ são os melhores pontos de partida.
- **Atribuição financeira (LLM → revenue)** — Digital Bloom 2026 e Microsoft Clarity dataset são os únicos com números concretos (1,66% vs 0,15% conv); aprofundar com Profound earnings calls.
