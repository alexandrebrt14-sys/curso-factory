# Estado do portal /educacao em 14/10/2026 e o que muda no curso-factory

Este documento dá ao curso-factory o contexto da reorganização do `landing-page-geo`
(Etapa 1 fechada em 14/10/2026, Etapa 2 em andamento) e fixa o formato de saída que a
fábrica passa a entregar. Tudo o que está aqui foi lido na `origin/master` do portal,
nos PRs #1409, #1421 e #1425 e nos relatórios `D:\GENESIS_OUTBOX\reorg-arquitetura-20261013\`
(`06-PLANO-ETAPA-1.md` e `08-FECHAMENTO-ETAPA-1.md`). Onde é estimativa, está dito.

Glosas: **tsc** é o verificador de tipos do TypeScript; **CI** é a esteira que roda testes e
build a cada PR; **gerado** é arquivo produzido por script a partir de outros; **payload RSC**
é a cópia dos dados da página que o Next.js embute no HTML para o navegador montar a tela;
**schema** é o contrato que diz quais campos um dado pode ter; **sidecar** é um arquivo
auxiliar gravado ao lado do principal, com o mesmo nome e outro sufixo.

## 1. O que mudou no portal

### 1.1 Conteúdo do curso em JSON, fora do grafo de tipos (14/10/2026)

