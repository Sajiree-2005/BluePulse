"""Turn any folder of recordings (wav/flac) into 3 s, 16 kHz, mono WAV clips laid out as data/<label>/<site>/*.wav.
python ml/prepare_clips.py --src D:/downloads/shipsear --label vessel --site shipsear [--max 400] [--clip 3.0]
Silent clips are skipped. Needs: pip install numpy scipy soundfile"""
import argparse, pathlib
import numpy as np, soundfile as sf
from math import gcd
from scipy.io import wavfile
from scipy.signal import resample_poly
LABELS = {"blast", "vessel", "biology", "environmental_noise", "ambient"}
def clips(path, clip_s=3.0, sr_out=16000):
    x, sr = sf.read(str(path), dtype="float32", always_2d=True); x = x.mean(axis=1)
    if sr != sr_out: g = gcd(sr, sr_out); x = resample_poly(x, sr_out // g, sr // g).astype(np.float32)
    n = int(clip_s * sr_out)
    for i in range(0, len(x) - n + 1, n):
        c = x[i:i + n]
        if np.sqrt(np.mean(c ** 2)) > 1e-4: yield c
if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("--src", required=True); ap.add_argument("--label", required=True, choices=sorted(LABELS)); ap.add_argument("--site", required=True)
    ap.add_argument("--max", type=int, default=400); ap.add_argument("--clip", type=float, default=3.0); a = ap.parse_args()
    out = pathlib.Path("data") / a.label / a.site; out.mkdir(parents=True, exist_ok=True); k = 0
    for f in sorted(p for p in pathlib.Path(a.src).rglob("*") if p.suffix.lower() in (".wav", ".flac")):
        for c in clips(f, a.clip):
            wavfile.write(out / f"{f.stem}_{k}.wav", 16000, (np.clip(c, -1, 1) * 32767).astype(np.int16)); k += 1
            if k >= a.max: break
        if k >= a.max: break
    print(f"wrote {k} clips to {out}")
