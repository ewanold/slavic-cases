# Implementation handover — 2026-10-10

## Current status

First native Android prototype implemented and verified. User completed Studio and
SDK installation and authorized autonomous continuation while away. No immediate
user answer was needed. Provisional implementation choices remain reviewable;
confirmed requirements are separate in MAIN.md and UI.md.

End-of-day update: user confirmed it works on their phone. Current APK version is
0.1, minimum Android 10 (API 29), build date 2026-10-10 UTC. Settings displays
version/date. Device light/dark mode is followed, with dynamic colors on Android
12+ and built-in palettes on Android 10/11. Correct/wrong feedback retains green/red.
Question spacing was tightened after a clipped fourth answer report; verified all
four answers at 720x1280/density 280. Russian and Polish adjective/ordinal prompts
now hide inflected nouns: Я вижу ___. (добрый брат). Answers remain adjective-only;
cardinal questions retain phrase answers. Generator/templates match the new rule.

Read MAIN.md, PROTOTYPE.md, UI.md, CONTENT_FORMAT.md, DEVELOPMENT.md, TODOS.md and
recent LOG.md. Keep decisions/build history in AI/, source/scripts outside it,
and all dependency downloads in reusable installers.

## Run and review

Open the repository root in Android Studio with its bundled JDK. Dependency setup:
bash scripts/install-build-tools.sh. Offline build/tests/lint: bash scripts/build.sh.
Debug APK: app/build/outputs/apk/debug/app-debug.apk (generated and ignored by Git).
Phone installation steps are in DEVELOPMENT.md, prominently linked in README.
Optional emulator: bash scripts/run-emulator.sh, after install-test-emulator.sh.
The original host already has the API 36 Google APIs x86-64 AVD installed.
The original headless validation emulator was stopped. User's emulator-5554 is
currently running; left at Russian accusative adjective question 1, in light mode.
No build is running. Do not shut down the user's emulator without a request.
run-emulator.sh now allows Quick Boot snapshots, GPU auto and audio; close normally
to save a snapshot. KVM works. Earlier SwiftShader/no-snapshot test arguments made
interactive use slow. No Google sign-in is needed: bash scripts/run-app.sh SERIAL
installs the existing APK and opens it directly. Ripgrep prerequisite is documented
and installed, when needed, by scripts/install-system-tools.sh.
Screen tests: bash scripts/build.sh connectedDebugAndroidTest with a test device
connected. The installer prepares uncached test dependencies if necessary.
Visual references are AI/reference/prototype-{menu,question,feedback}.png.

## Prototype and validation

Russian/Polish cases, separate noun/adjective-numeral tracks, mixed practice,
English/German GUI independent of learning language, native sentences and neutral
prompts, shuffled four-choice answers, first-answer scoring, green/red plus text,
selected-answer offline speech, Next, results, Repeat and originating-menu Back.
Settings persist and session state survives activity recreation. Exact defaults,
source organization and pinned build versions are in PROTOTYPE.md.

390 draft questions pass structural validation. Initial full validation passed 18 tests: 11 existing
content regressions, one deterministic asset integration test, three JVM tests,
and three emulator UI tests. Latest complete offline debug build/lint/tests passed
following the speech-feedback adjustment. Subsequent theme/minimum-SDK changes
passed build/lint and visual dark menu/feedback checks. Latest version/prompt changes
passed assembleDebug, three JVM tests, all 12 Python regressions and visual Settings/
adjective checks. The three instrumented tests were not rerun after these UI/content
changes; do not describe the initial full run as validation of every latest change.
Lint has zero errors, with newer-version and optional KTX suggestions. Legacy
Compose test-rule and SDK XML-version warnings remain nonblocking.
Release-content guard was tested and correctly rejected unreviewed YAML.
No release signing/publication configured; all lessons need human linguistic review.

## Environment and follow-ups

SDK platform API 36 revision 2; Build Tools 36.0.0; Platform Tools 37.0.1; SDK CLI
22.0; bundled JDK 25.0.3. Emulator 37.2.12 build 16428233, Google APIs API 36
x86-64 image revision 7. SDK package IDs do not pin repository revisions. Gradle
archive and wrapper JAR have official SHA-256 pins; initial repository dependency
verification baseline records 854 artifacts, with strict subsequent verification.

Checkout is on SMB/CIFS; debug build and offline tests work there. Duplicate
incremental resource entries were cleared by a clean build. Avoid editing sources
while a build reads them. A build client disconnected and was retried. KVM works.
Initial emulator launcher/System UI ANRs during busy first boot cleared; app tests
passed at 720x1280/density 280 with an animation scale disabled. No app crash was
found in inspected emulator errors. Headless test emulator used port 5580.

Next: continue the owner's phone review, especially Russian/Polish offline voice quality,
accessibility and provisional practice defaults. Linguistic review, dedicated
sample authoring preview/on-device import, additional languages, progress history,
and final application ID/release setup remain future work.
Phone model/OS and voice quality have not been recorded; basic phone operation is
confirmed. Android 10/11 theme fallback remains untested on an actual device.
Latest screenshots include prototype-settings-version.png,
prototype-adjective-neutral.png and prototype-dark-{menu,feedback}.png in reference/.
Build date is captured at Gradle configuration/build time in UTC; versionCode is
still 1 and must advance when starting published upgrades. Latest APK is generated,
not committed. No remaining task requires an immediate user answer tonight.

SDK Manager is deprecated but functional. Android CLI migration is queued until
its separately bootstrapped runtime can be pinned and verified. Help unexpectedly
downloaded/unpacked it during inspection; the operation is now recorded in
scripts/inspect-android-cli.sh. No SDK license was accepted by the agent.

All changes are local; no assistant commit, push, publication, issue or PR. No
signing keys or personal learning data added. run-codex.sh resumes the original
chat; committed AI notes let fork contributors continue without that chat.
