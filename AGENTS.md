# AGENTS.md

## Fonte de escrita e aplicação atual

Leia `DIRETRIZ_EDITORIAL.md` e `GUIA_ESCRITA_HUMANIZADA.md` antes de escrever.
São ponteiros para a fonte `escrita-empreendedor`; os critérios de fidelidade estão na
§10 da fonte e a aplicação ao pipeline está em `docs/ESCRITA_SEO_GEO.md`.
As notas históricas da antiga diretriz v4 não substituem a fonte vigente.

A aula resolve uma ideia para o dono de pequeno negócio, com abertura direta, e é um guia
aplicável: ensina a fazer em passos com verbo no imperativo, diz como saber que cada passo deu
certo, traz o erro comum com o conserto, a decisão "se isto, faça aquilo" e o critério de
pronto. O exemplo é curto e percorre os passos; personagem e cena são opcionais e nunca
conduzem a aula (desde 27/09/2026, `docs/DIAGNOSTICO_GUIA_APLICAVEL_20260927.md`). A evidência vem da pesquisa recebida. Preserve população, período, condição
e a diferença entre projeção, exemplo hipotético e resultado observado ao simplificar.
O detalhe da apuração fica no material de pesquisa; o limite que muda a decisão fica na prosa.

A camada visual do curso gerado (hierarquia da página, navegação entre capítulos, alvo de toque,
foco, movimento reduzido, figura com `alt` e dimensões, painel de números, metadados) segue
`GUIA_DESIGN_LAYOUT_UX.md` (07/10/2026); corrija no template e no prompt, nunca na saída.

## Formato de saída: curso em JSON do portal (obrigatório desde 14/10/2026)

