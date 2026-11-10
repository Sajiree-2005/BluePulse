"""Generates varied training pairs (pairs.jsonl) and a disjoint hold-out benchmark (benchmark.jsonl). python make_pairs.py"""
import json, random, pathlib
root = pathlib.Path(__file__).parent
def conf_word(p): return "high" if p >= .85 else "moderate" if p >= .6 else "low"
def make(rng, sensors, n):
    out = []
    for _ in range(n):
        s = rng.choice(sensors); k = rng.choice(["blast", "blast", "vessel", "biology", "noise", "lookalike"]); p = round(rng.uniform(.5, .98), 2); cw = conf_word(p)
        ns = rng.choice([1, 2, 3, 4]); on = rng.choice([6, 9, 14, 20, 45, 120])
        if k == "blast":
            q = f"Event: class=blast p={p}, sensor={s}, onset={on} ms, heard on {ns} sensor(s). Write a ranger briefing."
            act = "Dispatch a patrol to the estimated area and preserve the clip." if cw != "low" and on < 30 else "Send to a duty officer for review before any dispatch."
            a = f"Briefing: A sharp broadband event with a {on} ms onset was heard on {ns} sensor(s) near {s}, consistent with blast fishing. Confidence is {cw} ({p}). {act} Limits: one sensor gives an area, not a point, and a boat engine misfire cannot be fully excluded."
        elif k == "vessel":
            q = f"Event: class=vessel p={p}, sensor={s}, smooth level rise, harmonic lines. Write a ranger briefing."
            a = f"Briefing: A vessel with a steady engine tone passed {s}. Confidence is {cw} ({p}). Urgency is low unless it is inside a closed zone or coincides with a blast. {'Flag for human review.' if cw != 'high' else 'No action needed beyond logging.'}"
        elif k == "biology":
            d = rng.choice([-30, -15, 5, 18, 25]); q = f"Event: dusk chorus at {s} is {d:+d}% versus this site's baseline. Summarise for a reef manager."
            a = f"Summary: Biological sound at {s} is {abs(d)}% {'below' if d < 0 else 'above'} this site's own baseline. " + ("This is a possible decline signal, not a diagnosis. Check weather, boats and recorder changes, and watch the trend for several days." if d < -10 else "This looks normal or healthy for the site. No action is needed.")
        elif k == "noise":
            q = f"Event: class=environmental_noise p={p}, sensor={s}, rain-like broadband hiss. What should happen?"
            a = f"Briefing: Weather-like broadband noise at {s}. Confidence is {cw} ({p}). No alert is needed. Keep the data as context for later detections."
        else:
            q = f"Event: sharp isolated bang at {s} inside a steady engine tone, class=blast p={p}. Write a ranger briefing."
            a = f"Briefing: A sudden bang was heard at {s} while an engine tone was present. This may be an engine misfire rather than an explosion. Confidence is reduced. Mark as needs human review and listen to the clip for a bubble-pulse tail before dispatching."
        out.append({"instruction": q, "response": a})
    return out
sens_a = ["Malvan North", "Sindhudurg Reef", "Tarkarli Shelf", "Devbag Point", "Vengurla Rocks", "Achara Bay"]
sens_b = ["Gulf of Mannar 4", "Havelock East", "Netrani South", "Lakshadweep 2"]
tr = make(random.Random(1), sens_a, 320); bm = make(random.Random(2), sens_b, 100)
tr += [json.loads(l) for l in open(root / "pairs_seed.jsonl")] if (root / "pairs_seed.jsonl").exists() else []
with open(root / "pairs.jsonl", "w") as f: [f.write(json.dumps(x) + "\n") for x in tr]
with open(root / "benchmark.jsonl", "w") as f: [f.write(json.dumps(x) + "\n") for x in bm]
print(len(tr), "train pairs;", len(bm), "benchmark pairs (different sensors, different seed)")
