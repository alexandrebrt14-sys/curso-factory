# Checklist de Redação GEO 2026 — rubrica empírica para módulos de curso

> **Documento canônico operacional.** Rubrica derivada de **lifts de citação medidos** em papers de 2024-2026 (Aggarwal/Princeton KDD 2024, AutoGEO ICLR 2026, GEO-SFE/Berkeley 2025, AgenticGEO mar/2026) e estudos de mercado verificados até 03-jun-2026.
>
> **Versão:** 1.0 · 2026-06-03 · Owner: Brasil GEO (Alexandre Caramaschi)
>
> **Para que serve:** transformar a orientação genérica "cite fontes" em uma rubrica **com número-alvo por técnica e o lift empírico que justifica cada uma**. É a resposta direta à pergunta "como o conteúdo deve ser escrito para ter o maior ganho possível em Generative Engine Optimization".
>
> **Como usar:** este é o material que o prompt do redator (`src/templates/prompts/pt-br/draft.md`) carimba e que o `content_checker.py` valida por contagem. Complementa — não substitui — o padrão editorial HSM/HBR/MIT Sloan, os princípios de andragogia de Knowles e a barreira de acentuação PT-BR. Para a teoria por trás dos números, ver `GEO_KNOWLEDGE_BASE_2026_V3.md`; para os conceitos numerados, `GEO_50_CONCEITOS_CANONICAL.md`.

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

Abaixo do mínimo: **erro bloqueante** quando o playbook está habilitado; **aviso** quando desabilitado (default conservador para clientes não-GEO). A contagem ignora blocos de código e metadados.

---

## 2.1. Camada editorial humana: PT-BR, didática e decisão executiva

A rubrica GEO aumenta extração e citação por motores generativos, mas não substitui a qualidade do parágrafo para o leitor humano. Todo módulo deve manter a camada editorial abaixo:

| Critério | Regra de escrita | Por que importa |
|---|---|---|
| **PT-BR acentuado** | Todo texto de leitura humana em Português do Brasil com acentuação completa; preservar ASCII só em código, slugs, URLs, imports e variáveis. | Erro ortográfico quebra confiança e reprova no `accent_checker.py`. |
| **Utilidade por parágrafo** | Cada parágrafo entrega uma distinção, mecanismo, decisão, exemplo, risco ou próximo passo. | Parágrafos úteis viram melhores chunks para humanos e LLMs. |
| **WIIFM executivo** | O primeiro parágrafo explicita ROI do tempo de leitura: decisão, risco, ganho ou trade-off. | Decisor sênior abandona texto que não mostra valor rapidamente. |
| **Storytelling funcional** | Use microcaso, tensão de decisão ou cena profissional quando isso melhora compreensão. | História cria contexto sem substituir evidência. |
| **Metáfora inteligente** | Analogia deve reduzir carga cognitiva e voltar ao conceito técnico. | Metáfora decorativa aumenta ruído e reduz precisão. |
| **Autorreflexão executiva** | 2-3 perguntas por módulo, ligadas a governança, ROI, maturidade, risco ou alocação. | Ativa andragogia de Knowles sem tom professoral. |
| **Justificação** | React/Tailwind: `text-justify`; HTML/PDF/e-mail sem Tailwind: `<p align="justify">`. | Preserva a leitura longa e a regra visual do repo. |

Referências editoriais complementares ao padrão HSM/HBR/MIT Sloan: **IT Forum** para traduzir tecnologia em impacto operacional, ROI e governança; **Revista Exame** para decisão estratégica sob estresse corporativo; **MIT Sloan Management Review** para fluidez sintática, tom profissional quente e escolhas difíceis de liderança.

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
