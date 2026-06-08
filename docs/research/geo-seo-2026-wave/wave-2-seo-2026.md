# Wave 2 — SEO 2026 (Pesquisa Profunda Perplexity sonar-deep-research)

**Data:** 2026-05-17
**Wave:** 2 de N (foco SEO 2026: core updates, AI Overviews, Helpful Content, E-E-A-T, Technical SEO)
**Modelo:** `perplexity/sonar-deep-research` · temperature 0.1 · max_tokens 4000-8000 · `return_citations: true`
**Repositório:** `C:/Sandyboxclaude/curso-factory/`
**Comparar com:** `docs/GEO_KNOWLEDGE_BASE_2026.md`

---

## Sumário executivo

5 queries paralelas à API Perplexity. Q1, Q3 e Q5 reenviadas após erros de parsing (apóstrofo no payload inline) e Q1/Q3 reenviadas com `max_tokens=8000` (deep-research consome ~150-300k reasoning tokens internamente — `4000` insuficiente para o output final, `finish_reason=length`).

- **Q1 (Core Updates 2026):** 14.579 chars, 45 citações
- **Q2 (AI Overviews):** 7.315 chars, 50 citações
- **Q3 (Helpful Content System):** 30.549 chars, 50 citações
- **Q4 (E-E-A-T 2026):** 3.288 chars, 50 citações
- **Q5 (Technical SEO 2026):** 5.530 chars, 50 citações

**Total bruto:** ~61KB de análise + 245 fontes (verificáveis por URL).

URLs validadas via WebFetch:
- `https://status.search.google.com/products/rGHU1u87FJnkP6W2GwMi/history` (Google Search Status Dashboard) — confirma Feb 5/2026 Discover update (21d17h), Mar 24/2026 Spam (19h30m), Mar 27/2026 Core (12d4h)
- `https://developers.google.com/search/blog` (Google Search Central blog) — confirma posts: "Optimizing for generative AI" (May 2026), "Back button hijacking spam policy" (Apr 2026), "Inside Googlebot" (Mar 2026), "February 2026 Discover core update" (Feb 2026)
- `https://web.dev/articles/inp` — INP threshold ≤200ms (Good), 200-500ms (Needs Improvement), >500ms (Poor). Sem mudanças anunciadas em 2026.
- `https://web.dev/articles/lcp` — LCP threshold ≤2.5s (Good). Sem mudanças em 2026.
- `https://web.dev/articles/vitals` — CWV oficial: LCP, INP, CLS (sem nova métrica adicionada).

URLs 403 / não validadas via WebFetch (mas referenciadas pela Perplexity como fontes acreditáveis): Search Engine Land library, Search Engine Roundtable update tracker (provavelmente Cloudflare bot challenge).

---

## Q1 — Google Search Core Algorithm Updates (jan-mai 2026)

**Pergunta:** "Google Search core algorithm updates in 2026 - list every confirmed update from January 2026 to May 2026. Include announcement dates, impact, what was targeted, and recovery patterns observed."

### Conteúdo bruto (truncado a 6000 chars)

