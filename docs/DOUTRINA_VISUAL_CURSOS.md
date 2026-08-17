# Doutrina visual dos cursos gerados

Versão 1, de 17 de agosto de 2026. Complementa a seção 11.1 da `DIRETRIZ_EDITORIAL.md`, que é a forma curta e normativa desta doutrina, e o `docs/FRONTEND_PLAYBOOK.md`, que trata de contraste, animação e auditoria visual em geral.

Este repositório **gera** curso. A pergunta que ele faz não é "como eu escrevo melhor este parágrafo", e sim **que peça o gerador deve emitir, com que payload, e o que impede que ele a emita hoje**. O documento responde nessa ordem.

## 1. A regra, antes do argumento

Três limites, verificáveis por máquina, valem para todo curso novo:

1. **Nenhum parágrafo acima de 1.200 caracteres.** O teto é do parágrafo, não do bloco.
2. **Pelo menos três blocos visuais por módulo.**
3. **Pelo menos um bloco visual a cada 2.500 caracteres de prosa** daquele módulo.

Quem gera não precisa decorar mais nada. O resto do documento explica de onde vêm os números, que peça resolve qual defeito de leitura e onde a aplicação costuma dar errado.

O teto de 1.200 é medida de tela, não de gosto: é aproximadamente o que cabe em um celular de 390 pontos de largura no corpo de texto do motor, sem rolagem dentro do próprio parágrafo. Acima disso o leitor perde a referência de onde estava ao voltar do scroll.

## 2. O defeito que isso corrige

O curso `motor-de-crescimento-ia` foi ao ar em 17 de agosto de 2026 com **114 blocos de prosa acima de 1.200 caracteres**, o maior com 3.492, e com **nenhuma figura**. Os portões editorial, de fluidez, de acentuação e de entidade aprovaram todos, porque nenhum deles mede peso de bloco. A correção levou cinco ondas de trabalho.

| Medida | Antes | Depois |
| --- | --- | --- |
| Blocos de prosa acima de 1.200 caracteres | 114 | 0 |
| Maior parágrafo do curso | 3.492 | 1.199 |
| Parágrafo médio | não medido | 700 |
| Figuras e diagramas | 0 | 50 |
| Blocos visuais no total | 30 | 124 |

A varredura dos 55 cursos publicados no portal, feita no mesmo dia, mostrou que o caso não era isolado: **26 dos 52 cursos medidos não têm um único bloco visual**, 15 cursos têm ao menos um parágrafo acima de 1.200 caracteres (42 no total), o maior parágrafo do portal tem 4.590 caracteres em `prompt-engineering-avancado`, e a mediana de blocos visuais por curso é 2,5. Pela régua desta doutrina, **11 dos 50 cursos legíveis passam hoje**.

Nada nesse retrabalho exigiu conhecimento que o gerador não tivesse. Exigiu só que a régua existisse antes da geração.

## 3. O que o gerador emite hoje, e o que falta

Este é o ponto que separa esta doutrina de uma cópia da doutrina da landing.

O motor de cursos do `landing-page-geo` renderiza um vocabulário largo de blocos. O gerador deste repositório, hoje, emite **seis**. A enumeração está em `src/models.py::SectionType` e é espelhada em três lugares:

| Onde | O que declara |
| --- | --- |
| `src/models.py::SectionType` | `text`, `code`, `warning`, `tip`, `checkpoint` |
| `src/schemas/course.schema.json`, `$defs.CourseSection.type.enum` | os mesmos cinco |
| `src/templates/page.tsx.j2` | os cinco mais `image-placeholder`, com o `switch (section.type)` que os desenha |

Nenhum dos seis conta como bloco visual pela régua da seção 4. Um curso gerado hoje pelo caminho padrão, sem montagem manual depois, **nasce reprovado nos limites 2 e 3**.

A consequência prática é clara: cumprir esta doutrina no gerador é trabalho de código, não de prompt. Estender o vocabulário exige mexer nos três lugares da tabela ao mesmo tempo, porque o modelo Pydantic valida, o schema JSON documenta e o Jinja desenha. Acrescentar um tipo em só um deles produz bloco que o validador aceita e a página não mostra.

Enquanto o vocabulário não for estendido, a regra que vale é a de montagem: o curso gerado passa por conversão manual para o formato `<CoursePage>` da landing (fluxo descrito em `docs/GOVERNANCA_PUBLICACAO_CURSO.md`), e é nessa conversão que as peças visuais entram, sob o portão `node scripts/gate-peso-visual.mjs <slug>`.

