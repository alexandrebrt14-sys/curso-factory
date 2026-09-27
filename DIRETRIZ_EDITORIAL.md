# Diretriz editorial deste repositório (ponteiro)

fonte: https://github.com/alexandrebrt14-sys/escrita-empreendedor
hash-fonte: 999d02ddc87cfa2897cb0fafda4f6b5fdd170103fddd74c14c7750f96f91beae
sincronizado-em: 2026-09-10

A régua de escrita, os moldes de página, a tabela de tetos, o perfil do leitor e o glossário
vivem na fonte acima. Este arquivo não repete nenhum número nem nenhuma lista. Quando algo aqui
contradiz a fonte, a fonte vence e este arquivo é corrigido.

A unidade de medida do curso-factory é a **aula** (tipo D da fonte). O que era diretriz própria
deste repositório — piso de palavras por módulo, pisos de exercício, tabela, blockquote,
estatística e fonte, cota de palavras por parte, orçamento de formatação, fluxo de revisão em
três passadas, vícios de português, estruturas proibidas — passou a viver na fonte, em
`DIRETRIZ.md`, `MOLDES_DE_PAGINA.md` (seções 2, 3-D e 6) e `PERFIL_DO_LEITOR.md`.

## O que é específico deste repositório

- **Motor de cursos.** O vocabulário de peças visuais que o gerador sabe emitir (`figure`,
  `dataTable`, `comparison`, `matrix`, `statGrid`, `timeline`, `flow`, `checklist`, `glossary`,
  `accordion`, `template`, `useCase`, `tabs`, `slides`, `tipCard`, `stepGuide`, `codeDownload`),
  o payload de cada uma e as armadilhas do renderizador estão em `docs/DOUTRINA_VISUAL_CURSOS.md`.
  `code`, `prompt` e `sourceNote` são aparato, não respiro, e não contam como peça visual.
- **Teto de parágrafo em caracteres, no motor.** A fonte mede parágrafo em palavras (a faixa
  da aula está em `tetos.D.paragrafo` do espelho). O motor de cursos mede também em caracteres
  (1.200), porque o bloco de prosa da landing rola dentro de si mesmo num celular de 390 pontos.
  Os dois valem: o de palavras é editorial, o de caracteres é de renderização. Parâmetros em
  `config/quality_rules.yaml > validation.visual_density`.
- **Unidade de geração.** Desde 02/09/2026 o pipeline escreve, analisa, classifica e revisa uma
  AULA por chamada, com a pesquisa inteira, e cada etapa recebe o rascunho (não a saída da
  anterior). Os tetos da aula entram no prompt de redação como variáveis lidas do espelho.
  Registro em `wiki/decisions/geracao-por-aula-e-insumo-correto.md`.
- **Acervo publicado entra por linha de base congelada.** A dívida de cada curso existente fica
  registrada e só pode diminuir; a régua nova é obrigatória e integral só para curso novo.
- **Configuração que ninguém lê não protege nada.** Antes de confiar num gate, verifique se o
  código realmente carrega o arquivo de regras. Foi o defeito de 11/08/2026, quando o YAML tinha
  56 clichês e o gate rodava com 18 em código.

## Tamanho e ordem do curso (27/09/2026)

Os dados de uso do portal /educacao mostraram que curso curto termina e curso longo não, que o
aluno abandona na teoria que chega cedo, no capítulo de contexto com número de terceiros e no
apêndice de instalação, e que a rolagem média dos capítulos abandonados fica abaixo da metade
da página. Daí saem cinco orientações de planejamento, que entram no prompt de planejamento de
aulas e no de redação:

- para tema amplo, o curso inteiro fica numa faixa curta de aulas; aula que não muda uma
  decisão do aluno sai;
- as primeiras aulas do curso são as mais curtas e as mais práticas, com ganho no primeiro dia;
- teoria densa só da metade do curso em diante, e sempre depois de um caso contado inteiro;
- a tese e o que fazer ficam na primeira metade de cada aula; o fecho retoma o caso e não
  guarda a informação principal;
- nenhum apêndice de instalação no caminho: o passo vira passo a passo curto dentro da aula
  que precisa dele, ou link para o curso que já ensina.

Os números (faixa de aulas, quantas aulas iniciais, alvo de palavras delas) e os textos das
instruções vivem em `config/quality_rules.yaml > validation.planejamento`. O gate confere, como
aviso, o curso fora da faixa e a aula inicial acima do alvo (`src/validators/planejamento_checker.py`).

## Abertura e distração (R1 a R9)

Pedido do dono dos repositórios em 08/09/2026, literal na decisão
`wiki/decisions/abertura-direta-sem-distracao-20260908.md`: o topo carregado dispersa o leitor
e o card no meio compete com a leitura. A fonte de estilo 1.7.1 (ponteiro acima, ressincronizado
em 10/09/2026) carrega as mesmas regras no bloco `aberturaEDistracao` do espelho
`config/lexicos.json`, que o `abertura_checker` lê e soma aos padrões próprios; esta seção é o
resumo local, e em divergência a fonte vence.

