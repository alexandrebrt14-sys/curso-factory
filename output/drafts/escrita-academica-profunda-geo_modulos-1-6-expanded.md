# Escrita Acadêmica Profunda para Publicação em GEO e LLM Research

**Autor:** Alexandre Caramaschi — CEO da Brasil GEO, ex-CMO da Semantix (Nasdaq), cofundador da AI Brasil

**Escopo editorial:** curso avançado para pesquisadores aplicados (practitioners) que produzem pesquisa em Generative Engine Optimization, retrieval augmented generation e LLM research e querem publicar em SSRN, ArXiv (cs.IR), Zenodo, Semantic Scholar, workshops SIGIR/WWW e journals Q1 (Information Sciences, JASIST, IP&M).

---

# Módulo 1 — Fundamentos de escrita acadêmica: IMRAD, paradigmas de pesquisa e ciclo de vida do paper

## 1.1 Por que este módulo existe

O practitioner que decide publicar chega com três vícios previsíveis: confunde white paper com paper acadêmico, trata método como "o que eu fiz" em vez de justificar por que o fez, e apresenta resultados antes de declarar perguntas de pesquisa. Este módulo corrige os três vícios antes de tocar em qualquer canal de submissão.

A tese central do módulo é simples: **um paper acadêmico não é a sua opinião sobre GEO — é uma contribuição verificável que outro pesquisador consegue replicar, contestar ou estender com o material que você deixou no próprio paper.** Essa diferença de natureza guia todas as decisões editoriais seguintes.

Ao final do módulo, você será capaz de:

-- Analisar a estrutura IMRAD e suas variações aceitas em computer science e information retrieval
-- Comparar paradigmas de pesquisa (empirical, Design Science Research, Action Design Research, qualitative, systematic review) e justificar qual se aplica ao seu problema
-- Projetar o ciclo de vida do seu paper desde a ideação até a revisão pós-peer-review
-- Avaliar qual identificador persistente (ORCID, DOI, Handle, arXiv-id) cobre qual risco editorial

## 1.2 IMRAD e suas variações

IMRAD é a estrutura canônica para papers empíricos desde os anos 1970 e significa **Introduction, Methods, Results, Discussion**. A IMRAD não é obrigatória em todos os journals, mas é o default aceito em qualquer revisor sério, e desviar dela exige justificativa.

A estrutura IMRAD comparada ao que muitos practitioners entregam por intuição:

| Seção | Função acadêmica | Erro comum do practitioner |
|---|---|---|
| Introduction | Declarar o gap, posicionar a contribuição e listar as research questions | Virar um relato de jornada pessoal ou diagnóstico de mercado |
| Methods | Tornar o estudo replicável por outro pesquisador | Omitir seeds, prompts, versões de modelo, amostragem |
| Results | Reportar achados com estatística sem interpretar | Antecipar a discussão e misturar causa com correlação |
| Discussion | Interpretar resultados à luz das RQs e literatura | Repetir os resultados com adjetivos |

### Variações aceitas em CS/IR

A comunidade de information retrieval tolera variações razoáveis, especialmente em venues como SIGIR, ECIR e CIKM:

-- **Problema-Solução-Avaliação** em papers de sistema: substitui Methods+Results por uma seção de System Design seguida de Evaluation
-- **Related Work integrado** à Introduction quando o paper é curto (short papers de 4 páginas em SIGIR, por exemplo)
-- **Background antes de Methods** em papers que dependem de fundamentos técnicos não triviais (ex: tensores, grafos, embeddings)
-- **Ablation Study** como seção dedicada em papers de modelos — tornou-se de fato obrigatória em venues top-tier desde 2020

> **Regra prática:** se o seu paper é empírico, use IMRAD. Se é um paper de sistema ou framework, considere Design Science Research com a estrutura Awareness-Suggestion-Development-Evaluation-Conclusion (Vaishnavi e Kuechler 2004).

## 1.3 Paradigmas de pesquisa disponíveis para quem pesquisa GEO

Escolher o paradigma errado é o principal motivo de desk-rejection em papers de practitioner. Os cinco paradigmas abaixo cobrem mais de 95% do que você pode querer publicar sobre GEO e LLM research:

### Paradigma 1: Empirical research

Pesquisa empírica clássica: hipótese, experimento controlado, estatística inferencial. É o default em SIGIR, WWW e journals Q1 em information sciences. Exige N suficiente, baseline forte e testes de significância honestos. Para GEO, exemplos típicos:

-- Comparar taxa de citação em ChatGPT entre conteúdos com schema FAQPage vs sem schema
-- Medir efeito de structured markup sobre share-of-voice em Perplexity
-- Quantificar queda de inclusão em resposta generativa após robots.txt restritivo

### Paradigma 2: Design Science Research (Hevner 2004; Wieringa 2014)

Design Science Research (DSR) é o paradigma para practitioners que constroem artefatos — frameworks, métodos, modelos, instanciações — e demonstram utilidade em contexto real. Foi formalizado por Alan Hevner em **"Design Science in Information Systems Research"** (MIS Quarterly, 2004) e expandido por Roel Wieringa em **"Design Science Methodology for Information Systems and Software Engineering"** (Springer, 2014).

As sete guidelines de Hevner:

1. Design as an Artifact
2. Problem Relevance
3. Design Evaluation
4. Research Contributions
5. Research Rigor
6. Design as a Search Process
7. Communication of Research

### Paradigma 3: Action Design Research (Sein 2011)

Action Design Research (ADR), formalizado por Maung Sein e colegas em **"Action Design Research"** (MIS Quarterly, 2011), combina DSR com engajamento prático do pesquisador dentro da organização estudada. É o paradigma ideal para quem está publicando enquanto opera a empresa — situação típica do CEO-pesquisador.

### Paradigma 4: Qualitative research

Pesquisa qualitativa (entrevistas em profundidade, estudos de caso, grounded theory de Glaser e Strauss). Pouco usada em SIGIR mas aceita em Information Processing & Management e em workshops de human-centered IR.

### Paradigma 5: Systematic literature review

