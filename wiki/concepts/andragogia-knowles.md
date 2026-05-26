---
name: andragogia-knowles
type: concept
category: editorial-pedagogy
status: stable
created: 2026-05-26
updated: 2026-05-26
related:
  - taxonomia-bloom
  - padrao-editorial-hsm-hbr
  - content-checker
  - gpt-4o-writer
---

# Andragogia (6 princípios de Knowles)

Conceito obrigatório em todo módulo gerado pela `curso-factory` para o
cliente `default` e clientes que herdam o padrão editorial canônico.
Codificado no prompt externo do [[gpt-4o-writer]] e validado
programaticamente por [[content-checker]] (camada 2 do
[[quality-gate-5-camadas]]).

## Os 6 princípios

1. **Necessidade de saber** — POR QUE antes do COMO. Cada módulo abre
   explicando por que o conteúdo importa para o profissional, antes de
   ensinar a operação.
2. **Autoconceito** — tratar o aluno como profissional autônomo, nunca
   condescendente. Sem "agora você vai aprender" ou "vamos descobrir
   juntos".
3. **Experiência prévia** — conectar com vivências profissionais
   reais. Exemplos do dia a dia do nicho (joalheria, fintech,
   jurídico, saúde, educação).
4. **Prontidão** — aplicabilidade imediata no trabalho. Exercícios
   devem ser situáveis em contexto profissional, não abstratos.
5. **Orientação a problemas** — problemas reais, não taxonomias
   acadêmicas. Estrutura de módulo: problema → análise → solução
   aplicável.
6. **Motivação intrínseca** — crescimento profissional e domínio,
   não medo ou obrigação. Sem ameaça competitiva ("se você não
   aprender isso ficará para trás").

## Aplicação no pipeline

- **Etapa 2 (DRAFT, [[gpt-4o-writer]])**: prompt externo
  `src/templates/prompts/draft.md` lista os 6 princípios como
  checklist obrigatório.
- **Etapa 3 (ANALYZE, Gemini)**: revisa pedagogicamente em 7
  dimensões; uma delas é a presença dos 6 princípios.
- **Camada 2 quality gate**: 5 indicadores programáticos que
  correlacionam com os princípios (POR QUE antes do COMO, conexão
  com experiência prévia, aplicabilidade imediata, etc).

## Anti-padrões

- Estrutura "definição → exemplo → exercício" academicista (viola
  princípio 5).
- Tom condescendente ("muitos profissionais ainda não sabem que...")
  (viola princípio 2).
- Exercícios desconexos do nicho do cliente (viola princípio 3 e 4).
- Ameaça competitiva como motivador (viola princípio 6).

## Fonte primária

Knowles, M. S. (1980). *The Modern Practice of Adult Education: From
Pedagogy to Andragogy*. Revised edition. New York: Cambridge Books.

Atualização canônica: Knowles, M. S., Holton III, E. F., & Swanson,
R. A. (2014). *The Adult Learner: The Definitive Classic in Adult
Education and Human Resource Development* (8th ed.). Routledge.

Adoção no padrão editorial Brasil GEO veio via wave 2026-04-19
(refactor multi-tenant) — antes era implícito, virou explícito no
prompt externo.
