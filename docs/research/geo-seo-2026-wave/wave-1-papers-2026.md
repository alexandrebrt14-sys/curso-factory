# Wave 1 — Papers e Pesquisas 2026 (GEO, RAG, Multi-agent, E-E-A-T)

Pesquisa profunda executada em 2026-05-17 via Perplexity `sonar-deep-research` (4 queries) + retry `sonar-pro` (1 query Q3b) + validacao via WebFetch em 10 papers.

Custo total Perplexity: ~$0.12 (3 queries deep-research vieram com `total_cost: 0` por terem retornado `completion_tokens: 0` mas com search_results carregados; cobranca somente em Q1 = $0.068, Q4b = $0.014, Q3b = $0.053).

KB existente (NAO repetir): Aggarwal 2023 arXiv:2311.09735 e Chen 2025 arXiv:2509.08919.

---

## Q1 — GEO / LLM citation ranking 2026

### Resultado original (sonar-deep-research)

O modelo recusou-se a listar papers de 2026 alegando knowledge cutoff em 2024 e impossibilidade de verificar arXiv IDs. Resposta longa e meta-cognitiva sem citacoes uteis. Custo $0.068.

**Conteudo retornado (trecho)**:

```
The user’s question requests a precise, up‑to‑date catalogue of academic papers published between January and May 2026 on generative engine optimization (GEO)...
Because my training data end in late 2024 and I do not have live access to arXiv or conference proceedings, I cannot safely verify the existence, identifiers, or details of any 2026 papers, and providing such a list would necessarily involve fabrication. In lieu of returning unreliable or invented entries, this report explains in detail why I cannot produce the requested 2026 bibliography...
```

### Retry Q1b (sonar-pro com search_recency_filter=month)

Erro de parsing JSON (escaping shell). Nao retornou conteudo.

**Recomendacao**: papers GEO especificos vao aparecer em Q4 que tambem cobre LLM citation e source selection.

---

## Q2 — Multi-agent LLM orchestration + quality gates + hallucination detection 2026

Sonar-deep-research, 50 search queries, 23.908 citation tokens, 164.494 reasoning tokens. Custo total $0 (Perplexity bug — completion_tokens: 0).

**Citacoes (45 search_results retornados, todos validaveis no arXiv listing 2601-2605)**:

| # | arXiv ID | Titulo | Status |
|---|----------|--------|--------|
| 1 | 2601.02577 | Orchestral AI: A Framework for Agent... | [UNVERIFIED — citado mas nao fetched] |
| 2 | 2602.14259 | Detecting LLM Hallucinations via Embedding Cluster Geometry | [UNVERIFIED] |
| 3 | 2603.15676 | Automated Self-Testing as a Quality Gate: Evidence-Driven Release Management for LLM Applications | [UNVERIFIED] |
| 4 | 2604.25584 | DualFact+: A Multimodal Fact Verification Framework | [UNVERIFIED] |
| 5 | 2602.11790 | An LLM-Based Multi-Agent System for Educational Video Generation | [UNVERIFIED] |
| 6 | 2602.02290 | Hallucination or Creativity: How to Evaluate AI-Generated Scientific Stories (StoryScore) | [UNVERIFIED] |
| 7 | 2603.05471 | Leveraging LLM Parametric Knowledge for Fact Checking without Retrieval | [UNVERIFIED] |
| 8 | 2604.23366 | GSAR: Typed Grounding for Hallucination Detection and Recovery | [UNVERIFIED] |
| 9 | 2605.12943 | Reinforced Collaboration in Multi-Agent Flow Networks | [UNVERIFIED] |
| 10 | 2601.13589 | Motion-to-Response Content Generation via Multi-Agent AI System | [UNVERIFIED] |
| 11 | 2603.15547 | Can LLMs Model Incorrect Student Reasoning? Case Study | [UNVERIFIED] |
| 12 | 2605.08462 | Do Benchmarks Underestimate LLM Performance? Contextual Hallucination Detection | [UNVERIFIED] |
| 13 | **2601.12538** | **Agentic Reasoning for Large Language Models** (Wei et al., 28 autores Illinois) | **[VERIFIED 2026-01-18]** |
| 14 | 2602.08709 | FactSim: Fact-Checking for Opinion Summarization | [UNVERIFIED] |
| 15 | 2603.01940 | CoVe: Training Interactive Tool-Use Agents via Constraint-Guided | [UNVERIFIED] |
| 16 | **2604.00901** | **Experience as a Compass: Multi-agent RAG with Evolving Orchestration** (Li & Ramakrishnan) | **[VERIFIED 2026-04-01]** |
| 17 | 2605.04704 | UVMarvel: Automated LLM-aided UVM Machine | [UNVERIFIED, area HW] |
| 18 | **2602.03128** | **Understanding Multi-Agent LLM Frameworks: A Unified Benchmark** (Orogat, Rostam, Mansour) | **[VERIFIED 2026-02-03]** |
| 19 | **2603.11445** | **Verified Multi-Agent Orchestration (VMAO): A Plan-Execute-Verify-Replan Framework** (Zhang et al., 10 autores) | **[VERIFIED 2026-03-12]** |
| 20 | 2601.15160 | Knowledge Graphs are Implicit Reward Models | [UNVERIFIED] |

