# Project log

## Prototype implementation in progress — 2026-10-10

User completed SDK installation and authorized continuing implementation while
away, using judgment unless an immediate answer is required. Verified API 36
platform revision 2, Build Tools 36.0.0 and Platform Tools 37.0.1. Selected the
documented native Kotlin/Compose baseline as an implementation choice, not a newly
confirmed product preference: AGP 9.1.1, Gradle 9.3.1, built-in Kotlin/Compose
compiler 2.2.10, Compose BOM 2026.04.01, Activity Compose 1.10.1, minSdk 26.
Added reusable checksum-verified Gradle bootstrap and offline build scripts,
generated JSON packaging from validated authoritative YAML, and initial screens.
Generated assets now use the AGP variant API after first-build API validation failed.
All 390 questions and 11 existing content regression checks pass.

SDK Manager deprecation is confirmed by official Android documentation:
https://developer.android.com/tools/sdkmanager . Replacement Android CLI launcher
exists in the installed CLI package. Invoking help unexpectedly downloaded/unpacked
its runtime; this operation should have been scripted beforehand. Recorded the
inspection command in scripts/inspect-android-cli.sh (metrics disabled for subsequent
calls). Defer migration until the separate runtime can be independently pinned and
verified; existing sdkmanager remains usable. No license was accepted by the agent.
Optional emulator setup is scripted for API 36 Google APIs x86-64; existing KVM
access is available and no physical phone was connected. Declined an unrelated
unaccepted repository license prompt; selected packages are installing with the
user's existing SDK license acceptance.

## Beginner setup documentation — 2026-10-10

User requested a visible README link and development setup for Android beginners.
Added an early README setup section linking to DEVELOPMENT.md's sequential guide:
prerequisites, Studio/CLI and SDK installation, license prompts, verification,
environment scope, Studio startup and common errors. Explained that build/run and
device deployment await scaffolding, and retained proposed choices as proposals.
No installation performed as part of this documentation change.

## 2026-10-10

User requested an open-source Android app for learning Slavic cases, starting with
Russian and extending to all Slavic languages. Requested durable discussion/build
records in AI/, following polar-web-app, and reusable scripts for every install.
Later requested run-codex.sh containing the current chat ID.

Inspected sibling MAIN.md and LOG.md; adopted focused Markdown knowledge base
with executable scripts outside AI/. Retained existing MIT license.
Created contributor instructions, planning documents, setup instructions, pinned
checksum-verifying Android tool installer, and executable local chat resume script.
Recorded Kotlin/Compose and offline language packs as proposals.
Verified official Google download metadata; no development tools installed yet.
Validation: bash -n passed for both scripts; installer --help passed.
Installation, app builds, and actual chat resumption have not been exercised.

### Learning flow discussion

User specified startup menu with seven cases and mixed random noun/adjective/case
mode; simple contributor sample files; 15 example sentences for each "pair of case
and adjective"; separate GUI and learning-language settings; native-language example
and neutral question; four answers; green/red feedback; selected-item speech at
bottom left; Next at bottom right; results with Repeat or back one menu step.
Recorded requirements in UI.md and drafted CONTENT_FORMAT.md plus a one-question
YAML illustration under AI/reference/. Asked clarification about 15-sentence grouping
and native-text language. Other implementation choices remain explicitly proposed.
Verified Russian's six teaching cases with the University of Kansas course; the
requested seventh case remains an open product decision. No application implemented
or dependencies installed during this documentation work.

### Language cases and sample organization clarified

User confirmed six cases for Russian, requested a maximum of eight for each
language, separate language sample folders plus a templates folder, and native
sentence + neutral learning-language prompt in both samples and templates.
Created samples/ru/ with a six-case language definition and the illustrative draft;
created samples/templates/ with sample and language templates. Historical example
location now points contributors to the current draft. Updated current requirements
and removed the resolved seventh-case question. Vocative/other case treatment for
other languages awaits reviewed definitions. The exact 15-sentence grouping and
native-text selection setting remain unresolved. YAML remains a format proposal.
No application implementation or dependency installation was performed.

### Full starter sets, numerals, and public contribution guide

User clarified separate noun/adjective sets, inclusion of numbers in adjective
sets, accepted YAML, and requested a full implementation set including Polish.
Implemented the initial grouping as 15 questions per case per track: Russian
6×2×15=180 and Polish 7×2×15=210. Created 26 sample files, separate track templates,
a Polish language definition, a refusing-overwrite original-content exporter,
and a structural validator. English/German native sentences are included.
Adjective tracks contain explicitly labelled cardinal/ordinal numerals; Polish
vocative uses ordinal direct-address examples and instructions specifying the
traditional vocative. Cardinal answers can include the whole noun phrase.
All content is original AI-assisted MIT draft material pending linguistic review.

User also requested README instructions for creating sets and contributing or
providing GitHub feedback, then a personal introduction like the Polar project
about AI-driven development and the desire to learn Russian cases. Added these
sections with repository-specific fork/issue links and a clear app-development
status. Checked official GitHub workflow documentation. No issues, pull requests,
messages, commits or pushes were sent to GitHub.

Used existing PyYAML 6.0.1 without installing dependencies. Prepared a separate
Linux Python 3.12 dependency installer with official wheel SHA-256 hashes; it
has not been executed. Updating .gitignore failed with PermissionError even
outside the sandbox; the file was preserved and the tool environment defaults
outside the checkout. Final checks and any remaining limitations are recorded
below after verification.

Final verification: all 390 questions passed structural validation; all 11
focused regression checks passed. Installer shell syntax and --help passed without
installation. Python syntax, YAML parsing of all templates, 15-question template
counts and local README/documentation links passed. Linguistic review and Android
importer/build/device validation remain outstanding. No external publication or
installation occurred.

### Setup readiness before compaction

