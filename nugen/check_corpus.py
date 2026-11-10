"""Run before every upload: python check_corpus.py  (Nugen refuses .txt files under 500 words)"""
import json, pathlib, sys
root = pathlib.Path(__file__).parent; bad = 0
for f in sorted(root.glob("corpus/*.txt")):
    n = len(f.read_text(encoding="utf-8").split()); ok = n >= 500; bad += not ok
    print(f"{'OK  ' if ok else 'FAIL'} {n:5d} words  {f.name}")
for i, line in enumerate(open(root / "pairs.jsonl", encoding="utf-8"), 1):
    try: json.loads(line)
    except Exception as e: print("BAD JSONL line", i, e); bad += 1
sys.exit(1 if bad else 0)
