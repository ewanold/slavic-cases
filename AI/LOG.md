# Project log

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
