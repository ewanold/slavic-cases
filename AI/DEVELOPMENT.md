# Development setup

Observed host: Ubuntu 24.04, x86-64 Java runtime 21. No javac, adb, sdkmanager,
or studio found on PATH. Tools elsewhere on disk have not been ruled out.

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

No app build or device validation is possible yet: app source has not been created.

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
instead, which also avoids committing local dependencies. No app source or build
validation exists yet.