User asked whether any basic-setup topics block implementation and plans to
compact the chat, then run the installer. Reviewed scripts and project notes;
confirmed installer prerequisites and syntax. No product-design blockers to a
first prototype. Build-tool version selection, SDK components and device/emulator
setup remain normal next-phase tasks. Plain installer command only installs
Studio and SDK CLI, not platform/build/device packages.
Recorded provisional interaction defaults and next steps in HANDOVER.md rather
than treating unresolved settings/scoring/session choices as agreed requirements.
Observed working tree on CIFS/SMB, home ~51 GB free and root/tmp ~7.7 GB free; first
Gradle build must verify filesystem compatibility. No installation was performed.

### Android tools installed by user

User reports tools installed. Read-only verification found Studio build
AI-262.9437.185.2621.16467767, SDK CLI revision 22.0 and a working bundled
OpenJDK 25.0.3. SDK currently contains only cmdline-tools; platform/build-tools
and device tooling still need scripted setup. No further downloads or installs
performed. Updated setup status; application scaffolding and build remain next.

### Proposed first prototype build selection — 2026-10-10

User asked how to select platform and remaining tools. Recommend, not yet agreed:
minSdk 26 (Android 8), compileSdk/targetSdk 36 (Android 16), Build Tools 36.0.0,
platform-tools for adb, AGP 9.1.1 with Gradle 9.3.1. This is a conservative
baseline, not a claim that API 36 is the newest available platform. Minimum SDK
controls supported devices; compile SDK controls available APIs; target SDK
selects runtime behavior. No app feature currently demands a higher minimum.
AGP documentation specifies Gradle 9.3.1, Build Tools 36.0.0 and minimum JDK 17;
Gradle supports running on Java 25 starting at 9.1.0. Try installed JDK 25 with
this combination and verify the actual build before claiming end-to-end support.
Kotlin/Compose versions remain to be pinned during scaffolding. Start testing
on a physical phone if available; emulator/system image optional and selected
based on host architecture and test API. No NDK/CMake needed for proposed Kotlin app.
Install packages through existing reusable script:
bash scripts/install-android-tools.sh --sdk-packages 'platforms;android-36' 'build-tools;36.0.0' 'platform-tools'
No downloads/installations executed in this discussion.
Sources: https://developer.android.com/about/versions/16/setup-sdk
https://developer.android.com/build/releases/agp-9-1-0-release-notes
https://docs.gradle.org/current/userguide/compatibility.html

### First prototype verified

Completed case/track/mixed practice, independent English/German GUI and RU/PL
learning settings, authored prompts, shuffled four-choice answers, locked scoring,
color/text feedback, speech with offline installed-voice filtering and visible
snackbar errors, Next/results/repeat/back. Settings persist and session recreation
is covered. Defaults remain explicitly provisional in PROTOTYPE.md.

First Gradle build passed, but editing the still-running installer caused a shell
continuation error; rerunning the final script succeeded. Incremental resource
cache duplicated newly added resources; a clean build cleared it. One client
connection terminated mid-build; retry with two Gradle workers succeeded. Initial
emulator first boot produced stock launcher/System UI ANRs under CPU pressure;
after boot settled and reducing resolution/density, app checks passed. Inspected
errors did not show an app crash. Screen-test assertions were corrected to scope
selected language chips and scroll to feedback on smaller displays.

Final offline command: bash scripts/build.sh assembleDebug testDebugUnitTest
lintDebug connectedDebugAndroidTest — PASS. Three JVM and three emulator tests
passed, including a complete 15-question session/repeat, recreation, wrong-answer
locking, mixed mode Back and independent language settings/persistence. Speech
button enablement/selection was exercised; voice quality remains manual work.
All 390 content questions, 11 content regressions and one asset integration test
passed. Lint: zero errors; newer-version/KTX suggestions and nonblocking SDK XML
and legacy Compose test API warnings remain. Release guard intentionally rejected
drafts through :app:validateReleaseContent. Only whitespace formatting changed
after the complete successful app test run.

Gradle archive/wrapper official hashes verified; strict repository dependency
verification records 854 artifacts. Gradle/dependency and optional emulator setup
are in reusable scripts; SDK license handling now prompts only for requested
packages, avoiding unrelated repository license prompts. Emulator revision 37.2.12,
Google APIs API 36 x86-64 image revision 7. SDK package revision pin limitations
are documented. No license accepted by the agent; SDK packages used user acceptance.
Visual references and current handover saved in AI/. README links setup/build/phone
instructions. No commit, push or publication performed. Linguistic review, physical
phone testing and independently pinned Android CLI migration remain follow-ups.

Final artifact/documentation check: debug APK is 11.0 MiB and contains all 390
questions; README/setup/screenshot links exist; git diff --check passed. Stopped
only the headless test emulator on port 5580 after verification. No device or
build process remains pending. All source/build notes remain local changes.

### Required ripgrep tool

User requested adding `sudo apt install ripgrep` to the required tools.
Added `rg` to the development prerequisites and the reusable
scripts/install-system-tools.sh installer containing that command. Emulator setup
now checks for rg before installing SDK packages. APT uses the distribution's
authenticated package repositories rather than a pinned downloaded archive.
Installation was not requested or executed. Both installer scripts passed bash
syntax validation.

### Emulator usability

User reported very slow emulator and apparent Google setup requirement. Inspected
running emulator-5580: KVM usable, software SwiftShader rendering, two CPU cores,
snapshot disabled, display already reduced to 720x1280; host had 2.5 GiB swap in
use. Android device_provisioned and user_setup_complete were both 1. Our app was
not installed. Installed existing debug APK and launched MainActivity successfully
using new reusable scripts/run-app.sh; no Google account or download needed.
Updated run-emulator.sh to use GPU auto and allow Quick Boot snapshots, retaining
two cores and skipping boot animation; enabled audio for speech checks. Existing
running emulator was not restarted, so speed improvement remains unverified.
Both scripts passed bash syntax checks. Setup guide explains direct app launch,
graphics fallbacks and snapshot saving; official acceleration documentation:
https://developer.android.com/studio/run/emulator-acceleration

### Question answer visibility

