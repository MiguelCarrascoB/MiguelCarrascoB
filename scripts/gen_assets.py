"""Generate the profile README images.

Usage: python gen.py <out_dir> <router_results.json> <qwen_ui.png> <clef_console.gif>

Needs plexsans.ttf, plexmono.ttf and plexmono-med.ttf next to this script
(IBM Plex Sans variable and Plex Mono Regular/Medium from github.com/google/fonts,
ofl/ibmplexsans and ofl/ibmplexmono) and: pip install fonttools brotli pillow

Writes header-{light,dark}.svg, router-growth-{light,dark}.svg, qwen-ui.png and
clef-console.gif. Every number drawn comes from the user's repos:
  header readout  -> clef docs/screenshots/classify-dark.png (92.1 / 5.4 / 2.5 %, 206 ms)
  growth chart    -> laya-self-evolving-router results/results-v3-full.json
"""

from __future__ import annotations

import base64
import io
import json
import shutil
import sys
from pathlib import Path

from fontTools import subset
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer

HERE = Path(__file__).parent

THEMES = {
    "light": {"fg": "#1f2328", "muted": "#59636e", "faint": "#d1d9e0", "panel": "#f6f8fa",
              "accent": "#0969da", "track": "#e6eaef", "amber": "#bc4c00"},
    "dark": {"fg": "#e6edf3", "muted": "#9198a1", "faint": "#3d444d", "panel": "#151b23",
             "accent": "#4493f8", "track": "#262c36", "amber": "#f0883e"},
}


def font_face(family: str, ttf: Path, text: str, wght: int | None = None) -> str:
    font = TTFont(ttf)
    if wght is not None and "fvar" in font:
        font = instancer.instantiateVariableFont(font, {"wght": wght, "wdth": 100})
    opts = subset.Options()
    opts.flavor = "woff2"
    opts.layout_features = ["kern", "liga", "tnum"]
    opts.name_IDs = []
    sub = subset.Subsetter(opts)
    sub.populate(text=text)
    sub.subset(font)
    buf = io.BytesIO()
    font.flavor = "woff2"
    font.save(buf)
    b64 = base64.b64encode(buf.getvalue()).decode()
    return f"@font-face{{font-family:'{family}';src:url(data:font/woff2;base64,{b64}) format('woff2')}}"


# ---------------------------------------------------------------- header

NAME = "Miguel Carrasco Bueno"
ROLE = "AI / LLM engineer"
TAGLINE = "Serving, routing and training small decision models"
PROMPT = "Checkout is down, orders blocked"
ROWS = [("technical", 0.921), ("billing", 0.054), ("account", 0.025)]
FOOT = "clef · RX 7900 XTX · 206 ms"


def header(theme: str) -> str:
    c = THEMES[theme]
    sans_text = NAME + ROLE + TAGLINE
    mono_text = PROMPT + "".join(r for r, _ in ROWS) + "0123456789.%" + FOOT + '"$ classify'
    css = (
        font_face("Plex Sans SB", HERE / "plexsans.ttf", sans_text, 600)
        + font_face("Plex Sans", HERE / "plexsans.ttf", sans_text, 400)
        + font_face("Plex Mono", HERE / "plexmono.ttf", mono_text)
        + font_face("Plex Mono M", HERE / "plexmono-med.ttf", mono_text)
        + ".n{font:600 50px 'Plex Sans SB',system-ui,sans-serif;letter-spacing:-.5px}"
        + ".r{font:400 25px 'Plex Sans',system-ui,sans-serif}"
        + ".t{font:400 19px 'Plex Sans',system-ui,sans-serif}"
        + ".m{font:400 17px 'Plex Mono',ui-monospace,monospace}"
        + ".mm{font:500 17px 'Plex Mono M',ui-monospace,monospace}"
        + ".bar{transform-box:fill-box;transform-origin:left;animation:grow 1.1s cubic-bezier(.2,.7,.2,1) both}"
        + ".b2{animation-delay:.15s}.b3{animation-delay:.3s}"
        + ".v{animation:fade .5s ease-out both;animation-delay:.9s}"
        + "@keyframes grow{from{transform:scaleX(0)}to{transform:scaleX(1)}}"
        + "@keyframes fade{from{opacity:0}to{opacity:1}}"
        + "@media (prefers-reduced-motion:reduce){.bar,.v{animation:none}}"
    )
    W, H = 1200, 290
    px, py, pw, ph = 640, 30, 520, 232  # readout panel
    bx, bw = px + 140, 270  # bar x and full width
    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" '
        f'aria-label="{NAME}, {ROLE}. Example clef output: technical 92.1%, billing 5.4%, account 2.5%.">',
        f"<style>{css}</style>",
        # left: identity
        f'<text x="40" y="126" class="n" fill="{c["fg"]}">{NAME}</text>',
        f'<text x="42" y="172" class="r" fill="{c["accent"]}">{ROLE}</text>',
        f'<text x="42" y="212" class="t" fill="{c["muted"]}">{TAGLINE}</text>',
        # right: decision readout panel
        f'<rect x="{px}" y="{py}" width="{pw}" height="{ph}" rx="12" fill="{c["panel"]}" stroke="{c["faint"]}"/>',
        f'<text x="{px + 22}" y="{py + 38}" class="m"><tspan fill="{c["muted"]}">$ classify </tspan>'
        f'<tspan fill="{c["fg"]}">"{PROMPT}"</tspan></text>',
    ]
    for i, (label, p) in enumerate(ROWS):
        y = py + 88 + i * 36
        top = i == 0
        out.append(f'<text x="{px + 22}" y="{y + 6}" class="{"mm" if top else "m"}" '
                   f'fill="{c["fg"] if top else c["muted"]}">{label}</text>')
        out.append(f'<rect x="{bx}" y="{y - 7}" width="{bw}" height="12" rx="6" fill="{c["track"]}"/>')
        out.append(f'<rect class="bar b{i + 1}" x="{bx}" y="{y - 7}" width="{max(bw * p, 6):.1f}" height="12" rx="6" '
                   f'fill="{c["accent"] if top else c["faint"]}"/>')
        out.append(f'<text class="v {"mm" if top else "m"}" x="{px + pw - 22}" y="{y + 6}" text-anchor="end" '
                   f'fill="{c["fg"] if top else c["muted"]}">{p * 100:.1f}%</text>')
    out.append(f'<line x1="{px + 22}" y1="{py + ph - 48}" x2="{px + pw - 22}" y2="{py + ph - 48}" stroke="{c["faint"]}"/>')
    out.append(f'<text x="{px + 22}" y="{py + ph - 20}" class="m" fill="{c["muted"]}">{FOOT}</text>')
    out.append("</svg>")
    return "\n".join(out) + "\n"


