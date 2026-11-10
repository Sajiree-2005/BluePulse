"""Builds manifest.csv for train_ast.py from folders data/<label>/<site>/*.wav and adds SYNTHETIC blasts (marked) on your ambient clips.
python build_manifest.py   (needs numpy scipy; run from repo root with core on PYTHONPATH). Metrics must be reported on REAL-only validation too."""
import csv, pathlib, sys, numpy as np
sys.path.insert(0, str(pathlib.Path(__file__).parents[1] / "core"))
from scipy.io import wavfile
from bluepulse_core import synth_blast
root = pathlib.Path("data"); rows = []
for f in sorted(root.glob("*/*/*.wav")): rows.append((str(f), f.parts[1], f.parts[2], "real"))
syn = root / "synthetic_blast" / "synthetic"; syn.mkdir(parents=True, exist_ok=True); rng = np.random.default_rng(0)
for i in range(300): p = syn / f"s{i}.wav"; wavfile.write(p, 16000, synth_blast(16000, 3, rng.uniform(.5, 1.5), np.random.default_rng(i), snr_db=float(rng.uniform(-5, 20)))); rows.append((str(p), "blast", "synthetic", "synthetic"))
with open("manifest.csv", "w", newline="") as f:
    w = csv.writer(f); w.writerow(["path", "label", "site", "source"]); w.writerows(rows)
print(len(rows), "rows; real:", sum(r[3] == "real" for r in rows))
