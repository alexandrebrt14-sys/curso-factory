# Wave 4 — Discovery Standards para IA 2026

> Pesquisa profunda · 17-05-2026 · Alexandre Caramaschi / curso-factory
> 5 chamadas Perplexity (sonar-pro/sonar-deep-research) + 13 validações WebFetch
> Custo total Perplexity ~ $0,07 (Q1 e Q5 retry com sonar-pro depois de Q1/Q5 deep esgotarem reasoning_tokens)

---

## 1. Sumário executivo

- **llms.txt** atingiu adoção mensurável em 2026 (~10% de 300k domínios na SE Ranking) mas **não tem efeito de citação** em LLMs (ALLMO 94.614 URLs citadas: 1 com llms.txt = 0,001%). Limy mediu 500M eventos de bot e só 408 foram para `/llms.txt`. Anthropic/OpenAI/Google/Perplexity **não anunciaram suporte oficial** ao formato.
- **IETF AIPREF working group** é o caminho oficial: `draft-ietf-aipref-vocab-06` (28-abr-2026, Paul Keller + Martin Thomson) ainda sem consenso; `draft-ietf-aipref-attach-04` **expirou** em out/2025. Meta de submissão ao IESG: **31-ago-2026**.
- **Schema.org 30.0** (19-mar-2026) **não introduziu** `Agent`, `AIPolicy`, `GenerativeAI`, `AIContent` nem `AIServiceProvider`. A propriedade `agent` existe há anos (sub de `Action`), mas não é um tipo.
- **MCP (Model Context Protocol)**: registry oficial em preview desde set/2025 (Linux Foundation **Agentic AI Foundation**), >10.000 servers públicos (LF 2025), 7 servers reference Anthropic, marketplace Manifold com 7.700 servers (mai/2026).
- **AI crawlers canônicos 2026**: 200+ user-agents catalogados em ai-robots-txt e Known Agents. Distinção crítica: **training crawlers** (GPTBot, ClaudeBot, Bytespider, Google-Extended) vs **user-fetchers** (ChatGPT-User, Claude-User, Perplexity-User — geralmente **ignoram robots.txt**).

---

## 2. Tabela canônica AI crawlers 2026

Fontes: ai-robots-txt/robots.json (~200 entradas), Known Agents, docs oficiais de cada operadora, Q5 sonar-pro.

