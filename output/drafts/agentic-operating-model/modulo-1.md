# Módulo 1 — A Virada Agentic: da Assistência à Orquestração

## Aula 1.1 — A virada de 2026: por que a unidade de produção deixou de ser dev/hora e virou mudança verificada
Meta: id=`nova-unidade-de-producao` | duracao=`20 min` | icone=`workflow`
Descrição: A tese executiva da era agentic: o debate saiu de "IA acelera o dev" para como a organização redesenha seu sistema operacional para delegar, orquestrar, validar e governar trabalho feito por agentes.

### [text]
A unidade de produção de software deixou de ser dev/hora, story point ou sprint capacity porque agentes de IA assumiram parte relevante da execução. A nova unidade é a **mudança verificada**: intenção clara, spec verificável, roteamento de modelos, execução agentic, evidência de validação, governança proporcional ao risco e custo por mudança verificada. Segundo a Gartner, até 2027 mais de 65% dos times que usam agentic coding tratarão IDEs como opcionais — controle e validação migram para plataformas automatizadas.

No seu dia a dia, você provavelmente já sente o sintoma antes de nomear a causa. O relatório de sprint fecha com velocity estável, mas um único dev com agentes entrega em uma tarde o que o quadro estimou em duas semanas. As métricas que você reporta ao board descrevem esforço humano — e o esforço humano deixou de ser o fator limitante.

O segundo semestre de 2026 marca essa virada. O debate deixou de ser "IA ajuda o desenvolvedor a codar mais rápido" e passou a ser como uma organização redesenha seu sistema operacional para delegar, orquestrar, validar e governar trabalho feito por agentes. Não é uma troca de ferramenta; é uma troca de unidade de medida.

Os sete componentes da nova unidade de produção:

-- **Intenção clara**: o problema, o outcome e as restrições, definidos por humanos.
-- **Especificação verificável**: critérios de aceite que uma máquina ou um revisor consegue checar.
-- **Roteamento de modelos**: a tarefa certa no modelo certo, pelo custo certo.
-- **Execução agentic**: agentes implementam, humanos não digitam cada linha.
-- **Evidência de validação**: provas anexadas à entrega, não afirmações.
-- **Governança proporcional ao risco**: autonomia graduada conforme o blast radius.
-- **Custo por mudança verificada**: a conta que substitui o custo por dev.

> Na era agentic, velocidade sem prova é dívida.

Essa é a frase-tese do curso, extraída do documento-fonte. Cada módulo a seguir operacionaliza um pedaço dela.

### [text]
A mudança não é especulativa e tem duas fontes de peso. A Gartner descreve a transição de **`AI-assisted development`** para **agentic software development** ao longo de todo o SDLC, com controle, governança e validação migrando para plataformas automatizadas (Gartner). A McKinsey & Company chega à mesma conclusão por outro ângulo: as empresas que capturam mais valor com IA em software não estão apenas comprando ferramentas — estão rearquitetando o delivery inteiro e reposicionando humanos como orquestradores, validadores de arquitetura e gestores de qualidade (McKinsey & Company).

Compare o que suas métricas atuais medem com o que a nova gramática exige:

| Métrica da era Agile | O que ela mede de fato | Substituta na era agentic |
| --- | --- | --- |
| Dev/hora | Presença e esforço humano | Custo por mudança verificada |
| Story point | Estimativa de esforço humano | Risco de variação + custo de validação |
| Sprint capacity | Quanto o time produz por ciclo | Quanto o sistema humano + agentes verifica por ciclo |
| Velocity | Volume entregue | Trust Velocity: mudanças verificadas por tempo, custo e risco |

A leitura executiva da tabela é desconfortável: nenhuma métrica da coluna esquerda distingue **mudança verificada** de código gerado. Um agente pode inflar todas elas sem produzir uma única entrega com prova. É por isso que a coluna direita não é cosmética — ela muda o que o board enxerga.

Repare também no que o novo contexto adiciona à conversa que já existia. Scrum, Kanban, pontos, lead time, SDD e custo de tokens já estavam na mesa. A peça que faltava — e que este curso trata como espinha dorsal — é a **validação**.