> # Google Search Core Algorithm Updates in 2026 (January–May): Timeline, Impact, Targets, and Recovery Patterns
>
> From January through May 2026, Google publicly confirmed only two core algorithm updates that affect how content is evaluated and surfaced: the **February 2026 Discover core update**, which exclusively reshaped Google Discover feeds, and the **March 2026 core update**, which globally recalibrated web search rankings. Around these core changes, Google also rolled out a **March 2026 spam update** and a cluster of unconfirmed but clearly felt algorithm refinements in May, all against a backdrop of intensified focus on helpful content, topical authority, Core Web Vitals, and scrutiny of scaled AI-generated material. Together, these developments raised the bar for depth, originality, and user experience, especially for intermediaries and aggregators, while rewarding primary sources, authoritative brands, and sites demonstrating clear topical expertise and local relevance. Recovery data from affected sites and Google's own guidance show that technical performance improvements can begin to be recognized within several weeks, whereas substantial content and authority gains usually materialize over a **3–6 month window** and often coincide with subsequent core updates rather than immediate post-rollout reversals.
>
> ## 1. Context: 2026 Search Landscape and January Baseline
> The **December 2025 core update** (Dec 12-28, 2025) introduced significant refinements in how Google weighted experience, expertise, author signals, and overall content quality, producing large movements particularly affecting news publishers. Googlers reiterated that, beyond these headline events, Google now runs **smaller, unannounced core updates on a rolling basis**. January 2026 had **no confirmed core update**; fluctuations reflected aftermath of December's changes and ongoing smaller adjustments. By month's end, Google was tightening expectations around topical depth, user experience, and originality.
>
> ## 2. February 2026 Discover Core Update
> **Start:** Feb 5, 2026 09:00 PT. **End:** Feb 27, 2026 02:00 PT. **Duration:** ~21 days 17 hours.
> **Scope:** Limited to Google Discover (not web search). **Geography:** US English only initially.
> **Historically notable:** First confirmed Google update of 2026 AND first time Google publicly labeled a core update as Discover-only.
> **3 stated goals:** (a) surface more locally relevant content from sites based in user's own country; (b) reduce sensational content and clickbait; (c) highlight in-depth, original, timely content from sites with demonstrated topic expertise.
> **Impact:** Substantial volatility in Discover traffic Feb 5-27. Clickbait-driven publishers lost **50-70% of Discover impressions**; local news / niche expert blogs / specialist vertical publishers reported gains. Non-US publishers targeting US Discover traffic via syndicated coverage saw declines.
>
> ## 3. March 2026 Spam Update
> **Start:** Mar 24, 2026. **Duration:** ~19h30m (per Google Search Status Dashboard).
> **Target:** Scaled content abuse, expired domain manipulation, site reputation abuse. Enforcement of policies first articulated in March 2024.
> **Impact:** Sites publishing hundreds/thousands of AI-generated pages/day with minimal human review experienced **50-80% traffic drops**. Structural patterns: high semantic similarity across URLs, template-driven content (only city/product names change), AI-translated copies across dozens of languages, near-zero first-hand evidence.
>
> ## 4. March 2026 Core Update
> **Start:** Mar 27, 2026. **Duration:** ~12 days 4 hours (completed Apr 8).
> **Volatility:** SE Ranking — ~80% of top-3 positions changed (vs. 67% Dec 2025); 24% of top-10 pages dropped out of top 100. Semrush volatility sensor peaked at 8.7/10 (highest since Aug 2024 record).
> **Re-weighted dimensions:** (a) information originality / Information Gain; (b) author expertise (E-E-A-T); (c) domain-level topical coherence.
> **Winners:** First-party brand sites, official/government domains, specialist niche publishers (hotel chains and airlines in travel; employer career portals + USAJobs.gov + BLS.gov in jobs; NIH + GoodRx + specialist clinical sources in health).
> **Losers:** Aggregators (YouTube, Reddit, Instagram, TripAdvisor, Yelp, broad financial comparison portals); even WebMD/Mayo Clinic/Cleveland Clinic declined vs. government/institutional sources in health.
> **Recovery patterns:** Technical fixes (CWV, indexability) recognized in weeks. Content/authority gains take **3-6 months** and often coincide with subsequent core updates (not immediate reversals).
>
> ## 5. May 2026 Algorithmic Refinements
> Multiple unconfirmed but clearly-felt refinements; no single named update. Pattern: continued reward of original information, depreciation of derivative content, fine-tuning of Helpful Content classifier.

### Citações Q1 (45 fontes)

- [1] seroundtable.com/january-2026-google-webmaster-report-40696.html
- [2] developers.google.com/search/blog/2026/02/discover-core-update
- [3] amsive.com/insights/seo/google-march-2026-core-update-winners-losers-analysis/
- [4] digitalrootsmedia.com/blog/seo/google-march-2026-core-update-full-breakdown-after-rollout-completion-what-to-do-in-april/
- [5] seovendor.co/google-may-2026-algorithm-updates/
- [6] status.search.google.com/incidents/7eTbAa2jWdToLkraZj5y
- [7] searchengineland.com/march-2026-google-core-update-what-changed-474397
- [8] amaytics.com/google-march-2026-core-update-rollout-is-now-complete.html
- [9] seroundtable.com/april-may-2026-google-webmaster-report-41251.html
- [10] thehoth.com/blog/march-2026-update/
- [11] seroundtable.com/google-march-2026-spam-update-41109.html
- [12] status.search.google.com/incidents/mYbNTqV1ytDc2fA8hUz4
- [15] searchengineland.com/google-february-2026-discover-core-update-is-now-complete-469450
- [19] status.search.google.com/products/rGHU1u87FJnkP6W2GwMi/history
- [25] searchengineland.com/google-march-2026-core-update-rollout-is-now-complete-473883
- [28] searchenginejournal.com/googles-march-core-update-shifted-visibility-away-from-aggregators/573621/
- [35] developers.google.com/search/docs/appearance/core-updates
- (lista completa em `q1_content.txt`)

