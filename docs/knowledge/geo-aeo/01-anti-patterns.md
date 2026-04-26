---
titulo: Anti-Patterns — O que evitar em GEO, AEO e Comércio Agêntico
versao: 1.0
data: 2026-04-25
tipo: nucleo-doutrinario
---

# Anti-Patterns Consolidados

Lista exaustiva do que **NÃO fazer**, com a evidência empírica que justifica cada veto. Adições futuras só são aceitas com paper ou benchmark publicado que demonstre degradação.

---

## A1 — Otimizar somente para um engine (single-engine bias)

**Veto:** maximizar score isolado para ChatGPT, Perplexity, Gemini ou Claude.

**Por quê:** AutoGEO (arXiv:2510.11438, CMU) demonstra que cada engine tem regras de preferência distintas. *Clustering* intra-família é forte (cosseno > 0,67) e cross-family é fraco (< 0,33) — o que serve para a família OpenAI difere do que serve para a Anthropic (arXiv:2507.05301).

**Padrão correto:** otimização multi-engine ponderada (Instrução 13). Pesos sugeridos: ChatGPT 0,35 / Perplexity 0,25 / Gemini 0,20 / Claude 0,15 / Brave 0,05.

---

## A2 — Confiar em GEO técnico isolado

**Veto:** publicar páginas com G ≥ 0,70 e considerar o trabalho concluído.

**Por quê:** *Discovery Gap* (arXiv:2601.00912) reporta correlação r ≈ 0 entre GEO score e descoberta orgânica. O gap recognition→discovery é de 30:1.

**Padrão correto:** todo conteúdo otimizado tecnicamente exige plano paralelo de *referring domains* e presença em Reddit/Hacker News/Stack Overflow.

---

## A3 — Usar rótulos "patrocinado", "anúncio", "promocional" em produtos

**Veto:** incluir esses tokens em copy de produto, JSON-LD ou meta description quando se quer ser citado por agentes.

**Por quê:** *What Is Your AI Agent Buying?* (arXiv:2508.02630, Columbia/Microsoft) demonstra causalmente que agentes **penalizam** essas tags em e-commerce, com vieses heterogêneos por modelo (Claude Sonnet/Opus, GPT-4.1/5.1, Gemini 2.5/3.0 Pro).

**Padrão correto:** usar *endorsements* de plataforma (selos verificados, certificações, prêmios). Marcar explicitamente "best-seller" ou "modal choice" em catálogos.

---

## A4 — Ignorar reviews contraditórias e *red flags*

**Veto:** escalar GEO técnico com sentimento líquido < +0,4.

**Por quê:** *Sentiment Integrity* e *Clean Recommendations* (Uri Samet, GEO-First Framework, WJARR-2026-0152) são sinais que LLMs ponderam ao decidir citar uma marca. Reviews contraditórias e menções de fraude/processos suprimem citação mesmo com GEO técnico perfeito.

**Padrão correto:** varredura trimestral em Trustpilot, Reclame Aqui, Glassdoor, Reddit, G2. Plano público de resposta a reviews negativas com resolução documentada.

---

## A5 — Maximizar densidade de estatísticas

**Veto:** "encher" o texto de números achando que isso aumenta citação.

**Por quê:** CC-GSEO-Bench (arXiv:2509.05607) mostra que "Statistics" eleva impacto causal **mas degrada Trustworthiness** (7,613 vs baseline 8,352).

**Padrão correto:** máximo 1 estatística a cada 200 palavras, razão quote:estatística ≥ 2:1, toda estatística com link para fonte primária e ano de referência.

---

## A6 — Aplicar Knowledge Graphs indiscriminadamente

**Veto:** injetar todas as triplas disponíveis em Wikidata/DBpedia "para enriquecer".

**Por quê:** GraphRAG-Bench (arXiv:2506.05690, ICLR 2026) demonstra que **alguns métodos de KG degradam o LLM** por excesso de ruído. KG não é monotonicamente bom.

**Padrão correto:** Twin Branch Evaluation. Comparar `eval_rag(page_with_kg)` vs `eval_rag(page_without_kg)`. Se delta < 0,05, remover.

---

## A7 — Negrito decorativo ou em frases inteiras

**Veto:** negritar parágrafos completos ou usar **negrito** como elemento visual.

**Por quê:** Negrito é sinal de saliência tanto para humanos quanto para extratores de chunk. Excesso dilui o sinal — princípio aplicado consistentemente em CC-GSEO-Bench e validado em testes de extração por Perplexity.

**Padrão correto:** 1–3 trechos curtos por seção, máximo 12 palavras cada, somente em frases-tese.

---

## A8 — Replicar o mesmo conteúdo em Medium, Quora, LinkedIn e Substack

**Veto:** publicar a mesma versão em todas as plataformas.

**Por quê:** Cada plataforma tem norma editorial e mecânica de descoberta distintas. Reddit-Reddit correlation com descoberta (Discovery Gap) e o caso Pinterest GEO (arXiv:2602.02961, **+20% tráfego orgânico** com adaptação a especificidades visuais) confirmam que tom nativo importa.

**Padrão correto:** matriz por plataforma em `32-checklist-publicacao-multi.md`. Cada plataforma tem comprimento, tom, estrutura-chave e CTA distintos.

---

## A9 — Substituir SEO clássico por GEO

**Veto:** desinvestir de backlinks, EEAT, *Core Web Vitals* em nome de "fazer GEO".

