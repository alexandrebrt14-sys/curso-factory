---
name: herreira
type: client
status: stable
created: 2026-05-26
updated: 2026-05-26
config_path: config/clients/herreira/client.yaml
related:
  - multi-tenant-clientcontext
  - padrao-editorial-hsm-hbr
sameAs:
  - https://herreirasemijoias.com.br
---

# Cliente `herreira` — joalheria

Cliente real em produção. Vertical: **semijoias**. Domínio público:
`herreirasemijoias.com.br`. Output em `output/clients/herreira/`.

## Função no programa

Validação do `curso-factory` em vertical não-tech (joalheria de luxo
e semijoias). Caso de teste real de que o padrão editorial
[[padrao-editorial-hsm-hbr]] sobrevive em nicho criativo-sensorial.

## Customizações vs default

Algumas regras editoriais relaxadas vs cliente [[clients/default]]:

- Parágrafos podem chegar a 7 linhas (default: 5) em descrições
  sensoriais de peças.
- Vocabulário técnico de joalheria aceito sem glossário inline
  (ouro 750, prata 950, banho de ródio, micropavé, etc).
- Voice guard: lista canonical inclui termos de marca; banned
  inclui jargão concorrente.

## Cursos em produção

Drafts identificados em `output/drafts/`:

- `introducao-as-semijoias_20260419_190037.json`
- `seo-e-geo-para-revendedoras-de-joias-e-semijoias-autoridade-e-vendas-na-era-da-ia_20260328_182821.json`

Nenhum aprovado ainda. Aprovação pendente revisão editorial do
cliente.

## Cross-referencias com ecossistema externo

Cliente tem operação digital em múltiplos repos do ecossistema Brasil
GEO (não-curso-factory):

- Worker Cloudflare `herreira-discover`.
- Astro pages `herreira-home-v4`.
- Schema canônico `PATRICIA_PERSON_BASE` (Patrícia Herreira) com
  hasCredential e knowsAbout.

Detalhes em memória global `project_herreira_geo_7_ondas_20260520`.

## Status

`stable` — em produção desde 19-04-2026. Próxima revisão de pacote
editorial pendente para junho/2026.
