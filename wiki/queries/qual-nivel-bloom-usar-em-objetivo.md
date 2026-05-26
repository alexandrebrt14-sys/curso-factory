---
name: qual-nivel-bloom-usar-em-objetivo
type: query
status: stable
created: 2026-05-26
updated: 2026-05-26
asked_count: 3
related:
  - taxonomia-bloom
  - andragogia-knowles
  - content-checker
---

# Query: Qual nível Bloom usar em objetivo de aprendizagem?

Pergunta recorrente ao desenhar módulo novo. Sintetizada como página
para evitar re-pesquisa.

## Pergunta

Quando aceitar verbo nível 2 ("descrever", "compreender", "saber")
em objetivo de aprendizagem, vs forçar nível 3+ ("aplicar",
"analisar", "avaliar")?

## Resposta canônica

**Default: rejeitar nível 1-2.** Cursos da `curso-factory` são para
profissionais autônomos ([[andragogia-knowles]] princípio 2). Objetivo
declarativo ("saber o que é GEO") não é auditável e viola padrão
HBR-grade.

**Exceções aceitáveis (com escopo):**

1. **Objetivo secundário pré-requisito** que será imediatamente
   superado por objetivo principal nível 3+.
   - Exemplo OK: "Descrever os 3 componentes de Schema.org Course
     (objetivo secundário); aplicar Schema.org Course em landing page
     real (objetivo principal)."
2. **Verbo nível 2 composto** que evolui para 3+ na frase.
   - Exemplo OK: "Descrever **como diagnosticar** gaps de GEO em
     portal editorial."
3. **Domínio onde nível 2 é o limite** (raro). Ex: módulo de
   regulação YMYL onde o objetivo é literalmente conhecer uma
   resolução do conselho de classe, sem espaço para operação. Aceito
   com nota explícita no módulo.

## Decisões implementadas

- [[entities/content-checker]] cheque 7 rejeita verbos 1-2 no campo
  `objetivos`. Bloqueia aprovação.
- Prompt externo do [[entities/gpt-4o-writer]] traz tabela explícita
  na seção "Objetivos de aprendizagem — verbos aceitos e proibidos".
- [[entities/claude-reviewer]] (etapa 5) revisa fronteiros (verbo 2
  composto) caso a caso.

## Anti-padrões observados em produção

- "Compreender SEO": rejeitado, vira "Diagnosticar gaps de SEO em
  portal".
- "Entender o que é AI Overview": rejeitado, vira "Estruturar
  conteúdo para citação em AI Overview".
- "Conhecer os 5 LLMs do pipeline": rejeitado para curso público;
  aceito apenas em README interno da curso-factory.

## Quantas vezes essa pergunta foi feita

Campo `asked_count` no frontmatter rastreia. Atual: 3 vezes em
produção de cursos diferentes (semijoias, dentistas, advogados).
Cada nova ocorrência incrementa; threshold para promover a
página em `wiki/concepts/` dedicada: `asked_count >= 5`.

## Cross-references

- [[concepts/taxonomia-bloom]] — definição canônica completa dos 6
  níveis com tabela de verbos.
- [[concepts/andragogia-knowles]] — princípios que justificam a
  política.
- [[entities/content-checker]] — validador que opera a política.
