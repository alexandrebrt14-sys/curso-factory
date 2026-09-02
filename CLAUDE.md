# curso-factory — Instruções Claude Code

## Memória de decisões do projeto

Decisões de arquitetura, erros-a-evitar e insights vivem em `wiki/decisions/` como
arquivos `.md` versionados — a fonte da verdade, com índice navegável em
[`wiki/decisions/INDEX.md`](wiki/decisions/INDEX.md) (inclui os ADRs existentes).
Formato: **Verdade Compilada** (topo, reescrito quando o entendimento muda) + **Linha
do Tempo** (append-only). Guia e template em `wiki/decisions/README.md`.

Três disciplinas ao registrar conhecimento:
1. **Dedup antes de gravar** — se a decisão já existe, atualize-a; não duplique.
2. **Cross-link na escrita** — toda decisão nova linka 2-3 relacionadas via `[[nome]]`.
3. **Candidate-gate** — o hook de fim de sessão rascunha em `candidates/` (não
   versionado, não autoritativo); promova destilando numa decisão real.

Orçamento de contexto: cada linha do `INDEX.md` < ~200 caracteres; o detalhe mora no
arquivo da decisão, nunca no índice. O histórico datado de abril/2026 foi movido para
`wiki/decisions/CLAUDE-CHANGELOG.md`.

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

**Incremento canônico jun/2026 (operacionaliza a redação para GEO):**
- [`docs/GEO_REDACAO_CHECKLIST_2026.md`](docs/GEO_REDACAO_CHECKLIST_2026.md) — novo, 03-06-2026. **Rubrica de redação empírica de 13 técnicas com lift de citação medido** (Aggarwal/Princeton, AutoGEO ICLR 2026, GEO-SFE/Berkeley), mapeada para módulos de curso. É a fonte que o prompt `draft.md` carimba e que o `content_checker.py` valida por contagem (Cite Sources ≥3, Statistics ≥5, Quotation ≥1, answer capsule). **Referência obrigatória para qualquer módulo que deva competir por citação em LLM.**
- [`docs/GEO_KNOWLEDGE_BASE_2026_V3.md`](docs/GEO_KNOWLEDGE_BASE_2026_V3.md) — novo, 03-06-2026 (V3, delta sobre a V2). Consolida o que a literatura/mercado produziram entre 20-mai e 03-jun: **AutoGEO (GEO Score/GEU Score, +50,99%)**, **earned media 84%** (Muck Rack), **Selection Rate × Absorption Rate** (SIGIR 2026), super-geo (severidade Blocker/High/Med/Low + 4 tiers de agent-readiness), Karpathy LLM Wiki (ingest/query/lint), Multi-LLM Sampling Wave, os **13 conceitos novos (51-63)**, papers Q2 2026 (FeatGEO, GhostCite 14-95% citações fabricadas, SIGIR AIO 51,5%) e descobertas pós-I/O.
- [`docs/GEO_EARNED_MEDIA_2026.md`](docs/GEO_EARNED_MEDIA_2026.md) — novo, 03-06-2026. Evidência dura de que **earned media = 84% das citações de IA** (paid = 0,3%, GEO-morto); framework EMGE de 5 estágios, técnicas de colocação, KPIs K-EM-001 a 006, gap de PR de ~2%. Deriva o item 13 da rubrica e o Conceito 63.

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

**Nota (22-jul-2026):** o antigo corpus `docs/knowledge/geo-aeo/` não existe mais no repositório; a trilha canônica de conhecimento é a sequência de waves em `docs/research/` (a lista de papers 2026 verificados vive na wave julho-22).

**Wave Junho 2026 (07-06-2026)** — adiciona aos anteriores sem substituir:
- [`docs/research/geo-wave-junho-2026/GEO_WAVE_JUNHO_2026_CANONICAL.md`](docs/research/geo-wave-junho-2026/GEO_WAVE_JUNHO_2026_CANONICAL.md) — **doc canônico (300 linhas)**, delta 03-jun → 07-jun, gerado pelo orchestrator 5 LLMs (4 deep-research Perplexity + 1 board). Vira material didático direto: (a) **framework de 5 camadas de medição de GEO** = espinha de uma trilha "Como medir GEO" (1 aula por camada) + aula "Regra dos 9 KPIs e a língua do RevOps"; (b) **módulo novo "Ecossistema de ferramentas de AI Visibility 2026"** (Profound/Peec/Ahrefs/Semrush/Scrunch-Sitecore US$225M/Conductor/Clarity — o que cada uma habilita em qual camada; caso Digiday: "medição é triangulação, não número único"); (c) **fundamento técnico da rubrica de redação** (`GEO_REDACAO_CHECKLIST_2026.md`) agora verificável via ~25 papers da camada semântica/vetorial — chunkability (`2603.06976`), citation **absorption** vs selection (`2604.25707`, dataset `geo-citation-lab`), self-containment, alinhamento semântico; (d) fatores-gatekeeper de `2605.25517` (recência, número específico, match estrito de tópico) como checklist para `writer.py`/`reviewer.py`; (e) aula avançada "O motor é um agente, não um rankeador" (EcoGEO `2605.12887` + agentes sintéticos de teste com RAG local). Tags `classify.md` ganham `citation-absorption` e `entity-embedding`. **§7.3 é a aplicação específica deste repo** (4 módulos novos + base técnica da rubrica + prompts). Raw em [`raw/`](docs/research/geo-wave-junho-2026/raw/).

