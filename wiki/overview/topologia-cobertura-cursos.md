---
name: topologia-cobertura-cursos
type: overview
status: stable
created: 2026-05-26
updated: 2026-05-26
related:
  - default
  - herreira
  - acme
---

# Topologia de cobertura de cursos (snapshot 26-05-2026)

Mapa do estado atual da fábrica em termos de cursos produzidos,
aprovados, em draft e órfãos. Mantido como overview vivo: atualizar
a cada wave de produção significativa.

## Estado quantitativo

| Categoria             | Quantidade | Path                              |
|-----------------------|------------|-----------------------------------|
| **Aprovados**         | **2**      | `output/approved/` (default) + `output/clients/<id>/approved/` |
| Drafts                | 18         | `output/drafts/`                  |
| Convertidos órfãos    | 12         | `output/converted_from_drafts/`   |
| Deployed              | (n/a)      | `output/deployed/` (vazio)        |
| Páginas wiki/courses/ | 2          | `wiki/courses/`                   |

Cursos aprovados:

- `seo-geo-para-dentistas` (cliente [[clients/default]], vertical saúde).
- `introducao-as-semijoias` (cliente [[clients/herreira]], vertical
  semijoias) — descoberto pelo lint do wiki em 26-05-2026 e
  registrado automaticamente via `scripts/wiki/sync-courses.py`.

**Conclusão:** 2 cursos aprovados (de 18 em drafts e 30 totais).
Taxa de aprovação ~11%. Próximas waves devem priorizar revisão e
quality gate dos drafts antes de produzir cursos novos.

## Drafts identificados

| Slug                                                  | Cliente    | Tags principais            |
|-------------------------------------------------------|------------|----------------------------|
| automacao-com-n8n                                     | default    | automação, no-code         |
| automacao-com-n8n-e-make                              | default    | automação, no-code         |
| deploy-moderno                                        | default    | dev, infra                 |
| deploy-moderno-vercel (checkpoint)                    | default    | dev, infra                 |
| escrita-academica-profunda-geo                        | default    | escrita, geo               |
| geo-para-educacao-financeira-40                       | default    | geo, finanças              |
| geo-para-educacao-financeira-sub-18                   | default    | geo, finanças              |
| introducao-as-semijoias                               | herreira   | semijoias                  |
| llm-finops                                            | default    | finops, llm                |
| llm-finops-custos-otimizacao-e-governanca-de-ia      | default    | finops, llm                |
| mcp-avancado                                          | default    | mcp, dev                   |
| mcp-avancado-servidores-protocolos-e-integracoes     | default    | mcp, dev                   |
| prompt-engineering-avancado                           | default    | prompts                    |
| seo-e-geo-para-advogados                              | default    | seo, geo, jurídico         |
| **seo-e-geo-para-dentistas** (aprovado)               | default    | seo, geo, saúde            |
| seo-e-geo-para-revendedoras-de-joias-e-semijoias      | herreira   | seo, geo, semijoias        |

## Cobertura por vertical

- **Saúde**: 1 aprovado (dentistas). Drafts: 0.
- **Jurídico**: 0 aprovado. Drafts: 1 (advogados).
- **Joalheria/semijoias**: 0 aprovado. Drafts: 2 (cliente herreira).
- **Finanças**: 0 aprovado. Drafts: 2.
- **Dev/infra**: 0 aprovado. Drafts: 4 (n8n, deploy, mcp, prompts).
- **FinOps LLM**: 0 aprovado. Drafts: 2.
- **Escrita acadêmica**: 0 aprovado. Drafts: 1.

## Gaps críticos identificados

Verticais sem nenhum draft em maio/2026 que poderiam justificar
produção em waves Q3 2026:

- Imobiliário.
- Psicologia (sobreposição com ecossistema `geo-ipog`).
- Logística e supply chain.
- Educação executiva (MBA, pós-graduações).

Wikipage candidata em backlog: `[[overview/gaps-criticos-q3-2026]]`.

## Sobreposição cross-ecossistema

Cliente [[default]] tem programa GEO IPOG no repositório `geo-ipog`
focado em psicologia. Curso `seo-e-geo-para-dentistas` deste repo
pode ser modelo para curso futuro `seo-e-geo-para-psicologos` que
casaria com o ecossistema IPOG. Decisão sobre produção em backlog.

## Próxima atualização

Programada para fim de junho/2026 (próxima wave de produção). Script
`scripts/wiki/sync-courses.py` ao rodar deve detectar mudanças e
sugerir update desta página.
