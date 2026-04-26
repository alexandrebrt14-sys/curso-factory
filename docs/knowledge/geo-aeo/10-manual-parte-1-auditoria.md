---
titulo: Manual Operacional — Parte 1 — Auditoria Técnica e Estrutural
versao: 1.0
data: 2026-04-25
tipo: manual-operacional
escopo: Instruções 1 a 10
---

# Parte 1 — Auditoria Técnica e Estrutural (Instruções 1–10)

Pilares técnicos que toda página do ecossistema deve cumprir. Este conjunto de 10 instruções funciona como *gate* primário de auditoria. Páginas abaixo dos limiares aqui definidos entram em fila de reescrita obrigatória.

Cada instrução segue o padrão:
- **DIRETIVA** (regra imperativa)
- **RACIONAL** (justificativa com paper/dado)
- **PSEUDOCÓDIGO/CHECKLIST** (lógica acionável)

---

## Instrução 1 — Aplicar GEO-16 como gate primário

**DIRETIVA.** Toda página auditada deve ser pontuada nos 16 pilares do GEO-16. Aprovar somente páginas com **G ≥ 0,70 e ≥ 12 pilares acionados**. Páginas abaixo deste limiar entram em fila de reescrita obrigatória.

**RACIONAL.** O paper GEO-16 (arXiv:2509.08919) demonstra que páginas neste patamar atingem **78% de taxa de citação cross-engine**. Brave Summary cita preferencialmente páginas com G = 0,727; Perplexity tolera até G = 0,300, mas a otimização para o piso superior maximiza cobertura simultânea.

**PSEUDOCÓDIGO.**

```
score = 0
pilares_acionados = 0
for pilar in [metadata, freshness, semantic_html, structured_data,
              headings, entity_density, citations_out, authority_signals,
              answer_blocks, faq, schema_jsonld, canonical, internal_links,
              media_alt, accessibility, llms_txt]:
    if pilar.check(page):
        score += peso[pilar]
        pilares_acionados += 1
G = score / soma_pesos_max
APROVAR se G >= 0.70 AND pilares_acionados >= 12
SENÃO encaminhar para pipeline de reescrita (Parte 3)
```

---

## Instrução 2 — Metadata, Freshness e Structured Data são não-negociáveis

**DIRETIVA.** Mesmo que outros pilares falhem, **estes três devem estar 100% acionados**. Ausência de qualquer um bloqueia publicação.

**RACIONAL.** GEO-16 identifica esses três como pilares de maior peso marginal na taxa de citação. LLM4Schema.org (Sage 2025) mostra que **~75% das páginas web não possuem Schema.org markup** — quem fizer corretamente captura desproporcionalmente as citações.

**CHECKLIST.**

- `<meta name="description">` entre 140–160 caracteres, com entidade-âncora no início.
- `<meta property="article:modified_time">` ou `dateModified` em JSON-LD presente. Limiares: ≤ 90 dias evergreen, ≤ 14 dias temas voláteis.
- JSON-LD válido contra SHACL (Article, FAQPage, HowTo, Product, Organization conforme aplicável).
- `<meta property="og:*">` e `<meta name="twitter:*">` completos para *agent affordance* visual.

---

## Instrução 3 — Schema.org com validação SHACL automática

**DIRETIVA.** Gerar JSON-LD para toda página, validar contra SHACL antes de publicar, e linkar entidades a **Wikidata QIDs** sempre que possível via `sameAs`.

**RACIONAL.** O pipeline LLM4Schema.org (Sage 2025) demonstra que JSON-LD validado + linkagem a Wikidata aumenta materialmente a probabilidade de a entidade ser desambiguada corretamente por agentes RAG. *Grounding LLM Reasoning with KGs* (arXiv:2502.13247) reporta **+26,5% de acurácia** quando o raciocínio é ancorado em triplas de grafo de conhecimento.

**PSEUDOCÓDIGO.**

