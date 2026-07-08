# Módulo 4 — Controle de Agentes: TDD, Revisão de Testes e Evals em Produção

## Aula 4.1 — TDD volta ao centro: Red > Green > Refactor como mecanismo de controle de agente
Meta: id=`tdd-mecanismo-de-controle-de-agente` | duracao=`20 min` | icone=`workflow`
Descrição: Antes, TDD era técnica de qualidade de código; com agentes, o teste vira contrato — o agente gera a implementação, mas não decide sozinho o que é sucesso.

### [text]
TDD ganhou uma segunda vida na era agentic: de técnica de qualidade de código, o ciclo Red > Green > Refactor virou mecanismo de controle de output probabilístico. O teste escrito antes da implementação funciona como contrato — o agente gera o código, mas não decide sozinho o que é sucesso. Segundo Martin Fowler, em 2026, o TDD tornou o desenvolvimento assistido por IA sustentável em vez de caótico, mantendo o humano no loop.

Você provavelmente já travou esse debate uma década atrás. **TDD** (Test-Driven Development) dividiu times entre entusiastas do design emergente e céticos do custo de manutenção de testes. O ciclo clássico, na formulação de Martin Fowler, é direto: escreva o teste para o comportamento desejado, escreva código até o teste passar, refatore com a segurança da suíte verde.

O argumento histórico a favor sempre foi de engenharia: o teste primeiro força clareza de interface e impede a bagunça incremental. O argumento contra sempre foi de economia: escrever teste antes custa tempo de dev sênior. Agentes de IA mudaram os dois lados dessa conta ao mesmo tempo.

> "O teste vira contrato. O agente pode gerar código, mas não decide sozinho o que é sucesso." — Alexandre Caramaschi

O que mudou de verdade:

-- O custo de escrever a implementação despencou — o agente gera o código em minutos, não em dias.
-- O custo de aceitar implementação errada explodiu — output probabilístico produz código plausível que compila, roda e faz a coisa errada com confiança.
-- O **teste vermelho** escrito antes da delegação passa a ser o único artefato que define sucesso independentemente do agente que executa.

Fowler observou exatamente esse deslocamento em 2026: em desenvolvimento assistido por IA, o TDD deixou o workflow sustentável em vez de caótico. A razão é andragógica antes de ser técnica — não dá para escrever um teste significativo sem entender o que está sendo construído. O teste é a prova de que houve intenção humana antes da geração.

### [text]
A pergunta prática do CTO não é "adotamos TDD?", e sim "quem é dono de cada etapa quando um agente entra no meio do ciclo?". O **pipeline recomendado** tem sete etapas, cada uma com dono explícito:

Spec → Teste vermelho → Implementação agentic → Teste verde → Refactor → Validação adversarial → Evidence Manifest

A tabela de donos por etapa resolve a ambiguidade que hoje trava a maioria dos times:

| Etapa | O que acontece | Dono |
|---|---|---|
| Intenção | Problema, restrições e não-objetivos definidos | PM / founder |
| Critérios de sucesso | O que é verificável e mensurável | PM + Tech Lead |
| Teste vermelho | Contrato escrito antes do código | Dev ou agente sob supervisão humana |
| Implementação | Código gerado até o teste passar | Agente executor |
| Refactor | Limpeza estrutural com suíte verde | Agente + humano |
| Verificação | Evidências coletadas e criticadas | CI + agente revisor + humano por risco |
| Aceite | Decisão de que a entrega vale | Produto / owner |

Repare no padrão: o humano concentra-se nas pontas — intenção, critérios, contrato e aceite — e a máquina ocupa o meio. O agente executor nunca é dono da etapa que define o que é sucesso nem da que decide se a entrega vale. Essa separação é o mecanismo de controle; o resto é ferramenta.

A etapa de **validação adversarial** merece atenção especial: um segundo agente (ou o orquestrador) critica a implementação contra a spec antes de qualquer humano gastar atenção. O Evidence Manifest, apresentado no Módulo 3, fecha o ciclo — o pipeline não termina quando o teste passa, termina quando a evidência está anexada.

### [tip]
Comece pelo contrato, não pela ferramenta. Na próxima tarefa que você delegar a um agente, escreva primeiro dois ou três testes vermelhos que capturam o comportamento esperado — inclusive um caso de borda — e só então entregue a spec ao agente. Se você não consegue escrever o teste, o problema não é o agente: é que a intenção ainda não está clara o suficiente para ser delegada.

### [text]
Por que isso mantém o humano no loop de forma estrutural, e não performática? Porque escrever um teste significativo exige compreender o domínio, a interface e o comportamento esperado. Um gestor pode pular a leitura do diff de 800 linhas; não pode pular a definição do que é sucesso sem abrir mão do controle.

