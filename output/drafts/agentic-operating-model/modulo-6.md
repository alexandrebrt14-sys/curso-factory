# Módulo 6 — O Operating Model Completo: Forecast, Métricas de Board, Tiny Teams e Cadência

## Aula 6.1 — Histórico com prazo de validade: forecast probabilístico e o painel de board com Trust Velocity
Meta: id=`forecast-pos-ia-metricas-de-board` | duracao=`20 min` | icone=`bar-chart`
Descrição: Por que o histórico de velocity vira fóssil estatístico quando o regime muda, como montar um forecast em camadas com confiança P50-P75 e qual painel de quinze métricas substitui story points na conversa com o board.

### [text]
Com agentes de IA no delivery, o histórico de produtividade tem prazo de validade: a distribuição estatística muda sempre que muda o regime — modelo, prompt, workflow, budget. A resposta não é abandonar previsão, e sim encurtá-la e torná-la probabilística: forecast em camadas (7-14 dias, 4-6 semanas, 3 meses) e um painel de board centrado em **Trust Velocity** — mudanças verificadas por unidade de tempo, custo e risco.

Você provavelmente já viveu isso no modelo antigo: três meses de velocity estável davam uma base razoável para prometer um trimestre. Na era agentic, esse mesmo histórico pode ser um **fóssil estatístico**. O motivo é estrutural, não circunstancial: com agentes, a distribuição que gera seus números muda toda vez que muda o regime de execução.

O documento-fonte cataloga onze fatores que alteram o regime — e, portanto, invalidam o histórico bruto:

-- Modelo utilizado
-- Modo de execução (assistido, agentic, orquestrado)
-- Prompt padrão
-- Workflow de orquestração
-- Ferramenta em uso
-- Servidores MCP conectados
-- Suíte de testes
-- Política de permissão dos agentes
-- Cobertura de contexto disponível para o agente
-- Estratégia de orquestração (subagentes, revisão adversarial)
-- Budget de tokens por tarefa

> Se qualquer um desses onze fatores mudou no último mês, seu histórico de três meses não descreve o sistema que você opera hoje. Comprometer prazo em cima dele é falsa precisão.

Segundo o DORA 2025, a IA é um **amplificador das forças e fraquezas organizacionais** — o maior ROI não vem da ferramenta isolada, mas do sistema organizacional subjacente. Essa é a moldura executiva. Um sistema de forecast frágil, amplificado por agentes, produz promessas mais rápidas e igualmente erradas.

### [text]
A solução do documento-fonte é o **forecast pós-IA em camadas**, com pesos decrescentes conforme a distância do regime atual:

| Janela de dados | Papel no forecast | Como usar |
|---|---|---|
| Últimos 7-14 dias | Regime atual | Base primária: reflete modelo, prompts e workflow vigentes |
| Últimas 4-6 semanas | Forecast operacional | Compromissos de curto prazo com bandas de confiança |
| Últimos 3 meses | Referência contextual | Contexto e sazonalidade — nunca base de compromisso |
| Pré-mudança grande de regime | Arquivo histórico | Registro para auditoria, não insumo de previsão |

Sobre essa base, o **roadmap board-ready** troca a lista de features com datas por uma tabela fiduciária: frente × outcome × KPI × janela × confiança (P50-P75) × risco × **evidence gate**. Cada linha declara o que será entregue, como se mede, com que probabilidade e qual evidência destrava a próxima etapa.

A conversa com o stakeholder muda de gramática. Sai "entregamos X no dia Y"; entra "temos P75 de entregar este outcome nesta janela, desde que os evidence gates sejam cumpridos". É menos teatral — e mais fiduciário, porque expõe incerteza em vez de escondê-la.

O DORA e o Google Cloud (2025) sustentam a urgência dessa tradução: ganhos de velocidade em coding **não se convertem automaticamente em resultado financeiro** — líderes precisam conectar engenharia, valor e outcomes. O roadmap board-ready é exatamente esse conector.

### [tip]
Não tente implantar as camadas e o painel inteiro de uma vez. Escolha duas frentes do roadmap atual, reescreva-as no formato board-ready com confiança P50-P75 e apresente ao seu par de produto antes da reunião de board. As objeções que surgirem revelam onde falta evidence gate — e esse diagnóstico vale mais do que o template preenchido.

### [text]
O painel AI-native do documento-fonte tem quinze métricas, organizadas em torno de uma métrica-mãe:

> "Trust Velocity = mudanças verificadas por unidade de tempo, custo e risco." — Alexandre Caramaschi, documento-fonte

As quinze métricas do painel:

