# Komiksové tvary místo obdélníků/oválů (styl Lokál TV) – roztřepený papír, mráčky, výbuch, ručně kreslené bubliny.
# Používá generátory z pop.py; volá se z pop.patch().
import math, random
from pop import uri, burst, INK, Y, R, PAPER

DARK = "#15110b"


def torn(seed, fill, ring=None, m=3.0, amp=1.3):
    """roztřepený papír: zubaté hrany, obrys v px; ring = vnitřní barevná linka"""
    r = random.Random(seed)

    def edge(a, b, horiz):
        pts = []
        n = r.randint(7, 11)
        for i in range(n):
            t = i / n
            x = a[0] + (b[0] - a[0]) * t
            y = a[1] + (b[1] - a[1]) * t
            d = (r.random() - .5) * 2 * amp
            if horiz:
                y += d
            else:
                x += d
            pts.append((x, y))
        return pts

    c = [(m + r.random(), m + r.random()), (100 - m - r.random(), m + r.random()),
         (100 - m - r.random(), 100 - m - r.random()), (m + r.random(), 100 - m - r.random())]
    pts = edge(c[0], c[1], 1) + edge(c[1], c[2], 0) + edge(c[2], c[3], 1) + edge(c[3], c[0], 0)
    pts = [(min(max(x, 1.6), 98.4), min(max(y, 1.6), 98.4)) for x, y in pts]
    P = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    inner = ""
    if ring:
        Q = " ".join(f"{50 + (x - 50) * .955:.1f},{50 + (y - 50) * .94:.1f}" for x, y in pts)
        inner = f"<polygon points='{Q}' fill='none' stroke='{ring}' stroke-width='2.5' stroke-linejoin='round' vector-effect='non-scaling-stroke'/>"
    return uri(f"<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100' preserveAspectRatio='none'><polygon points='{P}' fill='{fill}' stroke='{INK}' stroke-width='3.5' stroke-linejoin='round' vector-effect='non-scaling-stroke'/>{inner}</svg>")


def cloudbox(seed, fill):
    """mráček přes celý prvek (vroubky po obvodu)"""
    r = random.Random(seed)
    m = 9
    pts = []
    for a, b in [((m, m), (100 - m, m)), ((100 - m, m), (100 - m, 100 - m)), ((100 - m, 100 - m), (m, 100 - m)), ((m, 100 - m), (m, m))]:
        n = 5 if a[1] == b[1] else 2
        for i in range(n):
            t = i / n
            pts.append((a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t))
    pts.append(pts[0])
    d = f"M{pts[0][0]:.1f},{pts[0][1]:.1f}"
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        mx, my = (x0 + x1) / 2, (y0 + y1) / 2
        nx, ny = (y1 - y0), -(x1 - x0)  # normála ven (obvod po směru hodin)
        L = math.hypot(nx, ny) or 1
        k = (7.5 + r.random() * 2.5) / L
        d += f" Q{mx + nx * k:.1f},{my + ny * k:.1f} {x1:.1f},{y1:.1f}"
    return uri(f"<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100' preserveAspectRatio='none'><path d='{d} Z' fill='{fill}' stroke='{INK}' stroke-width='3.5' stroke-linejoin='round' vector-effect='non-scaling-stroke'/></svg>")


def burstbox(seed, fill):
    r = random.Random(seed)
    return uri(f"<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100' preserveAspectRatio='none'><polygon points='{burst(50, 50, 48, 47, 16, .8, r)}' fill='{fill}' stroke='{INK}' stroke-width='3.5' stroke-linejoin='round' vector-effect='non-scaling-stroke'/></svg>")


RESET = (".game-root .gl:not(button),.game-root .gls,.game-root .cap,.game-root .loc-cap,.game-root .hud-toast,"
         ".game-root .hud-quest .gl,.game-root .ti-stats,.game-root .hud-top,.game-root .hud-bot,.game-root .djc,"
         ".game-root .ctag,.game-root .panel-dj>div:first-child>span:first-child,.game-root .ti-pl,"
         ".game-root .ti-poster>span,.game-root .pop-rank")

