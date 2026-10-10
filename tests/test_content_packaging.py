#!/usr/bin/env python3
"""Integration checks: Android asset retains authored IDs, answers and translations."""
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
import sys

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location("packaging", ROOT / "scripts/package-content.py")
packaging = importlib.util.module_from_spec(spec)
spec.loader.exec_module(packaging)

class ContentPackagingTest(unittest.TestCase):
    def test_authoritative_content_is_packaged_without_loss(self):
        with tempfile.TemporaryDirectory() as directory:
            first, second = Path(directory) / "first.json", Path(directory) / "second.json"
            packaging.package(ROOT / "samples", first)
            packaging.package(ROOT / "samples", second)
            self.assertEqual(first.read_bytes(), second.read_bytes())
            asset = json.loads(first.read_text())
            self.assertEqual({"ru", "pl"}, {p["learning_language"] for p in asset["languages"]})
            questions = [q for p in asset["languages"] for s in p["samples"] for q in s["sentences"]]
            self.assertEqual(390, len(questions))
            self.assertEqual(390, len({q["id"] for q in questions}))
            for question in questions:
                self.assertIn(question["correct"], question["options"])
                self.assertEqual({"en", "de"}, set(question["native_text"]))
                self.assertIn("___", question["neutral_prompt"])

if __name__ == "__main__":
    unittest.main()
