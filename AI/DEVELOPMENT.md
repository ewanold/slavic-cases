# Development setup

## Step-by-step setup

This guide is for Linux x86-64, with Ubuntu 24.04 as the observed development host.
Run commands in a terminal from the repository folder containing README.md.
The first prototype is now scaffolded. SDK installation prepares the tools;
step 6 builds the app. Commands below assume the installer's default directories.
If you override ANDROID_HOME, use your chosen SDK path instead.

### 1. Check prerequisites

```bash
uname -s
uname -m
command -v bash curl tar unzip sha256sum mktemp rg
```

Expect Linux, x86_64, and a path for every listed tool. Allow several gigabytes
of free space; an emulator needs additional space. Missing prerequisites must be
added to a reusable installer script before installation. The current script does
not support Windows, macOS, or Linux ARM.

Ripgrep supplies the `rg` command used for repository searches and emulator setup.
On Ubuntu/Debian, install it with the reusable system-tools installer:

```bash
bash scripts/install-system-tools.sh
```

The script runs `sudo apt install ripgrep`. APT uses your distribution's
authenticated repositories and available package version; this system package
is not pinned to a project-specific version.

### 2. Install the editor and SDK command-line tools

Android Studio is the editor/debugger. The Android SDK provides Android API files
and build/device tools. Studio includes a Java development kit (JDK).

```bash
bash scripts/install-android-tools.sh
```

This downloads pinned, checksum-verified archives into your home directory without
sudo and prints the installed paths. If you already ran it, continue to step 3.
Rerunning reuses existing installations.

### 3. Install the platform, build tools and phone tools

The recommended prototype baseline is Android 16 (API 36) and Build Tools 36.0.0.
Platform Tools includes adb, which communicates with a connected phone. Your phone
does not need Android 16 simply because we compile with this SDK. These choices
remain proposals until the first project build is verified.

```bash
bash scripts/install-android-tools.sh --sdk-packages \
  'platforms;android-36' \
  'build-tools;36.0.0' \
  'platform-tools'
```

Read and answer the license prompts if you accept the terms. Keep the quotes around
package IDs: semicolons otherwise have a special meaning in the shell. The script
reuses installed Studio and CLI tools. Google resolves SDK packages through its
repository; the bootstrap archive hashes do not cover these packages. Platform
Tools uses the repository's current revision; record it after installation.

### 4. Verify installation

```bash
"$HOME/.local/opt/slavic-cases/android-studio-rabbit1/jbr/bin/java" -version
"$HOME/Android/Sdk/platform-tools/adb" version
export JAVA_HOME="$HOME/.local/opt/slavic-cases/android-studio-rabbit1/jbr"
export ANDROID_HOME="$HOME/Android/Sdk"
"$ANDROID_HOME/cmdline-tools/15859902/bin/sdkmanager" --sdk_root="$ANDROID_HOME" --list_installed
```

Expect version output and installed entries for platforms;android-36,
build-tools;36.0.0, and platform-tools. The exports last only for this terminal.
The installer sets its own environment but cannot change the terminal that started
it. These checks do not request installation of additional packages.

### 5. Start Android Studio

```bash
"$HOME/.local/opt/slavic-cases/android-studio-rabbit1/bin/studio.sh"
```

Importing previous settings is optional. If the first-launch wizard offers SDK
downloads, skip them where possible and use the scripted installation above.
In Studio's SDK settings, select the directory printed by the installer, normally
Android/Sdk inside your home directory. Use Studio's bundled JDK for the proposed
Gradle setup.

Choose Open and select this repository's root folder. Do not create a separate
wizard project: the shared project is already here. Complete step 6's dependency
bootstrap before Gradle synchronization. Use Studio's offline Gradle mode for
later work; any missing dependency should be fetched through the reusable script.

### 6. Build and check the app

