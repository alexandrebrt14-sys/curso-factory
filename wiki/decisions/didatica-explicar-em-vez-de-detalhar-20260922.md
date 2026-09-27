---
name: didatica-explicar-em-vez-de-detalhar-20260922
description: "A régua de forma aprovava aula que o aluno abandona: o defeito está entre os parágrafos e nas superfícies ao redor (ficha, título, subtítulo, costura, fecho); o gate de didática mede isso e os prompts pedem explicação em vez de minúcia."
metadata:
  type: feedback
  created: 2026-09-22
---

Régua de tamanho é teto, nunca alvo. A aula troca minúcia por explicação sem inchar: glosa de
cada termo com analogia do cotidiano na primeira aparição (molde "spring: jeito de animar que
imita uma mola"), frases ligadas em raciocínio (o que é, por que importa para o negócio, o que
fazer), corte da enxurrada de versão, exemplo do negócio pequeno amarrado aos passos e fecho com
verbo no imperativo e critério de acerto. O que fica ao redor da prosa (ficha, dica, caso,
legenda, título, subtítulo, passagem entre aulas) sai no mesmo registro da aula. Medição e
regras em `docs/ESPECIFICACAO_DIDATICA_20260922.md`; gate em
`src/validators/didatica_checker.py` (categoria `didatica`, quase tudo aviso); números em
`config/quality_rules.yaml > validation.didatica`. Norma de origem: DIRETRIZ §18 do
`Escrita-Empresarial` (0.3.0).

Relacionadas: [[abertura-direta-sem-distracao-20260908]],
[[diretriz-editorial-v3-narrativa-sem-cota]], [[geracao-por-aula-e-insumo-correto]].

---

## Linha do tempo (append-only, ordem reversa)

- **2026-09-27**: [evolução] o exemplo deixa de ser contado inteiro: fica curto e percorre os
  passos do procedimento ([[guia-aplicavel-e-fonte-recente-20260927]]).
- **2026-09-22** — [criação] pedido do dono depois de auditar as superfícies que a bateria de
  reescrita não toca. Medido: 61 de 61 descrições do curso de frontends começando com "Você
  sai", 35 de 61 títulos sem verbo, 43% dos parágrafos abrindo com artigo, 94 pares vizinhos
  com a mesma primeira palavra, 146 fichas com 0,28 "você" por mil palavras e 11 conferências
  de fuga; no Portal Leadlovers, 183 pares em 2.207 parágrafos, 45% dos parágrafos abaixo de
  20 palavras e nenhum fecho com imperativo e critério. Nenhum verificador da casa media nada
  disso. Entraram o `didatica_checker`, a seção `didatica` do YAML, a linha `TÍTULO:` no
  orquestrador e as regras nos prompts de redação, revisão, trilha e análise.
