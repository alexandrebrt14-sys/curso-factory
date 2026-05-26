---
name: claude-reviewer
type: entity
category: llm-pipeline
status: stable
created: 2026-05-26
updated: 2026-05-26
related:
  - gpt-4o-writer
  - accent-checker
  - voice-guard
  - quality-gate-5-camadas
---

# Claude Opus (etapa 5: review)

LLM da etapa **5 — REVIEW** do pipeline. Modelo canônico:
`claude-opus-4-6`. Revisor final com **correção ativa**: acentuação
PT-BR completa, qualidade editorial, formatação. Última camada antes
do quality gate programático.

## Papel canônico

- Revisão crítica de cada módulo após análise do Gemini e
  classificação do Groq.
- Correção ativa de acentuação PT-BR (complementa
  [[accent-checker]] que roda depois).
- Validação fina contra anti-padrões editoriais (lista 18 clichês
  proibidos, em-dash banido, superlativos sem evidência).
- Aplicação de Anti-padrões §13 da wave 2026-05-20: `llms.txt` não é
  requisito; schema não é silver bullet; GEO ≠ substituto de SEO.

## Budget guard

- **Máximo $5 por curso** em chamadas Claude (camada 5 do
  [[quality-gate-5-camadas]]).
- Total do curso (5 LLMs somados): **$10 max**.
- Excede budget → pipeline aborta com erro em `cost_tracker.py`.

## Prompt externo

`src/templates/prompts/review.md`. Inclui checklist exaustivo de
acentuação (150+ palavras obrigatórias) e regras anti-clichê.

## Por que este LLM

- Melhor em instruções complexas e revisão crítica (vs GPT-4o e
  Gemini).
- Acentuação PT-BR mais consistente em produção do que GPT-4o em
  testes internos.
- Suporte a `extended-thinking` para casos de revisão profunda
  (cursos sensíveis YMYL).

## Anti-padrões

- Usar `claude-opus` para etapas anteriores (research, draft,
  analyze, classify): viola separação de papéis e estoura budget.
- Aceitar saída com em-dash em copy editorial (regra do
  [[padrao-editorial-hsm-hbr]]).
- Pular review em cursos "simples": review é parte do contrato de
  qualidade, não opcional.

## Versão futura

Considerar upgrade para `claude-opus-4-7` quando estabilizar latência.
Decisão pendente em backlog.
