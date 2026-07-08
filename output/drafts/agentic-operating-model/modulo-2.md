# Módulo 2 — Agentic Delivery: o Novo SDLC e a Orquestração por Camadas

## Aula 2.1 — O novo SDLC: de software delivery para Agentic Delivery
Meta: id=`do-sdlc-ao-agentic-delivery` | duracao=`20 min` | icone=`workflow`
Descrição: Lado a lado, o velho modelo (demanda, estimativa, implementação, QA, review, deploy) e o novo (intenção, orquestração, execução multi-modelo, crítica adversarial, revisão por risco, evidência anexada, forecast por regime).

### [text]
**Agentic Delivery** é o ciclo de vida de software redesenhado para trabalho executado por agentes de IA: parte de intenção e critérios de sucesso, passa por um orquestrador que planeja, decompõe e valida, e distribui a execução entre camadas de modelos e ferramentas determinísticas. Segundo o Gartner, até 2027 mais de 65% dos times que usam agentic coding tratarão IDEs como opcionais — controle, governança e validação migram para plataformas automatizadas.

Antes de redesenhar o fluxo, vale nomear o que ele substitui. O modelo tradicional de delivery opera em sete passos que, como profissional de engenharia, você provavelmente já executou de memória no seu dia a dia:

-- O PM escreve a demanda no backlog.
-- O time estima em pontos ou horas.
-- O dev implementa.
-- O QA testa.
-- O code review valida linha a linha.
-- O DevOps sobe para produção.
-- As métricas aparecem depois, se aparecerem.

Esse desenho já vinha sendo pressionado por Agile e DevOps havia duas décadas. Com agentes, ele se torna estruturalmente insuficiente: o Gartner descreve a transição de **`AI-assisted development`** para **agentic software development** ao longo de todo o SDLC — e um pipeline desenhado para humanos digitando código não tem onde encaixar um agente que produz um diff de milhares de linhas em minutos.

> O gargalo deixou de ser escrever código. O gargalo passou a ser provar que o código escrito por agentes está correto, seguro e aderente à intenção.

### [text]
O novo modelo tem oito passos, e a diferença central não é a automação — é onde nascem os critérios de sucesso e onde a prova é anexada:

-- O humano define **intenção**, restrições e critérios de sucesso mensuráveis.
-- O **orquestrador** cria o plano e o workflow de validação.
-- Modelos diferentes executam partes diferentes do trabalho (model routing, detalhado na Aula 2.3).
-- Ferramentas determinísticas validam: build, lint, typecheck, testes.
-- Agentes revisores fazem **crítica adversarial** sobre o output.
-- Humanos revisam por risco, não por volume.
-- As evidências são anexadas ao PR — não afirmadas em stand-up.
-- O forecast é recalibrado por regime de trabalho, não por histórico bruto.

Repare na inversão de sequência. No velho modelo, a validação era uma fase (QA) posicionada depois da implementação; no novo, o workflow de validação é criado no passo dois, antes de qualquer código existir. A McKinsey observa o mesmo padrão nas empresas que mais capturam valor com IA: elas não compram ferramenta — rearquitetam o delivery inteiro e reposicionam humanos como orquestradores, validadores de arquitetura e gestores de qualidade.

Dois passos merecem atenção executiva porque são os que quase nunca existem hoje. A crítica adversarial — um agente revisor tentando quebrar o trabalho de outro — e a evidência anexada ao PR reaparecem no Quality Evidence Stack (Módulo 3) e no papel do humano como auditor de risco (Módulo 5). São a peça que separa Agentic Delivery de simplesmente "usar IA mais rápido".

### [text]
A mudança de paradigma completa, tal como o documento-fonte a sistematiza, cabe em dez pares antes/depois:

| Antes (software delivery) | Depois (Agentic Delivery) |
|---|---|
| Backlog item | Spec executável |
| Story point | Risco de variação + custo de validação |
| Dev como executor | Dev como orquestrador |
| IA como copiloto | IA como força de trabalho agentic |
| Code review manual | Revisão multiagente + humana por risco |
| CI/CD | Trust pipeline |
| Definition of Done | **Definition of Verified** |
| Velocity | **Trust Velocity** |
| Custo por dev | Custo por mudança verificada |
| Squad como capacidade de execução | Squad como ownership, contexto e governança |

