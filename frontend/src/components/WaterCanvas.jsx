import { useEffect, useRef } from "react"
// Looking UP from underwater: Snell's window (bright circle of sky), rippling surface, caustics, light shafts, bubbles. Depth follows scroll.
export default function WaterCanvas() {
  const ref = useRef(null)
  useEffect(() => {
    const c = ref.current, x = c.getContext("2d"), dpr = Math.min(devicePixelRatio || 1, 2); let W, H, raf, mx = .5, pulses = []
    const rs = () => { W = c.width = innerWidth * dpr; H = c.height = innerHeight * dpr }; rs()
    const sp = document.createElement("canvas"); sp.width = sp.height = 64; const sg = sp.getContext("2d").createRadialGradient(32, 32, 0, 32, 32, 32)
    sg.addColorStop(0, "rgba(220,255,245,1)"); sg.addColorStop(1, "rgba(220,255,245,0)"); const sx = sp.getContext("2d"); sx.fillStyle = sg; sx.fillRect(0, 0, 64, 64)
    const bubs = Array.from({ length: 70 }, () => ({ x: Math.random(), y: Math.random(), r: 1 + Math.random() * 3, v: .0003 + Math.random() * .001 }))
    const depth = () => { const m = document.documentElement.scrollHeight - innerHeight; return m > 0 ? Math.min(1, scrollY / m) : 0 }
    const onMove = e => { mx = e.clientX / innerWidth }, onClick = e => { if (!e.target.closest("a,button,.dash")) pulses.push({ x: e.clientX * dpr, y: e.clientY * dpr, r: 0 }) }
    addEventListener("resize", rs); addEventListener("mousemove", onMove); addEventListener("click", onClick)
    const frame = t => {
      const d = depth(), fade = 1 - d * .85
      const g = x.createLinearGradient(0, 0, 0, H); g.addColorStop(0, `hsl(188,88%,${36 - d * 24}%)`); g.addColorStop(.55, `hsl(205,82%,${17 - d * 11}%)`); g.addColorStop(1, "#020b16")
      x.globalCompositeOperation = "source-over"; x.fillStyle = g; x.fillRect(0, 0, W, H); x.globalCompositeOperation = "lighter"
      const cx = W * (.5 + (mx - .5) * .12), cy = -H * .08 - d * H * .5, R = W * .5 * (1 - d * .55)           // Snell's window
      const w = x.createRadialGradient(cx, cy, 0, cx, cy, R); w.addColorStop(0, `rgba(235,255,250,${.95 * fade})`); w.addColorStop(.45, `rgba(130,245,230,${.38 * fade})`); w.addColorStop(1, "rgba(0,0,0,0)"); x.fillStyle = w; x.fillRect(0, 0, W, H)
      const sy = Math.max(-60 * dpr, 90 * dpr - scrollY * .35 * dpr)                                        // rippling surface ceiling
      for (let L = 0; L < 4; L++) { x.beginPath(); x.moveTo(0, 0); for (let i = 0; i <= W; i += 14 * dpr) x.lineTo(i, sy + L * 16 * dpr + Math.sin(i * .004 / dpr + t / (800 + L * 250)) * (18 - L * 3) * dpr + Math.sin(i * .011 / dpr - t / 520) * 6 * dpr); x.lineTo(W, 0); x.closePath(); x.fillStyle = L ? `rgba(120,255,235,${.14 * fade})` : `rgba(235,255,250,${.55 * fade})`; x.fill() }
      for (let i = 0; i < 8; i++) { const sx0 = W * (i / 8 + .05) + Math.sin(t / 2600 + i) * 70 * dpr, gr = x.createLinearGradient(sx0, 0, sx0 + 220 * dpr, H); gr.addColorStop(0, `rgba(150,255,235,${.16 * fade})`); gr.addColorStop(1, "rgba(0,0,0,0)"); x.fillStyle = gr; x.beginPath(); x.moveTo(sx0 - 20 * dpr, 0); x.lineTo(sx0 + 50 * dpr, 0); x.lineTo(sx0 + 330 * dpr, H); x.lineTo(sx0 + 120 * dpr, H); x.fill() }
      const step = 44 * dpr                                                                                  // caustic network
      for (let gx = 0; gx < W; gx += step) for (let gy = 0; gy < H * .85; gy += step) { const v = Math.sin(gx * .013 / dpr + t / 700) * Math.sin(gy * .016 / dpr - t / 900) + Math.sin((gx + gy) * .007 / dpr + t / 1300); const a = Math.max(0, v - .9) * .5 * fade * (1 - gy / H); if (a > .01) { x.globalAlpha = Math.min(.5, a); x.drawImage(sp, gx - step * .8, gy - step * .8, step * 1.6, step * 1.6) } }
      x.globalAlpha = 1
      bubs.forEach(b => { b.y -= b.v * (1 + d); b.x += Math.sin(t / 1200 + b.y * 9) * .0003; if (b.y < -.02) { b.y = 1.02; b.x = Math.random() } x.strokeStyle = "rgba(200,255,245,.35)"; x.lineWidth = dpr; x.beginPath(); x.arc(b.x * W, b.y * H, b.r * dpr, 0, 7); x.stroke() })
      pulses = pulses.filter(p => p.r < 420 * dpr); pulses.forEach(p => { p.r += 5 * dpr; x.strokeStyle = `rgba(200,255,61,${1 - p.r / (420 * dpr)})`; x.lineWidth = 3 * dpr; x.beginPath(); x.arc(p.x, p.y, p.r, 0, 7); x.stroke() })
      document.documentElement.style.setProperty("--depth", d.toFixed(3)); raf = requestAnimationFrame(frame)
    }
    raf = requestAnimationFrame(frame)
    return () => { cancelAnimationFrame(raf); removeEventListener("resize", rs); removeEventListener("mousemove", onMove); removeEventListener("click", onClick) }
  }, [])
  return <canvas ref={ref} className="sea" aria-hidden="true" />
}
