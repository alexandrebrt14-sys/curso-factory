# Checklist de Redação GEO 2026 — rubrica empírica para módulos de curso

> **Documento canônico operacional.** Rubrica derivada de **lifts de citação medidos** em papers de 2024-2026 (Aggarwal/Princeton KDD 2024, AutoGEO ICLR 2026, GEO-SFE/Berkeley 2025, AgenticGEO mar/2026) e estudos de mercado verificados até 03-jun-2026.
>
> **Revisão 2.0 (07/10/2026):** a seção logo abaixo do cabeçalho vence o restante. Nenhuma técnica desta rubrica promete citação em IA.
>
> **Versão:** 2.0 · 2026-10-07 (1.0 de 2026-06-03) · Owner: Brasil GEO (Alexandre Caramaschi)
>
> **Para que serve:** transformar a orientação genérica "cite fontes" em uma rubrica **com número-alvo por técnica e o lift empírico que justifica cada uma**. É a resposta direta à pergunta "como o conteúdo deve ser escrito para ter o maior ganho possível em Generative Engine Optimization".
>
> **Precedência (08/09/2026):** as regras de abertura e distração R1 a R9 (`DIRETRIZ_EDITORIAL.md`) vencem esta rubrica onde colidirem. Fonte inline discreta "(Autor, Ano)" continua valendo para Cite Sources; o que NÃO entra mais é fonte em card, callout ou linha "Fonte:" no meio do texto: a lista de fontes vive num único bloco pequeno no rodapé (R7). Citação de especialista, se entrar, entra como prosa com atribuição, nunca como card. A camada GEO é cobrada sobre o curso inteiro (trilha e rodapé), não por aula: nenhuma cota de fonte, estatística ou citação por aula, e os mínimos do curso vêm do bloco `geo_2026` do `client.yaml` (no cliente default, citação direta tem piso 0 desde 03/09/2026). Citação atribuída em prosa, sem travessão de atribuição (27/09/2026).
>
> **Como usar:** este é o material que o prompt do redator (`src/templates/prompts/pt-br/draft.md`) carimba e que o `content_checker.py` valida por contagem. Complementa, sem substituir, o registro de linguagem simples da fonte de estilo (HSM, HBR e MIT Sloan valem como rigor de evidência, não como registro), os princípios de andragogia de Knowles e a barreira de acentuação PT-BR. Para a teoria por trás dos números, ver `GEO_KNOWLEDGE_BASE_2026_V3.md`; para os conceitos numerados, `GEO_50_CONCEITOS_CANONICAL.md`.


---

## Revisão 2.0 (07/10/2026): o que mudou e o que esta rubrica deixou de afirmar

Esta seção vence o restante do documento onde colidirem. A versão 1.0 justificava cada técnica por um "lift de citação" medido em 2023-2024 e transformava as contagens em alvo. Três estudos do segundo semestre de 2026 tiram o chão dessa leitura, e o gate foi corrigido no mesmo commit desta revisão (`src/validators/content_checker.py > erros_de_geo`).

