# Módulo 3 — Validation Engineering na Prática: Evidência em Vez de Afirmação

## Aula 3.1 — 'Ficou melhor?' é a pergunta errada: peça evidências, não afirmações
Meta: id=`ficou-melhor-pergunta-errada` | duracao=`20 min` | icone=`scale`
Descrição: A pergunta operacionalmente correta é: que evidências mostram que o comportamento foi preservado ou melhorado, que o risco caiu e que o custo futuro de mudança diminuiu?

### [text]
Em entregas feitas por agentes de IA, a pergunta operacional não é "ficou melhor?", e sim: que evidências mostram que o comportamento esperado foi preservado ou melhorado, que o risco caiu e que o custo futuro de mudança diminuiu? Não existe nota universal de código — existe uma cesta de evidências. A regra da Anthropic para o Claude Code resume o novo standard: peça evidências, não afirmações; se não dá para verificar, não deveria ir para produção.

Se você já acompanhou uma entrega de agente no seu dia a dia, provavelmente já viveu essa cena: o refactor termina, alguém pergunta "ficou melhor?", e a resposta é um "sim" confiante — sem prova. A pergunta é intuitiva, mas operacionalmente fraca, porque convida a uma opinião em vez de exigir um fato verificável. Com um dev humano, a experiência do revisor compensava parte dessa fraqueza; com um agente que produz um diff gigantesco em minutos, ela vira um buraco de risco.

O problema estrutural é que "melhor" não tem métrica objetiva universal. Não existe instrumento que diga que o código "era nota 5 e virou 10". O que existe — e o que uma organização madura passa a exigir — é a **reformulação da pergunta** em três dimensões verificáveis:

-- **Comportamento**: que evidências mostram que o comportamento esperado foi preservado ou melhorado?
-- **Risco**: que evidências mostram que o risco caiu — segurança, regressão, blast radius?
-- **Custo futuro de mudança**: que evidências mostram que a estrutura ficou mais simples de evoluir?

> "Na era agentic, velocidade sem prova é dívida." — Alexandre Caramaschi

Essa é a tese que atravessa todo o curso, aplicada aqui à dimensão de qualidade. Um agente que entrega rápido sem evidência não está adiantando o trabalho: está transferindo o custo da verificação para o futuro, com juros.

### [text]
A documentação de boas práticas do Claude Code (Anthropic) formula a regra com precisão cirúrgica: **"peça evidências, não afirmações"**. Evidência pode ser saída de teste, comando executado, screenshot ou log — artefatos que qualquer revisor consegue inspecionar sem confiar na palavra de quem (ou do que) entregou. E a regra forte que completa o standard: se não dá para verificar, não deveria ir para produção.

A tradução prática dessa regra é um dicionário de conversão. Toda afirmação de entrega tem uma evidência correspondente que a converte em fato:

| Afirmação (fraca) | Evidência (verificável) |
|---|---|
| "Funciona" | Saída dos testes unitários e de integração passando |
| "Não quebrou nada" | Suíte de regressão executada, com resultado anexado |
| "Ficou mais rápido" | Load test com comparação estatística antes/depois |
| "A tela está correta" | Screenshot ou browser validation do fluxo completo |
| "O agente terminou" | Evidence Manifest: comandos, outputs e riscos residuais |

Esse movimento não é preciosismo de engenharia — é a direção do mercado. O Gartner projeta que, até 2027, mais de 65% dos times usando agentic coding tratarão IDEs como opcionais, com controle, governança e validação migrando para plataformas automatizadas (Gartner). O mesmo Gartner projeta que, até o fim de 2026, 40% das aplicações corporativas estarão integradas com agentes de IA task-specific, contra menos de 5% hoje (Gartner). A evidência precisa ser coletável por máquina, porque o volume de mudanças deixa de caber em revisão manual.

E a desconfiança humana justifica o rigor: no Stack Overflow Survey 2025, 46% dos desenvolvedores declararam desconfiar ativamente da precisão de ferramentas de IA, contra 33% que confiam — e os mais experientes são os mais céticos. A resposta organizacional correta a essa desconfiança não é frear a adoção: é institucionalizar a prova.

### [warning]
O anti-padrão mais caro da era agentic é aceitar o "done" declarado pelo próprio agente. Agentes afirmam conclusão com confiança máxima, inclusive quando a implementação está errada — e um "concluído" sem prova apenas troca falsa confiança humana por falsa confiança automatizada. Trate toda declaração de sucesso de um agente como hipótese a ser verificada, nunca como veredito. A exceção operacional (hotfix crítico com validação posterior) deve ser explícita, registrada e auditada — nunca o caminho padrão.