---

## Q2 — Evolução AI Overviews 2025-2026

**Pergunta:** Evolução AIO, rollout linguístico, estudos de CTR, padrões de citação, ads dentro de AIO, opt-out, lawsuits de publishers.

### Conteúdo bruto (truncado a 6000 chars)

> # The Evolution of Google AI Overviews, 2025–2026
>
> Across 2025 and 2026, Google's AI Overviews moved from an experimental search feature to a central interface for how billions of people access information, triggering profound shifts in click-through rates, publisher economics, advertising models, and regulatory scrutiny. Google expanded AI Overviews to more than 200 countries/territories and 40+ languages, then supported nearly 100 languages through AI Mode, extending AI-mediated search to over a billion additional people in historically underserved linguistic communities. Independent studies consistently documented substantial declines in organic CTR—**often 35-60% for queries where AI Overviews appear**—alongside sharp rise in zero-click behavior and concentration of surviving clicks on small subset of pages cited directly in AI answers.
>
> ## 1. From SGE to AI Overviews
> AI Overviews originated in Search Generative Experience (SGE) experimental features rolling out 2023-2024. May 2024: Google formally launched AI Overviews. Conceptually extended Google's shift from "find pages that might answer" to "directly answer your question while still letting you click through".
>
> ## 2. Transition from experimental to default
> Ahrefs/SEO platforms tracking: AI Overviews triggered on ~6.5% of queries Jan 2025, climbing to ~25% mid-2025, then stabilizing around 15-16% by Nov 2025. BrightEdge: 31% of monitored queries by Feb 2025 in healthcare/education/B2B tech.
>
> **Google I/O 2025:** AI Overviews reaching 1.5B users/month in 200+ countries and 40+ languages. By mid-2025: surpassed 2B monthly users (>50% of Google global user base). In US and India, AIO drove >10% increase in search usage for query types where they appear.
>
> ## 3. Citation patterns (Profound research)
> AI platforms privilege distinct mixes of sources:
> - **Google AI Overviews + Perplexity:** Reddit prominent input
> - **ChatGPT:** Wikipedia dominant
>
> ## 4. CTR studies 2026
> - Digiday: Google AI Overviews linked to **25% drop in publisher referral traffic**
> - SEJ: "AI Overview CTR fell 61% but clicks didn't collapse" — suggests CTR concentration on cited URLs
> - Sharpinnovations / digitalapplied: When AIO present, **~8% of users click regular results vs. ~15% without AIO**
>
> ## 5. Ads inside AIO (2026)
> - Google placing ads above, below, and in some cases within AI Overviews
> - Extended into AI Mode conversational interface
> - Piloting "Direct Offers" — deal-driven ads at point of purchase intent
> - 75M users in AI Mode by 2026 with ads in AI results (digitalapplied)
> - Search ads now optimize around conversational and context-level signals rather than discrete keywords
>
> ## 6. Publisher lawsuits + Regulatory actions 2026
> - **Penske Media** (US) lawsuit against Google AIO
> - **EU press publishers** lawsuits
> - **Leovy v. Google** (Baker Law) authors/illustrators copyright class action
> - **European Commission** formal antitrust investigation into Google's use of online content for AI purposes (ip_26_825, ip_26_203)
> - **UK CMA** proposed package of measures to improve Google Search services in UK (Jan 28, 2026 commentary)
> - **Digital Services Act** — could constrain AI Overviews in EU
> - **DMA** (Apr 16, 2026) Commission proposes measures for Google to share search engine data with third parties
> - **techpolicy.press:** "Why lawsuits over AI summaries will fail" — argues search rankings and AI summaries are protected expressive activity
>
> ## 7. Opt-out mechanisms (2026)
> - **The Register (Mar 19, 2026):** Google says it will let publishers opt-out of AI Overviews (commitments)
> - "Further Exploration" link blocks added to AIO design
> - Subscription labels added
> - Hover previews added
> - Publisher-level controls for generative features being developed