| Regra antiga (1.0) | Regra nova (2.0) | Fonte e data |
|---|---|---|
| Estatística, citação de especialista e fonte inline aumentam a citação (+32,8%, +42,6%, +40%) | Fonte atribuída e número com origem são **verificabilidade**: o leitor confere a afirmação. Nenhuma contagem promete citação. Estatísticas e falas viram **aviso**, nunca erro, e nunca alvo a cumprir | arXiv 2609.07559 (Bajemon e Rochet, 07/09/2026): as alavancas de 2023 não moveram citação em dez famílias de motores atuais; escore de página sem consultar o motor teve correlação de 0,11 com a citação dentro da consulta |
| Copiar o checklist de técnicas garante ganho | O ganho de cada heurística cai quando os concorrentes adotam a mesma tática; em categoria disputada, a tática da moda é a primeira a perder efeito | arXiv 2608.27631 (Sourirajan e outros, 27/08/2026) |
| Reescrever a página é a alavanca principal | Estar no conjunto que o motor recupera pesa mais que polir texto: cobrir as **variantes da pergunta** (o motor desdobra a consulta em buscas internas) e estar nas fontes de terceiros que o motor consulta | arXiv 2609.23162 (19/09/2026, observacional): menção de 2,8% (GPT) e 3,8% (Gemini) sem domínio nem marca na recuperação; 91,4% e 100% com domínio citado e marca nas buscas internas |
| Answer capsule rende 1,9× | A seção que abre pela resposta e se sustenta sozinha continua obrigatória, agora pelo motivo que se mantém: o motor recorta trechos soltos, e a condição precisa viajar na mesma frase | Doutrina editorial (COPY_PROMPT_PREFIX, item 27); o 1,9× saiu da mensagem do gate |
| FAQ e schema como alavanca de citação | FAQ e dados estruturados servem ao leitor e à busca clássica e descrevem só o que está visível. O `page.tsx` deixou de emitir `FAQPage` vazio e instrutor sem nome | Ahrefs (maio/2026), já no curso; orientação do Google de 01/10/2026 |
| Metadado gerado sai direto | Título, meta description, dados estruturados e texto alternativo gerados por IA passam por **checagem humana**; o `TsxGenerator.write` grava `REVISAO_HUMANA.md` com cada campo | Google Search Central, 01/10/2026 |
| Autoria livre | Byline, credencial ou selo de "revisado por especialista" sem pessoa real é proibido nos prompts de redação e revisão | Google, alerta de 06/10/2026 |
| Revisão trimestral | Curso publicado tem **próxima revisão** a cada 14 dias (`validation.revisao_publicacao.cadencia_revisao_dias`), com mudança editorial real | Profound (30/09/2026): meia-vida mediana da citação de 11 dias; 78% das páginas caem à metade em duas semanas |
| Medir citação numa rodada | Visibilidade em IA se mede em várias rodadas, por motor, em português no Google Brasil | arXiv 2609.22655 (19/09/2026): 84,9% dos pares de motores sem URL em comum; 67% das URLs trocaram no mesmo motor em um dia. arXiv 2609.24407 (21/09/2026): 3,4% de domínios em comum entre inglês e chinês |

O que continua igual: a rubrica de anti-invenção, a regra de não acrescentar número para parecer completo, o anti-padrão de keyword stuffing e a precedência das regras R1 a R9. As tabelas das seções 1 e 4 abaixo ficam como registro histórico da versão 1.0; a coluna de lift descreve o que os papers de 2023-2024 mediram, e não o que os motores de 2026 fazem.

---

## 0. Por que isto importa para um curso (e não só para um artigo)

Um módulo de curso bem escrito não compete só por aluno — compete por **citação em motores generativos**. Quando um profissional pergunta ao ChatGPT, Gemini, Claude ou Perplexity "como diagnosticar maturidade de dados?" ou "qual o melhor framework de GEO?", o motor responde citando as fontes que considera mais **extraíveis, verificáveis e autoritativas**. Um módulo que segue esta rubrica tem chance estruturalmente maior de ser essa fonte — e cada citação é um aluno potencial que descobre o portal pela resposta da IA, não pelo anúncio.

O lift não é uniforme: páginas que já estão em **posição 1 no Google** ganham pouco; páginas de **rank 5+** têm ganho máximo (até +115%). GEO é especialmente estratégico para conteúdo educacional novo, que ainda não domina o SEO tradicional — exatamente o caso de cada módulo recém-publicado.

---

## 1. As 13 técnicas ordenadas por lift de citação

Itens 1-12 ordenados pelo lift empírico individual; item 13 é a camada de mídia conquistada (earned media), tratada à parte em `GEO_EARNED_MEDIA_2026.md`.

