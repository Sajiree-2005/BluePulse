# Roadmap status (honest, work package by work package)

Legend: DONE = built and tested here · PARTIAL = works but incomplete · NOT DONE · UNTESTED = code exists, never run

| WP | Item | Status | Notes |
|---|---|---|---|
| 00 | Foundations (accounts, tools, services proven) | PARTIAL | Nugen proven (model deployed, called). Neon, Telegram, Render not yet proven |
| 01 | Contracts | PARTIAL | Event schema is in the roadmap docx (Appendix C), not yet a `/contracts` folder |
| A1 | Nugen corpus + benchmark | PARTIAL | 13 of 15 documents (law + protected areas need official sources); pairs/benchmark are templated |
| A2 | Nugen alignment, evaluation, deploy | PARTIAL | Smoke model deployed; briefing quality weak; full run + benchmark pending; evaluation job failed once |
| A3 | Signal library | DONE | 5 tests |
| A4 | Real audio + AST + ONNX | UNTESTED / NOT DONE | Scripts written; **no real audio in the project**; links in `ml/DATASETS.md`; clip tool tested |
| A5 | Edge agent | DONE | watch + replay modes; no live-stream mode |
| A6 | Reef-health engine | PARTIAL | Maths tested; live indices endpoint; weekly LLM narrative not built |
| A7 | Ask the Reef (RAG) | UNTESTED | `nugen/rag.py` prototype, no UI page |
| A8 | Colab backup LLM | UNTESTED | `ml/backup_llm.py` |
| B1 | Backend skeleton, DB, auth | PARTIAL | FastAPI + SQLite + per-sensor keys. **No user login/JWT, no Postgres/PostGIS, no Alembic** |
| B2 | Ingest, queue, worker | PARTIAL | Idempotent ingest works; no job queue, no inference semaphore, no retention pruning |
| B3 | Nugen client, decisions, alerts, provenance | DONE (alerts mocked) | Telegram/Brevo never sent live by the author |
| B4 | React dashboard | PARTIAL | 5 pages, live data, review actions, provenance. No real map tiles, per-event spectrogram/audio playback, or Ask page |
| X1 | Integration + evaluation | NOT DONE | No real data, so **no measured precision/recall/latency** |
| X2 | Security hardening | NOT DONE | Basic key auth, CORS `*`, no rate limits |
| X3 | Render deployment | UNTESTED | `DEPLOY.md` + `render.yaml` written |
| X4 | Docs + evidence pack | PARTIAL | README, guides, video script done; evidence pack and DATA_CARD pending |

**Automated tests: 18 passing** (core 5, edge 3, backend 8, clip tool 2). Frontend: builds; all five pages server-render without errors; animations not viewed in a browser by the author.
