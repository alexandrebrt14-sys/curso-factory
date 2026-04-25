---
titulo: Glossário Técnico — GEO, AEO e Comércio Agêntico
versao: 1.0
data: 2026-04-25
tipo: nucleo-doutrinario
---

# Glossário

Definições canônicas usadas em todo o corpus. Quando houver mais de uma definição corrente no mercado, esta base adota a forma indicada pelos papers acadêmicos do período 2025–2026.

---

## A

**A2A (Agent-to-Agent Protocol)** — Protocolo de comunicação entre agentes para execução colaborativa em mensageria multimodal. É o terceiro estágio da sequência de adoção MCP → ACP → A2A → ANP (arXiv:2505.02279).

**ACP (Agent Communication Protocol)** — Protocolo de mensageria multimodal entre agentes, intermediário entre MCP (acesso a tools) e A2A (execução colaborativa).

**AEO (Answer Engine Optimization)** — Otimização para *answer engines* (engines que retornam respostas diretas, não listas de links). Foco em blocos de resposta direta (40–80 palavras autocontidos) imediatamente após cada heading.

**Agent Attention Economy** — Paradigma econômico em que o ativo escasso passa a ser a atenção do agente, não do humano. Cunhado em *Agentic Web* (arXiv:2507.21206, Berkeley/Dawn Song).

**Agent Legibility** — Conjunto de características que tornam uma página, produto ou marca descritível e selecionável por agentes (VLM, LLM com tool-use, agentes comerciais). Inclui structured data validável, descrições otimizadas para VLM, KG próprio linkado a Wikidata, endpoint MCP. Tratada como **camada de produto**, não como adendo de marketing.

**ANP (Agent Network Protocol)** — Protocolo para marketplaces descentralizados de agentes. Quarto estágio da sequência de adoção (arXiv:2505.02279).

**AP2 (Agent Payment Protocol)** — Protocolo de pagamento para transações iniciadas por agentes. Frequentemente referenciado junto a UCP. Padronização em curso na Linux Foundation Agentic AI Foundation.