**Wave Junho 15B 2026 (15-06-2026, 2ª passada)** — adiciona aos anteriores; vira material didático direto:
- [`docs/research/geo-wave-junho-15b-2026/GEO_WAVE_JUNHO_15B_2026_CANONICAL.md`](docs/research/geo-wave-junho-15b-2026/GEO_WAVE_JUNHO_15B_2026_CANONICAL.md) — **doc canônico**, pesquisa viva cruzada (Perplexity `sonar-pro` com citações reais — raws `P1..P7.json` — + WebSearch/WebFetch do Claude com fonte primária). Aulas/módulos novos: (a) **aula "Como o motor escolhe a fonte" (pipeline de 4 estágios, §2)** — indexação BM25+vetor+grafo → recall híbrido + **query fan-out** → reranking cross-encoder + chunks citáveis → geração+atribuição; exercícios de answer capsule (40–80 palavras), chunking semântico e cobertura de fan-out; (b) **módulo de medição corrigido (§3)** — taxonomia SoV / **Answer Inclusion Rate** / Citation Rate ("Share of Answer" NÃO é termo técnico) + leitura crítica de benchmarks (RCT ISB-CMU −38% vs estudo observacional vs vendor claim — sempre nomear metodologia); (c) **atualização do módulo de ferramentas (§4)** — Profound US$1bi, **Scrunch→Sitecore (3-jun)**, Semrush×Perplexity MCP nativo, **Microsoft Clarity AI Citations grátis** como porta de entrada; ressalva "cada SoV não é comparável entre fornecedores"; (d) **aula de guardrail (Lily Ray, §6)** — táticas populares de GEO tratadas como spam (prompt injection/scaled content) → entra no prompt do `writer.py`/`reviewer.py` como proibição; (e) fundamento da rubrica reforçado por `2605.25517` (relevância tópica + recência + especificidade > formatação) e `2603.06976` (chunking semântico vence fixo-por-caractere). **§7.3 = aplicação deste repo** (3 módulos + base técnica + guardrails). **CORREÇÕES (§8):** "Share of Answer" não normalizado; AIPREF = header `Content-Usage` + robots.txt (NÃO `/.well-known/ai-preferences`); citar GEO-16/`2509.08919` como **set/2025**. Lembrete do repo: parágrafos justificados + acentuação PT-BR completa (carimbar `COPY_PROMPT_PREFIX.md` em sub-agents de geração longa). Raws em [`raw/`](docs/research/geo-wave-junho-15b-2026/raw/).

**Wave Junho 19 2026 (19-06-2026)** — adiciona aos anteriores; pesquisa profunda em 3 LLMs de ponta com web ao vivo (OpenAI `gpt-5.5` Responses+`web_search`, Gemini 3.1 Pro grounding, Perplexity `sonar-deep-research`) + doublecheck do Claude:
- [`docs/research/geo-wave-junho-19-2026/GEO_WAVE_JUNHO_19_2026_CANONICAL.md`](docs/research/geo-wave-junho-19-2026/GEO_WAVE_JUNHO_19_2026_CANONICAL.md) — **doc canônico delta**, foco no que a 15B não tinha: (a) **Google oficializa "GEO para Search é SEO"** (guia AI optimization do Search Central, 15-mai/15-jun) revelando RAG + **query fan-out** e listando 5 táticas "não precisa fazer" (llms.txt, markup-p/-IA, chunking, reescrita-p/-IA, overfoco em structured data) → aula "O que o Google realmente disse sobre GEO"; (b) **estudos causais Ahrefs que derrubam mitos (§2/§7)** — schema NÃO move citação (1.885 páginas diff-in-diff: AIO −4,6%) e 97% dos llms.txt nunca recebem requisição (137k domínios) → módulo "Anti-clichês de GEO: o que a evidência causal diz"; (c) **infra de medição (§5)** — GA4 canal "AI Assistant", GSC AI reports (impressão, sem CTR) + opt-out UK; (d) papers novos `2605.12887` EcoGEO (ecossistema de evidência) e `2605.21948` SCI-Defense; (e) comentários (Michael King "naive and self-serving", Roger Lynch "planejar como se o tráfego fosse zero"). **§7 = tabela de desmistificações** (carimbar no `reviewer.py` como proibições de copy). **§8 = aplicação direta nos ativos.** Raws em [`raw/`](docs/research/geo-wave-junho-19-2026/raw/).