User confirmed emulator works reasonably well and supplied a screenshot showing
the fourth answer clipped above the bottom controls. Reduced question-only column
spacing from 12 to 8 dp and vertical padding from 20 to 8 dp; button sizes and
fixed Speak/Next controls retained, scrolling remains available for longer content.
Offline assembleDebug passed. Installed updated APK on emulator-5554 and visually
verified Russian accusative noun practice at 720x1280 / 280 dpi: all four answer
buttons fully visible above bottom controls without scrolling. Screenshot saved
as AI/reference/prototype-question-spacing.png. No full regression suite rerun
for this spacing-only change. Installation restarted the app; left it at the first
accusative noun question for the user.

### Device theme and minimum Android version

User requested dark mode or device theming and said Android 8 support is no longer
needed. Implemented system light/dark following and Android 12+ dynamic Material
colors; Android 10/11 use built-in palettes. Green/red feedback has separate dark
colors with readable foregrounds. Chose minimum SDK 29 (Android 10) as an
implementation default consistent with system-wide dark mode, not a technical
requirement imposed by Compose. Compile/target SDK remain 36. Updated current
setup/prototype requirements; earlier Android 8 build-selection notes are history.
User asked about phone installation: documented direct APK transfer or adb helper,
Android 10+, installation permission for the chosen file source, no Google account.
Offline assembleDebug and lintDebug passed. Installed on emulator-5554, visually
checked dark menu and wrong/correct feedback and restored original light setting.
Reference screenshots: prototype-dark-menu.png and prototype-dark-feedback.png.
Android 10/11 fallback palette has not been device-tested. No new dependencies or
downloads. Official references:
https://developer.android.com/develop/ui/compose/designsystems/material3
https://developer.android.com/develop/ui/views/theming/darktheme

### Version display and non-revealing adjective hints

User confirmed the APK works on their phone. Requested Settings version 0.1 and
build date, and adjective prompts without an inflected noun revealing agreement.
Changed versionName to 0.1 (versionCode remains 1 during this initial development
iteration). BuildConfig captures the Gradle build/configuration date as ISO UTC;
Settings displays it in English/German, independent of installation date.
Changed only neutral_prompt in 159 Russian/Polish adjective and ordinal questions:
e.g. Я вижу ___. (добрый брат). Both dictionary forms are in the hint; options and
scoring still test the adjective/ordinal alone. Cardinal phrase questions already
used neutral noun hints and remain unchanged. Updated generator, template and
content authoring instructions; preserved all other lesson fields and draft status.
Validation: all 390 questions structurally valid; offline assembleDebug and three
JVM tests passed; 12 existing Python content/packaging regressions passed;
git diff --check passed. Installed on emulator-5554 and visually confirmed Settings
version/date and the Russian accusative adjective prompt, with four answers fully
visible. References: prototype-settings-version.png and
prototype-adjective-neutral.png. No download, commit or publication performed.

### End-of-day handover for compaction

User requested updating relevant notes before compacting/closing for today.
Refreshed HANDOVER, TODOS, PROTOTYPE and UI with phone success, version/date,
Android 10 minimum, device themes, corrected adjective hints, spacing fix, current
emulator helper behavior and exact validation scope. Distinguished earlier full
instrumented run from latest build/JVM/Python/visual checks. Recorded remaining
voice quality/accessibility, Android 10/11 fallback, linguistic review, CLI
migration and release work. User emulator-5554 remains running; no build pending.
Changes remain local; no assistant commit/push/publication. No immediate question
or blocker prevents continuing next session. Documentation whitespace check passed.

## 2026-10-11 — Topic packs and manual themes

User supplied ru-v2/pl-v2 and the sibling cyrillic-grouped.md reference. Implemented
case → track → authored topic → gender subgroup (gender exercises only), separate
pack IDs/Settings entries, variable question counts and three-choice gender items.
Preserved original starter behavior. IDs are scoped per pack because Polish
vocative samples reuse legacy IDs; extra German vocative translations are allowed.
New content remains YAML schema 1, rather than silently changing schema versions.
Added upper-right Light/Dark button with saved preference and system initial default;
passed effective theme into feedback colors. Previous version only followed device.

Validated 1,602 questions: 390 originals, 591 ru-v2 (43 topics matching reference
count), 621 pl-v2. Reusable audit script/report records topic sizes, null features
and three Russian duplicate-option questions. Source material and Polish adaptations
declare unspecified licenses. Retained provenance and blocked release validation
until permissions/review are recorded; local draft preview is not redistribution
approval. No downloads, installs, commits or publication performed.
All 13 Python regressions passed, including full-pack identity/topic/choice test.
Added Android regression for gender navigation/theme persistence; adjusted older
tests to distinguish pack IDs from learning-language codes. No adb device available,
so runtime UI/instrumented verification remains pending.

Offline assembleDebug, three JVM tests and lintDebug passed. Initial sandbox build
could not load Gradle native services; reran with approved access to installed
host tooling. Existing SDK XML warning remains nonblocking. Audit flags 601
questions with at least one unknown/null grammatical feature. git diff --check passed.
Updated debug APK: app/build/outputs/apk/debug/app-debug.apk.

## 2026-10-11 — Clipped answer feedback

User screenshot shows only the top pixels of the feedback paragraph below four
answers. Moved feedback out of the scrolling question column into the fixed bottom
control area above Speak/Next. Scaffold reserves its full measured height, including
wrapped feedback; long questions/answers remain scrollable. No content or scoring
change. Offline APK build requested; validation result follows.

Validation: offline assembleDebug passed and git diff --check passed. Installed on
emulator-5554 and selected a wrong answer in Russian v2 genitive practice. Verified
full feedback bounds [28,1070][610,1112] above Speak [70,1151][139,1186],
visually inspected AI/reference/prototype-fixed-feedback.png. Footer feedback
is fully visible; answer list still scrolls when its height exceeds available
space. No broad regression suite rerun for this layout-only change. Emulator left
running at the checked practice question.

## 2026-10-11 — Version 0.2 and local release artifact

User requested simple/deep pack labels, a release version and version 0.2.
Changed manifest names and removed inferred v2 suffix; saved IDs unchanged.
Updated instrumented selectors and packaging name assertion. VersionCode is 2.
Added explicit localReleasePreview property and reusable build helper: release
is non-debuggable and uses existing development key for private phone testing.
Drafts are included explicitly without marking them reviewed or licensed.
Normal publication build keeps content checks. No public release or upload.

