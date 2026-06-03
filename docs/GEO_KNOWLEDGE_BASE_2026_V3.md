# GEO Knowledge Base 2026 V3 — curso-factory

> **Versão:** 3.0 · 2026-06-03 · Owner: Brasil GEO (Alexandre Caramaschi)
>
> **O que é:** o incremento de conhecimento previsto pela V2 (§12), consolidando o que a literatura e o mercado produziram **entre 20-mai e 03-jun de 2026** — material que ainda não estava na V2 (escrita antes da aceitação dos papers no ICLR e antes da edição de maio do estudo Muck Rack). **Não substitui** a V1/V2 nem os demais docs canônicos; adiciona frameworks, métricas e papers novos, e aponta para os docs operacionais (`GEO_REDACAO_CHECKLIST_2026.md`, `GEO_EARNED_MEDIA_2026.md`).
>
> **Fontes confrontadas:** AutoGEO (CMU, ICLR 2026, arXiv:2510.11438), AgenticGEO (arXiv:2603.20213), Muck Rack/Generative Pulse "What is AI Reading?" (mai/2026), Selection×Absorption (arXiv:2604.25707), distribuição de amostragem (arXiv:2604.07585), `fseixas/super-geo-agent-readiness`, gist Karpathy LLM Wiki, e os 13 conceitos novos (51-63) de `GEO_50_CONCEITOS_CANONICAL.md` na linha de pesquisa Brasil GEO.

---

## Índice

- §0 — O que mudou desde a V2 (sumário)
- §1 — AutoGEO: GEO de crença para medição (GEO Score / GEU Score)
- §2 — Earned media é a camada dominante (Muck Rack 84%)
- §3 — Selection Rate × Absorption Rate (a citação tem duas dimensões)
- §4 — super-geo: severidade graduada + 4 tiers de agent-readiness
- §5 — Karpathy LLM Wiki: regime de manutenção (ingest/query/lint)
- §6 — Multi-LLM Sampling Wave (amostragem, não snapshot)
- §7 — Os 13 conceitos novos (51-63)
- §8 — Papers acadêmicos de Q2 2026
- §9 — Descobertas de mercado pós Google I/O 2026
- §10 — Implicações diretas para o curso-factory

---

## 0. O que mudou desde a V2 — sumário

| Mudança | V2 (≤20-mai) | V3 (≥31-mai) |
|---|---|---|
| **GEO como disciplina** | rubrica *a priori* de 50 conceitos | + loop empírico *a posteriori* (AutoGEO) que extrai regras do próprio engine-alvo |
| **Métrica de citação** | "citation rate" único | par **GEO Score / GEU Score** (AutoGEO) e par **Selection Rate / Absorption Rate** (SIGIR 2026) |
| **Earned media** | apêndice de "earned media plan" no Operating System | evidência dura: **84% das citações de IA vêm de earned media** (Muck Rack mai/2026) + framework EMGE + KPIs K-EM |
| **Rubrica de redação** | Princeton: 3 lifts (Cite +115% / Stats +41% / Quote +28%) | **13 técnicas** com lift individual (Aggarwal completo) em `GEO_REDACAO_CHECKLIST_2026.md`, agora **validadas por contagem** |
| **Conceitos** | 50 | **63** (+ Information Gain, Compression Fidelity, Citation Persistence, Multi-Source Consensus, Query Fan-Out, Schema Authority Stack, B2A, Earned Media Primacy…) |
| **Amostragem de medição** | snapshot pontual | **5+ amostras por prompt × modelo × dia** (distribuição, não número) |

---

## 1. AutoGEO — o GEO sai da crença e vira medição

**Paper:** Wu, Zhong, Kim, Xiong (CMU), aceito no **ICLR 2026** (arXiv:2510.11438). Código aberto: `github.com/cxcscmu/AutoGEO`.

A V2 tratava os conceitos de GEO como uma rubrica *a priori* (derivada de papers). O AutoGEO ensina a **extrair as regras de preferência do próprio engine-alvo, a posteriori**, comparando documentos vencedores e perdedores numa tarefa de RAG.

### 1.1 As duas métricas canônicas (adotar no dashboard)

