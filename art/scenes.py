# Generátor komiksových pozadí klubu (černo-zlatá, tlusté obrysy, rastr).
# Výstup: art/parket.html a art/bar.html (SVG 1600×1067) → rasterizace přes headless Chrome (art/render.mjs).
import math
import random
from pathlib import Path

W, H = 1600, 1067
INK = "#0a0806"
GOLD = "#E8B931"
GOLD_L = "#FFE08A"
GOLD_D = "#A87B12"
BRONZE = "#6b4a0c"
CREAM = "#FFF3D0"
WALL = "#140f08"
WINE = "#6a1b1b"
AMBER = "#C9771A"

OUT = Path(__file__).parent


def P(points):
    return " ".join(f"{x:.1f},{y:.1f}" for x, y in points)


def star(cx, cy, r1, r2, n=10, rot=0.0):
    pts = []
    for i in range(n * 2):
        r = r1 if i % 2 == 0 else r2
        a = rot + math.pi * i / n
        pts.append((cx + r * math.sin(a), cy - r * math.cos(a)))
    return P(pts)


DEFS = f"""
<defs>
  <pattern id="dots" width="12" height="12" patternUnits="userSpaceOnUse">
    <circle cx="3" cy="3" r="1.7" fill="{GOLD}" opacity=".22"/><circle cx="9" cy="9" r="1.7" fill="{GOLD}" opacity=".22"/>
  </pattern>
  <pattern id="dotsInk" width="10" height="10" patternUnits="userSpaceOnUse">
    <circle cx="2.5" cy="2.5" r="1.9" fill="{INK}" opacity=".35"/><circle cx="7.5" cy="7.5" r="1.9" fill="{INK}" opacity=".35"/>
  </pattern>
  <radialGradient id="glow" cx="50%" cy="50%" r="50%">
    <stop offset="0" stop-color="{GOLD_L}" stop-opacity=".55"/><stop offset=".45" stop-color="{GOLD}" stop-opacity=".18"/><stop offset="1" stop-color="{GOLD}" stop-opacity="0"/>
  </radialGradient>
  <linearGradient id="goldV" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="{GOLD_L}"/><stop offset=".5" stop-color="{GOLD}"/><stop offset="1" stop-color="{GOLD_D}"/>
  </linearGradient>
  <linearGradient id="beam" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="{GOLD_L}" stop-opacity=".55"/><stop offset="1" stop-color="{GOLD}" stop-opacity="0"/>
  </linearGradient>
  <radialGradient id="ball" cx="38%" cy="32%" r="70%">
    <stop offset="0" stop-color="#fffbe9"/><stop offset=".45" stop-color="{GOLD_L}"/><stop offset="1" stop-color="{GOLD_D}"/>
  </radialGradient>
  <clipPath id="ballClip"><circle cx="800" cy="175" r="88"/></clipPath>
</defs>"""


def page(svg_body, title):
    return f"""<!doctype html><html><head><meta charset="utf-8"><title>{title}</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Titan+One&display=swap">
<style>html,body{{margin:0;background:{INK}}}svg{{display:block}}text{{font-family:'Titan One',sans-serif}}</style></head>
<body><svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">{DEFS}{svg_body}</svg></body></html>"""


def sunburst(cx, cy, n, c1, c2, r=2200):
    out = []
    for i in range(n):
        a1 = 2 * math.pi * i / n
        a2 = 2 * math.pi * (i + 0.5) / n
        out.append(f'<polygon points="{P([(cx, cy), (cx + r * math.cos(a1), cy + r * math.sin(a1)), (cx + r * math.cos(a2), cy + r * math.sin(a2))])}" fill="{c1}"/>')
    return f'<rect width="{W}" height="{H}" fill="{c2}"/>' + "".join(out)


