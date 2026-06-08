# Wiki Log — curso-factory

> Append-only ledger de operações no wiki. Parseável com `grep`, `awk`,
> `sed`. Nunca editar entradas anteriores. Sempre append no final.
>
> Formato: `YYYY-MM-DD | tipo | autor | descricao | paginas-tocadas`
>
> Tipos válidos: `ingest`, `query`, `lint`, `maintain`, `sync`, `init`.

---

2026-05-26 | init | claude-opus-4-7 | Inauguracao da camada wiki Karpathy adaptada a fabrica de cursos. Skeleton + 6 entities + 6 concepts + 3 clients + 1 course (seed) + 1 query + 1 overview + 2 ADRs + 3 sources + 1 review baseline. Branch isolada wiki/karpathy-llm-wiki-pattern para nao conflitar com feat/geo-seo-knowledge-2026-deep-research. | wiki/README.md wiki/index.md wiki/log.md
2026-05-26 | ingest | claude-opus-4-7 | Ingerido gist Karpathy LLM Wiki como fonte canonica de arquitetura. | sources/2026-04-03-karpathy-llm-wiki-gist.md concepts/llm-wiki-karpathy.md decisions/ADR-001-adopcao-llm-wiki.md
2026-05-26 | ingest | claude-opus-4-7 | Atomizados conceitos editoriais fundadores do pipeline (andragogia Knowles 6 principios, Bloom 3-6 aceitos, HSM/HBR/MIT Sloan, ClientContext, Quality Gate 5 camadas). Antes em arquivos monoliticos (CLAUDE.md, docs/GEO_50_CONCEITOS_CANONICAL.md). | concepts/*.md
2026-05-26 | ingest | claude-opus-4-7 | Catalogados 3 dos 5 LLMs do pipeline e 3 dos 5 validators do quality gate. Outros 4 ficam no backlog declarado em index.md. | entities/*.md
2026-05-26 | sync | claude-opus-4-7 | Seed manual de wiki/courses/ com 1 unico curso aprovado (seo-geo-para-dentistas, cliente default). Futuros entram via scripts/wiki/sync-courses.py automatico. | courses/seo-geo-para-dentistas.md
2026-05-26 | maintain | claude-opus-4-7 | Mapeados 3 clientes multi-tenant ativos (default, acme, herreira). _template fica no backlog. | clients/*.md
2026-05-26 | lint | claude-opus-4-7 | Primeiro lint do grafo. Resultado em reviews/2026-05-26-baseline.md. | reviews/2026-05-26-baseline.md
2026-05-26 | sync | scripts/wiki/sync-courses.py | Sync output approved->wiki courses. Criadas: 1. Atualizadas: 0. | wiki/courses/introducao-as-semijoias.md
2026-05-26 | lint | scripts/wiki/lint.py | orfaos=0 broken=1 stale=0 conflitos=0 courses_sem_wiki=0 | wiki/log.md
