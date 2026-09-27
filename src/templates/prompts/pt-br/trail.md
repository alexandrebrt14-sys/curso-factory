# Prompt: fechamento da trilha (GPT-5.5)

## O que é

Uma trilha é um módulo de 4 a 6 aulas. As aulas já estão escritas. Você escreve só o que vive
no nível da TRILHA, uma vez: o que o aluno vai saber fazer, o que precisa antes, o glossário, as
perguntas frequentes e as fontes datadas. Nada disso entra em cada aula; entra aqui.

O leitor é o dono de um pequeno negócio, leigo em marketing e tecnologia, no celular. Português
do Brasil com acentuação completa, sem emoji, sem travessão, sem clichê.

## A trilha

- Curso: {course_name} (nível {course_level})
- Trilha {module_number}: {module_title}. {module_description}
- Aulas, na ordem: {lesson_titles}

## Anti-invenção (inviolável)

Toda fonte listada precisa aparecer no texto das aulas ou na pesquisa abaixo, com nome e data.
Fonte que não estiver em nenhum dos dois não entra. Se as aulas citam um dado sem fonte, não
crie a fonte: deixe o dado fora da lista.

## O que escrever, nesta ordem e com estes cabeçalhos

## O que você vai saber fazer

De três a cinco frases, uma por linha, cada uma começando por um verbo de ação no infinitivo
(analisar, comparar, calcular, montar, aplicar, escolher, medir, publicar). Nunca "entender",
"conhecer", "saber", "aprender". Cada frase nomeia um resultado que ele consegue conferir no
próprio negócio.

## Antes de começar

De um a três pré-requisitos, em uma linha cada: o que ele precisa ter em mãos (conta, dado,
ferramenta) ou já saber. Se a trilha não depende de nada, escreva uma linha dizendo isso.

## Glossário

Os termos técnicos que as aulas usam, em ordem alfabética, cada um com glosa de até {glosa_max_palavras}
palavras e uma comparação do dia a dia dele, no molde "spring: jeito de animar que imita uma
mola: em vez de mandar o movimento durar um tempo fixo, você diz o quanto ele é firme e o
quanto desacelera". Formato: `**termo**: glosa`. Entre cinco e doze termos; só o que as aulas
de fato usam. Nome de API cru sem a explicação prática não entra.

## Perguntas frequentes

De três a seis perguntas que o dono do negócio faria depois de terminar a trilha, cada uma
com resposta de duas a quatro frases, direta, sem preâmbulo. Pergunta em negrito, resposta em
prosa logo abaixo.

## Fontes

Uma linha por fonte, no formato `Nome da fonte, título ou relatório, data de publicação` (dia,
mês e ano; mês e ano quando o documento não traz o dia) e, quando houver, o link logo depois, só
com o que as aulas ou a pesquisa trazem. Fonte que é a origem do conceito (artigo fundador,
norma) leva "(origem do conceito)" depois da data. De uma a oito fontes.
É o ÚLTIMO bloco da trilha e o único lugar do curso onde fonte aparece (R7): cada linha tem até
{fonte_max_palavras} palavras, sem comentário, sem card, sem citação em destaque. Ela é desenhada no rodapé da
página, em corpo pequeno.

{bloco_fontes_recentes}

## Subtítulo da trilha

Se o pipeline pedir a descrição da trilha, ela é UMA promessa em até {subtitulo_max_palavras} palavras, sem fórmula
fixa ("Você sai com...") e sem corrente de vírgulas empilhando as promessas de cada aula. As
trilhas de um curso não podem começar todas com as mesmas duas palavras.

## Antes de entregar, confira

1. Cinco seções, nesta ordem, cada uma com o cabeçalho acima como H2; "Fontes" é a última.
6. Nenhum exercício, checkpoint, mockup, "requer verificação" nem menção à LGPD (R5 a R9).
2. Verbos de ação nos objetivos; nenhum "entender" ou "conhecer".
3. Glosa de até {glosa_max_palavras} palavras por termo; nenhum termo que as aulas não usem.
4. Nenhuma fonte inventada.
5. Frases de até {frase_max_palavras} palavras; sem travessão; acentuação completa.

Comece direto pelo primeiro H2, sem título de trilha (o pipeline o insere) e sem comentário
sobre este prompt.

--- AULAS DA TRILHA ---
{lessons}

--- DADOS DA PESQUISA ---
{context}
