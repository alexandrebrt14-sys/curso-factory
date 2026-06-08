---
name: gpt-4o-writer
type: entity
category: llm-pipeline
status: stable
created: 2026-05-26
updated: 2026-05-26
related:
  - perplexity-sonar
  - claude-reviewer
  - padrao-editorial-hsm-hbr
  - andragogia-knowles
  - taxonomia-bloom
---

# GPT-4o (etapa 2: draft)

LLM da etapa **2 — DRAFT** do pipeline. Modelo: `gpt-4o`. Redator
principal dos módulos do curso. Recebe o dossiê da Perplexity e
produz o conteúdo no padrão editorial [[padrao-editorial-hsm-hbr]]
com [[andragogia-knowles]] e [[taxonomia-bloom]].

## Papel canônico

- Redigir módulos de 2.500-4.000 palavras cada.
- Aplicar 6 princípios de Knowles em cada módulo.
- Usar verbos Bloom nível 3-6 nos objetivos de aprendizagem.
- Formatar: 1+ tabela comparativa, 3+ exercícios com contexto
  profissional, blockquotes para insights centrais.
- Padrão editorial HSM/HBR/MIT Sloan (para cliente `default`).

## Prompt externo

`src/templates/prompts/draft.md` (~150 linhas). Modificar este
arquivo altera comportamento do writer sem mexer em código Python.
Versões i18n em `src/templates/prompts/{pt-br,en,es}/draft.md`.

## Wave 2026-05-20 — Princeton GEO checklist obrigatória

Para cursos sobre temas GEO/SEO, prompt do writer inclui obrigatórias:

- **Cite Sources ≥3** outbound (Aggarwal KDD 2024 +115% lift).
  Detalhes em [[sources/aggarwal-kdd-2024]].
- **Statistics ≥5** com fonte+ano (+41% lift).
- **Quotes ≥1** atribuída (+28% lift).
- **AutoGEO 5 regras** (Wu/Zhong/Kim/Xiong CMU ICLR'26 +50,99%
  lift). Detalhes em [[sources/autogeo-iclr-26]].

## Por que este LLM

- Melhor redator longo em PT-BR (consistência de tom, manutenção de
  contexto em 4.000 palavras).
- API estável com rate limit confortável.
- Bom em seguir instruções editoriais densas (~150 linhas de prompt).

## Fallback

Em falha (rate limit, timeout, indisponibilidade): `claude-opus`
assume a redação. Comportamento idêntico exceto custo (mais alto) e
levemente diferente em tom.

## Anti-padrões

- **NUNCA** duplicar instruções entre prompt externo e template inline
  em `base.py`. Fonte única é o arquivo `.md`.
- **NUNCA** hardcode credencial Alexandre ou domínio
  `alexandrecaramaschi.com` no prompt — usa `{{ client.author.name }}`
  e `{{ client.domain }}` injetados via [[multi-tenant-clientcontext]].
- Aceitar clichê IA proibido na saída (lista de 18 expressões banidas
  em [[content-checker]]).