**Por quê:** C-SEO Bench (arXiv:2506.11097, NeurIPS 2025): a maioria dos métodos C-SEO é ineficaz, e **SEO tradicional + GEO combinados vencem**. A dinâmica é zero-sum quando vários competidores adotam a mesma tática.

**Padrão correto:** GEO é camada **adicional**, nunca substitutiva. Combine.

---

## A10 — Pular validação SHACL no JSON-LD

**Veto:** publicar Schema.org gerado por LLM sem validação automática.

**Por quê:** LLM4Schema.org (Sage 2025) demonstra que JSON-LD inválido equivale a JSON-LD ausente para muitos parsers. ~75% das páginas web não têm schema válido — quem fizer corretamente captura desproporcionalmente as citações.

**Padrão correto:** SHACL contra `schemaorg.shapes.ttl` antes do publish. Falha bloqueia deploy.

---

## A11 — Cabeçalhos genéricos ("Introdução", "Conclusão")

**Veto:** usar headings rótulo, sem semântica de pergunta.

**Por quê:** A-RAG (arXiv:2602.03442) descreve interfaces de recuperação hierárquica que dependem de *signposts* extractáveis. Headings genéricos não funcionam como âncoras de chunk.

**Padrão correto:** todo `<h2>`/`<h3>` responde uma pergunta específica e é seguido por bloco AEO de 40–80 palavras autocontido.

---

## A12 — Mencionar entidades sem linkar fonte canônica na primeira ocorrência

**Veto:** citar pessoas, empresas, papers, padrões técnicos sem `sameAs` para Wikidata, arXiv, DOI ou site oficial.

**Por quê:** Perde-se grounding em KG e o ganho de **+26,5% de acurácia em raciocínio** (arXiv:2502.13247).

**Padrão correto:** densidade de 1 entidade nomeada a cada 100 palavras, com pelo menos 30% linkadas a fonte canônica na primeira menção.

---

## A13 — Tratar `llms.txt` como opcional

**Veto:** considerar `/llms.txt` como item cosmético do *backlog*.

**Por quê:** Volpini et al. (WordLift, arXiv:2603) reportam **+29,6% de acurácia em RAG** quando páginas de entidade incluem instruções estilo `llms.txt`. Agentic RAG (C5) atinge 4,40 vs RAG padrão (C2) em 3,89 (Δ = +0,50, t = -5,22).

**Padrão correto:** `/llms.txt` (Markdown) **e** `/readme_ai.json` (formato NIST, arXiv:2509.19322) na raiz. Obrigatório para domínios B2B e e-commerce.

---

## A14 — Publicar sem `dateModified` ou com data desatualizada

**Veto:** páginas sem `<meta property="article:modified_time">` ou com `dateModified` em JSON-LD ausente.

**Por quê:** GEO-16 (arXiv:2509.08919) identifica **Freshness** como pilar crítico não-negociável. Ausência bloqueia publicação.

**Padrão correto:** ≤ 90 dias para conteúdo evergreen, ≤ 14 dias para temas voláteis. Atualizar `dateModified` em qualquer edição.

---

## A15 — Esperar Nível 5 para implementar MCP

**Veto:** adiar adoção de MCP/A2A "porque o mercado ainda não está maduro".

**Por quê:** Nível 4+ da Curva de Automação Agêntica (McKinsey, jan/2026) **já exige** integração agêntica em torno de elegibilidade, substituição e fidelidade. Quem espera, perde lugar no plano contínuo do agente.

**Padrão correto:** roadmap trimestral MCP no T1 → A2A no T3 → ANP avaliado no T4 (arXiv:2505.02279).

---

## A16 — Tratar conteúdo gerado por IA como definitivo sem verificação contra fonte

**Veto:** publicar afirmações factuais sem fonte primária linkada, dado em JSON-LD da própria página, ou tripla de KG referenciada.

**Por quê:** Mitigação de alucinação por LLM depende de conteúdo estruturado (KGs, Schema.org, JSON-LD). MATRIX Ontology e LLM4Schema.org convergem nesse ponto.

**Padrão correto:** toda afirmação factual deve ser verificável contra (a) link externo, (b) JSON-LD da página, ou (c) tripla de KG. Sem fonte → reescrever ou marcar `[FALTA EVIDÊNCIA]` para revisão.

---

## Tabela-resumo de bloqueio para o pipeline

| Anti-pattern | Detecção automática? | Camada do pipeline | Severidade |
|---|---|---|---|
| A3 (rótulos sponsored) | sim (regex) | Quality Gate / Conteúdo | bloqueante |
| A5 (excesso de stats) | sim (contagem) | Quality Gate / Conteúdo | aviso |
| A7 (negrito excessivo) | sim (contagem) | Quality Gate / Conteúdo | aviso |
| A10 (SHACL inválido) | sim (validador) | Quality Gate / HTML | bloqueante |
| A11 (headings genéricos) | sim (lista) | Quality Gate / Conteúdo | aviso |
| A12 (entidades sem link) | sim (NER + link check) | Quality Gate / Links | aviso |
| A13 (`llms.txt` ausente) | sim (curl raiz) | Pre-deploy | bloqueante |
| A14 (`dateModified` ausente) | sim (parser meta) | Quality Gate / HTML | bloqueante |
| A16 (afirmação sem fonte) | parcial (heurística) | Voice Guard | aviso |

Os demais (A1, A2, A4, A6, A8, A9, A15) são decisões estratégicas que dependem de planejamento, não de validação automática por chamada.