# ---------------------------------------------------------------- growth chart

WINDOW = 50


def growth(theme: str, results: dict) -> str:
    c = THEMES[theme]
    seen, ev = set(), []
    for e in results["events"]:
        if e["id"] not in seen:
            seen.add(e["id"])
            ev.append(e)
    rate, cats = [], []
    for i, e in enumerate(ev):
        win = ev[max(0, i - WINDOW + 1): i + 1]
        rate.append(sum(1 for w in win if w["route"] == "other") / len(win))
        cats.append(e["categories_at_route"])
    n, cap = len(ev), max(cats)
    top = -(-cap // 10) * 10

    text = "0123456789%other categories prompts seen in registry routed to"
    css = (font_face("Plex Sans", HERE / "plexsans.ttf", text + "ACDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz ()·,", 400)
           + ".a{font:400 22px 'Plex Sans',system-ui,sans-serif}"
           + ".l{font:400 26px 'Plex Sans',system-ui,sans-serif}")
    W, H = 1000, 580
    x0, x1, y0, y1 = 70, 930, 110, 500

    def pth(vals, vmax):
        return "M" + " L".join(
            f"{x0 + (x1 - x0) * i / (n - 1):.1f},{y1 - (y1 - y0) * v / vmax:.1f}" for i, v in enumerate(vals))

    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" '
        f'aria-label="Cold start: the registry grows from 0 to {cap} categories while the share of prompts '
        f'routed to other falls from 100% to about a third.">',
        f"<style>{css}</style>",
        f'<rect width="{W}" height="{H}" rx="18" fill="{c["panel"]}"/>',
    ]
    for frac in (0, 0.5, 1):
        y = y1 - (y1 - y0) * frac
        out.append(f'<line x1="{x0}" y1="{y:.1f}" x2="{x1}" y2="{y:.1f}" stroke="{c["faint"]}"/>')
        out.append(f'<text x="{x0 - 12}" y="{y + 8:.1f}" text-anchor="end" class="a" fill="{c["amber"]}">{frac * 100:.0f}%</text>')
        out.append(f'<text x="{x1 + 12}" y="{y + 8:.1f}" class="a" fill="{c["accent"]}">{frac * top:.0f}</text>')
    out.append(f'<path d="{pth(cats, top)}" fill="none" stroke="{c["accent"]}" stroke-width="4" stroke-linejoin="round"/>')
    out.append(f'<path d="{pth(rate, 1.0)}" fill="none" stroke="{c["amber"]}" stroke-width="4" stroke-linejoin="round"/>')
    out.append(f'<text x="{x0}" y="62" class="l" fill="{c["amber"]}">routed to other</text>')
    out.append(f'<text x="{x1}" y="62" text-anchor="end" class="l" fill="{c["accent"]}">categories in registry</text>')
    out.append(f'<text x="{x0}" y="{y1 + 44}" class="a" fill="{c["muted"]}">0</text>')
    out.append(f'<text x="{x1}" y="{y1 + 44}" text-anchor="end" class="a" fill="{c["muted"]}">{n} prompts seen</text>')
    out.append("</svg>")
    return "\n".join(out) + "\n"


def main() -> None:
    out, results, qwen_png, clef_gif = (Path(a) for a in sys.argv[1:5])
    out.mkdir(parents=True, exist_ok=True)
    data = json.loads(results.read_text(encoding="utf-8"))
    for t in THEMES:
        (out / f"header-{t}.svg").write_text(header(t), encoding="utf-8")
        (out / f"router-growth-{t}.svg").write_text(growth(t, data), encoding="utf-8")

    from PIL import Image  # crop the qwen UI to the prompt + result panels
    im = Image.open(qwen_png).convert("RGB")
    crop = im.crop((24, 74, 1350, 850))
    crop = crop.resize((1000, round(1000 * crop.height / crop.width)), Image.LANCZOS)
    crop.save(out / "qwen-ui.png", optimize=True)
    shutil.copyfile(clef_gif, out / "clef-console.gif")
    for f in sorted(out.iterdir()):
        print(f"{f.name:28} {f.stat().st_size / 1024:7.1f} KB")


if __name__ == "__main__":
    main()
