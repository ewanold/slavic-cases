"""Protect translator resource IDs and typed format arguments across locales."""
from pathlib import Path
import re
import unittest
import xml.etree.ElementTree as ET

RES = Path(__file__).resolve().parents[1] / 'app/src/main/res'

class UiTranslations(unittest.TestCase):
    def test_locales_cover_default_strings_and_preserve_format_arguments(self):
        def read(folder):
            entries = ET.parse(RES/folder/'strings.xml').getroot().findall('string')
            names = [item.attrib['name'] for item in entries]
            self.assertEqual(len(names),len(set(names)), 'Duplicate resource IDs')
            values = {item.attrib['name']: ''.join(item.itertext()) for item in entries}
            self.assertTrue(all(value.strip() for value in values.values()))
            return values
        english = read('values')
        for folder in ['values-de', 'values-ru', 'values-pl']:
            with self.subTest(locale=folder):
                translated = read(folder)
                self.assertEqual(set(english), set(translated), 'Missing or obsolete translations')
                for name, text in english.items():
                    expected = sorted(re.findall(r'%\d+\$[ds]', text))
                    actual = sorted(re.findall(r'%\d+\$[ds]', translated[name]))
                    self.assertEqual(expected, actual, name)
                    for value in [text, translated[name]]:
                        remainder = re.sub(r'%\d+\$[ds]|%%', '', value)
                        self.assertNotIn('%', remainder, f'{name}: use numbered arguments or %%')
