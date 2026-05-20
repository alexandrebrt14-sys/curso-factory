# seogeo-20260520 — Fontes brutas do incremento canônico

Esta pasta preserva os 3 documentos originais (DOCX + PDF) e as extrações em Markdown que originaram [`docs/SEO_GEO_INCREMENT_20260520.md`](../../SEO_GEO_INCREMENT_20260520.md).

## Arquivos

| Arquivo | Origem | Conteúdo |
|---|---|---|
| `00_source_io2026.docx` | Original | Ensaio "GEO, SEO e AI Search depois do Google I/O 2026" |
| `00_source_otimizacao.docx` | Original | Tratado "A Arquitetura da Síntese Baseada em Recuperação: SEO/AEO/GEO/ASO" |
| `00_source_master_prompt.pdf` | Original | PDF "PROMPT-MESTRE EXECUTÁVEL — Auditoria & Otimização de Portal Editorial em 5 Ondas — Edição 2026" |
| `doc1_io2026.md` | Extração | Texto extraído do DOCX 1 |
| `doc2_otimizacao.md` | Extração | Texto extraído do DOCX 2 |
| `doc3_master_prompt.md` | Extração | Texto extraído do PDF (47 páginas) |

## Como foi processado

- Extração DOCX via `python-docx` (preservando headings + tabelas como markdown).
- Extração PDF via `pdfplumber` (47 páginas, ~57KB de texto).
- Síntese e estruturação em `docs/SEO_GEO_INCREMENT_20260520.md` com:
  - Sumário executivo (BLUF, 5 teses)
  - Master Prompt 5 Ondas unificado
  - 38 camadas mapeadas
  - 8 query fan-out variant types
  - Princeton GEO playbook com lifts mensurados
  - Two-Phase JSON-LD theory
  - Entity Boundary Drift + cosine
  - Catálogo bots IA atualizado (mai/2026)
  - Anti-padrões 2026
  - Glossário canônico
  - Referências primárias

## Quando reler

- Antes de criar curso "GEO/SEO 2026" (writer GPT-4o usa o incremento; researcher Perplexity pode minerar nas fontes brutas se precisar de mais densidade).
- Antes de auditoria de portal cliente que queira a versão completa do Master Prompt 5 Ondas.
- Antes da próxima revisão trimestral do incremento (próxima: agosto/2026) — comparar com novos documentos canônicos Google/Microsoft/Cloudflare.

## Cuidado

Conteúdo das fontes traz números, lifts e benchmarks com data específica (maio/2026). Antes de citar em material novo (>3 meses depois), validar se as referências primárias (Google AI Optimization Guide, Bing AI Performance, Ahrefs, ALM Corp, Reuters Institute) ainda permanecem válidas — Google reescreve docs canônicos com frequência e benchmarks de mercado mudam rápido em 2026.
