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

A aula ensina UMA ideia até o fim e termina com o aluno tendo feito algo com um dado do
próprio negócio. Extensão: de {palavras_alvo_min} a {palavras_alvo_max} palavras. Abaixo de
{palavras_piso} a ideia ficou sem explicação; acima de {palavras_aviso} entrou uma segunda
ideia, que pertence a outra aula.

Cabeçalhos: **{h2_min} a {h2_max} H2**, e o normal são três, um por bloco abaixo. H3 só quando
um H2 passa de 350 palavras e precisa de duas partes (no máximo {h3_por_h2} por H2). Nada de
H4, nada de linha terminada em dois-pontos como subtítulo.

**Abertura, sem cabeçalho, em 2 ou 3 frases.** A primeira frase diz o que o aluno vai
conseguir fazer ao terminar. A segunda diz para quem isso serve ou o que ele ganha. Sem cena,
sem hora do dia, sem personagem, sem "neste módulo", sem lista de objetivos.

**H2 1: por que [a ideia] muda o seu resultado.** Explique a ideia em prosa corrida, sem
tópicos: de onde ela vem (quem a formulou e que problema resolvia), o que custa não saber
disso na operação dele (com número quando a pesquisa tiver), o que muda quando ele aplica
(comportamento observável, antes e depois) e o erro mais comum de quem ignora, marcado como
**Armadilha comum:**. Comece pelo problema e chegue à ideia; nunca abra com "a definição de X
é". Uma analogia do cotidiano do ramo dele ajuda; duas, se a segunda explicar o que a
primeira não explicou.

**H2 2: como fica no seu negócio.** UM exemplo do ramo do aluno, contado do começo ao fim:
quem é, o que estava acontecendo, o que a pessoa fez passo a passo, o que aconteceu depois,
com número. Meio exemplo não serve; três exemplos curtos também não.

**H2 3: faça agora.** Um exercício de 5 a 15 minutos, com estes campos: título que diz o que
ele vai produzir (nunca "Exercício 1"); etapas numeradas, cada uma com um verbo no imperativo e
um campo para o dado real do negócio dele; **Resultado esperado:** o que ele deve estar vendo
na tela ou no papel quando acertar; **Se travar:** uma saída que destrava sem entregar a resposta.
O exercício costuma ocupar entre um quarto e um terço da aula; o tamanho certo é o que o
aluno precisa para fazer, e não uma cota.

**Fecho, sem cabeçalho, em 3 a 5 linhas.** O que mudou no negócio dele depois desta aula,
dito pelo exemplo do H2 2, e uma única ponte para a próxima aula (verbo no imperativo com
objeto visível: abra, anote, liste, calcule, publique). Não resuma o que ele acabou de ler.

Objetivos formais, pré-requisitos, glossário, FAQ e fontes datadas vivem no nível da trilha,
uma vez; não entram na aula.

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
- Aviso legal genérico ("consulte um advogado", "conforme a legislação vigente", "de acordo
  com a LGPD", "isenção de responsabilidade"). Lei entra só quando muda a decisão do aluno, e
  entra com número: qual lei, qual artigo, qual prazo, qual valor.

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

1. A primeira frase diz o que o aluno vai conseguir fazer.
2. Uma ideia só, explicada até o fim; o exemplo é um e vai do começo ao fim, com número.
3. {h2_min} a {h2_max} H2; H3 só em H2 longo; nenhum H4.
4. Extensão entre {palavras_alvo_min} e {palavras_alvo_max} palavras; o exercício tem o tamanho
   que o aluno precisa para fazer.
5. Exercício com título, etapas numeradas com dado real do aluno, resultado esperado e "se travar".
6. Nenhum número sem origem na pesquisa; no máximo 3 marcadores `[FALTA EVIDÊNCIA]`.
7. Parágrafos de {paragrafo_min} a {paragrafo_max} palavras; frases até 28.
8. Até {figuras_max} apoios visuais, todos substituindo texto.
9. Nada da lista "O que nunca entra".
10. Fecho pelo exemplo, com uma ponte para a próxima aula.
11. Acentuação completa (não, você, também, até, já, só, será, está, conteúdo, prática, código).

Comece direto pela abertura da aula, sem cabeçalho de aula (o pipeline o insere), sem título de
módulo, sem comentário HTML e sem nenhuma frase sobre este prompt ou sobre o que você fez.

--- DADOS DA PESQUISA ---
{context}