**Wave Julho 2026 (14-07-2026)** — adiciona aos anteriores sem substituir; **inclui uma revogação de correção da 15B**; 6 rodadas em 4 provedores cloud (Perplexity ×2, OpenAI, Anthropic, xAI) + doublecheck Claude em fonte primária:
- [`docs/research/geo-wave-julho-2026/GEO_WAVE_JULHO_2026_CANONICAL.md`](docs/research/geo-wave-julho-2026/GEO_WAVE_JULHO_2026_CANONICAL.md) — **doc canônico delta** 19-jun → 14-jul: (a) **§7.1 REVOGA a correção §8.5 da 15B** — a Adobe **concluiu** a compra da Semrush (anúncio 19-nov-2025, US$ 1,9 bi; fechamento final de abr/2026; press release + 8-K verificados) → corrigir qualquer aula/copy que afirme "Semrush independente"; (b) **Semrush AI Visibility Index 2026 expandido** (26-jun; 126 mi prompts; ChatGPT ~15 fontes/resposta vs Gemini ~3; só 36 marcas no top-100 das 4 plataformas) e **81% vs 36%** (integração SEO+GEO vs separado) → argumento central de aulas de estratégia; (c) **estratégia por engine** (Profound 6,8 mi citações: Gemini 52,15% owned; ChatGPT 48,73% terceiros; Perplexity reviews) → módulo "uma estratégia por motor"; (d) concentração de referral (ChatGPT 92,4%; Claude cresceu 64x, ultrapassou Perplexity em mar-26) e **conversão por vertical com faixa 1,3x–23x** (§7.3 **proíbe "IA converte 4–5x" como constante** — carimbar no reviewer junto com §7.1); (e) **§5 funil vetorial mensurável** (`similarity → hit rate@k → rerank survival → citation share`, 7 métricas + chunks autocontidos 2–4 frases com entidade nomeada) → bloco prático para módulos técnicos e técnica adicional de citabilidade no `draft.md`; (f) **§4 framework de execução** (workflow 7 etapas, 10 papéis, cadência, 5 gates alinhados 1:1 ao `content_checker.py`, report de 8 perguntas) → esqueleto do módulo "como operar um programa de GEO". **§8.3 = aplicação neste repo.** §7.2 refuta 2 alucinações do Grok (Profound/Peec). Raws em [`raw/`](docs/research/geo-wave-julho-2026/raw/).
- [`docs/research/geo-wave-julho-22-2026/GEO_WAVE_JULHO_22_2026_CANONICAL.md`](docs/research/geo-wave-julho-22-2026/GEO_WAVE_JULHO_22_2026_CANONICAL.md) — **doc canônico delta** 14-jul → 22-jul, foco no CORPUS CIENTÍFICO: **32 papers arXiv verificados** (existência+abstract via API, XMLs em raw/; PDFs não lidos — ler antes de citar em copy/paper). Núcleo: (a) **survey crítico `2607.14035`** (45 estudos): GEO é pipeline estocástico; "nenhuma técnica demonstra efeito causal estável cross-plataforma sobre descobribilidade orgânica" (abstract textual) → antídoto contra promessa inflada; adota o **vetor de visibilidade em 4 camadas** (descobribilidade/citação/absorção/resultado); (b) **medição**: visibilidade como DISTRIBUIÇÃO com N execuções (`2604.07585`; mínimos: N≥5 monitoramento, N≥30 pré/pós), **controle on-domain** para descontar tailwind da plataforma (`2606.04362`: glasp 5,7x bruto vira 1,63x na razão e 1,82x no modelo; placebo p=0,16), **seleção ≠ absorção de citação** (`2604.25707`: ChatGPT cita menos com mais influência; rubrica mensal de absorção no §2.4), escada de estatura de marca (`2606.20065` Ranqo: global 73% / mid 44% / nicho 11%; listicles best-of ~21% das citações; sentimento flipa 6,7x mais que menção); (c) **alavancas com evidência** (§3, em ordem): relevância+posição no contexto (`2605.25517`, 252k trials), evidência extraível, preço explícito e data com atualização substantiva, estrutura 3 níveis (+17,3% citação, `2603.29979`), perfil documento-nível (`2604.19113`), portfólio de queries (`2601.13938`); formatação pura tem efeito pequeno; (d) **fronteira agêntica** (§4): diagnóstico ANTES de reescrita (`2603.09296`: +40% mudando 5% do conteúdo), skills por motor com validação causal (`2604.19516`), sites **agent-ready** (`2607.12056`: 89,3% vs 49,3% de sucesso de agente), horizonte pós-citação DAH (`2604.03656`); (e) **defesas e governança** (§5): SCI-Defense e afins classificam autoridade fabricada/comparativos/alegações temporais como manipulação (propostas acadêmicas, não implementação confirmada dos motores) → GEO agressivo tem prazo de validade; `2601.00912` (Discovery Gap): scores GEO não predizem descoberta, SEO tradicional sim → confirma "GEO = camada sobre SEO sólido"; (f) **indústria pós-14-jul** (§6): Brand Radar 406M+ prompts (atualiza ~340M), Ahrefs CTR −58% vs esperado (bruto ~79% em 2 anos, parte secular), seoClarity: ChatGPT REDUZIU citações externas desde mar/26 (janela AEO estreitando), Conductor AgentStack (apps LLM+MCP), llms.txt: 97% dos arquivos com zero requisição de IA; (g) **§7.4 NOVA regra de precedência epistemológica intra-wave** (7 níveis de fonte; níveis 6-7 nunca canonizam número sozinhos). Precedência entre waves: **Julho-22 §7 > Julho §7 > Wave 19 §7 > 15B §8**. **§8.3 = aplicação neste repo** (5 aulas candidatas novas: medição como distribuição, seleção vs absorção, diagnóstico antes de reescrita, agent-ready, GEO ético e defesas; `research.md` exige arXiv ID verificado; Checklist de Citabilidade no `draft.md` ganha evidência extraível + preço/data + estrutura 3 níveis; `content_checker.py`/`reviewer.py` alinham com SCI-Defense). Crítica GPT-5.5 (65 pontos) aplicada; raws em [`raw/`](docs/research/geo-wave-julho-22-2026/raw/).
- [`docs/research/geo-wave-julho-22b-2026/GEO_WAVE_JULHO_22B_2026_CANONICAL.md`](docs/research/geo-wave-julho-22b-2026/GEO_WAVE_JULHO_22B_2026_CANONICAL.md) — **doc canônico delta** (22-jul): INFRAESTRUTURA de GEO — crawlers, controle de acesso e atribuição, aterrado em docs oficiais acessadas em 22-jul-2026. Núcleo: (a) **matriz de crawlers por finalidade** (§2.1: treino=GPTBot/ClaudeBot/Google-Extended-token; busca=OAI-SearchBot/Claude-SearchBot/PerplexityBot; ação de usuário=ChatGPT-User/Claude-User/Perplexity-User, e estes dois últimos podem ignorar robots.txt por doc oficial); default Brasil GEO = liberar tudo, matriz restritiva só p/ conteúdo sensível, com linha EXPLÍCITA de Google-Extended; (b) **§7 REVOGA do corpus** o claim "bloquear Google-Extended remove de AIO" — AIO/AI Mode usam o Googlebot NORMAL (doc oficial); exposição em AIO gerencia-se com nosnippet/max-snippet/noindex; (c) **GA4**: canal default "AI Assistants" (medium ai-assistant; EXCLUI AIO/AI Mode que seguem em Organic Search; Perplexity ausente da lista em 22-jul) + custom channel group com regex ANCORADA (§4.1) + convenção utm_medium=ai-assistant; (d) **dark traffic**: ~70,6% das visitas de IA chegam sem referrer [vendor Loamly] → GA4 é o PISO do canal, declarar em todo report; (e) **crawl-to-referral** como métrica de troca justa (Anthropic ~70.900:1 em jun/2025; painel vivo radar.cloudflare.com/ai-insights prevalece); (f) Cloudflare: Content Signals Policy, AI Crawl Control, e POLÍTICA ANUNCIADA de bloqueio default Training/Agent em páginas com anúncios (15-set-2026, novos domínios CF); (g) **claims machine-readable com validade** (§6, novo padrão). **§5.3 = aplicação neste repo** (aula candidata "O encanamento do GEO"; atualizar template robots.txt de docs/templates/seo-geo-2026/ para a matriz por finalidade).
- [`docs/research/geo-wave-julho-22c-2026/GEO_WAVE_JULHO_22C_2026_CANONICAL.md`](docs/research/geo-wave-julho-22c-2026/GEO_WAVE_JULHO_22C_2026_CANONICAL.md) — **doc canônico delta** (22-jul): BRASIL + regulatório + segurança agêntica. Núcleo: (a) **Brasil primeira linha**: Modo IA pt-BR desde 08-set-2025 (primária Google BR); UCP/checkout no AI Mode reportado desde 19-mai-2026 [imprensa; primária pendente]; 3º maior usuário de ChatGPT [vendor via secundária]; Datafolha 93% usam IA MAS inclui IA embutida (não equivale a busca por IA); delegação de compra a agentes ainda 15%; (b) **mapa imprensa×IA**: Estadão×Google (dez/25), Folha×Google, Folha+UOL×OpenAI (25-mai-26); frente ANJ+Abert+Aner; CADE em fase avançada [classe processual a confirmar] — efeito dos acordos sobre citação é HIPÓTESE testável, não fato; (c) **regulatório com vetos**: PL 2338 NÃO aprovado (nunca citar como lei; reavaliar trimestral); CONAR = corresponsabilidade AUTORREGULATÓRIA por conteúdo de IA desde 01-jun-2026; LGPD já rege dados em pipelines; sandbox ANPD não é salvo-conduto; "OWASP LLM Top 10 2026" NÃO existe (vigente = 2025); (d) **segurança agêntica** (§6): prompt injection indireta demonstrada (Comet/Atlas, PoC) E observada in the wild (Unit 42) — checklist "agent-friendly sem virar vetor" (§6.2, 5 itens); Web Bot Auth/Signed Agents = padrão EMERGENTE draft (sinal positivo, nunca bloqueio único); (e) claims machine-readable (§9). **§8.3 = aplicação neste repo** (aulas "GEO no Brasil" e "Agent-ready sem virar vetor"; reviewer ganha os 2 vetos do §7: PL 2338 não é lei, OWASP 2026 não existe).

