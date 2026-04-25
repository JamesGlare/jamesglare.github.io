#!/usr/bin/env python3
from __future__ import annotations

import math
from pathlib import Path

ROOT = Path('/home/node/.openclaw/workspace/projects/jamesglare.github.io')
OUT = ROOT / 'symbol-lab' / 'v2'
ASSETS = OUT / 'assets'
SIZE = 160
CENTER = SIZE / 2
BG = '#0c0f14'
PANEL = '#131923'
STROKE = '#dce4ef'
MUTED = '#8792a8'
BORDER = 'rgba(255,255,255,0.08)'


def polar(cx: float, cy: float, r: float, deg: float) -> tuple[float, float]:
    rad = math.radians(deg)
    return cx + r * math.cos(rad), cy + r * math.sin(rad)


def arc_path(cx: float, cy: float, r: float, start: float, end: float) -> str:
    x1, y1 = polar(cx, cy, r, start)
    x2, y2 = polar(cx, cy, r, end)
    large = 1 if abs(end - start) > 180 else 0
    sweep = 1 if end > start else 0
    return f'M {x1:.2f} {y1:.2f} A {r:.2f} {r:.2f} 0 {large} {sweep} {x2:.2f} {y2:.2f}'


def svg(inner: str) -> str:
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {SIZE} {SIZE}" fill="none">
  <rect width="100%" height="100%" rx="30" fill="{PANEL}"/>
  {inner}
