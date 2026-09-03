# Wiki Index — curso-factory

> Catálogo navegável da wiki, organizado por categoria. Substitui infra
> RAG até escala moderada. Mantido em ordem alfabética por slug.
>
> Última atualização: 2026-05-26.

## Como usar

- Antes de criar página nova: conferir se já existe.
- Antes de iniciar pesquisa nova ou disparar chamada Perplexity:
  conferir se o tema já está em `concepts/`, `sources/` ou `queries/`.
- Antes de produzir curso novo: conferir `clients/<id>` e `overview/`
  para entender cobertura existente da vertical.

---

## Entities

LLMs do pipeline, validators, autores. Uma página por entidade
referenciada >1 vez.

- [accent-checker](entities/accent-checker.md) — validator. Camada 1
  do quality gate. 300+ mapeamentos PT-BR.
- [claude-reviewer](entities/claude-reviewer.md) — LLM. Etapa 5 do
  pipeline (revisão final).
- [content-checker](entities/content-checker.md) — validator. Camada 2
  do quality gate. 10+ regras editoriais.
- [gpt-4o-writer](entities/gpt-4o-writer.md) — LLM. Etapa 2 do
  pipeline (redação HSM/HBR).
- [perplexity-sonar](entities/perplexity-sonar.md) — LLM. Etapa 1 do
  pipeline (pesquisa).
- [voice-guard](entities/voice-guard.md) — validator. Camada 4 do
  quality gate. Bloqueia naming não-canônico do cliente ativo.

## Concepts

Definições atômicas reusáveis em múltiplos cursos, decisões e clientes.

- [andragogia-knowles](concepts/andragogia-knowles.md) — 6 princípios
  obrigatórios em todo módulo.
- [llm-wiki-karpathy](concepts/llm-wiki-karpathy.md) — padrão
  arquitetural desta wiki.
- [multi-tenant-clientcontext](concepts/multi-tenant-clientcontext.md)
  — arquitetura que tornou a fábrica replicável.
- [padrao-editorial-hsm-hbr](concepts/padrao-editorial-hsm-hbr.md) —
  voz default do cliente Brasil GEO.
- [quality-gate-5-camadas](concepts/quality-gate-5-camadas.md) —
  validação automática antes do approved.
- [taxonomia-bloom](concepts/taxonomia-bloom.md) — verbos aceitos
  (níveis 3-6) e proibidos (1-2) em objetivos de aprendizagem.

## Clients

Uma página por cliente multi-tenant configurado em
`config/clients/<id>/client.yaml`.

- [acme](clients/acme.md) — cliente exemplo de teste.
- [default](clients/default.md) — Brasil GEO (Alexandre Caramaschi).
  Cliente canônico.
- [herreira](clients/herreira.md) — joalheria. Vertical: semijoias.

## Courses

Uma página por curso aprovado em `output/approved/` (cliente default)
ou `output/clients/<id>/approved/` (outros clientes). Populado
automaticamente por `python scripts/wiki/sync-courses.py`.

- [introducao-as-semijoias](courses/introducao-as-semijoias.md) —
  vertical semijoias. Cliente [[clients/herreira]]. Página criada
  automaticamente pelo sync em 26-05-2026 (cheque do lint descobriu
  curso aprovado sem wiki).
- [seo-geo-para-dentistas](courses/seo-geo-para-dentistas.md) —
  vertical saúde. Cliente [[clients/default]]. Seed manual em
  26-05-2026.

## Queries

Q&A pré-sintetizado de decisões recorrentes. Cada query respondida
via wiki que valha repetir vira página aqui.

- [qual-nivel-bloom-usar-em-objetivo](queries/qual-nivel-bloom-usar-em-objetivo.md)
  — quando aceitar verbo nível 2 ("descrever") vs forçar nível 3+.

## Overview

Mapas de domínio: cobertura por vertical, gaps, sobreposições.

- [topologia-cobertura-cursos](overview/topologia-cobertura-cursos.md)
  — estado da cobertura: 1 aprovado, 18 drafts, 12 convertidos órfãos.

## Decisions

ADRs.

- [ADR-001-adopcao-llm-wiki](decisions/ADR-001-adopcao-llm-wiki.md) —
  adoção do padrão Karpathy em 2026-05-26.
- [ADR-002-sync-automatico-courses-wiki](decisions/ADR-002-sync-automatico-courses-wiki.md)
  — sync `output/approved/` → `wiki/courses/` como hook pós-aprovação.

## Sources

Uma página por fonte externa ou dossiê interno referenciado >1 vez.

- [2026-04-03-karpathy-llm-wiki-gist](sources/2026-04-03-karpathy-llm-wiki-gist.md)
  — gist original. Fonte canônica desta camada.
- [aggarwal-kdd-2024](sources/aggarwal-kdd-2024.md) — paper fundador
  GEO (arXiv:2311.09735). Princeton checklist (+115% Cite Sources,
  +41% Statistics, +28% Quotation).
- [autogeo-iclr-26](sources/autogeo-iclr-26.md) — Wu/Zhong/Kim/Xiong
  CMU ICLR'26 (+50,99% lift). Obrigatório em prompt do writer.py.

## Reviews

- [2026-05-26-baseline](reviews/2026-05-26-baseline.md) — estado
  inicial do grafo na inauguração.

---

## Backlog explícito de páginas pendentes

Cross-links presentes em páginas existentes apontando para slugs ainda
não criados. Cada onda fecha 1+ ou justifica.

- `[[entities/gemini-analyzer]]`
- `[[entities/groq-classifier]]`
- `[[entities/link-checker]]`
- `[[entities/html-validator]]`
- `[[entities/alexandre-caramaschi]]`
- `[[entities/brasil-geo]]`
- `[[concepts/finops-budget-guard]]`
- `[[concepts/circuit-breaker-fallback]]`
- `[[concepts/principio-mestre-vs-tatica]]`
- `[[concepts/two-phase-json-ld]]`
- `[[concepts/princeton-geo-playbook]]`
- `[[concepts/anti-padrao-clich-ai]]`
- `[[concepts/error-compounding]]`
- `[[concepts/humanizacao-ai-detection]]`
- `[[sources/geo-knowledge-base-2026-v2]]`
- `[[sources/seo-geo-increment-20260520]]`
- `[[sources/wave-maio-posio-2026]]`
- `[[decisions/ADR-003-prompts-externos-vs-inline]]`
- `[[decisions/ADR-004-jinja2-vs-heredocs]]`
- `[[decisions/ADR-005-providers-yaml-vs-hardcode]]`
- `[[clients/_template]]`
- `[[overview/cobertura-por-vertical]]`
- `[[overview/gaps-criticos-q3-2026]]`
- [Bastidor fora da aula, lei como fato, forma livre (03/09/2026)](decisions/bastidor-fora-da-aula-20260903.md)
