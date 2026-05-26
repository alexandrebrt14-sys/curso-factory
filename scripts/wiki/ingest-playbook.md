# Ingest playbook — wiki/ Karpathy no curso-factory

Receita canônica para processar uma fonte nova (paper, gist, dossiê,
transcrição de reunião) e atualizar de 5 a 15 páginas wiki, com
apêndice no `wiki/log.md`. Não é script automático: é prompt de
operação para agente LLM (Claude Code, Codex, OpenCode).

## Quando usar

- Recebeu link novo de paper ou gist do usuário.
- Terminou wave de research (Perplexity, sub-agents Opus) com
  dossiê novo em `docs/research/`.
- Recebeu transcrição de reunião com cliente que muda contexto
  editorial.
- **Sync após aprovação de curso novo** — caso especial coberto por
  `scripts/wiki/sync-courses.py`.

## Pré-requisitos

- Repositório `curso-factory` clonado, branch atualizada.
- Acesso de escrita ao `wiki/`.
- Saber o domínio da fonte (paper acadêmico, dossiê interno,
  decisão editorial).

## Passo a passo canônico

### 1. Identificar tipo da fonte

| Fonte                                | Onde guardar a página `source`              |
|--------------------------------------|---------------------------------------------|
| Gist, paper arxiv, post de autor     | `wiki/sources/YYYY-MM-DD-slug.md` ou `wiki/sources/<author-venue-year>.md` |
| Dossiê interno em `docs/research/`   | `wiki/sources/YYYY-MM-DD-slug.md` (ponteiro)|
| Transcrição de reunião               | `wiki/sources/YYYY-MM-DD-meet-slug.md`      |
| Dataset                              | `wiki/sources/YYYY-MM-DD-dataset-slug.md`   |
| **Curso aprovado**                   | `wiki/courses/<slug>.md` via `sync-courses.py` (não manual) |

### 2. Criar a página `source/`

Frontmatter mínimo:

```yaml
---
name: <slug-data-ou-autor>
type: source
source_type: gist | paper | internal-dossier | meeting | dataset
status: stable | provisional
created: YYYY-MM-DD
updated: YYYY-MM-DD
publication_date: YYYY-MM-DD
author: <quem produziu>
url: <se externo>
internal_path: <se interno>
related: []
---
```

Corpo deve conter:

- **Bibliografia mínima** (autor, venue, ano, URL).
- **Claims canônicos extraídos** em tabela `| ID | Claim | Alimenta |`.
  Cada claim recebe ID estável (`AGG-XX` para Aggarwal, `K-XX` para
  Karpathy, etc).
- **Páginas wiki alimentadas** (lista de cross-links).
- **Notas de leitura** opcionais.

### 3. Spot-check obrigatório (mitigação error compounding)

Antes de ingerir paper ou gist como fonte canônica:

- WebFetch das 3-5 URLs principais citadas.
- Confirmar que existem (não 404).
- Confirmar autor + ano + venue + claim principal.
- Se Perplexity ou agente confabulou DOI/URL: marcar `[FALTA EVIDÊNCIA]`
  na página source e NÃO usar como evidência em curso até resolver.

Risco "error compounding" (Hari Krishna): claim falso ingerido vira
evidência citada em queries futuras e em prompts dos LLMs do pipeline.
Corrupção compostos rápido. Spot-check é **obrigatório**, não opcional.

### 4. Mapear claims para páginas wiki

Para cada claim, decidir:

- Alimenta página **existente**? Atualizar, anexar evidência,
  incrementar `updated` no frontmatter.
- Justifica página **nova**? Criar em `entities/`, `concepts/`,
  `decisions/` ou `clients/` conforme natureza.
- É **opinião isolada** sem suporte cruzado? Não criar página;
  ficar apenas na source.

Meta canônica Karpathy: 1 fonte nova toca 5 a 15 páginas. <3 sugere
fonte fraca ou grafo pobre. >20 sugere fonte composta — decompor.

### 5. Aplicar cross-links

Toda página tocada ganha pelo menos 1 cross-link `[[slug]]` para
outra página wiki relevante. Cross-link unidirecional aceito; lint
detecta órfãos.

### 6. Atualizar `wiki/index.md`

- Adicionar página nova na categoria certa, ordem alfabética.
- Se criou conceito mencionado no backlog declarado, remover do
  backlog.
- Se mencionou conceito não-existente via `[[slug]]`, adicionar ao
  backlog.

### 7. Apendar `wiki/log.md`

Formato:

```
YYYY-MM-DD | ingest | <agent-id> | <descricao em 1 linha> | <paginas tocadas>
```

Nunca editar entradas anteriores. Sempre append no final.

### 8. Rodar lint

```bash
python scripts/wiki/lint.py
```

Endereçar `broken_crosslinks` fora do backlog e `missing_frontmatter`
zero antes de commit.

### 9. Commit

Padrão: `feat(wiki): ingest <source-slug> + tocar N paginas`.

Incluir: source page nova, todas páginas wiki tocadas, `index.md`
atualizado, `log.md` atualizado.

## Sync após aprovação de curso (caso especial)

Quando `python cli.py create "..."` termina com `aprovado=True`:

```bash
python scripts/wiki/sync-courses.py
```

Cria `wiki/courses/<slug>.md` esqueleto automaticamente. Apêndice
log entra como `sync`, não `ingest`. Enriquecimento manual da página
fica como tarefa humana opcional (cross-links extras, notas
pedagógicas, variantes para outras verticais).

Detalhes da decisão arquitetural em
`wiki/decisions/ADR-002-sync-automatico-courses-wiki.md`.

## Anti-padrões

- Criar página wiki com 1 parágrafo só para "abrir slot". Página
  atômica precisa de conteúdo real ou vira ruído.
- Cross-link `[[slug]]` para slug que você não pretende criar nem
  declarar no backlog.
- Esquecer de atualizar `wiki/log.md`.
- Ingerir 1 fonte que toca <3 páginas. Fonte fraca ou grafo pobre.
- Ingerir paper sem spot-check (risco error compounding).
- Misturar ingest manual de paper com sync automático de curso no
  mesmo commit (separação de domínio).
