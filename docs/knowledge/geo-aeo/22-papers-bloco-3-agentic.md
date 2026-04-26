---
titulo: Papers — Bloco 3 — Comércio Agêntico, MCP e Protocolos
versao: 1.0
data: 2026-04-25
tipo: catalogo-papers
escopo: 5 papers de infraestrutura agêntica
---

# Papers — Bloco 3 — Comércio Agêntico, MCP e Protocolos de Pagamento

Cinco papers que definem o horizonte 2026–2027 de comércio agêntico. Em conjunto com a Parte 4 do manual operacional, formam o argumento para tratar *agent legibility* como camada de produto e adotar a *stack* MCP → ACP → A2A → ANP em sequência.

---

## #16 — What Is Your AI Agent Buying? Evaluation, Implications and Emerging Questions for Agentic E-Commerce

- **Autores:** Amine Allouah, Omar Besbes, Josué D. Figueroa, Yash Kanoria, Akshit Kumar (**Columbia Business School / Microsoft**)
- **arXiv:** [2508.02630](https://arxiv.org/abs/2508.02630) — agosto 2025 (v3 dezembro 2025)

**Contribuição-chave.** Constrói o **ACES (Agentic e-Commerce Simulator)**, sandbox provider-agnóstico, e roda experimentos randomizados com:

- Claude Sonnet, Claude Opus
- GPT-4.1, GPT-5.1
- Gemini 2.5 Pro, Gemini 3.0 Pro

Descobertas causais:

- Agentes exibem **vieses de posição heterogêneos** (variação grande entre modelos).
- **PENALIZAM** tags "sponsored".
- **RECOMPENSAM** *endorsements* de plataforma.
- **Concentram demanda em poucos produtos modais**.
- Sellers podem **ganhar share substancial** otimizando descrições para preferências de agentes.

**Por que importa.** Evidência causal fundacional para qualquer estratégia de "agent legibility" em e-commerce.

**Aplicação no `curso-factory`.** Justifica a Instrução 27 (anti-signals "sponsored") e o anti-pattern A3.

---

## #17 — Model Context Protocol (MCP): Landscape, Security Threats, and Future Research Directions

- **Autores:** Xinyi Hou, Yanjie Zhao, Shenao Wang, Haoyu Wang (Huazhong University of Science and Technology)
- **arXiv:** [2503.23278](https://arxiv.org/abs/2503.23278) — março 2025 (v3 outubro 2025)

**Contribuição-chave.** Primeira análise acadêmica sistemática do ecossistema MCP. Estrutura:

- **Lifecycle do MCP server em 4 fases e 16 atividades**.
- **Taxonomia de ameaças cobrindo 4 tipos de atacantes**.
- Case studies de **OpenAI Agents SDK, Cursor, Claude Desktop**.
- Análise de adoção por **OpenAI, Cloudflare, Stripe, Block, Baidu**.

**Por que importa.** Paper fundacional de MCP como camada de tools — **pré-condição para qualquer integração entre LLMs e backends de comércio**.

**Aplicação no `curso-factory`.** Justifica a Instrução 28 (stack MCP → A2A → ANP) com metodologia de *threat model* concreta.

---

## #18 — A Survey of Agent Interoperability Protocols: MCP, ACP, A2A, and ANP

- **Autores:** Abul Ehtesham, Aditi Singh, Gaurav Kumar Gupta, Saket Kumar
- **arXiv:** [2505.02279](https://arxiv.org/abs/2505.02279) — maio 2025

**Contribuição-chave.** Compara os quatro protocolos emergentes em quatro dimensões:

| Dimensão | MCP | ACP | A2A | ANP |
|---|---|---|---|---|
| Modo de interação | tools | mensageria multimodal | execução colaborativa | marketplaces descentralizados |
| Discovery | servidor → cliente | broadcast | rendezvous | DHT |
| Padrão de comunicação | RPC | pub/sub | task delegation | network protocol |
| Modelo de segurança | OAuth | mTLS | identidade verificada | criptografia ponta-a-ponta |

Propõe **roadmap de adoção em fases**: **MCP → ACP → A2A → ANP**, conectando acesso a tools, mensageria multimodal, execução colaborativa e marketplaces descentralizados.

**Por que importa.** Mapeia formalmente onde UCP/AP2 se encaixam — **base teórica para arquitetura de comércio agente-a-agente**.

**Aplicação no `curso-factory`.** Justifica a sequência de adoção da Instrução 28.

---

## #19 — Agentic Web: Weaving the Next Web with AI Agents

- **Autores:** Yingxuan Yang, Mulei Ma, …, Pieter Abbeel, **Dawn Song**, Weinan Zhang, Jun Wang (UC Berkeley, SJTU et al., **18 autores**)
- **arXiv:** [2507.21206](https://arxiv.org/abs/2507.21206) — julho 2025

**Contribuição-chave.** Framework conceitual da **Agentic Web em três dimensões**:

1. **Inteligência** — IR, recomendação, planejamento, multi-agent learning.
2. **Interação** — protocolos de comunicação.
3. **Economia** — paradigma da **"Agent Attention Economy"**.

Aplicações em e-commerce ordering e travel planning. Autoria de peso (Berkeley/Dawn Song/Pieter Abbeel) confere referência canônica.

**Por que importa.** **Mapa conceitual** que situa GEO e payments como aplicações dentro de um framework arquitetônico maior.

**Aplicação no `curso-factory`.** Justifica a Instrução 29 (agent legibility como camada de produto) com framework teórico que articula as três dimensões.

---

## #20 — Agentic Commerce: A Survey of How AI Agents Are Reshaping Commerce

- **Autores:** Yifei Zhang, Bo Pan, Mengdan Zhu et al.
- **Venue:** TechRxiv (IEEE preprint), janeiro 2026
- **DOI:** [10.36227/techrxiv.176972193.39211542/v1](https://www.techrxiv.org/doi/full/10.36227/techrxiv.176972193.39211542/v1)

**Contribuição-chave.** Primeira survey sistemática de A-Commerce com:

- **Taxonomia lifecycle-based e agent-role-centric**.
- Formaliza comércio agêntico como **multi-agent setting**.
- Analisa papéis: **buyer, seller, marketplace agents** ao longo do ciclo.
- Examina ambientes online, hybrid online-to-offline e fisicamente situados.
- Revisa arquiteturas, protocolos (MCP, A2A, AP2), padrões de implementação e benchmarks.

**Por que importa.** Paper "guarda-chuva" que sistematiza o campo e ancora **onde GEO se posiciona** — interface entre seller agent layer e buyer agent visibility.

**Aplicação no `curso-factory`.** Fornece o vocabulário taxonômico para todos os cursos sobre comércio agêntico.

---

## Síntese estratégica do Bloco 3

Para um C-level com tempo limitado, a sequência de leitura recomendada é:

1. **#16 What Is Your AI Agent Buying?** — evidência causal para a estratégia de descrição de produto.
2. **#18 Agent Interoperability Survey** — mapa do roadmap MCP → ACP → A2A → ANP.
3. **#17 MCP Landscape & Security** — implementação concreta com *threat model*.
4. **#19 Agentic Web** — framework conceitual de validação.
5. **#20 Agentic Commerce Survey** — taxonomia integrada.

---

## Insights agregados merecem atenção de board

- **Primeiro:** a literatura empírica converge em que earned media, autoridade de domínio e presença em comunidades (especialmente Reddit) explicam mais variância de citação por LLM do que técnicas "GEO-puras".
- **Segundo:** há concentração crescente de autoridade — top 20 fontes capturam 67% das citações em modelos OpenAI — o que cria janela competitiva para marcas que invistam cedo em earned media especializada.
- **Terceiro:** o stack emergente (MCP + A2A + AP2/UCP) está se profissionalizando rápido, e a janela de diferenciação passa por **agent legibility**: descrições de produto otimizadas para VLMs, structured data validável e KGs próprios linkados a Wikidata.

---

## Lacuna de pesquisa relevante

Não há estudos longitudinais (≥ 12 meses) sobre estabilidade das estratégias GEO frente a updates de modelos. Todas as métricas quantitativas atuais são *snapshots*. Isso sugere:

1. Cautela ao tratar quaisquer "rankings GEO" como duráveis.
2. Investir em **ativos estruturais** (entity graph, brand mentions em earned media, presença em corpus de treinamento) em vez de táticas prompt-level específicas.

---

## Sumário do Bloco 3

| # | Paper | Achado central | Justifica instrução(ões) |
|---|---|---|---|
| 16 | What Is Your AI Agent Buying? | Agentes penalizam "sponsored", recompensam endorsements | 27 |
| 17 | MCP Landscape & Security | Lifecycle 4 fases / 16 atividades, 4 taxonomias de ameaça | 28 |
| 18 | Agent Interoperability Survey | Sequência MCP → ACP → A2A → ANP | 28 |
| 19 | Agentic Web | Framework 3 dimensões (inteligência, interação, economia) | 29 |
| 20 | Agentic Commerce Survey | Taxonomia buyer/seller/marketplace agents | 29 |