Cada linha é uma decisão de redesenho, não uma troca de vocabulário. Um backlog item vira **spec executável** quando carrega intenção, restrições e critérios verificáveis que um agente consegue executar sem ambiguidade. O story point deixa de medir esforço humano de digitação e passa a precificar **risco de variação + custo de validação** — a estimativa relevante quando o código nasce em minutos. E o CI/CD vira **trust pipeline** quando deixa de apenas compilar e passa a produzir o pacote de provas que sustenta o merge.

A linha mais cara de ignorar é a da revisão. Segundo o Stack Overflow Survey 2025, 46% dos desenvolvedores desconfiam ativamente da precisão de ferramentas de IA, contra 33% que confiam — e os mais experientes são os mais céticos. Revisar por risco, não por volume, é a única forma de honrar esse ceticismo sem afogar os seniores em diffs gigantescos.

### [tip]
Comece a migração pelo vocabulário dos artefatos, não pela ferramenta. Reescreva os próximos cinco itens do backlog com três campos obrigatórios: intenção, restrições e critérios de sucesso mensuráveis. Se um agente "literal-minded" não conseguiria executar o item sem perguntar nada, ele ainda é backlog item — não é spec executável. É um teste que você pode aplicar imediatamente: custa uma tarde e revela mais sobre a maturidade do time do que qualquer avaliação de ferramenta.

### [checkpoint]
-- **Exercício 1 — Re-desenho de fluxo.** Pegue a última feature relevante entregue pelo seu time e reconte a história dela seguindo os oito passos do Agentic Delivery. Marque em vermelho cada passo que hoje não existe ou é informal — tipicamente a crítica adversarial e a evidência anexada ao PR. Apresente o resultado ao tech lead e priorize um passo para formalizar neste trimestre.
-- **Exercício 2 — Tradução de vocabulário.** Reescreva 5 itens do seu backlog atual como specs executáveis, com intenção, restrições e critérios de sucesso mensuráveis. Compare o tempo de escrita com o tempo que o time gastaria esclarecendo ambiguidades no meio do sprint.
-- **Exercício 3 — Análise da tabela.** Dos dez pares antes/depois, avalie se a sua organização já opera cada linha: classifique em "já operamos assim", "em transição" ou "nem começamos" — e justifique com um exemplo concreto do último mês.

## Aula 2.2 — Ultracode não é modo mágico: é camada de planejamento, decomposição, verificação e auditoria
Meta: id=`ultracode-orquestrador-nao-modo-magico` | duracao=`20 min` | icone=`layers`
Descrição: O modo de raciocínio premium deve ser tratado como board member técnico da execução — não como estagiário caro fazendo batch job — e a pergunta certa não é "uso ou não", mas "qual etapa merece raciocínio premium".

### [text]
**Ultracode** — o modo de raciocínio premium — não é um botão que melhora qualquer tarefa: é uma camada de planejamento, decomposição, verificação e auditoria. Se o modelo cria sozinho o workflow de validação, ele opera como orquestrador, não como mais um gerador de código. A documentação da Anthropic adverte que **dynamic workflows** consomem significativamente mais recursos, e a recomendação explícita é começar com escopos menores antes de escalar.

O ponto de partida analítico é observar o que o modo premium efetivamente produz quando bem usado: plano, decomposição em subtarefas, mapa de riscos, critérios de validação e revisão adversarial do trabalho executado. Nenhum desses artefatos é código de feature. São artefatos de **orquestração** — o mesmo tipo de output que se espera de um staff engineer desenhando uma execução, não de alguém digitando a execução.

Na prática dos dynamic workflows descritos pela Anthropic, o padrão é concreto: o modelo escreve scripts de orquestração, dispara dezenas ou centenas de **subagentes** em paralelo e verifica o trabalho antes de consolidar. O raciocínio premium fica no topo da pirâmide, decidindo e auditando; o volume de execução desce para camadas mais baratas.

> "Modelo premium deve ser usado como board member técnico da execução, não como estagiário caro fazendo batch job." — Alexandre Caramaschi

### [warning]
A pegadinha executiva está no custo composto. Dynamic workflows consomem significativamente mais tokens e recursos do que o uso convencional — a própria Anthropic recomenda validar em escopos menores antes de escalar. O anti-padrão clássico é o time descobrir o modo premium, ligá-lo para tudo e apresentar ao CFO uma fatura que triplicou sem nenhuma métrica de mudança verificada para justificá-la. Escalar orquestração sem governança de custo é a versão financeira do débito técnico: invisível no demo, dolorosa no fechamento do mês.

### [text]
A maturidade chega quando a pergunta muda. "Uso Ultracode ou não?" é uma pergunta binária sobre ferramenta; a pergunta correta é: **qual etapa do fluxo merece raciocínio premium, e qual pode ser executada por modelos mais baratos ou por ferramentas determinísticas?**