### [text]
Adotar "evidência, não afirmação" como política muda o vocabulário do time: "done" deixa de ser um estado declarado e vira um estado provado. A separação decisiva é entre **"gerou código"** e **"entregou resultado verificável"** — e o DORA 2025 dá nome ao custo dessa separação: o **verification tax**, a parte do tempo economizado na escrita de código que é reempregada auditando, revisando e validando output de IA (DORA, 2025).

A boa notícia: esse imposto não precisa ser pago de forma artesanal. As evidências se organizam em dez camadas complementares, cada uma respondendo a uma pergunta distinta:

-- Funcional, regressão, estática e arquitetural — o código faz o que deveria e continua saudável?
-- Segurança, performance, produto/UX e operacional — a mudança é segura, performa e chega ao usuário?
-- Agentic e humana — o agente se comporta como esperado, e onde entra o julgamento contextual?

Esse conjunto é o **Quality Evidence Stack**, detalhado na próxima aula. Antes de conhecer as camadas, fixe o princípio que as governa: nenhuma camada isolada prova qualidade; a prova é o conjunto.

### [checkpoint]
-- **Exercício 1 — Tribunal de evidências.** Selecione 3 entregas marcadas como "done" no último sprint do seu time e submeta cada uma à pergunta reformulada — comportamento preservado, risco reduzido, custo futuro menor. Para cada afirmação sem prova ("funciona", "não quebrou nada"), especifique qual evidência concreta a converteria em fato verificável.
-- **Exercício 2 — Política de aceite.** Redija a regra de 3 linhas que o seu time adotaria para recusar PRs sem evidência, incluindo as exceções legítimas (por exemplo, hotfix crítico com validação posterior obrigatória e registrada). Avalie se cada exceção se justifica pelo risco que ela aceita.

## Aula 3.2 — Quality Evidence Stack: as dez camadas de evidência de uma entrega agentic
Meta: id=`quality-evidence-stack-dez-camadas` | duracao=`20 min` | icone=`layers`
Descrição: Funcional, regressão, estática, arquitetural, segurança, performance, produto/UX, operacional, agentic e humana — cada camada responde a uma pergunta distinta e tem instrumentos próprios.

### [text]
O **Quality Evidence Stack** organiza a prova de uma entrega agentic em dez camadas — funcional, regressão, estática, arquitetural, segurança, performance, produto/UX, operacional, agentic e humana. Cada camada responde a uma pergunta distinta e usa instrumentos próprios, de unit tests a spot check por risco. Segundo o DORA 2025, a IA amplifica as forças e fraquezas organizacionais: um stack de evidências fraco vira risco amplificado; um stack forte vira confiança amplificada.

Por que dez camadas, e não uma suíte de testes robusta? Porque perguntas diferentes exigem instrumentos diferentes. Um teste unitário que passa não prova que a arquitetura ficou mais simples; um typecheck limpo não prova que o usuário completa o fluxo; um load test não detecta um secret vazado no diff.

O erro clássico do gestor pressionado é tratar "temos CI verde" como sinônimo de "temos evidência". CI verde tipicamente cobre três das dez camadas — funcional, regressão e estática — e deixa as sete restantes no escuro. O stack existe exatamente para tornar esse escuro visível e priorizável.

### [text]
A tabela completa do stack, com a pergunta que cada camada responde e os instrumentos que a provam:

| Camada de evidência | O que responde | Instrumentos |
|---|---|---|
| Funcional | A aplicação faz o que deveria fazer? | unit tests, integration tests, E2E, browser validation |
| Regressão | O que funcionava antes continua funcionando? | suíte existente, golden tests, testes impactados |
| Estática | O código respeita contratos e padrões? | typecheck, lint, format, static analysis |
| Arquitetural | A estrutura ficou mais simples ou mais coerente? | dependency graph, boundaries, ADR, coupling analysis |
| Segurança | Criamos vulnerabilidade ou exposição? | SAST, dependency scan, secrets scan, OWASP checks |
| Performance | O sistema continua performando sob carga? | load test, stress test, análise estatística |
| Produto/UX | O usuário consegue completar o fluxo? | browser run, journey test, acceptance criteria |
| Operacional | Está seguro para produção? | logs, metrics, rollback, canary, error budget |
| Agentic | O agente se comporta como esperado? | evals, prompt regression, tool-call assertions |
| Humana | Há julgamento contextual suficiente? | spot check por risco, revisão de testes, revisão arquitetural |

