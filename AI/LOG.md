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