| # | Técnica | Lift medido (fonte) | Como aplicar no módulo de curso |
|---|---|---|---|
| 1 | **Citação de especialista atribuída** | **+42,6%** (Aggarwal KDD 2024 — maior lift individual) | Pelo menos um blockquote (`>`) por módulo com **nome completo + cargo + organização**. Texto direto entre aspas, não parafraseado. Ex.: `> "A maioria das implementações de IA falha por desalinhamento organizacional, não técnico." — Thomas Davenport, professor do Babson College, em HBR (2025)`. |
| 2 | **Fontes inline em afirmações factuais** | **+40%** geral; **+115,1%** para páginas rank 5+ (Aggarwal) | Após cada afirmação verificável: (Autor/Instituição, Ano). Em seções técnicas, citar o estudo, relatório ou paper específico. Mínimo **3 fontes externas distintas** por módulo. |
| 3 | **Estatísticas com número específico** | **+32,8%** (Aggarwal); 15+ dados = +50% citações (Growth Memo 2026) | Toda afirmação quantificável vira número concreto com fonte: "73% das empresas (Gartner 2025)" em vez de "a maioria". Mínimo **5 estatísticas com fonte+ano** por módulo. |
| 4 | **Fluência e coerência (Single Idea)** | **+28,7%** (Aggarwal) | Voz ativa, sem redundância. Regra "Single Idea" (AutoGEO): **um conceito central por parágrafo**. Transição explícita entre seções. Cada H2/H3 cobre uma ideia nuclear. |
| 5 | **Termos técnicos precisos do domínio** | **+18,5%** (Aggarwal) | Usar a nomenclatura canônica do campo (não parafrasear jargão). Definir o termo na **primeira ocorrência** e mantê-lo coerente (não trocar por sinônimo "elegante"). Popular as `palavras_chave_seo` com os termos de arte. |
| 6 | **Seção autossuficiente (chunkability)** | **+17,3%** consistente em 6 engines (GEO-SFE/Berkeley 2025) | Cada seção deve ser citável **sem o contexto das outras**: heading + claim em negrito + evidência + conclusão. Sem pronomes ("ele/ela/isso") cruzando headings sem antecedente. Repetir a entidade-chave em vez de pronominalizar. |
| 7 | **Linguagem acessível com analogia** | **+13,8%** (Aggarwal) | No início de seção técnica, uma analogia ou exemplo concreto **antes** da formalização. É também o princípio andragógico de experiência prévia: conectar ao que o aluno já domina. |
| 8 | **Tom autoritativo (sem hedging)** | **+11,8%** (Aggarwal) | Afirmações declarativas ("a evidência indica" > "pode-se argumentar"). Eliminar hedging vazio ("talvez", "de certa forma", "em alguma medida") quando não houver incerteza real medida. |
| 9 | **Bloco resposta-primeiro (BLUF / answer capsule)** | **1,9×** baseline (GEO-SFE); 44,2% das citações vêm dos primeiros 30% da página (Zyppy 2025); 72,4% das páginas citadas pelo ChatGPT têm capsule (Search Engine Land 2026) | O **primeiro parágrafo de 40-60 palavras após cada H2** responde diretamente à pergunta implícita do heading, de forma autossuficiente. Sem links internos no capsule. É o trecho que a IA extrai literalmente. |
| 10 | **Tabela comparativa com dados** | **2,5×** vs texto plano; dados originais **4,1×** (GEO-SFE; Advanced Web Ranking 2026) | Pelo menos uma tabela markdown com header descritivo e **dados numéricos** por módulo. Converter prosa comparativa em tabela (já é obrigatório no padrão editorial — aqui ganha justificativa empírica de GEO). |
| 11 | **Unicidade / Information Gain** | **4,1×** para dado original sem equivalente indexado (Advanced Web Ranking 2026) | Um dado, framework próprio ou análise **não disponível em concorrentes**: um exemplo brasileiro inédito, um cálculo, um quadro de decisão autoral. Posicionar a tese contraintuitiva nos primeiros 100 palavras do módulo. **Target: ≥30% de conteúdo original por longform** (Conceito 51). |
| 12 | **Profundidade + frescor** | >2.000 palavras = 3× citações; <30 dias = 3,2× (ConvertMate/Perplexity 2026) | 2.500-4.000 palavras explicando o **mecanismo causal** (não enchimento — já é o piso editorial do módulo). Referenciar dado de 2025/2026. Atualizar a data só com **delta editorial real (≥15%)** — redating vazio é detectado como "fake-fresh" e penalizado. |
| 13 | **Enquadramento de tendência + earned media** | press releases citados **3,5×** mais em respostas de tendência; tendência cita jornalismo a **2×+** how-to (Muck Rack mai/2026) | Camada de PR/distribuição, fora do módulo em si. Ver `GEO_EARNED_MEDIA_2026.md`. Para o módulo: ancorar claims em fonte de terceiros autoritativa, não em afirmação própria. |

