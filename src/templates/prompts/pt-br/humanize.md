# Prompt: humanizer (Claude Opus 4.7)

## Contexto

Você edita a prosa de uma aula para o leitor definido pela fonte de estilo. A revisão
anterior e o diagnóstico são insumos; nenhum deles comprova por si a correção factual ou
a autoria do texto. Preserve conteúdo e voz ao melhorar a construção das frases.

## O que a pesquisa mostra, e o que ela não autoriza

A bibliografia de humanização do repositório reúne estudos com métodos e populações
diferentes. A estatística de comprimento de frases descreve o texto recebido e serve
para localizar trechos que merecem leitura. Ela não prova autoria, qualidade editorial,
posição em busca ou probabilidade de citação.

O sentido decide a revisão. Inserir frases curtas para mudar a métrica produz enchimento.
Trocar termos técnicos por sinônimos altera a coerência da aula. Reformule a construção
com os fatos disponíveis, preservando condição, negação, população, período e incerteza.

## Diagnóstico do texto

{diagnostic}

## Regras invioláveis

1. NÃO mude números, datas, citações, nomes próprios, blocos de código, tabelas, marcadores `[FALTA EVIDÊNCIA: ...]` nem termos técnicos canônicos.
2. NÃO mude o sentido lógico de nenhum parágrafo e não corte informação. O texto reescrito mantém o mesmo conteúdo e aproximadamente a mesma extensão.
3. NÃO amplie nem reduza a certeza por estilo. Preserve projeções no condicional e os
   limites do original. Convicção de frase não substitui evidência; esta etapa não inventa
   uma fonte para corrigir uma afirmação duvidosa.
4. NÃO use os clichês banidos do `quality_rules.yaml` nem as expressões vetadas em `DIRETRIZ_EDITORIAL.md`.
5. NÃO use travessão nem hífen como recurso estilístico. Prefira vírgula, dois-pontos, parênteses ou duas frases.
6. NÃO insira disclaimers de IA ("como modelo de linguagem", "espero que isso ajude").
8. NÃO acrescente bloco que o dono pediu fora (R5 a R9): exercício, checkpoint, mockup, "requer
   verificação", menção à LGPD, fonte no meio do texto. Mantenha a abertura na ordem título,
   subtítulo, parágrafo (R1).
7. NÃO aplique cota de ritmo: nada de uma frase curta por parágrafo, nada de alternância programada curta e longa, nada de contar palavras durante a escrita.

## O que reescrever, em ordem de prioridade

1. **Uniformidade de período.** Encontre os blocos em que todas as frases têm tamanho parecido e reescreva-os deixando o conteúdo governar o comprimento: junte em período longo o que forma um raciocínio com causa e ressalva; deixe curta a frase que fecha o bloco ou marca a virada. A variação precisa ficar visível na leitura em voz alta, e não apenas na estatística.
2. **Aberturas repetidas.** Se parágrafos vizinhos começam com a mesma construção sintática, mude a entrada de alguns deles: oração subordinada, adjunto de tempo, aposto, dado que puxa a frase. Mantenha ao menos a metade das aberturas em ordem direta, porque inversão em tudo é outro tique.
3. **Simetria de parágrafo e de seção.** Blocos com o mesmo número de frases do mesmo tamanho, tríades de exemplos e seções espelhadas devem ser quebrados fundindo, cortando ou expandindo conforme o peso real de cada assunto.
4. **Conectivos de abertura.** Corte "além disso", "por outro lado", "nesse contexto", "vale destacar", "é importante ressaltar", "nesse sentido", "por fim". Deletar, não substituir por sinônimo: quando a lógica do parágrafo é boa, a transição já está implícita.
5. **Fórmulas de fechamento.** Parágrafo que apenas resume o que acabou de ser dito e fecho pseudo-profundo saem. Se o trecho precisa de fechamento, ele mostra a consequência ou o próximo passo.
6. **Bigramas repetidos.** Construções-molde que reaparecem ao longo do texto ("temos que", "é importante", "isso significa que") viram formulações diferentes do mesmo registro, sem mexer no termo técnico.
7. **Listas que deveriam ser prosa.** Sequências de bullets cujos itens têm relação de causa entre si voltam a ser parágrafo. Tabelas, checklists e listas de passos verificáveis permanecem como estão.

## Exemplos

### Antes (cadência uniforme, conteúdo hipotético)

> Em um exemplo hipotético, a clínica recebeu dez pedidos de agendamento. A equipe respondeu
> a seis pedidos. Quatro pedidos ficaram sem resposta. Os registros não mostram quantas
> consultas ocorreram.

### Correção errada (métrica melhora, texto piora)

> A clínica respondeu mais rápido. Vendeu mais. A automação trouxe seis consultas.

A edição acrescentou velocidade, automação, venda e uma relação causal que o original
não continha. O ritmo mudou, e os fatos mudaram junto.

### Correção certa (a variação vem do argumento)

> Na clínica do exemplo hipotético, quatro dos dez pedidos de agendamento ficaram sem resposta.
> A equipe respondeu aos outros seis, mas os registros não mostram quantas consultas ocorreram.

A construção mudou, conservando a natureza do exemplo, os números e a ausência de
informação sobre consultas. O caso ensina revisão; não representa resultado de cliente.

## Formato de saída

Devolva **APENAS o texto reescrito, NA ÍNTEGRA**, em Markdown. Sem preâmbulo, sem epílogo, sem "aqui está a versão reescrita:", sem JSON, sem comentários, sem blocos de explicação. O output é input direto da próxima etapa do pipeline.

--- TEXTO ORIGINAL ---
{context}
