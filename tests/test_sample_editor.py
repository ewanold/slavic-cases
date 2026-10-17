"""Persistence safety and compatibility checks for the desktop editor."""
from copy import deepcopy
from pathlib import Path
import runpy
import shutil
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
API = runpy.run_path(str(ROOT / 'tools/sample_editor/model.py'))
Project, Document, EditorError = (API[k] for k in ('Project', 'Document', 'EditorError'))


class SampleEditorTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.folder = Path(self.temp.name) / 'ru-v2'
        shutil.copytree(ROOT / 'samples/ru-v2', self.folder, ignore=shutil.ignore_patterns('.sample-editor-backups'))
        self.project = Project(self.folder)
        self.path = self.folder / 'nouns/genitive-mnogo-malo.yaml'
        self.doc = Document(self.project, self.path)

    def test_all_five_projects_recognize_every_filename_and_validate(self):
        for name in ('ru', 'ru-v2', 'pl', 'pl-v2', 'de'):
            with self.subTest(name=name):
                project = Project(ROOT / 'samples' / name)
                self.assertEqual(project.naming_issues(), [])
                paths = [p for track in project.tracks for case in project.cases
                         for p in project.files(track, case)]
                self.assertEqual(len(paths), len(list(project.folder.glob('*/*.yaml'))))
                self.assertGreater(project.validate(), 0)

    def test_roundtrip_preserves_every_question_field_and_attribution(self):
        for name, relative in [('ru', 'adjectives/dative.yaml'), ('pl', 'nouns/vocative.yaml'),
                               ('de', 'adjectives/genitive.yaml'), ('pl-v2', 'nouns/genitive-many-few.yaml'),
                               ('ru-v2', 'nouns/genitive-mnogo-malo.yaml')]:
            with self.subTest(name=name):
                folder = Path(self.temp.name) / 'roundtrip' / name
                shutil.copytree(ROOT / 'samples' / name, folder, ignore=shutil.ignore_patterns('.sample-editor-backups'))
                project = Project(folder)
                doc = Document(project, folder / relative)
                before = deepcopy(doc.data)
                doc.save(before, doc.track, doc.case, doc.extension)
                self.assertEqual(API['read'](doc.path), before)
                backups = list((folder / '.sample-editor-backups').glob('*/*.bak'))
                self.assertEqual(len(backups), 1)
                self.assertEqual(API['read'](backups[0]), before)
                self.assertTrue(doc.path.read_text().startswith('#'))

    def test_rename_keeps_ids_and_free_suffix(self):
        data = deepcopy(self.doc.data)
        data['sentences'][0]['native_text']['en'] = 'Updated apples sentence.'
        saved = self.doc.save(data, 'nouns', 'genitive', 'practice-1')
        self.assertEqual(saved.name, 'genitive-practice-1.yaml')
        self.assertFalse(self.path.exists())
        self.assertEqual(API['read'](saved), data)
        self.assertEqual(self.project.identity(saved), ('genitive', 'practice-1'))

    def test_copy_has_unique_ids_and_preserves_source(self):
        before = deepcopy(self.doc.data)
        saved = self.doc.save(before, 'nouns', 'genitive', 'practice-2', copy=True)
        after = API['read'](saved)
        self.assertNotEqual(after['id'], before['id'])
        self.assertNotEqual(after['sentences'][0]['id'], before['sentences'][0]['id'])
        self.assertEqual(after['sentences'][0]['source'], before['sentences'][0]['source'])
        self.assertEqual(after['review_status'], 'draft')
        self.assertEqual(API['read'](self.path), before)
        self.assertGreater(self.project.validate(), 0)

    def test_invalid_edits_do_not_touch_original_or_make_backup(self):
        original = self.path.read_bytes()
        data = deepcopy(self.doc.data)
        data['sentences'][0]['correct'] = 'missing'
        with self.assertRaisesRegex(EditorError, 'correct must reference'):
            self.doc.save(data, 'nouns', 'genitive', 'mnogo-malo')
        self.assertEqual(self.path.read_bytes(), original)
        self.assertFalse((self.folder / '.sample-editor-backups').exists())

    def test_external_changes_and_destination_collisions_are_protected(self):
        other = self.folder / 'nouns/genitive-practice-1.yaml'
        other.write_text('existing data', encoding='utf-8')
        with self.assertRaisesRegex(EditorError, 'already exists'):
            self.doc.save(self.doc.data, 'nouns', 'genitive', 'practice-1')
        self.assertEqual(other.read_text(), 'existing data')
        self.path.write_bytes(self.doc.original + b'\n# external change\n')
        with self.assertRaisesRegex(EditorError, 'changed outside'):
            self.doc.save(self.doc.data, 'nouns', 'genitive', 'mnogo-malo')
        self.assertTrue(self.path.read_text().endswith('# external change\n'))

    def test_new_lessons_are_blank_unsaved_and_require_valid_content(self):
        for name, track, case in [('ru', 'adjectives', 'dative'), ('ru-v2', 'nouns', 'genitive')]:
            with self.subTest(name=name):
                folder = Path(self.temp.name) / 'new' / name
                shutil.copytree(ROOT / 'samples' / name, folder, ignore=shutil.ignore_patterns('.sample-editor-backups'))
                project = Project(folder)
                doc = Document.new(project, track, case, 'practice-added')
                self.assertTrue(doc.is_new)
                self.assertFalse(doc.path.exists())
                self.assertEqual(doc.data['contributor'], '')
                self.assertTrue(all('source' not in q for q in doc.data['sentences']))
                self.assertEqual(len(doc.data['sentences']), 15 if name == 'ru' else 1)
                if track == 'adjectives':
                    self.assertIn('cardinal_numeral', {q['word_type'] for q in doc.data['sentences']})
                with self.assertRaises(EditorError):
                    doc.save(doc.data, track, case, doc.extension)
                self.assertFalse(doc.path.exists())
                template = API['read'](project.files(track, case)[0])
                filled = deepcopy(doc.data)
                for key in ('instruction', 'contributor', 'sources', 'license'):
                    filled[key] = template.get(key) or 'Original test material'
                for n, q in enumerate(filled['sentences']):
                    identifier = q['id']
                    q.clear()
                    q.update(deepcopy(template['sentences'][n]))
                    q['id'] = identifier
                doc.save(filled, track, case, doc.extension)
                self.assertFalse(doc.is_new)
                self.assertEqual(API['read'](doc.path), filled)
                self.assertFalse((folder / '.sample-editor-backups').exists())
                with self.assertRaisesRegex(EditorError, 'already exists'):
                    Document.new(project, track, case, 'practice-added')

    def test_delete_moves_original_to_recovery_and_protects_external_edits(self):
        original = self.path.read_bytes()
        backup = self.doc.delete()
        self.assertFalse(self.path.exists())
        self.assertEqual(backup.read_bytes(), original)
        self.assertIn('.sample-editor-backups', backup.parts)
        self.path.write_bytes(original)
        doc = Document(self.project, self.path)
        self.path.write_bytes(original + b'\n# external change\n')
        with self.assertRaisesRegex(EditorError, 'changed outside'):
            doc.delete()
        self.assertTrue(self.path.exists())

    def test_deleting_an_unsaved_draft_never_touches_a_file_created_elsewhere(self):
        doc = Document.new(self.project, 'nouns', 'genitive', 'new-draft')
        doc.path.write_text('external new file', encoding='utf-8')
        with self.assertRaisesRegex(EditorError, 'already exists'):
            doc.save(doc.data, 'nouns', 'genitive', 'new-draft')
        self.assertIsNone(doc.delete())
        self.assertEqual(doc.path.read_text(), 'external new file')

    def test_filename_rules_and_duplicate_yaml_keys(self):
        for suffix in ('../escape', 'bad/name', 'with spaces', '-prefix'):
            with self.assertRaises(EditorError):
                self.project.destination('nouns', 'genitive', suffix)
        self.assertEqual(self.project.destination('nouns', 'genitive', '').name, 'genitive.yaml')
        self.assertEqual(self.project.destination('adjectives', 'dative', 'mnogo-malo').name,
                         'dative-mnogo-malo.yaml')
        with self.assertRaisesRegex(EditorError, 'filename must start'):
            self.project.identity(Path('gentive-practice.yaml'))
        with self.assertRaisesRegex(EditorError, 'duplicate YAML key'):
            API['parse_mapping']('id: first\nid: second\n')


if __name__ == '__main__':
    unittest.main()
