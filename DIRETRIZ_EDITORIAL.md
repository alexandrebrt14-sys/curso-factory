# Diretriz Editorial Permanente

Versão 3, de 11 de agosto de 2026. A versão 2 (23 de julho de 2026) foi revisada depois que o curador constatou queda de qualidade nos conteúdos produzidos sob as regras então vigentes.

O diagnóstico encontrou uma doutrina construída quase inteiramente de mecanismos de reprovação: 46 expressões banidas com gate de CI, orçamento de formatação, tetos de bloco e de marcador, trava de estilometria. Nenhuma regra dizia o que a peça precisa ter, e o resultado é mecânico: texto curto, uniforme e sem argumento passa em todos os gates, porque nenhum deles mede substância. Somam-se a isso quatro causas específicas: cotas de cadência aritmeticamente insatisfazíveis nos prompts do pipeline, cotas de formatação que fragmentavam os textos, camadas de orientação contraditórias acumuladas e ausência completa de técnica narrativa.

Esta versão corrige as cinco: instala o piso de substância (seção 2.1), o storytelling como obrigação editorial (seção 3) e o diagnóstico de ritmo em duas faixas, incombinável com qualquer outra regra de comprimento (seção 4); recoloca a estrutura visual a serviço da leitura e da decisão (seção 6); e passa a ser a fonte única do padrão, à qual prompts e demais documentos devem se subordinar. O anexo prático `GUIA_ESCRITA_HUMANIZADA.md`, na raiz deste repositório, traz exemplos antes e depois, heurísticas mensuráveis e as fontes da pesquisa.

Este documento define o padrão editorial, técnico e comportamental deste repositório. Ele vale para todo agente de IA (Claude Code, Codex, Gemini CLI e equivalentes) e para todo colaborador que produza texto, documentação, cursos, relatórios, código ou artefatos aqui. Quando houver conflito entre velocidade e qualidade, prevalece a qualidade. Quando houver conflito entre uma convenção genérica e uma convenção explícita deste repositório, prevalece a do repositório, desde que isso não comprometa segurança, corretude ou requisitos informados pelo usuário.

O objetivo é que cada texto produzido aqui seja indistinguível do trabalho de um especialista experiente: consultor sênior, pesquisador, arquiteto de software ou executivo que domina o assunto. A referência editorial são publicações de alto nível em gestão, estratégia, tecnologia e engenharia de software, nas quais o raciocínio, a evidência e a utilidade prática valem mais do que o volume de palavras.

## 1. Idioma e formatação de base

Todo conteúdo de leitura humana é escrito em português do Brasil com acentuação completa. ASCII puro fica restrito a slugs, URLs, paths, identificadores, nomes de arquivo e de variável e imports. Em superfícies que suportam formatação de parágrafo (HTML, PDF, documentos gerados), os parágrafos usam alinhamento justificado (`text-align: justify`). Em Markdown puro, escreva parágrafos coesos em bloco contínuo, sem quebras artificiais no meio da frase.

Tipografia à brasileira, porque o padrão inglês em texto português é marca de tradução automática: títulos com maiúscula apenas na primeira palavra e em nomes próprios (title case é anglicismo); números de zero a dez por extenso e algarismos a partir de 11; vírgula como separador decimal e ponto no milhar; porcentagem com símbolo colado ao número (25%); siglas de até três letras em caixa alta (ONU, PIB) e siglas pronunciáveis de quatro ou mais letras só com inicial maiúscula (Ibama, Unesco), explicadas na primeira ocorrência. O registro fica fixo do início ao fim: norma culta acessível, tratamento por "você", sem mesóclise e sem oscilar entre formalidade de cartório e coloquialidade de rede social.

## 2. Estrutura do raciocínio

Desenvolva sempre uma linha de raciocínio lógica, com a conclusão antes da sustentação. Cada parágrafo deve acrescentar uma ideia nova; se um parágrafo apenas repete o anterior com outras palavras, ele deve ser cortado. Respostas infladas para parecer completas são um defeito, e respostas rasas diante de problemas complexos também. A profundidade certa é proporcional à complexidade do problema.

Explique causas, consequências, alternativas, riscos, benefícios, limitações e critérios de decisão sempre que forem relevantes. Quando existir mais de uma solução possível, compare as alternativas, explicite os critérios usados para escolher entre elas e indique em quais cenários cada abordagem funciona melhor. Uma matriz de decisão ou tabela comparativa costuma ser a forma mais honesta de registrar essa comparação: critérios nas linhas, alternativas nas colunas, e a recomendação justificada na prosa que a acompanha.

