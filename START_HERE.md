# BluePulse: what to do, from start to finish (Person 1)

Read **"The one requirement"** first, then follow the steps in order. Tick each box.
Legend: **MUST** = required. **SHOULD** = makes the project much stronger. **OPTIONAL** = only if time allows.

## The one requirement
The project must run its inference through your **Nugen-aligned model**. You already have one deployed (`model_01m6xcgy6n0qk91x`). So the minimum winning path is:
**edge agent sends a sound event -> backend calls your Nugen model -> briefing + confidence appears in the log.**
Everything else makes that path better, more real, or prettier.

## What is in the zip (folder `bluepulse/`)
| Folder | What it is | Tested here? |
|---|---|---|
| `nugen/` | corpus (13 documents), training pairs, benchmark, helper script, Nugen guide | corpus checked; helper partly |
| `backend/` | API that receives events, calls Nugen, logs everything | yes (13 tests) |
| `edge/` | program that listens to WAV files and sends events | yes |
| `core/` | sound-processing code | yes |
| `ml/` | AST training and ONNX export scripts for Colab | NOT run, only syntax-checked |
| `frontend/` | React app: underwater landing page + live dashboard | builds and server-renders OK; animations not viewed by me |

---
## PART 1: Set up your computer (once) [MUST]
1. Install Python 3.12 and Git (Windows PowerShell): `winget install Python.Python.3.12` and `winget install Git.Git`. Close and reopen PowerShell.
2. Unzip to `C:\dev\bluepulse` (any folder is fine). Open PowerShell there: `cd C:\dev\bluepulse`
3. Install packages: `pip install numpy scipy soundfile pytest fastapi uvicorn httpx requests`
4. Run the tests: `pytest core/tests edge/tests backend/test_app.py ml/test_prepare.py`
   **Expected:** "18 passed". If something fails, copy the full message to me.

## PART 2: Nugen, make the model good [MUST]
Where you are: model works but the briefing is generic ("Thank you for your prompt attention") and wrongly says the blast was "14 ms ago". Fix this in order.

**2.1 Write down your credits** (Nugen dashboard). Note the number.

**2.2 Re-test with the updated helper** (in PowerShell, folder `bp\nugen`):
```
$env:NUGEN_API_KEY="paste-your-key"
python nugen_cli.py ask model_01m6xcgy6n0qk91x "Event: class=blast p=0.91, sensor=Malvan North, onset=14 ms, heard on 3 sensors. Write a ranger briefing."
```
It now prints clean text and `confidence mean=... min=...`.

**2.3 Calibrate confidence (this decides your alert rules).** Run 10 blast prompts and 5 off-topic prompts (e.g. "Give me a pasta recipe", "Who won the cricket match?"). Fill a table:

| Prompt type | Mean confidence | Lowest |
|---|---|---|
| 10 blast/vessel/biology prompts | ? | ? |
| 5 off-topic prompts | ? | ? |

Rule of thumb: set **auto-dispatch** a little above the in-domain average, and **needs review** between the off-topic average and that. Write the numbers in `docs/decisions.md`. (My 80/50 were guesses; your 20-value test averaged about 69.)

**2.4 Improve the model: run alignment again.**
1. Nugen > **Manage Documents**: make sure all 13 `.txt` from `nugen/corpus` are there. First run `python check_corpus.py` and `python make_pairs.py` (creates `pairs.jsonl` and `benchmark.jsonl`).
2. Try to upload `pairs.jsonl` as a document too. **I have not confirmed Nugen accepts it.** If it is refused, ask Nugen Support: "How do I include instruction/response pairs (JSONL) in alignment?"
3. **Domain Alignment > Start New Alignment:** select all documents (and the pairs file if accepted), base model **Qwen2.5-1.5B-Instruct**, then at the Benchmark step upload `benchmark.jsonl` if allowed (otherwise let Nugen generate one). Name it `BluePulse v2`. Wait 30-45 min.
4. Check credits again. Write down the cost of this run.
5. **Deploy** the new model (5-15 min). Repeat 2.2 and 2.3 with the new model id and compare. Keep the better one; **undeploy/delete the other** (limit 10).
6. Still bad? Ask Nugen Support for a larger Instant Deploy model, or try `Llama-3.2-3B-Instruct` once (costs more).
7. Turn on **Save Inference Requests** on the model page (evidence).

## PART 3: Run the backend on your laptop [MUST]
```
cd C:\dev\bluepulse\backend
$env:SENSOR_KEYS="s1:secret"
$env:LLM_PROVIDER="nugen"
$env:NUGEN_API_KEY="paste-your-key"
$env:NUGEN_MODEL_ID="model_01m6xcgy6n0qk91x"   # use your newest model id
uvicorn app:app --port 8000
```
Open http://localhost:8000/docs to see the API. Leave this window running. (Use `$env:LLM_PROVIDER="fake"` to test without spending credits.)

