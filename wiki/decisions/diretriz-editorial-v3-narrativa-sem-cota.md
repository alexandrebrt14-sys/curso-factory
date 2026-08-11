---
name: diretriz-editorial-v3-narrativa-sem-cota
description: "Por que a v3 da diretriz editorial proibiu cota mecânica de ritmo e tornou storytelling obrigatório; qual era o defeito que derrubou a qualidade do conteúdo gerado entre julho e agosto de 2026."
metadata:
  type: mistake
  created: 2026-08-11
---

A qualidade do texto produzido pelo pipeline caiu porque a doutrina editorial era
feita quase só de mecanismos de reprovação, e as poucas regras positivas eram
mecânicas e se contradiziam entre camadas. Quatro defeitos, todos corrigidos na
`DIRETRIZ_EDITORIAL.md` v3 (11/08/2026):

0. **Doutrina só de reprovação.** 46 expressões banidas com `fail_on_found` no
   `quality_rules.yaml`, orçamento de formatação, tetos de bloco e de marcador,
   trava de estilometria, e nenhuma regra dizendo o que a peça precisa TER. As
   cinco camadas do quality gate medem forma (acento, clichê, contagem, marcação)
   e nenhuma mede argumento: módulo curto, uniforme e sem tese passa em todas.
   A v3 instala o piso de substância (§2.1, seis itens) e uma dimensão de
   aprovação no `analyze.md`, que é a única camada capaz de medir substância
   porque é LLM e não regex. Regra de precedência nova: em conflito entre
   proibição e piso de substância, o piso vence.
1. **Cota de ritmo.** `draft.md` e `humanize.md` exigiam "uma frase de 6 palavras ou
   menos em CADA parágrafo" e "nunca duas frases consecutivas na mesma faixa de
   comprimento". O `humanizer.py` reforçava isso reescrevendo em loop até subir o
   score de burstiness, e o `stylometry_checker.py` avisava quando faltava frase
   curta. O resultado foi staccato de manchete: melhora a métrica, piora a leitura,
   e continua sendo identificado como texto de máquina (Tabach, arXiv:2604.23471).
   Pior: o conjunto era insatisfazível. Regra de crescimento por frase mais ração
   de uma frase curta por bloco produz amplitude perto de 13 a 16 palavras em dez
   frases, e a mesma tabela de limiares reprovava amplitude abaixo de 30. Três
   regras derrubavam a quarta, e quem obedecia às quatro escrevia exatamente a
   faixa estreita que a diretriz classifica como assinatura de máquina. A métrica
   agora é diagnóstico do texto pronto, em duas faixas (abaixo de 15 é defeito,
   acima de 30 é folgado), e a v3 proíbe combiná-la com qualquer outra regra de
   comprimento.
2. **Cota de formatação.** "Parágrafo com no máximo 5 linhas", "sub-heading a cada
   2-3 parágrafos" e "nunca mais de 3 parágrafos sem elemento visual" fatiavam o
   raciocínio antes de ele terminar. A v3 mantém tabela, matriz de decisão e
   checklist como ferramentas obrigatórias quando há comparação, escolha ou passo
   verificável, e devolve à prosa o trabalho de carregar raciocínio.
3. **Ausência de narrativa e camadas divergentes.** Nenhum prompt pedia técnica de
   engajamento, e o `CLAUDE.md` acumulava três blocos editoriais sobrepostos com
   regras diferentes. A v3 instala a seção 3 (abertura em situação, tensão antes da
   solução, caso condutor, promessa cumprida, fechamento com callback, mostrar em
   vez de qualificar) e passa a ser fonte única, com prompts e resumos subordinados.

4. **Auto-correção de acento corrompendo português correto.** Achado colateral,
   e provavelmente o mais caro dos quatro. O `ACCENT_MAP` do `accent_checker.py`
   tratava homógrafos como erro de digitação, e o gate roda com `auto_fix=True`:
   "nos projetos" virava "nós projetos", "esta análise" virava "está análise",
   "seria bom" virava "séria bom", o imperativo "Analise os dados" virava
   "Análise os dados". Cada curso gerado saía com erro de gramática introduzido
   pelo próprio validador de qualidade. Descoberto ao rodar o validador contra a
   diretriz editorial nova: 14 achados, todos falsos. Os nove pares ambíguos
   foram movidos para `AMBIGUOUS_HOMOGRAPHS`, fora do dicionário de correção, e a
   responsabilidade passou para o `review.md`, que agora traz a tabela de
   desambiguação por classe gramatical. Regex cuida do inequívoco; contexto é
   trabalho do revisor LLM.