Leia a tabela como um instrumento de diagnóstico, não como um ideal distante. Nenhuma organização opera as dez camadas com maturidade uniforme — a questão executiva é saber quais camadas estão automatizadas, quais são manuais e quais simplesmente não existem no seu pipeline.

A priorização correta é por **blast radius**: a camada ausente cuja falha causaria o maior dano ao seu produto é a primeira a receber investimento. Em um sistema de billing, segurança e regressão vêm antes de arquitetural; em um produto de consumo, produto/UX e operacional sobem na fila.

### [text]
Duas camadas merecem atenção especial, porque são as que o SDLC tradicional não previa.

A camada **agentic** é a novidade estrutural do stack. Quando parte da sua produção é executada por agentes, o comportamento do próprio agente vira objeto de teste: evals, prompt regression e tool-call assertions respondem à pergunta "o agente se comporta como esperado?" — uma pergunta que não existia quando todo código era escrito por humanos. O Módulo 4 detalha esses instrumentos, incluindo a matriz de testes para agentes em produção.

A camada **humana** fecha o stack, e sua lógica muda de natureza: o humano não revisa volume, revisa risco. Spot check focado em arquivos críticos, revisão de testes e revisão arquitetural são formas de julgamento contextual que nenhuma automação substitui — mas aplicadas cirurgicamente, onde o blast radius justifica.

> "Não existe uma métrica objetiva universal que diga que o código era nota 5 e virou 10. O que existe é um pacote de evidências." — Alexandre Caramaschi

O DORA 2025 explica por que montar esse pacote é decisão estratégica, não higiene técnica: a IA é um amplificador das forças e fraquezas organizacionais, e o maior ROI não vem da ferramenta isolada, mas do sistema organizacional subjacente (DORA, 2025). Um time com stack de evidências forte amplifica confiança a cada entrega agentic; um time sem stack amplifica risco na mesma velocidade.

### [tip]
Comece pelo mínimo viável, não pelo stack completo. Automatize primeiro as camadas funcional, regressão e estática — elas têm o melhor custo-benefício e quase sempre já têm ferramenta instalada. Em seguida, ataque a camada ausente de maior blast radius no seu produto específico. Reserve a camada humana para o que ela faz de único: julgamento de risco, arquitetura e testes — nunca para reler diffs inteiros.

### [checkpoint]
-- **Exercício 3 — Heatmap do stack.** Monte a matriz das 10 camadas contra 3 estados (automatizado / manual / inexistente) para o seu pipeline atual. Identifique a camada cuja ausência tem o maior blast radius no seu produto e justifique a escolha com um cenário real de falha.
-- **Exercício 4 — MVP de evidência.** Para um microsserviço ou módulo específico do seu sistema, especifique o instrumento concreto de cada camada (nome da suíte, ferramenta de SAST, comando de load test) e estime o custo de implantação em dias. Priorize as três primeiras implantações pelo critério blast radius por dia de esforço.

## Aula 3.3 — Definition of Verified 2.0: o checklist executivo e o Evidence Manifest
Meta: id=`definition-of-verified-2-0` | duracao=`20 min` | icone=`workflow`
Descrição: Definition of Verified = Done + evidência automatizada + validação adversarial + revisão humana proporcional ao risco — operacionalizada em um checklist de 15 itens que culmina no Evidence Manifest anexado ao PR ou release.

### [text]
**Definition of Verified** é a camada acima da Definition of Done exigida quando agentes escrevem código: Done somado a evidência automatizada, validação adversarial e revisão humana proporcional ao risco. Sem esse pacote de provas — testes, scans, revisão de testes e Evidence Manifest anexado ao PR ou release — a entrega agentic não deveria ir para produção, em linha com o TEVV do NIST AI Risk Management Framework.

A Definition of Done continua necessária: critérios de aceite, código integrado, documentação. Mas em ambiente agentic ela não basta, porque foi desenhada para um mundo em que o autor do código era um humano cujo julgamento o time conhecia. Quando o autor é um agente probabilístico, "done" declarado precisa ser promovido a "verified" provado.

A fórmula é direta e cabe em uma linha de política de engenharia:

> Definition of Verified = Done + evidência automatizada + validação adversarial + revisão humana proporcional ao risco.

Cada termo da soma tem função própria. A **evidência automatizada** cobre o volume (as camadas do Quality Evidence Stack que rodam em pipeline). A **validação adversarial** coloca outro agente para tentar encontrar falhas — crítica ativa, não confirmação passiva. E a **revisão humana proporcional ao risco** aloca o recurso mais caro do sistema, o julgamento sênior, onde o blast radius justifica.

