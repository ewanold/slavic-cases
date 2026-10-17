#!/usr/bin/env python3
"""Reusable Linux/Windows dependency installer; every pip artifact is hash-pinned."""
import argparse
import hashlib
import json
import tempfile
from urllib.request import urlopen
import os
from pathlib import Path
import subprocess
import sys
import venv


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--ui', choices=('auto', 'qt', 'tk'), default='auto',
                        help='auto/qt installs PySide6 Essentials; tk installs only base tools')
    parser.add_argument('--venv', type=Path, help='optional environment location')
    args = parser.parse_args()
    if sys.version_info[:2] != (3, 12):
        parser.error('Python 3.12 is required by the pinned dependency set.')
    root = Path(__file__).resolve().parents[1]
    default = (Path(os.environ.get('LOCALAPPDATA', Path.home() / 'AppData/Local')) / 'LearnGrammaticalCases/sample-editor-venv'
               if sys.platform == 'win32' else Path.home() / '.local/share/slavic-cases/sample-editor-venv')
    folder = (args.venv or default).resolve()
    venv.EnvBuilder(with_pip=False).create(folder)
    python = folder / ('Scripts/python.exe' if sys.platform == 'win32' else 'bin/python')
    if subprocess.run([str(python), '-m', 'pip', '--version'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode:
        bootstrap = json.loads((root / 'requirements/sample-editor-pip.json').read_text(encoding='utf-8'))
        with tempfile.TemporaryDirectory(prefix='case-editor-pip-') as temp:
            wheel = Path(temp) / bootstrap['filename']
            with urlopen(bootstrap['url'], timeout=60) as response:
                content = response.read()
            if hashlib.sha256(content).hexdigest() != bootstrap['sha256']:
                raise RuntimeError('pip bootstrap checksum mismatch')
            wheel.write_bytes(content)
            environment = dict(os.environ, PYTHONPATH=str(wheel))
            subprocess.run([str(python), '-m', 'pip', 'install', '--no-index', '--no-deps', str(wheel)],
                           env=environment, check=True)
    for lock in ['sample-editor-base.txt'] + ([] if args.ui == 'tk' else ['sample-editor-qt.txt']):
        subprocess.run([str(python), '-m', 'pip', 'install', '--disable-pip-version-check',
                        '--only-binary=:all:', '--require-hashes', '-r', str(root / 'requirements' / lock)], check=True)
    subprocess.run([str(python), str(root / 'scripts/sample-editor-translations.py'), 'compile'], check=True)
    print(f'Ready: {python} {root / "tools/sample_editor/app.py"}')


if __name__ == '__main__':
    main()
