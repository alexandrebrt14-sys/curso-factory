# Templates SEO/GEO/AEO/B2A 2026

Templates prontos para deploy em portais editoriais alinhados ao incremento canônico de 20-05-2026.

**Ref canônica:** [`docs/SEO_GEO_INCREMENT_20260520.md`](../../SEO_GEO_INCREMENT_20260520.md) — leia primeiro o §11 (Templates prontos) e §13 (Anti-padrões 2026) antes de aplicar.

## Arquivos

| Arquivo | O que entrega | Quando usar |
|---|---|---|
| `robots-2026.txt` | robots.txt completo com 20+ user-agents IA (OpenAI retrieval/training/user + Anthropic + Perplexity + Google AI + Apple + Meta + Amazon + outros). Bytespider bloqueado por default. | Portal editorial de qualquer porte. Decisões training (GPTBot, ClaudeBot, CCBot, Google-Extended, Applebot-Extended, Meta-ExternalAgent) por política editorial — comentários inline mostram como trocar para Disallow. |
| `news-article-schema.jsonld` | NewsArticle em @graph aninhado conectando Article → Person → Organization → Wikidata IDs em mentions/about. Inclui Speakable em answer capsules. | Em toda página editorial. Critério 🟢 Onda 4. Schema-content parity obrigatória. |
| `paywall-schema.jsonld` | Paywall declarado conforme Google Search Central 2026 (isAccessibleForFree:false + hasPart WebPageElement cssSelector). | Conteúdo paywalled. NUNCA nest content sections. APENAS .class selectors no cssSelector. |
| `breadcrumb-schema.jsonld` | BreadcrumbList sitewide para páginas profundas. | Todas URLs com profundidade ≥2. |
| `llms.txt.template` | Template curado <200K tokens com Sobre/Autores/Verticais/Dados próprios/Optional. | **Opcional defensivo** (ROI direto marginal — 0,1% do tráfego de bot por OtterlyAI). Não confundir com requisito. |

## Aplicação no pipeline curso-factory

Esses templates podem ser distribuídos:

1. **Como recurso de aula** em módulos de curso "GEO/SEO 2026" (writer GPT-4o referencia o caminho relativo).
2. **Como ativo cliente** quando o portal cliente da curso-factory ingressa em onda de implementação SEO/GEO.
3. **Como contexto para o reviewer Claude** validar schema-content parity e adesão às regras Google 2026.

## Substituições obrigatórias antes de aplicar

Substitua `EXEMPLO.com.br` pelo domínio real do cliente. Em `news-article-schema.jsonld` substitua os Q-IDs Wikidata placeholders pelos reais (`Q12345` etc).

## Validação

- JSON-LD: [Schema.org validator](https://validator.schema.org/) + [Google Rich Results Test](https://search.google.com/test/rich-results).
- robots.txt: [Google Search Console robots tester](https://www.google.com/webmasters/tools/robots-testing-tool) + verificação manual nos logs de servidor após deploy.
- llms.txt: nenhum validador oficial; verificar manualmente que não excede 200K tokens (~700KB).
