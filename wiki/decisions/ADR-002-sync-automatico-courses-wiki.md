---
name: ADR-002-sync-automatico-courses-wiki
type: decision
status: accepted
created: 2026-05-26
updated: 2026-05-26
decision_date: 2026-05-26
decided_by: alexandre-caramaschi
related:
  - ADR-001-adopcao-llm-wiki
  - llm-wiki-karpathy
  - quality-gate-5-camadas
---

# ADR-002 — Sync automático `output/approved/` → `wiki/courses/`

**Status:** Accepted
**Data:** 2026-05-26
**Decidido por:** Alexandre Caramaschi

## Contexto

A camada `wiki/` adotada na [[ADR-001-adopcao-llm-wiki]] cria a pasta
`wiki/courses/` para conter uma página por curso aprovado. Como
garantir que essa pasta fique sincronizada com `output/approved/`
sem virar gargalo manual?

Três opções:

1. **Manual.** Autor cria página `wiki/courses/<slug>.md`
   manualmente após cada `python cli.py create` bem-sucedido.
   Rejeitada: viola princípio Karpathy "LLM faz a contabilidade,
   humano cura conteúdo".
2. **Hook pós-aprovação no orchestrator.** Modificar
   `src/orchestrator.py` para chamar gerador de wiki page ao final
   do quality gate. Rejeitada por enquanto: aumenta acoplamento; a
   geração de wiki page é distinta da geração de curso.
3. **Script standalone `sync-courses.py`.** Varre
   `output/approved/` e cria/atualiza páginas wiki faltantes.
   Idempotente. Aceita.

## Decisão

`scripts/wiki/sync-courses.py` standalone:

- Lê `output/approved/<slug>/` (cursos do cliente default).
- Lê `output/clients/<client>/approved/<slug>/` (outros clientes).
- Para cada slug, verifica se existe `wiki/courses/<slug>.md`.
- Se não existe, gera página com frontmatter canônico (name, type,
  status, client, slug, tags, etc) e corpo template (metadata,
  pipeline aplicado, cross-links para entities/concepts/clients).
- Se existe, atualiza apenas o `updated` no frontmatter.
- Apende entrada em `wiki/log.md` com formato `sync`.
- Idempotente: re-rodar não duplica nem destrói trabalho manual de
  enriquecer página.

## Quando rodar

- **Manual após `python cli.py create`** bem-sucedido.
- **Pre-push hook git** (opcional): bloqueia push se há curso
  aprovado sem página wiki correspondente.
- **CI cron diário** (opcional, em backlog): roda sync + lint
  automaticamente em main.

## Por que não é hook do orchestrator

Princípio de **separação de domínio**:

- Orchestrator/pipeline: gera curso.
- `sync-courses.py`: gera meta-informação no grafo wiki.

Falha no sync não deve bloquear aprovação do curso. Falha do
orchestrator não deve corromper wiki.

## Consequências

### Positivas

- Karpathy K-13 ("LLM faz contabilidade") aplicado em produção.
- `wiki/courses/` sempre reflete realidade de
  `output/approved/`.
- Enriquecimento manual de páginas wiki preservado entre syncs.

### Negativas

- Requer disciplina de rodar o script (não automático no pipeline).
  Mitigação: documentado em `wiki/README.md` e em
  `wiki/SUGGESTED_CLAUDE_MD_PATCH.md` como rotina obrigatória pós
  `cli.py create`.
- Página gerada automática é esqueleto. Enriquecimento manual
  (cross-links extras, notas pedagógicas, decisões editoriais) fica
  como tarefa humana opcional.

### Métricas de sucesso

- 100% dos cursos aprovados têm página wiki em <24h da aprovação.
- 0 cursos aprovados sem `wiki/courses/<slug>.md` correspondente
  no review mensal (cheque programático em
  `scripts/wiki/lint.py`).

## Implementação

Script em `scripts/wiki/sync-courses.py`. Documentação operacional
em `scripts/wiki/ingest-playbook.md` seção "Sync após aprovação".