SHAPES = f"""
/* ══ KOMIKSOVÉ TVARY MÍSTO OBDÉLNÍKŮ (styl Lokál TV) ══ */
{RESET}{{background-color:transparent!important;background-position:center!important;background-size:100% 100%!important;background-repeat:no-repeat!important;border:0!important;border-radius:0!important;box-shadow:none!important;-webkit-backdrop-filter:none!important;backdrop-filter:none!important}}
.game-root .gl:not(button){{background-image:{torn(101, DARK, Y)}!important;filter:drop-shadow(5px 6px 0 {INK})}}
.game-root .panel-loc{{background-image:{torn(102, DARK, Y)}!important;filter:drop-shadow(6px 7px 0 var(--acc)) drop-shadow(2px 2px 0 {INK})}}
.game-root .panel-dj{{background-image:{torn(103, DARK, Y)}!important}}
.game-root .gls{{background-image:{torn(104, DARK, Y)}!important;filter:drop-shadow(7px 8px 0 {R}) drop-shadow(2px 2px 0 {INK})}}
.game-root .gls.bubble{{background-image:{torn(105, PAPER)}!important}}
.game-root .cap{{background-image:{torn(106, PAPER)}!important;filter:drop-shadow(5px 6px 0 {INK});padding:16px 22px!important}}
.game-root .ev-bub .cap{{background-image:none!important;filter:none;padding:0!important}}
.game-root [data-screen-label="Intro"] .cap{{background-image:none!important;filter:none}}
.game-root .loc-cap{{background-image:{torn(107, Y)}!important;filter:drop-shadow(4px 5px 0 var(--acc)) drop-shadow(1px 1px 0 {INK});padding:14px 18px!important}}
.game-root .hud-toast{{background-image:{cloudbox(5, PAPER)}!important;filter:drop-shadow(5px 6px 0 {R});padding:22px 48px 22px 36px!important}}
.game-root .hud-toast::after{{display:none}}
.game-root .hud-toast::before{{right:24px;top:18px}}
.game-root .hud-quest .gl{{background-image:{cloudbox(6, PAPER)}!important;filter:drop-shadow(3px 4px 0 {INK});padding:8px 24px 8px 18px!important}}
.game-root .ti-stats{{background-image:{cloudbox(7, PAPER)}!important;filter:drop-shadow(3px 4px 0 {INK});padding:16px 26px!important}}
.game-root .hud-top,.game-root .hud-bot{{background-image:{torn(108, Y, None, 1.8, .9)}!important;filter:drop-shadow(5px 6px 0 {R}) drop-shadow(1px 1px 0 {INK})}}
.game-root .djc{{background-image:{torn(109, PAPER)}!important;filter:drop-shadow(4px 4px 0 {INK})}}
.game-root .djc-own{{background-image:{torn(110, Y)}!important}}
.game-root .djc-gone{{background-image:{torn(111, "#cfc6b2")}!important}}
.game-root .djc-now{{filter:drop-shadow(5px 5px 0 {R}) drop-shadow(1px 1px 0 {INK})}}
.game-root .ctag{{background-image:{torn(112, R)}!important;padding:7px 14px!important;filter:drop-shadow(3px 3px 0 {INK})}}
.game-root .panel-dj>div:first-child>span:first-child,.game-root .ti-pl,.game-root .ti-poster>span{{background-image:{torn(113, Y)}!important;filter:drop-shadow(3px 3px 0 {INK});padding:7px 16px 5px!important}}
.game-root .pop-rank{{background-image:{burstbox(9, Y)}!important;filter:drop-shadow(6px 7px 0 {R});padding:clamp(40px,7vw,70px) clamp(40px,8vw,90px)!important;align-items:center;text-align:center;transform:rotate(-2deg)!important}}
/* tlačítka = ručně kreslené bubliny (nepravidelné rohy) */
.game-root .gb,.game-root .gbd,.game-root .gp,.game-root .gi,.game-root .hud-meter,.game-root .hud-chip,.game-root .hud-clock{{border-radius:16px 30px 13px 34px / 30px 14px 32px 16px!important}}
.game-root .chat>.gb,.game-root .opts>.gb,.game-root .mg-opts>button{{--bb:{PAPER};color:{INK}!important;border-radius:24px 34px 6px 30px / 30px 22px 6px 34px!important;box-shadow:4px 5px 0 var(--acc),4px 5px 0 3px {INK}!important}}
.game-root .chat>.gb:nth-child(even),.game-root .opts>.gb:nth-child(even),.game-root .mg-opts>button:nth-child(even){{border-radius:34px 24px 6px 28px / 22px 32px 6px 30px!important;transform:rotate(.6deg)}}
.game-root .chat>.gb:nth-child(odd),.game-root .opts>.gb:nth-child(odd){{transform:rotate(-.5deg)}}
.game-root .chat>.gb:hover,.game-root .opts>.gb:hover,.game-root .mg-opts>button:hover{{--bb:{Y};color:{INK}!important;transform:translate(-2px,-2px) rotate(0)!important;box-shadow:6px 7px 0 {INK}!important}}
.game-root .chat>.gb>span:first-child>span:last-child{{color:{INK}!important;opacity:.7!important}}
.game-root .hud-tab{{border-radius:22px 30px 6px 26px / 26px 20px 6px 30px!important}}
.game-root .ti-start{{border-radius:40px 70px 36px 80px / 70px 36px 80px 40px!important}}
.game-root .gls,.game-root [data-screen-label="Pepa"] .gls.bubble{{padding:clamp(28px,4vh,40px) clamp(28px,4.5vw,44px)!important}}
.game-root .panel-loc,.game-root .panel-dj{{padding:42px 38px 38px!important}}
.game-root .hud-toast{{padding:28px 70px 28px 62px!important}}
.game-root .hud-toast::before{{right:34px;top:22px}}
.game-root .ti-in{{border-radius:22px 40px 20px 44px / 40px 20px 44px 22px!important}}
"""
