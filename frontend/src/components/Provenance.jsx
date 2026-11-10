import { useEffect, useState } from "react"
import { API } from "../api.js"
export default function Provenance() {
  const [rows, setRows] = useState(null)
  useEffect(() => { const load = () => fetch(`${API}/v1/provenance`).then(r => r.json()).then(setRows).catch(() => setRows(null)); load(); const t = setInterval(load, 7000); return () => clearInterval(t) }, [])
  const dl = () => { const a = document.createElement("a"); a.href = URL.createObjectURL(new Blob([JSON.stringify(rows, null, 2)], { type: "application/json" })); a.download = "bluepulse-provenance.json"; a.click() }
  return (<div className="prov"><div className="dash-bar"><b>Model provenance</b><span>Every AI call is logged. This is the evidence that events are served by your Nugen-aligned model.</span>{rows?.length > 0 && <button className="btn sm" onClick={dl}>Export JSON</button>}</div>
    {!rows ? <p className="hint">Start the backend to see live provenance.</p> : !rows.length ? <p className="hint">No AI calls yet. Send an event.</p> :
      <div className="tbl"><table><thead><tr><th>Provider</th><th>Model id</th><th>Latency</th><th>Confidence</th><th>Outcome</th></tr></thead>
        <tbody>{rows.slice(0, 8).map((r, i) => <tr key={i}><td><span className={"chip " + (r.provider === "nugen" ? "good" : "warn")}>{r.provider}</span></td><td>{r.model_id || "-"}</td><td>{r.latency_ms} ms</td><td>{r.confidence ?? "-"}</td><td>{r.outcome}</td></tr>)}</tbody></table></div>}</div>)
}