**Wave Agosto 2026 (27-08-2026)** — adiciona aos anteriores e em parte **CORRIGE**; 10 rodadas em 5 provedores com web ao vivo (Perplexity `sonar-pro` ×6 — as 4 `sonar-deep-research` em paralelo deram ReadTimeout aos 25 min —, Gemini 3.1 Pro grounding ×2, OpenAI `gpt-5.5` web_search, xAI `grok-4.6` via Agent Tools API) + doublecheck Claude (5 arXiv de jul–ago na página do arXiv, 30 URLs com sentinela):
- [`docs/research/geo-wave-agosto-2026/GEO_WAVE_AGOSTO_2026_CANONICAL.md`](docs/research/geo-wave-agosto-2026/GEO_WAVE_AGOSTO_2026_CANONICAL.md) — **doc canônico delta** 22-jul → 27-ago: FRAMEWORKS DE EXECUÇÃO, KPIs, REPORT e motores. Núcleo: (a) **o motor escolhe onde buscar antes de buscar** — 16–17% das fan-out queries do ChatGPT com `site:` desde 08-ago [Promptwatch/Willison]; Reddit 12% → 3% no ChatGPT Search [Similarweb 23-ago]; (b) **Google, em doc oficial, ignora `llms.txt`/markup especial e não exige chunking**; Mueller 24-ago: "nothing really special"; fan-out pages para manipular = scaled content abuse; **Preferred Sources (20-ago)** com badge em AIO/AI Mode; goto URLs (26-ago) quebram séries de scraping; **NÃO existe core update de agosto** (só spam 18–20-ago); (c) **ChatGPT Ads no Brasil (11-ago, OpenAI)** + Similarweb AI Ads → report separa orgânico | citação IA | referral | **pago em IA** | conversão (§5.3); (d) **volume de prompt não existe**: Ahrefs "AI adjusted volume" (17-ago, só proxy após 31-ago); Rand 12-ago: análise de citação engana; (e) **Cloudflare 15-set**: Training e Agent bloqueados por default em páginas com ads de domínios novos; (f) **corpus**: GEO-Flag `2608.16824` (detector F1 0,944; 8,90% das páginas recuperadas são GEO-otimizadas, 16,36% em 2026 → anti-padrões 1/5 viram risco mensurável), `2608.13956` (diversidade de documentos > duplicata/paráfrase, experimento controlado), `2606.00898` v2 (métrica de alucinação mede cobertura do grafo), reranker por rubrica `2608.03527`; (g) **framework de execução em 10 etapas** com cadência e papéis (§4) e **"GEO URL Ledger"** de 10 blocos (§5.4) — Conductor Pages Report (23-jul), Semrush ROI direto/assistido/autodeclarado/modelado (27-jul), Profound Index Summer 2026 (1,9 bi conversas; liderança é local em 24/30 indústrias); (h) vendors: Ahrefs 38% overlap AIO×top-10 (era 76%), CTR −58% com AIO, 5,3% do top é 100% IA. **§8 CORRIGE**: `llms.txt` rebaixado a "opcional, nunca entregável/KPI"; AI Mode 1 bi MAU × 0,13% das visitas são medidas diferentes (não compor); Reddit sai dos exemplos; xAI `chat/completions`+`search_parameters` está morto (410 → `/v1/responses`+`x_search`). Raw em [`raw/`](docs/research/geo-wave-agosto-2026/raw/). **§9.3 = aplicação neste repo** (aulas "O motor escolhe antes de buscar" e "O que o Google disse que ignora"; template de report §5.4 como exercício; aula GEO-Flag com os 5 anti-padrões; reviewer ganha 4 vetos: core update de agosto, volume de prompt sem rótulo, Reddit estável, `llms.txt` entregável; `writer.py` com bloco de evidência diversa).