(35 outras citacoes salvas em `_raw_q2.json`)

**JSON truncado (primeiros 6000 chars)** — ver arquivo `_raw_q2.json` na pasta.

---

## Q3 — RAG evaluation, embeddings, MTEB 2026

Sonar-deep-research, 80 search queries, 40.020 citation tokens. Custo $0 (bug Perplexity).

**Highlights de search_results (48 total)**:

| # | arXiv/URL | Titulo | Status |
|---|-----------|--------|--------|
| 1 | **2604.26649** | **When to Retrieve During Reasoning: Adaptive Retrieval for Large Reasoning Models** (Guo, Wu, Yiu) | **[VERIFIED 2026-04-29]** |
| 2 | 2605.09661 | A Benchmark for LLMs in Synthesizing Meta-Analysis Conclusion | [UNVERIFIED — search_results confirma 2026-05-10] |
| 3 | 2605.00400 | FollowTable: A Benchmark for Instruction-Following Table Retrieval (IRS metric) | [UNVERIFIED — 2026-05-01] |
| 4 | 2603.12572 | LMEB: Long-horizon Memory Embedding Benchmark | [UNVERIFIED] |
| 5 | 2602.20379 | **Case-Aware LLM-as-a-Judge Evaluation for Enterprise-Scale RAG** (Chhabra, Medrano, Verma) | **[VERIFIED 2026-02-23]** |
| 6 | 2601.16503 | **MRAG: Benchmarking RAG for Bio-medicine** (Li & Zhu) | **[VERIFIED 2026-01-23]** |
| 7 | 2604.18109 | FLiP: factorized linear projection for sentence embedding interpretation | [UNVERIFIED] |
| 8 | 2605.06132 | Reasoning-Aware Reranking for Agent Memory Retrieval (MemReranker 0.6B/4B) | [UNVERIFIED] |
| 9 | 2604.17344 | FLARE: Task-agnostic embedding model evaluation | [UNVERIFIED] |
| 10 | 2604.05764 | Generative Retrieval Overcomes Limitations of Dense Retrieval (LIMIT dataset) | [UNVERIFIED] |
| 11 | 2602.00296 | A Dataset and Benchmark for Adaptive RAG Routing (RAGRouter-Bench) | [UNVERIFIED] |
| 12 | 2604.19047 | RARE: Redundancy-Aware Retrieval Evaluation Framework | [UNVERIFIED] |
| 13 | 2601.16478 | DeepEra: A Deep Evidence Reranking Agent for Scientific Retrieval | [UNVERIFIED] |
| 14 | 2605.14503 | Component-Wise Empirical Study for SE Tasks (RAG testbed decoupling) | [UNVERIFIED — 2026-05-14] |
| 15 | aclanthology.org/2026.eacl-long.391 | Redefining Retrieval Evaluation in the Era of LLMs (EACL 2026) | [UNVERIFIED — venue confirmado] |
| 16 | aclanthology.org/2026.eacl-long.173 | A Representation Sharpening Framework for Zero-Shot Dense Retrieval (EACL 2026) | [UNVERIFIED — venue confirmado] |
| 17 | dl.acm.org/doi/10.1145/3805774 | A Survey on Retrieval-Augmented Text Generation for LLMs (ACM CSUR 2026-05-15) | [UNVERIFIED] |
| 18 | blog.voyageai.com/2026/01/15/voyage-multimodal-3-5/ | Voyage Multimodal 3.5 (com suporte video) | [UNVERIFIED — release blog] |
| 19 | blog.voyageai.com/2026/01/15/voyage-4/ | Voyage 4 family (MoE, shared embedding space) | [UNVERIFIED] |
| 20 | awesomeagents.ai/leaderboards/embedding-model-leaderboard-mteb-april-2026 | MTEB April 2026: Gemini Embedding 001 lidera com 68.32; Jina v4 entrou em abril | [UNVERIFIED] |
| 21 | cohere.com/blog/embed-4 | Embed 4 (multimodal, agentic) | [UNVERIFIED] |
| 22 | pecollective.com/tools/best-embedding-models | Best Embedding Models 2026 (OpenAI text-embedding-3-large $0.13/1M, Cohere embed-v4 $0.10/1M) | [UNVERIFIED — industry rank] |
| 23 | siliconflow.com/articles/en/most-accurate-reranker-for-real-time-search | Top 3 rerankers 2026: Qwen3-Reranker 8B/4B/0.6B | [UNVERIFIED] |
| 24 | futureagi.com/blog/best-rerankers-for-rag-2026 | 7 rerankers comparados 2026 | [UNVERIFIED] |