def crowd(rng, y0, x_from, x_to, count, scale=1.0):
    out = []
    for _ in range(count):
        x = rng.uniform(x_from, x_to)
        s = rng.uniform(0.8, 1.25) * scale
        y = y0 + rng.uniform(-25, 35)
        hr = 46 * s
        body = f'<path d="M{x - 95 * s:.1f},{H + 10} C{x - 90 * s:.1f},{y + 70 * s:.1f} {x - 60 * s:.1f},{y + 52 * s:.1f} {x:.1f},{y + 50 * s:.1f} C{x + 60 * s:.1f},{y + 52 * s:.1f} {x + 90 * s:.1f},{y + 70 * s:.1f} {x + 95 * s:.1f},{H + 10} Z" fill="{INK}" stroke="{GOLD}" stroke-width="5" stroke-linejoin="round"/>'
        arms = ""
        if rng.random() < 0.65:
            side = rng.choice([-1, 1])
            ax = x + side * 70 * s
            arms += f'<path d="M{ax:.1f},{y + 80 * s:.1f} L{ax + side * 40 * s:.1f},{y - 120 * s:.1f}" stroke="{INK}" stroke-width="{30 * s:.1f}" stroke-linecap="round"/>'
            arms += f'<path d="M{ax:.1f},{y + 80 * s:.1f} L{ax + side * 40 * s:.1f},{y - 120 * s:.1f}" stroke="{GOLD}" stroke-width="{30 * s + 10:.1f}" stroke-linecap="round" opacity="0"/>'
            arms = (f'<path d="M{ax:.1f},{y + 80 * s:.1f} L{ax + side * 40 * s:.1f},{y - 120 * s:.1f}" stroke="{GOLD}" stroke-width="{30 * s + 10:.1f}" stroke-linecap="round"/>'
                    f'<path d="M{ax:.1f},{y + 80 * s:.1f} L{ax + side * 40 * s:.1f},{y - 120 * s:.1f}" stroke="{INK}" stroke-width="{30 * s:.1f}" stroke-linecap="round"/>')
        head = f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{hr:.1f}" fill="{INK}" stroke="{GOLD}" stroke-width="5"/>'
        out.append(arms + body + head)
    return "".join(out)


def sparkle(x, y, r, fill=CREAM):
    return f'<polygon points="{star(x, y, r, r * 0.22, 4)}" fill="{fill}" stroke="{INK}" stroke-width="3" stroke-linejoin="round"/>'


def burst(x, y, r, word, rot=-8, fs=54):
    return (f'<g transform="rotate({rot} {x} {y})"><polygon points="{star(x, y, r, r * 0.72, 14)}" fill="{GOLD_L}" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>'
            f'<text x="{x}" y="{y + fs * 0.36:.1f}" font-size="{fs}" text-anchor="middle" fill="{INK}">{word}</text></g>')


def speaker(x, y, w, h):
    s = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="#1c150b" stroke="{INK}" stroke-width="8"/>',
         f'<rect x="{x + 8}" y="{y + 8}" width="{w - 16}" height="{h - 16}" rx="6" fill="none" stroke="{GOLD_D}" stroke-width="4"/>']
    cx = x + w / 2
    for cy, r in ((y + h * 0.28, w * 0.22), (y + h * 0.66, w * 0.36)):
        s.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{INK}" stroke="{GOLD}" stroke-width="6"/>')
        s.append(f'<circle cx="{cx}" cy="{cy}" r="{r * 0.62}" fill="#2a2010" stroke="{GOLD_D}" stroke-width="4"/>')
        s.append(f'<circle cx="{cx}" cy="{cy}" r="{r * 0.22}" fill="{GOLD}" stroke="{INK}" stroke-width="4"/>')
    return "".join(s)


