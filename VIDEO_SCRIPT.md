# BluePulse --- Video Demonstration Script

**Event:** PCCOE International Grand Challenge 2026\
**Theme:** AI for Climate Change\
**Project:** BluePulse --- AI-Powered Bioacoustic Monitoring for Marine
Ecosystem Health & Threat Detection\
**Target duration:** 6 minutes 30 seconds\
**Maximum duration:** 8 minutes\
**Speakers:** A (ML, audio processing and Nugen integration); B
(problem, platform, dashboard and deployment)

**Tagline:** *Listening to the Ocean. Protecting What We Cannot See.*

------------------------------------------------------------------------

## Video structure

  -----------------------------------------------------------------------
  Time              Section           Speaker           What to show
  ----------------- ----------------- ----------------- -----------------
  0:00--0:45        The problem       B                 Landing page,
                                                        reef visuals,
                                                        blast-fishing
                                                        visual

  0:45--1:30        Why it matters    A                 Coral reef
                                                        visuals and
                                                        climate
                                                        connection

  1:30--2:30        How BluePulse     A                 Solution and
                    works                               architecture
                                                        slides

  2:30--3:30        Live              B                 Replay script,
                    demonstration                       dashboard, event
                                                        details and
                                                        Telegram

  3:30--4:30        Human review and  A                 Review workflow
                    traceability                        and provenance

  4:30--5:15        AI and Nugen      A                 Nugen model page
                    integration                         and successful
                                                        provenance record

  5:15--6:00        Impact and        B                 Impact, target
                    feasibility                         users and
                                                        deployment slides

  6:00--6:30        Limitations and   Both              Both speakers,
                    closing                             logo and tagline
  -----------------------------------------------------------------------

------------------------------------------------------------------------

# Narration

## 0:00--0:45 --- The problem: What is happening underwater?

**Speaker B**\
**On screen:** Landing page, reef visuals and blast-fishing
illustration.

"Imagine trying to protect a forest when the only way to know what's
happening is to listen to it. Now imagine that forest is underwater.

Coral reefs are home to an enormous variety of marine life. They support
fisheries, protect coastlines and provide habitats for many species.

But one activity can destroy these habitats in seconds: blast fishing.
Explosives are used underwater to kill fish, but they also destroy coral
and harm marine life that was never the target.

The bigger problem is that these incidents happen underwater, often far
from people. Visual monitoring is difficult in dark or murky water,
patrols are expensive, and manual surveys only provide occasional
snapshots.

So how can we continuously monitor what we cannot easily see?

We are Jidnyasa and Sajiree, and this is BluePulse."

## 0:45--1:30 --- Why does it matter for climate change?

**Speaker A**\
**On screen:** Coral reef visuals, blast-fishing illustration and a
verified research statistic if available.

"Why does this matter beyond protecting fish?

Coral reefs support biodiversity, fisheries and coastal communities.
They also act as natural barriers that reduce wave energy along
coastlines.

Climate change is already putting reefs under pressure through rising
ocean temperatures and coral bleaching. When destructive activities such
as blast fishing damage these ecosystems further, they add another
pressure to already vulnerable marine environments.

There is also an opportunity hidden in the sound of the ocean. Healthy
reefs have characteristic soundscapes produced by fish, snapping shrimp
and other marine life.

By monitoring these sounds over time, we can look for changes in
biological activity and build a picture of reef conditions.

BluePulse is designed to address both sides of the problem: detecting
immediate acoustic threats and supporting long-term ecosystem-health
monitoring."

## 1:30--2:30 --- The solution: How does BluePulse work?

**Speaker A**\
**On screen:** Proposed Solution and Tech Stack & Architecture slides.
Highlight each stage as it is explained.

"BluePulse is an AI-powered underwater acoustic monitoring system.

Think of it as a security monitoring system, but instead of cameras, it
uses underwater microphones called hydrophones.

Here is the process.

**First, we listen.** Hydrophones capture underwater sounds, including
marine-life activity, vessels, machinery and unusual disturbances.

**Next, we filter.** Our audio-processing pipeline uses PCEN to reduce
background noise, such as waves and rain, and make important sound
patterns easier to analyse.

**Then, we detect.** Mel-spectrograms represent audio as visual
frequency patterns, which our audio-classification pipeline analyses to
identify sound categories such as vessels and possible blasts.

**Next, we interpret and alert.** A detection is converted into useful
event information. Our Nugen-integrated language-model component is
intended to turn technical detection output into a short briefing that a
ranger can understand.

Finally, the platform displays events on a GIS dashboard and can send
alerts to conservation teams.

BluePulse also has a second purpose. By building baseline reef
soundscapes and tracking biological activity over time, it can support
long-term monitoring of ecosystem health.

