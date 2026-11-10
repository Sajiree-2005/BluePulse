# Video demo script: BluePulse (target 6:30, limit 3-8 min) 
**Theme:** AI for Climate Change. **Speakers:** A = Person A (ML + Nugen), B = Person B (platform). Both appear on camera at least once.
Record screen + voice (OBS or Xbox Game Bar `Win+G`), 1080p, quiet room, upload as unlisted YouTube or Drive link.

## Timeline mapped to the five judging criteria
| Time | Criterion | Speaker | On screen |
|---|---|---|---|
| 0:00-0:45 | 1 Problem relevance | B | Landing page hero, dive scroll to the "1 / 62 min" stat |
| 0:45-1:30 | 1 Problem relevance | A | Slide or page: reef, blast fishing, why it matters for climate resilience |
| 1:30-2:30 | 2 AI innovation | A | Architecture diagram (README), spectrogram section |
| 2:30-4:30 | 3 Implementation + clarity | A + B | **Live demo**: run `demo_replay.py`, dashboard, briefing, confidence gate, Telegram, provenance |
| 4:30-5:15 | 3 + 5 Evidence | A | Nugen platform: aligned model page, credits, provenance table |
| 5:15-6:00 | 4 Impact + feasibility | B | Cost table, free-tier stack, Render deploy, limits |
| 6:00-6:30 | 5 Close | Both | Honest limits, next steps, call to action |

## Narration (read naturally, do not memorise word for word)
**0:00 B (hero, scroll down):** "Coral reefs protect coasts, feed millions of people and support huge biodiversity, and they are already under heat stress from climate change. Blast fishing destroys what is left, in seconds. A 2026 study in Indonesia's Spermonde Archipelago verified 3,567 bomb-fishing incidents in more than 3,650 hours of audio, about one every 62 minutes, detected from a low-cost recorder out to almost 17 kilometres. [source: Williams et al. 2026, Remote Sensing in Ecology and Conservation, DOI 10.1002/rse2.70093; show it on screen]. The problem is not that we cannot hear it. It is that nobody can listen, 24 hours a day, and respond in time. We are Jidnyasa and Sajiree, and this is BluePulse."

**0:45 A (reef slide):** "Healthy reefs are loud: snapping shrimp, fish choruses at dusk. Blasts break coral and silence the animals that make that sound. So the same hydrophone gives us two things: a threat alarm today, and a reef health trend over months. Protecting reefs now keeps them resilient as oceans warm. [add one cited statistic on reef value]."

**1:30 A (architecture):** "Here is the system. An edge agent next to any existing recorder removes ocean noise with PCEN and flags sudden sounds, so we send events, not hours of audio. The cloud classifies each sound. Then comes our key idea: a language model aligned with Nugen on marine acoustics documents turns that detection into a ranger briefing, and returns a confidence score. We use it as a router: high confidence dispatches, medium goes to a human, low sends a template alert. The model can add information to an alert, but it can never suppress one."
[If the AST model is trained, add: "Sounds are classified by an Audio Spectrogram Transformer fine-tuned on real recordings plus clearly labelled synthetic blasts." If not trained, say: "The classifier here is a transparent stand-in; the AST training pipeline is in the repo."]

**2:30 B (live demo, terminal then dashboard):** "I will replay a realistic scenario: two blasts, a boat, and rain." Run `python scripts/demo_replay.py <API> <key>`. "The edge sends each event with a unique id, so retries never duplicate. On the dashboard the first blast appears on the map." Click it. "Briefing, recommended action, uncertainty, and the confidence score from the Nugen model. This one is routed to *[read the gate label shown]*." Click the vessel. "Boat engines are not violations, so this is low priority." Show Telegram phone message with the map pin.

**3:30 A:** "Why a human stays in the loop: a boat engine misfire can look like a blast. Our alerts say what was heard and how sure we are, never who is guilty. Reviewers can confirm or reject, and those labels become training data." Click review button if wired, otherwise show `/docs`.

**4:30 A (Nugen evidence):** "Every call is logged. Here is the provenance table: provider *nugen*, our model id, latency, confidence. And here on Nugen's platform is the aligned model, based on Qwen2.5-1.5B, trained on our 13-document corpus." Show platform + credit usage. "This is how we know the prize requirement is met: real events, served by the aligned model."

**5:15 B (feasibility):** "It is deployable today at zero recurring cost: React and FastAPI on Render, Neon for Postgres, Telegram for alerts, Colab for training. Sensors can be existing recorders; the ZSL study used 150-dollar units. Rangers need only a phone. To scale: more sensors, time-synchronised for position fixes, and a paid always-on instance. Impact we target: faster response to blasts and a measured reef recovery trend. We will report these as measured results after pilots, not as promises."

**6:00 Both:** "Honest limits: one sensor gives an area, not a point; reef scores are relative to each site; our model needs more real blast data; the free tier sleeps. Next: field pilot with a marine park, more sensors, Marathi and Hindi alerts. BluePulse: hear the reef before it breaks. Thank you."

## What judges look for in each criterion (checklist)
- [ ] **1 Problem:** one cited statistic, link to climate (reef resilience, coastal protection), who is affected
- [ ] **2 AI:** domain-aligned LLM + audio model + confidence-gated human review is the innovation; say it in one sentence
- [ ] **3 Implementation:** architecture diagram + a LIVE run (no slides only); mention tests (18 passing) and idempotent edge buffering
- [ ] **4 Impact/feasibility:** cost, deployment, who uses it, what is measured, risks
- [ ] **5 Video/evidence:** screenshots of Nugen model, provenance table, credits, live Telegram alert; clear audio; under 8 min

## Rules for honesty (judges notice)
- Do **not** quote accuracy numbers you have not measured. If the AST model is untrained, say the classifier is a stand-in.
- Do not say "real-time" without a measured latency. Say "seconds" only if you timed it.
- Say which data are synthetic (demo events) and which are real.
- Do not claim position fixes from one sensor.

## Pre-recording checklist
- [ ] Backend awake: open `/healthz` 2 minutes before. Dashboard shows "Live from your backend" and the Nugen chip (green)
- [ ] `LLM_PROVIDER=nugen` (provenance shows `nugen`, not `fake`)
- [ ] Telegram chat open on phone, screen mirrored or filmed
- [ ] Clear old demo data (restart backend) so the first event is the story
- [ ] Rehearse once with a timer; cut anything over 7:30
- [ ] Close notifications and personal tabs; hide API keys on screen (blur the Environment page)

## Shot list for backup (if live demo fails)
Record a clean take of the demo first, then record voice-over on top. Keep the raw recording of the terminal output showing `provider=nugen`.