During the build user asked about common development environments. Recommended
already-installed Android Studio for editing, emulator/phone Run/Debug, Compose
inspection and Logcat; terminal scripts remain useful alongside it. Recorded setup
context and official IDE introduction in DEVELOPMENT.md.

Verified installed Studio bin/studio and bin/studio.sh exist; gave the default
launcher location. Release APK signature v2 verifies; aapt confirms version 0.2,
versionCode 2, minSdk 29, targetSdk 36 and no application-debuggable flag. Asset
contains all four simple/deep names and 1,602 questions. Packaging name regression
passed. Final build/lint result follows.

Offline assembleDebug, assembleRelease (explicit local preview), three JVM tests
and lintRelease all passed. Build duration 5m48s for first release variant.
Release artifact: app/build/outputs/apk/release/app-release.apk; no install or
publication performed. Reusable build helper passed bash syntax validation.

## 2026-10-11 — Friendly APK filenames

User requested slavic-cases.apk and slavic-cases-debug.apk. Added variant-aware
Gradle Copy exports to app/build/distributions/ wired into assemble tasks using
SingleArtifact.APK provider. Kept original AGP output/installation metadata intact;
exported APK bytes and signatures are unchanged. Updated current README/setup/
handover paths and run-app.sh. No app display name, version, package ID or signing
change. Historical LOG artifact paths intentionally preserved.

User confirmed finding Android Studio and creating its desktop link; requested
recording this in Markdown. Added confirmation to handover and reusable
Tools → Create Desktop Entry instructions to DEVELOPMENT.md. No desktop files
or machine-specific launcher paths added to the repository.

Validation: offline assembleDebug/assembleRelease with local preview passed.
Both renamed exports are SHA-256 identical to their source APKs (signatures
preserved); shell syntax and documentation whitespace checks passed. No runtime
suite rerun for artifact naming and documentation only. No publication/install.

## 2026-10-11 — Closing handover

User requested relevant file updates before closing. Replaced accumulated handover
with current 0.2 status, simple/deep navigation, manual themes, fixed feedback,
private release/signing limits, final artifact names and exact validation scope.
Refreshed MAIN, UI, PROTOTYPE and TODOS to remove stale current-version/flow claims.
Preserved historical work in this log. Recorded owner desktop launcher success.
Noted newly present untracked Gradle daemon JVM criteria file without modifying it;
it needs review for toolchain download behavior before adoption. User emulator
left running, no build pending, no commit/push/publication performed.

## 2026-10-11 — Architecture walkthrough

User requested a quick explanation of the app's inner workings and confirmed
there are three production Kotlin files. Explained MainActivity.kt as Compose UI,
navigation, saved session state, preferences, themes and Android speech;
Lessons.kt as data models and bundled JSON loader; Practice.kt as pure shuffle
and scoring rules. Content is authored in YAML, validated/converted by Python at
build time and bundled as JSON. Test Kotlin files are separate from production.
This is a compact prototype; splitting screens can follow as complexity grows.
Documentation-only discussion record; no app changes or tests required.

## 2026-10-11 — Automatic continuation setting

User requested a setting for automatic continuation. Added saved autoContinue
preference and English/German Settings switch. Chosen implementation defaults:
off, 2-second feedback delay for either answer outcome; final answer shows results.
Shared next action serves timer and manual button. Compose effect cancellation
handles manual Next/back/new sessions; Speak pauses advance for the current
question so pronunciation is not interrupted. No version bump requested.

Validation: offline assembleDebug passed (2m15s), including Kotlin compilation
and exported slavic-cases-debug.apk. git diff --check passed. Sandbox native
library initialization failed initially; host build succeeded. No device runtime
check, release rebuild, install or publication performed for this addition.

## 2026-10-11 — Guess the case

User requested random guess-the-case mode, default 30 questions with configurable
Settings count. Added persisted count (implementation range 1–200), main-menu
button and saved session mode. Pool is all questions of the selected language
pack across tracks/topics/cases, without replacement. Generated case questions
use authored correct form to fill blanks and identify target form explicitly (→).
Offer all cases of that pack, hiding the case from progress heading; source YAML
is unchanged. Shared answer feedback/results/auto-continuation work in both modes.
Speech reads target form. Added JVM checks for conversion, case identity, source
translation preservation, default 30 and small-pool behavior.

Validation: offline assembleDebug and testDebugUnitTest passed (2m30s), including
five JVM practice tests. Updated debug export contains both new settings/mode.
README and AI notes updated; git diff --check passed. No device runtime test,
release rebuild, install or publication performed.

## 2026-10-11 — Scope expansion to German and app rename

User requested Learn Grammatical Cases as the app name and a German lesson basis.
Added German simple (de): 120 original MIT draft questions, four cases, 15 per
case/track. Whole-phrase answers teach articles, genders, singular genitives,
weak masculine nouns, plural dative and weak/mixed/strong adjective patterns,
including cardinal/ordinal numerals. Reusable original exporter refuses overwrite;
YAML remains authoritative. Grammar references checked against IDS grammis and
recorded in AI/LINKS and samples/de/README. Independent review remains pending.
App label/header and Gradle project/APK names renamed. Android ID/namespace kept
for update/settings continuity, installer paths/repository URL unchanged.
Same-language native translations hidden so German GUI does not reveal answers.
Version remains 0.2. Added German structural/grammar regression checks and an
Android UI test for four-case navigation/translation hiding (device unavailable).

Validation exposed six existing Russian deep files missing contributor metadata;
added explicit unknown-original-author labels preserving sources/license/draft.
More Russian files subsequently lost the field while work was running; asked
whether user is concurrently editing/regenerating them. Do not infer authorship
or redistribution permission. Full validation/build status will follow.

Russian import files continued losing contributor fields during work. Reverted
only this turn's inserted contributor lines. Import-specific validation now allows
unknown author only for apk-topic-import with retained per-question source records,
sources and license; packaging labels the author explicitly unknown in JSON.
Original/simple/adaptation sets still require contributor. Release review/license
guards unchanged. This avoids repeated changes to externally edited source YAML.
First combined build stopped at missing contributor; rebuilding after this fix.
German-only checks passed; no connected device reported by adb.