### Citações Q2 (50 fontes)

- [2] blog.google/products-and-platforms/products/search/ai-overview-expansion-may-2025-update/
- [3] searchenginejournal.com/ai-overview-ctr-fell-61-but-clicks-didnt-collapse/572993/
- [4] tryprofound.com/blog/ai-platform-citation-patterns
- [7] lawfold.com/google-ai-overviews-lawsuit-news/
- [10] theregister.com/off-prem/2026/03/19/google-says-it-will-let-publishers-opt-out-of-ai-overviews/
- [13] bakerlaw.com/leovy-v-google/
- [14] blog.google/innovation-and-ai/technology/ai/google-ai-updates-march-2026/
- [25] nextmillennium.com/blog/google-ai-mode-direct-offers/
- [29] jurist.org/news/2025/12/new-york-times-sues-perplexity-ai-over-copyright-infringement/
- [32] digitalcontentnext.org/blog/2026/04/09/the-publishers-playbook-for-the-google-zero-era/
- [33] digiday.com/media/google-ai-overviews-linked-to-25-drop-in-publisher-referral-traffic-new-data-shows/
- [37] thenextweb.com/news/google-ai-overviews-publisher-links-search-traffic
- [38] blog.google/company-news/inside-google/around-the-globe/google-europe/cma-response/
- [39] digital-markets-act.ec.europa.eu/commission-proposes-measures-google-sharing-search-engine-data-third-parties-under-digital-markets-2026-04-16_en
- [40] gov.uk/government/news/cma-proposes-package-of-measures-to-improve-google-search-services-in-uk
- [41] loyensloeff.com/insights/news--events/news/the-european-commission-opens-formal-antitrust-investigation-into-googles-use-of-online-content-for-ai-purposes/
- [44] competitionandmarkets.blog.gov.uk/2026/01/28/improving-the-way-google-delivers-search-services-in-the-uk/
- (lista completa em `q2_content.txt`)

---

## Q3 — Helpful Content System em 2026

**Pergunta:** O que mudou no Helpful Content, comportamento dos classificadores, padrões penalizados vs recompensados, case studies de recovery/demotion.

### Conteúdo bruto (truncado a 6000 chars)

