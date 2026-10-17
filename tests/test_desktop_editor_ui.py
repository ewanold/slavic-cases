"""Backend selection, typed form preservation, PO coverage and real Qt integration."""
from copy import deepcopy
import ast
import gettext
import importlib.util
import os
from pathlib import Path
import shutil
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools/sample_editor'))
from app import select_backend
from fields import apply_fields, display_value, lesson_fields, question_fields
from i18n import configure
from model import Document, EditorError, Project, read


def unchanged(fields):
    return {f.path: f.value if f.kind == 'choice' else display_value(f) for f in fields}


class BackendAndForms(unittest.TestCase):
    def tearDown(self):
        configure('en')

    def test_backend_preference_fallback_and_explicit_request(self):
        def probe(available, calls):
            def load(name):
                calls.append(name)
                if name not in available:
                    raise ImportError(name)
            return load
        for available, expected in [({'PySide6.QtWidgets', 'PyQt6.QtWidgets', 'tkinter'}, ('qt', 'PySide6')),
                                    ({'PyQt6.QtWidgets', 'tkinter'}, ('qt', 'PyQt6')),
                                    ({'tkinter'}, ('tk', None))]:
            self.assertEqual(select_backend(probe=probe(available, [])), expected)
        calls = []
        self.assertEqual(select_backend('tk', probe({'tkinter'}, calls)), ('tk', None))
        self.assertEqual(calls, ['tkinter'])
        with self.assertRaises(RuntimeError):
            select_backend('qt', probe({'tkinter'}, []))
        with self.assertRaises(RuntimeError):
            select_backend(probe=probe(set(), []))

    def test_all_authored_fields_roundtrip_without_yaml_input(self):
        count = 0
        for manifest in sorted((ROOT / 'samples').glob('*/language.yaml')):
            if manifest.parent.name == 'templates':
                continue
            for path in manifest.parent.glob('*/*.yaml'):
                data = read(path)
                fields = lesson_fields(data)
                self.assertEqual(apply_fields(data, fields, unchanged(fields)), data)
                for question in data['sentences']:
                    fields = question_fields(question, data['native_languages'])
                    self.assertEqual(apply_fields(question, fields, unchanged(fields)), question)
                    count += 1
        self.assertEqual(count, 1722)

    def test_restricted_values_nulls_numbers_readonly_and_source_preservation(self):
        q = read(ROOT / 'samples/ru-v2/nouns/genitive-mnogo-malo.yaml')['sentences'][0]
        q['future_metadata'] = {'retain': [None, 123, 'source']}
        fields = question_fields(q, ['en'])
        values = unchanged(fields)
        values[('features', 'gender')] = 'feminine'
        values[('native_text', 'en')] = 'Edited apples.'
        values[('id',)] = 'malicious-id-change'
        result = apply_fields(q, fields, values)
        self.assertEqual(result['features']['gender'], 'feminine')
        self.assertIsNone(result['features']['number'])
        self.assertEqual(result['id'], q['id'])
        self.assertEqual(result['source'], q['source'])
        self.assertEqual(result['future_metadata'], q['future_metadata'])
        values[('features', 'gender')] = 'not-a-gender'
        with self.assertRaises(EditorError):
            apply_fields(q, fields, values)
        q['features']['quantity'] = 2
        fields = question_fields(q, ['en'])
        values = unchanged(fields)
        values[('features', 'quantity')] = '5'
        self.assertEqual(apply_fields(q, fields, values)['features']['quantity'], 5)
        values[('features', 'quantity')] = 'not a number'
        with self.assertRaises(EditorError):
            apply_fields(q, fields, values)

    def test_localized_labels_keep_schema_values_and_placeholders(self):
        for language, save in [('de', 'Speichern'), ('ru', 'Сохранить'), ('pl', 'Zapisz')]:
            configure(language)
            from i18n import _
            self.assertEqual(_('Save'), save)
            self.assertIn('5', _('{count} questions. Format checks passed. Grammar still needs human review.').format(count=5))
            q = read(ROOT / 'samples/ru/nouns/dative.yaml')['sentences'][0]
            fields = question_fields(q, ['en', 'de'])
            self.assertEqual(apply_fields(q, fields, unchanged(fields)), q)

    def test_po_catalogs_cover_template_and_compiled_runtime(self):
        try:
            from babel.messages import pofile
        except ImportError:
            self.skipTest('Babel authoring dependency unavailable')
        locales = ROOT / 'tools/sample_editor/locales'
        with (locales / 'sample-editor.pot').open('rb') as source:
            template = pofile.read_po(source)
        ids = {m.id for m in template if m.id}
        for source_path in [ROOT / 'scripts/validate-samples.py', ROOT / 'tools/sample_editor/model.py']:
            for node in ast.walk(ast.parse(source_path.read_text(encoding='utf-8'))):
                if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
                    position = {'EditorError': 0, 'ValidationError': 0, 'require': 1}.get(node.func.id)
                    if position is not None and len(node.args) > position:
                        message = node.args[position]
                        if isinstance(message, ast.Constant) and isinstance(message.value, str):
                            self.assertIn(message.value, ids)
        for code in ('de', 'ru', 'pl'):
            path = locales / code / 'LC_MESSAGES/sample-editor.po'
            with path.open('rb') as source:
                catalog = pofile.read_po(source, locale=code, abort_invalid=True)
            self.assertEqual({m.id for m in catalog if m.id}, ids)
            self.assertFalse(list(catalog.check()))
            with path.with_suffix('.mo').open('rb') as source:
                runtime = gettext.GNUTranslations(source)
            for message in catalog:
                if message.id:
                    self.assertTrue(message.string)
                    self.assertNotIn('fuzzy', message.flags)
                    self.assertEqual(runtime.gettext(message.id), message.string)


