#!/usr/bin/env python3
"""Extract/update gettext catalogs or compile PO to MO. Requires pinned Babel."""
import argparse
import ast
from datetime import datetime, timezone
from pathlib import Path
from babel.messages import Catalog, extract, mofile, pofile

ROOT = Path(__file__).resolve().parents[1] / 'tools/sample_editor'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=('extract', 'compile'))
    args = parser.parse_args()
    if args.action == 'extract':
        catalog = Catalog(project='Grammatical Cases Sample Editor', version='0.2',
                          creation_date=datetime(2026, 10, 17, tzinfo=timezone.utc),
                          copyright_holder='Learn Grammatical Cases contributors',
                          msgid_bugs_address='https://github.com/ewanold/slavic-cases/issues')
        for path in [*sorted(ROOT.glob('*.py')), ROOT.parents[1] / 'scripts/validate-samples.py']:
            with path.open('rb') as source:
                for line, message, comments, context in extract.extract('python', source, keywords={'_': None}):
                    catalog.add(message, locations=[(path.name, line)], auto_comments=comments, context=context)
            # AST positions are reliable even when require() conditions contain strings/lists.
            for node in ast.walk(ast.parse(path.read_text(encoding='utf-8'))):
                if not isinstance(node, ast.Call) or not isinstance(node.func, ast.Name):
                    continue
                position = {'EditorError': 0, 'ValidationError': 0, 'require': 1}.get(node.func.id)
                if position is not None and len(node.args) > position:
                    message = node.args[position]
                    if isinstance(message, ast.Constant) and isinstance(message.value, str):
                        catalog.add(message.value, locations=[(path.name, node.lineno)])
        with (ROOT / 'locales/sample-editor.pot').open('wb') as target:
            pofile.write_po(target, catalog, width=100)
        for path in ROOT.glob('locales/*/LC_MESSAGES/*.po'):
            with path.open('rb') as source:
                translation = pofile.read_po(source)
            translation.update(catalog)
            with path.open('wb') as target:
                pofile.write_po(target, translation, width=100)
    else:
        for path in ROOT.glob('locales/*/LC_MESSAGES/*.po'):
            with path.open('rb') as source:
                catalog = pofile.read_po(source, locale=path.parents[1].name, abort_invalid=True)
            errors = [(message.id, str(error)) for message, problem in catalog.check() for error in problem]
            if errors:
                raise ValueError(f'{path}: {errors}')
            with path.with_suffix('.mo').open('wb') as target:
                mofile.write_mo(target, catalog)
            print(f'Compiled {path.relative_to(ROOT)}')


if __name__ == '__main__':
    main()