| Métrica | Mede | Componentes |
|---|---|---|
| **GEO Score** | *Visibilidade* na resposta do engine | posição do documento na resposta + contagem de tokens da fonte que aparecem + frequência de citação |
| **GEU Score** | *Utilidade* (não degradar a resposta) | qualidade da citação + cobertura de keypoints (KPR) + coerência (minimizar contradição/KPC) |

**Princípio-chave:** maximizar GEO **sem derrubar** GEU. Otimização que degrada a utilidade da resposta é insustentável — o engine eventualmente penaliza. É o antídoto formal contra o pseudo-GEO.

### 1.2 O loop de extração de regras (rodável sem GPU, no orchestrator de 5 LLMs)

Não precisamos do AutoGEO_Mini (treino em 2× A100, ~52h). Precisamos do loop via API, em 5 estágios:

1. **Seleção de pares** — escolher dois documentos com maior diferença de visibilidade (`argmax |Vis(di)−Vis(dj)|`).
2. **Explainer** — perguntar ao engine-alvo *por que* preferiu o vencedor.
3. **Extractor** — sobre a explicação, extrair um array JSON de **regras determinísticas e reutilizáveis**.
4. **Merger** — chunking hierárquico das regras → 10-20 regras consolidadas.
5. **Filter** — `merged_rules.json` (chave `filtered_rules`).

Exemplos de regras extraídas pelo próprio repo: *"o documento deve responder diretamente à pergunta central da query"*, *"usar headings e listas claras para fácil parsing"*, *"fornecer detalhes específicos e acionáveis, não afirmações genéricas"*. **Overlap de regras entre engines:** Gemini-Claude 84,2%, Gemini-GPT 79% → existe um núcleo de ~15 regras comuns + 2-3 por engine ("Single Idea" no Claude, "Neutral Tone" no Gemini, "Informational Purpose" no GPT). **Lift médio: +50,99% no GEO Score.** A evolução **AgenticGEO** (arXiv:2603.20213) faz reescrita multi-turno (+46,4%).

> **Nota importante:** regras extraídas são **por-engine e por-domínio**. Não tratar uma regra do Gemini como universal. Isto **refina**, não substitui, os 63 conceitos e a rubrica de redação.

### 1.3 Aplicação no curso-factory

As regras genéricas que o AutoGEO extrai já estão, em larga medida, codificadas na rubrica `GEO_REDACAO_CHECKLIST_2026.md` (responder direto = answer capsule; headings/listas = formatação rica; detalhes acionáveis = exercícios + dados). O ganho marginal de rodar o loop é **calibrar por engine** os módulos estratégicos de um curso sobre GEO/IA — material avançado para o próprio curso ensinar.

---

## 2. Earned media é a camada dominante do GEO

**Fonte:** Muck Rack / Generative Pulse — *"What is AI Reading?"* (edição mai/2026, 25M+ links, 17 setores). Reforço: Chen et al. (arXiv:2509.08919).

A esmagadora maioria do que os modelos citam vem de **mídia conquistada** (jornalismo, pesquisa, governo, comunidades), não de conteúdo próprio nem de mídia paga.

| Tipo de fonte | Share das citações de IA |
|---|---|
| **Earned media** (jornalismo, academia, governo, comunidades) | **84%** (faixa 82-89%) |
| **Jornalismo profissional** (subconjunto) | **27%** (estável 25-27%) |
| Conteúdo próprio / blog corporativo (owned) | minoria do restante |
| **Mídia paga / advertorial** (paid) | **0,3%** — praticamente morta para GEO |

Cada modelo lê diferente: **ChatGPT** cita Wikipedia/veículos grandes (96% das respostas), **Gemini** cita Reddit/fóruns (82%), **Claude** prefere trade/nicho e sustenta cobertura por ~10 semanas (55%, o mais seletivo). **Gap acionável:** os jornalistas mais *pitchados* por PR e os mais *citados* pela IA têm sobreposição de apenas **~2%** — quem mapeia quem a IA realmente cita compra visibilidade barata.

O detalhamento (framework EMGE de 5 estágios, técnicas de colocação, KPIs K-EM-001 a 006, playbook de 90 dias) está em **`GEO_EARNED_MEDIA_2026.md`**. Para o pipeline educacional, a implicação é dupla: (a) cursos sobre GEO devem ensinar earned media como vetor dominante, não como apêndice; (b) o portal do cliente ganha mais citação investindo em pauta de imprensa especializada do que em mídia paga.