O portal /educacao (`landing-page-geo`) passou a guardar o conteúdo de cada curso em
`src/content/cursos/<slug>.json`, validado pelo schema zod de
`src/lib/educacao/conteudo/schema.ts` (piloto PR #1409; cursos #1421 e #1425; 55 a migrar).
O `page.tsx` com conteúdo embutido e os `modulos/aula-*.ts` deixaram de ser formato final.
Contexto completo, números e checklist em `docs/portal-educacao-estado-20261014.md`.

O que a fábrica entrega por curso, num PR por curso no portal:
1. `<slug>.json` no formato do schema (espelho em `config/schema-curso.json`, copiado da
   `origin/master` em 14/10/2026): chaves na ordem `id`, `title`, `duration`, `icon`,
   `description`, `content`, `faq`; ids ASCII minúsculos com hífen e estáveis (viram URL do
   capítulo); sem `codeHtml` nem `contentDeferred` (o servidor acrescenta); bloco `code`
   sempre com `language` que o Shiki aceita; indentação de 2 espaços e acento sem escape.
2. `<slug>.glossario.json` (id da aula para `[{term, def}]`), só ids do curso.
3. `<slug>.midia.json`: manifesto das figuras e imagens (origem, `alt`, dimensões); mídia
   nova vai para `midia.brasilgeo.ai`, nunca para `public/` em tamanho de matriz.
4. `<slug>.steps.ts` fino (`carregarCurso(slug)` mais guias em TS quando houver regra de
   montagem; guia só de conteúdo vai inline como bloco `tabs` "Guia prático" com prompt e saída).

Limites do portal reproduzidos aqui (`config/quality_rules.yaml > validation.curso_json`):
capítulo aberto na página até 72.000 caracteres (erro; aviso em 60.000), demais capítulos
até 110.000, curso até 1,2 milhão de caracteres ou 1,5 MB de JSON, acentos até 20 (80 em
arquivo de 1.000 linhas ou mais), emoji zero, até 3 figuras por capítulo como aviso.
Comandos: `python cli.py drafts-to-tsx --json`, `python cli.py exportar-json <CourseDefinition>`,
`python scripts/validar_curso_json.py <slug>.json --contrato-completo` (piso de 25
capítulos, mídia do capítulo 1, glossário e guia por capítulo quando o contrato pedir).
Antes do PR no portal, o checklist da seção 5 do documento: os `--check` do CI
(`llms`, `arquitetura:dominios`, `educacao:corpus`, `entity`, `curso:realce`), os testes que
o curso arrasta, `tsc`, build local, `gate-peso-html-cursos.mjs` e comparação de HTML.
O que não se corta para ganhar velocidade está na seção 7 (matriz qualidade x eficiência).

**Regras novas das Etapas 3 e 4 (15/10/2026), na seção 8 do mesmo documento:**
- Página do curso de servidor, nunca `"use client"` (P1).
- `steps.ts` só com `carregarCurso` (P2).
- Conteúdo sob demanda por capítulo pela rota `[curso]/[capitulo]/conteudo.json` (P3).
- Nenhum `import` do JSON do curso (P4).
- Nenhuma chave `url: undefined` (P5).

Antes do PR no portal, rode `python scripts/conferir_pagina_portal.py <portal>/src/app/educacao/<slug>`.
O template `src/templates/page.tsx.j2` é legado: curso novo copia a página de um curso já
migrado.

**Curso já publicado também segue o contrato** (seção 8.7): incremento, correção, estilo e
frontend editam o JSON ou um componente cliente filho, nunca reabrem conteúdo em
TypeScript nem viram página de cliente. Ids de capítulo são estáveis. Componente
compartilhado exige comparar o HTML de pelo menos três cursos. A alteração só termina na
página servida.

## Padrão de armazenamento, velocidade e memória (obrigatório desde 02/10/2026)

Toda ideia nova chega com o custo de armazenamento, velocidade e memória medido, sobretudo quando envolve imagem, vídeo, áudio, dependência ou arquivo gerado. Prefira sempre a opção mais barata e escalável que mantenha a qualidade. A decisão é do dono e vem de 02/10/2026, no landing-page-geo:
- o `public/` chegou a 1,83 GB;
- o acervo de criativos chegou a 1.029 peças, das quais 102 foram usadas em anúncio;
- o teto de memória do CI subiu para 10 GiB por causa de um SDK (`googleapis`) usado só pelo autenticador.

As regras:
1. **Mídia pesada fica fora do git.** Vídeo e áudio acima de 5 MB vão para armazenamento de objetos (Cloudflare R2 ou Vercel Blob, com URL estável) ou direto para a plataforma (YouTube, Meta, Google Ads). O repositório guarda o manifesto e a capa.
2. **Imagem vai no tamanho exibido**, em WebP, AVIF ou JPEG com qualidade 82, com miniatura de até 40 KB. A matriz de origem não é versionada.
3. **Produção em lote nasce com teto e poda.** Isso vale para criativos, prints e figuras de curso. O que não entrou em anúncio nem em página em 30 dias sai do repositório, e o texto fica registrado.
4. **Gerar pouco, medir e ampliar a vencedora.** É mais barato em créditos de API, em disco e em revisão.
5. **Dependência pelo que se usa.** Importe o subpacote que entrega a função. Antes de adotar um SDK grande, meça no tsc (`--extendedDiagnostics`) e no início a frio.
6. **Dado gerado grande fica fora do grafo de tipos.** Um JSON acima de 1 MB importado pelo código passa a ser string ou leitura em tempo de execução.
7. **Teto de memória, de tamanho ou de tempo só sobe com a causa medida** e com o plano de redução no mesmo PR.
8. **O PR com mídia ou dependência pesada traz os números:** tamanho somado, onde a mídia fica hospedada, custo mensal estimado, efeito no build e no CI, e a alternativa mais barata considerada.

Regra completa em `~/AGENTS.md`, seção "Armazenamento, velocidade e memória"; histórico em `landing-page-geo/governance/decisions/armazenamento-velocidade-e-memoria.md`.

## Prompts e contratos

O resolvedor lê `src/templates/prompts/pt-br/`; a raiz de `prompts/` guarda só o `tutor.md`
(as cópias de raiz dos demais prompts saíram em 27/09/2026, porque nunca carregavam). Preserve variáveis,
marcadores e o formato de retorno; a revisão devolve a aula e o relatório no contrato existente.
Os demais idiomas conservam seus próprios prompts e precisam de revisão própria ao estender
a orientação para eles.

O léxico de `config/lexicos.json` é gerado pela fonte; não copie nem edite seus números.
Tetos de aula, renderização, anti-invenção e abertura continuam valendo. Gate mede os padrões
implementados; nota estilométrica ou aprovação mecânica não demonstra qualidade factual,
autoria humana, ranking ou citação.

## Publicação e revisão

Mantenha H1, subtítulo e prosa direta, com um percurso de leitura. As regras de abertura
e distração continuam no ponteiro editorial e em `src/validators/abertura_checker.py`.
Metadados representam a aula, e fontes seguem o rodapé da trilha conforme o molde vigente.
Conserve autoria, referências e condições ao transferir a prova entre esses lugares.

Toda frase com número, data, versão ou nome de produto tem fonte primária aberta, com trecho
lido e data de acesso, numa tabela de proveniência que é arquivo de trabalho e nunca vai para
a página. O redator do pipeline devolve só a aula; a tabela sai do texto final
(`result.etapas["proveniencia"]` ou `python cli.py proveniencia <arquivo>`), e quem redige
fora do pipeline entrega a mesma tabela junto com a aula. Frase sem fonte sai do texto.
Cada fonte leva a data de publicação: o conceito central se apoia em fonte recente, a fonte
antiga entra só como origem do conceito, e nenhuma alegação de estado atual usa fonte velha.
A janela e a data de referência estão no bloco `fontes_recentes` do `client.yaml`; confira com
`python cli.py fontes-recentes <aula> --proveniencia <tabela>`.

Revise substância, estrutura e linguagem. Ganho de informação é o que a explicação acrescenta
à decisão do aluno, sem quota de dados ou garantia de visibilidade. Acentuação PT-BR completa,
sem emoji, sem travessão estilístico e sem cota de ritmo. Teste os contratos afetados e o
caminho efetivamente carregado pelo pipeline antes de entregar.
