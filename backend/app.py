"""BluePulse standalone backend (SQLite, runs anywhere). Person B can later swap SQLite for Neon Postgres + PostGIS (see docs/PERSON_B_PROMPT.md).
Run: pip install fastapi uvicorn numpy scipy ; set SENSOR_KEYS=s1:secret ; uvicorn app:app --port 8000"""
import asyncio, base64, io, json, os, sqlite3, sys, time, urllib.request
from pathlib import Path
import alerts
from fastapi import FastAPI, Header, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from scipy.io import wavfile
import numpy as np
sys.path.insert(0, str(Path(__file__).parents[1] / "core"))
from bluepulse_core import detect_transients, spectral_entropy

DB = os.environ.get("DB_PATH", "bluepulse.db"); PROVIDER = os.environ.get("LLM_PROVIDER", "fake"); HOLD_S = float(os.environ.get("ALERT_HOLD_S", "8"))
KEYS = dict(p.split(":", 1) for p in os.environ.get("SENSOR_KEYS", "s1:secret,malvan-north:secret,sindhudurg-reef:secret,tarkarli-shelf:secret").split(",")); db = sqlite3.connect(DB, check_same_thread=False)
db.executescript("create table if not exists events(id text primary key,sensor text,ts real,label text,probs text,severity text,briefing text,conf real,provider text,lat real,lon real,review text default 'new');"
                 "create table if not exists llm_calls(id integer primary key autoincrement,event_id text,provider text,model_id text,latency_ms int,confidence real,outcome text,ts real);"
                 "create table if not exists alerts(event_id text,channel text,ok int,ts real);create table if not exists heartbeats(sensor text,ts real,indices text);")
app = FastAPI(title="BluePulse API"); app.add_middleware(CORSMiddleware, allow_origins=os.environ.get("CORS_ORIGINS", "*").split(","), allow_methods=["*"], allow_headers=["*"])
subs: list[asyncio.Queue] = []

def parse_nugen(raw):
    """Handles BOTH plain JSON and the SSE stream your endpoint returns. Returns (text, mean_confidence, min_confidence)."""
    raw = raw.strip()
    if not raw.startswith("data:"):
        d = json.loads(raw); c = d.get("confidence_score"); return d["choices"][0]["message"]["content"], c, c
    text, conf = [], []
    for line in raw.splitlines():
        if not line.startswith("data:"): continue
        p = line[5:].strip()
        if p == "[DONE]": break
        try: d = json.loads(p)
        except ValueError: continue
        if d.get("object") == "confidence": conf.append(float(d["confidence_score"]))
        for ch in d.get("choices", []): text.append((ch.get("delta") or {}).get("content") or "")
    return "".join(text).strip(), (round(sum(conf)/len(conf), 1) if conf else None), (min(conf) if conf else None)

def classify(e):
    """Heuristic stand-in. Replace with the ONNX AST model (ml/export_onnx.py output) behind this same function signature."""
    sr, x = wavfile.read(io.BytesIO(base64.b64decode(e["clip"]["bytes_b64"]))); x = x.astype(np.float32) / 32768
    if detect_transients(x, sr): return "blast", {"blast": .9, "vessel": .05, "biology": .02, "environmental_noise": .02, "ambient": .01}
    return ("environmental_noise", {"environmental_noise": .6, "ambient": .4}) if spectral_entropy(x) > .8 else ("vessel", {"vessel": .6, "ambient": .4})

SYS = 'Reply ONLY in this format, max 60 words: "Briefing: <what was heard and where>. Recommended action: <one step>. Uncertainty: <main doubt>." Never thank the reader or add greetings.'
def template(label, p, sensor): return f"Template alert: {label} detected at {sensor} (p={p:.2f}). AI briefing pending. Verify before dispatch."

def llm_briefing(label, probs, sensor):
    """Returns (text, confidence_score|None, model_id). Never raises; never blocks longer than HOLD_S."""
    prompt = f"Event: class={label} p={max(probs.values())}, sensor={sensor}. Write a ranger briefing."
    if PROVIDER == "nugen":
        body = json.dumps({"model": os.environ["NUGEN_MODEL_ID"], "stream": False, "messages": [{"role": "system", "content": SYS}, {"role": "user", "content": prompt}], "max_tokens": 120, "temperature": 0.2}).encode()
        r = urllib.request.Request(os.environ.get("NUGEN_BASE_URL", "https://api.nugen.in/api/v3/inference") + "/chat/completions", body,
                                   {"Authorization": "Bearer " + os.environ["NUGEN_API_KEY"], "Content-Type": "application/json"})
        text, mean_c, _min = parse_nugen(urllib.request.urlopen(r, timeout=HOLD_S).read().decode()); return text, mean_c, os.environ["NUGEN_MODEL_ID"]
    return f"Briefing (fake LLM): {label} at {sensor}. Verify before acting.", 50.0, "fake"

