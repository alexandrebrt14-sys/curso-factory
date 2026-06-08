## Q1 content

[DRAFT]

Here’s a synthesis of what 2026 data actually shows about `llms.txt`, plus what’s known (and not known) about vendor positions and alternatives.

---

## 1. Measured llms.txt adoption in 2026

### 1.1 Overall web / large-scale crawls

Multiple independent 2025–2026 crawls converge on “roughly one in ten domains.”

**SE Ranking – 300,000-domain crawl**

- Sample: 300,000 domains across traffic tiers.  
- Finding: **10.13%** had an `llms.txt`.  
- Adoption flat across traffic tiers; high-traffic sites use it *slightly less*:

  - 0–100 monthly visits: **9.88%** adoption  
  - 1,001–5,000 monthly visits: **10.54%**  
  - 100,001+ monthly visits: **8.27%**  

- Cited in multiple 2026 syntheses, e.g.:

  - Signals blog: “Only 10.13% of sites have llms.txt” and “high-authority sites adopt *less* than small sites.”  
    https://signals.sh/blog/does-llms-txt-actually-work-adoption-reality  
  - Limy AI: “A SE Ranking study of 300,000 domains found a 10.13% adoption rate.”  
    https://limy.ai/blog/llms.txt-in-2026-the-full-guide  
  - Link Building HQ: “SE Ranking carried out a survey analyzing 300k domains. In it, they found that llms.txt had a 10.13% adoption rate.”  
    https://www.linkbuildinghq.com/blog/should-websites-implement-llms-txt-in-2026/  

These are all referencing the same SE Ranking study, but they align on ~10% adoption.

**OpenHermit “full guide” synthesis**

- Summarizes independent crawls (including SE Ranking) as:

  > “Adoption is low and not growing fast. Independent crawl studies place llms.txt adoption at roughly **10%** of scanned domains.”  
  https://www.openhermit.com/blog/llms-txt-guide  

### 1.2 Adoption specifically among highly cited / high-traffic sites

The key question you asked is: *What does adoption look like among the top ~10,000 or similarly “most-cited” websites?*  
There is no single canonical “top 10,000” llms.txt report, but several 2026 studies focus on **AI‑cited domains and top domains**. They all point in the same direction: adoption is **lower** among the sites LLMs actually cite.

#### Signals / ALLMO 2026 audit (citation-focused)

Signals summarizes ALLMO’s 2026 audit of AI citations:

- Sample: **94,614 cited URLs** from **11,867 AI responses**.  
- Finding: **Exactly 1** of those URLs used `llms.txt` (**0.00105693%** of cited URLs).  
- Domain-level: Among “the 50 most‑cited domains globally” only **1 runs an llms.txt (Target.com)**, and “**0 of the top 20 media and publishing domains** ship one.”  

Source:  
https://signals.sh/blog/does-llms-txt-actually-work-adoption-reality

This is a **citation-based** sample, not precisely “top 10,000 websites by traffic,” but it’s arguably more relevant for AI visibility. The core point: *among the most‑cited domains, llms.txt is almost nonexistent*.

#### Trakkr Research – 37,894 AI‑cited domains

Trakkr looked at domains that actually appear as citations in AI answers:

- Sample: **37,894 AI‑cited domains**, 337,362 citations, 882 citation snapshots.  
- Overall adoption in the corpus: **13.3%** had `llms.txt`.  
- Among the **top 50 cited domains** in that corpus, adoption was **6.0%**, i.e. *lower than the overall average*.

Source:  
https://trakkr.ai/trakkr-research/llmstxt-effect/facts/top-fifty-domain-adoption-is-even-lower-than-the-full-corpus

This “top 50” is a tiny subset, but it supports the same pattern as ALLMO: the more frequently AI models cite a domain, the less likely that domain is to use `llms.txt`.

#### Rankability – top 100 websites snapshot

Rankability’s ongoing tracker (note: only 30 domains scanned so far in their “top websites” set) reports:

- Top 100 websites (current sample: 30)  
- `llms.txt` adoption: **0.0%**  

Source:  
https://www.rankability.com/llms-report/