**arXiv** — Repositório de pre-prints da Universidade Cornell (https://arxiv.org). Identificador canônico no formato `YYMM.NNNNN` (ex.: `2509.08919`). Fonte primária aceita por todos os pilares deste corpus.

---

## B

**BLUF (Bottom Line Up Front)** — Padrão de redação militar/jornalística em que a primeira seção responde a pergunta central em 80–150 palavras autocontidos. Combinado com TL;DR no topo, forma a estrutura padrão de reescrita (Instrução 16).

**Brave Summary** — Engine de resposta gerativa do Brave Search. No GEO-16, é o engine mais exigente em score de pilar (preferência por G = 0,727).

---

## C

**C-SEO (Conversational SEO)** — Categoria geral de táticas de otimização para engines conversacionais. C-SEO Bench (arXiv:2506.11097, NeurIPS 2025) demonstra que muitas táticas C-SEO isoladas são ineficazes ou se anulam em equilíbrio competitivo.

**Chunk Read** — Uma das três interfaces hierárquicas de recuperação descritas em A-RAG (arXiv:2602.03442). Operação que extrai um trecho contínuo de uma página para inclusão em contexto.

**Clean Recommendations** — Sinal que LLMs ponderam ao decidir citar uma marca: ausência de menções a fraude, processos ou problemas regulatórios não resolvidos (Uri Samet, GEO-First Framework).

---

## D

**DSV-CF (Document Semantic Visibility — Citation Faithfulness)** — Métrica composta de visibilidade semântica e acurácia de citação introduzida em MAGEO (arXiv:2604.19516, ACL 2026 Findings).

---

## E

**Earned Media (mídia conquistada)** — Cobertura editorial não paga em domínios de autoridade (jornalismo, comunidades, especialistas). Discovery Gap mostra que *referring domains* são preditor dominante de descoberta (r = +0,319), mais relevante que GEO técnico isolado.

**EEAT (Experience, Expertise, Authoritativeness, Trustworthiness)** — Framework do Google para avaliação de qualidade de conteúdo. Continua relevante em modelos generativos — C-SEO Bench reforça que SEO clássico (incluindo EEAT) **complementa** GEO, não é substituído por ele.

**Entity Solidification** — Grau de associação consistente entre entidade (marca/produto/pessoa) e suas capacidades, especialistas e indústrias ao longo do grafo digital controlado. Definido por Uri Samet (GEO-First Framework, WJARR-2026-0152). Inconsistência fragmenta o grafo de conhecimento que LLMs constroem internamente.

---

## F

**Faithful Credit** — Métrica do CC-GSEO-Bench que mede se a citação de um conteúdo por um engine generativo preserva a atribuição correta à fonte original. "More Quotes" alcança 6,328 vs baseline.

**Freshness** — Pilar crítico não-negociável do GEO-16. Mede recência via `<meta property="article:modified_time">` ou `dateModified` em JSON-LD. Limiares: ≤ 90 dias evergreen, ≤ 14 dias temas voláteis.

---

## G

**G (Score GEO-16)** — Score normalizado [0,1] que combina os 16 pilares de GEO-16 ponderados. Gate de aprovação: G ≥ 0,70 e ≥ 12 pilares acionados (78% taxa de citação cross-engine). Brave prefere G = 0,727; Perplexity tolera até G = 0,300.

**G-Eval 2.0** — Rubrica de avaliação em 6 níveis aumentada por LLM, introduzida em Role-Augmented Intent-Driven GSEO (arXiv:2508.11158).

**GEO (Generative Engine Optimization)** — Otimização para engines generativos (LLMs com retrieval, *answer engines* gerativos). Conjunto de práticas técnicas, editoriais e de mídia que aumentam a probabilidade de o conteúdo ser citado em respostas geradas.

**GEO-16** — Framework de auditoria com 16 pilares: metadata, freshness, semantic_html, structured_data, headings, entity_density, citations_out, authority_signals, answer_blocks, faq, schema_jsonld, canonical, internal_links, media_alt, accessibility, llms_txt. Definido em arXiv:2509.08919.

**GraphRAG** — Variante de RAG que injeta triplas de Knowledge Graph no contexto. GraphRAG-Bench (arXiv:2506.05690, ICLR 2026) demonstra que **alguns métodos de KG degradam o LLM** por excesso de ruído — uso deve ser calibrado.

**Grounding** — Ancorar afirmações ou raciocínio do LLM em fontes verificáveis (KG, JSON-LD, links externos). +26,5% de acurácia quando reasoning é grounded em triplas (arXiv:2502.13247).

---

## H

**Headings AEO** — Headings semânticos cuja redação responde uma pergunta implícita (ex.: "Quanto custa implementar GEO?" em vez de "Custos"). Cada heading é seguido por um bloco AEO autocontido.

---

## J

**JSON-LD (JavaScript Object Notation for Linked Data)** — Formato canônico para incorporar Schema.org em páginas HTML. Validação SHACL obrigatória antes do publish.

---

## K

**Keyword Search / Semantic Search / Chunk Read** — Três interfaces hierárquicas de retrieval expostas por A-RAG (arXiv:2602.03442) que um agente pode escolher adaptativamente. Conteúdo bem estruturado é indexável simultaneamente nas três camadas.

**Knowledge Graph (KG)** — Grafo de triplas (sujeito, predicado, objeto) que representa entidades e relações. Wikidata, DBpedia, MATRIX Ontology são exemplos. Linkagem via `sameAs` em JSON-LD.

**Knowles, Malcolm** — Autor dos 6 princípios da andragogia (aprendizagem de adultos). Aplicação obrigatória nos cursos do `curso-factory`.

---

## L

**`llms.txt`** — Arquivo Markdown na raiz do domínio (`/llms.txt`) com propósito do site, URLs canônicas por tópico, políticas de citação e contatos. Volpini et al. (arXiv:2603) demonstram **+29,6% de acurácia em RAG** quando presente.

**LLM-SE (LLM-based Search Engine)** — Buscador cuja resposta é gerada por LLM sobre corpus indexado (ChatGPT Search, Perplexity, Gemini, Brave Summary). 37% dos domínios em LLM-SE não aparecem em buscadores tradicionais (arXiv:2512.09483).

---

## M

**MAGEO (Multi-Agent GEO)** — Framework multi-agente com Preference, Planner, Editor, Evaluator (arXiv:2604.19516, ACL 2026 Findings). Introduz Twin Branch Evaluation para atribuição causal de edições.

**MCP (Model Context Protocol)** — Protocolo da Anthropic para conexão entre LLMs e ferramentas/dados externos. Primeiro estágio da adoção agêntica. Lifecycle de servidor MCP: 4 fases, 16 atividades (arXiv:2503.23278).

**Modal Product** — Produto mais comum/representativo em uma categoria. Agentes concentram demanda em modais (arXiv:2508.02630). Marcar explicitamente em catálogos.

---

## N

**NER (Named Entity Recognition)** — Identificação automática de entidades nomeadas (pessoas, empresas, lugares, papers). Usado para auditar densidade de 1 entidade a cada 100 palavras.

---

## O

**Outlinks** — Links de saída para fontes externas. Importância SHAP de 0,799 como preditor de citação por LLM (arXiv:2512.09483, Source Coverage). Densidade mínima: 1 link a cada 250 palavras.

---

## R

**RAG (Retrieval-Augmented Generation)** — Padrão arquitetural em que o LLM consulta um corpus externo antes de gerar a resposta. A-RAG (arXiv:2602.03442) introduz versão agêntica com test-time scaling.

**Readme_AI** — Especificação machine-readable em formato JSON validável (NIST, arXiv:2509.19322). Alternativa estruturada ao `llms.txt`. Obrigatório em B2B e e-commerce.

**Referring Domains** — Domínios distintos que linkam para o seu site. Preditor dominante de descoberta orgânica em LLMs (r = +0,319, Discovery Gap arXiv:2601.00912).

---

## S

**Schema.org** — Vocabulário de tipos e propriedades para structured data, publicado em https://schema.org. Sage 2025 (LLM4Schema.org) reporta que **~75% das páginas web não têm Schema.org markup** — janela competitiva.

**SHACL (Shapes Constraint Language)** — Linguagem W3C para validação de RDF/JSON-LD contra esquemas. Validação obrigatória antes de publish. Schema inválido = schema ausente para muitos parsers.

**SHAP (SHapley Additive exPlanations)** — Método de explicação de modelos de ML. Source Coverage (arXiv:2512.09483) usou SHAP para isolar Tranco rank (0,923), outlinks (0,799) e TLD .com (0,623) como preditores dominantes de seleção de fonte por LLM.

**Sentiment Integrity** — Sinal que LLMs ponderam: ausência de contradição entre reviews públicas, sentimento líquido ≥ +0,4 em escala -1 a +1.

---

## T

**Test-Time Scaling Laws** — Observação de A-RAG (arXiv:2602.03442) de que agentes que iteram mais sobre o mesmo corpus extraem mais valor de conteúdo bem estruturado. Conteúdo otimizado nas três camadas (keyword, semantic, chunk) é desproporcionalmente recompensado.

**TL;DR (Too Long; Didn't Read)** — Bloco de 3–5 linhas no topo de conteúdo longo. Combinado com BLUF, forma o front-loading da resposta.

**Tranco Rank** — Ranking agregado de popularidade de domínios (https://tranco-list.eu). Importância SHAP de 0,923 como preditor dominante de citação (arXiv:2512.09483).

**Twin Branch Evaluation** — Método de MAGEO (arXiv:2604.19516) para atribuição causal: comparar resposta com e sem cada edição. Se delta < 0,05, edição não justificada.

---

## U

**UCP (Universal Commerce Protocol)** — Protocolo unificado de comércio agêntico, frequentemente referenciado junto a AP2. Em padronização na Linux Foundation Agentic AI Foundation.

---

## V

**VLM (Vision-Language Model)** — Modelo multimodal que processa imagem + texto. Pinterest GEO (arXiv:2602.02961) usa VLMs fine-tunados para *reverse search*. Implica que descrições de produto e *alt text* devem ser otimizadas para VLM (≥ 15 palavras descritivas, sem SEO-spam).

---

## W

**Wikidata QID** — Identificador canônico de entidade no Wikidata (formato `Qxxxxx`). Linkagem via `sameAs` em JSON-LD aumenta materialmente a probabilidade de desambiguação correta por agentes RAG.

---

## Acrônimos por tipo

| Tipo | Acrônimos |
|---|---|
| Engines | LLM-SE, GEO, AEO, C-SEO |
| Protocolos agênticos | MCP, ACP, A2A, ANP, AP2, UCP |
| Estruturas de dados | KG, JSON-LD, RDF, SHACL, SHAP |
| Frameworks editoriais | TL;DR, BLUF, EEAT, AEO blocks |
| Métricas | G (GEO-16), DSV-CF, Faithful Credit |
| Modelos | RAG, GraphRAG, A-RAG, MAGEO, AutoGEO, VLM, NER |
