---
name: seo-geo-para-dentistas
type: course
status: approved
created: 2026-05-26
updated: 2026-05-26
client: default
slug: seo-geo-para-dentistas
output_path: output/approved/seo-geo-para-dentistas/
draft_path: output/drafts/seo-e-geo-para-dentistas_20260419_183724.json
tags:
  - seo
  - geo
  - saude
  - vertical-odontologia
nivel: intermediario
related:
  - default
  - padrao-editorial-hsm-hbr
  - andragogia-knowles
  - taxonomia-bloom
  - quality-gate-5-camadas
---

# Curso: SEO e GEO para Dentistas

Único curso atualmente aprovado em `output/approved/` na data de
inauguração desta wiki (26-05-2026). Cliente: [[clients/default]]
(Brasil GEO). Vertical: saúde — odontologia.

## Metadata

- **Cliente**: default ([[clients/default]]).
- **Slug**: `seo-geo-para-dentistas`.
- **Nível**: intermediário.
- **Tags**: seo, geo, saude, vertical-odontologia.
- **Draft origem**: `output/drafts/seo-e-geo-para-dentistas_20260419_183724.json`.
- **Path aprovado**: `output/approved/seo-geo-para-dentistas/`.

## Pipeline aplicado

5 LLMs canônicos:

1. [[entities/perplexity-sonar]] (research) — papers GEO 2025-2026 +
   panorama digital de clínicas odontológicas BR.
2. [[entities/gpt-4o-writer]] (draft) — módulos seguindo
   [[padrao-editorial-hsm-hbr]] com [[andragogia-knowles]] e
   [[taxonomia-bloom]].
3. Gemini 2.5 Pro (analyze).
4. Groq Llama 3.3 (classify).
5. [[entities/claude-reviewer]] (review).

## Quality Gate (5 camadas — passou)

- [[entities/accent-checker]]: 0 erros após auto-fix.
- [[entities/content-checker]]: passou (palavras, tabelas, exercícios,
  Bloom, andragogia, clichês ok).
- link_checker: 0 URLs com acento.
- [[entities/voice-guard]]: score >= 70 cliente default.
- cost_tracker: dentro de $10 max por curso.

Detalhes do gate em [[concepts/quality-gate-5-camadas]].

## Por que está nesta wiki

Karpathy K-07: "respostas valiosas viram páginas novas". Cada curso
aprovado é literalmente uma "query respondida" (qual conteúdo SEO+GEO
prepare dentistas em 2026?) cuja síntese vale registrar para reuso.

Página criada **manualmente** nesta wave como seed. Futuros cursos
aprovados entram via `python scripts/wiki/sync-courses.py` automático.

## Cross-vertical

Este curso pode ser variante futura para outros nichos de saúde:
psicologia, fisioterapia, nutrição. Wikipage candidata em backlog:
`[[overview/cobertura-por-vertical]]`.

## Validação cruzada com ecossistema

Cliente default (Brasil GEO) também tem programa GEO IPOG no
ecossistema `geo-ipog`. Conceitos editoriais deste curso (saúde YMYL,
revisão por profissional registrado em conselho, disclaimer de "não
substitui consulta") podem ser harmonizados com padrão YMYL do
geo-ipog. Decisão sobre harmonização pendente.