Their methodology is limited (small sample, top by what metric isn’t fully spelled out), but it aligns with the broader story: among the very largest, mainstream domains, adoption is extremely low.

#### BeRecommended – Fortune 500

BeRecommended looked at another “high‑importance” cohort:

- **7.4% of Fortune 500** deployed `llms.txt`.  
- Among AI crawlers, llms.txt was read in **0.1% of requests**.  

Source:  
https://berecommended.com/blog/llms-txt-worth-it-adoption-vs-reality-2026

### 1.3 Summary: “Top 10,000” reality

No public study explicitly publishes “llms.txt adoption across the top 10,000 websites by traffic” with a method like Tranco/Alexa/Similarweb. What we *do* have:

- Large generic crawl: **~10.1%** adoption overall (SE Ranking, 300k domains).  
- AI‑cited domain corpus: **13.3% overall; 6.0% among top 50 cited domains** (Trakkr).  
- ALLMO audit of 94,614 citations: essentially **zero presence** (1 URL with llms.txt) and **1 of 50 most‑cited domains** using it (Signals summary).  
- Top-website snapshots: **0% adoption in a 30‑site “top 100” sample** (Rankability); **7.4%** among Fortune 500 (BeRecommended).

Putting those together, the most defensible 2026 statement is:

- Across the broader web: **≈10% of domains** ship `llms.txt`.  
- Among the largest / most‑cited domains (top N by traffic or by AI citation count): adoption is **lower**, typically **0–8%** depending on the cohort.  
- There is **no published 2026 dataset specifically for “top 10,000 websites,”** but every high‑tier subset examined so far has *equal or lower* adoption than the ~10% baseline.

---

## 2. Does llms.txt improve AI citations?

Because this affects whether adoption matters, it’s worth summarizing the 2026 evidence.

**Signals / ALLMO 2026**

- ALLMO’s AI‑citation audit:

  > “ALLMO's parallel 2026 audit examined **94,614 cited URLs** across **11,867 AI responses** and found **exactly 1 llms.txt URL in the entire citation set – 0.00105693%**.”  

  > “That is ‘no statistical relationship with the outcome the file claims to improve.’”  

- Conclusion:

  > “Does llms.txt actually work for AI citations? **No – not in any of the 2026 studies we trust.** Two independent analyses … both came back with the same answer: **no measurable citation lift.**”  

Source:  
https://signals.sh/blog/does-llms-txt-actually-work-adoption-reality

**Codersera 2026 guide**

Codersera summarizes multiple studies and notes that when they modeled AI citation likelihood:

- An XGBoost model trained on citation data **performed better when llms.txt was *not* treated as a positive feature**, i.e. no evidence that `llms.txt` predicts more citations.  
- They describe `llms.txt` as a “**low‑cost, low‑yield bet**” for now.  

Source:  
https://codersera.com/blog/llms-txt-complete-guide-2026/

**Limy AI traffic analysis**

Limy looked at more than **500 million LLM bot traffic events** across monitored brands:

- Only **408** of those requests targeted `llms.txt`.  
- They call this “statistically negligible” among AI search crawler traffic.  
- Their explicit answer:

  > “The file is almost untouched by the bots that matter for AI search visibility… That’s the honest answer to ‘will llms.txt improve my AI search rankings?’ Today, in 2026: **no**.”  

https://limy.ai/blog/llms.txt-in-2026-the-full-guide

Overall: **2026 data does not show any measurable AI‑citation benefit from using llms.txt.**

---

## 3. Official positions from Anthropic, OpenAI, Google, Perplexity

There is *no* formal, standardized `llms.txt` spec adopted by major vendors; it’s a de‑facto community convention. 2026 public sources make three things quite clear:

1. **Major AI companies do not treat llms.txt as a standards-backed, guaranteed control surface.**  
2. **Their public documentation centers on robots.txt and meta tags / HTTP headers instead.**  
3. **Independent log analyses show that their crawlers rarely, if ever, fetch llms.txt.**

### 3.1 Anthropic

Anthropic’s documented controls (as of 2026) are:

- **Robots.txt** directives for their crawlers (e.g., `User-agent: Claude-Web` / `ClaudeBot` patterns).  
- Standard `robots` meta tags and related mechanisms.

