"""
Generates Matrix-style green digital-rain SVGs for the README.

Outputs:
  assets/matrix-banner.svg  — tall hero with name + subtitle
  assets/matrix-footer.svg  — slim footer with closing tagline

The SVGs use native SMIL <animateTransform> so they animate as an <img src=...>
inside GitHub README (no CSS-in-img required).
"""

from __future__ import annotations

import random
from dataclasses import dataclass
from pathlib import Path

GLYPHS = (
    "01アァカサタナハマヤャラワガザダバパイィキシチニヒミリヰギジヂビピウゥクスツヌ"
    "フムユュルグズブヅプエェケセテネヘメレヱゲゼデベペオォコソトノホモヨョロヲゴゾ"
    "01<>/\\|+-*=#@$%&{}[]"
)


@dataclass
class Layout:
    name: str
    width: int
    height: int
    col_w: int
    char_h: int
    chars_per_col: int
    title: str
    title_size: int
    title_letter_spacing: int
    subtitle: str
    subtitle_size: int
    subtitle_letter_spacing: int
    top_left_lines: tuple[str, ...]
    top_right_lines: tuple[str, ...]
    show_cursor: bool
    seed: int


HERO = Layout(
    name="matrix-banner.svg",
    width=1280,
    height=300,
    col_w=16,
    char_h=16,
    chars_per_col=18,
    title="BIN MUSHAN",
    title_size=92,
    title_letter_spacing=6,
    subtitle="SOFTWARE DEV \u00a0\u00b7\u00a0 WEB \u00a0\u00b7\u00a0 DESIGN \u00a0\u00b7\u00a0 AUTOMATION",
    subtitle_size=17,
    subtitle_letter_spacing=4,
    top_left_lines=(
        "&gt; init binmushan.profile",
        "&gt; status: online \u00b7 learning \u00b7 shipping",
    ),
    top_right_lines=(
        "[ SEUSL // BSc ICT ]",
        "v.2026 \u00b7 sri lanka",
    ),
    show_cursor=True,
    seed=7,
)


FOOTER = Layout(
    name="matrix-footer.svg",
    width=1280,
    height=160,
    col_w=16,
    char_h=15,
    chars_per_col=10,
    title="BUILD  \u00b7  DESIGN  \u00b7  AUTOMATE  \u00b7  LEAD",
    title_size=32,
    title_letter_spacing=4,
    subtitle="one commit  \u00b7  one workflow  \u00b7  one team  \u2014  at a time",
    subtitle_size=13,
    subtitle_letter_spacing=2,
    top_left_lines=("&gt; end_of_transmission",),
    top_right_lines=("\u00a9 2026 binmushan",),
    show_cursor=True,
    seed=13,
)


def _esc(ch: str) -> str:
    if ch == "<":
        return "&lt;"
    if ch == ">":
        return "&gt;"
    if ch == "&":
        return "&amp;"
    return ch


def rain_columns(layout: Layout) -> str:
    rng = random.Random(layout.seed)
    n_cols = layout.width // layout.col_w
    start_y = -layout.chars_per_col * layout.char_h
    end_y = layout.height + layout.chars_per_col * layout.char_h

    out: list[str] = []
    for i in range(n_cols):
        x = i * layout.col_w + layout.col_w // 2
        dur = round(rng.uniform(3.6, 7.5), 2)
        delay = round(rng.uniform(-7.0, 0.0), 2)

        parts: list[str] = []
        for k in range(layout.chars_per_col):
            ch = _esc(rng.choice(GLYPHS))
            y = k * layout.char_h
            if k == 0:
                cls = "head"
            elif k <= 2:
                cls = "near"
            else:
                cls = f"t{min(k, 9)}"
            parts.append(f'<text x="0" y="{y}" class="{cls}">{ch}</text>')

        glyphs = "".join(parts)
        out.append(
            f'<g class="rain" transform="translate({x},{start_y})">'
            f"{glyphs}"
            f'<animateTransform attributeName="transform" type="translate" '
            f'from="{x},{start_y}" to="{x},{end_y}" '
            f'dur="{dur}s" begin="{delay}s" repeatCount="indefinite"/>'
            f"</g>"
        )
    return "\n".join(out)


