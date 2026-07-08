# Módulo 5 — Humanos, Governança e Specs: o Sistema Nervoso do Operating Model

## Aula 5.1 — Não é um júnior: é um júnior com alavancagem de staff engineer e julgamento não confiável
Meta: id=`humano-muda-de-funcao` | duracao=`20 min` | icone=`users`
Descrição: O humano não sai do loop — deixa de escrever código e revisar linha a linha para definir intenção, criar specs, revisar evidência e risco, e gerenciar dívida de validação.

### [text]
O agente de código não é um júnior comum: é um executor com alavancagem operacional de **staff engineer** — milhões de tokens processados, um diff gigantesco entregue em 45 minutos — combinada a um julgamento que ainda não é confiável. Por isso o humano não sai do loop: ele muda de função, de escritor de código para auditor de intenção, evidência e risco. Essa transição redefine o papel de todo sênior na organização.

A analogia que circula entre times é conhecida: "avalie o output do agente como avaliaria o de um júnior". Ela funciona como porta de entrada, mas o documento-fonte a corrige com uma ressalva decisiva. Nenhum júnior humano produz um diff de milhares de linhas em menos de uma hora atravessando dezenas de arquivos.

> A combinação é inédita: velocidade e alcance de staff engineer, julgamento de alguém que você ainda não pode deixar sozinho. Governar essa assimetria é o trabalho novo do humano.

Os dados sustentam o ceticismo estruturado. Segundo o **Stack Overflow Survey 2025**, 46% dos desenvolvedores desconfiam ativamente da precisão de ferramentas de IA, contra 33% que confiam — e os desenvolvedores mais experientes são exatamente os mais céticos. A verificação humana não é resistência cultural: é resposta racional à assimetria entre alavancagem e julgamento.

### [text]
Se o julgamento do agente não é confiável e a velocidade dele é ordens de grandeza maior, revisar linha a linha vira matematicamente impossível. A saída não é revisar mais — é mudar o que se revisa. O documento-fonte mapeia essa mudança na tabela antes/agora das funções do humano:

| Antes (SDLC tradicional) | Agora (Agentic Operating Model) |
|---|---|
| Escrever código | Definir intenção, restrições e critérios de sucesso |
| Revisar cada linha | Revisar evidência e risco |
| Estimar esforço | Estimar risco, custo de validação e confiança |
| Gerenciar sprint | Gerenciar fluxo, agentes e dívida de validação |
| Detalhar tarefas no backlog | Criar **specs verificáveis** |
| Aceitar "done" na palavra | Exigir pacote de evidências |
| Executar QA no final | Auditar pontos de decisão, exceções e alto blast radius |

A coluna da direita descreve o humano como **auditor de intenção e risco**: ele revisa spec, testes, evidências, riscos, pontos de decisão e tudo que tem alto blast radius. O que é rotineiro e de baixo risco desce para validação automatizada; o que é ambíguo, irreversível ou caro de errar sobe para o julgamento humano.

Há uma consequência econômica direta. Conforme o relatório DORA (2025), parte do tempo economizado na escrita de código é reempregado auditando, revisando e validando output de IA — fenômeno que o relatório nomeia de **verification tax**. A conta real da era agentic é essa — a IA reduz o custo de geração, mas aumenta a importância econômica da verificação.

### [tip]
Ao redistribuir o tempo dos seus sêniores, comece pelo blast radius, não pelo volume. Um sênior que passa duas horas por dia revisando evidências de mudanças em billing, autenticação e migrations protege mais valor do que um que revisa linha a linha vinte PRs de baixo risco. Use a coluna "agora" da tabela como job description provisória e ajuste a cada trimestre.

### [text]
A objeção previsível é que essa mudança "burocratiza" o trabalho. O argumento inverte a realidade: se você já tentou revisar linha a linha um diff de milhares de linhas gerado por agente, provavelmente já pagou o verification tax de forma desorganizada — revisando tudo com a mesma atenção e, portanto, revisando mal. Quem muda de função paga o mesmo imposto de forma deliberada — concentrado onde o risco mora.

Isso também explica por que os mais experientes são os mais céticos no Stack Overflow Survey 2025: eles reconhecem os padrões de erro que um output fluente esconde. Esse ceticismo é ativo, não paralisante. Ele se converte em specs melhores, testes-contrato e revisão por risco — os mecanismos dos módulos 3 e 4, agora com dono.

