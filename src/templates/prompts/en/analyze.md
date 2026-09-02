# Prompt: pedagogical quality analysis (Gemini)

## Context

You are an expert in instructional design, andragogy, and pedagogical quality, with experience in high-standard educational publications (Harvard Business Review, MIT Sloan Management Review, HSM Management). Your task is to critically analyze the draft below and produce a detailed diagnostic report.

## Identification

- **Course:** {course_name}

## Draft to analyze

{draft_content}

## Analytical dimensions

### 1. Coherence and Intellectual Rigor

- Are concepts presented with analytical depth, or do they remain superficial?
- Are there contradictions or self-cancelling claims?
- Does the logical progression of the content follow a clear argumentative line?
- Are important claims supported by evidence, data, or references?

### 2. Editorial Quality (HSM/HBR Standard)

- Is the tone analytical and propositional (not generic or condescending)?
- Does the content go beyond basic definitions, offering insights and analysis?
- Are there clichés or worn phrases that should be removed?
- Is the language direct, active, with intellectual authority?
- Does each paragraph carry one central idea developed until it closes? Fail both extremes: the block that stacks two subjects, and the run of one-sentence paragraphs that slices a single line of reasoning.
- Does the rhythm of the sentences follow the argument? Check any stretch of ten sentences: a gap of fewer than 15 words between the longest and the shortest signals machine uniformity; a run of short filler sentences, one per paragraph, signals the opposite defect (headline staccato). Neither is acceptable, and no length quota should be recommended in the correction.
- Is the text free of the em dash used as a stylistic device, of serial antithesis ("it is not X, it is Y"), of the triad used as rhythm, and of the mirror conclusion?

### 2.5. Substance and narrative (approval dimension, not rejection)

This dimension asks what the module HAS, and not only what it managed to avoid. A short, uniform, argument-free text passes every automated gate in the repository, because none of them measures substance. You are the layer that does.

Assess and score:

- **Own thesis**: does the module defend an identifiable position, or is it a neutral compilation of what already exists? Point to the sentence that carries the thesis; if there is none, the score for this dimension cannot go above 4.
- **Evidence tied to the thesis**: do the cited figures support the argument being defended, or do they merely decorate the text with loose numbers?
- **Information gain**: is there at least one data point, local-market example, comparison, or framework that the learner would not find in the first three pages of any search on the topic?
- **Opening**: does the module open on a concrete situation with explicit tension (a case, a hard decision, a number that contradicts expectation), or on a definition and a generic scenario?
- **Anchor case**: is there a named case that runs across the module and comes back in the conceptual grounding and in the exercises, or are the examples one-off?
- **Promise kept**: was what the opening promised actually delivered in the development?
- **Closing**: does the synthesis show what changed in the case or in the initial tension, or does it repeat what was already said?
- **Decision criterion**: when the module presents alternatives, does it compare them against explicit criteria and recommend with a justification, or does it list options without helping the learner choose?

Assess as well, within the same dimension:

- **Promise and tension**: does the promise appear in the opening, in twelve words at most, with the tension coming after it and not postponing the answer? Or is the answer buried under a long scene?
- **Proportion between claim and proof**: is the number of blocks that assert a result less than or equal to the number of dated proofs? Point out the surplus claims.
- **Case label**: is each case identified as real (with a source) or hypothetical (with the label repeated next to every number)? A case presented as real without a source is a serious defect and drops the score for this dimension to 2 or below.
- **Percentages**: does each one carry origin, date, method, and denominator in the same sentence? List the ones that fail.
- **Open markers**: count `[FALTA EVIDÊNCIA:` and `[PREENCHER-HUMANO:`. Above five, `approved` is false.
- **Ask before proof**: does any ask for data, for a sign-up, or for money appear before the first verifiable proof?
- **Subject of the failure sentences**: is the subject slot filled by an artifact or a process, rather than by the learner?

Normative reference for the two dimensions above: `DIRETRIZ_EDITORIAL.md`, sections 2, 3, 4, and 6.

### 3. Formatting and Visual Structure

- Does the content use comparative tables where appropriate?
- Are lists well structured (numbered for processes, bulleted for enumerations)?
- Is there a clear title hierarchy (H2 > H3 > H4)?
- Are key terms bolded on first occurrence?
- Are there blockquotes for central insights?
- Does each module have at least one table?

### 4. Andragogical Conformance

Evaluate the content against Knowles's 6 principles:

| Principle | What to verify | Score (0-10) |
|-----------|----------------|--------------|
| Need to know | Does the module explain WHY the learner needs this knowledge? | |
| Self-concept | Is the learner treated as an autonomous professional? | |
| Prior experience | Are there links to the learner's professional experiences? | |
| Readiness | Is immediate applicability demonstrated? | |
| Problem orientation | Does content start from real problems? | |
| Intrinsic motivation | Does learning connect to professional growth? | |

### 5. Content Gaps

- Are there cognitive leaps without intermediate explanation?
- Has any essential concept been omitted or treated superficially?
- Are prerequisites explicit?
- Are there enough practical examples to consolidate each concept?

### 6. Exercises and Assessment

- Do exercises use real professional contexts (not generic hypotheticals)?
- Is there a complexity progression (Bloom's taxonomy: apply → analyze → evaluate → create)?
- Are evaluation criteria clear and measurable?
- One executable exercise per lesson (5 to 15 minutes, real data, expected result)?

### 7. English usage and consistency

- Does the text use **American English consistently** (no British/American mixing)?
- Are there spelling drift instances? (e.g., `organise` → `organize`, `behaviour` → `behavior`, `colour` → `color`, `analyse` → `analyze`, `centre` → `center`, `catalogue` → `catalog`, `programme` → `program`, `modelling` → `modeling`, `travelling` → `traveling`, `learnt` → `learned`, `licence` (noun) → `license`).
- Are there British idioms that should be neutralized? (`whilst` → `while`, `amongst` → `among`, `towards` → `toward`).
- List ALL occurrences if any are found.

## Report format

Return a structured JSON with these fields:

```json
{
  "score": 0-100,
  "approved": true/false,
  "editorial_standard": "below_expected|adequate|excellent",
  "dimensions": {
    "coherence_rigor": {"score": 0-10, "notes": "..."},
    "editorial_quality": {"score": 0-10, "notes": "..."},
    "substancia_narrativa": {
      "nota": 0-10,
      "tese_identificada": "the sentence that carries the thesis, or null if absent",
      "information_gain": "what the module brings that no generic source has, or null",
      "abertura_em_situacao": true/false,
      "caso_condutor": "name of the case that runs across the module, or null",
      "promessa_cumprida": true/false,
      "fechamento_com_callback": true/false,
      "observacoes": "..."
    },
    "visual_formatting": {"score": 0-10, "notes": "..."},
    "andragogy": {
      "overall_score": 0-10,
      "need_to_know": 0-10,
      "self_concept": 0-10,
      "prior_experience": 0-10,
      "readiness": 0-10,
      "problem_orientation": 0-10,
      "intrinsic_motivation": 0-10,
      "notes": "..."
    },
    "gaps": {"score": 0-10, "notes": "..."},
    "exercises": {"score": 0-10, "notes": "..."},
    "language_consistency": {"score": 0-10, "british_americanism_drift": ["..."]}
  },
  "priority_improvements": ["...", "...", "..."],
  "strengths": ["...", "...", "..."],
  "spelling_corrections": ["wrong → correct", "..."]
}
```

Write all observations in clear, professional American English with consistent spelling throughout.
