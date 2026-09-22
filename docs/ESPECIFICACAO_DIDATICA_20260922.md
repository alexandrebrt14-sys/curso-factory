# Especificação de didática: explicar em vez de detalhar (22/09/2026)

Pedido do dono, em 22/09/2026: a régua de máquina das aulas aprova texto que o aluno abandona.
O verificador mede extensão, parágrafo, frase, jargão glosado e peso visual, e o curso sai
picado, com registro de ficha técnica nas superfícies que os agentes não reescrevem. Este
documento amplia o diagnóstico com medição, fixa a especificação e diz onde cada regra virou
máquina neste repositório. A norma editorial de origem é a DIRETRIZ §18 do `Escrita-Empresarial`
(0.3.0, PR #21, "explicar em vez de detalhar"); as regras aqui usam os mesmos nomes quando
existe equivalente.

## 1. Diagnóstico ampliado

Duas auditorias por máquina em 22/09/2026, sobre a fonte publicada, sem tocar nos repositórios
medidos. Scripts e relatórios integrais ficaram na sessão; os números abaixo são os que mudam a
especificação.

### 1.1 Portal /educacao (landing-page-geo): frontends, astra, RAG, gestão de projetos

| Medida | frontends | astra | RAG | gestão de projetos |
|---|---:|---:|---:|---:|
| Parágrafos de prosa | 1.060 | 700+ | 500+ | 900+ |
| Abrem com artigo definido (O, A, Os, As) | 43,1% | baixo | **53,1%** | baixo |
| Pares vizinhos com a mesma primeira palavra | 94 | poucos | **50** | poucos |
| Descrições que começam com "Você sai" | **61 de 61** | 31 de 31 | 0 ("Você termina sabendo") | 0 |
| Descrições com três ou mais vírgulas | 18 de 61 | 0 | 0 | 0 |
| Títulos sem verbo (substantivos empilhados) | **35 de 61** | 0 de 31 | 10 de 20 | 0 de 57 |
| Títulos com dois-pontos | 15 de 61 | 0 | 0 | 0 |
| Parágrafos acima de 60 palavras | 6,6% | **37,5%** | baixo | 0% |

O que os quatro cursos mostram juntos: a régua de frase e de parágrafo está sendo cumprida
(4,6% das frases do frontends passam de 28 palavras; mediana de 19), e mesmo assim o texto
lê picado. O defeito não está dentro do parágrafo, está entre os parágrafos e nas superfícies
ao redor deles. No curso de RAG, a palavra "armadilha" abre vinte parágrafos.

**Fichas de recurso (frontends, 146 blocos `resourceLesson`).** "Você" aparece 0,28 vezes por
mil palavras nas fichas, contra 1,66 nas aulas: a ficha fala sobre o assunto, a aula fala com
a pessoa. Nenhum nome de API em CamelCase vem seguido de glosa em 80 caracteres (zero casos
bons em 84 ocorrências); exemplos: `textContent`, `addPassthroughCopy`, `generateStaticParams`,
`createSignal`. A conferência foge em 11 fichas: "versão instalada" (7), "pode conter, pode
variar" (4), "documentação atual" (1).

**Costura de capítulo.** O consolidador funde duas ou três aulas por capítulo e a única emenda
é `### <nome da aula>`:

```ts
return i === 0 ? corpo : [{ type: "text", value: `### ${s.title}` }, ...corpo];
```

Nenhuma frase diz o que a aula anterior resolveu nem por que a próxima vem agora. A descrição
do capítulo sai de fórmula ("Você sai com uma entrega que integra...").

**O que os verificadores da casa não medem.** `check-aula-fvc.ts`, `check-aula-gdv.ts` e
`check-aula-gpg.ts` cobram título até 12 palavras, description até 35, parágrafo até 60 (teto
75), frase até 28 (teto 34), piso e teto de palavras e o léxico R1 a R9. Nenhum mede abertura
de parágrafo repetida, o tique "Você sai" (a ausência da fórmula é aviso, a presença nunca é
achado), o registro das fichas, a costura entre aulas nem título-índice. Só o `gpg` reprova
verbo fraco no título.

### 1.2 Portal Leadlovers (brasilgeo-worker), 12 páginas de setembro

- 2.207 parágrafos; 34,5% abrem com artigo definido; 183 pares vizinhos com a mesma
  primeira palavra (um a cada doze). Depois de "O" e "A", as entradas mais repetidas são
  rótulos de ficha: "Gatilho:" (80) e "Métrica:" (77).
- 45% dos parágrafos têm menos de 20 palavras; nos guias de segmento mais recentes passa de
  50% (franqueadoras 57%, corretores 52,6%). A frase é curta (mediana 14 palavras, 4,7% acima
  de 28): o defeito é o parágrafo fatiado, não a frase longa.
- 336 títulos H2 e H3: 47,3% sem verbo; "O que..." e "Como..." somam 36% dos títulos;
  "Quais números acompanhar toda semana?" repete literalmente em cinco páginas.
- Seis de doze descrições começam com "Guia de automação para <ramo>: dez use cases na
  Leadlovers"; a armação da frase não muda de página para página.
- Jargão sem glosa perto da primeira aparição: automação e funil e CRM em quatro páginas cada;
  webhook, UTM e API sem nenhuma explicação.
- Nenhuma das doze páginas fecha com verbo no imperativo e critério mensurável no mesmo
  parágrafo. Só duas páginas (energia solar e cuidado de idosos) contam um caso de negócio
  nomeado, com número e desfecho (Rafael da Solar do Vale; Vanessa do home care).
- Oito de doze páginas têm uma seção de casos em registro de ficha: título numerado, linha de
  metadados ("Gatilho:", "Canal:") e lista por dia, sem frase de ligação entre um cartão e o
  seguinte.

### 1.3 O contraste que prova o caminho

O próprio curso de frontends tem o padrão certo no glossário: "spring: jeito de animar que
imita uma mola: em vez de mandar o movimento durar um tempo fixo, você diz o quanto ele é
firme e o quanto desacelera". Glosa curta, analogia do cotidiano, o que muda para quem usa.
Esse padrão vale para toda superfície, e é o molde que os prompts deste repositório passam a
citar.

## 2. Princípio

Régua de tamanho é teto, nunca alvo. Trocar minúcia por explicação, sem inchar. A régua da
fonte (`escrita-empreendedor` 1.7.1, tipo D) já diz isso: piso é aviso, frase vai até 60
quando enumeração ou número com condição pedem, parágrafo de uma frase é legítimo quando a
ideia cabe nela, e nenhuma cota de ritmo. O que faltava era medir o que fica entre os blocos e
ao redor deles, e escrever isso nos prompts.

## 3. Especificação

Cada item traz o defeito, o que muda e onde vira máquina neste repositório. Quase tudo é AVISO,
porque didática se julga lendo; ERRO só para tique comprovado.

| # | Regra (nome no gate) | O que muda | Severidade |
|---|---|---|---|
| 1 | `abertura-repetida`, `abertura-em-serie`, `abertura-por-artigo` | Parágrafos vizinhos não abrem com a mesma palavra; a maioria não abre por artigo definido mais sujeito. Metade das entradas varia: condição, número, verbo, adjunto de tempo | aviso; série de 3 é erro |
| 2 | `jargao-sem-glosa` | Todo termo do `jargao` da fonte ganha glosa de até 12 palavras com analogia, na janela de `limiares.glosaJanelaCaracteres`, no molde "spring" | aviso |
| 3 | `fecho-sem-acao`, `fecho-sem-criterio`, `fecho-resumo` | O último parágrafo manda fazer (imperativo) e diz como conferir (número, prazo, condição); não resume | aviso |
| 4 | `enxurrada-de-versao` | Número de versão só quando muda a decisão; acima de 4 por mil palavras é minúcia | aviso |
| 5 | `titulo-com-dois-pontos`, `titulo-sem-verbo`, `titulo-longo` | Título é promessa do aluno com verbo, em até `limiares.h1MaxPalavras`; o redator pode propor `TÍTULO:` e o orquestrador troca | aviso |
| 6 | `subtitulo-formula`, `subtitulo-promessas-empilhadas`, `subtitulo-longo`, `subtitulo-formula-repetida` | Subtítulo é UMA promessa em até 25 palavras, sem "Você sai" nem corrente de vírgulas; a mesma dupla de palavras em três subtítulos do curso é tique | aviso; fórmula em 3 é erro |
| 7 | `ficha-registro-impessoal`, `ficha-abertura-repetida`, `ficha-api-crua`, `ficha-conferencia-de-fuga`, `fichas-em-paredao` | Ficha, dica, caso e legenda saem no registro da aula: "você", glosa, exemplo do negócio pequeno, conferência que diz o que aparece na tela; mais de seis seguidas pedem frase de ligação | aviso; fuga é erro |
| 8 | costura (prompt) | Aula com anterior pode abrir pela ponte de entrada em uma linha; o fecho carrega a ponte de saída com critério | prompt e revisão |

Correspondência com a DIRETRIZ §18 do `Escrita-Empresarial`: 1 = abertura-mesma-palavra,
abertura-periodica, abertura-em-artigo; 4 = muleta-de-versao; 5 = titulos-com-dois-pontos;
6 = promessa-em-formula, subtitulo-em-corrente; 7 = identificador-cru-em-prosa,
registro-que-muda, paredao-de-fichas; 8 = secao-sem-abertura.

## 4. Onde cada regra vive neste repositório

- **Prompts** (`src/templates/prompts/pt-br/` e raiz): `draft.md` ganha o molde da glosa, os
  três movimentos ligados (o que é, por que importa, o que fazer), o corte da enxurrada de
  versão, a ponte de entrada, o fecho com critério, a seção "Título da aula: promessa do
  aluno" com a linha `TÍTULO:`, a régua flexível de parágrafo e frase, a cadência de abertura
  e a seção "Blocos auxiliares". `review.md` ganha as mesmas correções (seções 3, 4 e 4b) e a
  linha de relatório "Correções de didática". `trail.md` ganha o molde da glosa no glossário e
  o subtítulo da trilha sem fórmula. `analyze.md` ganha a dimensão 4b.
- **Gate** (`src/validators/didatica_checker.py`): categoria `didatica` em
  `content_checker.check_content`, aula a aula, pelo `QualityGate` e pelo orquestrador.
  Regras em `config/quality_rules.yaml > validation.didatica`, lidas em runtime; janela de
  glosa e teto de título em `config/lexicos.json > limiares`.
- **Gerador** (`src/generators/tsx_generator.py`): `check_didatica_definicao` roda sobre o
  `CourseDefinition` montado (título e subtítulo de cada módulo, fórmula repetida entre
  módulos, cadência e fecho da prosa, fichas em sequência) e grava em
  `TsxGenerator.achados_didatica`, com aviso no log. Não recusa a renderização.
- **Orquestrador** (`src/orchestrator.py`): `_extrair_titulo_proposto` aceita a linha
  `TÍTULO:` no topo do rascunho e troca o título planejado.
- **Régua sincronizada**: os fallbacks do `content_checker` e os comentários do YAML passam a
  dizer o que a fonte 1.7.1 diz (piso 700, alvo 900 a 1.800, 1 H3 por H2, parágrafo 20 a 80);
  o achado de parágrafo já era aviso e continua aviso.
- **Testes**: `tests/test_didatica_checker.py` (24 casos) prova cada regra, a integração com
  o gate e o gerador, e que o número do YAML muda o veredito.

## 5. O que fica para os consumidores

Este repositório gera cursos; o curso de frontends e os portais medidos vivem em outros
repositórios. O que a especificação pede deles, para fechar o ciclo:

1. `landing-page-geo`: os verificadores `check-aula-*.ts` passam a ler título, description e
   os campos das fichas (`explanation`, `example`, `verification`) com as regras 1, 5, 6 e 7;
   `consolidacao.ts` insere a frase de passagem antes de cada aula a partir da segunda (regra
   8); `recursos-*.ts` são reescritos no registro da aula, com parágrafo de abertura por
   decisão do leitor e frase de ligação entre grupos.
2. `brasilgeo-worker` (Portal Leadlovers): os casos de segmento ("Gatilho:", "Métrica:")
   ganham a frase de ligação e o registro "você"; o molde de description dos guias deixa de
   ser fórmula; os fechos entregam imperativo com critério.
3. `escrita-empreendedor`: o piso de palavras e o prefixo "Você sai" saem do contrato; o
   `jargao` da fonte cresce com os termos de frontend (token, componente, framework, deploy,
   cache, API) para que o `jargao-sem-glosa` os alcance.

Prova comum a todos: exportar o curso ou a página em Markdown e rodar o gate com a categoria
`didatica`, esperando zero erro e avisos só onde a leitura humana os aceitar.