> # The Helpful Content System in 2026
>
> The system no longer merely nudges better pages upward; it primarily works as a **demotion mechanism** that suppresses domains and content clusters deemed unhelpful, thin, unoriginal, or misaligned with user intent. The March 2026 core update sharply reweighted **Information Gain as the dominant content-quality signal**, operationalized scaled content abuse enforcement against AI-heavy sites, and introduced **holistic Core Web Vitals scoring at site level**, producing 20-35% traffic drops for many affected sites and **60-80% losses for AI content farms**.
>
> ## 1. From Update to System (2022-2026)
> - **Aug 2022:** Launch as Helpful Content Update
> - **Mar 2024:** Fully incorporated into core ranking — Google stated this would reduce low-quality, unoriginal content by ~45%
> - **Mar 2024 spam policies:** Scaled content abuse, site reputation abuse, expired domain manipulation
> - **2025:** AI tools made it trivial to produce vast quantities of fluent low-Information-Gain content
> - **Early 2026:** Independent studies argue Google's Helpful Content + core ranking systems now mathematically scoring Information Gain
>
> ## 2. February 2026 Discover Core Update — Entity Authority Shift
> Shift from generic domain authority to **entity authority**. Google's Knowledge Graph contains tens of billions of entities and over a trillion facts. Sites lacking clear entity signals (no About page, unclear ownership, weak structured data, disconnected brand presence) more likely classified as unhelpful regardless of surface quality — termed the **"Disconnected Entity Hypothesis"**.
>
> ## 3. March 2026 Core Update Behavior
> ### Volatility
> - SE Ranking: ~80% of top-3 results changed (vs ~67% Dec 2025); 24% of top-10 pages dropped out of top 100
> - Semrush volatility sensor: peak 8.7/10 (highest since Aug 2024)
>
> ### Category losers (aggregators)
> Aggregators, UGC platforms, comparison-driven sites: YouTube, Reddit, Instagram, TripAdvisor, Yelp, major job boards, entertainment "what to watch" tools, broad financial comparison portals.
>
> **Travel:** Large OTAs and review aggregators lost; hotel chains, airlines, official park/airport sites gained.
> **Jobs/Education:** Job board aggregators declined; employer career portals + USAJobs + BLS.gov rose.
> **Health:** Even WebMD/Mayo Clinic/Cleveland Clinic declined relative to NIH + GoodRx + specialist clinical sources.
>
> ### Holistic Core Web Vitals scoring (NEW in Mar 2026)
> CWV moved from URL-level to **composite site-level scoring**. LCP+INP+CLS aggregated into single performance factor. Failing any one drags down composite. Sites failing one+ CWV thresholds (especially LCP > 3s) lost **8-23% more traffic** than faster competitors even with solid content.
>
> ### Information Gain dominance
> Originally described in 2020 Google patent. In Mar 2026 became "primary discriminator in contested search spaces".
> - **Wins:** Proprietary data, original research, first-hand case studies → 15-25% improvements
> - **Losses:** Templated/rewritten content → 30-50% declines
> - **Catastrophic losses:** Generic AI content farms → 60-80% collapses
>
> **Crucial shift:** Concise 600-word article with one genuinely original benchmark/dataset/insight can outrank a 3,000-word guide that comprehensively paraphrases existing public sources but adds nothing new. Length becomes tie-breaker rather than primary input.
>
> ### 5-dimension Information Gain rubric
> 1. Proprietary data
> 2. First-hand evidence
> 3. Original frameworks or conceptual models
> 4. Expert attribution and verifiable authorship
> 5. Freshness hooks tying content to recent events or data cuts
>
> ## 4. March 2026 Spam Update — Scaled Content Abuse
> Sites publishing hundreds/thousands of AI pages/day with minimal human review: **50-80% traffic drops**. Structural patterns Google detects:
> - High semantic similarity across large swaths of URLs
> - Template-driven content where only city/product names change
> - AI-translated copies across dozens of languages
> - Near-zero first-hand evidence or primary-source citations
>
> SpamBrain signals: publishing velocity anomalies, semantic redundancy, lack of authorship/entity signals, high bounce rates, short dwell times, external link patterns indicative of AI content networks.
>
> ## 5. Two-Surface Visibility
> Zero-click searches account for ~2/3 of queries. When AIO appears, CTR for traditional organic can drop by a third or more.
> - **AI Mode filter in Search Console (2026):** Separates traffic from AI-generated summaries vs traditional organic clicks
> - **"Ghost rankings":** AI models cite/recommend a brand's educational content but steer transactional intent toward better-known competitor
>
> ## 6. Recovery patterns
> Recovery requires deep structural change rather than superficial fixes. Successful recovery profile:
> - First-party data
> - First-hand experience
> - Original frameworks
> - Aligned topical ecosystems
> - Fast, stable user experiences
>
> Time horizon: **technical fixes weeks; content/authority gains 3-6 months and often coincide with subsequent core updates rather than immediate post-rollout reversals**.

### Citações Q3 (50 fontes)

- [3] logicodewebdesigncavan.ie/blog/google-helpful-content-guide.html (origens 2022)
- [5] keywordseverywhere.com/blog/does-google-penalize-ai-content/
- [6] hobo-web.co.uk/the-google-helpful-content-update-and-its-relevance-in-2026/ (síntese principal)
- [11] amsive.com/insights/seo/google-march-2026-core-update-winners-losers-analysis/
- [12] digitalapplied.com/blog/scaled-content-abuse-2026
- [20] digitalapplied.com/blog/e-e-a-t-march-2026-google-rewards-experience-content-guide
- [21] SE Ranking data on March 2026 volatility
- [23] digitalapplied.com (scaled content abuse + SpamBrain)
- [27] Hobo Web (system evolution timeline)
- [28] Google Knowledge Graph entity authority
- [29] digitalapplied.com/blog/information-gain-march-2026
- [32] visibility stack / content-engineering author entity
- (lista completa em `q3_content.txt`)

---

## Q4 — E-E-A-T 2026 e Quality Rater Guidelines

**Pergunta:** Updates do E-E-A-T e QRG em 2026, author entities, knowledge graph, Person schema, sinais usados por LLMs.

### Conteúdo bruto (truncado a 6000 chars)

