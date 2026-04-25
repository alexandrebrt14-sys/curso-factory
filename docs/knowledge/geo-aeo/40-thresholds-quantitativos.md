---
titulo: Thresholds Quantitativos — Tabela Mestre
versao: 1.0
data: 2026-04-25
tipo: referencia-rapida
---

# Thresholds Quantitativos — Tabela Mestre

Todos os limiares numéricos do corpus consolidados em uma única tabela. Use como referência rápida durante auditoria, redação ou planejamento.

---

## Tabela mestre — limiares

| Limiar | Valor | Métrica de quê | Fonte | Onde aplica |
|---|---|---|---|---|
| G ≥ 0,70 | score [0,1] | Aprovação GEO-16 | arXiv:2509.08919 | Auditoria de página |
| Pilares acionados ≥ 12 | de 16 | Aprovação GEO-16 | arXiv:2509.08919 | Auditoria de página |
| Citação cross-engine | 78% | Para páginas G ≥ 0,70 | arXiv:2509.08919 | Outcome esperado |
| G Brave preferred | 0,727 | Score preferencial Brave Summary | arXiv:2509.08919 | Otimização Brave |
| G Perplexity tolerância | 0,300 | Score mínimo aceito por Perplexity | arXiv:2509.08919 | Otimização Perplexity |
| `llms.txt` ganho RAG | +29,6% | Acurácia em RAG | Volpini/WordLift (arXiv:2603) | Justifica Instrução 4 |
| Agentic RAG C5 vs C2 | 4,40 vs 3,89 (Δ=+0,50, t=-5,22) | Score acurácia | Volpini/WordLift | Justifica Instrução 4 |
| KG grounding ganho | +26,5% | Acurácia em raciocínio | arXiv:2502.13247 | Justifica Instruções 3, 17 |
| Top 20 fontes | 67,3% | Concentração de citações OpenAI | arXiv:2507.05301 | Justifica Instrução 12 |
| Cluster intra-família | cosseno > 0,67 | Similaridade de citações | arXiv:2507.05301 | Justifica Instrução 13 |
| Cluster cross-family | cosseno < 0,33 | Divergência de citações | arXiv:2507.05301 | Justifica Instrução 13 |
| Tranco rank SHAP | 0,923 | Importância para citação | arXiv:2512.09483 | Justifica Princípio Mestre 3 |
| Outlinks SHAP | 0,799 | Importância para citação | arXiv:2512.09483 | Justifica Instrução 7 |
| TLD `.com` SHAP | 0,623 | Importância para citação | arXiv:2512.09483 | Justifica preferência por Medium |
| LLM-SE únicos | 37% | Domínios não em SE tradicional | arXiv:2512.09483 | Justifica investir em LLM-SE |
| Discovery Gap | 30:1 | Recognition vs Discovery | arXiv:2601.00912 | Justifica Princípio Mestre 1 |
| Recognition ChatGPT | 99,4% | Reconhecimento direto | arXiv:2601.00912 | Justifica Princípio Mestre 1 |
| Discovery ChatGPT | 3,32% | Descoberta orgânica | arXiv:2601.00912 | Justifica Princípio Mestre 1 |
| Recognition Perplexity | 94,3% | Reconhecimento direto | arXiv:2601.00912 | Justifica Princípio Mestre 1 |
| Discovery Perplexity | 8,29% | Descoberta orgânica | arXiv:2601.00912 | Justifica Princípio Mestre 1 |
| GEO score → discovery | r ≈ 0 | Correlação | arXiv:2601.00912 | Justifica Princípio Mestre 1 |
| Referring domains → discovery | r = +0,319 | Correlação | arXiv:2601.00912 | Justifica Instrução 11 |
| Reddit → discovery | r = +0,395, p = 0,002 | Correlação | arXiv:2601.00912 | Justifica Instrução 11 |
| Quotes Exposure | 5,769 | Eixo CC-GSEO-Bench | arXiv:2509.05607 | Justifica Princípio 4 |
| Quotes Faithful Credit | 6,328 | Eixo CC-GSEO-Bench | arXiv:2509.05607 | Justifica Princípio 4 |
| Stats degrada Trust | 7,613 vs 8,352 baseline | Trustworthiness | arXiv:2509.05607 | Justifica anti-pattern A5 |
| Pinterest tráfego | +20% | Tráfego orgânico | arXiv:2602.02961 | Justifica Instrução 29 |
| Pinterest topic-query | +19% | Alinhamento | arXiv:2602.02961 | Justifica Instrução 29 |
| Páginas sem Schema | ~75% | Web em 2025 | Sage 2025 (LLM4Schema.org) | Justifica Instrução 2 |