Revisão sistemática seguindo protocolo PRISMA (Page et al. 2021) ou Kitchenham (2007, **"Guidelines for performing Systematic Literature Reviews in Software Engineering"**). Excelente entrada para quem ainda não tem dados próprios e quer construir autoridade em GEO.

> **Recomendação para o portfólio Alexandre:** o primeiro paper SSRN 6460680 é um híbrido DSR+practitioner framework. O segundo pode ser empirical (medindo o próprio framework em amostra de sites). O terceiro pode ser systematic review cobrindo o estado-da-arte em GEO até 2026.

## 1.4 Ciclo de vida de um paper

O ciclo de vida abaixo se aplica a praticamente qualquer canal e serve como checklist antes de submeter:

**Fase 1 — Ideação e viabilidade:**
Você tem uma pergunta de pesquisa nova, um gap identificável na literatura e dados ou artefato para sustentar a resposta. Sem os três, pare. Ideias sem gap viram white paper, não paper.

**Fase 2 — Revisão de literatura:**
Antes de escrever uma linha, você mapeou o que já foi dito. Use Google Scholar, Semantic Scholar, ArXiv, ACL Anthology e dblp. Meta mínima: 30 referências relevantes para um paper de 15 páginas.

**Fase 3 — Design do estudo:**
Para empirical: hipóteses, variáveis, amostragem, métricas, análise estatística. Para DSR: requisitos do artefato, critérios de avaliação, ambiente de validação. Para systematic review: protocolo PRISMA com inclusão/exclusão.

**Fase 4 — Execução:**
Coleta de dados, construção do artefato, experimentos. Esta fase é o que a maioria dos practitioners faz bem. Também é a fase onde reproducibility nasce ou morre — se você não salvar seeds, prompts e versões agora, não tem como voltar depois.

**Fase 5 — Drafting:**
Escrever em ordem: Methods → Results → Introduction → Discussion → Related Work → Abstract → Conclusion. Escrever Introduction e Abstract por último é contraintuitivo mas reduz retrabalho em 40-60% porque eles precisam refletir o que o paper efetivamente entrega.

**Fase 6 — Submissão:**
Metadata completa, formatação do template do venue, cover letter quando aplicável, sugestão de revisores se o sistema permitir.

**Fase 7 — Peer review:**
Tempo médio de review: 2-4 semanas em workshops, 2-4 meses em conferências top, 6-12 meses em journals Q1.

**Fase 8 — Revisão pós-review:**
Responder ponto-a-ponto (response letter), revisar o manuscrito, resubmeter. Esta fase separa papers publicados de papers rejeitados — a qualidade da resposta ao revisor pesa tanto quanto o paper original.

## 1.5 Identificadores persistentes

Um paper sem identificadores persistentes é invisível para a economia de citações. Os quatro identificadores críticos:

-- **ORCID** (Open Researcher and Contributor ID): identificador único do autor. Grátis, 30 segundos para criar em orcid.org. Obrigatório em praticamente todo submission system desde 2019
-- **DOI** (Digital Object Identifier): identificador persistente do artefato. Atribuído pelo canal de publicação (SSRN, Zenodo, Crossref via journal). Formato: 10.xxxx/yyyy
-- **Handle**: identificador alternativo ao DOI, comum em repositórios institucionais
-- **arXiv-id**: identificador próprio do ArXiv, formato YYMM.NNNNN

## 1.6 Exercícios do Módulo 1

**Exercício 1 (Analisar):** pegue o paper SSRN 6460680 e classifique qual paradigma de pesquisa ele usa. Justifique com duas evidências textuais do próprio paper.

**Exercício 2 (Comparar):** escolha um paper publicado em SIGIR 2023 e um paper publicado em Information Sciences 2023, ambos sobre retrieval. Compare a estrutura IMRAD adotada e identifique desvios.

**Exercício 3 (Projetar):** para um dos três working papers em alexandrebrt14-sys/papers, desenhe o ciclo de vida completo (fases 1-8) com datas realistas considerando jornada de CEO com 20% do tempo disponível para pesquisa.

---

# Módulo 2 — Canais de publicação: SSRN, ArXiv (cs.IR), Zenodo, Semantic Scholar e journals Q1

## 2.1 Matriz de decisão de canal

A primeira pergunta não é "onde publicar" mas "qual risco editorial eu estou comprando". Cada canal troca velocidade por rigor, reach por autoridade, DOI rápido por indexação profunda. A matriz abaixo é o destilado operacional para practitioners em GEO:

| Canal | Tipo | DOI | APC | Tempo review | Rigor | Scope GEO |
|---|---|---|---|---|---|---|
| SSRN | Pre-print social sciences | Sim | Gratuito | Nenhum (pré-print) | Baixo | Excelente |
| ArXiv cs.IR | Pre-print STEM | Não (indexação via arXiv-id) | Gratuito | Moderação 1-3 dias | Baixo | Excelente |
| Zenodo | Open science | Sim | Gratuito | Nenhum | Baixo | Bom |
| Semantic Scholar | Indexador AI-powered | Derivado | Gratuito | Automático | Indexação | Excelente |
| SIGIR workshop | Workshop de conferência | Sim (via ACM) | USD 0-200 | 3-6 semanas | Médio-alto | Excelente |
| Information Sciences (Elsevier) | Journal Q1 | Sim | USD 3500 (OA opcional) | 6-12 meses | Muito alto | Bom |
| JASIST (Wiley) | Journal Q1 | Sim | USD 4500 (OA opcional) | 6-10 meses | Muito alto | Excelente |
| IP&M (Elsevier) | Journal Q1 | Sim | USD 3500 (OA opcional) | 5-9 meses | Muito alto | Excelente |

## 2.2 SSRN em profundidade

SSRN (Social Science Research Network) começou como pre-print de economia e direito e foi adquirido pela Elsevier em 2016. Para practitioners, é o canal ideal como primeira publicação porque:

-- Aprovação editorial em 2-5 dias úteis
-- DOI atribuído automaticamente no formato 10.2139/ssrn.XXXXXXX
-- Network de altmetrics próprio (Plum Print)
-- Indexação por Google Scholar, Semantic Scholar, RePEc
-- Nenhuma política de exclusividade — você pode submeter o mesmo paper depois para journal

