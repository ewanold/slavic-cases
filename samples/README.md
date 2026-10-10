# Sample sets

Each learning language has its own folder; templates/ contains copy-and-fill YAML.

```text
samples/
  templates/                   # Language, noun and adjective/numeral templates
  ru/
    language.yaml              # Six teaching cases
    nouns/<case>.yaml          # 15 questions per file
    adjectives/<case>.yaml     # 10 adjectives + 3 cardinals + 2 ordinals
  pl/
    language.yaml              # Seven cases including vocative
    nouns/<case>.yaml          # 15 questions per file
    adjectives/<case>.yaml     # Same split; vocative: 10 adjectives + 5 ordinals
```

Russian: 180 questions. Polish: 210 questions. English/German translations are
included. Every question contains native text and a neutral learning-language
prompt. Numerals have their own word_type and can use full-phrase answers.
The original starter files are draft material awaiting linguistic review.

See ../README.md for authoring, validation, forks, pull requests and feedback.
See ../AI/CONTENT_FORMAT.md for detailed schema and coverage decisions.
YAML is the editable source of truth; do not regenerate over contributed edits.
The exporter in ../scripts/create-starter-samples.py can recreate the original
starter material in a NEW directory; it refuses to overwrite existing files.
