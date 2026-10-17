"""Tkinter fallback view. Uses exactly the same controller and restricted forms."""
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, ttk

from fields import apply_fields, display_value
from i18n import _


class Value:
    def __init__(self, parent, choices=None, changed=None):
        self.var = tk.StringVar()
        self.items = []
        self.updating = False
        self.widget = ttk.Entry(parent, textvariable=self.var) if choices is None else ttk.Combobox(
            parent, textvariable=self.var, state='readonly')
        if choices is not None:
            self.choices(choices)
            if changed:
                self.widget.bind('<<ComboboxSelected>>', lambda e: changed())
        elif changed:
            self.var.trace_add('write', lambda *_: changed() if not self.updating else None)

    def choices(self, items):
        self.items = list(items)
        self.widget.configure(values=[label for _, label in items])

    def get(self):
        if isinstance(self.widget, ttk.Combobox):
            n = self.widget.current()
            return self.items[n][0] if n >= 0 else None
        return self.var.get()

    def set(self, value):
        if isinstance(self.widget, ttk.Combobox):
            n = next((n for n, (v, _) in enumerate(self.items) if v == value), -1)
            self.var.set(self.items[n][1] if n >= 0 else '')
        else:
            self.updating = True
            try:
                self.var.set(value)
            finally:
                self.updating = False


class List:
    def __init__(self, parent, callback):
        frame = ttk.Frame(parent)
        frame.pack(fill='both', expand=True)
        self.widget = tk.Listbox(frame, exportselection=False, height=9)
        scroll = ttk.Scrollbar(frame, command=self.widget.yview)
        scroll.pack(side='right', fill='y')
        self.widget.pack(fill='both', expand=True)
        self.widget.configure(yscrollcommand=scroll.set)
        self.widget.bind('<<ListboxSelect>>', lambda e: callback())

    def set(self, items, selected=None):
        self.widget.delete(0, 'end')
        for value in items:
            self.widget.insert('end', value)
        self.select(selected)

    def select(self, n):
        self.widget.selection_clear(0, 'end')
        if n is not None:
            self.widget.selection_set(n)
            self.widget.see(n)

    def selected(self):
        selection = self.widget.curselection()
        return selection[0] if selection else None


class Form(ttk.Frame):
    def __init__(self, parent, changed):
        super().__init__(parent)
        self.changed = changed
        self.fields, self.inputs = [], {}
        self.canvas = tk.Canvas(self, highlightthickness=0)
        scroll = ttk.Scrollbar(self, orient='vertical', command=self.canvas.yview)
        scroll.pack(side='right', fill='y')
        self.canvas.pack(fill='both', expand=True)
        self.canvas.configure(yscrollcommand=scroll.set)
        self.body = ttk.Frame(self.canvas, padding=8)
        self.window = self.canvas.create_window(0, 0, window=self.body, anchor='nw')
        self.body.bind('<Configure>', lambda e: self.canvas.configure(scrollregion=self.canvas.bbox('all')))
        self.canvas.bind('<Configure>', lambda e: self.canvas.itemconfigure(self.window, width=e.width))

    def wheel(self, event):
        if str(event.widget).startswith(str(self)):
            self.canvas.yview_scroll(-1 if event.num == 4 or event.delta > 0 else 1, 'units')

    def set_fields(self, fields):
        for child in self.body.winfo_children():
            child.destroy()
        self.fields, self.inputs, self.widgets = fields, {}, {}
        for field in fields:
            ttk.Label(self.body, text=field.label, wraplength=500).pack(anchor='w', pady=(5, 0))
            if field.kind in ('multiline', 'lines', 'details'):
                widget = tk.Text(self.body, height=6 if field.kind == 'details' else 3, wrap='word', undo=True)
                widget.insert('1.0', display_value(field))
                widget.edit_modified(False)
                if field.readonly:
                    widget.configure(state='disabled')
                else:
                    def modified(event, text=widget):
                        if text.edit_modified():
                            self.changed()
                            text.edit_modified(False)
                    widget.bind('<<Modified>>', modified)
                widget.pack(fill='x')
                getter = lambda w=widget: w.get('1.0', 'end-1c')
            else:
                value = Value(self.body, field.choices if field.kind == 'choice' else None, self.changed)
                value.set(field.value if field.kind == 'choice' else display_value(field))
                if field.readonly:
                    value.widget.configure(state='readonly')
                value.widget.pack(fill='x')
                getter = value.get
                widget = value.widget
            self.inputs[field.path] = getter
            self.widgets[field.path] = widget
        self.canvas.yview_moveto(0)

    def apply(self, data):
        return apply_fields(data, self.fields, {p: get() for p, get in self.inputs.items()})


