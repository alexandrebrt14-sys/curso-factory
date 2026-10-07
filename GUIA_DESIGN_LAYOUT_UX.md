# Guia de design, layout e experiência de uso do curso gerado

*Como a página de curso, o capítulo, o índice, a figura, a tabela, o painel de números e o rodapé que esta fábrica emite conversam com a aula que ela já sabe escrever.*

Versão 1, de 07 de outubro de 2026. Complementa `DIRETRIZ_EDITORIAL.md` (o que a aula diz), `docs/DOUTRINA_VISUAL_CURSOS.md` (quantas peças visuais a aula leva e qual peça resolve qual defeito) e `docs/FRONTEND_PLAYBOOK.md` (como auditar contraste, animação e tema na saída renderizada). Este guia cuida do que faltava entre os três: a hierarquia que o leitor vê antes de ler, o caminho entre os capítulos, o rótulo do botão, o estado vazio, a legenda, o número no painel e a conferência final no celular. Os critérios vêm do guia "Frontends com vibecoding" (fonte no rodapé) e seguem a mesma regra dos documentos irmãos de `escrita-empreendedor`, `Escrita-Empresarial` e `Geo-Leadlovers`: critério com número vence gosto, e nenhum item daqui cria gate novo, piso novo ou teto novo. O que virou código nesta rodada está na seção 12.

Este repositório gera curso. A pergunta que ele faz não é "a tela ficou bonita", e sim **o que o template emite, o que o redator escreve e o que a revisão confere para que a aula chegue inteira a quem lê no celular, em poucos minutos**. O documento responde nessa ordem: o que a fábrica desenha hoje (seção 1), os critérios por superfície (seções 2 a 10), a lista de conferência (seção 11) e o estado da implementação (seção 12).

## 1. O que a fábrica desenha, e onde cada decisão mora

A fábrica escreve Markdown por aula, converte em `CourseDefinition` e renderiza três artefatos. A decisão de design de cada um vive num arquivo, e corrigir fora dele é remendo que o próximo curso não herda.

| Superfície gerada | Arquivo que decide | O que já cumpre | O que este guia acrescenta |
|---|---|---|---|
| Página do curso (abertura, capítulos em acordeão, FAQ, autor, pré-requisitos, fontes, JSON-LD) | `src/templates/page.tsx.j2` | Abertura R1 a R9, um caminho linear, fontes no rodapé em 0,8 rem, tokens de cor, tabela que rola dentro do bloco, parágrafo justificado | Alvo de toque, foco visível, acordeão anunciado ao leitor de tela, movimento reduzido, figura com `alt`, `width` e `height` e carregamento tardio (seção 12) |
| Metadados da página (`title`, `description`, canônica, Open Graph) | `src/templates/layout.tsx.j2` e `CourseDefinition` em `src/models.py` | Uma descrição por página (R4), URL canônica, `inLanguage: pt-BR` | Descrição entre 150 e 160 caracteres, conferida na geração como aviso (seção 12) |
| Peças visuais (`figure`, `dataTable`, `comparison`, `statGrid`, `stepGuide`, `timeline`) | `src/models.py`, `src/schemas/course.schema.json`, `page.tsx.j2`, `tsx_generator.py` (os quatro lugares da doutrina) | Payload validado, valência fixa do comparativo, cor por token | Legenda que afirma, uma pergunta por painel, eixo e denominador escritos, tabela até três colunas de texto no celular (seções 6 e 8) |
| Texto das peças e dos rótulos | `src/templates/prompts/pt-br/draft.md`, `review.md`, `trail.md` | Registro da aula em ficha, dica, legenda e célula | Camada visual no prompt: legenda, alt, rótulo de passo, número com unidade e período (seção 12) |
| Certificado em HTML | `src/templates/certificate.html.j2` | `lang`, `title`, `meta description`, `alt` no QR | Nada muda: superfície de impressão, cor fixa coerente com texto fixo (seção 4) |
| Portal que recebe o curso (player de mídia, busca, quiz, barra de progresso) | landing-page-geo (`src/app/educacao/`) | Fora do alcance deste repositório | Critérios para quem monta lá o curso gerado aqui (seções 7 e 9) |

