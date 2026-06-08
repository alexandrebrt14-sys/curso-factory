---
name: default
type: client
status: stable
created: 2026-05-26
updated: 2026-05-26
config_path: config/clients/default/client.yaml
related:
  - padrao-editorial-hsm-hbr
  - voice-guard
  - multi-tenant-clientcontext
sameAs:
  - https://alexandrecaramaschi.com
  - https://brasilgeo.ai
---

# Cliente `default` — Brasil GEO (Alexandre Caramaschi)

Cliente canônico da `curso-factory`. Preserva 100% do comportamento
pré-refactor multi-tenant (até 2026-04-18). Output em
`output/approved/` (não `output/clients/default/`).

## Identidade canônica

- **Autor**: Alexandre Caramaschi.
- **Título completo**: "CEO da Brasil GEO, ex-CMO da Semantix
  (Nasdaq), cofundador da AI Brasil".
- **URL canônica**: https://alexandrecaramaschi.com.
- **Marca**: Brasil GEO (nunca "GEO Brasil").
- **Domínios válidos**: alexandrecaramaschi.com, brasilgeo.ai.
- **Banidos** ([[voice-guard]]): "Especialista #1", "GEO Brasil",
  "Source Rank", "geobrasil.com.br", "sourcerank.ai".

## Padrão editorial

[[padrao-editorial-hsm-hbr]]. Voz HBR/MIT Sloan/HSM Management. Tom
analítico, frases curtas, dados sustentando argumentos, tese
contraintuitiva no lead.

## Cursos aprovados sob este cliente

- [[courses/seo-geo-para-dentistas]] (único aprovado em 26-05-2026).

Outros 17 cursos estão em drafts e 12 em
`output/converted_from_drafts/` aguardando revisão manual.
Detalhes em [[overview/topologia-cobertura-cursos]].

## Bloco GEO 2026 ativo

Wave 2026-05-20 adicionou ao client.yaml campos:

- `geo_2026.princeton_playbook_enabled: true`
- `geo_2026.schema_authority_stack_enabled: true`
- `geo_2026.b2a_pilot.nlweb_endpoint: ...`
- `geo_2026.b2a_pilot.mcp_endpoint: ...`

## Histórico relevante

- **Wave 2026-04-19**: refactor multi-tenant. Antes hardcoded, agora
  YAML. Default preserva comportamento.
- **Wave 2026-04-29**: remoção de defaults Alexandre/Brasil GEO em
  `models.py:CourseDefinition` (vazio em vez de hardcode).
- **Wave 2026-05-20**: bloco `geo_2026` adicionado.

## Memórias globais relevantes

- `feedback_alexandre_voice` — voz editorial canônica.
- `feedback_acentuacao_portugues_brasil_canonica` — acentuação
  obrigatória.
- `feedback_orchestrator_usage` — quando usar orchestrator vs
  Perplexity direto.