Citar `§X.Y` dos KBs/INCREMENT/WAVE ao tomar decisões. **Em conflito de fato datado, prevalece a wave mais recente nos itens explicitamente marcados como correção: Agosto (§8 — `llms.txt` rebaixado, AI Mode 1 bi MAU × 0,13% visitas não se compõem, Reddit fora dos exemplos, core update de agosto inexistente, API xAI) > Julho (§7 — Adobe×Semrush, conversão por vertical) > Junho 19 (§7 — schema, llms.txt, "GEO = camada técnica separada") > 15B (§8); fora desses itens, o corpus anterior segue valendo.** Atualizar trimestralmente (próxima: agosto/2026).


## 2026-06-03 — Citabilidade GEO operacional + KB V3 (rubrica de redação que vira gate)

Incremento que **fecha o gap** entre a doutrina de GEO (que o repo já tinha em profundidade) e o que o pipeline efetivamente produz e valida. Confronto de junho com o conhecimento mais novo dos repos irmãos (`landing-page-geo/docs`: AutoGEO, earned media, conceitos 51-63) confirmou que as promessas do log de 2026-05-20 ("como aplicar no pipeline") **nunca tinham sido implementadas** — só documentadas. Agora foram.

**Documentação nova:**
- `docs/GEO_REDACAO_CHECKLIST_2026.md` — rubrica de 13 técnicas com lift empírico, mapeada para módulos de curso. É o "como escrever para o maior ganho em GEO".
- `docs/GEO_KNOWLEDGE_BASE_2026_V3.md` — a V3 prevista pela V2 (§12): AutoGEO/GEO+GEU Score, earned media 84%, Selection×Absorption, super-geo 4 tiers, Karpathy lint, MLSW, conceitos 51-63, papers Q2 2026, descobertas pós-I/O.
- `docs/GEO_EARNED_MEDIA_2026.md` — earned media como camada dominante (84% vs paid 0,3%), framework EMGE + KPIs K-EM.

**Código (promessas de 2026-05-20 agora CUMPRIDAS):**
- ✅ `src/templates/prompts/pt-br/draft.md` — nova seção "Checklist de Citabilidade GEO" (Cite Sources ≥3, Statistics ≥5, Quotation ≥1, answer capsule por H2, chunkability, Single Idea, Information Gain) + 4 itens no checklist de autoavaliação.
- ✅ `src/validators/content_checker.py` — contadores `_count_cite_sources`, `_count_statistics`, `_count_quotations` e detector `_has_answer_capsule`; bloco GEO opt-in em `check_content(text, module_name, geo_config=...)` (erro bloqueante com playbook ligado, aviso com desligado, ausente = retrocompatível).
- ✅ `src/clients/context.py` + `loader.py` — `Geo2026Config` (`princeton_playbook_enabled`, `min_cite_sources/statistics/quotations`, `require_answer_capsule`, `schema_authority_stack_enabled`), carregado de `client.yaml` bloco `geo_2026`.
- ✅ `src/validators/quality_gate.py` — passa `self.client.geo` ao `check_content`.
- ✅ `src/templates/prompts/pt-br/classify.md` — tags canônicas `geo-2026`, `citation-ready`, `aeo`, `aso`, `b2a`, `entity-drift`, `query-fan-out`.
- ✅ `config/clients/default/client.yaml` — bloco `geo_2026` ligado (Brasil GEO é GEO-first); `_template/client.yaml` documentado e desligado.
- ✅ `tests/test_validators_smoke.py` — 7 testes novos dos contadores + comportamento opt-in + retrocompatibilidade.

