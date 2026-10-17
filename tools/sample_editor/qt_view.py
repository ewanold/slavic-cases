"""Qt Widgets view; works with PySide6 or PyQt6, selected by the launcher."""
from fields import apply_fields, display_value
from i18n import _


def create_view(binding):
    import importlib
    W = importlib.import_module(binding + '.QtWidgets')
    C = importlib.import_module(binding + '.QtCore')

    class Value:
        def __init__(self, widget, choices=None):
            self.widget = widget
            if choices is not None:
                self.choices(choices)

        def choices(self, items):
            previous = self.widget.blockSignals(True)
            self.widget.clear()
            for value, label in items:
                self.widget.addItem(label, value)
            self.widget.blockSignals(previous)

        def get(self):
            return self.widget.currentData() if isinstance(self.widget, W.QComboBox) else self.widget.text()

        def set(self, value):
            previous = self.widget.blockSignals(True)
            if isinstance(self.widget, W.QComboBox):
                self.widget.setCurrentIndex(self.widget.findData(value))
            else:
                self.widget.setText(value)
            self.widget.blockSignals(previous)

    class List:
        def __init__(self, widget):
            self.widget = widget

        def set(self, items, selected=None):
            previous = self.widget.blockSignals(True)
            self.widget.clear()
            self.widget.addItems(items)
            self.select(selected)
            self.widget.blockSignals(previous)

        def select(self, n):
            previous = self.widget.blockSignals(True)
            self.widget.setCurrentRow(-1 if n is None else n)
            self.widget.blockSignals(previous)

        def selected(self):
            n = self.widget.currentRow()
            return n if n >= 0 else None

    class Form(W.QScrollArea):
        def __init__(self, changed):
            super().__init__()
            self.setWidgetResizable(True)
            self.changed = changed
            self.fields, self.inputs = [], {}

        def set_fields(self, fields):
            self.fields, self.inputs, self.widgets = fields, {}, {}
            old = self.takeWidget()
            if old:
                old.deleteLater()
            body = W.QWidget()
            layout = W.QFormLayout(body)
            layout.setFieldGrowthPolicy(W.QFormLayout.FieldGrowthPolicy.AllNonFixedFieldsGrow)
            layout.setRowWrapPolicy(W.QFormLayout.RowWrapPolicy.WrapLongRows)
            for field in fields:
                if field.kind == 'choice':
                    widget = W.QComboBox()
                    value = Value(widget, field.choices)
                    value.set(field.value)
                    getter = value.get
                    widget.currentIndexChanged.connect(self.changed)
                elif field.kind in ('multiline', 'lines', 'details'):
                    widget = W.QPlainTextEdit(display_value(field))
                    widget.setReadOnly(field.readonly)
                    widget.setMinimumHeight(75)
                    widget.setMaximumHeight(200 if field.kind == 'details' else 110)
                    getter = widget.toPlainText
                    widget.textChanged.connect(self.changed)
                else:
                    widget = W.QLineEdit(display_value(field))
                    widget.setReadOnly(field.readonly)
                    getter = widget.text
                    widget.textChanged.connect(self.changed)
                label = W.QLabel(field.label)
                label.setWordWrap(True)
                layout.addRow(label, widget)
                self.inputs[field.path] = getter
                self.widgets[field.path] = widget
            self.setWidget(body)
            self.verticalScrollBar().setValue(0)

        def apply(self, data):
            return apply_fields(data, self.fields, {p: get() for p, get in self.inputs.items()})

    class Window(W.QMainWindow):
        def closeEvent(self, event):
            if not getattr(self, 'close_approved', False) and self.view.controller and not self.view.controller.leave():
                event.ignore()
            else:
                event.accept()

    class View:
        def __init__(self):
            self.controller = None
            self.project_actions, self.lesson_actions = [], []
            self.app = W.QApplication.instance() or W.QApplication([])
            self.window = Window()
            self.window.view = self
            self.window.resize(1150, 820)
            self.window.setMinimumSize(800, 580)
            self.title('')
            body = W.QWidget()
            self.window.setCentralWidget(body)
            outer = W.QVBoxLayout(body)
            toolbar = W.QHBoxLayout()
            for label, method, args in [(_('New project…'), 'new_project', ()), (_('Open project…'), 'open_project', ()), (_('Save'), 'save', ()),
                                        (_('Save copy…'), 'save', (True,)), (_('Validate project'), 'validate', ())]:
                button = W.QPushButton(label)
                button.clicked.connect(lambda checked=False, m=method, a=args: self.call(m, *a))
                toolbar.addWidget(button)
                if method in ('save',):
                    self.lesson_actions.append(button)
                elif method == 'validate':
                    self.project_actions.append(button)
            self.project_text = W.QLabel(_('Create a project or open an existing one to begin.'))
            toolbar.addWidget(self.project_text, 1)
            outer.addLayout(toolbar)
            split = W.QSplitter(C.Qt.Orientation.Horizontal)
            outer.addWidget(split, 1)
            left, right = W.QWidget(), W.QWidget()
            split.addWidget(left)
            split.addWidget(right)
            split.setStretchFactor(1, 4)
            left_layout, right_layout = W.QVBoxLayout(left), W.QVBoxLayout(right)
            def combo(layout, label, choices, action):
                layout.addWidget(W.QLabel(label))
                widget = W.QComboBox()
                layout.addWidget(widget)
                value = Value(widget, choices)
                widget.currentIndexChanged.connect(lambda *_: self.call(action))
                return value
            tracks = [('nouns', _('Nouns')), ('adjectives', _('Adjectives and numerals'))]
            self.track = combo(left_layout, _('Group'), tracks, 'filter_changed')
            self.case = combo(left_layout, _('Case'), [], 'filter_changed')
            self.project_actions.extend([self.track.widget, self.case.widget])
            left_layout.addWidget(W.QLabel(_('Lessons (filename suffix)')))
            self.lessons = List(W.QListWidget())
            left_layout.addWidget(self.lessons.widget, 1)
            self.lessons.widget.currentRowChanged.connect(lambda *_: self.call('select_lesson'))
            lesson_buttons = W.QHBoxLayout()
            for text, method in [(_('Add lesson'), 'add_lesson'), (_('Delete lesson'), 'delete_lesson')]:
                button = W.QPushButton(text)
                button.clicked.connect(lambda checked=False, m=method: self.call(m))
                lesson_buttons.addWidget(button)
                (self.project_actions if method == 'add_lesson' else self.lesson_actions).append(button)
            left_layout.addLayout(lesson_buttons)
            left_layout.addWidget(W.QLabel(_('Questions')))
            self.questions = List(W.QListWidget())
            left_layout.addWidget(self.questions.widget, 1)
            self.questions.widget.currentRowChanged.connect(lambda *_: self.call('select_question'))
            buttons = W.QHBoxLayout()
            for label, method, args in [(_('Add'), 'add_question', ()), (_('Duplicate'), 'add_question', (True,)),
                                        (_('Delete'), 'delete_question', ())]:
                button = W.QPushButton(label)
                button.clicked.connect(lambda checked=False, m=method, a=args: self.call(m, *a))
                buttons.addWidget(button)
                self.lesson_actions.append(button)
            left_layout.addLayout(buttons)
            location = W.QGroupBox(_('Lesson file'))
            right_layout.addWidget(location)
            location_layout = W.QVBoxLayout(location)
            self.location_text = W.QLabel(_('Select a lesson'))
            location_layout.addWidget(self.location_text)
            move = W.QPushButton(_('Move lesson…'))
            move.clicked.connect(lambda *_: self.call('move_lesson'))
            location_layout.addWidget(move)
            self.lesson_actions.append(move)
            location_layout.addWidget(W.QLabel(_('Free filename suffix (optional)')))
            self.suffix = Value(W.QLineEdit())
            location_layout.addWidget(self.suffix.widget)
            self.lesson_actions.append(self.suffix.widget)
            self.suffix.widget.textChanged.connect(lambda *_: self.call('changed'))
            tabs = W.QTabWidget()
            right_layout.addWidget(tabs, 1)
            self.question_form = Form(lambda *_: self.call('changed'))
            self.lesson_form = Form(lambda *_: self.call('changed'))
            tabs.addTab(self.question_form, _('Question'))
            tabs.addTab(self.lesson_form, _('Lesson details'))
            self.window.statusBar().showMessage(_('Create a project or open an existing one to begin.'))
            self.window.addAction(self.action(_('Save'), 'Ctrl+S', 'save'))
            self.window.addAction(self.action(_('New project…'), 'Ctrl+N', 'new_project'))
            self.window.addAction(self.action(_('Open project…'), 'Ctrl+O', 'open_project'))

        def action(self, label, shortcut, method):
            import importlib
            G = importlib.import_module(binding + '.QtGui')
            action = G.QAction(label, self.window)
            action.setShortcut(shortcut)
            action.triggered.connect(lambda *_: self.call(method))
            if method == 'save':
                self.lesson_actions.append(action)
            return action

        def call(self, method, *args):
            if self.controller:
                return getattr(self.controller, method)(*args)

        def title(self, text):
            self.window.setWindowTitle(_('Grammatical Cases — Sample Editor') + (' — ' + text if text else ''))

        def status(self, text):
            self.window.statusBar().showMessage(text)

        def project_label(self, text):
            self.project_text.setText(text)

        def set_cases(self, cases):
            from vocabulary import label
            self.case.choices([(c, label(c)) for c in cases])

        def set_state(self, project_open, lesson_open):
            for widget in self.project_actions:
                widget.setEnabled(project_open)
            for widget in self.lesson_actions:
                widget.setEnabled(lesson_open)

        def location_label(self, text):
            self.location_text.setText(text)

        def ask_new_project(self):
            from pathlib import Path
            from project_setup import CASE_IDS, defaults, languages
            from vocabulary import label
            dialog = W.QDialog(self.window)
            dialog.setWindowTitle(_('New project…'))
            dialog.setMinimumWidth(660)
            layout = W.QFormLayout(dialog)
            target = Value(W.QComboBox(), languages())
            layout.addRow(_('Target language'), target.widget)
            code = W.QLineEdit('ru')
            layout.addRow(_('Language tag'), code)
            cases_box = W.QWidget()
            grid = W.QGridLayout(cases_box)
            case_boxes = {}
            for n, case in enumerate(CASE_IDS):
                box = W.QCheckBox(label(case))
                box.setObjectName('case_' + case)
                grid.addWidget(box, n // 2, n % 2)
                case_boxes[case] = box
            layout.addRow(_('Cases (select one to eight)'), cases_box)
            natives = W.QWidget()
            row = W.QHBoxLayout(natives)
            native_boxes = {}
            for native in ('en', 'de', 'ru', 'pl'):
                box = W.QCheckBox(native)
                row.addWidget(box)
                native_boxes[native] = box
            layout.addRow(_('Sentence translation languages'), natives)
            metadata = {}
            for key, title in [('contributor', _('Contributor')), ('license', _('License')), ('sources', _('Sources'))]:
                widget = W.QLineEdit() if key != 'sources' else W.QPlainTextEdit()
                widget.setObjectName('project_' + key)
                if key == 'license':
                    widget.setPlaceholderText('MIT, CC BY 4.0, …')
                if key == 'sources':
                    widget.setMaximumHeight(70)
                layout.addRow(title, widget)
                metadata[key] = widget
            hint = W.QLabel(_('These values are reused for every new lesson in this project.'))
            hint.setWordWrap(True)
            layout.addRow(hint)
            directory = W.QLineEdit()
            directory.setObjectName('project_directory')
            folder_row = W.QWidget()
            row = W.QHBoxLayout(folder_row)
            row.setContentsMargins(0, 0, 0, 0)
            row.addWidget(directory, 1)
            browse = W.QPushButton(_('Browse…'))
            row.addWidget(browse)
            layout.addRow(_('Project directory'), folder_row)
            hint = W.QLabel(_('Choose a new or empty directory. Existing files are never overwritten.'))
            hint.setWordWrap(True)
            layout.addRow(hint)
            suggested = ['']
            def suggest_folder():
                value = str(Path.home() / 'case-samples' / (code.text().strip() or 'new-project'))
                if not directory.text() or directory.text() == suggested[0]:
                    directory.setText(value)
                suggested[0] = value
            def select_language(*_args):
                selected = target.get()
                code.setReadOnly(selected != 'other')
                code.setText('' if selected == 'other' else selected)
                values = defaults(code.text())
                for case, box in case_boxes.items():
                    box.setChecked(case in values['cases'])
                for native, box in native_boxes.items():
                    box.setChecked(native in values['native_languages'])
                suggest_folder()
            target.widget.setObjectName('project_language')
            target.widget.currentIndexChanged.connect(select_language)
            code.textChanged.connect(lambda *_: suggest_folder())
            def choose_folder():
                path = W.QFileDialog.getExistingDirectory(dialog, _('Project directory'), directory.text())
                if path:
                    directory.setText(path)
            browse.clicked.connect(choose_folder)
            result = {}
            def accept():
                selected_cases = [c for c, box in case_boxes.items() if box.isChecked()]
                selected_natives = [c for c, box in native_boxes.items() if box.isChecked()]
                if not selected_cases or not selected_natives or not code.text().strip() or not directory.text().strip():
                    W.QMessageBox.warning(dialog, _('New project…'), _('Select a language, cases, translation languages and directory.'))
                    return
                values = {key: (widget.toPlainText() if key == 'sources' else widget.text()).strip() for key, widget in metadata.items()}
                for key, title in [('contributor', _('Contributor')), ('license', _('License')), ('sources', _('Sources'))]:
                    if not values[key]:
                        W.QMessageBox.warning(dialog, _('New project…'), _('Please enter {field}.').format(field=title))
                        metadata[key].setFocus()
                        return
                result.update(folder=directory.text(), code=code.text().strip(), cases=selected_cases, native_languages=selected_natives, **values)
                dialog.accept()
            buttons = W.QDialogButtonBox()
            buttons.addButton(_('Create project'), W.QDialogButtonBox.ButtonRole.AcceptRole)
            buttons.addButton(_('Cancel'), W.QDialogButtonBox.ButtonRole.RejectRole)
            buttons.accepted.connect(accept)
            buttons.rejected.connect(dialog.reject)
            layout.addRow(buttons)
            select_language()
            return result if dialog.exec() == W.QDialog.DialogCode.Accepted else None

        def ask_move(self, cases, track, case):
            from vocabulary import label
            dialog = W.QDialog(self.window)
            dialog.setWindowTitle(_('Move lesson…'))
            layout = W.QFormLayout(dialog)
            group = Value(W.QComboBox(), [('nouns', _('Nouns')), ('adjectives', _('Adjectives and numerals'))])
            selected_case = Value(W.QComboBox(), [(c, label(c)) for c in cases])
            group.set(track)
            selected_case.set(case)
            layout.addRow(_('Group'), group.widget)
            layout.addRow(_('Case'), selected_case.widget)
            hint = W.QLabel(_('The lesson will move when you press Save.'))
            hint.setWordWrap(True)
            layout.addRow(hint)
            B = W.QDialogButtonBox.StandardButton
            buttons = W.QDialogButtonBox(B.Ok | B.Cancel)
            buttons.accepted.connect(dialog.accept)
            buttons.rejected.connect(dialog.reject)
            layout.addRow(buttons)
            if dialog.exec() == W.QDialog.DialogCode.Accepted:
                return group.get(), selected_case.get()
            return None

        def confirm_delete_lesson(self, name):
            B = W.QMessageBox.StandardButton
            return W.QMessageBox.question(self.window, _('Delete lesson'),
                _('Delete {name}? Unsaved changes will be discarded. The saved file will be kept in recovery backups.').format(name=name),
                B.Yes | B.No, B.No) == B.Yes

        def clear_forms(self):
            self.question_form.set_fields([])
            self.lesson_form.set_fields([])

        def choose_project(self):
            return W.QFileDialog.getExistingDirectory(self.window, _('Choose a sample project'))

        def message(self, kind, title, text):
            function = {'error': W.QMessageBox.critical, 'warning': W.QMessageBox.warning, 'info': W.QMessageBox.information}[kind]
            function(self.window, title, text)

        def ask_save(self):
            B = W.QMessageBox.StandardButton
            result = W.QMessageBox.question(self.window, _('Unsaved changes'), _('Save this lesson before continuing?'),
                                           B.Save | B.Discard | B.Cancel, B.Save)
            return {B.Save: 'save', B.Discard: 'discard'}.get(result, 'cancel')

        def ask_suffix(self, initial):
            value, accepted = W.QInputDialog.getText(self.window, _('Lesson filename'), _('New filename suffix'), text=initial)
            return value if accepted else None

        def confirm_delete(self):
            B = W.QMessageBox.StandardButton
            return W.QMessageBox.question(self.window, _('Delete question'), _('Remove this question?'),
                                          B.Yes | B.No, B.No) == B.Yes

        def close(self):
            self.window.close_approved = True
            self.window.close()

        def run(self):
            self.window.show()
            return self.app.exec()

    return View()
