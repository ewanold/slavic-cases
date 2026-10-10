# Implementation handover — 2026-10-10

## Readiness

Ready to begin the first Android prototype. Product requirements and the accepted
YAML content model are sufficient. No Android app source, Gradle wrapper or SDK
platform has been created/installed yet. User plans to compact this conversation
and run the installer before the next implementation step. Do not install tools
on their behalf unless subsequently requested.

Read MAIN.md, UI.md, CONTENT_FORMAT.md, DEVELOPMENT.md, TODOS.md and recent LOG.md.
Preserve discussion/build history here in AI/ and keep all downloading/installing
in reusable scripts. README includes the owner's AI-development introduction and
instructions for sample creation, forks/PRs and feedback via GitHub Issues.

## First steps after compaction

1. User runs `bash scripts/install-android-tools.sh` from the project root.
   This installs pinned Android Studio and SDK CLI tools only. It does not install
   platform-tools, a platform SDK, build tools or an emulator without explicit
   --sdk-packages arguments. License acceptance happens interactively when SDK
   packages are requested. The script's exported environment ends with the script;
   it prints paths but does not alter the user's shell configuration.
2. Inspect actual installed Studio/JDK/SDK versions. Select and pin compatible
   Android Gradle Plugin, Kotlin, Compose and Gradle versions plus compile/target
   SDK and minimum supported Android version. Verify official compatibility docs.
3. Extend reusable setup/build scripts for the chosen SDK packages, Gradle wrapper
   and dependency bootstrap. Include platform-tools for device deployment; choose
   emulator/system image only if needed. Choose physical device versus emulator.
4. Scaffold the native Kotlin/Compose prototype (currently the proposed stack).
   Bundle YAML or a reproducibly generated content artifact; YAML remains the
   contributor-facing source of truth. Use drafts in development explicitly.
5. Implement one end-to-end session: menu -> case/track -> question -> feedback ->
   Next -> results -> Repeat/Back. Include independent GUI/learning language settings
   and selected-answer speech, then mixed mode. Verify build and device launch.

## Content already present

390 original, AI-assisted MIT questions in samples/:
- ru: 6 cases × nouns/adjectives × 15 = 180.
- pl: 7 cases (including vocative) × nouns/adjectives × 15 = 210.

Separate noun/adjective folders. Adjective tracks label ordinary adjectives,
cardinal numerals and ordinal numerals. Cardinal questions answer with a complete
phrase to represent noun government. Native English/German translations and neutral
learning-language prompts are inside samples. Language packs declare at most eight
teaching cases. Templates have 15 editable question slots. All starter content is
draft pending linguistic review; it is usable for implementation, not reviewed
release material. The exporter refuses overwrites; edited YAML is authoritative.

## Open choices and provisional defaults

These do not block initial scaffolding. They are proposals, not user-confirmed:
- Native sentence language: initially follow the GUI language where a supplied
  translation exists; explicitly handle missing translations. A separate native
  language setting remains an option. No silent language switch.
- Neutral display: one sentence blank with a dictionary-form hint, as in samples.
- Score the first selection, lock it, then enable Next; show text/icons plus colors.
- Case/track practice: use all questions in the selected sample (15 initially).
- Mixed mode: 15 reviewed/authored questions sampled without replacement across
  available cases/tracks; do not generate arbitrary vocabulary combinations.
- Repeat: same question set, shuffled answer positions; Back: originating menu.

Confirm/adjust choices when implementing their dependent screens. Initial learner
level, GUI language coverage, minimum supported device version and exact sampling
balance can be settled during the first prototype. Larger language coverage,
advanced declensions, review scheduling and release signing are later work.

## Verified setup and limitations

2026-10-10: bash/curl/tar/unzip/sha256sum/mktemp are available. Shell syntax checks
passed for Android installer, content installer and resume script. No downloads or
installs executed. Observed free space: home ~51 GB, root/tmp ~7.7 GB.

Working tree is on a CIFS/SMB share (/home/ewald/sonne). Test Gradle/build behavior;
if locking or executable/permission behavior fails, use a local-disk checkout or
worktree and document the workflow. Do not assume the first build is verified.
Updating the existing .gitignore was denied even with escalation; it was preserved.
Content-tool environments default outside the checkout to avoid local dependencies.

Existing Python 3.12 / PyYAML 6.0.1 validated all 390 questions, and 11 focused
regression checks passed. Optional scripts/install-content-tools.sh is prepared
with hash-pinned Linux CPython 3.12 wheels, but is unnecessary on the observed host.

Resume original local chat with run-codex.sh. The committed notes also support a
new chat or fork without access to the original conversation. Files are local
changes; no commit, push, issue or PR has been made by the assistant.
