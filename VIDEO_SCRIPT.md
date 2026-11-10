# **BluePulse — Video Demo Script**

**Event:** PCCOE International Grand Challenge 2026  
**Theme:** AI for Climate Change  
**Project:** BluePulse — AI-Powered Bioacoustic Monitoring for Marine Ecosystem Health & Threat Detection  
**Target Duration:** 6 minutes 30 seconds  
**Speaker:** One speaker throughout

---

## **0:00–0:45 \| Opening — Understanding the Problem**

**On screen:** BluePulse title slide, followed by visuals of coral reefs, underwater life and blast fishing.

**Narration:**

Imagine trying to protect a forest without being able to see it. That is one of the challenges of protecting our oceans.

Underwater, destructive activities like blast fishing can destroy coral reefs, kill marine life and disturb entire ecosystems.

But monitoring these areas is difficult. Cameras struggle in dark and murky water, patrols are expensive, and diving surveys only provide information at specific times and locations.

So, how can we continuously monitor what is happening underwater, even when we cannot see it?

That is the problem BluePulse aims to solve.

---

## **0:45–1:30 \| Why Does This Matter?**

**On screen:** Problem, Gaps & Core Need slide. Highlight the four major problems and SDG 13 and SDG 14\.

**Narration:**

Coral reefs support marine biodiversity and help protect coastal communities. However, they are already facing pressure from climate-related changes such as rising ocean temperatures and coral bleaching.

Destructive activities like blast fishing add further stress by damaging reef structures and affecting marine life.

Existing monitoring methods cannot provide continuous coverage across large marine protected areas.

BluePulse addresses this gap by using underwater sound as another source of information.

It supports two important goals: **SDG 13 — Climate Action** and **SDG 14 — Life Below Water**, by helping conservation teams identify potential threats and observe changes in marine ecosystems.

---

## **1:30–2:30 \| Our Solution — How BluePulse Works**

**On screen:** Proposed Solution slide. Show the flow: Hydrophones → Filter → Analyze → Alert. Then display the architecture diagram.

**Narration:**

BluePulse is an AI-powered system that listens to underwater environments using devices called **hydrophones**. A hydrophone works like a microphone, but it records sound underwater.

Here is how our solution works.

**First, Listen.** Hydrophones capture underwater sounds, including marine-life activity, vessels, machinery and possible explosions.

**Second, Filter.** Our audio-processing pipeline uses PCEN to reduce background noise, helping the system focus on useful sound patterns.

**Third, Analyze.** We convert audio into Mel-spectrograms and use our acoustic-classification pipeline to identify different event categories, such as vessel activity and possible blast events.

**Finally, Alert.** Detected events can be displayed on our monitoring dashboard and routed to conservation teams for review.

But BluePulse does more than detect threats. It also aims to establish baseline reef soundscapes and observe changes in biological activity over time.

In simple terms, **one acoustic monitoring system supports both threat detection and long-term reef-health observation.**

---

## **2:30–3:30 \| Live Demonstration — From Sound to Detection**

**On screen:** Open the BluePulse dashboard. Run the prepared demo replay. Show the event list and select an example event.

**Narration:**

Now, let me demonstrate how BluePulse works.

For this demonstration, I am using prepared replay events to show how our platform processes and displays detections. These are sample demo inputs, not live recordings from the ocean.

As the replay runs, events start appearing on our dashboard.

Each event displays relevant information such as its sensor, predicted category and available status or confidence details.

For example, the system can classify an input as a possible blast event, vessel activity or environmental noise.

This allows monitoring teams to identify events that may require attention instead of manually listening through hours of underwater recordings.

The dashboard brings these detections together, making it easier to review what was detected and which monitoring sensor reported it.

---

## **3:30–4:30 \| Responsible Monitoring — Review and Traceability**

**On screen:** Select an event. Show its details, sensor information, status and provenance/log record. Show Telegram only if the integration is working.

**Narration:**

An important part of BluePulse is that an AI detection should not automatically be treated as proof of illegal activity.

Underwater sound can be complex. A strong sound may have multiple possible explanations, and an AI model can make mistakes.

That is why uncertain detections should be reviewed by a human before any enforcement action is taken.

Our system is designed to maintain traceable event records, including the detection details and processing outcome. This helps reviewers understand what the system reported and follow up when necessary.

Where the alert integration is enabled, event information can also be forwarded to the relevant response channel.