## 4. O que conta como bloco visual

Três famílias, com pesos diferentes no que resolvem.

**Ilustração e diagrama** são o que quebra parede de verdade, porque interrompem a coluna de texto: `figure` (SVG autoral inline ou imagem) e diagrama Mermaid compilado no build, entregue também como `figure`.

**Estrutura** organiza informação que já era comparável ou sequencial: `dataTable`, `comparison`, `matrix`, `statGrid`, `timeline`, `flow`, `checklist`, `glossary`, `accordion`, `template`, `useCase`.

**Leitura moderna no celular** divide conteúdo longo sem perder profundidade: `tabs`, `slides`, `tipCard`, `stepGuide`, `codeDownload`.

Não contam como alívio visual: `code`, `prompt` e `sourceNote`. Os três são aparato. O `sourceNote` em particular é registro de procedência, servido em corpo reduzido dentro de caixa recuada, e **não deve ser contado nem como paredão nem como bloco visual**. Quem mede pelo DOM precisa filtrar pela cadeia de ancestrais, e não só pelo tamanho do parágrafo, sob pena de condenar o bloco certo pelo motivo errado.

## 5. Qual peça para qual problema

A escolha não é de gosto. Cada defeito de leitura tem uma peça que o resolve, e o gerador deve decidir a peça no momento em que monta o índice do módulo.

| O que trava o leitor | A peça | O que o payload precisa ter |
| --- | --- | --- |
| Dois ou mais caminhos com critérios | `comparison` ou `dataTable` | As alternativas nas colunas e o critério nas linhas, nunca o contrário |
| Um processo com ordem que importa | `stepGuide` ou `flow` | Um verbo por passo e o resultado observável de cada um |
| Números que só fazem sentido juntos | `statGrid` | A origem de cada número no próprio cartão |
| Fontes que discordam entre si | `dataTable` de três colunas | Régua, número e de onde vem, uma linha por fonte |
| Conceito abstrato sem âncora | `figure` com SVG ou diagrama | Legenda que afirma o que a figura mostra, não o que ela é |
| Regra curta que o leitor vai reencontrar | `tipCard` | Cabe no formato fechado dele, e só |
| Sequência longa demais para uma tela | `slides` ou `tabs` | Cada painel autônomo, legível fora de ordem |
| Verificação que o leitor fará depois | `checklist` | Itens que se pode marcar, não afirmações |
| Decisão com consequência | `decisionCase` | O contexto antes da pergunta |

Quando nenhuma linha descreve o caso, a resposta certa quase sempre é **quebrar o parágrafo em dois**, e não inventar bloco. Bloco inventado para cumprir cota é o mesmo defeito de outro ângulo.

## 6. As quatro famílias de ilustração, com o custo de cada uma

**SVG autoral inline, como `figure`.** Dá o maior controle e é o único que garante os dois temas, porque usa os tokens CSS da casa. Custo: precisa ser escrito. A convenção da landing são constantes com prefixo por curso, em arquivos `figuras*.ts` ao lado dos módulos. Três regras que o componente cobra:

- **todo `<text>` precisa do seu próprio `fill`**, porque SVG não herda cor de ancestral;
- cor sempre por token, nunca hex cravado, e texto sobre a cor de acento usa `var(--course-accent-fg,#fff)` em vez de `#ffffff` cru, porque curso com acento claro no tema escuro reprova o contraste AA com branco fixo;
- o SVG raiz leva `role="img"` e um `<title>`, e esse `<title>` é texto de leitura humana, com acentuação completa.

**Diagrama Mermaid compilado no build.** Fonte em `.mmd`, convertida por `mmdc` com cores-sentinela que depois viram tokens, e o script falha de propósito quando sobra um hex fora do mapa, que é a proteção contra cor cravada. Entra na página como `figure`, nunca como `diagram`. Cada `.mmd` leva `accTitle` e `accDescr`, que são ASCII por exigência da ferramenta. **Mermaid nunca roda no navegador do leitor**: é compilação de build, e é por isso que o CI e a Vercel não precisam de Chromium. Fluxograma que o aluno vê e que exige fonte legível vai de cartões HTML e CSS, conforme a seção 5 do `docs/FRONTEND_PLAYBOOK.md`.