Essa troca reorganiza o pipeline inteiro em torno de uma alocação, não de uma adesão:

-- Decisão de arquitetura, decomposição de problema ambíguo, revisão adversarial de mudança crítica: candidatas legítimas a raciocínio premium.
-- Refactor mecânico, geração de testes a partir de spec clara, pesquisa no repositório, documentação: trabalho de modelos intermediários ou eficientes.
-- Build, lint, typecheck, execução de testes: ferramentas determinísticas, custo marginal próximo de zero e resultado binário.

O critério de corte é o valor do julgamento na etapa. Onde um erro de decisão contamina todo o trabalho a jusante — o plano errado gera cem subagentes executando a coisa errada — o raciocínio premium se paga. Onde a tarefa é repetível e verificável por teste, pagar preço de board member por trabalho de batch job é desperdício puro.

O custo, aliás, é variável de projeto, não rodapé de fatura. Há diferenças materiais de preço entre modelos como Fable, Opus, Sonnet e Haiku, e alavancas como prompt caching e o runtime de agentes alteram a conta de forma significativa — tema da próxima aula, onde essa alocação vira topologia formal de cinco camadas.

### [tip]
Institua a regra do "um ponto premium por entrega": ao planejar qualquer entrega relevante, o time declara antecipadamente qual único ponto do workflow exige raciocínio premium — em geral o plano inicial ou a revisão adversarial final. Se alguém quiser um segundo ponto, precisa justificar por risco, não por conveniência. A regra força a conversa de alocação antes do gasto e cria o hábito que a métrica Model Mix Efficiency (Módulo 6) vai medir depois.

### [checkpoint]
-- **Exercício 4 — Auditoria de desperdício premium.** Liste os últimos 5 usos de modelo de raciocínio elevado no seu fluxo e classifique cada um como decisão/arquitetura (uso correto) ou tarefa repetível (desperdício). Estime o custo evitável em reais por mês se os usos incorretos descessem uma camada.
-- **Exercício 5 — Desenho de workflow.** Para um problema real do próximo sprint, escreva o workflow que o orquestrador deveria criar — decomposição em subtarefas, subagentes envolvidos, pontos de verificação — e marque o único ponto que exige raciocínio premium. Defenda a escolha diante do tech lead.
-- **Exercício 6 — Justificativa executiva.** Redija o parágrafo que você usaria para explicar ao seu CFO por que o gasto com o modo premium deve subir na etapa de planejamento e cair na etapa de execução — usando a lógica de board member versus estagiário caro.

## Aula 2.3 — Model routing como disciplina econômica: a topologia de cinco camadas de execução
Meta: id=`model-routing-topologia-cinco-camadas` | duracao=`20 min` | icone=`scale`
Descrição: Premium define plano e revisão adversarial; intermediários executam refactors; eficientes fazem tarefas repetíveis; ferramentas determinísticas validam; o humano sênior arbitra riscos e trade-offs.

### [text]
**Model routing** é a disciplina de colocar o modelo certo, na etapa certa, com a permissão certa, pelo custo certo. A topologia recomendada tem cinco camadas: premium define plano e revisão adversarial; intermediários executam refactors; eficientes fazem tarefas repetíveis; ferramentas determinísticas validam; o humano sênior arbitra riscos e trade-offs. Como a documentação de preços da Anthropic mostra diferenças materiais de custo entre modelos como Fable, Opus, Sonnet e Haiku, o roteamento é decisão econômica, não apenas técnica.

A analogia útil vem da própria gestão. Nenhum CTO aloca o arquiteto mais caro da empresa para renomear variáveis, nem delega a decisão de migração de banco ao estagiário — e ninguém chama isso de "política de RH": chama-se alocação de capacidade por valor. Com modelos de IA, a mesma lógica ganha precisão de tabela de preços, porque cada camada tem custo por token conhecido e publicado.

O erro comum é tratar o roteamento como preferência individual do dev ("eu gosto de usar o modelo X"). Em Agentic Delivery, o roteamento é política de engenharia: uma matriz explícita de tipo de tarefa por camada de execução, com dono, revisão periódica e uma métrica de board que a audita — **Model Mix Efficiency**, apresentada no Módulo 6.

### [text]
A topologia de cinco camadas, conforme o documento-fonte a recomenda:

