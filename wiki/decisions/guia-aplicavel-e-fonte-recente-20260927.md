---
name: guia-aplicavel-e-fonte-recente-20260927
description: "A aula gerada vira guia de como fazer (passos, verificação, erro comum, decisão, critério de pronto), a história só entra quando carrega o procedimento e todo conceito se apoia em fonte recente e datada; três validadores com números no client.yaml, tudo como aviso."
metadata:
  type: feedback
  created: 2026-09-27
---

A aula é um guia aplicável: a primeira frase diz o que o aluno sai sabendo fazer, o porquê é
curto e apoiado em fonte, o procedimento vem em passos numerados com verbo no imperativo,
verificação e erro comum com conserto, as decisões aparecem como "se isto, faça aquilo" e o
fecho dá o critério de pronto e o próximo passo. O exemplo é curto e percorre os passos;
personagem é opcional e não conduz a aula; caso nomeado obrigatório, cena no H2 do caso e fecho
que volta ao personagem saíram dos prompts, dos fallbacks e das mensagens do gate. Cada
conceito central se apoia em fonte primária com data de publicação, recente em tema que muda
rápido; fonte antiga só como origem do conceito.

| Regra | Configuração | Validador | Severidade |
|---|---|---|---|
| Molde de aula-guia nos prompts | `quality_rules.yaml > validation.guia_aplicavel.esqueleto` e `instrucao_*` | `{bloco_molde_da_aula}` em `draft.md`, `review.md`, `analyze.md`; `instrucao_plano` no planejamento | não se aplica |
| Completude do como fazer, por tipo de aula | pisos e marcadores em `validation.guia_aplicavel`; liga, tipo e severidade no bloco `guia_aplicavel` do `client.yaml` | `guia_aplicavel_checker.py` | aviso |
| Orçamento de narrativa e abertura sem história | marcadores em `validation.orcamento_narrativa`; teto e severidade no bloco `narrativa` | `narrativa_checker.py` | aviso |
| Fonte datada e recente, estado atual com fonte nova | formatos e marcadores em `validation.fontes_recentes`; janela, parcela, teto e data de referência no bloco `fontes_recentes` (cliente ou curso) | `fontes_recentes_checker.py`, coluna "Data de publicação" em `proveniencia.py`, `cli.py fontes-recentes` | aviso |

Valores de partida no cliente default: narrativa até 20% dos parágrafos de prosa; ao menos
metade das fontes com até 12 meses; alegação de estado atual com fonte de até 18 meses; aula
prática com ao menos três passos, todos no imperativo, uma verificação, um erro comum, uma
decisão e o critério de pronto. O `_template` deixa as três regras desligadas, e sem o bloco
no `client.yaml` o gate fica como antes. O exemplo de referência está em `examples/` (guia e
narrativa antiga, mesmo tema, fontes abertas e datadas).

O medidor de narrativa conta marcas de superfície (pretérito em série, cena, nome que volta com
verbo no passado). Ele não sabe se o exemplo carrega um passo, não separa relato necessário de
história gratuita e não vê narrativa no presente; por isso é aviso, e a amarra entre exemplo e
passo fica com o prompt e com a revisão.

**Pendências para o dono decidir**

1. Subir alguma das três regras para erro depois de três cursos reais aprovados.
2. Tipo de aula por aula: hoje vale o `tipo_de_aula` do cliente para todas; o planejamento
   poderia marcar cada aula como prática ou conceitual.
3. Levar a regra à fonte `escrita-empreendedor`: o molde D ainda pede "um exemplo do ramo
   dele, contado de ponta a ponta" e o fecho "pelo exemplo"; aqui o exemplo ficou curto e o
   fecho, no critério de pronto.
4. Prompts en e es continuam no molde antigo (auditoria B1: nenhum agente os carrega).

Relacionadas: [[boas-praticas-de-escrita-20260927]],
[[didatica-explicar-em-vez-de-detalhar-20260922]],
[[diretriz-editorial-v3-narrativa-sem-cota]].

---

## Linha do tempo (append-only, ordem reversa)

- **2026-09-27**: [criação] pedido do dono: "mais completo em guia sobre como fazer e reduzir
  um pouco o excesso de storytelling muito aleatório", com o `Escrita-Empresarial` como
  referência e fontes recentes. Evidência da produção do mesmo dia: o caso da pousada
  atravessando 16 aulas com cena datada, e 24 correções de aulas já escritas vindas de artigos
  de julho a setembro de 2026, entre elas um limite de 2024 dado como número atual.
  Diagnóstico em `docs/DIAGNOSTICO_GUIA_APLICAVEL_20260927.md`.