Toda atribuição é nomeada. Fórmulas como "especialistas apontam" e "estudos mostram" sem fonte identificável são um dos marcadores mais documentados de texto sintético e estão vetadas: diga qual estudo, de quem, de quando. Números vêm com fonte e data; número sem proveniência verificável não entra no texto.

### 2.1 Piso de substância: o que toda peça precisa ter

As seções seguintes deste documento listam sobretudo o que evitar, e uma doutrina feita só de proibição tem um furo previsível: texto curto, uniforme e sem argumento não viola nenhuma regra e mesmo assim não serve. Os gates automáticos do repositório agravam isso, porque medem forma (acento, clichê, contagem, marcação) e não conseguem medir substância. Aprovação nos gates nunca equivale a aprovação editorial.

Antes de olhar para o que cortar, verifique se a peça tem:

1. **Uma tese identificável.** Uma frase que o autor defende e com a qual seria possível discordar. Compilação neutra do que já existe não é peça pronta.
2. **Evidência que sustenta a tese**, e não números avulsos decorando o texto. Cada dado importante precisa estar ligado ao argumento que ele serve.
3. **Ganho de informação.** Ao menos um dado, caso, comparação ou framework que o leitor não acharia nas primeiras páginas de qualquer busca sobre o tema. Sem isso, a peça é redundante mesmo estando correta.
4. **Critério de decisão explícito** quando houver alternativas: o que compara, com quais critérios, e qual a recomendação com o seu porquê.
5. **Arco de leitura** conforme a seção 3: abertura em situação, tensão, desenvolvimento que paga a promessa e fechamento que retoma.
6. **Consequência para o leitor.** O que ele faz diferente depois de ler, dito de forma que dê para executar.

Peça que falha em qualquer um destes seis itens não é corrigida cortando trechos; é reescrita ou devolvida ao autor. Nenhuma regra de estilo deste documento autoriza sacrificar um dos seis para cumprir uma proibição: quando a proibição e o piso de substância entrarem em conflito, o piso vence e o trecho é reformulado até cumprir os dois.

## 3. Narrativa e engajamento

Profundidade que ninguém lê não ensina nada. O texto precisa prender o leitor pelo interesse, nunca pelo artifício, e as técnicas que sustentam isso em publicação de negócios de alto nível são conhecidas. As seis abaixo são obrigatórias em conteúdo de leitura humana com mais de algumas centenas de palavras (artigo, aula, landing page, capítulo, post longo):

1. Abertura em situação, não em definição. Comece por uma cena concreta, um caso, um número que contraria a expectativa ou uma decisão difícil que o leitor reconhece da própria rotina. A definição chega depois, quando o leitor já sabe por que precisa dela. Abrir com "X é..." ou com cenário genérico desperdiça a frase mais lida do texto.
2. Tensão real antes da solução. Antes de apresentar a resposta, deixe claro o que está em jogo: o custo de errar, o ganho de acertar, o prazo que aperta, com dado quando houver. Solução sem tensão chega como catálogo.
3. Caso condutor. Quando houver material, conduza o argumento por um caso nomeado (empresa, projeto, situação) que atravessa o texto e reaparece nos exemplos. Caso real vem de fonte verificável; cenário hipotético é sinalizado como tal; caso inventado apresentado como real é defeito grave (regra de proveniência da seção 8).
4. Loop aberto honesto. A abertura promete algo que o texto entrega de verdade, e o leitor percebe a promessa sendo cumprida. Curiosity gap fabricado ("o que descobrimos vai te surpreender") é isca, não narrativa, e está vetado.
5. Fechamento com callback. O final retoma o caso ou a tensão da abertura e mostra a resolução que o desenvolvimento construiu. Isso substitui o parágrafo-recap proibido na seção 5: em vez de repetir o que foi dito, o fechamento mostra o que mudou.
6. Mostrar antes de qualificar. Em vez de afirmar que algo é grave, transformador ou urgente, mostre o prejuízo, o ganho ou o prazo em número e consequência. O leitor conclui a gravidade sozinho, e conclusão própria persuade mais que adjetivo alheio.

O limite é o mesmo de toda técnica: a história serve ao argumento. Drama fabricado, suspense artificial e anedota que não sustenta a tese saem do texto junto com os clichês. Quando a história e a tese competem, corta-se a história.

## 4. Humanização da escrita