---

## Limiares operacionais derivados

Limiares prescritivos no manual operacional, derivados ou calibrados a partir dos papers:

| Limiar | Valor prescritivo | Instrução |
|---|---|---|
| Densidade entidades nomeadas | ≥ 1 a cada 100 palavras | Instrução 17 |
| Densidade outlinks | ≥ 1 a cada 250 palavras | Instrução 7 |
| Densidade estatísticas | ≤ 1 a cada 200 palavras | Instrução 8 |
| Razão quote:estatística | ≥ 2:1 | Instrução 8 |
| Bloco AEO pós-heading | 40–80 palavras | Instrução 6 |
| Negrito por seção | 1–3 trechos, máx 12 palavras | Instrução 23 |
| Meta description | 140–160 caracteres | Instrução 2 |
| Freshness evergreen | ≤ 90 dias | Instrução 2 |
| Freshness temas voláteis | ≤ 14 dias | Instrução 2 |
| Alt text descritivo | ≥ 15 palavras | Instrução 29 |
| Sentimento líquido | ≥ +0,4 (escala -1 a +1) | Instrução 15 |
| Calibragem KG (delta) | ≥ 0,05 ou remover | Instrução 10 |
| Backlinks contextuais | 1 a cada 60 dias em top-20 | Instrução 12 |

---

## Limiares por plataforma de publicação

| Plataforma | Comprimento ideal | Tags / hashtags | Pull quotes |
|---|---|---|---|
| Medium | 1.500–2.500 palavras | 5 (2 amplas + 3 nichadas) | 1 a cada 500 palavras |
| Quora | 600–1.200 palavras | n/a | 1 quote autoritativa |
| LinkedIn Newsletter | 1.000–1.800 palavras | máx 5, profissionais | 1 estatística por insight |
| Substack | 2.000–4.000 palavras | n/a (categorias) | footnotes numeradas |

---

## Pesos sugeridos (multi-engine optimization, Instrução 13)

| Engine | Peso default | Quando aumentar |
|---|---|---|
| ChatGPT | 0,35 | B2B + tráfego majoritário ChatGPT Search → 0,45 |
| Perplexity | 0,25 | Audiência técnica/developer → 0,35 |
| Gemini | 0,20 | E-commerce + Google Shopping → 0,30 |
| Claude | 0,15 | Conteúdo técnico/longform → 0,20 |
| Brave | 0,05 | Audiência privacy-focused → 0,10 |

A soma deve ser 1,00 após ajustes.

---

## FinOps — limiares de custo (ecossistema Brasil GEO)

| Limiar | Valor | Aplicação |
|---|---|---|
| Builds Vercel `landing-page-geo` | máx 2 pushes/dia | FinOps real ($0,26/push) |
| Custo Claude por curso | máx $5 | `cost_tracker` budget guard |
| Custo total por curso | máx $10 | `cost_tracker` budget guard |
| Cache TTL | 24h | SHA-256 |

---

## Como atualizar esta tabela

- Toda nova métrica quantitativa de paper aceito no corpus deve aparecer aqui na primeira atualização trimestral seguinte.
- Métricas conflitantes entre papers: documentar ambas com coluna "fonte" e adicionar nota de reconciliação.
- Limiares prescritivos podem mudar com nova evidência — versionamento via tag de commit.
