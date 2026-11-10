"""Fills your running backend with a realistic, reproducible demo (for the video). python scripts/demo_replay.py [API_URL] [KEY]
Uses synthetic audio: 2 blasts (different sensors), 1 boat engine tone, 1 rain-like noise. Needs backend SENSOR_KEYS to include these sensors (default does)."""
import json, sys, time, urllib.request, uuid, pathlib
import numpy as np
R = pathlib.Path(__file__).parents[1]; sys.path[:0] = [str(R / "core"), str(R / "edge")]
from bluepulse_core import synth_blast
from bluepulse_edge.agent import clip_b64
API = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8000"; KEY = sys.argv[2] if len(sys.argv) > 2 else "secret"; SR = 16000; rng = np.random.default_rng(7)
t = np.arange(SR * 3) / SR
boat = sum(np.sin(2*np.pi*f*t) / (i+1) for i, f in enumerate((55, 110, 165, 220))) * (0.1 + 0.05*np.sin(2*np.pi*0.4*t)); boat = (boat + rng.normal(0, .005, len(t))).astype(np.float32)
rain = rng.normal(0, .08, len(t)).astype(np.float32)
SCEN = [("malvan-north", 16.06, 73.46, synth_blast(SR, 3, 1.0, np.random.default_rng(1), snr_db=18)), ("sindhudurg-reef", 15.90, 73.50, boat),
        ("tarkarli-shelf", 16.00, 73.58, rain), ("malvan-north", 16.07, 73.45, synth_blast(SR, 3, 1.2, np.random.default_rng(2), snr_db=12))]
for sid, lat, lon, x in SCEN:
    ev = {"event_id": uuid.uuid4().hex, "sensor_id": sid, "started_at": time.time(), "duration_s": 3.0, "sensor_position": {"lat": lat, "lon": lon},
          "sample_rate_hz": SR, "tier0": {"detector": "demo"}, "clip": {"format": "wav", "bytes_b64": clip_b64(x, SR)}, "edge_version": "demo"}
    r = urllib.request.Request(API + "/v1/ingest/events", json.dumps(ev).encode(), {"Content-Type": "application/json", "X-Sensor-Key": KEY})
    o = json.load(urllib.request.urlopen(r, timeout=30)); print(f"{sid:16s} -> {o['label']:20s} {o['severity']:8s} conf={o['confidence_score']}  provider={o['provider']}"); time.sleep(1.5)
