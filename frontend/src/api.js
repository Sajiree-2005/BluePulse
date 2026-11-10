export const API = import.meta.env.VITE_API_URL || "http://localhost:8000"
export const DEMO = [
  { id: "d1", sensor: "Malvan North", label: "blast", severity: "critical", conf: 91, lat: 16.06, lon: 73.46, ts: 0, provider: "demo", briefing: "Briefing: A sharp broadband slam, 14 ms onset, heard on 3 sensors off Malvan North. Recommended action: dispatch a patrol and preserve the clip. Uncertainty: an engine misfire cannot be fully excluded." },
  { id: "d2", sensor: "Sindhudurg Reef", label: "vessel", severity: "low", conf: 68, lat: 15.9, lon: 73.5, ts: 0, provider: "demo", briefing: "Briefing: Diesel engine with a surge pattern, probably a small fishing boat. Recommended action: log it. Uncertainty: moderate confidence, flagged for human review." },
  { id: "d3", sensor: "Tarkarli Shelf", label: "biology", severity: "info", conf: 83, lat: 16.0, lon: 73.58, ts: 0, provider: "demo", briefing: "Briefing: Dusk fish chorus 22% above this site's baseline. Recommended action: none. Uncertainty: low." },
]
export async function getEvents() { const r = await fetch(`${API}/v1/events`); if (!r.ok) throw new Error(r.status); return r.json() }
export async function getInfo() { const r = await fetch(`${API}/v1/system/info`); return r.json() }
