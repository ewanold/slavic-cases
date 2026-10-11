# Proposed architecture

Native Android application using Kotlin and Jetpack Compose.
Separate UI, exercise evaluation, content loading, and progress persistence.
Bundle reviewed starter material for offline use. Keep content separate from UI
translations so a learner's explanation language can differ from the target language.
Use stable IDs and versioned content packs; progress references exercise IDs.
Choose database and review scheduling after defining the first exercises.
No backend, account, analytics, or external content service is currently required.
All stack choices remain proposals until the initial app design is agreed.

## Implemented prototype and broader language scope (2026-10-11)

The app is now Learn Grammatical Cases and includes German alongside Russian and
Polish. Three production Kotlin files implement Compose UI/session state/preferences/
speech (MainActivity), content models/JSON loading (Lessons), and pure practice rules
(Practice). YAML is validated and converted by Python during the Gradle build;
JSON is bundled offline. Case inventory and phrase answers come from each pack.
The proposed database/review scheduling above remains future work.
