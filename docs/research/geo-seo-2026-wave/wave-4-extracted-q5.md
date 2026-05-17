## Q5 content

[DRAFT]

Below is a consolidated 2025–2026 view of major *AI-related* crawlers and user agents, based only on documentation or reasonably credible third‑party references. I’ll separate:

- **Officially documented / strongly corroborated user agents**  
- **Legacy / commonly mentioned but now deprecated or uncertain strings**

Where something is uncertain, I mark it explicitly.

---

## 1. OpenAI

### 1.1 GPTBot

- **Operator**: OpenAI  
- **Primary purpose**:  
  - Large‑scale web crawling for *training* and improving OpenAI models (GPT‑4.x, GPT‑5, etc.).  
- **Typical default behavior**:
  - Respects `robots.txt`.  
  - Crawls pages from public web content and data partners.  
- **Robots.txt user-agent token (opt-out)**:
  - `GPTBot`  
- **Example robots.txt**:
  ```txt
  User-agent: GPTBot
  Disallow: /
  ```
- **Key source**: OpenAI GPTBot documentation (not in your snippets, but official and well known).  
  - https://platform.openai.com/docs/gptbot

---

### 1.2 OAI-SearchBot

- **Operator**: OpenAI  
- **Primary purpose**:
  - *Search / retrieval indexing* for tools like “Browse with Bing” / web‑connected GPT experiences (non‑training, retrieval index).  
- **Typical default behavior**:
  - Respects `robots.txt`.  
  - Usually fetches pages more selectively than GPTBot; focused on search/retrieval index.  
- **Robots.txt user-agent token (opt-out)**:
  - `OAI-SearchBot`  
- **Example robots.txt**:
  ```txt
  User-agent: OAI-SearchBot
  Disallow: /
  ```
- **Corroboration**:
  - Mentioned as one of OpenAI’s “indexing crawlers” in 2026 AI-crawler guides: EvolveAMZ: “OpenAI – GPTBot (training), OAI-SearchBot (index)” [6].  
    - https://evolveamz.com/ai-crawler-list-2026-ecommerce/

---

### 1.3 ChatGPT-User

- **Operator**: OpenAI  
- **Primary purpose**:
  - *Real-time, user-triggered fetching* when a ChatGPT user opens a URL or asks the model to “open” / “browse” a specific page.  
  - This is typically not broad crawling; it is one‑off fetches driven by user actions.  
- **Typical default behavior**:
  - Respects `robots.txt`.  
  - Much lower volume than GPTBot; fetches only URLs requested inside ChatGPT interfaces.  
- **Robots.txt user-agent token (opt-out)**:
  - `ChatGPT-User`  
- **Example robots.txt**:
  ```txt
  User-agent: ChatGPT-User
  Disallow: /
  ```
- **Corroboration**:
  - Listed in AI bot aggregators and 2026 ecommerce crawler configs as “real‑time fetcher” paired with GPTBot and OAI‑SearchBot [2][4][6].  
  - Nohacks 2026 landscape lists `GPTBot|OAI-SearchBot|ChatGPT-User` as OpenAI’s set [2].  
    - https://nohacks.co/blog/ai-user-agents-landscape-2026  
    - https://crawlercheck.com/directory/ai-bots  

---

## 2. Anthropic (Claude)

Anthropic has gone through a couple of generations of user‑agent tokens. According to sources like nohacks and crawlercheck, older tokens are deprecated.

### 2.1 ClaudeBot

- **Operator**: Anthropic  
- **Primary purpose**:
  - Main *training and retrieval* crawler for Claude models. Newer consolidated bot per Anthropic’s 2024 change.  
- **Typical default behavior**:
  - Respects `robots.txt`.  
  - Broad crawling of the public web and retrieval index building.  
- **Robots.txt user-agent token (opt-out)**:
  - `ClaudeBot`  
- **Example robots.txt**:
  ```txt
  User-agent: ClaudeBot
  Disallow: /
  ```
- **Corroboration**:
  - Nohacks: “Anthropic consolidated its crawler fleet in 2024 to three bots: ClaudeBot (training), Claude-User (user-triggered), Claude-SearchBot (retrieval indexing)” and notes that `anthropic-ai` and `claude-web` are deprecated [2].  
  - https://nohacks.co/blog/ai-user-agents-landscape-2026  