A regra que organiza o resto cabe numa frase, a mesma dos documentos irmãos: **uma tela responde a uma pergunta e sustenta uma decisão; o que disputa atenção com essa decisão sai.** Na página de curso, a pergunta é "o que eu consigo fazer depois desta aula?", e a decisão é abrir o próximo capítulo ou fechar o celular com o passo anotado.

## 2. Hierarquia visual a serviço da aula

**D1. A abertura visual é a abertura R1.** O leitor chega pela busca ou pelo catálogo e dá menos de um minuto. O template abre com H1, subtítulo em uma frase e o parágrafo de descrição, sobre o degradê do curso; depois vêm os capítulos. Nada antes do H1 além do breadcrumb, nada entre H1 e módulos: sem barra de estatísticas, sem barra de progresso fixa, sem índice lateral, sem card "o que você vai aprender". O teste `tests/test_abertura_sem_distracao.py` mede isso no template e continua valendo.

**D2. Uma decisão por capítulo, um elemento memorável por página.** O único lugar de ousadia visual da página do curso é o degradê da abertura (`hero_gradient_from` e `hero_gradient_to`). Dentro do capítulo, a hierarquia é feita por tamanho e espaço: H3 do capítulo em 18 px negrito, subtítulo em 14 px, corpo em 15 px, H4 interno em 15 px negrito com linha abaixo. Dez efeitos espalhados dispersam; um degradê bem escolhido rende lembrança.

**D3. Cartão só onde há item repetido.** O capítulo é um cartão porque se repete com dados diferentes; a FAQ é uma lista de `details` porque se repete. A prosa do capítulo corre em coluna, sem caixinha. Quem monta o curso na landing não parte os parágrafos em cards com a mesma sombra: é o sinal mais comum de página que ninguém desenhou.

Antes: três parágrafos do capítulo, cada um dentro de um card com ícone e sombra, e um rótulo "CONCEITO" em caixa alta acima de cada um.
Depois: os três parágrafos em coluna, com um H4 acima quando o assunto muda; o card fica para a comparação (`comparison`) e para o painel de números (`statGrid`).

**D4. Cinco padrões genéricos têm nome e saem pelo nome.** Fundo creme com título em serifa e detalhe cor de argila; fundo quase preto com um único verde ácido; fios finos, canto reto e colunas densas de jornal; tudo em cartões iguais; rótulo em caixa alta acima de cada título, ponto no meio entre metadados e seta no texto do botão. O template não emite nenhum dos cinco; quem muda o template ou monta a landing recusa os cinco pelo nome, e não por "não pareça feito por IA".

**D5. O curso parece do autor, não da ferramenta.** Teste do sósia: esconda logotipo e nome, mostre a abertura e um capítulo a alguém de fora e anote a resposta literal. "Alguma empresa de tecnologia" é a resposta da ferramenta; o ramo do aluno (oficina, clínica, loja) é a resposta da marca. O texto ajuda quando usa o vocabulário do balcão que o prompt já pede; o visual ajuda quando o degradê e os ícones dos capítulos vêm do cliente (`config/clients/<id>/client.yaml`), e nunca do padrão da ferramenta.

## 3. Tipografia e espaçamento

Os números da coluna de leitura são os da fonte de estilo (`MOLDES_DE_PAGINA.md`, seção 4, espelhada em `config/lexicos.json`): coluna de 640 a 720 px, corpo nunca abaixo de 16 px, entrelinha 1,6, H1 de 32 a 40 px. O template cumpre a coluna (`max-w-3xl`, 768 px com o recuo dos ícones), o H1 (`clamp(28px, 4vw, 44px)`) e a entrelinha (`leading-[1.75]`). Os critérios abaixo somam a esses sem mudar nenhum.

**D6. Linha de até 80 caracteres.** A coluna existe para isso: linha mais longa perde o leitor na volta, mais curta pica a frase. Em 390 px a coluna é a tela menos as margens de 24 px (`px-6`). O teto de 1.200 caracteres por parágrafo da doutrina visual é o irmão desta regra na vertical: ambos medem o que cabe no celular sem rolar dentro do próprio bloco.