### Pontos de atenção em SSRN

A política de revisão do SSRN é editorial, não peer-review. Isso significa que o paper aparece rápido mas **não carrega o selo de peer-reviewed**. Em currículo acadêmico, pre-print SSRN conta como working paper, não como publicação peer-reviewed.

Categorias relevantes para GEO no SSRN:
-- **Information Systems & eBusiness**
-- **Computer Science (Topic: Information Retrieval)**
-- **Marketing Research**
-- **Cognitive Social Science**

JEL codes recomendados para papers GEO com componente de marketing: **M31 (Marketing), M37 (Advertising), L86 (Information and Internet Services)**.

## 2.3 ArXiv e o track cs.IR

ArXiv é o pre-print server de STEM, hospedado pela Cornell University desde 1991. O track **cs.IR (Information Retrieval)** é onde pesquisa em GEO naturalmente se aloja. Também são relevantes para GEO:

-- **cs.CL** (Computation and Language)
-- **cs.AI** (Artificial Intelligence)
-- **cs.DL** (Digital Libraries)
-- **cs.HC** (Human-Computer Interaction)

### Requisitos de submissão no ArXiv

ArXiv tem moderação humana. Você precisa:

1. Criar conta com email institucional (.edu ou corporate). Gmail/Outlook pode exigir endosso de autor já publicado.
2. Submeter em LaTeX (preferido) ou PDF.
3. Aguardar moderação: 1-3 dias úteis, raramente mais.
4. Opcional: submeter ao mesmo tempo para um venue peer-reviewed.

ArXiv não atribui DOI, mas atribui arXiv-id único (ex: arXiv:2401.12345). Esse id é citável e permanente.

## 2.4 Zenodo: o coringa open science

Zenodo é hospedado pelo CERN e financiado pela União Europeia. Aceita qualquer artefato de pesquisa: papers, datasets, software, slides, pôsteres. Dá DOI grátis.

Casos de uso específicos para practitioners em GEO:

-- **Dataset** usado no seu paper SSRN (para que outros repliquem)
-- **Código** do framework 10-layer (Python package, notebooks)
-- **Slides** de apresentação em evento internacional
-- **Working paper** alternativo quando SSRN ou ArXiv não for aceito

## 2.5 Semantic Scholar: indexação e autoridade

Semantic Scholar é o indexador AI-powered do Allen Institute for AI. Extrai metadata via Crossref, constrói grafo de citações e calcula métricas como Influential Citations e Highly Influential Citations.

Para o practitioner:

1. Claim Authorship: ir em semanticscholar.org, buscar seu nome, clicar em "Claim Author Page", vincular ORCID. Isso consolida todos os seus papers em um perfil único.
2. Monitorar Highly Influential Citations: métrica que mede quantas citações efetivamente engajam com seu trabalho (não apenas mencionam).
3. Usar o Semantic Scholar API para construir dashboards próprios de impacto.

## 2.6 Journals Q1 em information sciences

Q1 significa primeiro quartil no Scimago Journal Rank (SJR) ou Journal Citation Reports (JCR). Para GEO, os journals Q1 mais relevantes em 2026:

### Information Sciences (Elsevier)
-- Impact factor 2024: ~8.1
-- Scope: information theory, data science, AI, IR
-- Tempo médio de primeira decisão: 8-12 semanas
-- APC (OA opcional): USD 3500

### JASIST — Journal of the Association for Information Science and Technology (Wiley)
-- Impact factor 2024: ~2.9 (mais baixo mas enorme prestígio no campo)
-- Scope: information science, scientometrics, IR, digital libraries
-- Excelente para papers híbridos com componente bibliométrica

### Information Processing & Management (Elsevier)
-- Impact factor 2024: ~7.4
-- Scope: IR, text mining, NLP, information systems
-- Aceita replication studies e systematic reviews, diferencial para practitioners

### SIGIR Proceedings (ACM)
-- Não é journal, é anais de conferência, mas conta como Q1 em CS
-- Acceptance rate 2024: ~18% (full papers), ~26% (short papers)
-- Tempo: submission em janeiro/fevereiro, decisão em abril/maio

## 2.7 Workshops de entrada

Para o practitioner sem histórico acadêmico, workshops são a porta de entrada certa. Tempo de review mais curto, taxa de aceitação mais alta, oportunidade de networking em conferência:

-- **SIGIR Workshops** — temas rotacionam por ano (LLM4IR, GenIR, BIRDS, etc.)
-- **ECIR** — European Conference on Information Retrieval
-- **CHIIR** — Conference on Human Information Interaction and Retrieval
-- **CIKM** — Conference on Information and Knowledge Management
-- **WSDM** — Web Search and Data Mining

## 2.8 Exercícios do Módulo 2

**Exercício 1 (Aplicar):** para o segundo working paper em alexandrebrt14-sys/papers, escolha três canais (um pre-print, um workshop, um journal Q1) e justifique o matching de scope, timing e APC.

**Exercício 2 (Avaliar):** compare o tempo total de visibility entre publicar primeiro em SSRN+ArXiv e depois submeter para IP&M, vs publicar direto em IP&M sem pre-print.

**Exercício 3 (Projetar):** desenhe um pipeline de 12 meses que gere 1 pre-print SSRN, 1 workshop paper SIGIR e 1 submissão a journal Q1, com marcos mensais verificáveis.

---

# Módulo 3 — Metodologia e rigor em pesquisa com LLM

## 3.1 O problema do rigor em LLM research

Pesquisa com LLM carrega três fontes de fragilidade metodológica que revisores de journals Q1 atacam primeiro: **não-determinismo**, **moving targets** e **N pequeno**. Quem não lida explicitamente com os três recebe desk-rejection.

Não-determinismo: mesmo com temperature zero, muitos modelos proprietários dão respostas ligeiramente diferentes entre runs. Moving targets: o modelo que você testou em janeiro pode se comportar diferente em março sem aviso. N pequeno: avaliar 30 prompts em três modelos não é estudo, é vinheta — o revisor vai rejeitar.

## 3.2 Reproducibility checklist