Our goal is not to replace marine authorities or conservation teams. It is to help them identify and review potential threats sooner.

---

## **4:30–5:15 \| AI Innovation — What Makes BluePulse Different?**

**On screen:** Innovation & Uniqueness slide. Show the acoustic-processing pipeline and relevant model/configuration screen.

**Narration:**

What makes BluePulse different is that it looks at the underwater soundscape as a whole.

Traditional monitoring often depends on visual observation or periodic surveys. BluePulse uses acoustic sensing, noise-aware processing and AI-based event classification to work even when underwater visibility is poor.

It combines two important capabilities: identifying potentially harmful acoustic events and observing longer-term changes in reef soundscapes.

Our language-model component is intended to convert technical event information into short, understandable briefings for monitoring teams, making the results easier to interpret.

The key innovation is the complete workflow: **from underwater sound to an understandable and reviewable conservation signal.**

---

## **5:15–6:00 \| Feasibility, Impact and Deployment**

**On screen:** Challenges, Feasibility & Deployment slide, followed by Impact & Benefits. Highlight existing hydrophones, edge processing and the three deployment phases.

**Narration:**

BluePulse is designed with practical deployment in mind.

It can work with existing hydrophones and autonomous underwater recorders, reducing the need to build an entirely new sensing network.

Edge processing can filter and analyze audio locally, so the system does not need to continuously transmit large raw audio files over limited ocean connectivity.

Our proposed deployment has three stages.

**Phase one:** A pilot in a marine protected area to collect local soundscape data and establish a baseline.

**Phase two:** Edge and cloud integration, allowing local processing to work alongside remote event monitoring.

**Phase three:** A command-centre dashboard and alert workflow for conservation teams.

The potential benefits include earlier awareness of destructive activities, more continuous monitoring and useful long-term acoustic information for researchers and marine authorities.

A field pilot will be essential to validate detection performance, false alarms, location accuracy and reef-health indicators under real marine conditions.

---

## **6:00–6:30 \| Limitations, Future Scope and Closing**

**On screen:** Future Scope and Conclusion slides. End with the BluePulse logo and tagline.

**Narration:**

Of course, BluePulse also has challenges to address.

Ocean noise can affect detection, more real-world recordings are needed to improve reliability, and sensors must withstand harsh marine conditions.

Our future scope includes improving classification across different marine environments, identifying more marine species and vessel signatures, and developing predictive reef diagnostics.

BluePulse aims to make underwater monitoring more continuous, accessible and actionable.

Because protecting the ocean starts with understanding what is happening beneath the surface.

**BluePulse — Listening to the Ocean. Protecting What We Cannot See.**

---

# **Demo Checklist**

Before recording:

* Open the dashboard and confirm that it loads.  
* Confirm that the replay script runs and events appear.  
* Clearly identify sample or simulated events. Do not present them as live ocean recordings.  
* Verify the event category and sensor details shown on screen.  
* Show confidence values only if the current system actually produces them.  
* Show a Nugen-generated briefing only after confirming that the live request succeeds and the returned text is displayed.  
* If the system displays a fallback template, describe it as a fallback/template, not as a successful Nugen response.  
* Show Telegram or another alert channel only if a test alert is successfully delivered.  
* Show provenance as traceability information, not as proof that every AI component succeeded.  
* Avoid claiming measured accuracy, instant performance, precise GPS localization or validated reef-health diagnosis without supporting test results.  
* Keep the demonstration focused. Avoid spending too much time on code or terminal output.

# **Suggested Slide and Video Timeline**

| Video Time | Presentation Section |
| ----- | ----- |
| 0:00–0:45 | Title — BluePulse |
| 0:45–1:30 | Problem, Gaps & Core Need; SDG Alignment |
| 1:30–2:30 | Proposed Solution; Tech Stack & Architecture |
| 2:30–3:30 | Live Dashboard Demonstration |
| 3:30–4:30 | Event Review, Alert Workflow & Traceability |
| 4:30–5:15 | Innovation & Uniqueness |
| 5:15–6:00 | Challenges, Feasibility & Deployment; Impact & Benefits |
| 6:00–6:30 | Future Scope; Conclusion |

**Recording note:** The presentation describes capabilities such as GPS-tagged alerts, real-time dispatch, AST classification and continuous reef-health diagnostics. Present these as implemented features only where they are demonstrably working. Otherwise, describe them as proposed capabilities, prototype functionality or future deployment goals, as appropriate.