Há também um efeito econômico direto, documentado pelo relatório DORA (2025) como **verification tax**: parte do tempo economizado na escrita de código é reempregado auditando, revisando e validando output de IA. O teste-contrato reduz esse imposto porque automatiza a primeira camada da auditoria — a suíte responde "o comportamento contratado existe?" antes de qualquer olho humano.

> Teste antes do código deixou de ser preferência metodológica. Em delivery agentic, é a diferença entre delegar e abdicar.

A conclusão operacional: TDD não voltou como moda de engenharia — voltou como instrumento de governança. O teste é o contrato operacionalizável entre a intenção humana e a execução probabilística. Times que tratam Red > Green > Refactor como burocracia estão, na prática, deixando o agente decidir sozinho o que é sucesso.

### [checkpoint]
-- **Exercício 1 — RACI do pipeline.** Preencha a tabela de donos das sete etapas (Spec, Teste vermelho, Implementação, Teste verde, Refactor, Validação adversarial, Evidence Manifest) para o seu time real, nomeando pessoas e agentes. Identifique a etapa órfã — tipicamente a validação adversarial — e proponha um dono com nome e rito.
-- **Exercício 2 — Contrato antes do código.** Escolha uma tarefa do backlog e escreva os testes vermelhos ANTES de delegar ao agente. Depois compare o diff entregue com o que você teria aceito sem o contrato — documente as diferenças e apresente ao time como evidência do valor do teste-contrato.

## Aula 4.2 — Teste gerado por agente é output, não garantia: os oito vícios e a pesquisa TDAD
Meta: id=`testes-gerados-por-ia-tdad` | duracao=`20 min` | icone=`layers`
Descrição: Teste ruim é anestesia corporativa: agentes escrevem testes que confirmam a implementação errada, mockam demais e reduzem tudo a happy path — a regressão precisa virar métrica de primeira classe.

### [text]
Teste gerado por agente é output, não garantia. Agentes escrevem testes que confirmam a implementação errada, mockam demais, ignoram edge cases e reduzem tudo a happy path — oito vícios catalogados que fabricam confiança sem fabricar segurança. A pesquisa TDAD (arXiv 2603.17973, 2026) mostra que agentes resolvem uma issue e quebram testes anteriores, e propõe regressão como métrica de primeira classe. A resposta operacional é um rito formal de **revisão de testes**.

A aula anterior estabeleceu o teste como contrato. Essa aula ataca a falha lógica que compromete esse contrato: se o mesmo agente que escreve o código escreve os testes, quem garante o contrato? A frase "o agente escreveu testes" descreve um artefato produzido, não uma verificação realizada.

Há dado externo sustentando a desconfiança. Segundo a Stack Overflow Survey 2025, 46% dos desenvolvedores desconfiam ativamente da precisão de ferramentas de IA, contra 33% que confiam — e os desenvolvedores mais experientes são os mais céticos. O ceticismo dos seniores não é resistência cultural: é reconhecimento de padrão.

> "Teste gerado por agente é output, não garantia." — Alexandre Caramaschi

### [warning]
Teste ruim é anestesia corporativa. Uma suíte com centenas de testes verdes gerados por IA pode passar integralmente com o comportamento errado em produção — e o dashboard verde desativa exatamente o instinto de auditoria que salvaria a entrega. O pior cenário não é o time sem testes; é o time que parou de olhar porque "os testes passam". Cobertura alta com testes viciados é passivo disfarçado de ativo.

### [text]
Os oito vícios catalogados dos testes gerados por agentes formam um checklist de auditoria direto:

| # | Vício | O que parece | O que esconde |
|---|---|---|---|
| 1 | Confirmar a implementação errada | Teste alinhado ao código | O teste foi escrito olhando o bug, e o valida |
| 2 | Mockar demais | Isolamento limpo | Nada real é exercitado; só o mock é testado |
| 3 | Testar detalhes irrelevantes | Cobertura alta | Estrutura interna testada, comportamento não |
| 4 | Ignorar edge cases | Suíte enxuta | Nulos, limites e concorrência sem cobertura |
| 5 | Passar com comportamento incorreto | Verde no CI | Assertions fracas ou tautológicas |
| 6 | Atualizar snapshots sem análise | Suíte "corrigida" | Regressão aceita como novo baseline |
| 7 | Reduzir tudo a happy path | Fluxo principal coberto | Erros, timeouts e falhas parciais ignorados |
| 8 | Criar falsa confiança | Métricas boas | Decisões de merge baseadas em teatro |

