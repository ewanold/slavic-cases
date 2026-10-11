"""Version 2 compatibility and hierarchy integration checks."""
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
import sys
sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("packaging", ROOT / "scripts/package-content.py")
p = importlib.util.module_from_spec(spec)
spec.loader.exec_module(p)

class TopicPackaging(unittest.TestCase):
    def test_pack_identity_topics_and_variable_choices_survive(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "content.json"
            p.package(ROOT / "samples", output)
            packs = {x["pack_id"]: x for x in json.loads(output.read_text())["languages"]}
            self.assertEqual(set(packs), {"ru", "pl", "de", "ru-v2", "pl-v2"})
            self.assertEqual({"Russian simple", "Russian deep", "Polish simple", "Polish deep", "German simple"}, {x["name"] for x in packs.values()})
            for pack in packs.values():
                self.assertEqual({"en", "de", "ru", "pl"}, set(pack["names"]))
                self.assertEqual(pack["name"], pack["names"]["en"])
                topics = {s["topic"]["id"] for s in pack["samples"] if "topic" in s}
                self.assertEqual(topics, set(pack.get("topic_names", {})))
                for names in pack.get("topic_names", {}).values():
                    self.assertEqual({"en", "de", "ru", "pl"}, set(names))
            self.assertEqual("Russisch vertieft", packs["ru-v2"]["names"]["de"])
            self.assertEqual("Geschlechter", packs["ru-v2"]["topic_names"]["genders"]["de"])
            ru = packs["ru-v2"]
            self.assertTrue(all(s.get("contributor") for s in ru["samples"]))
            self.assertEqual(591, sum(len(s["sentences"]) for s in ru["samples"]))
            genders = next(s for s in ru["samples"] if s["topic"]["id"] == "genders")
            self.assertEqual({"feminine", "masculine", "neuter"}, {q["features"]["gender"] for q in genders["sentences"]})
            self.assertTrue(all(len(q["options"]) == 3 for q in genders["sentences"]))
            self.assertTrue(any(s["topic"]["id"] == "bez-dlya" for s in ru["samples"]))