Gradle runs the build; the Android Gradle Plugin adds Android support. The prototype
uses Kotlin/Compose, AGP 9.1.1 and Gradle 9.3.1, with pinned dependencies. Python
and PyYAML are also required to validate and package the editable sample files.
If your Python 3.12 already has PyYAML, use it. Otherwise prepare the content tools:

```bash
bash scripts/install-content-tools.sh
export CONTENT_PYTHON="$HOME/.local/share/slavic-cases/content-venv/bin/python"
```

Keep that export in the terminal where you build; in Studio, the same environment
must be available to Gradle. If python3 already has PyYAML, no override is needed.
Prepare Gradle and download the project dependencies through the reusable script:

```bash
bash scripts/install-build-tools.sh
```

This verifies the Gradle archive checksum, prepares the wrapper cache, builds the
debug APK, runs JVM tests and Android lint. Dependencies are verified against the
recorded hashes in gradle/verification-metadata.xml. First-time hashes are a
repository bootstrap baseline; they do not independently authenticate publishers.
The SDK platform/build-tools must already be installed; automatic SDK download
during Gradle builds is disabled.

For subsequent builds using cached dependencies:

```bash
bash scripts/build.sh
```

The APK is app/build/distributions/learn-grammatical-cases-debug.apk. Test and lint reports are in
app/build/reports/. If offline mode reports a missing dependency, run the installer
again. Release builds intentionally fail until all samples have linguistic review.

### 7. Install on a phone or test with an emulator

A physical phone needs Android 10 or later for this prototype. Enable Developer
options and USB debugging in the phone's settings, connect by USB, and accept the
phone's debugging authorization prompt for your computer. Run:

```bash
"$HOME/Android/Sdk/platform-tools/adb" devices -l
"$HOME/Android/Sdk/platform-tools/adb" install -r app/build/distributions/learn-grammatical-cases-debug.apk
"$HOME/Android/Sdk/platform-tools/adb" shell am start -n org.slaviccases.app/.MainActivity
```

The device list should show one device with status device. If unauthorized, check
the phone's screen; if no device appears, check USB mode/cable and Linux device
permissions. With multiple devices, specify adb -s SERIAL. Open the app from its
launcher icon after installation if preferred. Use an installed offline Russian
or Polish text-to-speech voice for the Speak button; unavailable speech does not
prevent practice.

For an optional API 36 emulator on Linux x86-64:

```bash
bash scripts/install-test-emulator.sh
bash scripts/run-emulator.sh
```

The launcher now uses automatic graphics selection and enables Quick Boot
snapshots; close the emulator normally to save a snapshot for the next start.
Avoid `-gpu swiftshader` for everyday use: it renders graphics on the CPU.
If automatic graphics works poorly, try `bash scripts/run-emulator.sh -gpu host`;
if hardware rendering fails, use `-gpu software` as a slower fallback.
Reference: https://developer.android.com/studio/run/emulator-acceleration

No Google account is required to install or use this app. Skip Google sign-in;
after Android finishes booting, install and open our existing debug build directly:

```bash
bash scripts/run-app.sh
```

With multiple devices, pass the emulator serial, for example
`bash scripts/run-app.sh emulator-5580`. This does not use the Play Store.
The Google APIs image was chosen for testing, not because the app requires Google
services. Speech still requires an installed suitable voice.

The installer reuses accepted SDK licenses, prompts for any missing ones, and
creates a Pixel 6 virtual device. KVM access is recommended. Once it finishes
booting, use the same adb install/start commands above. SDK repository revisions
for the emulator/image are recorded after installation; package IDs alone do not
pin their revisions. Screen-level tests require a connected phone or emulator:

```bash
bash scripts/install-build-tools.sh connectedDebugAndroidTest
```

Once test dependencies are cached, use scripts/build.sh instead for an offline
run. Instrumented tests exercise a complete session, rotation/recreation, repeat,
incorrect-answer locking and mixed mode. Do not use personal learning data during
these development tests.

### Common problems

