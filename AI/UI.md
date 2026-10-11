# Learning flow

## Confirmed requirements (2026-10-10)

Startup opens a main menu with language-specific case choices, at most eight,
plus a mixed mode with random selection of noun, adjective, and case.
Russian has six case choices, as confirmed by the user.
Case practice has separate noun and adjective tracks. The adjective track also
contains cardinal and ordinal numerals. Contributor sample files use accepted YAML.
The initial implementation provides 15 example questions per case and track, with
full Russian and Polish starter sets. Their linguistic review is pending.
Settings select the GUI language independently from the language being learned.
Settings show the current version (0.2) and build date. Initial appearance follows
the device; the upper-right Light/Dark button saves a manual override.
Adjective/ordinal prompts put both dictionary forms inside brackets and omit the
inflected noun from the sentence so it cannot reveal the answer's case ending.

Every sample and template contains both the example in the learner's native
language and the neutral question in the language being learned. The question
page displays those authored texts. Simple packs have four answer options; imported deep gender exercises have three.
Correct selections turn green; incorrect selections turn red.
A bottom-left speech button reads the selected option aloud.
A bottom-right Next button advances to the next question.
After all session questions are answered, show results with Repeat and a button
to go back one menu step.

## Provisional interaction defaults

Implemented under the user's authorization to continue autonomously. These remain
reviewable choices, not additional confirmed product requirements. See PROTOTYPE.md.

Main menu -> case -> noun/adjective track -> topic (deep packs) -> gender subgroup
(gender exercises) -> question session -> results. Mixed mode starts a session
directly. Deep topic grouping preserves authored combined preposition lessons.
Settings are accessible from the main menu. Show selected learning language.
Language packs declare their available teaching cases. Russian uses six; each
language may declare up to eight. Do not fill unused slots or assume vocative is
present. Other languages and treatment of additional cases need reviewed content.

Interpret "neutral form" provisionally as the authored sentence with a blank and
dictionary-form hint. The prototype now uses this representation.
Example: native-language sentence, then `Я вижу ___. (новый дом)`.
Render the authored candidate words or phrases according to the sample's answer_scope.
Adjective/ordinal questions use word answers; cardinal questions use phrase answers.
Shuffle options once per question and retain
that order while the question is visible. Keep the correct answer by stable ID.

Proposed scoring: one scored selection per question, then lock answer selection.
Show Correct/Incorrect text or icons as well as color. Enable Next after selection.
If wrong, highlight the correct answer too; this additional feedback is a proposal.
Speech reads the selected answer in the learning language, including a wrong answer
if that is selected. Disable Speech until an item is selected. If no suitable voice
is available, explain that without blocking practice. The prototype implements
this using installed offline voices and a visible, nonblocking status message.
Results show correct answers, total questions, and percentage. Repeat restarts the
same set with fresh option order; Back returns to the menu that started the session.
Mixed mode samples complete, reviewed questions across available cases and word pairs;
do not randomly combine unrelated words into unreviewed sentences.
The prototype uses 15 questions, uniformly sampled without replacement within the
selected learning pack; Repeat retains the set with a fresh option shuffle.

## Open decisions

- Does native-language text follow the GUI setting or require a third setting?
- Review neutral hints for new languages; adjective/noun bracket placement is confirmed.
- Are wrong answers final, or may learners retry before Next?
- How many questions belong to a mixed session?

Correct/incorrect feedback stays in the fixed footer above Speak/Next. Long
question bodies and answer lists remain scrollable. Simple/deep display names
do not change stable pack IDs or stored language selection.

Automatic continuation: Settings offers a saved switch, off by default. When on,
answered questions advance after 2 seconds, including to the final results screen.
Speak pauses the timer for that question; manual Next resumes the session.
Navigation away cancels pending advancement.

Guess the case: main-menu mode uses random questions from the whole selected pack.
Default length 30, saved Settings count adjustable 1–200. Sampling is without
replacement and capped at available questions. Show the completed sentence and
its target form (→), with native translation; choices are all language cases.
Question heading conceals the correct case. Speak reads the target form; standard
feedback, automatic advancement and results/repeat behavior apply.

German simple declares only four cases; shared menus and Guess the case read the
manifest without a Russian case assumption. Answers are complete phrases. Hide
native translation whenever GUI locale equals learning-language code, since it
would show the completed answer. Header uses a weighted smaller title so the new
Learn Grammatical Cases name and theme button can wrap within the available width.

App title localization: English Learn Grammatical Cases / German Grammatische
Fälle lernen. In-app title follows the saved interface language immediately;
phone launcher label follows Android locale through localized app_name resources.
Changing the learning pack does not change either name.

Language-pack selection chips, selected-pack header, topic selection buttons and
gender-topic heading now use manifest GUI translations (English/German/Russian/Polish). Stable
IDs and source topic names remain intact; labels fall back to source names for
older packs. Settings build date displays YYYY-MM-DD without the UTC suffix.

Interface copy uses Android string resources for English/default and German,
including entire formatted messages and feedback labels. Resource resolution uses
the saved GUI locale, independently of Android launcher locale and learning pack.
Lesson copy and localized pack/topic labels remain authored YAML content.