---

### 2.2 Claude-User

- **Operator**: Anthropic  
- **Primary purpose**:
  - *User-triggered fetcher* for Claude chat products, analogous to ChatGPT‑User: fetches URLs a user explicitly asks Claude to open or summarize.  
- **Typical default behavior**:
  - Respects `robots.txt`.  
  - Low-volume “on demand” fetching rather than systematic crawl.  
- **Robots.txt user-agent token (opt-out)**:
  - `Claude-User`  
- **Robots.txt example**:
  ```txt
  User-agent: Claude-User
  Disallow: /
  ```
- **Corroboration**:
  - Listed in crawlercheck’s AI bots live robots.txt snippet [4].  
  - Also referenced as part of Anthropic’s consolidated bots in the nohacks article [2].  
  - https://crawlercheck.com/directory/ai-bots  

---

### 2.3 Claude-SearchBot

- **Operator**: Anthropic  
- **Primary purpose**:
  - *Retrieval/search indexer* for Claude’s web-based answering and AI search features (real-time answer generation).  
- **Typical default behavior**:
  - Respects `robots.txt`.  
  - Crawls pages to maintain a fresh index for Claude’s retrieval.  
- **Robots.txt user-agent token (opt-out)**:
  - `Claude-SearchBot`  
- **Example robots.txt**:
  ```txt
  User-agent: Claude-SearchBot
  Disallow: /
  ```
- **Corroboration**:
  - Explicitly described as “Anthropic's retrieval crawler used for AI search systems and real-time answer generation” in CS‑Cart 2026 blog [8].  
  - Appears in crawlercheck snippet [4].  
  - https://www.cs-cart.com/blog/good-and-bad-crawling-bots-list/  
  - https://crawlercheck.com/directory/ai-bots  

---

### 2.4 Legacy Anthropic user agents (deprecated / not canonical now)

**Per nohacks** [2] and crawlercheck [4]:

- `anthropic-ai` – legacy  
- `claude-web` – legacy  

These are now considered deprecated; Anthropic recommends targeting the newer tokens (`ClaudeBot`, `Claude-User`, `Claude-SearchBot`) instead. Robots rules that only target `anthropic-ai` or `claude-web` may no longer affect current Anthropic traffic.

- **Robots.txt tokens (if you still want to include)**:
  ```txt
  User-agent: anthropic-ai
  Disallow: /
  User-agent: claude-web
  Disallow: /
  ```

---

## 3. Google AI Crawlers

Google has multiple interrelated bots.

### 3.1 Google-Extended

- **Operator**: Google  
- **Primary purpose**:
  - Opt‑out mechanism for *AI training and generative features* (e.g., Gemini) that rely on content initially fetched via Google’s standard crawlers.  
  - `Google-Extended` itself does not fetch; it’s a control token.  
- **Typical default behavior**:
  - By default, public content accessible to Googlebot can be used for AI products *unless* blocked by `Google-Extended` or other policy.  
- **Robots.txt user-agent token (opt-out)**:
  - `Google-Extended`  
- **Example robots.txt**:
  ```txt
  User-agent: Google-Extended
  Disallow: /
  ```
- **Official documentation**:
  - Google: “Control your content in generative AI with Google-Extended”  
    - https://developers.google.com/search/docs/crawling-indexing/google-extended  

---

### 3.2 Google’s common crawlers (Googlebot, Google-CloudVertexBot, etc.)

From Google’s official “common crawlers” list [1]:

- **Googlebot** (including `Googlebot` variations)  
  - **Operator**: Google  
  - **Purpose**: Standard search index crawling; also effectively underpins AI search/answers.  
  - **Robots token**: `Googlebot`  

- **Google-CloudVertexBot**
  - **Operator**: Google Cloud  
  - **Purpose**: Crawling for Vertex AI Search and related Google Cloud products.  
  - **Robots token**: `Google-CloudVertexBot`  

- **Google-Read-Aloud**, **Google-NotebookLM**, others  
  - **Operator**: Google  
  - **Purpose**: Specific products (e.g., read-aloud services, NotebookLM).  
  - **Robots tokens**: `Google-Read-Aloud`, `Google-NotebookLM`  

- **Official list**:
  - https://developers.google.com/crawling/docs/crawlers-fetchers/google-common-crawlers [1]

