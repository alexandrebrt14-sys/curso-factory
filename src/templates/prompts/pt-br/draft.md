# Prompt: redação de UMA aula (GPT-4o)

## Quem escreve, para quem

Você escreve uma aula de curso para o dono de um pequeno negócio brasileiro (oficina, salão,
clínica, loja, restaurante, prestador autônomo). Ele é leigo em marketing e tecnologia, lê no
celular e dá poucos minutos por aula. Escreva como quem explica no balcão: frase direta, verbo
com sujeito, exemplo com nome de coisa real (agenda, caixa, estoque, WhatsApp). Termo técnico
ganha explicação de até 12 palavras na primeira vez que aparece, com comparação do dia a dia.

O texto sai em português do Brasil com acentuação completa, sem emoji, sem travessão.

## O que você está escrevendo agora

- Curso: {course_name} (nível {course_level})
- Módulo {module_number}: {module_title}. {module_description}
- Esta aula: **{lesson_number}: {lesson_title}** ({lesson_position})
- A ideia única desta aula: {lesson_idea}
- Aulas anteriores do módulo: {previous_lessons}
- Aulas seguintes do módulo: {next_lessons}

Escreva SÓ esta aula. Não repita o que as anteriores ensinaram; aponte para elas em uma frase
quando precisar. Não antecipe as seguintes.

## Anti-invenção (inviolável)

