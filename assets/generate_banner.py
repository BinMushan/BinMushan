"""
Generates a Matrix-style green digital-rain banner SVG for the README hero.

Output: assets/matrix-banner.svg

The SVG uses native SMIL <animateTransform> so it animates as an <img src=...>
inside GitHub README (no CSS-in-img required).
"""

from __future__ import annotations

import random
from pathlib import Path

# ── canvas ──────────────────────────────────────────────────────────────
W, H = 1280, 300
COL_W = 16                  # column width in px
CHAR_H = 16                 # vertical spacing between chars
N_COLS = W // COL_W         # number of rain columns
CHARS_PER_COL = 18          # how tall each rain "string" is

GLYPHS = (
    "01アァカサタナハマヤャラワガザダバパイィキシチニヒミリヰギジヂビピウゥクスツヌ"
    "フムユュルグズブヅプエェケセテネヘメレヱゲゼデベペオォコソトノホモヨョロヲゴゾ"
    "01<>/\\|+-*=#@$%&{}[]"
)

random.seed(7)              # deterministic output


def rand_string(n: int) -> list[str]:
    return [random.choice(GLYPHS) for _ in range(n)]


def column(i: int) -> str:
    x = i * COL_W + COL_W // 2
    dur = round(random.uniform(3.6, 7.5), 2)         # fall speed
    delay = round(random.uniform(-7.0, 0.0), 2)      # stagger start
    chars = rand_string(CHARS_PER_COL)
    start_y = -CHARS_PER_COL * CHAR_H

    # build text glyphs inside the column; head glyph is bright
    parts = []
    for k, ch in enumerate(chars):
        y = k * CHAR_H
        if k == 0:
            cls = "head"
        elif k <= 2:
            cls = "near"
        else:
            # fade older chars
            cls = f"t{min(k, 9)}"
        # escape XML
        if ch == "<":
            ch = "&lt;"
        elif ch == ">":
            ch = "&gt;"
        elif ch == "&":
            ch = "&amp;"
        parts.append(f'<text x="0" y="{y}" class="{cls}">{ch}</text>')

    glyphs = "".join(parts)

    return (
        f'<g class="rain" transform="translate({x},{start_y})">'
        f"{glyphs}"
        f'<animateTransform attributeName="transform" type="translate" '
        f'from="{x},{start_y}" to="{x},{H + CHARS_PER_COL * CHAR_H}" '
        f'dur="{dur}s" begin="{delay}s" repeatCount="indefinite"/>'
        f"</g>"
    )


columns_svg = "\n".join(column(i) for i in range(N_COLS))