A checklist abaixo é baseada em Dodge et al. (2019) **"Show Your Work"** e Pineau et al. (2021) **"Improving Reproducibility in Machine Learning Research"** (NeurIPS), adaptada para pesquisa aplicada em GEO:

**Hardware e software:**
-- Versão exata do modelo (ex: gpt-4o-2024-08-06, não apenas "GPT-4o")
-- Versão da API client library
-- Hardware usado (se rodou local)
-- Sistema operacional, versão Python, seeds globais

**Dados:**
-- Fonte dos dados (URL, data de coleta)
-- Preprocessing aplicado (código disponível)
-- Split treino/validação/teste com seeds
-- Licença do dataset

**Experimento:**
-- Prompts completos (em appendix ou repo)
-- Temperature, top_p, max_tokens, frequency_penalty, presence_penalty
-- Seeds usados (quando o provider suporta — OpenAI suporta desde 2023)
-- Data e hora dos runs (para reconstruir contexto de versão de modelo)

**Código e dados:**
-- Repositório público (GitHub, GitLab)
-- Zenodo com DOI para versão congelada usada no paper
-- README com instruções de replicação

> **Regra de ouro:** se um revisor sério não consegue reproduzir seus resultados em 2 horas com o material do paper, o paper é rejeitado. Ponto.

## 3.3 Estatística para N pequeno

Practitioners subestimam estatística. Revisores não. Três conceitos mínimos:

### Effect size

Effect size mede magnitude do efeito, não apenas presença. As duas métricas mais usadas em LLM research:

-- **Cohen's d**: diferença padronizada entre duas médias. d=0.2 é pequeno, 0.5 médio, 0.8 grande (convenção de Cohen 1988)
-- **Hedges's g**: correção de Cohen's d para amostras pequenas (N < 20 por grupo)

### Intervalo de confiança (CI)

Reportar IC 95% é obrigatório em qualquer paper Q1 moderno. Se você reporta "precision 0.82" sem IC, o revisor assume que você não sabe o quanto confiar no número.

### Multiple-testing corrections

Se você testa 10 hipóteses com alpha=0.05, a chance de ter um falso positivo é 40%, não 5%. Corrija com:

-- **Bonferroni**: conservador, divide alpha pelo número de testes. Simples mas perde poder
-- **Holm-Bonferroni** (Holm 1979): menos conservador, ordena p-values
-- **FDR de Benjamini-Hochberg** (1995): controla taxa de falsas descobertas, não probabilidade familiar-wise. Default em IR research moderno

### Bayes factor (alternativa frequentista)

Bayes factor compara evidência a favor de H1 vs H0. Útil quando N é muito pequeno e você quer reportar força de evidência em vez de p-value. BF > 10 é considerado evidência forte.

## 3.4 Pre-registration

Pre-registration é declarar hipóteses, método e análise **antes** de coletar os dados, em registro público com timestamp. Combate HARKing (Hypothesizing After Results are Known) e p-hacking.

Registros aceitos pela comunidade:

-- **OSF Registries** (osf.io) — default em social sciences e crescente em CS
-- **AEA RCT Registry** — economics
-- **AsPredicted** — curto, 9 perguntas, usado em psicologia
-- **ClinicalTrials.gov** — obrigatório em ensaios clínicos, adaptável para IR com humans-in-the-loop

Para GEO, pre-registration agrega credibilidade gigante em papers que medem efeitos pequenos (share-of-voice generativo, taxa de citação).

## 3.5 Gestão de viés em LLM-as-a-judge

Avaliar output de LLM com outro LLM (LLM-as-a-judge) virou prática comum desde 2023 (Zheng et al. 2023 **"Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena"**). Mas carrega vieses conhecidos:

-- **Position bias**: LLM-juiz prefere a primeira resposta em comparações par-a-par
-- **Verbosity bias**: prefere respostas mais longas
-- **Self-enhancement bias**: modelo prefere output de modelos da mesma família
-- **Limited reasoning bias**: em tarefas matemáticas complexas, juiz erra sistematicamente

Mitigação obrigatória:

1. Randomizar ordem das respostas
2. Usar múltiplos juízes (ex: GPT-4o + Claude Sonnet + Gemini Pro)
3. Validar contra ground truth humano em subsample (mínimo 100 pares)
4. Reportar inter-rater agreement (Cohen's kappa ou Krippendorff's alpha)

## 3.6 Ablation studies

Ablation study responde "qual componente do meu sistema efetivamente importa". Removendo componentes um a um, você mede contribuição marginal. Em SIGIR desde 2020, ablation é de fato obrigatória para papers de sistema.

Para o framework 10-layer de Algorithmic Citability, uma ablation study mediria a contribuição marginal de cada camada na taxa de citação generativa — dado que o paper SSRN já postula o framework, a ablation seria um natural paper 2.

## 3.7 Threats to validity

Toda Discussion competente declara ameaças à validade em quatro categorias (Cook e Campbell 1979; Wohlin et al. 2012 **"Experimentation in Software Engineering"**):

-- **Internal validity**: seus resultados são explicados por algo diferente da sua manipulação?
-- **External validity**: seus resultados generalizam para outras populações, tempos, contextos?
-- **Construct validity**: suas métricas medem o que você acha que medem?
-- **Conclusion validity**: suas análises estatísticas são apropriadas?

## 3.8 Exercícios do Módulo 3

**Exercício 1 (Aplicar):** escreva a reproducibility checklist completa para um experimento GEO hipotético que compara taxa de citação em ChatGPT para conteúdos com e sem schema FAQPage, N=100 páginas.

**Exercício 2 (Analisar):** revise o paper SSRN 6460680 e identifique três threats to validity não declarados. Para cada um, proponha como mitigá-los em um paper follow-up.

**Exercício 3 (Criar):** projete um protocolo de pre-registration no OSF Registries para medir efeito de um novo método de estruturação de conteúdo sobre share-of-voice em Perplexity, com 2 grupos, N=60 por grupo, corrigido por FDR.

---

# Módulo 4 — Writing craft: abstract estruturado, related work tematizado e contribution statement

## 4.1 O abstract é o paper

Revisor de conferência top-tier lê 15-30 papers por ciclo. Editor de journal Q1 descarta 60% dos manuscritos submetidos só com abstract + introduction. Se seu abstract não vende o paper, ninguém lê o resto.

