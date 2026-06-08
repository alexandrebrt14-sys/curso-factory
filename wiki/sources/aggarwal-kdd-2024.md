---
name: aggarwal-kdd-2024
type: source
source_type: paper
status: stable
created: 2026-05-26
updated: 2026-05-26
publication_date: 2024-08
author: Pranjal Aggarwal et al.
venue: ACM KDD 2024
url: https://arxiv.org/abs/2311.09735
related:
  - padrao-editorial-hsm-hbr
  - gpt-4o-writer
  - content-checker
---

# Aggarwal et al., KDD 2024 — paper fundador GEO

Paper âncora do programa GEO. Princeton GEO playbook com lifts
mensurados. Referência obrigatória no prompt externo do
[[entities/gpt-4o-writer]] para qualquer curso GEO/SEO produzido a
partir da wave 2026-05-20.

## Bibliografia

- **Autores principais**: Pranjal Aggarwal et al. (Princeton).
- **Título**: "GEO: Generative Engine Optimization".
- **Venue**: ACM KDD 2024.
- **arXiv**: https://arxiv.org/abs/2311.09735.
- **Publicado**: agosto/2024 (versão arxiv anterior em nov/2023).

## Claims canônicos extraídos (lifts mensurados)

| ID     | Claim                                                                          | Aplicação              |
|--------|--------------------------------------------------------------------------------|------------------------|
| AGG-01 | **Cite Sources +115%** lift em visibility em motores generativos.              | Prompt writer.py: 3+ outbound links |
| AGG-02 | **Statistics +41%** lift quando claims acompanham número + fonte + ano.        | Prompt writer.py: 5+ estatísticas |
| AGG-03 | **Quotation +28%** lift quando insight central é citação direta atribuída.    | Prompt writer.py: 1+ quote |
| AGG-04 | Combinação dos 3 supera intervenção isolada (efeito não-aditivo).              | Princeton checklist completa |
| AGG-05 | Intervenções estilísticas (mais simples, mais técnico) tem efeito menor que estruturais. | Foco em estrutura, não floreio |
| AGG-06 | Efeito varia por categoria de query (informational > transactional > navigational). | Considerar tipo de curso |

## Aplicação no pipeline

- **[[entities/gpt-4o-writer]]** — Princeton checklist é cheque
  obrigatório no prompt para cursos com tags `geo-2026`, `seo-2026`.
- **[[entities/content-checker]]** — camada 2 do quality gate ganha
  cheques opcionais (bloqueantes apenas para tags GEO):
  Cite Sources count, Statistics count, Quotation count.
- **[[clients/default]]** — `client.yaml` campo
  `geo_2026.princeton_playbook_enabled: true`.

## Páginas wiki alimentadas

- [[padrao-editorial-hsm-hbr]] — Cite Sources e Statistics se alinham
  com regra "nunca afirmar sem evidência".
- [[entities/gpt-4o-writer]] — referência canônica no prompt
  externo.
- [[entities/content-checker]] — referência das validações opcionais.

## Notas de leitura

- Lifts foram medidos em GEO-bench, dataset proprietário Princeton.
  Generalização para LLMs comerciais (ChatGPT, Claude, Gemini) é
  empiricamente plausível mas não controlada pelo experimento
  original.
- Wave 2026-05-20 (`docs/SEO_GEO_INCREMENT_20260520.md`) consolidou
  o playbook em forma executável para o pipeline.
- Replicação interna parcial em wave 2026-05-17 confirmou direção
  do efeito em ChatGPT 4.5 e Claude Opus 4.5.

## Fonte canônica derivada

`docs/SEO_GEO_INCREMENT_20260520.md` seção "(c) Princeton GEO
playbook com lifts mensurados". Cobre integração com prompt do
writer.py.