# ───────────────────────── PARKET ─────────────────────────
def parket():
    rng = random.Random(54)
    b = []
    VP = (800, 600)
    # stěna – art-deco paprsky za pultem
    b.append(sunburst(800, 560, 36, "#24190a", WALL))
    b.append(f'<circle cx="800" cy="470" r="560" fill="url(#glow)"/>')
    # art-deco oblouky na zdi
    for i, r in enumerate((520, 455, 390)):
        b.append(f'<path d="M{800 - r},600 A{r},{r} 0 0 1 {800 + r},600" fill="none" stroke="{GOLD if i == 0 else GOLD_D}" stroke-width="{10 - i * 2}"/>')
    # sloupy po stranách
    for x in (300, 1220):
        b.append(f'<rect x="{x}" y="0" width="80" height="600" fill="#1f170b" stroke="{INK}" stroke-width="8"/>')
        for k in range(4):
            b.append(f'<rect x="{x + 12 + k * 15}" y="0" width="7" height="600" fill="{GOLD_D}"/>')
        b.append(f'<rect x="{x - 12}" y="560" width="104" height="40" fill="url(#goldV)" stroke="{INK}" stroke-width="6"/>')
    # paprsky světel od stropu
    for (x1, x2, x3) in ((200, 380, 760), (1400, 1220, 840), (560, 640, 520), (1040, 960, 1080)):
        b.append(f'<polygon points="{P([(x1, 0), (x2, 0), (x3 + 120, 1067), (x3 - 120, 1067)])}" fill="url(#beam)" opacity=".45"/>')
    # cedule STUDIO 54
    b.append(f'<g transform="rotate(-2 800 340)"><rect x="560" y="290" width="480" height="104" rx="18" fill="{INK}" stroke="{GOLD}" stroke-width="8"/>')
    for k in range(18):
        bx = 575 + k * 26.5
        b.append(f'<circle cx="{bx:.1f}" cy="300" r="5" fill="{CREAM}"/><circle cx="{bx:.1f}" cy="384" r="5" fill="{CREAM}"/>')
    b.append(f'<text x="800" y="368" font-size="68" text-anchor="middle" fill="{GOLD}" stroke="{INK}" stroke-width="10" paint-order="stroke" letter-spacing="2">STUDIO 54</text></g>')
    # reproduktory
    b.append(speaker(440, 380, 150, 250))
    b.append(speaker(1010, 380, 150, 250))
    # DJ za pultem (silueta)
    b.append(f'<circle cx="800" cy="455" r="44" fill="{INK}" stroke="{GOLD}" stroke-width="5"/>')
    b.append(f'<path d="M752,452 A50,50 0 0 1 848,452" fill="none" stroke="{GOLD}" stroke-width="9"/><rect x="738" y="440" width="22" height="36" rx="8" fill="{GOLD}" stroke="{INK}" stroke-width="4"/><rect x="840" y="440" width="22" height="36" rx="8" fill="{GOLD}" stroke="{INK}" stroke-width="4"/>')
    b.append(f'<path d="M720,560 C725,505 760,495 800,495 C840,495 875,505 880,560 Z" fill="{INK}" stroke="{GOLD}" stroke-width="5"/>')
    # DJ pult
    b.append(f'<polygon points="{P([(600, 535), (1000, 535), (1035, 690), (565, 690)])}" fill="url(#goldV)" stroke="{INK}" stroke-width="9" stroke-linejoin="round"/>')
    for k in range(9):
        x = 640 + k * 40
        b.append(f'<line x1="{x}" y1="560" x2="{x + (x - 800) * 0.09:.1f}" y2="670" stroke="{BRONZE}" stroke-width="6"/>')
    b.append(f'<rect x="585" y="520" width="430" height="26" rx="6" fill="{INK}" stroke="{GOLD}" stroke-width="5"/>')
    for cx in (690, 910):
        b.append(f'<ellipse cx="{cx}" cy="522" rx="62" ry="15" fill="#1c150b" stroke="{GOLD}" stroke-width="5"/><ellipse cx="{cx}" cy="522" rx="12" ry="4" fill="{GOLD_L}"/>')
    b.append(f'<rect x="770" y="508" width="60" height="18" rx="4" fill="{GOLD_D}" stroke="{INK}" stroke-width="4"/>')
    # parket – perspektivní dlaždice
    rows = [600]
    y = 612.0
    step = 14.0
    while y < H + 200:
        rows.append(y)
        y += step
        step *= 1.32
    xs = list(range(-2400, 4001, 160))
    def at(xb, yy):
        return VP[0] + (xb - VP[0]) * (yy - VP[1]) / (H - VP[1])
    tiles = []
    for j in range(len(rows) - 1):
        y1, y2 = rows[j], rows[j + 1]
        for i in range(len(xs) - 1):
            q = [(at(xs[i], y1), y1), (at(xs[i + 1], y1), y1), (at(xs[i + 1], y2), y2), (at(xs[i], y2), y2)]
            if q[1][0] < -50 or q[0][0] > W + 50:
                continue
            r = rng.random()
            if (i + j) % 2 == 0:
                fill = CREAM if r < 0.22 else GOLD if r < 0.62 else GOLD_D
            else:
                fill = "#1a1309" if r < 0.8 else BRONZE
            tiles.append(f'<polygon points="{P(q)}" fill="{fill}" stroke="{INK}" stroke-width="{1.5 + j * 1.1:.1f}" stroke-linejoin="round"/>')
    b.append("<g>" + "".join(tiles) + "</g>")
    b.append(f'<rect x="0" y="600" width="{W}" height="{H - 600}" fill="url(#dotsInk)"/>')
    b.append(f'<ellipse cx="800" cy="760" rx="520" ry="120" fill="url(#glow)" opacity=".8"/>')
    # disko koule
    b.append(f'<line x1="800" y1="0" x2="800" y2="90" stroke="{INK}" stroke-width="6"/>')
    b.append(f'<g clip-path="url(#ballClip)"><rect x="700" y="80" width="200" height="200" fill="url(#ball)"/>')
    for gx in range(712, 900, 18):
        for gy in range(87, 265, 18):
            if rng.random() < 0.28:
                b.append(f'<rect x="{gx + 2}" y="{gy + 2}" width="14" height="14" fill="{CREAM if rng.random() < .6 else BRONZE}" opacity=".85"/>')
    for gx in range(712, 900, 18):
        b.append(f'<line x1="{gx}" y1="80" x2="{gx}" y2="280" stroke="{BRONZE}" stroke-width="2"/>')
    for gy in range(87, 265, 18):
        b.append(f'<line x1="700" y1="{gy}" x2="900" y2="{gy}" stroke="{BRONZE}" stroke-width="2"/>')
    b.append('</g>')
    b.append(f'<circle cx="800" cy="175" r="88" fill="none" stroke="{INK}" stroke-width="8"/>')
    for (x, y, r) in ((690, 120, 26), (915, 230, 22), (930, 105, 16), (668, 245, 14), (1000, 170, 12), (600, 170, 12)):
        b.append(sparkle(x, y, r))
    # onomatopoie
    b.append(burst(1085, 300, 84, "BUM!", -10, 38))
    b.append(burst(520, 300, 62, "ŤUC", 9, 34))
    # dav v popředí
    b.append(crowd(rng, 900, -60, 520, 6))
    b.append(crowd(rng, 905, 1080, 1660, 6))
    b.append(crowd(rng, 980, 520, 1080, 5, 0.85))
    # rastr přes celek
    b.append(f'<rect width="{W}" height="{H}" fill="url(#dots)"/>')
    return page("".join(b), "Parket")


