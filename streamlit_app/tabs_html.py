# HTML for the "How it works" and "Model" tabs, in the same style as the game.

import base64
import math
import random


def svg_img(svg, style=""):
    # st.html removes inline <svg> tags, so drawings are embedded as images
    if "xmlns" not in svg:
        svg = svg.replace("<svg ", '<svg xmlns="http://www.w3.org/2000/svg" ', 1)
    data = base64.b64encode(svg.encode("utf-8")).decode("ascii")
    return f'<img src="data:image/svg+xml;base64,{data}" style="{style}" alt="">'


# KNN result from the Grid Search in Test2.ipynb (k=75, Manhattan distance, distance weights)
KNN_TUNED_ACCURACY = 0.6576

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Oswald:wght@500;600&family=Inter:wght@400;500;600&display=swap');
.bm { --panel:#15171c; --panel2:#1c1f26; --border:#2a2e37; --text:#eceef2; --muted:#8b919e; --gold:#f0b429; --slate:#5b6b85;
      --good:#4cc38a; --bad:#e5484d; color:var(--text); font-family:Inter, system-ui, sans-serif; max-width:1120px; margin:0 auto 40px; }
.bm h2, .bm h3, .bm .num { font-family:Oswald, "Arial Narrow", sans-serif; font-weight:600; letter-spacing:.5px; }
.bm h2 { font-size:26px; margin:34px 0 4px; }
.bm .lead { color:var(--muted); font-size:14px; margin:0 0 16px; }
.bm .hero { position:relative; overflow:hidden; border-radius:10px; padding:34px 36px; margin-top:8px;
            background:linear-gradient(115deg, #2a1d10 0%, #3b2914 45%, #1a1714 100%); border:1px solid #3a2c1c; }
.bm .hero { height:250px; box-sizing:border-box; border-radius:16px; }
.bm .hero img.art { position:absolute; right:0; top:0; height:100%; width:auto;
                    -webkit-mask-image:linear-gradient(90deg, transparent 0, #000 30%); mask-image:linear-gradient(90deg, transparent 0, #000 30%); }
.bm .hero > *:not(img) { position:relative; max-width:560px; }
.bm .hero > .chips { max-width:none; flex-wrap:nowrap; }
@media (max-width: 900px) { .bm .hero img.art { display:none; } }
.bm .eyebrow { color:var(--gold); font-size:12px; letter-spacing:3px; text-transform:uppercase; font-weight:600; }
.bm .hero h1 { font-family:Oswald, "Arial Narrow", sans-serif; font-size:44px; margin:6px 0 8px; letter-spacing:1px; color:#fff; }
.bm .hero p { color:#d9cfc2; max-width:620px; font-size:15px; line-height:1.6; margin:0; }
.bm .chips { display:flex; flex-wrap:wrap; gap:8px; margin-top:16px; }
.bm .chip { font-size:12px; padding:6px 12px; border-radius:20px; white-space:nowrap; color:#f1e6cf;
            background:rgba(255,255,255,.07); border:1px solid rgba(255,255,255,.14); backdrop-filter:blur(6px); }
.bm .grid { display:grid; gap:14px; }
.bm .g4 { grid-template-columns:repeat(4, 1fr); }
.bm .g3 { grid-template-columns:repeat(3, 1fr); }
.bm .g2 { grid-template-columns:1.1fr 1fr; }
@media (max-width: 900px) { .bm .g4, .bm .g3, .bm .g2 { grid-template-columns:1fr 1fr; } }
/* Soft glass cards */
.bm .card { position:relative; padding:20px 20px 18px; border-radius:16px;
            background:linear-gradient(160deg, rgba(255,255,255,.065), rgba(255,255,255,.018));
            border:1px solid rgba(255,255,255,.08); backdrop-filter:blur(10px);
            box-shadow:0 10px 30px rgba(0,0,0,.28), inset 0 1px 0 rgba(255,255,255,.06); }
.bm .step .n { font-family:Oswald, "Arial Narrow", sans-serif; font-size:38px; color:#3a3f4a; position:absolute; right:16px; top:8px; }
.bm .icon { width:42px; height:42px; border-radius:50%; display:grid; place-items:center; margin-bottom:12px;
            background:rgba(240,180,41,.1); border:1px solid rgba(240,180,41,.22); }
.bm .icon img { width:22px; height:22px; display:block; }
.bm .step h3 { font-size:18px; margin:0 0 6px; }
.bm .step p { color:#b9bec8; font-size:13px; line-height:1.55; margin:0; }
.bm .map { display:grid; grid-template-columns:1fr 34px 1.2fr; align-items:center; gap:10px; padding:12px 16px; border-bottom:1px solid var(--border); }
.bm .map:last-child { border-bottom:0; }
.bm .map .what { font-size:14px; }
.bm .map .what small { display:block; color:var(--muted); font-size:12px; margin-top:2px; }
.bm .map .arrow { color:var(--gold); text-align:center; }
.bm .code { font-family:ui-monospace, Consolas, monospace; font-size:12px; padding:3px 9px; border-radius:20px; background:rgba(240,180,41,.08); border:1px solid rgba(240,180,41,.2); color:#e8c46a; margin:2px 4px 2px 0; display:inline-block; }
.bm .verdict { background:rgba(255,255,255,.04); border:1px solid rgba(255,255,255,.08); border-radius:12px; padding:10px 12px; }
.bm .verdict .who { font-size:11px; color:var(--muted); letter-spacing:1px; text-transform:uppercase; }
.bm .verdict .what { font-family:Oswald, "Arial Narrow", sans-serif; font-size:22px; }
.bm .pill { display:inline-block; font-size:12px; padding:5px 12px; border-radius:20px; margin:4px 6px 0 0; }
.bm .pill.up { background:rgba(76,195,138,.12); color:#8fe0b6; border:1px solid rgba(76,195,138,.35); }
.bm .pill.down { background:rgba(229,72,77,.12); color:#f3a1a4; border:1px solid rgba(229,72,77,.35); }
.bm .formula { display:flex; flex-wrap:wrap; align-items:center; gap:8px; margin-top:12px; font-size:13px; color:#b9bec8; }
.bm .formula .box { padding:6px 12px; border-radius:20px; background:rgba(255,255,255,.05); border:1px solid rgba(255,255,255,.1); }
.bm .formula .res { padding:6px 14px; border-radius:20px; background:var(--gold); color:#111; font-weight:600; }
.bm .kpi .label { color:var(--muted); font-size:12px; text-transform:uppercase; letter-spacing:1px; }
.bm .kpi .num { font-size:38px; margin-top:4px; }
.bm .kpi .sub { color:#b9bec8; font-size:12px; margin-top:2px; }
.bm .bars .row { display:grid; grid-template-columns:190px 1fr 60px; align-items:center; gap:12px; margin:12px 0; }
.bm .bars .name { font-size:14px; }
.bm .bars .name small { display:block; color:var(--muted); font-size:11px; }
.bm .track { height:14px; background:rgba(255,255,255,.05); border-radius:7px; overflow:hidden; border:1px solid rgba(255,255,255,.06); }
.bm .fill { height:100%; border-radius:7px; }
.bm .bars .val { font-family:Oswald, "Arial Narrow", sans-serif; font-size:18px; text-align:right; }
.bm .wt { display:grid; grid-template-columns:230px 1fr 1fr; align-items:center; gap:0; margin:6px 0; font-size:13px; }
.bm .wt .lbl { color:#d5d9e0; padding-right:12px; text-align:right; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; }
.bm .wt .lbl small { color:var(--muted); }
.bm .wt .neg { display:flex; justify-content:flex-end; border-right:1px solid #3a3f4a; }
.bm .wt .pos { display:flex; border-left:1px solid #3a3f4a; }
.bm .wt .b { height:16px; }
.bm table.shots { width:100%; border-collapse:collapse; font-size:13px; }
.bm table.shots th { text-align:left; color:var(--muted); font-weight:500; font-size:11px; text-transform:uppercase; letter-spacing:1px; padding:8px 10px; border-bottom:1px solid var(--border); }
.bm table.shots td { padding:9px 10px; border-bottom:1px solid #1f222a; }
.bm table.shots tr:last-child td { border-bottom:0; }
.bm .mini { display:flex; align-items:center; gap:10px; }
.bm .mini .track { width:140px; height:8px; }
.bm .legend { display:flex; align-items:center; gap:8px; color:var(--muted); font-size:12px; margin-top:10px; }
.bm .legend .scale { width:140px; height:8px; border-radius:4px; background:linear-gradient(90deg, #2b3446, #f0b429); }
.bm .note { color:var(--muted); font-size:12px; margin-top:10px; line-height:1.5; }
</style>
"""

ICONS = {
    "ball": '<svg viewBox="0 0 24 24" fill="none" stroke="#f0b429" stroke-width="1.8"><circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3v18M5.6 5.6c3.5 3.5 3.5 9.3 0 12.8M18.4 5.6c-3.5 3.5-3.5 9.3 0 12.8"/></svg>',
    "tap": '<svg viewBox="0 0 24 24" fill="none" stroke="#f0b429" stroke-width="1.8"><path d="M9 11V5a2 2 0 0 1 4 0v6"/><path d="M13 10a2 2 0 0 1 4 0v1a2 2 0 0 1 4 0v4a6 6 0 0 1-6 6h-2a6 6 0 0 1-5-2.7L5.3 15a2 2 0 0 1 3.2-2.4L9 13"/></svg>',
    "chip": '<svg viewBox="0 0 24 24" fill="none" stroke="#f0b429" stroke-width="1.8"><rect x="6" y="6" width="12" height="12" rx="2"/><path d="M9 2v4M15 2v4M9 18v4M15 18v4M2 9h4M2 15h4M18 9h4M18 15h4"/><path d="M10 10h4v4h-4z"/></svg>',
    "board": '<svg viewBox="0 0 24 24" fill="none" stroke="#f0b429" stroke-width="1.8"><rect x="2" y="5" width="20" height="14" rx="2"/><path d="M12 5v14M6 10v4M16 10h3v2h-3v2h3"/></svg>',
}

def hoop_art():
    # Realistic basket for the page headers: arena lights, glass backboard, rim with net, ball and a wooden floor
    rnd = random.Random(9)
    vx, vy, floor_y = 280, 150, 215
    out = ["""<svg viewBox="0 0 560 320" width="560" height="320">
<defs>
<linearGradient id="bg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0e0b08"/><stop offset="1" stop-color="#2b1c0f"/></linearGradient>
<radialGradient id="spot" cx=".5" cy=".28" r=".55"><stop offset="0" stop-color="#ffe9c4" stop-opacity=".38"/><stop offset="1" stop-color="#ffe9c4" stop-opacity="0"/></radialGradient>
<linearGradient id="floor" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#7d4f25"/><stop offset="1" stop-color="#c99560"/></linearGradient>
<linearGradient id="glass" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#fff" stop-opacity=".26"/><stop offset=".5" stop-color="#fff" stop-opacity=".07"/><stop offset="1" stop-color="#fff" stop-opacity=".16"/></linearGradient>
<radialGradient id="ball" cx=".35" cy=".3" r=".75"><stop offset="0" stop-color="#f8ab66"/><stop offset=".55" stop-color="#d9661f"/><stop offset="1" stop-color="#7f3210"/></radialGradient>
<linearGradient id="pole" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#2a2f38"/><stop offset=".5" stop-color="#5a6270"/><stop offset="1" stop-color="#2a2f38"/></linearGradient>
<radialGradient id="vig" cx=".5" cy=".45" r=".75"><stop offset=".55" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".55"/></radialGradient>
<filter id="blur"><feGaussianBlur stdDeviation="1.6"/></filter><filter id="soft"><feGaussianBlur stdDeviation="4"/></filter>
</defs>
<rect width="560" height="320" fill="url(#bg)"/>"""]
    # Crowd in the stands, out of focus
    crowd = []
    for row in range(16):
        y = 18 + row * 12
        x = rnd.random() * 8
        while x < 560:
            light = 10 + rnd.random() * 22 + row
            crowd.append(f'<circle cx="{x:.0f}" cy="{y + rnd.random() * 4:.0f}" r="{3 + rnd.random() * 1.5:.1f}" '
                         f'fill="hsl({rnd.random() * 360:.0f},{12 + rnd.random() * 20:.0f}%,{light:.0f}%)"/>')
            x += 9 + rnd.random() * 5
    out.append(f'<g filter="url(#blur)" opacity=".75">{"".join(crowd)}</g>')
    out.append('<rect width="560" height="320" fill="url(#spot)"/>')
    # Floor boards running toward the camera
    out.append(f'<polygon points="0,{floor_y} 560,{floor_y} 560,320 0,320" fill="url(#floor)"/>')
    k = (320 - vy) / (floor_y - vy)
    for n in range(-34, 35):
        xb, xb2 = vx + n * 17, vx + (n + 1) * 17
        xt, xt2 = vx + (xb - vx) / k, vx + (xb2 - vx) / k
        tone = "255,232,195" if rnd.random() > .5 else "90,50,20"
        out.append(f'<polygon points="{xt:.1f},{floor_y} {xt2:.1f},{floor_y} {xb2:.1f},320 {xb:.1f},320" '
                   f'fill="rgba({tone},{rnd.random() * .09:.3f})"/>')
        out.append(f'<line x1="{xt:.1f}" y1="{floor_y}" x2="{xb:.1f}" y2="320" stroke="rgba(70,38,14,.35)" stroke-width=".7"/>')
    # Painted lane, baseline and restricted area
    lane_l = vx + (220 - vx) * (320 - vy) / (232 - vy)
    lane_r = vx + (340 - vx) * (320 - vy) / (232 - vy)
    out.append(f'<polygon points="220,232 340,232 {lane_r:.1f},320 {lane_l:.1f},320" fill="#5a2c10" opacity=".4"/>')
    out.append(f'<g stroke="#f6f1e7" stroke-width="2.4" fill="none" opacity=".88"><line x1="0" y1="232" x2="560" y2="232"/>'
               f'<line x1="220" y1="232" x2="{lane_l:.1f}" y2="320"/><line x1="340" y1="232" x2="{lane_r:.1f}" y2="320"/>'
               f'<path d="M226 248A54 13 0 0 0 334 248"/></g>')
    # Light reflected on the varnish and the ball's shadow
    out.append('<ellipse cx="280" cy="262" rx="120" ry="18" fill="#ffe9c4" opacity=".14" filter="url(#soft)"/>')
    out.append('<ellipse cx="306" cy="268" rx="26" ry="5" fill="#000" opacity=".35" filter="url(#soft)"/>')
    # Support arm and backboard
    out.append('<rect x="272" y="0" width="16" height="56" fill="url(#pole)"/>'
               '<path d="M262 0L276 50M298 0L284 50" stroke="#3b424e" stroke-width="5"/>')
    out.append('<rect x="183" y="50" width="194" height="110" rx="3" fill="url(#glass)" stroke="#f2f2f2" stroke-width="5"/>'
               '<rect x="244" y="108" width="72" height="50" fill="none" stroke="#f2f2f2" stroke-width="3.5"/>'
               '<line x1="190" y1="58" x2="370" y2="58" stroke="#fff" stroke-opacity=".35" stroke-width="2"/>'
               '<rect x="272" y="158" width="16" height="10" fill="#b8461a"/>')
    # Rim (back half), net and rim (front half)
    out.append('<path d="M242 170A38 9 0 0 1 318 170" fill="none" stroke="#b8461a" stroke-width="5"/>')
    rings = [(38, 170), (31, 190), (25, 208)]
    net = []
    for r in range(len(rings) - 1):
        (r1, y1), (r2, y2) = rings[r], rings[r + 1]
        for n in range(14):
            a1 = math.pi * n / 13
            x1p, y1p = 280 + r1 * math.cos(a1), y1 + 9 * (r1 / 38) * math.sin(a1)
            for a in (math.pi * (n + .5) / 13, math.pi * (n - .5) / 13):
                x2p, y2p = 280 + r2 * math.cos(a), y2 + 9 * (r2 / 38) * math.sin(a)
                net.append(f'<line x1="{x1p:.1f}" y1="{y1p:.1f}" x2="{x2p:.1f}" y2="{y2p:.1f}"/>')
    out.append(f'<g stroke="#f4f4f4" stroke-opacity=".85" stroke-width="1.3">{"".join(net)}</g>')
    out.append('<path d="M242 170A38 9 0 0 0 318 170" fill="none" stroke="#e0561b" stroke-width="5"/>')
    # Ball dropping toward the rim
    out.append('<circle cx="306" cy="116" r="27" fill="url(#ball)"/>'
               '<g fill="none" stroke="#3a1606" stroke-width="1.8"><path d="M279 116h54"/><path d="M306 89c-11 9-11 45 0 54"/>'
               '<path d="M285 98c9 6 9 30 0 36"/><path d="M327 98c-9 6-9 30 0 36"/></g>'
               '<ellipse cx="296" cy="104" rx="8" ry="5" fill="#fff" opacity=".22"/>')
    out.append('<rect width="560" height="320" fill="url(#vig)"/></svg>')
    return svg_img("".join(out)).replace("<img ", '<img class="art" ', 1)


HERO_ART = hoop_art()


def _mix(rate, low=0.30, high=0.62):
    # Color from slate (low accuracy) to gold (high accuracy)
    t = max(0.0, min(1.0, (rate - low) / (high - low)))
    a, b = (0x2B, 0x34, 0x46), (0xF0, 0xB4, 0x29)
    return "#" + "".join(f"{round(a[i] + (b[i] - a[i]) * t):02x}" for i in range(3))


def _pct(v):
    return f"{v * 100:.0f}%"


def court_zones_svg(zones):
    r = {k: v["made_rate"] for k, v in zones.items()}
    label = lambda x, y, z, size=18: (f'<text x="{x}" y="{y}" text-anchor="middle" font-family="Arial Narrow, Arial, sans-serif" font-weight="bold" '
                                       f'font-size="{size}" fill="#fff" stroke="#000" stroke-opacity=".35" stroke-width="3" paint-order="stroke">{_pct(r[z])}</text>')
    return svg_img(f"""<svg viewBox="0 0 500 470" width="500" height="470">
<rect width="500" height="470" fill="{_mix(r['Above the Break 3'])}"/>
<rect x="0" y="0" width="30" height="142" fill="{_mix(r['Left Corner 3'])}"/>
<rect x="470" y="0" width="30" height="142" fill="{_mix(r['Right Corner 3'])}"/>
<path d="M30 0V142A237.5 237.5 0 0 0 470 142V0Z" fill="{_mix(r['Mid-Range'])}"/>
<rect x="170" y="0" width="160" height="190" fill="{_mix(r['In The Paint (Non-RA)'])}"/>
<circle cx="250" cy="52.5" r="40" fill="{_mix(r['Restricted Area'])}"/>
<g fill="none" stroke="rgba(255,255,255,.85)" stroke-width="2.5">
<rect x="1.5" y="1.5" width="497" height="467"/><rect x="170" y="0" width="160" height="190"/>
<path d="M30 0V142A237.5 237.5 0 0 0 470 142V0"/><circle cx="250" cy="190" r="60" stroke-dasharray="8 8"/>
<path d="M210 52.5A40 40 0 0 0 290 52.5"/><path d="M190 470A60 60 0 0 1 310 470"/></g>
<path d="M220 40h60" stroke="#fff" stroke-width="3"/><circle cx="250" cy="52.5" r="7.5" fill="none" stroke="#e0561b" stroke-width="3"/>
{label(250, 90, 'Restricted Area')}{label(250, 170, 'In The Paint (Non-RA)')}{label(105, 150, 'Mid-Range')}{label(395, 150, 'Mid-Range')}
{label(250, 380, 'Above the Break 3', 22)}{label(15, 125, 'Left Corner 3', 11)}{label(485, 125, 'Right Corner 3', 11)}
</svg>""", "width:100%;display:block;border-radius:8px")


def distance_svg(rates):
    rows = [d for d in rates if d["count"] >= 50]
    w, h, pad = 520, 210, 28
    bw = (w - pad) / len(rows)
    out = [f'<svg viewBox="0 0 {w} {h}" width="{w}" height="{h}">']
    for i, d in enumerate(rows):
        bh = d["made_rate"] / 0.7 * (h - 60)
        x, y = pad + i * bw + 3, h - 30 - bh
        out.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{bw - 6:.1f}" height="{bh:.1f}" rx="3" fill="{_mix(d["made_rate"])}"/>')
        out.append(f'<text x="{x + (bw - 6) / 2:.1f}" y="{y - 6:.1f}" text-anchor="middle" font-size="11" fill="#d5d9e0" font-family="Inter, sans-serif">{_pct(d["made_rate"])}</text>')
        out.append(f'<text x="{x + (bw - 6) / 2:.1f}" y="{h - 12}" text-anchor="middle" font-size="11" fill="#8b919e" font-family="Inter, sans-serif">{d["ft"]}</text>')
    out.append(f'<line x1="{pad}" y1="{h - 30}" x2="{w}" y2="{h - 30}" stroke="#3a3f4a"/>')
    out.append(f'<text x="0" y="{h - 12}" font-size="11" fill="#8b919e" font-family="Inter, sans-serif">ft</text></svg>')
    return svg_img("".join(out), "width:100%;display:block")


def how_it_works_html(model):
    m = model["metrics"]
    # A clear example: the model says IN, and the main thing against the shot is its type or distance
    example = next(q for q in model["quiz"] if q["helps"] and q["hurts"] and q["p"] >= .5
                   and q["hurts"].startswith(("Shot type", "Distance")))
    steps = [
        ("ball", "A real shot", "The game picks a shot Kobe really took. It comes from the test set, so the model never saw it while training."),
        ("tap", "You guess", "Look at the spot, the shot type and the game situation, then choose IN or OUT."),
        ("chip", "The model guesses", "Logistic Regression gives a probability. 50% or more means IN, less means OUT."),
        ("board", "The real result", "Kobe takes the shot with its real result from the data. Whoever guessed right scores a point."),
    ]
    cards = "".join(f'<div class="card step wood"><span class="n">0{i + 1}</span><div class="icon">{svg_img(ICONS[ic])}</div>'
                    f'<h3>{t}</h3><p>{d}</p></div>' for i, (ic, t, d) in enumerate(steps))
    mapping = [
        ("Kobe's spot and the distance", "Where he stands on the court", ["loc_x", "loc_y", "shot_distance", "shot_zone_*", "shot_type"]),
        ("The name of the shot", "Jump Shot, Layup, Fadeaway…", ["action_type", "combined_shot_type"]),
        ("Quarter and time left", "Shown under the court", ["period", "time_remaining"]),
        ("The defender's team", "His jersey colors", ["opponent"]),
        ("Kobe's uniform", "Gold at home, purple away", ["home"]),
        ("Kobe's number", "#8 until 2005-06, then #24", ["season_start"]),
        ("Playoffs", "Shown next to the season", ["playoffs"]),
    ]
    rows = "".join(f'<div class="map"><div class="what">{a}<small>{b}</small></div><div class="arrow">&rarr;</div>'
                   f'<div>{"".join(f"<span class=code>{c}</span>" for c in cs)}</div></div>' for a, b, cs in mapping)
    said_in = example["p"] >= .5
    return CSS + f"""
<div class="bm">
  <div class="hero">{HERO_ART}
    <div class="eyebrow">How it works</div>
    <h1>Beat the Model</h1>
    <p>Ten real Kobe Bryant shots. Guess if each one went in and try to beat our model,
       which is right {m['test_accuracy'] * 100:.1f}% of the time on shots it has never seen.</p>
    <div class="chips"><span class="chip">{m['test_rows']:,} test shots</span><span class="chip">15 features</span>
      <span class="chip">Real results only</span></div>
  </div>

  <h2>Four steps</h2>
  <p class="lead">One decision per shot. No controls to learn.</p>
  <div class="grid g4">{cards}</div>

  <h2>From the screen to the model</h2>
  <p class="lead">Everything you see on the court is one of the features the model was trained on.</p>
  <div class="card" style="padding:4px 0">{rows}</div>

  <h2>Why the model said that</h2>
  <p class="lead">After each guess the game shows what pushed the model's answer up and down. A real example:</p>
  <div class="grid g2">
    <div class="card">
      <div style="font-family:Oswald,'Arial Narrow',sans-serif;font-size:20px">{example['action']} &middot; {example['dist']} ft</div>
      <div style="color:var(--muted);font-size:12px;margin:2px 0 12px">Real shot from the test set</div>
      <div class="grid" style="grid-template-columns:1fr 1fr;gap:10px">
        <div class="verdict"><div class="who">Model said</div><div class="what">{'IN' if said_in else 'OUT'} &middot; {_pct(example['p'])}</div></div>
        <div class="verdict"><div class="who">Real result</div><div class="what" style="color:{'var(--good)' if example['made'] else 'var(--bad)'}">{'IN' if example['made'] else 'OUT'}</div></div>
      </div>
      <span class="pill up">Helped: {example['helps']}</span><span class="pill down">Hurt: {example['hurts']}</span>
    </div>
    <div class="card">
      <h3 style="margin:0 0 6px;font-size:18px">How the probability is built</h3>
      <p style="color:#b9bec8;font-size:13px;line-height:1.6;margin:0">Each feature has a weight learned from 20,557 training shots.
        The model adds the weights of the shot's features into one score, then the sigmoid function turns that score into a probability between 0% and 100%.</p>
      <div class="formula"><span class="box">shot type</span>+<span class="box">distance</span>+<span class="box">spot</span>+<span class="box">time</span>+<span class="box">&hellip;</span>
        &rarr;<span class="box">sigmoid</span>&rarr;<span class="res">{_pct(example['p'])}</span></div>
      <p class="note">The biggest positive part is shown as "Helped" and the biggest negative part as "Hurt".</p>
    </div>
  </div>
</div>"""


def _nice(feature, category):
    names = {"action_type": "Shot", "combined_shot_type": "Shot family", "shot_zone_area": "Area",
             "shot_zone_basic": "Zone", "shot_zone_range": "Range", "shot_type": "Type", "opponent": "Opponent"}
    return f"<small>{names.get(feature, feature)}:</small> {category}"


def model_html(model):
    m = model["metrics"]
    acc, base = m["test_accuracy"], m["baseline_accuracy"]
    kpis = [
        ("Test accuracy", f"{acc * 100:.1f}%", f"on {m['test_rows']:,} shots the model never saw"),
        ("Above guessing", f"+{(acc - base) * 100:.1f}", f"points better than always saying miss ({base * 100:.1f}%)"),
        ("Training shots", f"{m['train_rows']:,}", "80% of the 25,697 labeled shots"),
        ("Model inputs", f"15 &rarr; {m['encoded_columns']}", "features before and after one-hot encoding"),
    ]
    kpi_html = "".join(f'<div class="card kpi wood"><div class="label">{a}</div><div class="num">{b}</div><div class="sub">{c}</div></div>'
                       for a, b, c in kpis)
    compare = [
        ("Always guess miss", "No model at all", base, "#3a3f4a"),
        ("KNN (tuned)", "k = 75, Grid Search", KNN_TUNED_ACCURACY, "#5b6b85"),
        ("Logistic Regression", "C = 0.1, used in the game", acc, "#f0b429"),
    ]
    compare_html = "".join(f'<div class="row"><div class="name">{a}<small>{b}</small></div><div class="track">'
                           f'<div class="fill" style="width:{v * 100:.1f}%;background:{c}"></div></div><div class="val">{v * 100:.1f}%</div></div>'
                           for a, b, v, c in compare)

    weights = [(f, c, w) for f, table in model["weights"]["categorical"].items() for c, w in table.items()]
    weights.sort(key=lambda t: t[2])
    top = weights[:7] + weights[-7:]
    biggest = max(abs(w) for _, _, w in top)
    wt_rows = []
    for f, c, w in sorted(top, key=lambda t: -t[2]):
        size = abs(w) / biggest * 100
        bar = f'<div class="b" style="width:{size:.0f}%;background:{"#f0b429" if w > 0 else "#5b6b85"};border-radius:{"0 4px 4px 0" if w > 0 else "4px 0 0 4px"}"></div>'
        wt_rows.append(f'<div class="wt"><div class="lbl">{_nice(f, c)}</div><div class="neg">{bar if w < 0 else ""}</div><div class="pos">{bar if w > 0 else ""}</div></div>')

    shots = sorted(model["moves"].items(), key=lambda kv: -kv[1]["count"])
    shot_rows = "".join(f'<tr><td>{name}</td><td>{info["count"]:,}</td><td><div class="mini"><div class="track">'
                        f'<div class="fill" style="width:{info["made_rate"] * 100:.0f}%;background:{_mix(info["made_rate"], .3, .8)}"></div></div>'
                        f'{_pct(info["made_rate"])}</div></td><td>{info["min"]}&ndash;{info["max"]} ft</td></tr>' for name, info in shots)

    return CSS + f"""
<div class="bm">
  <div class="hero">{HERO_ART}
    <div class="eyebrow">The model</div>
    <h1>Logistic Regression</h1>
    <p>Trained in Test2.ipynb on Kobe Bryant's shots. It predicts the probability that a shot goes in from where, how and when it was taken.</p>
    <div class="chips"><span class="chip">C = 0.1 (Grid Search)</span><span class="chip">StandardScaler</span>
      <span class="chip">OneHotEncoder</span><span class="chip">80 / 20 stratified split</span><span class="chip">No data leakage</span></div>
  </div>

  <h2>Results</h2>
  <p class="lead">All numbers come from the test set.</p>
  <div class="grid g4">{kpi_html}</div>

  <h2>Compared to other options</h2>
  <p class="lead">Accuracy on the same test shots.</p>
  <div class="card bars">{compare_html}
    <p class="note">About 68% is a normal result for this dataset: the same shot from the same spot sometimes goes in and sometimes not,
      and the data has no information about defenders.</p></div>

  <h2>Where Kobe scores</h2>
  <p class="lead">Real made rate in each zone and by distance. The model learned these patterns.</p>
  <div class="grid g2">
    <div class="card">{court_zones_svg(model['zone_rates'])}
      <div class="legend">low<span class="scale"></span>high made rate</div></div>
    <div class="card"><h3 style="margin:0 0 4px;font-size:18px">Made rate by distance</h3>
      <p style="color:var(--muted);font-size:12px;margin:0 0 10px">Shots grouped every 2 feet</p>
      {distance_svg(model['distance_rates'])}
      <p class="note">Shots at the rim go in 64% of the time. From 26 feet and beyond it drops to about 30%.</p></div>
  </div>

  <h2>What the model learned</h2>
  <p class="lead">The strongest weights. Gold pushes a shot toward IN, slate pushes it toward OUT.</p>
  <div class="card">{''.join(wt_rows)}</div>

  <h2>Shot types</h2>
  <p class="lead">The shots that appear in the game, with Kobe's real made rate.</p>
  <div class="card" style="padding:6px 8px">
    <table class="shots"><tr><th>Shot</th><th>Shots in data</th><th>Made rate</th><th>Distance</th></tr>{shot_rows}</table>
  </div>
</div>"""