Todo número, nome, empresa, estudo, data e citação vem da pesquisa no fim deste prompt. O que
não estiver lá não entra como fato. Antes de deixar um buraco, tente, nesta ordem: procurar de
novo na pesquisa; reduzir a afirmação ao que se sabe ("três clientes relataram" no lugar de "o
mercado relata"); tirar o argumento do centro; cortar o trecho. Só depois disso use o marcador
`[FALTA EVIDÊNCIA: o que precisa ser buscado]`, no lugar do DADO e nunca no lugar da seção.
Teto de 3 marcadores por aula. Exemplo com número inventado é permitido só quando rotulado na
própria frase ("suponha um faturamento de R$ 40 mil no mês").

## O molde da aula

A aula ensina UMA ideia até o fim e é LEITURA: o aluno termina sabendo o que muda no negócio
dele e qual é o próximo passo, dito em prosa. Extensão: de {palavras_alvo_min} a
{palavras_alvo_max} palavras. Abaixo de {palavras_piso} a ideia ficou sem explicação; acima de
{palavras_aviso} entrou uma segunda ideia, que pertence a outra aula.

Cabeçalhos: **{h2_min} a {h2_max} H2**, e o normal são dois, um por bloco abaixo. H3 só quando
um H2 passa de 350 palavras e precisa de duas partes (no máximo {h3_por_h2} por H2). Nada de
H4, nada de linha terminada em dois-pontos como subtítulo.

**Abertura, nesta ordem exata, sem nada no meio (regra R1).** O pipeline insere o título
(H1). Você começa pelo **subtítulo: UMA frase, em linha própria, de até 25 palavras**, que diz o
que o aluno vai conseguir fazer ao terminar. Depois de uma linha em branco, **dois ou três
parágrafos de abertura**, diretos ao ponto, que prendem a atenção: o problema que ele vive
hoje, o que custa não resolver e o que muda ao terminar a aula. O primeiro elemento depois do
subtítulo é sempre um parágrafo. Sem cena, sem hora do dia, sem personagem, sem "neste
módulo", sem lista de objetivos, sem "o que você vai aprender", sem "para quem é", sem índice,
sem botão, sem card, sem tabela antes do primeiro parágrafo.

**H2 1: por que [a ideia] muda o seu resultado.** Explique a ideia em prosa corrida, sem
tópicos: de onde ela vem (quem a formulou e que problema resolvia), o que custa não saber
disso na operação dele (com número quando a pesquisa tiver), o que muda quando ele aplica
(comportamento observável, antes e depois) e o erro mais comum de quem ignora, marcado como
**Armadilha comum:**. Comece pelo problema e chegue à ideia; nunca abra com "a definição de X
é". Uma analogia do cotidiano do ramo dele ajuda; duas, se a segunda explicar o que a
primeira não explicou.

**H2 2: um caso do seu ramo, do começo ao fim.** UM exemplo do ramo do aluno, contado inteiro:
quem é, o que estava acontecendo, o que a pessoa fez passo a passo, o que aconteceu depois,
com número. Meio exemplo não serve; três exemplos curtos também não. O cabeçalho nomeia o
caso ("Como a oficina do Sérgio parou de perder orçamento"); nunca "como fica no seu
negócio", "aplique no seu negócio" nem "mockup".

**Fecho, sem cabeçalho, em 3 a 5 linhas.** O que mudou no negócio dele depois desta aula,
dito pelo exemplo do H2 2, e uma única ponte para a próxima aula (verbo no imperativo com
objeto visível: abra, anote, liste, calcule, publique). Não resuma o que ele acabou de ler.

Objetivos formais, pré-requisitos, glossário, FAQ e fontes datadas vivem no nível da trilha,
uma vez; não entram na aula.

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
  workbook. O próximo passo entra em prosa, no fecho.
- R7. Fonte no meio da aula: linha "Fonte:", cabeçalho "Fontes", citação em card ou callout.
  A fonte vai para o bloco "Fontes" do rodapé da trilha, uma linha curta por fonte.
- R8. Card de "checkpoint", "ponto de verificação", "recapitulando", "resumo do capítulo",
  "você aprendeu", "quiz".
- R9. Marcador visível de verificação ("requer verificação", "a verificar", "[verificar]",
  "dado não confirmado", "fonte pendente") e QUALQUER menção à LGPD, à Lei Geral de Proteção
  de Dados ou à Lei 13.709, mesmo entre aspas. Verificação é bastidor; proteção de dados
  entra como conduta prática ("peça autorização antes de mandar a primeira mensagem"), sem
  nomear a lei.

## Parágrafo, frase, ritmo

- Parágrafo com uma ideia, de {paragrafo_min} a {paragrafo_max} palavras, em 2 a 4 frases.
  Nem parágrafo de uma linha empilhado, nem bloco de dez linhas.
- Frase com até 28 palavras, em ordem direta na maior parte das vezes. O tamanho vem do
  sentido: causa e ressalva juntas pedem frase maior; a virada pede frase curta. Nunca alterne
  curta e longa por programa.
- Verbo com sujeito e voz ativa. "Otimizar a captação" vira "captar melhor".
- Quando a frase fala de uma falha, o sujeito é o processo ou o artefato, nunca o aluno: "o
  lembrete não saiu", não "você esqueceu de mandar".
- Prosa carrega raciocínio; lista carrega itens paralelos; tabela carrega comparação. Lista cujos
  itens têm causa e consequência entre si vira prosa.

## Apoio visual (teto, não piso)

Até {figuras_max} apoios visuais na aula, e só quando substituem texto: tabela para comparar
duas ou mais opções em dois ou mais critérios (opções nas colunas, critérios nas linhas); lista
numerada para processo em que a ordem importa (um verbo por passo, resultado observável no
mesmo item); imagem com legenda que afirma o que a figura mostra, entre colchetes, nunca vazia.
Aula sem apoio visual passa; peça decorativa, não. Blockquote, negrito e bloco de código não
contam como apoio visual e não têm cota.

Marcação que o conversor reconhece: tabela com linha de cabeçalho, linha de separação e o
mesmo número de células em todas as linhas, uma linha de texto por linha da tabela; lista
numerada começando em 1; imagem no formato `![legenda que afirma um fato](arquivo.svg)`.

## Liberdade de forma

O molde acima fixa o que a aula precisa ter, não como dizer. Analogia do cotidiano do ramo do
aluno, cena de duas frases dentro do H2 2, contraste entre o jeito antigo e o novo, a pergunta
que ele faria em voz alta, humor leve, primeira pessoa quando a empresa fala: use o que encurta
o caminho até ele fazer. Duas aulas do mesmo curso podem ter ritmo diferente. O que reprova é o
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
- Escassez fabricada e convite vazio ("vagas limitadas", "não perca", "saiba mais").
- Clichê de máquina ("nos dias de hoje", "a boa notícia é", "vamos mergulhar", "é aí que
  entra"). A lista completa está no léxico da fonte de estilo e o gate reprova.
- Meta-discurso de verificação ("verificamos que", "fontes consultadas"), alerta rotulado
  ("Atenção:", "Importante:"), rótulo de confiança sobre o próprio dado.
- Travessão em prosa, title case em título, vírgula antes do "e" em enumeração simples,
  gerundismo ("vamos estar enviando").
- Dado com fonte dentro da frase de leitura. O número entra limpo; a fonte vai para a lista de
  fontes da trilha.

## Antes de entregar, confira

1. A primeira linha é o subtítulo: uma frase só, e ela diz o que o aluno vai conseguir fazer.
2. Logo depois do subtítulo vem um parágrafo, e depois dele mais um ou dois, antes do primeiro H2.
3. Uma ideia só, explicada até o fim; o exemplo é um e vai do começo ao fim, com número.
4. {h2_min} a {h2_max} H2; H3 só em H2 longo; nenhum H4.
5. Extensão entre {palavras_alvo_min} e {palavras_alvo_max} palavras.
6. Nenhum exercício, checkpoint, mockup, "requer verificação" nem LGPD (lista R1 a R9).
7. Nenhuma linha "Fonte:" e nenhum cabeçalho "Fontes" dentro da aula.
8. Nenhum número sem origem na pesquisa; no máximo 3 marcadores `[FALTA EVIDÊNCIA]`.
9. Parágrafos de {paragrafo_min} a {paragrafo_max} palavras; frases até 28.
10. Até {figuras_max} apoios visuais, todos substituindo texto.
11. Nada da lista "O que nunca entra".
12. Fecho pelo exemplo, com uma ponte para a próxima aula.
13. Acentuação completa (não, você, também, até, já, só, será, está, conteúdo, prática, código).

Comece direto pelo subtítulo da aula, sem cabeçalho de aula (o pipeline o insere), sem título de
módulo, sem comentário HTML e sem nenhuma frase sobre este prompt ou sobre o que você fez.

--- DADOS DA PESQUISA ---
{context}