O vício 6 é o mais silencioso e o mais corrosivo. Atualizar um snapshot é um clique; analisar por que ele mudou exige contexto. Agentes otimizam para suíte verde — e a forma mais rápida de deixar a suíte verde é aceitar o novo comportamento como correto.

Os vícios 1 e 5 são os que quebram o contrato da aula anterior: se o teste foi escrito depois do código, olhando o código, ele valida o que foi feito — não o que deveria ter sido feito. É a inversão exata do Red > Green > Refactor.

### [text]
A pesquisa **TDAD** (Test-Driven Agentic Development, arXiv 2603.17973, 2026) deu forma empírica ao problema. Os autores mostram que benchmarks focados apenas em resolução de tarefa ignoram regressões: agentes resolvem a issue proposta e, no mesmo movimento, quebram testes anteriores. A tarefa fecha; o sistema piora.

Duas contribuições do estudo importam para quem lidera times de engenharia:

-- Regressão como **métrica de primeira classe** — medir só "resolveu a tarefa?" é medir metade do trabalho; a outra metade é "preservou o que funcionava?".
-- Redução relevante de regressões quando os agentes são guiados por **grafos de dependência** entre código e testes — o agente que enxerga o que sua mudança impacta quebra menos.

A resposta organizacional é um rito de revisão de testes com a postura certa. A analogia que calibra o rigor: revise o trabalho do agente como revisaria o de um júnior brilhante, rápido e perigosamente confiante. Você não descartaria o trabalho do júnior — mas também não faria merge sem ler as assertions, questionar os mocks e perguntar onde estão os casos de erro.

Esse rito não é overhead solto: ele já tem lugar reservado no operating model. A revisão de testes é item do checklist da Definition of Verified (Módulo 3), e Test Review Coverage e Regression Rate entram no painel de board do Módulo 6. O que essa aula acrescenta é o método — os oito vícios como pauta objetiva da revisão.

### [checkpoint]
-- **Exercício 3 — Caça aos vícios.** Audite 10 testes gerados por IA no seu repositório contra a lista dos oito vícios. Classifique cada teste e calcule a proporção de anestesia — testes que passariam mesmo com comportamento incorreto (vícios 1, 5 e 7). Apresente o número ao time como baseline de Test Review Coverage.
-- **Exercício 4 — Política de snapshot.** Escreva a regra do time para atualização de snapshots por agentes — quando é permitida, quem revisa, qual evidência acompanha o commit. É o vício mais silencioso da lista; a política de três linhas elimina a maior parte do risco.
-- **Exercício 5 — Regressão como métrica.** Usando a lógica da TDAD, defina como seu CI passaria a reportar "issues resolvidas × testes anteriores quebrados" por PR de agente — e qual threshold bloqueia o merge.

## Aula 4.3 — Evals de agentes em produção e Nightly Agentic Verification: o code review que revisa evidências
Meta: id=`evals-producao-nightly-agentic-verification` | duracao=`20 min` | icone=`scale`
Descrição: Testar um agente em produção é outro universo — golden prompts, policy tests, drift tests, telemetria — e a validação estruturada roda à noite, entregando pela manhã um Evidence Manifest para revisão humana por risco.

### [text]
Testar um agente em produção exige uma matriz própria: golden prompts, regression prompts, prompts adversariais, tool-call assertions, policy tests, memory tests, drift tests, hidden evals, mutation tests, human preference review e telemetria — onze tipos que unit tests não cobrem. A **Nightly Agentic Verification** operacionaliza a disciplina: o orquestrador roda a validação estruturada à noite e entrega pela manhã um Evidence Manifest para revisão humana por risco.

A distinção decisiva vem antes da ferramenta. Testar uma função determinística é verificar que a mesma entrada produz a mesma saída — unit, integration, E2E, typecheck, load. Testar um agente que recebe prompts, usa ferramentas, consulta memória e toma ações é outro universo: a mesma entrada pode produzir saídas diferentes, e a falha pode estar na ação tomada, não no texto retornado.

E o problema deixou de ser nicho. Segundo o Gartner, até o fim de 2026, 40% das aplicações corporativas estarão integradas com agentes de IA task-specific, contra menos de 5% no início do período — cada uma dessas integrações é um agente em produção que alguém precisa validar continuamente. A matriz dos onze tipos de teste para agente em produção:

