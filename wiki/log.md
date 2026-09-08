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
2026-09-08 | ingest | claude-fable-5-1 | Pedido do dono (abertura direta e sem distracao, R1 a R9) aplicado no PR #83 em tres niveis (doutrina, gerador, gate). Conceito com as nove regras, antes/depois e mapa bloco proibido -> arquivo/funcao -> mudanca; entidade do validador novo abertura_checker (como rodar, como estender validation.abertura); decisao datada com frontmatter completo. | concepts/abertura-direta-sem-distracao.md entities/abertura-checker.md decisions/abertura-direta-sem-distracao-20260908.md
2026-09-08 | maintain | claude-fable-5-1 | content-checker e quality-gate-5-camadas atualizados: zero exercicio por aula, categoria abertura na camada 2, AberturaError na publicacao; index.md com as tres paginas novas. Testes antigos que exigiam checkpoint/exercicio invertidos, registrados no conceito. | entities/content-checker.md concepts/quality-gate-5-camadas.md index.md
2026-09-08 | lint | scripts/wiki/lint.py | orfaos=3 broken=2 stale=23 conflitos=0 courses_sem_wiki=0 | wiki/log.md
2026-09-08 | maintain | claude-fable-5-1 | PR #83 mergeado na main (e55f5a9). Fonte de estilo 1.6.0 ressincronizada (hash 2fc0817a, lexicos.json regerado com aberturaEDistracao); abertura_checker soma as familias da fonte. Estado registrado no conceito, na entidade e na decisao. | concepts/abertura-direta-sem-distracao.md entities/abertura-checker.md decisions/abertura-direta-sem-distracao-20260908.md
