# First prototype implementation

User authorized autonomous continuation on 2026-10-10. The following are initial
implementation choices for review, not additional confirmed product requirements.

## Behavior

- Native Kotlin/Compose, bundled offline content, no backend or internet permission.
- English/German interface controls; Russian/Polish learning packs independently selected.
- Native sentence translations follow the interface language. Missing translations
  produce an explicit message rather than silently switching languages.
- Case menu opens a noun/adjective-numeral track menu. Case/track sessions include
  all authored questions for that combination (currently 15).
- Mixed mode samples 15 authored questions without replacement within one learning
  language, uniformly over questions, rather than composing unrelated word pairs.
- Authored blank-and-dictionary-hint prompts appear unchanged.
- Adjective/ordinal hints contain both dictionary forms, with no inflected noun
  in the sentence; their choices still test the adjective/ordinal alone.
- Device light/dark mode is followed; Android 12+ uses dynamic Material colors,
  Android 10/11 built-in palettes. Green/red feedback uses suitable dark variants.
- Settings displays version 0.1 and the build date captured in UTC by Gradle.
- First selection scores and locks the answer. Correct/wrong choices show text plus
  green/red; a wrong selection also reveals the correct answer. Next requires an answer.
- Speech reads the selected item, even if wrong, using an installed offline voice
  in the learning language. Voices marked as not installed are excluded. Missing
  voice/init errors appear above the bottom controls in a nonblocking snackbar.
- Results show score/total and percentage. Repeat retains the question set and
  reshuffles options; Back returns to the originating case/track or main menu.
- Settings persist in Android SharedPreferences. Current question IDs, answers,
  position and shuffle seed use saved instance state so rotation/recreation preserves
  progress. There is no learning-history database or long-term progress tracking yet.
- Draft content is labelled on the debug menu. Release build requires reviewed
  YAML, and the Android loader also excludes draft samples outside debug.

## Files and build

MainActivity.kt contains Compose screens and state. Lessons.kt loads the generated
JSON asset; Practice.kt contains pure sampling/shuffling/scoring rules. The YAML
source of truth remains samples/. package-content.py validates and deterministically
packages it for Gradle through the generated-assets variant API. Build requires
Python 3.12/PyYAML as documented; no Android YAML library is needed.

AGP 9.1.1, Gradle 9.3.1, built-in Kotlin and Compose compiler 2.2.10,
Compose BOM 2026.04.01, Activity Compose 1.10.1, compile/target SDK 36,
Build Tools 36.0.0, minimum SDK 29 (Android 10), bytecode target Java 17. Host build runs on
Studio's bundled Java 25.0.3. Application ID org.slaviccases.app is provisional
and must be finalized before public distribution. MIT license remains unchanged.

Gradle distribution is checked against its officially published SHA-256. Dependency
verification metadata is generated from the initial trusted repository bootstrap;
it is a recorded baseline, not independent cryptographic provenance. Subsequent
builds verify those hashes. Install-build-tools.sh owns Gradle/dependency downloads;
build.sh uses the existing installation and --offline. SDK package archives/revisions
are resolved by Google's SDK tooling, independently of bootstrap archive hashes.

## Validation scope

Visual checks: [menu](reference/prototype-menu.png),
[question](reference/prototype-question.png), and
[incorrect-answer feedback](reference/prototype-feedback.png). Small displays
scroll the question body; Speak and Next stay at the bottom.

Existing content validator regressions, deterministic asset integration test,
JVM session-rule tests, Android lint/build, and Compose instrumented session tests.
Actual results are recorded in LOG.md as completed. Instrumented tests cover full
session/results/repeat, recreation, wrong-answer locking, and mixed-mode Back.
Language material still requires human review; speech voice quality and physical
phone voice quality need manual testing; user confirmed basic phone operation.
Latest version/prompt changes passed build, JVM/content checks and emulator visual
checks; instrumented tests last ran before these later changes (see HANDOVER.md).
No publication, commit or push is authorized
or performed as part of this prototype work.