> # E-E-A-T, Quality Rater Guidelines 2026, and the Rise of Author Entities
>
> 2026 marks a turning point: systems no longer simply parse pages, they assess **people**, **entities**, and **evidence**. Google's E-E-A-T framework sharpened through successive updates to QRG, culminating in 2025-2026 revisions emphasizing:
> - Verifiable authorship
> - First-hand experience
> - Strict standards for YMYL topics
> - Explicit treatment of AI-generated content
>
> March 2026 core update reweighted signals toward **original information, experiential depth, and strong author and brand identity**, often at the expense of generic aggregators and anonymous, surface-level content.
>
> ## 1. Quality Rater Guidelines as Trust Blueprint
> QRG first published publicly in 2015. Updated 2-3 times/year. Guidelines don't define ranking factors directly but shape training/calibration of the ML systems that do. Raters' judgments train evaluation models, which influence how ranking systems weigh quality signals.
>
> **February 2026 QRG update** (seodefend.com #3) — tightened standards for verifiable authorship and AI-generated content treatment.
>
> ## 2. Underlying semantic infrastructure
> - Author entities modeled in **knowledge graphs**
> - Represented in **schema.org Person markup** with `sameAs` links to external profiles (LinkedIn, Wikidata, etc.)
> - Reinforced through consistent bylines, topical focus, and third-party validation
>
> ## 3. LLMs converge on same trust signals
> AI systems and LLM-driven search surfaces — Google's AI Overviews to independent assistants — are converging on very similar trust signals:
> - Recognized entities
> - Structured data
> - Original research
> - Transparent methodology
> - Cross-source corroboration
>
> Hallucinations mitigated through: retrieval, reliability-aware RAG frameworks, multi-view validation.
>
> **Empirical:** AI citation sets are **narrower than SERPs**, skew toward entity-rich, extractable content, increasingly favor brands/authors that appear as stable nodes in the broader web of data rather than those who merely win on traditional keyword or link metrics.
>
> ## 4. Person schema canonical (schema.org/Person)
> Core properties used by Knowledge Graph:
> - `name`
> - `jobTitle`
> - `worksFor` → Organization
> - `affiliation`
> - `alumniOf`
> - `sameAs` (LinkedIn, Wikidata, Wikipedia, ORCID, academic profiles)
> - `knowsAbout` (topics)
> - `image`
> - `url`
>
> ## 5. AI Disclosure 2026 (Dynamis LLP)
> Brands and influencers face new disclosure requirements for AI-generated content. Recent FTC/legal developments require explicit labeling in many contexts.

### Citações Q4 (50 fontes)

- [3] seodefend.com/google-february-2026-quality-rater-guidelines-update-what-changed-and-why-it-matters/
- [5] digitalapplied.com/blog/e-e-a-t-march-2026-google-rewards-experience-content-guide
- [10] schema.org/Person (canônico)
- [11] visibilitystack.ai/academy/content-engineering/author-entity
- [14] digitalapplied.com/blog/schema-markup-after-march-2026-structured-data-strategies
- [19] ai-marketinglabs.com/lab-experiments/how-does-ai-decide-which-brands-to-trust-in-its-search-results
- [21] contently.com/2025/12/29/the-emerging-signals-llms-use-to-trust-your-brand-top-10-platforms-for-2026/
- [25] seroundtable.com/google-search-quality-raters-guidelines-update-40092.html
- [28] groundingpage.com/facts/google-search-quality-rater-guidelines/
- [30] broworks.net/blog/googles-2026-search-quality-rater-guidelines-what-you-need-to-know
- [33] recomaze.ai/how-google-gemini-selects-sources-for-ai-answers
- [37] ziptie.dev/blog/google-ai-overviews-source-selection/
- [38] seomytics.com/author-authority-ranking-signal-how-google-weighs-it-2026/
- [41] dynamisllp.com/knowledge/ai-disclosure-in-2026-recent-developments-and-practical-steps-for-brands-and-influencers
- [48] schema.org/sameAs (canônico)
- [49] artifaktdigital.com/how-unlinked-brand-mentions-help-your-ai-visibility-strategy/
- (lista completa em `q4_content.txt`)

---

## Q5 — Technical SEO 2026

**Pergunta:** Core Web Vitals (INP, LCP, novas métricas), MUVERA multi-vector retrieval, FastEmbed, SSR vs JS, Cloudflare/Vercel CDN, hreflang multi-língua.

### Conteúdo bruto (truncado a 6000 chars)

> # Technical SEO in 2026: Page Experience, Semantic Retrieval, Rendering, CDNs, Internationalization
>
> ## 1. Core Web Vitals 2026
> CWV remain central ranking input. Thresholds (75th percentile of real users):
> - **LCP (Largest Contentful Paint):** ≤2.5s good, 2.5-4s needs improvement, >4s poor
> - **INP (Interaction to Next Paint):** ≤200ms good, 200-500ms needs improvement, >500ms poor
> - **CLS (Cumulative Layout Shift):** ≤0.1 good, 0.1-0.25 needs improvement, >0.25 poor
>
> **Mar 2026 core update operationalized SITE-LEVEL composite CWV scoring** (was URL-level). Failing any one of three drags down composite. Sites failing 1+ CWV (especially LCP > 3s) lost 8-23% more traffic than faster competitors.
>
> Field data measured via **Chrome UX Report** surfaced in **Search Console**.
>
> ## 2. MUVERA multi-vector retrieval
> Google Research blog (research.google/blog/muvera-making-multi-vector-retrieval-as-fast-as-single-vector-search/) + arxiv.org/abs/2504.01818.
>
> MUVERA = "Making multi-vector retrieval as fast as single-vector search". Shifts relevance from keyword coincidence to **semantic similarity and entity relationships**. Production deployment at Google scale enables retrieval systems to use multi-vector embeddings (richer than single-vector) without performance penalty.
>
> ## 3. FastEmbed (Qdrant)
> github.com/qdrant/fastembed + crates.io/crates/fastembed/5.3.1 + langchain integration.
>
> Rust-based, lightweight embedding library. Strong performance/cost ratio. Increasingly adopted in enterprise RAG pipelines and SEO tools that score content embeddings against query embeddings.
>
> ## 4. SSR vs JavaScript rendering (2026 verdict)
> jasminedirectory.com/blog/server-side-rendering-ssr-vs-client-side-the-2026-verdict/
>
> Under universal mobile-first indexing, rendering strategy determines indexability + CWV + crawl efficiency:
> - **SSR / SSG / ISR:** Default recommendation. Fast TTFB, good for CWV.
> - **Partial hydration:** Emerging pattern (Astro, Qwik, Angular 18). Hydrate islands not whole tree.
> - **Pure CSR:** Risky — Google can render JS but crawl budget penalty and CWV impact (LCP often >2.5s).
> - **Dynamic rendering:** Google deprecated (developers.google.com/search/docs/crawling-indexing/javascript/dynamic-rendering).
>
> ## 5. Cloudflare CDN best practices (developers.cloudflare.com/fundamentals/performance/improve-seo/)
> - Cache HTML at edge (where possible) for TTFB
> - Brotli compression
> - HTTP/3
> - Image optimization (Polish, Mirage, Image Resizing)
> - Workers for edge compute (personalization without origin hit)
> - Avoid bot challenges that block Googlebot — use bot management with verified bot allow-list
>
> ## 6. Vercel CDN (vercel.com/docs/cdn)
> - Edge Network globally distributed
> - Edge Functions for SSR at edge
> - Incremental Static Regeneration (ISR) — best of static + dynamic
> - Image Optimization API
> - Automatic Brotli + HTTP/3
> - Vercel Speed Insights surfaces field CWV
>
> ## 7. Hreflang for multi-language SEO
> digitalapplied.com/blog/international-seo-2026-hreflang-multilingual-guide + weglot/contentful/geotargetly guides.
>
> Studies: majority of international sites still misconfigure hreflang. Most common errors:
> - Missing reciprocal annotations
> - Incorrect language codes (e.g., `pt` vs `pt-BR` vs `pt-PT`)
> - Self-referencing missing
> - Mixing hreflang with conflicting canonical
>
> **Alternatives to hreflang considered:** Vary: Accept-Language headers, geotargeting in Search Console (deprecated for ccTLDs), explicit subdirectory structures.
>
> ## 8. AIO citation signals (technical)
> Pages cited within AIO see **~18-35% CTR lift** vs equivalent non-cited rankings. Technical signals facilitating citation:
> - Robust structured data (Article, FAQPage, HowTo, Person, Organization)
> - Clear entity markup
> - Fast performance
> - Crawlable static HTML (no JS gates)

### Citações Q5 (50 fontes)

- [1] developers.google.com/search/docs/appearance/core-web-vitals
- [3] web.dev/articles/inp
- [4] parachutedesign.ca/blog/largest-contentful-paint/
- [6] research.google/blog/muvera-making-multi-vector-retrieval-as-fast-as-single-vector-search/
- [7] arxiv.org/abs/2504.01818 (MUVERA paper)
- [11] jasminedirectory.com/blog/server-side-rendering-ssr-vs-client-side-the-2026-verdict/
- [13] dev.to/playfulprogramming-angular/angular-18-improving-application-performance-with-partial-hydration-and-ssr-2nie
- [14] developers.google.com/search/docs/crawling-indexing/javascript/dynamic-rendering
- [16] developers.cloudflare.com/fundamentals/performance/improve-seo/
- [17] vercel.com/docs/cdn
- [21] digitalapplied.com/blog/international-seo-2026-hreflang-multilingual-guide
- [25] geotargetly.com/blog/hreflang-tag-seo-guide
- [26] github.com/qdrant/fastembed
- [27] docs.langchain.com/oss/python/integrations/embeddings/fastembed
- [31] marketermilk.com/blog/seo-trends-2026
- [37] evertune.ai/resources/insights-on-ai/googles-march-2026-core-update-a-content-best-practices-guide-for-seo-and-ai-search
- [38] searchengineland.com/guide/entity-first-content-optimization
- [43] digitalapplied.com/blog/featured-snippets-ai-overview-era-optimization-2026
- [46] upwardengine.com/blog/core-web-vitals-2026/
- (lista completa em `q5_content.txt`)

---

## Validação WebFetch das principais fontes

| Fonte | Status | Confirma |
|---|---|---|
| Google Search Status Dashboard (`status.search.google.com/products/.../history`) | OK 200 | Feb 5/2026 Discover update (21d17h) · Mar 24/2026 Spam (19h30m) · Mar 27/2026 Core (12d4h) |
| Google Search Central blog (`developers.google.com/search/blog`) | OK 200 | Posts confirmados: "Optimizing for generative AI" (May 2026), "Back button hijacking" (Apr 2026), "Inside Googlebot" (Mar 2026), "February 2026 Discover update" |
| web.dev INP article | OK 200 | INP thresholds inalterados em 2026 (200/500ms) |
| web.dev LCP article | OK 200 | LCP threshold inalterado (2.5s) |
| web.dev Core Web Vitals (`/articles/vitals`) | OK 200 | CWV oficial = LCP + INP + CLS. Sem nova métrica adicionada. |
| Search Engine Land library page | 403 (Cloudflare bot challenge) | Não validável via WebFetch — Perplexity acessou via search API |
| Search Engine Roundtable update tracker | 403 (Cloudflare bot challenge) | Não validável via WebFetch — Perplexity acessou via search API |
| `developers.google.com/search/blog/2026/05/optimizing-for-ai-search` (URL especulativa) | 404 | URL exata desconhecida — somente título confirmado via blog index |
| `developers.google.com/search/blog/2026/02/february-2026-discover-update` (URL especulativa) | 404 | URL exata desconhecida — somente título confirmado via blog index |

**Conclusão de validação:** Os 3 core updates de 2026 (Feb Discover, Mar Spam, Mar Core) e Core Web Vitals thresholds (LCP 2.5s, INP 200ms, CLS 0.1) estão CONFIRMADOS via fontes primárias Google. Demais detalhes (Information Gain dominância, 60-80% drop em AI farms, 18-35% CTR lift em citações AIO) vêm de análises de SE Ranking, Semrush, SISTRIX, Digital Applied, Amsive — não auditados independentemente, marcar `[ANÁLISE DE TERCEIROS]` ao usar.

---

## Arquivos brutos

- `payload_q1.json` / `payload_q3.json` / `payload_q5.json` — payloads canônicos (após fix do parsing error)
- `q1_core_updates.json` (30.9KB) · `q1_content.txt` (14.8KB)
- `q2_ai_overviews.json` (29.3KB) · `q2_content.txt` (7.4KB)
- `q3_helpful_content.json` (48.5KB) · `q3_content.txt` (34.5KB)
- `q4_eeat.json` (23.4KB) · `q4_content.txt` (3.4KB)
- `q5_technical_seo.json` (25.5KB) · `q5_content.txt` (5.6KB)
