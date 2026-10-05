"""
Generate a Neofetch-style info card SVG that looks like a terminal output.
Features animated line-by-line typewriter/fade-in, key-value colored rows,
traffic light titlebar, and Unix color blocks.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "info-card.svg")

CANVAS_W = 504
CANVAS_H = 524
PAD = 22
TITLEBAR_H = 30

BG = "#0d1117"
BG2 = "#111722"
FRAME = "#30363d"
TITLE_TEXT = "#7d8590"

# Terminal syntax colors
KEY_COLOR = "#58a6ff"       # blue
VAL_COLOR = "#c9d1d9"       # light gray
ACCENT = "#22d3ee"          # cyan
HIGHLIGHT = "#3fb950"       # green
MUTED = "#8b949e"           # muted gray
HEADER_COLOR = "#f0883e"    # orange

lines = [
    ("header", "sandesh@dev-box"),
    ("separator", "-------------"),
    ("OS", "Linux / Arch x86_64"),
    ("Role", "Full-Stack Software Engineer"),
    ("Focus", "Web Apps • Backend APIs • Mobile"),
    ("Backend", "Python, Django, PHP, REST APIs"),
    ("Frontend", "TypeScript, React, Expo Router, Tailwind"),
    ("Database", "PostgreSQL, MySQL, SQLite"),
    ("Location", "Nepal 🇳🇵"),
    ("Status", "Building scalable real-world products"),
    ("Uptime", "Passionate coder • Continuous learner"),
]

palette_colors = ["#ff5f56", "#ffbd2e", "#27c93f", "#58a6ff", "#bc8cff", "#39d353", "#22d3ee", "#e6edf3"]

def generate_info_card():
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{CANVAS_W}" height="{CANVAS_H}" '
        f'viewBox="0 0 {CANVAS_W} {CANVAS_H}" font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace">',
        '<style>',
        '@keyframes slideIn {',
        '  0% { opacity: 0; transform: translateX(-10px); }',
        '  100% { opacity: 1; transform: translateX(0); }',
        '}',
        '.row { opacity: 0; animation: slideIn 0.38s ease-out forwards; }',
        '</style>',
        '<defs>',
        f'<linearGradient id="ibg" x1="0" y1="0" x2="0" y2="1">',
        f'<stop offset="0" stop-color="{BG2}"/><stop offset="1" stop-color="{BG}"/>',
        '</linearGradient>',
        '</defs>',
        f'<rect width="{CANVAS_W}" height="{CANVAS_H}" rx="12" fill="url(#ibg)"/>',
        f'<rect x="0.5" y="0.5" width="{CANVAS_W-1}" height="{CANVAS_H-1}" rx="12" fill="none" stroke="{FRAME}" stroke-width="1"/>',
        f'<line x1="0" y1="{TITLEBAR_H}" x2="{CANVAS_W}" y2="{TITLEBAR_H}" stroke="{FRAME}"/>',
    ]

    # Traffic light dots
    for i, dot in enumerate(["#ff5f56", "#ffbd2e", "#27c93f"]):
        parts.append(f'<circle cx="{PAD + i*16}" cy="{TITLEBAR_H/2}" r="5" fill="{dot}"/>')
    parts.append(f'<text x="{CANVAS_W/2}" y="{TITLEBAR_H/2 + 4}" fill="{TITLE_TEXT}" font-size="12" text-anchor="middle">sandesh@github: ~$ neofetch</text>')

    y_pos = TITLEBAR_H + 34
    line_step = 28
    delay = 0.15

    for item in lines:
        if item[0] == "header":
            parts.append(
                f'<g class="row" style="animation-delay:{delay:.2f}s">'
                f'<text x="{PAD}" y="{y_pos}" fill="{HEADER_COLOR}" font-size="14" font-weight="700">{item[1]}</text>'
                f'</g>'
            )
        elif item[0] == "separator":
            parts.append(
                f'<g class="row" style="animation-delay:{delay:.2f}s">'
                f'<text x="{PAD}" y="{y_pos}" fill="{MUTED}" font-size="13">{item[1]}</text>'
                f'</g>'
            )
        else:
            key, val = item
            parts.append(
                f'<g class="row" style="animation-delay:{delay:.2f}s">'
                f'<text x="{PAD}" y="{y_pos}" font-size="12.5">'
                f'<tspan fill="{KEY_COLOR}" font-weight="600">{key}: </tspan>'
                f'<tspan fill="{VAL_COLOR}">{val}</tspan>'
                f'</text>'
                f'</g>'
            )
        y_pos += line_step
        delay += 0.08

    # Terminal color blocks row at the bottom
    color_box_y = y_pos + 12
    box_size = 20
    box_gap = 8
    parts.append(f'<g class="row" style="animation-delay:{delay:.2f}s">')
    for i, color in enumerate(palette_colors):
        bx = PAD + i * (box_size + box_gap)
        parts.append(f'<rect x="{bx}" y="{color_box_y}" width="{box_size}" height="{box_size}" rx="4" fill="{color}"/>')
    parts.append('</g>')

    # Blinking cursor prompt
    prompt_y = color_box_y + box_size + 28
    parts.append(
        f'<text x="{PAD}" y="{prompt_y}" fill="{MUTED}" font-size="13">'
        f'<tspan fill="{HIGHLIGHT}">sandesh@github</tspan>:<tspan fill="{KEY_COLOR}">~</tspan>$ '
        f'<tspan fill="{VAL_COLOR}">echo &quot;Let&#39;s collaborate!&quot;</tspan>'
        f'</text>'
    )
    parts.append(
        f'<rect x="{PAD + 276}" y="{prompt_y - 12}" width="8" height="15" fill="{VAL_COLOR}">'
        f'<animate attributeName="opacity" values="1;1;0;0" keyTimes="0;0.5;0.51;1" dur="1s" repeatCount="indefinite"/>'
        f'</rect>'
    )

    parts.append('</svg>')
    svg = "".join(parts)
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"wrote {OUT} ({len(svg)} bytes)")

if __name__ == "__main__":
    generate_info_card()