```
jsonld = generate_schema(page, type=detect_type(page))
jsonld["sameAs"] = [wikidata_qid(entity) for entity in extract_entities(page)]
if not shacl_validate(jsonld, shape="schemaorg.shapes.ttl"):
    raise ValidationError
inject_into_html(page, jsonld)
```

---

## Instrução 4 — Publicar `llms.txt` E `readme_ai.json`

**DIRETIVA.** Toda propriedade web deve expor `/llms.txt` (Markdown) **E** `/readme_ai.json` (formato NIST). O segundo é obrigatório para domínios B2B e e-commerce.

**RACIONAL.** Volpini et al. (WordLift, arXiv:2603) demonstram **+29,6% de acurácia em RAG** quando páginas de entidade incluem instruções estilo `llms.txt` — JSON-LD sozinho é insuficiente. Agentic RAG (configuração C5) atinge 4,40 vs RAG padrão (C2) em 3,89 (Δ = +0,50, t = -5,22). O Readme_AI (arXiv:2509.19322, NIST) oferece formato JSON validável complementar.

**CHECKLIST.**

- `llms.txt` lista: propósito do site, URLs canônicas por tópico, políticas de citação, contatos.
- `readme_ai.json` traz: tags semânticas, schema de produtos/artigos, *capabilities* expostas, endpoints MCP se houver.
- Ambos servidos com `Content-Type` correto (`text/markdown` e `application/json`).

---

## Instrução 5 — HTML semântico estrito e hierarquia consistente

**DIRETIVA.** Um único `<h1>` por página. `<h2>` para seções principais, `<h3>` para sub-respostas. Usar `<article>`, `<section>`, `<aside>`, `<nav>` corretamente. Sem `<div>` substituindo elementos semânticos.

**RACIONAL.** A-RAG (arXiv:2602.03442) descreve interfaces hierárquicas de retrieval (`keyword_search`, `semantic_search`, `chunk_read`). Conteúdo precisa ser indexável nas três camadas — HTML semântico é o que permite *chunking* limpo pelo retriever do agente.

**CHECKLIST.**

- Headings respondem perguntas (não são rótulos como "Introdução").
- Cada `<h2>` é seguido por um parágrafo-resposta de 40–80 palavras (bloco AEO).
- `<dl>`, `<table>`, `<figure>` usados onde aplicável para máxima estruturação.

---

## Instrução 6 — Blocos de resposta direta (AEO) no topo de cada seção

**DIRETIVA.** Imediatamente após cada `<h2>`/`<h3>`, escrever **um parágrafo de 40–80 palavras** que responda a pergunta implícita do heading de forma autocontida, sem pronomes referenciais ambíguos.

**RACIONAL.** CC-GSEO-Bench (arXiv:2509.05607) e o Role-Augmented Intent-Driven GSEO (arXiv:2508.11158, G-Eval 2.0) mostram que blocos auto-contidos com intenção explícita são preferencialmente extraídos como citação literal por engines generativos.

**PSEUDOCÓDIGO.**

```
for heading in page.headings:
    pergunta = headings_to_question(heading)
    bloco = generate_self_contained_answer(pergunta, max_words=80, min_words=40)
    assert no_dangling_pronouns(bloco)
    insert_after(heading, bloco)
```

---

## Instrução 7 — Densidade de citações externas: 1 a cada 250 palavras

**DIRETIVA.** Inserir links de saída para fontes primárias autoritativas (papers, órgãos oficiais, dados estatísticos) com densidade mínima de **1 link a cada 250 palavras** em conteúdo de longo formato.

**RACIONAL.** Source Coverage and Citation Bias (arXiv:2512.09483) identifica via SHAP que **outlinks count tem importância 0,799** como preditor de citação por LLM, atrás apenas de Tranco rank (0,923). Discovery Gap (arXiv:2601.00912) confirma que *referring domains* correlacionam r = +0,319 com descoberta orgânica.

**CHECKLIST.**

