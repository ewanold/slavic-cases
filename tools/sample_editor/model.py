"""Desktop author's project model. Never changes Android content implicitly."""
from copy import deepcopy
import os
from pathlib import Path
import re
import runpy
import shutil
import tempfile
import uuid

import yaml

VALIDATOR = runpy.run_path(str(Path(__file__).resolve().parents[2] / 'scripts/validate-samples.py'))
read = VALIDATOR['read']


class EditorError(ValueError):
    def __init__(self, template, **params):
        self.template, self.params = template, params
        super().__init__(template.format(**params) if params else template)


def parse_mapping(text):
    try:
        value = yaml.load(text, Loader=VALIDATOR['UniqueLoader'])
    except (yaml.YAMLError, ValueError, TypeError) as exc:
        raise EditorError(str(exc)) from exc
    if not isinstance(value, dict):
        raise EditorError('Expected a YAML mapping (field: value).')
    return value


def dump(value):
    return yaml.safe_dump(value, allow_unicode=True, sort_keys=False, width=100)


class Project:
    def __init__(self, folder):
        self.folder = Path(folder).resolve()
        self.manifest = read(self.folder / 'language.yaml')
        code = self.manifest.get('learning_language')
        if not isinstance(code, str) or not re.fullmatch(r'[a-z]{2,3}(?:-[A-Za-z0-9]{2,8})*', code):
            raise EditorError('Invalid learning-language tag in language.yaml.')
        metadata = self.manifest.get('lesson_defaults', {})
        if not isinstance(metadata, dict) or not all(isinstance(metadata.get(k, ''), str) for k in ('contributor', 'license', 'sources')):
            raise EditorError('Project lesson defaults must contain text values.')
        self.cases = [c['id'] for c in self.manifest['cases']]
        self.tracks = self.manifest['tracks']
        if (not 1 <= len(self.cases) <= 8 or len(set(self.cases)) != len(self.cases)
                or not all(isinstance(c, str) and re.fullmatch(r'[a-z][a-z0-9_-]*', c) for c in self.cases)
                or self.tracks != ['nouns', 'adjectives']):
            raise EditorError('Project must declare safe, distinct case IDs and nouns/adjectives tracks.')

    @classmethod
    def create(cls, folder, code, cases, native_languages, case_names=None, name=None, contributor='', license='', sources=''):
        code = code.strip()
        tag = r'[a-z]{2,3}(?:-[A-Za-z0-9]{2,8})*'
        if not re.fullmatch(tag, code):
            raise EditorError('Enter a language tag such as ru, pl, de or cs.')
        allowed = {'nominative', 'genitive', 'dative', 'accusative', 'instrumental', 'prepositional', 'locative', 'vocative'}
        if not cases or len(cases) > 8 or len(set(cases)) != len(cases) or not set(cases) <= allowed:
            raise EditorError('Select between one and eight distinct cases.')
        if (not native_languages or len(set(native_languages)) != len(native_languages)
                or not all(isinstance(c, str) and re.fullmatch(tag, c) for c in native_languages)):
            raise EditorError('Select at least one translation language.')
        if not str(folder).strip():
            raise EditorError('Choose a project directory.')
        folder = Path(folder).expanduser()
        if folder.is_symlink():
            raise EditorError('Choose a directory that is not a symlink.')
        folder = folder.resolve()
        if folder.exists() and (not folder.is_dir() or any(folder.iterdir())):
            raise EditorError('Choose a new or empty directory. Existing files will not be overwritten.')
        manifest = dict(schema_version=1, learning_language=code, name=name or code,
                        native_languages=list(native_languages), tracks=['nouns', 'adjectives'],
                        cases=[dict(id=c, name=(case_names or {}).get(c, c.capitalize())) for c in cases])
        metadata = dict(contributor=contributor.strip(), license=license.strip(), sources=sources.strip())
        if any(metadata.values()):
            manifest['lesson_defaults'] = metadata
        created, made_folder, made_manifest = [], not folder.exists(), False
        try:
            folder.mkdir(parents=True, exist_ok=True)
            for track in manifest['tracks']:
                directory = folder / track
                directory.mkdir()
                created.append(directory)
            with (folder / 'language.yaml').open('x', encoding='utf-8') as stream:
                made_manifest = True
                stream.write('# Original authoring project; lessons are drafts until reviewed.\n' + dump(manifest))
            return cls(folder)
        except Exception:
            if made_manifest:
                (folder / 'language.yaml').unlink()
            for directory in reversed(created):
                try:
                    directory.rmdir()
                except OSError:
                    pass
            if made_folder:
                try:
                    folder.rmdir()
                except OSError:
                    pass
            raise

    def identity(self, path):
        path = Path(path)
        for case in sorted(self.cases, key=len, reverse=True):
            if path.stem == case:
                return case, ''
            if path.stem.startswith(case + '-'):
                return case, path.stem[len(case) + 1:]
        raise EditorError('{filename}: filename must start with a declared case, e.g. genitive-practice-1.yaml', filename=path.name)

    def files(self, track, case):
        result = []
        for path in sorted((self.folder / track).glob('*.yaml')):
            try:
                if self.identity(path)[0] == case:
                    result.append(path)
            except EditorError:
                continue
        return result

    def naming_issues(self):
        issues = []
        for track in self.tracks:
            for path in sorted((self.folder / track).glob('*.yaml')):
                try:
                    case, _ = self.identity(path)
                    data = read(path)
                    if data.get('case') != case or data.get('track') != track:
                        issues.append(EditorError('{filename}: filename/folder and YAML case/track disagree', filename=str(path.relative_to(self.folder))))
                except (EditorError, VALIDATOR['ValidationError']) as exc:
                    issues.append(exc)
        return issues

    def destination(self, track, case, extension):
        if track not in self.tracks or case not in self.cases:
            raise EditorError('Choose a declared track and case.')
        extension = extension.strip()
        if extension and not re.fullmatch(r'[^\W_][\w-]*', extension, re.UNICODE):
            raise EditorError('Suffix must use letters, numbers, hyphens or underscores; no spaces or paths.')
        return self.folder / track / (case + ('-' + extension if extension else '') + '.yaml')

    def validate(self, replacement=None, allow_incomplete=False):
        # Use the authoritative validator, scoped to this project rather than siblings.
        with tempfile.TemporaryDirectory(prefix='case-editor-') as temp:
            root = Path(temp)
            copied = root / self.manifest['learning_language']
            shutil.copytree(self.folder, copied, ignore=shutil.ignore_patterns('.sample-editor-backups'))
            if replacement:
                old, target, data = replacement
                if old is not None and old != target:
                    (copied / old.relative_to(self.folder)).unlink()
                (copied / target.relative_to(self.folder)).write_text(dump(data), encoding='utf-8')
            try:
                totals, _, _ = VALIDATOR['validate'](root, allow_incomplete=allow_incomplete)
            except (VALIDATOR['ValidationError'], TypeError, KeyError) as exc:
                if hasattr(exc, 'template'):
                    params = {k: str(v).replace(str(copied), str(self.folder)) if isinstance(v, (str, Path)) else v
                              for k, v in exc.params.items()}
                    raise EditorError(exc.template, **params) from exc
                raise EditorError(str(exc).replace(str(copied), str(self.folder))) from exc
            return sum(totals.values())


