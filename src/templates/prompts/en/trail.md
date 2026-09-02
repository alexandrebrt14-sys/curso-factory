# Prompt: track closing (GPT-5.5)

## What this is

A track is a module of 4 to 6 lessons. The lessons are already written. You write only what
lives at the TRACK level, once: what the student will be able to do, what they need before,
the glossary, the frequently asked questions and the dated sources. None of this goes into
each lesson; it goes here.

The reader is a small business owner, a layperson in marketing and technology, on a phone.
Correct spelling and diacritics, no emoji, no em dash, no clichés.

## The track

- Course: {course_name} (level {course_level})
- Track {module_number}: {module_title}. {module_description}
- Lessons, in order: {lesson_titles}

## Anti-invention (inviolable)

Every listed source must appear in the lessons' text or in the research below, with name and
date. A source that is in neither does not enter. If the lessons cite a figure without a
source, do not create the source: leave the figure out of the list.

## What to write, in this order and with these headings

## What you will be able to do

Three to five sentences, one per line, each starting with an action verb in the infinitive
(analyze, compare, calculate, build, apply, choose, measure, publish). Never "understand",
"know", "learn". Each sentence names a result they can check in their own business.

## Before you start

One to three prerequisites, one line each: what they need at hand (account, data, tool) or
already know. If the track depends on nothing, say so in one line.

## Glossary

The technical terms the lessons use, in alphabetical order, each with a gloss of up to 12
words and a comparison from daily life. Format: `**term**: gloss`. Between five and twelve
terms; only what the lessons actually use.

## Frequently asked questions

Three to six questions the business owner would ask after finishing the track, each with a
direct answer of two to four sentences, no preamble. Question in bold, answer in prose right
below.

## Sources

One line per source, in the form `Source name, title or report, month and year`, only with
what the lessons or the research bring. One to eight sources.

## Before delivering, check

1. Five sections, in this order, each with the heading above as H2.
2. Action verbs in the objectives; no "understand" or "know".
3. Gloss of up to 12 words per term; no term the lessons do not use.
4. No invented source.
5. Sentences up to 28 words; no em dash; correct spelling.

Start directly with the first H2, with no track title (the pipeline inserts it) and no comment
about this prompt.

--- TRACK LESSONS ---
{lessons}

--- RESEARCH DATA ---
{context}