**Aplicação no pipeline (atualizada):** o redator (GPT-4o) recebe a rubrica carimbada; o gate conta os mínimos; o classificador emite as tags GEO; o revisor (Claude) trata `[FALTA EVIDÊNCIA]` para garantir Cite Sources reais (GhostCite mostra 14-95% de citações fabricadas em LLM — fonte verificável virou diferencial de GEO, não só higiene). Para ligar em outro cliente: bloco `geo_2026` no `client.yaml`.


## 2026-05-20 — Incremento canônico pós Google I/O 2026 (SEO+GEO+AEO+B2A)

Adicionado em `docs/SEO_GEO_INCREMENT_20260520.md` o material consolidado de 3 fontes canônicas datadas mai/2026 sobre o estado da arte SEO+GEO+AEO+B2A pós Google I/O 2026 (15-mai-2026). **Não substitui** os 5 docs canônicos existentes (`GEO_KNOWLEDGE_BASE_2026.md`, `_V2`, `SEO_KNOWLEDGE_BASE_2026.md`, `AI_DISCOVERY_STANDARDS_2026.md`, `GEO_50_CONCEITOS_CANONICAL.md`) — **complementa** com camada operacional: Master Prompt 5 Ondas executável, 38 camadas técnicas mapeadas, Princeton GEO playbook (lifts mensurados), Two-Phase JSON-LD theory, Entity Boundary Drift, 8 Query Fan-Out variant types de King, ASO/B2A com NLWeb+MCP, anti-padrões 2026 e templates prontos (robots.txt, JSON-LD, llms.txt).

**Como aplicar no pipeline:**
- `writer.py` (GPT-4o): incluir Princeton checklist obrigatória em módulos GEO/SEO — Cite Sources ≥3 outbound, Stats ≥5 com fonte+ano, Quotes ≥1 atribuída
- `analyzer.py` (Gemini): validar Two-Phase JSON-LD theory ao revisar páginas schema-related
- `classifier.py` (Groq): tags canônicas `geo-2026`, `aeo`, `aso`, `b2a`, `entity-drift`, `query-fan-out`
- `reviewer.py` (Claude): aplicar Anti-padrões §13 (llms.txt não é requisito; schema não é silver bullet; GEO ≠ substituto de SEO)
- `content_checker.py`: validações opcionais Cite Sources count, Statistics count, Quotation count, Compression Fidelity, Schema-content parity (bloqueante)
- `client.yaml`: campos `geo_2026.princeton_playbook_enabled`, `geo_2026.schema_authority_stack_enabled`, `geo_2026.b2a_pilot.{nlweb_endpoint,mcp_endpoint,openapi_spec_url}`


## Histórico (changelog)

Mudanças aplicadas datadas de abril/2026 — refactors (multi-tenant, 5 waves), base de conhecimento GEO/AEO e auditorias (Waves A-D) — foram movidas para [`wiki/decisions/CLAUDE-CHANGELOG.md`](wiki/decisions/CLAUDE-CHANGELOG.md), mantendo este arquivo enxuto no contexto. As **regras vivas** seguem abaixo.

## Regras Fundamentais

### Frontend — layout, UX, animação, contraste (LEIA ANTES de mexer em template visual)
Playbook canônico: **`docs/FRONTEND_PLAYBOOK.md`** — como este repo é um GERADOR, corrija sempre no TEMPLATE para que todo curso gerado herde a prática. Cobre: layout/UX/navegabilidade de conteúdo longo, régua de stacks premium 2026, **REGRA inviolável de contraste WCAG AA nos dois temas** (dark/light; spans inline; `pre` com fundo escuro fixo), **parágrafos justificados** (`text-justify`), **animação à prova de falha** (nunca esconder dependendo de JS; CSS `fill:both`; `prefers-reduced-motion`), **auditoria da SAÍDA renderizada** (dois temas, transições mortas, cache-bust, iterar até zerar) e catálogo de **erros frequentes** (inclui acentuação em geração longa). Defeito no template multiplica por todos os cursos — pegue cedo.

### Peso visual do curso gerado (LEIA ANTES de gerar curso)
Doutrina canônica: **`docs/DOUTRINA_VISUAL_CURSOS.md`**. Desde 27/08/2026 a obrigação editorial é o TETO de apoios visuais por aula (`tetos.D.figuras_max` em `config/lexicos.json`), e só quando a peça substitui texto; o piso por módulo e o teto de 1.200 caracteres por parágrafo seguem como rede do motor de renderização da landing (`config/quality_rules.yaml > validation.visual_density`), não como régua de escrita. **O que mudou no gerador:** o contrato de geração passou a emitir seis tipos de bloco visual (`figure`, `dataTable`, `comparison`, `statGrid`, `stepGuide`, `timeline`), declarados sempre nos mesmos quatro lugares (`src/models.py`, `src/schemas/course.schema.json`, `src/templates/page.tsx.j2` e o filtro `js_json` de `src/generators/tsx_generator.py`); o parser promove sozinho tabela, lista numerada de passos e imagem com legenda; e a camada `visual_density` do `config/quality_rules.yaml` deixou de ser declarativa e é cobrada dentro de `TsxGenerator.render_page`. Curso que nasce como coluna de texto **não chega a virar arquivo**: a cobrança levanta `VisualDensityError` antes da renderização. Curso legado atravessa com `cobrar_peso_visual=False`, com os achados só no log.

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
1. Perplexity (sonar-deep-research) → pesquisa, fundamentação acadêmica e análise competitiva
2. GPT-5.5 → planeja as aulas de cada módulo e redige UMA aula por chamada, em linguagem simples (fonte de estilo escrita-empreendedor), com a pesquisa inteira
3. Gemini (3.1-pro-preview) → análise pedagógica do rascunho inteiro, aula a aula, em 7 dimensões
4. Gemini (3.7-flash) → classificação, tags e metadados, a partir do rascunho (a Groq saiu do parque do geo-orchestrator em 2026-07-08)
5. Claude (sonnet-5) → revisão final UMA aula por chamada, devolvendo o texto inteiro; revisão que encolhe o texto é descartada e o rascunho fica ($5 max/curso)