| User-agent (robots token) | Operadora | Classe | Respeita robots.txt | Flag opt-out canônica | Notas |
|---|---|---|---|---|---|
| **GPTBot** | OpenAI | Training | Sim | `User-agent: GPTBot` | Crawler principal para treinar GPT-4.x/5 |
| **ChatGPT-User** | OpenAI | User-fetcher | Parcial (on demand) | `User-agent: ChatGPT-User` | Disparado quando usuário pede para abrir URL |
| **OAI-SearchBot** | OpenAI | Search index | Sim | `User-agent: OAI-SearchBot` | Indexa para SearchGPT/Browse |
| **ChatGPT Agent** | OpenAI | Agent (browser automation) | Variável | `User-agent: ChatGPT Agent` | Novo em 2026, automação tipo Operator |
| **ClaudeBot** | Anthropic | Training | Sim | `User-agent: ClaudeBot` | Consolidação 2024 do antigo `anthropic-ai` |
| **Claude-User** | Anthropic | User-fetcher | Parcial | `User-agent: Claude-User` | Disparado por usuário Claude |
| **Claude-SearchBot** | Anthropic | Search index | Sim | `User-agent: Claude-SearchBot` | Indexa para AI search Claude |
| **anthropic-ai** | Anthropic | **DEPRECADO** | — | — | Legado; bloquear ainda por compatibilidade |
| **Claude-Web** | Anthropic | **DEPRECADO** | — | — | Legado |
| **Google-Extended** | Google | Training opt-out | Token de controle | `User-agent: Google-Extended` | NÃO é crawler — token de policy. Bloqueia uso para Gemini/Vertex AI training |
| **Google-CloudVertexBot** | Google | Vertex AI Search | Sim | `User-agent: Google-CloudVertexBot` | Crawla para Vertex AI Search dos clientes |
| **GoogleOther** / `-Image` / `-Video` | Google | Product fetcher | Sim | `User-agent: GoogleOther` | Vários produtos internos |
| **Google-NotebookLM** | Google | Research assistant | Variável | `User-agent: Google-NotebookLM` | Coleta para NotebookLM |
| **GoogleAgent-Mariner** | Google | Browser agent | Variável | `User-agent: GoogleAgent-Mariner` | Agente browser experimental |
| **PerplexityBot** | Perplexity | Search index | Sim | `User-agent: PerplexityBot` | IP list: `perplexity.com/perplexitybot.json` |
| **Perplexity-User** | Perplexity | User-fetcher | **NÃO** (oficial) | `User-agent: Perplexity-User` | Doc oficial declara que **ignora robots.txt** por ser user-action |
| **Bytespider** | ByteDance | Training | Sim | `User-agent: Bytespider` | Treina LLMs TikTok/Doubao |
| **TikTokSpider** | ByteDance | Training | Sim | `User-agent: TikTokSpider` | — |
| **Amazonbot** | Amazon | Search + Alexa + Rufus | Sim | `User-agent: Amazonbot` | Rufus (LLM Amazon) usa este crawler |
| **AmazonBuyForMe** | Amazon | AI shopping agent | — | `User-agent: AmazonBuyForMe` | Novo 2026 |
| **bedrockbot** | Amazon | Bedrock customer crawl | Sim | `User-agent: bedrockbot` | Crawl para customer-built RAG no Bedrock |
| **amazon-kendra** | Amazon | Enterprise search | Sim | `User-agent: amazon-kendra` | NL search |
| **Applebot** | Apple | Search (Siri, Spotlight) | Sim | `User-agent: Applebot` | — |
| **Applebot-Extended** | Apple | Training opt-out | Token de controle | `User-agent: Applebot-Extended` | Bloqueia uso para Apple Intelligence |
| **meta-externalagent** | Meta | Training + AI features | Sim (declarado) | `User-agent: meta-externalagent` | Crawler oficial Meta AI |
| **meta-externalfetcher** | Meta | User-fetcher | Parcial | `User-agent: meta-externalfetcher` | Status documentação fraca |
| **meta-webindexer** | Meta | Meta AI search | Sim | `User-agent: meta-webindexer` | — |
| **FacebookBot** | Meta | LLM training | Sim | `User-agent: FacebookBot` | — |
| **bingbot** | Microsoft | Search + Copilot | Sim | `User-agent: bingbot` | Copilot reaproveita índice Bing — sem UA separado |
| **MistralAI-User** | Mistral | User-fetcher | Sim | `User-agent: MistralAI-User` | Le Chat user actions |
| **DuckAssistBot** | DuckDuckGo | AI assistant | Sim | `User-agent: DuckAssistBot` | — |
| **CCBot** | Common Crawl | Open dataset | Sim | `User-agent: CCBot` | Dataset que treina ~todos os LLMs |
| **cohere-ai** | Cohere | User responses | Sim | `User-agent: cohere-ai` | — |
| **cohere-training-data-crawler** | Cohere | Training | Sim | `User-agent: cohere-training-data-crawler` | — |
| **PetalBot** | Huawei | Search + AI | Sim | `User-agent: PetalBot` | PanGu LLM |
| **PanguBot** | Huawei | Training | Sim | `User-agent: PanguBot` | — |
| **YandexAdditional** | Yandex | YandexGPT training | Sim | `User-agent: YandexAdditional` | — |
| **DeepSeekBot** | DeepSeek | Training | Sim | `User-agent: DeepSeekBot` | — |
| **Diffbot** | Diffbot | Structured data ML | Sim | `User-agent: Diffbot` | — |
| **TavilyBot / ExaBot / FirecrawlAgent** | Tavily/Exa/Firecrawl | Data provider para outras IAs | Variável | tokens próprios | Camada B2B de scrap-as-a-service |
| **SemrushBot-OCOB / -SWA** | Semrush | AI features (ContentShake, Writing Assistant) | Sim | tokens específicos | — |
| **Kagi-fetcher** | Kagi | AI assistant | Sim | `User-agent: Kagi-fetcher` | — |
| **Andibot / PhindBot / YouBot / iAskBot** | múltiplos | AI search | Sim (em geral) | tokens próprios | Long-tail de AI search engines |

