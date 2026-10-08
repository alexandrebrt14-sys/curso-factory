---
name: publicacao-conteudo-midia-20261008
type: insight
status: proposed
created: 2026-10-08
updated: 2026-10-08
author: Codex
sources:
  - docs/PUBLICACAO_CONTEUDO_MIDIA.md
  - src/generators/metadata_sync.py
  - src/output_paths.py
related:
  - arquivo-de-conteudo-sem-consumidor
  - integracao-conflitos-tem-dono
---

# Proposta: comprovar a entrega de conteúdo e mídia

**Sem aprovação do dono.** Este registro não integra `decisions/INDEX.md`, prompts nem
regras vivas. A execução autorizada da migração não aprova automaticamente esta lição.

Evidência: a migração de 08/10/2026 no landing-page-geo retirou mídia do checkout com
inventário, SHA-256, piloto, recibo integral e backup; a leitura desta fábrica mostrou
que `MetadataSync` atribui `deployed` pela existência da pasta, sem consultar produção.
O `course_catalog.json` emitido não tem consumidor automático confirmado na landing.

Proposta: distinguir geração local, entrega revisada e publicação verificável. Manter
intermediários na fábrica; entregar mídias pelo contrato do portal e conferir CDN,
download, consumidores de imagem e exportação offline antes de retirar os originais.
Não inferir deploy a partir de um nome de pasta ou sucesso do gerador.

A guarda implementada para rascunhos e catálogo, seus limites e as automações ainda
ausentes estão em [Publicação de conteúdo e mídia](../../docs/PUBLICACAO_CONTEUDO_MIDIA.md).
Relacionadas: [[arquivo-de-conteudo-sem-consumidor]] e [[integracao-conflitos-tem-dono]].

## Linha do tempo

- 08/10/2026 — Codex registrou a proposta a partir da migração e da inspeção dos produtores.
  Sem aprovação, promoção a regra ou alteração do status do dono.
