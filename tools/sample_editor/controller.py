"""Backend-independent navigation and persistence. Views contain widgets only."""
from copy import deepcopy
import uuid

from fields import apply_fields, lesson_fields, question_fields
from i18n import _, language
from model import Document, EditorError, Project
from vocabulary import label
from diagnostics import localize_error


class Editor:
    def __init__(self, view, folder=None):
        self.view, self.project, self.doc = view, None, None
        self.index = None
        self.dirty = False
        self.loading = False
        self.paths = []
        view.controller = self
        view.set_state(False, False)
        if folder:
            self.open_project(folder)

    def changed(self, *_):
        if self.doc and not self.loading:
            self.dirty = True
            self.view.title(self.doc.path.name + ' *')

    def guarded(self, action):
        try:
            return action()
        except Exception as exc:
            self.view.message('error', _('Sample editor'), localize_error(exc))
            return False

    def leave(self):
        if not self.dirty:
            return True
        answer = self.view.ask_save()
        return self.save() if answer == 'save' else answer == 'discard'

    def open_project(self, folder=None):
        if not self.leave():
            return
        folder = folder or self.view.choose_project()
        if not folder:
            return
        self.guarded(lambda: self.activate_project(Project(folder)))

    def activate_project(self, project):
        issues = project.naming_issues()
        self.project = project
        self.clear_document()
        name = project.manifest.get('names', {}).get(language(), project.manifest['name'])
        self.view.project_label(f'{project.folder.name} — {name}')
        self.view.set_cases(project.cases)
        self.view.track.set('nouns')
        self.view.case.set(project.cases[0])
        self.refresh_lessons()
        if issues:
            self.view.message('warning', _('Project naming issues'), '\n'.join(localize_error(issue) for issue in issues))

    def new_project(self):
        if not self.leave():
            return
        setup = self.view.ask_new_project()
        if setup is None:
            return
        def action():
            from project_setup import PRESETS
            preset = PRESETS.get(setup['code'], {})
            project = Project.create(**setup, case_names=preset.get('cases'), name=preset.get('name'))
            self.activate_project(project)
            document = Document.new(project, 'nouns', project.cases[0], 'practice-1')
            self.load_document(document.path, document)
            self.changed()
            self.refresh_lessons(document.path)
            self.view.status(_('Project created. Complete the first lesson, then Save.'))
        self.guarded(action)

    def filter_changed(self):
        if not self.project:
            return
        track, case = self.view.track.get(), self.view.case.get()
        if not self.leave():
            self.view.track.set(self.doc.track)
            self.view.case.set(self.doc.case)
            return
        self.clear_document()
        self.view.track.set(track)
        self.view.case.set(case)
        self.refresh_lessons()

    def refresh_lessons(self, selected=None):
        self.paths = self.project.files(self.view.track.get(), self.view.case.get())
        if (self.doc and self.doc.is_new and self.doc.path not in self.paths
                and self.doc.track == self.view.track.get() and self.doc.case == self.view.case.get()):
            self.paths.append(self.doc.path)
        names = [(self.project.identity(p)[1] or _('Base lesson')) +
                 (' *' if self.doc and self.doc.is_new and p == self.doc.path else '') for p in self.paths]
        self.view.lessons.set(names, self.paths.index(selected) if selected in self.paths else None)

    def select_lesson(self, n=None):
        n = self.view.lessons.selected() if n is None else n
        if n is None or n >= len(self.paths):
            return
        path = self.paths[n]
        if self.doc and path == self.doc.path:
            return
        if not self.leave():
            self.refresh_lessons(self.doc.path)
            return
        def action():
            self.load_document(path)
            self.refresh_lessons(path)
        self.guarded(action)

    def load_document(self, path, document=None):
        doc = document or Document(self.project, path)
        self.loading = True
        try:
            self.doc, self.data, self.index = doc, deepcopy(doc.data), None
            self.destination_track, self.destination_case = doc.track, doc.case
            self.show_location()
            self.view.suffix.set(doc.extension)
            self.view.lesson_form.set_fields(lesson_fields(self.data))
            self.refresh_questions(0)
            self.dirty = False
            self.view.title(doc.path.name)
            self.view.status(str(doc.path))
            self.view.set_state(True, True)
        finally:
            self.loading = False

    def clear_document(self):
        self.doc, self.index, self.dirty = None, None, False
        self.view.clear_forms()
        self.view.questions.set([])
        self.view.suffix.set('')
        self.view.location_label(_('Select a lesson'))
        self.view.title('')
        self.view.set_state(self.project is not None, False)

    def show_location(self):
        group = _('Nouns') if self.destination_track == 'nouns' else _('Adjectives and numerals')
        self.view.location_label(f'{group} / {label(self.destination_case)}')

    def move_lesson(self):
        if not self.doc:
            return
        destination = self.view.ask_move(self.project.cases, self.destination_track, self.destination_case)
        if destination and destination != (self.destination_track, self.destination_case):
            self.destination_track, self.destination_case = destination
            self.show_location()
            self.changed()
            self.view.status(_('The lesson will move when you press Save.'))

    def add_lesson(self):
        if not self.project:
            return
        track, case = self.view.track.get(), self.view.case.get()
        if not self.leave():
            return
        n = 1
        while self.project.destination(track, case, f'practice-{n}').exists():
            n += 1
        suffix = self.view.ask_suffix(f'practice-{n}')
        if suffix is None:
            return
        def action():
            document = Document.new(self.project, track, case, suffix)
            self.view.track.set(track)
            self.view.case.set(case)
            self.load_document(document.path, document)
            self.changed()
            self.refresh_lessons(document.path)
            self.view.status(_('New lesson: fill the questions and lesson details, then Save.'))
        self.guarded(action)

    def delete_lesson(self):
        if not self.doc or not self.view.confirm_delete_lesson(self.doc.path.name):
            return
        def action():
            # Deletion deliberately discards unsaved edits; the dialog explains this.
            backup = self.doc.delete()
            self.clear_document()
            self.refresh_lessons()
            self.view.status(_('Lesson removed. The saved original is in recovery backups.') if backup else _('Unsaved lesson discarded.'))
        self.guarded(action)

    def store_question(self):
        if self.index is not None:
            self.data['sentences'][self.index] = self.view.question_form.apply(self.data['sentences'][self.index])

    def refresh_questions(self, selected):
        self.view.questions.set([f'{n}. {q.get("dictionary_form", "")}'
                                 for n, q in enumerate(self.data['sentences'], 1)],
                                selected if self.data['sentences'] else None)
        self.index = None
        if self.data['sentences']:
            self.load_question(selected)
        else:
            self.view.question_form.set_fields([])

    def load_question(self, n):
        self.index = n
        self.view.question_form.set_fields(question_fields(self.data['sentences'][n], self.data['native_languages']))

    def select_question(self, n=None):
        if not self.doc:
            return
        n = self.view.questions.selected() if n is None else n
        if n is None or n == self.index:
            return
        def action():
            self.store_question()
            self.load_question(n)
        if self.guarded(action) is False:
            self.view.questions.select(self.index)

    def add_question(self, duplicate=False):
        if not self.doc:
            return
        def action():
            self.store_question()
            q = deepcopy(self.data['sentences'][self.index]) if duplicate and self.index is not None else dict(
                word_type='noun' if self.destination_track == 'nouns' else 'adjective',
                dictionary_form='', neutral_prompt='___', features={'number': 'singular'},
                native_text={c: '' for c in self.data['native_languages']}, answer_scope='word',
                options={k: '' for k in 'abcd'}, correct='a')
            q['id'] = f'{self.data["id"]}-{uuid.uuid4().hex[:12]}'
            self.data['sentences'].append(q)
            self.refresh_questions(len(self.data['sentences']) - 1)
            self.changed()
        self.guarded(action)

    def delete_question(self):
        if self.index is None or not self.view.confirm_delete():
            return
        index = self.index
        del self.data['sentences'][index]
        self.refresh_questions(max(0, min(index, len(self.data['sentences']) - 1)))
        self.changed()

    def candidate(self):
        self.store_question()
        data = self.view.lesson_form.apply(self.data)
        data['case'], data['track'] = self.destination_case, self.destination_track
        return data

    def save(self, copy=False):
        if not self.doc:
            return False
        def action():
            suffix = self.view.suffix.get()
            if copy:
                suffix = self.view.ask_suffix(suffix + '-copy' if suffix else 'practice-1')
                if suffix is None:
                    return False
            path = self.doc.save(self.candidate(), self.destination_track, self.destination_case, suffix, copy=copy)
            self.dirty = False
            self.view.track.set(self.doc.track)
            self.view.case.set(self.doc.case)
            self.refresh_lessons(path)
            self.load_document(path)
            self.view.status(_('Saved {name}. Validation passed.').format(name=path.name))
            return True
        return self.guarded(action)

    def validate(self):
        if not self.project:
            return
        def action():
            if self.doc:
                target = self.project.destination(self.destination_track, self.destination_case, self.view.suffix.get())
                if (self.doc.is_new or target != self.doc.path) and target.exists():
                    raise EditorError(_('Destination exists. Choose another suffix.'))
                count = self.project.validate((None if self.doc.is_new else self.doc.path, target, self.candidate()))
            else:
                count = self.project.validate()
            self.view.message('info', _('Validation passed'),
                              _('{count} questions. Format checks passed. Grammar still needs human review.').format(count=count))
        self.guarded(action)

    def close(self):
        if self.leave():
            self.view.close()
