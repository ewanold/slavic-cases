# Desktop sample editor

Create and edit grammatical-case sample projects using forms rather than YAML.
The editor runs with Python 3.12 on Linux and Windows x64. It prefers **Qt**
(PySide6, then PyQt6); **Tkinter** is the fallback if neither Qt binding is
available in the Python interpreter running the editor. No server or account is
needed, and editing works offline. The default installer prepares PySide6
Essentials (Qt Widgets), PyYAML and Babel in a user-local environment.

## Linux setup and launch

Run from the repository root with Python 3.12 available:

```bash
bash scripts/install-sample-editor.sh
bash scripts/run-sample-editor.sh samples/ru-v2
```

The Qt setup does not need sudo. For the smaller Tkinter-only installation:

```bash
bash scripts/install-sample-editor.sh --ui tk
bash scripts/run-sample-editor.sh --ui tk samples/ru-v2
```

If Tkinter is missing, that installer uses `sudo apt install python3-tk` on
Debian/Ubuntu. This OS package follows the authenticated distribution repository.
The isolated environment defaults to
`~/.local/share/slavic-cases/sample-editor-venv`, outside SMB/network checkouts.
The installer bootstraps a checksum-verified pip wheel if ensurepip/pip is missing;
`python3-venv` is not required for that bootstrap.

## Windows setup and launch

Download/clone the repository, then open a terminal in its folder. Run:

```powershell
powershell -ExecutionPolicy Bypass -File scripts\install-sample-editor.ps1 -InstallPython
scripts\run-sample-editor.cmd samples\ru-v2
```

`-InstallPython` allows the script to install Python **3.12.10 x64** for this user
if Python 3.12 is absent. It downloads the official python.org installer, checks
its committed SHA-256, and enables Tcl/Tk and the Python launcher. If Python 3.12
is already installed, it is reused; omit `-InstallPython` to require an existing
installation. The PowerShell execution-policy override applies to this process.
No system-wide execution policy is changed. Python version/checksum changes belong
in the installer, not in ad-hoc download commands.

The environment lives in
`%LOCALAPPDATA%\LearnGrammaticalCases\sample-editor-venv`; dependencies are not
installed into system Python. Double-click `scripts\run-sample-editor.cmd` to open
an editor without a preselected project. To install only the Tkinter dependencies,
pass `-Ui tk` to the installer and `--ui tk` to the launcher. Windows setup targets
x64; native Windows/PowerShell testing is still pending. No standalone .exe has
been packaged.

## Selecting the interface and language

Omit the project argument to select a folder in the app. Examples on Linux:

```bash
bash scripts/run-sample-editor.sh --ui qt --language de samples/ru-v2
bash scripts/run-sample-editor.sh --ui tk --language ru samples/pl-v2
bash scripts/run-sample-editor.sh --language pl samples/ru
```

Use the same arguments with `scripts\run-sample-editor.cmd` on Windows. Default
`--ui auto` tries PySide6, PyQt6, then Tkinter. `--ui qt` reports an error if neither
Qt binding is available; it does not silently switch toolkits. Selection concerns
Python bindings in the chosen environment, not a separately installed Qt SDK.
Neither startup nor fallback downloads anything. Display/Qt platform-plugin failures
are reported separately from missing bindings; a usable desktop display is needed.

The interface follows the OS/environment language by default, with English fallback.
`--language en|de|ru|pl` overrides it for this run. App controls, field labels,
dialogs, case names, grammar choices and project display names are localized.
Sentence translations remain authored lesson content. Editor and structural
validation errors use the same PO catalogs, including missing attribution,
translations, answer checks and save conflicts. File paths and question IDs remain
unchanged. Low-level OS and YAML-parser detail may remain in its original language.
Translation wording awaits native-speaker review.

