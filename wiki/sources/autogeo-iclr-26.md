---
name: autogeo-iclr-26
type: source
source_type: paper
status: stable
created: 2026-05-26
updated: 2026-05-26
publication_date: 2026-05
author: Wu, Zhong, Kim, Xiong (CMU)
venue: ICLR 2026
url: https://github.com/cxcscmu/AutoGEO
related:
  - aggarwal-kdd-2024
  - gpt-4o-writer
---

# AutoGEO (Wu/Zhong/Kim/Xiong CMU) — ICLR 2026

Paper ICLR'26 que reporta **+50,99% lift** em GEO via 5 regras
operacionais simples. Reportado em maio/2026. Obrigatório no prompt
externo do [[entities/gpt-4o-writer]] para qualquer curso GEO/SEO a
partir da wave 2026-05-24.

## Bibliografia

- **Autores**: Wu, Zhong, Kim, Xiong (Carnegie Mellon University).
- **Título**: AutoGEO.
- **Venue**: ICLR 2026.
- **Código + paper**: https://github.com/cxcscmu/AutoGEO.

## Claims canônicos extraídos

| ID     | Claim                                                            | Aplicação            |
|--------|------------------------------------------------------------------|----------------------|
| AGE-01 | **+50,99% lift** combinando 5 regras AutoGEO em GEO-bench.        | Justifica prioridade no prompt |
| AGE-02 | Regra 1: estruturar conteúdo em blocos atômicos com header claro. | Sub-headings a cada 2-3 parágrafos (já em [[padrao-editorial-hsm-hbr]]) |
| AGE-03 | Regra 2: incluir estatísticas com fonte (overlap com Aggarwal AGG-02). | Cheque Statistics no [[entities/content-checker]] |
| AGE-04 | Regra 3: usar formato tabela para comparativos (lift adicional). | Já obrigatório em [[padrao-editorial-hsm-hbr]] |
| AGE-05 | Regra 4: incluir 1-2 citações diretas atribuídas (overlap AGG-03). | Cheque Quotation |
| AGE-06 | Regra 5: TL;DR de 1-2 frases logo após h1 (Speakable hook).      | Backlog: adicionar componente TLDR no template |

## Aplicação no pipeline

- **[[entities/gpt-4o-writer]]** — prompt externo
  `src/templates/prompts/draft.md` inclui as 5 regras AutoGEO como
  bloco obrigatório para tags `geo-2026`.
- **[[clients/default]]** — `client.yaml` campo
  `geo_2026_pos_io.autogeo_enabled: true` (proposto na wave
  2026-05-24 em desenvolvimento).

## Páginas wiki alimentadas

- [[entities/gpt-4o-writer]] — referência no prompt.
- Sobreposição com [[sources/aggarwal-kdd-2024]] em AGG-02/AGG-03.

## Notas de leitura

- Lift de +50,99% é grande para uma única intervenção paramétrica.
  Sugere que o GEO-bench original ainda tem espaço significativo
  para otimização estrutural simples.
- Wave 2026-05-24 (`docs/research/geo-wave-maio-posio-2026/`) trouxe
  paper para o radar. Doc canônico
  `WAVE_MAIO_2026_POSIO_CANONICAL.md` seção sobre AutoGEO ICLR'26.
- Replicação interna pendente em junho/2026.

## Fonte canônica derivada

`docs/research/geo-wave-maio-posio-2026/WAVE_MAIO_2026_POSIO_CANONICAL.md`
seção "AutoGEO ICLR'26".
