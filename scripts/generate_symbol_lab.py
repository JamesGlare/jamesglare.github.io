#!/usr/bin/env python3
from __future__ import annotations

import math
from pathlib import Path
from typing import Iterable

ROOT = Path("/home/node/.openclaw/workspace/projects/jamesglare.github.io")
OUT = ROOT / "symbol-lab"
ASSETS = OUT / "assets"
SIZE = 128
CENTER = SIZE / 2
STROKE = "#d7deea"
MUTED = "#7f8aa0"
BG = "#0c0f14"
PANEL = "#131923"
BORDER = "rgba(255,255,255,0.08)"


def polar(cx: float, cy: float, r: float, deg: float) -> tuple[float, float]:
    rad = math.radians(deg)
    return cx + r * math.cos(rad), cy + r * math.sin(rad)


def arc_path(cx: float, cy: float, r: float, start: float, end: float) -> str:
    x1, y1 = polar(cx, cy, r, start)
    x2, y2 = polar(cx, cy, r, end)
    large = 1 if abs(end - start) > 180 else 0
    sweep = 1 if end > start else 0
    return f"M {x1:.2f} {y1:.2f} A {r:.2f} {r:.2f} 0 {large} {sweep} {x2:.2f} {y2:.2f}"


def svg_wrap(inner: str, view_box: int = SIZE) -> str:
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {view_box} {view_box}" fill="none">
  <rect width="100%" height="100%" rx="24" fill="{PANEL}"/>
  {inner}
