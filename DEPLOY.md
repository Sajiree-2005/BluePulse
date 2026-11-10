# Deployment guide (Render free tier + Nugen)

**Goal:** a public dashboard URL + a public API URL, with `LLM_PROVIDER=nugen`, plus proof it works.
**Time:** about 45 minutes if the Nugen model is already deployed.

## 0. Before you start
- [ ] `pytest core/tests edge/tests backend/test_app.py` shows **15 passed**
- [ ] You have: GitHub account, Render account, Nugen API key and **model id** (`model_...`), (optional) Telegram bot token + chat id
- [ ] Choose a **sensor key** (any long random string), e.g. generate one in PowerShell: `[guid]::NewGuid().ToString("N")`

## 1. Put the code on GitHub
```powershell
cd C:\dev\bluepulse
git init -b main; git add .; git commit -m "BluePulse"
# create an empty repo on github.com, then:
git remote add origin https://github.com/<you>/bluepulse.git; git push -u origin main
```
Check `git status` shows no `.env`. **Never commit keys.**

## 2. Deploy the backend (Web Service)
Render dashboard > **New > Web Service** > pick the repo.
| Field | Value |
|---|---|
| Root Directory | `backend` |
| Runtime | Python 3 |
| Build Command | `pip install -r requirements.txt` |
| Start Command | `uvicorn app:app --host 0.0.0.0 --port $PORT` |
| Instance type | **Free** |
| Health check path | `/healthz` |

Environment variables (Environment tab):
| Key | Value |
|---|---|
| `PYTHON_VERSION` | `3.12` |
| `LLM_PROVIDER` | `nugen` |
| `NUGEN_API_KEY` | your key |
| `NUGEN_MODEL_ID` | your `model_...` id |
| `SENSOR_KEYS` | `malvan-north:<key>,sindhudurg-reef:<key>,tarkarli-shelf:<key>` |
| `CORS_ORIGINS` | your dashboard URL (step 3), or `*` for now |
| `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_IDS` | optional, for ranger alerts |
| `BREVO_API_KEY`, `ALERT_EMAIL_TO`, `ALERT_EMAIL_FROM` | optional email alerts |

Wait for "Live". Open `https://<api>.onrender.com/healthz` (expect `{"ok":true}`) and `/v1/system/info` (expect `"nugen_active": true`).

## 3. Deploy the dashboard (Static Site)
**New > Static Site** > same repo. Root Directory `frontend`, Build `npm ci && npm run build`, Publish `dist`.
Environment: `VITE_API_URL` = your backend URL (no trailing slash). Add a **Rewrite** rule `/*` -> `/index.html`.
Then set the backend `CORS_ORIGINS` to the dashboard URL.
(`render.yaml` in the repo does both; verify field names at render.com/docs/yaml-spec.)

## 4. Feed it data and prove it works
From your laptop, in the repo root:
```powershell
pip install numpy scipy
python scripts/demo_replay.py https://<api>.onrender.com <key>
```
(use the same `<key>` for every sensor, or edit the script). Expect 4 lines ending `provider=nugen`. Open the dashboard: events on the map, briefings, confidence, and the **Model provenance** table showing `nugen` and your model id. **Screenshot this: it is your evidence.**
First request after idle can take about a minute (free tier wakes up). Run the script twice.

## 5. Real sensors
Edge agent on any PC next to your recorder:
```powershell
$env:PYTHONPATH="core;edge"
python -m bluepulse_edge.agent watch D:\recordings --api https://<api>.onrender.com --key <key> --sensor malvan-north --lat 16.06 --lon 73.46
```
It buffers locally if the cloud is asleep, and never sends an event twice.

## 6. Know the limits (say them out loud in your video)
| Limit | Effect | Fix |
|---|---|---|
| Free service sleeps after 15 min idle | First alert can be ~1 min late | Edge buffer; paid always-on instance (~USD 7/mo) |
| **No persistent disk: SQLite is wiped on restart** | Events disappear after redeploy | Move to Neon Postgres (`docs/PERSON_B_PROMPT.md`) |
| 512 MB RAM, 0.1 CPU | Heavy AST model may be too slow | Keep heuristic/lighter model, or paid instance |
| Classifier is a heuristic stand-in until the AST model is trained | Accuracy claims not allowed | Do `ml/` steps (START_HERE Part 6) and report real metrics |

## 7. Troubleshooting
| Symptom | Cause / fix |
|---|---|
| Dashboard says "Demo data" | `VITE_API_URL` wrong, or backend asleep (wait, refresh) |
| `401 bad sensor key` | key in command differs from `SENSOR_KEYS` |
| `provider=fake` in provenance | `LLM_PROVIDER` not set to `nugen` on Render |
| Outcome `fallback` | Nugen timeout (>8 s), bad key/model id; check `/v1/provenance` |
| CORS error in browser console | set `CORS_ORIGINS` to the dashboard URL |
| Build fails on `numpy` | set `PYTHON_VERSION=3.12` |
