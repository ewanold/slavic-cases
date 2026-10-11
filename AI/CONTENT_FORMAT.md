# Contributor-friendly sample files

## Accepted format and grouping

The user accepted the YAML examples and clarified separate noun and adjective
sets, with numbers included in the adjective sets. The initial implementation
uses 15 questions per language × case × track. Nouns and adjectives are never
required to form one shared vocabulary pair. Numerals retain their own subtype.

Use UTF-8 YAML and the copy-and-fill templates under samples/templates/.
Authors provide the sentences and four answer options directly; no programming
or algorithmic distractor generation is required. README.md explains submission
through a fork/pull request or plain-text feedback in a GitHub Issue.

## Layout

- samples/<learning-language>/language.yaml declares teaching cases (maximum eight),
  native translation languages, and the nouns/adjectives tracks.
- samples/<learning-language>/nouns/*.yaml contains noun sample sets.
- samples/<learning-language>/adjectives/*.yaml contains adjective/numeral sets.
- samples/templates/ contains language and 15-question track templates.
- AI/reference/sample-draft.yaml preserves the superseded one-question prototype.

Russian declares six cases. Polish declares seven including vocative. Other
language case lists must be reviewed before adding packs. Do not invent cases to
fill eight slots. More than eight categories requires a later design decision.

## Schema version 1

Language file: schema_version, learning_language, name, native_languages, tracks,
and cases (a list of stable id and learning-language name).

Sample: schema_version, unique id, learning_language, track, declared case,
native_languages, translated instruction, contributor, license, sources,
review_status (draft/reviewed), and exactly 15 sentences.

Adjective and ordinal prompts must put both dictionary forms in the hint:
`Я вижу ___. (добрый брат)`, rather than `Я вижу ___ брата. (добрый)`.
This avoids revealing the target case through an already-inflected noun. For
word-scope questions, choices still contain only the adjective/ordinal being
tested; the noun in brackets supplies context. Cardinal phrase questions retain
their existing dictionary-form hints and full-phrase answers.

Question: unique id, word_type (noun/adjective/cardinal_numeral/ordinal_numeral),
dictionary_form, features, native_text (language-to-text mapping), neutral_prompt
(one ___ blank plus dictionary-form hint), answer_scope (word/phrase), options
(a,b,c,d), and correct (one option key). IDs stay stable when text changes.
Features are language/subtype-specific. Typical word features are number, gender
and animacy; cardinal questions describe quantity and the noun dictionary form.
The prompt may contain already inflected context words; the target word/phrase is
shown in dictionary form in its hint. UI displays authored text, without inventing
translations or generating morphology at runtime. The precise presentation of the
neutral prompt remains a UI decision; this blank-and-hint representation is ready
for implementation.

Native text belongs to samples independently from GUI translations. A sample may
contain more than one native-language translation. English and German are provided
in the starter sets; the app's setting/fallback policy remains to be agreed.
Update native_languages in both language and sample definitions when changing the
required translation set. Every sample in a language must supply those translations.

## Starter coverage and grammar considerations

Russian: 6 × 2 × 15 = 180 questions. Polish: 7 × 2 × 15 = 210 questions.
Noun questions use 15 singular people/family nouns. Adjective questions use 10
singular masculine/feminine agreement examples plus five numeral questions per case.
Outside vocative, numerals include cardinal quantities 1, 2, 5 with books and two
ordinals. Polish vocative uses five ordinal examples addressing numbered competitors.
This covers all declared cases/tracks for development, not all declension classes,
genders, plurals, compound numbers or every use of each case.

Cardinal answer_scope is phrase: the numeral can govern a noun in a different
case/number from the selected case. For example, a nominative numeral phrase with
five contains a genitive-plural noun. Do not model every component as having the
selected case. Other questions answer with one word.
Case syncretism is expected: deduplicate identical option text instead of offering
several keys with the same answer. Feminine adjective questions may use a plural
form as a distractor when there are fewer than four distinct singular forms.
The fixed singular context excludes that distractor.
Polish vocative instructions explicitly require traditional vocative, since
nominative direct address can be acceptable colloquially. The selected case and
instruction are part of the exercise constraints, not a claim that all other
forms are impossible in everyday speech.

## Validation and review

Run python3 scripts/validate-samples.py to check language/case/track coverage,
15-question counts, unique IDs, YAML duplicate keys, native translations, one
prompt blank, four distinct options and a valid answer key. Templates and archives
are excluded. Default mode includes drafts so implementation can use the full set.
For publishing, --release requires all loaded samples to be marked reviewed.
The prototype validates and packages YAML into a deterministic JSON asset via
scripts/package-content.py, then loads it in Android. Its loader excludes drafts
outside debug, and release builds require reviewed YAML. Direct on-device YAML
import and a dedicated authoring preview remain unimplemented.

The validator does not prove linguistic correctness or unique grammatical validity.
Human review must check every correct answer, distractor, native translation and
context. Keep sources and redistribution permission explicit. Original AI-assisted
sentences use the repository MIT license and remain marked draft pending review.
Do not import textbook sentences without permission. Grammar reference links in
AI/LINKS.md informed review; the datasets were not copied from those publications.

Existing host PyYAML 6.0.1 was used without installing anything. Optional Linux
Python 3.12 setup is in scripts/install-content-tools.sh with hash-pinned wheels.
The exporter scripts/create-starter-samples.py documents the original authoring
paradigms and refuses overwrites; contributed YAML is authoritative after export.

### Topic-based content revisions

Folders ru-v2/pl-v2 are separate selectable packs, still using schema_version: 1.
Their manifests use content_profile apk-topic-import / polish-topic-adaptation;
each set declares topic: {id: stable-topic-id, name: readable-title}. These
profiles allow nonempty variable-sized lessons and three or four keyed choices.
IDs are unique within a pack (legacy Polish vocative IDs are reused between packs).
Additional native translations are accepted beyond the manifest's required locales.
Gender exercises use exercise_type: gender and features.gender for submenu grouping.
Other lessons use the authored topic without guessing preposition subgroups.
Legacy starter profiles retain the 15-question/four-distinct-choice requirements.
Imported duplicate answer text is preserved and reported by
scripts/audit-topic-samples.py, not approved for publication. Release validation
also rejects unspecified/unknown redistribution licenses.

German starter material is in samples/de (four cases, 15 items per track/case).
Use answer_scope: phrase for complete article/adjective/noun answers. Features
include noun gender/number and adjective declension pattern. Native translations
may match the learning language in YAML, but the UI hides that translation to
avoid answer disclosure. Grammar/source/review guidance: samples/de/README.md.

APK import attribution: content_profile apk-topic-import may omit contributor if
all questions retain nonempty source metadata and the sample declares sources and
license. Packaging records "Unknown original author; APK source metadata preserved"
explicitly. Original/simple and Polish adaptation sets still require a contributor.
This does not grant redistribution permission or bypass draft/release checks.

## Interface labels in language manifests

Keep stable pack IDs and original `name` fallback. Optional `names` supplies GUI
translations, separate from `native_languages` (sentence translations):

```yaml
names:
  en: Russian deep
  de: Russisch vertieft
topic_names:
  genders:
    en: Genders
    de: Geschlechter
```

`topic_names` maps the authored topic ID to GUI-language labels and belongs in
language.yaml, so questions/source metadata need not be rewritten for localization.
Current manifests provide English/German labels for every topic. The validator
checks nonempty English/German values when these optional mappings are present;
older packs fall back to their original names. Prepositions/examples in the target
language can remain untranslated within otherwise localized labels.
