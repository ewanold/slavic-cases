# Implementation plan

1. Establish durable documentation and reusable setup scripts.
2. Agree initial learner level, explanation languages, and exercise types.
3. Select and pin a compatible Android Studio / AGP / Kotlin / Gradle / SDK set.
4. Create a minimal Android app and reproducible Gradle wrapper build.
5. Define a versioned content schema and reviewed Russian starter lessons.
6. Implement one complete lesson-to-exercise-to-feedback learning flow.
7. Add local progress and review scheduling, with persistence checks.
8. Validate accessibility, offline behavior, answer evaluation, and real-device UI.
9. Add contributor guidance, content review process, CI, and release instructions.
10. Expand language packs incrementally; track coverage and review status explicitly.

Validation: shell syntax for installers; clean build once app exists; focused tests
for answer evaluation, content validation and progress; emulator/device smoke tests.
An emulator is optional initially if a physical Android device is available.

## First playable flow

Implement the agreed startup case menu and mixed mode, independent language
settings, YAML sample loading and validation, native sentence plus neutral prompt,
four options, answer feedback, selected-item speech, Next, and results/Repeat/Back.
Finalize the open decisions in UI.md before implementing dependent behavior.
Use language-defined case menus and reviewed questions for mixed mode.

## Starter content implementation completed

Accepted YAML and separate noun/adjective tracks, with cardinal/ordinal numerals
in the adjective track. Created 180 Russian and 210 Polish draft questions,
covering every declared case with 15 questions per track. Structural validator,
regression checks, templates and contributor instructions are available.
Next content-dependent work is the Android importer and first playable screen;
linguistic review is required before learning material is released as reviewed.
