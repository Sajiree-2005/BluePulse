# Nugen step-by-step (do these in order)

Why: this project must run its inference through a **Nugen-aligned model**. Nugen aligns *text* models on *text documents*, so BluePulse uses the aligned model to write event briefings and confidence scores (AST hears, Nugen reasons).

## 0. Before you spend credits
1. Platform dashboard: write down your credit balance (you had Rs 9,406.53).
2. `pip install requests`. PowerShell: `$env:NUGEN_API_KEY="<key from the API Keys page>"` (never commit it).
3. `cd nugen`, then `python check_corpus.py`. Every .txt must be **500+ words** or the upload fails.

## 1. Upload documents (platform: Manage Documents, or CLI)
`python nugen_cli.py upload` and copy the returned document ids. Plain `.txt` only on the developer edition. Wait until each document is READY.

## 2. Pick the base model
`python nugen_cli.py models`. For the smoke run use the smallest (the docs use `Qwen/Qwen2.5-0.5B-Instruct`). Go larger only after step 4.

## 3. Smoke alignment (cheap)
`python nugen_cli.py align "BluePulse smoke" <base_model_id> <doc_id>` starts as QUEUED. It takes about 30-45 minutes: `python nugen_cli.py status <alignment_id>`.
Platform route: **Domain Alignment > Start New Alignment** (documents, base model, benchmark, start).
**Read your credit balance again.** The difference is your cost per run. Write it down before any further run.

## 4. Deploy and test
`python nugen_cli.py deploy <aligned_model_id>` (5-15 min, check with `dstatus`). Then:
`python nugen_cli.py ask <aligned_model_id> "Event: class=blast p=0.91 onset=14 ms. Write a ranger briefing."`
Look for `confidence_score` in the reply. Also ask 5 off-topic questions (recipes, cricket): scores should be clearly lower.

## 5. Full run
Write the remaining documents (CORPUS_PLAN.md), grow `pairs.jsonl`, prepare a hold-out benchmark (see the Upload Benchmark page on docs.nugen.in for its file format), then repeat step 3 with all document ids. Limits: **10 alignment projects and 10 deployments** per organisation; delete failed ones.

## 6. Wire it in
Set `NUGEN_API_KEY`, `NUGEN_MODEL_ID`, `LLM_PROVIDER=nugen` in Render environment settings. Keep project ids, model id, dates and screenshots of the Domain Alignment page as proof of usage.

## Troubleshooting
- 400 on upload: a file is under 500 words or not plain text.
- 409 on align: you reached 10 projects.
- Slow reply or 504: lower `max_tokens`, retry once, shorten the prompt.
- Credits dropping fast: stop and review your step 3 numbers.