- Missing adb: complete step 3; the basic installer only installs Studio and CLI.
- Java not on PATH: use the full bundled Java path or the exports in step 4.
- SDK Manager deprecation warning: installed SDK components still work. Migration
  to Android CLI is tracked in TODOS.md; its launcher bootstraps a separate runtime
  which needs version/checksum handling before replacing the scripted setup.
- Studio uses another SDK: select the SDK directory printed by the installer.
- No Android Run configuration: open the repository root and complete Gradle sync.
- Download/checksum error: read the error and retry the script. If it reports an
  incomplete installation directory, inspect that directory before changing it.
- SMB/CIFS checkout: the first build must verify locking and permissions; a
  local-disk checkout may be necessary if Gradle cannot work on the share.

Sample-only contributors can use the content authoring instructions below without
installing Android tools.

Initial observation before installation: Ubuntu 24.04, x86-64 Java runtime 21;
Android tools absent from PATH. Studio and SDK CLI are now installed; see the
verified installation record below.

## Reusable installation

Run `bash scripts/install-android-tools.sh --help` to see usage.
The script installs pinned Linux x86-64 Android Studio and command-line tools
under user-owned directories, verifying SHA-256. It uses Studio's bundled JDK.
Requirements: bash, curl, tar, unzip, sha256sum. Missing OS packages must be
handled by a reusable script before installation; no packages were installed yet.

Run `bash scripts/install-android-tools.sh` to install tools. Review Google's
terms at https://developer.android.com/studio before downloading/using them.
Run `bash scripts/install-android-tools.sh --sdk-packages 'platforms;android-N' 'build-tools;VERSION'`
with actual versions once the app build set is selected. SDK license acceptance
is interactive. Package IDs are explicit; the script does not guess app targets.
SDK manager resolves packages through Google's repository; these packages are not
covered by the bootstrap archive hashes. Record chosen package versions here.

Default Studio location: ~/.local/opt/slavic-cases/android-studio-rabbit1.
Default SDK: ~/Android/Sdk (ANDROID_HOME can override it).
Start Studio using its bin/studio.sh. Set its SDK path to the same SDK directory.
Do not use the IDE wizard for undocumented downloads; add required package IDs
to the reusable command above. Emulator images and AVD setup remain future work.
Gradle wrapper/dependency downloads must also have a documented reusable setup
command when the Android project is created.

## Resume the current chat

From the repository run `bash run-codex.sh` (or `./run-codex.sh`).
It changes to the repository directory and runs:
`codex resume 01a125a2-e082-7913-92e6-699493f09cca`.
Extra arguments are passed through. The Codex CLI and locally stored original
chat must be available; forks should start their own session using AI/ notes.

For current prototype behavior and validation limits, see PROTOTYPE.md and LOG.md.

## Content authoring and checks

The existing host provides Python 3.12 and PyYAML 6.0.1. No installation was
needed to export or validate the sets. Run:

```bash
python3 scripts/validate-samples.py
python3 tests/test_sample_validation.py
```

For a fresh Linux Python 3.12 host with venv support, use the reusable installer
scripts/install-content-tools.sh. It installs only hash-verified PyYAML 6.0.1
wheels for x86-64/aarch64 into ~/.local/share/slavic-cases/content-venv (override
with CONTENT_VENV_DIR). The installer has not been executed. Additional Python/OS
prerequisites must be added to reusable installation scripts before installation.
The original archive hashes came from official PyPI metadata; no archives were
downloaded during creation of this setup script.

The original content exporter can write to a new directory using --output. It
refuses overwrites. Editable samples/ YAML is authoritative after export.
--release validation intentionally fails while samples remain draft.

During setup, updating the existing .gitignore was denied despite escalation;
its content was preserved. The content environment was placed outside the checkout
instead, which also avoids committing local dependencies. At that initial stage,
app source/build validation did not yet exist; current results are in LOG.md.

## Device theme and APK transfer