**D7. Uma escala, escrita uma vez.** O template usa quatro tamanhos de corpo (15 px na prosa, 14 px em ficha e passo, 13 px em célula de tabela, 12 px em legenda e nota) e uma escala de espaço em múltiplos de 4 px (`space-y-4`, `my-5`, `p-4`, `gap-3`). Quem acrescenta componente usa os mesmos degraus; tamanho fora da escala é o sinal de espaçamento gerado por padrão. Texto abaixo de 12 px não entra em nenhuma superfície.

**D8. Três tiques tipográficos denunciam página gerada** e saem com uma linha de instrução: uma palavra do título em cor ou itálico; rótulo em caixa alta acima do conteúdo; rótulo desnecessário. O cabeçalho de tabela em caixa alta de 13 px (`uppercase tracking-wider`) é a única caixa alta que o template emite, e é de dado, não de rótulo decorativo.

**D9. Número em coluna usa algarismos de largura igual.** `statGrid` e `dataTable` com valores que mudam pedem `tabular-nums`, para a coluna não dançar. Formato brasileiro sempre: R$ 1.234,56, 4,4x, 62%, com unidade e período na própria célula ou no rótulo.

**D10. Sentence case em tudo.** Título de capítulo, subtítulo, rótulo de botão e cabeçalho de seção levam maiúscula só na primeira letra e nos nomes próprios. O gate de `title case` da fonte já reprova na prosa; vale também para `step.title`, `data.title` e o texto do botão.

## 4. Cor, contraste e os dois temas

**D11. Dois pisos de contraste, medidos nos dois temas.** Texto normal pede 4,5:1. Texto grande (18 pt, ou 14 pt em negrito), borda de campo, anel de foco e ícone com sentido pedem 3:1. O segundo piso é o esquecido: medir só o texto aprova um acordeão em que ninguém acha a seta. A medição é no navegador renderizado, com transições mortas, nos dois temas, pelo processo da seção 6 do `docs/FRONTEND_PLAYBOOK.md`.

**D12. Cor vem do token, com papel.** `--text`, `--text-muted`, `--border`, `--card`, `--bg-muted`, `--accent`, `--accent-dark`, `--accent-lighter`, `--success`, `--success-light`, `--danger`, `--danger-light` e `--course-accent` são os tokens que a landing confirma. Hex cravado em componente novo reprova em `tests/test_template_blocos_visuais.py`. As exceções do template são deliberadas e seguem a regra "fundo fixo pede texto fixo": o bloco de código (fundo `#1e1e2e`, texto `#cdd6f4`) e o aviso (`#fff8e1` com `#5d4037`) não mudam de tema e por isso não somem em nenhum.

**D13. Tom médio da escala não recebe texto.** Numa escala de 50 a 950, o degrau 500 reprova com texto branco (3,96:1) e com texto quase-preto (4,49:1). O botão "Marcar como concluído" usa `--accent` com texto branco; quem define `--accent` para um cliente escolhe o degrau 600 ou mais escuro e mede. O degradê da abertura carrega H1 e subtítulo em branco: `hero_gradient_to` claro demais reprova o subtítulo (`text-white/90`); confira os dois extremos do degradê.

Caso da clínica. Antes: acento do cliente no degrau 500 da marca, botão de concluir com 3,96:1, o aluno mais velho não enxerga o botão no sol. Depois: acento no degrau 600 (5,51:1 com branco), medido de novo no tema escuro.

**D14. SVG de figura nasce nos dois temas.** Todo `<text>` leva o próprio `fill` por token; texto sobre a cor de acento usa `var(--course-accent-fg, #fff)`; o SVG raiz leva `role="img"` e `<title>` em português com acentuação. Regras completas na seção 6 da doutrina visual.

## 5. Layout, navegação entre capítulos e o celular de verdade

**D15. A navegação do curso é um único caminho, na ordem.** Os capítulos ficam em acordeão, um aberto por vez, o primeiro aberto ao chegar. Marcar o capítulo como concluído abre o seguinte: esse é o "próximo" da página, e não precisa de barra de botões. O breadcrumb (Início, Cursos, curso) é a única navegação antes do H1. Sem sidebar, sem sumário no topo, sem "escolha seu caminho" (R3).

**D16. Cada capítulo responde sozinho.** Quem chega por link direto (`#id-do-capitulo`) ou pela busca lê o capítulo sem o anterior. O título do capítulo é promessa com verbo (o `TÍTULO:` que o redator propõe), o subtítulo em uma frase vira a descrição do cartão fechado, e o primeiro elemento do conteúdo é parágrafo. O capítulo fechado mostra título, subtítulo e ícone: é o índice do curso, e dispensa um índice separado.

