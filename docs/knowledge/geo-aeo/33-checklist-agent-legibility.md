---
titulo: Checklist — Agent Legibility (JSON-LD + MCP + Anti-Signals)
versao: 1.0
data: 2026-04-25
tipo: checklist-operacional
uso: aplicado a páginas de produto/serviço/curso
---

# Checklist Operacional — Agent Legibility

Cobre Instruções 26–30 da Parte 4 do manual. Aplicável a páginas de produto, serviço, curso ou qualquer recurso comercial que precisa ser **selecionável por agentes** no nível 4+ da Curva de Automação Agêntica.

---

## A — Schema.org `Product` / `Course` enriquecido (Instrução 26)

### Campos básicos (Schema.org clássico)
- [ ] `@type` — `Product`, `Course`, `Service` conforme aplicável.
- [ ] `name` — nome canônico, igual em todos os perfis.
- [ ] `description` — 140–250 caracteres com entidade-âncora no início.
- [ ] `image` — URL absoluta + `caption` + `width` + `height`.
- [ ] `brand` — `Organization` com `sameAs` para Wikidata + perfis canônicos.
- [ ] `aggregateRating` quando aplicável.

### Campos para nível 4+ (agent legibility)
- [ ] `eligibility` — quem pode comprar/se matricular (texto claro).
- [ ] `loyaltyProgram` — `ProgramMembership` se houver fidelidade.
- [ ] `serviceLevel` — SLA, atualizações, suporte.
- [ ] `replacementPolicy` — qual SKU equivale em ruptura, política de cancelamento.
- [ ] `offers.priceValidUntil` — data de expiração de preço.
- [ ] `offers.availability` — `InStock`, `LimitedAvailability`, `PreOrder`.

