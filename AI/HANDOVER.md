# Implementation handover — 2026-10-17

## Desktop editor current status

User requested a PC editor, then Windows, Qt preference with Tkinter fallback,
restricted forms and German/Russian/Polish PO catalogs. Current implementation
uses shared controller.py/fields.py, qt_view.py and tk_view.py. app.py selects
PySide6 → PyQt6 → Tkinter, with explicit --ui and --language overrides. Structured
forms replace raw YAML tabs; IDs/imported source/unknown nested fields are read-only
and preserved. Projects can be created or opened; save suffixes remain independent
of topic metadata. See tools/sample_editor/README.md for current commands/limits.

New project (Ctrl+N) is available on startup. Both views offer target language,
case checkboxes and a new/empty directory, plus native translation languages.
Defaults: ru six, pl seven, de four; custom language tags need an explicit case
selection. Creation writes language.yaml/track directories and opens a first
blank noun lesson. Invalid startup controls are disabled. Arbitrary editor folder
names work through safe temporary validation normalization. Completed first lessons
can be saved before full coverage exists; explicit validation/build/release remain
strict. allow_incomplete skips only missing lessons/cases and is ignored for release.
New projects use the original simple 15-question format, no imported profile.
New project also requires contributor, license and sources once, stores them in
language.yaml/lesson_defaults, and prefills all future new lessons after reopen.
Existing/imported lessons keep their own attribution; per-lesson overrides remain.
No automatic license or contributor identity is assumed.

Only the left group/case pair is visible for browsing. Lesson location is text on
the right; Move lesson opens an explicit dialog and applies on Save. Add/Delete
lesson buttons are beneath the lesson list. Add starts a blank draft (15 starter
slots, one deep slot) with original attribution fields to fill; it is written only
after complete validation. Delete confirms and moves a saved file to recovery
backups, or discards an unsaved draft. Deleting a last case/track lesson can leave
coverage incomplete until replacement/restoration. Browse changes clear old details.

Linux: `bash scripts/install-sample-editor.sh`, then
`bash scripts/run-sample-editor.sh samples/ru-v2`.
Windows x64: scripts/install-sample-editor.ps1 and scripts/run-sample-editor.cmd.
Optional -InstallPython bootstraps SHA-256-verified Python 3.12.10 x64.
Pinned/hash-verified dependencies live in user-local storage, outside SMB checkouts.
A pinned pip bootstrap handles hosts without ensurepip. The newest installer was
verified only into /tmp/grammatical-cases-editor-venv here; nothing installed into
system Python. Earlier Tkinter-missing/password-blocked notes describe the first
prototype and are superseded for the current Qt setup.

PO/MO catalogs plus English POT: tools/sample_editor/locales/. Update/compile using
scripts/sample-editor-translations.py with Babel from the editor environment.
Runtime gettext needs no Babel. All 192 interface/diagnostic messages have de/ru/pl translations;
native-speaker review remains pending. Editor/model and structural validator errors
are localized from structured templates; CLI/Android diagnostics stay English.
Low-level OS/YAML-parser detail passes through unchanged. Android strings.xml
localization is unchanged.

Validation: full 38-test suite passed, including real Qt New dialog defaults,
custom case selection, project creation, first completed-lesson save with other
tracks/cases empty, reopen and cancellation. Model checks cover arbitrary editor
folder names, unsafe tags, nonempty-directory refusal, incremental saves and
strict build/release coverage. New checks cover shared attribution in both tracks
after reopening and localized field/answer diagnostics with unchanged English CLI
messages and real paths/IDs. Existing lesson management, PO, packaging and all
1,722 typed-question round trips pass. German startup/New dialog screenshots were
rendered and inspected. The first lesson is still an unsaved draft until complete;
project metadata itself is persisted by creation. No new dependencies were needed.
Windows PowerShell/native execution and visible Tkinter checks remain pending.
Tkinter imports here but cannot connect to display :0. Actual PyQt6 is not installed;
its selection path is covered by a probe. No Android build/content changes required.
No commit, push or publication requested. An existing owner edit in
samples/ru-v2/nouns/nominative-plural-masculine.yaml and local recovery backups
were preserved; tests ignore recovery folders when copying project fixtures.

## Current status

Usable Kotlin/Compose Android app, version 0.2 (versionCode 2), Android 10+
(minSdk 29), compile/target SDK 36. Settings shows version and date-only build date.
Owner previously confirmed basic phone operation; newest 0.2 APK phone testing
includes owner-supplied screenshots of menus and answer feedback; a complete
runtime test of the newest build is not yet recorded. Android Studio found and
desktop launcher created by owner.
No build is pending. The emulator was previously left running, but adb now reports no connected
devices. No new runtime verification was possible. No commit, push or publication.

Read MAIN.md, TODOS.md and recent LOG.md before working. AI/ contains decisions,
validation and handover; source/scripts live outside it. Downloads/installations
must use reusable installers with pinned bootstrap archives/checksums.