> Lista completa machine-readable: `https://github.com/ai-robots-txt/ai.robots.txt/blob/main/robots.json` (200+ bots).

**Padrão emergente 2026**: distinção entre *training crawlers* (respeitam robots.txt; permitem opt-out via UA específico) e *user-fetchers* (parcial ou totalmente fora do robots.txt porque executam ação solicitada pelo usuário — Perplexity-User é o caso mais documentado disso).

---

## 3. Status real do llms.txt em 2026

### 3.1 Adoção mensurada

| Estudo | Amostra | Adoção llms.txt | Citação na resposta de LLM? |
|---|---|---|---|
| SE Ranking (2026) | 300.000 domínios | **10,13%** | Não mediu |
| Trakkr Research (2026) | 37.894 domínios AI-cited | 13,3% geral / **6,0% nos top 50** | Sem correlação positiva |
| ALLMO (Signals 2026) | 94.614 URLs citadas em 11.867 respostas IA | **1 URL** (0,001%) | Não — só 1 dos top 50 domínios usa (Target.com) |
| Rankability (2026) | Top 100 (n=30 amostra) | **0,0%** | — |
| BeRecommended (2026) | Fortune 500 | 7,4% | AI crawlers leram em 0,1% das requests |
| Limy AI (2026) | 500M eventos de bot AI | — | Só **408 requests** para llms.txt em 500M |

### 3.2 Posicionamento oficial dos LLMs

- **Anthropic**: sem documentação que cite llms.txt; controle continua sendo robots.txt.
- **OpenAI**: sem doc oficial; pipeline de retrieval não consulta llms.txt (Signals 2026, Limy).
- **Google**: explicitamente listado por LBN Tech Solutions (2026) como "sem adoção pelas grandes IAs incluindo Google".
- **Perplexity**: documentação foca em `PerplexityBot` e `Perplexity-User` (robots.txt + IP lists JSON). Não menciona llms.txt.

**Conclusão consensual de 6 estudos 2026**: llms.txt **não move o ponteiro** de citações em LLM, mas tem nicho legítimo para *developer docs* (FastHTML, Cloudflare, Vercel AI SDK, Hugging Face — todos publicam `llms-full.txt` para IDE agents).

### 3.3 Alternativas 2026

- **ai.txt** — proposta, sem vendor buy-in, sem adoção mensurável.
- **/.well-known/ai-policy** + **ai-policy.json** — citado em discussões W3C, sem spec publicada nem crawler study.
- **robots.txt + UA tokens** — única alternativa **com tração real** (todos os vendors documentam UA).
- **IETF AIPREF** (`draft-ietf-aipref-vocab-06`) — caminho oficial em andamento; entrega prevista 31-ago-2026.

---

## 4. Top 5 standards emergentes 2026

