## Q3 content

[DRAFT]

# Schema.org Vocabulary Updates in 2025–2026 and their Relevance to AI Systems and Agents

The Schema.org vocabulary continues to evolve steadily, but the 2025–2026 releases do **not** introduce a dedicated family of AI‑ or agent‑specific types such as *Agent*, *AIPolicy*, *GenerativeAI*, *AIContent*, or *AIServiceProvider* into the core schema. Instead, the project has focused on incremental improvements to its general modeling capabilities, new equivalence mappings to other vocabularies, and domain‑specific additions, while the AI ecosystem has learned to rely on existing types such as **SoftwareApplication**, **Service**, **CreativeWork**, **Action**, and the **agent** property to describe AI tools and their behavior.[1][29][7] At the same time, search platforms and AI systems have tightened their expectations around structured data quality and narrowed the set of types that generate visible *rich results* in traditional search, even as they increasingly consume Schema.org data for answer generation and entity understanding.[15][22][28][39] There are no officially standardized Schema.org properties for crawler permissions; site owners still control AI and search crawling primarily through **robots.txt**, robots meta tags, and `X‑Robots‑Tag` headers rather than through JSON‑LD or Schema.org markup.[18][33][37][38] Validation infrastructure has bifurcated into two complementary pillars: the Schema Markup Validator at `validator.schema.org`, which checks conformance against the full vocabulary, and Google’s Rich Results Test, which tests a shrinking subset of Schema.org types for enhanced display eligibility.[28][15][36][7] This report synthesizes the official release notes, public issues, and adjacent SEO and AI guidance to clarify what Schema.org actually changed in 2025–2026, how AI and agents make use of those changes, what remains only at the level of proposal or third‑party speculation, and how practitioners should think about structured data, crawler control, and validation in an AI‑dominated search landscape.

## 1. Background: Schema.org, AI Systems, and the Myth of “AI Schema”

Schema.org was launched in 2011 as a joint initiative of Google, Bing, Yahoo, and Yandex to create a shared vocabulary for structured data on the web.[1][21] The core idea was to provide a standardized set of **types** (representing entities such as persons, organizations, products, and events) and **properties** (attributes and relationships) that publishers could embed into their pages so that machines could interpret content more reliably.[10][21] Over time, the vocabulary has grown to more than eight hundred types and nearly fifteen hundred properties, organized in a hierarchical fashion under the root type **Thing**, with subtrees for creative works, organizations, places, events, products, and a rich set of intangibles.[10][21] Crucially, Schema.org is agnostic about the consuming application; it is equally intended for search engines, recommendation systems, knowledge graphs, and—today—large‑scale generative AI agents.[1][21][28]

AI systems and agents, from conversational systems to shopping assistants, treat Schema.org as a kind of machine‑readable dictionary for the web.[2][12][28] JSON‑LD, the dominant serialization format, allows developers to embed self‑contained blocks of structured data into pages via `<script type="application/ld+json">`, declaring entities with `@type` and using a shared `@context` of `https://schema.org`.[12][15][23] AI crawlers and search engines parse these blocks, integrate them into internal knowledge graphs, and use them for tasks such as disambiguating entities, verifying claims against external sources, and constructing answer snippets or product comparisons.[2][15][22][28] As multiple SEO‑oriented analyses emphasize, AI systems do not currently rely on any special “AI schema”; instead, they consume the same Schema.org vocabulary that has long been used for classical SEO, but they depend more heavily on **entity depth**, rich interlinking between entities, and consistent identifiers.[2][15][23][15]

Within this landscape, it is natural for practitioners to wonder whether Schema.org has, or soon will have, a dedicated set of types for AI‑specific concepts such as *GenerativeAI* services, *AIContent* disclosures, *AIPolicy* pages, or *AIServiceProvider* organizations. GitHub issues within the Schema.org repository reflect similar community questions, including explicit proposals for vocabulary “helping sites declare generative AI technologies were used” and for a *WebPageSemanticRepresentation* type designed for AI agent consumption.[24][32][34] However, as of version 30.0 of Schema.org, published on 19 March 2026, these ideas remain at the level of discussion and have not become part of the official schema.[13][13][7] The authoritative release notes for 2025–2026 contain no mention of types named *Agent*, *AIPolicy*, *GenerativeAI*, *AIContent*, or *AIServiceProvider*, and the live schema browser at `schema.org` similarly lacks such entries.[1][13][7]