**D17. Estado que o aluno quer compartilhar vive no endereço.** Cada cartão tem `id={step.id}`, então o link com `#` leva ao capítulo. O capítulo aberto e o progresso ficam no navegador do aluno (`localStorage`) e não no endereço; é pendência conhecida, registrada na seção 12. Quem monta na landing não troca o acordeão por rolagem infinita nem por abas sem endereço.

**D18. Alvo de toque: 24 px é o piso, 44 px é o alvo, 8 px entre vizinhos.** O piso vem do critério 2.5.8 da WCAG 2.2; a Apple pede 44 e o Android, 48. No template, o cabeçalho do capítulo, o botão de concluir, a pergunta da FAQ e o botão de recomeçar têm 44 px de altura mínima; o botão de copiar código fica em 32 px porque é ação secundária dentro de uma barra de 40 px, acima do piso e com 8 px de folga. Três alvos de 24 px colados passam no piso e continuam errados.

**D19. Teclado antes do mouse.** Tab chega a todo cabeçalho de capítulo, botão e pergunta da FAQ; Enter aciona; o anel de foco aparece só para quem navega pelo teclado (`focus-visible`), em `--accent`, com 2 px e 2 px de afastamento. O cabeçalho do capítulo anuncia o estado ao leitor de tela (`aria-expanded`) e aponta o conteúdo que controla (`aria-controls`). Lista de links continua lista de links; o papel `menu` promete setas que a lista não entrega.

**D20. Celular de verdade, do botão ao teclado.** A tabela rola dentro do próprio bloco (`overflow-x-auto` com `max-w-full`), então a página nunca rola na horizontal. O comparativo empilha os dois lados abaixo de 768 px e fica lado a lado acima. O painel de números vai de uma coluna a três conforme a largura. Teste em 390 px no aparelho, com o capítulo aberto: o motor da landing monta um capítulo por vez no cliente, e o HTML servido não mostra o conteúdo.

**D21. Um cartão, não dois.** O cartão do capítulo fechado e o aberto são a mesma peça com estados diferentes (borda `--border`, `--accent` quando aberto, `--success` quando concluído). Altura mínima fixa sobra num cartão e corta texto no outro; o cartão cresce com o subtítulo.

## 6. Peças visuais: figura, tabela, comparativo, passo a passo e linha do tempo

A doutrina visual decide quantas peças entram e qual peça resolve qual defeito. Os critérios abaixo cuidam de como cada peça fica legível.

**D22. A legenda afirma um fato; o `alt` descreve a cena.** `![legenda que afirma](arquivo.svg)` vira `figure` com a legenda em `figcaption`. Quando o valor é um caminho de imagem, o template emite `<img>` com `alt` igual à legenda, `loading="lazy"`, `decoding="async"` e `width` e `height` declarados, para o conteúdo não pular quando a imagem chega. Quando o valor é SVG inline, o `<title>` do SVG faz o papel do `alt`. Legenda vazia não é promovida: a imagem continua no texto em vez de virar figura muda.

Antes: `![](grafico.png)`, legenda "Gráfico 1", e a imagem some no tema escuro porque o texto está pintado dentro dela.
Depois: `![O tempo de resposta cai de 4 horas para 12 minutos quando a oficina usa resposta automática](tempo-de-resposta.svg)`, com os rótulos em `<text fill="var(--text)">` dentro do SVG.

**D23. Texto nunca fica dentro da imagem raster.** Modelo de imagem erra palavra escrita, e o erro piora em português. Rótulo, número e legenda vão por cima, em HTML ou em `<text>` de SVG, onde o buscador lê e o tema colore. Imagem raster gerada serve para abertura e cena, nunca para informação que precise ser lida (seção 6 da doutrina).

**D24. Tabela com até três colunas de texto no celular.** A coluna do critério e duas opções, como o prompt já pede; a quarta coluna só quando é número curto. O cabeçalho é a opção, a linha é o critério, nunca o contrário. `min-w-[520px]` garante que a tabela role em vez de espremer; o `note` fica abaixo em 12 px; a fonte sobe para o rodapé (R7).

