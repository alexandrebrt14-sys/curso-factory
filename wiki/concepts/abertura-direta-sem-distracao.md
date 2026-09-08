---
name: abertura-direta-sem-distracao
type: concept
category: editorial
status: stable
created: 2026-09-08
updated: 2026-09-08
status_merge: "PR #83 mergeado em e55f5a9 (08/09/2026); fonte 1.6.0 ressincronizada"
related:
  - abertura-checker
  - content-checker
  - quality-gate-5-camadas
  - padrao-editorial-hsm-hbr
  - abertura-direta-sem-distracao-20260908
---

# Abertura direta e sem distração (R1 a R9)

Princípio editorial e de renderização que governa toda página, artigo, aula e capítulo
gerado por este repositório desde 08/09/2026: **título, subtítulo em uma frase e parágrafos
diretos ao ponto; leitura linear; fontes pequenas no rodapé; verificação é bastidor.** Nasce
do pedido do dono (ver [[abertura-direta-sem-distracao-20260908]]) e é cobrado em três níveis:
prompts, gerador e gate ([[abertura-checker]]). Versão longa, com exemplos antes/depois e
tabela de rastreabilidade completa, na wiki do GitHub:
https://github.com/alexandrebrt14-sys/curso-factory/wiki/Abertura-direta-e-sem-distracao-R1-R9

## O problema que corrige

Antes de 08/09/2026 a página gerada abria com rótulo acima do H1, barra de estatísticas,
barra de progresso fixa, índice lateral de módulos, card de pré-requisitos e um card "O que
você vai aprender" repetindo a descrição. Dentro de cada módulo havia o card "Checkpoint"
(fabricado pelo parser quando o autor não escrevia), o H2 "faça agora" com exercício, o H2
"como fica no seu negócio", e "Fonte:" desenhado dentro de tabelas e painéis. Marcadores de
verificação e a sigla da lei de dados chegavam ao texto de leitura. Nada disso era defeito de
um curso: era o gerador.

## As nove regras

| # | Regra | Proibido | Permitido |
|---|---|---|---|
| R1 | Abertura mínima | qualquer coisa entre H1, subtítulo e primeiro parágrafo (botão, metadado, resumo, índice, card, "para quem é") | subtítulo em linha própria; dois ou três parágrafos; depois H2 |
| R2 | Sem CTA no início | botão ou convite antes do corpo | um botão por módulo, após a leitura; CTAs no fim |
| R3 | Um percurso | "escolha seu caminho", "se você é X vá para Y", abas por perfil, índice lateral | módulos na ordem; ponte para a próxima aula no fecho |
| R4 | Uma descrição | resumo repetido em card | `description` uma vez, no hero |
| R5 | Sem mockup | "mockup", "maquete", seção "no seu negócio" | prosa sobre o negócio do leitor; H2 que nomeia o caso |
| R6 | Sem exercício | "faça agora", "exercício", "mão na massa", "sua vez", "pratique", "tarefa", "desafio", "Resultado esperado:", "Se travar:" | próximo passo em prosa no fecho |
| R7 | Fontes no rodapé | "Fonte:" na aula; fonte em card, callout, tabela; comentário longo | bloco único "Fontes" ao fim, `0.8rem`, nome e link, uma linha; citação parentética inline |
| R8 | Sem checkpoint | "checkpoint", "recapitulando", "resumo do capítulo", "você aprendeu", "quiz", "o que você vai aprender" | `> DICA:` e `> AVISO:` |
| R9 | Sem verificação exposta, sem LGPD | "requer verificação", "a verificar", "[verificar]", "fonte pendente", `[FALTA EVIDÊNCIA:` no publicado; LGPD / Lei 13.709 em qualquer linha, mesmo entre aspas | conduta de proteção de dados em prosa, sem nomear a lei |

Antes e depois, em uma aula:

```markdown
# Aula 1.1: Responder em cinco minutos          # Aula 1.1: Responder em cinco minutos

## O que você vai aprender                       Você vai responder o cliente antes que ele desista.
- Por que a demora custa a venda
                                                 A mensagem que fica meia hora sem resposta vira
## Como fica no seu negócio                      orçamento no concorrente. [...]
...
## Faça agora                                    ## Como a oficina do Sérgio parou de perder orçamento
1. Abra o WhatsApp...                            [...] Abra o WhatsApp e anote o horário da próxima
**Resultado esperado:** ...                      mensagem sem resposta.
> CHECKPOINT: revise.
Fonte: IBGE 2025.                                (fonte no rodapé da trilha, "## Fontes", última seção)
```

## Onde cada regra mora (mapa do código)