A pesquisa de 2026 mostra que a detecção de texto de IA migrou do vocabulário isolado para padrões estruturais: uniformidade de ritmo, simetria de parágrafos e fórmulas de abertura e fechamento persistem mesmo nos modelos mais recentes. As regras a seguir atacam esses padrões na origem.

1. Varie o ritmo de verdade. Texto de modelo concentra quase todas as frases numa faixa estreita de comprimento; escrita humana vai da frase de quatro palavras ao período de cinquenta. O diagnóstico se aplica ao texto pronto, em duas faixas: num bloco de dez frases, diferença abaixo de 15 palavras entre a mais longa e a mais curta é defeito e pede reescrita daquele trecho; acima de 30 é folgadamente compatível com escrita humana. O intervalo entre as duas é aceitável quando a variação acompanha o argumento. Nada disso é alvo a perseguir durante a escrita, e nenhuma outra regra de comprimento (crescimento por frase, teto por parágrafo, ração de frase curta) pode ser combinada com este diagnóstico: a soma dessas regras é aritmeticamente insatisfazível e produz exatamente a faixa estreita que ela diz combater. A variação emerge do sentido, com frase curta para ênfase e período longo para desenvolvimento; alternância mecânica de curta e longa soa tão artificial quanto a uniformidade.
2. Não abra parágrafos sucessivos com a mesma construção sintática. O mesmo início aparecendo três vezes no texto é sinal de falha.
3. Corte conectivos por subtração, sem trocar por sinônimo. "Além disso", "por outro lado", "nesse contexto", "vale destacar", "é importante ressaltar", "nesse sentido", "em suma", "por fim": a maioria sai sem perda de sentido quando a lógica do texto é boa. Trocar "além disso" por "ademais" mantém o ritmo metronômico e ainda soma um cacoete.
4. Nada de clichês nem frases genéricas que caberiam em qualquer assunto. Aberturas de cenário ("no cenário atual em constante evolução"), meta-comentário ("nesta seção veremos") e parágrafo final que apenas resume o que acabou de ser dito devem ser cortados.
5. Exemplos devem ser concretos, nomeados e plausíveis. Tenha opinião e assuma posição quando o assunto pedir; neutralidade relutante e hedging uniforme em todas as afirmações são marcas de máquina, não de prudência.
6. O tom é o de um especialista experiente conversando com outro profissional experiente: sem promoção, sem entusiasmo excessivo, sem adjetivos desnecessários. Precisão vale mais que ênfase.
7. Medição do próprio corpus descreve, não prescreve. Número extraído dos textos da casa entra como descrição do registro que a casa pratica, e só ganha estatuto de regra depois de passar por dois testes. O primeiro é o de registro: fala transcrita, locução gravada e conversa não governam forma de página escrita, então corpus dessa natureza fica fora da amostra que define forma. O segundo é o de compatibilidade: o limiar novo precisa ser satisfazível junto com todos os que já valem, e quem propõe faz a conta antes de publicar. A doutrina anterior falhou nos dois, e o resultado foi uma fôrma de parágrafo derivada majoritariamente de conversa transcrita e aritmeticamente incompatível com a tabela de limiares que a acompanhava: as regras de crescimento produziam amplitude perto de 13 a 16 palavras, e a última linha da mesma tabela exigia mais de 30. Três linhas reprovavam a quarta, e quem tentava obedecer às quatro escrevia a faixa estreita que a diretriz classifica como assinatura de máquina.
8. Nenhuma cota mecânica de ritmo, nunca. Regras do tipo "uma frase curta em cada parágrafo" ou "nunca duas frases seguidas do mesmo tamanho" produzem um staccato de manchete que os catálogos de detecção listam como assinatura de máquina tanto quanto a uniformidade que pretendiam corrigir; foi o principal cacoete introduzido pela geração anterior deste pipeline. O diagnóstico de amplitude do item 1 mede o texto pronto e aponta onde reescrever; ele nunca vira fórmula de produção, contagem de palavras durante a escrita ou alternância programada.

## 5. Estruturas proibidas

Os padrões abaixo estão documentados em catálogos de 2026 como assinaturas de texto gerado por modelo. Nenhum deles pode aparecer como padrão recorrente; a maioria não deve aparecer nunca.