Public statements and log analyses:

- Signals:

  > “The 2026 retrieval pipelines at OpenAI, Anthropic, and Google were built **without llms.txt in the loop**. For that to change, at least one of those engines would have to announce consumption, publish documentation, and start showing the file in their user-agent fetch patterns. **None of those signals have appeared.**”  
  https://signals.sh/blog/does-llms-txt-actually-work-adoption-reality  

- Limy:

  > “AI search crawlers are almost never fetching llms.txt… The file is almost untouched by the bots that matter for AI search visibility.”  
  https://limy.ai/blog/llms.txt-in-2026-the-full-guide

I’m not aware of any official Anthropic policy document or blog post that endorses `llms.txt` as a recognized standard. Anthropic’s control documentation focuses on robots.txt and related norms; if they start officially supporting `llms.txt`, they would need to publish that, and the 2026 studies explicitly note that such an announcement has **not** happened.

### 3.2 OpenAI

OpenAI’s relevant control surfaces (based on their public docs and industry summaries) are:

- **Robots.txt** (e.g., directives for `GPTBot`, `ChatGPT-User` style user-agents).  
- Standard **meta tags** (noindex/nofollow equivalents).  

In the 2026 secondary literature:

- Signals explicitly groups OpenAI with Anthropic and Google as **not using llms.txt in their retrieval pipelines** and having made **no announcement** of support:  
  https://signals.sh/blog/does-llms-txt-actually-work-adoption-reality  

- Limy’s crawler logs (500M events) showed essentially **no requests** from any major AI bot to `llms.txt`, implying OpenAI’s crawlers aren’t looking for it in a systematic way:  
  https://limy.ai/blog/llms.txt-in-2026-the-full-guide  

I’m not aware of any 2026 OpenAI engineering blog post or official spec stating they read `llms.txt`, and none of the empirical crawler studies report a meaningful OpenAI signal around the file.

### 3.3 Google (Search / AI Overviews / “AI Mode”)

Google’s official position is more explicit:

- 2026 SEO‑facing articles summarizing Google’s stance:

  - LBN Tech Solutions:

    > “Unlike robots.txt, [llms.txt] has **no standardization, no enforcement, and no adoption from major AI companies, **including Google, OpenAI, Meta, Anthropic** …”  
    https://lbntechsolutions.com/blogs/llms-txt-google-search-seo-guide/  

  - OpenHermit:

    > “On the consumer side, the major AI vendors have been **quiet** about whether they actively read llms.txt.”  
    https://www.openhermit.com/blog/llms-txt-guide  

- Google’s publicly documented crawling and AI visibility controls continue to emphasize:

  - `robots.txt`  
  - `X-Robots-Tag` HTTP headers  
  - page-level meta tags  

I’m not aware of any Google Search Central documentation or public Google blog that cites `llms.txt` as an officially supported mechanism in 2026.

### 3.4 Perplexity

Perplexity has been more open about AI crawling, but again, 2026 analyses do **not** show them treating `llms.txt` as a first‑class standard:

- Limy’s 500M‑event log analysis includes Perplexity’s crawlers in their “AI search crawlers” set and still finds only **408 requests** to `llms.txt` overall:  
  https://limy.ai/blog/llms.txt-in-2026-the-full-guide  

- Signals, OpenHermit, Codersera, and others all group Perplexity with the majors that *do not* currently treat `llms.txt` as a supported standard.

I haven’t seen a Perplexity engineering post that formally endorses `llms.txt` for crawl/answer control. Their published guidance focuses on robots.txt and fair-use compliance.

### 3.5 Overall vendor-position summary

Across Anthropic, OpenAI, Google, Perplexity:

- **No 2026 official spec** or standard from any of them that says: “We support `llms.txt` and interpret it in X way.”  
- Public and semi‑official guidance continues to lean on **robots.txt** and existing web standards.  
- 2026 **log‑level studies** (Limy; BeRecommended; Signals/ALLMO) show **near‑zero llms.txt fetches** by major AI crawlers.  
- Independent researchers consistently describe `llms.txt` as **not in the loop** for current AI retrieval pipelines.

---

## 4. Alternatives and adjacent proposals in 2026