**D25. Comparativo tem valência fixa.** `left` é o lado a evitar (`--danger`, ícone de recusa) e `right` o recomendado (`--success`, ícone de acerto). Inverter o payload carimba um certo justamente no que o texto manda descartar. Os dois lados têm o mesmo número de itens, ou o leitor conclui que o lado curto é o pior.

**D26. Passo a passo: um verbo por passo, resultado observável no mesmo passo.** `label` começa pelo verbo no imperativo; `detail` diz como; `success` ("Deu certo quando") e `pitfall` ("Onde se erra") têm cor e ícone próprios, e nunca compartilham cor. `outcome` fecha com o que o aluno tem no fim. Passo sem `success` é lista de tarefas, não guia.

**D27. Linha do tempo com um marco "agora".** `tone: "now"` destaca um único evento; dois "agora" anulam o destaque. A data vem em formato brasileiro ou ano cheio; evento sem `detail` só quando o `label` fecha a ideia.

**D28. Ícone de capítulo vem do dicionário, cor herdada.** Os ícones dos capítulos (`STEP_ICONS`) saem de um dicionário só, em traço 1,75, e herdam a cor do texto (`currentColor`). Sino de uma família ao lado de engrenagem de outra denuncia montagem às pressas. Ícone ao lado de texto é decorativo; ícone sozinho exige nome acessível.

## 7. Player de mídia, quiz e formulário (para quem monta na landing)

O template deste repositório não emite player, quiz nem formulário: a aula é leitura (R6, R8), e o quiz do portal nasce de `src/engagement/quiz.py` para a trilha, fora da aula. Os critérios abaixo valem para quem monta o curso gerado na landing e para quem um dia estender o template.

**D29. Vídeo e áudio com imagem de espera, sem baixar antes do toque.** `poster`, `preload="none"`, legenda e transcrição em HTML; som nunca começa sozinho; o player oferece velocidade. Arquivo acima de 5 MB fica fora do git, em armazenamento de objetos com URL estável, e o repositório guarda o manifesto e a capa (regra de armazenamento do `AGENTS.md`). Quem veio ler o passo não paga a banda do vídeo inteiro.

**D30. Toda tela que busca dado tem quatro estados: vazio, carregando, erro e cheio.** Quem desenha só o cheio testa com conta que já tem progresso. O aluno novo abre a tela vazia.

| Estado | O que a tela mostra | Exemplo no curso |
|---|---|---|
| Vazio | o que fazer e o primeiro passo | "Nenhum capítulo concluído ainda. Abra o primeiro e marque quando terminar." |
| Carregando | esqueleto com a forma do conteúdo, não roda girando | contornos cinza no lugar dos cartões dos capítulos |
| Erro | o que houve e como resolver, com botão de tentar de novo | "O quiz não carregou. O servidor não respondeu em dez segundos. Tente de novo." |
| Cheio | o conteúdo, testado com nome longo | título de capítulo com 12 palavras no celular, sem cortar |

**D31. O botão diz o que acontece, e mantém o nome no fluxo inteiro.** "Marcar como concluído" vira "Concluído"; "Copiar" vira "Copiado"; "Recomeçar do primeiro módulo" diz o destino. Nunca "Enviar", "Continuar", "Saiba mais" ou "Clique aqui". Leia cada rótulo isolado do resto da tela antes de aprovar.

**D32. Erro explica e orienta, sem culpa e sem desculpa.** O sujeito da falha é o processo ou o campo, como a diretriz já manda para a prosa: "A resposta não foi salva. Confira a conexão e tente de novo", nunca "Você errou" nem "Ops!". A validação fala na hora certa: ajuda antes do erro, erro só depois de sair do campo, acerto confirmado. Campo de senha aceita colar (critério 3.3.8 da WCAG 2.2).

**D33. Quiz da trilha é leitura com resposta, não prova.** Uma pergunta por tela, a alternativa tocável inteira (não só o círculo), a explicação da resposta logo abaixo, e o resultado diz o que reler, nunca "você falhou". Nada disso entra na aula: entra na trilha ou no portal.

## 8. Dados na tela: painel de números, tabela e gráfico