### [tip]
Antes de redesenhar qualquer processo, faça o teste da tradução: pegue o último relatório que seu time enviou ao board e tente reescrever cada número como "mudanças verificadas". Se um número não sobrevive à tradução, ele mede esforço, não resultado. Esse exercício de 30 minutos costuma expor mais do que uma consultoria de três meses.

### [text]
Para diagnosticar sua organização, use três estágios de maturidade. No estágio **`AI-assisted`**, devs usam copilotos, mas o SDLC é o mesmo: PM escreve, dev implementa, QA testa. No estágio **agentic parcial**, agentes executam tarefas ponta a ponta em bolsões, sem governança formal nem evidência padronizada. No **Agentic Operating Model**, a organização opera as sete peças da nova unidade como sistema: specs verificáveis, roteamento, evidência e autonomia graduada.

A honestidade do diagnóstico importa mais que o rótulo. A maioria das empresas que se declara "agentic" está no estágio parcial: tem agentes rodando, mas ninguém responde quem escreve specs, quem valida e quem governa autonomia. Essas três perguntas são o teste de estágio.

> A pergunta que define seu estágio não é "quantos agentes você roda?" — é "quem prova que o que eles entregam funciona?".

O restante do módulo ataca exatamente essa pergunta: a Aula 1.2 apresenta a disciplina que monta o pacote de provas, e a Aula 1.3 mostra por que todos os grandes vendors estão convergindo para o mesmo desenho.

### [checkpoint]
Verifique, como profissional, sua capacidade de aplicar a tese a um cenário real do seu contexto:

-- **Exercício 1 — Auditoria da unidade de produção.** Liste as 3 métricas que seu time reporta hoje ao board (ex.: velocity, story points, deploys/semana) e reescreva cada uma na gramática da nova unidade de produção. Qual delas sobrevive como "mudança verificada" e qual é teatro?
-- **Exercício 2 — Diagnóstico de virada.** Classifique sua organização em um dos três estágios (`AI-assisted`, agentic parcial, Agentic Operating Model), justificando com evidências concretas do último trimestre — quem escreve specs, quem valida, quem governa autonomia.

## Aula 1.2 — Validation Engineering: a disciplina que responde "como saber se ficou melhor?"
Meta: id=`validation-engineering-disciplina` | duracao=`20 min` | icone=`layers`
Descrição: Não existe métrica objetiva universal que diga que o código "era nota 5 e virou 10" — o que existe é um pacote de evidências, e montar esse pacote virou disciplina estratégica.

### [text]
**Validation Engineering** é a disciplina que responde "como saber se ficou melhor?" sem depender de intuição: em vez de uma nota universal de qualidade, ela monta um pacote de evidências — testes automatizados, TDD, validação no browser, análise estática, load test, revisão de testes, spot check humano, evals, critérios de sucesso e observabilidade. É a disciplina estratégica do segundo semestre de 2026, porque separa "gerou código" de "entregou resultado verificável".

O motivo de existir dessa disciplina são sete perguntas que o mundo agentic colocou na mesa e que os ritos do Agile não respondem:

-- Como saber se ficou melhor?
-- Como validar sem revisar tudo?
-- Como usar TDD com agentes?
-- Como testar agente em produção?
-- Como medir drift e alucinação?
-- Como operar um orquestrador de raciocínio premium (Ultracode)?
-- Como separar "gerou código" de "entregou resultado verificável"?

Perguntas intuitivas como "ficou melhor?" ou "o agente terminou?" são operacionalmente fracas: qualquer resposta é uma afirmação sem prova. Em um regime onde o agente produz um diff gigantesco em 45 minutos, afirmação sem prova é exatamente o que não escala.

### [text]
O insight mais maduro do documento-fonte merece citação direta:

> "Não existe uma métrica objetiva universal que diga que o código era nota 5 e virou 10. O que existe é um pacote de evidências." — Alexandre Caramaschi, documento-fonte do curso

Duas evidências externas sustentam por que isso virou pauta de gestão, não de tooling. O relatório DORA 2025 nomeia o **verification tax**: parte do tempo economizado na escrita de código é reempregado auditando, revisando e validando output de IA (DORA, 2025). E o Stack Overflow Survey 2025 mostra que 46% dos desenvolvedores desconfiam ativamente da precisão de ferramentas de IA, contra 33% que confiam — e os mais experientes são os mais céticos (Stack Overflow, 2025).

