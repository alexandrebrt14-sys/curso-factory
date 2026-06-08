---
name: perplexity-sonar
type: entity
category: llm-pipeline
status: stable
created: 2026-05-26
updated: 2026-05-26
sources:
  - 2026-04-03-karpathy-llm-wiki-gist
related:
  - gpt-4o-writer
  - quality-gate-5-camadas
sameAs:
  - https://docs.perplexity.ai/
---

# Perplexity Sonar (etapa 1: research)

LLM da etapa **1 — RESEARCH** do pipeline da `curso-factory`. Modelo
canônico: `sonar-pro` (alternativa: `sonar-deep-research` para waves
canônicas trimestrais). Único LLM do pipeline com acesso a web em
tempo real e citações verificáveis.

## Papel canônico

- Coletar dados atualizados, fontes primárias e tendências do período
  para o tema do curso solicitado.
- Fundamentação acadêmica: prioridade para papers arXiv 2025-2026,
  estudos peer-reviewed, comunicados oficiais (Google, OpenAI,
  Anthropic).
- Análise competitiva: mapeamento de cursos/conteúdos existentes na
  vertical.
- Saída: dossiê markdown em `output/drafts/<slug>_<timestamp>.json`
  campo `research` com lista de URLs verificáveis.

## Configuração no `providers.yaml`

- Provider: `perplexity`.
- Modelo default: `sonar-pro`.
- Endpoint: `https://api.perplexity.ai/chat/completions`.
- Fallback (em falha): Gemini com prompt de pesquisa adaptado (perde
  acesso a web; vira síntese paramétrica). Detalhes em
  [[concepts/circuit-breaker-fallback]].

## Por que este LLM

- Único LLM acessível com web real-time e citações primárias em PT-BR
  confiáveis em maio/2026.
- Custo por chamada baixo vs alternativas com browsing (GPT-4o web
  search é mais caro e tem latência maior).
- Suporte a `search_recency` (week/month/year) e domínios filtrados.

## Anti-padrões

- Aceitar URL ou DOI confabulado sem spot-check. Risco real:
  Perplexity ocasionalmente cita URL 404 ou inventa DOI. Mitigação:
  WebFetch das 3-5 fontes principais antes de aprovar o dossiê.
- Usar `sonar-pro` para tarefa que exige browsing profundo
  (decomposição de tese complexa): subir para `sonar-deep-research`
  apesar do custo 10-20x maior.
- Repetir chamada para mesmo curso quando cache disponível. Cache
  obrigatório (TTL 24h via [[concepts/quality-gate-5-camadas]]).

## Histórico

- Adotado desde versão inicial do pipeline.
- Wave 2026-04-25 adicionou catálogo de 25+ papers em
  `docs/knowledge/geo-aeo/50-fontes-e-links.md` como "fontes-âncora
  aceitas" — toda afirmação factual deve casar com pelo menos um
  paper do catálogo.