O cliente LLM (`src/llm_client.py`) classifica toda falha (cota, chave, modelo, rate limit, transitório, formato) e reage por classe: cota e modelo morto tiram o provedor da sessão sem retry; o fallback é a cadeia `fallback_chain` de `config/providers.yaml`; HTTP 200 sem texto não abre circuito. Detalhe em `wiki/decisions/cliente-llm-resiliente.md`. Os modelos seguem o `catalog/model_catalog.yaml` do geo-orchestrator (v4.6, task_routing: research, writing, analysis, classification, review); mudar modelo é mudar `config/providers.yaml` e o agente, nunca hardcode em prompt. Cada etapa recebe o RASCUNHO (não a saída da etapa anterior). Até 02/09/2026 a revisão recebia o JSON da classificação e devolvia um relatório no lugar do curso; ver `wiki/decisions/geracao-por-aula-e-insumo-correto.md`.

### Prompts Externos (IMPORTANTE)
- Os prompts dos 5 agentes ficam em `src/templates/prompts/*.md`
- Os agentes em `src/agents/` carregam automaticamente o prompt externo via `base.py`
- Para alterar o comportamento de um agente, edite o arquivo .md correspondente
- Se o arquivo .md não existir, o agente usa o TEMPLATE inline como fallback
- NUNCA duplicar instruções entre o prompt externo e o template inline


## Padrão Editorial — Regras de Qualidade

Fonte normativa: [`DIRETRIZ_EDITORIAL.md`](DIRETRIZ_EDITORIAL.md) (v3, 11/08/2026) e o anexo [`GUIA_ESCRITA_HUMANIZADA.md`](GUIA_ESCRITA_HUMANIZADA.md). Em conflito, a diretriz prevalece sobre o resumo desta seção.

### Estilo HSM/HBR/MIT Sloan
- Tom analítico, direto, orientado por dados, sem jargão vazio
- Uma ideia central por parágrafo, desenvolvida até a ideia terminar. O ritmo vem do conteúdo: período longo para raciocínio com causa e ressalva, frase curta quando houver o que enfatizar. PROIBIDA qualquer cota de ritmo (frase curta por parágrafo, alternância programada, teto fixo de linhas), que produz staccato de manchete
- Dados e estatísticas para sustentar argumentos, nunca afirmar sem evidência
- Evitar superlativos sem evidência ("o melhor", "revolucionário")
- Narrativa obrigatória: abrir em situação concreta com tensão explícita, conduzir por um caso nomeado, cumprir a promessa da abertura e fechar retomando esse caso (diretriz §3)

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

### Molde da aula (unidade de geração desde 02/09/2026)
- A unidade que o pipeline escreve, revisa e mede é a AULA, uma por chamada de LLM
  (`Orchestrator._draft_lesson`), com a pesquisa inteira no prompt
- Os números da aula (palavras, H2, H3 por H2, figuras, parágrafo) vêm de `config/lexicos.json`,
  espelho da fonte de estilo `escrita-empreendedor`, e entram no prompt como variáveis
  (`{palavras_alvo_min}`, `{figuras_max}`...). NUNCA repita número de régua em prompt ou doc
- Abertura de 2 ou 3 frases dizendo o que o aluno vai conseguir fazer; 2 a 4 H2 (o normal são
  três: por que a ideia muda o resultado; como fica no seu negócio; faça agora); H3 só em H2
  acima de 350 palavras; nada de H4 nem subtítulo por linha terminada em dois-pontos
- Um exercício por aula, com título, etapas numeradas com dado real do aluno, resultado esperado
  e dica. Sem bateria de exercícios
- Apoio visual é TETO (até `figuras_max` por aula), só quando substitui texto. Sem piso de
  tabela, blockquote, negrito ou figura
- Objetivos, pré-requisitos, glossário, FAQ e fontes datadas vivem no nível da trilha: o
  pipeline os escreve UMA vez por módulo, depois da última aula, como `# Trilha n: título`
  (`Orchestrator._close_trail`, prompt `trail.md`); a revisão pula essa unidade e o gate não
  aplica a ela a régua da aula. A camada GEO (fontes, estatísticas, citação, cápsula) é cobrada
  sobre o curso inteiro, nunca por aula
- Bullets com `-- ` (dois hífens), NUNCA `- ` (um hífen), no conteúdo renderizado pelo `FormattedText`

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

### REGRA — Parágrafos SEMPRE justificados (invariável)
Todo conteúdo de texto gerado por este repositório (drafts → páginas) deve sair com
**parágrafos justificados** — o equivalente canônico do estilo `<p align="justify">`.
- No stack React/Tailwind deste repo, isso é materializado por `className="text-justify"`
  (NÃO usar o atributo HTML deprecado `align="justify"` em JSX/TSX).
- Todo `<p>` de corpo emitido pelo template deve conter `text-justify`. O parágrafo de corpo
  do `FormattedText` (`src/templates/page.tsx.j2`, ~linha 483) já cumpre — NUNCA remover esse
  utilitário ao editar o template, e replicá-lo em qualquer novo `<p>` de texto corrido.
- Vale para qualquer destino: se um curso for exportado para HTML cru / PDF / e-mail (onde o
  Tailwind não roda), emitir o atributo literal `<p align="justify">` no artefato exportado.