### [text]
Essa abordagem não é invenção isolada: o **NIST AI Risk Management Framework** enfatiza TEVV — test, evaluation, verification and validation — ao longo do ciclo de vida de sistemas de IA, com processos documentados, repetíveis e escaláveis para medir e acompanhar riscos emergentes (NIST AI RMF). Documentado, repetível e escalável é exatamente o que um checklist executivo entrega — e o que uma cultura de "confia no agente" não entrega.

O checklist da Definition of Verified 2.0 tem 15 itens, cada um com sua evidência mínima:

| # | Item | Evidência mínima |
|---|---|---|
| 1 | Spec vinculada | intenção, non-goals, restrições e critérios de aceite |
| 2 | Plano de validação | o que será provado e por quais testes/ferramentas |
| 3 | Teste vermelho quando aplicável | comportamento desejado falha antes da implementação |
| 4 | Red > Green > Refactor | ciclo documentado para mudanças determinísticas |
| 5 | Build limpo | CI sem falhas |
| 6 | Typecheck/lint | sem regressões relevantes |
| 7 | Testes unitários | menor unidade possível cobrindo comportamento |
| 8 | Testes de integração/E2E | fluxos críticos passando |
| 9 | Browser validation | aplicação aberta e fluxo validado quando aplicável |
| 10 | Load/performance test | análise estatística quando performance importa |
| 11 | Security/dependency scan | vulnerabilidades, secrets e dependências avaliadas |
| 12 | Revisão de testes | humano ou agente sênior avalia se os testes fazem sentido |
| 13 | Revisão adversarial | outro agente tenta encontrar falhas |
| 14 | Spot check humano | focado em arquivos críticos e alto blast radius |
| 15 | Rollback/canary | plano de reversão e implantação segura |

Note a arquitetura do checklist: os itens 1-2 ancoram a entrega na intenção (spec e plano); os itens 3-11 são evidência majoritariamente automatizável; os itens 12-14 são as três formas de revisão — de testes, adversarial e humana por risco; o item 15 garante reversibilidade. O item 12 merece destaque: teste gerado por agente é output, não garantia, e por isso os próprios testes entram na pauta de revisão — tema central do Módulo 4.

### [tip]
Não implante os 15 itens como gate bloqueante no primeiro dia. Rode o checklist como gate informal ao longo dos próximos 5 PRs relevantes, meça quantos itens passam hoje e use o resultado como baseline de Evidence Completeness — a métrica que o Módulo 6 leva ao painel de board. Gates que nascem bloqueando 100% das entregas morrem em uma semana; gates que nascem medindo sobrevivem e apertam gradualmente.

### [text]
O item que fecha o ciclo — e que transforma o checklist em ativo auditável — é o **Evidence Manifest**: um resumo anexado ao PR ou release com os comandos executados, os outputs obtidos e os riscos residuais. Testes que rodaram, testes que falharam, testes que foram pulados e por quê, onde houve spot check humano, o que ficou sem cobertura.

O manifest muda a economia da revisão. O revisor deixa de reconstruir mentalmente o que o agente fez e passa a auditar um dossiê estruturado — julgando riscos e deltas em minutos, em vez de reler diffs por horas. É a materialização, no nível do PR, do princípio de revisar por risco e não por volume.

> "A entrega não é o agente concluiu. A entrega é: o pacote de evidências sustenta que a mudança é correta, segura e aderente à intenção." — Alexandre Caramaschi

Há também um argumento de sobrevivência institucional. O Gartner projeta que, até 2027, 40% das empresas descomissionarão ou rebaixarão agentes autônomos por falhas de governança (Gartner) — e a Definition of Verified é precisamente a infraestrutura de governança que separa quem escala agentes de quem os desliga. Com o gate e o manifest operando, o time está pronto para a próxima camada do operating model: usar TDD e evals como mecanismos de controle do próprio agente, tema do Módulo 4.

### [checkpoint]
-- **Exercício 5 — Gate piloto.** Aplique o checklist de 15 itens ao próximo PR relevante do seu time como gate informal (sem bloquear merge) e meça quantos itens passam hoje. Use o resultado como baseline de Evidence Completeness e projete a meta trimestral — quais 3 itens sobem primeiro e com qual investimento.
-- **Exercício 6 — Template de Evidence Manifest.** Crie o template markdown do manifesto para o seu repositório — comandos executados, outputs, testes pulados e a justificativa, riscos residuais, onde houve spot check humano — e proponha o ponto exato do CI onde ele é gerado automaticamente. Avalie se o template atende ao critério TEVV do NIST: documentado, repetível, escalável.