def severity(label, conf): return "critical" if label == "blast" and (conf or 0) >= 80 else "high" if label == "blast" else "low"

@app.get("/healthz")
def healthz(): return {"ok": True}
@app.get("/v1/system/info")
def info(): return {"llm_provider": PROVIDER, "model_id": os.environ.get("NUGEN_MODEL_ID"), "nugen_active": PROVIDER == "nugen"}

@app.post("/v1/ingest/events")
async def ingest(e: dict, x_sensor_key: str = Header(None)):
    if KEYS.get(e.get("sensor_id")) != x_sensor_key: raise HTTPException(401, "bad sensor key")
    label, probs = classify(e); t0 = time.time(); outcome = "ok"
    try: text, conf, model = await asyncio.wait_for(asyncio.to_thread(llm_briefing, label, probs, e["sensor_id"]), HOLD_S)
    except Exception: text, conf, model, outcome = template(label, max(probs.values()), e["sensor_id"]), None, None, "fallback"   # LLM adds, never blocks the alert
    pos = e.get("sensor_position", {}); sev = severity(label, conf)
    db.execute("insert or ignore into events(id,sensor,ts,label,probs,severity,briefing,conf,provider,lat,lon) values(?,?,?,?,?,?,?,?,?,?,?)",
               (e["event_id"], e["sensor_id"], e["started_at"], label, json.dumps(probs), sev, text, conf, PROVIDER, pos.get("lat"), pos.get("lon")))
    db.execute("insert into llm_calls(event_id,provider,model_id,latency_ms,confidence,outcome,ts) values(?,?,?,?,?,?,?)", (e["event_id"], PROVIDER, model, int((time.time()-t0)*1000), conf, outcome, time.time())); db.commit()
    out = {"event_id": e["event_id"], "label": label, "severity": sev, "briefing": text, "confidence_score": conf, "provider": PROVIDER, "lat": pos.get("lat"), "lon": pos.get("lon")}
    for q in subs: q.put_nowait(out)
    if outcome == "ok" or sev in ("critical", "high"):
        async def _send():
            for ch, ok in await asyncio.to_thread(alerts.dispatch, {**out, "sensor": e["sensor_id"]}): db.execute("insert into alerts values(?,?,?,?)", (e["event_id"], ch, int(ok), time.time())); db.commit()
        asyncio.create_task(_send())
    return out

@app.post("/v1/ingest/heartbeat")
def heartbeat(h: dict, x_sensor_key: str = Header(None)):
    if KEYS.get(h.get("sensor_id")) != x_sensor_key: raise HTTPException(401, "bad sensor key")
    db.execute("insert into heartbeats values(?,?,?)", (h["sensor_id"], h["ts"], json.dumps(h["indices"]))); db.commit(); return {"ok": True}

@app.get("/v1/events")
def events(limit: int = 50):
    cols = ["id", "sensor", "ts", "label", "severity", "briefing", "conf", "provider", "lat", "lon", "review"]
    return [dict(zip(cols, r)) for r in db.execute(f"select {','.join(cols)} from events order by ts desc limit ?", (limit,))]
@app.get("/v1/provenance")
def provenance(limit: int = 100):
    return [dict(zip(["event_id", "provider", "model_id", "latency_ms", "confidence", "outcome"], r)) for r in db.execute("select event_id,provider,model_id,latency_ms,confidence,outcome from llm_calls order by id desc limit ?", (limit,))]
@app.get("/v1/heartbeats")
def heartbeats(limit: int = 200):
    return [{"sensor": s, "ts": t, "indices": json.loads(i)} for s, t, i in db.execute("select sensor,ts,indices from heartbeats order by ts desc limit ?", (limit,))]
@app.post("/v1/events/{eid}/review")
def review(eid: str, body: dict): db.execute("update events set review=? where id=?", (body.get("review", "confirmed"), eid)); db.commit(); return {"ok": True}

@app.get("/v1/stream")
async def stream(request: Request):
    q: asyncio.Queue = asyncio.Queue(); subs.append(q)
    async def gen():
        try:
            while not await request.is_disconnected():
                try: yield f"data: {json.dumps(await asyncio.wait_for(q.get(), 15))}\n\n"
                except asyncio.TimeoutError: yield ": keepalive\n\n"
        finally: subs.remove(q)
    return StreamingResponse(gen(), media_type="text/event-stream")
