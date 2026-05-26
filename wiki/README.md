# Wiki — curso-factory

> Base de conhecimento persistente da fábrica de cursos, mantida por agentes LLM
> conforme o padrão descrito por Andrej Karpathy em
> [gist.github.com/karpathy/442a6bf555914893e9891c11519de94f](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)
> (3 de abril de 2026).
>
> Adaptado ao contexto da `curso-factory`: o repositório **produz artefatos**
> (cursos) e a wiki vira o **catálogo navegável do produto** com cada curso
> aprovado virando uma página `wiki/courses/<slug>.md` automaticamente.

## Por que esta camada existe

A `curso-factory` já tem três camadas de conhecimento:

1. **Raw imutável** em `docs/research/` (waves Perplexity + Opus) e
   `docs/knowledge/geo-aeo/` (25+ papers + 30 instruções operacionais).
2. **Canônico longo** em `docs/` (7 KBs: GEO_KNOWLEDGE_BASE_2026 v1/v2,
   SEO_KNOWLEDGE_BASE_2026, AI_DISCOVERY_STANDARDS_2026,
   GEO_OPERATING_SYSTEM, GEO_50_CONCEITOS_CANONICAL,
   SEO_GEO_INCREMENT_20260520).
3. **Ledger narrativo** em `CLAUDE.md` (waves históricas 2026-04-09 a
   2026-05-20).

O que faltava: um grafo **vivo, atômico e indexado** que conecte
**cursos produzidos** (output do pipeline) com **conceitos editoriais**
(andragogia Knowles, Bloom, padrão HSM/HBR/MIT Sloan), **clientes
multi-tenant** (default Brasil GEO, herreira, acme), **decisões
arquiteturais** (multi-tenant 2026-04-19, refactor 5-waves 2026-04-29) e
**papers ancora** (Aggarwal KDD 2024, AutoGEO ICLR'26, VMAO).

Tese central Karpathy: **conhecimento que não é catalogado é
redescoberto**. Cada curso novo paga o custo de re-leitura dos 7 KBs
canônicos para encontrar conceito relevante. Atomizar em páginas wiki
cross-linkadas faz o conhecimento compor: o segundo curso de uma
vertical chega 10x mais barato porque entidades, conceitos e fontes
já estão prontos.

## Layout

```
wiki/
  README.md       — este arquivo
  index.md        — catálogo navegável por categoria
  log.md          — ledger append-only de operações
  entities/       — LLMs do pipeline, validators, autores canônicos
  concepts/       — andragogia, Bloom, padrão editorial, quality gate, etc.
  clients/        — uma página por cliente multi-tenant
  courses/        — uma página por curso aprovado (sync automático)
  queries/        — Q&A pré-sintetizado de decisões recorrentes
  overview/       — mapas de cobertura por vertical, gaps
  decisions/      — ADRs estilo "por que escolhemos X"
  sources/        — papers, gists, dossiês externos referenciados >1 vez
  reviews/        — relatórios periódicos de lint
  SUGGESTED_CLAUDE_MD_PATCH.md — bloco a mesclar no CLAUDE.md em onda futura
```

## Operações canônicas

- **Ingest** — `scripts/wiki/ingest-playbook.md`. Toda fonte nova
  (paper, dossiê, transcrição) atualiza 5 a 15 páginas wiki +
  apêndice no log.
- **Query** — `scripts/wiki/query-playbook.md`. Consultar grafo antes
  de re-ler KB monolítico ou disparar nova chamada Perplexity.
- **Lint** — `scripts/wiki/lint.py`. Frontmatter, cross-links, órfãos,
  stale claims, conflitos. Cheque específico curso-factory: curso
  aprovado em `output/approved/` sem página `wiki/courses/`.
- **Sync** — `scripts/wiki/sync-courses.py`. Novidade curso-factory:
  varre `output/approved/` e cria página `wiki/courses/<slug>.md`
  automaticamente para cada curso aprovado sem entrada wiki.

## Convenções obrigatórias

1. Frontmatter YAML em toda página: `name`, `type`, `status`, `created`,
   `updated`, `sources`, `related`.
2. Cross-links via `[[slug]]`. Lint distingue broken vs backlog
   declarado no `index.md`.
3. Filenames ASCII kebab-case. Acentuação mora no corpo.
4. Português PT-BR com acentuação completa (regra REGRA #0 do
   CLAUDE.md).
5. Sem emojis. Sem em-dash em copy editorial.
6. Página atômica: uma página descreve uma coisa.

## Como começar

1. Ler `wiki/index.md` para mapa atual.
2. Antes de iniciar produção de curso novo: buscar `wiki/concepts/`,
   `wiki/clients/<id>`, `wiki/sources/` por termos do tema.
3. Após `python cli.py create "..."` ser aprovado: rodar
   `python scripts/wiki/sync-courses.py` para registrar o curso novo no
   grafo automaticamente.
4. Antes de qualquer push em `wiki/`: rodar `python scripts/wiki/lint.py`.

## Plug-in no `cli.py` (proposto para próxima onda)

Bloco em `wiki/SUGGESTED_CLAUDE_MD_PATCH.md` propõe adicionar
sub-comando `python cli.py wiki {sync, lint, query}` para reduzir
fricção. Esta wave deixa scripts standalone para evitar conflito com
trabalho em andamento na branch `feat/geo-seo-knowledge-2026-deep-research`.

## Linhagem

Vannevar Bush (Memex, 1945). Ted Nelson (Xanadu). Niklas Luhmann
(Zettelkasten). Andy Matuschak (evergreen notes). Detalhes em
`docs/karpathy-llm-wiki-methodology.md`. Decisão arquitetural em
`wiki/decisions/ADR-001-adopcao-llm-wiki.md`.