It is also important to distinguish between the **agent** property and the notion of an **Agent** type. Schema.org defines **agent** as a property of **Action**, representing “the direct performer or driver of the action (animate or inanimate).”[14][14][14] In other words, an AI assistant or software bot participating in an action can be indicated as the value of this property, typically as an instance of **Person**, **Organization**, or **SoftwareApplication**, but **agent** itself is not a standalone type and has been part of the vocabulary for many years rather than being a new AI‑specific addition.[14][14][14] Misunderstandings about an “Agent type” often arise from this naming.

Parallel to vocabulary evolution, the technical and policy environment surrounding crawling and content usage has changed significantly. The traditional Robots Exclusion Protocol, implemented via `robots.txt`, remains the primary control over whether search and AI crawlers may access particular paths, and it has recently been used by many sites to restrict access for generative AI bots specifically.[18][37][38] Google also continues to honor robots meta tags and `X‑Robots-Tag` headers for indexing and snippet behavior, but these mechanisms are independent of Schema.org and are interpreted by crawlers rather than by structured data parsers.[18][33] No official Schema.org property currently allows page‑embedded JSON‑LD to override or supplement robots rules for web crawlers.

Against that backdrop, the remainder of this report addresses four overarching questions. First, what exactly changed in the Schema.org vocabulary during the 2025–2026 releases, especially in areas that might impact AI and agents. Second, how can practitioners represent AI systems, AI‑generated content, and AI policies using existing Schema.org types and properties, in the absence of dedicated AI vocabulary. Third, how do crawler permissions, robots controls, and structured data interact in practice, and why are there still no Schema.org properties for

### Q3 citations
- https://schema.org
- https://www.jasminedirectory.com/blog/json-ld-masterclass-implementing-schema-for-ai-agents/
- https://schema.org/Service
- https://schema.org/permissions
- https://schema.org/releaseNotes
- https://github.com/schemaorg/schemaorg/discussions/4651
- https://schema.org/docs/releases.html
- https://github.com/schemaorg/schemaorg/blob/main/versions.json
- https://schema.org/Blog
- https://schema.org/docs/schemas.html
- https://schema.org/Event
- https://dev.family/blog/article/schemaorg-structured-data-how-to-teach-search-engines-to-understand-your-website
- https://schema.org/version/latest
- https://schema.org/agent
- https://www.digitalapplied.com/blog/schema-markup-ai-generation-guide-2026
- http://blog.schema.org/2013/08/vocabulary-for-describing-civic-services.html
- https://www.searchenginejournal.com/google-drops-faq-rich-results-from-search/574429/
- https://developers.google.com/crawling/docs/robots-txt/robots-txt-spec
- https://github.com/schemaorg/schemaorg/issues/4466
- https://schema.org/robots.txt
- https://www.schemaapp.com/schema-markup/guide-to-the-schema-org-vocabulary/
- https://neuronwriter.com/schema-markup-ai-agents-2026/
- https://www.digitalapplied.com/blog/schema-markup-types-complete-structured-data-reference
- https://github.com/schemaorg/schemaorg/issues/3391
- https://blog.schema.org
- https://docs.cloud.google.com/vertex-ai/generative-ai/docs/reference/rest/v1/Schema
- https://github.com/NirDiamant/GenAI_Agents
- https://www.wearetg.com/blog/schema-markup/
- https://schema.org/Property
- https://schema.org/releaseDate
- https://www.servicenow.com/docs/r/yokohama/intelligent-experiences/generative-ai-controller/configure-a-provider-for-a-generative-ai-capability.html
- https://github.com/schemaorg/schemaorg/issues
- https://developers.google.com/search/docs/crawling-indexing/robots-meta-tag
- https://github.com/schemaorg/schemaorg
- https://www.schemaapp.com/schema-markup/entity-governance-the-missing-layer-in-ai-ready-content-systems/
- https://validator.schema.org
- https://en.wikipedia.org/wiki/Robots.txt
- https://www.averi.ai/how-to/technical-geo-setup-schema-robots.txt-templates
- https://www.sacbee.com/news/business/article315102559.html
- https://github.com/json-schema-org/website/issues/197