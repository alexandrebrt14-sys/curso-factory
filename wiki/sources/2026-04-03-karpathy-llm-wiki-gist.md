---
name: 2026-04-03-karpathy-llm-wiki-gist
type: source
source_type: gist
status: stable
created: 2026-05-26
updated: 2026-05-26
publication_date: 2026-04-03
author: Andrej Karpathy
url: https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f
related:
  - llm-wiki-karpathy
  - ADR-001-adopcao-llm-wiki
  - ADR-002-sync-automatico-courses-wiki
---

# Karpathy LLM Wiki Gist (3 abr 2026)

Fonte canônica da arquitetura da camada `wiki/` no `curso-factory`.
Mesma fonte também adotada no repositório irmão `geo-ipog` em
2026-05-26.

## Bibliografia mínima

- **Autor**: Andrej Karpathy.
- **Publicado**: 3 de abril de 2026.
- **URL**: https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f
- **Formato**: gist GitHub público, markdown.
- **Linhagem citada pelo autor**: Vannevar Bush, Memex (1945).
- **Implementações comunitárias mapeadas**: 15+ no thread de
  comentários (ΩmegaWiki, Link, Synthadoc, Synto, sqz, LLM-WIKI-MCP,
  SciAI Wiki).

## Análises complementares lidas (não verbatim do gist)

- **Krishnan Srinivasan, Towards AI** (abr/2026): infraestrutura
  Python — helpers `read_wiki`, `write_wiki_updates`, `call_llm`
  (temp 0.3), `browse_wiki`; schema como "single most important
  piece"; INDEX.md/LOG.md como "critical infrastructure".
- **Felix Mao, maoxunxing.com** (abr/2026): implementação Git+Hugo
  com `raw/ → notes/ → posts/`; slash commands `/kb collect`,
  `/kb compile`, `/kb check`.
- **Hari Krishna, Substack** (abr/2026): inclusão de `queries/`
  como categoria (Q&A pré-sintetizado); risco "error compounding"
  (claims falsos viram evidência citada em queries futuras);
  scaling threshold ~100 sources antes de exigir search tools;
  Obsidian + LLM agent side-by-side.

## Claims canônicos extraídos

| ID    | Claim                                                                                              | Alimenta                  |
|-------|----------------------------------------------------------------------------------------------------|---------------------------|
| K-01  | "RAG re-descobre conhecimento do zero a cada query; acúmulo é zero."                               | [[llm-wiki-karpathy]]     |
| K-02  | "LLM Wiki é stateful; conhecimento ingerido vira páginas que compõem ao longo do tempo."           | [[llm-wiki-karpathy]]     |
| K-03  | "Wikis humanos morrem por manutenção crescente; LLMs invertem esse modo."                          | [[llm-wiki-karpathy]]     |
| K-04  | "Arquitetura de 3 camadas: raw (imutável), wiki core (mutável), schema (configuração)."            | [[ADR-001-adopcao-llm-wiki]] |
| K-05  | "4 operações canônicas: Ingest, Query, Lint, Maintain."                                            | `scripts/wiki/*.md`       |
| K-06  | "Ingest: 1 fonte toca 5-15 páginas wiki + apêndice no log."                                        | `scripts/wiki/ingest-playbook.md` |
| K-07  | "Query: buscar no wiki primeiro; respostas valiosas viram páginas novas."                          | `scripts/wiki/query-playbook.md` + [[ADR-002-sync-automatico-courses-wiki]] |
| K-08  | "Lint: checa contradições, órfãos, missing links, stale claims."                                   | `scripts/wiki/lint.py`    |
| K-09  | "index.md: catálogo navegável; substitui infra RAG em escala moderada."                            | `wiki/index.md`           |
| K-10  | "log.md: ledger append-only; parseável com Unix tools."                                            | `wiki/log.md`             |
| K-11  | "Pattern, não blueprint: cada implementação co-evolui com seu agente."                             | `wiki/README.md`          |
| K-12  | "Schema é a peça mais importante; sem ele temos chatbot, com ele temos wiki disciplinada."         | `CLAUDE.md` + governance  |
| K-13  | "Humanos curam fontes e direcionam análise; LLMs fazem a contabilidade."                           | [[ADR-002-sync-automatico-courses-wiki]] |
| HK-01 | "Adicionar `queries/` e `overview/` como categorias canônicas além das 4 originais."               | `wiki/queries/`, `wiki/overview/` |
| HK-02 | "Error compounding: claims falsos viram evidência. Revisão humana em ingest é critica."            | `scripts/wiki/ingest-playbook.md` |
| HK-03 | "Scaling threshold: ~100 sources antes de exigir search tools complementares."                     | Backlog: integração `qmd` |
| TI-01 | "Temperature 0.3 mantém agente consistente; >0.5 vira inventivo."                                  | Não-aplicável (sem agente roteado direto) |

(K = Karpathy original; HK = Hari Krishna; TI = Towards AI Srinivasan)

## Páginas wiki alimentadas

- [[llm-wiki-karpathy]] — conceito canônico.
- [[ADR-001-adopcao-llm-wiki]] — decisão arquitetural.
- [[ADR-002-sync-automatico-courses-wiki]] — decisão sobre hook
  pós-aprovação.
- `wiki/README.md`, `wiki/index.md`, `wiki/log.md` — skeleton.
- `scripts/wiki/lint.py`, `scripts/wiki/sync-courses.py`,
  `scripts/wiki/{ingest,query}-playbook.md` — operacionalização.

## Notas de leitura

- Karpathy evita prescrever diretórios. Adaptamos categorizando em
  10 pastas (vs 4 do gist) para acomodar produto curso-factory.
- Sintaxe de cross-link wiki herdada de Obsidian/TiddlyWiki (formato
  com colchetes duplos).
- Frontmatter YAML obrigatório (não está no gist; nossa convenção).
- Risco "error compounding" reportado por Hari Krishna recebe
  mitigação no ingest playbook: spot-check de 3-5 fontes obrigatório
  antes de ingerir paper novo (regra herdada do CLAUDE.md do
  `geo-ipog`).