- A construção que nega uma ideia para afirmar a oposta: "Não se trata de X. Trata-se de Y.", "Não é apenas X. É Y.", "Não basta X. É preciso Y.", "Mais do que X, Y." e o calque "não é sobre X, é sobre Y". Tolerada apenas em ocasião isolada, quando realmente melhorar a clareza.
- A regra de três mecânica: tríades de adjetivos, de benefícios, de exemplos, de seções. Quando três itens forem genuínos, tudo bem; a tríade como tique de ritmo, não.
- Inflação de significância: "marca um momento crucial", "é um testemunho de", "representa um divisor de águas". Se algo importa, mostre a consequência concreta.
- Conclusões-espelho que reafirmam a abertura e fechos pseudo-profundos ("O futuro não está chegando. Já chegou.").
- Fuga da cópula simples: "serve como", "atua como", "funciona como" onde "é" resolve.
- Gerúndio analítico vago encerrando frases: "contribuindo para", "promovendo", "impulsionando".
- Perguntas retóricas repetidas, conclusões idênticas em tópicos sucessivos e excesso de paralelismo sintático.

## 6. Pontuação, estilo e estrutura visual

Não use travessão. Em 2026 os modelos aprenderam a evitá-lo quando instruídos, e a frequência dele deixou de ser um detector confiável; a regra desta casa permanece por outra razão: quase sempre existe construção mais fluida com vírgulas, parênteses ou duas frases. Não use hífen como recurso estilístico. A pontuação é a tradicional, sem vírgula antes do "e" em enumeração simples (a vírgula de Oxford é anglicismo) e nunca entre sujeito e verbo.

Formatação tem orçamento, e o orçamento existe para proteger o destaque do que merece destaque. Negrito só em termos que o leitor precisará reencontrar ao escanear a página; destacar palavras por hábito dilui o destaque de todas. No máximo uma analogia por texto.

Elementos estruturados são ferramentas de consultoria, não enfeite, e devem ser usados sempre que organizarem informação genuinamente comparável, sequencial ou verificável: tabela comparativa quando há alternativas com critérios, matriz de decisão quando o leitor precisa escolher, checklist quando há passos verificáveis, lista numerada quando a ordem importa, fluxo de trabalho quando há processo, resumo executivo quando o documento é longo o bastante para ser lido em dois níveis. Um profissional decide mais rápido com uma matriz bem construída do que com três parágrafos de prosa equivalente. A proibição atinge outra coisa: lista que substitui argumentação, bullets que escondem relação de causa entre os itens (esses viram prosa), série de "termo em negrito: explicação" como esqueleto de seção e o texto inteiro fatiado em fragmentos escaneáveis sem um parágrafo desenvolvido. Prosa carrega raciocínio; estrutura carrega comparação, sequência e verificação. Cada formato faz o seu trabalho, e nenhum dos dois entra por cota.

## 7. Vícios de português gerado por IA

Modelos escrevendo português do Brasil produzem vícios próprios, na maioria calques do inglês. Os principais, com o conserto:

- Gerundismo: "vamos estar enviando" vira "enviaremos". O gerúndio legítimo de ação em curso continua normal.
- Falsos cognatos: "endereçar um problema" vira "tratar de" ou "resolver"; software "suporta" vira "é compatível com" ou "aceita"; "eventualmente" no sentido de "no fim" vira "mais cedo ou mais tarde" (em português significa "ocasionalmente"); "assumir" no sentido de supor vira "supor" ou "presumir"; "aplicar para" vira "candidatar-se a"; "realizar" no sentido de perceber vira "perceber" ou "dar-se conta".
- Calques de estrutura: "espero que esta mensagem o encontre bem" se corta; possessivo excessivo ("lave suas mãos") vira artigo ("lave as mãos"); sujeito pronominal repetido em toda frase dá lugar ao sujeito oculto natural do português.
- Adjetivos vazios e vocabulário etéreo: "robusto", "crucial", "fascinante", "transformador", "disruptivo", "jornada", "essência", "mergulhar em", "abordagem holística". O conserto nunca é o sinônimo; é substituir o adjetivo pelo dado, pelo número ou pela consequência que o justificaria.
- Voz passiva e nominalização em cadeia: "foi realizada a implementação da solução" vira "implementamos a solução". Ordem direta como norma, passiva só quando o agente é irrelevante ou desconhecido.

## 8. Profundidade técnica e honestidade de proveniência

Ao explicar um conceito técnico, cubra o que for pertinente entre contexto, motivação, funcionamento, benefícios, limitações, impactos, boas práticas, erros comuns e critérios de decisão. Toda recomendação vem acompanhada do seu motivo; regra sem porquê não ensina e não convence.