</svg>
'''


def path(d: str, width: float = 1.8, opacity: float = 1.0) -> str:
    return f'<path d="{d}" stroke="{STROKE}" stroke-width="{width}" stroke-linecap="round" stroke-linejoin="round" opacity="{opacity}"/>'


def line(x1: float, y1: float, x2: float, y2: float, width: float = 1.5, opacity: float = 1.0) -> str:
    return f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" stroke="{STROKE}" stroke-width="{width}" opacity="{opacity}" stroke-linecap="round"/>'


def dot(x: float, y: float, r: float = 1.9, opacity: float = 1.0) -> str:
    return f'<circle cx="{x:.2f}" cy="{y:.2f}" r="{r:.2f}" fill="{STROKE}" opacity="{opacity}"/>'


def rings_a() -> str:
    parts = [
        path(arc_path(CENTER, CENTER, 46, -8, 108), 2.0, 0.98),
        path(arc_path(CENTER, CENTER, 46, 152, 290), 2.0, 0.7),
        path(arc_path(CENTER, CENTER, 32, 12, 158), 1.75, 0.84),
        path(arc_path(CENTER, CENTER, 32, 208, 346), 1.75, 0.56),
        path(arc_path(CENTER, CENTER, 18, -30, 184), 1.55, 0.88),
        dot(CENTER + 46, CENTER - 1, 1.4, 0.9),
        dot(CENTER - 16, CENTER + 22, 1.3, 0.52),
    ]
    return svg('\n  '.join(parts))


def rings_b() -> str:
    parts = [
        path(arc_path(CENTER - 3, CENTER + 2, 44, -22, 132), 1.95, 0.9),
        path(arc_path(CENTER - 3, CENTER + 2, 44, 188, 314), 1.95, 0.5),
        path(arc_path(CENTER + 8, CENTER - 6, 28, 34, 200), 1.7, 0.78),
        path(arc_path(CENTER + 8, CENTER - 6, 28, 228, 356), 1.7, 0.42),
        path('M 53 109 C 71 101, 88 99, 106 105', 1.4, 0.34),
        dot(110, 60, 1.5, 0.82),
    ]
    return svg('\n  '.join(parts))


def contours_a() -> str:
    parts = [
        path('M 35 96 C 42 59, 68 35, 101 39 C 118 41, 126 54, 123 71 C 120 87, 108 98, 92 101 C 74 105, 62 100, 49 108', 1.95, 0.96),
        path('M 42 108 C 48 73, 70 50, 96 52 C 111 54, 117 64, 114 77 C 111 89, 102 97, 89 100 C 75 103, 64 99, 55 105', 1.65, 0.7),
        path('M 49 119 C 54 88, 71 67, 92 67 C 103 67, 108 75, 105 85 C 102 94, 95 100, 84 102 C 72 104, 64 99, 58 103', 1.35, 0.46),
        dot(108, 46, 1.4, 0.48),
    ]
    return svg('\n  '.join(parts))


def contours_b() -> str:
    parts = [
        path('M 34 82 C 44 52, 72 35, 102 39 C 119 41, 126 55, 120 70 C 114 84, 100 91, 84 90 C 69 89, 58 96, 49 112', 1.9, 0.94),
        path('M 44 92 C 52 66, 74 52, 97 55 C 110 57, 115 67, 111 78 C 107 88, 97 93, 86 93 C 73 92, 64 97, 57 108', 1.55, 0.68),
        path('M 55 101 C 61 80, 77 69, 94 71 C 103 72, 107 79, 104 87 C 101 94, 94 98, 85 98 C 76 98, 68 101, 62 108', 1.25, 0.42),
        path('M 40 35 C 47 38, 50 42, 53 49', 1.2, 0.28),
    ]
    return svg('\n  '.join(parts))


def lissajous_a() -> str:
    pts = []
    for i in range(320):
        t = math.tau * i / 319
        x = CENTER + 40 * math.sin(2 * t + 0.55)
        y = CENTER + 29 * math.sin(3 * t)
        pts.append((x, y))
    d = 'M ' + ' L '.join(f'{x:.2f} {y:.2f}' for x, y in pts)
    return svg('\n  '.join([path(d, 1.55, 0.92), dot(*pts[0], 1.5, 0.55), dot(*pts[160], 1.5, 0.55)]))


def lissajous_b() -> str:
    pts = []
    for i in range(320):
        t = math.tau * i / 319
        x = CENTER + 34 * math.sin(3 * t + 0.2)
        y = CENTER + 34 * math.sin(2 * t)
        pts.append((x, y))
    d = 'M ' + ' L '.join(f'{x:.2f} {y:.2f}' for x, y in pts)
    return svg('\n  '.join([path(d, 1.45, 0.88), line(80, 30, 80, 130, 0.9, 0.14), line(30, 80, 130, 80, 0.9, 0.14)]))


def cells_a() -> str:
    parts = [
        '<rect x="30" y="28" width="34" height="34" rx="9" stroke="%s" stroke-width="1.6" opacity="0.56"/>' % STROKE,
        '<rect x="68" y="34" width="24" height="24" rx="7" stroke="%s" stroke-width="1.6" opacity="0.84"/>' % STROKE,
        '<rect x="98" y="38" width="20" height="20" rx="6" stroke="%s" stroke-width="1.4" opacity="0.34"/>' % STROKE,
        '<rect x="42" y="74" width="38" height="38" rx="10" stroke="%s" stroke-width="1.7" opacity="0.92"/>' % STROKE,
        '<rect x="88" y="82" width="24" height="24" rx="7" stroke="%s" stroke-width="1.5" opacity="0.58"/>' % STROKE,
        line(64, 45, 68, 46, 1.1, 0.4),
        line(92, 48, 98, 48, 1.1, 0.3),
        line(80, 93, 88, 94, 1.1, 0.34),
        dot(59, 93, 1.5, 0.78),
    ]
    return svg('\n  '.join(parts))


def cells_b() -> str:
    parts = [
        '<rect x="32" y="34" width="28" height="28" rx="8" stroke="%s" stroke-width="1.5" opacity="0.46"/>' % STROKE,
        '<rect x="63" y="29" width="38" height="38" rx="10" stroke="%s" stroke-width="1.7" opacity="0.92"/>' % STROKE,
        '<rect x="106" y="35" width="18" height="18" rx="6" stroke="%s" stroke-width="1.4" opacity="0.28"/>' % STROKE,
        '<rect x="47" y="79" width="26" height="26" rx="7" stroke="%s" stroke-width="1.45" opacity="0.74"/>' % STROKE,
        '<rect x="79" y="73" width="34" height="34" rx="9" stroke="%s" stroke-width="1.6" opacity="0.6"/>' % STROKE,
        line(60, 47, 63, 46, 1.1, 0.36),
        line(101, 48, 106, 44, 1.1, 0.26),
        line(73, 89, 79, 89, 1.1, 0.3),
        dot(96, 90, 1.45, 0.72),
    ]
    return svg('\n  '.join(parts))


def spiral_a() -> str:
    pts = []
    for i in range(250):
        t = i / 18.5
        r = 3 + i * 0.22
        x = CENTER + math.cos(t) * r * 0.92
        y = CENTER + math.sin(t) * r * 0.68
        pts.append((x, y))
    d = 'M ' + ' L '.join(f'{x:.2f} {y:.2f}' for x, y in pts)
    return svg('\n  '.join([path(d, 1.45, 0.92), dot(CENTER, CENTER, 2.0, 0.88)]))


def spiral_b() -> str:
    pts = []
    for i in range(260):
        t = i / 17.5
        r = 2 + i * 0.18
        x = CENTER + math.cos(t + 0.35) * r * 0.72
        y = CENTER + math.sin(t) * r * 0.94
        pts.append((x, y))
    d = 'M ' + ' L '.join(f'{x:.2f} {y:.2f}' for x, y in pts)
    return svg('\n  '.join([path(d, 1.38, 0.9), path('M 42 120 C 52 113, 63 110, 74 108', 1.05, 0.22)]))


SYMBOLS = [
    ('rings-a', 'Broken rings', 'Variant A', rings_a),
    ('rings-b', 'Broken rings', 'Variant B', rings_b),
    ('contours-a', 'Contour bands', 'Variant A', contours_a),
    ('contours-b', 'Contour bands', 'Variant B', contours_b),
    ('lissajous-a', 'Lissajous loop', 'Variant A', lissajous_a),
    ('lissajous-b', 'Lissajous loop', 'Variant B', lissajous_b),
    ('cells-a', 'Nested cells', 'Variant A', cells_a),
    ('cells-b', 'Nested cells', 'Variant B', cells_b),
    ('spiral-a', 'Spiral attractor', 'Variant A', spiral_a),
    ('spiral-b', 'Spiral attractor', 'Variant B', spiral_b),
]


def ensure_dirs() -> None:
    ASSETS.mkdir(parents=True, exist_ok=True)


def write_assets() -> None:
    for slug, _, _, fn in SYMBOLS:
        (ASSETS / f'{slug}.svg').write_text(fn(), encoding='utf-8')


def preview_html() -> str:
    cards = []
    for slug, family, variant, _ in SYMBOLS:
        cards.append(f'''<article class="card">
  <img src="assets/{slug}.svg" alt="{family} {variant}" loading="lazy" />
  <div class="meta">
    <p class="family">{family}</p>
    <h3>{variant}</h3>
    <code>{slug}</code>
  </div>