5. **Configuração decorativa: o gate que ninguém executava.** Ao propagar a v4,
   a verificação mostrou que `config/quality_rules.yaml` NÃO era lido por nenhum
   código do repositório. As "46 expressões banidas com gate de CI" que a
   auditoria responsabilizou pela doutrina de reprovação eram, na prática, as 18
   hardcoded em `content_checker.FORBIDDEN_CLICHES`. As 28 restantes nunca foram
   checadas, incluindo "especialistas apontam" e "estudos indicam", que a
   doutrina trata como marcador grave de atribuição vaga. `require_source_for_percentages`
   e `fail_if_unresolved_markers_above` também eram texto sem efeito. Corrigido
   com `src/validators/rules_loader.py`, que carrega o YAML em runtime com
   fallback seguro, e com a implementação dos dois checks (percentual sem fonte
   como aviso, marcador acima do teto como erro bloqueante). Lista ativa passou
   de 18 para 56 expressões.

Quatro regras práticas ao mexer em doutrina editorial neste repo:

1. Toda instrução de estilo precisa poder ser cumprida por um bom escritor humano
   sem contar palavras. Se vira aritmética durante a escrita, vira cacoete no
   texto. E antes de adicionar qualquer limiar novo, teste se ele é satisfazível
   junto com os que já existem.
2. Nenhuma regra de reprovação entra sozinha. Quem proíbe precisa dizer o que
   colocar no lugar, senão o caminho mais barato para passar no gate é escrever
   menos e dizer nada.
3. Todo validador com auto-correção deve ser rodado contra um texto que se sabe
   correto antes de entrar em produção. Falso positivo em validador que só
   reporta custa atenção; em validador que corrige, custa a qualidade que ele
   deveria proteger.
4. Antes de creditar proteção a um gate, confirme que o código lê o arquivo de
   regras. `grep` pelo nome do arquivo de config nos fontes leva dez segundos e
   evita meses de falsa segurança. Config que ninguém carrega não é governança,
   é documentação com aparência de governança.

Relacionadas: [[padrao-editorial-hsm-hbr]], [[ADR-001-adopcao-llm-wiki]].

---

## Linha do tempo (append-only, ordem reversa)

- **2026-08-11** — [evolução] v4 da diretriz, no mesmo dia da v3, fechando o que
  faltava: prova antes da escrita com a regra de proporção afirmação/prova e as
  quatro saídas antes do marcador (§2.2), promessa e tensão redigidas antes do
  esqueleto com o portão das três condições (§3.1), esqueleto por gênero (§3.2),
  abertura com sujeito de falha em artefato ou processo (§3.3), rótulo de tipo do
  caso condutor (§3.4), veto a escassez fabricada (§3.5), um pedido por peça com
  a fórmula de quatro peças (§3.6), travessão vetado em prosa mas tolerado em
  título, e travas verificáveis de revisão (§13). Nesta rodada apareceu o defeito
  5, a configuração decorativa.

- **2026-08-11** — [correção] v3 da diretriz: storytelling obrigatório (§3), veto a
  cota mecânica de ritmo (§4.8), estrutura visual reposicionada a serviço da decisão
  (§6). Propagado para `draft.md`, `review.md` e `humanize.md` (pt-br, raiz, en, es),
  `humanizer.py`, `stylometry_checker.py`, `content_checker.py` (teto de parágrafo de
  5 para 8 linhas), `voice_guard.py`, `quality_rules.yaml`, `CLAUDE.md`, `AGENTS.md`
  e `GEMINI.md`. Origem: curador reportou queda de qualidade nos conteúdos gerados.
- **2026-07-23** — [criação] v2 da diretriz e anexo `GUIA_ESCRITA_HUMANIZADA.md`
  (PRs #59 e #60), com pesquisa de junho e julho de 2026 sobre marcadores de texto
  sintético. A v2 já tratava estrutura, mas não revogou as cotas dos prompts nem
  cobria narrativa, e foi sob ela que a queda de qualidade apareceu.
