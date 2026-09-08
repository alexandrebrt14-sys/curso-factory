---
name: abertura-direta-sem-distracao-20260908
description: "Toda aula abre com título, subtítulo e parágrafo; sem faça agora, mockup, checkpoint, requer verificação, LGPD; fontes só no rodapé (R1 a R9, pedido do dono)."
type: feedback   # preferência declarada pelo dono: não decai
status: stable
created: 2026-09-08
updated: 2026-09-08
related:
  - abertura-direta-sem-distracao
  - abertura-checker
metadata:
  type: feedback
  created: 2026-09-08
---

Toda página, artigo, aula e capítulo gerado por este repositório começa com H1, subtítulo em
UMA frase e parágrafos diretos ao ponto, sem nada antes nem entre eles (R1). A aula é leitura:
não carrega exercício "faça agora" (R6), "mockup no seu negócio" (R5), card "checkpoint" (R8),
marcador "requer verificação" nem menção à LGPD (R9), botão antes do corpo (R2), percurso
alternativo (R3) nem segunda descrição no topo (R4). As fontes ficam num único bloco no rodapé,
em corpo pequeno, com nome e link (R7). As nove regras estão numeradas em
`DIRETRIZ_EDITORIAL.md` e são garantidas em três níveis: prompts (`draft.md`, `review.md`,
`analyze.md`, `expand.md`, `trail.md`, nos três idiomas), gerador (`page.tsx.j2`,
`markdown_parser.py`, `schema_builder.py`, `draft_to_course.py`, `tsx_generator.py`) e gate
(`src/validators/abertura_checker.py`, chamado por `content_checker.check_content`, pelo
`QualityGate`, pelo orquestrador e por `TsxGenerator.render_page`, que levanta `AberturaError`
e não escreve o arquivo).

Relacionadas: [[abertura-direta-sem-distracao]] (conceito), [[abertura-checker]] (gate),
[[bastidor-fora-da-aula-20260903]], [[geracao-por-aula-e-insumo-correto]],
[[diretriz-editorial-v3-narrativa-sem-cota]].

---

## Contexto

Pedido do Alexandre, dono dos repositórios, em 08/09/2026, literal: "Todas as vezes que pedimos
a escrita de uma página, artigo ou curso, eles criam excesso de conteúdos no início, com muitas
segmentações, muitas metadescrições, muitas possibilidades confusas de navegação. Precisamos
que tudo sempre comece com um título, subtítulo e parágrafos direto ao ponto, que prendam a
atenção do leitor. [...] remover excesso de botões no começo, remover opções diversas de
percursos que confundam o leitor, remover 'mockup no seu negócio' e remover também exercícios
práticos do tipo 'faça agora'. Fontes verificadas também devem estar apenas ao final de cada
conteúdo perto do rodapé, em fontes bem pequenas [...]. Cards do tipo checkpoint também devem
ser evitados. Cards com 'requer verificação' não devem estar explícitos nas escritas das páginas
e nem citações de LGPD. Garanta explicitamente estes ajustes nos algoritmos dos 4 GITs."

O que este repositório emitia, medido no código antes da mudança:

- `src/templates/prompts/*/draft.md` mandava um "H2 3: faça agora" com "Resultado esperado:" e
  "Se travar:", e um "H2 2: como fica no seu negócio"; `review.md` e `analyze.md` cobravam o
  exercício; `content_checker` reprovava aula SEM exercício (`min_exercises_per_lesson: 1`).