---

## 3. Selection Rate × Absorption Rate — a citação tem duas dimensões

**Fonte:** Zhang, He, Yao (arXiv:2604.25707, SIGIR 2026).

O KPI antigo "citation rate" trata como equivalentes duas coisas distintas:

- **Selection Rate** — % de prompts em que a página é **citada** (frequência).
- **Absorption Rate** — **profundidade** da citação (nº de tokens, duração da menção, peso na resposta).

ChatGPT cita **poucas fontes com peso altíssimo** (alta absorção); Perplexity cita **muitas fontes com peso médio-baixo**. Uma página pode ter alta selection e baixa absorption — sintoma de que é citada de passagem, não usada como espinha dorsal da resposta. **Correção:** reescrever essas páginas com bullets explícitos, comparações de duas colunas e um número-pivô destacado (exatamente os itens 9 e 10 da rubrica de redação). No tracking, sempre registrar o **par** `(selection_rate, absorption_rate)`, nunca um número só.

---

## 4. super-geo — severidade graduada + 4 tiers de agent-readiness

**Fonte:** `fseixas/super-geo-agent-readiness` (Claude Skill de auditoria GEO).

### 4.1 Severidade graduada (camada de priorização que os 63 conceitos não tinham)

- **Blocker** — crawler de IA não alcança o conteúdo (SPA sem SSR, robots bloqueando por engano, sem HTTPS).
- **High** — sinal maior ausente que impede citação (autor sem credencial, sem fonte primária, schema `Article` sem `author`/`dateModified`).
- **Medium** — lacuna de otimização (FAQ schema ausente, comprehensiveness incompleta).
- **Low** — polimento (linguagem promocional, slug subótimo).

**Regra de escopo crítica:** a severidade **muda com o alvo**. `llms.txt` é **Low** para auditoria Google-only (Google declarou no I/O 2026 que não é sinal de citação) mas **High** para os demais engines. Sempre perguntar primeiro: *"Google AI Overviews/AI Mode, ou todos os engines?"*

### 4.2 Escada de agent-readiness em 4 tiers

- **Tier 1 (todo site):** robots.txt com política de IA, sitemap, llms.txt, JSON-LD, HTTPS+HSTS.
- **Tier 2 (publishers):** markdown content negotiation (`Accept: text/markdown`), `/index.md` fallback, HTTP `Link` headers expondo sitemap/llms.txt.
- **Tier 3 (produtos com APIs/tools):** MCP Server Card em `/.well-known/mcp/server-card.json`, OpenAPI spec, API Catalog (RFC 9727).
- **Tier 4 (identidade/acesso/comércio):** OAuth metadata (RFC 8414/9728), Web Bot Auth, x402/ACP/UCP para pagamento agêntico.

> **Não fabricar pseudo-readiness:** criar um `.well-known` vazio de Tier 4 quando não há checkout nem API protegida é anti-padrão. Implementar só o que o modelo de negócio do portal exige. Um portal de cursos vive em Tier 1-2, com Tier 3 (MCP) como diferencial.

### 4.3 Modelo de arbitragem em 3 camadas (por que SEO clássico ainda importa)

Um LLM produz a resposta por (1) **conhecimento latente** do treino, (2) **retrieval ativo** (RAG/browsing) e (3) **arbitragem final** da fonte citada. SEO clássico continua sendo a fundação que alimenta as camadas 2 e 3 — por isso **GEO não substitui SEO**, complementa.

### 4.4 Fatos por-engine acionáveis

- **ChatGPT** — ~86% do tráfego de referral de IA; usa índice **Bing** (registrar no Bing Webmaster Tools é alavanca direta); ~90% das citações vêm de URLs que rankeiam 21+ no Google.
- **Perplexity** — 82% de overlap com a 1ª página do Google; cita **verbatim** → escrever Q&A direto.
- **Google AI Overviews** — domínios mais citados: Quora #1, Reddit #2; FAQ schema é high-leverage.
- **Claude** — cauteloso com baixa autoridade; valoriza markdown negotiation + llms.txt; janela de citação ~10 semanas.
- **Grok** — DeepSearch combina web + X.

---

