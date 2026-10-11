#!/usr/bin/env python3
"""Validate authoritative YAML and generate an offline Android JSON asset. No downloads."""
import argparse
import importlib.util
import json
from pathlib import Path
import sys

sys.dont_write_bytecode = True

def package(root, output):
    spec = importlib.util.spec_from_file_location("validation", Path(__file__).with_name("validate-samples.py"))
    validation = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(validation)
    validation.validate(root)
    packs = []
    for manifest in sorted(root.glob("*/language.yaml")):
        language = validation.read(manifest)
        sets = [validation.read(p) for track in language["tracks"]
                for p in sorted((manifest.parent / track).glob("*.yaml"))]
        for sample in sets:
            if sample.get("content_profile") == "apk-topic-import" and not sample.get("contributor"):
                sample["contributor"] = "Unknown original author; APK source metadata preserved"
        packs.append({**language, "pack_id": manifest.parent.name,
                      "name": language["name"], "samples": sets})
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps({"schema_version": 1, "languages": packs}, ensure_ascii=False,
                                 sort_keys=True, indent=2) + "\n", encoding="utf-8")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    package(Path(__file__).resolve().parent.parent / "samples", args.output)
