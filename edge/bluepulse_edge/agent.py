"""BluePulse edge agent. Attaches to existing recorders: watches a folder of WAV files, runs Tier-0 detection,
buffers events in SQLite, uploads with retries.  python -m bluepulse_edge.agent watch DIR --api URL --key KEY --sensor ID --lat 16.05 --lon 73.46"""
import argparse, base64, io, json, pathlib, sqlite3, sys, time, urllib.request, uuid
from datetime import datetime, timezone
import numpy as np
from scipy.io import wavfile
from scipy.signal import resample_poly
from bluepulse_core import detect_transients, spectral_entropy, aci

TARGET_SR = 16000

def load_wav(path):
    sr, x = wavfile.read(path)
    x = x.astype(np.float32) / (np.iinfo(x.dtype).max if np.issubdtype(x.dtype, np.integer) else 1.0)
    if x.ndim > 1: x = x.mean(axis=1)
    if sr != TARGET_SR:
        from math import gcd; g = gcd(sr, TARGET_SR); x = resample_poly(x, TARGET_SR // g, sr // g).astype(np.float32)
    return TARGET_SR, x

def clip_b64(x, sr):
    b = io.BytesIO(); wavfile.write(b, sr, (np.clip(x, -1, 1) * 32767).astype(np.int16)); return base64.b64encode(b.getvalue()).decode()

def events_from_audio(x, sr, sensor, lat, lon, start=None):
    start = start or datetime.now(timezone.utc); out = []
    for t in detect_transients(x, sr):
        a, b = max(0, int((t - 1) * sr)), min(len(x), int((t + 2) * sr)); seg = x[a:b]
        out.append({"event_id": uuid.uuid4().hex, "sensor_id": sensor, "started_at": (start.timestamp() + t - 1 if a else start.timestamp() + t),
                    "duration_s": len(seg) / sr, "sensor_position": {"lat": lat, "lon": lon}, "sample_rate_hz": sr,
                    "tier0": {"peak_db": float(20*np.log10(np.abs(seg).max() + 1e-9)), "detector": "transient_v1"},
                    "clip": {"format": "wav", "bytes_b64": clip_b64(seg, sr)}, "edge_version": "0.1.0"})
    return out

def heartbeat(x, sr, sensor):
    return {"sensor_id": sensor, "ts": time.time(), "indices": {"aci": aci(x[:sr*10]), "spectral_entropy": spectral_entropy(x[:sr*10])}}

class Buffer:
    """SQLite outbox: nothing is lost if the cloud sleeps. event_id is the idempotency key."""
    def __init__(self, path=":memory:"):
        self.db = sqlite3.connect(path); self.db.execute("create table if not exists q(id text primary key, kind text, payload text, sent int default 0)")
    def add(self, kind, p): self.db.execute("insert or ignore into q(id,kind,payload) values(?,?,?)", (p.get("event_id", uuid.uuid4().hex), kind, json.dumps(p))); self.db.commit()
    def pending(self): return self.db.execute("select id,kind,payload from q where sent=0").fetchall()
    def flush(self, send):
        n = 0
        for id_, kind, p in self.pending():
            try: send(kind, json.loads(p))
            except Exception: break          # stop on first failure; retry next round
            self.db.execute("update q set sent=1 where id=?", (id_,)); self.db.commit(); n += 1
        return n

def http_sender(api, key):
    def send(kind, p):
        route = "/v1/ingest/events" if kind == "event" else "/v1/ingest/heartbeat"
        r = urllib.request.Request(api + route, json.dumps(p).encode(), {"Content-Type": "application/json", "X-Sensor-Key": key})
        urllib.request.urlopen(r, timeout=20).read()
    return send

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("mode", choices=["watch", "replay"]); ap.add_argument("path")
    for a in ("api", "key", "sensor"): ap.add_argument("--" + a, required=True)
    ap.add_argument("--lat", type=float, required=True); ap.add_argument("--lon", type=float, required=True); ap.add_argument("--db", default="outbox.db")
    a = ap.parse_args(); buf = Buffer(a.db); send = http_sender(a.api, a.key); seen = set()
    while True:
        files = [pathlib.Path(a.path)] if a.mode == "replay" else sorted(pathlib.Path(a.path).glob("*.wav"))
        for f in files:
            if f in seen: continue
            seen.add(f); sr, x = load_wav(f)
            for e in events_from_audio(x, sr, a.sensor, a.lat, a.lon): buf.add("event", e)
            buf.add("heartbeat", heartbeat(x, sr, a.sensor))
        print("sent", buf.flush(send), "pending", len(buf.pending()), flush=True)
        if a.mode == "replay": break
        time.sleep(10)

if __name__ == "__main__": main()