| Camada | Quem executa | Responsabilidade |
|---|---|---|
| 1. Premium / Ultracode | Modelo de raciocínio elevado | Plano, riscos, critérios de validação, decomposição, revisão adversarial |
| 2. Intermediária | Modelos de capacidade média | Refactors, sínteses, mudanças complexas de código |
| 3. Eficiente | Modelos rápidos e baratos | Pesquisa no repo, alterações repetíveis, geração de testes, documentação |
| 4. Determinística | Ferramentas clássicas | Build, lint, typecheck, tests, SAST, dependency scan, load test |
| 5. Humano sênior | Tech lead / staff / CTO | Riscos, arquitetura, segurança, produto, testes, trade-offs |

Duas leituras estruturais importam. Primeira: a camada 4 não é opcional nem "menos nobre" — ferramentas determinísticas produzem veredito binário a custo marginal quase nulo, e tudo que puder ser verificado por elas não deveria consumir token de modelo algum. Segunda: o humano sênior é uma camada de execução do pipeline, com responsabilidade definida — arbitrar o que nenhuma automação arbitra —, não um supervisor externo olhando por cima do ombro.

O fluxo típico de um PR atravessa as camadas em forma de ampulheta: nasce na camada 1 (plano e decomposição), engorda nas camadas 2 e 3 (execução paralela), é espremido pela camada 4 (validação determinística) e volta a subir — revisão adversarial na camada 1, arbitragem de risco na camada 5. O contexto dessa disciplina é o mercado que o Módulo 1 descreveu. Segundo o Gartner, até o fim de 2026 40% das aplicações corporativas estarão integradas com agentes task-specific, contra menos de 5% hoje — e a mesma consultoria estima até US$ 234 bilhões em gastos com SaaS expostos ao agentic arbitrage (Gartner, projeção para 2030). Quem orquestra em cinco camadas opera essa escala; quem usa um modelo único para tudo paga por ela.

### [tip]
Antes de otimizar o roteamento, capture as duas alavancas de custo que independem dele: prompt caching e o runtime de agentes. Cachear o contexto estável (spec, convenções do repo, instruções de sistema) reduz o custo de cada chamada subsequente, e o runtime determina quantas chamadas uma tarefa consome de fato. Um roteamento perfeito sobre prompts sem cache pode custar mais do que um roteamento mediano com caching bem configurado — meça as duas coisas juntas.

### [text]
A regra de ouro do operating model, antecipando a conclusão do curso: **o modelo certo, na etapa certa, com a permissão certa, pelo custo certo**. Cada um dos quatro termos é um eixo de governança — capacidade, posição no fluxo, autonomia concedida e unit economics — e a topologia de cinco camadas é a forma operacional de cumprir os quatro ao mesmo tempo.

> "Usar modelo premium para tudo é desperdício. Usar modelo barato para decisão crítica é risco." — documento-fonte, conclusão 20.6

Os dois erros são simétricos e igualmente caros. O primeiro aparece na fatura: paga-se preço de raciocínio elevado por triagem de issue e geração de boilerplate. O segundo aparece no incidente: uma decisão de arquitetura ou uma mudança de alto blast radius delegada a um modelo eficiente, sem revisão adversarial nem arbitragem humana, cujo custo só se revela em produção.

A disciplina fecha o ciclo com medição. **Cost per Verified Change** — o custo por mudança verificada, componente da nova unidade de produção do Módulo 1 — só é gerenciável quando o roteamento é política explícita; e a Model Mix Efficiency, no painel de board do Módulo 6, mede exatamente se cada classe de tarefa está rodando na camada certa. Sem matriz de roteamento, essas métricas não têm o que medir: há apenas gasto agregado e intuição.

### [checkpoint]
-- **Exercício 7 — Matriz de roteamento.** Construa a tabela tarefa × camada para as 10 tarefas mais frequentes do seu time (triagem de issue, geração de teste, refactor, migration, revisão adversarial, documentação, pesquisa no repo, entre outras) e valide com o tech lead onde a matriz diverge da prática atual. Cada divergência é desperdício ou risco — classifique qual.
-- **Exercício 8 — Simulação de unit economics.** Para um PR típico, estime o custo do fluxo "tudo premium" versus o fluxo roteado pela topologia de cinco camadas, usando a tabela de preços pública dos modelos que seu time usa. Calcule a economia percentual e descreva o risco que o roteamento introduz (e como a camada 5 o mitiga).
-- **Exercício 9 — Projeto de política.** Redija a política de roteamento de uma página para o seu time — camadas, tipos de tarefa por camada, exceções permitidas, dono da matriz e cadência de revisão — e defina como a aderência será auditada quando a Model Mix Efficiency entrar no painel.