## Run and artifacts

- Debug: bash scripts/build.sh (offline build, JVM tests and lint).
- Local release: bash scripts/build-local-release.sh.
- Debug APK: app/build/distributions/learn-grammatical-cases-debug.apk.
- Local release APK: app/build/distributions/learn-grammatical-cases.apk.
- Install/launch debug on a connected device: bash scripts/run-app.sh SERIAL.
- Optional emulator: bash scripts/run-emulator.sh (GPU auto, audio, Quick Boot).
- Instrumented tests: bash scripts/build.sh connectedDebugAndroidTest.
- Python tests: PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v.

Gradle exports friendly filenames automatically during assemble; APK copies are
byte-identical to internal outputs/apk artifacts and retain their signatures.
Local release is non-debuggable, signed with the existing development key and
explicitly includes drafts via localReleasePreview / ALLOW_DRAFT_CONTENT.
It is for private testing. Normal publication build retains review/license checks;
production signing and public distribution remain unfinished. No keys are in Git.
See DEVELOPMENT.md and README for installer, Studio launch/desktop entry and
phone instructions. run-codex.sh resumes the original local chat.

## Current behavior and material

Five separately selectable packs: Russian simple/deep, Polish simple/deep, German simple.
Stable IDs ru/ru-v2/pl/pl-v2 preserve saved choices; speech uses ru/pl/de language codes.
Simple packs: case → noun/adjective-numeral track → 15-question session.
Deep packs: case → track → authored topic → gender subgroup for gender exercises.
Topic groups preserve combined prepositions such as без, для. Three-choice gender
items and variable topic lengths are supported. Other exercises have four choices.
Mixed mode samples up to 15 questions from the selected pack without replacement.

English/German interface and learning pack are independent. Native translations
follow GUI locale; deep packs mostly have English only (missing German is explicit).
First answer locks/scores; correct green, wrong red, correct option revealed.
Selected-option offline speech, Next, results, Repeat and originating-menu Back.
Settings/session state persist across activity recreation. No progress database.
Initial theme follows device; upper-right Light/Dark saves override. Android 12+
dynamic colors, Android 10/11 static fallback. Correct/incorrect feedback now stays
in the fixed footer above Speak/Next; long question bodies/answers scroll.
Simple adjective/ordinal hints include neutral adjective and noun in brackets;
deep imports remain authored source material and require further linguistic review.

1,722 draft questions: Russian/Polish simple 390, German simple 120, Russian deep
591 in 43 sets, Polish deep 621. German covers four cases with whole-phrase answers.
YAML remains schema 1 with explicit topic content profiles. IDs are unique per pack.
Extra native translations are allowed for deep samples. Strict legacy requirements
remain for simple packs. Audit: V2_SAMPLE_AUDIT.md and scripts/audit-topic-samples.py.
Three imported Russian questions have duplicate choice text; 601 questions contain
unknown/null grammatical features. Imported licenses are unspecified. Preserve
provenance; do not publish until redistribution permissions and review are recorded.

## Exact validation scope

- Original prototype: 12 Python, 3 JVM and 3 instrumented tests passed earlier.
- Deep pack implementation: 13 Python checks, debug build, 3 JVM tests and lint passed.
- Footer fix: debug build and emulator visual verification passed; reference image
  AI/reference/prototype-fixed-feedback.png shows full wrong-answer feedback.
- Version 0.2 / labels: debug and local release builds, 3 JVM tests, release lint,
  packaging label regression and release signature/version checks passed.
- APK filename exports: both builds passed; exported/source SHA-256 matches.
- Final documentation-only changes: whitespace and artifact/link checks.

Five instrumented tests now exist (topic/gender/theme and German tests added), but have
not been rerun after today's implementation changes. No latest-release runtime
claim should be inferred from older instrumented results. Earlier release signature v2
verified, version 0.2/code 2, minSdk 29, target 36, non-debuggable, then four packs
and 1,602 questions packaged. This predates German: current artifacts contain
five packs and 1,722 questions as documented below. SDK XML/native-symbol warnings
are nonblocking.

## Environment and next work

AGP 9.1.1, Gradle 9.3.1, built-in Kotlin/Compose compiler 2.2.10,
Compose BOM 2026.04.01, Activity Compose 1.10.1, Java bytecode 17,
Studio JDK 25.0.3. Build Tools 36.0.0, Platform Tools 37.0.1, SDK CLI 22.0;
emulator 37.2.12, Google APIs API 36 x86-64 image revision 7. SDK package revisions
are repository-resolved rather than pinned; installer bootstrap checksums are pinned.
SMB/CIFS checkout can make builds/copies slow. Do not edit sources during a build.
An untracked gradle/gradle-daemon-jvm.properties appeared during Studio setup;
not changed by the assistant. It requests Java 25 with toolchain download URLs;
review against the installer-only download policy before retaining it in a fork.