## PART 4: Send a real test event through the whole pipeline [MUST]
Open a **second** PowerShell in `C:\dev\bluepulse`:
```
$env:PYTHONPATH="core;edge"
python -c "from bluepulse_core import synth_blast; from scipy.io import wavfile; wavfile.write('test.wav',16000,synth_blast(16000,6,3.0))"
python -m bluepulse_edge.agent replay test.wav --api http://localhost:8000 --key secret --sensor s1 --lat 16.05 --lon 73.46
```
Then open http://localhost:8000/v1/events (the alert with a briefing) and http://localhost:8000/v1/provenance (**must show provider `nugen` and your model id**). Screenshot both. This is your proof.
Note: the backend's classifier is a simple stand-in until you finish Part 6.

## PART 5: Run the React frontend [SHOULD]
```
cd C:\dev\bluepulse\frontend
npm install
copy .env.example .env      # points at http://localhost:8000
npm run dev
```
Open the printed address (usually http://localhost:5173). Scroll to dive; click the water for a sonar ring. With the backend from Part 3 running, the dashboard shows **"Live from your backend"** and your real events; otherwise it shows demo data. Install Node first: `winget install OpenJS.NodeJS.LTS`.

## PART 6: Real audio + the AST model [SHOULD, the biggest remaining job]
I could not download audio from my environment, so you do this part. Everything else is prepared.
1. Open `ml/DATASETS.md`: verified links for blast (BombDetect repo + paper), vessel (ShipsEar, email request for full set), background (NOAA bucket). Start with **a few hundred clips per class**.
2. Email the BombDetect authors if the GitHub repo has no labelled audio (address on the paper page). This is your most valuable data.
3. For each folder you download: `python ml/prepare_clips.py --src <folder> --label vessel --site shipsear` (also `blast`, `ambient`, `biology`, `environmental_noise`). Tested tool.
4. `python ml/build_manifest.py`, then Colab: `ml/train_ast.py` (never run: expect small fixes; paste errors to me), then `ml/export_onnx.py`.
5. Fill `DATA_CARD.md` (source, link, licence, date) and keep real-only test results separate from synthetic-blast results.
6. Test speed with Docker `--cpus=0.1 --memory=512m`; plug the model into `classify()` in `backend/app.py`.

## PART 7: Put it online on Render [SHOULD]
1. Push the folder to a GitHub repository (never commit your API key).
2. Render > **New Web Service** > your repo. Root directory `backend`, build `pip install -r requirements.txt`, start `uvicorn app:app --host 0.0.0.0 --port $PORT`, plan **Free**. Add environment variables from Part 3 (`SENSOR_KEYS`, `LLM_PROVIDER=nugen`, `NUGEN_API_KEY`, `NUGEN_MODEL_ID`). Set `PYTHON_VERSION=3.12`.
3. Render > **New Static Site** > same repo, root `frontend`, build `npm ci && npm run build`, publish `dist`, env var `VITE_API_URL` = your backend URL. (Or use `render.yaml`.)
4. **Warnings:** the backend uses SQLite, and Render's free plan has no persistent disk, so **data is wiped on every restart or sleep**. Fine for a demo; for real use Person B moves it to Neon Postgres (`docs/PERSON_B_PROMPT.md`). The free service sleeps after 15 minutes idle and takes about a minute to wake. I have not tested the Render deploy.
5. Point the edge agent at your Render URL: `--api https://your-app.onrender.com`.

## PART 8: Evidence pack and handoff [MUST before release]
- [ ] Screenshots: Domain Alignment page, your deployed model, credits before/after
- [ ] Provenance output showing `provider: nugen` and your model id (Part 4)
- [ ] Your confidence calibration table (Part 2.3)
- [ ] `DATA_CARD.md` with data sources and licences; honest note on which data are synthetic
- [ ] Give Person B: `backend/`, `docs/PERSON_B_PROMPT.md`, your model id (not the key; share keys privately)
- [ ] Final test recorded with `LLM_PROVIDER=nugen`

## If you only have a little time
Do **Parts 1, 2.2-2.3, 3, 4, 8**. That proves the Nugen path end to end. Then 2.4, then 6.

## Still missing (be honest in your documentation)
Two corpus documents on protected areas and fisheries law (write from official sources, see `nugen/TEMPLATE_marine_protected_areas_and_law.md`), real training data, a dashboard connected to the backend, and a persistent database.


## PART 9: Deploy, demo, video [MUST]
1. Follow `DEPLOY.md`.
2. Run `python scripts/demo_replay.py <API> <key>` to create demo events.
3. Record with `VIDEO_SCRIPT.md` (6:30, mapped to the evaluation criteria). Both of you speak.
