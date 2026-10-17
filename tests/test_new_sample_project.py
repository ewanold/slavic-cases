"""Project setup safety and incremental authoring without weakening build checks."""
from copy import deepcopy
from pathlib import Path
import shutil
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools/sample_editor'))
from i18n import configure
from model import Document, EditorError, Project, VALIDATOR, dump, read
from project_setup import PRESETS, defaults


class NewProjectTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        configure('en')

    def test_language_defaults_and_selected_cases_are_written(self):
        for code, count in [('ru', 6), ('pl', 7), ('de', 4)]:
            with self.subTest(code=code):
                values = defaults(code)
                self.assertEqual(len(values['cases']), count)
                project = Project.create(self.root / f'My {code} lessons', code, **values,
                                         case_names=PRESETS[code]['cases'], name=PRESETS[code]['name'])
                self.assertEqual(project.cases, values['cases'])
                self.assertEqual(project.manifest['cases'][0]['name'], PRESETS[code]['cases']['nominative'])
                self.assertEqual(project.manifest['learning_language'], code)
                self.assertTrue(all((project.folder / track).is_dir() for track in project.tracks))
                self.assertEqual(project.validate(allow_incomplete=True), 0)
                self.assertEqual(list(project.folder.glob('*/*.yaml')), [])

    def test_project_defaults_survive_reopen_and_seed_all_new_lessons(self):
        metadata = dict(contributor='Test author', license='MIT', sources='Original examples\nReference notes')
        folder = self.root / 'New project'
        Project.create(folder, 'ru', ['nominative', 'genitive'], ['en'], **metadata)
        project = Project(folder)
        self.assertEqual(project.manifest['lesson_defaults'], metadata)
        for track in project.tracks:
            for case in project.cases:
                doc = Document.new(project, track, case, 'practice-1')
                self.assertEqual({k: doc.data[k] for k in metadata}, metadata)
                doc.data['sources'] = 'Specific lesson source'
                other = Document.new(project, track, case, 'practice-2')
                self.assertEqual(other.data['sources'], metadata['sources'])
        malformed = deepcopy(project.manifest)
        malformed['lesson_defaults']['sources'] = ['not text']
        (folder / 'language.yaml').write_text(dump(malformed), encoding='utf-8')
        with self.assertRaisesRegex(EditorError, 'text values'):
            Project(folder)

    def test_validation_errors_translate_fields_and_keep_original_diagnostics(self):
        from diagnostics import localize_error
        from i18n import _
        project = Project.create(self.root / 'Übungen {draft}', 'de', ['nominative'], ['en', 'de'])
        doc = Document.new(project, 'nouns', 'nominative', 'practice-1')
        original = read(ROOT / 'samples/de/nouns/nominative.yaml')
        try:
            for code, expected in [('de', 'Angabe fehlt'), ('ru', 'отсутствует поле'), ('pl', 'brak pola')]:
                configure(code)
                for field in ('contributor', 'license', 'sources'):
                    data = deepcopy(original)
                    data[field] = ''
                    with self.assertRaises(EditorError) as raised:
                        doc.save(data, 'nouns', 'nominative', 'practice-1')
                    error = raised.exception
                    localized = localize_error(error)
                    self.assertIn(expected, localized)
                    self.assertIn(_({'contributor': 'Contributor', 'license': 'License', 'sources': 'Sources'}[field]), localized)
                    self.assertIn(str(project.folder), localized)
                    self.assertIn('missing ' + field, str(error))
                    self.assertNotIn('case-editor-', localized)
                data = deepcopy(original)
                data['sentences'][0]['correct'] = 'missing'
                with self.assertRaises(EditorError) as raised:
                    doc.save(data, 'nouns', 'nominative', 'practice-1')
                self.assertNotIn('correct must reference', localize_error(raised.exception))
                self.assertIn(data['sentences'][0]['id'], localize_error(raised.exception))
                # Literal braces in raw parser/system diagnostics must survive unchanged.
                self.assertEqual(localize_error(ValueError('raw {value}')), 'raw {value}')
                malformed = EditorError('{location}: undeclared case {case!r}', location='example.yaml', case={'bad': 'case'})
                self.assertIn("{'bad': 'case'}", localize_error(malformed))
        finally:
            configure('en')

    def test_invalid_setup_and_existing_files_are_not_changed(self):
        folder = self.root / 'target'
        for code, cases, natives in [('ru', [], ['en']), ('../bad', ['genitive'], ['en']),
                                      ('ru', ['genitive', 'genitive'], ['en']),
                                      ('ru', ['invalid'], ['en']), ('ru', ['dative'], [])]:
            with self.assertRaises(EditorError):
                Project.create(folder, code, cases, natives)
            self.assertFalse(folder.exists())
        folder.mkdir()
        marker = folder / 'keep.txt'
        marker.write_text('existing user data', encoding='utf-8')
        with self.assertRaisesRegex(EditorError, 'empty directory'):
            Project.create(folder, 'ru', ['dative'], ['en'])
        self.assertEqual(marker.read_text(), 'existing user data')
        self.assertEqual(list(folder.iterdir()), [marker])
        empty = self.root / 'empty'
        empty.mkdir()
        custom = Project.create(empty, 'cs', ['nominative', 'locative'], ['en'])
        self.assertEqual(custom.cases, ['nominative', 'locative'])
        malformed = deepcopy(custom.manifest)
        malformed['learning_language'] = '../../outside'
        (empty / 'language.yaml').write_text(dump(malformed), encoding='utf-8')
        with self.assertRaisesRegex(EditorError, 'Invalid learning-language tag'):
            Project(empty)

    def test_first_lesson_saves_in_arbitrary_folder_but_strict_build_requires_coverage(self):
        project = Project.create(self.root / 'My German course', 'de', ['nominative'], ['en', 'de'])
        doc = Document.new(project, 'nouns', 'nominative', 'practice-1')
        data = deepcopy(read(ROOT / 'samples/de/nouns/nominative.yaml'))
        data['id'] = doc.data['id']
        for n, question in enumerate(data['sentences']):
            question['id'] = doc.data['sentences'][n]['id']
        doc.save(data, 'nouns', 'nominative', 'practice-1')
        self.assertEqual(read(doc.path), data)
        self.assertEqual(project.validate(allow_incomplete=True), 15)
        with self.assertRaisesRegex(EditorError, 'no samples'):
            project.validate()
        # A bad answer still fails during incomplete-project authoring.
        invalid = deepcopy(data)
        invalid['sentences'][0]['correct'] = 'missing'
        with self.assertRaisesRegex(EditorError, 'correct must reference'):
            doc.save(invalid, 'nouns', 'nominative', 'practice-1')
        self.assertEqual(read(doc.path), data)
        canonical = self.root / 'build-input' / 'de'
        shutil.copytree(project.folder, canonical)
        manifest = canonical / doc.path.relative_to(project.folder)
        data['review_status'] = 'reviewed'
        manifest.write_text(dump(data), encoding='utf-8')
        for kwargs in ({}, {'release': True, 'allow_incomplete': True}):
            with self.assertRaisesRegex(VALIDATOR['ValidationError'], 'no samples'):
                VALIDATOR['validate'](canonical.parent, **kwargs)
