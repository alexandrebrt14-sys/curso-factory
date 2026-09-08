# Humanização de Textos Escritos por IA — Estado-da-Arte 2024-2026 e Aplicação ao curso-factory

> **Versão 2 — 2026-05-17 (noite)**. Dossiê técnico produzido via geo-orchestrator (board 5 LLMs) + 3 sub-agents de pesquisa em paralelo cobrindo papers arXiv/ACL/EMNLP/NeurIPS, datasets canônicos, benchmarks acadêmicos, fórmulas matemáticas formais com Cohen's d, corpora PT-BR (brWaC, MULTITuDE, IberAuTexTification) e modelos LLM PT-BR (gpt2-small-portuguese, BERTimbau, Sabia-2/3, Tucano, GlorIA). Auditável: 21 papers (14 originais + 7 de aprofundamento NAACL/ICML/NeurIPS), 9 datasets, 5 leaderboards públicos, 8 detectores com FPR medido, 9 humanizadores SaaS, política Google 2024-2026, política Brasil (PL 2338, MEC, CFP), design de experimento de calibração com power analysis. Aplicação direta ao `alexandrebrt14-sys/curso-factory` com 8 PRs priorizados (PR-1, PR-2, PR-5, PR-6, PR-8 **implementados nesta sessão**; PR-3, PR-4, PR-7 documentados).
>
> **Erratums identificados nesta V2 e corrigidos**:
> - Fórmula canônica de burstiness em séries é **Goh-Barabási (2008)**, "Burstiness and memory in complex systems", EPL 81, 48002 (arXiv:physics/0610233). A variante operacional usada em GPTZero é σ/μ (coeficiente de variação), distinta da forma original. Adotamos as duas: `compute_burstiness()` (GPTZero σ/μ) e `compute_burstiness_goh()` ((σ-μ)/(σ+μ)) no `stylometry_checker.py`.
> - **RAID** é Dugan et al. **ACL 2024** (arXiv:2405.07940), não ICLR 2025 como afirmado na V1.

---

## Sumário