**D34. Uma pergunta por peça, com período e denominador escritos nela.** "Crescemos 40%" sem base nem período é desenho sem informação. O `statGrid` responde a uma pergunta por painel; cada cartão traz valor, rótulo e `sub` com origem, período ou denominador ("Contra a busca clássica", "Amostra de agosto de 2026"). Quarenta números e nenhuma decisão é bonito na demonstração e ninguém reabre.

**D35. Todo número chega a fonte, definição e data em dois toques.** Na aula, isso é o `sub` do cartão mais a linha correspondente no bloco "Fontes" do rodapé (R7). O `source` do payload de `dataTable` e `statGrid` sobe sozinho para o rodapé; o redator não repete a fonte na célula.

**D36. Barra vence pizza; nada em 3D; eixo começa em zero.** Quando o curso montado na landing tiver gráfico, a forma segue a pergunta: "estamos na meta?" pede barra com traço de meta, nunca velocímetro; "como cada unidade evoluiu?" pede a mesma miniatura repetida, nunca dez linhas embaralhadas. Gráfico tem tabela equivalente para o leitor de tela, escondida da tela e presente para o leitor, nunca com `display: none`. Rótulo de eixo em cinza de fábrica reprova no contraste.

**D37. Tabela cabe em 390 px ou rola dentro do bloco.** Já cumprido pelo template (D20, D24). Número parado fica em texto; número que muda ao vivo pode ganhar animação dos dígitos, na direção da mudança, e só na landing.

**D38. Diagrama até 12 elementos, com a cor do tema.** Acima disso, agrupe ou divida em duas figuras. SVG chamado como imagem externa não enxerga os tokens da página e some no tema escuro: cole o desenho na página (`figure` com SVG inline) ou gere as duas versões.

## 9. Movimento

**D39. Movimento passa num teste de utilidade e fica no degrau mais barato.** Passam três casos: retorno de ação (o botão que muda ao clicar), transição de estado (o capítulo que abre) e orientação espacial (a seta que gira). Reprovam: texto letra por letra, elemento que gira sem motivo, animação que segura o conteúdo. O template só anima borda, cor e a rotação da seta, em 200 a 300 ms, por CSS.

**D40. Com "movimento reduzido" ligado no aparelho, nada some.** As transições do template desligam sob `prefers-reduced-motion: reduce` (`motion-reduce:transition-none`), e cada estado se distingue com a tela parada: aberto tem borda `--accent`, concluído tem borda e fundo `--success`. A regra da casa continua: estado base sempre visível, nunca esconder conteúdo esperando que o JavaScript o revele (seção 7 da doutrina visual).

**D41. Uma assinatura de movimento por página.** Se a landing acrescentar uma cena de abertura ao curso, é a única; o resto responde a uma ação. Scroll-reveal só com rede de proteção que force o estado visível.

## 10. Acessibilidade, desempenho e busca como critério de pronto

**D42. O alvo técnico é WCAG 2.2 no nível AA.** Contraste (D11), teclado (D19), alvo de toque (D18), fechamento de diálogo e senha colável são os cinco itens que mais reprovam. A ferramenta automática alcança de 30% a 40% dos critérios; o resto é percorrer a página com Tab, Shift+Tab, Enter e Esc, nos dois temas, com um capítulo aberto e a FAQ aberta.

**D43. Três sinais de velocidade, no percentil 75 das visitas, separados entre celular e computador.** Maior bloco visível em 2,5 s ou menos (o vilão é a imagem grande na abertura, e por isso a abertura do template é degradê, não foto). Salto de layout de 0,1 ou menos (o vilão é a imagem sem altura reservada, e por isso a figura leva `width` e `height`). Resposta ao toque em 200 ms ou menos (o vilão é a rotina longa segurando o navegador; o template não roda biblioteca de animação).

**D44. Imagem abaixo de 150 KB no tamanho em que aparece.** AVIF primeiro, WebP depois, JPEG por último; ícone, desenho de linha e diagrama em SVG. A matriz de origem fica fora do repositório, e a troca de formato sai no build da landing (`sharp` ou `next/image`), uma vez por imagem. Regra de armazenamento do `AGENTS.md`: imagem do tamanho em que aparece.

**D45. O texto existe sem JavaScript.** O conteúdo dos capítulos vive no array `STEPS` e o acordeão monta no cliente; por isso a verificação de publicação é no navegador, com o capítulo aberto, e nunca pelo HTML servido (seção 11 da doutrina). O JSON-LD descreve só o que a página mostra: curso, FAQ e breadcrumb.

