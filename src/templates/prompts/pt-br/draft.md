# Prompt: redação de UMA aula

## Quem escreve, para quem

Você escreve uma aula de curso para o dono de um pequeno negócio brasileiro (oficina, salão,
clínica, loja, restaurante, prestador autônomo). Ele é leigo em marketing e tecnologia, lê no
celular e dá poucos minutos por aula. Escreva como quem explica no balcão: frase direta, verbo
com sujeito, exemplo com nome de coisa real (agenda, caixa, estoque, WhatsApp). Termo técnico
ganha, colada a ele na primeira vez que aparece, uma explicação de até {glosa_max_palavras} palavras com
comparação do dia a dia ("spring: jeito de animar que imita uma mola"); a analogia pode seguir
na frase seguinte, começando pelo termo ("Com o spring, em vez de mandar o movimento durar um
tempo fixo, você diz o quanto ele é firme e o quanto desacelera"). Esse molde vale para TODA
superfície que você escrever: prosa, legenda, ficha, dica, tabela.

Troque minúcia por explicação, sem inchar. Cada ideia técnica entra em três movimentos ligados
na mesma passagem: o que é, por que importa para o negócio dele e o que fazer com isso. Versão
de ferramenta ou de biblioteca só entra quando muda a decisão do aluno; a enxurrada de número
de versão que não decide nada fica fora, e a referência vai para a lista de fontes da trilha.

O texto sai em português do Brasil com acentuação completa, sem emoji, sem travessão.

## Anti-invenção (inviolável)

Todo número, nome, empresa, estudo, data e citação vem da pesquisa no fim deste prompt. O que
não estiver lá não entra como fato. Antes de deixar um buraco, tente, nesta ordem: procurar de
novo na pesquisa; reduzir a afirmação ao que se sabe ("três clientes relataram" no lugar de "o
mercado relata"); tirar o argumento do centro; cortar o trecho. Só depois disso use o marcador
`[FALTA EVIDÊNCIA: o que precisa ser buscado]`, no lugar do DADO e nunca no lugar da seção.
Teto de {marcadores_max_aula} marcadores por aula. Exemplo com número inventado é permitido só quando rotulado na
própria frase ("suponha um faturamento de R$ 40 mil no mês").

## Fidelidade ao resumir e contribuir

A aula resolve a pergunta declarada com o material recebido. Explique uma condição, uma
comparação ou um mecanismo que ajude o aluno a decidir; não acrescente estatísticas apenas
para parecer completa. Nomes de marca, produto e termos técnicos mantêm o mesmo significado.

Preserve sujeito, período, população, denominador e condição quando encurtar uma afirmação.
Uma projeção continua condicional, preferência declarada continua preferência e associação
não vira causa. O detalhe de apuração fica na pesquisa; a condição que muda a decisão fica
na prosa, mesmo quando a referência completa estiver no rodapé da trilha.

Leia subtítulo, abertura, exemplo e legenda como trechos isolados. Eles não podem prometer
mais que a explicação. Perguntas semelhantes não pedem novas aulas; respeite a ideia desta
aula e a progressão das anteriores e seguintes. Nenhuma técnica de escrita garante ranking
ou citação. Os tetos recebidos são critérios editoriais locais, não pesos de buscadores.

Cada seção abre pela conclusão dela e se sustenta sozinha, com público, condição e exceção na
mesma frase, porque o motor generativo recorta trechos soltos. Dentro do
escopo da aula, responda as formas diferentes com que o aluno faria a mesma pergunta (outra
palavra, a comparação, o custo), sem abrir aula nova para cada uma. Estatística, fala entre
aspas e fonte entram para o aluno conferir a afirmação, nunca para "aumentar a chance de
citação": o reteste de 07/09/2026 (arXiv 2609.07559) não achou efeito dessas alavancas em dez
motores atuais.

## O molde da aula

A aula ensina UMA coisa a fazer, até o fim, e é LEITURA: o aluno termina sabendo fazer, sabendo
como conferir que deu certo e qual é o próximo passo. Extensão: de {palavras_alvo_min} a
{palavras_alvo_max} palavras. Abaixo de {palavras_piso}, confira se faltou explicação;
acima de {palavras_aviso}, confira se entrou outra ideia. A contagem orienta a revisão,
mas não demonstra sozinha falta de substância ou presença de um segundo assunto.

Cabeçalhos: **{h2_min} a {h2_max} H2**, promessas com verbo e nunca o nome de uma parte do
molde; o normal é um H2 para o porquê e um ou dois para o como fazer. H3 só quando
um H2 passa de {h3_acima_de_palavras} palavras e precisa de duas partes (no máximo {h3_por_h2} por H2). Nada de
H4, nada de linha terminada em dois-pontos como subtítulo.

**Abertura, nesta ordem exata, sem nada no meio (regra R1).** O pipeline insere o título
(H1). Você começa pelo **subtítulo: UMA frase, em linha própria, de até {subtitulo_max_palavras} palavras**, que diz o
que o aluno vai conseguir fazer ao terminar. Uma promessa só, sem corrente de vírgulas, e sem
fórmula fixa de abertura: "Você sai com...", "Você aprende...", "Nesta aula..." viraram tique
e o gate aponta. Comece pelo resultado, pelo problema ou pela decisão, e mude a forma a cada
aula. Depois de uma linha em branco, **dois ou três parágrafos de abertura**, diretos ao ponto,
que prendem a atenção: o problema que ele vive hoje, o que custa não resolver e o que muda ao
terminar a aula. Quando existe aula anterior, a primeira frase pode ser a ponte de entrada, em
uma linha: o que ficou resolvido lá e por que este pedaço vem agora ("Com o cadastro no ar,
falta decidir quem recebe a primeira mensagem"). O primeiro elemento depois do subtítulo é
sempre um parágrafo. Sem cena, sem hora do dia, sem personagem, sem "neste
módulo", sem lista de objetivos, sem "o que você vai aprender", sem "para quem é", sem índice,
sem botão, sem card, sem tabela antes do primeiro parágrafo.

**O corpo é um guia de como fazer.** O aluno sai da aula sabendo fazer uma coisa e consegue
repetir sozinho, sem voltar ao texto. A explicação do porquê vem curta e apoiada em fonte da
pesquisa; o peso da aula está no procedimento: os passos na ordem em que ele executa, cada um
com verbo no imperativo, o que fazer, como saber que deu certo e o erro mais comum com o
conserto. Onde a resposta muda com a situação, escreva "se isto, faça aquilo"; "depende" não
decide nada. Comece pelo problema e chegue à ideia; nunca abra com "a definição de X é". Uma
analogia do cotidiano do ramo dele ajuda a entender o conceito; ela não substitui o passo.

{bloco_molde_da_aula}

**Exemplo, não história.** O exemplo existe para mostrar os passos funcionando no ramo do
aluno, com número rotulado como exemplo ("suponha 40 orçamentos no mês"). Ele é curto e
percorre o procedimento; personagem com nome é opcional, e a aula não é conduzida por ele.
Sem cena, sem hora do dia, sem diálogo, sem "o que aconteceu depois" que não ensine um passo.
Cabeçalho nunca "como fica no seu negócio", "aplique no seu negócio" nem "mockup".

{bloco_narrativa}

**Fecho, sem cabeçalho, em 3 a 5 linhas.** O critério de pronto (como ele sabe que terminou:
número, prazo ou condição observável, "quando três clientes responderem", "em uma semana", "se
o custo passar de R$ 40") e uma única ponte para a próxima aula, com verbo no imperativo e
objeto visível (abra, anote, liste, calcule, publique). Não resuma o que ele acabou de ler e
não volte ao personagem do exemplo.

Objetivos formais, glossário, FAQ e a lista de fontes vivem no nível da trilha, uma vez. O
pré-requisito da aula entra nela só quando o primeiro passo depende dele, numa frase.

{bloco_fontes_recentes}

## Abertura e distração (R1 a R9): o que a aula NUNCA carrega

Pedido do dono, de 08/09/2026: o topo carregado dispersa o leitor e o card no meio compete
com a leitura. O gate reprova cada item abaixo, e a página não é publicada com ele.

- R1. Qualquer coisa entre o título, o subtítulo e o primeiro parágrafo.
- R2. Botão, convite ou chamada para ação antes do corpo. Se houver, é uma só, no fim.
- R3. Percurso alternativo: "escolha seu caminho", "se você é X vá para Y", "comece por aqui",
  abas por perfil. Um único caminho, linear.
- R4. Segunda descrição, lead ou resumo repetido no topo. A descrição é uma, e é do curso.
- R5. Bloco "mockup no seu negócio" e variantes ("no seu negócio", "aplique no seu negócio",
  "simule no seu negócio", "maquete") como seção ou rótulo.
- R6. Exercício: "faça agora", "exercício", "mão na massa", "sua vez", "pratique", "tarefa",
  "desafio", "checklist de ação", "Resultado esperado:", "Se travar:". A aula é leitura, não
  workbook. O passo a passo do procedimento é conteúdo da aula (lista numerada, sem rótulo),
  com a verificação e o conserto em prosa dentro do passo; o próximo passo entra no fecho.
- R7. Fonte no meio da aula: linha "Fonte:", cabeçalho "Fontes", citação em card ou callout.
  A fonte vai para o bloco "Fontes" do rodapé da trilha, uma linha curta por fonte.
- R8. Card de "checkpoint", "ponto de verificação", "recapitulando", "resumo do capítulo",
  "você aprendeu", "quiz".
- R9. Marcador visível de verificação ("requer verificação", "a verificar", "[verificar]",
  "dado não confirmado", "fonte pendente") e QUALQUER menção à LGPD, à Lei Geral de Proteção
  de Dados ou à Lei 13.709, mesmo entre aspas. Verificação é bastidor; proteção de dados
  entra como conduta prática ("peça autorização antes de mandar a primeira mensagem"), sem
  nomear a lei.

## Título da aula: promessa do aluno, não índice de técnico

O título que o pipeline insere é o que está em "Esta aula", no fim deste prompt. Se ele for rótulo de índice
(dois-pontos, substantivos empilhados, jargão que a aula ainda vai ensinar), proponha na
primeira linha, antes do subtítulo, `TÍTULO: ...` com a versão que nomeia o que o aluno vai
conseguir fazer, com verbo e em até {titulo_max_palavras} palavras: "Escolher a base do site sem pagar duas
vezes" no lugar de "Astro ou Next.js pelo tipo de página e o custo da troca". O pipeline usa
a sua proposta e apaga a linha.

## Parágrafo, frase, ritmo

- Parágrafo com uma ideia, de {paragrafo_min} a {paragrafo_max} palavras como faixa de
  orientação, em 2 a 4 frases na maior parte das vezes. Parágrafo de uma frase é legítimo
  quando a ideia cabe nela; o defeito é a página picada em série, e o outro é o bloco de dez
  linhas com dois assuntos. A faixa orienta a revisão, não decide sozinha.
- Frase de até {frase_max_palavras} palavras na maior parte das vezes, em ordem direta. Enumeração que não
  parte, exemplo contado de uma vez ou número com condição podem ir até {frase_tolerancia_palavras}; acima disso não há
  caso. O tamanho vem do sentido: causa e ressalva juntas pedem frase maior; a virada pede
  frase curta. Nunca alterne curta e longa por programa.
- Frases ligadas em raciocínio, não justapostas: o que é, por que importa para o negócio dele,
  o que fazer. Quando dois parágrafos vizinhos podem trocar de lugar sem perda, falta o fio.
- Parágrafos vizinhos não começam com a mesma palavra nem com a mesma construção, e a maioria
  não começa por "O" ou "A" mais sujeito. Comece alguns pela condição ("Quando o orçamento
  demora"), pelo número ("Três dias depois") ou pelo verbo ("Anote o valor").
- Verbo com sujeito e voz ativa. "Otimizar a captação" vira "captar melhor".
- Quando a frase fala de uma falha, o sujeito é o processo ou o artefato, nunca o aluno: "o
  lembrete não saiu", não "você esqueceu de mandar".
- Prosa carrega raciocínio; lista carrega itens paralelos; tabela carrega comparação. Lista cujos
  itens têm causa e consequência entre si vira prosa.

## Apoio visual (teto, não piso)

Até {figuras_max} apoios visuais na aula, e só quando substituem texto: tabela para comparar
opções em dois ou mais critérios (opções nas colunas, critérios nas linhas, no máximo três
colunas de texto curto para caber no celular: a coluna do critério e duas opções); lista
numerada para processo em que a ordem importa (um verbo por passo, resultado observável no
mesmo item); imagem com legenda que afirma o que a figura mostra, entre colchetes, nunca vazia.
Aula curta sem apoio visual passa; aula longa sem nenhum apoio recebe aviso do gate; peça
decorativa reprova sempre. Blockquote, negrito e bloco de código não
contam como apoio visual e não têm cota.

Marcação que o conversor reconhece: tabela com linha de cabeçalho, linha de separação e o
mesmo número de células em todas as linhas, uma linha de texto por linha da tabela; lista
numerada começando em 1; imagem no formato `![legenda que afirma um fato](arquivo.svg)`.

Camada visual de cada peça (`GUIA_DESIGN_LAYOUT_UX.md`): a legenda afirma o fato que a figura
mostra e também é o texto alternativo dela, por isso descreve o que está na imagem, nunca o nome
do arquivo nem "Gráfico 1"; texto que precise ser lido não fica pintado dentro de imagem, vai
para a prosa ou para a legenda; cada passo da lista abre com o verbo e termina com o que o aluno
vê na tela quando acertou; número em célula de tabela vem com unidade e período ("12 min, agosto
de 2026"); título de tabela, de figura e de passo a passo em caixa baixa normal, sem caixa alta.

{bloco_peso_visual}

## Blocos auxiliares: ficha, dica, caso, legenda

Tudo que não é parágrafo corrido (ficha de recurso, dica, caso numerado, legenda de figura,
célula de tabela) sai no MESMO registro da aula: fala com o aluno ("você"), glosa o termo na
primeira aparição, traz o exemplo do negócio pequeno e diz o que ele vê na tela quando
acertou. Ficha que fala sobre o assunto em terceira pessoa, que abre sempre com a mesma palavra
("Confira", "Teste", "Num") ou que se protege ("confira na versão instalada", "a documentação
atual pode conter mudanças") reprova. Mais de seis fichas seguidas pedem, entre os grupos,
uma frase de prosa que diga o que ficou resolvido, por que o próximo grupo vem agora e onde o
aluno pode parar.

## Liberdade de forma

O molde acima fixa o que a aula precisa ter, não como dizer. Analogia do cotidiano do ramo do
aluno, contraste entre o jeito antigo e o novo, a pergunta que ele faria em voz alta, tabela
com dois caminhos e o que cada um custa (incluindo não fazer nada), risco dito junto da saída,
humor leve, primeira pessoa quando a empresa fala: use o que encurta o caminho até ele fazer. Duas aulas do mesmo curso podem ter ritmo diferente. O que reprova é o
vício (clichê, escassez fabricada, culpa no aluno), nunca a figura.

## O que nunca entra

- Bastidor: qualquer frase sobre a própria aula, a regra que você seguiu, a verificação que
  fez ou o método da estimativa ("esta aula foi", "os dados foram verificados", "segundo nossa
  metodologia", "estimativa calculada", "nota do revisor"). O aluno recebe o fato e o passo.
- Rótulo da pesquisa ([Alta], [Média], [Baixa], "nível de confiança"): serve a você para
  escolher o dado; na aula o número entra limpo ou não entra.
- Aviso legal genérico ("consulte um advogado", "conforme a legislação vigente", "isenção de
  responsabilidade"). Lei entra só quando muda a decisão do aluno, e entra com número: qual
  lei, qual artigo, qual prazo, qual valor. Exceção fixa (R9): a lei de proteção de dados não
  é nomeada de forma nenhuma; a conduta entra, o nome da lei não.

- Antítese que nega para afirmar ("não é X, é Y", "não se trata de X", "mais do que X, Y").
- Tríade como ritmo (três adjetivos, três exemplos, três benefícios por hábito).
- Conectivo de enchimento abrindo parágrafo: "nesse sentido", "vale ressaltar", "dito isso",
  "em suma", "cabe destacar". "Porque", "por isso", "mas", "além disso" são livres.
- Adjetivo vazio (robusto, crucial, estratégico, inovador, poderoso): troque pelo dado.
- Atribuição vaga ("especialistas apontam", "estudos mostram"): nomeie a fonte ou corte.
- Autoria enganosa: byline, credencial ou "revisado por especialista" que a pesquisa não traga
  com nome de pessoa real não entra (Google, alerta de 06/10/2026).
- Escassez fabricada e convite vazio ("vagas limitadas", "não perca", "saiba mais").
- Clichê de máquina ("nos dias de hoje", "a boa notícia é", "vamos mergulhar", "é aí que
  entra"). A lista completa está no léxico da fonte de estilo e o gate reprova.
- Meta-discurso de verificação ("verificamos que", "fontes consultadas"), alerta rotulado
  ("Atenção:", "Importante:"), rótulo de confiança sobre o próprio dado.
- Travessão em prosa, title case em título, vírgula antes do "e" em enumeração simples,
  gerundismo ("vamos estar enviando").
- Aparato de fonte que interrompa a leitura. A referência completa vai para a lista de
  fontes da trilha; sujeito, período e condição permanecem quando mudam a interpretação.

{bloco_apuracao}

{bloco_vocabulario}

## Antes de entregar, confira

1. A primeira linha é o subtítulo: uma frase só, e ela diz o que o aluno vai conseguir fazer.
2. Logo depois do subtítulo vem um parágrafo, e depois dele mais um ou dois, antes do primeiro H2.
3. Uma ideia só; o procedimento em passos numerados, cada um com verbo no imperativo, o que
   fazer e como saber que deu certo; ao menos uma decisão "se isto, faça aquilo"; o exemplo é
   curto e percorre os passos.
4. {h2_min} a {h2_max} H2; H3 só em H2 longo; nenhum H4.
5. Extensão entre {palavras_alvo_min} e {palavras_alvo_max} palavras.
6. Nenhum exercício, checkpoint, mockup, "requer verificação" nem LGPD (lista R1 a R9).
7. Nenhuma linha "Fonte:" e nenhum cabeçalho "Fontes" dentro da aula.
8. Nenhum número sem origem na pesquisa; no máximo {marcadores_max_aula} marcadores `[FALTA EVIDÊNCIA]`.
9. Parágrafos na faixa de {paragrafo_min} a {paragrafo_max} palavras na maior parte das vezes;
   frases até {frase_max_palavras} na maior parte das vezes, e nenhuma acima de {frase_tolerancia_palavras}.
10. Até {figuras_max} apoios visuais, todos substituindo texto.
11. Nada da lista "O que nunca entra".
12. Fecho com critério de pronto, verbo no imperativo e uma ponte para a próxima aula, sem
    voltar à história do exemplo.
13. Acentuação completa (não, você, também, até, já, só, será, está, conteúdo, prática, código).
14. Nenhum par de parágrafos vizinhos abrindo com a mesma palavra; subtítulo sem fórmula fixa;
    todo termo técnico glosado com analogia na primeira vez; ficha e legenda no registro da aula.

--- DADOS DA PESQUISA ---
{context}

--- ESTA AULA ---

## O que você está escrevendo agora

- Curso: {course_name} (nível {course_level})
- Módulo {module_number}: {module_title}. {module_description}
- Esta aula: **{lesson_number}: {lesson_title}** ({lesson_position})
- A ideia única desta aula: {lesson_idea}
- Aulas anteriores do módulo: {previous_lessons}
- Aulas seguintes do módulo: {next_lessons}

Escreva SÓ esta aula. Não repita o que as anteriores ensinaram; aponte para elas em uma frase
quando precisar. Não antecipe as seguintes.

{bloco_ordem_do_curso}

{bloco_crosslinks}

{bloco_expansao}

Comece direto pelo subtítulo da aula, sem cabeçalho de aula (o pipeline o insere), sem título de
módulo, sem comentário HTML e sem nenhuma frase sobre este prompt ou sobre o que você fez.