In one system, we bring together threat detection and reef soundscape
diagnostics."

> **Implementation accuracy note:** Only describe PCEN, Mel-spectrograms
> and AST as active in the demonstrated pipeline if they are actually
> running in the submitted build. If AST is not trained or integrated,
> say: "The architecture includes an AST-based classification pipeline;
> the current demonstration uses the classifier implemented in this
> build." Do not imply an unimplemented component is operational.

## 2:30--3:30 --- Live demonstration: From sound event to alert

**Speaker B**\
**On screen:** Terminal, then BluePulse dashboard.

"Let's see how this works.

We are replaying four labelled demonstration events: two simulated blast
events, one vessel and one environmental-noise event. These are
demonstration inputs, not live recordings from the ocean."

**Action:** Run the demo replay script.

``` bash
python scripts/demo_replay.py http://127.0.0.1:8000 secret
```

**Continue narration:**

"Each event is sent to the backend with its own unique ID.

Now let's move to the dashboard.

Here, we can see the incoming events, their classifications, severity
levels and mapped sensor locations.

Let's open the first possible blast event.

The event details help a ranger understand what the system detected and
where it was recorded. The briefing is designed to make the result
easier to interpret without requiring the ranger to analyse raw audio or
model output.

Now let's look at the vessel event.

A vessel sound is not automatically illegal activity. It may simply be
normal boat movement. This is why classification, uncertainty and human
review matter. We do not want every unusual sound to become an
accusation.

The platform can also send notifications through Telegram, so
conservation teams can receive important event information without
continuously watching the dashboard."

**Action:** Show a Telegram alert if the integration is working. If it
is not working, do not claim that a live alert was delivered; show the
implemented interface or explain that it is part of the planned
workflow.

## 3:30--4:30 --- Human oversight and traceability

**Speaker A**\
**On screen:** Review interface, event details and provenance table.

"Underwater environments are unpredictable. A vessel engine, a natural
acoustic event or recording interference may sometimes resemble a
suspicious sound.

That is why BluePulse is designed to assist rangers, not replace their
judgement.

Events can be reviewed by a human operator. Reviewers can confirm or
reject detections, and verified feedback can help improve the system as
more labelled data becomes available.

We also maintain event provenance. This means we can trace which AI
provider processed an event, which model was used, how long the request
took and whether the inference succeeded.

For a conservation system, traceability matters. We need to understand
not only what the system reported, but also how that result was
produced.

The goal is to give conservation teams useful information while keeping
final decisions with people."

## 4:30--5:15 --- AI innovation and Nugen integration

**Speaker A**\
**On screen:** Nugen model page, verified model configuration, credits
and successful provenance record.

"Let's look more closely at the language-model component.

BluePulse integrates Nugen to bring language-model capabilities into the
event-interpretation workflow.

A sound classifier may return a technical label such as 'blast' with a
probability. But a ranger needs something more useful: a concise
explanation of what was detected, the uncertainty involved and what
should be checked next.

The language-model component is designed to turn detection information
into that kind of briefing.

We also record the provider, model identifier, latency and inference
outcome for each request. This lets us verify which model was used and
whether the request succeeded.

Here is the model configuration and an example of the integration."

> **Before recording:** Show a successful Nugen inference and a
> provenance entry with `provider=nugen`, the actual model ID and
> `outcome=ok`. Do not present a fallback template as a model-generated
> briefing. Only mention the model architecture, training corpus,
> alignment process or credits if those details are visible and verified
> on the Nugen platform.

## 5:15--6:00 --- Impact, feasibility and deployment

**Speaker B**\
**On screen:** Impact & Benefits, Target Users, Challenges, Feasibility
and Deployment slides.

"BluePulse is designed for practical use by marine authorities,
marine-protected-area managers, conservation organisations, researchers
and coastal communities.

It can work with existing hydrophones and autonomous recording
equipment, reducing the need to build an entirely new monitoring
network.

Our architecture combines edge processing, a FastAPI backend and a
GIS-based dashboard. Edge processing can reduce the amount of raw audio
that needs to be transmitted, while the dashboard helps teams view
events and sensor information.

The intended benefits are earlier identification of possible destructive
activity, more informed use of patrol resources and continuous acoustic
records that can support reef-health research.

Deployment can begin with a pilot in a marine-protected area, followed
by additional hydrophone nodes, edge-to-cloud event transmission and a
command-centre dashboard.

We would measure detection performance, false alarms, alert latency,
operating costs and changes in acoustic indicators during field pilots.
These are targets for validation, not results we are claiming today."

## 6:00--6:30 --- Limitations and closing

**Both speakers**\
**On screen:** Both speakers appear on camera, followed by BluePulse
logo and tagline.