**D46. Descrição da página entre 150 e 160 caracteres, uma por página.** `CourseDefinition.descricao` vira `description`, Open Graph e JSON-LD de uma vez. Abaixo de 70 caracteres ela não diz o que o curso ensina; acima de 160 o buscador corta. O gerador avisa no log quando sai da faixa (seção 12) e não bloqueia, porque o acervo publicado entra por linha de base congelada.

## 11. Revisão da entrega: conferir nesta ordem

Cada resposta negativa vira um pedido de uma linha sobre o ponto exato que faltou, no template ou no prompt, nunca na saída. Um ajuste por vez.

| O que conferir | O que abrir | O que ver |
|---|---|---|
| Abertura | a página no celular, em 390 px | H1, subtítulo, parágrafo, primeiro capítulo; nada antes nem entre eles |
| Os quatro estados | o curso sem progresso, com tudo concluído, com a FAQ aberta, offline | mensagem própria em cada estado; o cartão de conclusão só quando todos terminam |
| Contraste | inspeção do navegador, aba de acessibilidade, nos dois temas, transições mortas | 4,5:1 no texto; 3:1 na borda do cartão, no anel de foco e na seta |
| Teclado | a mesma página, sem mouse | foco visível em todo cabeçalho de capítulo, botão e pergunta; Enter abre e fecha |
| Toque | o aparelho, não o simulador | 44 px nos alvos principais, nada cortado atrás da barra do navegador |
| Peças visuais | cada capítulo aberto | legenda que afirma, tabela rolando dentro do bloco, comparativo com os lados certos, passo com verificação |
| Movimento reduzido | o aparelho com a opção ligada | nada some; aberto, fechado e concluído se distinguem parados |
| Metadados | o HTML servido | uma descrição de 150 a 160 caracteres, canônica igual ao endereço, JSON-LD sem campo que a página não mostra |
| Print | a captura nos dois temas, celular e computador | o botão cortado e o cinza ilegível que o código esconde |

Lista curta, para colar na descrição do PR que muda template, prompt ou montagem:

1. Nada compete com a primeira frase: sem barra, card, selo ou animação antes do primeiro parágrafo.
2. Um elemento memorável (o degradê) e uma decisão por capítulo (o próximo passo).
3. Cartão só onde há item repetido; nenhum dos cinco padrões genéricos; nenhum dos três tiques tipográficos.
4. Linha de até 80 caracteres; corpo em 15 px, nada abaixo de 12 px; espaço em múltiplos de 4 px.
5. Contraste medido nos dois temas: 4,5:1 no texto, 3:1 em borda, foco e ícone; nenhum texto sobre o degrau 500.
6. Cor por token com papel; hex só em fundo fixo com texto fixo (código e aviso).
7. Um caminho linear; cada capítulo responde sozinho; link com `#` leva ao capítulo.
8. Todo rótulo, lido sozinho, diz o que acontece; nenhum "Saiba mais", "Enviar" ou "Clique aqui".
9. Alvo de 44 px nos botões principais (piso 24), 8 px entre vizinhos.
10. Tab, Enter e Esc percorrem a página com foco visível; o acordeão anuncia aberto e fechado.
11. Legenda afirma um fato; `alt` descreve a cena; `width` e `height` declarados; imagem abaixo de 150 KB; texto fora da imagem raster.
12. Tabela com até três colunas de texto, rolando dentro do bloco em 390 px; comparativo com os lados certos; passo com verificação.
13. Uma pergunta por painel; valor, rótulo e `sub` com período ou denominador; fonte no rodapé.
14. Transições desligam com movimento reduzido; nenhum conteúdo depende de JavaScript para aparecer.
15. Maior bloco em 2,5 s, salto de 0,1, resposta em 200 ms, no percentil 75, celular e computador separados.
16. Descrição de 150 a 160 caracteres; canônica igual ao endereço; JSON-LD fiel à página.
17. Revisão na ordem: abertura, estados, contraste, teclado, toque, peças, movimento, metadados, print.

Os itens 1 a 3, 7, 8 e 13 são leitura humana. Os demais têm número e se medem com o auditor do navegador, o verificador de acessibilidade e o relatório de velocidade da landing.