Final validation: all 1,722 draft questions pass structure; 15 Python and five
JVM checks pass. Offline assembleDebug, explicit local-preview assembleRelease,
assembleDebugAndroidTest and lintDebug pass (6m38s). aapt confirms Learn Grammatical
Cases launcher label, unchanged org.slaviccases.app identity, version 0.2/code 2.
Both exports match internal APK SHA-256 and contain five packs / 1,722 questions;
German has four cases and 120 questions. Local release signature verifies.
No connected emulator/phone: five UI tests compiled but not run. No new downloads,
installations, commit, push or publication. README, sample guide, AI scope/design/
setup/handover/research notes updated for German and naming. Device testing and
independent German linguistic review remain pending.

## 2026-10-11 — Localized launcher and in-app name

User asked whether the phone launcher and app title can be translated. Added
values-de app_name Grammatische Fälle lernen, using the existing manifest resource
label; English remains the default. In-app title now loads app_name through a
configuration context for the saved GUI language, avoiding dependence on device
locale. Both header and load-error title share it. Launcher locale is Android's
choice, independent of the app's internal GUI preference. Consulted official
Android localization guide; no dependencies/downloads or app identity change.

While the localization build was running, user requested removing the UTC marker
from the date-only build date. Will remove the Settings suffix and rebuild after
the current source-reading build completes. Underlying date generation unchanged.

User further identified English-only sample selection buttons. Extend the pending
fix to localized language-pack names in Settings/header and authored topic labels
in deep menus. Store translations with pack metadata, retaining stable IDs and
original fallback names. Existing build finishes before modifying source inputs.

Localization-only builds completed, but debug lint correctly caught reading device
Configuration through LocalContext (could become stale). Fixed by observing
LocalConfiguration and keying title lookup on configuration and GUI changes.
Then applied user steering: date-only Settings suffix removed; manifest names and
topic_names provide English/German pack/topic labels; loader and UI use them in
selection chips, header and deep menus. Translations remain separate from source
questions/native texts. Added metadata validation, extended packaging coverage
check, and updated GUI persistence test to check German title/pack labels.
Rebuilding both APKs, compiling Android tests, rerunning JVM/Python/lint checks.

Final localization/date validation: offline debug/local release builds, Android
UI-test APK compilation, five JVM tests and debug lint passed (6m14s). All 15
Python checks and 1,722-question structure validation passed. aapt verified default
Learn Grammatical Cases and German Grammatische Fälle lernen launcher labels.
Both APKs bundle five translated pack names and 84 topic labels (32 RU, 52 PL).
Original names/IDs remain intact; unknown-label fallback remains for older packs.
Whitespace check passed. No emulator/phone install or runtime check, download,
publication or commit. In-app title/selection labels follow GUI setting; launcher
follows Android locale; date-only Settings value no longer includes UTC.

## 2026-10-11 — Interface string resources

User asked where button translations live and why Kotlin pairs were used.
Explained that this was a first-prototype implementation shortcut, not an Android
requirement/user preference. User agreed to migrate to localized strings.xml.
Moved all interface literals into 58 English/default and German resource entries:
buttons, settings/headings, cases/genders, speech/error notices, answer feedback,
guess-case instruction, formatted counts/progress/results/version/date. Resource
lookup uses saved GUI locale and observes device configuration changes. Full
formatted phrases use numbered typed placeholders rather than concatenated labels.
Practice rules no longer embed the guess-case UI instruction. Authored lessons and
pack/topic names remain YAML. Added translation ID/typed-placeholder parity check.

User asked about other prototype shortcuts while work continued. Explained the
large MainActivity, string-based routes, SharedPreferences/saved session state,
bundled-only content (no Android importer/author preview), fixed mixed size 15,
draft content and development-signed private release. This is disclosure of current
implementation/limits, not authorization or an agreed plan to rewrite them.

Interface migration validation: offline debug/local release builds, Android test
APK compilation, JVM tests and debug lint passed (5m15s). New XML translation
parity check passed. Device execution remains pending.

User clarified Google Play is not intended, F-Droid may be used, and the current
phone runs GrapheneOS. Research: APK signing is required for direct installs too;
GrapheneOS uses Android application signing, separate from OS verified-boot keys.
Current local release explicitly uses the debug signing configuration. Recommend
a separate protected release key for developer-distributed APKs; this is a
proposal, no key generated. F-Droid normally builds/signs with its own per-app key;
verified reproducible builds can retain the developer signature. Different signing
identities normally prevent in-place updates; plan the testing-to-release transition.
Current wall-clock BUILD_DATE needs a reproducible value if pursuing that route.
Sources: https://developer.android.com/studio/publish/app-signing ;
https://f-droid.org/docs/FAQ_-_App_Developers/ ;
https://f-droid.org/docs/Reproducible_Builds/ ; https://grapheneos.org/usage .
No publication, signing-key creation, download or installation performed.

## 2026-10-11 — README screenshots

User supplied four screenshots and requested adding them to README based on their
names. Visually inspected all four: main menu, Russian deep genitive topic menu,
German genitive adjective practice, and Russian guess-the-case feedback. Added a
two-column gallery near the top with descriptive captions/alt text and 280-pixel
display widths. Original screenshot files and filenames remain unchanged.
Verified all gallery paths exist and whitespace checks pass; no app build needed.

## 2026-10-11 — End-of-day handover

User requested final documentation updates before closing. Refreshed HANDOVER
with screenshots, current five-pack/1,722-question totals versus historical
four-pack validation, uncommitted work and restart priorities. Screenshot evidence
shows menus/feedback, but is not a complete newest-build runtime test. Updated
completed screenshot task in TODOS. Latest builds/checks remain those recorded
above; closing changes are documentation only, with whitespace validation. No
commit, push, publication, new installation or key generation requested/performed.

## 2026-10-11 — Russian and Polish GUI

