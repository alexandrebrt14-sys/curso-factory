---
titulo: Papers — Bloco 2 — RAG, Knowledge Graphs e Dados Estruturados
versao: 1.0
data: 2026-04-25
tipo: catalogo-papers
escopo: 6 papers de infraestrutura
---

# Papers — Bloco 2 — RAG, Knowledge Graphs e Dados Estruturados

Seis papers que definem a infraestrutura de descoberta agêntica: como o conteúdo é recuperado, quando KG ajuda (e quando atrapalha), como expor dados estruturados e quais formatos machine-readable os agentes preferem.

---

## #10 — A-RAG: Scaling Agentic Retrieval-Augmented Generation via Hierarchical Retrieval Interfaces

- **Autores:** Chiwei Zhu et al.
- **arXiv:** [2602.03442](https://arxiv.org/abs/2602.03442) — fevereiro 2026

**Contribuição-chave.** Framework de RAG agêntico que expõe **três ferramentas hierárquicas**:

- `keyword_search` — busca léxica.
- `semantic_search` — busca por embeddings.
- `chunk_read` — leitura de chunk específico.

O agente decide adaptativamente granularidade e número de iterações. Em múltiplos benchmarks open-domain, supera consistentemente paradigmas one-shot e workflows fixos com **menor consumo de tokens**, revelando *test-time scaling laws* para RAG.

**Por que importa.** Define como agentes comerciais devem orquestrar retrieval — implica que conteúdo precisa ser indexável simultaneamente por keyword, semântica e chunk.

**Aplicação no `curso-factory`.** Justifica a Instrução 30 (test-time scaling laws aplicados ao próprio conteúdo).

---

## #11 — When to Use Graphs in RAG (GraphRAG-Bench)

- **Autores:** Zhishang Xiang, Chuanjie Wu, Qinggang Zhang, Shengyuan Chen, Zijin Hong, Xiao Huang, Jinsong Su
- **Venue:** ICLR 2026 (aceito)
- **arXiv:** [2506.05690](https://arxiv.org/abs/2506.05690) — junho 2025

**Contribuição-chave.** Primeiro benchmark abrangente de GraphRAG, comparando RAG vetorial contra **HippoRAG, GFM-RAG, ToG, KGP, DALK, LightRAG, GraphRAG e G-Retriever**. Achados críticos:

- GraphRAG e HippoRAG **melhoram significativamente** o GPT-4o-mini em multi-hop QA.
- Mas **alguns métodos KG DEGRADAM o LLM** por excesso de ruído.
- Quantifica indexing time, latência de retrieval e accuracy de geração.

**Por que importa.** Evidência empírica para decidir **quando** investir em entity graphs Wikidata-linked versus apenas embeddings.

**Aplicação no `curso-factory`.** Justifica a Instrução 10 (calibrar KG) e o Princípio Mestre 7 (calibragem sobre maximalismo).

---

## #12 — Grounding LLM Reasoning with Knowledge Graphs

- **Autores:** Alfonso Amayuelas, Joy Sain, Simerjot Kaur, Charese Smiley
- **arXiv:** [2502.13247](https://arxiv.org/abs/2502.13247) — fevereiro 2025 (v3 dezembro 2025)

**Contribuição-chave.** Integra cada passo de reasoning (CoT, ToT, GoT) a triplas de Knowledge Graphs, transformando "thoughts" em **traços auditáveis**. No benchmark GRBench, reporta:

- **≥ 26,5% de melhoria sobre baselines CoT** em accuracy.
- Análise de profundidade, branching e tamanho de modelo afetando *faithfulness*.

**Por que importa.** Justifica investimento em KGs/Schema.org como **camada anti-hallucination** para conteúdo a ser citado.

**Aplicação no `curso-factory`.** Justifica a Instrução 3 (Schema.org com Wikidata via `sameAs`) e a Instrução 17 (densidade de entidades 1/100 palavras com 30% linkadas).

---

## #13 — LLM4Schema.org: Generating Schema.org Markups With Large Language Models

- **Autores:** Minh-Hoang Dang, Thi Hoang Thi Pham, Pascal Molli, Hala Skaf-Molli, Alban Gaignard
- **Venue:** Semantic Web Journal (Sage), 2025
- **DOI:** [10.1177/22104968251382172](https://journals.sagepub.com/doi/10.1177/22104968251382172)

**Contribuição-chave.** Aborda o fato de que **~75% das páginas web não têm markup Schema.org** e propõe pipeline LLM com prompt engineering e validação SHACL para gerar JSON-LD válido. Avalia em domínios de turismo/Wikidata e quantifica:

- Precisão de geração de triplas RDF.
- Cobertura de propriedades versus baselines manuais.

**Por que importa.** Operacionaliza produção em escala de structured data, **pré-requisito para legibilidade por agentes comerciais**.

**Aplicação no `curso-factory`.** Justifica a Instrução 2 (Schema.org não-negociável) e a Instrução 3 (SHACL automática).

---

## #14 — Readme_AI: Dynamic Context Construction for Large Language Models

- **Autores:** Pedro Antonio Tabasco Ribeiro, Brian Cloteaux et al. (NIST)
- **arXiv:** [2509.19322](https://arxiv.org/abs/2509.19322) — setembro 2025

**Contribuição-chave.** Propõe especificação machine-readable (`Readme_AI.json`) e implementação em MCP (FastMCP) para construção dinâmica de contexto a partir de fontes web. Posiciona-se como **alternativa estruturada ao `llms.txt`** e Context7. Discute trade-offs entre:

- Markdown estático (`llms.txt`).
- JSON dinâmico com tags e schemas validáveis (`readme_ai.json`).

**Por que importa.** Uma das primeiras publicações acadêmicas formais (NIST, governo) tratando do espaço `llms.txt` — relevante para **padronização** de afordâncias para agentes.

**Aplicação no `curso-factory`.** Justifica a Instrução 4 (publicar `llms.txt` E `readme_ai.json`).

---

## #15 — The MATRIX Ontology: Semantic Memory for Multi-agent Experience Transfer

- **Autores:** Ekaterina Artemova et al.
- **Venue:** CAiSE 2025 Workshops, **Springer LNBIP vol. 556**
- **DOI:** [10.1007/978-3-031-94931-9_8](https://link.springer.com/chapter/10.1007/978-3-031-94931-9_8)

**Contribuição-chave.** Modelo de memória baseado em **grafos RDF compartilháveis** entre agentes RL (neurais) e agentes LLM (simbólicos). Provê:

- **Interoperabilidade** entre arquiteturas heterogêneas.
- **Explicabilidade** auditável.
- **Transferência de experiência** long-term.

Define ontologia formal para *working memory* e *long-term memory* de equipes multi-agente, unificando camadas neural e simbólica em RDF.

**Por que importa.** Apresenta linked data como **infraestrutura de memória persistente e auditável** — crítico para comércio agêntico onde rastreabilidade é requisito regulatório.

**Aplicação no `curso-factory`.** Justifica a Instrução 9 (entity solidification via RDF + `sameAs`) e o Princípio Mestre 6 (solidificação ao longo de TODO o grafo digital).

---

## Paper bonus — Volpini et al. (Structured Linked Data / `llms.txt`)

- **Autores:** equipe WordLift
- **arXiv:** referência truncada nas screenshots originais como `arXiv:2603` — ID completo a confirmar

**Contribuição-chave.** Demonstra ganho de **+29,6% em acurácia de RAG** quando páginas de entidade incluem instruções estilo `llms.txt`. Contraste:

- **Agentic RAG (configuração C5):** 4,40
- **RAG padrão (configuração C2):** 3,89
- **Δ = +0,50, t = -5,22** (estatisticamente significativo).

**Por que importa.** Evidência empírica direta para a Instrução 4 (`llms.txt` não é cosmético, é infraestrutura).

**Aplicação no `curso-factory`.** Citado como racional do Princípio Mestre 2 (estrutura validável vence prosa eloquente).

---

## Sumário do Bloco 2

| # | Paper | Achado central | Justifica instrução(ões) |
|---|---|---|---|
| 10 | A-RAG | Test-time scaling laws com 3 interfaces hierárquicas | 30 |
| 11 | GraphRAG-Bench | Alguns métodos KG DEGRADAM LLM (calibragem obrigatória) | 10 |
| 12 | Grounding KG Reasoning | +26,5% acurácia com triplas KG | 3, 17 |
| 13 | LLM4Schema.org | 75% das páginas sem schema (janela competitiva) | 2, 3 |
| 14 | Readme_AI | NIST formaliza alternativa JSON ao llms.txt | 4 |
| 15 | MATRIX Ontology | RDF como memória cross-agente auditável | 9 |
| Bonus | Volpini et al. | +29,6% RAG com llms.txt | 4 |
