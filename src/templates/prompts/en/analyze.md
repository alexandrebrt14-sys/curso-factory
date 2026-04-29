# Prompt — Pedagogical Quality Analysis (Gemini)

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
- Are paragraphs concise (max 5 lines)?

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
- At least 3 exercises per module?

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