User requested Russian and Polish interface translations before closing. Added
values-ru/values-pl resources, 60 entries matching English/German (including two
new language autonyms). Settings offers four saved GUI choices in two rows.
Launcher labels also localize. Added Russian/Polish pack and topic names to YAML
metadata without changing lesson texts, provenance or question counts. Missing
sentence translations stay explicit. Extended resource and packaging parity
checks; building debug/local release and compiling Android tests offline. Native
speaker and device review remain pending. No downloads or signing changes.

Russian/Polish GUI validation complete: offline debug and private release builds,
Android test APK compilation, five JVM tests and debug lint passed (7m13s).
All 16 Python checks passed across the full run and the corrected packaging-check
rerun: its old two-locale expectation was updated to four. Resource IDs and typed
placeholders match across all four 60-entry files; all pack/topic labels include
four locales. Phone execution and native-speaker review remain pending. Both APKs
are ready at the usual distribution paths; no build is running.

## 2026-10-14 — Host-specific chat launcher and sandbox diagnosis

User requested hostname-based chat selection, with the original ID assigned to
optiplex and an entry for the current PC. Added latitude5540 with its current
chat ID. Short-hostname selection preserves argument forwarding; unknown PCs
fail clearly. Updated DEVELOPMENT.md.

Sandbox commands failed with the loopback RTM_NEWADDR permission error. User
pointed to the prior bubblewrap repair notes. This PC allows user namespaces
(limit 55310) but enables AppArmor userns restriction and lacks both installed
and extra-source bwrap-userns-restrict profiles. Codex 0.162.1, bubblewrap 0.9.0.
The notes document installing/loading the AppArmor profile as the preferred
repair; no system settings or packages changed in this task.

Validation: Bash syntax passed; mocked executables verified both host mappings,
argument preservation and unknown-host failure. Git whitespace check passed.

## 2026-10-14 — Sandbox repair verification and CLI syntax correction

After the AppArmor repair instructions, user reported that the suggested
`codex sandbox linux -- /bin/true` panicked while trying to execute linux.
Installed Codex 0.162.1 help shows no linux subcommand: correct verification is
`codex sandbox -- /bin/true`. This command passed from /tmp with exit status 0.
Ordinary sandboxed tool commands now also execute successfully. The earlier
verification command was incorrect for this installed CLI.

## 2026-10-14 — Shared home wiki discovery (separate from app scope)

User requested a shared home llm-wiki based on the OKF specification used at
work, for faster troubleshooting and generalized knowledge across home PCs.
Inspected the network share at directory level and document-area file metadata.
Created provisional README, SETUP, and SOURCE_INVENTORY in the requested wiki
folder. No source files moved or bulk imported. Exact OKF specification, audience,
source-retention policy, and starting subjects remain open questions. Proposed
curated summaries/playbooks and source links are not agreed decisions. This is
separate knowledge-management work, not an expansion of the Android app scope.

## 2026-10-14 — Home wiki pilot and archive move

User chose a troubleshooting pilot and then explicitly requested moving the
problem archive into the wiki while retaining browseable files and folders.
Moved its eight files into llm-wiki/problem-solvers with original topic folders
and filenames; verified relative names and sizes. Updated wiki inventory links
and recorded the decision there. Wiki is now the archive home. No content
conversion yet; a preserved credentials file was not read or indexed.

## 2026-10-14 — Home wiki language and navigation

User chose mostly English and intends to browse with a tool such as Obsidian.
Added six standard Markdown indexes in the shared wiki, preserving original
notes. All 14 index links validated. Maintenance workflow and OKF conversion
remain pending; no reader installation or plugin setup performed.

## 2026-10-14 — Automatic wiki maintenance and reusable setup

User authorized automatically saving important reusable topics, visibly
reporting edits, and asking in doubtful cases. Requested a dedicated setup
entry with copyable instructions. Implemented shared wiki AGENTS.md, setup
guide, log, and current bubblewrap playbook; updated navigation and added
OKF type metadata without rewriting incident bodies. OKF v0.2 is an
implementation choice. Added secret/reader-state ignore patterns without
initializing Git or reading credential contents. Validated metadata, indexes,
local links, and log date. Other projects need an explicit wiki pointer for
discovery; global agent configuration was not changed.

## 2026-10-14 — Quarterly shared-wiki change logs

User requested a short entry for every wiki change and quarterly rotation,
placing old logs in a log folder. Existing root log.md was present. Added a
standard-library Python helper that logs changes and rotates older date groups
to log/YYYY-QN/log.md; archive index and original entries retained. Rotation
is triggered by writes or explicitly, not scheduled. Updated wiki instructions,
setup guide, decisions, overview, navigation, and ignore rules; recorded eight
short entries for these changes. Isolated checks passed for quarter/year
rollover, relative-link preservation, idempotent retries, future-date refusal,
and conflicting archive preservation. Metadata and local-link validation passed.

## 2026-10-14 — Global Codex shared-wiki discovery

User requested wiki rules in every session and wiki as the nickname for queries
and explicit additions. Created a reusable installer in the shared wiki and
installed its block in this PC’s global Codex instructions, preserving project
rules. Installer check passed; the conversation subsequently received combined
global and project instructions, confirming discovery. Shared policy and setup
guide updated, all distinct changes logged through the quarterly helper. Other
PCs/profiles still require running the installer; no remote PC was configured.
Preservation/idempotence/override/path-update/malformed-marker checks passed;
metadata and links passed. Global instructions do not extend sandbox permissions.

## 2026-10-14 — Wiki installer write access

User requested explicit wiki access in the installer. Added merging of
sandbox_workspace_write.writable_roots with semantic TOML preservation checks,
retaining existing roots and approval/sandbox/network settings. --check now
checks access too. Isolated tests passed for nine TOML layouts, configuration
preservation, idempotence, missing access, malformed settings and header without
newline. Current real config merge verified read-only; installer was not applied
to the real Codex home, outside the current writable roots with approvals never.
Updated wiki instructions/docs and recorded five changes through quarterly log.
Metadata and local links passed. User should re-run installer in their terminal.

## 2026-10-14 — Imported problem-solver TXT conversion