O saldo entre tempo economizado gerando e tempo gasto validando é mensurável. Ele reaparece no Módulo 6 como **AI Delivery Drag**, uma das quinze métricas do painel de board. A função nova do humano é justamente manter esse saldo positivo.

### [checkpoint]
-- **Exercício 1 — Redesenho de papel.** Para cada sênior do seu time, mapeie a distribuição de tempo atual entre as colunas "antes" e "agora" da tabela das sete funções. Proponha a realocação-alvo para o próximo trimestre e liste o que precisa existir antes (specs, evals, Evidence Manifests) para viabilizá-la.
-- **Exercício 2 — Análise do verification tax.** Meça em um sprint quanto tempo o time gastou validando output de IA versus quanto economizou gerando. Justifique o saldo encontrado — ele é o seu AI Delivery Drag local e será baseline no Módulo 6.
-- **Exercício 3 — Diagnóstico de ceticismo.** Com base na sua experiência como profissional, compare a postura dos seus devs mais e menos experientes frente ao output de agentes com o padrão do Stack Overflow Survey 2025 (46% desconfiam, 33% confiam). Avalie se o ceticismo dos sêniores está sendo convertido em mecanismo (testes, spot checks) ou desperdiçado em retrabalho.

## Aula 5.2 — Governança proporcional ao risco: os seis níveis de autonomia L0-L5 e os doze guardrails mínimos
Meta: id=`autonomia-l0-l5-guardrails` | duracao=`20 min` | icone=`shield`
Descrição: Não se aplica a mesma liberdade a um agente que lê documentação e a outro que altera billing: a autonomia é graduada de read-only a critical autonomy, com controles crescentes.

### [text]
Governança agentic não é um interruptor liga/desliga: é uma escala de seis níveis de autonomia, de **L0 (read-only)** a **L5 (critical autonomy)**, em que cada degrau adiciona permissões e exige controles proporcionais. Um agente que lê documentação não carrega o mesmo risco de um agente que altera billing, deploy, permissões ou dados de cliente. O princípio operacional: autonomia se concede por nível de risco, nunca por conveniência.

O erro mais comum das organizações é tratar "agente" como categoria única. Na prática, o mesmo modelo pode operar como analista inofensivo pela manhã e como operador de produção à tarde — e o controle precisa acompanhar a operação, não a ferramenta. A escala do problema cresce rápido. Segundo o Gartner, até o fim de 2026, 40% das aplicações corporativas estarão integradas com agentes de IA task-specific, contra menos de 5% hoje — cada integração nova é mais um ponto de autonomia que alguém precisa classificar e controlar.

A pressão para acertar isso não é teórica. O **OWASP Gen AI Security Project** cataloga as **Agentic AI Threats** como categoria própria de risco: autonomia, uso de ferramentas, memória, subagentes e tomada de decisão. No centro está a **Excessive Agency** — ferramentas, permissões ou autonomia excessivas que transformam uma alucinação, um prompt injection ou uma extensão comprometida em ação danosa real.

### [warning]
Segundo o Gartner (previsão para 2027), 40% das empresas irão descomissionar ou rebaixar agentes autônomos por falhas de governança. O padrão da falha é sempre o mesmo: autonomia concedida acima do que os controles sustentam, incidente, e retrocesso generalizado que queima a credibilidade do programa inteiro. O guia conjunto dos Five Eyes para agentic AI em infraestrutura crítica aponta a mesma direção — visibilidade, assurance e alinhamento com modelos de segurança existentes, sem jamais conceder acesso amplo ou irrestrito.

### [text]
O modelo de graduação do documento-fonte organiza a autonomia em seis níveis:

| Nível | Nome | Permissão | Exemplo | Controle mínimo |
|---|---|---|---|---|
| L0 | Read-only | Lê repo e docs, sem escrita | Análise de repositório, triagem | Audit logs |
| L1 | Draft | Produz rascunhos que o humano aplica | Sugestão de código e documentação | Revisão humana integral |
| L2 | PR sandbox | Escreve em branch isolada e abre PR | Implementação com CI completo | Branch protection + gates de CI |
| L3 | Act with approval | Executa ações mediante aprovação explícita | Merge, migration, deploy em staging | Approval gates + audit logs |
| L4 | Bounded autonomy | Age sozinho dentro de limites definidos | Rotinas repetíveis com allowlist e budget | Allowlist, budget caps, circuit breakers, rollback |
| L5 | Critical autonomy | Produção sensível (billing, permissões, dados de cliente) | Ação autônoma em sistema crítico | Governança pesada — ou nível evitado |