- **R1. Abertura mínima obrigatória.** Toda página, artigo, aula e capítulo começa com H1
  (título), depois subtítulo em UMA frase, depois parágrafos diretos ao ponto. Nada antes nem
  entre eles: sem barra de botões, sem bloco de metadados, resumo ou "o que você vai
  aprender", sem índice, sem card, sem "trilhas", sem "para quem é". O primeiro elemento
  depois do subtítulo é um parágrafo.
- **R2. Sem excesso de botões.** Zero chamadas para ação antes do corpo; se houver, uma, no fim.
- **R3. Sem percursos alternativos.** Nada de "escolha seu caminho", "se você é X vá para Y",
  abas por perfil, vários "comece por aqui". Um único caminho, linear.
- **R4. Uma descrição só.** Uma `description` por página; o resumo não se repete em card.
- **R5. Sem "mockup no seu negócio"** e variantes ("no seu negócio", "aplique no seu
  negócio", "simule", "maquete") como seção ou rótulo.
- **R6. Sem exercício "faça agora"** e variantes ("exercício", "mão na massa", "sua vez",
  "pratique", "tarefa", "desafio", "checklist de ação", "Resultado esperado:", "Se
  travar:"). Conteúdo é leitura, não workbook; o próximo passo entra em prosa, no fecho.
- **R7. Fontes só no rodapé.** Um único bloco "Fontes" ao fim, em corpo pequeno
  (`0.8rem`), com nome da fonte e link, uma linha curta por fonte. Nenhuma fonte em card,
  callout, sidebar ou linha "Fonte:" no meio do texto. Link inline discreto é aceito.
- **R8. Sem card "checkpoint"** e variantes ("ponto de verificação", "recapitulando", "resumo
  do capítulo", "você aprendeu", "quiz").
- **R9. Sem "requer verificação" e sem LGPD.** Nenhum marcador visível de apuração ("requer
  verificação", "a verificar", "[verificar]", "dado não confirmado", "fonte pendente",
  `[FALTA EVIDÊNCIA:` no publicado); verificação é bastidor. Nenhuma menção à LGPD, à Lei
  Geral de Proteção de Dados ou à Lei 13.709 em texto de leitura, mesmo entre aspas.

Onde cada regra é garantida: prompts (`src/templates/prompts/*/draft.md`, `review.md`,
`analyze.md`), gerador (`src/templates/page.tsx.j2`, `src/parsers/markdown_parser.py`,
`src/generators/tsx_generator.py`) e gate (`src/validators/abertura_checker.py`, chamado
por `content_checker.check_content` e por `TsxGenerator.render_page`, que levanta
`AberturaError`). R2 e R4 são cobradas no template por teste (`tests/test_abertura_sem_distracao.py`).

## Didática: explicar em vez de detalhar (22/09/2026)

Pedido do dono, literal na decisão `wiki/decisions/didatica-explicar-em-vez-de-detalhar-20260922.md`:
a régua de máquina aprovava aula que o aluno abandona. Régua de tamanho é teto, nunca alvo. A
aula troca minúcia por explicação sem inchar: glosa com analogia do cotidiano na primeira
aparição de cada termo, frases ligadas em raciocínio (o que é, por que importa para o negócio,
o que fazer), corte da enxurrada de versão, exemplo do negócio pequeno contado inteiro, fecho
com verbo no imperativo e critério de acerto. Ficha, dica, caso, legenda, título, subtítulo e
a passagem entre aulas saem no mesmo registro da aula. Norma de origem: DIRETRIZ §18 do
`Escrita-Empresarial`; especificação, medição e nomes de regra em
`docs/ESPECIFICACAO_DIDATICA_20260922.md`.

Onde vira máquina: prompts (`draft.md`, `review.md`, `trail.md`, `analyze.md`), gate
(`src/validators/didatica_checker.py`, categoria `didatica`, quase tudo aviso), gerador
(`check_didatica_definicao`, só log) e orquestrador (linha `TÍTULO:`). Os números vivem em
`config/quality_rules.yaml > validation.didatica`; a janela de glosa e o teto do título vêm
de `config/lexicos.json > limiares`.

## Compatibilidade editorial de 10/09/2026

Fonte consultada e incorporada no commit `2479179e199f768c4e96aebbadfa5d864523b34e`, versão 1.7.1.
A aplicação de SEO e GEO às etapas de pesquisa, escrita, revisão e humanização está em
`docs/ESCRITA_SEO_GEO.md`. A fonte §10 rege a fidelidade; os prompts da raiz e de `pt-br/`
executam essa orientação sem alterar o formato de retorno do pipeline.

## Como sincronizar

```
python -m escrita.sincronizar verificar DIRETRIZ_EDITORIAL.md   # reprova se o hash divergir
python -m escrita.cli lexicos --json > config/lexicos.json      # espelho lido pelos validadores
```

`config/lexicos.json` é gerado, nunca editado à mão. É dele que
`src/validators/content_checker.py` tira os tetos da aula e as listas de expressão vetada.
