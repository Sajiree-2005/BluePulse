import os, sys, pathlib, tempfile
os.environ["DB_PATH"] = tempfile.mktemp(suffix=".db"); os.environ["SENSOR_KEYS"] = "s1:secret"
R = pathlib.Path(__file__).parents[1]; sys.path[:0] = [str(R/"core"), str(R/"edge"), str(pathlib.Path(__file__).parent)]
import numpy as np, tempfile as tf
from scipy.io import wavfile
from fastapi.testclient import TestClient
from bluepulse_core import synth_blast
from bluepulse_edge.agent import load_wav, events_from_audio
import app as A
c = TestClient(A.app)
def _event():
    p = pathlib.Path(tf.mkdtemp())/"a.wav"; wavfile.write(p, 16000, synth_blast(16000, 6, 3.0)); sr, x = load_wav(p)
    return events_from_audio(x, sr, "s1", 16.05, 73.46)[0]
def test_auth_required(): assert c.post("/v1/ingest/events", json=_event(), headers={"X-Sensor-Key": "bad"}).status_code == 401
def test_edge_event_end_to_end():
    e = _event(); r = c.post("/v1/ingest/events", json=e, headers={"X-Sensor-Key": "secret"}); assert r.status_code == 200
    assert r.json()["label"] == "blast" and r.json()["briefing"]
    assert c.post("/v1/ingest/events", json=e, headers={"X-Sensor-Key": "secret"}).status_code == 200      # idempotent retry
    assert len(c.get("/v1/events").json()) == 1 and c.get("/v1/provenance").json()[0]["provider"] == "fake"
def test_llm_timeout_falls_back(monkeypatch):
    monkeypatch.setattr(A, "llm_briefing", lambda *a: (_ for _ in ()).throw(TimeoutError())); e = _event(); e["event_id"] = "x2"
    r = c.post("/v1/ingest/events", json=e, headers={"X-Sensor-Key": "secret"}).json(); assert r["briefing"].startswith("Template alert") and r["label"] == "blast"
def test_health(): assert c.get("/healthz").json() == {"ok": True}

def test_parse_nugen_sse_and_json():
    sse = 'data: {"choices":[{"delta":{"content":"Briefing: "}}]}\n\ndata: {"object":"confidence","confidence_score":60}\n\ndata: {"choices":[{"delta":{"content":"x"}}]}\n\ndata: {"object":"confidence","confidence_score":80}\n\ndata: [DONE]\n'
    assert A.parse_nugen(sse) == ("Briefing: x", 70.0, 60.0)
    assert A.parse_nugen('{"choices":[{"message":{"content":"hi"}}],"confidence_score":88}') == ("hi", 88, 88)

def test_alerts_telegram_message_and_pin(monkeypatch):
    import alerts, os; calls = []
    monkeypatch.setattr(alerts, "_post", lambda url, body, headers=None: calls.append((url, body)))
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "T"); monkeypatch.setenv("TELEGRAM_CHAT_IDS", "42")
    r = alerts.dispatch({"label": "blast", "severity": "critical", "briefing": "b", "confidence_score": 90, "sensor": "s1", "lat": 16.0, "lon": 73.4})
    assert r == [("telegram", True)] and calls[0][0].endswith("/sendMessage") and calls[1][0].endswith("/sendLocation") and calls[1][1]["latitude"] == 16.0
    assert alerts.dispatch({"label": "vessel", "severity": "low", "briefing": "b", "sensor": "s1"}) == []      # low severity: no page
def test_alert_failure_never_raises(monkeypatch):
    import alerts; monkeypatch.setattr(alerts, "_post", lambda *a, **k: (_ for _ in ()).throw(OSError()))
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "T"); monkeypatch.setenv("TELEGRAM_CHAT_IDS", "1")
    assert alerts.dispatch({"label": "blast", "severity": "high", "briefing": "b", "sensor": "s"}) == [("telegram", False)]

def test_heartbeats_and_review():
    assert c.post("/v1/ingest/heartbeat", json={"sensor_id": "s1", "ts": 1.0, "indices": {"aci": 2.0}}, headers={"X-Sensor-Key": "secret"}).status_code == 200
    assert c.get("/v1/heartbeats").json()[0]["indices"]["aci"] == 2.0
    e = _event(); e["event_id"] = "rv1"; c.post("/v1/ingest/events", json=e, headers={"X-Sensor-Key": "secret"})
    assert c.post("/v1/events/rv1/review", json={"review": "false_positive"}).json() == {"ok": True}
    assert [x for x in c.get("/v1/events").json() if x["id"] == "rv1"][0]["review"] == "false_positive"