**Regarding “Gemini-Deep-Research”**  
I have not found an official user-agent string named `Gemini-Deep-Research` in Google’s published crawler lists as of the latest documentation I can see [1]. It appears in some third‑party discussions as a feature name, but I do not have a reliable, documented UA string to list. I would treat it as *not confirmed*.

---

## 4. Perplexity

### 4.1 PerplexityBot

- **Operator**: Perplexity AI  
- **Primary purpose**:
  - *Indexing crawler* for Perplexity’s answer engine.  
- **Typical default behavior**:
  - Respects `robots.txt`.  
  - Crawls broadly but within resource constraints.  
- **Robots.txt user-agent token (opt-out)**:
  - `PerplexityBot`  
- **Example robots.txt**:
  ```txt
  User-agent: PerplexityBot
  Disallow: /
  ```
- **Corroboration**:
  - Included in multiple 2025–2026 AI crawler lists [2][4][5][6].  
  - E.g., CrawlerCheck [4], SearchEngineJournal AI crawler list [5].  
  - https://crawlercheck.com/directory/ai-bots  
  - https://www.searchenginejournal.com/ai-crawler-user-agents-list/558130/  

---

### 4.2 Perplexity-User

- **Operator**: Perplexity AI  
- **Primary purpose**:
  - *Real-time user-triggered fetcher* when a Perplexity user clicks a link or when the system fetches content specifically for that query.  
- **Typical default behavior**:
  - Respects `robots.txt`.  
  - Lower volume, on-demand.  
- **Robots.txt user-agent token (opt-out)**:
  - `Perplexity-User`  
- **Example robots.txt**:
  ```txt
  User-agent: Perplexity-User
  Disallow: /
  ```
- **Corroboration**:
  - In crawlercheck [4], evolveamz [6], and nohacks [2] as Perplexity’s real-time fetcher.  

---

## 5. ByteDance / ByteSpider

### ByteSpider

- **Operator**: ByteDance (TikTok / related products)  
- **Primary purpose**:
  - Web crawler often associated with content discovery and potentially training for recommendation/AI systems.  
- **Default behavior**:
  - Typically identifies itself with user agent including `Bytespider` or `ByteSpider`.  
  - Generally respects `robots.txt`.  
- **Robots.txt user-agent token (opt-out)**:
  - `Bytespider` or `ByteSpider` (operators often include rules for both variants).  
- **Example robots.txt**:
  ```txt
  User-agent: Bytespider
  Disallow: /
  User-agent: ByteSpider
  Disallow: /
  ```
- **Corroboration**:
  - Frequently listed in “top bots” references and bot management vendors; see, e.g., DataDome bot list [9].  
  - https://datadome.co/bots/  

(There is no single canonical AI-specific doc for ByteSpider that I can locate; classification as “AI” is mainly by behavior and operator.)

---

## 6. Amazon

### Amazonbot

- **Operator**: Amazon  
- **Primary purpose**:
  - Web crawling powering Amazon Search, Alexa, and newer AI products such as Rufus.  
- **Default behavior**:
  - Respects `robots.txt`.  
  - Combined indexing / discovery crawler.  
- **Robots.txt user-agent token (opt-out)**:
  - `Amazonbot`  
- **Example robots.txt**:
  ```txt
  User-agent: Amazonbot
  Disallow: /
  ```
- **Corroboration**:
  - Listed as a major AI‑relevant crawler in ecommerce-focused references [6], as well as bot lists (DataDome, CrawlerCheck) [4][9].  

---

## 7. Apple

### Applebot & Applebot-Extended

- **Operator**: Apple  
- **Primary purpose**:
  - `Applebot`: General web crawler for Siri, Spotlight, and Apple’s search products.  
  - `Applebot-Extended`: Opt‑out mechanism for Apple’s generative AI / training use, similar conceptually to Google‑Extended.  
- **Default behavior**:
  - `Applebot` respects `robots.txt` and `robots` meta tags.  
  - `Applebot-Extended` provides fine‑grained control of how content is used for Apple’s generative features.  
- **Robots.txt user-agent tokens (opt-out)**:
  ```txt
  User-agent: Applebot
  Disallow: /
  User-agent: Applebot-Extended
  Disallow: /
  ```