- `src/models.py` exigia ao menos um `checkpoint` e três seções por step;
  `markdown_parser.parse_module_to_sections` fabricava o checkpoint sintético ("Verifique seu
  entendimento...") e enchia com "Reflita sobre como aplicar este conteúdo" para chegar a três.
- `src/templates/page.tsx.j2` desenhava, antes do corpo: rótulo antes do H1, barra de
  estatísticas (tempo, módulos, nível, tags), barra de progresso fixa, índice lateral de
  módulos com card de pré-requisitos e o card "O que você vai aprender" repetindo a
  descrição. Desenhava o card "Checkpoint" e a linha "Fonte:" dentro de tabela e painel.

## Decisão

1. **Doutrina.** Seção "Abertura e distração (R1 a R9)" em `DIRETRIZ_EDITORIAL.md`,
   `CLAUDE.md`, `AGENTS.md`, `GEMINI.md`, `docs/DOUTRINA_VISUAL_CURSOS.md`,
   `docs/GOVERNANCA_PUBLICACAO_CURSO.md` e nota de precedência em
   `docs/GEO_REDACAO_CHECKLIST_2026.md`. Onde a fonte de estilo (molde D) ainda pede o
   exercício por aula, a regra nova vence e o ponteiro registra a divergência.
2. **Prompts.** O molde da aula passa a ser: subtítulo em uma frase, dois ou três parágrafos de
   abertura, H2 "por que a ideia muda o resultado", H2 com o caso do ramo nomeado, fecho em
   prosa com o próximo passo. Lista R1 a R9 carimbada em `draft.md`; `review.md` remove os
   blocos sem substituto; `analyze.md` os aponta e reprova; `trail.md` mantém "Fontes" como
   último H2, uma linha curta por fonte; `expand.md`, `classify.md`, `research.md` e
   `humanize.md` deixam de pedir exercício. Nos três idiomas.
3. **Gerador.** `SectionType.CHECKPOINT` sai do vocabulário (modelo e schema); o parser descarta
   `> CHECKPOINT:`, `> EXERCÍCIO:`, `> FAÇA AGORA:` e afins, não fabrica mais seção; o subtítulo
   vira `description` do step (`extrair_subtitulo`); a seção `## Fontes` da trilha e o `source`
   de tabela e painel são hasteados para `CourseDefinition.fontes` e desenhados uma vez no
   rodapé, em `0.8rem`, com URL virando link. O template abre com H1, subtítulo e parágrafo, e
   perde rótulo pré-H1, barra de estatísticas, barra de progresso, índice lateral, card de
   pré-requisitos (vira uma linha no rodapé) e card "o que você vai aprender".
4. **Gate.** `src/validators/abertura_checker.py` mede R1, R3, R5, R6, R7, R8 e R9 no Markdown
   (categoria `abertura`, erro bloqueante, aula e trilha) e `check_abertura_definicao` mede o
   curso montado; `TsxGenerator.render_page` levanta `AberturaError` e não escreve o arquivo.
   R2 e R4 são cobradas no template por teste. `min_exercises_per_lesson` vai a zero.
   `config/quality_rules.yaml > validation.abertura` pode acrescentar termos, nunca remover.
5. **Dados.** `config/courses.yaml` perde "LGPD" em títulos e descrições de módulo (vira
   "proteção de dados", com a conduta no lugar do nome da lei), porque título de módulo é texto
   de leitura e R9 o reprovaria.

## O que muda para quem opera

- Aula antiga com "## Faça agora" ou "> CHECKPOINT:" reprova em `python cli.py validate` e não
  vira TSX. O conserto é apagar o bloco e levar o passo prático para o fecho, em prosa.
- Curso que menciona LGPD por nome reprova. A conduta ("peça autorização antes da primeira
  mensagem") entra; o nome da lei, não.
- Fonte que vivia num "Fonte:" abaixo da tabela aparece no rodapé da página; nada se perde.

## Linha do tempo (append-only, ordem reversa)

- **2026-09-08** — [criação] pedido do dono aplicado nos três níveis (doutrina, gerador, gate),
  com `tests/test_abertura_sem_distracao.py` e ajuste dos testes que exigiam checkpoint e
  exercício (`test_regua_aula`, `test_parsers`, `test_parser_blocos_visuais`,
  `test_models_blocos_visuais`, `test_template_blocos_visuais`, `test_visual_density`,
  `test_agentic`, fixture `sample_course.json`).