class View:
    def __init__(self):
        self.controller = None
        self.project_actions, self.lesson_actions = [], []
        self.root = tk.Tk()
        self.root.geometry('1150x820')
        self.root.minsize(800, 580)
        self.title('')
        self.root.protocol('WM_DELETE_WINDOW', lambda: self.call('close'))
        toolbar = ttk.Frame(self.root, padding=8)
        toolbar.pack(fill='x')
        for label, method, args in [(_('New project…'), 'new_project', ()), (_('Open project…'), 'open_project', ()), (_('Save'), 'save', ()),
                                    (_('Save copy…'), 'save', (True,)), (_('Validate project'), 'validate', ())]:
            button = ttk.Button(toolbar, text=label, command=lambda m=method, a=args: self.call(m, *a))
            button.pack(side='left', padx=3)
            if method == 'save':
                self.lesson_actions.append(button)
            elif method == 'validate':
                self.project_actions.append(button)
        self.project_text = ttk.Label(toolbar, text=_('Create a project or open an existing one to begin.'), wraplength=320)
        self.project_text.pack(side='left', padx=8)
        pane = ttk.Panedwindow(self.root, orient='horizontal')
        pane.pack(fill='both', expand=True, padx=8)
        left, right = ttk.Frame(pane), ttk.Frame(pane)
        pane.add(left, weight=1)
        pane.add(right, weight=4)
        def combo(parent, label, choices, action):
            ttk.Label(parent, text=label).pack(anchor='w')
            value = Value(parent, choices, lambda: self.call(action))
            value.widget.pack(fill='x', pady=(0, 5))
            return value
        tracks = [('nouns', _('Nouns')), ('adjectives', _('Adjectives and numerals'))]
        self.track = combo(left, _('Group'), tracks, 'filter_changed')
        self.case = combo(left, _('Case'), [], 'filter_changed')
        self.project_actions.extend([self.track.widget, self.case.widget])
        ttk.Label(left, text=_('Lessons (filename suffix)')).pack(anchor='w')
        self.lessons = List(left, lambda: self.call('select_lesson'))
        lesson_buttons = ttk.Frame(left)
        lesson_buttons.pack(fill='x', pady=5)
        for text, method in [(_('Add lesson'), 'add_lesson'), (_('Delete lesson'), 'delete_lesson')]:
            button = ttk.Button(lesson_buttons, text=text, command=lambda m=method: self.call(m))
            button.pack(side='left')
            (self.project_actions if method == 'add_lesson' else self.lesson_actions).append(button)
        ttk.Label(left, text=_('Questions')).pack(anchor='w', pady=(8, 0))
        self.questions = List(left, lambda: self.call('select_question'))
        buttons = ttk.Frame(left)
        buttons.pack(fill='x', pady=5)
        for label, method, args in [(_('Add'), 'add_question', ()), (_('Duplicate'), 'add_question', (True,)),
                                    (_('Delete'), 'delete_question', ())]:
            button = ttk.Button(buttons, text=label, command=lambda m=method, a=args: self.call(m, *a))
            button.pack(side='left')
            self.lesson_actions.append(button)
        location = ttk.LabelFrame(right, text=_('Lesson file'), padding=6)
        location.pack(fill='x')
        self.location_text = ttk.Label(location, text=_('Select a lesson'))
        self.location_text.pack(anchor='w')
        move = ttk.Button(location, text=_('Move lesson…'), command=lambda: self.call('move_lesson'))
        move.pack(anchor='w', pady=4)
        self.lesson_actions.append(move)
        ttk.Label(location, text=_('Free filename suffix (optional)')).pack(anchor='w')
        self.suffix = Value(location, changed=lambda: self.call('changed'))
        self.suffix.widget.pack(fill='x')
        self.lesson_actions.append(self.suffix.widget)
        tabs = ttk.Notebook(right)
        tabs.pack(fill='both', expand=True, pady=8)
        self.question_form = Form(tabs, lambda: self.call('changed'))
        self.lesson_form = Form(tabs, lambda: self.call('changed'))
        tabs.add(self.question_form, text=_('Question'))
        tabs.add(self.lesson_form, text=_('Lesson details'))
        self.status_var = tk.StringVar(value=_('Create a project or open an existing one to begin.'))
        ttk.Label(self.root, textvariable=self.status_var, padding=8, wraplength=1000).pack(fill='x')
        for form in (self.question_form, self.lesson_form):
            for event in ('<MouseWheel>', '<Button-4>', '<Button-5>'):
                self.root.bind_all(event, form.wheel, add='+')
        self.root.bind('<Control-n>', lambda e: self.call('new_project'))
        self.root.bind('<Control-s>', lambda e: self.call('save'))
        self.root.bind('<Control-o>', lambda e: self.call('open_project'))

    def call(self, method, *args):
        if self.controller:
            return getattr(self.controller, method)(*args)

    def title(self, text):
        self.root.title(_('Grammatical Cases — Sample Editor') + (' — ' + text if text else ''))

    def status(self, text):
        self.status_var.set(text)

    def project_label(self, text):
        self.project_text.configure(text=text)

    def set_cases(self, cases):
        from vocabulary import label
        self.case.choices([(c, label(c)) for c in cases])

    def set_state(self, project_open, lesson_open):
        for widget, enabled in [(w, project_open) for w in self.project_actions] + [(w, lesson_open) for w in self.lesson_actions]:
            widget.configure(state=('readonly' if isinstance(widget, ttk.Combobox) else 'normal') if enabled else 'disabled')

    def location_label(self, text):
        self.location_text.configure(text=text)

    def ask_new_project(self):
        from pathlib import Path
        from project_setup import CASE_IDS, defaults, languages
        from vocabulary import label
        class NewProjectDialog(simpledialog.Dialog):
            def body(self, master):
                ttk.Label(master, text=_('Target language')).pack(anchor='w')
                self.target = Value(master, languages())
                self.target.set('ru')
                self.target.widget.pack(fill='x')
                ttk.Label(master, text=_('Language tag')).pack(anchor='w')
                self.code = Value(master)
                self.code.widget.pack(fill='x')
                ttk.Label(master, text=_('Cases (select one to eight)')).pack(anchor='w', pady=(8, 0))
                cases = ttk.Frame(master)
                cases.pack(fill='x')
                self.cases = {}
                for n, case in enumerate(CASE_IDS):
                    var = tk.BooleanVar()
                    ttk.Checkbutton(cases, text=label(case), variable=var).grid(row=n // 2, column=n % 2, sticky='w')
                    self.cases[case] = var
                ttk.Label(master, text=_('Sentence translation languages')).pack(anchor='w', pady=(8, 0))
                natives = ttk.Frame(master)
                natives.pack(fill='x')
                self.natives = {}
                for native in ('en', 'de', 'ru', 'pl'):
                    var = tk.BooleanVar()
                    ttk.Checkbutton(natives, text=native, variable=var).pack(side='left')
                    self.natives[native] = var
                self.metadata = {}
                for key, title in [('contributor', _('Contributor')), ('license', _('License')), ('sources', _('Sources'))]:
                    ttk.Label(master, text=title).pack(anchor='w', pady=(5, 0))
                    if key == 'sources':
                        widget = tk.Text(master, height=3, width=64, wrap='word')
                        widget.pack(fill='x')
                        self.metadata[key] = lambda w=widget: w.get('1.0', 'end-1c')
                    else:
                        value = Value(master)
                        value.widget.pack(fill='x')
                        self.metadata[key] = value.get
                ttk.Label(master, text=_('These values are reused for every new lesson in this project.'), wraplength=480).pack(pady=6)
                ttk.Label(master, text=_('Project directory')).pack(anchor='w', pady=(8, 0))
                self.directory = Value(master)
                self.directory.widget.configure(width=64)
                self.directory.widget.pack(fill='x')
                def browse():
                    path = filedialog.askdirectory(parent=self, title=_('Project directory'), mustexist=False)
                    if path:
                        self.directory.set(path)
                ttk.Button(master, text=_('Browse…'), command=browse).pack(anchor='w')
                ttk.Label(master, text=_('Choose a new or empty directory. Existing files are never overwritten.'), wraplength=480).pack(pady=8)
                self.suggested = ''
                def suggest(*_args):
                    value = str(Path.home() / 'case-samples' / (self.code.get().strip() or 'new-project'))
                    if not self.directory.get() or self.directory.get() == self.suggested:
                        self.directory.set(value)
                    self.suggested = value
                def select(*_args):
                    target = self.target.get()
                    self.code.set('' if target == 'other' else target)
                    self.code.widget.configure(state='normal' if target == 'other' else 'readonly')
                    values = defaults(self.code.get())
                    for case, var in self.cases.items():
                        var.set(case in values['cases'])
                    for native, var in self.natives.items():
                        var.set(native in values['native_languages'])
                    suggest()
                self.target.widget.bind('<<ComboboxSelected>>', select)
                self.code.var.trace_add('write', suggest)
                select()
                return self.target.widget

            def buttonbox(self):
                frame = ttk.Frame(self)
                ttk.Button(frame, text=_('Create project'), command=self.ok).pack(side='left', padx=5)
                ttk.Button(frame, text=_('Cancel'), command=self.cancel).pack(side='left', padx=5)
                frame.pack(pady=8)
                self.bind('<Return>', self.ok)
                self.bind('<Escape>', self.cancel)

            def validate(self):
                self.result = dict(folder=self.directory.get(), code=self.code.get().strip(),
                                   cases=[c for c, v in self.cases.items() if v.get()],
                                   native_languages=[c for c, v in self.natives.items() if v.get()])
                if not all(self.result.values()):
                    messagebox.showwarning(_('New project…'), _('Select a language, cases, translation languages and directory.'), parent=self)
                    self.result = None
                    return False
                values = {key: getter().strip() for key, getter in self.metadata.items()}
                for key, title in [('contributor', _('Contributor')), ('license', _('License')), ('sources', _('Sources'))]:
                    if not values[key]:
                        messagebox.showwarning(_('New project…'), _('Please enter {field}.').format(field=title), parent=self)
                        self.result = None
                        return False
                self.result.update(values)
                return True
        return NewProjectDialog(self.root, _('New project…')).result

    def ask_move(self, cases, track, case):
        from vocabulary import label
        class MoveDialog(simpledialog.Dialog):
            def body(self, master):
                ttk.Label(master, text=_('Group')).pack(anchor='w')
                self.group = Value(master, [('nouns', _('Nouns')), ('adjectives', _('Adjectives and numerals'))])
                self.group.set(track)
                self.group.widget.pack(fill='x')
                ttk.Label(master, text=_('Case')).pack(anchor='w')
                self.case = Value(master, [(c, label(c)) for c in cases])
                self.case.set(case)
                self.case.widget.pack(fill='x')
                ttk.Label(master, text=_('The lesson will move when you press Save.'), wraplength=380).pack(pady=8)
                return self.group.widget

            def apply(self):
                self.result = self.group.get(), self.case.get()
        return MoveDialog(self.root, _('Move lesson…')).result

    def confirm_delete_lesson(self, name):
        return messagebox.askyesno(_('Delete lesson'),
            _('Delete {name}? Unsaved changes will be discarded. The saved file will be kept in recovery backups.').format(name=name), parent=self.root)

    def clear_forms(self):
        self.question_form.set_fields([])
        self.lesson_form.set_fields([])

    def choose_project(self):
        return filedialog.askdirectory(title=_('Choose a sample project'), parent=self.root)

    def message(self, kind, title, text):
        {'error': messagebox.showerror, 'warning': messagebox.showwarning, 'info': messagebox.showinfo}[kind](title, text, parent=self.root)

    def ask_save(self):
        answer = messagebox.askyesnocancel(_('Unsaved changes'), _('Save this lesson before continuing?'), parent=self.root)
        return 'cancel' if answer is None else ('save' if answer else 'discard')

    def ask_suffix(self, initial):
        return simpledialog.askstring(_('Lesson filename'), _('New filename suffix'), initialvalue=initial, parent=self.root)

    def confirm_delete(self):
        return messagebox.askyesno(_('Delete question'), _('Remove this question?'), parent=self.root)

    def close(self):
        self.root.destroy()

    def run(self):
        self.root.mainloop()