### Validação automática
- [ ] SHACL contra `schemaorg.shapes.ttl` retorna sem erros.
- [ ] Schema.org Validator (https://validator.schema.org) retorna 0 errors.
- [ ] Google Rich Results Test passa.

### Exemplo — `Course` para o `curso-factory`

```json
{
  "@context": "https://schema.org",
  "@type": "Course",
  "name": "Curso GEO para Executivos",
  "description": "Generative Engine Optimization aplicado: 10 módulos com auditoria GEO-16, plano de mídia conquistada e implementação MCP para C-level.",
  "provider": {
    "@type": "Organization",
    "name": "Brasil GEO",
    "sameAs": [
      "https://www.wikidata.org/wiki/Q138755507",
      "https://brasilgeo.ai"
    ]
  },
  "author": {
    "@type": "Person",
    "name": "Alexandre Caramaschi",
    "jobTitle": "CEO da Brasil GEO, ex-CMO da Semantix (Nasdaq), cofundador da AI Brasil",
    "sameAs": [
      "https://orcid.org/0009-0004-9150-485X",
      "https://www.wikidata.org/wiki/Q138755507"
    ]
  },
  "courseCode": "GEO-EXEC-2026",
  "educationalLevel": "Executive",
  "timeRequired": "PT12H",
  "eligibility": "Profissionais com 5+ anos em marketing digital ou liderança de produto",
  "serviceLevel": "Acesso vitalício, atualizações trimestrais alinhadas a novos papers",
  "replacementPolicy": "Reembolso integral em 7 dias",
  "offers": {
    "@type": "Offer",
    "price": "1497.00",
    "priceCurrency": "BRL",
    "availability": "https://schema.org/InStock",
    "priceValidUntil": "2026-12-31"
  }
}
```

---

## B — Endpoint MCP para o produto (Instrução 26 + 28)

- [ ] Servidor MCP rodando em domínio próprio (ex.: `/api/mcp`).
- [ ] Tool `getProductDetails(id)` retorna o mesmo conteúdo do JSON-LD.
- [ ] Tool `listAvailableSubstitutes(id)` retorna SKUs equivalentes em ruptura.
- [ ] Tool `checkEligibility(profile)` valida se o agente comprador é elegível.
- [ ] Tool `getServiceLevel()` retorna SLA legível por agente.
- [ ] CORS configurado para acesso por agentes externos.
- [ ] OAuth ou autenticação por *bearer token* quando há dados sensíveis.

### Estado atual do ecossistema Brasil GEO

- MCP `/api/mcp` ativo em alexandrecaramaschi.com com 4 tools (`getBusinessInfo`, `getLocation`, `contactUs`, `listCourses`).
- Tool `getCourseDetails(slug)` ainda não implementada — backlog.

---

## C — Anti-signals removidos (Instrução 27)

Auditoria contra rótulos que agentes **penalizam**:

- [ ] Sem "patrocinado", "sponsored", "promo" no JSON-LD.
- [ ] Sem "anúncio", "ad" em meta description.
- [ ] Sem "promocional" em copy de produto.
- [ ] Sem badges "patrocinado" em listagens.
- [ ] Para conteúdo orgânico: sem rotular como "guest post" sponsored.

---

## D — Endorsements de plataforma adicionados (Instrução 27)

- [ ] Selos verificados (Google Verified, Trustpilot Verified, etc.).
- [ ] Certificações listadas explicitamente em JSON-LD.
- [ ] Prêmios e reconhecimentos com `Award` schema.
- [ ] Rating agregado de plataforma com `aggregateRating`.
- [ ] Para produtos modais: marcar `hasMerchantReturnPolicy.merchantReturnDays`.

---

## E — VLM-friendly visual (Instrução 29)

- [ ] *Alt text* denso (≥ 15 palavras descritivas).
- [ ] Atributos visuais explícitos: cor, formato, material, contexto de uso.
- [ ] Casos de uso textualizados próximos à imagem.
- [ ] Imagens em alta resolução (≥ 1.500 px lado maior).
- [ ] WebP ou AVIF para performance, mas com fallback JPG/PNG.

### Exemplo de alt text adequado

❌ Ruim: "Logo Brasil GEO"

✅ Bom: "Logo da Brasil GEO em fundo escuro, tipografia em laranja minimalista, com slogan 'Generative Engine Optimization para o Brasil', usado em apresentações executivas e materiais institucionais 2026"

---

## F — KG próprio publicado (Instrução 29)

- [ ] Triplestore (Neo4j, GraphDB, Apache Jena, Stardog) configurado.
- [ ] **Entidades canônicas** representadas como nodos:
  - Pessoa (Alexandre Caramaschi, Q138755507)
  - Organização (Brasil GEO, Semantix, AI Brasil)
  - Produtos/Cursos (cada curso é entidade)
  - Papers e referências
- [ ] **Predicados RDF** seguindo Schema.org + Wikidata:
  - `schema:author`
  - `schema:about`
  - `schema:cites`
  - `schema:sameAs`
- [ ] Export RDF público em endpoint dedicado (ex.: `/data/kg.ttl`).
- [ ] SPARQL endpoint opcional para consulta direta.

---

## G — 3 camadas de indexação (Instrução 30)

### Camada 1 — léxica
- [ ] Termos canônicos do nicho aparecem com TF-IDF balanceado.
- [ ] Sem keyword stuffing.
- [ ] Sem ausência dos termos-âncora (ex.: "GEO" deve aparecer ≥ 3 vezes em página de GEO).

### Camada 2 — semântica
- [ ] Embeddings da página clusterizam corretamente com queries-alvo.
- [ ] Teste empírico com `text-embedding-3-large`: similaridade cosseno ≥ 0,75 com a query principal.
- [ ] Página não dispersa em múltiplos tópicos sem relação.

### Camada 3 — extrativa
- [ ] Cada chunk de 200–400 tokens é autocontido.
- [ ] Pode ser citado isolado sem perder sentido.
- [ ] Headings funcionam como *signposts* de chunk.
- [ ] Sem pronomes ambíguos cruzando fronteiras de chunk.

---

## H — *Threat model* mínimo para MCP server (Instrução 28)

Baseado nas 4 taxonomias de atacante de **MCP Landscape & Security** (arXiv:2503.23278):

- [ ] **Atacante 1 — input malicioso:** sanitização de todos os parâmetros recebidos por tools.
- [ ] **Atacante 2 — exfiltração:** rate limiting + audit log de todas as chamadas.
- [ ] **Atacante 3 — supply chain:** dependências do MCP server fixadas em `requirements.txt` com hashes.
- [ ] **Atacante 4 — escalada de permissão:** cada tool tem escopo mínimo necessário, sem acesso global.

---

## I — Validação final pré-deploy

- [ ] JSON-LD valida em SHACL + Google Rich Results.
- [ ] MCP server responde a `mcp.list()` retornando todas as tools.
- [ ] Anti-signals zerados (regex automático).
- [ ] Alt text auditado em todas as imagens.
- [ ] Endpoints retornam 200 com `Content-Type` correto.
- [ ] `dateModified` atualizado.

---

## Roadmap sugerido para implementação progressiva

| Trimestre | Entregável |
|---|---|
| **T1 atual** | A (Schema.org enriquecido) + B (MCP server com 4 tools básicas) + C (anti-signals removidos) |
| **T2** | D (endorsements) + E (VLM-friendly) + G (3 camadas) |
| **T3** | F (KG próprio publicado) + I (validação automática em CI) |
| **T4** | H (threat model formal) + avaliação de A2A |

---

## Tese deste checklist em uma frase

**No nível 4+, cada produto é uma API consumida por agentes. Schema.org é o swagger; MCP é a runtime. *Anti-signals* são o que tira você do shortlist do agente.**