# ───────────────────────── BAR + VIP ─────────────────────────
def bar():
    rng = random.Random(1977)
    b = []
    b.append(sunburst(800, 120, 40, "#22180a", WALL))
    # zrcadlová stěna s art-deco rámem
    b.append(f'<rect x="150" y="210" width="1300" height="370" fill="#1b140a" stroke="{INK}" stroke-width="10"/>')
    b.append(f'<rect x="166" y="226" width="1268" height="338" fill="none" stroke="{GOLD}" stroke-width="6"/>')
    b.append(f'<ellipse cx="800" cy="400" rx="640" ry="190" fill="url(#glow)" opacity=".9"/>')
    # police s lahvemi
    colors = [GOLD, AMBER, GOLD_D, CREAM, WINE, "#2f4a1c", GOLD_L]
    for sy in (330, 445, 560):
        b.append(f'<rect x="170" y="{sy}" width="1260" height="16" fill="url(#goldV)" stroke="{INK}" stroke-width="5"/>')
        x = 185
        while x < 1400:
            w = rng.uniform(26, 40)
            h = rng.uniform(62, 98)
            c = rng.choice(colors)
            neck = w * 0.34
            top = sy - h
            path = (f'M{x:.1f},{sy} L{x:.1f},{top + h * 0.38:.1f} Q{x:.1f},{top + h * 0.22:.1f} {x + w / 2 - neck / 2:.1f},{top + h * 0.14:.1f} '
                    f'L{x + w / 2 - neck / 2:.1f},{top:.1f} L{x + w / 2 + neck / 2:.1f},{top:.1f} L{x + w / 2 + neck / 2:.1f},{top + h * 0.14:.1f} '
                    f'Q{x + w:.1f},{top + h * 0.22:.1f} {x + w:.1f},{top + h * 0.38:.1f} L{x + w:.1f},{sy} Z')
            b.append(f'<path d="{path}" fill="{c}" stroke="{INK}" stroke-width="4" stroke-linejoin="round"/>')
            b.append(f'<rect x="{x + w * 0.18:.1f}" y="{top + h * 0.5:.1f}" width="{w * 0.64:.1f}" height="{h * 0.22:.1f}" fill="{CREAM}" stroke="{INK}" stroke-width="2.5"/>')
            b.append(f'<line x1="{x + w * 0.22:.1f}" y1="{top + h * 0.3:.1f}" x2="{x + w * 0.22:.1f}" y2="{sy - 8:.1f}" stroke="#fff" stroke-width="3" opacity=".55"/>')
            x += w + rng.uniform(6, 16)
    # cedule BAR se žárovkami
    b.append(f'<g transform="rotate(-2 800 140)"><rect x="610" y="78" width="380" height="124" rx="20" fill="{INK}" stroke="{GOLD}" stroke-width="9"/>')
    for k in range(14):
        bx = 628 + k * 26.5
        b.append(f'<circle cx="{bx:.1f}" cy="90" r="6" fill="{CREAM}"/><circle cx="{bx:.1f}" cy="190" r="6" fill="{CREAM}"/>')
    b.append(f'<text x="800" y="172" font-size="88" text-anchor="middle" fill="{GOLD}" stroke="{INK}" stroke-width="12" paint-order="stroke" letter-spacing="6">BAR</text></g>')
    # závěsné lampy
    for x in (330, 600, 1000, 1270):
        b.append(f'<line x1="{x}" y1="0" x2="{x}" y2="60" stroke="{INK}" stroke-width="5"/>')
        b.append(f'<polygon points="{P([(x - 46, 108), (x + 46, 108), (x + 18, 60), (x - 18, 60)])}" fill="url(#goldV)" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>')
        b.append(f'<polygon points="{P([(x - 46, 108), (x + 46, 108), (x + 170, 660), (x - 170, 660)])}" fill="url(#beam)" opacity=".35"/>')
    # barový pult
    b.append(f'<rect x="-20" y="600" width="{W + 40}" height="46" fill="url(#goldV)" stroke="{INK}" stroke-width="9"/>')
    b.append(f'<rect x="-20" y="646" width="{W + 40}" height="260" fill="#1d150a" stroke="{INK}" stroke-width="9"/>')
    for k in range(0, W + 80, 90):
        b.append(f'<rect x="{k}" y="660" width="34" height="232" rx="10" fill="{GOLD_D}" stroke="{INK}" stroke-width="5"/>')
        b.append(f'<rect x="{k + 8}" y="672" width="8" height="208" fill="{GOLD_L}" opacity=".7"/>')
    b.append(f'<rect x="0" y="646" width="{W}" height="260" fill="url(#dotsInk)"/>')
    # sklenice a šampaňské na pultu
    def martini(x, y, s=1.0, liquid=GOLD):
        return (f'<polygon points="{P([(x - 34 * s, y - 70 * s), (x + 34 * s, y - 70 * s), (x, y - 26 * s)])}" fill="{liquid}" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>'
                f'<line x1="{x}" y1="{y - 26 * s}" x2="{x}" y2="{y}" stroke="{INK}" stroke-width="6"/><ellipse cx="{x}" cy="{y}" rx="{20 * s}" ry="{5 * s}" fill="{CREAM}" stroke="{INK}" stroke-width="4"/>'
                f'<circle cx="{x + 14 * s}" cy="{y - 64 * s}" r="{7 * s}" fill="{WINE}" stroke="{INK}" stroke-width="3"/>')
    for x in (430, 520, 1180):
        b.append(martini(x, 602))
    # kbelík se šampaňským
    b.append(f'<path d="M640,598 L662,520 L778,520 L800,598 Z" fill="url(#goldV)" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>')
    b.append(f'<path d="M700,522 L708,430 L722,410 L736,410 L742,430 L746,522 Z" fill="#2f4a1c" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/><rect x="718" y="396" width="22" height="20" fill="{GOLD}" stroke="{INK}" stroke-width="4"/>')
    for (x, y, r) in ((690, 400, 14), (770, 380, 18), (735, 350, 10)):
        b.append(sparkle(x, y, r))
    b.append(burst(905, 470, 66, "CINK!", 8, 32))
    # barové stoličky
    for x in (160, 400, 640, 880):
        b.append(f'<line x1="{x}" y1="930" x2="{x}" y2="1067" stroke="{INK}" stroke-width="16"/><line x1="{x}" y1="930" x2="{x}" y2="1067" stroke="{GOLD_D}" stroke-width="6"/>')
        b.append(f'<ellipse cx="{x}" cy="1030" rx="60" ry="12" fill="none" stroke="{GOLD}" stroke-width="7"/>')
        b.append(f'<ellipse cx="{x}" cy="925" rx="92" ry="26" fill="{WINE}" stroke="{INK}" stroke-width="8"/><ellipse cx="{x - 20}" cy="918" rx="40" ry="7" fill="#fff" opacity=".25"/>')
    # VIP – sametový provaz se zlatými sloupky
    for x in (1080, 1250, 1420):
        b.append(f'<rect x="{x - 12}" y="820" width="24" height="230" rx="10" fill="url(#goldV)" stroke="{INK}" stroke-width="6"/>')
        b.append(f'<circle cx="{x}" cy="812" r="22" fill="{GOLD_L}" stroke="{INK}" stroke-width="6"/>')
        b.append(f'<ellipse cx="{x}" cy="1052" rx="50" ry="14" fill="url(#goldV)" stroke="{INK}" stroke-width="6"/>')
    for x1, x2 in ((1080, 1250), (1250, 1420)):
        b.append(f'<path d="M{x1},835 Q{(x1 + x2) / 2},930 {x2},835" fill="none" stroke="{INK}" stroke-width="26" stroke-linecap="round"/>')
        b.append(f'<path d="M{x1},835 Q{(x1 + x2) / 2},930 {x2},835" fill="none" stroke="{WINE}" stroke-width="16" stroke-linecap="round"/>')
    b.append(f'<g transform="rotate(4 1250 760)"><rect x="1185" y="725" width="130" height="64" rx="10" fill="{INK}" stroke="{GOLD}" stroke-width="6"/><text x="1250" y="774" font-size="44" text-anchor="middle" fill="{GOLD}">VIP</text></g>')
    b.append(f'<rect width="{W}" height="{H}" fill="url(#dots)"/>')
    return page("".join(b), "Bar")


if __name__ == "__main__":
    (OUT / "parket.html").write_text(parket(), encoding="utf-8")
    (OUT / "bar.html").write_text(bar(), encoding="utf-8")
    print("ok")
