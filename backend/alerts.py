"""Ranger alerts (free): Telegram message + map pin, Brevo email. Never raises; failures are recorded, never block ingest."""
import json, os, urllib.request

def _post(url, body, headers=None):
    r = urllib.request.Request(url, json.dumps(body).encode(), {"Content-Type": "application/json", **(headers or {})})
    return urllib.request.urlopen(r, timeout=10).read()

def dispatch(ev):
    """ev: dict with label, severity, briefing, confidence_score, sensor_id/sensor, lat, lon. Returns list of (channel, ok)."""
    res = []; sev_ok = ev.get("severity") in ("critical", "high")
    if not sev_ok: return res
    text = f"[{ev['severity'].upper()}] {ev['label']} at {ev.get('sensor', '?')} (AI confidence {ev.get('confidence_score')})\n{ev['briefing']}\nA human must verify before action."
    tok, chats = os.environ.get("TELEGRAM_BOT_TOKEN"), [c for c in os.environ.get("TELEGRAM_CHAT_IDS", "").split(",") if c]
    for c in (chats if tok else []):
        try:
            _post(f"https://api.telegram.org/bot{tok}/sendMessage", {"chat_id": c, "text": text})
            if ev.get("lat") is not None: _post(f"https://api.telegram.org/bot{tok}/sendLocation", {"chat_id": c, "latitude": ev["lat"], "longitude": ev["lon"]})
            res.append(("telegram", True))
        except Exception: res.append(("telegram", False))
    key, to = os.environ.get("BREVO_API_KEY"), os.environ.get("ALERT_EMAIL_TO")
    if key and to:
        try:
            _post("https://api.brevo.com/v3/smtp/email", {"sender": {"email": os.environ.get("ALERT_EMAIL_FROM", to), "name": "BluePulse"}, "to": [{"email": to}],
                  "subject": f"BluePulse {ev['severity']}: {ev['label']} at {ev.get('sensor')}", "textContent": text}, {"api-key": key}); res.append(("email", True))
        except Exception: res.append(("email", False))
    return res
