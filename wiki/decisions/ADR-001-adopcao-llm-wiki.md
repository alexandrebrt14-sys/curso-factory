---
name: ADR-001-adopcao-llm-wiki
type: decision
status: accepted
created: 2026-05-26
updated: 2026-05-26
decision_date: 2026-05-26
decided_by: alexandre-caramaschi
sources:
  - 2026-04-03-karpathy-llm-wiki-gist
related:
  - llm-wiki-karpathy
  - default
---

# ADR-001 — Adoção do padrão LLM Wiki Karpathy na camada `wiki/` do `curso-factory`

**Status:** Accepted
**Data:** 2026-05-26
**Decidido por:** Alexandre Caramaschi
**Sponsor:** cliente [[clients/default]] (Brasil GEO)

## Contexto

Em maio/2026 o `curso-factory` acumulava:

- 7 KBs canônicos em `docs/` (GEO_KNOWLEDGE_BASE_2026 v1/v2,
  SEO_KNOWLEDGE_BASE_2026, AI_DISCOVERY_STANDARDS_2026,
  GEO_OPERATING_SYSTEM, GEO_50_CONCEITOS_CANONICAL,
  SEO_GEO_INCREMENT_20260520).
- 4 waves de research em `docs/research/`.
- 18 drafts e 1 aprovado (`seo-geo-para-dentistas`).
- 12 cursos convertidos órfãos aguardando revisão.
- 4 clientes multi-tenant (default, acme, herreira, _template).
- CLAUDE.md de 29 KB com waves históricas (2026-04-09, 2026-04-19,
  2026-04-25, 2026-04-29, 2026-05-17, 2026-05-20).

Sintomas observados:

1. **Re-leitura dos 7 KBs como gargalo**. Cada curso novo paga custo
   de re-leitura para encontrar conceito editorial relevante.
2. **Acúmulo sem composição.** Cursos aprovados ficam em
   `output/approved/` mas sem grafo navegável que conecte conceitos
   editoriais aplicados, fontes citadas e clientes atendidos.
3. **Decisões arquiteturais narradas no CLAUDE.md**, não atomizadas.
   Waves importantes (refactor multi-tenant, refactor 5-waves,
   Princeton checklist) misturadas com instruções operacionais.
4. **Pergunta recorrente "qual padrão usar para cliente Y?"** exige
   re-leitura do `client.yaml` toda vez.

## Alternativas consideradas

1. **Status quo.** Continuar com CLAUDE.md monolítico + docs/ longos.
   Custo de re-leitura cresce com cada cliente e curso. Rejeitada.
2. **RAG vetorial sobre `docs/`.** Resolve descoberta mas não resolve
   acúmulo nem composição. Cada query reinventa síntese. Rejeitada.
3. **Migrar para Notion ou similar.** Quebra fluxo git-nativo do
   pipeline. Perde versionamento e auditabilidade. Rejeitada.
4. **LLM Wiki padrão Karpathy.** Camada `wiki/` mutável,
   cross-linkada, com sync automático de cursos aprovados. Aceita.

## Decisão

Adotar o padrão descrito em
[gist.github.com/karpathy/442a6bf555914893e9891c11519de94f](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)
como camada complementar (não substitutiva) das existentes:

- `docs/research/`, `docs/knowledge/geo-aeo/`: **raw imutável**.
- `docs/*.md` (7 KBs): **canônico longo** com governança formal.
- `CLAUDE.md`: **schema + ledger narrativo**.
- `output/approved/`, `output/deployed/`: **produto entregue**.
- `wiki/`: **camada mutável atômica cross-linkada** (esta camada nova).

Adaptação específica curso-factory: 5 categorias canônicas além das 4
do gist Karpathy:

- `wiki/clients/` (multi-tenant nativo).
- `wiki/courses/` (sync automático de produto).
- `wiki/queries/` (Q&A sintetizado, inspirado em Hari Krishna).
- `wiki/overview/` (mapas de cobertura, inspirado em Hari Krishna).
- `wiki/reviews/` (lint periódico).

## Consequências

### Positivas esperadas

- Queries futuras consultam `wiki/index.md` antes de re-ler KB
  monolítico.
- Cada curso aprovado entra automaticamente no grafo via
  `python scripts/wiki/sync-courses.py` (detalhes em
  [[decisions/ADR-002-sync-automatico-courses-wiki]]).
- Lint detecta órfãos, cross-links quebrados, stale claims **e**
  curso aprovado sem página wiki.
- ADRs atomizadas substituem narrativa de waves no CLAUDE.md de
  forma incremental (legado preservado).

### Negativas e custo

- Disciplina nova: toda wave de produção atualiza wiki + log.
- Risco de duplicação com `docs/` se fronteira não respeitada.
  Mitigação: regra explícita ("docs é canônico longo, wiki é
  atômico cross-linkado").
- Custo inicial: ~24 páginas escritas manualmente nesta inauguração.

### Métricas de sucesso (30/60/90 dias)

- Pelo menos 50% dos cursos aprovados do trimestre têm
  `wiki/courses/<slug>.md` correspondente.
- Backlog explícito reduz por wave.
- 0 órfãos não-justificados em review mensal.
- Pelo menos 1 query operacional respondida via wiki sem re-leitura
  de KB (medido via `wiki/log.md` apêndice).

## Implementação

Concluída em 2026-05-26 (este commit) em branch isolada
`wiki/karpathy-llm-wiki-pattern`. Bloco para mesclar em CLAUDE.md
fornecido em `wiki/SUGGESTED_CLAUDE_MD_PATCH.md` para aplicação
controlada após merge da `feat/geo-seo-knowledge-2026-deep-research`.

Detalhes em `docs/karpathy-llm-wiki-methodology.md`.
