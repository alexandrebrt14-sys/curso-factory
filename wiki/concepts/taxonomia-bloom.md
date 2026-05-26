---
name: taxonomia-bloom
type: concept
category: editorial-pedagogy
status: stable
created: 2026-05-26
updated: 2026-05-26
related:
  - andragogia-knowles
  - content-checker
  - gpt-4o-writer
---

# Taxonomia de Bloom nos objetivos de aprendizagem

Conceito obrigatório em todos objetivos de aprendizagem dos cursos
produzidos pela `curso-factory`. Validado programaticamente em
[[content-checker]] (camada 2 do [[quality-gate-5-camadas]]).

## Verbos aceitos (níveis 3-6)

| Nível | Categoria | Verbos exemplos                              |
|-------|-----------|----------------------------------------------|
| 3     | Aplicar   | aplicar, implementar, executar, operar       |
| 4     | Analisar  | analisar, comparar, diagnosticar, examinar   |
| 5     | Avaliar   | avaliar, justificar, criticar, defender      |
| 6     | Criar     | criar, projetar, formular, planejar, compor  |

## Verbos proibidos (níveis 1-2)

| Nível | Categoria   | Verbos proibidos                             |
|-------|-------------|----------------------------------------------|
| 1     | Lembrar     | lembrar, memorizar, listar, identificar      |
| 2     | Compreender | entender, conhecer, saber, descrever         |

## Por que esta política

Conteúdo HBR-grade para profissionais autônomos exige objetivos que
descrevam **operação no mundo**, não meramente conhecimento
declarativo. "Compreender o que é GEO" não tem como ser auditado;
"diagnosticar gaps de GEO num portal editorial" sim. Alinhado ao
princípio 5 da [[andragogia-knowles]] (orientação a problemas).

## Aplicação no pipeline

- Prompt externo do [[gpt-4o-writer]]
  (`src/templates/prompts/draft.md`) inclui tabela de verbos aceitos
  e proibidos com instrução literal de rejeição.
- [[content-checker]] cheque 7 valida verbos Bloom no campo
  `objetivos` do módulo. Detecta proibido → bloqueia aprovação.
- Etapa 3 (ANALYZE, Gemini) confere e sugere reescrita quando aceito
  é fronteiriço ("descrever" é proibido mas "descrever como
  diagnosticar" pode ser borderline aceitável).

## Decisão recorrente

Q&A canônica em [[queries/qual-nivel-bloom-usar-em-objetivo]] cobre o
caso "quando aceitar verbo nível 2 em objetivo secundário".

## Fonte primária

Anderson, L. W., & Krathwohl, D. R. (Eds.) (2001). *A Taxonomy for
Learning, Teaching, and Assessing: A Revision of Bloom's Taxonomy of
Educational Objectives*. New York: Longman.

Versão original: Bloom, B. S., Engelhart, M. D., Furst, E. J., Hill,
W. H., & Krathwohl, D. R. (1956). *Taxonomy of Educational
Objectives: The Classification of Educational Goals. Handbook I:
Cognitive Domain*. New York: David McKay Company.
