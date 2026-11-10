"""Ask the Reef (local prototype): chunk corpus, embed with Nugen, cosine search, answer only from passages. UNTESTED against the live API;
confirm the embeddings/rerank request shape on docs.nugen.in (https://api.nugen.in/openapi-public.json) first."""
import glob, os, sys, json, numpy as np, requests
B = "https://api.nugen.in/api/v3/inference"; H = {"Authorization": f"Bearer {os.environ.get('NUGEN_API_KEY','')}", "Content-Type": "application/json"}
def chunk(text, size=300, overlap=50):
    w = text.split(); return [" ".join(w[i:i+size]) for i in range(0, max(1, len(w)-overlap), size-overlap)]
def embed(model, texts): return np.array([d["embedding"] for d in requests.post(f"{B}/embeddings", headers=H, json={"model": model, "input": texts}).json()["data"]])
def ask(model, q, docs="corpus/*.txt", k=4):
    ch = [c for f in sorted(glob.glob(docs)) for c in chunk(open(f, encoding="utf-8").read())]
    E = embed(model, ch); qv = embed(model, [q])[0]; top = np.argsort(-(E @ qv / (np.linalg.norm(E, axis=1) * np.linalg.norm(qv))))[:k]
    ctx = "\n\n".join(ch[i] for i in top)
    r = requests.post(f"{B}/chat/completions", headers=H, json={"model": model, "max_tokens": 300, "temperature": 0.1, "messages": [
        {"role": "user", "content": f"Answer ONLY from the passages. If they do not contain the answer, say 'I do not have enough information'.\n\nPASSAGES:\n{ctx}\n\nQUESTION: {q}"}]}).json()
    return r["choices"][0]["message"]["content"], r.get("confidence_score")
if __name__ == "__main__": print(ask(sys.argv[1], sys.argv[2]))
