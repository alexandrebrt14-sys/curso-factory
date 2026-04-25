# Base de Conhecimento — GEO, AEO e Comércio Agêntico

**Curador:** Alexandre Caramaschi — CEO da Brasil GEO, ex-CMO da Semantix (Nasdaq), cofundador da AI Brasil.
**Versão:** 1.0 (2026-04-25)
**Idioma:** Português do Brasil com acentuação completa.
**Escopo:** Sintetiza 25+ papers acadêmicos e relatórios de mercado (2025–2026) em diretivas operacionais, checklists e princípios mestres prontos para guiar a produção editorial do `curso-factory`.

---

## Por que este corpus existe

Esta base de conhecimento consolida o estado da arte em **Generative Engine Optimization (GEO)**, **Answer Engine Optimization (AEO)** e **Comércio Agêntico** entre janeiro de 2025 e abril de 2026. Toda decisão editorial, todo prompt, todo módulo de curso e todo artigo do ecossistema Brasil GEO deve se ancorar aqui — em vez de em folclore de marketing ou táticas anedóticas.

A literatura empírica do período produz uma reorientação estratégica que precisa ser internalizada antes de qualquer execução: **muitas táticas "GEO-puras" são ineficazes ou se anulam em equilíbrio competitivo**, enquanto fundamentos clássicos — autoridade de domínio, mídia conquistada, presença em comunidades como Reddit — explicam a maior parte da variância de citação por LLMs. O debate "GEO vs. SEO" foi superado pelo *stack* "**SEO + entity graph + agent legibility**".

---

## Como usar este conhecimento

1. **Para auditar uma página existente** → comece por `30-checklist-auditoria-geo16.md` e use os limiares de `40-thresholds-quantitativos.md` como gates.
2. **Para reescrever ou gerar conteúdo novo** → siga `31-checklist-reescrita.md` (TL;DR + BLUF + Corpo + Síntese) e adapte por plataforma com `32-checklist-publicacao-multi.md`.
3. **Para preparar produtos para agentes** → `33-checklist-agent-legibility.md` cobre JSON-LD, MCP, AP2/UCP e o nível 4+ da curva McKinsey.
4. **Para entender o porquê** → leia primeiro `00-principios-mestres.md` e depois aprofunde nos papers.

---

## Índice

### Núcleo doutrinário

- [00-principios-mestres.md](00-principios-mestres.md) — **Os 7 princípios mestres** que sintetizam toda a base. Reler a cada ciclo trimestral.
- [01-anti-patterns.md](01-anti-patterns.md) — **O que evitar**: 14 anti-patterns consolidados do manual e dos papers.
- [02-glossario.md](02-glossario.md) — Glossário técnico: GEO, AEO, RAG, KG, MCP, A2A, ANP, AP2/UCP, JSON-LD, SHACL, VLM, *agent legibility*.

### Manual operacional — 30 instruções

- [10-manual-parte-1-auditoria.md](10-manual-parte-1-auditoria.md) — **Auditoria técnica e estrutural** (Instruções 1–10): GEO-16, Schema.org/SHACL, `llms.txt`, HTML semântico, blocos AEO, citações, *entity solidification*, KG calibrado.
- [11-manual-parte-2-descoberta.md](11-manual-parte-2-descoberta.md) — **Descoberta, autoridade e dinâmica competitiva** (Instruções 11–15): mídia conquistada, top-20 de fontes, otimização multi-engine, jogo de soma zero, *sentiment integrity*.
- [12-manual-parte-3-reescrita.md](12-manual-parte-3-reescrita.md) — **Reescrita e geração de conteúdo longo** (Instruções 16–25): estrutura TL;DR/BLUF, densidade de entidades, normas por plataforma (Medium/Quora/LinkedIn/Substack), negrito estratégico, anti-alucinação.
- [13-manual-parte-4-agentic.md](13-manual-parte-4-agentic.md) — **Comércio agêntico e infraestrutura** (Instruções 26–30): nível 4+ McKinsey, *anti-signals*, MCP→ACP→A2A→ANP, *agent legibility* como camada de produto, *test-time scaling*.

### Catálogo de papers

