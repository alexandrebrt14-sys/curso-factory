# Metodologia LLM Wiki Karpathy aplicada ao `curso-factory`

Documento canônico de governança que descreve a tese, as fontes
externas, as implementações comunitárias relevantes e a adaptação
concreta adotada no repositório `curso-factory`.

Última revisão: 2026-05-26.

---

## 1. Origem

Andrej Karpathy publicou em 3 de abril de 2026 o gist
[gist.github.com/karpathy/442a6bf555914893e9891c11519de94f](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)
descrevendo um padrão arquitetural para bases de conhecimento
mantidas por agentes LLM. O gist explicitamente evita prescrever
diretórios, formatos e tooling: é uma ideia para ser "copiada,
colada e adaptada".

## 2. Tese central

**RAG é amnésico.** Cada query re-descobre conhecimento do zero. Não
há acúmulo entre execuções. O custo cognitivo por consulta cresce
indefinidamente com o tamanho da base.

**LLM Wiki é stateful.** Conhecimento ingerido vira páginas markdown
vivas que compõem ao longo do tempo. Conexões pré-estabelecidas.
Contradições já sinalizadas. Cada onda nova reduz custo da próxima.

**Inversão do modo de falha humano.** Wikis humanos morrem porque
manutenção cresce mais rápido que valor. LLMs não cansam, não
esquecem cross-references, não pulam atualização. O humano cura
fontes e direciona análise; o LLM faz a contabilidade.

## 3. Linhagem intelectual

- **Vannevar Bush, "As We May Think", 1945.** Conceito do Memex.
  Bush não resolveu manutenção porque era humana.
- **Ted Nelson, Project Xanadu, anos 1960.** Hipertexto bidirecional
  com transclusão. Inspiração para sintaxe `[[slug]]`.
- **Niklas Luhmann, Zettelkasten.** Cartões atômicos com
  cross-references explícitos. "Uma ideia, um cartão" herdado em
  "uma página descreve uma coisa".
- **TiddlyWiki, Obsidian.** Implementações modernas Zettelkasten.
- **Andy Matuschak, evergreen notes.** "Notes should be atomic,
  densely linked, and concept-oriented."

## 4. Análises comunitárias incorporadas

Lemos e incorporamos peças específicas de 3 análises além do gist:

- **Krishnan Srinivasan, Towards AI** — Schema é "the single most
  important piece of the whole system" (incorporamos como princípio).
  Temperature 0.3 mantém agente consistente (não-aplicável aqui:
  ainda não temos agente roteado direto).
- **Felix Mao, maoxunxing.com** — Slash commands `/kb collect`,
  `/kb compile`, `/kb check`. Adaptamos como sub-comando proposto
  `cli.py wiki {sync, lint, query}` em
  `wiki/SUGGESTED_CLAUDE_MD_PATCH.md`.
- **Hari Krishna, Substack** — Categorias adicionais `queries/` e
  `overview/`; risco "error compounding"; scaling threshold ~100
  sources. **Os três insights são incorporados no curso-factory**
  (categorias criadas, spot-check obrigatório no ingest, integração
  com search tool em backlog para quando passarmos de 100 páginas).

## 5. Adaptação canônica no `curso-factory`

### 5.1 Diretório raiz

`wiki/` na raiz do repositório. Não em `docs/` para evitar mistura
com KBs canônicos longos.

### 5.2 Tipos canônicos de página (10 categorias)

Karpathy original tem 4 categorias (`entities`, `concepts`,
`decisions`, `sources`). Adaptamos para 10 dado o contexto produto:

| Tipo       | Pasta            | Critério                                     |
|------------|------------------|----------------------------------------------|
| entity     | `entities/`      | LLMs do pipeline, validators, autores        |
| concept    | `concepts/`      | Definição atômica reusável                   |
| client     | `clients/`       | Cliente multi-tenant (espelho do client.yaml)|
| course     | `courses/`       | Curso aprovado (sync automático)             |
| query      | `queries/`       | Q&A sintetizada (Hari Krishna)               |
| overview   | `overview/`      | Mapa de cobertura/gaps (Hari Krishna)        |
| decision   | `decisions/`     | ADR cujo "porquê" não cabe em commit         |
| source     | `sources/`       | Fonte externa ou dossiê referenciado >1 vez  |
| review     | `reviews/`       | Relatório periódico de lint                  |
| meta       | (arquivos raiz)  | README, index, log, SUGGESTED_CLAUDE_MD_PATCH|

### 5.3 Convenções

- Frontmatter YAML obrigatório (`name`, `type`, `status`, `created`,
  `updated`, `sources`, `related`).