- **Official documentation**:
  - Applebot support doc (includes Applebot-Extended) – Apple Support  
    - https://support.apple.com/en-us/HT204683  

---

## 8. Meta

### 8.1 Meta-ExternalAgent

- **Operator**: Meta (Facebook/Instagram)  
- **Primary purpose**:
  - Crawler / agent associated with Meta’s generative AI features and retrieval, including content used for answering questions.  
- **Default behavior**:
  - Intended to respect `robots.txt`.  
  - Used for AI features beyond pure link preview scraping.  
- **Robots.txt user-agent token (opt-out)**:
  - `meta-externalagent` (case varies in examples, but token is usually matched case-insensitively).  
- **Example robots.txt**:
  ```txt
  User-agent: meta-externalagent
  Disallow: /
  ```
- **Corroboration**:
  - Listed in multiple AI crawler compilations (nohacks [2], data protection tools [9]).  

---

### 8.2 Meta-ExternalFetcher (STATUS: uncertain)

- There are references in some third‑party sources to a `meta-externalfetcher` or similar bot name, but I do not have a clearly documented, official string with behavior defined the way `meta-externalagent` is.  
- I therefore cannot confidently include a canonical `Meta-ExternalFetcher` user agent string. If you need to be cautious, some admins opt to block `meta-` or `meta-external*` patterns, but that’s heuristic rather than documented.

---

## 9. Microsoft / Bing / Copilot

### 9.1 bingbot

- **Operator**: Microsoft  
- **Primary purpose**:
  - Core web crawler for Bing Search and for AI answers in Bing Chat / Copilot.  
- **Default behavior**:
  - Respects `robots.txt`.  
  - High-volume crawler.  
- **Robots.txt user-agent token (opt-out)**:
  - `bingbot`  
- **Example robots.txt**:
  ```txt
  User-agent: bingbot
  Disallow: /
  ```
- **Official documentation**:
  - https://www.bing.com/webmasters/help/which-crawlers-does-bing-use-8c184ec0  
- **SEJ example**:
  - Search Engine Journal includes a full UA string example for Bingbot [5].  
    - https://www.searchenginejournal.com/ai-crawler-user-agents-list/558130/  

### 9.2 Microsoft Copilot-specific user agent (STATUS: not clearly documented as separate)

- Microsoft describes Bingbot and other crawlers, but I do not have an official, distinct UA named “Microsoft Copilot” for crawling beyond the use of Bingbot for Copilot answers. Many references imply Copilot uses Bing’s existing index rather than its own new crawler UA.

---

## 10. Mistral

### MistralAI-User

- **Operator**: Mistral AI  
- **Primary purpose**:
  - User-triggered fetcher for Mistral-based chat/assistant products.  
- **Default behavior**:
  - Respects `robots.txt`.  
  - Low volume, per-query fetches.  
- **Robots.txt user-agent token (opt-out)**:
  - `MistralAI-User` (also variants like `mistralai-user` in some crawlers lists) [4].  
- **Example robots.txt**:
  ```txt
  User-agent: MistralAI-User
  Disallow: /
  User-agent: mistralai-user
  Disallow: /
  ```
- **Corroboration**:
  - Appears in crawlercheck list and dark‑visitors=Cf. resources cited in evolveamz [6] and crawlercheck [4].  

(Official, detailed documentation from Mistral on this crawler is limited, but the UA is widely observed.)

---

## 11. DuckDuckGo – DuckAssistBot

### DuckAssistBot

- **Operator**: DuckDuckGo  
- **Primary purpose**:
  - Crawler associated with DuckAssist and DuckDuckGo’s A

### Q5 citations
- https://developers.google.com/crawling/docs/crawlers-fetchers/google-common-crawlers
- https://nohacks.co/blog/ai-user-agents-landscape-2026
- https://www.humansecurity.com/learn/blog/crawlers-list-known-bots-guide/
- https://crawlercheck.com/directory/ai-bots
- https://www.searchenginejournal.com/ai-crawler-user-agents-list/558130/
- https://evolveamz.com/ai-crawler-list-2026-ecommerce/
- https://www.scraperapi.com/web-scraping/best-user-agent-list-for-web-scraping/
- https://www.cs-cart.com/blog/good-and-bad-crawling-bots-list/
- https://datadome.co/bots/