Next: owner phone review of 0.2, speech/accessibility, rerun instrumented checks,
review duplicate options/null features and deep prompt quality, permissions for
imported data, German deep translations/topic names, Android 10/11 fallback test,
then production signing/publication. Author preview/on-device importer, more Slavic
languages and Android CLI migration remain queued. Progress history is a proposal,
not a new confirmed requirement. Native-language third setting remains undecided.
No immediate question or blocking action remains for closing this chat.

Latest addition: persisted Settings switch for automatic continuation (default off,
2-second delay after any answer). Speak pauses it for the current question until
manual Next. See MAIN/UI/LOG for requirement and implementation defaults.

Guess the case added to main menu: default 30 random questions from selected pack,
all cases/tracks/topics; saved Settings count 1–200. All language cases are choices,
completed sentence/target form displayed, header hides correct case. Speech reads
target form; automatic continuation works. Source samples unchanged.

App renamed Learn Grammatical Cases; applicationId org.slaviccases.app unchanged
for install/settings continuity, repository and installer locations unchanged.
New APK names listed above. Same-language native translations hidden to prevent
answer disclosure. German source guidance: samples/de/README.md; reproducible
initial exporter: scripts/create-german-samples.py (never overwrites edited YAML).

Latest rename/German validation: all 1,722 draft questions structurally valid;
15 Python and five JVM tests passed. Offline debug and local release builds,
Android test APK compilation and debug lint passed (6m38s). Both new exports are
byte-identical to their internal originals and contain five packs / 1,722 items.
Launcher label Learn Grammatical Cases verified with aapt; release signature
verified. Version remains 0.2/code 2. No install/publication performed. Five UI
tests compile, but current device checks are pending (adb has no devices).
APK-import unknown authors are labelled explicitly during packaging and require
preserved source metadata; other content still requires contributor attribution.

Localized name added: German launcher label Grammatische Fälle lernen; English
fallback Learn Grammatical Cases. Launcher follows device locale, in-app header
and load-error title follow saved GUI locale independently of learning language.

Additional user corrections: sample-pack and topic labels follow GUI language via
manifest names/topic_names mappings, not learning or phone locale. German examples:
Russisch einfach/vertieft, Polnisch einfach/vertieft, Deutsch einfach, Geschlechter,
Übung 1. Original names and IDs preserved. Settings date now omits the UTC suffix.

Localization/date validation: 15 Python and five JVM tests passed; debug/local
release APKs, Android test APK compilation and debug lint passed (6m14s).
aapt verified default English and German launcher labels. Both artifacts contain
five localized pack names and all 84 distinct topic labels (32 Russian, 52 Polish),
with unchanged 1,722 questions. No device install/runtime check; UI tests compile
but remain pending. Date display no longer includes UTC. No new downloads.

Interface translations now live in app/src/main/res/values/strings.xml and
values-de/strings.xml (58 entries each). MainActivity Labels is now a resource
lookup helper, not an English/German text-pair table. All interface messages,
including guess-case instruction, use GUI-localized resources. Lessons and
pack/topic labels remain YAML. tests/test_ui_strings.py checks IDs/typed format
placeholders. Broader prototype shortcuts discussed in LOG; no rewrite authorized.

Latest interface migration build passed: debug/local release, Android test APK
compilation, JVM tests and debug lint (5m15s); translation parity check passed.
Runtime verification on a device remains pending. Owner uses GrapheneOS; Google
Play is not intended and F-Droid is only a possible channel. Private previews are
still development-signed. Publication signing and reproducible build-date strategy
remain open; no new key created. See LOG and TODOS for findings and proposals.

## End-of-day restart notes

README now includes the four owner-supplied screenshots from screenshots/ in a
two-column gallery: main menu, Russian genitive topics, German genitive practice,
and guess-the-case feedback. All four were visually inspected; paths verified.
Keep original files/names unless a later change requires renaming them.

Today's source work and documentation are uncommitted, including new resources,
German/deep packs, screenshots and tests. No build or action remains running.
Resume with MAIN/TODOS/recent LOG, then prioritize phone/runtime checks (including
GUI language, speech, automatic continuation and guess-case count) and content
review. Signing choices remain deferred until public distribution is planned.

Latest extension: GUI now supports English/German/Russian/Polish; four resource
files contain 60 matching entries. Settings choices are in two rows; launcher
names and all five pack names/84 topic labels include Russian/Polish. Authored
sentence translations were not added; missing translations show the localized
notice, same-language translations stay hidden. Native-speaker/device review pending.

Russian/Polish GUI validation complete: offline debug and private release builds,
Android test APK compilation, five JVM tests and debug lint passed (7m13s).
All 16 Python checks passed across the full run and the corrected packaging-check
rerun: its old two-locale expectation was updated to four. Resource IDs and typed
placeholders match across all four 60-entry files; all pack/topic labels include
four locales. Phone execution and native-speaker review remain pending. Both APKs
are ready at the usual distribution paths; no build is running.