### Abstract estruturado Emerald/Q1

A convenção Emerald (Q1 em business e information) divide o abstract em seis campos:

1. **Purpose**: qual é o objetivo do estudo
2. **Design/methodology/approach**: qual paradigma e método
3. **Findings**: quais foram os resultados
4. **Research limitations/implications**: limitações e direções futuras
5. **Practical implications**: o que o practitioner faz com isso
6. **Originality/value**: por que isso é novo

SIGIR e ArXiv não exigem estrutura Emerald mas permitem. O abstract estruturado é sempre mais forte, principalmente em practitioner research onde o leitor quer saber rápido se aplica ao seu contexto.

### Regras de tamanho

-- Journals Q1: 150-300 palavras
-- SIGIR full paper: 150-200 palavras
-- SSRN: até 2000 caracteres, mas eficaz com 200-300 palavras
-- ArXiv: até 1920 caracteres

## 4.2 Hedging language

Hedging é a arte de fazer afirmações calibradas à evidência. Practitioners tendem a afirmação absoluta ("GEO aumenta leads em 40%"); revisores bloqueiam. Academicos Q1 usam hedging cirúrgico.

Hedging forte (afirmação robusta):
-- "Our results show that..."
-- "The evidence demonstrates..."
-- "This finding confirms..."

Hedging médio (afirmação calibrada):
-- "The data suggest that..."
-- "Results indicate a tendency for..."
-- "This pattern is consistent with..."

Hedging fraco (hipótese em aberto):
-- "It is possible that..."
-- "These findings may imply..."
-- "Further research is needed to confirm..."

> **Regra prática:** use hedging forte apenas quando você tem significância estatística robusta, tamanho de efeito grande e reproducibility validada. Em qualquer outro caso, hedging médio ou fraco.

## 4.3 Related Work tematizado vs cronológico

Related Work cronológico é o default do iniciante: "em 2019 X fez A. Em 2020 Y fez B. Em 2022 Z fez C." Isso é inútil para o revisor — ele quer ver tensões teóricas, não linha do tempo.

Related Work tematizado organiza a literatura por construto ou debate:

**Exemplo ruim (cronológico):**
> Brown et al. (2020) introduced GPT-3. Liu et al. (2021) demonstrated prompt engineering. Wei et al. (2022) proposed chain-of-thought.

**Exemplo bom (tematizado):**
> Três linhas de pesquisa dialogam sobre o problema de eliciação de comportamento em LLMs: escala de parâmetros (Brown et al. 2020; Hoffmann et al. 2022), design de prompt (Liu et al. 2021; Reynolds e McDonell 2021) e prompting estruturado como CoT e ToT (Wei et al. 2022; Yao et al. 2023). Nossa contribuição se posiciona na segunda linha, especificamente...

A segunda versão mostra ao revisor: você domina o campo, você entende tensões, você sabe onde sua contribuição se encaixa.

## 4.4 Contribution statement explícito

Toda Introduction Q1 termina com um bloco de Contribution Statement. Sem exceção. É o bloco que o revisor copia para a avaliação interna.

### Estrutura padrão

Depois de declarar gap e research questions, escreva:

> **Our contributions are:**
> -- **C1** (nome do construto): descrição em uma frase
> -- **C2** (nome do construto): descrição em uma frase
> -- **C3** (nome do construto): descrição em uma frase

Três contribuições é o ponto doce. Uma é insuficiente para paper longo; cinco é inflação e o revisor vai cortar.

### Exemplo aplicado a GEO

> **Our contributions are:**
> -- **C1** (Algorithmic Citability framework): we formalize a 10-layer model of content attributes that predict citation probability in generative engines
> -- **C2** (Empirical validation): we evaluate the framework on 240 URLs across 3 generative engines (ChatGPT, Perplexity, Gemini), demonstrating 0.71 AUC
> -- **C3** (Practitioner playbook): we release an open dataset and Python package implementing the Citability Scorer

## 4.5 Discussion que responde RQs

Discussion fraca: resume Results com adjetivos. Discussion forte: responde explicitamente cada research question declarada na Introduction, interpreta à luz da literatura e declara surprise findings.

### Estrutura Discussion Q1

1. **Answering the RQs**: para cada RQ, uma subseção respondendo diretamente
2. **Comparison with prior work**: como seus achados confirmam, estendem ou contradizem literatura
3. **Theoretical implications**: o que muda na teoria
4. **Practical implications**: o que o practitioner faz amanhã
5. **Limitations**: honestas, cobrindo internal/external/construct validity
6. **Future work**: três direções específicas, não genéricas

## 4.6 Limitations honestas

Limitations é a seção mais fácil de escrever bem e a mais comum de sabotar. Limitations mal feitas:

-- "Mais pesquisa é necessária" (vazio)
-- "Limitações de tempo e orçamento" (irrelevante)
-- "Apenas uma amostra" (sem explicar por que importa)

Limitations boas:

-- "Nossa amostra de 240 URLs é enviesada para domínios em inglês (88%), limitando generalização para conteúdo em português e espanhol"
-- "Medimos citation em snapshot de janeiro 2026; comportamento de modelos pode mudar com releases subsequentes, como já documentado por Chen et al. (2024)"
-- "Framework 10-layer foi validado em três generative engines proprietárias; modelos open-source como Llama e Mistral não foram testados e podem apresentar priors diferentes"

## 4.7 Expressões proibidas na redação Q1

Lista negra (todas geram reject-as-weak do revisor):

-- "In today's world..." / "Nos dias de hoje..."
-- "It is well known that..." / "É bem sabido que..."
-- "Revolutionary" / "Revolucionário"
-- "Paradigm shift" (usado sem justificativa)
-- "Cutting edge"
-- "State of the art" (exceto com citação comparativa)
-- "Significant" sem contexto estatístico (use apenas quando estatisticamente significante)
-- "Novel" sem especificar vs quê

## 4.8 Exercícios do Módulo 4

**Exercício 1 (Criar):** escreva o abstract estruturado Emerald completo (6 campos, 250 palavras) para o paper SSRN 6460680 existente, no estilo Q1.