---

## 2. Os números-alvo (o que o `content_checker.py` mede)

A rubrica acima vira **gate automático**. Por módulo, com o `geo_2026.princeton_playbook_enabled: true` no `client.yaml`:

| Métrica | Mínimo | Detecção |
|---|---|---|
| **Cite Sources** (fontes externas atribuídas) | **≥ 3** | padrões "(Autor, Ano)", "Segundo X (ano)", "de acordo com", links externos |
| **Statistics** (dados quantitativos com contexto) | **≥ 5** | "NN%", "de X para Y", valores com unidade, "N×" |
| **Quotations** (citação direta atribuída) | **≥ 1** | blockquote com aspas + travessão de atribuição |
| **Answer capsule** (BLUF após heading) | **≥ 1** por módulo | parágrafo curto (40-60 palavras) imediatamente após um H2 |

Abaixo do mínimo, desde a revisão 2.0 (07/10/2026): fontes atribuídas e cápsula de resposta viram **erro bloqueante** quando o playbook está habilitado e **aviso** quando desabilitado; estatísticas e citações diretas são **sempre aviso**. A mensagem do gate não cita mais lift de citação. A contagem ignora blocos de código e metadados.

---

## 3. Anti-padrão eliminatório

- **Keyword stuffing → −8,7%** (Aggarwal — a única técnica com lift **negativo** comprovado). Variar o vocabulário semanticamente; no máximo ~2 ocorrências do termo principal por 500 palavras. O `content_checker.py` já penaliza a "variação elegante demais" (padrão 15 de cara de IA) — aqui o limite é o oposto: nem repetir demais (stuffing), nem trocar por sinônimo a ponto de quebrar a coerência terminológica (item 5).
- Mais os anti-padrões canônicos de `GEO_50_CONCEITOS_CANONICAL.md`: pseudo-GEO (prometer citação garantida), schema inflado (JSON-LD que não reflete o conteúdo visível), llms.txt-talismã, slugs com acento, "GEO substitui SEO", "schema = citação", redating vazio.

---

## 4. Variação por domínio do curso (Aggarwal GEO-bench)

O lift de cada técnica muda conforme a vertical do módulo:

| Domínio do módulo | Técnicas a priorizar |
|---|---|
| **Ciência / Tecnologia / Dados** | termos técnicos precisos (5) + fontes inline (2) + tabela com dados (10) |
| **Negócios / Estratégia / Gestão** | estatísticas (3) + citação de especialista (1) + information gain (11) |
| **Pessoas / Liderança / História de caso** | quotation (1) + analogia (7) |
| **Marketing / GEO / IA** (núcleo Brasil GEO) | mix dominante: itens **1, 2, 3, 6, 11** |

O classificador (`classify.md`) já identifica a categoria do curso — usar essa categoria para calibrar onde o redator concentra esforço.

---

## 5. Como esta rubrica se conecta ao pipeline de 5 LLMs

1. **Pesquisa (Perplexity)** → entrega o material com fontes verificáveis que alimentam os itens 1, 2, 3 (sem fonte na pesquisa, o redator marca `[FALTA EVIDÊNCIA]`, nunca inventa).
2. **Redação (GPT-4o)** → aplica os 12 itens; o prompt carimba esta rubrica com os números-alvo.
3. **Análise (Gemini)** → reporta lacunas (capsule ausente, claim sem fonte, seção não-autossuficiente).
4. **Classificação (Groq)** → emite as tags GEO canônicas (`geo-2026`, `citation-ready`, etc.) e a categoria que calibra a §4.
5. **Revisão (Claude)** → trata os `[FALTA EVIDÊNCIA]`, adiciona blockquote atribuído se faltar, garante os mínimos antes do gate.

> **Princípio operacional.** Estrutura validável vence prosa eloquente. Um módulo lindo sem fonte atribuída perde para um módulo correto e bem-estruturado com 5 estatísticas e 3 citações. A rubrica é a ponte entre o rigor editorial (que já temos) e a citabilidade por IA (o ganho novo).

---

*Fim do documento. Próxima revisão: trimestral (próxima agosto/2026) ou quando sair nova edição dos benchmarks Aggarwal/AutoGEO.*