(24 outras citacoes em `_raw_q3.json`)

---

## Q4 — E-E-A-T, brand authority, LLM citation behavior 2026

Sonar-deep-research, 51 search queries, 23.951 citation tokens. Custo $0.

**Highlights (44 search_results)**:

| # | URL / arXiv | Titulo | Status |
|---|-------------|--------|--------|
| 1 | **2605.06635** | **Cited but Not Verified: Parsing and Evaluating Source Attribution in LLM Deep Research Agents** (Onweller, Lumer, Huber, Ramchandani, Subbiah, Feld) | **[VERIFIED 2026-05-07]** |
| 2 | **2605.14021** | **Measuring Google AI Overviews: Activation, Source Quality, Claim Fidelity, and Publisher Impact** (Xu, Iqbal, Montgomery) | **[VERIFIED 2026-05-13]** — estudo longitudinal 55.393 queries em 40 dias |
| 3 | **2603.18014** | **Real-Time Trustworthiness Scoring for LLM Structured Outputs (CONSTRUCT)** (Goh & Mueller) | **[VERIFIED 2026-02-24]** |
| 4 | yext.com/research/ai-citation-refresh-january-2026 | Yext AI Citation Analysis Spring 2026: 23M+ citations em 17M URLs unicas | [UNVERIFIED — pagina protegida, mas URL existe] |
| 5 | yext.com/research/ai-citation-behavior-across-models | Yext AI Citation Behavior: evidence from 17.2M citations across models | [UNVERIFIED] |
| 6 | hai.stanford.edu/ai-index/2026-ai-index-report | Stanford HAI 2026 AI Index Report | [UNVERIFIED — content truncado mas pagina existe] |
| 7 | oumi.ai/blog/oumis-study-finds-50-of-ai-overviews | Oumi: 50% das AI Overviews untrustworthy; visitas a sites de midia cairam >50% entre 2024 e early 2026 | [UNVERIFIED] |
| 8 | digitalapplied.com/blog/ai-model-hallucination-rate-benchmarks-2026-study | AI Hallucination Rate Benchmarks 2026: extended thinking reduz factual recall em 41% (8.3% to 4.9%), citation accuracy 37% (14.7% to 9.3%) | [UNVERIFIED] |
| 9 | tryprofound.com/blog/best-generative-engine-optimization-tools | Profound: Best GEO Tools 2026 (BrightEdge entity recognition) | [UNVERIFIED] |
| 10 | searchengineland.com/links-brand-signals-seo-authority-model-475968 | "From links to brand signals: The new SEO authority model" | [UNVERIFIED] |
| 11 | idx.inc/newsroom/the-authority-flywheel | IDX: The Authority Flywheel — how to win LLM visibility 2026 | [UNVERIFIED] |
| 12 | galileo.ai/blog/deepmind-facts-framework-llm-factual-accuracy | DeepMind FACTS Framework: 3-judge LLM evaluation, top models so atingem 74% accuracy | [UNVERIFIED] |
| 13 | atlan.com/know/llm-evaluation-frameworks-compared | RAGAS vs TruLens vs DeepEval (2026) | [UNVERIFIED] |
| 14 | goodfirms.co/resources/seo-statistics-ai-search-rankings-zero-click-trends | AI SEO Stats 2026: 58.5% zero-click, 83% AI queries terminam na SERP, so 14% das brands trackeiam AI visibility | [UNVERIFIED] |
| 15 | openai.com/signals/research/2026q1-update | OpenAI Q1 2026: adoption surge entre 35+, gender mais balanceado | [UNVERIFIED — pagina OpenAI oficial] |
| 16 | dailygeoinsights.com/llm-citation-source-selection-research | How LLMs Decide Whom to Cite (2026 research analysis) | [UNVERIFIED] |
| 17 | scale.stanford.edu/ai/repository/enhancing-rag-entity-linking-educational | Stanford SCALE: RAG + Entity Linking para plataformas educacionais | [UNVERIFIED] |
| 18 | 2603.25862 | Methods for Knowledge Graph Construction from Text Collections (PhD thesis) | [UNVERIFIED] |
| 19 | 2602.21728 | Explore-on-Graph: Autonomous Exploration of LLMs on Knowledge Graphs | [UNVERIFIED] |
| 20 | 2604.06028 | Multi-Stage Validation Framework for Trustworthy Large-scale LLM-as-judge | [UNVERIFIED] |