- Priorizar `.gov`, `.edu`, arXiv, DOI, e fontes top-20 (concentram 67,3% das citações em modelos OpenAI — arXiv:2507.05301).
- Evitar links para agregadores de notícias quando a fonte primária está acessível.

---

## Instrução 8 — Densidade de quotes vs. estatísticas, calibrada

**DIRETIVA.** Aumentar densidade de **quotes diretas** (citações entre aspas atribuíveis) — estratégia mais robusta segundo CC-GSEO-Bench. Adicionar estatísticas com moderação: **máximo 1 estatística a cada 200 palavras**.

**RACIONAL.** CC-GSEO-Bench (arXiv:2509.05607): "More Quotes" é a estratégia mais robusta (Exposure 5,769; Faithful Credit 6,328). "Statistics" eleva impacto causal **mas degrada Trustworthiness** (7,613 vs baseline 8,352). Excesso de números soa promocional e reduz citação.

**CHECKLIST.**

- Toda quote tem fonte nomeada (pessoa, cargo, organização, data).
- Toda estatística tem link para fonte primária e ano de referência.
- Razão *quote:estatística* ≥ 2:1 em conteúdo orientativo.

---

## Instrução 9 — Solidificação de Entidade

**DIRETIVA.** Para toda marca/produto/pessoa central na página, garantir consistência de associação entre **capacidades, especialistas e indústrias** ao longo de todo o grafo digital controlado (site, perfis sociais, Wikipedia/Wikidata, GitHub, perfis de especialistas).

**RACIONAL.** GEO-First Framework (Uri Samet, WJARR-2026-0152) define *Entity Solidification* como o grau de associação consistente. MATRIX Ontology (Springer LNBIP 556, CAiSE 2025) reforça uso de RDF para memória cross-agente. Inconsistência fragmenta o grafo de conhecimento que LLMs constroem internamente.

**CHECKLIST.**

- Mesma descrição-âncora (1–2 frases) em todos os perfis.
- Mesmo conjunto de 3–5 capacidades centrais mencionadas em cada propriedade.
- `sameAs` em JSON-LD listando todos os perfis canônicos (Wikidata, LinkedIn, GitHub, ORCID, site oficial).
- Para o ecossistema Brasil GEO, ver identificadores em `50-fontes-e-links.md`.

---

## Instrução 10 — Calibrar uso de Knowledge Graphs para evitar ruído

**DIRETIVA.** Antes de injetar triplas de KG ou conexões a grafos públicos, validar que adicionam sinal e não ruído. **Testar com e sem** o enriquecimento e medir delta de qualidade.

**RACIONAL.** GraphRAG-Bench (arXiv:2506.05690, ICLR 2026) demonstra que **alguns métodos de KG DEGRADAM o desempenho do LLM** ao adicionar ruído. O uso de grafo deve ser calibrado, não maximalista.

**PSEUDOCÓDIGO.**

```
baseline_score = eval_rag(page_without_kg)
enriched_score = eval_rag(page_with_kg_triples)
if enriched_score - baseline_score < 0.05:
    log("KG enrichment não justificado; remover")
    remove_kg_injection(page)
```

---

## Resumo da Parte 1

| Instrução | Limiar / Métrica | Bloqueante? |
|---|---|---|
| 1 — GEO-16 gate | G ≥ 0,70 e ≥ 12 pilares | sim |
| 2 — Metadata/Freshness/Schema | 100% acionados | sim |
| 3 — SHACL validation | erro = não publica | sim |
| 4 — `llms.txt` + `readme_ai.json` | ambos presentes | sim (B2B/e-commerce) |
| 5 — HTML semântico | um único `<h1>` | aviso |
| 6 — Blocos AEO | 40–80 palavras pós-heading | aviso |
| 7 — Outlinks | ≥ 1 a cada 250 palavras | aviso |
| 8 — Quotes vs stats | razão ≥ 2:1, max 1 stat / 200 palavras | aviso |
| 9 — Entity Solidification | descrição-âncora consistente | aviso |
| 10 — KG calibrado | delta ≥ 0,05 ou remover | aviso |