@unittest.skipUnless(importlib.util.find_spec('PySide6'), 'Optional Qt dependency not installed')
class QtIntegration(unittest.TestCase):
    def test_new_project_dialog_defaults_creation_and_first_save(self):
        os.environ.setdefault('QT_QPA_PLATFORM', 'offscreen')
        from controller import Editor
        from qt_view import create_view
        from PySide6.QtCore import QTimer
        from PySide6.QtWidgets import QApplication, QCheckBox, QComboBox, QDialogButtonBox, QLineEdit, QPlainTextEdit, QPushButton
        configure('en')
        view = create_view('PySide6')
        editor = Editor(view)
        errors = []
        view.message = lambda *args: errors.append(args)
        self.assertFalse(view.track.widget.isEnabled())
        self.assertFalse(view.case.widget.isEnabled())
        self.assertTrue(all(not w.isEnabled() for w in view.lesson_actions))
        self.assertTrue(next(b for b in view.window.findChildren(QPushButton) if b.text() == 'New project…').isEnabled())
        with tempfile.TemporaryDirectory() as temporary:
            folder = Path(temporary) / 'My Polish course'
            observed = []
            def choose_setup():
                dialog = QApplication.activeModalWidget()
                language = dialog.findChild(QComboBox, 'project_language')
                for code, count in [('ru', 6), ('de', 4), ('pl', 7)]:
                    language.setCurrentIndex(language.findData(code))
                    observed.append(sum(b.isChecked() for b in dialog.findChildren(QCheckBox) if b.objectName().startswith('case_')))
                    self.assertEqual(observed[-1], count)
                dialog.findChild(QCheckBox, 'case_vocative').setChecked(False)
                dialog.findChild(QLineEdit, 'project_directory').setText(str(folder))
                dialog.findChild(QLineEdit, 'project_contributor').setText('Test author')
                dialog.findChild(QLineEdit, 'project_license').setText('MIT')
                dialog.findChild(QPlainTextEdit, 'project_sources').setPlainText('Original examples\nTest notes')
                button = next(b for b in dialog.findChild(QDialogButtonBox).buttons() if b.text() == 'Create project')
                button.click()
            QTimer.singleShot(0, choose_setup)
            setup = view.ask_new_project()
            self.assertEqual(setup['code'], 'pl')
            self.assertEqual(setup['contributor'], 'Test author')
            self.assertEqual(setup['sources'], 'Original examples\nTest notes')
            self.assertEqual(len(setup['cases']), 6)
            self.assertFalse(folder.exists())
            view.ask_new_project = lambda: setup
            editor.new_project()
            self.assertEqual(editor.project.folder, folder)
            self.assertTrue(editor.doc.is_new)
            self.assertEqual(editor.data['contributor'], 'Test author')
            self.assertEqual(editor.project.manifest['lesson_defaults']['license'], 'MIT')
            self.assertEqual(editor.data['sources'], 'Original examples\nTest notes')
            self.assertEqual(len(editor.data['sentences']), 15)
            self.assertTrue(view.case.widget.isEnabled())
            self.assertEqual(view.case.get(), 'nominative')
            self.assertNotIn('vocative', editor.project.cases)
            self.assertTrue((folder / 'language.yaml').exists())
            filled = deepcopy(read(ROOT / 'samples/pl/nouns/nominative.yaml'))
            filled['id'] = editor.data['id']
            filled.update({k: editor.data[k] for k in ('contributor', 'license', 'sources')})
            filled['native_languages'] = editor.data['native_languages']
            for n, question in enumerate(filled['sentences']):
                question['id'] = editor.data['sentences'][n]['id']
            editor.data = filled
            view.lesson_form.set_fields(lesson_fields(filled))
            editor.refresh_questions(0)
            self.assertTrue(editor.save())
            saved = editor.doc.path
            self.assertEqual(read(saved), filled)
            self.assertEqual(errors, [])
            editor.open_project(folder)
            editor.select_lesson(0)
            self.assertEqual(editor.doc.path, saved)
            self.assertEqual(editor.candidate(), filled)
            # New lessons reuse metadata after reopening, including the other track.
            view.track.set('adjectives')
            editor.filter_changed()
            view.ask_suffix = lambda initial: initial
            editor.add_lesson()
            self.assertEqual(editor.data['contributor'], 'Test author')
            self.assertEqual(editor.data['sources'], 'Original examples\nTest notes')
            self.assertEqual(editor.data['license'], 'MIT')
            editor.dirty = False
            # Cancelling the real setup dialog has no side effects.
            # Restore the original bound method after the setup stub.
            del view.ask_new_project
            QTimer.singleShot(0, lambda: QApplication.activeModalWidget().reject())
            self.assertIsNone(view.ask_new_project())
            self.assertEqual(editor.project.folder, folder)
            editor.dirty = False
            view.close()

    def test_real_qt_forms_edit_navigation_and_save(self):
        os.environ.setdefault('QT_QPA_PLATFORM', 'offscreen')
        from controller import Editor
        from qt_view import create_view
        configure('ru')
        view = create_view('PySide6')
        self.addCleanup(lambda: configure('en'))
        with tempfile.TemporaryDirectory() as temporary:
            folder = Path(temporary) / 'ru-v2'
            shutil.copytree(ROOT / 'samples/ru-v2', folder, ignore=shutil.ignore_patterns('.sample-editor-backups'))
            editor = Editor(view, folder)
            errors = []
            view.message = lambda *args: errors.append(args)
            view.case.set('genitive')
            editor.filter_changed()
            selected = next(i for i, p in enumerate(editor.paths) if p.stem == 'genitive-mnogo-malo')
            editor.select_lesson(selected)
            self.assertEqual(editor.candidate(), editor.data)
            self.assertTrue(view.question_form.widgets[('id',)].isReadOnly())
            self.assertTrue(view.question_form.widgets[()].isReadOnly())
            view.question_form.widgets[('native_text', 'en')].setPlainText('Changed in the Qt form.')
            editor.select_question(1)
            self.assertTrue(editor.dirty)
            self.assertEqual(editor.data['sentences'][0]['native_text']['en'], 'Changed in the Qt form.')
            self.assertTrue(editor.save())
            self.assertEqual(read(editor.doc.path)['sentences'][0]['native_text']['en'], 'Changed in the Qt form.')
            self.assertEqual(errors, [])
            self.assertIn('Родительный', [view.case.widget.itemText(i) for i in range(view.case.widget.count())])
            self.assertIn('Русский', view.project_text.text())
            # Cancel navigation must keep edits and restore filter selection.
            editor.changed()
            view.ask_save = lambda: 'cancel'
            view.case.set('dative')
            editor.filter_changed()
            self.assertEqual(view.case.get(), 'genitive')
            editor.dirty = False
            self.assertFalse(hasattr(view, 'save_case'))
            self.assertFalse(hasattr(view, 'save_track'))
            # An explicit move changes the pending destination without changing browsing.
            move_dialog = view.ask_move
            view.ask_move = lambda *args: ('nouns', 'dative')
            editor.move_lesson()
            self.assertEqual(editor.destination_case, 'dative')
            self.assertEqual(view.case.get(), 'genitive')
            self.assertIn('Дательный', view.location_text.text())
            editor.dirty = False
            view.ask_suffix = lambda initial: 'new-lesson'
            editor.add_lesson()
            self.assertTrue(editor.doc.is_new)
            self.assertEqual(editor.doc.case, 'genitive')
            self.assertEqual(len(editor.data['sentences']), 1)
            self.assertFalse(editor.doc.path.exists())
            view.confirm_delete_lesson = lambda name: False
            editor.delete_lesson()
            self.assertIsNotNone(editor.doc)
            view.confirm_delete_lesson = lambda name: True
            editor.delete_lesson()
            self.assertIsNone(editor.doc)
            # Saved lessons are deleted only after confirmation and stay recoverable.
            selected = next(i for i, p in enumerate(editor.paths) if p.stem == 'genitive-mnogo-malo')
            editor.select_lesson(selected)
            deleted = editor.doc.path
            original = deleted.read_bytes()
            editor.delete_lesson()
            self.assertFalse(deleted.exists())
            self.assertTrue(any(p.read_bytes() == original for p in (folder / '.sample-editor-backups/nouns').glob('*.bak')))
            self.assertIsNone(editor.doc)
            # Discarding on filter navigation clears the old details and keeps the requested filter.
            editor.select_lesson(0)
            editor.changed()
            view.ask_save = lambda: 'discard'
            view.case.set('dative')
            editor.filter_changed()
            self.assertIsNone(editor.doc)
            self.assertFalse(editor.dirty)
            self.assertEqual(view.case.get(), 'dative')
            self.assertEqual(errors, [])
            # Exercise the actual modal move dialog, including cancellation.
            from PySide6.QtCore import QTimer
            from PySide6.QtWidgets import QApplication
            QTimer.singleShot(0, lambda: QApplication.activeModalWidget().accept())
            self.assertEqual(move_dialog(editor.project.cases, 'nouns', 'dative'), ('nouns', 'dative'))
            QTimer.singleShot(0, lambda: QApplication.activeModalWidget().reject())
            self.assertIsNone(move_dialog(editor.project.cases, 'nouns', 'dative'))
            view.close()