(24 outras em `_raw_q4.json` — inclui CLEF-2026 CheckThat! Lab, MIT GenAI 2026 Forum)

---

## Sumario de validacao

- **10 papers VERIFIED via WebFetch direto no arxiv.org**: 2601.12538, 2601.16503, 2602.03128, 2602.20379, 2603.11445, 2603.18014, 2604.00901, 2604.26649, 2605.06635, 2605.14021.
- **~80 papers UNVERIFIED mas com search_results da Perplexity** (URL + snippet retornados pelo motor de busca — alta probabilidade de existirem).
- **0 papers fabricados** identificados na amostra validada.

## Arquivos brutos salvos

- `_raw_q1.json` (11.996 bytes) — resposta deep-research que recusou
- `_raw_q1b.json` (48 bytes) — erro parsing
- `_raw_q2.json` (15.724 bytes) — 45 search_results multi-agent
- `_raw_q2b.json` (48 bytes) — erro parsing
- `_raw_q3.json` (17.907 bytes) — 48 search_results RAG/embeddings
- `_raw_q3b.json` (12.000+ bytes) — retry sonar-pro com 14 itens curados
- `_raw_q4.json` (16.980 bytes) — 44 search_results E-E-A-T/LLM credibility
- `_raw_q4b.json` (4.180 bytes) — retry com 4 blogs E-E-A-T 2026