-- **Trust Velocity** — a métrica-mãe: quanto resultado verificado o sistema produz
-- **Cost per Verified Change** e **Token Burn Rate** — a dimensão econômica
-- **Validation Debt** e **AI Delivery Drag** — o passivo de verificação acumulado
-- **Model Mix Efficiency** — se o roteamento de modelos (Módulo 2) está correto
-- **Regression Rate**, **Change Failure Rate** e **Deployment Rework Rate** — a estabilidade
-- **Evidence Completeness**, **Test Review Coverage** e **Spec Clarity Score** — a qualidade dos insumos e das provas
-- **Prompt/Agent Drift Score** e **Safety Near Misses** — o comportamento dos agentes
-- **Estimate TTL Breach** — quantas estimativas venceram antes da entrega

Nenhuma delas é story point. Todas respondem às perguntas que o board deveria fazer no lugar de "quantos pontos entregamos?" — quantas mudanças verificadas saíram, a que custo, com que taxa de regressão, com quanta dívida de validação. O documento-fonte lista nove dessas perguntas; a lição executiva é que o painel existe para respondê-las, não para decorar slide.

Repare também na conexão entre o painel e o forecast: **Estimate TTL Breach** mede quantas estimativas venceram antes da entrega — ou seja, quantas vezes o regime mudou mais rápido do que a previsão feita sobre ele. Quando essa métrica sobe, o sinal não é "o time estima mal"; é que a janela de forecast precisa encurtar. O painel e as camadas de previsão são o mesmo sistema visto de dois ângulos: um mede, o outro promete.

### [checkpoint]
-- **Exercício 1 — Roadmap board-ready.** Reescreva as 3 frentes principais do seu roadmap atual — um cenário real da sua operação, não um exemplo de laboratório — no formato frente × outcome × KPI × janela × confiança (P50-P90) × risco × evidence gate. Apresente ao seu par de produto e registre as objeções — cada objeção aponta um gate mal definido.
-- **Exercício 2 — Painel mínimo.** Das quinze métricas, selecione as 5 que sua organização consegue medir em 30 dias com dados existentes (Regression Rate, Change Failure Rate e Token Burn Rate costumam já ter fonte) e defina a fórmula operacional de cada uma, com origem do dado e dono da medição.

## Aula 6.2 — Tiny teams e as cinco camadas do Agentic Operating Model: Intent, Spec, Orchestration, Verification, Governance
Meta: id=`tiny-teams-operating-model-cinco-camadas` | duracao=`20 min` | icone=`layers`
Descrição: Squads continuam existindo, mas mudam de propósito: menores, muito mais sofisticados, com seis novas capacidades, operando um modelo de cinco camadas onde nascem previsibilidade, alavancagem, confiança e escala.

### [text]
Tiny teams não são corte de custo: são squads menores e muito mais sofisticados, que trocam distribuição de tarefas por garantia de contexto e accountability. Segundo a Gartner, até 2029, 60% das organizações adotarão tiny software engineering teams em escala, contra 15% em 2026. Esses times operam um modelo de cinco camadas — Intent, Spec, Orchestration, Verification, Governance — sustentado por seis novas capacidades.

A provocação que abre a aula vem do próprio documento-fonte: se uma pessoa com agentes entrega ponta a ponta, squads ainda fazem sentido? A resposta é sim — mas não como antes. O squad deixa de ser um pool de capacidade de codificação e vira uma unidade de **ownership, contexto e governança**.

Os números do Gartner dimensionam a transição: os times de referência têm 4-5 pessoas hoje e podem chegar a 2-3 conforme skills e IA amadurecem. A condição que costuma ser ignorada: tiny teams **exigem platform teams** e capacidades novas — PM, UX/AX designer, AI-native software engineer. Encolher o squad sem construir a plataforma embaixo é demissão disfarçada de estratégia.

### [text]
O documento-fonte descreve o novo squad em sete transições de propósito:

| Squad tradicional | Squad AI-native |
|---|---|
| Distribui tarefas entre devs | Garante contexto e accountability |
| QA valida no fim | Validação nasce na spec |
| Tech Lead revisa código | Tech Lead revisa arquitetura, testes e risco |
| Capacidade medida em pessoas | Capacidade medida em orquestração e verificação |
| Estima esforço | Estima risco, validação e confiança |
| Rituais de status | Inspeção de evidências e agent runs |
| Cresce contratando | Cresce sofisticando plataforma e agentes |

Sustentando essas transições, seis novos papéis — **capacidades, não cargos**:

-- **Intent Architect** — transforma problema de negócio em spec verificável
-- **Agent Orchestrator** — desenha workflow, escolhe modelos, define permissões
-- **Validation Engineer** — constrói harnesses, evals e evidence gates
-- **AI Unit Economist** — mede custo, token e model mix por outcome
-- **Agent Safety Lead** — mantém guardrails e circuit breakers
-- **Outcome Auditor** — verifica o valor real da entrega, não a atividade