You asked about several: `ai.txt`, `ai-policy.json`, `.well-known/ai-policy`, robots.txt extensions. None has the status of a formal, broadly adopted standard in 2026, but some are more active than others.

### 4.1 ai.txt

There are occasional blog posts proposing an `ai.txt` convention (patterned on robots.txt) to specify AI training and inference policies. However:

- I’m not aware of any **major AI vendor** officially adopting an `ai.txt` spec in 2026.  
- No credible adoption numbers or crawler-log studies show systematic `ai.txt` fetching.  
- None of the 2026 adoption reports (Signals, Limy, Trakkr, SE Ranking, etc.) treat `ai.txt` as a class with measurable impact.

So far, `ai.txt` remains more of a *proposal* than something with demonstrated traction.

### 4.2 ai-policy.json and .well-known/ai-policy

These refer to JSON-based machine-readable policy documents, often proposed under a `/.well-known/ai-policy` path or similar.

Current status (as reflected in 2026 sources):

- Several advocacy groups and governance conversations reference machine-readable AI use policies, sometimes in JSON under `.well-known`.  
- However, I’m not aware of:

  - A published, widely recognized **specification** for `ai-policy.json` / `.well-known/ai-policy` that has vendor buy‑in.  
  - Any large‑scale **crawler study** that measures adoption or crawler fetch rates for these paths.

Most 2026 technical/SEO‑oriented analyses simply **don’t mention** these formats, which is itself a signal that they have not achieved meaningful deployment in the mainstream web yet.

### 4.3 Robots.txt extensions & existing standards

In contrast, **robots.txt** and related mechanisms are firmly entrenched and actually supported by AI vendors:

- Multiple 2026 guides emphasize that:

  > “Unlike robots.txt, [llms.txt] has no standardization, no enforcement, and no adoption from major AI companies …”  
  https://lbntechsolutions.com/blogs/llms-txt-google-search-seo-guide/  

- AI bots including those from OpenAI, Anthropic, Google, and Perplexity have **documented user agents** and implement robots.txt semantics for those agents.  
- Some guidance suggests *using existing robots.txt conventions* (e.g., `User-agent: GPTBot`) rather than inventing new files.

In practice, the **only “alternative” with real traction** is “robots.txt plus AI-specific user-agent tokens,” not a brand-new file like `ai.txt`.

---

## 5. When llms.txt actually *is* useful in 2026

While it doesn’t affect AI search visibility, there *is* a narrow niche where `llms.txt` has real utility:

- **Developer documentation / B2A (business-to-agent) UX**

  - Signals:

    > “Ship it if you run a developer-documentation site and your users copy-paste context into LLMs. The single legitimate use case in 2026 is the Mintlify pattern … an `llms-full.txt` flat file saves them the scrape-and-clean step. That is a user-experience win for a technical audience, not a retrieval-side citation play.”  
    https://signals.sh/blog/does-llms-txt-actually-work-adoption-reality  

  - OpenHermit:

    > “Documentation-heavy sites adopt at higher rates because the format genuinely fits how their content is consumed by IDE agents and coding assistants.”  
    https://www.openhermit.com/blog/llms-txt-guide  

Here, `llms.txt` or `llms-full.txt` functions as a **content delivery convenience** for human developers and agent-like tools, not a signal to big AI crawlers.

---

## 6. Bottom-line answers to your specific

### Q1 citations
- https://signals.sh/blog/does-llms-txt-actually-work-adoption-reality
- https://trakkr.ai/trakkr-research/llmstxt-effect/facts/top-fifty-domain-adoption-is-even-lower-than-the-full-corpus
- https://limy.ai/blog/llms.txt-in-2026-the-full-guide
- https://www.rankability.com/llms-report/
- https://www.openhermit.com/blog/llms-txt-guide
- https://www.linkbuildinghq.com/blog/should-websites-implement-llms-txt-in-2026/
- https://codersera.com/blog/llms-txt-complete-guide-2026/
- https://lbntechsolutions.com/blogs/llms-txt-google-search-seo-guide/
- https://www.hostinger.com/tutorials/llm-statistics
- https://berecommended.com/blog/llms-txt-worth-it-adoption-vs-reality-2026