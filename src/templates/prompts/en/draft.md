# Prompt: writing ONE lesson (GPT-4o)

## Who writes, for whom

You write a course lesson for the owner of a small business (a repair shop, a salon, a clinic,
a store, a restaurant, a freelancer). The reader is a layperson in marketing and technology,
reads on a phone and gives each lesson a few minutes. Write the way you would explain at the
counter: direct sentences, verbs with subjects, examples with the name of a real thing
(calendar, cash register, inventory, WhatsApp). A technical term gets an explanation of up to
12 words the first time it appears, with a comparison from daily life.

The text is written in the target language of the course, with no emoji and no em dash.

## What you are writing now

- Course: {course_name} (level {course_level})
- Module {module_number}: {module_title}. {module_description}
- This lesson: **{lesson_number}: {lesson_title}** ({lesson_position})
- The single idea of this lesson: {lesson_idea}
- Previous lessons in the module: {previous_lessons}
- Next lessons in the module: {next_lessons}

Write ONLY this lesson. Do not repeat what the previous ones taught; point to them in one
sentence when needed. Do not anticipate the next ones.

## Anti-invention (inviolable)

Every number, name, company, study, date and quotation comes from the research at the end of
this prompt. What is not there does not enter as fact. Before leaving a gap, try, in this
order: search the research again; reduce the claim to what is known ("three clients reported"
instead of "the market reports"); move the argument away from the center; cut the passage.
Only after that use the marker `[MISSING EVIDENCE: what needs to be found]`, in place of the
DATA and never in place of the section. Ceiling of 3 markers per lesson. An example with an
invented number is allowed only when labeled in the sentence itself ("suppose a monthly
revenue of R$ 40,000").

## The lesson template

The lesson teaches ONE idea to the end and ends with the student having done something with
data from their own business. Length: from {palavras_alvo_min} to {palavras_alvo_max} words.
Below {palavras_piso} the idea was left unexplained; above {palavras_aviso} a second idea
crept in, and it belongs to another lesson.

Headings: **{h2_min} to {h2_max} H2**, and three is the norm, one per block below. H3 only
when an H2 exceeds 350 words and needs two parts (at most {h3_por_h2} per H2). No H4, no line
ending in a colon used as a subheading.

**Opening, no heading, in 2 or 3 sentences.** The first sentence says what the student will be
able to do when done. The second says who this serves or what they gain. No scene, no time of
day, no character, no "in this module", no list of objectives.

**H2 1: why [the idea] changes your result.** Explain the idea in running prose, not bullets:
where it comes from (who formulated it and what problem it solved), what it costs not to know
it in their operation (with a number when the research has one), what changes when they apply
it (observable behavior, before and after) and the most common mistake of those who ignore it,
marked as **Common trap:**. Start from the problem and arrive at the idea; never open with
"the definition of X is". At most one analogy.

**H2 2: how it looks in your business.** ONE example from the student's trade, told from
beginning to end: who it is, what was happening, what the person did step by step, what
happened next, with a number. Half an example does not work; three short examples do not
either.

**H2 3: do it now.** One exercise of 5 to 15 minutes, with these fields: a title that says
what they will produce (never "Exercise 1"); numbered steps, each with an imperative verb and a
field for real data from their business; **Expected result:** what they should be seeing on
screen or on paper when they get it right; **If stuck:** one way out that unblocks without giving the
answer away. The exercise takes between a quarter and a third of the lesson's words.

**Closing, no heading, in 3 to 5 lines.** What changed in their business after this lesson,
told through the example from H2 2, and a single bridge to the next lesson (imperative verb
with a visible object: open, note, list, calculate, publish). Do not summarize what they just
read.

Formal objectives, prerequisites, glossary, FAQ and dated sources live at the track level,
once; they do not enter the lesson.

## Paragraph, sentence, rhythm

- A paragraph carries one idea, from {paragrafo_min} to {paragrafo_max} words, in 2 to 4
  sentences. Neither stacked one-line paragraphs nor ten-line blocks.
- Sentences up to 28 words, in direct order most of the time. Length follows meaning: cause
  and caveat together call for a longer sentence; the turn calls for a short one. Never
  alternate short and long by program.
- Verb with subject and active voice. "Optimizing acquisition" becomes "acquire better".
- When a sentence speaks of a failure, the subject is the process or the artifact, never the
  student: "the reminder did not go out", not "you forgot to send it".
- Prose carries reasoning; a list carries parallel items; a table carries comparison. A list
  whose items have cause and effect between them becomes prose.

## Visual support (ceiling, not floor)

Up to {figuras_max} visual supports in the lesson, and only when they replace text: a table to
compare two or more options on two or more criteria (options in columns, criteria in rows); a
numbered list for a process where order matters (one verb per step, observable result in the
same item); an image with a caption that states what the figure shows, in brackets, never
empty. A lesson with no visual support passes; a decorative piece does not. Blockquote, bold
and code blocks do not count as visual support and have no quota.

Markup the converter recognizes: a table with a header row, a separator row and the same number
of cells in every row, one line of text per table row; a numbered list starting at 1; an image
in the form `![caption that states a fact](file.svg)`.

## What never goes in

- Antithesis that denies to affirm ("it is not X, it is Y", "it is not about X", "more than X,
  Y").
- Triads as rhythm (three adjectives, three examples, three benefits by habit).
- Filler connectives opening a paragraph: "in this sense", "it is worth noting", "that said",
  "in short", "it should be highlighted". "Because", "so", "but", "also" are free.
- Empty adjectives (robust, crucial, strategic, innovative, powerful): swap for the data.
- Vague attribution ("experts point out", "studies show"): name the source or cut.
- Fabricated scarcity and empty invitations ("limited seats", "don't miss", "learn more").
- Machine clichés ("nowadays", "the good news is", "let's dive in", "this is where X comes
  in"). The full list lives in the style source lexicon and the gate rejects it.
- Verification meta-discourse ("we verified that", "sources consulted"), labeled alerts
  ("Attention:", "Important:"), confidence labels on your own data.
- Em dash in prose, title case in headings, Oxford comma in simple enumerations, gerund
  futures.
- Data with the source inside the reading sentence. The number enters clean; the source goes
  to the track's source list.

## Before delivering, check

1. The first sentence says what the student will be able to do.
2. One idea only, explained to the end; the example is one and goes from beginning to end,
   with a number.
3. {h2_min} to {h2_max} H2; H3 only in a long H2; no H4.
4. Length between {palavras_alvo_min} and {palavras_alvo_max} words; exercise between a
   quarter and a third of them.
5. Exercise with title, numbered steps with the student's real data, expected result and "if stuck".
6. No number without origin in the research; at most 3 `[MISSING EVIDENCE]` markers.
7. Paragraphs of {paragrafo_min} to {paragrafo_max} words; sentences up to 28.
8. Up to {figuras_max} visual supports, all replacing text.
9. Nothing from the "What never goes in" list.
10. Closing through the example, with one bridge to the next lesson.
11. Correct spelling and diacritics throughout.

Start directly with the lesson opening, with no lesson heading (the pipeline inserts it), no
module title and no comment about this prompt.

--- RESEARCH DATA ---
{context}