`SAMPLE_EDITOR_PYTHON` selects another Python executable for either launcher. The
Linux launcher also accepts the legacy content-tools environment as a fallback.
Custom environments can be prepared with
`python3 scripts/install-sample-editor.py --venv /your/local/folder` (use `py -3.12`
on Windows). Python packages are version-pinned and wheel hashes are committed in
`requirements/sample-editor-{base,qt}.txt`; source builds are excluded. Reusable
`scripts/update-sample-editor-locks.py` refreshes their hashes from the pinned
PyPI releases for maintainer review. Qt package licensing remains its upstream
[LGPL/GPL/commercial licensing](https://doc.qt.io/qtforpython-6/commercial/index.html); this repository's own editor code is MIT. This
source-based setup does not bundle a standalone Qt application installer.

## Editing a project

Click **New project…** (Ctrl+N) to create a project without hand-writing YAML.
The dialog lets you choose:

- **Target language:** Russian, Polish or German, or **Other language** with a
  language tag such as `cs`.
- **Cases:** defaults are Russian six, Polish seven (including vocative), or
  German four. Adjust the checkboxes as needed; choose one to eight cases.
  Other languages start with no guessed inventory: select their teaching cases.
- **Sentence translation languages:** choose English, German, Russian and/or
  Polish. The default is the current GUI language if it differs from the target;
  otherwise English (German when the target is English).
- **Contributor, License, Sources:** enter the common attribution once. These
  required values are stored in the project and prefilled for every new lesson,
  including after reopening. Sources can contain several lines. No license or
  author identity is assumed on your behalf.
- **Project directory:** a new or empty folder; the suggested location is
  `~/case-samples/<language-tag>`. Existing nonempty folders are refused.

Creation writes `language.yaml` and the `nouns/` and `adjectives/` folders, then
opens a blank first noun lesson for the first selected case. The manifest and
attribution defaults are saved immediately; the blank lesson is an unsaved draft until completed. No
example content or source attribution is fabricated. New projects use the simple
15-question lesson format; existing deep/topic projects keep their own format.
Before creating/opening a project, controls requiring it are disabled rather
than presenting editable but unusable selectors or Save buttons.

A project can have any directory name, for example `My Russian course`. Use
**Open project…** for an existing folder containing `language.yaml`, `nouns/` and
`adjectives/`. The manifest supplies the case inventory. For Android packaging,
copy a completed project into a compatible `samples/<language-tag>/` or
`samples/<language-tag>-v2/` folder without overwriting another pack. Arbitrary
editor folder names are normalized only in the editor's temporary validation
copy; build/package naming rules remain unchanged. Imported language manifests
can still be edited externally for unsupported metadata.

1. Select **Group**, **Case**, then a lesson in the left column. Adjectives include
   cardinal and ordinal numerals. Select a question below the lessons.
2. Edit the dictionary form, prompt, native translations, answers and correct key.
   Word type, answer scope, gender, number, animacy and declension use dropdowns.
   Quantity fields accept whole numbers. Unknown grammatical features retain their
   original null value until you explicitly select a value. Answer d can be blank
   in a deep three-choice lesson.
3. **Lesson details** provides contributor, license, source description, review
   status, translated instructions and topic fields. Imported source details,
   schema metadata, stable IDs and unsupported nested fields are read-only and
   preserved. There are no raw YAML input tabs. Complex source metadata/new
   manifest structures still require an external text editor.
4. **Add**, **Duplicate** and **Delete** manage questions. Simple lessons must
   still contain exactly 15 valid questions when saved; deep lesson sizes vary.
5. **Validate project** checks the current unsaved lesson alongside the other
   project files without writing. **Save** (Ctrl+S) validates, backs up an existing
   original, then saves. **Save copy** creates new IDs with draft status. Unsaved
   changes prompt before navigation or closing.

Save checks the completed lessons already present and permits missing case/group
coverage while you build the project. Blank questions or missing required metadata
still block saving a lesson. **Validate project**, Android builds and release
checks require full coverage; release also requires review and redistribution rights.

The **Group** and **Case** selectors on the left are for browsing only. The right
side shows the current lesson's group/case as text. **Move lesson…** opens a dialog
to change its destination; the file moves only on **Save**. Editing the filename
suffix renames it on Save. IDs remain stable. Changing group requires compatible
word types. Moving the only lesson for a required case/track leaves coverage
incomplete until it is replaced, so whole-project validation/building will fail.
Changing the browse filter clears the details after handling unsaved changes.

**Add lesson** and **Delete lesson** sit below the lesson list, separate from the
question controls. Add creates a blank, unsaved draft in the currently browsed
group/case and asks for a filename suffix. Simple lessons start with 15 question
slots (including numeral slots for adjectives); deep lessons start with one and
can grow. No imported author/source claims are copied into a new lesson. Fill the
questions and instructions before its first Save. Contributor, license and sources
come from the project's saved defaults; you can override them in Lesson details
when a particular lesson has different attribution. Existing projects without
saved defaults keep the previous blank metadata behavior; imported lessons are
never relabelled automatically. Nothing is written until the lesson and all other existing lessons pass structural
validation; missing case/group coverage does not block an authoring save. A star
in the lesson list marks the unsaved draft. Discarding it leaves no file.

Delete asks for confirmation and discards unsaved edits to that lesson. An existing
saved file is moved into recovery backups immediately; there is no need to press
Save afterwards. An unsaved draft is simply discarded. A file changed elsewhere
cannot be deleted through stale editor state. Deleting the last lesson for a
case/track can temporarily leave the project incomplete: add a replacement or
restore its recovery copy before validation/building. `language.yaml` is unchanged.

Filenames use a declared case ID and optional suffix: `genitive.yaml`,
`genitive-practice-1.yaml`, `genitive-mnogo-malo.yaml`. The spelling is `genitive`.
Suffixes accept letters, digits, hyphens and underscores, and start with a letter
or digit. Case/group selectors own the prefix and folder. File/metadata mismatches
are reported and must be corrected externally before opening. Renaming a file
never rewrites topic IDs or translated topic names in `language.yaml`.

Original stable IDs, unknown YAML fields, source attribution and null features
survive round trips. Saves retain introductory comments but PyYAML reformats the
rest and drops inline/interior comments. Review the Git diff before contributing.
Format validation cannot judge grammar or redistribution permissions. Return edited
reviewed content to draft until someone has reviewed the changes.

Every save retains the previous file in
`<project>/.sample-editor-backups/<track>/`, ignored by Git and Android packaging.
To recover it, close the editor, copy the chosen `.bak` over the original lesson
filename, then reopen. Renames/copies refuse existing destinations; externally
changed files must be reopened before saving. Symlinked lessons and multiple
simultaneously open lesson tabs are unsupported. Saved YAML enters the Android
app on its next build; installed phone apps are not patched by the editor.

## Translating with PO files

Both interfaces share the English
[template](locales/sample-editor.pot) and these UTF-8 catalogs:

- [German](locales/de/LC_MESSAGES/sample-editor.po)
- [Russian](locales/ru/LC_MESSAGES/sample-editor.po)
- [Polish](locales/pl/LC_MESSAGES/sample-editor.po)

Edit `msgstr` in a PO editor such as Poedit. Keep `msgid` and placeholders such as
`{name}`, `{language}` and `{count}` unchanged. Recompile after editing (the
installer also does this). Use the editor environment's Python:

```bash
~/.local/share/slavic-cases/sample-editor-venv/bin/python scripts/sample-editor-translations.py compile
```

Windows equivalent:

```powershell
& "$env:LOCALAPPDATA\LearnGrammaticalCases\sample-editor-venv\Scripts\python.exe" scripts/sample-editor-translations.py compile
```

Compiled `.mo` files are committed so normal startup needs only Python's standard
gettext module. For a new language, copy the POT into
`locales/<code>/LC_MESSAGES/sample-editor.po`, set its Language/Plural-Forms
headers, translate, compile and launch with `--language <code>`. Maintainers run
`scripts/sample-editor-translations.py extract` with the editor Python after
changing interface text; it updates the template and merges existing catalogs.
Review fuzzy entries before recompiling. Babel compilation checks placeholder
compatibility. This PO workflow applies to the desktop editor; the Android GUI
continues to use its existing `strings.xml` resources.

## Verification

Run all Python tests with the editor Python. The optional Qt test uses an offscreen
platform and edits only temporary copies:

```bash
QT_QPA_PLATFORM=offscreen ~/.local/share/slavic-cases/sample-editor-venv/bin/python -m unittest discover -s tests -v
```

Windows: set `$env:QT_QPA_PLATFORM='offscreen'` and use the environment's Python
path shown above. Without PySide6 the Qt integration test is skipped. Pure model,
backend selection, PO coverage and all 1,722 typed-question round trips still run.
The Qt window has been inspected from an offscreen screenshot. Native Windows
and Tkinter window testing remain pending; this environment has Tkinter but cannot
connect to a desktop display.

Manual desktop check on working copies: open each project, change case/group,
edit/save/reopen, create/copy/move/delete a lesson, test cancel/discard/save prompts, add/delete
questions and scroll at a small window size. Check English/German/Russian/Polish
with `--language`. Check `--ui qt`, `--ui tk` and automatic fallback independently.
