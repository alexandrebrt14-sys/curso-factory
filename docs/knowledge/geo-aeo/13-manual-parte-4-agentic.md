---
titulo: Manual Operacional — Parte 4 — Comércio Agêntico e Infraestrutura
versao: 1.0
data: 2026-04-25
tipo: manual-operacional
escopo: Instruções 26 a 30
---

# Parte 4 — Comércio Agêntico e Infraestrutura Agêntica (Instruções 26–30)

Cinco instruções que preparam páginas, produtos e a *stack* do negócio para operar no nível 4+ da Curva de Automação Agêntica (McKinsey, *The Automation Curve in Agentic Commerce*, jan/2026). Aplicáveis tanto a páginas de produto/serviço quanto a integrações comerciais (e-commerce, marketplaces).

---

## Instrução 26 — Preparar páginas para o Nível 4+

**DIRETIVA.** Estruturar páginas de produto/serviço expondo: critérios de **elegibilidade**, **substitutos aceitáveis**, **garantias de serviço**, **integração com programas de fidelidade**. Esses dados devem estar em JSON-LD **e** em endpoints consumíveis por agentes (idealmente MCP).

**RACIONAL.** McKinsey *The Automation Curve in Agentic Commerce* (jan/2026): no nível 4+, a competição muda de "ganhar o clique" para **"ganhar lugar no plano contínuo do agente"**. Comerciantes precisam de integração mais profunda em torno de elegibilidade, substituições e garantias.

**CHECKLIST.**

- `Product` JSON-LD com campos `eligibility`, `loyaltyProgram`, `serviceLevel`, `replacementPolicy`.
- Endpoint MCP `/agent/product/<id>` retornando os mesmos campos em JSON.
- Política de substituição declarada (qual SKU equivale a qual em caso de ruptura).
- Para cursos no `curso-factory`: expor pré-requisitos, duração estimada, certificação, política de cancelamento.

**EXEMPLO JSON-LD.**

```json
{
  "@context": "https://schema.org",
  "@type": "Product",
  "name": "Curso GEO para Executivos",
  "eligibility": "Profissionais com 5+ anos em marketing digital",
  "loyaltyProgram": {
    "@type": "ProgramMembership",
    "programName": "Brasil GEO Alumni"
  },
  "serviceLevel": "Acesso vitalício, atualizações trimestrais",
  "replacementPolicy": "Reembolso integral em 7 dias"
}
```

---

## Instrução 27 — Otimizar descrições para preferências de agente, evitando *anti-signals*

**DIRETIVA.** Em descrições de produto:

- **REMOVER** rótulos "patrocinado" / "anúncio" / "promocional".
- **ADICIONAR** *endorsements* de plataforma (selos verificados, certificações).
- Posicionar o produto-modal (mais comum/representativo) com clareza.

**RACIONAL.** *What Is Your AI Agent Buying?* (arXiv:2508.02630, Columbia Business School / Microsoft) demonstra causalmente, via simulador ACES (Agentic e-Commerce Simulator) com Claude Sonnet/Opus, GPT-4.1/5.1 e Gemini 2.5/3.0 Pro, que agentes:

- Têm vieses de posição **heterogêneos** entre modelos.
- **PENALIZAM** rótulos "sponsored".
- **RECOMPENSAM** *endorsements* de plataforma.
- Concentram demanda em produtos modais.
- Podem ser influenciados por sellers que otimizam descrições para essas preferências (ganho substancial de share documentado).

**CHECKLIST.**

- Auditar copy: nenhum uso de "patrocinado", "anúncio", "promocional", "promo" no JSON-LD ou meta description.
- Listar certificações, prêmios, selos verificados de plataforma.
- Em catálogos, marcar explicitamente "best-seller" ou "modal choice" via Schema.org.

---

## Instrução 28 — Adotar a stack profissional MCP + A2A + AP2/UCP

**DIRETIVA.** Para qualquer operação comercial agêntica, implementar progressivamente: **MCP** (Model Context Protocol) primeiro, depois **ACP** (Agent Communication), **A2A** (Agent-to-Agent), **ANP** (Agent Network Protocol) conforme maturidade.