O que só o autor humano pode fornecer não se inventa. Quando o texto pedir um caso vivido, um número proprietário ou uma posição de negócio que o agente não tem como saber, o agente deixa o marcador `[PREENCHER-HUMANO: descrição do que falta]` no lugar, em vez de fabricar experiência. Texto com dado inventado é defeito grave, não rascunho aproveitável.

## 9. Escrita para leitores e para motores generativos

Os sites deste ecossistema precisam ser citáveis por motores de busca generativos sem soar sintéticos para leitores humanos. A pesquisa de 2026 (incluindo o guia oficial do Google de maio de 2026) indica que essa tensão é menor do que parece: o que determina citação é relevância e evidência extraível, que a boa prosa também exige. As regras de conciliação:

- Abra cada seção interna com uma cápsula de resposta autossuficiente: uma ou duas frases declarativas que respondem a pergunta do título, com a entidade e um dado. Depois desenvolva com voz, opinião e contexto. Enterrar a resposta sob abertura anedótica prejudica leitor e máquina.
- A cápsula convive com a narrativa, e a divisão de trabalho é clara: a abertura do texto inteiro (o lede) usa as técnicas da seção 3 para prender o leitor; as seções internas, com headings que são perguntas reais, abrem com resposta direta. Um artigo pode instalar tensão na abertura e ainda assim entregar resposta extraível em cada H2.
- Dados proprietários, datados e com metodologia valem mais que dez listas. Um número seu, com data e fonte, é o diferencial de citação com melhor evidência.
- Demonstre experiência de primeira mão no próprio texto: o caso concreto, com quando e o que mudou, e não só afirmações de autoridade.
- Não fragmente o texto artificialmente para "facilitar para a IA": os sistemas extraem a passagem relevante de páginas multitópico. Headings que são perguntas reais do público e seções que se sustentam sozinhas bastam.
- Reescrita mecânica "para citação" e publicação de IA em massa sem revisão editorial destroem os dois públicos ao mesmo tempo; conteúdo em escala sem valor é alvo declarado de rebaixamento desde março de 2026.

## 10. Aprendizado a partir do repositório

Trate este repositório como fonte de conhecimento para o trabalho nele. Analise arquitetura, organização, documentação, convenções, padrões de código, decisões registradas (READMEs, ADRs, guias de contribuição, especificações) e fluxos de trabalho, e use esse conhecimento para manter consistência em tudo o que produzir. Convenção explícita do projeto prevalece sobre convenção genérica, com a única ressalva de segurança e corretude.

## 11. Conteúdo educacional

Documentação, tutoriais, cursos e materiais de aprendizagem começam pelo problema que será resolvido e pelo motivo de aquele conhecimento importar, e a seção 3 vale integralmente aqui: o problema chega como situação concreta, com tensão e custo, antes da teoria que o resolve. Conecte o tema a situações reais, apresente exemplos completos, use estudos de caso quando fizer sentido, proponha exercícios contextualizados e feche com uma síntese prática que o leitor consiga aplicar, retomando o caso da abertura quando houver um.

## 12. Código

Código limpo e legível, com nomes consistentes e sem complexidade desnecessária. Decisões arquiteturais relevantes são explicadas. Sugestões de refatoração vêm com os ganhos esperados. Comentários existem para registrar restrições que o código não consegue mostrar, nunca para narrar o óbvio.

## 13. Fluxo de revisão obrigatório

Antes de entregar qualquer texto, revise em três passadas, nesta ordem, porque polir frase antes de consertar estrutura desperdiça a passada: primeiro substância (os seis itens da seção 2.1, mais fatos, datas, fontes e se há dado inventado ou marcador `[PREENCHER-HUMANO]` pendente); depois estrutura (organização, arco narrativo da seção 3, seções redundantes, simetria artificial, parágrafo-recap, e se a abertura prende e o fechamento retoma); por último linguagem, contra a lista deste documento: ritmo dos períodos, aberturas de parágrafo, conectivos, estruturas proibidas da seção 5, vícios de português da seção 7, orçamento de formatação da seção 6.

Dois testes baratos fecham a revisão: a leitura em voz alta (frase que trava a língua trava o leitor) e o teste do bloco de dez frases da seção 4. O conserto de um trecho reprovado é a reescrita da estrutura, nunca a troca de palavras por sinônimos, que mantém o ritmo sintético e cria um cacoete novo. Um texto que precisa ser relido para ser entendido desperdiça o tempo que a concisão fingiu economizar.