| Bloco proibido | Quem o emitia | O que mudou em 08/09/2026 |
|---|---|---|
| Exercício "faça agora" (R6) | `src/templates/prompts/{pt-br,en,es}/draft.md` e raiz ("H2 3: faça agora"); `review.md`, `analyze.md`, `expand.md` cobravam; `Orchestrator._plan_lessons`; `content_checker` reprovava aula SEM exercício (`min_exercises_per_lesson: 1`) | molde novo (subtítulo, parágrafos, H2 "por que", H2 com o caso nomeado, fecho em prosa) e lista R1–R9 carimbada nos três idiomas; `min_exercises_per_lesson: 0` |
| "Como fica no seu negócio" (R5) | `draft.md` H2 2 | H2 2 nomeia o caso |
| Card checkpoint (R8) | `src/models.py` (`SectionType.CHECKPOINT`; `StepDefinition` exigia ≥1 checkpoint e ≥3 seções); `markdown_parser.parse_module_to_sections` fabricava o checkpoint sintético e enchia com `tip`; `page.tsx.j2` `case "checkpoint"`; `course.schema.json` | enum sem `checkpoint`; ≥1 seção; parser descarta `> CHECKPOINT:` e afins e não fabrica nada; `case` removido |
| Topo carregado (R1–R4) | `page.tsx.j2`: `sf-label` antes do H1, "Stats row", barra `sticky`, `<aside>`/`<nav>` de módulos, card "Pré-requisitos", card "O que você vai aprender", chip de duração | hero = H1 → `descricao_curta` (subtítulo) → `descricao` uma vez; coluna única; pré-requisitos em uma linha `0.8rem` no rodapé; progresso ao fim do módulo |
| Fonte no card (R7) | `BlockFootnote` desenhava `Fonte: {source}` em `DataTableBlock` e `StatGridBlock`; trilha escrevia `## Fontes` que virava seção de step | `tsx_generator._fontes_do_curso` hasteia `data.source` e `CourseDefinition.fontes`; `markdown_parser.extrair_fontes`; bloco único `<section aria-label="Fontes">` após o FAQ, `text-[0.8rem]`, filtro `fonte_jsx` (URL vira link) |
| Subtítulo ausente (R1) | `description` do step era a primeira linha cortada em 120 caracteres | `markdown_parser.extrair_subtitulo`; `schema_builder._build_step` e `draft_to_course._build_steps` a usam como `description` e a tiram do corpo (R4) |
| Verificação e LGPD (R9) | `config/courses.yaml` com LGPD em títulos de módulo; só "de acordo com a LGPD" era muleta legal no prompt | títulos reescritos ("proteção de dados"); R9 explícito; `check_abertura_definicao` barra `[FALTA EVIDÊNCIA:` no publicado |

## Conflitos com a doutrina anterior

- Molde D da fonte de estilo e `draft.md` pediam um exercício por aula e o gate reprovava a
  aula sem ele → zero exercício (R6); precedência registrada em `DIRETRIZ_EDITORIAL.md` até a
  fonte ser regerada (escrita-empreendedor 1.6.0, PR #9, sha256
  `2fc0817a84c052e2931bfab470c822cd72b24e33ab2204d0db85433e1435c55d`).
- `StepDefinition` exigia checkpoint e três seções; o parser fabricava os dois → removidos (R8).
- Doutrina visual e `docs/GEO_REDACAO_CHECKLIST_2026.md` admitiam fonte dentro do bloco e
  citação em card → fonte só no rodapé; citação de especialista vira prosa (R7).
- Testes invertidos: `test_regua_aula` (sem exercício passa; com exercício reprova por R5/R6),
  `test_parsers`, `test_parser_blocos_visuais`, `test_models_blocos_visuais`,
  `test_template_blocos_visuais`, `test_visual_density`, `test_agentic`, dublês de
  `test_orchestrator_aulas` e `test_expansao_de_aula_curta`, fixture `sample_course.json`.

## Estado (08/09/2026)

- PR [#83](https://github.com/alexandrebrt14-sys/curso-factory/pull/83) **mergeado** por squash na
  `main` em `e55f5a9` (08/09/2026); suíte na `main`: 487 verdes, `ruff` limpo.
- Fonte de estilo 1.6.0 (escrita-empreendedor PR #9, merge `9d7c341`, sha256
  `2fc0817a84c052e2931bfab470c822cd72b24e33ab2204d0db85433e1435c55d`) **ressincronizada**:
  ponteiros `DIRETRIZ_EDITORIAL.md` e `GUIA_ESCRITA_HUMANIZADA.md` no hash novo,
  `config/lexicos.json` regerado (bloco `aberturaEDistracao`; jargão sem a sigla da lei;
  `tetos.D` igual). O [[abertura-checker]] passou a somar as famílias da fonte aos padrões
  próprios e a ler `subtituloMaxPalavras` (25) para R1. Verificação:
  `python -m escrita.sincronizar verificar DIRETRIZ_EDITORIAL.md` devolve "ponteiro sincronizado".

## Propagação

A cada nova versão da fonte: `python -m escrita.sincronizar verificar DIRETRIZ_EDITORIAL.md`
(e o GUIA), atualizar `hash-fonte`/`sincronizado-em` nos dois ponteiros e
`python -m escrita.cli lexicos --json > config/lexicos.json`. Os padrões próprios do
[[abertura-checker]] continuam existindo como piso quando o espelho não traz o bloco.

## Checklist para quem escreve

1. Primeira linha depois do título: subtítulo, uma frase, linha própria.
2. Dois ou três parágrafos ao ponto antes de qualquer H2, lista, tabela ou card.
3. Um caminho só; nenhum "se você é X".
4. Nenhum "faça agora", "exercício", "Resultado esperado:", "mockup", "no seu negócio" como
   título ou rótulo; o próximo passo em prosa no fecho.
5. Nenhum "checkpoint", "recapitulando", "quiz", "requer verificação"; nunca o nome da lei de dados.
6. Fonte só no rodapé da trilha, uma linha curta com link.
7. `python cli.py validate <arquivo>` sem linha `[abertura]`.

## Cross-references

- [[abertura-checker]]: o validador, como rodar e como estender os léxicos.
- [[content-checker]]: camada 2 do [[quality-gate-5-camadas]], que agora carrega a categoria
  `abertura`.
- [[abertura-direta-sem-distracao-20260908]]: a decisão datada, tipo `feedback`.
- Outros repos da rodada: Escrita-Empresarial #17, escrita-empreendedor #9, Geo-Leadlovers #44.
