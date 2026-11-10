import { useEffect, useRef } from "react"
export default function Spectrogram() {
  const ref = useRef(null)
  useEffect(() => {
    const c = ref.current, x = c.getContext("2d"), dpr = devicePixelRatio || 1; const rs = () => { c.width = c.clientWidth * dpr; c.height = c.clientHeight * dpr }; rs(); addEventListener("resize", rs)
    const id = setInterval(() => { const h = c.height, w = c.width; x.drawImage(c, -3, 0); const blast = Math.random() < .035
      for (let y = 0; y < h; y += 3) { const f = 1 - y / h; let v = Math.random() * .25 + f * .22 + (Math.random() < .02 * (1 - f) ? .6 : 0); if (blast) v = .9 + Math.random() * .1
        x.fillStyle = blast ? `rgb(255,${77 + v * 100 | 0},61)` : `rgb(${v * 200 | 0},${60 + v * 190 | 0},${80 + v * 120 | 0})`; x.fillRect(w - 3, y, 3, 3) } }, 40)
    return () => { clearInterval(id); removeEventListener("resize", rs) }
  }, [])
  return <canvas ref={ref} className="spec" role="img" aria-label="Live spectrogram: red bursts are blasts" />
}