- Sub-agentes que escrevem páginas/drafts: carimbar esta regra no prompt junto ao bloco de
  acentuação (a justificação é invariante de saída, não opcional).

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
- Roda ao fim do pipeline, aula a aula, e grava `PipelineResult.gate` e a etapa `gate_report`
  (reprovação vira aviso, não falha); `python cli.py validate` continua servindo para rascunhos
- Medida por AULA quando o texto traz `# Aula i.j:` (`QualityGate._check_content_por_unidade`);
  texto sem esse cabeçalho é medido inteiro na unidade pedida (`unidade="modulo"` multiplica a
  régua da aula por 4 a 6)
- Extensão, H2, H3 por H2, teto de apoios visuais e faixa de parágrafo: números de `tetos.D` em
  `config/lexicos.json`
- Um exercício por aula (erro se faltar); hierarquia de títulos sem pulos
- Clichês proibidos: união de `lexicos.json`, `quality_rules.yaml` e fallback do módulo
- Verbos de Bloom só quando existe seção de objetivos; andragogia só avisa
- Emojis proibidos; teto de marcadores `[FALTA EVIDÊNCIA]`; percentual sem fonte avisa

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
- config/quality_rules.yaml — regras de qualidade (inclui a camada `visual_density`, cobrada em runtime)
- docs/DOUTRINA_VISUAL_CURSOS.md — doutrina de peso visual: tetos, os seis tipos de bloco e os quatro lugares que mudam juntos
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

## Padrão editorial obrigatório

Antes de produzir qualquer texto de leitura humana neste repositório (documentação, cursos, páginas, relatórios, descrições de PR, mensagens longas de commit), leia e aplique [`DIRETRIZ_EDITORIAL.md`](DIRETRIZ_EDITORIAL.md) na raiz (versão 4, 11/08/2026) e consulte o anexo prático [`GUIA_ESCRITA_HUMANIZADA.md`](GUIA_ESCRITA_HUMANIZADA.md), com exemplos antes e depois, heurísticas mensuráveis e fontes. Esta é a fonte única do padrão editorial do repositório: os prompts do pipeline (`src/templates/prompts/`) e o resumo da seção "Padrão Editorial" acima se subordinam a ela, e a duplicação de camadas editoriais divergentes foi o que degradou a qualidade entre julho e agosto de 2026 (ver `wiki/decisions/diretriz-editorial-v3-narrativa-sem-cota.md`).

Antes de qualquer regra de evitação vem o piso de substância (diretriz §2.1), porque os gates automáticos deste repo medem forma e nenhum deles mede argumento: texto raso e uniforme passa em todos. Toda peça precisa ter tese identificável, evidência ligada à tese, ganho de informação, critério de decisão explícito onde houver alternativas, arco de leitura e consequência executável para o leitor. Aprovação no gate não é aprovação editorial, e em conflito entre proibição e piso de substância o piso vence.

Antes da primeira frase vem a prova (diretriz §2.2). Levante o material de evidência, e ele define o tamanho da peça: o número de blocos que afirmam resultado é menor ou igual ao número de provas datadas disponíveis hoje. Faltando prova, tente as quatro saídas nesta ordem (pesquisar a origem, reduzir a afirmação ao que se sabe, restringir o uso, segurar a publicação) antes de usar marcador. `[FALTA EVIDÊNCIA: ...]` é lacuna que pesquisa resolve; `[PREENCHER-HUMANO: ...]` é o que só o autor humano tem. Teto de cinco marcadores abertos por documento, agora verificado pelo `content_checker.py`.

Promessa e tensão são escritas antes do esqueleto (§3.1), o esqueleto segue a ordem do gênero (§3.2), o pedido é um só por peça com as quatro peças da fórmula (§3.6), e toda porcentagem dispara quatro conferências na mesma frase: origem, data, método e denominador (§13).

O essencial, em uma passada: escrita de especialista sênior em português do Brasil com acentuação completa e tipografia brasileira (sem title case, numerais à brasileira); conclusão antes da sustentação e cada parágrafo acrescentando uma ideia nova; storytelling obrigatório em conteúdo longo (abertura em situação, tensão antes da solução, caso condutor, promessa cumprida, fechamento com callback, mostrar em vez de qualificar); ritmo nascido do sentido, com o teste do bloco de dez frases servindo de diagnóstico depois de escrever e nunca de cota durante a escrita; proibido travessão como recurso estilístico; proibidas como padrão as construções que negam para afirmar ("não é X, é Y"), a regra de três mecânica, as conclusões-espelho e a atribuição vaga sem fonte nomeada; conectivos cortados por subtração, sem clichês nem vícios de português de LLM (gerundismo, "endereçar", "suportar", "eventualmente" como eventually); tabela, matriz de decisão e checklist usados sempre que houver comparação, escolha ou passo verificável, e prosa sempre que houver raciocínio encadeado; dado sem fonte e data não entra, e o que só o autor humano sabe vira marcador `[PREENCHER-HUMANO]`, nunca invenção; em superfícies HTML ou PDF, parágrafos com alinhamento justificado (`text-align: justify`); revisão final em três passadas (substância, estrutura, linguagem) com leitura em voz alta.

Sub-agentes que geram copy longa recebem o bloco de `C:/Sandyboxclaude/scripts/prompts/COPY_PROMPT_PREFIX.md` carimbado no prompt. Os documentos completos prevalecem sobre este resumo, e as convenções específicas deste repositório prevalecem sobre convenções genéricas, exceto quando comprometerem segurança ou corretude.