A leitura combinada é direta: a geração ficou barata, a confiança ficou cara. Quem trata validação como etapa final de QA paga o verification tax de forma desorganizada. Quem trata validação como disciplina — com dono, instrumentos e rito — converte o mesmo custo em ativo de velocidade.

### [warning]
O anti-padrão mais caro da era agentic é aceitar "done" sem evidência. Ele troca a falsa confiança humana ("revisei por cima, parece bom") pela falsa confiança automatizada ("o agente disse que terminou e os testes dele passaram"). Se a sua definição de pronto não exige prova anexada, você não tem Validation Engineering — tem esperança com CI.

### [text]
O pacote de evidências tem dez componentes, e cada um prova uma coisa diferente. Confundi-los é a origem de a maioria das discussões improdutivas sobre "qualidade":

| Componente | O que ele prova |
| --- | --- |
| Testes automatizados | O comportamento esperado se mantém executável e checável |
| TDD | O critério de sucesso existia antes da implementação |
| Validação no browser | O fluxo real do usuário completa de ponta a ponta |
| Análise estática | Contratos, tipos e padrões são respeitados |
| Load test | O sistema performa sob carga, com análise estatística |
| Revisão de testes | Os testes fazem sentido — não confirmam a solução errada |
| Spot check humano | Julgamento contextual em pontos de maior risco |
| Evals para agentes | O agente se comporta como esperado, não só o código |
| Critérios de sucesso | A entrega é aderente à intenção declarada |
| Loops de validação + observabilidade | O comportamento em produção é medido, não presumido |

Montar e operar esse pacote é trabalho de engenharia — por isso o nome. A disciplina se materializa ao longo do curso: o **Quality Evidence Stack** detalha as camadas no Módulo 3, TDD e evals viram mecanismos de controle no Módulo 4, e a governança fecha o ciclo no Módulo 5. O papel formal de Validation Engineer aparece no Módulo 6.

A decisão executiva desta aula é uma só: Validation Engineering precisa de dono e de rito no seu time. Sem dono, o pacote de evidências vira checklist morto; sem rito, vira burocracia que o próximo deadline atropela.

### [checkpoint]
Aplicação prática da disciplina no seu pipeline atual:

-- **Exercício 3 — Inventário de evidências.** Pegue o último PR relevante gerado com IA no seu time e liste quais dos dez componentes do pacote de evidências existiam de fato. Atribua um score de completude (0 a 10) e identifique as duas lacunas de maior risco.
-- **Exercício 4 — Desenho de papel.** Escreva a job description de 1 parágrafo para a capacidade "Validation Engineer" no seu contexto — o que essa pessoa (ou agente) constrói, o que ela veta e a quem responde. O papel formal será detalhado no Módulo 6; aqui, o objetivo é confrontar o desenho com a sua estrutura real.

## Aula 1.3 — De chatbot a control plane: a convergência de Anthropic, OpenAI, Google, GitHub e Microsoft
Meta: id=`convergencia-vendors-control-plane` | duracao=`20 min` | icone=`scale`
Descrição: O movimento não é de um vendor: todos os grandes ecossistemas convergem para agentes que planejam, executam, revisam PRs e validam — e o stack empresarial se desloca de features para outcomes.

### [text]
Anthropic, OpenAI, Google, GitHub e Microsoft convergem para o mesmo padrão: agentes que planejam, executam, revisam PRs e validam trabalho, operados por humanos a partir de um **control plane** — não de um chat. A Gartner projeta que, até o fim de 2026, 40% das aplicações corporativas estarão integradas com agentes de IA task-specific, contra menos de 5% hoje. O futuro próximo não é um dev usando um chatbot; é um humano operando um plano de controle de agentes.

O movimento extrapola a engenharia de software. A integração de agentes task-specific desloca o stack empresarial para workflows dinâmicos e orquestração entre agentes (Gartner). Isso significa que a mesma virada que atinge seu time de produto atinge seus fornecedores — e seus contratos.

