# Learn Grammatical Cases

## Confirmed requirements

- Build an Android app to learn grammatical cases, expanded from Slavic languages
  to include German; app name is Learn Grammatical Cases.
- Russian is the personal starting point; provide material for all Slavic languages
  over time, with German now included.
- Release as open source; the repository already has an MIT license.
- Preserve discussion and build knowledge in AI/ for the owner and fork contributors.
- Follow the durable documentation approach of the sibling polar-web-app project.
- Record all downloading and installation in reusable installer scripts.
- Provide run-codex.sh to resume the current local chat.
- Follow the device theme; user requested dark mode and no longer requires Android 8 support.
  Android 10 minimum is the resulting implementation choice.
- Settings show the app version (currently 0.2) and build date. User confirmed the app works on their phone.
- Adjective prompts put adjective and noun dictionary forms together in brackets;
  do not reveal the noun's inflected target-case form in the sentence.

## Confirmed learning flow

Startup case menu plus random mixed practice; noun/adjective sentence samples;
four answer options with green/red feedback; selected-option speech at bottom left;
Next at bottom right; end-of-session results with Repeat and Back.
GUI and learning language have independent settings. Russian uses six cases;
language packs may offer up to eight. Each language has its own sample folder,
with reusable templates in samples/templates/. Samples contain native-language
sentences and neutral prompts in the learning language. See UI.md and
CONTENT_FORMAT.md for the accepted format and initial grouping.
Noun and adjective sets are separate; adjective sets include labelled cardinal and
ordinal numerals. Starter Russian and Polish sets contain 15 questions per case
and track: 180 Russian + 210 Polish, all draft pending linguistic review.

## Proposed product and stack

Native Kotlin with Jetpack Compose; offline lessons and exercises; local progress.
Start with a small reviewed Russian learning path, then add language packs using
shared exercise infrastructure and language-specific grammar descriptions.
The first prototype now uses Kotlin/Compose under the user's authorization to
continue implementation autonomously. This is an implementation choice; broader
offline/local-progress proposals are not newly confirmed product requirements.
See PROTOTYPE.md for provisional defaults implemented for later review.
Do not assume every Slavic language has Russian's case system or morphology.

## Documentation map

- HANDOVER.md: setup readiness and exact next steps after chat compaction.
- PROTOTYPE.md: implemented first-prototype behavior, build choices and validation scope.

- DOCUMENTATION.md: maintenance and handover rules.
- IMPLEMENTATION_PLAN.md: phased delivery and validation.
- ARCHITECTURE.md: proposed application structure.
- UI.md: confirmed learning flow and proposed interaction details.
- CONTENT_FORMAT.md: contributor-friendly sample proposal and reference template.
- DATA_MODEL.md: proposed learning-content model.
- DEVELOPMENT.md: setup, installer, local chat restart.
- LINKS.md: researched primary references.
- TODOS.md: next steps and unresolved questions.
- LOG.md: dated discussion outcomes, changes, and validation.

The committed knowledge base records relevant discussion outcomes and implementation
history; it is not an automatic verbatim export of the private conversation.

## Version 2 topic navigation (2026-10-11)

User supplied ru-v2/pl-v2 and requested topic levels, including gender subgroups,
plus a persistent light/dark button at the upper right. Imported YAML remains
schema 1 with content_profile and topic id/name. Case → track → topic → gender
(where exercise_type is gender) is the implemented interpretation. Source topic
groups such as без, для remain combined; separate preposition lessons would need
separate authored topic data. Original and v2 packs remain separately selectable.
Imported source licenses are unspecified; local draft preview does not establish
permission to redistribute them with the open-source release.

## Version 0.2 and pack names (2026-10-11)

User requested Russian simple/deep and Polish simple/deep, version 0.2 and a
release build. Stable folder/pack IDs stay unchanged; versionCode increases to 2.
Explicit local release preview builds a non-debuggable APK with draft lessons,
signed with the existing development key for private testing. Normal publication
builds still require linguistic review and redistribution permissions.

APK filenames requested by user: slavic-cases.apk (release) and
slavic-cases-debug.apk (debug). Builds export these to app/build/distributions/.

## Automatic continuation (2026-10-11)

User requested a Settings option to automatically continue to the next question.
Implemented a persisted English/German switch. Implementation defaults: off,
2-second feedback delay for correct and incorrect answers; final answer opens
results. Manual Next remains available. Speak pauses automatic continuation for
that question until Next is pressed, allowing pronunciation without interruption.

## Guess the case (2026-10-11)

User requested a main-menu guess-the-case mode drawn randomly from all questions,
with default 30 and configurable count in Settings. Implemented pool: all questions
in the selected simple/deep language pack, across cases and tracks. Implementation
choices: no replacement; count saved locally, adjustable 1–200, capped by pool size.
Display the completed source prompt and explicitly identify its target form, retain
native translation, and offer every case in that language as an answer. Hide case
from the progress heading. Existing feedback, automatic continuation, repeat and
results apply. Speak reads the target form rather than the selected case label.

## German and app rename (2026-10-11)

User renamed the app to Learn Grammatical Cases and requested a German lesson
basis, recognising four cases and different grammar. Implemented German simple
(de), 120 original MIT draft questions: 15 × four cases × nouns/adjectives tracks.
Answers are full noun phrases, covering articles, genders, plural dative, weak
masculines, weak/mixed/strong adjective patterns, cardinal/ordinal numerals.
Native text includes English/German; same-language translation is hidden to avoid
revealing the answer. Default learning pack remains Russian. App label, header,
Gradle project name and APK filenames are renamed; Android ID/namespace and local
installer paths stay stable to preserve updates/settings. Current exports:
learn-grammatical-cases.apk / learn-grammatical-cases-debug.apk. Repository rename
and public publishing were not requested. Version remains 0.2.

## Localized app name (2026-10-11)

User requested a translated phone launcher label and in-app title. Added German
app_name resource: Grammatische Fälle lernen (English/default: Learn Grammatical
Cases). Launcher uses Android/device locale; in-app title explicitly uses the
saved GUI setting, independently of phone and learning languages. Both normal
header and content-load failure title use the chosen GUI locale.

User requested omitting the UTC suffix from the date-only Settings build date
(2026-10-11). Display YYYY-MM-DD; build-date generation remains unchanged.

User also requested sample selection buttons follow GUI language (2026-10-11).
Apply localized pack names to Settings and the selected-pack header; localize
English topic-menu labels as well, preserving target-language prepositions.

## Interface translation files (2026-10-11)

User agreed to migrate all hardcoded interface translation pairs to Android
strings.xml. English/default and German resource files now contain 58 matching
entries, including buttons, headings, grammar labels, speech/errors, guess-case
instruction and whole formatted messages. GUI-localized resource context preserves
independence from phone locale. Lesson instructions/native texts and pack/topic
names remain authored YAML content. No .po files introduced.

## Distribution and owner device (2026-10-11)

User does not intend Google Play distribution; F-Droid is a possible future
channel, not yet a submission decision. Owner currently uses GrapheneOS. Ordinary
Android APK signing applies; no GrapheneOS-specific app key is required. Current
private preview uses the development key, not a publication signing setup.

## Russian and Polish interface (2026-10-11)

User requested Russian and Polish GUI translations. Added both as saved GUI
choices alongside English/German, with 60 matching resource entries per locale,
localized launcher names, five pack names and all 84 topic labels. Language
choices use autonyms in two rows. Sentence translations remain authored content;
missing Russian/Polish sentence translations show a localized notice. Same-language
translations remain hidden. These translations await native-speaker review.