## 12. Estado da implementação neste repositório

Registro do que existe para que ninguém confunda regra escrita com regra aplicada.

| Critério | Onde mora | Estado em 07/10/2026 |
|---|---|---|
| Abertura R1 a R9 no template | `page.tsx.j2`, `abertura_checker.py` | Cobrado por teste e por `AberturaError` |
| Tabela rola dentro do bloco | `DataTableBlock`, `renderTable` | Cobrado em `tests/test_template_blocos_visuais.py` |
| Cor por token, sem hex novo | blocos visuais | Cobrado pelo mesmo teste |
| Alvo de toque de 44 px nos botões principais | cabeçalho do capítulo, concluir, FAQ, recomeçar | Aplicado nesta rodada; teste em `tests/test_template_design_ux.py` |
| Foco visível em `--accent` | os mesmos elementos e o botão de copiar | Aplicado nesta rodada; mesmo teste |
| Acordeão anunciado (`aria-expanded`, `aria-controls`) | cabeçalho e conteúdo do capítulo | Aplicado nesta rodada; mesmo teste |
| Movimento reduzido | cartão, ícone, seta, botão de concluir | Aplicado nesta rodada (`motion-reduce:transition-none`); mesmo teste |
| Figura por caminho vira `<img>` com `alt`, `width`, `height`, `loading="lazy"` | `FigureBlock` | Aplicado nesta rodada; mesmo teste |
| Descrição da página fora de 70 a 160 caracteres | `TsxGenerator.render_layout` | Aviso no log nesta rodada; mesmo teste |
| Camada visual no prompt (legenda, alt, rótulo de passo, número com período) | `draft.md` (pt-br, en, es) e `review.md` | Aplicado nesta rodada; referência do pipeline regravada |
| Capítulo aberto no endereço (`#`) | `page.tsx.j2` | Pendente: o `id` existe, o acordeão não lê o `hash` ao carregar |
| Contraste, velocidade e peso de imagem medidos | landing-page-geo | Fora deste repositório: auditor do navegador e portões da landing |
| Player, quiz e formulário | landing-page-geo e `src/engagement/` | Fora do template; critérios na seção 7 |

Nenhum item virou erro bloqueante. O caminho para um critério daqui virar gate é o da casa: número em `config/quality_rules.yaml` ou no espelho da fonte, validador que lê o arquivo, teste que prova que mudar o número muda o veredito. Configuração que ninguém lê não protege nada.

## Fontes

<small>

- Alexandre Caramaschi, guia "Frontends com vibecoding", portal de educação, trilhas 1 (fundamentos e briefing), 3 (identidade visual), 4 (layout, menus e navegação), 5 (animação, imagem e vídeo), 6 (formulários, busca e idiomas), 7 (dados na tela), 9 (acessibilidade, desempenho e segurança) e 10 (publicação, qualidade e revisão), edição de setembro de 2026, lido em 07/10/2026: https://alexandrecaramaschi.com/educacao/frontends-com-vibecoding
- W3C, WCAG 2.2, critérios 1.4.3 (contraste de texto), 1.4.11 (contraste de componente), 2.5.8 (alvo de toque) e 3.3.8 (autenticação acessível), conforme citados no guia: https://www.w3.org/TR/WCAG22/
- Google, web.dev, limiares de LCP, CLS e INP no percentil 75, conforme citados no guia: https://web.dev/articles/vitals
- Documentos irmãos que este guia assume e não contradiz: `DIRETRIZ_DESIGN_LAYOUT_UX.md` do `escrita-empreendedor` (1.9.0, critérios V1 a V54), `DIRETRIZ_DESIGN_LAYOUT_UX.md` do `Escrita-Empresarial` e `GUIA_DESIGN_LAYOUT_UX.md` do `Geo-Leadlovers`, todos de 07/10/2026.
- Documentos desta casa: `DIRETRIZ_EDITORIAL.md` (R1 a R9), `docs/DOUTRINA_VISUAL_CURSOS.md` (seções 5 a 9 e 11), `docs/FRONTEND_PLAYBOOK.md` (seções 3, 4 e 6), `docs/GOVERNANCA_PUBLICACAO_CURSO.md` e a regra de armazenamento, velocidade e memória do `AGENTS.md`.

</small>
