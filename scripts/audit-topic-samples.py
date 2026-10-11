#!/usr/bin/env python3
"""Report imported topic structure and unresolved source issues; no downloads."""
from collections import Counter
from pathlib import Path
import importlib.util
import sys
sys.dont_write_bytecode = True
spec = importlib.util.spec_from_file_location("validator", Path(__file__).with_name("validate-samples.py"))
v = importlib.util.module_from_spec(spec)
spec.loader.exec_module(v)
root = Path(__file__).resolve().parents[1] / "samples"
v.validate(root)
print("# Version 2 sample audit\n")
print("These are content revisions using YAML schema 1. Local draft previews only; unspecified licenses do not establish redistribution permission.\n")
for folder in sorted(root.glob("*-v2")):
    print(f"## {folder.name}\n")
    counts = Counter()
    problems = []
    for path in sorted(folder.glob("*/*.yaml")):
        data = v.read(path)
        questions = data["sentences"]
        counts[data["track"]] += len(questions)
        print(f"- {data['case']} / {data['track']} / {data['topic']['name']}: {len(questions)}")
        for q in questions:
            texts = [x.strip().casefold() for x in q["options"].values()]
            if len(set(texts)) != len(texts):
                problems.append(f"{q['id']}: duplicate option text")
            if any(x is None for x in q["features"].values()):
                problems.append(f"{q['id']}: unknown grammatical feature")
    print(f"\nTotals: {dict(counts)}.\n")
    print("Source issues retained for review:\n")
    for problem in problems:
        print(f"- {problem}")
    if not problems:
        print("- No duplicate choices or null grammatical features found.")
    print()