</svg>
'''


def stroke(path: str, width: float = 1.7, opacity: float = 1.0, linecap: str = "round") -> str:
    return f'<path d="{path}" stroke="{STROKE}" stroke-width="{width}" stroke-linecap="{linecap}" stroke-linejoin="round" opacity="{opacity}"/>'


def circle(cx: float, cy: float, r: float, width: float = 1.7, opacity: float = 1.0, dash: str | None = None) -> str:
    extra = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<circle cx="{cx:.2f}" cy="{cy:.2f}" r="{r:.2f}" stroke="{STROKE}" stroke-width="{width}" opacity="{opacity}" fill="none"{extra}/>'


def line(x1: float, y1: float, x2: float, y2: float, width: float = 1.4, opacity: float = 1.0) -> str:
    return f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" stroke="{STROKE}" stroke-width="{width}" opacity="{opacity}" stroke-linecap="round"/>'


def dot(x: float, y: float, r: float = 1.8, opacity: float = 1.0, fill: str = STROKE) -> str:
    return f'<circle cx="{x:.2f}" cy="{y:.2f}" r="{r:.2f}" fill="{fill}" opacity="{opacity}"/>'


def optical_broken_rings() -> str:
    parts = [
        stroke(arc_path(CENTER, CENTER, 36, -18, 126), 1.8),
        stroke(arc_path(CENTER, CENTER, 36, 164, 296), 1.8, 0.82),
        stroke(arc_path(CENTER, CENTER, 25, 18, 168), 1.6, 0.86),
        stroke(arc_path(CENTER, CENTER, 25, 210, 338), 1.6, 0.66),
        stroke(arc_path(CENTER, CENTER, 14, -32, 190), 1.5, 0.9),
        dot(CENTER + 36, CENTER, 1.5, 0.9),
        dot(CENTER - 20, CENTER + 15, 1.4, 0.55),
    ]
    return svg_wrap("\n  ".join(parts))


def optical_wavefront() -> str:
    parts = [
        stroke(arc_path(36, CENTER + 4, 22, -56, 56), 1.6, 0.95),
        stroke(arc_path(36, CENTER + 4, 33, -52, 52), 1.6, 0.8),
        stroke(arc_path(36, CENTER + 4, 45, -48, 48), 1.6, 0.62),
        line(34, 24, 34, 104, 1.2, 0.22),
        dot(34, CENTER + 4, 2.4, 1.0),
        stroke("M 77 36 C 91 47, 95 60, 90 74 C 86 86, 92 96, 103 99", 1.5, 0.75),
    ]
    return svg_wrap("\n  ".join(parts))


def optical_interference() -> str:
    parts: list[str] = []
    for x in [38, 53, 68, 83, 98]:
        for y in [36, 51, 66, 81, 96]:
            dist = math.hypot(x - 68, y - 64)
            opacity = max(0.25, 1 - dist / 55)
            parts.append(dot(x, y, 1.4 + (0.8 if dist < 12 else 0), opacity))
    parts.extend([
        stroke(arc_path(46, 66, 24, -40, 40), 1.2, 0.4),
        stroke(arc_path(84, 62, 24, 140, 220), 1.2, 0.4),
        stroke("M 28 64 C 42 58, 57 58, 71 64 C 84 70, 98 70, 110 64", 1.3, 0.52),
    ])
    return svg_wrap("\n  ".join(parts))


def optical_contours() -> str:
    parts = [
        stroke("M 25 78 C 35 45, 60 28, 88 31 C 103 33, 108 44, 106 57 C 104 70, 96 79, 84 82 C 69 86, 57 81, 46 88", 1.7, 0.95),
        stroke("M 31 88 C 39 57, 61 40, 83 42 C 95 43, 99 51, 97 61 C 95 71, 89 78, 78 81 C 65 84, 56 79, 49 85", 1.5, 0.7),
        stroke("M 37 98 C 44 69, 62 53, 79 53 C 88 53, 91 60, 89 67 C 87 75, 82 80, 73 81 C 62 83, 56 78, 52 82", 1.3, 0.45),
        dot(92, 35, 1.5, 0.5),
    ]
    return svg_wrap("\n  ".join(parts))


def dynamics_lissajous() -> str:
    pts = []
    for i in range(241):
        t = (math.pi * 2 * i) / 240
        x = CENTER + 31 * math.sin(2 * t + 0.6)
        y = CENTER + 22 * math.sin(3 * t)
        pts.append((x, y))
    d = "M " + " L ".join(f"{x:.2f} {y:.2f}" for x, y in pts)
    parts = [stroke(d, 1.5, 0.9), dot(*pts[0], 1.6, 0.55), dot(*pts[120], 1.6, 0.55)]
    return svg_wrap("\n  ".join(parts))


def dynamics_spiral() -> str:
    pts = []
    for i in range(220):
        t = i / 18
        r = 2 + i * 0.19
        x = CENTER + math.cos(t) * r * 0.9
        y = CENTER + math.sin(t) * r * 0.62
        pts.append((x, y))
    d = "M " + " L ".join(f"{x:.2f} {y:.2f}" for x, y in pts)
    parts = [stroke(d, 1.45, 0.92), dot(CENTER, CENTER, 2.0, 0.9)]
    return svg_wrap("\n  ".join(parts))


def dynamics_branch() -> str:
    parts = [
        stroke("M 26 92 C 43 85, 57 72, 64 58 C 71 44, 82 34, 103 28", 1.7, 0.9),
        stroke("M 64 58 C 74 56, 85 61, 98 76", 1.45, 0.75),
        stroke("M 63 59 C 71 68, 78 81, 83 101", 1.45, 0.6),
        stroke("M 49 72 C 40 71, 31 75, 23 84", 1.25, 0.5),
        dot(64, 58, 2.2, 1.0),
        dot(103, 28, 1.7, 0.8),
        dot(98, 76, 1.7, 0.65),
        dot(83, 101, 1.7, 0.55),
    ]
    return svg_wrap("\n  ".join(parts))


def dynamics_field() -> str:
    parts: list[str] = []
    for x in [28, 48, 68, 88]:
        for y in [34, 54, 74, 94]:
            angle = (x * 0.055) - (y * 0.035)
            dx = math.cos(angle) * 8
            dy = math.sin(angle) * 8
            parts.append(line(x - dx, y - dy, x + dx, y + dy, 1.1, 0.42))
    parts.extend([
        stroke("M 23 80 C 40 62, 60 51, 81 51 C 91 51, 99 56, 105 66", 1.6, 0.9),
        stroke("M 28 95 C 46 79, 61 71, 79 72 C 92 73, 100 81, 103 92", 1.35, 0.58),
    ])
    return svg_wrap("\n  ".join(parts))


def geom_lattice() -> str:
    pts = [(34, 34), (64, 28), (93, 38), (28, 66), (61, 61), (95, 70), (36, 96), (69, 89)]
    edges = [(0, 1), (1, 2), (0, 3), (1, 4), (2, 5), (3, 4), (4, 5), (3, 6), (4, 7), (6, 7)]
    parts = [line(*pts[a], *pts[b], 1.3, 0.55) for a, b in edges]
    parts.extend(dot(x, y, 2.0 if i in {1, 4} else 1.6, 1.0 if i in {1, 4} else 0.75) for i, (x, y) in enumerate(pts))
    return svg_wrap("\n  ".join(parts))


def geom_transform() -> str:
    parts = []
    xs = [33, 48, 63, 78, 93]
    heights = [22, 38, 56, 38, 22]
    for x, h in zip(xs, heights):
        parts.append(line(x, CENTER - h / 2, x, CENTER + h / 2, 2.0, 0.82))
    parts.extend([
        line(26, CENTER, 100, CENTER, 1.1, 0.25),
        stroke("M 26 82 C 40 70, 56 66, 64 64 C 77 61, 91 53, 101 39", 1.35, 0.5),
    ])
    return svg_wrap("\n  ".join(parts))


def geom_cells() -> str:
    parts = [
        '<rect x="28" y="28" width="24" height="24" rx="6" stroke="%s" stroke-width="1.5" opacity="0.55"/>' % STROKE,
        '<rect x="56" y="28" width="18" height="18" rx="5" stroke="%s" stroke-width="1.5" opacity="0.8"/>' % STROKE,
        '<rect x="80" y="34" width="20" height="20" rx="6" stroke="%s" stroke-width="1.5" opacity="0.38"/>' % STROKE,
        '<rect x="40" y="62" width="28" height="28" rx="8" stroke="%s" stroke-width="1.5" opacity="0.88"/>' % STROKE,
        '<rect x="77" y="69" width="18" height="18" rx="5" stroke="%s" stroke-width="1.5" opacity="0.6"/>' % STROKE,
        line(52, 40, 56, 37, 1.2, 0.5),
        line(74, 38, 80, 44, 1.2, 0.4),
        line(68, 76, 77, 78, 1.2, 0.42),
        dot(54, 76, 1.5, 0.75),
    ]
    return svg_wrap("\n  ".join(parts))


def geom_asym_grid() -> str:
    parts = []
    for x in [30, 46, 62, 78, 94]:
        parts.append(line(x, 28, x, 100, 0.9, 0.12 if x not in {46, 78} else 0.24))
    for y in [30, 46, 62, 78, 94]:
        parts.append(line(28, y, 100, y, 0.9, 0.12 if y not in {46, 78} else 0.24))
    parts.extend([
        stroke("M 31 95 C 44 88, 51 77, 58 60 C 63 47, 74 37, 98 31", 1.5, 0.8),
        dot(58, 60, 2.2, 1.0),
        dot(46, 46, 1.4, 0.44),
        dot(78, 78, 1.4, 0.44),
    ])
    return svg_wrap("\n  ".join(parts))


SYMBOLS = [
    ("optical-broken-rings", "Optical", "Broken rings"),
    ("optical-wavefront", "Optical", "Wavefront arcs"),
    ("optical-interference", "Optical", "Interference field"),
    ("optical-contours", "Optical", "Contour bands"),
    ("dynamics-lissajous", "Dynamics", "Lissajous loop"),
    ("dynamics-spiral", "Dynamics", "Spiral attractor"),
    ("dynamics-branch", "Dynamics", "Branching trajectory"),
    ("dynamics-field", "Dynamics", "Field sweep"),
    ("geom-lattice", "Geometric", "Sparse lattice"),
    ("geom-transform", "Geometric", "Transform bars"),
    ("geom-cells", "Geometric", "Nested cells"),
    ("geom-asym-grid", "Geometric", "Asymmetric grid"),
]

GENERATORS = {
    "optical-broken-rings": optical_broken_rings,
    "optical-wavefront": optical_wavefront,
    "optical-interference": optical_interference,
    "optical-contours": optical_contours,
    "dynamics-lissajous": dynamics_lissajous,
    "dynamics-spiral": dynamics_spiral,
    "dynamics-branch": dynamics_branch,
    "dynamics-field": dynamics_field,
    "geom-lattice": geom_lattice,
    "geom-transform": geom_transform,
    "geom-cells": geom_cells,
    "geom-asym-grid": geom_asym_grid,
}


def ensure_dirs() -> None:
    ASSETS.mkdir(parents=True, exist_ok=True)


def write_symbols() -> None:
    for slug, _, _ in SYMBOLS:
        (ASSETS / f"{slug}.svg").write_text(GENERATORS[slug](), encoding="utf-8")


def preview_html() -> str:
    cards = []
    for slug, family, title in SYMBOLS:
        cards.append(f'''<article class="card">
  <img src="assets/{slug}.svg" alt="{title}" loading="lazy" />
  <div class="meta">
    <p class="family">{family}</p>
    <h3>{title}</h3>
    <code>{slug}</code>
  </div>