| # | Standard | Tier maturidade | Operador | Status verificado |
|---|---|---|---|---|
| 1 | **MCP (Model Context Protocol)** | **Adotado** | Linux Foundation Agentic AI Foundation (Anthropic, Block, OpenAI) | Registry preview ([registry.modelcontextprotocol.io](https://registry.modelcontextprotocol.io)) desde set/2025. >10.000 servers públicos. Suporte nativo Claude, ChatGPT, VS Code, Cursor, Copilot, Gemini |
| 2 | **C2PA (Content Authenticity Initiative)** | **Adotado / produção** | C2PA Steering Committee (Adobe, Amazon, BBC, Google, Meta, Microsoft, OpenAI, Sony, Truepic, Publicis) | Spec 2.3. Adoção em câmeras Leica/Sony, Photoshop, ChatGPT image gen |
| 3 | **IETF AIPREF (`draft-ietf-aipref-vocab-06`)** | **[DRAFT]** Active I-D (sem consenso WG) | IETF Web and Internet Transport Area | Última revisão 28-abr-2026 (Paul Keller, Martin Thomson). Meta IESG: 31-ago-2026 |
| 4 | **IETF AIPREF (`draft-ietf-aipref-attach`)** | **[DRAFT]** EXPIRADO em out/2025 | Gary Illyes (Google), Martin Thomson | Atualiza RFC 9309 (Robots) para incluir preferências de uso. Aguarda nova revisão |
| 5 | **llms.txt** | **De facto** (sem vendor backing) | Comunidade (Jeremy Howard, Answer.AI) | 10% adoção geral; 0% impacto em citações; útil só para dev docs |

**Outros drafts IETF citados (não-AIPREF, individuais)**:
- `draft-cui-ai-agent-discovery-invocation-01` (12-fev-2026, Yong Cui et al.)
- `draft-aiendpoint-ai-discovery-00` (23-mar-2026, 최영재)
- `draft-han-ai-manifest-01` (15-mai-2026, Wonpyo Han)

Nenhum desses 3 é endossado pelo IETF — são drafts individuais que podem virar working items.

**Schema.org**: **versão 30.0 não adicionou tipos AI**. Único caminho hoje é usar `SoftwareApplication`, `Service`, `CreativeWork` + propriedade `agent` (que é da `Action`, não tipo standalone).

---

## 5. MCP servers production-ready para SEO/GEO

### 5.1 Reference servers (Anthropic / modelcontextprotocol org)
7 servers no [`modelcontextprotocol/servers`](https://github.com/modelcontextprotocol/servers): Everything, Fetch, Filesystem, Git, Memory, Sequential Thinking, Time.

### 5.2 Top 3 production-ready para SEO/GEO (verificados em Q4)

| # | MCP Server | Operador | Função SEO/GEO |
|---|---|---|---|
| 1 | **SE Ranking MCP** | SE Ranking | Keyword research automation, position tracking, competitor analysis. Doc: https://chrisraulf.com/se-ranking-mcp-keyword-research-automation/ |
| 2 | **Firecrawl MCP** | Firecrawl | Scrape + crawl + extract structured data; integra com schema validation. Usado em pipelines de GEO content publishing |
| 3 | **AWS Location MCP** | AWS Labs | Geospatial queries, geocoding, places API — para "GEO" no sentido geográfico, mas também usado por agentes que precisam disambiguar localização em queries |

**Plataformas que catalogam MCP servers em 2026**:
- **Registry oficial**: registry.modelcontextprotocol.io (preview, mantido por Anthropic/PulseMCP/GitHub/Stacklok)
- **mcp.so** — diretório aberto
- **MCP Market** (mcpmarket.com)
- **Manifold** — marketplace com 7.700 servers e foco em segurança (anunciado 12-mai-2026)
- **Smithery, Glama, Docker MCP Hub** — registries de terceiros

**Modelo de segurança 2026**: OAuth 2.1 + signed manifests + sandboxing + host-level consent. Publicação de servers exige verificação de namespace (GitHub OAuth ou DNS/HTTP TXT record).

---

## 6. Recomendação prática para curso-factory

### O que publicar **HOJE** (ROI comprovado)

1. **`/robots.txt`** — fonte da verdade. Bloquear/permitir explicitamente cada UA da tabela § 2.
   ```txt
   # Training crawlers — decidir conforme política
   User-agent: GPTBot
   Allow: /
   User-agent: ClaudeBot
   Allow: /
   User-agent: Google-Extended
   Allow: /
   User-agent: Applebot-Extended
   Allow: /
   User-agent: Bytespider
   Disallow: /

   # User-fetchers — recomendação: SEMPRE permitir
   User-agent: ChatGPT-User
   Allow: /
   User-agent: Claude-User
   Allow: /
   User-agent: Perplexity-User
   Allow: /

   Sitemap: https://curso.brasilgeo.ai/sitemap.xml
   ```

2. **JSON-LD Schema.org** — `Course`, `CourseInstance`, `EducationalOccupationalProgram`, `Organization`, `Person` (instrutor Alexandre). Não inventar `AIPolicy`/`GenerativeAI` — usar `SoftwareApplication` para descrever ferramentas do curso.

3. **`llms-full.txt`** — somente porque o curso é dev-doc-heavy (vibe coding, Claude Code, MCP). É **ZERO** efeito em citation, mas vira UX win para alunos que copiam para o próprio Claude/ChatGPT. Inspirar-se em Cloudflare (49KB) e Vercel AI SDK (293KB).

4. **`/sitemap.xml` + `sitemap-index.xml`** — protocolo canônico que os AI crawlers efetivamente leem (Limy 500M events confirmou).

### O que publicar **EM 30 DIAS** (alta probabilidade de virar canônico)

5. **`/.well-known/ai-preferences`** (placeholder) — preparar estrutura. Quando AIPREF (`draft-ietf-aipref-vocab-06`) for aprovado pelo IESG em ~ago/2026, o caminho `.well-known/ai-preferences` será o método canônico de attach.

6. **C2PA Content Credentials** em qualquer imagem/video gerado por IA — selo "made with AI" embarcado no arquivo. Adobe, Google, OpenAI já assinam por padrão.

7. **MCP server `curso-factory-mcp`** — expor catálogo do curso como MCP server (tools: `search_lesson`, `list_modules`, `get_certificate_path`). Publicar no registry.modelcontextprotocol.io. Vira surface para Claude/ChatGPT recomendarem aulas dentro do chat do aluno.

### O que **NÃO publicar** (sem ROI)

- **ai.txt** — sem buy-in de vendor, sem tração.
- **ai-policy.json em path custom** — esperar AIPREF resolver o path canônico.
- **`Agent`, `AIPolicy`, `GenerativeAI` no @graph** — tipos NÃO existem no Schema.org 30.0; validators vão alertar.

---

## 7. Anexos

- Q1 (llms.txt adoption): [wave-4-extracted-q1.md](./wave-4-extracted-q1.md)
- Q2 (IETF/W3C drafts): [wave-4-extracted-q2.md](./wave-4-extracted-q2.md)
- Q3 (Schema.org 2025-2026): [wave-4-extracted-q3.md](./wave-4-extracted-q3.md)
- Q4 (MCP ecosystem): [wave-4-extracted-q4.md](./wave-4-extracted-q4.md)
- Q5 (AI crawlers canônicos): [wave-4-extracted-q5.md](./wave-4-extracted-q5.md)
- Raw JSON Perplexity: `wave-4-raw-q[1-5].json`

### Fontes validadas via WebFetch

- llmstxt.org/ (spec original) — comunidade, sem endorsement vendor
- schema.org/docs/releases.html — confirmou v30.0 (19-mar-2026) e v29.4 (08-dez-2025) sem tipos AI
- c2pa.org — confirmou spec 2.3, Steering Committee (Adobe, Amazon, BBC, Google, Meta, Microsoft, OpenAI, Sony, Truepic, Publicis)
- modelcontextprotocol.io — confirmou suporte Claude + ChatGPT + VS Code + Cursor + Gemini
- datatracker.ietf.org/wg/aipref/about/ — confirmou WG Active, metas ago/2026
- datatracker.ietf.org/doc/draft-ietf-aipref-vocab/ — v06, 28-abr-2026, sem consenso WG
- datatracker.ietf.org/doc/draft-ietf-aipref-attach/ — v04, expirado out/2025
- github.com/ai-robots-txt/ai.robots.txt + raw robots.json — 200+ bots catalogados
- github.com/modelcontextprotocol/servers — 7 reference servers
- github.com/modelcontextprotocol/registry — 6.8k stars, governance Anthropic/PulseMCP/GitHub/Stacklok
- knownagents.com/agents (ex-darkvisitors) — catálogo público de AI crawlers
- directory.llmstxt.cloud — 1.503+ adopters listados
- developers.google.com/.../google-common-crawlers — confirmou Google-Extended, Google-CloudVertexBot, GoogleOther
- docs.perplexity.ai/guides/bots — confirmou que Perplexity-User **ignora** robots.txt (oficial)
- anthropic.com/robots.txt — `User-Agent: *` `Allow: /` (sem restrição)