A leitura executiva da tabela: a maioria dos times deveria operar entre L1 e L3 hoje, subir para L4 apenas em fluxos com validação madura, e tratar L5 como exceção justificada caso a caso — muitas vezes a decisão correta é não conceder.

Sustentando a escala, o documento-fonte define os **doze guardrails mínimos** de qualquer operação agentic:

-- **Least privilege**: cada agente com o mínimo de acesso necessário à tarefa.
-- **Command allowlist**: comandos permitidos enumerados, não inferidos.
-- **Protected files**: arquivos sensíveis fora do alcance de escrita.
-- **Branch protection**: nenhuma escrita direta em branches protegidas.
-- **Budget caps**: teto de tokens e custo por execução e por período.
-- **Audit logs**: toda ação registrada e atribuível.
-- **Approval gates**: aprovação humana explícita em cada ponto definido.
-- **Rollback automático**: toda mudança reversível por mecanismo, não por heroísmo.
-- **Canary deploy**: exposição gradual antes de tráfego total.
-- **Circuit breakers**: interrupção automática ao detectar comportamento anômalo ou estouro de budget.
-- **Segregation of duties**: quem executa não aprova; quem aprova não executa.
-- **Human approval para alto blast radius**: nenhuma ação de dano potencial amplo sem humano no gate.

### [tip]
Implante a escala pelo caminho inverso do entusiasmo: comece classificando o que já roda (CI bots, crons, agentes de código) antes de autorizar qualquer coisa nova. Na prática, três guardrails destravam a subida de nível com mais frequência — budget caps, circuit breakers e segregation of duties — porque são os que faltam em setups montados às pressas. A síntese do documento-fonte vale como critério de decisão: "A governança boa não mata velocidade. Ela impede que velocidade vire passivo." — Alexandre Caramaschi

### [checkpoint]
-- **Exercício 4 — Censo de autonomia.** Inventarie todos os agentes e automações com acesso ao seu ambiente no seu dia a dia (CI bots, agentes de código, crons) e classifique cada um em L0-L5. Sinalize os que operam acima do nível que o controle atual sustenta — esses são os candidatos ao cenário Gartner de descomissionamento até 2027.
-- **Exercício 5 — Gap de guardrails.** Para o agente de maior autonomia do censo, verifique os doze guardrails um a um e projete o plano de 30 dias para fechar os três gaps mais críticos, com dono e evidência de fechamento por item.
-- **Exercício 6 — Julgamento de L5.** Escolha um fluxo sensível da sua operação (billing, permissões ou dados de cliente) e justifique por escrito, em dez linhas, a decisão de conceder ou vetar autonomia L5 — usando Excessive Agency (OWASP) e o guia Five Eyes como critérios.

## Aula 5.3 — SDD como sistema nervoso: do Spec Kit ao Spec Acceptance Pack de onze artefatos
Meta: id=`sdd-spec-acceptance-pack` | duracao=`20 min` | icone=`file-text`
Descrição: Spec-Driven Development deixou de ser boa prática e virou infraestrutura: agentes são literal-minded pair programmers, e sem intent, non-goals, risk map e evidence requirements a entrega é vibe shipping com verniz corporativo.

### [text]
**Spec-Driven Development (SDD)** deixou de ser boa prática de documentação e virou infraestrutura do Agentic Operating Model: é a spec que conecta a intenção humana à validação automatizada, funcionando como contrato executável entre quem define o problema e o agente que o resolve. Sem spec verificável, a governança da aula anterior não tem o que proteger e a validação dos módulos 3 e 4 não tem contra o que verificar.

A razão é da natureza dos agentes. O **GitHub Blog** os define como "literal-minded pair programmers" — parceiros de programação que interpretam ao pé da letra e, por isso, precisam de instruções não ambíguas. Cada frase vaga em uma issue não desaparece: ela transfere a decisão para o agente, que decidirá com o julgamento não confiável da Aula 5.1.