Até 13/10 cada curso vivia em `src/app/educacao/<slug>/modulos/aula-*.ts`: TypeScript
compilado pelo tsc, pelo lint e pelo empacotador a cada build. O piloto (PR #1409, curso
`video-com-ia-claude-code-codex-elevenlabs`) e os dois primeiros cursos da Etapa 2
(#1421 `autoridade-tematica`, #1425 `seo-programatico`) moveram o conteúdo para
`src/content/cursos/<slug>.json`, lido do disco em tempo de execução por
`src/lib/educacao/conteudo/carregar.ts` e validado pelo schema zod de `schema.ts`.

| Curso | Linhas de TS que saíram | JSON | Capítulos | HTML da página servida |
| --- | ---: | ---: | ---: | ---: |
| video-com-ia (piloto, #1409) | 12.838 | 1.291.780 B (10.504 linhas) + glossário de 190 termos | 25 | 978 KB no piloto (1.004 KB na master anterior) |
| autoridade-tematica (#1421) | 18.968 | 1.394.754 B (13.521 linhas) | 19 | 770.460 B |
| seo-programatico (#1425) | 10.739 | 1.075.548 B (6.692 linhas) | 21 | 768.981 B |

Em curso em 14/10: `agentic-operating-model` (#1427), `mcp-chrome` e `seo-geo`. Faltam 55
dos 58 cursos; a receita está em `docs/arquitetura/piloto-curso-json-20261014.md` do portal.

O que fica em TypeScript de propósito, por curso: `steps.ts` fino (27 a 36 linhas:
`carregarCurso(slug)` mais os guias práticos), `guias/*.ts` (pós-processamento com regras:
ponto de inserção, soma de minutos, fusão de fontes), a mídia do capítulo 1
(`midia-capitulo-1.ts` ou `modulos/<slug>-cap01-midia*.ts`, porque a página lê as constantes
para o JSON-LD de vídeo e podcast), `layout.tsx`, `page.tsx`, `opengraph-image.tsx`.

O schema (`CursoJsonSchema`) é estrito: campo desconhecido reprova. `Step` tem `id`,
`title`, `duration`, `icon` (nome da chave em `courseIcons.tsx`, nunca o componente),
`description`, `content`, e os opcionais `legacyIds`, `faq`, `contentDeferred`. `Section`
tem `type` (39 literais), `value` (string; SVG e `<img>` entram como HTML em string),
`language`, `codeHtml`, `label`, `title` e `data` (só valor JSON: sem função, `Date`,
`Map`, `NaN`). O espelho está em `config/schema-curso.json` deste repositório.

### 1.2 Quatro geradores precisam ler o JSON

Achado 8 do fechamento: migrar um curso exige ensinar os geradores a ler o JSON, senão o
realce de código some em silêncio (no piloto, −52 KB na página e −960 KB no `conteudo.json`
antes do ajuste). Os quatro: realce de código (`scripts/build-course-code-highlight.mjs`,
Shiki; 947 → 1.065 blocos no mapa), manifesto de capítulos atualizados
(`scripts/capitulos-atualizados.mjs`; o teste `capitulos-atualizados-em-dia` levou 12,7 s
com o JSON de 1,25 MB até o script pular a busca de imports em JSON), corpus e índice de
busca (`scripts/build-educacao-corpus.mjs`; o curso em JSON é reescrito no formato dos `.ts`
antes dos mesmos regex, e `mediaPlayer` fica de fora de propósito) e o atalho de imports.
Por isso a **comparação de HTML servido** (build da master e do PR, `curl`, normalização de
hash e `diff` com 0 linhas) virou passo obrigatório de cada migração.

### 1.3 Registro de conteúdo sob demanda e teto de peso

`src/lib/course-steps-registry.ts` lista os cursos cujo `STEPS` vive em `steps.ts`. Curso
registrado ganha três coisas: `/educacao/<slug>/conteudo.json` com o corpo dos capítulos
fora do HTML (`course-deferred-content.ts`: só o capítulo aberto por padrão vai no HTML, os
outros chegam com `content: []` e `contentDeferred: true`), uma URL estática por capítulo
(`/educacao/<slug>/<capitulo>`, com canonical, breadcrumb e sitemap) e entrada no manifesto
`src/generated/course-chapters.json`. Em 13/10 eram 14 de 58 cursos; em 14/10, 18. Curso
novo precisa antes da curadoria da ordem de estudo (`educacao-ordem-curada.json`), porque o
gate de integridade do grafo barra capítulo sem "Estude antes".

O gate `scripts/gate-peso-html-cursos.mjs` mede o HTML descomprimido de cada rota de curso
no servidor local do build: teto de 900 KB (`TETO_HTML_CURSO_KB`), rota dinâmica
(`no-store`, `private`) reprova sempre, e o acervo que já passava entra numa linha de base
que **só desce** (`scripts/peso-html-cursos-baseline.json`, 10% de folga). Em 13/10 eram 13
rotas acima do teto; em 14/10, 5 (astra-profundo 1.693 KB, glossario-dev 2.302 KB,
saude-mental 1.052 KB, seo-geo 952 KB, frontends-com-vibecoding 942 KB). Desde 11/10 o
excesso numa rota que o PR não tocou é aviso "herdado da master"; rota tocada reprova.

### 1.4 Guias práticos, mídia do capítulo 1, glossário, figuras

- Guias práticos em abas (PR #1332, 12/10): um bloco `tabs` por capítulo (Funções, Casos de
  uso, Aplicações) com prompt e saída reproduzíveis, inserido antes do primeiro callout
  "Entregável" (ou do primeiro `checkpoint`, ou no fim), com as fontes somadas ao bloco
  `fontes` do capítulo e os minutos somados à duração. Ficam em `guias/*.ts` porque são
  regra de montagem, não dado.
- Mídia do capítulo 1 (NotebookLM): bloco `mediaPlayer` com vídeo e podcast, constantes de
  `src`, poster, duração e transcrição lidas pela página para o JSON-LD; a transcrição
  fica só na página do curso (modelo do capítulo, 30/09).
- Glossário por curso: `glossario.ts` monta `GLOSSARIO_<CURSO>` a partir do sidecar
  `<slug>.glossario.json` (`{ id da aula: [{term, def}] }`); chave que não é aula do curso
  reprova ao carregar.
- Figuras: SVG autoral inline (`role="img"`, `<title>`, cor por token, texto sobre acento
  com `var(--course-accent-fg,#fff)`) ou `<img>` com `alt`, `width`, `height`, `loading="lazy"`;
  imagem nova vai para `https://midia.brasilgeo.ai/...` (contrato R2, 08/10), nunca para
  `public/` em tamanho de matriz.

### 1.5 Guardas que um curso novo precisa passar

No CI (`grep -n "run .*:check" .github/workflows/ci-and-deploy.yml`): `llms:build && llms:check`,
`arquitetura:dominios:check`, `educacao:corpus:check`, `entity:check`. Fora deles, mas
exigidos antes do push pelos PRs de migração: `curso:realce:check`, `npm run test:prebuild`.
Testes que um curso novo arrasta: `tracing-dados-gerados` (toda rota que alcança o registro
leva `./src/content/cursos/*.json` em `outputFileTracingIncludes`),
`capitulos-atualizados-em-dia` (hash por capítulo; regerar o manifesto),
`course-chapters-manifest`, `cursos-contagens` (contagens por curso no catálogo),
`modelo-do-capitulo` (capítulo aberto por padrão), gabarito de busca do /educacao
(`src/data/mcp-gabarito-da-busca.ts` e `piso-de-qualidade.lento.test.ts`: palavra nova no
vocabulário do BM25 muda o corretor de grafia e derruba o gabarito, como "score" por "store"
no #1421). Guardas de texto: acentos (`scripts/ci/check-ptbr-accents.sh`: até 20
ocorrências; 80 quando a mudança tem 1.000 linhas ou mais ou 30 arquivos; nunca renomear
identificador para fugir), emoji zero (`scripts/ci/lint-emoji.mjs`), contraste de acento
sólido, e as regras de escrita do dono (12/10: ritmo pelo sentido, aberturas variadas, zero
construção que nega para afirmar, conectivos cortados por subtração, sem vícios de máquina
nem adjetivo vazio, tipografia brasileira, glosa breve de conceito técnico).

### 1.6 Modo foco do CI (D-1) e gerados versionados

Desde 14/10 (`FOCO_PADRAO`), um PR cujos arquivos fora de documentação são só
`src/**/*.{ts,tsx,css}` ou `scripts/__tests__/*.test.mjs` roda `vitest related`, as
invariantes do admin, type check (por fatia: Educação custa 25% do Check, 2,6 GB) e lint;
build e gates pós-build ficam para o push de master e para a noturna. `FOCO_EXCECOES` devolve
à esteira completa o que muda o site servido sem teste unitário: `middleware.ts`, qualquer
`layout.tsx`, sitemap, robots, feeds, `opengraph-image*`, autenticação, migrações,
`src/data/**` e `src/generated/**`.

**`src/content/cursos/*.json` não casa `FOCO_PADRAO`** (o comentário do workflow é explícito:
"JSON, TXT, HTML, SQL e fixtures continuam fora: lidos pelo disco, não entram no `vitest
related`"). Resultado: todo PR que entrega ou edita um curso em JSON roda a esteira completa
(27,6 min de mediana em 14/10; 33,2 min em 13/10), e o mesmo vale para o que o curso arrasta
em `src/generated` (manifesto de capítulos, corpus, realce) e em `src/data` (catálogo
`educacao-courses.ts`). Pedido ao landing-page-geo na seção 6.

Gerados versionados (`docs/arquitetura/gerados-versionados-decisao-20261014.md`): nenhum sai
do git nesta etapa, porque o CI valida antes de gerar e os worktrees começam sem build. Cinco
ciclos de CI foram perdidos em 13 e 14/10 por gerados defasados; a regra é rodar os
`--check` locais antes do push.

## 2. O que era ineficiente antes e o que muda

| Antes (até 13/10/2026) | Número | Depois (receita de 14/10) |
| --- | ---: | --- |
| Conteúdo dos cursos em TypeScript, recompilado pelo tsc, lint e empacotador a cada PR, mesmo de um capítulo | cerca de 370 mil linhas de TS de conteúdo em 850 arquivos (plano D6: −350 mil linhas, −850 arquivos ao migrar os 57 cursos); programa do tsc com 11.227 arquivos e 7,2 GB | JSON lido do disco, fora do grafo de tipos e do bundle; cada curso migrado tira 10 a 19 mil linhas (−12.838, −18.968, −10.739 nos três primeiros) |
| Curso novo tocava arquivos fora da própria pasta: catálogo, registro, manifestos, corpus, tracing, `next.config.ts`, espelhos `.md` públicos | cerca de 37 arquivos fora de `src/app/educacao/<slug>/` por curso (perícia 05); o piloto mexeu em 47 arquivos, o #1421 em 27, o #1425 em 28 | A fábrica entrega o JSON, o sidecar de glossário, o manifesto de mídia e o `steps.ts` fino; o resto é regenerado por script no portal, num PR por curso |
| Cursos fora do registro de conteúdo sob demanda: corpo inteiro no HTML e no payload | 44 de 58 fora do registro em 13/10 (14 dentro); 18 dentro em 14/10 | Curso novo nasce registrado: `conteudo.json`, URL por capítulo, manifesto; o validador mede o capítulo aberto (o único que vai no HTML) |
| Páginas acima do teto de 900 KB de HTML | 13 rotas em 13/10; 5 em 14/10; antes da Onda 3 (09/09) eram 2,39 MB em `/educacao/seo-geo` | Teto medido antes do PR: capítulo aberto até 72 mil caracteres (erro), curso até 1,2 milhão (aviso) |
| Ciclos de CI perdidos por gerado defasado (capítulos, corpus, conteúdo do painel, tracing) | 5 ciclos em 13 e 14/10, a 27 a 35 min cada; 7.498 min de Actions entre 07 e 13/10 com franquia de 3.000 | Checklist de entrega com os `--check` exatos antes do push (seção 5) |
| Um PR por capítulo, cada um na esteira completa | 41 builds da Vercel para 52 merges em 13/10; 49% das corridas de PR vermelhas ou canceladas em 13/10, 31% em 14/10 | Um PR por curso; o JSON já cai na esteira completa de qualquer jeito, então dividir só multiplica os 27 min |
| Pesquisa refeita a cada execução (TTL do cache de 1 h) | a pesquisa (`sonar-deep-research`) é a chamada mais cara por módulo | Cache da pesquisa por tópico com validade de 7 dias (`CACHE_TTL_PESQUISA_SECONDS`), por provider |

### 2.1 O caminho novo, etapa por etapa, com o tempo esperado

| Etapa | Onde | O que sai | Tempo esperado |
| --- | --- | --- | --- |
| 1. Contrato do curso | `config/courses.yaml` (`estrutura_modulos` com a pesquisa densa em `descricao`), `client.yaml` | número de capítulos (25 quando o contrato pedir), ordem de leitura, peças visuais decididas junto com o índice | 1 a 2 h de curadoria do dono ou do agente; sem LLM |
| 2. Pesquisa por tópico | `python cli.py create` (Perplexity), cache de 7 dias por tópico | material de pesquisa com data por fonte e tabela de proveniência | 3 a 8 min por módulo na primeira vez; segundos no reuso |
| 3. Redação, análise, classificação e revisão | pipeline de cinco LLMs, uma aula por vez | rascunho em `output/drafts/<slug>_<ts>.json` com relatório da revisão | 10 a 20 min por curso de 12 módulos em paralelo; 25 capítulos em 25 a 40 min |
| 4. Variações pequenas antes do lote | 5 a 10 capítulos (ou figuras, ou prompts de guia) revisados pelo dono antes de gerar os 25 | decisão de ampliar ou refazer o molde | 30 a 60 min de leitura; evita regerar 25 capítulos com o mesmo defeito |
| 5. Exportar para o formato do portal | `python cli.py drafts-to-tsx --json` ou `python cli.py exportar-json <CourseDefinition>` | `<slug>.json`, `<slug>.glossario.json`, `<slug>.midia.json`, `<slug>.steps.ts` | segundos |
| 6. Validar aqui | `python scripts/validar_curso_json.py <slug>.json --contrato-completo` | schema, ids, peso por capítulo, linguagem dos blocos, acentos, emoji, escrita, guia, mídia, glossário, figuras | segundos |
| 7. Revisão editorial humana | `REVISAO_HUMANA.md`, leitura pelo guia de escrita e pelas regras do dono | correções no JSON (fonte única) | 1 a 3 h por curso, a parte que não se corta |
| 8. Entregar no portal | worktree de `origin/master`, um PR por curso, checklist da seção 5 | JSON em `src/content/cursos/`, `steps.ts`, registro, catálogo, gerados regenerados, comparação de HTML | 40 a 90 min de máquina (build local 6 a 8 min, `tsc` 1 a 4 min, gates) + 28 min de CI |
| 9. Confirmar no ar | string-sentinela na página servida (nova presente, antiga ausente), capítulo aberto no navegador | registro do SHA e da data no `REVISAO_HUMANA.md` | 5 min depois do deploy em janela |

## 3. O que o curso-factory deixa de fazer e passa a fazer

Deixa de fazer:

- Entregar `modulos/aula-*.ts` ou `page.tsx` com o conteúdo embutido como formato final.
  O `TsxGenerator` continua existindo para o esqueleto da página (`page.tsx`, `layout.tsx`)
  e para a revisão local (`REVISAO_HUMANA.md`), mas o que o portal lê é o JSON.
- Abrir um PR por capítulo no portal.
- Emitir `codeHtml` ou `contentDeferred`: o servidor acrescenta os dois por cópia.
- Entregar figura em tamanho de matriz ou vídeo e áudio acima de 5 MB no repositório.

Passa a fazer:

- Gerar `src/content/cursos/<slug>.json` validado pelo espelho do schema
  (`config/schema-curso.json`, copiado da `origin/master` em 14/10/2026), com as chaves na
  ordem do portal (`id`, `title`, `duration`, `icon`, `description`, `content`, `faq`),
  indentação de 2 espaços, UTF-8 sem escapar acento e quebra de linha final (o `git diff`
  lê uma linha por campo).
- Ids e slug estáveis: ASCII minúsculo com hífen; o id vira âncora e URL do capítulo e não
  muda depois de publicado (`legacyIds` guarda o nome antigo quando precisar renomear).
- Sidecar `<slug>.glossario.json` com os termos por aula (só ids que existem no curso).
- Guias práticos em TS fino (`guias/*.ts` + `aplicar.ts`, como o portal faz) quando o guia
  tiver regra de montagem; quando for só conteúdo, vai inline no JSON como bloco `tabs`
  rotulado "Guia prático", com prompt e saída reproduzíveis por capítulo.
- Manifesto de mídia `<slug>.midia.json` (origem, `alt`, dimensões, SVG inline ou não) para
  o inventário do contrato de mídia; a fábrica não envia nada ao R2.
- Blocos `code` sempre com `language` que o Shiki aceita (`bash`, `python`, `typescript`,
  `tsx`, `json`, `yaml`, `markdown`, `html`, `css`, `sql`, `toml`, `csv`, `text` e os
  aliases `sh`, `js`, `ts`, `yml`, `md`); rótulo editorial como "saída" vira `text` e não
  colore.
- Rodar o checklist de entrega (seção 5) antes de abrir o PR no portal.

## 4. Limites de tamanho e como foram calculados

Medidas de 14/10/2026 nas páginas servidas em produção (`curl --compressed`, bytes
descomprimidos) e nos JSON da `origin/master`:

| Curso | Caracteres de conteúdo no JSON | Capítulo aberto na página (caracteres) | HTML da página | `conteudo.json` servido | Bytes por caractere no `conteudo.json` |
| --- | ---: | ---: | ---: | ---: | ---: |
| autoridade-tematica | 1.116.586 (19 caps; maior 105.074) | 62.083 | 770.460 B | 1.365.134 B | 1,22 |
| seo-programatico | 867.206 (21 caps; maior 64.280) | 64.280 | 768.981 B | 1.511.549 B | 1,74 |
| video-com-ia | 1.098.000 (25 caps; maior 63.392) | 33.700 (+ transcrição de mídia) | 1.004.410 B na master; 978 KB no piloto | 3.141.617 B | 2,86 |

Leitura: o `conteudo.json` pesa de 1,2 a 2,9 bytes por caractere de conteúdo; a diferença é
o realce de código (60 blocos no curso de vídeo contra 18 no de autoridade: cada bloco
realçado vira dezenas de `<span>`). A página do curso leva o capítulo aberto duas vezes
(renderizado e no payload RSC): com 62 a 64 mil caracteres no capítulo aberto, as duas
páginas migradas ficaram em 770 KB, 130 KB abaixo do teto. Daí os limites em
`config/quality_rules.yaml > validation.curso_json`:

- capítulo aberto (o primeiro do array): aviso a partir de 60.000 caracteres, erro a partir
  de 72.000 (cerca de 2,5 bytes de HTML por caractere, o que deixa a página abaixo de 900 KB
  com 10% de folga);
- demais capítulos: aviso em 80.000, erro em 110.000 (só a URL do capítulo e o
  `conteudo.json` os carregam; o maior capítulo migrado tem 105.074);
- curso: aviso em 1,2 milhão de caracteres ou 1,5 MB de JSON (o manifesto de capítulos
  levou 12,7 s com 1,25 MB antes do ajuste do #1409; o diff do git lê linha a linha);
- acentos: 20 ocorrências, 80 quando o arquivo tem 1.000 linhas ou mais (todo curso novo),
  mesma regra do portal; emoji: zero.

Os três cursos migrados passam no validador com esses limites (0 erros; avisos de figuras
por capítulo, escrita e acentos ficam no relatório para a revisão editorial).

## 5. Checklist de entrega no portal (reproduz os checks antes do PR)

Executar no worktree do `landing-page-geo` criado de `origin/master`
(`git worktree add D:/wt/<nome> origin/master`, `npm ci`), com o JSON já aprovado por
`scripts/validar_curso_json.py` aqui:

```
# 1. Colocar os arquivos
#    src/content/cursos/<slug>.json e <slug>.glossario.json
#    src/app/educacao/<slug>/steps.ts (fino), layout.tsx, page.tsx, guias/*.ts, midia do cap. 1
#    src/data/educacao-courses.ts (catálogo, com iconKey) e course-steps-registry.ts (registro)
#    educacao-ordem-curada.json (ordem de estudo: o gate do grafo barra capítulo sem "Estude antes")

# 2. Validar o JSON pelo schema do portal (o carregador reprova com o caminho do campo)
npx vitest run src/lib/educacao/conteudo

# 3. Regenerar os gerados que o curso arrasta e conferir que ficaram em dia
npm run chapters:manifest                 # src/generated/course-chapters.json
npm run curso:realce && npm run curso:realce:check
npm run educacao:corpus && npm run educacao:corpus:check
npm run build:admin:conteudo              # inclui scripts/capitulos-atualizados.mjs
npm run llms:build && npm run llms:check
npm run arquitetura:dominios:check
npm run entity:check

# 4. Testes que um curso novo arrasta
npx vitest run src/__tests__/tracing-dados-gerados.test.ts src/__tests__/capitulos-atualizados-em-dia.test.ts src/__tests__/course-chapters-manifest.test.ts src/__tests__/cursos-contagens.test.ts src/__tests__/modelo-do-capitulo.test.ts src/__tests__/course-inline-links.test.ts src/__tests__/course-peso-visual-vocabulario.test.ts
npx vitest related --run <arquivos tocados>
npm run test:prebuild

# 5. Tipos, lint, texto
NODE_OPTIONS=--max-old-space-size=8192 npx tsc --noEmit
npx eslint <arquivos tocados>
git diff --name-only origin/master...HEAD | bash scripts/ci/check-ptbr-accents.sh   # no Windows, pelo validador daqui
npm run lint:emoji

# 6. Build local, gate de peso e comparação de HTML
npm run build && npx next start -p 3123 &   # guardar o PID; encerrar pelo PID, nunca por nome
node scripts/gate-peso-html-cursos.mjs       # sem --gravar-baseline
node scripts/gate-peso-visual.mjs <slug>
curl -s http://localhost:3123/educacao/<slug> -o depois.html   # comparar com a master quando for edição de curso existente
```

Regras do PR: um PR por curso; título `feat(educacao): curso <slug> em JSON`; o corpo traz a
tabela de medidas (linhas de TS, bytes de JSON, HTML da página, `conteudo.json`, blocos no
mapa de realce), os comandos rodados e como reverter. Commit com prefixo `docs:`, `chore:`,
`style:`, `ci:`, `test:` ou `revert:` não gera deploy (`should-build.sh`); desde 14/10 o
deploy sai em janela a cada 2 h entre 9h e 19h (D-3, #1419) ou pelo botão "Publicar agora"
em `/admin/deploys`. Confirmar no ar com string-sentinela e com o capítulo aberto no
navegador, porque o corpo dos capítulos fechados chega pelo `conteudo.json`.

## 6. Pedidos ao landing-page-geo (não editados aqui)

1. **Modo foco para `src/content/cursos/*.json`.** Hoje o JSON de curso fica fora de
   `FOCO_PADRAO` e todo PR de curso roda a esteira completa (27,6 min). Proposta: aceitar
   `src/content/cursos/[a-z0-9-]+(\.glossario)?\.json` no foco e mapear, no passo `reuso`,
   os testes que leem o disco (`src/lib/educacao/conteudo/__tests__`,
   `capitulos-atualizados-em-dia`, `course-chapters-manifest`, `cursos-contagens`,
   `tracing-dados-gerados`) para rodarem junto com o `vitest related`, já que o `related`
   não segue leitura de disco. O que o curso arrasta em `src/generated` e `src/data`
   continua na esteira completa pela exceção, então o ganho só aparece quando a edição é
   só de conteúdo (correção de texto, capítulo novo num curso já registrado): o caso mais
   comum depois da migração.
2. **Opção de glossário no gerador** `extrair-curso.mts` (limite conhecido do piloto): hoje
   o sidecar é montado à mão; a fábrica já entrega o sidecar pronto, então o pedido é só
   para os 55 cursos legados.
3. **Lista de ícones e de linguagens exportável** (`courseIcons.tsx` e `ALIAS_LINGUAGEM` do
   realce) num JSON gerado, para o espelho daqui não envelhecer à mão.

## 7. Matriz qualidade x eficiência: o que não se corta para ganhar velocidade

| Prática | Custo | Por que fica | O que pode ser cortado no lugar |
| --- | --- | --- | --- |
| Revisão editorial humana do JSON (guia de escrita, regras do dono de 12/10, `REVISAO_HUMANA.md`) | 1 a 3 h por curso | Nota estilométrica e gate mecânico não demonstram qualidade factual nem autoria; o Google (01/10) estende a checagem humana a título, meta description, JSON-LD e `alt` | Revisar sobre as 5 a 10 variações antes do lote, não sobre 25 capítulos prontos |
| Comparação de HTML servido (master x PR, `diff` 0 linhas) ao migrar ou editar curso existente | 15 a 25 min de máquina (dois builds) | Foi o que pegou o realce sumindo em silêncio no piloto (−960 KB no `conteudo.json`) | Para curso novo não há "antes"; vale o gate de peso e o capítulo aberto no navegador |
| Geração de 5 a 10 variações antes de 50 (regra do dono de armazenamento, 02/10) | 30 a 60 min de leitura | Regerar 25 capítulos com o mesmo defeito custa 25 vezes o LLM, o disco e a revisão | Cortar a cota de variações, não a etapa |
| Revisão cruzada entre modelos (redação em um, análise em outro, revisão em um terceiro) | 3 chamadas a mais por aula | A revisão por outro modelo é o que acha o fato errado e a antítese de máquina que o redator não vê; os juízes multi-LLM do /educacao de 11/10 acham bug real | Modelos mais baratos na análise e na classificação (Sonnet e Haiku), nunca na revisão final |
| Tabela de proveniência (frase com número, data, versão ou produto com fonte aberta e data de acesso) | minutos por aula | Frase sem fonte sai do texto; a tabela nunca vai para a página | Nada |
| Peso visual medido, não cota: até 3 figuras por capítulo, só quando substituem texto | aviso no validador | Enfeite para cumprir cota foi o que o gerador fazia antes de 27/08 | A cota, que já saiu |
| Gates do portal rodados localmente antes do push | 10 a 20 min | 5 ciclos de CI perdidos em dois dias por gerado defasado | Esperar o CI remoto para descobrir |
| Mídia fora do git e imagem no tamanho exibido | minutos | `public/` chegou a 1,83 GB; 10% dos criativos foram usados | Matriz de origem no repositório |

O que ganha velocidade sem tocar nessas práticas: cache de pesquisa por tópico (7 dias),
um PR por curso, exportação direta para o formato final, validador local que reproduz os
gates do portal em segundos, build local uma vez por curso em vez de uma por capítulo.

## 8. Regras novas das Etapas 3 e 4 (14 e 15/10/2026): valem para todo curso gerado e publicado

As Etapas 3 e 4 da reorganização do landing-page-geo migraram mais 17 cursos para JSON e
mudaram a esteira. Nesse caminho, treze cursos ficaram presos: o padrão antigo os impedia de
migrar. Esta seção diz o que a fábrica entrega a partir de agora e por quê. A conferência
automática das regras P1 a P5 está em `scripts/conferir_pagina_portal.py`, com testes em
`tests/test_pagina_portal.py`.

### 8.1 A página do curso é de servidor (regra P1)

Componente de servidor é a página que o Next.js monta no servidor. Ela pode ler o JSON do
disco e manda ao navegador só o HTML e as partes interativas.

- O `page.tsx` do curso **não** começa com `"use client"`. Toda interação (abas, progresso,
  player, busca do glossário) fica em componentes cliente filhos, já prontos no portal
  (`CoursePage`, `CourseGlossarySearch`, `MotionToggle`).
- Motivo medido: o carregador `carregarCurso` usa `node:fs`. Em página de cliente o
  `next build` reprova com "does not support external modules (node:fs)". Treze cursos
  ficaram fora da Etapa 4 por isso, entre eles cro-experimentacao, mcp-avancado e
  prompt-engineering-avancado.
- O template legado `src/templates/page.tsx.j2` emite página de cliente com o conteúdo
  embutido. Ele serve só para curso legado. Curso novo usa como modelo a página de um curso
  já migrado no portal, como `src/app/educacao/meta-ads-2027/page.tsx`.

### 8.2 `steps.ts` fino e conteúdo só no JSON (regras P2 e P4)

- O `steps.ts` tem uma linha de trabalho: `export const STEPS = carregarCurso(SLUG)`. Nada
  de `content: [...]` escrito no arquivo.
- Nenhum arquivo do curso faz `import` do JSON. Um JSON importado entra no programa de tipos
  de todo PR. O curso frontends-com-vibecoding tem 2,0 MB de JSON.
- Conteúdo que não serializa (chamada de função, `${}` em template, referência a outra
  constante) continua em TypeScript, documentado no `steps.ts`. O extrator do portal tem um
  modo `--inline` que recusa esses casos apontando a linha (PR #1480).

### 8.3 Conteúdo sob demanda por capítulo (regra P3)

- A página serve no HTML o capítulo aberto e todo o texto indexável por buscadores e LLMs.
  Os demais capítulos chegam pela rota estática `[curso]/[capitulo]/conteudo.json`, um
  segmento de caminho por capítulo (PR #1464). Com query string a rota seria dinâmica e
  cada capítulo custaria uma função na Vercel.
- A página usa `deferStepContent` e `courseContentJsonPath`. Sem isso o HTML leva todos os
  capítulos e passa do teto de 900 KB do gate de peso.
- O astra-profundo, com 1,65 MB, passou para esse caminho na Etapa 4 (#1471 e #1475).

### 8.4 Limites de tamanho que voltam a valer na geração

- Capítulo até 72.000 caracteres (erro; aviso a partir de 60.000), medido em JSON compacto.
  Na migração do frontends-com-vibecoding, dez capítulos passaram de 72 mil por causa de
  figuras SVG escritas no texto. Curso novo não nasce assim: figura grande vai para
  `midia.brasilgeo.ai` como arquivo, e o capítulo guarda o endereço.
- Chave indefinida não existe em JSON (regra P5). Fonte sem link omite `url`, em vez de
  `url: undefined`.

### 8.5 O que mudou na esteira do portal e muda a entrega

- **Gerados do painel fora do PR.** `src/generated/admin-conteudo.json` sai do git e é gerado
  no build (#1458). Os mapas de arquitetura e o piso das linhas de base moram na branch
  `gerados`, regravada por um robô depois de cada merge (#1451). O PR do curso não regrava
  esses arquivos.
- **Gerados do curso continuam no PR.** Capítulos atualizados, corpus de busca, realce de
  código e `llms.txt` seguem versionados. Rode os `--check` antes do push: foram 21 corridas
  vermelhas em 7 dias só por `capitulos-atualizados` defasado.
- **Leitores do JSON.** Todo gerador que lia o TypeScript do curso precisa ler o JSON. Na
  migração do frontends-com-vibecoding, o corpus ainda lia as aulas-fonte apagadas e
  derrubava o piso de qualidade da busca (#1472).
- **Modo de curso no CI.** Um PR que só muda `src/content/cursos/<slug>.json` roda 34
  arquivos de teste em vez da suíte inteira: de 28 para 17 min (#1442). O `pre-pr` e o
  `master-red` reconhecem o JSON como toque na rota do curso (#1460).
- **Corte rápido.** O job `verificar` reprova tipos e lint em cerca de 7 min e cancela a
  corrida (#1450). Erro de tipo no PR do curso aparece antes dos testes.
- **Tracing no `next.config.ts`.** Cada curso tem uma chave. Dois cursos em paralelo
  conflitam nessa linha. A resolução certa é unir os arrays, nunca ficar com a primeira
  ocorrência.
- **Merge não é publicação.** A produção publica em janela de 2 h em horário comercial, ou
  pelo botão "Publicar agora" do `/admin/deploys`. Curso só está no ar quando a página
  servida mostra o texto novo e não mostra o antigo.

### 8.6 Ordem de entrega de um curso novo, com as regras novas

1. Gerar e revisar pelo pipeline da fábrica (as seções 3 e 7 seguem valendo).
2. `python cli.py exportar-json <CourseDefinition>`, depois
   `python scripts/validar_curso_json.py <slug>.json --contrato-completo`.
3. Colocar no portal: `<slug>.json`, `<slug>.glossario.json`, `steps.ts` fino, `layout.tsx`,
   `page.tsx` de servidor copiada de um curso migrado, registro e catálogo.
4. `python scripts/conferir_pagina_portal.py <portal>/src/app/educacao/<slug>`: P1 a P5 verdes.
5. No portal: `--check` dos gerados do curso, `tsc` antes do `next build`, build, gate de
   peso e capítulo aberto no navegador. Em curso já existente, comparar o HTML servido.
6. Um PR por curso. Merge com CI verde e master verde, publicação pela janela e conferência
   na página servida.
