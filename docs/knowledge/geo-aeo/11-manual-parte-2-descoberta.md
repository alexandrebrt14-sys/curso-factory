---
titulo: Manual Operacional — Parte 2 — Descoberta, Autoridade e Dinâmica Competitiva
versao: 1.0
data: 2026-04-25
tipo: manual-operacional
escopo: Instruções 11 a 15
---

# Parte 2 — Descoberta, Autoridade e Dinâmica Competitiva (Instruções 11–15)

Cinco instruções que reorientam o eixo "técnico" da Parte 1 para o eixo "mídia conquistada e posicionamento competitivo". Em conjunto com a Parte 1, formam o que o corpus chama de *stack* "**SEO + entity graph + agent legibility**".

---

## Instrução 11 — Não confiar exclusivamente em GEO técnico

**DIRETIVA.** Para toda peça de conteúdo otimizada via GEO-16, executar em paralelo um **plano de aquisição de *referring domains* e presença em comunidades** (Reddit, Hacker News, Stack Overflow, Substack, fóruns verticais).

**RACIONAL.** Discovery Gap (arXiv:2601.00912) é o achado mais contraintuitivo do corpus: scores GEO **NÃO correlacionam com descoberta** (r ≈ 0). O que prediz descoberta é:

- **Referring domains** (r = +0,319)
- **Presença no Reddit** (r = +0,395, p = 0,002)

Há um gap de **30:1** entre reconhecimento (99,4% no ChatGPT) e descoberta orgânica (3,32%) em 112 startups testadas em 2.240 queries.

**CHECKLIST.**

- Toda publicação central tem versão derivada para Reddit (subreddit relevante), com tom nativo da plataforma.
- Mínimo de **3 menções/links** de domínios de autoridade no primeiro trimestre pós-publicação.
- Monitorar Tranco rank do domínio próprio trimestralmente.
- Para conteúdo do Brasil GEO: derivar para r/MachineLearning, r/SEO, r/marketing, r/brasil, Hacker News (categoria *Show HN* quando aplicável).

---

## Instrução 12 — Mapear e disputar o cluster Top-20

**DIRETIVA.** Identificar quais 20 domínios concentram citação no nicho-alvo e desenhar estratégia de *guest posts*, co-autorias e *backlinks* contextuais a partir deles.

**RACIONAL.** News Source Citing Patterns (arXiv:2507.05301) analisou **366.087 URLs em 24.069 conversas** entre março e maio de 2025: **Top 20 fontes = 67,3% das citações em modelos OpenAI**. Há *clustering* intra-família forte (cosseno > 0,67) e cross-family fraco (< 0,33) — uma estratégia alinhada à família OpenAI difere da alinhada à Anthropic.

**CHECKLIST.**

- Listar top-20 do nicho via análise de citações em ChatGPT, Perplexity, Gemini, Claude.
- Para cada domínio: identificar editor, formato preferido, política de contribuição.
- **Meta:** 1 publicação ou backlink contextual a cada 60 dias em domínios desse cluster.
- Mapeamento separado por família de LLM (OpenAI, Anthropic, Google, Perplexity).

---

## Instrução 13 — Otimização multi-engine ponderada

**DIRETIVA.** Otimizar para **múltiplos engines simultaneamente** com pesos definidos pelo perfil de tráfego do negócio. **Nunca otimizar apenas para um.**

**RACIONAL.** AutoGEO (arXiv:2510.11438, CMU) demonstra que cada engine tem regras de preferência distintas — Gemini, Claude e GPT respondem diferentemente aos mesmos sinais. MAGEO (arXiv:2604.19516, ACL 2026 Findings) propõe Twin Branch Evaluation para atribuição causal de edições.

**PSEUDOCÓDIGO.**

```
pesos = {"chatgpt": 0.35, "perplexity": 0.25, "gemini": 0.20, "claude": 0.15, "brave": 0.05}
score_total = sum(pesos[e] * score_engine(page, e) for e in pesos)
otimizar para maximizar score_total, NÃO score_engine isolado
```

**Notas sobre pesos.** Os valores acima são default sugerido pela literatura para um portfólio diversificado. Ajustes recomendados:

- Negócios B2B com tráfego majoritário via ChatGPT Search → ChatGPT 0,45 / Perplexity 0,20.
- Negócios com perfil técnico (developers) → Perplexity 0,35 / Claude 0,20.
- E-commerce → ChatGPT 0,30 / Gemini 0,30 (Google Shopping integration).

---

## Instrução 14 — Otimização é jogo de soma zero em escala

**DIRETIVA.** Reconhecer que ganhos de citação relativa são **zero-sum** — o agente cita N fontes; se você entra, alguém sai. Priorizar verticais onde a competição GEO ainda é fraca.

**RACIONAL.** C-SEO Bench (arXiv:2506.11097, NeurIPS 2025) demonstra que (a) a maioria dos métodos C-SEO é ineficaz, (b) **SEO tradicional + GEO combinados vencem**, (c) **dinâmica competitiva é zero-sum** quando vários competidores adotam a mesma tática. Concentração de 67% no top-20 cria janela para *early movers* em verticais ainda não disputadas.

**CHECKLIST.**

- Mapear nichos com baixa densidade de conteúdo GEO-otimizado (verificar G médio dos top-10 de SERP).
- Combinar SEO clássico (backlinks, EEAT, *Core Web Vitals*) com GEO — nunca substituir.
- Priorizar nichos onde o autor tem credencial verificável (no caso do Brasil GEO: GEO no Brasil, marketing por IA, comércio agêntico em PT-BR).

---

## Instrução 15 — Verificar Sentiment Integrity e Clean Recommendations

**DIRETIVA.** Auditar reviews, menções e citações públicas da marca para detectar contradições e *red flags*. Resolver dissonâncias antes de escalar GEO.

**RACIONAL.** GEO-First Framework (Uri Samet) destaca **Sentiment Integrity** e **Clean Recommendations** como sinais que LLMs ponderam ao decidir citar uma marca. Reviews contraditórias ou menções de fraude/processos suprimem citação mesmo com GEO técnico perfeito.

**CHECKLIST.**

- Varredura **trimestral** em Trustpilot, Reclame Aqui, Glassdoor, Reddit, G2.
- Sentimento líquido **≥ +0,4** em escala -1 a +1.
- Plano público de resposta a reviews negativas com resolução documentada.
- Para o ecossistema Brasil GEO: monitorar menções no Twitter/X, LinkedIn e em comunidades de marketing digital brasileiras.

---

## Resumo da Parte 2

| Instrução | Métrica chave | Frequência |
|---|---|---|
| 11 — Mídia conquistada | ≥ 3 referring domains/trimestre | trimestral |
| 12 — Cluster Top-20 | 1 backlink contextual / 60 dias | bimensal |
| 13 — Multi-engine | score ponderado consolidado | mensal |
| 14 — Zero-sum vigilance | G médio dos top-10 do nicho | trimestral |
| 15 — Sentiment Integrity | sentimento líquido ≥ +0,4 | trimestral |

---

## Tese da Parte 2 em uma frase

**Otimização técnica te coloca no jogo. Mídia conquistada e cluster Top-20 te fazem ganhar.**
