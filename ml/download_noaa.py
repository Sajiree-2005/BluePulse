"""UNTESTED (no network in build sandbox). Downloads a few NOAA SanctSound audio files from the public bucket over HTTPS.
python ml/download_noaa.py --prefix sanctsound/audio/ --list          # browse folders
python ml/download_noaa.py --prefix sanctsound/audio/<site>/ --n 5 --out raw/noaa
Then: python ml/prepare_clips.py --src raw/noaa --label ambient --site noaa_<site>
NOAA audio is UNLABELLED: use it as ambient/background (and as noise to mix under synthetic blasts), not as ground-truth biology."""
import argparse, json, pathlib, urllib.parse, urllib.request
B = "noaa-passive-bioacoustic"; ap = argparse.ArgumentParser(); ap.add_argument("--prefix", required=True); ap.add_argument("--list", action="store_true"); ap.add_argument("--n", type=int, default=5); ap.add_argument("--out", default="raw/noaa"); a = ap.parse_args()
q = urllib.parse.urlencode({"prefix": a.prefix, "delimiter": "/", "maxResults": 200}); d = json.load(urllib.request.urlopen(f"https://storage.googleapis.com/storage/v1/b/{B}/o?{q}"))
if a.list: print("folders:", *d.get("prefixes", []), sep="\n  "); print("files:", *[i["name"] for i in d.get("items", [])][:20], sep="\n  ")
else:
    out = pathlib.Path(a.out); out.mkdir(parents=True, exist_ok=True)
    for it in [i for i in d.get("items", []) if i["name"].lower().endswith((".flac", ".wav"))][:a.n]:
        dest = out / pathlib.Path(it["name"]).name; urllib.request.urlretrieve(f"https://storage.googleapis.com/{B}/{urllib.parse.quote(it['name'])}", dest); print("got", dest)