**Ilustração raster gerada.** Imagens por Nano Banana ou equivalente, e material do NotebookLM. Três custos reais: peso de arquivo, ausência de adaptação ao tema e **custo de token de saída em imagem cerca de vinte vezes o de texto no mesmo modelo**, o que faz disso uma decisão de FinOps e não só de estética (ver `docs/FINOPS.md`). Some o registro obrigatório de plataforma, data, instrução e edição humana, e a regra de licença que proíbe imagem gerada por modelo como símbolo de marca. Use para abertura de módulo e para cena, nunca para informação que precise ser lida. Prepare a imagem no build com `sharp` ou `next/image`: a foto da pasta não é a foto do site.

**Ícones e setas.** Vêm do dicionário compartilhado do motor (`courseIcons.tsx` na landing, referenciado por `stepIcons`), e não são desenhados por curso. Baratos e eficazes para marcar seção e direção de fluxo, viram ruído quando decoram sem significar.

## 7. Animação: só a que sobrevive à falha

Animação é ganho de compreensão quando mostra transição de estado, e é ruído quando decora. A regra da casa é CSS-first, à prova de falha, e tem uma formulação operacional:

> **Estado base sempre visível.** Nunca esconda conteúdo esperando que o JavaScript o revele. Se o gatilho não disparar, o conteúdo some para sempre.

Na prática: o `from { opacity: 0 }` vive só dentro do `@keyframes`, com `animation-fill-mode: both`, de modo que a animação dispara no carregamento e termina visível, sem biblioteca e sem JavaScript. Quando o efeito exigir código, use a API de animação do navegador com degradação silenciosa: confira `prefers-reduced-motion`, confira se o elemento existe e siga sem animar quando faltar qualquer um. Scroll-reveal por biblioteca só entra com rede de proteção, um tempo limite ou observador que force o estado visível.

Já houve incidente de "carrega e some": ícones carregados tardiamente mudaram a altura da página, o gatilho de scroll nunca disparou e o conteúdo ficou invisível em produção. Num gerador o estrago se multiplica, porque o defeito mora no template e sai em todos os cursos.

## 8. Contraste e tema

Toda peça visual nasce nos dois temas, e **qualidade visual não é opinião, é verificação**: mede-se no navegador renderizado, nos dois temas, nunca a olho. Os pisos são os da WCAG AA, 4,5:1 para texto normal e 3:1 para texto grande. O processo de auditoria está na seção 6 do `docs/FRONTEND_PLAYBOOK.md`, com a advertência de matar transições antes de medir.

Cor cravada em hex dentro de SVG de curso é defeito, porque some no tema escuro. Use os tokens reais do repositório de destino, e confirme na fonte quais existem: já houve rodada perdida por escrever `var(--surface)`, que não existe, quando o correto era `--card`. Os tokens confirmados hoje na landing são `--text`, `--text-muted`, `--border`, `--card`, `--bg-white`, `--bg-muted`, `--accent`, `--accent-dark`, `--accent-lighter`, `--accent-solid`, `--success`, `--success-light`, `--success-text`, `--warning`, `--warning-light`, `--danger`, `--danger-light`, `--course-accent` e `--course-accent-fg`.

Duas sutilezas que já derrubaram medição: regra de tema que escurece um bloco **não alcança `<span>` ou `<b>` com cor inline própria**, e uma regra genérica de tema pode vencer a regra do nó sólido mesmo com `!important` dos dois lados. Teste a precedência em vez de supor.

## 9. Armadilhas que já custaram retrabalho