</article>''')
    return f'''<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Symbol lab v2</title>
    <style>
      :root {{
        --bg: {BG};
        --panel: {PANEL};
        --text: #eef2f7;
        --muted: {MUTED};
        --border: {BORDER};
      }}
      * {{ box-sizing: border-box; }}
      body {{ margin: 0; font-family: Inter, system-ui, sans-serif; background: radial-gradient(circle at top, #162131 0, var(--bg) 44%); color: var(--text); }}
      main {{ width: min(1080px, calc(100% - 32px)); margin: 0 auto; padding: 48px 0 64px; }}
      h1 {{ font-size: clamp(2rem, 5vw, 3.3rem); margin: 0; letter-spacing: -0.04em; }}
      p.lead {{ max-width: 780px; color: var(--muted); margin: 16px 0 0; line-height: 1.7; }}
      .back {{ display: inline-block; margin-top: 14px; color: #b5f0d0; text-decoration: none; }}
      .grid {{ display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 18px; margin-top: 34px; }}
      .card {{ background: linear-gradient(180deg, #131923, #1a2230); border: 1px solid var(--border); border-radius: 22px; padding: 18px; }}
      img {{ width: 100%; height: auto; display: block; border-radius: 18px; }}
      .meta {{ margin-top: 14px; }}
      .family {{ margin: 0 0 8px; color: #b5f0d0; text-transform: uppercase; letter-spacing: 0.12em; font-size: 0.78rem; }}
      h3 {{ margin: 0; font-size: 1.05rem; }}
      code {{ display: block; margin-top: 8px; color: var(--muted); font-size: 0.84rem; }}
      .notes {{ margin-top: 32px; padding: 18px 20px; border-radius: 18px; border: 1px solid var(--border); background: rgba(255,255,255,0.02); color: var(--muted); line-height: 1.7; }}
      @media (max-width: 760px) {{ .grid {{ grid-template-columns: 1fr; }} }}
    </style>
  </head>
  <body>
    <main>
      <h1>Symbol lab v2</h1>
      <p class="lead">Second pass around the symbols Jannes liked most: broken rings, contour bands, Lissajous loops, nested cells, and spiral attractors. Each family now has two more deliberate variants so we can identify what feels best before placing anything on the homepage.</p>
      <a class="back" href="/symbol-lab/">← back to v1 sheet</a>
      <section class="grid">{''.join(cards)}</section>
      <section class="notes">Recommendation: pick 1 to 2 families that feel most like your site, then I will unify them even harder and test an actual placement. My guess is broken rings + contour bands or broken rings + nested cells.</section>
    </main>
  </body>
</html>
'''


def main() -> None:
    ensure_dirs()
    write_assets()
    (OUT / 'index.html').write_text(preview_html(), encoding='utf-8')
    print(f'Wrote {len(SYMBOLS)} symbols to {ASSETS}')
    print(f'Preview: {OUT / "index.html"}')


if __name__ == '__main__':
    main()
