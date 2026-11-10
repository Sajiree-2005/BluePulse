import { useEffect, useMemo, useState } from "react"
import { API, DEMO, getEvents, getInfo } from "../api.js"
const COL = { blast: "#ff4d3d", vessel: "#ffb020", biology: "#c8ff3d", environmental_noise: "#7fd6ff" }
export default function Dashboard() {
  const [events, setEvents] = useState(DEMO), [live, setLive] = useState(false), [sel, setSel] = useState(DEMO[0]), [info, setInfo] = useState(null)
  useEffect(() => {
    let es; const load = () => getEvents().then(e => { if (e.length) { setEvents(e.map(v => ({ ...v, conf: v.conf ?? null }))); setSel(s => s?.id?.startsWith("d") ? e[0] : s) } setLive(true) }).catch(() => setLive(false))
    load(); const t = setInterval(load, 6000); getInfo().then(setInfo).catch(() => {})
    try { es = new EventSource(`${API}/v1/stream`); es.onmessage = () => load() } catch { }
    return () => { clearInterval(t); es?.close() }
  }, [])
  const pts = useMemo(() => { const f = events.filter(e => e.lat != null); const la = f.map(e => e.lat), lo = f.map(e => e.lon), a = Math.min(...la, 15.8) - .05, b = Math.max(...la, 16.2) + .05, c = Math.min(...lo, 73.3) - .05, d = Math.max(...lo, 73.7) + .05
    return f.map(e => ({ ...e, x: (e.lon - c) / (d - c), y: 1 - (e.lat - a) / (b - a) })) }, [events])
  const gate = c => c == null ? ["No score", "#9fc4d4"] : c >= 80 ? ["Auto-dispatch", "#c8ff3d"] : c >= 50 ? ["Needs human review", "#ffb020"] : ["Template alert only", "#ff4d3d"]
  const [gl, gc] = gate(sel?.conf)
  return (
    <div className="dash">
      <div className="dash-bar"><span className={"dot " + (live ? "on" : "")} />{live ? "Live from your backend" : "Demo data (backend offline)"}
        {info && <span className={"chip " + (info.nugen_active ? "good" : "warn")}>{info.nugen_active ? `Nugen model ${info.model_id}` : `LLM: ${info.llm_provider} (not Nugen)`}</span>}</div>
      <div className="dash-grid">
        <div className="map" role="img" aria-label="Sensor map">
          <svg viewBox="0 0 100 75" preserveAspectRatio="none"><path d="M0 0H22C14 20 24 45 8 75H0Z" fill="#0b5a52" />
            {[20, 40, 60, 80].map(g => <line key={g} x1={g} y1="0" x2={g} y2="75" stroke="#ffffff10" />)}</svg>
          {pts.map(p => <button key={p.id} className={"pin " + (sel?.id === p.id ? "sel" : "")} style={{ left: p.x * 100 + "%", top: p.y * 100 + "%", "--c": COL[p.label] || "#fff" }} onClick={() => setSel(p)} aria-label={`${p.sensor} ${p.label}`}><i /><b>{p.sensor}</b></button>)}
        </div>
        <div className="panel">
          {sel && <><span className="tag" style={{ background: COL[sel.label] || "#0fb5a6" }}>{sel.label?.toUpperCase()}</span> <span className="sev">{sel.severity}</span>
            <h3>{sel.sensor}</h3>
            <div className="meter"><i style={{ width: (sel.conf ?? 0) + "%", background: gc }} /></div>
            <p className="gate" style={{ color: gc }}>AI confidence {sel.conf ?? "n/a"} &middot; {gl}</p>
            <p className="brief">{sel.briefing}</p></>}
          <div className="feed">{events.slice(0, 6).map(e => <button key={e.id} className={sel?.id === e.id ? "on" : ""} onClick={() => setSel(e)}><i style={{ background: COL[e.label] || "#fff" }} />{e.sensor}<em>{e.label}</em></button>)}</div>
        </div>
      </div>
    </div>)
}
