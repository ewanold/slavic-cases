# Slavic Cases

## Confirmed requirements

- Build an Android app to learn Slavic grammatical cases in general.
- Prioritize Russian now; provide material for all Slavic languages over time.
- Release as open source; the repository already has an MIT license.
- Preserve discussion and build knowledge in AI/ for the owner and fork contributors.
- Follow the durable documentation approach of the sibling polar-web-app project.
- Record all downloading and installation in reusable installer scripts.
- Provide run-codex.sh to resume the current local chat.

## Confirmed learning flow

Startup case menu plus random mixed practice; noun/adjective sentence samples;
four answer options with green/red feedback; selected-option speech at bottom left;
Next at bottom right; end-of-session results with Repeat and Back.
GUI and learning language have independent settings. Russian uses six cases;
language packs may offer up to eight. Each language has its own sample folder,
with reusable templates in samples/templates/. Samples contain native-language
sentences and neutral prompts in the learning language. See UI.md and
CONTENT_FORMAT.md for the accepted format and initial grouping.
Noun and adjective sets are separate; adjective sets include labelled cardinal and
ordinal numerals. Starter Russian and Polish sets contain 15 questions per case
and track: 180 Russian + 210 Polish, all draft pending linguistic review.

## Proposed product and stack

Native Kotlin with Jetpack Compose; offline lessons and exercises; local progress.
Start with a small reviewed Russian learning path, then add language packs using
shared exercise infrastructure and language-specific grammar descriptions.
These are proposals, not yet user-approved product decisions.
Do not assume every Slavic language has Russian's case system or morphology.

## Documentation map

- HANDOVER.md: setup readiness and exact next steps after chat compaction.

- DOCUMENTATION.md: maintenance and handover rules.
- IMPLEMENTATION_PLAN.md: phased delivery and validation.
- ARCHITECTURE.md: proposed application structure.
- UI.md: confirmed learning flow and proposed interaction details.
- CONTENT_FORMAT.md: contributor-friendly sample proposal and reference template.
- DATA_MODEL.md: proposed learning-content model.
- DEVELOPMENT.md: setup, installer, local chat restart.
- LINKS.md: researched primary references.
- TODOS.md: next steps and unresolved questions.
- LOG.md: dated discussion outcomes, changes, and validation.

The committed knowledge base records relevant discussion outcomes and implementation
history; it is not an automatic verbatim export of the private conversation.
