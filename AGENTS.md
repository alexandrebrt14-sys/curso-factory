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
