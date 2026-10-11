"""German teaching constraints: syncretism, phrase answers and declension coverage."""
from pathlib import Path
import unittest
import yaml

ROOT = Path(__file__).resolve().parents[1] / 'samples/de'

class GermanSamples(unittest.TestCase):
    def test_complete_original_pack_and_unambiguous_choice_labels(self):
        manifest = yaml.safe_load((ROOT/'language.yaml').read_text())
        self.assertEqual(['nominative','genitive','dative','accusative'], [c['id'] for c in manifest['cases']])
        documents = [yaml.safe_load(p.read_text()) for p in ROOT.glob('*/*.yaml')]
        self.assertEqual(8,len(documents))
        for document in documents:
            self.assertEqual('MIT', document['license'])
            self.assertEqual('draft', document['review_status'])
            self.assertEqual(15,len(document['sentences']))
            for q in document['sentences']:
                self.assertEqual('phrase',q['answer_scope'])
                self.assertEqual(4,len(set(q['options'].values())))
                self.assertEqual({'en','de'},set(q['native_text']))
                self.assertEqual(1,q['neutral_prompt'].count('___'))
                filled = q['neutral_prompt'].split(' (')[0].replace('___', q['options'][q['correct']])
                self.assertEqual(filled[0].upper()+filled[1:],q['native_text']['de'])

    def test_german_specific_forms_and_patterns(self):
        def answer(track,case,index):
            q=yaml.safe_load((ROOT/track/f'{case}.yaml').read_text())['sentences'][index]
            return q['options'][q['correct']]
        self.assertEqual('des Studenten',answer('nouns','genitive',8))
        self.assertEqual('dem Nachbarn',answer('nouns','dative',9))
        self.assertEqual('den Kindern',answer('nouns','dative',14))
        self.assertEqual('des guten Freundes',answer('adjectives','genitive',0))
        self.assertEqual('ein junger Lehrer',answer('adjectives','nominative',4))
        self.assertEqual('frischen Tees',answer('adjectives','genitive',7))
        self.assertEqual('kalten Wassers',answer('adjectives','genitive',9))
        self.assertEqual('zwei Kindern',answer('adjectives','dative',11))
        self.assertEqual('der fünf Bücher',answer('adjectives','genitive',12))
        qs=yaml.safe_load((ROOT/'adjectives/nominative.yaml').read_text())['sentences']
        self.assertTrue({'weak','mixed','strong'}.issubset({q['features']['declension'] for q in qs}))
        self.assertEqual({'adjective','cardinal_numeral','ordinal_numeral'},{q['word_type'] for q in qs})
