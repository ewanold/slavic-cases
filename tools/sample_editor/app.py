#!/usr/bin/env python3
"""Cross-platform launcher. Prefer Qt bindings, fall back to Tkinter."""
import argparse
import importlib
from pathlib import Path
import sys


def select_backend(preferred='auto', probe=importlib.import_module):
    failures = []
    if preferred in ('auto', 'qt'):
        for binding in ('PySide6', 'PyQt6'):
            try:
                probe(binding + '.QtWidgets')
                return 'qt', binding
            except (ImportError, OSError) as exc:
                failures.append(str(exc))
    if preferred in ('auto', 'tk'):
        try:
            probe('tkinter')
            return 'tk', None
        except (ImportError, OSError) as exc:
            failures.append(str(exc))
    raise RuntimeError('No usable GUI backend. Run the sample-editor installer.\n' + '\n'.join(failures))


def main(argv=None):
    parser = argparse.ArgumentParser(description='Edit grammatical-case sample projects with Qt or Tkinter.')
    parser.add_argument('project', nargs='?', type=Path, help='folder containing language.yaml')
    parser.add_argument('--ui', choices=('auto', 'qt', 'tk'), default='auto')
    parser.add_argument('--language', help='interface language, e.g. en or de; default: OS locale')
    args = parser.parse_args(argv)
    from i18n import configure
    configure(args.language)
    try:
        backend, binding = select_backend(args.ui)
        if backend == 'qt':
            from qt_view import create_view
            view = create_view(binding)
        else:
            from tk_view import View
            view = View()
        from controller import Editor
        Editor(view, args.project)
        return view.run() or 0
    except (ImportError, RuntimeError) as exc:
        print(str(exc), file=sys.stderr)
        return 1
    except Exception as exc:
        print(f'Cannot start sample editor: {exc}', file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