</article>''')
    return f'''<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Symbol lab</title>
    <style>
      :root {{
        --bg: {BG};
        --panel: {PANEL};
        --text: #eef2f7;
        --muted: {MUTED};
        --border: {BORDER};
      }}
      * {{ box-sizing: border-box; }}
      body {{
        margin: 0;
        font-family: Inter, system-ui, sans-serif;
        background: radial-gradient(circle at top, #162131 0, var(--bg) 44%);
        color: var(--text);
      }}
      main {{
        width: min(1120px, calc(100% - 32px));
        margin: 0 auto;
        padding: 48px 0 64px;
      }}
      h1 {{ font-size: clamp(2rem, 5vw, 3.4rem); margin: 0; letter-spacing: -0.04em; }}
      p.lead {{ max-width: 760px; color: var(--muted); margin: 16px 0 0; line-height: 1.7; }}
      .grid {{
        display: grid;
        grid-template-columns: repeat(4, minmax(0, 1fr));
        gap: 18px;
        margin-top: 34px;
      }}
      .card {{
        background: linear-gradient(180deg, #131923, #1a2230);
        border: 1px solid var(--border);
        border-radius: 22px;
        padding: 18px;
      }}
      img {{ width: 100%; height: auto; display: block; border-radius: 16px; }}
      .meta {{ margin-top: 14px; }}
      .family {{ margin: 0 0 8px; color: #b5f0d0; text-transform: uppercase; letter-spacing: 0.12em; font-size: 0.78rem; }}
      h3 {{ margin: 0; font-size: 1.02rem; }}
      code {{ display: block; margin-top: 8px; color: var(--muted); font-size: 0.84rem; }}
      .notes {{ margin-top: 34px; padding: 18px 20px; border-radius: 18px; border: 1px solid var(--border); background: rgba(255,255,255,0.02); color: var(--muted); }}
      @media (max-width: 920px) {{ .grid {{ grid-template-columns: repeat(2, minmax(0, 1fr)); }} }}
      @media (max-width: 560px) {{ .grid {{ grid-template-columns: 1fr; }} main {{ width: min(1120px, calc(100% - 22px)); }} }}
    </style>
  </head>
  <body>
    <main>
      <h1>Symbol lab</h1>
      <p class="lead">First-pass procedural SVG glyphs for Jannes Gladrow's website. These are intentionally monochrome, sparse, and slightly enigmatic, with three families: optical, dynamics, and geometric. The goal is not final decoration yet, just finding a visual language that feels scientific without going full startup or sci-fi kitsch.</p>
      <section class="grid">
        {''.join(cards)}
      </section>
      <section class="notes">
        Good next steps: pick 2 to 4 favorites, unify stroke weight and spacing further, then test tiny placements in the hero, section headers, or project cards. If one family clearly wins, we can generate a tighter second generation around it.
      </section>
    </main>
  </body>
</html>
'''


def main() -> None:
    ensure_dirs()
    write_symbols()
    (OUT / "index.html").write_text(preview_html(), encoding="utf-8")
    print(f"Wrote {len(SYMBOLS)} symbols to {ASSETS}")
    print(f"Preview: {OUT / 'index.html'}")


if __name__ == "__main__":
    main()
