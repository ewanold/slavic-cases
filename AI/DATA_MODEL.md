# Proposed learning-content model

Language pack: stable ID, language tag, script/variant, title, version, contributor,
source attribution, license, review status, and supported lesson/exercise IDs.
Grammar profile: language-specific case inventory and other relevant features.
Lesson: explanation, examples, learning objectives, prerequisite IDs.
Exercise: prompt, context, expected answer(s), feedback, target features, stable ID.
Progress: exercise ID, attempts, outcomes, timestamps; optional review due date.

Avoid imposing a fixed case count, script, or singular/plural-only structure on
all languages. Distinguish grammatical case from its use in a sentence.
Answer normalization must be explicit per language and exercise; retain meaningful
letters and diacritics. Handling stress marks and alternate forms needs a policy.

Before authoring packs, define the language/variant coverage matrix, including
smaller and historical languages. Broad coverage is a roadmap, not available content.
Each example needs linguistic review and clear provenance before release.

## Concrete practice proposal

CONTENT_FORMAT.md defines accepted YAML for separate noun and adjective/numeral
tracks under samples/<language>/. The starter implementation uses 15 questions
per case and track, with translated sentences, neutral prompts, four answer
options and a stable correct-answer key. GUI locale, learning language and native-text locale are
separate concepts; whether native text uses GUI locale is still open.
A session is a finite list of question IDs plus recorded answers and option order.
Do not generate arbitrary noun/adjective/case combinations in mixed mode unless
reviewed content supplies a valid question and unambiguous answers.

## Confirmed language-pack constraints

One sample-set folder per learning language, plus a shared templates folder.
Each language definition declares its teaching case list, with a maximum of eight;
Russian declares six. A sample must contain native text and a neutral prompt in
the learning language. Native translations remain content, independently of GUI
strings. Their selection setting is still open. See samples/ for the draft layout.

The full starter sets are Russian (six cases, 180 questions) and Polish (seven
cases, 210 questions). Cardinal questions may answer with a complete phrase to
represent numeral government; the selected numeral case does not force the same
case on its noun. Keep word_type and answer_scope explicit. All sets remain draft.