def render(layout: Layout) -> str:
    W, H = layout.width, layout.height
    cx, cy = W / 2, H / 2

    rain = rain_columns(layout)

    tl_lines = "".join(
        f'<text x="0" y="{i * 20}" {"opacity=\"0.7\"" if i > 0 else ""}>{line}</text>'
        for i, line in enumerate(layout.top_left_lines)
    )
    tr_lines = "".join(
        f'<text x="0" y="{i * 18}" {"opacity=\"0.65\"" if i > 0 else ""}>{line}</text>'
        for i, line in enumerate(layout.top_right_lines)
    )

    title_y = cy + (12 if layout.subtitle else 8)
    subtitle_y = cy + 44 if layout.subtitle else None

    cursor = ""
    if layout.show_cursor and subtitle_y is not None:
        # rough subtitle pixel width approximation, monospace-ish
        sub_chars = len(layout.subtitle)
        sub_px = sub_chars * (layout.subtitle_size * 0.62 + layout.subtitle_letter_spacing)
        cursor_x = cx + sub_px / 2 + 14
        cursor = (
            f'<rect x="{cursor_x:.1f}" y="{subtitle_y - 14}" width="10" height="16" class="cursor">'
            f'<animate attributeName="opacity" values="1;1;0;0" keyTimes="0;0.5;0.5;1" '
            f'dur="1.1s" repeatCount="indefinite"/>'
            f'</rect>'
        )

    subtitle_block = (
        f'<text x="{cx}" y="{subtitle_y}" text-anchor="middle" class="sub">{layout.subtitle}</text>'
        if layout.subtitle
        else ""
    )

    return f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="100%" preserveAspectRatio="xMidYMid slice" role="img" aria-label="{layout.title}">
  <defs>
    <linearGradient id="bg-{layout.seed}" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%"  stop-color="#020a05"/>
      <stop offset="55%" stop-color="#01140a"/>
      <stop offset="100%" stop-color="#000604"/>
    </linearGradient>
    <radialGradient id="vignette-{layout.seed}" cx="50%" cy="50%" r="65%">
      <stop offset="55%" stop-color="#000000" stop-opacity="0"/>
      <stop offset="100%" stop-color="#000000" stop-opacity="0.85"/>
    </radialGradient>
    <radialGradient id="centerShade-{layout.seed}" cx="50%" cy="50%" r="42%">
      <stop offset="0%"  stop-color="#000000" stop-opacity="0.85"/>
      <stop offset="55%" stop-color="#000000" stop-opacity="0.55"/>
      <stop offset="100%" stop-color="#000000" stop-opacity="0"/>
    </radialGradient>
    <pattern id="scanlines-{layout.seed}" width="3" height="3" patternUnits="userSpaceOnUse">
      <rect width="3" height="3" fill="transparent"/>
      <rect width="3" height="1" fill="#00ff88" opacity="0.04"/>
    </pattern>
    <filter id="glow-{layout.seed}" x="-20%" y="-50%" width="140%" height="200%">
      <feGaussianBlur stdDeviation="2.4" result="b"/>
      <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <filter id="softGlow-{layout.seed}" x="-20%" y="-50%" width="140%" height="200%">
      <feGaussianBlur stdDeviation="1.2" result="b"/>
      <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <style><![CDATA[
      .rain {{
        font-family: 'JetBrains Mono','Fira Code','Courier New',monospace;
        font-size: 14px;
        font-weight: 600;
      }}
      .head {{ fill: #d6ffe6; filter: url(#glow-{layout.seed}); }}
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
        font-size: {layout.title_size}px;
        letter-spacing: {layout.title_letter_spacing}px;
        fill: #ecffef;
      }}
      .sub {{
        font-family: 'JetBrains Mono','Fira Code','Courier New',monospace;
        font-weight: 500;
        font-size: {layout.subtitle_size}px;
        letter-spacing: {layout.subtitle_letter_spacing}px;
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

  <rect width="{W}" height="{H}" fill="url(#bg-{layout.seed})"/>

  <g>
{rain}
  </g>

  <rect width="{W}" height="{H}" fill="url(#vignette-{layout.seed})"/>
  <rect width="{W}" height="{H}" fill="url(#centerShade-{layout.seed})"/>
  <rect width="{W}" height="{H}" fill="url(#scanlines-{layout.seed})"/>

  <g transform="translate(44, 44)" class="tag tag-lg">
    {tl_lines}
  </g>

  <g transform="translate({W-44}, 44)" class="tag" text-anchor="end">
    {tr_lines}
  </g>

  <g stroke="#5fe48f" stroke-width="1.6" fill="none" opacity="0.6">
    <path d="M28 28 L28 62 M28 28 L62 28"/>
    <path d="M{W-28} 28 L{W-28} 62 M{W-28} 28 L{W-62} 28"/>
    <path d="M28 {H-28} L28 {H-62} M28 {H-28} L62 {H-28}"/>
    <path d="M{W-28} {H-28} L{W-28} {H-62} M{W-28} {H-28} L{W-62} {H-28}"/>
  </g>

  <g filter="url(#softGlow-{layout.seed})">
    <text x="{cx}" y="{title_y}" text-anchor="middle" class="title">{layout.title}</text>
  </g>
  {subtitle_block}
  {cursor}
</svg>
"""


def main() -> None:
    out_dir = Path(__file__).parent
    for layout in (HERO, FOOTER):
        path = out_dir / layout.name
        path.write_text(render(layout), encoding="utf-8")
        print(f"wrote {path}  ({path.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()