**RACIONAL.** Agent Interoperability Protocols Survey (arXiv:2505.02279) descreve a sequência de adoção MCP → ACP → A2A → ANP. Linux Foundation Agentic AI Foundation consolida MCP/UCP como padrões para transações autônomas. MCP Landscape & Security (arXiv:2503.23278) detalha 4 fases de ciclo de vida de servidor e 16 atividades — base para implementação segura.

**CHECKLIST.**

- Inventário: quais capacidades expor via MCP server próprio?
- Threat model usando as 4 taxonomias de atacante do paper MCP Security.
- Roadmap trimestral: **MCP no T1, A2A no T3, ANP avaliado no T4**.

**ESTADO ATUAL DO ECOSSISTEMA BRASIL GEO** (referência, atualizar conforme evolução):

- MCP `/api/mcp` ativo em alexandrecaramaschi.com com 4 tools (`getBusinessInfo`, `getLocation`, `contactUs`, `listCourses`).
- A2A: ainda não implementado. Avaliar em 2026-T3 quando volume de cursos justificar.
- ANP: monitorar padronização da Linux Foundation Agentic AI Foundation.

---

## Instrução 29 — *Agent Legibility* como diferencial estratégico

**DIRETIVA.** Operacionalizar **agent legibility** — descrições otimizadas para VLM, dados estruturados validáveis, KG próprio linkado a Wikidata — como **camada de produto**, não como adendo de marketing.

**RACIONAL.** O paper Agentic Web (arXiv:2507.21206, Berkeley/Dawn Song) define 3 dimensões — **inteligência, interação, economia** — e o paradigma da "Agent Attention Economy". Agentic Commerce Survey (TechRxiv jan/2026) detalha taxonomia de papéis (buyer/seller/marketplace agents). Pinterest GEO mostra ganhos concretos quando descrições são otimizadas para VLM (**+20% tráfego orgânico**).

**CHECKLIST.**

- Imagens com *alt text* denso (≥ 15 palavras descritivas, não SEO-spam).
- Descrições de produto incluem atributos visuais, materiais, casos de uso.
- KG próprio (Neo4j, GraphDB ou triplestore) com export RDF público.
- Para o Brasil GEO: triplestore com entidade Alexandre Caramaschi (Q138755507), Brasil GEO, AI Brasil, Semantix, ligadas via predicados RDF canônicos.

---

## Instrução 30 — Aplicar test-time scaling laws ao próprio conteúdo

**DIRETIVA.** Investir em conteúdo que sobreviva ao raciocínio iterativo de agentes — múltiplas passadas de retrieval. Páginas devem ser **indexáveis em três níveis**: keyword-search, semantic-search, e chunk-read.

**RACIONAL.** A-RAG (arXiv:2602.03442) demonstra que test-time scaling laws aplicam-se a RAG: agentes que iteram mais sobre o mesmo corpus extraem mais valor de conteúdo bem estruturado. Conteúdo otimizado em três camadas é desproporcionalmente recompensado.

**PSEUDOCÓDIGO.**

```
assert keyword_density_ok(page)        # camada 1: léxica
assert embedding_quality_ok(page)      # camada 2: semântica
assert chunk_self_contained(page)      # camada 3: extrativa
publish if all 3 pass else rewrite
```

**OPERACIONAL.**

- Camada 1 (léxica): TF-IDF dos termos canônicos do nicho está balanceado (sem keyword stuffing, mas sem ausência).
- Camada 2 (semântica): embeddings da página clusterizam corretamente com queries-alvo (testar com `text-embedding-3-large`).
- Camada 3 (extrativa): cada chunk de 200–400 tokens é autocontido — pode ser citado isolado sem perder sentido.

---

## Resumo da Parte 4

| Instrução | Camada | Bloqueante para e-commerce? |
|---|---|---|
| 26 — Eligibility/loyalty/SLA em Product JSON-LD | dados estruturados | sim |
| 27 — Anti-signals "sponsored" | copy | sim |
| 28 — Stack MCP → A2A → ANP | infraestrutura | progressivo |
| 29 — Agent legibility como produto | produto | sim |
| 30 — 3 camadas de indexação | conteúdo | sim |

---

## Tese da Parte 4 em uma frase

**No nível 4+, vence quem expõe elegibilidade, substituição, fidelidade e garantia de forma estruturada e consumível por agentes. *Agent legibility* é a nova SEO.**
