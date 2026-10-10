#!/usr/bin/env python3
"""Focused regression checks for contributor mistakes; uses stdlib unittest."""
from pathlib import Path
import runpy
import shutil
import tempfile
import unittest
import yaml

PROJECT=Path(__file__).resolve().parents[1]
API=runpy.run_path(str(PROJECT/'scripts/validate-samples.py'))
validate=API['validate']
ValidationError=API['ValidationError']

class ContentValidation(unittest.TestCase):
    def setUp(self):
        self.directory=tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.root=Path(self.directory.name)/'samples'
        shutil.copytree(PROJECT/'samples',self.root)
        self.path=self.root/'ru/nouns/dative.yaml'
        self.data=yaml.safe_load(self.path.read_text(encoding='utf-8'))

    def reject(self,change,message):
        change(self.data)
        self.path.write_text(yaml.safe_dump(self.data,allow_unicode=True,sort_keys=False),encoding='utf-8')
        with self.assertRaisesRegex(ValidationError,message):
            validate(self.root)

    def test_complete_draft_set_is_usable_for_implementation(self):
        totals,subtypes,statuses=validate(self.root)
        self.assertEqual(sum(totals.values()),390)
        self.assertEqual(set(totals),{('ru','nouns'),('ru','adjectives'),('pl','nouns'),('pl','adjectives')})
        self.assertTrue(subtypes[('ru','cardinal_numeral')] and subtypes[('pl','ordinal_numeral')])
        self.assertEqual(statuses['draft'],390)

    def test_duplicate_option_after_unicode_and_case_normalization(self):
        self.reject(lambda d:d['sentences'][0]['options'].update(b=d['sentences'][0]['options']['a'].upper()),'duplicate answer text')

    def test_missing_native_translation(self):
        self.reject(lambda d:d['sentences'][0]['native_text'].pop('de'),'missing translation')

    def test_broken_correct_answer_key(self):
        self.reject(lambda d:d['sentences'][0].update(correct='e'),'correct must reference')

    def test_incomplete_fifteen_sentence_sample(self):
        self.reject(lambda d:d['sentences'].pop(),'exactly 15')

    def test_numeral_cannot_be_misfiled_in_nouns(self):
        self.reject(lambda d:d['sentences'][0].update(word_type='cardinal_numeral'),'does not belong')

    def test_duplicate_question_id_across_files(self):
        other=yaml.safe_load((self.root/'ru/nouns/accusative.yaml').read_text(encoding='utf-8'))
        self.reject(lambda d:d['sentences'][0].update(id=other['sentences'][0]['id']),'duplicate question ID')

    def test_yaml_duplicate_key_is_not_silently_overwritten(self):
        with self.path.open('a',encoding='utf-8') as f:
            f.write('\ncase: accusative\n')
        with self.assertRaisesRegex(ValidationError,'duplicate YAML key'):
            validate(self.root)

    def test_missing_case_is_reported(self):
        self.path.unlink()
        with self.assertRaisesRegex(ValidationError,'missing cases'):
            validate(self.root)

    def test_drafts_fail_release_validation(self):
        with self.assertRaisesRegex(ValidationError,'linguistic review required'):
            validate(self.root,release=True)

    def test_option_reordering_retains_stable_correct_key(self):
        q=self.data['sentences'][0]
        correct_text=q['options'][q['correct']]
        q['options']=dict(reversed(list(q['options'].items())))
        self.path.write_text(yaml.safe_dump(self.data,allow_unicode=True,sort_keys=False),encoding='utf-8')
        validate(self.root)
        self.assertEqual(q['options'][q['correct']],correct_text)

if __name__=='__main__':
    unittest.main()
