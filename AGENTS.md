# AGENTS.md

## Padrão editorial obrigatório

Antes de produzir qualquer texto de leitura humana neste repositório (documentação, cursos, páginas, relatórios, descrições de PR, mensagens longas de commit), leia e aplique `DIRETRIZ_EDITORIAL.md` na raiz do repositório (versão 4, 11/08/2026) e consulte o anexo prático `GUIA_ESCRITA_HUMANIZADA.md`, que traz exemplos antes e depois, heurísticas mensuráveis e fontes. A diretriz é a fonte única do padrão: os prompts do pipeline em `src/templates/prompts/` se subordinam a ela.

Antes de qualquer regra de evitação vem o piso de substância (diretriz §2.1), porque os gates automáticos do repositório medem forma e nenhum deles mede argumento: texto raso e uniforme passa em todos. Toda peça precisa ter tese identificável, evidência ligada à tese, ganho de informação, critério de decisão explícito onde houver alternativas, arco de leitura e consequência executável para o leitor. Aprovação no gate não é aprovação editorial, e em conflito entre proibição e piso de substância o piso vence.

Antes da primeira frase vem a prova (diretriz §2.2): o material de evidência define o tamanho da peça, porque o número de blocos que afirmam resultado é menor ou igual ao número de provas datadas disponíveis hoje. Faltando prova, tente as quatro saídas nesta ordem (pesquisar a origem, reduzir a afirmação ao que se sabe, restringir o uso, segurar a publicação) antes de usar marcador; `[FALTA EVIDÊNCIA: ...]` é lacuna que pesquisa resolve e `[PREENCHER-HUMANO: ...]` é o que só o autor humano tem, com teto de cinco marcadores abertos por documento. Promessa e tensão são escritas antes do esqueleto (§3.1), o esqueleto segue a ordem do gênero (§3.2), o pedido é um só por peça com verbo de ação, valor concreto, tempo ou esforço e risco removido (§3.6), e toda porcentagem dispara quatro conferências na mesma frase: origem, data, método e denominador (§13).

O essencial: escrita de especialista sênior em português do Brasil com acentuação completa e tipografia brasileira (sem title case, numerais à brasileira); conclusão antes da sustentação e cada parágrafo acrescentando uma ideia nova; storytelling obrigatório em conteúdo longo (abertura em situação concreta, tensão antes da solução, caso condutor, promessa da abertura cumprida, fechamento que retoma a abertura, mostrar em vez de qualificar); ritmo nascido do sentido, com o teste do bloco de dez frases usado como diagnóstico depois de escrever e nunca como cota durante a escrita (cota de frase curta por parágrafo e alternância programada estão proibidas); proibido travessão como recurso estilístico; proibidas como padrão as construções que negam para afirmar ("não é X, é Y"), a regra de três mecânica, as conclusões-espelho e a atribuição vaga sem fonte nomeada; conectivos cortados por subtração, sem clichês nem vícios de português de LLM (gerundismo, "endereçar", "suportar", "eventualmente" como eventually); tabela comparativa, matriz de decisão e checklist sempre que houver alternativas com critérios, escolha a fazer ou passos verificáveis, e prosa sempre que houver raciocínio encadeado; dado sem fonte e data não entra, e o que só o autor humano sabe vira marcador `[PREENCHER-HUMANO]`, nunca invenção; em superfícies HTML ou PDF, parágrafos com alinhamento justificado (`text-align: justify`); revisão final em três passadas (substância, estrutura, linguagem) com leitura em voz alta. Os documentos completos prevalecem sobre este resumo, e as convenções específicas deste repositório prevalecem sobre convenções genéricas, exceto quando comprometerem segurança ou corretude.

## Abertura e distração (R1 a R9)

Regras do dono, de 08/09/2026, que vencem qualquer molde anterior: toda página, artigo, aula ou
capítulo começa com H1, subtítulo em uma frase e parágrafos diretos ao ponto, sem nada antes ou
entre eles (R1); sem botões antes do corpo (R2); um único percurso (R3); uma descrição só (R4);
sem "mockup no seu negócio" (R5); sem exercício "faça agora" (R6); fontes só no rodapé, em corpo
pequeno, nome e link (R7); sem card "checkpoint" (R8); sem "requer verificação" visível e sem
menção à LGPD (R9). Detalhe em `DIRETRIZ_EDITORIAL.md`, seção "Abertura e distração", e em
`wiki/decisions/abertura-direta-sem-distracao-20260908.md`. O gate
`src/validators/abertura_checker.py` reprova o que escapar, no Markdown e na publicação.