O fluxo de referência é o **Spec Kit** (Microsoft Developer): requisitos transformados em planos, tarefas e validação através de sete fases — **Constitution, Specify, Clarify, Plan, Tasks, Implement, Validate**. O argumento central da Microsoft é econômico: clareza cedo reduz retrabalho caro depois. Boas specs capturam intenção, restrições e critérios de aceite antes de qualquer token ser gasto em implementação.

### [text]
Martin Fowler e a Thoughtworks descrevem a maturidade dessa prática em três níveis: **spec-first** (a spec existe antes do código), **spec-anchored** (o código permanece ancorado na spec ao longo da evolução) e **spec-as-source** (a spec é a fonte de verdade da qual código e testes derivam). Em todos, a spec é fonte de verdade compartilhada entre humano e agente — artefato vivo, não documento morto.

Para operacionalizar, o documento-fonte propõe o **Spec Acceptance Pack**: onze artefatos, cada um respondendo a uma pergunta que, sem resposta explícita, vira decisão implícita do agente.

| Artefato | Pergunta que responde |
|---|---|
| Intent | Qual problema estamos resolvendo? |
| Non-goals | O que está explicitamente fora do escopo? |
| Acceptance criteria | O que prova, de forma verificável, que a entrega atendeu? |
| Risk map | O que pode dar errado e qual o blast radius? |
| Architecture constraints | Que limites de arquitetura o código deve respeitar? |
| Test strategy | Como a mudança será testada, e em que camadas? |
| Agent policy | O que o agente pode decidir sozinho e o que escala para humano? |
| Tool permissions | Quais ferramentas e acessos o agente recebe (nível L0-L5)? |
| Rollback plan | Como a mudança é desfeita se algo falhar? |
| Evidence requirements | Quais provas devem acompanhar a entrega no Evidence Manifest? |
| Budget | Quanto token, tempo e custo podemos queimar? |

Repare como o pack costura o curso inteiro: acceptance criteria e evidence requirements alimentam a Definition of Verified (Módulo 3); test strategy alimenta o TDD como contrato (Módulo 4); agent policy e tool permissions materializam o L0-L5 desta aula; budget conecta com o model routing (Módulo 2) e com as métricas de board (Módulo 6).

### [tip]
Não transforme o pack em burocracia de onze documentos: os onze artefatos cabem em uma página. Preencha na ordem intent, non-goals e acceptance criteria primeiro — se esses três não saírem em minutos, a entrega não está pronta para ser delegada a agente nenhum. Cronometre o exercício: se o pack de uma entrega comum leva mais de 90 minutos, o gargalo está na clareza da intenção, não no template.

### [text]
A régua de corte do documento-fonte é direta:

> "Sem isso, não é AI-native engineering. É vibe shipping com verniz corporativo." — Alexandre Caramaschi

"Vibe shipping" é o anti-padrão: delegar a partir de uma frase vaga, aceitar o diff porque parece bom e chamar de inovação. O verniz corporativo — cerimônias, dashboards, nomenclatura agentic — não muda a natureza do processo se a decisão do que é sucesso continuar implícita.

O contraste define o sistema nervoso do operating model. A spec transporta a intenção (Aula 5.1) até a validação; a governança L0-L5 (Aula 5.2) define com que liberdade o agente percorre esse caminho; o Spec Acceptance Pack registra as decisões para que nenhuma delas seja tomada por omissão. Com esses três elementos, o Módulo 6 pode fechar o modelo com forecast probabilístico e métricas de board — porque passa a existir algo verificável para medir.

### [checkpoint]
-- **Exercício 7 — Pack em 1 página.** Escolha um problema real do seu roadmap e crie o Spec Acceptance Pack completo, com os onze artefatos em no máximo uma página. Cronometre; se levar mais de 90 minutos, diagnostique onde a intenção está vaga.
-- **Exercício 8 — Auditoria de ambiguidade.** Pegue 3 issues abertas do backlog e marque cada frase que um "literal-minded pair programmer" interpretaria de duas formas. Reescreva as três piores como acceptance criteria verificáveis.
-- **Exercício 9 — Avaliação de maturidade SDD.** Classifique seu time em spec-first, spec-anchored ou spec-as-source, justificando com exemplos do último mês — e projete o que precisaria mudar no fluxo de PR para subir um nível em um trimestre.
