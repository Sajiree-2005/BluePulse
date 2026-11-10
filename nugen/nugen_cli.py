"""Nugen helper. Setup: pip install requests ; PowerShell: $env:NUGEN_API_KEY="..."
Commands: models | upload | align NAME BASE_MODEL_ID DOC_ID,DOC_ID | status ALIGNMENT_ID | deploy MODEL_ID | dstatus MODEL_ID | ask MODEL_ID "text"
Paths follow docs.nugen.in; if a field differs see https://api.nugen.in/openapi-public.json"""
import glob, json, os, sys, requests
B = "https://api.nugen.in"; H = {"Authorization": f"Bearer {os.environ['NUGEN_API_KEY']}"}
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
    body = {"model": a[1], "messages": [{"role": "user", "content": a[2]}], "max_tokens": 300, "temperature": 0.2}
    body["stream"] = False
    r = requests.post(f"{B}/api/v3/inference/chat/completions", headers=J, json=body); print(r.status_code)
    sys.path.insert(0, "../backend"); from app import parse_nugen
    t, mean_c, min_c = parse_nugen(r.text); print(t); print(f"confidence mean={mean_c} min={min_c}")
else: sys.exit(__doc__)
