"""Typed, restricted forms shared by Qt and Tk. YAML is never accepted as input."""
from copy import deepcopy
from dataclasses import dataclass
import json

from i18n import _
from model import EditorError
from vocabulary import label as vocabulary_label


@dataclass
class Field:
    path: tuple
    label: str
    value: object
    kind: str = 'text'
    choices: tuple = ()
    readonly: bool = False


def options(values, current):
    values = list(values)
    if current not in values:
        values.append(current)  # Preserve an authored value outside today's vocabulary.
    return tuple((v, _('Unknown / not specified') if v is None else vocabulary_label(str(v))) for v in values)


def question_fields(question, locales):
    fields = []
    def add(key, label, kind='text', values=()):
        value = question.get(key, '')
        fields.append(Field((key,), label, value, kind, options(values, value) if kind == 'choice' else (), key == 'id'))
    add('id', _('Question ID'))
    add('dictionary_form', _('Dictionary form'))
    add('neutral_prompt', _('Prompt (one ___ blank)'), 'multiline')
    add('word_type', _('Word type'), 'choice', ('noun', 'adjective', 'cardinal_numeral', 'ordinal_numeral'))
    add('answer_scope', _('Answer scope'), 'choice', ('word', 'phrase'))
    if 'exercise_type' in question:
        add('exercise_type', _('Exercise type'), 'choice', ('inflection', 'gender'))
    for code in dict.fromkeys([*locales, *question.get('native_text', {})]):
        fields.append(Field(('native_text', code), _('Native sentence — {language}').format(language=code),
                            question.get('native_text', {}).get(code, ''), 'multiline'))
    for key in 'abcd':
        fields.append(Field(('options', key), _('Answer {key}').format(key=key), question.get('options', {}).get(key, '')))
    add('correct', _('Correct option'), 'choice', tuple('abcd'))
    feature_choices = {
        'number': (None, 'singular', 'plural'),
        'gender': (None, 'masculine', 'feminine', 'neuter'),
        'animacy': (None, 'animate', 'inanimate'),
        'noun_gender': (None, 'masculine', 'feminine', 'neuter'),
        'declension': (None, 'noun', 'weak', 'mixed', 'strong', 'numeral'),
        'plural_gender': (None, 'masculine-personal', 'non-masculine-personal'),
    }
    for key, value in question.get('features', {}).items():
        label = _('Feature — {name}').format(name=vocabulary_label(key))
        if key in feature_choices:
            fields.append(Field(('features', key), label, value, 'choice', options(feature_choices[key], value)))
        elif isinstance(value, int) and not isinstance(value, bool):
            fields.append(Field(('features', key), label, value, 'integer'))
        elif isinstance(value, str):
            fields.append(Field(('features', key), label, value))
        else:
            fields.append(Field(('features', key), label, value, 'details', readonly=True))
    if isinstance(question.get('review_notes'), list) and all(isinstance(v, str) for v in question['review_notes']):
        fields.append(Field(('review_notes',), _('Review notes (one per line)'), question['review_notes'], 'lines'))
    known = {f.path[0] for f in fields}
    remaining = {k: v for k, v in question.items() if k not in known}
    if remaining:
        fields.append(Field((), _('Imported source and other preserved data'), remaining, 'details', readonly=True))
    return fields


def lesson_fields(data):
    fields = [Field(('id',), _('Lesson ID'), data['id'], readonly=True)]
    for key, label in [('contributor', _('Contributor')), ('license', _('License')), ('sources', _('Sources'))]:
        fields.append(Field((key,), label, data.get(key, ''), 'multiline' if key == 'sources' else 'text'))
    fields.append(Field(('review_status',), _('Review status'), data['review_status'], 'choice',
                        options(('draft', 'reviewed'), data['review_status'])))
    for code, value in data.get('instruction', {}).items():
        fields.append(Field(('instruction', code), _('Instruction — {language}').format(language=code), value, 'multiline'))
    for key, label in [('id', _('Topic ID')), ('name', _('Topic name'))]:
        if 'topic' in data:
            fields.append(Field(('topic', key), label, data['topic'].get(key, '')))
    hidden = {k: v for k, v in data.items() if k not in {f.path[0] for f in fields} | {'sentences'}}
    fields.append(Field((), _('Project metadata (preserved)'), hidden, 'details', readonly=True))
    return fields


def display_value(field):
    if field.kind == 'details':
        return json.dumps(field.value, ensure_ascii=False, indent=2)
    if field.kind == 'lines':
        return '\n'.join(field.value)
    return '' if field.value is None else str(field.value)


def apply_fields(original, fields, values):
    result = deepcopy(original)
    for field in fields:
        if field.readonly:
            continue
        value = values[field.path]
        initial = field.value if field.kind == 'choice' else display_value(field)
        if value == initial:
            continue  # Preserve missing keys, null values and all original scalar types.
        if field.kind == 'choice':
            if value not in [v for v, _label in field.choices]:
                raise EditorError(_('Choose a value from the list.'))
        elif field.kind == 'integer':
            try:
                value = int(value)
            except ValueError as exc:
                raise EditorError(_('Enter a whole number.')) from exc
        elif field.kind == 'lines':
            value = value.splitlines()
        elif not isinstance(value, str):
            raise EditorError(_('Enter plain text.'))
        target = result
        for part in field.path[:-1]:
            target = target.setdefault(part, {})
        if field.path[:1] == ('options',) and field.path[-1] == 'd' and not value:
            target.pop('d', None)
        else:
            target[field.path[-1]] = value
    return result