**Exercício 2 (Aplicar):** pegue a Introdução atual do paper SSRN e reescreva o final com um Contribution Statement explícito de 3 contribuições (C1, C2, C3) seguindo o padrão do módulo.

**Exercício 3 (Avaliar):** escolha dois papers Q1 publicados em Information Sciences em 2024 e analise a qualidade das Limitations. Identifique duas limitations fracas e reescreva-as no padrão do módulo.

---

# Módulo 5 — Publicando e divulgando: metadata, cross-posting e altmetrics

## 5.1 Metadata por canal

Metadata é o que os indexadores leem para decidir em quais resultados você aparece. Metadata ruim mata paper bom. A matriz operacional:

| Canal | Campos críticos | Controlled vocabularies |
|---|---|---|
| SSRN | Keywords, JEL codes, classification | JEL Classification System |
| ArXiv | Primary category, cross-listings, MSC | arXiv taxonomy, MSC codes |
| Zenodo | Keywords, subjects, communities | Open keywords + DOAJ subjects |
| Semantic Scholar | Deriva de Crossref + fields of study | Computer Science taxonomy |
| Journal Q1 | Keywords controlled, ACM CCS | ACM CCS 2012, keywords do journal |

### JEL codes para GEO (SSRN)

JEL Classification System é mantido pela American Economic Association. Códigos relevantes:

-- **L86**: Information and Internet Services
-- **M31**: Marketing
-- **M37**: Advertising
-- **M15**: IT Management
-- **O33**: Technological Change: Choices and Consequences

### ACM CCS 2012 (ArXiv e journals CS)

ACM Computing Classification System tem três níveis hierárquicos. Para GEO, os caminhos mais relevantes:

-- **Information systems → Information retrieval → Retrieval models and ranking**
-- **Information systems → Information retrieval → Evaluation of retrieval results**
-- **Computing methodologies → Artificial intelligence → Natural language processing**
-- **Applied computing → Electronic commerce**

### Keywords que funcionam

Keywords são lidas por indexadores, leitores e motores de busca acadêmica. Regras:

-- 5-8 keywords por paper (mais é inflação, menos é subotimização)
-- Mix de termo amplo + termo específico: "information retrieval" + "generative engine optimization"
-- Inclua sinônimos conhecidos: "LLM", "large language model", "generative AI"
-- Evite keywords que aparecem no título (redundante)

## 5.2 Cross-posting sem violar exclusividade

A regra geral: **pre-prints são permitidos em praticamente todo journal Q1 moderno**, mas as políticas variam. Checklist antes de cross-postar:

1. Consultar Sherpa Romeo (sherpa.ac.uk/romeo) para política do journal alvo
2. Ler a submission guideline do journal específico (nem sempre reflete Sherpa)
3. Ler o copyright transfer agreement que você vai assinar se aceito

### Políticas típicas

-- **Elsevier journals**: permite pre-print em SSRN e ArXiv antes e durante submission; exige link para versão publicada depois
-- **Wiley journals**: permite pre-print; algumas revistas pedem que você remova o pre-print depois de publicação (cada vez mais raro)
-- **ACM**: permite pre-print em ArXiv (política oficial desde 2022)
-- **IEEE**: permite pre-print em ArXiv com label específico

### Estratégia recomendada para practitioners

1. Postar em SSRN imediatamente após ter draft final (dia 0)
2. Postar em ArXiv em paralelo ou 1-7 dias depois (dia 1-7)
3. Submeter para workshop SIGIR/ECIR simultaneamente (dia 7-30)
4. Se aceito em workshop, decidir se expande para journal Q1 (mês 3-6)
5. Se vai para journal, atualizar o SSRN/ArXiv com versão revisada e DOI do journal

## 5.3 Divulgação pós-publicação

Publicar não é o fim. Divulgação determina se o paper vira citado ou morre esquecido.

### LinkedIn com DOI completo

Post de divulgação no LinkedIn deve ter:

-- Título do paper entre aspas
-- Autor(es) com @mention quando possível
-- DOI completo (não apenas URL encurtada) — importante para altmetrics
-- Uma frase para cada: purpose, method, finding, implication
-- Call to action específico (ler, citar, contestar, replicar)
-- 3-5 hashtags temáticas

### Substack ou blog técnico

Artigo complementar que traduz o paper para practitioner. Diferente do paper, aqui você pode:

-- Usar linguagem mais direta
-- Incluir código rodado em real
-- Mostrar decisões editoriais que ficaram fora do paper
-- Convidar para webinar ou discussão

### Medium, Dev.to, Hashnode

Canais de alcance horizontal. Republicar com ajustes vs duplicação:

-- **Medium**: aceita versões lightly edited
-- **Dev.to**: exige canonical link para não afetar SEO
-- **Hashnode**: aceita canonical e repost direto

### ResearchGate e Academia.edu

Perfis acadêmicos com métricas próprias. ResearchGate tem um RG Score controverso mas gera visibility. Academia.edu oferece estatísticas de leitura detalhadas.

## 5.4 Altmetrics: medindo impacto além de citations

Citations demoram 18-36 meses para aparecer. Altmetrics capturam impacto em dias e semanas.

### Plum Print (SSRN)

Visualização de cinco dimensões: Usage, Captures, Mentions, Social Media, Citations. Aparece ao lado do paper no SSRN. Útil para ver velocidade de adoção inicial.

### Altmetric.com

Score único colorido (Altmetric Attention Score) baseado em menções em news, blogs, Twitter, Wikipedia, policy documents. DOI obrigatório.

### Impactstory / OurResearch

Agregador open-source que calcula métricas baseadas em DOI: Highly Cited (percentil via OpenAlex), Open Access, usage, etc.

### Google Scholar Citations

Perfil do autor no Google Scholar consolida citations cross-papers. Métricas:

-- **h-index**: número h tal que você tem h papers com h ou mais citations cada
-- **i10-index**: número de papers com 10+ citations
-- **Total citations**

### Crossref e OpenAlex

Crossref é o registry de DOIs. OpenAlex é um dataset aberto (sucessor do Microsoft Academic Graph) que consolida metadata e citations. Ambos são fontes primárias, Semantic Scholar e Google Scholar são derivadas.

