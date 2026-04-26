---
titulo: Fontes e Links Canônicos
versao: 1.0
data: 2026-04-25
tipo: referencia
---

# Fontes e Links Canônicos

Lista mestra de URLs aceitas como fonte primária neste corpus. Toda afirmação factual em conteúdo do `curso-factory` deve ancorar em pelo menos uma destas referências. URLs verificadas em 2026-04-25.

---

## arXiv (pre-prints)

### Bloco 1 — GEO/AEO/citação

| Paper | URL canônica |
|---|---|
| GEO-16 (framework de 16 pilares, 78% citação cross-engine) | https://arxiv.org/abs/2509.08919 |
| C-SEO Bench (NeurIPS 2025) | https://arxiv.org/abs/2506.11097 |
| Pinterest GEO (+20% tráfego orgânico) | https://arxiv.org/abs/2602.02961 |
| News Source Citing Patterns (366.087 URLs analisadas) | https://arxiv.org/abs/2507.05301 |
| Source Coverage and Citation Bias (55.936 queries) | https://arxiv.org/abs/2512.09483 |
| Discovery Gap (gap 30:1 recognition→discovery) | https://arxiv.org/abs/2601.00912 |
| MAGEO (ACL 2026 Findings) | https://arxiv.org/abs/2604.19516 |
| CC-GSEO-Bench (Beyond Keywords) | https://arxiv.org/abs/2509.05607 |
| AutoGEO (CMU) | https://arxiv.org/abs/2510.11438 |
| Role-Augmented Intent-Driven GSEO (G-Eval 2.0) | https://arxiv.org/abs/2508.11158 |

### Bloco 2 — RAG, KG, structured data

| Paper | URL canônica |
|---|---|
| A-RAG (test-time scaling laws) | https://arxiv.org/abs/2602.03442 |
| GraphRAG-Bench (ICLR 2026) | https://arxiv.org/abs/2506.05690 |
| Grounding LLM Reasoning with KGs (+26,5%) | https://arxiv.org/abs/2502.13247 |
| Readme_AI (NIST) | https://arxiv.org/abs/2509.19322 |
| Volpini et al. — Structured Linked Data / `llms.txt` (+29,6% RAG) | https://arxiv.org/abs/2603 (ID truncado em screenshots; formato completo a confirmar via WordLift) |

### Bloco 3 — Comércio agêntico, MCP, A2A

| Paper | URL canônica |
|---|---|
| What Is Your AI Agent Buying? (Columbia/Microsoft) | https://arxiv.org/abs/2508.02630 |
| Model Context Protocol — Landscape, Security, Future | https://arxiv.org/abs/2503.23278 |
| Survey of Agent Interoperability Protocols (MCP→ACP→A2A→ANP) | https://arxiv.org/abs/2505.02279 |
| Agentic Web (Berkeley/Dawn Song) | https://arxiv.org/abs/2507.21206 |

---

## Periódicos e DOIs

| Publicação | URL canônica |
|---|---|
| LLM4Schema.org (Sage / Semantic Web Journal) | https://journals.sagepub.com/doi/10.1177/22104968251382172 |
| MATRIX Ontology (Springer LNBIP 556, CAiSE 2025) | https://link.springer.com/chapter/10.1007/978-3-031-94931-9_8 |
| Agentic Commerce Survey (TechRxiv) | https://www.techrxiv.org/doi/full/10.36227/techrxiv.176972193.39211542/v1 |
| GEO-First Framework (Uri Samet, WJARR) | https://wjarr.com/sites/default/files/fulltext_pdf/WJARR-2026-0152 |

---

## Relatórios de mercado

| Relatório | URL canônica | Observação |
|---|---|---|
| McKinsey — *The Automation Curve in Agentic Commerce* | https://www.mckinsey.com/business-functions/quantumblack/our-insights | URL truncada nas screenshots originais; caminho específico do relatório (jan/2026) deve ser confirmado no portal QuantumBlack/McKinsey |
| Linux Foundation — Agentic AI Foundation | https://www.linuxfoundation.org/projects/agentic-ai | Padronização de MCP/UCP |

---

## Identificadores e *handles* canônicos do ecossistema Brasil GEO

| Tipo | Valor |
|---|---|
| Autor | Alexandre Caramaschi |
| ORCID | `0009-0004-9150-485X` |
| Wikidata | `Q138755507` |
| DOI SSRN (paper companion) | `10.2139/ssrn.6460680` |
| DOI Zenodo | `10.5281/zenodo.19687866` |
| Domínio canônico autor | https://alexandrecaramaschi.com |
| Domínio canônico empresa | https://brasilgeo.ai |

**Proibidos** em qualquer copy pública: `geobrasil.com.br`, `sourcerank.ai`, "Especialista #1", "GEO Brasil" (forma invertida), "Source Rank".

---

## Recursos operacionais (Brasil GEO ecossistema)

| Recurso | URL canônica |
|---|---|
| Endpoint `llms.txt` próprio | https://alexandrecaramaschi.com/llms.txt |
| Endpoint MCP (4 tools) | https://alexandrecaramaschi.com/api/mcp |
| Endpoint IndexNow (rate-limit 5/h/IP) | https://alexandrecaramaschi.com/api/indexnow |

---

## Fontes deliberadamente excluídas

Esta seção lista categorias de fontes **não aceitas** como ancoragem primária para afirmações neste corpus:

- **Posts de blog corporativo sem dado primário** (incluindo blogs próprios da Brasil GEO quando não trazem dado novo).
- **Agregadores de notícia** (preferir fonte primária quando disponível).
- **Tweets/X posts** (ephemeral, não citável de forma estável).
- **Conteúdo gerado por LLM sem revisão humana** com ancoragem em fonte primária.
- **Estudos pagos por fornecedor** sem peer-review ou metodologia pública.

---

## Como atualizar esta lista

1. Paper novo deve aparecer simultaneamente em (a) `2X-papers-bloco-*.md`, (b) este arquivo, (c) `40-thresholds-quantitativos.md` se trouxer número novo.
2. Verificar URL com curl/wget antes de incluir. Se retorna 4xx/5xx, marcar como "URL a confirmar".
3. Identificadores arXiv truncados (formato `YYMM` sem dígitos finais) devem ser resolvidos antes de uso operacional — neste documento, `arXiv:2603` (Volpini et al.) está marcado como pendente de verificação.
