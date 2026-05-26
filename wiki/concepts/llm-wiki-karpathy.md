---
name: llm-wiki-karpathy
type: concept
category: architecture-pattern
status: stable
created: 2026-05-26
updated: 2026-05-26
sources:
  - 2026-04-03-karpathy-llm-wiki-gist
related:
  - quality-gate-5-camadas
sameAs:
  - https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f
---

# LLM Wiki (padrão Karpathy) adaptado a `curso-factory`

Padrão arquitetural proposto por Andrej Karpathy em 03-04-2026 para
construir bases de conhecimento persistentes mantidas por agentes LLM.
Conceito-mãe desta camada `wiki/` do repositório `curso-factory`.
Fonte canônica em [[sources/2026-04-03-karpathy-llm-wiki-gist]].

## Tese central

**RAG é amnésico.** Cada query re-descobre conhecimento. Acúmulo
zero. **LLM Wiki é stateful.** Conhecimento ingerido vira páginas
markdown vivas que compõem ao longo do tempo. O modo de falha humano
(manutenção cresce mais rápido que valor) se inverte: LLMs não
cansam, não esquecem cross-links, não pulam atualização.

## Adaptação ao contexto curso-factory

O gist é proposital agnóstico de domínio. Adaptações específicas para
este repositório:

1. **`wiki/courses/` populado automaticamente.** Curso aprovado em
   `output/approved/` vira página wiki via
   `scripts/wiki/sync-courses.py`. Karpathy K-07 ("respostas valiosas
   viram páginas novas") aplicado em produção real: cada curso é uma
   "query respondida" sobre um tema editorial.
2. **`wiki/clients/` espelha multi-tenant.** Uma página por cliente
   em `config/clients/<id>/client.yaml`, legível e cross-linkada.
3. **`wiki/queries/` herdado de Hari Krishna** — Q&A pré-sintetizado
   para decisões recorrentes (qual nível Bloom, qual padrão
   editorial, etc).
4. **`wiki/overview/` herdado de Hari Krishna** — mapas de cobertura
   por vertical (joalheria, fintech, jurídico, saúde, educação),
   gaps, sobreposições.
5. **Lint cheque específico**: além dos cheques Karpathy (órfãos,
   stale, broken crosslinks), valida curso aprovado em
   `output/approved/` sem página `wiki/courses/<slug>.md`
   correspondente.

## Arquitetura de 3 camadas (mapeamento curso-factory)

| Karpathy        | curso-factory                                          |
|-----------------|--------------------------------------------------------|
| Raw imutável    | `docs/research/`, `docs/knowledge/geo-aeo/`            |
| Wiki mutável    | `wiki/` (esta camada)                                  |
| Schema/config   | `CLAUDE.md` + `docs/karpathy-llm-wiki-methodology.md`  |

E uma quarta camada distinta deste repo:

| curso-factory específico | exemplo                                |
|--------------------------|----------------------------------------|
| Output de produto        | `output/{drafts,approved,deployed}/`   |

A camada de output é onde a wiki "compõe": cada artefato aprovado
vira nó no grafo.

## 4 operações canônicas (adaptadas)

- **Ingest** — `scripts/wiki/ingest-playbook.md`. Toda fonte nova
  toca 5-15 páginas wiki + apêndice no log.
- **Query** — `scripts/wiki/query-playbook.md`. Consultar antes de
  re-ler KB monolítico em `docs/`.
- **Lint** — `scripts/wiki/lint.py`. Inclui cheque
  curso-aprovado-sem-wiki.
- **Sync** — `scripts/wiki/sync-courses.py`. **Novidade
  curso-factory**. Hook pós-aprovação.

## Por que adotamos no curso-factory

Antes da camada wiki, cada curso novo pagava o custo de re-leitura
dos 7 KBs canônicos em `docs/` para encontrar conceito editorial
relevante. Em maio/2026 tínhamos 7 KBs, 4 waves de research, 18
drafts, 1 aprovado, 4 clientes — a complexidade do grafo de
conhecimento implícito já superava capacidade de manter na cabeça.

Decisão arquitetural completa em [[decisions/ADR-001-adopcao-llm-wiki]].
Decisão sobre sync automático em
[[decisions/ADR-002-sync-automatico-courses-wiki]].