- Cross-links via `[[slug]]`. Lint distingue broken vs backlog.
- Filenames ASCII kebab-case.
- Português PT-BR com acentuação completa (REGRA #0 do CLAUDE.md).
- Sem emojis. Sem em-dash em copy editorial.
- Página atômica: uma página descreve uma coisa.

### 5.4 Coexistência com camadas existentes

- `docs/research/`, `docs/knowledge/geo-aeo/`: **raw imutável**.
- `docs/*.md` (7 KBs): **canônico longo** com governança formal.
- `CLAUDE.md`: **schema + ledger narrativo**.
- `output/{drafts,approved,deployed}/`: **produto entregue**.
- `wiki/`: **camada mutável atômica cross-linkada** (esta camada
  nova).
- `wiki/log.md`: **ledger append-only parseável** (para automação).

### 5.5 Operações canônicas

| Operação  | Implementação                                |
|-----------|----------------------------------------------|
| Ingest    | `scripts/wiki/ingest-playbook.md`            |
| Query     | `scripts/wiki/query-playbook.md`             |
| Lint      | `scripts/wiki/lint.py` (Python funcional)    |
| Sync      | `scripts/wiki/sync-courses.py` (Python)      |
| Maintain  | implícito em ingest/query                    |

### 5.6 Específico curso-factory: 3 novidades

1. **`wiki/courses/` com sync automático.** Cada curso em
   `output/approved/` ganha página wiki esqueleto via
   `sync-courses.py`. Idempotente. Decisão em ADR-002.
2. **`wiki/clients/` espelha multi-tenant.** Uma página por cliente
   em `config/clients/<id>/client.yaml`.
3. **Cheque adicional no lint.** `python scripts/wiki/lint.py`
   reporta cursos aprovados sem página wiki como
   `courses_sem_wiki`. Zero tolerância (sync resolve).

## 6. Disciplina obrigatória nas waves futuras

1. **Antes** de produzir curso novo via `python cli.py create`:
   consultar `wiki/index.md`, `wiki/clients/<id>.md` e
   `wiki/overview/`.
2. **Após** quality gate aprovar curso: rodar
   `python scripts/wiki/sync-courses.py`.
3. **Antes** de qualquer push em `wiki/`: rodar
   `python scripts/wiki/lint.py`.
4. **Antes** de pesquisa externa: consultar `wiki/concepts/`,
   `wiki/sources/`, `wiki/queries/`. Regra Karpathy K-07.
5. **Mensalmente**: review formal em `wiki/reviews/YYYY-MM-DD-mensal.md`.

## 7. Métricas de sucesso

Revisar em 30, 60 e 90 dias após inauguração (2026-05-26):

- Pelo menos 50% dos cursos aprovados do trimestre com
  `wiki/courses/<slug>.md` correspondente.
- Crescimento: 3+ páginas novas por wave de produção.
- Backlog explícito reduz por wave.
- 0 órfãos não-justificados em review mensal.
- 0 cursos aprovados sem página wiki (sync resolve).
- Tempo médio de resposta a query operacional <2 min.

## 8. Riscos conhecidos e mitigações

- **Duplicação com `docs/`.** Mitigação: docs é canônico longo,
  wiki é atômico cross-linkado.
- **Error compounding** (Hari Krishna). Mitigação: spot-check
  obrigatório no ingest playbook.
- **Cemitério de páginas semi-prontas.** Mitigação: threshold de
  lint para órfãos e stale; review mensal obrigatório.
- **Sync automático sobrescreve enriquecimento manual.** Mitigação:
  `sync-courses.py` é idempotente; apenas cria páginas faltantes e
  atualiza `updated` quando `--force-update`. Não destrói cross-links
  manuais.
- **Branch isolada da `feat/geo-seo-knowledge-2026-deep-research`.**
  Mitigação: `wiki/SUGGESTED_CLAUDE_MD_PATCH.md` documenta merge
  controlado em onda futura.

## 9. Referências

- Karpathy, A. "LLM Wiki gist", 03-04-2026:
  https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f
- Bush, V. "As We May Think", The Atlantic, jul/1945:
  https://www.theatlantic.com/magazine/archive/1945/07/as-we-may-think/303881/
- Srinivasan, K. "Compounding Knowledge With LLMs: Karpathy's Wiki
  Pattern in Action", Towards AI, abr/2026.
- Mao, F. "Practicing Karpathy's Personal Knowledge Base Method with
  a Git Repository", abr/2026:
  https://maoxunxing.com/karpathy-knowledge-base-practice/
- Krishna, H. "Andrej Karpathy's LLM Wiki: Full Breakdown and How to
  Build Your Own", Substack, abr/2026:
  https://nandigamharikrishna.substack.com/p/andrej-karpathys-llm-wiki-full-breakdown
- Matuschak, A. "Evergreen notes":
  https://notes.andymatuschak.org/Evergreen_notes
- Decisão arquitetural derivada:
  `wiki/decisions/ADR-001-adopcao-llm-wiki.md`.
- Decisão sync automático:
  `wiki/decisions/ADR-002-sync-automatico-courses-wiki.md`.
- Implementação irmã no repo `geo-ipog`: commit `d4766d8` em
  `alexandrebrt14-sys/geo-ipog`.
