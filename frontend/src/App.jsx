import { useEffect, useRef, useState } from "react"
import WaterCanvas from "./components/WaterCanvas.jsx"; import Spectrogram from "./components/Spectrogram.jsx"; import Dashboard from "./components/Dashboard.jsx"; import Provenance from "./components/Provenance.jsx"; import { Command, Reef, Evidence, How } from "./pages.jsx"
function useReveal() { const r = useRef(); useEffect(() => { const o = new IntersectionObserver(([e]) => e.isIntersecting && r.current.classList.add("in"), { threshold: .2 }); o.observe(r.current); return () => o.disconnect() }, []); return r }
function Count({ to }) { const [n, setN] = useState(0), r = useReveal(); useEffect(() => { let i = 0; const id = setInterval(() => { i += to / 40; setN(Math.min(to, Math.round(i))); if (i >= to) clearInterval(id) }, 30); return () => clearInterval(id) }, [to]); return <span ref={r} className="big">1 / {n} min</span> }
const Sec = ({ id, children }) => { const r = useReveal(); return <section id={id} ref={r} className="reveal">{children}</section> }
const ROUTES = [["/", "Home"], ["/command", "Command center"], ["/reef", "Reef health"], ["/evidence", "Evidence"], ["/how", "How it works"]]
const useRoute = () => { const [r, setR] = useState(location.hash.slice(1) || "/"); useEffect(() => { const f = () => { setR(location.hash.slice(1) || "/"); scrollTo(0, 0) }; addEventListener("hashchange", f); return () => removeEventListener("hashchange", f) }, []); return r }
export default function App() {
  const route = useRoute(); const [d, setD] = useState("0"); const [menu, setMenu] = useState(false)
  useEffect(() => { const t = setInterval(() => setD((parseFloat(getComputedStyle(document.documentElement).getPropertyValue("--depth")) * 30 || 0).toFixed(0)), 200); return () => clearInterval(t) }, [])
  return (<>
    <WaterCanvas />
    <nav><a className="logo" href="#/">Blue<b>Pulse</b></a><button className="burger" onClick={() => setMenu(!menu)} aria-label="Menu">&#9776;</button><div className={"links " + (menu ? "open" : "")}>{ROUTES.map(([p, t]) => <a key={p} href={"#" + p} className={route === p ? "on" : ""} onClick={() => setMenu(false)}>{t}</a>)}</div></nav>
    <div className="depth" aria-hidden="true"><span>{d} m</span><small>depth</small></div>
    <main>
      {route === "/command" ? <Command /> : route === "/reef" ? <Reef /> : route === "/evidence" ? <Evidence /> : route === "/how" ? <How /> : <>
      <Sec id="top"><h1>Hear the reef<br />before it <em>breaks.</em></h1>
        <p className="lead">Hydrophones listen. AI recognises a blast in seconds. Rangers get a pin and a plain-language briefing. Scroll to dive.</p><a className="cta" href="#stat">Dive in &darr;</a></Sec>
      <Sec id="stat"><Count to={62} /><h2>One bomb. Every <em>hour.</em></h2><p className="lead">A 2026 study off Sulawesi heard a blast roughly once every 62 minutes from a single $150 recorder.</p></Sec>
      <Sec id="voice"><h2>The reef has a <em>voice.</em></h2><p className="lead">Snapping shrimp crackle. Fish chorus at dusk. A blast is a sharp, broadband slam. BluePulse learns the difference.</p><Spectrogram />
        <div className="cols"><div className="card"><h3>1. Listen</h3>An edge agent cleans ocean noise (PCEN) and flags candidates.</div><div className="card"><h3>2. Classify</h3>An audio model labels blast, vessel, biology or noise.</div><div className="card"><h3>3. Explain</h3>A Nugen-aligned model writes the briefing and a confidence score.</div></div></Sec>
      <Sec id="cmd"><h2>Command <em>center</em></h2><p className="lead">Tap a sensor. High confidence dispatches, medium goes to a human, low sends a template alert.</p><Dashboard /><a className="cta" href="#/command">Open the full command center &rarr;</a></Sec></>}
    </main>
    <footer>BluePulse &middot; AI bioacoustic monitoring for coral reefs</footer></>)
}