| Tipo de teste | O que verifica |
|---|---|
| Golden prompts | Casos canônicos continuam produzindo a resposta esperada |
| Regression prompts | Mudança de modelo/prompt não degradou casos já resolvidos |
| Adversarial prompts | Resistência a prompt injection e instruções maliciosas |
| Tool-call assertions | O agente chama as ferramentas certas, com os argumentos certos |
| Policy tests | Regras de negócio e limites de conduta são respeitados |
| Memory tests | A memória não contamina nem vaza contexto entre sessões |
| Drift tests | O comportamento não se degrada silenciosamente ao longo do tempo |
| Hidden evals | Avaliações que o agente não conhece e não pode otimizar |
| Mutation tests | Pequenas variações de entrada não invertem a decisão |
| Human preference review | Amostras julgadas por humanos contra critérios de qualidade |
| Telemetria em produção | O comportamento real, medido onde importa |

### [text]
Por que essa matriz precisa existir como controle formal, e não como boa vontade do time? Porque os riscos são específicos e catalogados. O OWASP LLM Top 10 lista prompt injection, insecure output handling, model denial of service, insecure plugin design, excessive agency e overreliance; o OWASP Gen AI Security Project (Agentic AI Threats) trata agentes como categoria com riscos próprios — autonomia, uso de ferramentas, memória, subagentes e tomada de decisão.

Nenhum unit test detecta excessive agency. Nenhuma suíte de integração pega um drift de comportamento após troca de modelo. Para agentes, teste não é só unit test — é eval, política, telemetria e controle de agência. Desse conjunto nasce um campo de prática próprio: **Agent Evaluation Engineering**.

O custo de ignorar isso já tem número (Gartner, previsão para 2027): 40% das empresas descomissionarão ou rebaixarão agentes autônomos por falhas de governança. Evals em produção são a linha de defesa que separa o agente auditável do agente que será desligado.

A **Nightly Agentic Verification** transforma a matriz em rotina. No fim do dia, o orquestrador de testes roda o ciclo completo:

-- Testes impactados pelo diff do dia e suíte mínima de regressão.
-- Integração, E2E e validação no browser.
-- Load test, análise estática e security scan.
-- Revisão adversarial por agente e comparação do resultado com as specs.
-- Geração do **Evidence Manifest** consolidado — comandos, outputs, falhas e riscos residuais.

Na manhã seguinte, o humano não revisa tudo: revisa evidências, falhas, deltas críticos, testes novos, arquivos de alto risco e recomendações. Revisão por risco, não por volume — o princípio do Módulo 2 aplicado à rotina diária. É a mesma direção que o Gartner projeta para 2027: mais de 65% dos times usando agentic coding com controle, governança e validação migrando para plataformas automatizadas.

A base determinística disso existe hoje: os hooks do Claude Code, na documentação da Anthropic, executam comandos de shell automaticamente quando o agente edita arquivos, completa tarefas ou precisa de input — controle determinístico em vez de comportamento probabilístico. E o critério do que entra no manifesto segue a regra das boas práticas do Claude Code: "peça evidências, não afirmações" — evidência pode ser saída de teste, comando, screenshot ou log.

> "O futuro do code review não é revisar mais linhas. É revisar melhores evidências." — Alexandre Caramaschi

### [warning]
O erro mais comum ao montar evals é publicar todos os critérios para o próprio agente — que passa a otimizar para o eval em vez de para o comportamento correto. Mantenha hidden evals fora do contexto do agente e trate overreliance (OWASP) como risco do lado humano: a revisão matinal que vira carimbo automático depois de duas semanas de manifests verdes é o mesmo vício da anestesia de testes, um nível acima.

### [tip]
Não comece pelos onze tipos: comece com cinco golden prompts, três adversarial prompts e dois policy tests para um único agente em produção, com threshold explícito de aprovação. Agende a primeira Nightly Agentic Verification só com o que seu CI já roda hoje — testes impactados, lint e security scan — e acrescente uma camada por semana. A pauta matinal cabe em 15 minutos se o manifesto for bem estruturado.

### [checkpoint]
-- **Exercício 6 — Suíte mínima de evals.** Para um agente em produção (ou planejado) da sua empresa, escreva 5 golden prompts, 3 adversarial prompts — incluindo ao menos um de prompt injection — e 2 policy tests. Defina o threshold de aprovação e o que acontece quando ele é violado (bloqueio, alerta, rollback).
-- **Exercício 7 — Desenho do nightly.** Especifique o pipeline de Nightly Agentic Verification do seu repositório principal — o que roda, em que ordem, o que entra no Evidence Manifest — e redija a pauta de 15 minutos da revisão matinal, separando o que o humano lê sempre do que só lê quando falha.
-- **Exercício 8 — Mapa de risco OWASP.** Cruze os agentes do seu ambiente com os riscos do OWASP LLM Top 10 e do Agentic AI Threats — para cada par agente × risco relevante, aponte qual dos onze tipos de teste o cobre hoje e onde não há cobertura alguma.