## 5. Karpathy LLM Wiki — regime de manutenção do llms.txt

**Fonte:** gist de Andrej Karpathy sobre "LLM Wiki" — base de conhecimento mantida por LLM que **compõe ao longo do tempo**, com três operações: **ingest, query, lint**.

O curso-factory já tem `docs/karpathy-llm-wiki-methodology.md` e a skill `wiki`. O que a V3 acrescenta é o **lint como gate de processo**:

- **Ingest** — ao publicar um curso/módulo, adicionar o slug ao `llms.txt` do portal.
- **Lint (gap de processo)** — verificação periódica: links 200/404, claims obsoletas (datas/números), páginas órfãs (no site mas não no llms.txt e vice-versa), contradições com docs canônicos. Referência de implementação: `scripts/geo/lint_llms_txt.mjs` do `landing-page-geo` (staleness de datas, slugs com acento, paridade sitemap↔llms.txt).
- **Log append-only** — `llms-changelog.md` com timestamp parseável (`## [2026-06-03] ingest | <título do curso>`), útil para a auditoria trimestral de Citation Accuracy.

**KPI:** cobertura de paridade cursos↔llms.txt (target 100%). No `landing-page-geo`, esse lint subiu a cobertura de 45→104 artigos ao expor os slugs ausentes.

---

## 6. Multi-LLM Sampling Wave (MLSW) — amostragem, não snapshot

**Fonte:** Schulte, Bleeker, Kaufmann (arXiv:2604.07585).

A citação de IA é **estocástica**. Medir uma vez é inútil. Protocolo canônico: **5+ amostras por prompt × modelo × dia**, com perfis determinístico (T=0) e estocástico (T=0,7).

- **Tiers de prioridade:** P0 (20-50 amostras), P1 (10), P2 (5).
- **Citation Drift (Profound):** 40-60% dos domínios citados mudam por mês (AIO 59,3%; ChatGPT 54,1%; Perplexity 40,5%) → medição contínua.
- **Custo para um portal:** 50 prompts P0 × 5 LLMs × 10 amostras = 2.500 chamadas/onda × 4/mês ≈ US$40-80/mês.

Para o curso-factory: medir a citação por curso publicado, com um pequeno portfólio de prompts representativos do tema do curso, não um snapshot único pós-publicação.

---

## 7. Os 13 conceitos novos (51-63)

Resumo; definição completa, evidência e target em `GEO_50_CONCEITOS_CANONICAL.md`.

| # | Conceito | Target |
|---|---|---|
| 51 | **Information Gain** — % de conteúdo original (dados próprios, frameworks, benchmarks) | ≥30% por longform |
| 52 | **Answer Capsule** — parágrafo auto-contido 120-150 caracteres após heading-pergunta | ≥80% dos informacionais |
| 53 | **Compression Fidelity** — sobrevive a "sintetize em 25 palavras" sem perder tese/marca | ≥80% de retenção |
| 54 | **Citation Persistence** — estabilidade da citação (variância D+0/D+14/D+30) | <20% drift em pillars |
| 55 | **Multi-Source Consensus** — claim corroborado em ≥3 fontes externas independentes | ≥3 por claim de pillar |
| 56 | **Retrieval Fitness** — chunkable e self-contained para RAG (chunk 512 tokens) | cosine intra-cluster >0,80 |
| 57 | **Source Eligibility** — sinais binários (HTTPS, autor, datas, editor, política editorial) | pré-requisito de tudo |
| 58 | **Entity Boundary Drift** — dispersão semântica de identidade entre fontes (`cos θ`) | `cos θ > 0,95` |
| 59 | **Consensus Engine Theory** — motores validam claim por corroboração múltipla | claim único sem respaldo é omitido |
| 60 | **Query Fan-Out Readiness** — cobertura dos 8 variant types do AI Mode | ≥6/8 por pillar (hub+spoke) |
| 61 | **Schema Authority Stack** — `@graph` aninhado Article→Person→Organization→Wikidata | 100% das templates |
| 62 | **B2A Readiness** — portal pronto para agentes (MCP/NLWeb + política B2A) | ≥1 endpoint MCP/NLWeb |
| 63 | **Earned Media Primacy** — peso de earned media no que a IA cita | earned ≥80%; paid leakage ≈0 |