## 5.5 Monitoramento contínuo

Montar dashboard simples para acompanhar o paper pós-publicação:

-- **Google Scholar alerts** com seu nome e título do paper
-- **Semantic Scholar API** puxando citations e influential citations semanalmente
-- **Altmetric Explorer** (pago, mas há versão free limited)
-- **Wikipedia citations** — checar se o paper foi citado em artigos Wikipedia (forte sinal de adoção pública)

## 5.6 Exercícios do Módulo 5

**Exercício 1 (Criar):** escreva metadata completa (keywords, JEL codes, ACM CCS) para o paper SSRN 6460680 alinhada ao que um journal Q1 exigiria se você resubmeter depois.

**Exercício 2 (Aplicar):** desenhe um plano de divulgação de 30 dias para o próximo working paper, cobrindo LinkedIn, Substack, Medium, ResearchGate e Twitter/X.

**Exercício 3 (Avaliar):** use Semantic Scholar para analisar três papers altamente citados em GEO/LLM research publicados em 2024. Identifique padrões comuns de metadata, keywords e canais de divulgação.

---

# Módulo 6 — Caso prático: paper SSRN 6460680 e roadmap dos próximos 3 papers

## 6.1 Decomposição do paper SSRN 6460680

O paper **"Algorithmic Authority: A Practitioner Framework for GEO"** (DOI 10.2139/ssrn.6460680), publicado em 2026 por Alexandre Caramaschi, é o primeiro artefato formal que mapeia o campo emergente de Generative Engine Optimization a partir de perspectiva de practitioner.

### Estrutura geral

O paper é um híbrido Design Science Research + practitioner framework. Contribui:

-- **C1**: formaliza um modelo de 10 camadas (10-layer) que descrevem atributos de conteúdo correlacionados com probabilidade de citação em motores generativos
-- **C2**: propõe o construto **Algorithmic Citability** como dimensão mensurável acima de atributos SEO tradicionais
-- **C3**: deriva o score composto **ECS (Engagement-Citation Score)** como métrica operacional

### Paradigma de pesquisa

DSR segundo as guidelines de Hevner (2004). O artefato é o framework; a avaliação acontece parcialmente no paper e é deixada como follow-up para pesquisa empírica.

### Canal escolhido: SSRN

Por três razões:

1. **Velocidade**: DOI em 3 dias úteis permite citar em produção (decks, LinkedIn, site) imediatamente
2. **Scope editorial**: SSRN aceita practitioner frameworks em Information Systems & eBusiness sem exigir peer-review prévia
3. **Reputação editorial Elsevier**: SSRN está na constelação Elsevier, o que dá trampolim para resubmissão em Information Sciences ou IP&M mais adiante

### Decisões editoriais analisadas

O paper fez cinco decisões conscientes alinhadas ao padrão Q1:

-- Abstract estruturado Emerald com 6 campos
-- Contribution Statement explícito ao final da Introduction
-- Related Work tematizado (SEO tradicional vs GEO vs IR) em vez de cronológico
-- Limitations honestas cobrindo external e construct validity
-- Referências canônicas ao lado de literatura prática (Hevner 2004, Sein 2011 co-citados com práticas de SEO)

### Lições aprendidas na primeira submissão

1. **Tempo de editorial decision em SSRN**: 2 dias úteis no caso específico. Canal justificado.
2. **Feedback editorial**: SSRN não oferece peer review; o feedback vem da comunidade depois, via altmetrics e downloads.
3. **Revisão pós-publicação**: SSRN permite versioning. Versões futuras devem sumarizar mudanças no campo Abstract Revision History.

## 6.2 Roadmap dos próximos 3 papers

O repositório **alexandrebrt14-sys/papers** mantém três working papers em preparação. O roadmap abaixo mapeia cada um ao canal, paradigma e cronograma realista considerando a jornada de CEO que aloca 20% do tempo em pesquisa.

### Paper 2 — Empirical validation do framework 10-layer

**Paradigma**: empirical research.
**Research Question**: em que grau cada uma das 10 camadas prediz probabilidade de citação em ChatGPT, Perplexity e Gemini?
**Método**: coleta de N=300 URLs estratificadas por domínio e vertical, scoring manual + automático das 10 camadas, medição de citation outcomes via API de busca em cada engine.
**Estatística**: regressão logística hierárquica, AUC por engine, ablation de layers.
**Canal primário**: workshop SIGIR (ex: LLM4IR, GenIR 2026).
**Canal secundário**: pre-print ArXiv cs.IR + Zenodo (dataset e código).
**Cronograma**: coleta Q2 2026, análise Q3 2026, submissão workshop Q4 2026, workshop em 2027.

### Paper 3 — Systematic review do campo GEO 2023-2026

**Paradigma**: systematic literature review (protocolo PRISMA 2020).
**Research Question**: qual é o estado da arte em GEO, quais construtos emergiram, e quais gaps de pesquisa estão abertos?
**Método**: busca sistemática em Semantic Scholar, Google Scholar, dblp, ACL Anthology com strings definidas, critérios de inclusão/exclusão pré-registrados, síntese qualitativa e thematic analysis.
**Canal primário**: JASIST (scope perfeito: information science + scientometrics).
**Canal secundário**: pre-print SSRN + Zenodo (supplementary material com extraction sheets).
**Cronograma**: protocolo Q2 2026, busca Q3 2026, extração e síntese Q4 2026, redação Q1 2027, submissão JASIST Q2 2027.

### Paper 4 — Measuring GEO in Portuguese: cross-lingual evidence

**Paradigma**: empirical research com componente comparativa cross-lingual.
**Research Question**: o framework 10-layer se generaliza para conteúdo em português, ou priors linguísticos dos modelos introduzem vieses sistemáticos?
**Método**: réplica do Paper 2 com N=150 URLs em português, comparação direta com subsample em inglês, análise de variance por camada e por língua.
**Canal primário**: Information Processing & Management (scope: IR + text mining + multilingual).
**Canal secundário**: pre-print ArXiv + workshop ECIR (European venue, receptivo a cross-lingual work).
**Cronograma**: coleta em paralelo ao Paper 2 (Q2-Q3 2026), análise dedicada Q1 2027, submissão IP&M Q2 2027.

