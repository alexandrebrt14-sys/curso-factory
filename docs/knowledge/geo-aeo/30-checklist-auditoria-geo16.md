---
titulo: Checklist — Auditoria GEO-16
versao: 1.0
data: 2026-04-25
tipo: checklist-operacional
uso: aplicado a toda página antes de publicação
---

# Checklist Operacional — Auditoria GEO-16

Checklist binário (sim/não) aplicado a toda página antes da publicação ou após reescrita. **Gate de aprovação:** G ≥ 0,70 e ≥ 12 pilares acionados. Páginas que falham vão para fila de reescrita seguindo o template em `31-checklist-reescrita.md`.

---

## Os 16 pilares

### Pilares críticos não-negociáveis (ausência bloqueia publicação)

- [ ] **1. metadata** — `<meta name="description">` 140–160 caracteres com entidade-âncora; `og:*` e `twitter:*` completos.
- [ ] **2. freshness** — `<meta property="article:modified_time">` ou `dateModified` JSON-LD presente. Limiares: ≤ 90 dias evergreen, ≤ 14 dias temas voláteis.
- [ ] **4. structured_data** — JSON-LD válido contra SHACL para o tipo aplicável (Article, FAQPage, HowTo, Product, Organization). `sameAs` linka entidades a Wikidata QIDs.

### Pilares estruturais (ausência reduz G mas não bloqueia)

- [ ] **3. semantic_html** — único `<h1>`, hierarquia consistente, uso correto de `<article>`, `<section>`, `<aside>`, `<nav>`. Sem `<div>` substituindo elementos semânticos.
- [ ] **5. headings** — todos os `<h2>`/`<h3>` respondem perguntas (não rótulos genéricos como "Introdução").
- [ ] **6. answer_blocks** — bloco AEO de 40–80 palavras autocontidos imediatamente após cada `<h2>`/`<h3>`.
- [ ] **9. faq** — `FAQPage` JSON-LD presente quando aplicável, com 3–7 pares pergunta/resposta autocontidos.
- [ ] **11. schema_jsonld** — JSON-LD completo (não apenas `Article` mínimo) com `author`, `datePublished`, `dateModified`, `inLanguage`, `keywords`.
- [ ] **12. canonical** — `<link rel="canonical">` presente e correto.
- [ ] **13. internal_links** — pelo menos 3 links internos contextuais por página.

### Pilares de descoberta (autoridade e densidade)

- [ ] **7. entity_density** — densidade de 1 entidade nomeada a cada 100 palavras, com ≥ 30% linkadas a Wikidata/arXiv/site oficial na primeira menção.
- [ ] **8. citations_out** — ≥ 1 link externo a cada 250 palavras, priorizando `.gov`, `.edu`, arXiv, DOI.
- [ ] **10. authority_signals** — autor identificado com credencial verificável (`schema:Person` com `sameAs`), ORCID quando aplicável.

### Pilares de acessibilidade e indexação

- [ ] **14. media_alt** — *alt text* denso (≥ 15 palavras descritivas) em todas as imagens.
- [ ] **15. accessibility** — contraste ≥ 4.5:1, *focus indicators*, ARIA labels onde necessário.
- [ ] **16. llms_txt** — `/llms.txt` E `/readme_ai.json` na raiz do domínio.

---

## Pesos sugeridos para cálculo de G

Os pesos devem ser configurados conforme o perfil do site, mas a literatura sugere distribuição:

| Pilar | Peso |
|---|---|
| metadata | 0,10 |
| freshness | 0,10 |
| structured_data | 0,10 |
| schema_jsonld | 0,08 |
| answer_blocks | 0,08 |
| llms_txt | 0,07 |
| entity_density | 0,07 |
| citations_out | 0,07 |
| headings | 0,06 |
| semantic_html | 0,05 |
| authority_signals | 0,05 |
| internal_links | 0,05 |
| canonical | 0,04 |
| faq | 0,04 |
| media_alt | 0,02 |
| accessibility | 0,02 |
| **Soma** | **1,00** |

---

## Exemplo de auditoria

Página `https://exemplo.com/artigo-x` auditada:

| Pilar | Status | Pontuação |
|---|---|---|
| metadata | ✓ | 0,10 |
| freshness | ✓ | 0,10 |
| semantic_html | ✓ | 0,05 |
| structured_data | ✓ | 0,10 |
| headings | ✗ | 0,00 |
| entity_density | ✓ | 0,07 |
| citations_out | ✓ | 0,07 |
| authority_signals | ✓ | 0,05 |
| answer_blocks | ✗ | 0,00 |
| faq | ✗ | 0,00 |
| schema_jsonld | ✓ | 0,08 |
| canonical | ✓ | 0,04 |
| internal_links | ✓ | 0,05 |
| media_alt | ✓ | 0,02 |
| accessibility | ✓ | 0,02 |
| llms_txt | ✗ | 0,00 |

**G = 0,75 — pilares acionados = 12 — APROVADO**

Mas com observação: pilares ausentes (headings genéricos, answer_blocks ausentes, llms.txt) devem entrar em backlog para reescrita futura.

---

## Comandos automáticos para auditoria

```bash
# Validar JSON-LD via SHACL
python -m pyshacl -s schemaorg.shapes.ttl -f turtle pagina.jsonld

# Validar llms.txt
curl -I https://exemplo.com/llms.txt | head -1
curl -I https://exemplo.com/readme_ai.json | head -1

# Contar densidade de entidades (NER)
python -m spacy download pt_core_news_lg
python scripts/audit_entity_density.py pagina.html

# Listar outlinks
curl -s pagina.html | grep -oP 'href="https?://[^"]+"' | sort -u
```

---

## Quando reauditar

- **Após qualquer edição** que altere headings, JSON-LD ou meta tags.
- **A cada 90 dias** em conteúdo evergreen (validar freshness).
- **A cada 14 dias** em temas voláteis (notícias, lançamentos).
- **Quando o engine-alvo principal mudar de modelo** (ex.: ChatGPT migra de gpt-4o para gpt-5).

---

## Quando uma página falha o gate

Se G < 0,70 ou pilares acionados < 12:

1. Listar pilares ausentes em ordem de peso.
2. Encaminhar para reescrita seguindo `31-checklist-reescrita.md`.
3. Não publicar atualizações até regate.
4. Se reescrita adicionar gating crítico (1, 2, 4) → deploy imediato após validação.
