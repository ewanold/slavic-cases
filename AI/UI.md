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

Every sample and template contains both the example in the learner's native
language and the neutral question in the language being learned. The question
page displays those authored texts. The learner chooses one of four answer options.
Correct selections turn green; incorrect selections turn red.
A bottom-left speech button reads the selected option aloud.
A bottom-right Next button advances to the next question.
After all session questions are answered, show results with Repeat and a button
to go back one menu step.

## Proposed interaction details

Main menu -> case and noun/adjective track (or mixed mode) -> finite question
session -> results. The precise placement of the track choice is still proposed.
Settings are accessible from the main menu. Show selected learning language.
Language packs declare their available teaching cases. Russian uses six; each
language may declare up to eight. Do not fill unused slots or assume vocative is
present. Other languages and treatment of additional cases need reviewed content.

Interpret "neutral form" provisionally as a sentence with a blank and the target
noun/adjective given in dictionary form. Confirm before implementing this behavior.
Example: native-language sentence, then `Я вижу ___. (новый дом)`.
Render four complete candidate phrases. Shuffle options once per question and retain
that order while the question is visible. Keep the correct answer by stable ID.

Proposed scoring: one scored selection per question, then lock answer selection.
Show Correct/Incorrect text or icons as well as color. Enable Next after selection.
If wrong, highlight the correct answer too; this additional feedback is a proposal.
Speech reads the selected answer in the learning language, including a wrong answer
if that is selected. Disable Speech until an item is selected. If no suitable voice
is available, explain that without blocking practice. Audio behavior is not implemented.
Results show correct answers, total questions, and percentage. Repeat restarts the
same set with fresh option order; Back returns to the menu that started the session.
Mixed mode samples complete, reviewed questions across available cases and word pairs;
do not randomly combine unrelated words into unreviewed sentences.
Mixed session length, sampling distribution, and repeat behavior await agreement.

## Open decisions

- Does native-language text follow the GUI setting or require a third setting?
- What precisely should "neutral form" show?
- Are wrong answers final, or may learners retry before Next?
- How many questions belong to a mixed session?