class Document:
    @classmethod
    def new(cls, project, track, case, extension):
        """Start an unsaved original lesson; never clone imported attribution."""
        path = project.destination(track, case, extension)
        if path.exists():
            raise EditorError('Destination already exists. Choose another suffix.')
        doc = cls.__new__(cls)
        doc.project, doc.path = project, path
        doc.track, doc.case, doc.extension = track, case, extension.strip()
        doc.original, doc.header, doc.is_new = None, '# Original draft lesson; review is pending.\n', True
        manifest = project.manifest
        language = manifest['learning_language']
        identifier = f'{language}-{track}-{case}-{uuid.uuid4().hex[:12]}'
        doc.data = dict(schema_version=1, id=identifier, learning_language=language, track=track,
                        case=case, native_languages=list(manifest['native_languages']),
                        instruction={code: '' for code in manifest['native_languages']},
                        contributor='', license='', sources='', review_status='draft', sentences=[])
        doc.data.update({key: manifest.get('lesson_defaults', {}).get(key, '')
                         for key in ('contributor', 'license', 'sources')})
        profile = manifest.get('content_profile')
        topic_profile = profile in ('apk-topic-import', 'polish-topic-adaptation')
        if profile is not None:
            doc.data['content_profile'] = profile
        if topic_profile:
            doc.data['topic'] = {'id': extension.strip() or 'practice', 'name': extension.strip() or 'Practice'}
        for n in range(1 if topic_profile else 15):
            word_type = 'noun' if track == 'nouns' else 'adjective'
            if track == 'adjectives' and not topic_profile and n >= 13:
                word_type = 'cardinal_numeral' if n == 13 else 'ordinal_numeral'
            features = dict(number=None, gender=None, animacy=None)
            if word_type == 'cardinal_numeral':
                features.update(quantity=1, noun_dictionary_form='')
            doc.data['sentences'].append(dict(
                id=f'{identifier}-{n + 1:03}', word_type=word_type, dictionary_form='',
                features=features, native_text={c: '' for c in manifest['native_languages']},
                neutral_prompt='___', answer_scope='word', options={k: '' for k in 'abcd'}, correct='a'))
        return doc

    def __init__(self, project, path):
        self.project = project
        if Path(path).is_symlink():
            raise EditorError('Editing symlinked lessons is not supported.')
        self.path = Path(path).resolve()
        if self.path.parent.parent != project.folder or self.path.parent.name not in project.tracks:
            raise EditorError('Select a YAML lesson in this project’s nouns/adjectives folder.')
        self.case, self.extension = project.identity(self.path)
        self.track = self.path.parent.name
        self.original = self.path.read_bytes()
        self.is_new = False
        self.data = read(self.path)
        if self.data.get('case') != self.case or self.data.get('track') != self.track:
            raise EditorError('Filename/folder and YAML case/track disagree. Correct the source before editing.')
        # Keep introductory attribution/comments. PyYAML reformats the rest.
        self.header = ''
        for line in self.original.decode('utf-8').splitlines(keepends=True):
            if line.startswith('#') or not line.strip():
                self.header += line
            else:
                break

    def save(self, data, track, case, extension, copy=False):
        target = self.project.destination(track, case, extension)
        if self.path.is_symlink() or target.is_symlink() or target.parent.resolve() != self.project.folder / track:
            raise EditorError('Saving through symlinks is not supported.')
        if not self.is_new and self.path.read_bytes() != self.original:
            raise EditorError('File changed outside the editor. Reopen it before saving.')
        if ((target != self.path or self.is_new) and target.exists()) or (copy and target == self.path):
            raise EditorError('Destination already exists. Choose another suffix.')
        updated = deepcopy(data)
        updated['case'], updated['track'] = case, track
        if copy:
            # Clones must not introduce duplicate stable IDs or carry a review claim.
            token = uuid.uuid4().hex[:12]
            updated['id'] = f'{self.project.manifest["learning_language"]}-{track}-{case}-{token}'
            for n, question in enumerate(updated['sentences'], 1):
                question['id'] = f'{updated["id"]}-{n:03}'
            updated['review_status'] = 'draft'
        self.project.validate((None if copy or self.is_new else self.path, target, updated), allow_incomplete=True)
        if not self.is_new:
            self.backup_path().write_bytes(self.original)
        content = (self.header + dump(updated)).encode('utf-8')
        fd, staging = tempfile.mkstemp(prefix='.case-editor-', dir=target.parent)
        try:
            with os.fdopen(fd, 'wb') as stream:
                stream.write(content)
                stream.flush()
                os.fsync(stream.fileno())
            # Check again after validation, before replacing the source.
            if not self.is_new and self.path.read_bytes() != self.original:
                raise EditorError('File changed while validating; save cancelled.')
            if target == self.path and not self.is_new:
                os.replace(staging, target)
            else:
                if os.name == 'nt':
                    # Windows rename is exclusive and also works on volumes without hard links.
                    os.rename(staging, target)
                else:
                    # POSIX rename would overwrite, so create an exclusive hard link instead.
                    os.link(staging, target)
                    os.unlink(staging)
                if not copy and not self.is_new:
                    self.path.unlink()
        finally:
            if os.path.exists(staging):
                os.unlink(staging)
        self.path, self.original, self.data = target, content, updated
        self.case, self.track, self.extension = case, track, extension.strip()
        self.is_new = False
        return target

    def backup_path(self):
        folder = self.project.folder / '.sample-editor-backups' / self.track
        folder.mkdir(parents=True, exist_ok=True)
        return folder / (self.path.name + '.' + uuid.uuid4().hex + '.bak')

    def delete(self):
        """Move a saved lesson to recovery storage; refuse stale editor state."""
        if self.is_new:
            return None
        if self.path.is_symlink() or self.path.read_bytes() != self.original:
            raise EditorError('File changed outside the editor. Reopen it before deleting.')
        backup = self.backup_path()
        os.rename(self.path, backup)
        return backup
