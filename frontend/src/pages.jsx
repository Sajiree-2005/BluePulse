import { useEffect, useMemo, useState } from "react"
import { API, DEMO, getEvents, getInfo } from "./api.js"
import Dashboard from "./components/Dashboard.jsx"; import Provenance from "./components/Provenance.jsx"
const Head = ({ k, t, d }) => <header className="ph"><small>{k}</small><h2>{t}</h2><p className="lead">{d}</p></header>

export function Command() {
  const [ev, setEv] = useState(DEMO)
  useEffect(() => { const l = () => getEvents().then(e => e.length && setEv(e)).catch(() => {}); l(); const t = setInterval(l, 6000); return () => clearInterval(t) }, [])
  const n = k => ev.filter(e => e.label === k).length
  const review = (id, r) => fetch(`${API}/v1/events/${id}/review`, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ review: r }) }).then(() => setEv(v => v.map(e => e.id === id ? { ...e, review: r } : e))).catch(() => {})
  return (<div className="page"><Head k="LIVE OPERATIONS" t="Command center" d="Every detection, with the AI briefing and a clear decision. Humans confirm or reject; those labels become training data." />
    <div className="stats">{[["Events", ev.length], ["Blasts", n("blast")], ["Vessels", n("vessel")], ["Needs review", ev.filter(e => e.conf != null && e.conf < 80).length]].map(([a, b]) => <div className="stat" key={a}><b>{b}</b><span>{a}</span></div>)}</div>
    <Dashboard />
    <h3 className="sub">Event log</h3><div className="tbl"><table><thead><tr><th>Sensor</th><th>Class</th><th>Severity</th><th>AI conf.</th><th>Review</th><th></th></tr></thead>
      <tbody>{ev.slice(0, 12).map(e => <tr key={e.id}><td>{e.sensor}</td><td>{e.label}</td><td>{e.severity}</td><td>{e.conf ?? "-"}</td><td>{e.review || "new"}</td>
        <td className="act"><button onClick={() => review(e.id, "confirmed")}>Confirm</button><button onClick={() => review(e.id, "false_positive")}>False alarm</button></td></tr>)}</tbody></table></div></div>)
}

export function Reef() {
  const [live, setLive] = useState([])
  useEffect(() => { fetch(`${API}/v1/heartbeats`).then(r => r.json()).then(setLive).catch(() => {}) }, [])
  const sim = useMemo(() => Array.from({ length: 21 }, (_, i) => Math.round(94 - (i >= 12 && i <= 15 ? 38 - (i - 12) * 6 : 0) + Math.sin(i * 1.7) * 3)), [])
  const useLive = live.length >= 6; const ser = useLive ? live.slice().reverse().map(h => h.indices.aci ?? 0) : sim
  const mx = Math.max(...ser), mn = Math.min(...ser), pts = ser.map((v, i) => `${(i / (ser.length - 1)) * 600},${150 - ((v - mn) / (mx - mn || 1)) * 130 - 10}`).join(" ")
  return (<div className="page"><Head k="LONG-TERM MONITORING" t="Reef health" d="The same hydrophone also listens to the living reef. We track sound against each site's own baseline, a trend indicator and not a diagnosis." />
    <div className="chart"><svg viewBox="0 0 600 160" preserveAspectRatio="none"><polyline points={pts} fill="none" stroke="#c8ff3d" strokeWidth="3" />{!useLive && <rect x={12 / 20 * 600} y="0" width={3 / 20 * 600} height="160" fill="#ff4d3d" opacity=".18" />}</svg>
      <p className="hint">{useLive ? "Live: acoustic complexity from your sensors' heartbeats." : "SIMULATED 21-day series (activity score 0-100) with an injected drop. Live heartbeats will replace it when 6+ arrive."}</p></div>
    <div className="cols"><div className="card"><h3>Activity score</h3>100 = sounds like this site's normal for the hour. Drops in biological sound cost more than rises.</div>
      <div className="card"><h3>Indices</h3>Acoustic complexity (ACI), spectral entropy, low-band fish and high-band shrimp energy.</div>
      <div className="card"><h3>Read with care</h3>Check weather, boats and recorder changes first. Only a long, persistent deviation matters.</div></div></div>)
}

export function Evidence() {
  const [info, setInfo] = useState(null); useEffect(() => { getInfo().then(setInfo).catch(() => {}) }, [])
  const ok = info?.nugen_active
  return (<div className="page"><Head k="TRUST AND PROOF" t="Model evidence" d="Every AI call is logged. This page proves which model served each event." />
    <div className="stats"><div className="stat"><b style={{ color: ok ? "#c8ff3d" : "#ff4d3d" }}>{ok ? "NUGEN" : info ? info.llm_provider : "offline"}</b><span>Active provider</span></div><div className="stat"><b className="sm">{info?.model_id || "-"}</b><span>Aligned model id</span></div></div>
    <Provenance />
    <h3 className="sub">Safety rules built in</h3><div className="cols"><div className="card"><h3>Adds, never removes</h3>The language model cannot suppress or downgrade a blast alert.</div><div className="card"><h3>8-second rule</h3>If the model is slow, a template alert goes out first.</div><div className="card"><h3>Human in the loop</h3>Medium and low confidence go to a reviewer. Alerts never name a culprit.</div></div></div>)
}

export function How() {
  const S = [["1", "Listen", "Edge agent beside any recorder. PCEN removes steady ocean noise; a transient detector flags candidates."], ["2", "Classify", "Blast, vessel, biology or noise, with probabilities."], ["3", "Explain", "A Nugen-aligned model writes the briefing and a confidence score."], ["4", "Decide", "High confidence dispatches, medium asks a human, low sends a template."], ["5", "Alert", "Telegram message with a map pin, plus email."], ["6", "Learn", "Reviewer decisions become labelled training data."]]
  return (<div className="page"><Head k="THE SYSTEM" t="How it works" d="From underwater sound to a ranger's phone in six steps." />
    <ol className="steps">{S.map(([n, a, b]) => <li key={n}><i>{n}</i><div><h3>{a}</h3><p>{b}</p></div></li>)}</ol>
    <h3 className="sub">Honest limits</h3><div className="cols"><div className="card"><h3>One sensor = an area</h3>A point fix needs 3+ synchronised sensors.</div><div className="card"><h3>Look-alikes</h3>Engine misfires can sound like blasts, so uncertain events go to people.</div><div className="card"><h3>Free-tier hosting</h3>The cloud may sleep; the edge agent buffers and retries.</div></div></div>)
}
