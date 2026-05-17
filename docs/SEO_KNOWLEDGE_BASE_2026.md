# SEO Knowledge Base 2026 — curso-factory

> Versão 1.0 · 17-05-2026 · Owner: Brasil GEO (Alexandre Caramaschi — CEO da Brasil GEO, ex-CMO da Semantix (Nasdaq), cofundador da AI Brasil)
> Fonte: Wave 2 da pesquisa GEO/SEO 2026 (Perplexity sonar-deep-research + WebFetch validação)
> Como usar: anexe como contexto em prompts sobre SEO técnico, conteúdo educacional e estratégia de visibilidade orgânica.

---

## Índice

0. [Sumário executivo](#0-sumário-executivo)
1. [Timeline cronológica dos updates do Google em 2026](#1-timeline-cronológica-dos-updates-do-google-em-2026)
2. [AI Overviews em 2026 — o que mudou](#2-ai-overviews-em-2026--o-que-mudou)
3. [E-E-A-T 2026 — o sinal de autoridade no centro](#3-e-e-a-t-2026--o-sinal-de-autoridade-no-centro)
4. [Best practices técnicas SEO 2026](#4-best-practices-técnicas-seo-2026)
5. [Conteúdo educacional brasileiro — ameaças e oportunidades](#5-conteúdo-educacional-brasileiro--ameaças-e-oportunidades)
6. [Convergência SEO ↔ GEO para curso-factory](#6-convergência-seo--geo-para-curso-factory)
7. [Anti-padrões SEO 2026](#7-anti-padrões-seo-2026)
8. [Checklist trimestral de auditoria SEO](#8-checklist-trimestral-de-auditoria-seo)
9. [Apêndice A — Glossário de 25 termos canônicos](#9-apêndice-a--glossário-de-25-termos-canônicos)
10. [Apêndice B — Citações com URLs](#10-apêndice-b--citações-com-urls)

---

## 0. Sumário executivo

**Tese 1 — O eixo deslocou do "documento" para o "agente epistêmico".** O Google deixou de avaliar páginas isoladas e passou a avaliar quem produz, com qual evidência, e com qual rastreabilidade entitária. O core update de março de 2026 reponderou três dimensões simultaneamente: originalidade da informação (Information Gain), expertise do autor (E-E-A-T) e coerência tópica do domínio inteiro ([Search Engine Land](https://searchengineland.com/march-2026-google-core-update-what-changed-474397) · [Amsive](https://www.amsive.com/insights/seo/google-march-2026-core-update-winners-losers-analysis/)). Implicação para curso-factory: um curso vendido como ativo único hoje compete contra um curso ancorado em pessoa real verificável, com publicações, schema Person `sameAs` para LinkedIn/Wikidata/ORCID, e prova de experiência de campo. Quem não opera em camada entitária some.

**Tese 2 — A visibilidade está bifurcada em duas superfícies que pagam de modos diferentes.** Existe agora um web tradicional (links azuis, CTR clássico) e um web AI-first (AI Overviews + AI Mode + ChatGPT + Perplexity + Gemini) que não devolvem clique mas devolvem citação. A análise da Digiday mostra queda de 25% no tráfego de referência editorial só pelos AI Overviews ([Digiday](https://digiday.com/media/google-ai-overviews-linked-to-25-drop-in-publisher-referral-traffic-new-data-shows/)). A Search Engine Journal documentou CTR caindo 61% em queries com AIO, sem colapso absoluto de cliques — porque os poucos cliques restantes concentram-se nas URLs citadas dentro do bloco ([SEJ](https://www.searchenginejournal.com/ai-overview-ctr-fell-61-but-clicks-didnt-collapse/572993/)). Implicação para curso-factory: KPIs precisam medir LLM mention rate, posição de citação em AIO e ghost ranking (quando o LLM cita seu curso e converte para concorrente), não apenas posição no SERP.

**Tese 3 — A penalidade não vem por "ser AI", vem por "ser derivativo em escala".** O spam update de 24 de março de 2026 e o core update subsequente derrubaram 50-80% do tráfego de sites que publicavam centenas de páginas AI por dia sem revisão humana, sem first-hand evidence e com alta similaridade semântica ([Digital Applied](https://www.digitalapplied.com/blog/scaled-content-abuse-2026) · [Digital Applied](https://www.digitalapplied.com/blog/information-gain-march-2026)). Conteúdo assistido por AI com edição humana forte, dados próprios e originalidade permaneceu intacto ou ganhou tráfego. Implicação para curso-factory: o pipeline editorial deve gerar páginas com pelo menos 1 das 5 dimensões de Information Gain (dado proprietário, evidência de primeira mão, framework original, autoria expert verificável, gancho de atualidade) — não basta produzir mais aulas, é preciso produzir aulas que ninguém mais tem.

---

## 1. Timeline cronológica dos updates do Google em 2026

**Tese contraintuitiva:** 2026 teve apenas dois core updates confirmados de janeiro a maio, mas a volatilidade do mês de março foi a maior desde agosto de 2024 ([SE Ranking via Digital Applied](https://www.digitalapplied.com/blog/google-march-2026-core-update-impact-analysis-recovery)). Menos updates não significa menor impacto — significa que o Google está rodando continuous tuning entre os updates oficiais e reservando o anúncio público para mudanças estruturais.

**Evidência:** [Google Search Status Dashboard](https://status.search.google.com/products/rGHU1u87FJnkP6W2GwMi/history) (URL canônica validada via WebFetch) confirma os incidentes oficiais. [Search Engine Roundtable janeiro 2026](https://www.seroundtable.com/january-2026-google-webmaster-report-40696.html) e [abril/maio 2026](https://www.seroundtable.com/april-may-2026-google-webmaster-report-41251.html) cobrem os relatórios mensais de Webmaster.

**Mecanismo:** Googlers reiteraram em comunicações públicas que o Google agora roda "smaller, unannounced core updates on a rolling basis" — ou seja, sinais de qualidade são ajustados continuamente, e o anúncio público só ocorre quando há recalibração ampla ([SE Roundtable janeiro 2026](https://www.seroundtable.com/january-2026-google-webmaster-report-40696.html)).

### Tabela 1.1 — Updates confirmados Google 2026 (jan-mai)

| Data início | Nome | Duração | Escopo | Geografia inicial | Foco declarado | Impacto medido |
|---|---|---|---|---|---|---|
| 05-fev-2026 09:00 PT | February 2026 Discover core update | ~21d 17h (terminou 27-fev 02:00 PT) | Apenas Google Discover (não web search) | EN-US apenas no rollout inicial | Local relevance + redução de clickbait + in-depth content de sites com expertise tópica | Clickbait perdeu 50-70% de impressions em Discover; local news e niche expert blogs ganharam ([SE Land](https://searchengineland.com/google-february-2026-discover-core-update-is-now-complete-469450)) |
| 24-mar-2026 | March 2026 Spam Update | ~19h30m | Site-wide spam policies | Global | Scaled content abuse + expired domain manipulation + site reputation abuse (políticas de mar/2024) | 50-80% queda em sites com publicação massiva de AI sem revisão ([Digital Applied](https://www.digitalapplied.com/blog/google-march-2026-spam-update-second-algorithm-change)) |
| 27-mar-2026 | March 2026 Core Update | ~12d 4h (concluiu 08-abr) | Web search global | Global | Information Gain + author E-E-A-T + topical coherence + composite CWV | 80% dos top-3 mudaram (vs 67% em dez/2025); Semrush volatility sensor 8.7/10 (recorde desde ago/2024) ([SE Land](https://searchengineland.com/google-march-2026-core-update-rollout-is-now-complete-473883) · [SEJ](https://www.searchenginejournal.com/googles-march-core-update-shifted-visibility-away-from-aggregators/573621/)) |
| Maio 2026 (múltiplas datas) | Refinamentos não-anunciados | n/a | Web search | Global | Continuação do tuning de Helpful Content + Information Gain | Movimento perceptível mas sem nome oficial; [SE Vendor](https://seovendor.co/google-may-2026-algorithm-updates/) e [Quantifimedia](https://www.quantifimedia.com/google-algorithm-update-may-2026-what-changed-and-how-it-impacts-your-rankings) reportaram volatilidade focada em conteúdo derivativo |

### Tabela 1.2 — Categorias vencedoras vs perdedoras no March 2026 Core Update

| Categoria | Vencedores | Perdedores |
|---|---|---|
| Travel | Redes hoteleiras, companhias aéreas, sites oficiais de parques/aeroportos | OTAs grandes, sites de review agregador (TripAdvisor, Yelp) |
| Jobs/Educação | Portais de carreira do próprio empregador, USAJobs.gov, BLS.gov | Job boards agregadores |
| Saúde | NIH, GoodRx, fontes clínicas especialistas | WebMD, Mayo Clinic, Cleveland Clinic (caíram em relativo aos primários institucionais) |
| Comércio/Comparação | Marcas first-party, sites de fabricante | Portais financeiros de comparação ampla |
| UGC/Social | n/a (todos perderam) | YouTube, Reddit, Instagram (perderam visibilidade orgânica) |
| Notícias/Discover | Local news com cobertura profunda, niche expert blogs | Clickbait, listicles, syndicated coverage |

Fonte agregada: [Amsive winners/losers](https://www.amsive.com/insights/seo/google-march-2026-core-update-winners-losers-analysis/) usando SISTRIX Visibility Index + Google Product Taxonomy.

**Implicação para curso-factory:** trilhas educacionais batem como "first-party content" quando produzidas pelo dono da metodologia (Alexandre, Brasil GEO, instrutor com credencial verificável). Trilhas que apenas reescrevem conteúdo público disponível em outros cursos rankearam pior depois do March 2026. Pipeline de aulas precisa priorizar metodologia proprietária + caso real + dado coletado dentro da operação.

### 1.1 Detalhamento do February 2026 Discover Core Update

Foi o **primeiro update confirmado de 2026** E a **primeira vez que o Google rotulou publicamente um core update como Discover-only**, separando explicitamente Discover de web search ([SE Land complete](https://searchengineland.com/google-february-2026-discover-core-update-is-now-complete-469450)). Os 3 objetivos declarados pelo Google ([Google Search Central — Feb 2026 Discover](https://developers.google.com/search/blog/2026/02/discover-core-update)):

1. **Local relevance:** elevar conteúdo de sites baseados no mesmo país do usuário
2. **Reduzir clickbait e conteúdo sensacionalista:** rebaixar headlines emocionais que prometem mais do que entregam
3. **Highlight in-depth content:** priorizar coverage profunda, original e oportuna de sites com expertise tópica demonstrada

**Modelagem topic-by-topic:** o Google explicitou no blog que avalia expertise por tópico, não por domínio inteiro. O exemplo oficial do blog: um site local de notícias com seção dedicada a jardinagem pode ser tratado como autoridade em jardinagem em Discover, mesmo cobrindo também esportes e política. Já um site de reviews de filmes que publica 1 artigo sobre jardinagem não será tratado como expert no tema. Implicação: **autoridade tópica não é binária ao nível do site, é multidimensional ao nível do cluster**.

**Cross-border impact:** publishers não-EUA que ganhavam tráfego US Discover via cobertura sindicalizada caíram. Publishers locais com cobertura profunda de comunidade, eventos locais, política local e questões de saúde regional ganharam ([Khalid SEO Feb 2026](https://khalidseo.com/february-2026-discover-core-update-traffic-drop/)). Padrão: a perda foi **step-change** (alinhada com o rollout), não gradual.

### 1.2 Detalhamento do March 2026 Spam Update (24-mar)

Atacou políticas anunciadas em **março de 2024** que só agora ganharam enforcement em escala industrial: scaled content abuse, site reputation abuse e expired domain manipulation ([Digital Applied Spam Update](https://www.digitalapplied.com/blog/google-march-2026-spam-update-second-algorithm-change) · [Link Building HQ](https://www.linkbuildinghq.com/blog/march-spam-update-2026/)).

**Padrões estruturais detectados pelo SpamBrain (sinais que o Google usa):**

- High semantic similarity em URLs (centenas de páginas variando apenas cidade ou produto)
- Templates onde só o nome muda
- AI-translated copies do mesmo conteúdo em dezenas de idiomas
- Quase zero first-hand evidence ou primary-source citations
- Velocity anomalies (publicação de >100 páginas/dia sem explicação editorial)
- Lack of authorship/entity signals (autor anônimo ou "redação")
- High bounce rate + short dwell time
- External link patterns indicativos de redes AI

**Crucial:** Google enforça contra **thin content em escala**, não contra AI per se. Conteúdo escrito à mão mas com baixo valor cai na mesma política. Conteúdo AI-assisted com editorial humano forte e originalidade não é penalizado ([Pravinkumar AI penalty myth](https://www.pravinkumar.co/blog/google-ai-content-penalty-myth-what-actually-matters-2026)).

### 1.3 Detalhamento do March 2026 Core Update (27-mar a 08-abr)

**Volatilidade recorde:** SE Ranking — 80% dos top-3 mudaram (vs 67% em dezembro/2025); 24% das páginas top-10 caíram fora do top-100. Apenas 20% dos top-3 mantiveram posição exata, e menos de 10% dos top-10 retiveram seu spot. Semrush volatility sensor: 8.7/10 — maior leitura desde agosto/2024.

**Três dimensões reponderadas simultaneamente:**

1. **Information Gain** (originalidade — ver seção 4.2)
2. **Author E-E-A-T** (autoria verificável — ver seção 3)
3. **Topical coherence** (coerência tópica ao nível do domínio)

**Composite CWV scoring** introduzido formalmente (antes era URL-level, agora é site-level — ver seção 4.1).

### 1.4 Padrão de recuperação observado

Recuperação técnica (CWV, indexabilidade, crawl): semanas. Recuperação de conteúdo e autoridade: **3-6 meses, e geralmente coincide com o próximo core update**, não com reversão imediata pós-rollout ([Digital Roots Media](https://www.digitalrootsmedia.com/blog/seo/google-march-2026-core-update-full-breakdown-after-rollout-completion-what-to-do-in-april/) · [Google core updates doc](https://developers.google.com/search/docs/appearance/core-updates)). Isso significa que sites afetados em março de 2026 provavelmente só veem recuperação completa no próximo core update (esperado set-out/2026 com base na cadência histórica).

**Perfil de recuperação bem-sucedido** ([Web Expand checklist](https://www.webexpand.co.uk/website-traffic-dropped-suddenly-the-2026-diagnostic-checklist-to-recover-your-rankings/) · [Digital Applied recovery plan](https://www.digitalapplied.com/blog/march-2026-core-update-ranking-drops-recovery-plan)):

- First-party data publicada (estudos próprios, surveys, dataset coletado)
- First-hand experience demonstrada (caso real, prova de uso, foto de processo)
- Original frameworks nomeados (metodologia proprietária registrada como tal)
- Topical ecosystem aligned (cluster de conteúdo coeso, internal linking semântico)
- Fast, stable UX (CWV composite passing em mobile)
- Entity clarity (About page detalhada, autoria verificável, Person/Organization schema)

### 1.5 Mai 2026 — refinamentos não-anunciados

Em maio, múltiplos refinamentos sem nome oficial mas claramente sentidos por trackers ([SE Vendor May 2026](https://seovendor.co/google-may-2026-algorithm-updates/) · [Quantifimedia](https://www.quantifimedia.com/google-algorithm-update-may-2026-what-changed-and-how-it-impacts-your-rankings) · [9to5Google May 2026 system updates](https://9to5google.com/2026/05/11/may-2026-google-system-updates/)). Padrão: continuação do reward para informação original, depreciação ainda mais agressiva de conteúdo derivativo, fine-tuning do Helpful Content classifier. Google Search Central blog cobriu posts editoriais "Optimizing for generative AI" (mai/2026), "Back button hijacking spam policy" (abr/2026) e "Inside Googlebot" (mar/2026) — confirmados via WebFetch da home do blog em [developers.google.com/search/blog](https://developers.google.com/search/blog).

---

## 2. AI Overviews em 2026 — o que mudou

**Tese contraintuitiva:** AI Overviews não destruíram o tráfego orgânico — concentraram-no. CTR caiu 61% nas queries com AIO, mas os cliques sobreviventes vão majoritariamente para as 3-5 URLs citadas dentro do bloco ([SEJ](https://www.searchenginejournal.com/ai-overview-ctr-fell-61-but-clicks-didnt-collapse/572993/)). Quem está dentro do bloco ganha 18-35% de CTR lift versus rankings equivalentes não-citados ([Digital Applied](https://www.digitalapplied.com/blog/featured-snippets-ai-overview-era-optimization-2026)). Quem está fora do bloco vê a base de cliques evaporar.

**Mecanismo:** AIO funciona como uma camada de curadoria que extrai 3-5 fontes do top do SERP, sintetiza a resposta, e mostra links "Further Exploration" abaixo. O usuário lê a síntese — se quiser aprofundar, clica num dos poucos links destacados. O resto do top-10 perde tráfego mesmo mantendo posição.

### 2.1 — Cinco mudanças confirmadas em 2026

| # | Mudança | Evidência | Fonte |
|---|---|---|---|
| 1 | Expansão linguística massiva: 200+ países, 40+ idiomas em AIO; ~100 idiomas em AI Mode | Google I/O 2025 anunciou 1.5B users/mês; meados de 2025 superou 2B (>50% da base global) | [Google blog](https://blog.google/products-and-platforms/products/search/ai-overview-expansion-may-2025-update/) · [ALM Corp](https://almcorp.com/blog/google-ai-mode-expands-53-languages-analysis/) |
| 2 | Cobertura de queries estabilizou em 15-16% (após pico de ~25% em meio-2025); verticais saúde/educação/B2B tech chegam a 31% | Ahrefs + BrightEdge tracking | [QuickSEO 60 data points](https://quickseo.ai/blog/google-ai-overviews-statistics-2026-60-data-points-every-seo-should-know) · [ALM Corp 9 industries](https://almcorp.com/blog/google-ai-overviews-surge-9-industries/) |
| 3 | Ads dentro de AIO (acima, abaixo e em alguns casos no próprio bloco) + extensão para AI Mode + "Direct Offers" piloto | 75M users em AI Mode com ads por 2026 | [Sharp Innovations](https://www.sharpinnovations.com/blog/2026/02/ads-in-google-ai-overviews/) · [Next Millennium Direct Offers](https://nextmillennium.com/blog/google-ai-mode-direct-offers/) · [Digital Applied 75M users](https://www.digitalapplied.com/blog/google-ai-mode-75m-users-ads-in-ai-results-2026) |
| 4 | Opt-out parcial via "publisher commitments" anunciado em 19-mar-2026; UK CMA e EU DMA forçando controles granulares | The Register cobriu o anúncio do publisher opt-out; UK CMA propôs pacote em jan/2026; EC abriu investigação antitrust formal em 2026 | [The Register](https://www.theregister.com/off-prem/2026/03/19/google-says-it-will-let-publishers-opt-out-of-ai-overviews/) · [UK CMA](https://www.gov.uk/government/news/cma-proposes-package-of-measures-to-improve-google-search-services-in-uk) · [Loyens Loeff EC investigation](https://www.loyensloeff.com/insights/news--events/news/the-european-commission-opens-formal-antitrust-investigation-into-googles-use-of-online-content-for-ai-purposes/) |
| 5 | AI Mode filter em Search Console: separa tráfego AI-gerado de orgânico tradicional, abrindo medição da "segunda superfície" | Função lançada em 2026 e documentada por Digital Applied | [Digital Applied schema strategies](https://www.digitalapplied.com/blog/schema-markup-after-march-2026-structured-data-strategies) |

### 2.2 — Padrões de citação por plataforma AI

Pesquisa da Profound mapeou que cada engine AI privilegia mixagens distintas de fontes ([Profound](https://www.tryprofound.com/blog/ai-platform-citation-patterns)):

| Plataforma | Fontes dominantes | Implicação |
|---|---|---|
| Google AI Overviews | Reddit + sites institucionais | Brand mentions em Reddit + Knowledge Panel forte importam |
| Perplexity | Reddit + diversas fontes editoriais | Cobertura ampla em mídia especializada |
| ChatGPT | Wikipedia dominante | Wikidata entity + Wikipedia page para a marca/pessoa é alavanca |
| Gemini (Google) | Mistura com viés para Google index | Forte sobreposição com SERP tradicional |

**Implicação para curso-factory:** otimização para AI Mention Rate exige presença distribuída em Reddit (com voz autêntica, não marketing), Wikipedia/Wikidata (entity verificada), e mídia editorial. O dashboard de prompts âncora da Brasil GEO já mede isso para a marca pessoal Alexandre — replicar lógica para curso-factory significa cada curso ter sua superfície entitária mapeada.

### 2.3 — CTR studies 2026 (números consolidados)

| Estudo | Métrica | Valor |
|---|---|---|
| Digiday | Queda no tráfego de referência editorial atribuível a AIO | -25% ([Digiday](https://digiday.com/media/google-ai-overviews-linked-to-25-drop-in-publisher-referral-traffic-new-data-shows/)) |
| SEJ | Queda de CTR em queries com AIO presente | -61% ([SEJ](https://www.searchenginejournal.com/ai-overview-ctr-fell-61-but-clicks-didnt-collapse/572993/)) |
| Sharp/Digital Applied | % de usuários que clicam em resultado orgânico com AIO presente | ~8% (vs ~15% sem AIO) ([Sharp Innovations](https://www.sharpinnovations.com/blog/2026/02/ads-in-google-ai-overviews/)) |
| Digital Applied | CTR lift para URLs citadas dentro de AIO | +18-35% ([Digital Applied](https://www.digitalapplied.com/blog/featured-snippets-ai-overview-era-optimization-2026)) |

### 2.4 — Lawsuits e ações regulatórias 2026

Frente legal ativa contra AIO em 2026:

- **Penske Media v. Google** (EUA): ação por uso editorial sem compensação ([Lawfold](https://lawfold.com/google-ai-overviews-lawsuit-news/))
- **Leovy v. Google** (Baker Law): class action de autores/ilustradores por copyright ([Baker Law](https://www.bakerlaw.com/leovy-v-google/))
- **NYT v. Perplexity** (dez/2025): copyright infringement ([Jurist](https://www.jurist.org/news/2025/12/new-york-times-sues-perplexity-ai-over-copyright-infringement/))
- **EU Commission**: investigação antitrust formal sobre uso de conteúdo online para IA (ip_26_825, ip_26_203) ([EC](https://ec.europa.eu/commission/presscorner/detail/en/ip_26_825))
- **UK CMA**: pacote de medidas para Google Search no UK (jan-2026) ([Gov.UK](https://www.gov.uk/government/news/cma-proposes-package-of-measures-to-improve-google-search-services-in-uk))
- **DMA** (16-abr-2026): comissão propôs compartilhamento de dados de search engine com terceiros ([DMA](https://digital-markets-act.ec.europa.eu/commission-proposes-measures-google-sharing-search-engine-data-third-parties-under-digital-markets-2026-04-16_en))

**Implicação para curso-factory:** se opera no mercado brasileiro, ainda não há regulação local equivalente (LGPD não cobre AIO especificamente). Mas o vetor regulatório global pode forçar Google a expandir opt-out — o que torna decisão de "estar dentro do AIO" estratégica e não default.

---

## 3. E-E-A-T 2026 — o sinal de autoridade no centro

**Tese contraintuitiva:** E-E-A-T não é uma checklist de ranking; é o output de um modelo de classificação que avalia se o autor existe como entidade verificável no grafo de conhecimento do Google. Páginas escritas por autores anônimos ou por "equipe editorial" perderam massivamente em 2026 ([Digital Applied EEAT](https://www.digitalapplied.com/blog/e-e-a-t-march-2026-google-rewards-experience-content-guide) · [Seomytics](https://seomytics.com/author-authority-ranking-signal-how-google-weighs-it-2026/)).

**Evidência:** A revisão de fevereiro de 2026 das Quality Rater Guidelines apertou os padrões para autoria verificável e tratamento explícito de AI-generated content ([SEO Defend](https://seodefend.com/google-february-2026-quality-rater-guidelines-update-what-changed-and-why-it-matters/) · [Bro Works](https://www.broworks.net/blog/googles-2026-search-quality-rater-guidelines-what-you-need-to-know/)). A SE Roundtable confirmou que o QRG segue sendo atualizado 2-3 vezes por ano ([SE Roundtable QRG](https://www.seroundtable.com/google-search-quality-raters-guidelines-update-40092.html)).

**Mecanismo:** o QRG não define ranking factors diretamente — ele treina o modelo que treina o modelo. Raters humanos avaliam SERPs usando o QRG, suas decisões alimentam datasets de calibração, e esses datasets ajustam pesos no ML de ranking. Mudança no QRG = mudança downstream nos sinais ([Grounding Page QRG](https://groundingpage.com/facts/google-search-quality-rater-guidelines/)).

### 3.1 — Três padrões de E-E-A-T 2026 com evidência

#### Padrão 1: Author entities com `sameAs` em múltiplas fontes externas

Knowledge Graph do Google contém >10 bilhões de entidades e >1 trilhão de fatos relacionando organizações, pessoas e conceitos ([Digital Applied EEAT](https://www.digitalapplied.com/blog/e-e-a-t-march-2026-google-rewards-experience-content-guide)). Schema.org Person canônico ([schema.org/Person](https://schema.org/Person)) usa as propriedades:

- `name`
- `jobTitle`
- `worksFor` → Organization
- `affiliation`
- `alumniOf`
- `sameAs` (LinkedIn, Wikidata, Wikipedia, ORCID, Google Scholar, GitHub, perfis acadêmicos) — [schema.org/sameAs](https://schema.org/sameAs)
- `knowsAbout` (tópicos de expertise)
- `image`
- `url`

Sem `sameAs` apontando para registros externos verificáveis, o Google não consegue resolver o autor como entidade no Knowledge Graph, e o conteúdo é avaliado como "anônimo" mesmo com byline visível ([Visibility Stack author entity](https://www.visibilitystack.ai/academy/content-engineering/author-entity)).

#### Padrão 2: Unlinked brand mentions como sinal de confiança AI

Análise da Artifakt Digital documenta que LLMs e Google AIO consideram **menções não-linkadas** da marca em fontes confiáveis como evidência de relevância entitária — não é mais necessário backlink para sinalizar autoridade, mas é necessário que a marca apareça em contextos de cobertura editorial ([Artifakt Digital](https://www.artifaktdigital.com/how-unlinked-brand-mentions-help-your-ai-visibility-strategy/)). Isso é particularmente relevante para curso-factory porque a maior parte das citações que sustentam autoridade educacional brasileira não envia backlink (menções em LinkedIn, podcasts, vídeos de YouTube, threads no X).

#### Padrão 3: AI Disclosure obrigatório para YMYL

FTC e desenvolvimentos legais recentes em 2026 exigem labeling explícito de conteúdo AI-generated em contextos sensíveis (saúde, finanças, jurídico) ([Dynamis LLP](https://www.dynamisllp.com/knowledge/ai-disclosure-in-2026-recent-developments-and-practical-steps-for-brands-and-influencers)). Para curso-factory, qualquer aula em vertical YMYL (psicologia, finanças, saúde) precisa indicar editorial oversight humano + autoria nomeada + disclosure de uso de AI assistance, sob risco de penalização tanto algorítmica quanto regulatória.

### 3.2 — Sinais de confiança convergentes (Google + LLMs)

A QRG é o documento que instrui raters humanos do Google a avaliar SERPs. Foi publicada publicamente pela primeira vez em **2015**, é atualizada **2-3 vezes por ano**, e embora não defina ranking factors diretamente, **shape o treinamento dos modelos de ML que definem**. As decisões dos raters alimentam datasets que treinam evaluation models, que por sua vez influenciam como os ranking systems pesam sinais de qualidade em escala ([Grounding Page QRG](https://groundingpage.com/facts/google-search-quality-rater-guidelines/)).

A revisão de fevereiro de 2026 ([SEO Defend Feb 2026](https://seodefend.com/google-february-2026-quality-rater-guidelines-update-what-changed-and-why-it-matters/)) apertou três áreas:

1. **Verifiable authorship:** raters agora penalizam ativamente páginas YMYL sem autor identificável + credenciais
2. **AI-generated content:** treatment explícito, exigindo disclosure quando aplicável e oversight humano demonstrável
3. **YMYL scope expansion:** novos sub-tópicos incluídos como YMYL (decisões financeiras pessoais granulares, saúde mental específica, jurídico cotidiano)

Pesquisa AI Marketing Labs ([AI Marketing Labs](https://ai-marketinglabs.com/lab-experiments/how-does-ai-decide-which-brands-to-trust-in-its-search-results)) + Contently ([Contently](https://contently.com/2025/12/29/the-emerging-signals-llms-use-to-trust-your-brand-top-10-platforms-for-2026/)) + Ziptie ([Ziptie](https://ziptie.dev/blog/google-ai-overviews-source-selection/)) confirmam que AIO, ChatGPT, Perplexity e Gemini convergem em 5 sinais:

1. **Entidades reconhecidas** (presença em Knowledge Graph e Wikidata)
2. **Structured data robusto** (Article, FAQPage, HowTo, Person, Organization)
3. **Original research** (estudos, dados próprios, pesquisas exclusivas)
4. **Transparent methodology** (como o dado foi coletado, qual o n, qual a margem)
5. **Cross-source corroboration** (a afirmação aparece em múltiplas fontes independentes)

**Conjuntos de citação AI são mais estreitos do que SERPs** ([Ziptie](https://ziptie.dev/blog/google-ai-overviews-source-selection/)) — ou seja, estar no top-10 não garante ser citado; é preciso ter densidade entitária superior.

---

## 4. Best practices técnicas SEO 2026

**Tese contraintuitiva:** o "Core Web Vitals" deixou de ser métrica de página e virou métrica de site composta. Falhar em 1 das 3 (LCP, INP, CLS) arrasta o score composto do site inteiro, mesmo que a página em questão esteja perfeita ([Digital Applied CWV](https://www.digitalapplied.com/blog/google-march-2026-core-update-impact-analysis-recovery)). Sites que falharam em pelo menos 1 CWV (especialmente LCP > 3s) perderam 8-23% mais tráfego do que competidores rápidos no March 2026 Core ([Digital Applied](https://www.digitalapplied.com/blog/google-march-2026-core-update-impact-analysis-recovery)).

**Evidência primária:** [web.dev/articles/vitals](https://web.dev/articles/vitals) (validado via WebFetch) confirma que CWV oficiais em 2026 seguem sendo LCP + INP + CLS. Sem nova métrica adicionada. Thresholds inalterados: LCP ≤2.5s, INP ≤200ms, CLS ≤0.1.

### 4.1 — Core Web Vitals composite scoring

| Métrica | Good | Needs Improvement | Poor | Fonte canônica |
|---|---|---|---|---|
| LCP (Largest Contentful Paint) | ≤2.5s | 2.5-4s | >4s | [web.dev/articles/lcp](https://web.dev/articles/lcp) |
| INP (Interaction to Next Paint) | ≤200ms | 200-500ms | >500ms | [web.dev/articles/inp](https://web.dev/articles/inp) |
| CLS (Cumulative Layout Shift) | ≤0.1 | 0.1-0.25 | >0.25 | [Google CWV doc](https://developers.google.com/search/docs/appearance/core-web-vitals) |

Field data é medido via Chrome UX Report (CrUX) — agregado do 75º percentil de usuários reais — e surfaceado no Search Console ([Upward Engine CWV 2026](https://upwardengine.com/blog/core-web-vitals-2026/)).

**Mudança operacional em 2026:** Site-level composite scoring. Antes, otimizar landing pages-chave bastava. Agora, falha em template global (ex: footer com CLS > 0.1 em todas as páginas) pesa contra o site inteiro ([Digital Applied mobile SEO](https://www.digitalapplied.com/blog/mobile-seo-2026-mobile-first-indexing-guide)).

### 4.2 — Information Gain como sinal dominante

Information Gain originou-se em [patente Google de 2020](https://patents.google.com) (citação no [Digital Applied Information Gain](https://www.digitalapplied.com/blog/information-gain-march-2026)). Em março de 2026 virou "primary discriminator in contested search spaces". Resultados medidos:

- **Vencedores (Information Gain alto):** proprietary data, original research, first-hand case studies — ganhos típicos de 15-25%
- **Perdedores (Information Gain médio):** conteúdo templated ou rewritten — quedas de 30-50%
- **Catastróficos (Information Gain baixo):** AI content farms genéricos — colapsos de 60-80%

**5 dimensões da rubrica Information Gain** ([Digital Applied](https://www.digitalapplied.com/blog/information-gain-march-2026)):

1. Proprietary data (dado que só você tem)
2. First-hand evidence (você viu/testou/mediu pessoalmente)
3. Original frameworks ou modelos conceituais (você nomeou e formalizou)
4. Expert attribution + verifiable authorship (autor real, com prova)
5. Freshness hooks (conexão explícita com eventos ou data cuts recentes)

**Shift crucial:** um artigo conciso de 600 palavras com 1 dado original pode ranquear acima de um guia de 3.000 palavras que parafraseia fontes públicas. Comprimento virou tie-breaker, não input primário.

### 4.3 — SSR vs JavaScript rendering (veredicto 2026)

| Estratégia | Recomendação | Razão | Fonte |
|---|---|---|---|
| SSR / SSG / ISR | Default | TTFB rápido, bom para CWV, indexação garantida | [Jasmine Directory](https://www.jasminedirectory.com/blog/server-side-rendering-ssr-vs-client-side-the-2026-verdict/) |
| Partial hydration (islands) | Emergente, recomendado para sites mistos | Hidrata só onde precisa (Astro, Qwik, Angular 18) | [Dev.to Angular 18](https://dev.to/playfulprogramming-angular/angular-18-improving-application-performance-with-partial-hydration-and-ssr-2nie) |
| CSR puro | Arriscado | Google renderiza JS mas com penalidade de crawl budget e LCP típico >2.5s | [Stackmatix JS SEO](https://www.stackmatix.com/blog/javascript-rendering-seo-best-practices) |
| Dynamic rendering | Depreciado | Google explicitamente removeu da documentação | [Google deprecation](https://developers.google.com/search/docs/crawling-indexing/javascript/dynamic-rendering) |

**Implicação para curso-factory:** o stack ideal é Next.js (SSR/ISR), Astro (islands) ou Remix. SPAs React puras (CRA, Vite SPA sem SSR) são bandeira vermelha em 2026.

### 4.4 — MUVERA multi-vector retrieval

MUVERA = "Making multi-vector retrieval as fast as single-vector search" ([Google Research blog](https://research.google/blog/muvera-making-multi-vector-retrieval-as-fast-as-single-vector-search/) · [arXiv 2504.01818](https://arxiv.org/abs/2504.01818)). Em deployment de produção no Google, permite que sistemas de retrieval usem multi-vector embeddings (mais ricos que single-vector) sem penalidade de performance.

**Mecanismo:** ao invés de mapear documento → 1 vetor, mapeia documento → N vetores (parágrafo, entidade, contexto). Permite scoring de relevância por sub-trechos. Para SEO, significa que parágrafos individuais com alta densidade entitária podem ser retornados isoladamente em AIO, mesmo se a página inteira não rankeia bem.

**Implicação para curso-factory:** cada parágrafo de aula deve poder existir isoladamente como answer chunk. Headings semânticos (H2/H3) + parágrafos auto-suficientes + entidades nomeadas no primeiro terço de cada bloco aumentam chances de citação em AIO.

### 4.5 — Hreflang multi-língua

Estudos mostram que maioria dos sites internacionais ainda misconfigura hreflang ([Digital Applied hreflang](https://www.digitalapplied.com/blog/international-seo-2026-hreflang-multilingual-guide) · [Geotargetly](https://geotargetly.com/blog/hreflang-tag-seo-guide)). Erros mais comuns:

1. **Falta de reciprocal annotations:** página A aponta para B, mas B não aponta para A
2. **Códigos incorretos:** `pt` (genérico) vs `pt-BR` (Brasil) vs `pt-PT` (Portugal) — usar sempre o mais específico
3. **Self-referencing missing:** página em pt-BR precisa ter `hreflang="pt-BR"` apontando para si própria
4. **Canonical conflitante:** hreflang aponta para variante, mas canonical aponta para outra
5. **Sitemap sem hreflang declarado:** alternativa preferida do Google para sites grandes

**Para curso-factory educação brasileira:** usar sempre `pt-BR` (não apenas `pt`) e, se houver variante para Portugal, declarar `pt-PT` separadamente. Se houver curso em inglês para alunos brasileiros, declarar `en-BR` ou `en-US` conforme público real.

### 4.6 — CDN: Cloudflare vs Vercel

| Recurso | Cloudflare | Vercel | Implicação SEO |
|---|---|---|---|
| Edge cache HTML | Sim (Workers Cache API) | Sim (Edge Network) | TTFB <100ms global |
| Brotli compression | Auto | Auto | Reduz payload ~20% vs gzip |
| HTTP/3 | Auto | Auto | RTT reduzido em conexões móveis |
| Image optimization | Polish, Mirage, Image Resizing | Image Optimization API | LCP otimizado |
| Edge functions | Workers | Edge Functions | SSR em <50ms |
| ISR | Via Workers manual | Nativo (Next.js) | Estático + dinâmico |
| Speed Insights | Web Analytics (limitado) | Speed Insights (CWV field data) | Monitoramento direto |
| Bot management | Avançado, mas atenção: bloqueios podem barrar Googlebot se mal configurado | Auto | Bot allow-list verificada |

Fontes: [Cloudflare SEO](https://developers.cloudflare.com/fundamentals/performance/improve-seo/) · [Vercel CDN](https://vercel.com/docs/cdn).

**Atenção operacional:** Cloudflare bot challenges (Turnstile, JS Challenge) podem bloquear Googlebot se a rule não tiver exceção para verified bots. Já incidente reportado em 2026 (referenciado em [Search Engine Land](https://searchengineland.com/seo-2026-higher-standards-ai-influence-web-catching-up-473540)).

### 4.7 — FastEmbed e embedding-based SEO tools

[FastEmbed (Qdrant)](https://github.com/qdrant/fastembed) é biblioteca Rust-based leve para embeddings, com integração LangChain ([LangChain FastEmbed](https://docs.langchain.com/oss/python/integrations/embeddings/fastembed)). Adoção crescente em pipelines RAG corporativas e em ferramentas SEO que comparam embedding do conteúdo do site com embedding da query — score de relevância semântica que prevê probabilidade de citação em AIO.

**Implicação para curso-factory:** rodar similarity scoring entre cada aula e os 25 prompts âncora do dashboard pode antecipar quais aulas são candidatas naturais a citação. Score baixo → reescrever para aumentar densidade entitária e match semântico com a query alvo.

### 4.8 — Featured snippets e citation optimization

Featured snippets continuam relevantes em 2026 mas mudaram de natureza: viraram **answer chunks para AIO** ([Digital Applied featured snippets](https://www.digitalapplied.com/blog/featured-snippets-ai-overview-era-optimization-2026)). Estrutura que funciona:

- Pergunta como H2 ou H3 (formato exato da query do usuário)
- Resposta direta nos primeiros 40-60 palavras logo abaixo do heading
- Tabela ou lista numerada se a resposta tem estrutura
- FAQPage schema validando o par Q&A
- Entidade primária mencionada nas primeiras 100 palavras da página

**KPI a monitorar:** % de queries que disparam featured snippet, % desses snippets onde a fonte é seu site, % de citações dentro de AIO onde sua URL aparece (1ª, 2ª, 3ª, 4ª, 5ª posição).

### 4.9 — HTTPS, security e trust signals técnicos

[Web Spider Solutions HTTPS 2026](https://webspidersolutions.com/why-https-matters-boost-security-rankings-trust-2026/) reitera que HTTPS é hard requirement (não diferencial). Em 2026, atenção adicional para:

- HSTS header com `includeSubDomains; preload`
- CSP (Content-Security-Policy) configurada (não bloqueia ranking diretamente mas evita mixed content que prejudica CWV)
- TLS 1.3 mínimo
- Certificado válido sem warnings de subdomain
- Bot management que distingue Googlebot/AI bots de tráfego abusivo (não bloqueia os primeiros)

---

## 5. Conteúdo educacional brasileiro — ameaças e oportunidades específicas

**Tese contraintuitiva:** o mercado brasileiro de cursos online tem mais oportunidades do que o americano em 2026 porque o gap de Information Gain é maior. Há pouco conteúdo educacional brasileiro com dado proprietário, first-hand evidence em português, e métricas locais. Quem produzir isso captura simultaneamente Google + AIO + ChatGPT + Gemini sem competir com a saturação anglófona.

### 5.1 — Cenário 1: Cursos YMYL (saúde, finanças, jurídico, psicologia)

**Ameaça:** AI Disclosure obrigatório (ver seção 3.1 padrão 3) + tratamento agressivo do Google contra AI-scaled content em verticais YMYL. Sites como WebMD perderam para NIH no March 2026; analogia brasileira seria curso de psicologia genérico perder para conteúdo do CFP, CRP, SBP. [NÃO CONFIRMADO se Google trata fontes regulatórias brasileiras (CFP, CFM, COFEN) como autoridades primárias equivalentes a NIH/CDC — não há estudo específico no research bruto]

**Oportunidade:** cursos com instrutor verificável (CRP, CRM, OAB), produzindo content que cita normativos brasileiros recentes (Portaria MS, Resolução CFM, Lei XX/2026), com dados de pesquisa de campo brasileira (não tradução de paper americano), ganham densidade entitária superior a qualquer concorrente AI-only.

**Ação para curso-factory:** todo curso YMYL deve ter: (1) Person schema do instrutor com `sameAs` para conselho regulatório, (2) referências a normativos brasileiros datados, (3) disclosure de uso de AI assistance, (4) Original research ou case study local com n e metodologia explícitos.

### 5.2 — Cenário 2: Cursos profissionalizantes técnicos (programação, design, marketing)

**Ameaça:** alta saturação de conteúdo educacional gratuito (YouTube, Reddit, dev.to). [Search Engine Journal](https://www.searchenginejournal.com/googles-march-core-update-shifted-visibility-away-from-aggregators/573621/) documenta que agregadores e UGC perderam visibilidade orgânica em março/2026 — mas isso não significa que o curso pago automaticamente ganhe, significa que first-party content de marca técnica reconhecida ganha.

**Oportunidade:** se o curso-factory operar como "first-party brand" para uma metodologia nomeada (ex: "Brasil GEO Method", "Caramaschi Framework"), ele entra na categoria vencedora. Cursos genéricos ("Aprenda Python do Zero") competem contra Google Cloud, Microsoft Learn, freeCodeCamp.

**Ação:** nomear a metodologia. Publicar a metodologia como framework citável. Ter Wikipedia entry da metodologia ou da pessoa criadora (Wikidata como mínimo). Schema CourseInstance + Person + Organization conectados.

### 5.2.1 — Subcenário: cursos com afiliação a comunidades técnicas

[TechCrunch, mai/2026](https://techcrunch.com/2026/05/06/google-updates-ai-search-to-include-expert-advice-from-reddit-and-other-web-forums/) reportou que Google agora inclui expert advice de Reddit e outros web forums no AI Search. Profound confirmou que Reddit é fonte dominante em AIO e Perplexity ([Profound](https://www.tryprofound.com/blog/ai-platform-citation-patterns)). Para curso-factory, isso significa:

- Subreddits técnicos brasileiros (r/brdev, r/marketingbr, r/financasbr) são canais GEO de alto leverage
- Instrutor com histórico longo de participação genuína nesses subreddits tem entity signal forte
- Curso que cita threads reais de Reddit como caso de estudo ancora-se em fonte que LLMs já trustam
- Política 9:1 (9 contribuições genuínas para cada 1 menção comercial) é regra de sobrevivência — Reddit shadowbana marketing disfarçado e isso destrói o sinal entitário inteiro

### 5.3 — Cenário 3: Cursos B2B/corporate (educação executiva, MBA)

**Ameaça:** AI Overviews em queries B2B atingem 31% de cobertura em verticais como educação e B2B tech ([QuickSEO](https://quickseo.ai/blog/google-ai-overviews-statistics-2026-60-data-points-every-seo-should-know)). Decisor que pesquisa "melhor MBA executivo SP" recebe síntese AI antes de ver lista de programas.

**Oportunidade:** entrar nas 3-5 URLs citadas dentro do bloco AIO. CTR lift de 18-35% para citados ([Digital Applied](https://www.digitalapplied.com/blog/featured-snippets-ai-overview-era-optimization-2026)) torna isso o KPI principal.

**Ação:** otimizar cada landing de programa para ser **answer chunk** auto-suficiente. Estrutura: H2 "O que é o MBA X" → parágrafo de 80-120 palavras com tese clara → tabela comparativa estruturada → FAQPage schema com 8-12 perguntas reais. [Digital Applied schema](https://www.digitalapplied.com/blog/schema-markup-after-march-2026-structured-data-strategies) detalha o padrão.

### 5.4 — Cenário 4: ghost ranking em educação

Já documentado como padrão emergente: LLM cita o conteúdo educacional gratuito da escola A (porque tem Information Gain) mas, na hora de recomendar onde estudar, sugere escola B (porque tem brand recognition maior). Resultado: escola A subsidia awareness da escola B.

**Mitigação:**

- Sempre incluir CTA pessoal na assinatura do autor ("Alexandre Caramaschi leciona X no curso Y")
- Conteúdo educacional gratuito deve nomear explicitamente o curso pago (não apenas a metodologia)
- Schema Course associado a Person (instrutor) e Organization (escola) com `provider` correto
- Construir brand search volume da escola — sem isso o LLM não trusta o nome em recomendação
- Medir ghost ranking rate trimestralmente (script que extrai URLs sugeridas pelos LLMs em prompts de "onde estudar X")

### 5.5 — Cenário 5: conteúdo educacional em pt-BR com tradução genérica

[Digital Applied hreflang](https://www.digitalapplied.com/blog/international-seo-2026-hreflang-multilingual-guide) e [Geotargetly](https://geotargetly.com/blog/hreflang-tag-seo-guide) documentam que tradução automática de conteúdo educacional (do inglês para pt-BR sem revisão local) é detectada como AI-translated copy e cai dentro da política de scaled content abuse mesmo quando o original é legítimo.

**Ação para curso-factory:** se traduzir material, marcar explicitamente como "traduzido de" + adicionar comentário editorial brasileiro (contextualização local, exemplo nacional, dado IBGE/CADE/CGU) que diferencie da versão original. Hreflang `en-US` ↔ `pt-BR` deve apontar para versões realmente equivalentes, não para tradução crua.

---

## 6. Convergência SEO ↔ GEO para curso-factory

**Tese contraintuitiva:** SEO e GEO não são canais separados; são duas medições do mesmo modelo subjacente de autoridade entitária. Quem otimiza só para SEO fica visível mas sem clique. Quem otimiza só para GEO fica citado mas sem venda. Quem otimiza ambos captura citação + clique no mesmo conteúdo.

### 6.1 — Matriz prática: o mesmo investimento, dois retornos

| Ativo | Retorno SEO | Retorno GEO | Como medir |
|---|---|---|---|
| Schema Person do instrutor com `sameAs` rico | Knowledge Panel + sitelinks | LLM cita o nome em answer quando query é sobre o tópico | GSC sitelinks + LLM mention rate em 25 prompts âncora |
| Original research publicado como página separada | Backlinks editoriais + Information Gain boost | ChatGPT/Perplexity citam o study quando perguntado sobre o tema | Backlinks Ahrefs + LLM citation tracking |
| FAQPage schema bem estruturado | Featured snippet + People Also Ask | AIO source extraction | GSC impressões em rich result + screenshots AIO |
| Glossário com 100+ termos definidos | Long-tail rankings | LLM busca definição canônica | GSC queries + LLM definition matching |
| Caso de cliente com nome real + métricas | Trust signal humano | LLM cita o caso como evidência | Conversão de leads + LLM mention de case |
| Wikipedia / Wikidata entry da marca | Knowledge Graph trust | ChatGPT trust (Wikipedia é fonte dominante para ChatGPT) | Profound citation pattern analysis |

### 6.2 — Two-surface measurement playbook

Fontes: [Profound](https://www.tryprofound.com/blog/ai-platform-citation-patterns) + [Digital Applied schema strategies](https://www.digitalapplied.com/blog/schema-markup-after-march-2026-structured-data-strategies).

| KPI | Onde medir | Frequência |
|---|---|---|
| Posição média no SERP | Search Console | Semanal |
| CTR por query | Search Console | Semanal |
| AI Mode filter clicks | Search Console (filtro AI Mode 2026) | Semanal |
| LLM mention rate (% de prompts âncora que citam a marca) | Profound, Peec, Otterly, ou script próprio rodando GPT-4o/Claude/Gemini/Perplexity | Semanal |
| LLM citation position (qual a posição da citação dentro da resposta) | Script próprio | Quinzenal |
| Ghost ranking rate (% de respostas que citam você mas linkam concorrente) | Análise manual + script de URL extraction | Mensal |
| Schema validation health | Schema Markup Validator + Rich Results Test | A cada deploy |
| CWV composite | PageSpeed Insights + CrUX + Search Console | Semanal |

### 6.3 — Para curso-factory operacionalmente

O repositório `curso-factory` produz cursos para múltiplos clientes (Herreira, Semijoias-Educa, GEO IPOG, dinheirodaminhaempresa, etc.). A convergência SEO↔GEO se aplica do seguinte modo por cliente:

1. **Identidade entitária do dono do conteúdo** (Person schema com `sameAs` para LinkedIn, conselho regulatório, Wikidata se possível)
2. **Identidade entitária da escola/marca** (Organization schema com `sameAs` para CNPJ no portal Receita Federal, redes sociais oficiais, parcerias)
3. **Identidade entitária do curso** (Course schema com `provider`, `instructor`, `educationalCredentialAwarded`)
4. **Estrutura answer-chunk** em cada landing de aula/módulo
5. **Original research por nicho** (pesquisa de campo brasileira, dataset de alunos com consentimento LGPD)
6. **Glossário canônico do nicho** (100+ termos)
7. **FAQPage por curso** (8-12 Q&As)
8. **AI Disclosure** em todo conteúdo gerado/assistido por IA

---

## 7. Anti-padrões SEO 2026

10 práticas que custam tráfego em 2026, com explicação curta:

1. **Mass AI-generated content sem editorial oversight** — 50-80% queda no March 2026 spam update ([Digital Applied](https://www.digitalapplied.com/blog/scaled-content-abuse-2026)).
2. **Conteúdo derivativo (rewrite de top-10)** — 30-50% queda mesmo escrito por humano se Information Gain baixo ([Digital Applied IG](https://www.digitalapplied.com/blog/information-gain-march-2026)).
3. **Páginas de autor sem `sameAs`** — autor não resolve no Knowledge Graph → conteúdo tratado como anônimo ([Visibility Stack](https://www.visibilitystack.ai/academy/content-engineering/author-entity)).
4. **Hreflang com `pt` genérico** (sem `pt-BR` ou `pt-PT`) — mistura sinais e fragmenta rankings ([Geotargetly](https://geotargetly.com/blog/hreflang-tag-seo-guide)).
5. **CSR puro sem SSR fallback** — LCP típico >2.5s + crawl budget penalty ([Jasmine Directory](https://www.jasminedirectory.com/blog/server-side-rendering-ssr-vs-client-side-the-2026-verdict/)).
6. **Dynamic rendering** — deprecated pelo Google ([Google deprecation](https://developers.google.com/search/docs/crawling-indexing/javascript/dynamic-rendering)).
7. **Cloudflare bot challenge bloqueando Googlebot** — incidentes reais em 2026 quando rule não tem exceção para verified bots.
8. **CLS em template global** (footer, header) — site-level composite score puxa o site inteiro para baixo ([Digital Applied CWV](https://www.digitalapplied.com/blog/google-march-2026-core-update-impact-analysis-recovery)).
9. **Clickbait em meta description e H1** — February 2026 Discover update removeu 50-70% das impressions de publishers clickbait ([Search Engine Land](https://searchengineland.com/google-february-2026-discover-core-update-is-now-complete-469450)).
10. **About page genérica + footer sem dados da empresa** — Disconnected Entity Hypothesis → Helpful Content classifier rebaixa o domínio inteiro ([Digital Applied EEAT](https://www.digitalapplied.com/blog/e-e-a-t-march-2026-google-rewards-experience-content-guide)).

---

## 8. Checklist trimestral de auditoria SEO

Use a cada 90 dias. Cada item idealmente passa em 95%+ das páginas.

### 8.1 Entidades e autoria (10 checks)

- [ ] Toda página de aula/artigo tem Person schema do autor com `name`, `jobTitle`, `worksFor`, `sameAs` (mínimo 3 links externos)
- [ ] `sameAs` inclui LinkedIn do autor
- [ ] `sameAs` inclui Wikidata do autor (se autor é figura pública)
- [ ] `sameAs` inclui conselho regulatório quando YMYL (CRP, CRM, OAB, etc.)
- [ ] Organization schema do site/marca tem `sameAs` para LinkedIn corporativo
- [ ] Organization schema tem `taxID` (CNPJ no formato XX.XXX.XXX/XXXX-XX)
- [ ] About page descreve quem é a empresa, quando foi fundada, sede física
- [ ] Footer tem dados completos (CNPJ, endereço, CNAE se aplicável)
- [ ] Author archive page existe para cada autor (URL única, agregando posts)
- [ ] Toda página tem byline visível com nome real do autor (não "Equipe Editorial")

### 8.2 Information Gain (5 checks)

- [ ] Cada página tem pelo menos 1 das 5 dimensões: proprietary data, first-hand evidence, original framework, expert attribution, freshness hook
- [ ] Páginas YMYL têm sempre dado próprio ou citação direta de normativo regulatório com data
- [ ] Estudos ou pesquisas próprias publicadas com metodologia explícita (n, período, instrumento)
- [ ] Frameworks proprietários nomeados e descritos como tal (ex: "Caramaschi Hook-Valor-Receipt")
- [ ] Conteúdo evergreen revisado a cada 6 meses com "Atualizado em" visível

### 8.3 Core Web Vitals composite (5 checks)

- [ ] LCP ≤2.5s em 75º percentil mobile (CrUX) para top 100 landing pages
- [ ] INP ≤200ms em 75º percentil mobile
- [ ] CLS ≤0.1 em 75º percentil mobile
- [ ] Template global (header, footer, modal) não causa CLS em nenhuma página
- [ ] PageSpeed Insights score ≥85 em mobile para top 20 landing pages

### 8.4 Rendering e crawl (5 checks)

- [ ] Stack é SSR, SSG, ISR ou partial hydration (não CSR puro)
- [ ] robots.txt permite Googlebot, Googlebot-Image, Googlebot-News
- [ ] robots.txt permite AI crawlers desejados (GPTBot, Claude-Web, PerplexityBot, etc.) — decisão consciente
- [ ] Cloudflare/CDN não bloqueia Googlebot via bot challenge
- [ ] llms.txt existe na raiz se quer fornecer guidance específica para LLMs

### 8.5 Internacionalização (3 checks)

- [ ] Hreflang usa códigos específicos (`pt-BR`, `en-US`, nunca apenas `pt` ou `en`)
- [ ] Hreflang tem reciprocal annotations (A→B e B→A)
- [ ] Hreflang tem self-referencing tag na própria página

### 8.6 Structured data (6 checks)

- [ ] Article schema em todo post longo
- [ ] FAQPage schema em landings com 5+ Q&As reais
- [ ] HowTo schema em tutoriais com passos numerados
- [ ] Course schema em landings de curso (com `provider`, `instructor`)
- [ ] BreadcrumbList schema em todas as páginas internas
- [ ] Schema validation: Rich Results Test passa em 100% das páginas amostradas

### 8.7 AI/LLM measurement (6 checks)

- [ ] Dashboard de 25 prompts âncora para a marca está rodando semanalmente
- [ ] LLM mention rate medido em ChatGPT, Claude, Gemini, Perplexity, Groq
- [ ] Ghost ranking rate medido (% de citações que linkam concorrente)
- [ ] Search Console AI Mode filter monitorado semanalmente
- [ ] Citation position dentro de AIO trackeada (1ª, 2ª, 3ª, 4ª, 5ª)
- [ ] Profound, Peec ou Otterly subscriptions ativos OU script próprio rodando

**Total: 40 checks.** Score esperado >90% em sites maduros, >75% em sites em construção.

---

## 9. Apêndice A — Glossário de 25 termos canônicos

| # | Termo | Definição |
|---|---|---|
| 1 | **AI Overviews (AIO)** | Bloco de resposta AI gerado pelo Google no topo do SERP, sintetizando informação de múltiplas fontes e mostrando 3-5 links "Further Exploration" |
| 2 | **AI Mode** | Interface conversacional do Google Search lançada em 2025-2026 com 75M usuários por 2026, suporta ~100 idiomas |
| 3 | **Composite CWV scoring** | Modelo introduzido em março 2026 onde LCP+INP+CLS são agregados num único score performance ao nível do site (não mais URL) |
| 4 | **CrUX (Chrome UX Report)** | Dataset público do Chrome com field data real de CWV no 75º percentil de usuários, surfaceado em PageSpeed Insights e Search Console |
| 5 | **CTR (Click-Through Rate)** | % de usuários que clicam num resultado dado X impressões; caiu 25-61% em queries com AIO conforme estudo |
| 6 | **Disconnected Entity Hypothesis** | Tese de que sites sem entidade verificável (About vaga, autoria anônima, sem `sameAs`) são classificados como unhelpful pelo Helpful Content classifier independente da qualidade textual |
| 7 | **E-E-A-T** | Experience, Expertise, Authoritativeness, Trustworthiness — framework do Google para avaliar qualidade de conteúdo, particularmente YMYL |
| 8 | **Entity authority** | Substituiu "domain authority" como conceito-chave em 2026; mede se a marca/autor existe como entidade verificável no Knowledge Graph dentro de um tópico específico |
| 9 | **First-hand experience** | Componente da Experience em E-E-A-T; conteúdo onde o autor mostra ter testado, vivido ou medido pessoalmente o que descreve |
| 10 | **Ghost ranking** | Padrão emergente onde LLM cita um conteúdo educacional de uma marca, mas redireciona intent transacional para concorrente mais conhecido |
| 11 | **Helpful Content System** | Sistema de classificação do Google (lançado 2022, incorporado ao core em mar/2024) que opera primariamente como demotion engine ao nível do domínio |
| 12 | **Hreflang** | Atributo HTML/HTTP/sitemap que sinaliza idioma+região de uma página para o Google; uso correto requer códigos específicos (pt-BR não pt) e reciprocal annotations |
| 13 | **Information Gain** | Sinal originado de patente Google 2020; mede quanto de informação nova uma página oferece além do que já existe no top do SERP. Em mar/2026 virou primary discriminator |
| 14 | **INP (Interaction to Next Paint)** | Métrica CWV substituindo FID em 2024; mede latência da próxima pintura após interação. Good ≤200ms |
| 15 | **Knowledge Graph** | Grafo de entidades e fatos do Google (>10B entidades, >1T fatos) que conecta pessoas, organizações, conceitos e suas relações |
| 16 | **LCP (Largest Contentful Paint)** | Métrica CWV; tempo até o maior elemento de conteúdo visível ser pintado. Good ≤2.5s |
| 17 | **LLM mention rate** | KPI GEO; % de prompts âncora em que a marca/pessoa é citada por nome em resposta de LLM (ChatGPT, Claude, Gemini, Perplexity) |
| 18 | **MUVERA** | Algoritmo Google Research 2025-2026 para multi-vector retrieval na velocidade de single-vector; permite scoring de relevância por sub-trechos |
| 19 | **Person schema** | Tipo schema.org canônico para representar pessoa (autor, instrutor, executivo); propriedades-chave: name, jobTitle, worksFor, sameAs, knowsAbout |
| 20 | **Quality Rater Guidelines (QRG)** | Documento público do Google que instrui raters humanos como avaliar SERPs; atualizado 2-3x/ano; treina indiretamente modelos de ranking |
| 21 | **sameAs** | Propriedade schema.org que aponta para registros externos da mesma entidade (LinkedIn, Wikidata, ORCID); essencial para resolução entitária no Knowledge Graph |
| 22 | **Scaled content abuse** | Política de spam do Google (formalizada mar/2024, enforced mar/2026) contra geração massiva de páginas sem valor real, independente do método (humano ou AI) |
| 23 | **Topical coherence** | Avaliação ao nível do domínio que mede se um site cobre seu tópico declarado com profundidade e consistência |
| 24 | **Two-surface visibility** | Modelo onde visibilidade se mede em duas camadas: SERP tradicional (rankings, CTR) e camada AI (citation rate, mention rate) |
| 25 | **YMYL (Your Money or Your Life)** | Categoria do QRG para tópicos sensíveis (saúde, finanças, jurídico, civic life) onde padrões de E-E-A-T são mais rigorosos |

---

## 10. Apêndice B — Citações com URLs

Fontes utilizadas neste documento, extraídas do research bruto da Wave 2 (Perplexity sonar-deep-research, 245 citações no total disponíveis em `docs/research/geo-seo-2026-wave/`).

### Google / fontes primárias (validadas via WebFetch)

1. [Google Search Status Dashboard](https://status.search.google.com/products/rGHU1u87FJnkP6W2GwMi/history)
2. [Google Search Central — February 2026 Discover core update](https://developers.google.com/search/blog/2026/02/discover-core-update)
3. [Google Search Central — core updates documentation](https://developers.google.com/search/docs/appearance/core-updates)
4. [Google Search Central — Core Web Vitals](https://developers.google.com/search/docs/appearance/core-web-vitals)
5. [Google Search Central — dynamic rendering (deprecated)](https://developers.google.com/search/docs/crawling-indexing/javascript/dynamic-rendering)
6. [Google Blog — AI Overview expansion May 2025](https://blog.google/products-and-platforms/products/search/ai-overview-expansion-may-2025-update/)
7. [Google Blog — AI updates March 2026](https://blog.google/innovation-and-ai/technology/ai/google-ai-updates-march-2026/)
8. [Google Blog — CMA response](https://blog.google/company-news/inside-google/around-the-globe/google-europe/cma-response/)
9. [Google Research — MUVERA](https://research.google/blog/muvera-making-multi-vector-retrieval-as-fast-as-single-vector-search/)
10. [Google Search Status — incident mYbNTqV1ytDc2fA8hUz4 (Feb Discover)](https://status.search.google.com/incidents/mYbNTqV1ytDc2fA8hUz4)
11. [Google Search Status — incident 7eTbAa2jWdToLkraZj5y (Mar Core)](https://status.search.google.com/incidents/7eTbAa2jWdToLkraZj5y)

### web.dev (validadas via WebFetch)

12. [web.dev — Core Web Vitals oficial](https://web.dev/articles/vitals)
13. [web.dev — INP thresholds](https://web.dev/articles/inp)
14. [web.dev — LCP thresholds](https://web.dev/articles/lcp)
15. [web.dev — CDN best practices](https://web.dev/articles/content-delivery-networks)

### Schema.org (canônicos)

16. [schema.org/Person](https://schema.org/Person)
17. [schema.org/sameAs](https://schema.org/sameAs)
18. [Google Search Central — structured data intro](https://developers.google.com/search/docs/appearance/structured-data/intro-structured-data)

### Search Engine Land

19. [Search Engine Land — March 2026 core update what changed](https://searchengineland.com/march-2026-google-core-update-what-changed-474397)
20. [Search Engine Land — March 2026 core update rollout complete](https://searchengineland.com/google-march-2026-core-update-rollout-is-now-complete-473883)
21. [Search Engine Land — February 2026 Discover core update complete](https://searchengineland.com/google-february-2026-discover-core-update-is-now-complete-469450)
22. [Search Engine Land — SEOs biggest threat in 2026](https://searchengineland.com/seos-biggest-threat-in-2026-your-own-organization-472281)
23. [Search Engine Land — SEO 2026 higher standards AI influence](https://searchengineland.com/seo-2026-higher-standards-ai-influence-web-catching-up-473540)
24. [Search Engine Land — entity-first content optimization guide](https://searchengineland.com/guide/entity-first-content-optimization)

### Search Engine Journal

25. [SEJ — AI Overview CTR fell 61% but clicks didnt collapse](https://www.searchenginejournal.com/ai-overview-ctr-fell-61-but-clicks-didnt-collapse/572993/)
26. [SEJ — Googles March core update shifted visibility away from aggregators](https://www.searchenginejournal.com/googles-march-core-update-shifted-visibility-away-from-aggregators/573621/)

### Search Engine Roundtable

27. [SE Roundtable — January 2026 Google Webmaster Report](https://www.seroundtable.com/january-2026-google-webmaster-report-40696.html)
28. [SE Roundtable — April/May 2026 Webmaster Report](https://www.seroundtable.com/april-may-2026-google-webmaster-report-41251.html)
29. [SE Roundtable — Google March 2026 spam update](https://www.seroundtable.com/google-march-2026-spam-update-41109.html)
30. [SE Roundtable — Quality Rater Guidelines update](https://www.seroundtable.com/google-search-quality-raters-guidelines-update-40092.html)

### Análises de terceiros (Digital Applied, Amsive, Profound)

31. [Profound — AI platform citation patterns](https://www.tryprofound.com/blog/ai-platform-citation-patterns)
32. [Digital Applied — E-E-A-T March 2026](https://www.digitalapplied.com/blog/e-e-a-t-march-2026-google-rewards-experience-content-guide)
33. [Digital Applied — Information Gain March 2026](https://www.digitalapplied.com/blog/information-gain-march-2026)
34. [Digital Applied — scaled content abuse 2026](https://www.digitalapplied.com/blog/scaled-content-abuse-2026)
35. [Digital Applied — March 2026 core update impact analysis](https://www.digitalapplied.com/blog/google-march-2026-core-update-impact-analysis-recovery)
36. [Digital Applied — schema markup after March 2026](https://www.digitalapplied.com/blog/schema-markup-after-march-2026-structured-data-strategies)
37. [Digital Applied — mobile SEO 2026 mobile-first indexing guide](https://www.digitalapplied.com/blog/mobile-seo-2026-mobile-first-indexing-guide)
38. [Digital Applied — international SEO 2026 hreflang multilingual guide](https://www.digitalapplied.com/blog/international-seo-2026-hreflang-multilingual-guide)
39. [Digital Applied — featured snippets AI overview era optimization 2026](https://www.digitalapplied.com/blog/featured-snippets-ai-overview-era-optimization-2026)
40. [Digital Applied — Google AI Mode 75M users ads](https://www.digitalapplied.com/blog/google-ai-mode-75m-users-ads-in-ai-results-2026)
41. [Digital Applied — Google March 2026 spam update](https://www.digitalapplied.com/blog/google-march-2026-spam-update-second-algorithm-change)
42. [Amsive — Google March 2026 core update winners losers](https://www.amsive.com/insights/seo/google-march-2026-core-update-winners-losers-analysis/)
43. [Digital Roots Media — March 2026 full breakdown](https://www.digitalrootsmedia.com/blog/seo/google-march-2026-core-update-full-breakdown-after-rollout-completion-what-to-do-in-april/)

### Stack rendering e CDN

44. [Jasmine Directory — SSR vs CSR 2026 verdict](https://www.jasminedirectory.com/blog/server-side-rendering-ssr-vs-client-side-the-2026-verdict/)
45. [Dev.to — Angular 18 partial hydration](https://dev.to/playfulprogramming-angular/angular-18-improving-application-performance-with-partial-hydration-and-ssr-2nie)
46. [Cloudflare — SEO improvement](https://developers.cloudflare.com/fundamentals/performance/improve-seo/)
47. [Vercel — CDN documentation](https://vercel.com/docs/cdn)
48. [Stackmatix — JavaScript rendering SEO best practices](https://www.stackmatix.com/blog/javascript-rendering-seo-best-practices)

### Hreflang e i18n

49. [Geotargetly — hreflang tag SEO guide](https://geotargetly.com/blog/hreflang-tag-seo-guide)
50. [Weglot — hreflang tag guide](https://www.weglot.com/guides/hreflang-tag)
51. [Contentful — international SEO guide](https://www.contentful.com/seo-guide/international-seo/)

### MUVERA e embeddings

52. [arXiv 2504.01818 — MUVERA paper](https://arxiv.org/abs/2504.01818)
53. [Qdrant FastEmbed GitHub](https://github.com/qdrant/fastembed)
54. [LangChain — FastEmbed integration](https://docs.langchain.com/oss/python/integrations/embeddings/fastembed)

### E-E-A-T e author entities

55. [SEO Defend — February 2026 QRG update](https://seodefend.com/google-february-2026-quality-rater-guidelines-update-what-changed-and-why-it-matters/)
56. [Bro Works — Google 2026 QRG what you need to know](https://www.broworks.net/blog/googles-2026-search-quality-rater-guidelines-what-you-need-to-know/)
57. [Grounding Page — Google Search Quality Rater Guidelines](https://groundingpage.com/facts/google-search-quality-rater-guidelines/)
58. [Visibility Stack — author entity content engineering](https://www.visibilitystack.ai/academy/content-engineering/author-entity)
59. [AI Marketing Labs — how AI decides which brands to trust](https://ai-marketinglabs.com/lab-experiments/how-does-ai-decide-which-brands-to-trust-in-its-search-results)
60. [Contently — emerging signals LLMs use to trust your brand 2026](https://contently.com/2025/12/29/the-emerging-signals-llms-use-to-trust-your-brand-top-10-platforms-for-2026/)
61. [Ziptie — Google AI Overviews source selection](https://ziptie.dev/blog/google-ai-overviews-source-selection/)
62. [Seomytics — author authority ranking signal 2026](https://seomytics.com/author-authority-ranking-signal-how-google-weighs-it-2026/)
63. [Dynamis LLP — AI disclosure 2026](https://www.dynamisllp.com/knowledge/ai-disclosure-in-2026-recent-developments-and-practical-steps-for-brands-and-influencers)
64. [Artifakt Digital — unlinked brand mentions AI visibility](https://www.artifaktdigital.com/how-unlinked-brand-mentions-help-your-ai-visibility-strategy/)

### Lawsuits e regulatório

65. [The Register — Google says publishers can opt-out of AI Overviews](https://www.theregister.com/off-prem/2026/03/19/google-says-it-will-let-publishers-opt-out-of-ai-overviews/)
66. [Lawfold — Google AI Overviews lawsuit news](https://lawfold.com/google-ai-overviews-lawsuit-news/)
67. [Baker Law — Leovy v. Google](https://www.bakerlaw.com/leovy-v-google/)
68. [Jurist — NYT sues Perplexity over copyright](https://www.jurist.org/news/2025/12/new-york-times-sues-perplexity-ai-over-copyright-infringement/)
69. [Loyens Loeff — EC formal antitrust investigation Google AI](https://www.loyensloeff.com/insights/news--events/news/the-european-commission-opens-formal-antitrust-investigation-into-googles-use-of-online-content-for-ai-purposes/)
70. [UK CMA — package of measures for Google Search](https://www.gov.uk/government/news/cma-proposes-package-of-measures-to-improve-google-search-services-in-uk)
71. [DMA — Commission proposes Google data sharing 2026](https://digital-markets-act.ec.europa.eu/commission-proposes-measures-google-sharing-search-engine-data-third-parties-under-digital-markets-2026-04-16_en)
72. [EC press corner — ip_26_825](https://ec.europa.eu/commission/presscorner/detail/en/ip_26_825)
73. [Digiday — Google AI Overviews 25% drop publisher traffic](https://digiday.com/media/google-ai-overviews-linked-to-25-drop-in-publisher-referral-traffic-new-data-shows/)

### Estatísticas e adoption

74. [QuickSEO — Google AI Overviews statistics 2026 60 data points](https://quickseo.ai/blog/google-ai-overviews-statistics-2026-60-data-points-every-seo-should-know)
75. [ALM Corp — Google AI Overviews surge 9 industries](https://almcorp.com/blog/google-ai-overviews-surge-9-industries/)
76. [ALM Corp — Google AI Mode expands 53 languages](https://almcorp.com/blog/google-ai-mode-expands-53-languages-analysis/)
77. [Sharp Innovations — ads in Google AI Overviews](https://www.sharpinnovations.com/blog/2026/02/ads-in-google-ai-overviews/)
78. [Next Millennium — Google AI Mode Direct Offers](https://nextmillennium.com/blog/google-ai-mode-direct-offers/)
79. [Upward Engine — Core Web Vitals 2026](https://upwardengine.com/blog/core-web-vitals-2026/)
80. [Evertune — March 2026 core update content best practices](https://www.evertune.ai/resources/insights-on-ai/googles-march-2026-core-update-a-content-best-practices-guide-for-seo-and-ai-search)

---

**Manutenção:** este documento deve ser revisado após cada core update confirmado do Google. Próxima revisão programada: setembro-outubro 2026 (provável próximo core update). Owner: Brasil GEO. Adicionar nova versão como `SEO_KNOWLEDGE_BASE_2026_v2.md` quando houver mudança estrutural.