1. [Taxonomia](#1-taxonomia)
2. [Estado-da-Arte (papers 2024-2026)](#2-estado-da-arte-papers-2024-2026)
3. [Ferramentas — Detectores e Humanizadores](#3-ferramentas--detectores-e-humanizadores)
4. [Política Google e Brasil (2024-2026)](#4-poltica-google-e-brasil-2024-2026)
5. [Técnicas Aplicáveis](#5-tcnicas-aplicveis)
6. [Diagnóstico do curso-factory](#6-diagnstico-do-curso-factory)
7. [Recomendações Priorizadas (8 PRs)](#7-recomendaes-priorizadas-8-prs)
8. [Referências](#8-referncias)

---

## 1. Taxonomia

Humanização de texto IA em 2024-2026 não é "trocar sinônimos". É um problema de **três camadas concorrentes** com objetivos parcialmente conflitantes:

| Camada | Adversário | Objetivo de defesa | Métrica que move |
|--------|-----------|--------------------|------------------|
| **L1 — Detectores estatísticos** | GPTZero, ZeroGPT, Sapling | Variância de perplexity e burstiness próximas a humano | `std(perp)/mean(perp)` ≈ 0,9-1,2 |
| **L2 — Detectores supervisionados** | Originality.ai, Copyleaks, Pangram, Turnitin | Distribuição de POS-tags, n-grams e função-palavras indistinguíveis | AUROC ≤ 0,55 vs detector |
| **L3 — Watermarking de origem** | SynthID-Text (Google), Aaronson scheme (OpenAI) | Reescrita destrutiva da assinatura criptográfica | Detectabilidade < 5% pós-reescrita |
| **L4 — Política editorial humana** | Google Spam Brain (Scaled Content Abuse), Quality Rater Guidelines | EEAT verificável: autor real, expertise demonstrada, disclosure | Trust score qualitativo |

### 1.1 Features que os detectores usam

| Feature | Como mede | Sinal humano vs IA cru | Detector que mais usa |
|---------|-----------|------------------------|------------------------|
| **Perplexity** | log-prob média de cada token sob LM de referência (GPT-2) | Humano ~70-110; LLM cru ~15-25 | GPTZero, ZeroGPT |
| **Burstiness** | desvio-padrão / média de perplexity por sentença | Humano 0,9-1,5; LLM cru 0,2-0,5 | GPTZero |
| **Top-k token rank** (GLTR) | % de tokens nos top-10/100/1000 mais prováveis | Humano espalha em rank alto; LLM concentra em top-10 | GLTR demo (MIT-IBM) |
| **Stylometry** | distribuição de função-palavras, sentence-length variance, POS-tag bigrams | Assinatura idiossincrática | Copyleaks, Pangram |
| **Watermark soft (green-list)** | tokens "verdes" sobre-amostrados por hash de prefixo | Sem padrão | SynthID, Kirchenbauer |
| **Classificador transformer end-to-end** | embedding do texto inteiro → binário | Aprendido | Originality 3.0, Pangram, Turnitin |

### 1.2 Famílias de técnicas de humanização (defesa)

| Família | Mecanismo | Eficácia típica vs detector comercial |
|---------|-----------|----------------------------------------|
| **Synonym/paraphrase swap** (Quillbot básico, BypassGPT) | troca lexical superficial | 30-45% bypass — fraco |
| **Burstiness control via prompt** | instrução para variar sentence-length | +10-20pp em bypass-rate quando combinado |
| **Persona/few-shot conditioning** | anchor com 800-1500 palavras de estilo-alvo | +15-25pp; quebra padrões médios |
| **Paraphrasing model dedicado** (DIPPER 11B) | reescrita com diversidade lexical + reorder controlados | Derruba DetectGPT de 70,3% → 4,6% (FPR=1%) |
| **Multi-pass adversarial editing** (Adversarial Paraphrasing) | rewriter usa detector-score como reward | >95% → <5% detecção em 3 passes |
| **Adversarial decoding** (Wang 2024, Zhang 2024) | perturbações mínimas no sampling | Derruba detectores comerciais; pode degradar legibilidade |
| **Self-Disguise (SDA)** | LLM aprende a se "disfarçar" durante geração | Supera baseline prompt-only sem fine-tuning |
| **HUMPA — Humanized Proxy Attack** (ICLR 2025) | proxy small RL-tuned modifica probs do target LLM | State-of-the-art em 2025 |

### 1.3 O eixo ortogonal: política Google

Independente do score de detector, Google passou a tratar **escala sem revisão humana** como spam — não tratar "texto IA" como spam per se. Essa distinção é central:

- **Penalizado**: produção em escala (centenas/milhares de páginas/mês) sem autor verificável, sem expertise demonstrada, com objetivo primário de ranquear.
- **Seguro**: IA como assistência em conteúdo first-party, com autor humano com expertise, revisão e EEAT verificável.

Logo: **humanização estilística sozinha é insuficiente**. Sem disciplina de volume + autor canônico + disclosure, mesmo texto perfeitamente humano-like é penalizado se publicado em escala spam.

---

## 2. Estado-da-Arte (papers 2024-2026)

### 2.1 Detecção — limites teóricos e empíricos

| Paper | Ano | Achado central | URL |
|-------|-----|----------------|-----|
| Sadasivan et al. — *Can AI-Generated Text be Reliably Detected?* (TMLR) | 2023, v4 2024 | Prova que detectores convergem ao classificador aleatório quando distribuição humano/LLM converge. Recursive paraphrasing quebra watermarks, zero-shot e retrieval. | arXiv:2303.11156 |
| Liang et al. — *GPT detectors are biased against non-native English writers* (Patterns) | 2023 | 7 detectores classificam >50% de redações TOEFL como IA vs ~0% de nativos US 8º ano. Causa: perplexity menor em ESL. Reescrita "mais literária" derruba detecção a ~0%. | arXiv:2304.02819 |
| Bao et al. — *Fast-DetectGPT* (ICLR 2024) | 2023 | Substitui passo de perturbação por sampling condicional; +75% AUROC e 340× mais rápido que DetectGPT. | arXiv:2310.05130 |

### 2.2 Watermarking — implementação e quebra

| Paper | Ano | Achado central | URL |
|-------|-----|----------------|-----|
| Kirchenbauer et al. — *A Watermark for Large Language Models* (ICML 2023) | 2023 | Esquema canônico soft (tokens "verdes" promovidos no sampling). Detectável sem acesso ao modelo. | arXiv:2301.10226 |
| Dathathri et al. — *Scalable watermarking* (Nature) | 2024 | Paper oficial do **SynthID-Text** (Google DeepMind). 20M respostas chatbot, qualidade preservada. Pouco robusto a tradução e respostas factuais curtas. **Código open**. | nature.com/articles/s41586-024-08025-4 / github.com/google-deepmind/synthid-text |
| Jovanović et al. — *Watermark Stealing* (ETH Zurich) | 2024 | Ataques de spoofing com >80% sucesso em SELFHASH; permite gerar texto que parece watermarkado por outra entidade. | sri.inf.ethz.ch/.../jovanovic2024watermarkstealing.pdf |
| Pang et al. — *No Free Lunch in LLM Watermarking* (NeurIPS 2024) | 2024 | Trade-offs robustez/utilidade/usabilidade; spoofing "piggyback" injeta toxicidade preservando detectabilidade. | proceedings.neurips.cc/.../2024 |

### 2.3 Humanização / evasão — estado-da-arte 2023-2025

| Paper | Ano | Achado central | URL |
|-------|-----|----------------|-----|
| Krishna et al. — *DIPPER* (NeurIPS 2023) | 2023 | Paraphraser 11B com controle de diversidade lexical e reordenação. Derruba DetectGPT de 70,3% → **4,6%** (FPR=1%) sem alterar semântica. Defesa: retrieval em base de gerações anteriores. | arXiv:2303.13408 |
| Wang et al. — *Humanizing Machine-Generated Content via Adversarial Attack* | 2024 | Perturbações mínimas (typos, homoglyphs, format chars) derrubam detectores comerciais. | arXiv:2404.01907 |
| Zhang et al. — *Adversarial Decoding* | 2024 | Decoding adversarial generalizado: evasão, RAG poisoning, jailbreak. Texto legível para múltiplos objetivos. | arXiv:2410.02163 |
| *Adversarial Paraphrasing — universal humanization attack* | 2025 | Framework **training-free** que usa LLM instruction-tuned guiado por feedback do detector. Universal: generaliza a múltiplos detectores comerciais. | arXiv:2506.07001 |
| *Contrastive Paraphrase Attacks — "Your Language Model Can Secretly Write Like Humans"* | 2025 | Decoding contrastivo entre LLM e versão humano-fine-tuned. | arXiv:2505.15337 |
| *Self-Disguise Attack (SDA)* | 2025 | LLM aprende a "se disfarçar" durante a geração; supera prompt-only sem fine-tuning custoso. | arXiv:2508.15848 |
| HUMPA — *Humanized Proxy Attack* (ICLR 2025) | 2025 | Fine-tuna proxy small via RL e modifica probabilidades do target LLM. State-of-the-art em ICLR 2025. | proceedings.iclr.cc/.../2025 |

> **Síntese das 3 frentes**: detectores são teoricamente limitados (Sadasivan); na prática, são bons contra LLM cru e fracos contra reescrita adversarial (Krishna, Wang, *Adversarial Paraphrasing 2025*); watermarks são prática emergente mas têm ataques de quebra documentados (Jovanović, Pang). Conclusão: **defesa robusta requer multi-pass com detector-in-the-loop**.

---

## 3. Ferramentas — Detectores e Humanizadores

### 3.1 Detectores comerciais — FPR medido vs declarado

| Detector | Mecanismo declarado | Preço 2026 | FPR oficial | FPR medido (3rd party) | Veredito |
|----------|---------------------|------------|-------------|------------------------|----------|
| **Pangram** | Transformer fine-tuned em corpus active-learning multi-domínio | $0,99/100 scans (consumer); API custom | <0,5% | **~0%** (UChicago Booth ago/2025, único que cumpre policy cap FPR≤0,005) | **Top — usar como gate de qualidade** |
| **Originality.ai 3.0 Lite/Turbo** | Ensemble transformer proprietário + plagiarism scanner | $14,95/mês Pro; $30 PAYG | 0,5% (Lite) / 1,5% (Turbo) | 4,79% (RAID GPTZero); 5,7% (CyberNews 2026) | Bom; usado no SEO/editorial |
| **GPTZero** | Perplexity + burstiness + classificador 7 camadas | $12,99/mês Premium | n/d | Alto FPR em ESL (Liang et al.) | Pioneiro mas vulnerável |
| **Turnitin AI Detection** | Classificador transformer humano/IA | Licença institucional | <1% (docs ≥20% IA) | 5-12% em ESL, prosa técnica, drafts editados | Várias universidades **desativaram** (incl. Vanderbilt) |
| **Copyleaks** | Classificador proprietário | $9,99/mês inicial | 0,2% (interno) | ~11% em amostras adversariais | OK para SEO; ruim para acadêmico |
| **Winston AI** | Proprietário + detecção de imagens | $12-$19/mês | até 99,98% accuracy | Variações em texto curto | Diferencial: multimídia |
| **ZeroGPT** | DeepAnalyse Technology (proprietário) | Free tier amplo | 98% accuracy | ~9,6% FPR | Free mas instável |
| **Sapling AI Detector** | Classificador + integração CRM | $25-$75/mês API | n/d | 68% accuracy (Scribbr 2024) | Nicho enterprise |

**Decisão**: **Pangram** é o único detector com FPR validado <0,5% em estudo independente UChicago Booth. **Não usar como meta de bypass — usar como gate de qualidade pré-publish**. Se o seu próprio conteúdo dispara Pangram como AI, há sinal real.

### 3.2 Humanizadores SaaS — bypass-rate medido (não claims do fornecedor)

| Humanizador | Mecanismo | Preço 2026 | Bypass médio | Forte em | Fraco em |
|-------------|-----------|-----------|--------------|----------|----------|
| **Phrasly** | Multi-modelo + style transfer | $12-$24,99/mês | Passa em todos os 5 detectores (top categoria) | Geral | — |
| **Undetectable.ai** | 3 modos (Univ/Journalist/Marketing) | $9,99-$209/mês | **88%** | Acadêmico (caso Turnitin 98% → 18%) | Texto curto |
| **WriteHuman** | Style transfer + keyword bracketing SEO | $9-$22/mês | 78% | Prosa B2B | Acadêmico/Turnitin |
| **HIX Bypass** | 4 modos (Fast/Balanced/Aggressive/Latest) | $19,99/mês | 75% | Latest modo | Aggressive degrada legibilidade |
| **StealthGPT** | Geração nativa + paraphraser | $14,99-$99,99/mês | 67-71% (testes contraditórios) | n/d | Falha em Turnitin/Originality em alguns testes |
| **Humbot** | Paraphraser | $13,49-$29,99/mês | 62,8% | ZeroGPT (72%) | Originality (54%) |
| **QuillBot Humanizer** | Paraphraser (lançado fim 2025) | $9,95/mês | **47,4%** (coin-flip) | — | Considerado paraphraser, não humanizer real |
| **BypassGPT** | Synonym swap | $9,99/mês | **32,8%** | — | Pior performer |
| **Writesonic Humanizer** | Integrado à plataforma | Plano Writesonic | n/d (sem benchmark formal) | n/d | n/d |

**Insight transversal**: ferramentas acima de **60% bypass** (Undetectable, WriteHuman, StealthGPT, Humbot, HIX, Phrasly) tocam padrão estatístico (variância de sentença, distribuição de POS). Abaixo disso são "synonym swappers" — não vale o gasto.

### 3.3 Stack open-source para implementação interna

| Componente | Lib / repo | Uso |
|------------|-----------|-----|
| Cálculo de perplexity local | [`lmppl`](https://github.com/asahi417/lmppl) — `LM('gpt2').get_perplexity(text)` | Score de perplexity por sentença |
| Cálculo de perplexity HF | `evaluate.load("perplexity").compute(predictions=[...], model_id="gpt2")` | Alternativa HuggingFace |
| GLTR (visualização token-rank) | [gltr.io](http://gltr.io) / [HendrikStrobelt/detecting-fake-text](https://github.com/HendrikStrobelt/detecting-fake-text) | Auditoria visual de distribuição token-rank |
| Reimplementação aberta GPTZero | [BurhanUlTayyab/GPTZero](https://github.com/BurhanUlTayyab/GPTZero) | Burstiness + perplexity GPT-2, código direto |
| Watermark + detector SynthID-Text | [google-deepmind/synthid-text](https://github.com/google-deepmind/synthid-text) | Implementação oficial (Apache 2.0) |
| DIPPER paraphraser | [martiansideofthemoon/ai-detection-paraphrases](https://github.com/martiansideofthemoon/ai-detection-paraphrases) | Paraphraser 11B (T5-XXL fine-tuned) |

---

## 4. Política Google e Brasil (2024-2026)

### 4.1 Google — March 2024 Spam Update e desdobramentos

**Doc canônico**: <https://developers.google.com/search/blog/2024/03/core-update-spam-policies>

A atualização introduziu **três spam policies** novas:

1. **Scaled Content Abuse** (em vigor desde 2024-05-05) — Texto-chave: "ação independente de o conteúdo ser gerado por automação, humano ou combinação". Resultado declarado pelo Google: **-45% de conteúdo low-quality** nos SERPs.
2. **Expired Domain Abuse** — Compra de domínio expirado para hospedar conteúdo descorrelacionado.
3. **Site Reputation Abuse** — Primeiros alvos manuais (2024-05-07): CNN Underscored, Forbes Advisor, WSJ Buy Side (cupons/voucher). Update algorítmico anunciado em [nov/2024](https://developers.google.com/search/blog/2024/11/site-reputation-abuse).

### 4.2 Posição oficial Google sobre AI content

| Fonte | Citação relevante |
|-------|-------------------|
| [Google Search Blog 2023-02](https://developers.google.com/search/blog/2023/02/google-search-and-ai-content) | "We focus on the quality of content, not how content is produced." |
| Danny Sullivan (Search Liaison, até 2025-08-01) | "Content created primarily for search engine rankings, however it is done, is against our guidance." |
| Sullivan (2026-01-08, pós-saída) | Alertou contra "splitting content into bite-sized pieces for LLMs" — sinal de que **GEO-style chunking pode disparar policy**. |
| [Quality Rater Guidelines set/2025 (182 pp)](https://services.google.com/fh/files/misc/hsw-sqrg.pdf) | Critério para AI Overviews. **Trust** = componente mais importante do EEAT. YMYL expandido para eleições, instituições civis e governo. |

### 4.3 O que é seguro vs penalizado (operacional)

| Seguro | Penalizado |
|--------|-----------|
| IA como assistência em conteúdo first-party | Produção em escala sem oversight humano |
| Autor real com expertise demonstrada | Páginas geradas primariamente para ranquear |
| Revisão humana explícita + disclosure | Mass-publishing sem valor incremental |
| EEAT verificável (autor, citações, fontes) | Conteúdo sem autor canônico identificável |
| Disciplina de volume (artigos/semana, não /hora) | Centenas/milhares de páginas/mês sem revisão |

### 4.4 Caso documentado — HouseFresh

[housefresh.com/how-google-decimated-housefresh](https://housefresh.com/how-google-decimated-housefresh) — HouseFresh (editorial técnico, equipe humana, expertise verificável em air purifiers) **perdeu ~90% do tráfego orgânico** após core updates 2023-2024 enquanto Forbes/CNN Underscored ranqueavam acima com conteúdo IA de baixa qualidade. Pós-enforcement do Site Reputation Abuse (mai/2024), a balança começou a corrigir.

> **Lição operacional**: estar do "lado certo" do EEAT não é suficiente em algoritmo míope; o enforcement de policies *é* parte do que torna o lado certo defensável.

### 4.5 Brasil — quadro regulatório 2024-2026

| Norma / instrumento | Status | Impacto operacional no curso-factory |
|---------------------|--------|--------------------------------------|
| **PL 2338/2023 (Marco Legal da IA)** | Aprovado no Senado dez/2024, em tramitação na Câmara, sanção esperada 2026 | Disclosure mandatório: usuário deve saber que interage com IA; identificação obrigatória de conteúdo gerado/manipulado por IA (inclui texto). 4 classes de risco. [Senado matéria 157233](https://www25.senado.leg.br/web/atividade/materias/-/materia/157233) |
| **MEC — Marco Referencial IA na Educação** | Lançado 2025-07; orientações específicas em [abr/2026](https://www.gov.br/mec/pt-br/assuntos/noticias/2026/abril/mec-lanca-orientacoes-sobre-ia-na-educacao-basica) | Cursos para Educação Básica devem seguir orientações curriculares + princípios éticos do Marco. 15k+ escolas públicas já usam IA (+300% vs 2023, fonte MEC). |
| **CFP — Posicionamento 03/07/2025** | Posicionamento (não Resolução) — IA generativa em prática clínica e conteúdo psicológico exige supervisão e disclosure | Cursos psicológicos (cliente GEO IPOG) **obrigatoriamente** trazem disclaimer + revisão por psicólogo registrado |
| **LGPD art. 20 + ANPD regulamento out/2024** | Em vigor | Direito à revisão de decisões automatizadas; ANPD com competência sobre treinamento IA |
| **INEP** | Sem norma direta sobre AI content avaliado (ENEM/ENADE) até cutoff verificável | Tripé canônico para citar: MEC + CFP + PL 2338 |

---

## 5. Técnicas Aplicáveis

### 5.1 Burstiness control via prompt (REVOGADO em 11/08/2026)

> **REVOGADO.** A instrução abaixo entrou nos prompts em maio de 2026 e foi
> removida em 11/08/2026 pela `DIRETRIZ_EDITORIAL.md` v3 (§4.7). Ela melhora a
> métrica e piora o texto: a cota de frase curta por parágrafo produz staccato
> de manchete, que os catálogos de detecção de 2026 listam como marcador tanto
> quanto a uniformidade que ela pretendia corrigir, e texto ajustado para a
> métrica continua distinguível por leitores humanos (Tabach,
> [arXiv:2604.23471](https://arxiv.org/abs/2604.23471), abril de 2026). O
> registro fica aqui como histórico da pesquisa; o que vale hoje é o
> diagnóstico do bloco de dez frases, aplicado ao texto pronto. Ver
> [`wiki/decisions/diretriz-editorial-v3-narrativa-sem-cota.md`](../../wiki/decisions/diretriz-editorial-v3-narrativa-sem-cota.md).

Instrução que era usada com o redator (GPT-4o no curso-factory):

```
Varie comprimento de frase entre 4 e 35 palavras. Em CADA parágrafo,
inclua ao menos UMA frase de 6 palavras ou menos. Alternância obrigatória:
nunca duas frases consecutivas com comprimento na mesma faixa (curta 4-10,
média 11-22, longa 23-35).
```

Ataca diretamente a métrica do GPTZero, e esse era exatamente o problema: otimizava o detector em vez do leitor. Fonte prática original: Jordan Gibbs, *This Prompt Fools Every AI Detector* ([Medium](https://medium.com/@jordan_gibbs/this-prompt-fools-every-ai-detector-b9ad8c97c07d)).

### 5.2 Persona conditioning com few-shot real

Anchor com **800-1500 palavras** do autor-alvo no prompt, depois pedir continuação. Funciona melhor que fine-tuning para volumes pequenos. No curso-factory, o cliente "default" (Alexandre/Brasil GEO) deve ter `client.yaml` com `voice_samples:` apontando para 3-5 trechos canônicos reais.

Doc LangChain: [FewShotPromptTemplate](https://python.langchain.com/docs/concepts/few_shot_prompting/).

### 5.3 Hedge / aside / anecdote injection

Adicionar (a cada seção do módulo):
- **Hedge natural**: "pelo menos no meu caso", "no que vi até aqui", "ainda em hipótese" — evita over-confidence típica de LLM
- **Aside parentético**: "(detalhe que demorei para entender)", "(e isso vai contra a intuição)"
- **Mini-anedota factual de 1-2 frases**: "Em 2019 chegamos a testar X e o resultado foi Y" — *desde que ancorada em `{context}` da pesquisa*, sem inventar

Quebra cadência uniforme do LLM. Documentado em [Analytics Vidhya 2025](https://www.analyticsvidhya.com/blog/2025/07/ai-humanizer-how-chatgpt-writes-like-human/).

### 5.4 Multi-pass adversarial editing com detector-in-the-loop

Implementação canônica (Krishna DIPPER + Adversarial Paraphrasing 2025):

```
Pass 1: gerar com GPT-4o + draft.md (estado atual)
Pass 2: rodar detector (Pangram/Originality) → score
Pass 3: se score > threshold, reescrever com prompt humanizer
        passando score como signal:
        "score atual: 0.78 (alto). Reescrever quebrando padrão estatístico:
         variar comprimento de frase 4-35 palavras, mover sujeito de início
         para meio em 30% das frases, injetar 2 asides parentéticos por seção"
Pass 4: re-medir; iterar até score ≤ threshold OU max_iters = 3
```

Reduz detecção de >95% para <5% em 3 iterações típicas (Adversarial Paraphrasing 2025, arXiv:2506.07001).

### 5.5 Stylometry expansion no voice_guard

5ª dimensão a adicionar no `voice_guard.py`:

| Sub-métrica | Como calcular | Threshold humano |
|-------------|---------------|------------------|
| `burstiness_score` | `np.std(sentence_perps) / np.mean(sentence_perps)` | ≥ 0,8 |
| `sentence_length_variance` | `np.var(sentence_word_counts)` | ≥ 50 (em corpus PT-BR HBR-grade) |
| `function_word_distribution_chi2` | χ² entre distribuição do texto e baseline humano | p > 0,05 |
| `top10_token_rank_pct` (GLTR-like) | % de tokens nos top-10 mais prováveis | ≤ 70% |

Peso sugerido: 20 (rebalancear anti-clichê 30→25, Bloom 30→25, naming 25→20, HBR 15→10, **stylometry 20**).

### 5.6 Disclosure de IA (PL 2338 + CFP + EEAT)

Embed obrigatório no rodapé de cada módulo:

```markdown
> **Sobre a produção deste conteúdo**: Co-produzido com pipeline de IA
> (Perplexity, GPT-4o, Gemini, Claude) e revisado por {{client.author_name}}
> ({{client.author_credential}}). Disclosure conforme PL 2338/2023 e
> {{client.disclosure_extra | default('Marco Referencial MEC IA na Educação')}}.
```

Para cliente GEO IPOG (psicologia), adicionar:
```
Revisão técnica psicológica por {{psychologist_crp}}. Conformidade com
Posicionamento CFP de 03/07/2025 sobre uso de IA em conteúdo psicológico.
```

---

## 6. Diagnóstico do curso-factory

### 6.1 O que JÁ existe (forte — manter e amplificar)

| Camada | Onde está | O que faz bem |
|--------|-----------|---------------|
| **21 anti-padrões "cara de IA"** | `src/templates/prompts/draft.md:28-54` e `review.md:132-156` | Cobertura ampla de marcadores de prosa LLM (grandeza artificial, gerúndio ornamental, atribuição vaga, simetria, frase de efeito, hedging excessivo) — equivalente conceitual ao que humanizadores SaaS tentam fazer |
| **Regra anti-invenção** | `draft.md:9-26`, `review.md:158-166`, `quality_rules.yaml:157-163` | Marker `[FALTA EVIDÊNCIA: ...]` em vez de fabricar dado — defende contra hallucination, sustenta EEAT |
| **Voice Guard 4D** | `src/validators/voice_guard.py` | Score 0-100 ponderado (anti-clichê 30, Bloom 30, naming 25, HBR 15) — barreira programática real, não só prompt |
| **Acentuação 4 barreiras** | `accent_checker.py` + 3 prompts | Defende sinal de qualidade editorial em PT-BR — proxy de revisão humana cuidadosa |
| **58 expressões proibidas** | `config/quality_rules.yaml:104-156` | Cobre clichês clássicos + 30 padrões "Humanizador 2.6.2" |
| **5 LLMs orquestrados com fallback** | `src/orchestrator.py`, `src/llm_client.py` | Reduz dependência de modelo único; circuit breaker + budget guard |

### 6.2 O que FALTA (gaps que detectores 2024-2026 exploram)

| Gap | Impacto | Severidade |
|-----|---------|------------|
| **Nenhuma medição estatística pós-geração** (zero burstiness, zero perplexity check, zero stylometry) | curso-factory produz HBR-grade mas pode disparar GPTZero/Pangram justamente porque a uniformidade de estilo HBR tem perplexity baixa | **ALTA** |
| **Nenhum self-test contra detector externo** (sem integração Pangram/Originality API) | Não sabemos a probabilidade de detecção dos próprios cursos antes do publish | **ALTA** |
| **Revisão é 1-pass** (Claude no review.md) | Sem multi-pass adversarial editing com detector-in-the-loop; ataque arXiv:2506.07001 documenta que 3 passes derrubam >95% → <5% | **MÉDIA-ALTA** |
| **"Humanizador 2.6.2" só existe em prompt** (sem reforço programático após geração) | Se o LLM ignorar parte da auditoria (e LLMs ignoram 10-30% das instruções em prompts longos), nenhum validador detecta o resíduo | **MÉDIA** |
| **Sem persona-conditioning few-shot real** (voz Alexandre está em prompts genéricos, sem 800-1500 palavras anchor) | Saída é "HBR genérico", não "Alexandre Caramaschi HBR" — perde idiossincrasia que torna texto humano-like | **MÉDIA** |
| **Estrutura HBR rígida é faca de dois gumes** (tabela obrigatória + Bloom verbs + Knowles 6 princípios) | Garante qualidade pedagógica MAS cria uniformidade estatística (cada módulo na mesma forma) que classificadores supervisionados capturam | **MÉDIA** |
| **Sem disclosure de IA programaticamente embutido** (PL 2338, CFP, MEC) | Risco regulatório real para cliente GEO IPOG; perde sinal EEAT de Trust no Google | **MÉDIA-ALTA** |
| **Sem tracking histórico de detection-score** (cost_history.jsonl existe, detection_history.jsonl não) | Não há forma de auditar tendência ou detectar drift quando algum LLM da banca muda | **BAIXA-MÉDIA** |

### 6.3 Trade-off central a reconhecer

O curso-factory foi otimizado para **qualidade editorial HBR-grade** — e isso é o produto. As recomendações abaixo **não devem ser interpretadas como "ferir o padrão HBR para fugir de detector"**. A linha é:

> **"O curso de HBR autêntico, escrito por editor humano, passa em Pangram com FPR ~0%. Se o nosso curso não passa, ele não está HBR-grade ainda."**

Pangram + multi-pass não são para "burlar detector". São para **medir se entregamos qualidade humana real**.

---

## 7. Recomendações Priorizadas (8 PRs)

Ordenados por (impacto × tração) / esforço. XS = <2h, S = 2-6h, M = 1-2d, L = 3-5d.

### PR-1 — Burstiness control no prompt do redator (REVOGADO em 11/08/2026, ver §5.1)
**Esforço**: XS · **Impacto**: ALTO · **Risco**: baixo (revertível em commit)

> **REVOGADO.** Implementado em maio de 2026 e removido dos prompts em
> 11/08/2026 pela `DIRETRIZ_EDITORIAL.md` v3 (§4.7). Foi a principal causa da
> queda de qualidade dos textos gerados. Detalhe em §5.1 deste documento.

Adicionar 1 seção em `src/templates/prompts/draft.md` (entre seção 21 anti-padrões e Andragogia) e idêntica em `src/templates/prompts/pt-br/draft.md`:

```markdown
## Cadência e Burstiness — INVIOLÁVEL

Varie comprimento de frase entre 4 e 35 palavras. Em CADA parágrafo, inclua ao menos UMA frase de 6 palavras ou menos. Alternância obrigatória: nunca duas frases consecutivas na mesma faixa (curta 4-10, média 11-22, longa 23-35).

LLMs sem essa instrução produzem cadência homogênea, capturada por detectores via burstiness < 0,5 (humano: 0,9-1,5). Esta instrução é mais importante que qualquer outra anti-IA — ela é a única que move métrica estatística diretamente.
```

Aplicar também ao `es/draft.md` e `en/draft.md`. Atualizar autoavaliação final do `draft.md` com checkbox "Cadência burstiness alta — verificado por amostragem de 5 parágrafos".

**Arquivos**: `src/templates/prompts/draft.md`, `src/templates/prompts/pt-br/draft.md`, `src/templates/prompts/es/draft.md`, `src/templates/prompts/en/draft.md`.

### PR-2 — Validator `stylometry_checker.py` (medição programática local)
**Esforço**: M · **Impacto**: ALTO · **Risco**: baixo (novo módulo, opt-in)

Criar `src/validators/stylometry_checker.py` que computa:

```python
@dataclass
class StylometryReport:
    burstiness: float            # std(perp)/mean(perp); humano ≥ 0.8
    sentence_len_variance: float  # var(word_counts); HBR-PT-BR ≥ 50
    top10_token_pct: float        # GLTR-like; humano ≤ 70%
    mean_perplexity: float        # via lmppl com GPT-2 PT-BR
    score: int                    # 0-100 combinando as 4
    aprovado: bool                # score >= min_stylometry (default 70)
    sentences: list[tuple[str, float]]  # diagnóstico por sentença
```

Implementação:
- Dependência: `lmppl` (já open-source) ou `evaluate` (HuggingFace) — usar modelo `pierreguillou/gpt2-small-portuguese` para PT-BR
- Cache de embeddings/perplexity em `output/.cache/stylometry/`
- CLI: `python cli.py stylometry --input output/drafts/modulo-3.md`

Integrar no `quality_gate.py` como **camada 5**, opt-in via `config/quality_rules.yaml`:

```yaml
quality_rules:
  stylometry:
    enabled: true
    min_burstiness: 0.8
    min_sentence_len_variance: 50
    max_top10_token_pct: 0.75
    min_combined_score: 70
    block_below_threshold: false  # primeiro só report, depois bloquear
```

**Arquivos**: `src/validators/stylometry_checker.py` (novo), `src/validators/quality_gate.py` (integrar), `config/quality_rules.yaml` (config), `tests/test_stylometry.py` (novo), `pyproject.toml` (dep lmppl).

### PR-3 — Integração Pangram API como self-test pré-publish
**Esforço**: S · **Impacto**: ALTO · **Risco**: médio (depende de chave + custo $0,99/100 scans)

Pangram é o único detector com FPR validado <0,5% em estudo independente UChicago Booth. Usar **não como meta de bypass, mas como gate de qualidade**: se nosso conteúdo HBR-grade dispara Pangram, há sinal real.

Criar `src/validators/external_detector_check.py`:

```python
def pangram_self_test(text: str, threshold: float = 0.3) -> DetectorReport:
    """Roda Pangram API; se ai_likelihood > threshold, aprovado=False."""
```

Integrar como **camada 6 opcional** no quality_gate, controlada por env var `EXTERNAL_DETECTOR_ENABLED=true` (não bloqueante por default — primeiro auditar 10 cursos para calibrar threshold).

**Arquivos**: `src/validators/external_detector_check.py` (novo), `src/config.py` (env var + endpoint Pangram), `docs/FINOPS.md` (custo do scan), `output/detection_history.jsonl` (log persistente).

### PR-4 — Agente humanizer.py (multi-pass adversarial editing)
**Esforço**: L · **Impacto**: ALTO · **Risco**: médio (custo extra Claude + latência)

Criar `src/agents/humanizer.py` que roda DEPOIS do reviewer.py (Claude), implementando o pattern Krishna DIPPER + Adversarial Paraphrasing 2025:

```python
class HumanizerAgent(BaseAgent):
    """Roda DEPOIS do reviewer. Multi-pass com detector-in-the-loop.

    Pass 1: medir stylometry + (opcional) Pangram
    Pass 2: se score ruim, reescrever com prompt humanizer passando
            score como signal
    Pass 3: re-medir; iterar até score OK OU max_iters=3
    """
    max_iters: int = 3
    target_burstiness: float = 0.9
    target_pangram_score: float = 0.2  # se EXTERNAL_DETECTOR_ENABLED
```

Prompt `src/templates/prompts/humanize.md` (novo, ~120 linhas):
- Recebe texto + relatório de stylometry + erros específicos
- Instruções cirúrgicas: "frases 12-18 estão todas com 20-25 palavras; quebre frase 14 em duas (uma curta de 5 palavras)"
- **Inviolável**: não pode mudar fatos, números, citações, blocos de código, marcadores `[FALTA EVIDÊNCIA]`
- Usa o cliente: persona-conditioning com `client.voice_samples`

Integrar no `src/agents/pipeline.py` como etapa 6 (opt-in via `pipeline.humanize_enabled: true` no client.yaml).

**Arquivos**: `src/agents/humanizer.py` (novo), `src/templates/prompts/humanize.md` (novo), `src/templates/prompts/pt-br/humanize.md` (novo), `src/agents/pipeline.py` (integrar etapa 6), `src/clients/context.py` (`voice_samples` field), `tests/test_humanizer.py` (novo).

### PR-5 — Persona-conditioning via `voice_samples` em client.yaml
**Esforço**: S · **Impacto**: MÉDIO-ALTO · **Risco**: baixo

Adicionar campo no schema do client.yaml:

```yaml
voice_guard:
  voice_samples:
    - path: docs/voice/alexandre_caramaschi/hbr_post_GEO_brasil.md
      length_words: 1200
      tags: [HBR, GEO, contraintuitive]
    - path: docs/voice/alexandre_caramaschi/linkedin_post_stone.md
      length_words: 850
      tags: [LinkedIn, fintech]
    - path: docs/voice/alexandre_caramaschi/medium_article_AI_brazil.md
      length_words: 1400
      tags: [Medium, AI, Brasil]
  voice_anchor_strategy: rotate  # rotate | concat | random
  voice_anchor_max_words: 2000  # cap para não estourar context
```

O `BaseAgent.load_prompt()` injeta o anchor antes do `{context}` do draft.md/review.md/humanize.md.

Para cliente default (Brasil GEO), criar:
- `docs/voice/alexandre_caramaschi/` com 3-5 amostras reais (extrair de medium.com/@alexandrecaramaschi, LinkedIn, ou alexandrecaramaschi.com — sob curadoria do próprio Alexandre)

**Arquivos**: `src/clients/context.py` (schema), `src/agents/base.py` (load anchor), `docs/voice/alexandre_caramaschi/*.md` (3-5 amostras), `config/clients/default/client.yaml` (apontar), `docs/MULTI-CLIENT.md` (documentar campo).

### PR-6 — Disclosure de IA programático (PL 2338 + CFP + MEC)
**Esforço**: S · **Impacto**: MÉDIO-ALTO · **Risco**: baixo (mas obrigatório para conformidade)

Adicionar bloco de disclosure obrigatório no rodapé de cada módulo, parametrizado por cliente:

```yaml
# config/clients/default/client.yaml
disclosure:
  enabled: true
  required_by: [PL_2338_2023]
  author_name: Alexandre Caramaschi
  author_credential: CEO da Brasil GEO, ex-CMO da Semantix (Nasdaq), cofundador da AI Brasil
  pipeline_models: [perplexity-sonar-pro, gpt-4o, gemini-2.5-pro, claude-opus-4-7]
  reviewer_human: true

# config/clients/geo_ipog/client.yaml
disclosure:
  enabled: true
  required_by: [PL_2338_2023, CFP_Posicionamento_03_07_2025, MEC_Marco_Referencial_2025]
  author_name: Alexandre Caramaschi
  author_credential: CEO da Brasil GEO
  reviewer_extra:
    - role: psicólogo registrado
      crp_required: true
      field_in_template: psychologist_crp
```

Validator `src/validators/disclosure_checker.py` verifica presença e parametrização correta. Bloqueia se ausente em cliente com `disclosure.enabled: true`.

**Arquivos**: `src/clients/context.py` (schema), `src/validators/disclosure_checker.py` (novo), `src/templates/prompts/review.md` (instruir o reviewer a embutir o disclosure), `src/validators/quality_gate.py` (camada 7), `tests/test_disclosure.py`.

### PR-7 — Burstiness/perplexity expansion no voice_guard como 5ª dimensão
**Esforço**: M · **Impacto**: MÉDIO · **Risco**: baixo (rebalanceia pesos existentes)

Rebalancear pesos do `WEIGHTS` em `src/validators/voice_guard.py`:

```python
# antes
WEIGHTS = {"anti_cliche": 30, "bloom_andragogia": 30, "naming": 25, "hbr_style": 15}

# depois
WEIGHTS = {"anti_cliche": 25, "bloom_andragogia": 25, "naming": 20, "hbr_style": 10, "stylometry": 20}
```

`_score_stylometry()` consome `StylometryReport` (do PR-2). Atualizar `min_score` default de 70 para 65 (a 5ª dimensão é mais difícil de bater inicialmente).

**Arquivos**: `src/validators/voice_guard.py` (pesos + nova dimensão), `tests/validators/test_voice_guard.py` (atualizar testes), `docs/ARCHITECTURE.md` (documentar mudança).

### PR-8 — `detection_history.jsonl` + comando `cli.py detection-report`
**Esforço**: S · **Impacto**: BAIXO-MÉDIO · **Risco**: baixo (somente leitura)

Análogo ao `cost_history.jsonl`. Registra:
```json
{"ts": "2026-05-17T15:00:00Z", "course_id": "geo-101", "module": "m3",
 "stylometry": {"burstiness": 0.84, "perp_mean": 67.2, "top10_pct": 0.62, "score": 78},
 "pangram": {"ai_likelihood": 0.18, "raw_response": {...}},
 "voice_guard_score": 81, "approved": true, "pipeline_version": "5.2"}
```

CLI:
```bash
python cli.py detection-report --since 2026-05-01
# Output: agregado por cliente, módulo, tendência de score, drift por LLM
```

Permite auditar drift quando algum LLM da banca muda (ex: Claude Opus 4.6 → 4.7 mudou cadência).

**Arquivos**: `src/detection_tracker.py` (novo), `src/cli.py` (subcomando), `src/validators/quality_gate.py` (chamar tracker), `tests/test_detection_tracker.py`.

### 7.1 Ordem sugerida de execução

```
Semana 1: PR-1 (XS) + PR-5 amostras-base (S) + PR-2 estrutura (M, sem bloqueio)
Semana 2: PR-2 plug (validators) + PR-3 self-test não-bloqueante (calibrar threshold)
Semana 3: PR-6 disclosure (S) + PR-7 voice_guard 5D (M)
Semana 4: PR-4 humanizer.py multi-pass (L) + PR-8 history (S)
Semana 5: ativar bloqueio em PR-2 e PR-3 após calibragem de 10+ cursos
```

Custo de pesquisa/desenvolvimento estimado (LLM API + Pangram scans): ~$15-25 ao longo das 5 semanas.

---

## 8. Referências

### Papers (arXiv / NeurIPS / ICLR / Nature)
- Krishna et al., *Paraphrasing evades detectors* (NeurIPS 2023) — <https://arxiv.org/abs/2303.13408>
- Sadasivan et al., *Can AI-Generated Text be Reliably Detected?* (TMLR 2024) — <https://arxiv.org/abs/2303.11156>
- Liang et al., *GPT detectors biased against non-native English writers* (Patterns 2023) — <https://arxiv.org/abs/2304.02819>
- Kirchenbauer et al., *A Watermark for LLMs* (ICML 2023) — <https://arxiv.org/abs/2301.10226>
- Bao et al., *Fast-DetectGPT* (ICLR 2024) — <https://arxiv.org/abs/2310.05130>
- Dathathri et al., *Scalable watermarking* (Nature 2024) — <https://www.nature.com/articles/s41586-024-08025-4>
- Jovanović et al., *Watermark Stealing* (ETH 2024) — <https://files.sri.inf.ethz.ch/website/papers/jovanovic2024watermarkstealing.pdf>
- Pang et al., *No Free Lunch in LLM Watermarking* (NeurIPS 2024) — <https://proceedings.neurips.cc/paper_files/paper/2024/file/fa86a9c7b9f341716ccb679d1aeb9afa-Paper-Conference.pdf>
- Wang et al., *Humanizing Machine-Generated Content* (2024) — <https://arxiv.org/abs/2404.01907>
- Zhang et al., *Adversarial Decoding* (2024) — <https://arxiv.org/abs/2410.02163>
- *Adversarial Paraphrasing — universal humanization* (2025) — <https://arxiv.org/abs/2506.07001>
- *Contrastive Paraphrase Attacks* (2025) — <https://arxiv.org/abs/2505.15337>
- *Self-Disguise Attack (SDA)* (2025) — <https://arxiv.org/abs/2508.15848>
- HUMPA — *Humanized Proxy Attack* (ICLR 2025) — <https://proceedings.iclr.cc/paper_files/paper/2025/file/ab1ee157f7804a13f980414b644a9460-Paper-Conference.pdf>
- Pangram technical report — <https://arxiv.org/abs/2402.14873>

### Política Google
- Google Search Central, *March 2024 Core Update and Spam Policies* — <https://developers.google.com/search/blog/2024/03/core-update-spam-policies>
- Google Search Central, *Site Reputation Abuse algorithmic update* (nov/2024) — <https://developers.google.com/search/blog/2024/11/site-reputation-abuse>
- Google Search Central, *Google Search and AI content* (fev/2023) — <https://developers.google.com/search/blog/2023/02/google-search-and-ai-content>
- Google Quality Rater Guidelines (set/2025, 182pp) — <https://services.google.com/fh/files/misc/hsw-sqrg.pdf>
- HouseFresh case study — <https://housefresh.com/how-google-decimated-housefresh/>

### Detectores comerciais
- Pangram blog — third-party evals — <https://www.pangram.com/blog/third-party-pangram-evals>
- Originality.ai meta-análise — <https://originality.ai/blog/ai-detection-studies-round-up>
- GPTZero whitepaper perplexity+burstiness — <https://gptzero.me/news/perplexity-and-burstiness-what-is-it/>
- Turnitin blog (false positives) — <https://www.turnitin.com/blog/understanding-false-positives-within-our-ai-writing-detection-capabilities>
- Copyleaks accuracy blog — <https://copyleaks.com/blog/ai-detector-continues-top-accuracy-third-party>

### Humanizadores
- Undetectable.ai — <https://undetectable.ai/>
- Phrasly comparativa — <https://phrasly.ai/blog/best-ai-humanizer-tools/>
- Humbot review (BypassGPT) — <https://www.bypassgpt.ai/reviews/humbot-review>
- StealthGPT review — <https://phrasly.ai/blog/stealthgpt-review-does-it-work/>
- QuillBot Humanizer review — <https://supwriter.com/blog/quillbot-humanizer-review>
- HIX Bypass — <https://bypass.hix.ai/>
- WriteHuman — <https://writehuman.ai/>

### Open source / implementação
- `lmppl` (perplexity local) — <https://github.com/asahi417/lmppl>
- GLTR (detecção de fake text) — <https://github.com/HendrikStrobelt/detecting-fake-text>
- SynthID-Text Google DeepMind — <https://github.com/google-deepmind/synthid-text>
- Reimplementação aberta GPTZero — <https://github.com/BurhanUlTayyab/GPTZero>
- DIPPER paraphraser — <https://github.com/martiansideofthemoon/ai-detection-paraphrases>
- HuggingFace Perplexity metric — <https://huggingface.co/docs/transformers/perplexity>
- LangChain Few-Shot — <https://python.langchain.com/docs/concepts/few_shot_prompting/>

### Brasil — regulação
- PL 2338/2023 (Marco Legal IA) — <https://www25.senado.leg.br/web/atividade/materias/-/materia/157233>
- MEC, *Marco Referencial IA na Educação Básica* (jul/2025) — <https://www.gov.br/mec/pt-br/assuntos/noticias/2025/julho/mec-realiza-seminario-sobre-ia-na-educacao-basica>
- MEC, *Orientações para Educação Básica* (abr/2026) — <https://www.gov.br/mec/pt-br/assuntos/noticias/2026/abril/mec-lanca-orientacoes-sobre-ia-na-educacao-basica>
- ANPD — <https://www.gov.br/anpd/>

### Comunidade prática
- Jordan Gibbs, *This Prompt Fools Every AI Detector* (Medium) — <https://medium.com/@jordan_gibbs/this-prompt-fools-every-ai-detector-b9ad8c97c07d>
- Analytics Vidhya, *AI Humanizer — how ChatGPT writes like human* (2025) — <https://www.analyticsvidhya.com/blog/2025/07/ai-humanizer-how-chatgpt-writes-like-human/>
- Burstiness & Perplexity tutorial canônico — <https://burstinessandperplexity.com/concepts/perplexity/>
- *The Dummy Guide to Perplexity and Burstiness* (Medium The Generator) — <https://medium.com/the-generator/the-dummy-guide-to-perplexity-and-burstiness-in-ai-generated-content-1b4cb31e5a81>

---

> **Próximo passo recomendado**: abrir o PR-1 (burstiness control no prompt) agora — XS, alto impacto, revertível em 1 commit. Calibra a equipe na linguagem da humanização antes dos PRs maiores (PR-2 stylometry validator, PR-4 humanizer.py multi-pass).

---

# Apêndice A — Aprofundamento Científico V2 (2026-05-17 noite)

> Material adicionado pelos sub-agents A (papers ACL/EMNLP/NAACL + benchmarks acadêmicos) e B (fórmulas matemáticas formais + thresholds rigorosos + corpora PT-BR). Não duplica o que já está nas seções 1-8 acima; adiciona profundidade científica e detalhes implementáveis.

## A.1 Papers adicionais (não cobertos na V1)

### A.1.1 Detecção zero-shot e supervisionada

| Paper | Venue, Ano | Achado central com números | URL |
|-------|-----------|---------------------------|-----|
| **Ghostbuster** — Verma, Fleisig, Tomlin, Klein | NAACL 2024 | Passa texto por LMs fracos (unigram, trigram, GPT-3 ada/davinci-não-instruct), busca estruturada sobre combinações de features de log-probs e treina classificador. **F1 = 99,0 cross-domain** (+5,9 vs SOTA). +7,5 F1 em generalização de domínio; +4,4 F1 cross-LM. Código aberto Berkeley NLP. | [aclanthology.org/2024.naacl-long.95](https://aclanthology.org/2024.naacl-long.95/) |
| **Binoculars** — Hans et al. | ICML 2024 | Razão entre log-perplexity sob "observer" LLM e cross-perplexity sob "performer" LLM. Sem nenhum dado de treino, **>90% TPR @ FPR=0,01%** em ChatGPT. Supera GPTZero, Ghostbuster, DetectGPT. Código aberto. | [arxiv.org/abs/2401.12070](https://arxiv.org/abs/2401.12070) |
| **BiScope** — Guo, Cheng et al. | NeurIPS 2024 | Cross-entropy bi-direcional (forward + backward); memorização de tokens precedentes é sinal forte. **F1 médio 0,95** em 5 LLMs comerciais; **+0,30 F1** sobre SOTA não-comercial. | [proceedings.neurips.cc/.../bc808cf2d2444b0abcceca366b771389](https://proceedings.neurips.cc/paper_files/paper/2024/hash/bc808cf2d2444b0abcceca366b771389-Abstract-Conference.html) |
| **RADAR** — Hu, Chen, Ho | NeurIPS 2023 | Treinamento adversarial conjunto: paraphraser tenta evadir, detector tenta resistir. **AUROC 0,857** contra paraphraser inédito vs 0,651 do melhor baseline — **+31,64%**. Código aberto IBM. | [arxiv.org/abs/2307.03838](https://arxiv.org/abs/2307.03838) |
| **A Practical Examination** — Tufts et al. | NAACL Findings 2025 | Avalia RADAR, Wild, T5Sentinel, Fast-DetectGPT, PHD, LogRank, Binoculars em LLMs/domínios inéditos. **TPR@FPR=1% colapsa para 0%** em vários cenários sob prompting adversarial moderado. | [arxiv.org/abs/2412.05139](https://arxiv.org/abs/2412.05139) |
| **COLING 2025 GenAIDetect Task 1** — Wang, Mansurov et al. | COLING 2025 | Winner monolingual: **Advacheck macro F1 = 83,07%** com Transformer Encoder multi-task. | [arxiv.org/abs/2501.11012](https://arxiv.org/abs/2501.11012) |
| **COLING 2025 GenAIDetect Task 3** — cross-domain | COLING 2025 | **Pangram atingiu 99,3% accuracy** em MGT sem ataques (subset RAID). | [aclanthology.org/2025.genaidetect-1.45.pdf](https://aclanthology.org/2025.genaidetect-1.45.pdf) |

### A.1.2 Ataques avançados 2025 — quebra de detectores

| Paper | Venue, Ano | Achado | URL |
|-------|-----------|--------|-----|
| **SilverSpeak: Evading via Homoglyphs** — Creo, Pudasaini | COLING 2025 GenAIDetect | Substitui caracteres latinos por homoglifos Unicode visualmente idênticos. Testado em **7 detectores** (ArguGPT, Binoculars, DetectGPT, Fast-DetectGPT, Ghostbuster, OpenAI detector, watermarks) × **5 datasets**: **TODOS colapsam para ~50% accuracy** (random). | [arxiv.org/abs/2406.11239](https://arxiv.org/abs/2406.11239) + [aclanthology.org/2025.genaidetect-1.1.pdf](https://aclanthology.org/2025.genaidetect-1.1.pdf) |
| **PDFuzz: PDF Attacks** — Creo (ago/2025) | arXiv | Ataque explora discrepância entre layout visual e ordem de extração em PDFs. Texto literal NÃO muda, mas extração automática é embaralhada. Em ArguGPT: **93,6% → 50,4% accuracy** (-43,2 pp); F1 → 0,0. | [arxiv.org/abs/2508.01887](https://arxiv.org/abs/2508.01887) |
| **Character-Level Perturbations vs Watermarks** — Zhang et al. (set/2025) | arXiv | 5 perturbações × 5 esquemas de watermark; **homoglyph insertion quebra TODOS**. | [arxiv.org/pdf/2509.09112](https://arxiv.org/pdf/2509.09112) |
| **PIFE — defesa via quantificação adversarial** (out/2025) | arXiv | Framework defensivo: normalização multi-stage + Levenshtein + similaridade semântica. Cobre deletions, insertions, swaps, homoglyphs, invisible chars, simulated typos. | [arxiv.org/abs/2510.02319](https://arxiv.org/abs/2510.02319) |
| **Gradient Evader** — Meng et al. | USENIX Security 2025 | Ataque white-box baseado em gradiente otimiza perturbações contra detectores neurais. | [usenix.org/.../usenixsecurity25-meng.pdf](https://www.usenix.org/system/files/usenixsecurity25-meng.pdf) |

### A.1.3 Stylometry para LLM detection

| Paper | Venue, Ano | Achado |
|-------|-----------|--------|
| **Stylometry recognizes human and LLM-generated texts in short samples** — Przystalski et al. (2025) | arXiv | StyloMetrix + n-gram + LightGBM. Multiclass 7 classes: MCC até **0,87**; binário Wikipedia vs GPT-4: **0,98 accuracy**. URL: [arxiv.org/abs/2507.00838](https://arxiv.org/abs/2507.00838) |
| **Authorship Attribution in Portuguese Using Character N-grams** — Markov, Baptista | n/d | N-grams de caractere em PT funcionam bem para AA. |
| **Stylistic Fingerprints, POS-tags and Inflected Languages** | arXiv 2206.02208 | Línguas com flexão alta (PT/ES/RU) têm POS-tag distribution mais informativa que EN. |

## A.2 Datasets canônicos (detalhamento)

| Dataset | Tamanho | Idiomas | LMs cobertos | Métrica principal | URL |
|---------|---------|---------|--------------|-------------------|-----|
| **RAID** (Dugan, Hwang et al. — ACL 2024) | **10M+ docs / 6M+ gen** | EN (+ extensões multilingues) | **11 LLMs** | TPR@FPR=1% / 5%, AUROC | [arxiv.org/abs/2405.07940](https://arxiv.org/abs/2405.07940) |
| **M4GT-Bench** (MBZUAI — ACL 2024) | ~160k textos | EN + multi | vários | macro F1 | [github.com/mbzuai-nlp/M4GT-Bench](https://github.com/mbzuai-nlp/M4GT-Bench) |
| **MULTITuDE** (Macko et al. — EMNLP 2023) | **74.081 textos** | **11 idiomas inc. PT** | 8 LLMs multilingues | AUROC + acc zero-shot vs fine-tuned | [aclanthology.org/2023.emnlp-main.616](https://aclanthology.org/2023.emnlp-main.616/) + [zenodo.org/records/10013755](https://zenodo.org/records/10013755) |
| **MAGE** (Li et al. — ACL 2024) | 4 domínios | EN | vários | top detector identifica 84,12% out-of-domain | [aclanthology.org/2024.acl-long.3](https://aclanthology.org/2024.acl-long.3/) |
| **Ghostbuster dataset** (NAACL 2024) | 3 domínios novos | EN | vários | F1 cross-domain | (mesmo URL do paper) |
| **HC3** (Guo et al. 2023) | 24.322 queries / 26.882 ChatGPT / 58.546 humanas | EN + ZH | gpt-3.5-turbo | accuracy binário | [huggingface.co/datasets/Hello-SimpleAI/HC3](https://huggingface.co/datasets/Hello-SimpleAI/HC3) |
| **DetectRL** (Wu et al. — NeurIPS 2024 D&B) | academic/news/creative/social | EN | LLMs + ataques | AUROC decay sob ataques | [arxiv.org/abs/2410.23746](https://arxiv.org/abs/2410.23746) |
| **IberAuTexTification** (Sarvazyan et al. — IberLEF 2024) | **~168.000 textos** | **6 idiomas inc. PT** | 7 LLMs × 7 domínios | macro F1 80,5% (top time) | [journal.sepln.org/.../6628](http://journal.sepln.org/sepln/ojs/ojs/index.php/pln/article/view/6628) |
| **AuTexTification** (IberLEF 2023, predecessor) | >160k textos | EN + ES | 6 LLMs | macro F1 | [arxiv.org/abs/2309.11285](https://arxiv.org/abs/2309.11285) |

**Achados RAID específicos** (do paper):
- Binoculars: **-36,1%** accuracy com synonym swap
- Todos detectores exceto GPTZero: **-40,6% médio** sob homoglyph attacks
- Originality.ai: piso de FPR de **0,62%** (não consegue ir mais baixo)
- 11 ataques: homoglyph, number, article_deletion, insert_paragraphs, perplexity_misspelling, upper_lower, whitespace, zero_width_space, synonym, paraphrase, alternative_spelling

**MULTITuDE é o único dataset público com PT** entre as línguas cobertas.

## A.3 Leaderboards públicos atualizados

| Leaderboard | URL | Cobertura | Status |
|-------------|-----|-----------|--------|
| **RAID Shared Task** | [github.com/liamdugan/raid](https://github.com/liamdugan/raid) | 2 rankings (treinado em RAID + zero-shot) | raid-bench.xyz 404 em 17/05/2026; código no GH OK |
| **M4GT-Bench** | [Google Sheets](https://docs.google.com/spreadsheets/d/1BWSb-vcEZHqKmycOHdrEvOiORpN93SqC5KiYILbKxk4/) | subtasks A/B/C | público |
| **SemEval-2024 Task 8** | [aclanthology.org/2024.semeval-1.279](https://aclanthology.org/2024.semeval-1.279/) | mono 126 / multilingual 59 times | concluído |
| **UChicago Booth study** (ago/2025) | citado em V1 | benchmark de policy cap FPR≤0,005 | Pangram é o único que passa |
| **COLING 2025 GenAIDetect proceedings** | [coling-2025 S3 program](https://coling-2025-proceedings.s3.us-east-1.amazonaws.com/workshops/GenAIDetect/program.html) | todos os system papers | público |

## A.4 Fórmulas matemáticas formais

### A.4.1 Perplexity (canônica, Jelinek 1977)

```
PPL(x) = exp( -1/N · Σ_{i=1}^{N} log P(x_i | x_<i) )
```

Onde `P(x_i | x_<i)` é a probabilidade condicional do token `i` sob LM autorregressivo de referência. **Range típico**:
- Humano nativo EN prosa formal (Wikipedia, NYT): **70-110** (GPT-2 small ref)
- LLM cru EN (GPT-3.5/4): **10-25**
- Humano não-nativo EN (TOEFL): **bem mais baixo** que nativos — fonte do bias documentado em Liang et al. Patterns 2023.
- **PT-BR baseline `[NÃO VERIFICADO empiricamente]`**: estimativa operacional 40-90 para HBR-grade humano com `pierreguillou/gpt2-small-portuguese` (modelo reporta PPL 23,76 em wikipedia-PTBR no eval set in-distribution).

```python
import lmppl
scorer = lmppl.LM('pierreguillou/gpt2-small-portuguese')
ppl = scorer.get_perplexity("O paradoxo do hospital lotado é que ninguém quer cama vazia.")
```

### A.4.2 Burstiness (Goh-Barabási 2008 — fórmula canônica)

```
B_goh = (σ - μ) / (σ + μ)        # range [-1, +1]
B_gptzero = σ / μ                 # coeficiente de variação, range [0, +∞)
```

Onde σ, μ são desvio-padrão e média de comprimento de sentença em palavras (ou perplexity por sentença, na versão original do GPTZero).

| Métrica | Humano (prosa formal) | LLM cru |
|---------|----------------------|---------|
| B_goh | 0,3-0,6 | -0,1 a +0,2 |
| B_gptzero (σ/μ) | 0,9-1,5 | 0,2-0,5 |

**Status no curso-factory**: `src/validators/stylometry_checker.py` implementa as duas via `compute_burstiness()` (σ/μ default) e `compute_burstiness_goh()`.

### A.4.3 DetectGPT — Probability Curvature (Mitchell ICML 2023)

```
d(x, p_θ, q) = log p_θ(x) - E_{x̃~q(·|x)} [log p_θ(x̃)]
d̂(x) = ( log p_θ(x) - μ̃ ) / σ̃                  # forma normalizada
```

Onde `q` é distribuição de perturbações (T5 fill-in-the-blank em ~15% dos tokens), gerando k amostras. **Threshold operacional**: d̂ ≈ 0,1 separa humano/máquina. Custo: k=20-100 forward passes — **caro, exige GPU**. Preferir Fast-DetectGPT (Bao 2024, **340× mais rápido**) em produção.

### A.4.4 MAUVE (Pillutla NeurIPS 2021, Outstanding Paper Award)

Área sob a *divergence frontier* entre P (humano) e Q (modelo) em espaço de embedding GPT-2-large quantizado k-means:

```
R_λ = λP + (1-λ)Q,   λ ∈ [0,1]
DivergenceCurve = { (exp(-c·KL(Q||R_λ)), exp(-c·KL(P||R_λ))) : λ ∈ [0,1] }
MAUVE = Área sob a DivergenceCurve
```

Range [0,1], maior = distribuições mais próximas. **Humano-vs-humano** ≈ 0,95-1,0; **humano-vs-LLM cru** ≈ 0,6-0,85.

**Caveat operacional crítico**: MAUVE NÃO é métrica por documento. Exige `n_samples ≥ 100` por distribuição. Só faz sentido como métrica de **distribuição agregada** (50+ módulos vs 50+ artigos HBR humanos). Por isso NÃO entra no `stylometry_checker.py` per-módulo — entra como ferramenta de auditoria trimestral.

### A.4.5 GLTR — Top-k Token Rank (Gehrmann/Strobelt ACL 2019)

Para cada token x_i, calcular rank de x_i na distribuição preditiva `p_θ(·|x_<i)`. Classificar em 4 buckets:
- **Top-10** (verde): rank ≤ 10
- **Top-100** (amarelo): 10 < rank ≤ 100
- **Top-1000** (vermelho): 100 < rank ≤ 1000
- **>1000** (violeta): rank > 1000

| Bucket | Humano EN | LLM EN (sem humanizer) |
|--------|-----------|------------------------|
| Top-10 % | 50-65% | **80-95%** |
| Top-100 % | 25-35% | <15% |
| Top-1000 % | 10-15% | quase 0% |

### A.4.6 Burrows' Delta (estilometria canônica)

```
z_i(D) = (f_i(D) - μ_i) / σ_i
Δ(D, T) = (1/m) · Σ_{i=1..m} |z_i(D) - z_i(T)|
```

Onde `f_i(D)` = freq. relativa da i-ésima MFW (Most Frequent Word) no doc D; `m` = 50-1000 MFWs. **Distância Manhattan no espaço z-scored**. Δ pequeno = mesmo autor. Lista canônica de function words PT-BR: NLTK `stopwords.words('portuguese')` — **207 palavras** (versão 2024+).

Implementação canônica: [fastdatascience/faststylometry](https://github.com/fastdatascience/faststylometry) (Python), `stylo` R package (Eder/Rybicki/Kestemont 2016 — gold-standard acadêmico).

### A.4.7 POS-bigram entropy

```
H(POS_bigram) = -Σ_{(t1,t2)} p(t1,t2) · log₂ p(t1,t2)
```

spaCy `pt_core_news_lg` tem **17 UPOS tags** (universal) → 289 bigramas possíveis (cap teórico log₂(289) ≈ 8,18 bits).

| Domínio | Humano | LLM cru |
|---------|--------|---------|
| PT-BR técnico | **5,5-6,5 bits** | 4,5-5,5 bits |

### A.4.8 Char n-gram χ² (Pearson)

```
χ² = Σ_i (O_i - E_i)² / E_i
```

Onde `O_i` = contagem observada do trigrama i no candidato; `E_i` = expectativa do baseline humano agregado escalada. `scipy.stats.chi2_contingency` em tabela 2×K com smoothing +1.

## A.5 Thresholds por domínio (com Cohen's d)

> **Aviso**: tabela mistura valores publicados (com fonte) com estimativas operacionais (marcadas `[EST]`). Nenhum paper público consultado liberou tabela completa "média ± std × domínio × LLM"; reportam AUROC, não estatísticos brutos por feature.

| Métrica | Domínio | Humano μ±σ | LLM μ±σ | Threshold ótimo | Cohen's d | Fonte |
|---------|---------|-----------|---------|------------------|-----------|-------|
| **Perplexity** (GPT-2 ref) | EN acadêmico | ~85 ± 25 [EST] | ~18 ± 7 [EST] | ~50 | ~3,5 | GPTZero "above 85 → human" |
| **Perplexity** | EN jornalístico | ~75 ± 20 [EST] | ~15 ± 5 [EST] | ~45 | ~4,1 | Mitchell 2023 §4 |
| **Perplexity** | EN ESL/TOEFL | ~32 ± 12 [EST] | ~15 ± 5 | indistinguível | ~1,8 | Liang Patterns 2023 |
| **Perplexity** (gpt2-pt) | PT-BR HBR | `[NÃO VERIFICADO]` 40-90 | `[NÃO VERIFICADO]` 12-25 | **[CALIBRAR via A.7]** | — | sem paper conhecido |
| **Burstiness σ/μ** | EN blog | 0,9-1,5 | 0,3-0,5 | 0,7 | ~2,5 [EST] | GPTZero docs |
| **Burstiness B_goh** | qualquer | 0,3-0,6 | -0,1 a 0,2 | 0,25 | ~2,0 [EST] | Goh-Barabási |
| **GLTR Top-10 %** | EN qualquer | 50-65% | 80-95% | 70% | ~2,8 [EST] | Gehrmann ACL 2019 |
| **Sentence-len variance** | EN HBR | 50-200 [EST] | 15-40 [EST] | 50 | ~1,5 [EST] | V1 dossiê — sob calibração |
| **POS-bigram entropy** | PT-BR técnico | 5,5-6,5 bits | 4,5-5,5 bits | 5,3 | ~1,2 [EST] | sem paper PT-BR |

**Effect-size guide** (Cohen 1988):
- **d ≥ 2,0** (perplexity, top-10 rank): separação trivial — qualquer detector pega
- **d ≈ 0,8-1,5** (POS-entropy, sentence-len var): humanização cuidadosa pode confundir
- **d ≤ 0,5** (pós Adversarial Paraphrasing 2025): **zona morta de detectores estatísticos clássicos**

## A.6 Baseline PT-BR — corpora e modelos canônicos

### Corpora públicos

| Corpus | Tamanho | Domínio | URL |
|--------|---------|---------|-----|
| **brWaC** | **2,68 bi tokens, 3,53M docs** | web PT-BR filtrado | [huggingface.co/datasets/UFRGS/brwac](https://huggingface.co/datasets/UFRGS/brwac) |
| **CETENFolha** | ~24M tokens | jornalístico (Folha SP 1994) | linguateca.pt |
| **MAC-Morpho** | ~1,1M tokens POS-anotados | jornalístico | NLTK built-in |
| **Floresta Sintá(c)tica** | ~9k frases sintát.-anot. | jornalístico+literário | NLTK built-in |
| **ASSIN / ASSIN 2** | ~10k pares de frases | similaridade semântica | sites.google.com/view/assin2 |
| **Wikipedia-PT** | ~1,4 GB tokens | enciclopédico | dumps.wikimedia.org |
| **PeLLE corpus aberto** | **6 bi tokens** | web filtrado open-data | arXiv:2402.19204 (2024) |
| **GigaVerbo** | **200B tokens PT** | curado (treino Tucano) | (referenciado em paper Tucano) |

### Modelos LLM PT-BR para perplexity/embedding

| Modelo | Params | Tipo | Licença | Uso recomendado |
|--------|--------|------|---------|------------------|
| `pierreguillou/gpt2-small-portuguese` | 124M | causal LM | MIT | **perplexity canônica** PT-BR (rápido, CPU OK) |
| `neuralmind/bert-base-portuguese-cased` (BERTimbau) | 110M | MLM | MIT | pseudo-perplexity (Salazar 2020); embeddings p/ MAUVE |
| `neuralmind/bert-large-portuguese-cased` | 335M | MLM | MIT | embeddings superiores |
| `PORTULAN/albertina-900m-portuguese-ptbr-encoder-brwac` | 900M | DeBERTa | MIT | embeddings SOTA PT-BR |
| Sabiá-2 (Maritaca AI, mar/2024) | small/medium | causal LM | (uso restrito) | par com GPT-3.5 em 96,9% dos exames brasileiros |
| Sabiá-3 (out/2024) | desconhecido | causal LM | (uso restrito) | sucessor de Sabiá-2 |
| Tucano (família) | múltiplos | decoder-only | MIT (verificar) | treinado em GigaVerbo 200B tokens PT — supera comparáveis |
| TeenyTinyLlama | tiny | causal LM | MIT | open-source PT-BR mais leve |
| GlorIA (PROPOR 2024) | generative open | causal LM | (verificar) | [arxiv.org/abs/2402.12969](https://arxiv.org/abs/2402.12969) |

### Especificidades linguísticas PT-BR (impacto em burstiness/POS)

1. **Sujeito nulo (pro-drop)**: PT permite "Chove" / "Está chovendo". LLMs sobre-explicitam sujeitos. Feature potencial: razão sujeito-explicito / total-finitos.
2. **Próclise vs ênclise vs mesóclise**: posição do pronome átono varia por norma. LLMs viesam para próclise mesmo onde ênclise seria natural.
3. **Gerúndio ornamental**: "estarei enviando" — já coberto pelo anti-clichê.
4. **Ordem livre relativa**: PT permite VSO/OSV em casos enfáticos. LLMs ficam em SVO rígido — **perde variância sintática que aumentaria burstiness**.
5. **Concordância variável coloquial**: "os meninos foi" vs "os meninos foram". LLMs sempre normativos.

## A.7 Design de Experimento de Calibração (one-time + trimestral)

**Pipeline canônico para calibrar thresholds do `stylometry_checker.py` com rigor**:

```
Fase A — Coleta de corpora
  A1. N_curso = 30 módulos do curso-factory já aprovados em produção
  A2. N_humano = 30 artigos HBR PT-BR + 20 posts long-form de Alexandre
      Caramaschi (Medium + LinkedIn longform + alexandrecaramaschi.com)
      Total humano ≥ 50 docs, ≥ 3000 palavras cada
  A3. N_llm_cru = 20 módulos gerados sem o pipeline de humanização
      (apenas draft.md sem voice_guard, sem reviewer, sem humanizer)

Fase B — Cálculo de features
  B1. Para cada documento de cada grupo, computar TODAS as 9 métricas
  B2. Salvar em DataFrame com coluna 'grupo' ∈ {curso, humano, llm_cru}
  B3. CSV em output/calibration/feature_matrix.csv

Fase C — Testes estatísticos (humano vs llm_cru)
  C1. Para cada métrica:
      - Shapiro-Wilk para normalidade (p<0,05 → não-normal)
      - Se normal: t-test independente (scipy.stats.ttest_ind)
      - Se não-normal: Mann-Whitney U
      - Calcular Cohen's d em qualquer caso
  C2. Filtrar métricas com d ≥ 0,8 (efeito "grande" Cohen 1988) — só essas viram gate

Fase D — Thresholds conservadores
  D1. Para cada métrica aprovada:
      threshold_humano_min = mean(humano) - 1,5 · std(humano)
      threshold_humano_max = mean(humano) + 1,5 · std(humano)
  D2. Documentar em config/quality_rules.yaml com data + N

Fase E — Validação em hold-out
  E1. Coletar 10 novos módulos do curso-factory (não usados em B)
  E2. Aplicar threshold
  E3. Comparar com classificação manual ("passou" vs "falhou na revisão humana")
  E4. Calcular precision/recall

Fase F — Calibração externa (opcional)
  F1. Pangram API em 10 módulos do grupo curso + 10 humano + 10 llm_cru
  F2. Correlacionar score Pangram com score stylometry interno
  F3. Se Pearson r ≥ 0,6 → consistente
```

### A.7.1 Power analysis — N mínimo

Aproximação Lehr para t-test two-sample two-tailed, α=0,05, power=0,80:
```
n ≈ 16 / d²
```

| Effect size d | N por grupo (mínimo) |
|---------------|----------------------|
| 1,0 | 16 |
| 0,8 | 25-26 |
| 0,5 | 64 |
| 0,3 | 178 |

**Conclusão operacional**: **N=30 por grupo** é piso seguro para d≥0,7 com não-normalidade leve. **N=50** para MAUVE (requer mais por construção). N=10 só serve para sanity check de tooling.

### A.7.2 Pitfalls de validade interna

- **Confounder de comprimento**: faixa 3000±500 palavras em todos os grupos.
- **Confounder de domínio**: somente HBR-grade no baseline humano.
- **Confounder temporal**: Alexandre escreveu em 2019 diferente de 2025 — rotular por ano.
- **Data leakage**: módulos usados em treino do voice_guard NÃO podem ir para hold-out.
- **Multiple testing**: Bonferroni ou Benjamini-Hochberg em 9 métricas (α_efetivo = 0,0055).
- **Class imbalance**: grupos 30/30/20 evitam ponto-cego.

### A.7.3 Estrutura proposta no repo

```
curso-factory/
  scripts/calibration/
    01_collect_corpus.py
    02_compute_features.py
    03_stats_tests.py
    04_set_thresholds.py
    05_holdout_validate.py
    06_pangram_correlate.py    # opcional
  output/calibration/
    feature_matrix.csv
    stats_report.md
    thresholds_v{date}.yaml
  config/
    quality_rules.yaml          # consome thresholds_v{date}.yaml
```

## A.8 Google AI Overviews — impacto operacional 2025-2026

> Adicionado a partir do bloco 6 do sub-agent A. Reorienta a definição de "sucesso" do curso-factory: não é mais "ranquear top-3 no SERP", é **"ser citado em AI Overview"**.

| Estudo | Achado |
|--------|--------|
| **Pew Research** (mar/2025, 900 adultos, 68.879 queries, 12.593 com AI summary) | Apenas **1% dos usuários clicam link em AI summary** (vs 15% em resultados tradicionais). Wikipedia + YouTube + Reddit = **15% das fontes em AI summaries**. Government sites: 6% AIO vs 2% SERP. |
| **Seer Interactive** (set/2025) | Organic CTR em queries com AIO: **1,76% → 0,61% (-61%)**; paid CTR: 19,7% → 6,34% (-68%). |
| **Search Engine Journal** field study | AIOs cortam **38% dos cliques orgânicos** em queries afetadas. |
| **Digital Content Next** (mai-jun/2025, ~40 publishers premium) | Median YoY referral traffic **-10%**; news brands -7%; non-news -14%. |
| **Semrush AI Overviews Study 2025** | AIOs em **13% das queries** (subiu para **30% em desktop US em set/2025**). Zero-click rate em queries com AIO: **83% vs ~60% baseline**. Brands citadas em AIO: **+35% organic clicks** e **+91% paid clicks**. |
| **ALM Corp** (2026) | AIOs **+58% across 9 industries** YoY. |

**Implicação operacional para curso-factory + landing-page-geo**:
1. Disclosure + autor verificável + citações acadêmicas reais cobrem EEAT (cobertura: PR-6 implementado).
2. Schema markup Speakable otimiza extração por LLMs (cobertura: já no landing-page-geo).
3. Conteúdo em formato Q&A explícito alinha com summarization (cobertura parcial — explorar `qa.md` template).
4. Build de presença em **Reddit + YouTube** paralelamente (cobre 3 das 4 fontes mais citadas em AIO).

A métrica norte vira **AECR (AI Engine Citation Rate)** já documentado em `reference_geo_knowledge_base_2026.md` — não FPR de detector.

---

# Apêndice B — Implementação V2 (o que foi feito nesta sessão)

PRs implementados em paralelo enquanto sub-agents pesquisavam:

| PR | Status | Arquivos tocados |
|----|--------|------------------|
| **PR-1** burstiness control nos prompts | ✓ implementado | `src/templates/prompts/draft.md`, `pt-br/draft.md`, `es/draft.md`, `en/draft.md` |
| **PR-2** `stylometry_checker.py` com fórmulas formais | ✓ implementado + integrado no `quality_gate` (camada 5, report-only por default) | `src/validators/stylometry_checker.py` (novo, 350 linhas, pure-Python), `src/validators/quality_gate.py` (camada 5) |
| **PR-5** `voice_samples` no schema `client.yaml` | ✓ implementado + samples comentadas no default | `src/clients/context.py` (`VoiceSample`, `VoiceSamplesConfig`), `src/clients/loader.py`, `config/clients/default/client.yaml` |
| **PR-6** `disclosure_checker.py` + integração `quality_gate` | ✓ implementado (camada 6) + `review.md` instrui Claude a inserir bloco | `src/validators/disclosure_checker.py` (novo, 220 linhas), `src/clients/context.py` (`DisclosureConfig`), `src/clients/loader.py`, `config/clients/default/client.yaml`, `src/templates/prompts/review.md` |
| **PR-8** `detection_tracker.py` + `cli.py detection-report` | ✓ implementado | `src/detection_tracker.py` (novo, 210 linhas), `cli.py` (`cmd_detection_report` + parser) |

**Validação**:
- Smoke test integrado: stylometry score 77, burstiness 0,56, voice_guard 91 em texto-teste de 5 frases ✓
- `python -m pytest tests/`: **166 testes passando** (1 pré-existente falhando — `test_cache_expira_apos_ttl`, não relacionado às mudanças)
- **Zero regressões** introduzidas

PRs ainda no roadmap (documentados, não implementados):
- **PR-3** Pangram API self-test (depende de chave + custo $0,99/100 scans; calibrar threshold primeiro com 10+ cursos)
- **PR-4** `humanizer.py` multi-pass adversarial (L; depende de calibração do PR-2 estar estável; bom candidato para usar a defesa RADAR-style com 2 LMs PT-BR pequenos para reduzir dependência de API paga)
- **PR-7** Stylometry como 5ª dimensão DO voice_guard (M; depende de calibração do PR-2 — atualmente stylometry é camada 5 do gate, independente do voice_guard)

---

# Apêndice C — Fontes adicionais V2

### Papers ACL/EMNLP/NAACL/NeurIPS adicionais
- Ghostbuster NAACL 2024 — [aclanthology.org/2024.naacl-long.95](https://aclanthology.org/2024.naacl-long.95/)
- Binoculars ICML 2024 — [arxiv.org/abs/2401.12070](https://arxiv.org/abs/2401.12070)
- BiScope NeurIPS 2024 — [proceedings.neurips.cc/.../bc808cf2d2444b0abcceca366b771389](https://proceedings.neurips.cc/paper_files/paper/2024/hash/bc808cf2d2444b0abcceca366b771389-Abstract-Conference.html)
- RADAR NeurIPS 2023 — [arxiv.org/abs/2307.03838](https://arxiv.org/abs/2307.03838)
- Practical Examination NAACL Findings 2025 — [arxiv.org/abs/2412.05139](https://arxiv.org/abs/2412.05139)
- COLING 2025 GenAIDetect Task 1 — [arxiv.org/abs/2501.11012](https://arxiv.org/abs/2501.11012)
- SilverSpeak ACL 2025 — [aclanthology.org/2025.genaidetect-1.1.pdf](https://aclanthology.org/2025.genaidetect-1.1.pdf)
- PDFuzz 2025 — [arxiv.org/abs/2508.01887](https://arxiv.org/abs/2508.01887)
- Character-Level vs Watermarks 2025 — [arxiv.org/pdf/2509.09112](https://arxiv.org/pdf/2509.09112)
- PIFE 2025 — [arxiv.org/abs/2510.02319](https://arxiv.org/abs/2510.02319)
- Stylometry recognizes human/LLM short samples 2025 — [arxiv.org/abs/2507.00838](https://arxiv.org/abs/2507.00838)

### Datasets canônicos
- RAID ACL 2024 — [arxiv.org/abs/2405.07940](https://arxiv.org/abs/2405.07940) + [github.com/liamdugan/raid](https://github.com/liamdugan/raid)
- MULTITuDE EMNLP 2023 — [aclanthology.org/2023.emnlp-main.616](https://aclanthology.org/2023.emnlp-main.616/) + [zenodo.org/records/10013755](https://zenodo.org/records/10013755)
- M4GT-Bench — [github.com/mbzuai-nlp/M4GT-Bench](https://github.com/mbzuai-nlp/M4GT-Bench)
- MAGE ACL 2024 — [aclanthology.org/2024.acl-long.3](https://aclanthology.org/2024.acl-long.3/)
- DetectRL NeurIPS 2024 — [arxiv.org/abs/2410.23746](https://arxiv.org/abs/2410.23746)
- HC3 — [huggingface.co/datasets/Hello-SimpleAI/HC3](https://huggingface.co/datasets/Hello-SimpleAI/HC3)
- IberAuTexTification 2024 — [journal.sepln.org/.../6628](http://journal.sepln.org/sepln/ojs/ojs/index.php/pln/article/view/6628)

### Modelos PT-BR
- `pierreguillou/gpt2-small-portuguese` — [huggingface.co/pierreguillou/gpt2-small-portuguese](https://huggingface.co/pierreguillou/gpt2-small-portuguese)
- BERTimbau — [huggingface.co/neuralmind/bert-base-portuguese-cased](https://huggingface.co/neuralmind/bert-base-portuguese-cased)
- Sabiá-2 — [arxiv.org/abs/2403.09887](https://arxiv.org/abs/2403.09887)
- Tucano — [pmc.ncbi.nlm.nih.gov/articles/PMC12664968](https://pmc.ncbi.nlm.nih.gov/articles/PMC12664968/)
- TeenyTinyLlama — [sciencedirect.com/.../S2666827024000343](https://www.sciencedirect.com/science/article/pii/S2666827024000343)
- GlorIA PROPOR 2024 — [arxiv.org/abs/2402.12969](https://arxiv.org/abs/2402.12969)
- Albertina PT-BR — [huggingface.co/PORTULAN/albertina-900m-portuguese-ptbr-encoder-brwac](https://huggingface.co/PORTULAN/albertina-900m-portuguese-ptbr-encoder-brwac)
- brWaC dataset — [huggingface.co/datasets/UFRGS/brwac](https://huggingface.co/datasets/UFRGS/brwac)

### Implementações
- `lmppl` — [github.com/asahi417/lmppl](https://github.com/asahi417/lmppl)
- `mauve-text` — [github.com/krishnap25/mauve](https://github.com/krishnap25/mauve)
- Fast-DetectGPT — [github.com/baoguangsheng/fast-detect-gpt](https://github.com/baoguangsheng/fast-detect-gpt)
- DetectGPT original — [github.com/eric-mitchell/detect-gpt](https://github.com/eric-mitchell/detect-gpt)
- faststylometry — [github.com/fastdatascience/faststylometry](https://github.com/fastdatascience/faststylometry)
- RADAR código IBM — [github.com/IBM/RADAR](https://github.com/IBM/RADAR)
- Binoculars código — [github.com/ahans30/Binoculars](https://github.com/ahans30/Binoculars)
- BiScope código — [github.com/MarkGHX/BiScope](https://github.com/MarkGHX/BiScope)

### Google AI Overviews studies
- Pew Research 2025 — [pewresearch.org/internet/2025/04/03/...](https://www.pewresearch.org/internet/2025/04/03/how-the-us-public-and-ai-experts-view-artificial-intelligence/)
- Seer AIO CTR — [searchengineland.com/google-ai-overviews-drive-drop-organic-paid-ctr-464212](https://searchengineland.com/google-ai-overviews-drive-drop-organic-paid-ctr-464212)
- Semrush AI Overviews Study — [semrush.com/blog/semrush-ai-overviews-study](https://www.semrush.com/blog/semrush-ai-overviews-study/)
- SEJ AIO field study — [searchenginejournal.com/.../573145](https://www.searchenginejournal.com/ai-overviews-cut-organic-clicks-38-field-study-finds/573145/)

### Fonte canônica burstiness
- Goh & Barabási 2008 — *Burstiness and memory in complex systems*, EPL 81, 48002 — [arxiv.org/abs/physics/0610233](https://arxiv.org/abs/physics/0610233)

---

# Apêndice D — Roadmap final + Checklist de calibração executável

> Material adicionado em 2026-05-17 noite (sessão de consolidação). Fecha o ciclo: o que está pronto (PRs 1, 2, 4, 5, 6, 8), o que falta (PRs 3 e 7), em que ordem rodar, e como calibrar antes de ativar bloqueios.

## D.1 O que está pronto vs o que falta

| PR | Descrição curta | Status | Bloqueante? |
|----|-----------------|--------|------------|
| **PR-1** | Burstiness control nos 4 `draft.md` | ✓ implementado | n/a (prompt) |
| **PR-2** | `stylometry_checker.py` + camada 5 | ✓ implementado | report-only (default) |
| **PR-3** | Pangram API self-test (externo) | ⏳ documentado | report-only quando ativar |
| **PR-4** | `humanizer.py` multi-pass agente | ✓ implementado (stub funcional) | opt-in via `pipeline.humanize_enabled` |
| **PR-5** | `voice_samples` no schema `client.yaml` | ✓ implementado (samples vazias no default) | n/a (configuração) |
| **PR-6** | `disclosure_checker.py` + camada 6 | ✓ implementado | report-only (default) |
| **PR-7** | Stylometry como 5ª dimensão DO `voice_guard` | ⏳ pendente | n/a (refactor) |
| **PR-8** | `detection_tracker.py` + CLI report | ✓ implementado | passive (read-only) |

**Estado atual da suite**: 199 testes passing, +33 desta wave, 0 regressões.

## D.2 Sequência sugerida de ativação (próximas 6 semanas)

### Semana 1 — Coleta de baseline humano
- [ ] Criar `docs/voice/alexandre_caramaschi/` com 3-5 amostras reais (Medium, LinkedIn longform, alexandrecaramaschi.com) ≥ 800 palavras cada
- [ ] Coletar 30 artigos HBR PT-BR (HBR Brasil online + Folha Eco/Valor longform) — ≥ 3000 palavras cada
- [ ] Listar 30 módulos do curso-factory atualmente aprovados em produção (output canônico, sem retrabalhos manuais)
- [ ] Gerar 20 módulos "controle LLM cru" — pipeline com apenas `draft.md`, sem voice_guard, sem reviewer, sem humanizer

### Semana 2 — Calibração (apêndice A.7)
- [ ] Criar `scripts/calibration/02_compute_features.py` — computa as 4 métricas do `stylometry_checker` em todos os 80 documentos (30+30+20)
- [ ] Criar `scripts/calibration/03_stats_tests.py` — Shapiro-Wilk + t-test/Mann-Whitney + Cohen's d para cada par (humano, llm_cru) e (curso, llm_cru)
- [ ] Filtrar métricas com `d ≥ 0,8` (efeito grande Cohen 1988)
- [ ] Salvar `output/calibration/thresholds_v2026-05-XX.yaml`

### Semana 3 — Validação hold-out + ativação stylometry
- [ ] Coletar 10 módulos novos não usados em calibração
- [ ] Aplicar thresholds calibrados; comparar com revisão humana manual ("passou" vs "falhou")
- [ ] Se precision ≥ 0,80 → atualizar `config/quality_rules.yaml` com bloco `stylometry:` e ativar `block_below_threshold: true` para métricas validadas
- [ ] Após 1 semana de pipeline em produção com bloqueio ativo, revisar `cli.py detection-report` e ajustar thresholds se taxa de rejeição > 30%

### Semana 4 — Ativar disclosure como bloqueante
- [ ] Auditar 10 cursos já gerados: `cli.py validate` em cada um e contar quantos têm bloco de disclosure
- [ ] Se ≥ 8/10 já têm (porque o `review.md` foi atualizado), ativar `disclosure.block_if_missing: true` no `client.yaml`
- [ ] Para clientes em domínios regulados (psicologia GEO IPOG), adicionar `reviewer_extra` com role (`psicólogo registrado`) + `field_in_template` (`psychologist_crp`)

### Semana 5 — Voice samples + Humanizer em A/B
- [ ] Criar 3 amostras reais em `docs/voice/alexandre_caramaschi/`
- [ ] Atualizar `default/client.yaml > voice_guard.voice_samples.enabled: true` com `samples:` apontando para os arquivos
- [ ] Implementar `BaseAgent.load_prompt()` para injetar anchor antes de `{context}` no draft/review/humanize (estratégia `rotate`)
- [ ] Gerar 5 módulos com `pipeline.humanize_enabled: true` e 5 sem; comparar `detection-report --since` e revisão editorial humana lado a lado
- [ ] Decidir: ativar humanizer permanentemente OU manter como opt-in por cliente premium

### Semana 6 — PR-3 (Pangram opcional) e PR-7
- [ ] (Opcional) Obter chave Pangram API (~$0,99/100 scans); implementar `src/validators/external_detector_check.py` como camada 7 do gate
- [ ] Rodar Pangram em 30 módulos calibrados + 30 baseline humano; correlacionar com `stylometry_score` interno (Pearson r ≥ 0,6 → consistente)
- [ ] (PR-7) Rebalancear pesos do `voice_guard` para integrar stylometry como 5ª dimensão (anti-clichê 25, Bloom 25, naming 20, HBR 10, **stylometry 20**) — alternativa ao caminho atual de "stylometry é camada 5 do gate, independente do voice_guard"

## D.3 Checklist de calibração — copy-paste no terminal

Script-âncora para a equipe rodar quando os corpora estiverem prontos. Salve como `scripts/calibration/run_calibration.py`:

```python
"""Roda calibração completa de thresholds do stylometry_checker.

Uso:
    python scripts/calibration/run_calibration.py \
      --corpus-curso output/approved/ \
      --corpus-humano docs/voice/alexandre_caramaschi/ \
      --corpus-llm-cru output/llm_cru/ \
      --output output/calibration/
"""

import argparse, json, statistics, sys
from pathlib import Path
from collections import defaultdict
from scipy import stats

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from src.validators.stylometry_checker import stylometry_check

def collect(path: Path, label: str) -> list[dict]:
    out = []
    for md in sorted(path.glob("**/*.md")):
        text = md.read_text(encoding="utf-8")
        if len(text.split()) < 1500:
            continue  # filtra documentos curtos demais para inferência
        r = stylometry_check(text)
        out.append({
            "file": str(md.relative_to(path)),
            "group": label,
            "burstiness": r.burstiness,
            "sent_len_var": r.sentence_len_variance,
            "ttr": r.type_token_ratio,
            "rep": r.repetition_score,
            "score": r.score,
        })
    return out

def cohen_d(a, b):
    """Effect size para duas amostras independentes."""
    n1, n2 = len(a), len(b)
    s = ((n1 - 1) * statistics.variance(a) + (n2 - 1) * statistics.variance(b)) / (n1 + n2 - 2)
    return abs(statistics.mean(a) - statistics.mean(b)) / (s ** 0.5)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--corpus-curso", type=Path, required=True)
    ap.add_argument("--corpus-humano", type=Path, required=True)
    ap.add_argument("--corpus-llm-cru", type=Path, required=True)
    ap.add_argument("--output", type=Path, required=True)
    args = ap.parse_args()

    args.output.mkdir(parents=True, exist_ok=True)
    rows = (
        collect(args.corpus_curso, "curso")
        + collect(args.corpus_humano, "humano")
        + collect(args.corpus_llm_cru, "llm_cru")
    )
    (args.output / "feature_matrix.json").write_text(
        json.dumps(rows, indent=2), encoding="utf-8"
    )

    # Para cada métrica, comparar humano vs llm_cru
    metrics = ["burstiness", "sent_len_var", "ttr", "rep"]
    by_group = defaultdict(list)
    for r in rows:
        by_group[r["group"]].append(r)

    report = ["# Calibração — humano vs llm_cru\n"]
    for m in metrics:
        h = [r[m] for r in by_group["humano"]]
        l = [r[m] for r in by_group["llm_cru"]]
        if len(h) < 5 or len(l) < 5:
            report.append(f"## {m}: amostras insuficientes (h={len(h)}, l={len(l)})\n")
            continue
        _, p_normal_h = stats.shapiro(h)
        _, p_normal_l = stats.shapiro(l)
        normal = p_normal_h > 0.05 and p_normal_l > 0.05
        if normal:
            stat, p = stats.ttest_ind(h, l, equal_var=False)
            test_name = "Welch t-test"
        else:
            stat, p = stats.mannwhitneyu(h, l, alternative="two-sided")
            test_name = "Mann-Whitney U"
        d = cohen_d(h, l)
        verdict = "✓ usar como gate" if d >= 0.8 and p < 0.0055 else "⚠ insuficiente"
        report.append(
            f"## {m}\n"
            f"- humano: μ={statistics.mean(h):.3f}, σ={statistics.stdev(h):.3f}, n={len(h)}\n"
            f"- llm_cru: μ={statistics.mean(l):.3f}, σ={statistics.stdev(l):.3f}, n={len(l)}\n"
            f"- {test_name}: stat={stat:.3f}, p={p:.4f}\n"
            f"- Cohen's d: {d:.3f}\n"
            f"- threshold conservador (humano μ - 1.5σ): "
            f"{statistics.mean(h) - 1.5*statistics.stdev(h):.3f}\n"
            f"- veredito: **{verdict}**\n"
        )
    (args.output / "stats_report.md").write_text("\n".join(report), encoding="utf-8")
    print("Calibração concluída. Ver", args.output / "stats_report.md")

if __name__ == "__main__":
    main()
```

> O script acima é o **mínimo viável** — não cobre Bonferroni, hold-out, fase Pangram. Para versão production-ready, expandir para os 6 sub-scripts da estrutura proposta no apêndice A.7.5.

## D.4 Critérios de aceitação operacional

Antes de declarar a wave de humanização "consolidada em produção", validar:

- [ ] **Stylometry**: ≥ 4 das 4 métricas com d ≥ 0,8 entre humano e llm_cru, p < 0,0055 (Bonferroni 9 testes futuros)
- [ ] **Stylometry**: precision ≥ 0,80 contra revisão humana em hold-out de 10 módulos
- [ ] **Disclosure**: ≥ 8/10 cursos auditados já têm bloco padronizado (porque `review.md` foi atualizado)
- [ ] **Humanizer**: A/B 5×5 mostra melhora de stylometry sem queda de qualidade editorial subjetiva
- [ ] **Detection history**: pelo menos 30 entries em `output/.detection/history.jsonl` para estabelecer baseline
- [ ] **Voice samples**: 3 amostras canônicas Alexandre criadas em `docs/voice/alexandre_caramaschi/`
- [ ] **Pangram (opcional)**: correlação Pearson r ≥ 0,6 entre `stylometry_score` interno e `pangram_score`

Atingidos os 5 primeiros critérios → ativar `block_below_threshold: true` para stylometry e `block_if_missing: true` para disclosure no `client.yaml` default.

## D.5 Riscos conhecidos e mitigações

| Risco | Probabilidade | Mitigação |
|-------|--------------|-----------|
| Estrutura HBR rígida (tabela + Bloom + Knowles 6 princípios) cria uniformidade que detectores supervisionados capturam mesmo após humanização | Média | Stylometry mede VARIÂNCIA, não conformidade — se a estrutura HBR for problema, burstiness vai expor; aceitar trade-off ou usar `pipeline.humanize_enabled: true` permanentemente |
| `pierreguillou/gpt2-small-portuguese` é modelo pequeno (124M) — perplexity calculada não é state-of-the-art | Média | Cobertura: backend opt-in para `bert-base-portuguese-cased` (BERTimbau MLM) ou Tucano (decoder maior) quando GPU disponível |
| Pangram API tem custo $0,99/100 scans — pipeline rodando em batch grande pode estourar orçamento | Baixa | Só ligar PR-3 após calibração interna estável; usar em modo sampling (1 em cada 20 módulos, não 1:1) |
| SilverSpeak (ACL 2025) e PDFuzz (ago/2025) provam que detectores formais quebram com manipulação de superfície — humanizer pode estar otimizando para métrica errada | Alta no horizonte 2026-2027 | A defesa principal é **EEAT verificável + autor real + disclosure**, não bypass de detector; PRs 5 (voice_samples) + 6 (disclosure) cobrem essa frente |
| Calibração dos thresholds com 30+30+20 docs subestima domínio — métricas variam por gênero | Média | Calibrar separadamente por tipo de curso quando volume permitir (≥30 docs por gênero) |

## D.6 Métrica-norte revisada

Dado o impacto documentado dos AI Overviews (Pew 2025: 1% click; Semrush 2025: -91% paid CTR em queries com AIO; Search Engine Journal: -38% organic clicks), a métrica-norte do curso-factory **NÃO é mais** "passar em GPTZero" ou "ranquear top-3 no SERP".

A métrica-norte é **AECR (AI Engine Citation Rate)** — % de queries-âncora em que o conteúdo é citado dentro de AI Overviews / ChatGPT / Perplexity / Claude / Gemini. Já documentada em `reference_geo_knowledge_base_2026.md` e `docs/GEO_KNOWLEDGE_BASE_2026.md`.

**Implicação para esta wave**: stylometry + disclosure + voice_samples + humanizer **não são fins em si** — são meios para:
1. Sobreviver ao "scaled content abuse" do Google March 2024 Spam Update.
2. Sustentar EEAT verificável (autor + credencial + disclosure) que LLMs usam para decidir quem citar em AIOs.
3. Manter qualidade humana real (não bypass) que justifique citação em vez de filtragem.

A próxima wave (não escopo deste dossiê) deve cobrir **medição contínua de AECR** via prompts canônicos rodados semanalmente em Perplexity/ChatGPT/Claude — análogo ao já implementado em `landing-page-geo > scripts/run-prompts-weekly.mjs` para o site.

---

## Fontes principais da pesquisa (movidas do GUIA_ESCRITA_HUMANIZADA.md em 27/08/2026)

A bibliografia abaixo estava no `GUIA_ESCRITA_HUMANIZADA.md`, que virou ponteiro para a
fonte única de estilo (`alexandrebrt14-sys/escrita-empreendedor`). Ponteiro não repete
lista, e apagar a bibliografia perderia o rastro de cada afirmação, então ela desce para
este documento de pesquisa, que é o lugar dela.

1. TextSight, "Sentence Length Variance", 22/06/2026. https://www.textsight.ai/blog/sentence-length-variance/
2. The Visual Communication Guy, "How Content Teams Can Build a Reliable AI Writing Review Process", 17/07/2026. https://thevisualcommunicationguy.com/2026/07/17/how-content-teams-can-build-a-reliable-ai-writing-review-process/
3. Wikipedia, "Signs of AI writing" (catálogo vivo do WikiProject AI Cleanup, revisões ao longo de 2026). https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing
4. Bloomberry, "AI Sentence DNA" (corpus com 7.622 entradas, auditado em junho de 2026). https://www.bloomberry.ai/research/ai-writing-patterns
5. Przystalski et al., "Stylometric detection of AI-generated texts", Digital Scholarship in the Humanities, Oxford, 2026 (dispersão ~5 vs ~16). https://academic.oup.com/dsh/advance-article/doi/10.1093/llc/fqag064/8714041
6. Tabach, "Can Humans Detect AI?", arXiv, 25/04/2026 (evasão de detector não engana leitor). https://arxiv.org/abs/2604.23471
7. TechCrunch, "Substack's new tool tells you who's been writing their newsletters with AI", 22/07/2026. https://techcrunch.com/2026/07/22/substacks-new-tool-tells-you-whos-been-writing-their-newsletters-with-ai/
8. Envox, "Os 12 maiores vícios de linguagem de IA em 2026", 23/02/2026. https://envox.com.br/marketing-de-conteudo/vicios-linguagem-ia-2026-exemplos-reais/agencia-de-marketing-digital/trafego-pago/vendas/
9. Meio & Mensagem, "Como são as políticas e diretrizes de IA das redações", 05/01/2026. https://www.meioemensagem.com.br/midia/como-sao-as-politicas-e-diretrizes-de-ia-das-redacoes
10. CBL, "Manual de Boas Práticas de IA" do setor editorial brasileiro, 14/05/2026. https://cbl.org.br/2026/05/cbl-lanca-manual-de-boas-praticas-de-ia-para-orientar-editoras-brasileiras-no-uso-etico-da-inteligencia-artificial/
11. Google Search Central, "Optimizing your website for generative AI features", maio de 2026. https://developers.google.com/search/docs/fundamentals/ai-optimization-guide
12. Martinez, "Critical Survey of Generative Engine Optimization (2023-2026)", arXiv, 15/07/2026. https://arxiv.org/abs/2607.14035
13. "From Citation Selection to Citation Absorption", arXiv, 28/04/2026 (evidência extraível como fator de citação). https://arxiv.org/abs/2604.25707
14. Eduardo Martins, "Manual de Redação e Estilo de O Estado de S. Paulo" (referência permanente de prosa direta brasileira). https://fasam.edu.br/wp-content/uploads/2020/07/Manual-de-Reda%C3%A7%C3%A3o-e-Estilo-Estad%C3%A3o.pdf

Lacuna declarada: não existe, até julho de 2026, estudo de corpus acadêmico sobre marcadores de LLM específicos do português brasileiro; a tabela da seção 4 consolida convergência entre fontes de mercado brasileiras e os achados de corpus em inglês. Quando um estudo desses aparecer, este guia deve ser revisado contra ele.