## 6.3 Ética acadêmica para practitioners

O practitioner-pesquisador carrega conflitos de interesse específicos que revisores legítimos flagam. A transparência ética não é opcional — é condição de publicabilidade em Q1.

### Conflito de interesse

Toda submissão Q1 moderna exige Conflict of Interest Statement. Para o CEO-pesquisador:

-- Declarar vínculo com empresa cujos produtos ou serviços estão relacionados ao tópico
-- Declarar se dados usados vieram de clientes da empresa
-- Declarar se o paper pode beneficiar comercialmente a empresa
-- Separar claramente o que é achado científico do que é pitch comercial

### Disclosure de funding

Se a pesquisa foi financiada pela empresa (mesmo que indiretamente via tempo alocado), declarar. Ocultamento de funding é má conduta séria.

### Wikipedia WP:BIO vs Wikidata

Wikipedia tem política de notabilidade **WP:BIO** restritiva. Um CEO de uma startup em growth stage geralmente não atende WP:BIO — tentar criar artigo sobre si próprio (COI) é bloqueado e gera tag na conta. O caminho correto para CEO-pesquisador:

-- Não criar artigo próprio na Wikipedia
-- Esperar terceiro independente criar, quando/se os papers citados criarem notabilidade
-- Usar Wikidata em paralelo: Wikidata tem política mais permissiva (Wikidata:Notability) e aceita identidade de pesquisador com ORCID + DOI de publicações
-- Linkar Wikidata ao perfil Semantic Scholar e ORCID

### Conduct em peer-review

Quando você receber convite para revisar paper em sua área, a comunidade espera que aceite proporcionalmente ao que submete. Regra informal: revisar 3x mais papers do que submete por ano.

### Retraction Watch

Retraction Watch (retractionwatch.com) lista papers retratados. Familiaridade com casos conhecidos é cultura geral acadêmica que separa o practitioner amadurecido do que só quer publicar.

## 6.4 Conexão com o portfólio Brasil GEO

Os quatro papers formam um portfólio de pesquisa coerente e citável que sustenta credibilidade acadêmica do Alexandre e da Brasil GEO:

-- **Paper 1 (SSRN 6460680)**: framework conceitual. Referência teórica default.
-- **Paper 2 (workshop SIGIR)**: validação empírica. Prova que o framework funciona.
-- **Paper 3 (JASIST)**: systematic review. Posiciona Alexandre como voz que mapeou o campo.
-- **Paper 4 (IP&M)**: cross-lingual. Posiciona Brasil GEO como referência em GEO para mercados lusófonos.

Do ponto de vista de portfólio, quatro papers em três anos com uma publicação Q1 é patamar aceitável para transição de practitioner para practitioner-scholar.

## 6.5 Exercícios do Módulo 6

**Exercício 1 (Analisar):** leia o paper SSRN 6460680 completo e identifique três pontos em que um revisor Q1 cobraria rigor adicional. Para cada ponto, especifique que dado/análise adicional resolveria a cobrança.

**Exercício 2 (Projetar):** para o Paper 2 (empirical validation), escreva o protocolo completo de pre-registration no OSF Registries, incluindo hipóteses, variáveis, análise planejada e critérios de stopping.

**Exercício 3 (Criar):** redija o Contribution Statement explícito (3 contribuições nomeadas C1-C3) para cada um dos três próximos papers (2, 3 e 4) no padrão Q1 do Módulo 4.

**Exercício 4 (Avaliar):** analise criticamente a viabilidade de submeter o Paper 3 (systematic review JASIST) considerando: tempo disponível de 20% da semana, curva de aprendizado em PRISMA, e custo de APC se aceito em open access. Recomende ajuste ou alternativa realista.

---

## Referências canônicas citadas no curso

-- Benjamini, Y., & Hochberg, Y. (1995). Controlling the false discovery rate. *Journal of the Royal Statistical Society: Series B*, 57(1), 289-300.
-- Cohen, J. (1988). *Statistical Power Analysis for the Behavioral Sciences* (2nd ed.). Lawrence Erlbaum.
-- Cook, T. D., & Campbell, D. T. (1979). *Quasi-Experimentation: Design and Analysis for Field Settings*. Rand McNally.
-- Dodge, J., Gururangan, S., Card, D., Schwartz, R., & Smith, N. A. (2019). Show Your Work: Improved Reporting of Experimental Results. *EMNLP 2019*.
-- Glaser, B. G., & Strauss, A. L. (1967). *The Discovery of Grounded Theory*. Aldine.
-- Hevner, A. R., March, S. T., Park, J., & Ram, S. (2004). Design Science in Information Systems Research. *MIS Quarterly*, 28(1), 75-105.
-- Holm, S. (1979). A simple sequentially rejective multiple test procedure. *Scandinavian Journal of Statistics*, 6(2), 65-70.
-- Kitchenham, B. (2007). *Guidelines for Performing Systematic Literature Reviews in Software Engineering*. EBSE Technical Report.
-- Page, M. J., McKenzie, J. E., Bossuyt, P. M., et al. (2021). The PRISMA 2020 statement. *BMJ*, 372:n71.
-- Pineau, J., Vincent-Lamarre, P., Sinha, K., et al. (2021). Improving Reproducibility in Machine Learning Research. *Journal of Machine Learning Research*, 22(164).
-- Sein, M. K., Henfridsson, O., Purao, S., Rossi, M., & Lindgren, R. (2011). Action Design Research. *MIS Quarterly*, 35(1), 37-56.
-- Vaishnavi, V., & Kuechler, W. (2004). Design Research in Information Systems. AIS.
-- Wieringa, R. J. (2014). *Design Science Methodology for Information Systems and Software Engineering*. Springer.
-- Wohlin, C., Runeson, P., Höst, M., Ohlsson, M. C., Regnell, B., & Wesslén, A. (2012). *Experimentation in Software Engineering*. Springer.
-- Zheng, L., Chiang, W.-L., Sheng, Y., et al. (2023). Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena. *NeurIPS 2023 Datasets and Benchmarks*.