Conceitos auxiliares pós-I/O: Attribution Gap, Competitive Shadow, Adversarial Exposure, Zero-Click Risk, Cold Start GEO.

---

## 8. Papers acadêmicos de Q2 2026

| Paper | Achado canônico |
|---|---|
| **AutoGEO** (ICLR 2026, arXiv:2510.11438) | extração de regras vencedor-vs-perdedor; **+50,99%** visibilidade |
| **AgenticGEO** (arXiv:2603.20213) | reescrita multi-turno; **+46,4%** |
| **Selection × Absorption** (arXiv:2604.25707) | citação tem duas dimensões; ChatGPT poucas/peso alto vs Perplexity muitas/peso baixo |
| **Distribuição de amostragem** (arXiv:2604.07585) | 5+ amostras por prompt × modelo × dia; snapshot único é inútil |
| **GhostCite** (arXiv:2602.06718) | **14-95%** de citações fabricadas em LLMs — risco de alucinação de fonte |
| **SIGIR AIO Survey** (arXiv:2604.27790) | **51,5%** das queries têm AI Overview ativa |
| **FeatGEO** (arXiv:2604.19113) | otimização em nível de feature estrutural supera copy lexical |
| **Tabular Chunking** | structure-aware chunking de tabelas: MRR 0,357→0,594 |
| **Chen et al.** (arXiv:2509.08919) | earned media pesa **2,3-3,1×** o owned |

> **GhostCite tem implicação editorial direta:** se os modelos fabricam citações em 14-95% dos casos, a Regra Anti-Invenção do redator (`draft.md`) deixa de ser higiene e vira **diferencial competitivo de GEO** — conteúdo com fonte real e verificável é o que sobrevive à arbitragem do engine.

---

## 9. Descobertas de mercado pós Google I/O 2026 (15-mai)

| Descoberta | Ação para o portal de cursos |
|---|---|
| AI Mode 1B+ MAU; AI Overviews 2,5B+ MAU | escalar medição de AIO (51,5% das queries) |
| **88% das citações do AI Mode NÃO estão no top-10 orgânico** (Moz, 40k queries) | páginas-satélite long-tail (500-800 palavras) por subtópico de curso |
| **63% das citações de LLM apontam para páginas com lista**; Top-N +71-86% | usar `ItemList` + converter prosa enumerada em lista numerada |
| LCP "Good" caiu para 2,0s (Google, 15-mai) | auditar Core Web Vitals do portal |
| GA4 canal nativo "AI Assistant" (13-mai) | validar + criar canal custom "AI Referral Expanded" |
| Perplexity Publisher Program (pool US$42,5M) | candidatar o portal (exige `datePublished`/`dateModified` visíveis) |
| FAQ rich results encerrados (7-mai) | manter `FAQPage` como trust signal para IA, mesmo sem rich result |

---

## 10. Implicações diretas para o curso-factory

1. **Rubrica de redação operacional** — `GEO_REDACAO_CHECKLIST_2026.md` substitui o "Princeton checklist genérico" por 13 técnicas com número-alvo, agora validadas por contagem no `content_checker.py` (Cite Sources ≥3, Stats ≥5, Quotes ≥1, answer capsule).
2. **Config por cliente** — bloco `geo_2026` no `client.yaml` liga/desliga o playbook e ajusta os mínimos.
3. **Tags GEO canônicas** — o classificador (`classify.md`) emite `geo-2026`, `citation-ready`, `aeo`, `aso`, `b2a`, `entity-drift`, `query-fan-out`.
4. **Conteúdo do próprio curso de GEO** — AutoGEO, GEO/GEU Score, earned media (84%), Selection×Absorption, super-geo tiers e os papers Q2 são material de aula de altíssimo valor; um curso "GEO/SEO 2026" deve cobri-los.
5. **Anti-invenção como GEO** — GhostCite torna a fonte verificável um diferencial, não só uma regra de higiene.
6. **Medição como pipeline** — adotar MLSW (5+ amostras) e o par Selection/Absorption ao avaliar a performance de um curso publicado, nunca snapshot único.

---

*Fim do documento. Próxima revisão: V4 prevista para setembro/2026 (cadência trimestral), ou quando sair edição nova do Muck Rack / novo batch de papers GEO.*
