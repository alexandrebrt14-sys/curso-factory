# Diagnóstico: da aula contada à aula-guia (27/09/2026)

Pedido do dono, em 27/09/2026: "o curso factory precisa ser mais completo em guia sobre como
fazer e reduzir um pouco o excesso de storytelling muito aleatório. Pra isso, pegue mais dicas
em https://github.com/alexandrebrt14-sys/Escrita-Empresarial e torne o curso factory mais
parecido com guias aplicáveis e sempre bem embasados conceitualmente em fontes recentes".

Três objetivos saem do pedido: a aula ensina a fazer, do começo ao fim; caso, personagem e cena
só entram quando carregam o procedimento; todo conceito central se apoia em fonte recente e
verificável, com data. Este documento registra onde o repositório empurra hoje para a narrativa,
o que falta para a aula virar guia, como a data das fontes é tratada e a proposta, regra por
regra. A implementação está no mesmo PR.

## 1. Onde o repositório empurra para a narrativa

A narrativa entrou como correção. Em 11/08/2026 a diretriz v3 tornou o storytelling
obrigatório (`wiki/decisions/diretriz-editorial-v3-narrativa-sem-cota.md`, linhas 42 a 46:
"abertura em situação, tensão antes da solução, caso condutor, promessa cumprida, fechamento com
callback"), porque o texto da época era só reprovação e não prendia ninguém. Em 08/09 a abertura
em cena caiu (R1), mas o caso condutor ficou no centro do molde, e a produção de 27/09 mostrou o
efeito: no curso de super agentes pessoais, a pousada da Marta atravessa as 16 aulas, com cena
datada ("Numa sexta às 18h, o agente da Marta respondia a doze pedidos...") e a técnica "o caso
anda uma casa por aula" recomendada como decisiva (`TECNICAS_ADICIONAIS.md`, A5 e A17). O
exemplo virou o fio da aula, e o procedimento ficou espalhado em prosa no meio dele.

| Arquivo e linha | O que pede hoje | Efeito |
|---|---|---|
| `src/templates/prompts/pt-br/draft.md:83-87` | "H2 2: um caso do seu ramo, do começo ao fim", "quem é, o que estava acontecendo, o que a pessoa fez passo a passo, o que aconteceu depois"; o cabeçalho "nomeia o caso" ("Como a oficina do Sérgio...") | um H2 inteiro obrigatório de narrativa com personagem |
| `draft.md:89-91` | "Sem etapas numeradas de exercício" | o redator lê como proibição de passo a passo e dilui o procedimento em prosa |
| `draft.md:93-94` e `:239` | fecho "dito pelo exemplo do H2 2"; "Fecho pelo exemplo" | a aula termina no personagem, não no critério de pronto |
| `draft.md:188` | "cena de duas frases dentro do H2 2" como liberdade de forma | legitima cena dentro do caso |
| `draft.md:229` | "o exemplo é um e vai do começo ao fim" | conferência final cobra o caso, não o procedimento |
| `review.md:16`, `:23-24`, `:43-44`, `:55` | "um exemplo contado por inteiro"; "um caso do ramo, do começo ao fim"; "Fecho ... pelo exemplo" | o revisor acrescenta narrativa quando falta |
| `analyze.md:12-13`, `:37`, `:98` | "exemplo ... contado por inteiro"; campo `aulas_sem_exemplo_inteiro` | a análise pontua a ausência de caso inteiro como falha |
| `expand.md:7` | "no segundo, o exemplo contado do começo ao fim" | a expansão de aula curta cresce pela história |
| `research.md:57-61` | "3 a 5 casos reais ... contados do começo ao fim" | a pesquisa busca história, não procedimento |
| `src/agents/writer.py:34` e `src/agents/researcher.py:32` | fallback inline com "caso do ramo do aluno contado inteiro" e "casos contáveis do começo ao fim" | o mesmo pedido no caminho de reserva |
| `config/quality_rules.yaml:558` e `:563` | "teoria densa ... sempre depois de um caso contado inteiro"; "o fecho retoma o caso" | a ordem do curso e o fecho de cada aula dependem de caso |
| `src/validators/content_checker.py:858-859` e `:948-950` | mensagens do gate: "falta a narrativa ... ou o exemplo contado por inteiro"; "contar o caso do ramo do aluno até o fim" | o próprio verificador pede narrativa |
| `CLAUDE.md:106`, `:161-162`, `:341` | "O caso nomeado entra no H2 do exemplo e o fecho o retoma"; "caso condutor contado inteiro no H2 do exemplo ... fecho que retoma o caso" | documentação de entrada repete a exigência |
| `DIRETRIZ_EDITORIAL.md:50-52` e `:105` | "sempre depois de um caso contado inteiro"; "o fecho retoma o caso"; "exemplo do negócio pequeno contado inteiro" | seção própria do repositório repete a exigência |

A fonte de estilo não obriga nada disso. O `escrita-empreendedor` 1.8.0 proíbe abrir em cena,
hora ou personagem (DIRETRIZ §2 regra 2), pede no molde D "um exemplo do ramo dele, contado de
ponta a ponta, com número" e admite "cena de duas frases no meio da seção" quando encurta o
caminho até a decisão (regra 26). Personagem com nome, caso que atravessa o curso e fecho que
volta ao personagem são acréscimos deste repositório. O `Escrita-Empresarial` guarda o "caso
condutor" (§3) para o gênero artigo de opinião; no memorando, no parecer e na análise, que são
os gêneros de decisão, o esqueleto é resposta, opções com custo, riscos com mitigação e pedido
com dono e prazo (`MOLDES_DE_GENERO.md`).

## 2. O que falta para a aula ser um guia de como fazer

A aula de hoje explica bem por que a ideia importa e mostra alguém aplicando. Ela não entrega,
de forma que o aluno consiga repetir sozinho:

1. **O procedimento em passos.** Nenhum prompt pede passos em sequência, e o `draft.md` desencoraja
   etapa numerada. A peça certa já existe no gerador (`stepGuide`, promovido da lista numerada
   pelo parser) e o `Escrita-Empresarial` a descreve: "Processo em que a ordem importa: guia de
   passos, um verbo por passo e o resultado observável de cada um" (DIRETRIZ §11).
2. **Pré-requisitos da aula.** Hoje vivem só na trilha (`draft.md:99-100`); a aula que exige uma
   conta, um dado ou uma ferramenta não diz isso antes do primeiro passo.
3. **Verificação por passo.** O critério de acerto existe só no fecho. Passo sem "como saber que
   deu certo" deixa o aluno sem saber se pode seguir.
4. **Erro comum com o conserto.** O erro aparece no H2 1, em prosa, como argumento; não aparece
   junto do passo em que acontece, com a saída.
5. **Decisão condicional.** Nada pede a sensibilidade do `Escrita-Empresarial` ("o que muda se o
   dado mudar", esqueleto da análise) nem a forma "se isto, faça aquilo" no lugar de "depende".
6. **Caminhos com custo.** Quando há escolha, o memorando de referência mostra duas ou três
   opções com o que custam, incluindo não fazer nada (`exemplos/memorando_bom.md`); a aula não pede.
7. **Critério de pronto.** O fecho tem critério de acerto, mas nenhuma regra separa "terminou o
   procedimento" de "gostou da aula".
8. **Nenhum verificador mede nada disso.** A categoria `didatica` mede cadência, glosa, fecho,
   título e fichas; nenhuma medida diz se a aula ensina a fazer.

## 3. Como a pesquisa e a redação tratam a data das fontes

| Ponto | Hoje | Consequência |
|---|---|---|
| `research.md:49` | "Priorize fontes de 2024–2026", janela escrita à mão | envelhece sozinha; em 2027 a mesma frase aceita fonte de três anos |
| `research.md:75-77` | "Use a data de publicação e a data do fenômeno" | bom princípio, sem campo que registre a data por fonte |
| `research.md:94` | referência com "ano" | ano sem mês não separa fonte de janeiro de fonte de dezembro |
| `trail.md:54` | fonte da trilha com "mês e ano" | a data chega ao rodapé, mas ninguém a mede |
| `proveniencia.py` | colunas URL, trecho lido e data de acesso | data de acesso diz quando se leu, não quando foi publicado |
| gate | `check_geo` conta fontes atribuídas | nenhuma medida de recência; fonte sem data passa |

A produção de 27/09 mostra o custo. O `PLANO_DE_INCREMENTOS.md` do curso de super agentes aplicou
75 edições em 16 aulas já escritas; 24 foram correções, em que o texto ficava errado ou prometia
mais do que o fato, e as fontes novas vieram de 215 artigos publicados de 01/07 a 27/09/2026. No
`COMPATIBILIDADE.md`, o ajuste 09.2 é o caso típico: a aula dava o limite de contexto publicado em
2024 como número atual, quando em setembro de 2026 os maiores modelos aceitam 1 milhão de tokens.
Uma alegação de estado atual apoiada em fonte de dois anos passou pelo pipeline sem aviso.

## 4. Proposta, regra por regra

Toda regra positiva nasce como aviso, como manda a GOVERNANCA do `Escrita-Empresarial` ("só sobe
a ERRO com três textos reais aprovados"). Os números ficam na configuração; o código só lê.

| # | Regra | O que muda | Configuração | Validador | Severidade de partida |
|---|---|---|---|---|---|
| A | Molde de aula-guia | Esqueleto em oito partes, cada uma só quando tem conteúdo: resposta na primeira frase; o que é e por que importa, com fonte; o que precisa estar pronto; passos com verbo no imperativo, verificação e erro comum com conserto; decisões "se isto, faça aquilo"; exemplo curto que percorre os passos; critério de pronto e próximo passo; fontes no rodapé. Entra no planejamento, na redação, na análise, na revisão e na expansão | `validation.guia_aplicavel.esqueleto` e `instrucao_*` | prompts via `{bloco_molde_da_aula}` | não se aplica |
| B | Completude do como fazer | Mede procedimento (lista numerada ou bloco de passos), verbo no imperativo abrindo cada passo, verificação, erro comum, decisão condicional e critério de pronto, com piso por tipo de aula (prática ou conceitual; a conceitual nunca fica com zero orientação) | pisos e marcadores em `validation.guia_aplicavel`; liga e severidade no `client.yaml` (`guia_aplicavel`) | `src/validators/guia_aplicavel_checker.py` | aviso |
| C | Orçamento de narrativa | Parcela máxima de parágrafos de prosa com marcas de narrativa (pretérito em série, cena, personagem recorrente); abertura em cena ou em história reprova à parte; personagem opcional; fim do caso nomeado obrigatório e do fecho que retoma o caso | marcadores em `validation.orcamento_narrativa`; teto e severidade no `client.yaml` (`narrativa`) | `src/validators/narrativa_checker.py` | aviso |
| D | Fonte recente | Pesquisa e redação pedem fonte primária por conceito central, com data de publicação; fonte antiga só como origem do conceito, dita como tal. O gate lê o bloco de fontes e a tabela de proveniência, exige data por fonte, calcula a parcela recente e confere alegação de estado atual contra a idade da fonte; fonte sem data conta como não recente; a data de referência é injetada | formatos e marcadores em `validation.fontes_recentes`; janela, parcela, teto do estado atual e data de referência no `client.yaml` (`fontes_recentes`) ou no curso | `src/validators/fontes_recentes_checker.py`; coluna "Data de publicação" em `proveniencia.py` | aviso |
| E | Documentação | `CLAUDE.md`, `AGENTS.md`, `DIRETRIZ_EDITORIAL.md`, especificação de didática, decisão nova, índice e changelog; onde havia narrativa obrigatória, corrigido | não se aplica | não se aplica | não se aplica |
| F | Exemplo de referência | Aula curta no molde novo e a mesma aula no estilo antigo, com fontes abertas e datadas, usadas nos testes como antes e depois | `examples/` | testes | não se aplica |

Três fronteiras ficam como estão. A R6 continua: passo de procedimento é conteúdo da aula, dito
com verbo e resultado, e nunca bloco rotulado "exercício", "faça agora", "Resultado esperado:" ou
"Se travar:"; a verificação e o conserto entram em prosa dentro do passo. A R7 continua: fonte só
no rodapé, e a aula não conta como a fonte foi checada. O molde não vira formulário: a parte que
não tem conteúdo não entra, e nenhuma parte ganha cabeçalho fixo.

### O que o medidor de narrativa consegue e o que não consegue medir

Ele conta marcas de superfície por parágrafo: verbos no pretérito perfeito e imperfeito em
sequência, marcadores de cena (hora do dia, dia da semana, "naquela manhã", fala entre aspas com
verbo de dizer) e nome próprio que volta em mais de um parágrafo com verbo no passado. Ele
consegue apontar a aula em que a história ocupa espaço demais e a abertura que começa em cena.
Ele não entende se o exemplo carrega um passo do procedimento, não distingue um relato histórico
necessário (a origem do conceito) de uma história gratuita, confunde marca comercial com
personagem quando a marca volta com verbo no passado e deixa passar narrativa escrita no presente
("a Marta abre a agenda"). Por isso ele nasce como aviso, com o teto no `client.yaml`, e a amarra
entre exemplo e passo fica com o prompt e com a revisão.

### Valores de partida

- Narrativa: até 20% dos parágrafos de prosa da aula, a proposta do dono. Numa aula de 12
  parágrafos, cabem dois de exemplo, que é o tamanho de um exemplo aplicado curto.
- Recência: ao menos metade das fontes com até 12 meses, e nenhuma alegação de estado atual
  apoiada em fonte com mais de 18 meses. Os 12 meses cobrem a janela que o `PLANO_DE_INCREMENTOS`
  precisou para corrigir as aulas de 27/09; os 18 meses dão folga para relatório anual que ainda
  não teve sucessor. A fonte de origem do conceito fica fora da conta.
- Completude, aula prática: ao menos três passos, todos abrindo com verbo no imperativo, uma
  verificação, um erro comum com conserto, uma decisão condicional e um critério de pronto. Aula
  conceitual: dois passos ou uma decisão condicional, e o critério de pronto.

### O que só a geração real vai dizer

Se o redator cumpre o esqueleto sem virar formulário; se o teto de 20% corta exemplo útil; se os
marcadores de passo e de verificação têm falso negativo relevante no texto do GPT; e se a janela
de 12 meses é alcançável em tema estável. Os números estão na configuração para ajustar depois da
primeira rodada, sem mexer em código.
