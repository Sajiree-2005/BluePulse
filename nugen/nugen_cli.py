"""Nugen helper. Setup: pip install requests ; PowerShell: $env:NUGEN_API_KEY="..."
Commands: models | upload | align NAME BASE_MODEL_ID DOC_ID,DOC_ID | status ALIGNMENT_ID | deploy MODEL_ID | dstatus MODEL_ID | ask MODEL_ID "text"
Paths follow docs.nugen.in; if a field differs see https://api.nugen.in/openapi-public.json"""
import glob
import json
import os
import sys
import requests

from pathlib import Path
from dotenv import load_dotenv

# Load the shared BluePulse root .env file
ROOT = Path(__file__).resolve().parents[1]
load_dotenv(ROOT / ".env", override=True)

B = "https://api.nugen.in"

API_KEY = os.getenv("NUGEN_API_KEY")
MODEL_ID = os.getenv("NUGEN_MODEL_ID")
INFERENCE_URL = (
    os.getenv(
        "NUGEN_BASE_URL",
        f"{B}/api/v3/inference"
    ).rstrip("/") + "/chat/completions"
)

if not API_KEY:
    sys.exit("ERROR: NUGEN_API_KEY not found in BluePulse/.env")

H = {"Authorization": f"Bearer {API_KEY}"}
J = {**H, "Content-Type": "application/json"}
def show(r):
    print(r.status_code)
    try: print(json.dumps(r.json(), indent=2))
    except Exception: print(r.text)
a = sys.argv[1:]
if not a: sys.exit(__doc__)
if a[0] == "models": show(requests.get(f"{B}/api/v3/models/base", headers=H))
elif a[0] == "upload":
    fs = [("files", (os.path.basename(p), open(p, "rb"), "text/plain")) for p in sorted(glob.glob("corpus/*.txt"))]
    show(requests.post(f"{B}/api/v3/documents/create", headers=H, files=fs))
elif a[0] == "align":
    body = {"alignment_name": a[1], "base_model_id": a[2], "document_ids": a[3].split(","), "description": "BluePulse marine bioacoustics"}
    show(requests.post(f"{B}/api/v3/alignment-projects/create", headers=J, json=body))
elif a[0] == "status": show(requests.get(f"{B}/api/v3/alignment-projects/{a[1]}/status", headers=H))
elif a[0] == "deploy": show(requests.post(f"{B}/api/v3/models/{a[1]}/deployment", headers=H))
elif a[0] == "dstatus": show(requests.get(f"{B}/api/v3/models/{a[1]}/deployment/status", headers=H))
elif a[0] == "ask":
    if len(a) < 3:
        sys.exit('Usage: python nugen_cli.py ask MODEL_ID "Your prompt"')

    model = a[1] or MODEL_ID

    body = {
        "model": model,
        "messages": [
            {"role": "user", "content": a[2]}
        ],
        "max_tokens": 300,
        "temperature": 0.2,
        "stream": False
    }

    try:
        r = requests.post(
            INFERENCE_URL,
            headers=J,
            json=body,
            timeout=60
        )

        print("HTTP Status:", r.status_code)
        r.raise_for_status()

        sys.path.insert(0, str(ROOT / "backend"))
        from app import parse_nugen

        t, mean_c, min_c = parse_nugen(r.text)

        print("Provider: nugen")
        print("Model:", model)
        print("Briefing:", t)
        print(f"Confidence mean={mean_c}, min={min_c}")

    except requests.RequestException as ex:
        print("NUGEN API ERROR:", ex)
        if getattr(ex, "response", None) is not None:
            print("Response:", ex.response.text)

    except Exception as ex:
        print("NUGEN RESPONSE ERROR:", type(ex).__name__, ex)
else: sys.exit(__doc__)