User requested proper Markdown for the imported text notes and clarified the
credentials file was an incomplete reminder. Converted all four TXT notes,
using placeholders for the reminder and preserving other recorded expressions,
paths and commands. Added headings, code blocks, provenance/scope and OKF type
metadata; original TXT files replaced. Updated wiki indexes, source inventory,
template policy and setup notes; distinct changes logged. Metadata and links
validated; no TXT notes remain in problem-solvers. No operational commands
from the imported notes executed or newly claimed as verified.

## 2026-10-17 — Desktop sample editor

User requirements: PC app for existing sample editing; pack folder (ru, ru-v2,
pl, pl-v2, etc.) as project; recognize nouns/adjectives and case-prefixed filenames;
selectors plus free suffixes such as practice-1 and mnogo-malo. User suggested
Python. Implementation choice: Tkinter desktop forms, reusing existing PyYAML
and schema validation, without Android changes or new Python dependencies.

Added tools/sample_editor/model.py and app.py, reusable installer/launcher scripts,
usage/recovery guide, README entry and AI handover/setup/content notes. Case IDs
come from manifests. Question fields include native translations, dictionary form,
prompt, word type, scope, answer choices and correct key. Advanced YAML tabs keep
features, sources, instructions, topics and unknown fields. Add/duplicate/delete
questions, rename/move via save selectors, and copy with new IDs/draft status.
Saves validate the whole selected project before writing, keep local ignored
backups, detect external source changes and refuse destination collisions. Atomic
same-file replacement and exclusive new-file creation protect writes. Introductory
comments retained; PyYAML reformats files and drops inline/interior comments.
Topic metadata is independent from filename suffixes. Existing manifests are not
edited through dedicated forms; editor UI is English. These are implementation
limits, not additional agreed product requirements.

Validation: seven desktop persistence/compatibility integration tests passed,
covering all five project manifests/filenames and validator compatibility; save
round trips in all five packs preserve semantic data/source attribution; backups,
rename IDs, clone IDs/draft status, invalid-save refusal, collision protection,
stale-source refusal, suffix/path checks and duplicate YAML keys checked.
Python compilation, shell syntax and launcher help passed. Existing sample files
were not modified. Tkinter import failed on this host. Installer was written first,
then attempted; sudo requires an interactive password, so it stopped before apt
or venv changes. No archive download or new package installation occurred. GUI
window/interaction checks remain pending and are explicitly documented for the
owner. No Android build required; no commit/push/publication requested.

Final validation for this addition: the complete Python suite passed all 23 tests
in 115.488 seconds. An isolated temporary project on this SMB checkout additionally
passed validated save, backup creation and exclusive lesson copying; hard-link
creation is supported here. Temporary projects were removed. Final Python/shell
syntax and Git whitespace checks passed. Desktop-window testing is still pending.

## 2026-10-17 — Desktop editor portability and restricted forms (in progress)

User requested Windows support, Qt preference with Tkinter fallback, .po-format
internationalization and more restrictive editing for ordinary PC users. Follow-up
explicitly requested German, Russian and Polish PO catalogs. Implementation choices:
shared controller and typed fields, PySide6 then PyQt6 then Tkinter; explicit backend
and locale flags; gettext PO/MO with Babel authoring tools. No raw YAML input in
normal editor views; unknown/imported source fields remain read-only and preserved.

Pinned dependency locks were generated from public PyPI release metadata through
a reusable script. Isolated dependencies installed in /tmp through the new installer
with checksum checks: PyYAML 6.0.1, Babel 2.17.0, PySide6 Essentials/shiboken6 6.8.3,
pip bootstrap 25.0.1. No system packages changed. An attempted checkout-local venv
failed because SMB rejects its lib64 symlink; installer defaults moved to user-local
storage. Host lacks ensurepip/pip, so installer has an explicit pinned/hash-verified
pip-wheel bootstrap and uses venv without ensurepip. Windows setup includes opt-in
Python 3.12.10 x64 installation, SHA-256 checked against Microsoft's official winget
manifest and downloaded from python.org. Native Windows verification still pending.

Desktop refinement completed: restricted forms and shared navigation/save logic
in both views; Qt preference with explicit overrides; Windows x64 setup/launcher;
English POT, German/Russian/Polish PO and compiled MO catalogs covering all 97
interface messages. Runtime locale follows OS or --language. Project display names
follow the catalog locale. Technical model/validator diagnostics remain English.
All original samples are unchanged. Current setup/recovery/translation instructions
are in tools/sample_editor/README.md, README and AI/DEVELOPMENT.md.

Validation: full Python suite 29/29 passed (122.510 seconds), including actual Qt
Widgets form edits, navigation, save/reload, read-only fields and cancelled unsaved
navigation. Six focused backend/form/PO/Qt tests passed again (15.246 seconds) after
final view refinements. All 1,722 question forms round-trip semantically unchanged;
all five pack formats and existing regression checks pass. Catalog completeness,
placeholder checks, compiled runtime translations and localized schema-choice
stability pass. German offscreen Qt screenshot rendered to a temporary file and
visually inspected. Installer rerun succeeded using already installed pinned
packages and compiled all three catalogs. Python compilation, shell syntax and
launcher help checked. Windows saving uses exclusive os.rename instead of hard
links so non-NTFS volumes can work; this needs native Windows verification.

Remaining verification: native Windows/PowerShell, actual PyQt6 (selection tested
through a probe), visible Tkinter (module available, but display :0 inaccessible),
and native-speaker translation review. No Android build required. No system
package installation, secrets, original sample edits, commit, push or publication.

## 2026-10-17 — Clear lesson navigation and lesson Add/Delete

User reported confusing duplicate group/case selectors and requested lesson
Add/Delete controls like those for questions. Explained that the left pair browsed
lessons while the right pair changed save destination. Implementation choice:
remove the right pair, show a location label and provide an explicit Move lesson
dialog; relocation remains pending until Save. The free filename suffix remains.
Both views now have separate Add lesson/Delete lesson controls below the lessons.

