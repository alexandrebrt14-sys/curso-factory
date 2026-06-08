# Prompt — Content Classification (Groq)

## Context

You are an expert in educational taxonomy and online-course cataloging. Your task is to classify the content below with precise, standardized metadata for indexing, discovery, and recommendation on educational platforms.

## Identification

- **Course:** {course_name}

## Content to classify

{content}

## Required classifications

### 1. Difficulty level

Choose exactly one:

- `beginner` — no prior knowledge of the topic required
- `intermediate` — basic familiarity with the topic assumed
- `advanced` — solid command of prior concepts required

Justify the choice in 1–2 sentences, referencing specific elements of the content.

### 2. Thematic tags

List 5 to 10 tags that describe the content, prioritizing:

- Domain-specific technical terms
- Tools and technologies mentioned
- Skills and competencies developed
- Format and pedagogical methodology

### 3. Prerequisites

List the knowledge the student should have before starting this course. For each prerequisite, indicate the expected level (basic, intermediate, advanced). If none, explicitly write "None".

### 4. Estimated duration per module

Estimate the study time per module, considering:

- Reading the theoretical content
- Completing the practical exercises
- Practice/experimentation time

Provide the estimate in minutes per module and total in hours.

### 5. Primary category

Choose the category that best describes the course on platforms such as Coursera, Udemy, edX or Hotmart (e.g., "Technology", "Business", "Design", "Marketing", "Personal Development", "Languages", etc.).

### 6. Target audience profile

Describe the ideal learner: role, experience, sector, motivation for taking the course.

## Output format

Return a JSON with the following structure:

```json
{
  "level": "beginner|intermediate|advanced",
  "level_rationale": "...",
  "tags": ["tag1", "tag2", "..."],
  "prerequisites": [
    {"knowledge": "...", "expected_level": "basic|intermediate|advanced"}
  ],
  "duration_per_module_minutes": [30, 25, ...],
  "total_duration_hours": 0,
  "category": "...",
  "target_audience": "...",
  "seo_keywords": ["...", "..."]
}
```

Use clear, professional American English with consistent spelling in all text fields.