- **`diagram` e `mockup` exigem componente React registrado.** Curso novo que emita esses tipos renderiza vazio, sem erro. Mermaid e SVG entram como `figure`.
- **Bloco estruturado sem `data` some sem avisar.** Todos os casos do renderizador só desenham quando `section.data` existe; faltando o campo, o bloco vira nada, sem erro e sem registro no console. É a falha mais silenciosa do motor, e a mais provável num gerador que serializa payload por template.
- **Blocos com payload precisam de `value: ""` além do `data`.** Faltando o `value`, o bloco degrada para nada.
- **`comparison` tem valência fixa:** `left` é sempre "a evitar" e `right` é sempre "recomendado". Inverter o payload carimba um certo justamente no que o texto manda descartar.
- **`flow` tem duas formas incompatíveis:** a histórica, por `value`, e a estruturada, por `data`. Misturar as duas rende bloco vazio.
- **`tipCard` tem payload fechado:** categoria curta, título de até 60 caracteres, a regra em uma frase e de três a cinco bullets de até 90 caracteres cada, mais um fecho opcional. Não serve para mover um parágrafo inteiro, e fatiar uma frase entre dois bullets para caber lê pior que o parágrafo original. Para prosa livre em destaque, use `tip`.
- **Travessão em legenda de figura reprova o portão editorial.** Legenda é texto de leitura humana como qualquer outro, e a seção 6 da `DIRETRIZ_EDITORIAL.md` vale nela.
- **`<title>` de SVG leva acentuação completa**, ao contrário do `accTitle` do Mermaid, que é ASCII. Já houve rodada em que a convenção errada foi copiada e a guarda de acentuação reprovou. O `check-ptbr-accents.sh` da landing verifica texto de SVG com espaço, conforme já registrado em `docs/GOVERNANCA_PUBLICACAO_CURSO.md`.
- **Cenário inventado exige o selo `fictional`.** Caso narrado no pretérito com números específicos, sem selo, é lido como fato apurado. Isso é fabricação publicada.
- **O motor abre um módulo por vez.** Medir a página pelo HTML servido não enxerga o que o motor monta no cliente. Verificação de verdade é no navegador, com o módulo aberto.
- **`grep -c` em HTML de uma linha conta linhas**, devolve no máximo 1 e parece "não achei". Conte com Python.

## 10. Reduzir paredão não é deriva

A doutrina de correção manda **deriva zero**, isto é, consertar um texto publicado sem trair os fatos dele. Isso já foi lido como proibição de mexer na forma, e essa leitura está errada.

Deriva zero protege **fato**: número, data, nome próprio, atribuição de fonte e afirmação verificável. A versão corrigida precisa conter os mesmos fatos, nem um a mais, nem um a menos.

Quebrar um parágrafo em dois, mover uma comparação de prosa para tabela e acrescentar uma figura que mostra o que o texto já dizia não altera fato nenhum. É rearranjo de forma, e é exatamente o que esta doutrina pede. O que a deriva zero proíbe, e continua proibindo, é a figura que afirma o que o texto não afirmava, a tabela que arredonda um número para caber na célula e a legenda que atribui a fonte errada.

Regra prática: ao mover conteúdo para uma peça visual, extraia antes a lista de fatos do trecho e confira um a um na versão final.

## 11. Como medir, e em que ordem

1. **Antes de gerar**, decida as peças visuais de cada módulo junto com o índice, dentro da `descricao` de `estrutura_modulos` em `config/courses.yaml`, que é o canal que chega ao redator. Peça visual escolhida depois é remendo, e remendo foi o que gerou as cinco ondas.
2. **Durante**, meça o peso de bloco a cada módulo fechado, contra os três limites da seção 1.
3. **Antes de publicar**, os portões deste repositório (`src/validators/quality_gate.py` e a camada `visual_density` de `config/quality_rules.yaml`) e os da landing: editorial, fluidez, acentuação, entidade, tipos e testes, mais `node scripts/gate-peso-visual.mjs <slug>`.
4. **Depois de publicar**, meça no navegador, módulo a módulo, com iframe de 390 pontos para o celular. Publicar não é entregar, e mergear não é publicar.

Nenhum portão prova conteúdo ausente, e aprovação em portão nunca equivale a aprovação editorial. O caso do `motor-de-crescimento-ia` é a prova: quatro portões verdes sobre 114 paredões.

## 12. Estado da implementação neste repositório

Registro honesto do que existe hoje, para que ninguém confunda regra escrita com regra aplicada.

| Peça | Estado |
| --- | --- |
| Os três limites, como norma | Escritos na seção 11.1 da `DIRETRIZ_EDITORIAL.md` e aqui |
| `validation.visual_density` em `config/quality_rules.yaml` | Declarado, **não lido por código** |
| Vocabulário de blocos visuais no gerador | **Ausente**, ver seção 3 |
| Portão de peso visual | Existe na landing (`scripts/gate-peso-visual.mjs`), não neste repositório |

O `src/validators/rules_loader.py` lê o YAML em runtime, mas hoje só `forbidden_expressions.expressions` e a seção `anti_invencao` são consumidos por validador. Fazer `visual_density` valer exige um checador novo que leia a seção e conte parágrafos e blocos por módulo. A advertência final da `DIRETRIZ_EDITORIAL.md` vale literalmente aqui: configuração que ninguém lê não protege nada.
