---
name: multi-tenant-clientcontext
type: concept
category: architecture
status: stable
created: 2026-05-26
updated: 2026-05-26
related:
  - voice-guard
  - padrao-editorial-hsm-hbr
---

# Multi-tenant via ClientContext

Arquitetura adotada na **wave 2026-04-19** que tornou a
`curso-factory` replicável para múltiplos clientes sem fork.
Implementada em `src/clients/context.py` e
`src/clients/loader.py`.

## Problema que resolvia

Antes (até 2026-04-18): credencial de Alexandre Caramaschi, domínio
`alexandrecaramaschi.com`, padrão HSM/HBR/MIT Sloan e regras do
voice guard estavam **hardcoded** em `models.py`, `voice_guard.py`,
`pyproject.toml`. Para rodar a fábrica para outro cliente seria
necessário fork do repo inteiro.

## Solução

Tudo que varia por cliente vem de `config/clients/<id>/client.yaml`.
Framework carrega o YAML em um `ClientContext` (dataclass em
`src/clients/context.py`) e injeta em todos os pontos sensíveis a
identidade:

- `CourseFactory` (orquestrador)
- `Orchestrator` (pipeline)
- `SchemaBuilder` (gerador JSON-LD)
- `QualityGate` (camadas de validação)
- `voice_guard_check` ([[voice-guard]])
- Prompts Jinja2 via `{{ client.author.name }}`, `{{ client.domain }}`

## Comportamento canônico

- Cliente `default` preserva 100% do comportamento pré-refactor (Brasil
  GEO). Output em `output/approved/`.
- Qualquer `<id>` diferente escreve em `output/clients/<id>/`.
- CLI: `python cli.py create "Curso" --client minhaempresa` ou
  `export CURSO_FACTORY_CLIENT=<id>`.
- Listar: `python cli.py clients`.

## Schema YAML do cliente

Campos canônicos em `config/clients/<id>/client.yaml`:

```yaml
id: <id>
author:
  name: ...
  title: ...
  url: ...
domain: ...
editorial:
  voice_profile: hsm-hbr-mit-sloan | custom
voice_guard:
  canonical: [...]
  banned: [...]
  min_score: 70
quality_rules:
  content: { ... }
```

Wave 2026-05-20 adicionou bloco `geo_2026.{princeton_playbook_enabled,
schema_authority_stack_enabled, b2a_pilot.*}`.

Wave 2026-05-24 (em desenvolvimento na branch
`feat/geo-seo-knowledge-2026-deep-research`) adiciona
`geo_2026_pos_io.{autogeo_enabled, citation_absorption_tracking, ...}`.

## Regra para trabalhos futuros

> Ao tocar em qualquer lógica sensível a autor/domínio/padrão
> editorial: passe pelo `ClientContext`, **não** hardcode. Se
> precisar de uma constante que varia por cliente, é campo de YAML.

(Citação literal do CLAUDE.md seção "Regra para trabalhos futuros"
da wave 2026-04-19.)

## Clientes ativos

- [[clients/default]] — Brasil GEO, Alexandre Caramaschi.
- [[clients/acme]] — cliente exemplo (smoke test).
- [[clients/herreira]] — joalheria, vertical semijoias.

Template para novos: `config/clients/_template/`. Em backlog.

## Anti-padrões

- Hardcode de qualquer string identitária em código Python.
- Defaults "Alexandre" ou "Brasil GEO" em `models.py:CourseDefinition`
  (removidos na wave 2026-04-29).
- Output em `output/approved/` para cliente `!= default` (sempre
  `output/clients/<id>/`).