- [20-papers-bloco-1-geo-aeo.md](20-papers-bloco-1-geo-aeo.md) — **GEO/AEO e comportamento de citação por LLMs** (9 papers): C-SEO Bench, Pinterest GEO, News Source Citing, Source Coverage, Discovery Gap, MAGEO, CC-GSEO-Bench, AutoGEO, Role-Augmented Intent.
- [21-papers-bloco-2-rag-kg.md](21-papers-bloco-2-rag-kg.md) — **RAG, knowledge graphs e dados estruturados** (6 papers): A-RAG, GraphRAG-Bench, Grounding LLM Reasoning with KGs, LLM4Schema.org, Readme_AI, MATRIX Ontology.
- [22-papers-bloco-3-agentic.md](22-papers-bloco-3-agentic.md) — **Comércio agêntico, MCP e protocolos** (5 papers): What Is Your AI Agent Buying?, MCP Landscape & Security, Agent Interoperability Survey, Agentic Web, Agentic Commerce Survey.

### Checklists operacionais

- [30-checklist-auditoria-geo16.md](30-checklist-auditoria-geo16.md) — Os 16 pilares + gates de aprovação (G≥0,70 e ≥12 pilares acionados).
- [31-checklist-reescrita.md](31-checklist-reescrita.md) — Template editorial reutilizável e densidade de entidades.
- [32-checklist-publicacao-multi.md](32-checklist-publicacao-multi.md) — Matriz por plataforma (Medium, Quora, LinkedIn Newsletter, Substack).
- [33-checklist-agent-legibility.md](33-checklist-agent-legibility.md) — JSON-LD `Product`, endpoint MCP, *anti-signals* a remover.

### Referência rápida

- [40-thresholds-quantitativos.md](40-thresholds-quantitativos.md) — **Todos os limiares numéricos** consolidados em uma única tabela: G≥0,70, +29,6% RAG, 67,3% top-20, +26,5% KG-grounded, 78% citação cross-engine, 30:1 *discovery gap*, etc.
- [50-fontes-e-links.md](50-fontes-e-links.md) — Lista canônica de URLs (arXiv, DOI, Springer, Sage, NIST, McKinsey) com identificadores corrigidos.

---

## Como esta base se conecta ao `curso-factory`

O `curso-factory` é a fábrica de cursos do ecossistema Brasil GEO (cliente `default`). Seus 5 LLMs (Perplexity, GPT-4o, Gemini, Groq, Claude) operam sob padrão editorial HSM/HBR/MIT Sloan e validação em 5 camadas (acentos, conteúdo, links, HTML, FinOps).

Esta base de conhecimento é o **layer doutrinário** que orienta:

1. **Pesquisa (Perplexity)** → as fontes-âncora aceitas estão em `50-fontes-e-links.md`. Toda afirmação factual deve casar com pelo menos um paper deste catálogo.
2. **Redação (GPT-4o)** → os princípios de `00-principios-mestres.md`, a estrutura de `31-checklist-reescrita.md` e a densidade de entidades (1 a cada 100 palavras) são requisitos obrigatórios.
3. **Análise (Gemini)** → deve verificar os 16 pilares de `30-checklist-auditoria-geo16.md` em cada módulo gerado.
4. **Classificação (Groq)** → tags devem incluir os termos canônicos do glossário (`02-glossario.md`).
5. **Revisão (Claude)** → varredura final contra `01-anti-patterns.md` antes da aprovação.

Cursos que abordam temas de GEO, AEO, marketing por IA ou comércio agêntico devem usar este corpus como fonte primária. Onde a literatura conflitar, prevalece a regra de **otimização multi-engine ponderada** descrita na Instrução 13.

---

## Convenções de manutenção

- **Frequência de revisão:** trimestral. Atualizar limiares quantitativos quando novos papers do corpus forem incorporados.
- **Quando adicionar um paper:** ele deve aparecer em (a) `2X-papers-bloco-*.md` com contribuição-chave, (b) `40-thresholds-quantitativos.md` se trouxer dado numérico novo, e (c) `50-fontes-e-links.md` com URL canônica verificada.
- **Quando criar uma nova diretiva:** registrar em `1X-manual-parte-*.md` seguindo o formato DIRETIVA → RACIONAL → PSEUDOCÓDIGO/CHECKLIST.
- **Anti-patterns** são adicionados em `01-anti-patterns.md` somente quando há evidência empírica de degradação (não opinião editorial).

---

## Tese central em uma frase

**GEO técnico é necessário, não suficiente. Estrutura validável (Schema.org + SHACL + Wikidata + `llms.txt`) vence prosa eloquente. Mídia conquistada explica a maior parte da variância de citação. *Agent legibility* é a nova SEO.**
