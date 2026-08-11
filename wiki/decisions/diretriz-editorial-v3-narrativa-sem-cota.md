---
name: diretriz-editorial-v3-narrativa-sem-cota
description: "Por que a v3 da diretriz editorial proibiu cota mecânica de ritmo e tornou storytelling obrigatório; qual era o defeito que derrubou a qualidade do conteúdo gerado entre julho e agosto de 2026."
metadata:
  type: mistake
  created: 2026-08-11
---

A qualidade do texto produzido pelo pipeline caiu porque as regras de escrita eram
mecânicas e se contradiziam entre camadas. Três defeitos, todos corrigidos na
`DIRETRIZ_EDITORIAL.md` v3 (11/08/2026):

1. **Cota de ritmo.** `draft.md` e `humanize.md` exigiam "uma frase de 6 palavras ou
   menos em CADA parágrafo" e "nunca duas frases consecutivas na mesma faixa de
   comprimento". O `humanizer.py` reforçava isso reescrevendo em loop até subir o
   score de burstiness, e o `stylometry_checker.py` avisava quando faltava frase
   curta. O resultado foi staccato de manchete: melhora a métrica, piora a leitura,
   e continua sendo identificado como texto de máquina (Tabach, arXiv:2604.23471).
   A métrica agora é diagnóstico do texto pronto, nunca fórmula de produção.
2. **Cota de formatação.** "Parágrafo com no máximo 5 linhas", "sub-heading a cada
   2-3 parágrafos" e "nunca mais de 3 parágrafos sem elemento visual" fatiavam o
   raciocínio antes de ele terminar. A v3 mantém tabela, matriz de decisão e
   checklist como ferramentas obrigatórias quando há comparação, escolha ou passo
   verificável, e devolve à prosa o trabalho de carregar raciocínio.
3. **Ausência de narrativa e camadas divergentes.** Nenhum prompt pedia técnica de
   engajamento, e o `CLAUDE.md` acumulava três blocos editoriais sobrepostos com
   regras diferentes. A v3 instala a seção 3 (abertura em situação, tensão antes da
   solução, caso condutor, promessa cumprida, fechamento com callback, mostrar em
   vez de qualificar) e passa a ser fonte única, com prompts e resumos subordinados.

Regra prática ao mexer em prompt de escrita neste repo: toda instrução de estilo
precisa poder ser cumprida por um bom escritor humano sem contar palavras. Se a
instrução vira aritmética durante a escrita, ela vira cacoete no texto.

Relacionadas: [[padrao-editorial-hsm-hbr]], [[ADR-001-adopcao-llm-wiki]].

---

## Linha do tempo (append-only, ordem reversa)

- **2026-08-11** — [correção] v3 da diretriz: storytelling obrigatório (§3), veto a
  cota mecânica de ritmo (§4.7), estrutura visual reposicionada a serviço da decisão
  (§6). Propagado para `draft.md`, `review.md` e `humanize.md` (pt-br, raiz, en, es),
  `humanizer.py`, `stylometry_checker.py`, `content_checker.py` (teto de parágrafo de
  5 para 8 linhas), `voice_guard.py`, `quality_rules.yaml`, `CLAUDE.md`, `AGENTS.md`
  e `GEMINI.md`. Origem: curador reportou queda de qualidade nos conteúdos gerados.
- **2026-07-23** — [criação] v2 da diretriz e anexo `GUIA_ESCRITA_HUMANIZADA.md`
  (PRs #59 e #60), com pesquisa de junho e julho de 2026 sobre marcadores de texto
  sintético. A v2 já tratava estrutura, mas não revogou as cotas dos prompts nem
  cobria narrativa, e foi sob ela que a queda de qualidade apareceu.