### [tip]
Trate os seis papéis como chapéus, não como headcount. Em um squad de quatro pessoas, uma pessoa acumula duas ou três capacidades, e parte delas pode ser parcialmente agentic (um agente de evals cobre metade do trabalho do Validation Engineer). O erro caro é a capacidade descoberta: ninguém responde por unit economics ou por safety, e a lacuna só aparece no incidente. Avalie se, no seu squad atual, alguma das seis está sem dono — essa é a primeira lacuna a fechar.

### [text]
As capacidades operam dentro do **Agentic Operating Model em cinco camadas** — a arquitetura que consolida todo o curso:

| Camada | O que nasce nela | Módulo de origem |
|---|---|---|
| Intent Layer | Direção — intenção clara e critérios de sucesso | M1, M5 |
| Spec Layer | Previsibilidade — specs verificáveis, Spec Acceptance Pack | M5 |
| Agent Orchestration Layer | Alavancagem — model routing, subagentes, workflows | M2 |
| Verification Layer | Confiança — Quality Evidence Stack, Definition of Verified, evals | M3, M4 |
| Governance Layer | Escala corporativa — autonomia L0-L5, guardrails, auditoria | M5 |

> "Sem intenção clara, agente só acelera ambiguidade." — Alexandre Caramaschi, documento-fonte, sobre a Camada 1

A ordem das camadas importa. Orquestração sem spec produz volume sem previsibilidade; verificação sem governança produz confiança que não escala. E o risco de pular a última camada tem número: o Gartner estima que até 2027, 40% das empresas descomissionarão ou rebaixarão agentes autônomos por falhas de governança. O fecho do documento-fonte resume o trade-off: o squad AI-native é menor, mas precisa ser muito mais sofisticado.

Cada camada também nomeia o que ela entrega ao negócio: na Intent Layer nasce a direção; na Spec Layer, a previsibilidade; na Orchestration Layer, a alavancagem; na Verification Layer, a confiança; na Governance Layer, a escala corporativa. Quando um executivo pergunta "onde investir primeiro?", a resposta operacional é: na camada mais fraca do seu diagnóstico — porque o valor das camadas de cima é limitado pela camada que falta embaixo.

### [checkpoint]
-- **Exercício 3 — Matriz papéis × pessoas.** Distribua as seis capacidades novas entre os membros reais de um squad seu (uma pessoa pode acumular; capacidade pode ser parcialmente agentic). Identifique a capacidade descoberta e escreva em duas frases o custo de deixá-la vaga por mais um trimestre.
-- **Exercício 4 — Diagnóstico de camadas.** Avalie sua organização de 0 a 5 em cada uma das cinco camadas do operating model e defina a iniciativa única de maior alavancagem para a camada mais fraca — tipicamente Verification ou Governance. Justifique por que ela destrava as demais.

## Aula 6.3 — A nova cadência operacional: IA não matou Agile — matou o Agile performático
Meta: id=`cadencia-operacional-fim-do-agile-performatico` | duracao=`20 min` | icone=`calendar-clock`
Descrição: Do daily ao quarterly, a cadência agentic substitui rituais de status por inspeção de agent runs, Evidence Manifests e recalibração de regime — e o veredito final separa o que morre (sprint como teatro) do que sobrevive (empirismo, fluxo, feedback).

### [text]
A IA não eliminou a cadência operacional — eliminou os rituais performáticos. A cadência agentic opera em cinco ritmos: daily (bloqueios, aging, agent runs críticos), end-of-day (Nightly Agentic Verification e Evidence Manifest), weekly (tail review, validation debt, reforecast), monthly (guardrails e produtividade real) e quarterly (portfólio por outcomes e unit economics). Sobrevive o empirismo; morre o teatro.

O ponto de partida andragógico: você não precisa de mais reuniões — precisa que as reuniões existentes inspecionem coisas diferentes. A tabela abaixo, do documento-fonte, redefine cada ritmo:

| Ritmo | O que se inspeciona na cadência agentic |
|---|---|
| Daily | Bloqueios, aging de itens, agent runs críticos da noite anterior |
| End-of-day | Orquestrador roda testes impactados, suíte, E2E, security scan; gera Evidence Manifest e revisão adversarial |
| Weekly | Tail review (P85/P90), validation debt, reforecast, calibração de model routing |
| Monthly | Guardrails, near misses, produtividade real vs percebida, atualização da Definition of Verified |
| Quarterly | Portfólio por outcomes, tiny teams, unit economics, decisão build/buy/agentic arbitrage |