A ameaça econômica tem nome: **agentic arbitrage**. A Gartner estima que até US$ 234 bilhões em gastos corporativos com SaaS de aplicações empresariais ficarão expostos a esse fenômeno até 2030, porque agentes poderão executar tarefas end-to-end através de múltiplos sistemas, deslocando valor de features, telas e dashboards para **outcomes** (Gartner).

> Quando um agente atravessa três sistemas para executar o outcome, o valor deixa de estar nas telas desses sistemas — e passa a estar em quem orquestra e verifica a travessia.

### [text]
Em engenharia, a convergência dos cinco grandes ecossistemas é visível na direção estratégica de cada um:

| Ecossistema | Direção estratégica |
| --- | --- |
| Anthropic / Claude Code | Workflows dinâmicos, ultracode, subagentes, hooks, code review agentic |
| OpenAI / Codex | Delegação de tarefas como "coworker", integração com Slack, SDK, revisão automática de PRs |
| Google / Gemini CLI | Agente em GitHub Actions: triagem de issues, revisão de PRs, testes, correção de bugs, com least privilege e allowlisting de comandos |
| GitHub / Spec Kit | Especificação como artefato vivo e executável |
| Microsoft / SDD | Requisitos, planos, tarefas e validação integrados ao ciclo spec-first |

Três detalhes dessa tabela merecem atenção executiva. A Anthropic descreve **dynamic workflows** como a capacidade de o Claude escrever scripts de orquestração, rodar dezenas ou centenas de subagentes em paralelo e verificar o trabalho antes de consolidar resultados (Anthropic, documentação do Claude). A verificação antes da consolidação é o padrão que a Aula 1.2 nomeou como disciplina.

A OpenAI afirma que o Codex evoluiu para delegação de tarefas como um "coworker", com uso interno massivo e aumento de PRs por semana (OpenAI). O sinal relevante não é o volume — é que a própria vendor mede a si mesma em PRs delegados, não em sugestões aceitas no editor.

O Google posiciona o Gemini CLI em GitHub Actions como colaborador autônomo sob controles explícitos: **least privilege** e **allowlisting** de comandos (Google). Governança nasce embutida no produto, não como camada posterior — antecipação direta do Módulo 5.

### [tip]
Não tente adotar as cinco direções de uma vez. Escolha a capacidade mais próxima do seu gargalo atual — para a maioria dos times, é a revisão agentic de PRs — e implante com allowlisting desde o primeiro dia. Uma capacidade operando com governança ensina mais sobre o seu estágio de maturidade do que cinco pilotos sem controle.

### [text]
A conclusão da convergência fecha a tese do módulo:

> O futuro próximo não é um dev usando um chatbot. É um humano operando um control plane de agentes.

Para o executivo, isso gera duas agendas imediatas. A primeira é defensiva: revisar a carteira de SaaS sob a lente do agentic arbitrage, perguntando contrato a contrato se o outcome pode ser executado por um agente atravessando sistemas. A segunda é ofensiva: mapear quais capacidades de control plane — subagentes, hooks, revisão agentic de PRs, allowlisting — sua organização já opera e quais ainda dependem de processo manual.

Esse mapa de gaps é o insumo do Módulo 2, que desenha o novo SDLC: como a intenção vira plano, como o orquestrador decompõe o trabalho e como o roteamento de modelos vira disciplina econômica. A infraestrutura conceitual — nova unidade de produção, Validation Engineering e control plane — está posta.

### [checkpoint]
Transforme a convergência em decisão de portfólio:

-- **Exercício 5 — Mapa de exposição.** Para os 3 maiores contratos SaaS da sua empresa, avalie se há risco de agentic arbitrage (o outcome pode ser executado por um agente atravessando sistemas?) e classifique cada um em manter, renegociar ou substituir por agente. Justifique com o critério de valor: feature ou outcome?
-- **Exercício 6 — Gap de control plane.** Compare seu setup atual com a tabela de vendors — quais capacidades (subagentes, hooks, PR review agentic, allowlisting) você já opera e quais ainda dependem de processo manual? Priorize o fechamento de 1 gap para os próximos 30 dias.