Added original blank drafts with unique IDs, manifest-compatible metadata/profile,
15 starter questions or one deep-topic question, and numeral slots for starter
adjectives. Contributor/license/sources/instructions must be filled; no imported
source attribution is copied. Drafts remain in memory until valid first Save.
Deletion confirms, discards unsaved edits and moves the saved original into ignored
recovery backups; unsaved drafts never touch disk. External-change/collision checks
apply to first saves and deletion. A deleted last case/track may leave validation
incomplete until replacement/restoration; manifests are not altered.
Browse-filter changes now clear old details and retain the requested filter even
when Save during navigation refreshes selection. German/Russian/Polish catalogs
updated for the new actions/dialogs/status messages; usage guide updated.

Initial focused run caught fuzzy catalog entries while translations were still
being merged, plus test assumptions that input projects contained no recovery
backups. Tests now exclude existing user backup folders when copying fixtures;
user recovery files are untouched. New translations were completed and compiled.
Final validation follows below. No original sample changes, downloads, Android
build, commit or publication were needed for this task.

Final lesson-management validation: full suite 32/32 passed in 111.088 seconds.
Six focused UI/form/PO checks passed again in 15.212 seconds after the final
refinement, including acceptance/cancellation of the actual Qt Move dialog.
Checks cover blank drafts for starter/deep profiles, valid first saves, no file
on invalid first save, no fabricated source claims, unique IDs, backup-based
removal, external-change and collision protection, explicit pending relocation,
new-draft cancellation, deleted lesson recovery, and clearing discarded details
when browsing. All 106 desktop messages have complete de/ru/pl catalogs; compiled
catalog/placeholder checks pass. German Qt layout rendered and visually inspected.
Python compilation and Git whitespace checks passed. Native Windows/Tk display
limits remain as documented. Existing owner changes to the Russian masculine-plural
sample and local recovery backups were preserved, not reverted or edited by this task.

## 2026-10-17 — New project and usable empty-state authoring

User requested New project because startup had no way to choose cases/create
questions or save without an existing pack. Requested target language, cases,
directory and applicable defaults. Added a shared setup definition and Qt/Tk
creation dialogs: Russian six, Polish seven, German four cases; custom language
tag with explicit case selection; one to eight standard case categories; selected
native translations; new/empty directory only, default ~/case-samples/<code>.
Existing files are never overwritten. Project creation writes manifest/track
folders and opens a first unsaved 15-question noun lesson. New/Open stay enabled;
project/lesson actions are disabled until their prerequisites exist.

Found a functional obstacle to the first save: old saves demanded every case in
both tracks. Added an internal allow_incomplete authoring-validation option that
skips only empty track/missing-case coverage. All existing lesson fields/questions
still validate; strict defaults for CLI/build/package remain and release forcibly
disables the override. Editor staging normalizes its directory to the language
tag, allowing arbitrary working-folder names without changing Android pack naming.
New projects use the existing simple format; no import profile or invented sample
content/attribution. German/Russian/Polish PO/MO and guides updated.

Initial new-project regression fixture wrote a second copy of a lesson rather
than overwriting its copied test path, producing duplicate-ID rejection; corrected
the fixture path. Real Qt dialog/default/creation/first-save/reopen checks passed.
Final suite results follow below. Existing owner sample edits/backups preserved;
no installs, downloads, Android build, commit or publication needed.

Final New-project validation: full 36-test suite passed in 104.176 seconds.
After final folder/tag safeguards and dialog sizing, three setup/model checks
passed again in 0.374 seconds and seven UI/form/PO checks in 12.400 seconds.
Actual Qt dialogs verified language default inventories, checkbox adjustment,
cancellation, project creation, first save into an incomplete project, and reopen.
Model checks verify nonempty-folder preservation, custom directory names/language
codes, unsafe-tag rejection, first-save schema checks and strict release/build
coverage even when an incomplete-authoring override is requested. German startup
and New-dialog screenshots rendered and visually inspected; directory input width
was enlarged after inspection. All 121 desktop messages have complete de/ru/pl
PO/MO translations and no catalog errors. Python syntax and whitespace checks pass.
No new dependency installation or Android build was needed. Existing owner sample
edit and recovery copies are preserved. Native Windows/Tk display limits remain.

## 2026-10-17 — Shared attribution and translated diagnostics

User requested contributor, license and sources in New project so these need only
be entered once, plus translation of missing-contributor and other diagnostics.
Both creation dialogs require those common values, persist optional lesson_defaults
in language.yaml and prefill every new lesson, including after reopening. Existing
sample attribution is untouched and per-lesson overrides remain. Old manifests
without the optional block stay supported. Neither author identity nor license is
assumed. New default values are structurally checked as text.

Refactored validator errors to store stable English templates/named parameters,
retaining original CLI text and checks. Desktop localizes these and editor errors
through PO/MO, preserving paths/IDs and translating field labels. No regex guessing
of English failure text; native OS/parser details pass through. Extractor now
includes validator diagnostics using AST argument positions, avoiding miscounting
strings inside boolean conditions. Syntax checks caught and corrected a UTF-8
source-offset issue during template conversion before validation ran. All 192
interface/diagnostic messages have complete German/Russian/Polish translations.

Focused model/default/localized-error checks passed (5 tests), as did Qt/form/PO
checks (7 tests). Qt tests fill the actual New-dialog fields, save/reopen, and
verify new lessons in the other track retain common attribution. Localized missing
contributor/license/sources and answer errors preserve original English exceptions,
real project paths (including braces/Unicode) and question IDs. German New-dialog
screenshot rendered and visually inspected. Full regression results follow below.
No new dependencies, downloads, Android build, original sample edits, commit or
publication were needed. Existing owner sample edit/recovery files preserved.

Final shared-attribution/localization validation: full 38-test suite passed in
102.673 seconds. The five focused setup/default/error checks also passed after
hardening malformed-case diagnostic rendering. PO completeness/placeholder/runtime
checks cover all 192 entries and AST checks ensure editor/validator diagnostics
are included in the template. Original validation failures still have their English
exception text; GUI formatting is localized without altering data. Compilation
and whitespace checks pass. Native Windows/Tk display verification and translation
native-speaker review remain pending as before; the Qt dialog was inspected offscreen.
