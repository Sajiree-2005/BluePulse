import sys, pathlib, tempfile, numpy as np
R = pathlib.Path(__file__).parents[2]; sys.path[:0] = [str(R/"core"), str(R/"edge")]
from scipy.io import wavfile
from bluepulse_core import synth_blast
from bluepulse_core.reef_health import fit_baseline, zscore, activity_score
from bluepulse_edge.agent import load_wav, events_from_audio, Buffer, heartbeat

def test_wav_to_event_to_buffer_to_upload():
    with tempfile.TemporaryDirectory() as d:
        p = pathlib.Path(d)/"a.wav"; wavfile.write(p, 16000, synth_blast(16000, 6, 3.0)); sr, x = load_wav(p)
        ev = events_from_audio(x, sr, "s1", 16.05, 73.46); assert len(ev) == 1 and ev[0]["clip"]["bytes_b64"]
        b = Buffer(); b.add("event", ev[0]); b.add("event", ev[0]); assert len(b.pending()) == 1   # idempotent
        assert b.flush(lambda k, p: (_ for _ in ()).throw(OSError())) == 0 and len(b.pending()) == 1  # cloud down: kept
        got = []; assert b.flush(lambda k, p: got.append(p)) == 1 and not b.pending() and got[0]["sensor_id"] == "s1"
def test_resample_and_heartbeat():
    with tempfile.TemporaryDirectory() as d:
        p = pathlib.Path(d)/"b.wav"; wavfile.write(p, 8000, (np.random.default_rng(0).normal(0, .05, 8000*12)*32767).astype(np.int16))
        sr, x = load_wav(p); assert sr == 16000 and len(x) == 16000*12 and "aci" in heartbeat(x, sr, "s1")["indices"]
def test_reef_health_drop_is_visible():
    rng = np.random.default_rng(1); base = fit_baseline([(h, 10 + rng.normal(0, 1)) for h in range(24) for _ in range(30)])
    ok = activity_score([zscore(10.2, base, 5)]); low = activity_score([zscore(4.0, base, 5)])
    assert ok > 90 and low < 60