**Speaker A:**

"BluePulse has limitations. Underwater sounds can be ambiguous, models
need validation with more real-world recordings, and a single sensor
cannot precisely locate an incident."

**Speaker B:**

"Our next steps are field testing, expanding verified acoustic datasets,
improving multi-sensor localisation and making alerts accessible in
regional languages."

**Both:**

"Because protecting marine ecosystems starts with understanding what is
happening beneath the surface.

BluePulse --- Listening to the Ocean. Protecting What We Cannot See.

Thank you."

------------------------------------------------------------------------

# What to show for each judging criterion

  -----------------------------------------------------------------------
  Judging criterion                   Evidence to show
  ----------------------------------- -----------------------------------
  **1. Problem relevance**            Blast-fishing problem, limitations
                                      of visual monitoring and patrols,
                                      climate and biodiversity connection

  **2. AI innovation**                Hydrophone-to-AI pipeline, noise
                                      processing, audio classification,
                                      Nugen briefing workflow and human
                                      review

  **3. Implementation and clarity**   Architecture, live event replay,
                                      dashboard, event details, review
                                      flow and provenance

  **4. Impact and feasibility**       Target users, existing-hydrophone
                                      compatibility, edge processing,
                                      deployment phases and measurable
                                      pilot outcomes

  **5. Evidence and presentation**    Working demo, successful Nugen
                                      inference evidence, provenance,
                                      clear narration and honest
                                      limitations
  -----------------------------------------------------------------------

------------------------------------------------------------------------

# Pre-recording checklist

## Backend and AI

-   [ ] Backend is running and `/healthz` responds.
-   [ ] `/v1/system/info` reports `llm_provider=nugen`.
-   [ ] Nugen API key and model ID are loaded from the shared `.env`.
-   [ ] Generate a fresh event and verify that provenance reports
    `provider=nugen`.
-   [ ] Verify at least one successful inference with `outcome=ok` and
    the actual model ID.
-   [ ] Ensure the briefing shown in the dashboard is genuinely
    generated by Nugen, not a fallback template.
-   [ ] Keep API keys and other secrets hidden from the recording.

## Live demonstration

-   [ ] Run the demo replay once before recording.
-   [ ] Confirm the expected sensor IDs are accepted.
-   [ ] Check that the dashboard displays the new events.
-   [ ] Confirm event details and review controls work.
-   [ ] Confirm Telegram notifications work before promising to show
    one.
-   [ ] Prepare a clean backup recording in case the live demo fails.
-   [ ] Clearly identify replayed or synthetic events as demonstration
    data.

## Presentation and recording

-   [ ] Both speakers appear on camera at least once.
-   [ ] Record at 1080p with clear audio.
-   [ ] Close notifications and unrelated browser tabs.
-   [ ] Keep the architecture diagram readable.
-   [ ] Show the relevant PPT slides at the planned timestamps.
-   [ ] Rehearse with a timer and keep the final video below 7:30.
-   [ ] Upload as an unlisted YouTube video or shareable Drive link.

------------------------------------------------------------------------

# Backup demo shot list

If the live demo fails, use a clean screen recording with voice-over.

1.  Show the backend starting and the system-info response.
2.  Show the demo replay command and clearly label the events as
    simulated.
3.  Show the resulting event cards on the dashboard.
4.  Open a possible blast event and show its details.
5.  Open a vessel event and explain why human review matters.
6.  Show the Telegram alert only if a genuine notification was received.
7.  Show a successful Nugen provenance entry. Do not use a fallback
    event as evidence of successful Nugen inference.
8.  End with the BluePulse dashboard and project tagline.

------------------------------------------------------------------------

# Claims and evidence to verify before recording

-   **Research statistic:** If using the "one incident every 62 minutes"
    statistic, show the original paper and verify the exact wording,
    study location, recording duration and incident count.
-   **Classifier status:** Clearly distinguish a trained and integrated
    classifier from a prototype or stand-in.
-   **Nugen integration:** Show successful inference, not just provider
    configuration or an HTTP 200 response.
-   **Confidence:** Do not describe an LLM-generated confidence value as
    calibrated model confidence unless it has been validated.
-   **Location:** A single hydrophone provides a sensor-associated
    location, not precise incident localisation.
-   **Continuous monitoring:** Distinguish the intended 24/7 hydrophone
    monitoring design from what the current demo actually demonstrates.
-   **Performance:** Do not quote accuracy, precision, false-positive
    rates or real-time latency without measured results.
-   **Impact:** Describe environmental benefits as intended outcomes
    until validated through field deployment.

**Final message:** BluePulse listens to underwater soundscapes,
identifies potential threats, turns detections into understandable
information and supports long-term marine ecosystem monitoring.