O daily deixa de ser status report — os agentes reportam status por telemetria — e vira triagem de risco. O end-of-day institucionaliza a prática do Módulo 4: a máquina valida à noite, o humano revisa evidências pela manhã. A decisão quarterly de build/buy ganha um insumo novo: o Gartner estima até US$ 234 bilhões em gastos corporativos com SaaS de aplicações empresariais expostos ao **agentic arbitrage** até 2030 — cada renovação de contrato agora compete com um agente executando o mesmo outcome.

O weekly merece atenção especial porque é onde o operating model se recalibra: o tail review de P85/P90 expõe os itens que envelhecem na cauda da distribuição, o estoque de validation debt diz se a verificação está acompanhando a geração, e a calibração de model routing corrige o mix de modelos antes que o custo derive. É a reunião que substitui a sprint review — inspeciona evidências e regime, não demos ensaiadas.

### [text]
A conclusão 20.1 do documento-fonte é o veredito do curso — e exige separar com precisão o que morre do que sobrevive:

| Morre (Agile performático) | Sobrevive (empirismo real) |
|---|---|
| Sprint como teatro de comprometimento | Inspeção e adaptação sobre evidências |
| Story point como contrato | Fluxo, WIP e lead time |
| Roadmap como ficção determinística | Forecast probabilístico por regime |
| Daily como status report | Daily como triagem de bloqueios e agent runs |
| Code review como gargalo cego de volume | Revisão de evidências, proporcional ao risco |
| "Done" sem evidência | Definition of Verified com Evidence Manifest |
| Retrospectiva ritualística | Retrospectiva sobre validation debt e near misses |

> "IA não matou Agile. Matou a falsa precisão." — Alexandre Caramaschi, documento-fonte

Note o que a coluna da direita preserva: empirismo, fluxo, feedback, WIP, lead time, retrospectiva, inspeção, adaptação. São os fundamentos que o Agile sempre reivindicou — agora operando em cima de agentes, com evidência no lugar de cerimônia. Quem lê essa tabela como "abandone o Scrum" errou o diagnóstico; quem lê como "pare de fingir precisão" acertou.

O ceticismo humano continua sendo insumo, não obstáculo: segundo o Stack Overflow Survey 2025, 46% dos desenvolvedores desconfiam ativamente da precisão de ferramentas de IA, contra 33% que confiam — e os mais experientes são os mais céticos. A cadência agentic canaliza essa desconfiança para os pontos de maior risco, em vez de dissolvê-la em rituais.

### [tip]
Implante a cadência por fatia, não por decreto — é um recorte que você pode aplicar sem pedir aprovação do board. Rode por duas semanas apenas o end-of-day (orquestrador de testes + Evidence Manifest + revisão matinal de 15 minutos) e o weekly (validation debt + reforecast). Meça o delta de retrabalho nessas duas semanas e use o número — não o argumento — para expandir aos demais ritmos.

### [text]
O fechamento amarra as sete conclusões do documento-fonte em um único sistema operacional:

-- **Validação é o novo gargalo estratégico** (20.3): o gargalo não é gerar código — é provar que funciona, não quebrou nada, respeita arquitetura, não cria vulnerabilidade, performa, é reversível e cumpre a intenção
-- **TDD como controle de agente** (20.2) e **Agent Evaluation Engineering** (20.4): o teste é contrato, o eval é o teste do agente
-- **O humano como auditor de intenção e risco** (20.5): revisa spec, evidências e blast radius — não linha a linha
-- **Model routing como vantagem competitiva** (20.6): o modelo certo, na etapa certa, com a permissão certa, pelo custo certo

A síntese da seção 21: o novo operating model = spec-first + TDD/evals + model routing + validation engineering + governança proporcional ao risco + forecast probabilístico. Cada termo dessa equação foi um módulo deste curso; a cadência desta aula é o que os faz girar juntos, semana após semana.

> "Na era dos agentes, não ganha quem gera mais código; ganha quem transforma intenção em resultado verificado, com menor custo, menor risco e maior velocidade de confiança." — Alexandre Caramaschi, documento-fonte, frase final

### [checkpoint]
-- **Exercício 5 — Piloto de cadência.** Implemente por 2 semanas apenas o end-of-day (orquestrador de testes + Evidence Manifest + revisão matinal de 15 min) e o weekly (validation debt + reforecast). Documente o delta de retrabalho e apresente o caso interno para expandir aos demais ritmos — com número, não com narrativa.
-- **Exercício 6 — Plano de 90 dias.** Consolide o curso em um roadmap de adoção com 3 marcos mensais — mês 1: Definition of Verified + checklist no PR; mês 2: model routing + autonomia L0-L5; mês 3: painel com 5 métricas + forecast em camadas. Defina o evidence gate de cada marco: qual prova precisa existir para declarar o marco cumprido.