svg = f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="100%" preserveAspectRatio="xMidYMid slice" role="img" aria-label="Bin Mushan — Software Dev, Web, Design, Automation">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%"  stop-color="#020a05"/>
      <stop offset="55%" stop-color="#01140a"/>
      <stop offset="100%" stop-color="#000604"/>
    </linearGradient>
    <radialGradient id="vignette" cx="50%" cy="50%" r="65%">
      <stop offset="55%" stop-color="#000000" stop-opacity="0"/>
      <stop offset="100%" stop-color="#000000" stop-opacity="0.85"/>
    </radialGradient>
    <radialGradient id="centerShade" cx="50%" cy="50%" r="42%">
      <stop offset="0%"  stop-color="#000000" stop-opacity="0.85"/>
      <stop offset="55%" stop-color="#000000" stop-opacity="0.55"/>
      <stop offset="100%" stop-color="#000000" stop-opacity="0"/>
    </radialGradient>
    <pattern id="scanlines" width="3" height="3" patternUnits="userSpaceOnUse">
      <rect width="3" height="3" fill="transparent"/>
      <rect width="3" height="1" fill="#00ff88" opacity="0.04"/>
    </pattern>
    <filter id="glow" x="-20%" y="-50%" width="140%" height="200%">
      <feGaussianBlur stdDeviation="2.4" result="b"/>
      <feMerge>
        <feMergeNode in="b"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="softGlow" x="-20%" y="-50%" width="140%" height="200%">
      <feGaussianBlur stdDeviation="1.2" result="b"/>
      <feMerge>
        <feMergeNode in="b"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <style><![CDATA[
      .rain {{
        font-family: 'JetBrains Mono','Fira Code','Courier New',monospace;
        font-size: 14px;
        font-weight: 600;
      }}
      .head {{ fill: #d6ffe6; filter: url(#glow); }}
      .near {{ fill: #6cf3a4; }}
      .t3   {{ fill: #43d97f; }}
      .t4   {{ fill: #2dbe66; opacity: 0.92; }}
      .t5   {{ fill: #22a557; opacity: 0.82; }}
      .t6   {{ fill: #1a8d49; opacity: 0.72; }}
      .t7   {{ fill: #15743c; opacity: 0.6;  }}
      .t8   {{ fill: #105c30; opacity: 0.45; }}
      .t9   {{ fill: #0b4624; opacity: 0.32; }}
      .title {{
        font-family: 'JetBrains Mono','Fira Code','Courier New',monospace;
        font-weight: 800;
        font-size: 92px;
        letter-spacing: 6px;
        fill: #ecffef;
      }}
      .sub {{
        font-family: 'JetBrains Mono','Fira Code','Courier New',monospace;
        font-weight: 500;
        font-size: 17px;
        letter-spacing: 4px;
        fill: #8af3ad;
      }}
      .tag {{
        font-family: 'JetBrains Mono','Fira Code','Courier New',monospace;
        font-weight: 500;
        font-size: 13px;
        fill: #3fd47a;
        opacity: 0.85;
      }}
      .tag-lg {{ font-size: 14px; }}
      .cursor {{ fill: #6cf3a4; }}
    ]]></style>
  </defs>

  <!-- background -->
  <rect width="{W}" height="{H}" fill="url(#bg)"/>

  <!-- digital rain -->
  <g>
{columns_svg}
  </g>

  <!-- vignette + center shade so the title stays readable -->
  <rect width="{W}" height="{H}" fill="url(#vignette)"/>
  <rect width="{W}" height="{H}" fill="url(#centerShade)"/>
  <rect width="{W}" height="{H}" fill="url(#scanlines)"/>

  <!-- top-left terminal tag -->
  <g transform="translate(44, 44)" class="tag tag-lg">
    <text x="0" y="0">&gt; init binmushan.profile</text>
    <text x="0" y="20" opacity="0.7">&gt; status: online &#183; learning &#183; shipping</text>
  </g>

  <!-- top-right system tag -->
  <g transform="translate({W-44}, 44)" class="tag" text-anchor="end">
    <text x="0" y="0">[ SEUSL // BSc ICT ]</text>
    <text x="0" y="18" opacity="0.65">v.2026 &#183; sri lanka</text>
  </g>

  <!-- corner brackets -->
  <g stroke="#5fe48f" stroke-width="1.6" fill="none" opacity="0.6">
    <path d="M28 28 L28 62 M28 28 L62 28"/>
    <path d="M{W-28} 28 L{W-28} 62 M{W-28} 28 L{W-62} 28"/>
    <path d="M28 {H-28} L28 {H-62} M28 {H-28} L62 {H-28}"/>
    <path d="M{W-28} {H-28} L{W-28} {H-62} M{W-28} {H-28} L{W-62} {H-28}"/>
  </g>

  <!-- title -->
  <g filter="url(#softGlow)">
    <text x="{W/2}" y="{H/2 + 12}" text-anchor="middle" class="title">BIN MUSHAN</text>
  </g>
  <text x="{W/2}" y="{H/2 + 56}" text-anchor="middle" class="sub">SOFTWARE DEV &#160;&#183;&#160; WEB &#160;&#183;&#160; DESIGN &#160;&#183;&#160; AUTOMATION</text>

  <!-- blinking cursor next to subtitle -->
  <rect x="{W/2 + 372}" y="{H/2 + 42}" width="12" height="18" class="cursor">
    <animate attributeName="opacity" values="1;1;0;0" keyTimes="0;0.5;0.5;1" dur="1.1s" repeatCount="indefinite"/>
  </rect>
</svg>
"""

out = Path(__file__).parent / "matrix-banner.svg"
out.write_text(svg, encoding="utf-8")
print(f"wrote {out}  ({out.stat().st_size} bytes, {N_COLS} columns)")
