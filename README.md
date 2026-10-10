# Slavic Cases

I want to learn Russian cases through practical examples, rather than only
memorising grammar tables. This project is my attempt to build an Android app
for that purpose, with help from AI.

Like my Polar project, this is an experiment in AI-driven development. I provide
the ideas, questions and direction; AI helps turn them into plans, learning
material and code. Russian is my personal starting point, but the long-term goal
is to support all Slavic languages. I am releasing the project as open source so
others can contribute examples, improve it, or continue it in a fork.

**Current status:** the first Android prototype builds and passes emulator tests. It
contains Russian/Polish practice, mixed sessions, English/German controls and
speech support. The 390 draft questions still need linguistic review.
The project uses the [MIT license](LICENSE).

## Set up for development

New to Android development? Follow the [step-by-step setup guide](AI/DEVELOPMENT.md#step-by-step-setup).
It explains installation, checking the tools, starting Android Studio, and the
remaining steps before we can build the app. The installer supports Linux x86-64.
You do not need Android tools to contribute sample sentences.

After installing the SDK and Python content tools, prepare dependencies and build:

```bash
bash scripts/install-build-tools.sh
```

For later builds with dependencies already cached:

```bash
bash scripts/build.sh
```

The debug APK is generated at `app/build/outputs/apk/debug/app-debug.apk`.
The setup guide explains how to install it on a phone or use the optional emulator.

## Planned learning experience

Choose a grammatical case, then practise nouns or adjectives and numerals using
four answer options. A mixed mode will combine questions across cases and tracks.
Correct selections turn green and incorrect selections red. A speech button reads
the selected answer, Next continues the session, and a results page offers Repeat
or Back. GUI language and learning language have independent settings.

## Starter sample sets

| Learning language | Cases | Noun questions | Adjective/numeral questions | Total |
| --- | --- | --- | --- | --- |
| Russian | 6 | 90 | 90 | 180 |
| Polish | 7, including vocative | 105 | 105 | 210 |

Each case/track file contains 15 questions. Samples include English and German
native-language text plus a neutral prompt in the learning language. The noun and
adjective tracks live in separate folders under [samples/](samples/README.md).
Numerals are in the adjective track but labelled as cardinal or ordinal numerals.
The initial sets focus on singular person nouns/adjectives, ordinal agreement,
and quantities one, two and five with books. Polish vocative numeral questions
use ordinals in direct address. These sets cover every declared case and track;
they are starter material rather than a complete grammar course.

## Creating a sample set

You can write samples in any plain-text editor; no Android programming is needed.
Use UTF-8 YAML and follow an existing example, such as
[Russian noun practice](samples/ru/nouns/dative.yaml) or
[Polish adjective practice](samples/pl/adjectives/accusative.yaml).

1. Choose the learning language folder, for example `samples/ru/` or `samples/pl/`.
   For a new language, copy [the language template](samples/templates/language.template.yaml)
   to `samples/<language-tag>/language.yaml` and declare its teaching cases, at most eight.
2. Copy [the noun template](samples/templates/nouns.template.yaml) into its `nouns/`
   folder, or [the adjective/numeral template](samples/templates/adjectives.template.yaml)
   into its `adjectives/` folder. Use a descriptive filename such as `dative-family.yaml`.
3. Replace the placeholders and give the sample and every question a unique ID.
   Set the language, case, contributor, source and license. Keep `review_status: draft`
   until linguistic review is complete. You must have permission to redistribute the material.
4. Fill all 15 questions with native-language sentence text, a neutral prompt in the
   learning language containing one `___` blank, and the target dictionary form.
   Keep the native text inside each sample. Change the native language tags/list
   together if you supply translations other than English and German.
5. Supply four different answers, labelled `a` to `d`, and set `correct` to the key
   of the correct answer. Use `answer_scope: word` for a single word or `phrase` when
   the complete numeral/noun phrase is being practised. Do not include a second valid
   answer as a distractor. Preserve accents and other meaningful letters.
6. Validate the files, or ask a maintainer to validate them when submitting.

With Python and PyYAML already installed, run from the project root:

```bash
python3 scripts/validate-samples.py
```

For Linux with Python 3.12 and virtual-environment support, a reusable installer
prepares an isolated validator environment outside the checkout:

```bash
bash scripts/install-content-tools.sh
"$HOME/.local/share/slavic-cases/content-venv/bin/python" scripts/validate-samples.py
```

The installer pins PyYAML and verifies wheel checksums. It has not been run in
this project session; validation used the machine's existing PyYAML installation.
If you use another platform or cannot run the validator, you can still submit
sample text for a maintainer to check. Structural validation checks the file format;
a person familiar with the language must check the grammar and answers.
See [the detailed content format](AI/CONTENT_FORMAT.md) for the schema and review rules.

## Contributing samples and providing feedback

To propose files, [fork this repository](https://github.com/ewanold/slavic-cases/fork),
copy/edit the templates in your fork, commit the changes, then open a pull request
against the original repository. You can edit text files through GitHub's website;
cloning and using the command line are optional. In the pull request, describe the
language, cases and track covered, translation languages, sources/license, and
whether you checked the answers or need help reviewing them.
[GitHub's contribution guide](https://docs.github.com/en/get-started/exploring-projects-on-github/contributing-to-a-project)
explains the fork and pull-request workflow.

For corrections, suggestions, or sample text you would rather not submit through
a fork, [open an issue](https://github.com/ewanold/slavic-cases/issues/new).
Use a title such as `Polish dative: correction to student question`, and include
the sample filename, question ID, current wording, proposed correction, and a short
explanation or reference. You can also paste a new sample into an issue inside a
YAML code block and ask for help turning it into a file. No programming knowledge
is required. Please check existing issues first and use an existing issue or
pull-request conversation when your feedback belongs there.
[GitHub's issue guide](https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/creating-an-issue)
shows how to post feedback. If Issues are not yet enabled, use a pull request.

## Development and AI handover

Start with [AI/MAIN.md](AI/MAIN.md), [the work queue](AI/TODOS.md), and
[development setup](AI/DEVELOPMENT.md). Contributors: read [AGENTS.md](AGENTS.md).
The `AI/` folder records discussion outcomes, decisions and build history so a
person or another AI session can continue the work.

Resume the original local development chat with `bash run-codex.sh`.
Fork contributors should start their own chat; cloning the repository does not
provide access to the original conversation. Use the committed AI notes instead.
