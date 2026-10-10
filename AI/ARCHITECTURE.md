# Proposed architecture

Native Android application using Kotlin and Jetpack Compose.
Separate UI, exercise evaluation, content loading, and progress persistence.
Bundle reviewed starter material for offline use. Keep content separate from UI
translations so a learner's explanation language can differ from the target language.
Use stable IDs and versioned content packs; progress references exercise IDs.
Choose database and review scheduling after defining the first exercises.
No backend, account, analytics, or external content service is currently required.
All stack choices remain proposals until the initial app design is agreed.