The app follows the device's light/dark setting, using wallpaper-derived Material
colors on Android 12+ and a built-in palette on Android 10/11. Correct/incorrect
answers retain green/red colors in both themes. Android 10 (API 29) is the current
minimum; the earlier Android 8 baseline below is historical.

You can also transfer app/build/distributions/learn-grammatical-cases-debug.apk to your phone and
open it from a file manager. Permit installation from that source when Android
asks. No Google account is required. This is the development/debug build; lesson
content still awaits linguistic review.

## User installation verified — 2026-10-10

User reports running the Android tools installer. Verified Studio build
AI-262.9437.185.2621.16467767 at the documented default location, SDK command-line
tools revision 22.0 in cmdline-tools/15859902, and bundled OpenJDK 25.0.3
(build 25.0.3+-15898627-b508.16). The Java executable runs successfully.
At this initial verification, the SDK contained only cmdline-tools; platform,
build-tools, platform-tools and emulator installation followed later. Studio GUI launch was not tested.
Choose build dependencies compatible with this JDK, or script a separate supported
build JDK before building; do not assume the bundled Java version is 21.

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

### Version 0.2 local release build

Run `bash scripts/build-local-release.sh` for a non-debuggable APK at
`app/build/distributions/learn-grammatical-cases.apk`. This private-testing mode uses
`-PlocalReleasePreview=true`, includes drafts and signs with the existing Android
development key. It can update a debug installation built with the same key.
Never commit the key; a fork uses its own development key.
Normal `bash scripts/build.sh assembleRelease` still enforces review and licensing.
Publication needs cleared content and a dedicated protected signing key.
Neither helper uploads to a store or creates a public GitHub release.

### Editing and debugging

Android Studio is the standard IDE for this Kotlin/Compose app. Open the project
root, edit Kotlin in app/src/main/java, and use Run/Debug with an emulator or phone.
Logcat shows device messages; Layout Inspector helps investigate Compose layouts.
Terminal scripts remain the repeatable build route. Other text editors can edit
sources but do not supply the same integrated Android tooling.
Official introduction: https://developer.android.com/studio/intro

Installed Linux Studio launcher (default installer layout):
`~/.local/opt/slavic-cases/android-studio-rabbit1/bin/studio`.
Run it from a terminal, then Open the repository root.

### APK filenames

Every assembleDebug/assembleRelease build exports the corresponding APK to
`app/build/distributions/learn-grammatical-cases-debug.apk` or
`app/build/distributions/learn-grammatical-cases.apk`. These are byte-for-byte copies of
AGP's generated APKs, preserving signatures. Gradle's internal output files and
installation metadata stay together in outputs/apk/ for Android Studio.
The filenames do not affect the installed app name, package ID or update identity.

For a Linux application-menu launcher, open Android Studio and choose
**Tools → Create Desktop Entry**. The owner confirmed finding the executable and
creating the desktop launcher on 2026-10-11. The launcher is local desktop setup,
not a repository file; fork contributors create their own entry after installation.

## Translating the interface

Edit `app/src/main/res/values/strings.xml` (English/default) and
`app/src/main/res/values-de/strings.xml` (German),
`app/src/main/res/values-ru/strings.xml` (Russian), and
`app/src/main/res/values-pl/strings.xml` (Polish). Match resource IDs; preserve
numbered, typed placeholders such as `%1$s` (text), `%2$d` (integer), and `%%`
(literal percent). Translate the whole message and reorder placeholders as needed.
Use valid UTF-8 XML; escape XML characters (`&amp;`, `&lt;`) and Android string
apostrophes when needed. GUI selection drives in-app resource resolution; launcher
label uses Android locale. No `.po` tooling or dependency is required.

Run `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_ui_strings.py`
for translation key/placeholder checks, then `bash scripts/build.sh` for Android
resource compilation, JVM tests and lint. Lessons, pack names and topic labels
are content translations in YAML; see CONTENT_FORMAT.md. To add another GUI
language, add its values-language resources and a selector entry, then extend the
resource parity check for that locale.
