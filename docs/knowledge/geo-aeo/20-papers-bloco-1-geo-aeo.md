---
titulo: Papers — Bloco 1 — GEO, AEO e Comportamento de Citação por LLMs
versao: 1.0
data: 2026-04-25
tipo: catalogo-papers
escopo: 9 papers fundacionais
---

# Papers — Bloco 1 — GEO, AEO e Comportamento de Citação por LLMs

Nove papers que definem o estado da arte em otimização para engines generativos. Lidos em conjunto, formam o argumento empírico da **Parte 1** e **Parte 2** do manual operacional. **Para C-level com tempo limitado, a sequência recomendada é: C-SEO Bench (#1) e Discovery Gap (#5) primeiro** — definem o que *não* funciona; depois Pinterest GEO (#2) e News Source Citing Patterns (#3) para evidência de mercado.

---

## #1 — C-SEO Bench: Does Conversational SEO Work?

- **Autores:** Haritz Puerto, Martin Gubri, Tommaso Green, Seong Joon Oh, Sangdoo Yun (Parameter Lab)
- **Venue:** NeurIPS 2025 Datasets & Benchmarks Track
- **arXiv:** [2506.11097](https://arxiv.org/abs/2506.11097) — junho 2025
- **Repo:** https://github.com/parameterlab/c-seo-bench

**Contribuição-chave.** Primeiro benchmark *peer-reviewed* de Conversational SEO em QA e recomendação de produto, em 6 domínios e múltiplos atores modelados como **jogo não-cooperativo** (adoção de 0% a 100%). Avalia 10 métodos C-SEO e mostra que:

1. A **maioria dos métodos C-SEO é ineficaz**.
2. **SEO tradicional aplicado ao contexto do LLM permanece significativamente mais efetivo**.
3. Há **dinâmica zero-sum** quando vários competidores adotam a mesma tática.

**Por que importa.** Funciona como "teste de realidade" para qualquer roadmap GEO — mostra que ganhos competitivos exigem **combinação de SEO + GEO**, não substituição.

**Aplicação no `curso-factory`.** Cursos sobre marketing por IA devem desbancar a narrativa popular de "SEO morreu, agora é só GEO". A evidência aponta para GEO como camada **adicional**.

---

## #2 — Generative Engine Optimization: A VLM and Agent Framework for Pinterest Acquisition Growth

- **Autores:** Faye Zhang, Qianyu Cheng, Jasmine Wan, Vishwakarma Singh, Jinfeng Rao, Kofi Boakye (Pinterest)
- **arXiv:** [2602.02961](https://arxiv.org/abs/2602.02961) — fevereiro 2026

**Contribuição-chave.** Único caso publicado de GEO **em produção em escala bilionária**. Combina:

- VLMs fine-tunados para *reverse search* (imagem → query).
- Agentes de mineração de tendências.
- Arquitetura two-tower ANN com sinais de autoridade.

**Resultados reportados.**

- **+20% de tráfego orgânico**.
- **+19% em alinhamento topic-query**.
- MAU adicional de milhões de usuários.

**Por que importa.** Blueprint validado de implantação industrial — referência direta para CMOs/CPOs em plataformas com inventário visual ou catálogos de produto.

**Aplicação no `curso-factory`.** Justifica a Instrução 29 (*agent legibility* como camada de produto) com evidência empírica de produção.

---

## #3 — News Source Citing Patterns in AI Search Systems

- **Equipe:** baseada no AI Search Arena dataset (LMArena/Miroyan et al.)
- **arXiv:** [2507.05301](https://arxiv.org/abs/2507.05301) — julho 2025

**Contribuição-chave.** Análise de **366.087 URLs citadas em 24.069 conversas reais** entre março e maio de 2025, cobrindo 12 modelos da OpenAI, Perplexity e Google. Achados quantitativos:

- **Top 20 fontes = 67,3% das citações em modelos OpenAI**.
- *Clustering* intra-família forte: cosseno > 0,67.
- *Clustering* cross-family fraco: cosseno < 0,33.

**Por que importa.** Fornece base empírica para alocar budget de PR/earned media **por motor**. Cada plataforma tem "gravitacionais" editoriais distintos.

**Aplicação no `curso-factory`.** Justifica a Instrução 12 (mapear top-20 por família de LLM) e a Instrução 13 (otimização multi-engine ponderada).

---

## #4 — Source Coverage and Citation Bias in LLM-based vs. Traditional Search Engines

- **Autores:** equipe acadêmica (autoria a confirmar)
- **arXiv:** [2512.09483](https://arxiv.org/abs/2512.09483) — dezembro 2025

**Contribuição-chave.** Maior comparação empírica até hoje entre 6 LLM-Search Engines e 2 buscadores tradicionais (Google, Bing): **55.936 queries, 124.287 domínios, 1.418.733 hyperlinks**. Achados:

- **37% dos domínios em LLM-SEs não aparecem em buscadores tradicionais** — reorienta percepção de overlap.
- Análise SHAP isola preditores dominantes de seleção de fonte:
  - **Tranco rank: importância 0,923**
  - **Outlinks count: importância 0,799**
  - **TLD .com: importância 0,623**

**Por que importa.** Quantifica os fatores de visibilidade em LLMs com modelagem causal — orienta priorização técnica e de PR.

**Aplicação no `curso-factory`.** Justifica a Instrução 7 (densidade de outlinks ≥ 1 a cada 250 palavras) e a recomendação geral de monitorar Tranco rank do domínio próprio.

---

## #5 — The Discovery Gap: How Product Hunt Startups Vanish in LLM Organic Discovery Queries

- **Autor:** Amit Prakash Sharma (IIT Patna)
- **arXiv:** [2601.00912](https://arxiv.org/abs/2601.00912) — janeiro 2026

**Contribuição-chave.** Testa **112 startups em 2.240 queries** contra ChatGPT (gpt-4o-mini) e Perplexity (sonar). Achados quantitativos:

- **Recognition direto:** 99,4% (ChatGPT), 94,3% (Perplexity).
- **Discovery orgânico:** 3,32% (ChatGPT), 8,29% (Perplexity).
- **Gap de 30:1** entre recognition e discovery.
- **Scores GEO NÃO correlacionam com discovery** (r ≈ 0).
- **Referring domains** correlacionam r = +0,319 com descoberta.
- **Presença em Reddit** correlaciona r = +0,395, p = 0,002.

**Por que importa.** Achado mais contraintuitivo do corpus. Desinfla o hype de GEO isolado e reforça que earned media e comunidades são **pré-requisito**, não tática auxiliar.

**Aplicação no `curso-factory`.** Justifica a Instrução 11 (mídia conquistada paralela ao GEO técnico) e o Princípio Mestre 1 (GEO técnico é necessário, não suficiente).

---

## #6 — From Experience to Skill: Multi-Agent Generative Engine Optimization (MAGEO)

- **Autores:** Beining Wu, Fuyou Mao, Jiong Lin, Cheng Yang et al.
- **Venue:** ACL 2026 Findings (aceito)
- **arXiv:** [2604.19516](https://arxiv.org/abs/2604.19516) — abril 2026

**Contribuição-chave.** Reformula GEO como problema de *skill learning* multi-agente com 4 papéis:

- **Preference** — modela preferência de cada engine.
- **Planner** — decide o que editar.
- **Editor** — executa a edição.
- **Evaluator** — mede impacto.

Introduz **Twin Branch Evaluation** para atribuição causal de edições e a métrica **DSV-CF** (visibilidade semântica + acurácia de citação). Libera o benchmark MSME-GEO-Bench, superando baselines heurísticas em 3 motores.

**Por que importa.** Move GEO de táticas pontuais para estratégias transferíveis — relevante para operações que rodam GEO em escala.

**Aplicação no `curso-factory`.** Justifica a Instrução 10 (calibrar KG via teste com/sem) — mesmo método aplicado a qualquer enriquecimento.

---

## #7 — Beyond Keywords: Driving GSEO with Content-Centric Agents (CC-GSEO-Bench)

- **Autores:** equipe acadêmica (autoria a confirmar)
- **arXiv:** [2509.05607](https://arxiv.org/abs/2509.05607) — setembro 2025

**Contribuição-chave.** Benchmark com **1.000+ artigos-fonte e 5.000+ queries** em estrutura one-to-many, com avaliação multidimensional em 5 eixos: **Exposure, Faithful Credit, Causal Impact, Readability, Trustworthiness**. Achados:

- "More Quotes" é a estratégia mais robusta:
  - Exposure: **5,769**
  - Faithful Credit: **6,328**
- "Statistics" aumenta impacto causal mas **degrada Trustworthiness**:
  - 7,613 vs baseline 8,352.

**Por que importa.** Quantifica trade-offs entre estratégias editoriais — útil para guidelines de redação corporativa em IA.

**Aplicação no `curso-factory`.** Justifica a Instrução 8 (densidade de quotes vs. estatísticas calibrada) e o Princípio Mestre 4 (quotes vencem estatísticas).

---

## #8 — AutoGEO: What Generative Search Engines Like and How to Optimize Cooperatively

- **Autores:** Yujiang Wu, Shanshan Zhong, Yubin Kim, Chenyan Xiong (Carnegie Mellon)
- **arXiv:** [2510.11438](https://arxiv.org/abs/2510.11438) — outubro 2025

**Contribuição-chave.** Extrai automaticamente regras de preferência de **Gemini, Claude e GPT** que explicam por que escolhem citar dado conteúdo. Usa as regras de duas formas:

1. **AutoGEO_API** — context engineering em produção.
2. **AutoGEO_Mini** — recompensa GRPO em fine-tuning.

Avaliado em GEO-Bench, Researchy-GEO e e-commerce a partir de LMSYS-Chat-1M, mostra ganhos consistentes de visibilidade preservando utilidade do motor.

**Por que importa.** Operacionaliza otimização *engine-específica* — base técnica para diferenciar conteúdo por motor-alvo.

**Aplicação no `curso-factory`.** Justifica a Instrução 13 (otimização multi-engine ponderada) com método empírico de extração de preferências.

---

## #9 — Role-Augmented Intent-Driven Generative Search Engine Optimization

- **Autores:** Xiaolu Chen, Haojie Wu, Jie Bao, Zhen Chen, Yong Liao, Hu Huang
- **arXiv:** [2508.11158](https://arxiv.org/abs/2508.11158) — v2 março 2026

**Contribuição-chave.** Usa intenção de busca como sinal explícito para guiar otimização em GSEs RAG-powered. Estende o dataset GEO com variações de queries e introduz **G-Eval 2.0**, rubrica em 6 níveis aumentada por LLM. Reporta melhorias significativas sobre baselines single-aspect tanto em métricas subjetivas quanto em visibilidade objetiva.

**Por que importa.** Reforça a tese de que GEO precisa modelar intenção, não apenas keywords — convergente com agentes que carregam contexto rico.

**Aplicação no `curso-factory`.** Justifica a Instrução 24 (casar intenção do usuário com framing explícito).

---

## Sumário do Bloco 1

| # | Paper | Achado central | Justifica instrução(ões) |
|---|---|---|---|
| 1 | C-SEO Bench | SEO + GEO combinados vencem; muitas táticas C-SEO são ineficazes | 14 |
| 2 | Pinterest GEO | +20% tráfego com VLM + agentes em produção | 29 |
| 3 | News Source Citing | Top 20 = 67,3% das citações OpenAI; clustering por família | 12, 13 |
| 4 | Source Coverage | Tranco 0,923 / outlinks 0,799 / .com 0,623 (SHAP) | 7 |
| 5 | Discovery Gap | Recognition 99% vs discovery 3% (gap 30:1); GEO score r≈0 | 11 |
| 6 | MAGEO | Twin Branch Evaluation para atribuição causal | 10 |
| 7 | CC-GSEO-Bench | Quotes vencem stats (Exposure 5,769 vs degrada Trust 7,613) | 8 |
| 8 | AutoGEO | Regras de preferência por engine extraídas automaticamente | 13 |
| 9 | Role-Augmented Intent | Intenção como sinal explícito (G-Eval 2.0) | 24 |
