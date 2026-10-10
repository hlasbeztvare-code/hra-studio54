# Postavy ve stylu „dospělé animovky“ (inspirace Lokál TV, vlastní kresba): protáhlé karikaturní hlavy,
# přivřená víčka, velké nosy, kamenné výrazy, ploché barvy, tenký hnědočerný obrys.
# python art/lokal.py → art/lokal/*.svg + náhled art/lokal/_sheet.html
import json, pathlib

OUT = pathlib.Path(__file__).with_name("lokal")
LN = "#2b1e18"  # obrys
SW = 4
SKIN = {"light": ("#F3CBA8", "#E0AE88"), "tan": ("#DCA47C", "#C48A62"), "brown": ("#A8704A", "#8E5A38"), "pale": ("#F7D9C0", "#E8BE9C")}


class C:
    def __init__(s, **k):
        s.__dict__.update(dict(bg="#2fd3f5", skin="light", hw=96, top=78, bot=318, jw=46, hair="short", hc="#3a2a1f", lid=.5,
                               look=(0, 2), nose="long", mouth="flat", beard=None, bc=None, stub=False, glasses=None, gtint="#111",
                               phones=None, cap=None, capc="#222", shirt="#f4f1ea", stext="", stc="#fff", deck=True,
                               earring=False, lashes=False, lips=None, brows="flat", jacket=None, tattoo=False, tank=False,
                               earpiece=False, bun=None, mole=False))
        s.__dict__.update(k)
        s.n = 0

    def uid(s, p):
        s.n += 1
        return f"{p}{s.n}"


def head_path(c, dx=0, sc=1.0):
    hw, t, b, jw = c.hw * sc, c.top, c.bot, c.jw * sc
    cx = 200 + dx
    m = t + (b - t) * .42
    return (f"M{cx},{t} C{cx + hw * .95},{t} {cx + hw},{m - 70} {cx + hw},{m} "
            f"C{cx + hw},{m + 70} {cx + jw + 22},{b - 6} {cx},{b} "
            f"C{cx - jw - 22},{b - 6} {cx - hw},{m + 70} {cx - hw},{m} "
            f"C{cx - hw},{m - 70} {cx - hw * .95},{t} {cx},{t} Z")


def svg(c):
    sk, sd = SKIN[c.skin]
    t, b = c.top, c.bot
    ey = t + (b - t) * .47
    hid = c.uid("h")
    o = [f"<rect width='400' height='460' fill='{c.bg}'/>",
         f"<circle cx='70' cy='60' r='60' fill='#fff' opacity='.13'/><circle cx='340' cy='120' r='34' fill='#fff' opacity='.1'/>",
         f"<defs><clipPath id='{hid}'><path d='{head_path(c)}'/></clipPath></defs>"]
    # dlouhé vlasy za hlavou
    if c.hair in ("long", "longblond"):
        o.append(f"<path d='M{200 - c.hw - 22},{ey - 40} C{200 - c.hw - 30},{t - 40} {200 + c.hw + 30},{t - 40} {200 + c.hw + 22},{ey - 40} "
                 f"L{200 + c.hw + 34},{430} L{200 - c.hw - 34},{430} Z' fill='{c.hc}' stroke='{LN}' stroke-width='{SW}' stroke-linejoin='round'/>")
    if c.bun:
        o.append(f"<circle cx='{200 + 40}' cy='{t - 18}' r='38' fill='{c.hc}' stroke='{LN}' stroke-width='{SW}'/>")
    # tělo
    o.append(body(c, sk, sd))
    # krk
    o.append(f"<path d='M168,{b - 40} L166,{b + 40} Q200,{b + 58} 234,{b + 40} L232,{b - 40} Z' fill='{sd}' stroke='{LN}' stroke-width='{SW}'/>")
    # uši
    for sx in (-1, 1):
        ex = 200 + sx * (c.hw - 4)
        o.append(f"<ellipse cx='{ex + sx * 8}' cy='{ey + 8}' rx='16' ry='24' fill='{sk}' stroke='{LN}' stroke-width='{SW}'/>"
                 f"<path d='M{ex + sx * 10},{ey - 4} q{sx * 8},10 0,22' fill='none' stroke='{LN}' stroke-width='2.5' stroke-linecap='round'/>")
        if c.earring:
            o.append(f"<circle cx='{ex + sx * 10}' cy='{ey + 36}' r='6' fill='#F5C518' stroke='{LN}' stroke-width='2.5'/>")
    # hlava + stínování
    o.append(f"<path d='{head_path(c)}' fill='{sk}' stroke='{LN}' stroke-width='{SW}' stroke-linejoin='round'/>")
    o.append(f"<g clip-path='url(#{hid})'><path d='M{200 + c.hw * .45},{t - 20} C{200 + c.hw * .9},{t + 80} {200 + c.hw * .8},{b - 60} {200 + c.jw * .4},{b + 20} L{260 + c.hw},{b + 20} L{260 + c.hw},{t - 20} Z' fill='{sd}' opacity='.55'/>")
    if c.stub:
        o.append(f"<path d='M{200 - c.hw},{ey + 50} Q200,{ey + 30} {200 + c.hw},{ey + 50} L{200 + c.hw},{b + 10} L{200 - c.hw},{b + 10} Z' fill='#5a4636' opacity='.22'/>")
    if c.beard:
        bc = c.bc or c.hc
        o.append(f"<path d='M{200 - c.hw - 5},{ey + 18} C{200 - c.hw + 10},{ey + 80} {170},{ey + 58} 200,{ey + 60} C{230},{ey + 58} {200 + c.hw - 10},{ey + 80} {200 + c.hw + 5},{ey + 18} "
                 f"L{200 + c.hw + 5},{b + 30} L{200 - c.hw - 5},{b + 30} Z' fill='{bc}'/>")
    o.append("</g>")
    if c.beard:  # obrys vousů po bradě
        o.append(f"<path d='{head_path(c)}' fill='none' stroke='{LN}' stroke-width='{SW}'/>")
    if c.mole:
        o.append(f"<circle cx='{200 + 44}' cy='{ey + 74}' r='3.5' fill='#6b4a35'/>")
    # vlasy navrch
    o.append(hair(c, ey, hid))
    # obočí
    for sx in (-1, 1):
        x0 = 200 + sx * 14
        x1 = 200 + sx * 62
        lift = {"flat": (0, 0), "raised": (0, -12 if sx > 0 else 0), "angry": (8, -4), "sad": (-6, 6)}[c.brows]
        o.append(f"<path d='M{x0},{ey - 36 + lift[0]} Q{(x0 + x1) / 2},{ey - 46 + lift[1]} {x1},{ey - 38 + lift[1]}' fill='none' stroke='{c.hc if c.hair not in ('bald',) else LN}' stroke-width='7' stroke-linecap='round'/>"
                 f"<path d='M{x0},{ey - 36 + lift[0]} Q{(x0 + x1) / 2},{ey - 46 + lift[1]} {x1},{ey - 38 + lift[1]}' fill='none' stroke='{LN}' stroke-width='2' stroke-linecap='round' opacity='.6'/>")
    # oči (přivřená víčka)
    for sx in (-1, 1):
        cx, rx, ry = 200 + sx * 31, 29, 23
        eid = c.uid("e")
        lidy = ey - ry + ry * 2 * c.lid
        o.append(f"<defs><clipPath id='{eid}'><ellipse cx='{cx}' cy='{ey}' rx='{rx}' ry='{ry}'/></clipPath></defs>"
                 f"<ellipse cx='{cx}' cy='{ey}' rx='{rx}' ry='{ry}' fill='#FFFDF4'/>"
                 f"<g clip-path='url(#{eid})'><circle cx='{cx + c.look[0] + sx * 2}' cy='{ey + c.look[1] + 4}' r='7.5' fill='{LN}'/>"
                 f"<circle cx='{cx + c.look[0] + sx * 2 + 2.5}' cy='{ey + c.look[1] + 1.5}' r='2' fill='#fff'/>"
                 f"<rect x='{cx - rx - 2}' y='{ey - ry - 2}' width='{rx * 2 + 4}' height='{lidy - (ey - ry) + 2}' fill='{sk}'/>"
                 f"<rect x='{cx - rx - 2}' y='{ey - ry - 2}' width='{rx * 2 + 4}' height='{lidy - (ey - ry) + 2}' fill='{sd}' opacity='.35'/></g>"
                 f"<path d='M{cx - rx + 1},{lidy + 2} Q{cx},{lidy - 4} {cx + rx - 1},{lidy + 2}' fill='none' stroke='{LN}' stroke-width='3.5' stroke-linecap='round'/>"
                 f"<ellipse cx='{cx}' cy='{ey}' rx='{rx}' ry='{ry}' fill='none' stroke='{LN}' stroke-width='3'/>")
        if c.lashes:
            ox = cx + sx * (rx - 4)
            o.append(f"<path d='M{ox},{lidy} l{sx * 12},-8 M{ox - sx * 6},{lidy - 3} l{sx * 9},-11' stroke='{LN}' stroke-width='3' stroke-linecap='round'/>")
    if c.glasses == "sun":
        o.append(f"<path d='M140,{ey - 22} h50 q10,0 10,10 v12 q0,22 -30,22 q-34,0 -34,-26 q0,-18 4,-18 Z M260,{ey - 22} h-50 q-10,0 -10,10 v12 q0,22 30,22 q34,0 34,-26 q0,-18 -4,-18 Z' fill='{c.gtint}' stroke='{LN}' stroke-width='{SW}' stroke-linejoin='round'/>"
                 f"<line x1='190' y1='{ey - 14}' x2='210' y2='{ey - 14}' stroke='{LN}' stroke-width='5'/>"
                 f"<line x1='136' y1='{ey - 18}' x2='{200 - c.hw + 2}' y2='{ey - 10}' stroke='{LN}' stroke-width='5'/><line x1='264' y1='{ey - 18}' x2='{200 + c.hw - 2}' y2='{ey - 10}' stroke='{LN}' stroke-width='5'/>"
                 f"<path d='M150,{ey - 14} l14,0 M218,{ey - 14} l14,0' stroke='#fff' stroke-width='4' stroke-linecap='round' opacity='.55'/>")
    elif c.glasses == "frame":
        o.append(f"<rect x='{200 - 66}' y='{ey - 28}' width='64' height='54' rx='14' fill='#fff' fill-opacity='.12' stroke='{LN}' stroke-width='6'/>"
                 f"<rect x='{200 + 2}' y='{ey - 28}' width='64' height='54' rx='14' fill='#fff' fill-opacity='.12' stroke='{LN}' stroke-width='6'/>"
                 f"<path d='M{200 - 2},{ey - 8} q2,-6 4,0' stroke='{LN}' stroke-width='5' fill='none'/>")
    # nos
    o.append(nose(c, ey, sk, sd))
    # pusa
    o.append(mouth(c, ey))
    if c.phones:
        o.append(f"<path d='M{200 - c.hw - 6},{ey + 4} C{200 - c.hw - 14},{t - 70} {200 + c.hw + 14},{t - 70} {200 + c.hw + 6},{ey + 4}' fill='none' stroke='{LN}' stroke-width='18' stroke-linecap='round'/>"
                 f"<path d='M{200 - c.hw - 6},{ey + 4} C{200 - c.hw - 14},{t - 70} {200 + c.hw + 14},{t - 70} {200 + c.hw + 6},{ey + 4}' fill='none' stroke='{c.phones}' stroke-width='10' stroke-linecap='round'/>")
        for sx in (-1, 1):
            o.append(f"<rect x='{200 + sx * (c.hw + 6) - 18}' y='{ey - 18}' width='36' height='56' rx='14' fill='{c.phones}' stroke='{LN}' stroke-width='{SW}'/>")
    if c.earpiece:
        x = 200 + c.hw + 4
        o.append(f"<path d='M{x},{ey + 18} c18,14 -10,30 8,46 c16,14 -12,30 4,50' fill='none' stroke='{LN}' stroke-width='3'/><circle cx='{x - 2}' cy='{ey + 14}' r='6' fill='{LN}'/>")
    if c.deck:
        o.append(deck(c))
    return f"<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 400 460'>{''.join(o)}</svg>"


def body(c, sk, sd):
    b = c.bot
    o = []
    if c.tank:
        o.append(f"<path d='M30,460 C30,{b + 70} 100,{b + 30} 200,{b + 26} C300,{b + 30} 370,{b + 70} 370,460 Z' fill='{sk}' stroke='{LN}' stroke-width='{SW}'/>")
        o.append(f"<path d='M112,460 L120,{b + 52} Q200,{b + 96} 280,{b + 52} L288,460 Z' fill='{c.shirt}' stroke='{LN}' stroke-width='{SW}'/>")
        if c.tattoo:
            o.append(f"<path d='M58,{b + 90} q20,-14 30,6 q-14,14 -30,-6 M70,{b + 118} l26,10 M300,{b + 80} c14,10 24,6 30,20 M312,{b + 112} q14,-10 26,4' fill='none' stroke='#2f5d8a' stroke-width='4' stroke-linecap='round'/>")
    else:
        o.append(f"<path d='M30,460 C30,{b + 70} 100,{b + 30} 200,{b + 26} C300,{b + 30} 370,{b + 70} 370,460 Z' fill='{c.shirt}' stroke='{LN}' stroke-width='{SW}'/>")
        o.append(f"<path d='M150,{b + 30} Q200,{b + 70} 250,{b + 30}' fill='none' stroke='{LN}' stroke-width='{SW}'/>")
        if c.jacket:
            o.append(f"<path d='M30,460 C30,{b + 70} 90,{b + 36} 150,{b + 28} L180,460 Z M370,460 C370,{b + 70} 310,{b + 36} 250,{b + 28} L220,460 Z' fill='{c.jacket}' stroke='{LN}' stroke-width='{SW}' stroke-linejoin='round'/>")
    if c.stext and not c.deck:
        o.append(f"<text x='200' y='{b + 118}' text-anchor='middle' font-family='Arial Black,Arial' font-weight='900' font-size='26' letter-spacing='2' fill='{c.stc}'>{c.stext}</text>")
    if c.stext and c.deck:
        o.append(f"<text x='200' y='{b + 70}' text-anchor='middle' font-family='Arial Black,Arial' font-weight='900' font-size='15' letter-spacing='1' fill='{c.stc}'>{c.stext}</text>")
    return "".join(o)


def hair(c, ey, hid):
    t, hw, hcl = c.top, c.hw, c.hc
    line = ey - 62
    o = []
    hp = head_path(c, sc=1.05)
    if c.cap:
        cid = c.uid("c")
        o.append(f"<defs><clipPath id='{cid}'><rect x='0' y='0' width='400' height='{line + 8}'/></clipPath></defs>"
                 f"<path d='{head_path(c, sc=1.07)}' transform='translate(0,-12)' fill='{c.capc}' stroke='{LN}' stroke-width='{SW}' clip-path='url(#{cid})'/>"
                 f"<path d='M{200 - hw - 4},{line + 2} L{200 + hw + 4},{line + 2}' stroke='{LN}' stroke-width='{SW}'/>")
        if c.cap == "beanie":
            o.append(f"<rect x='{200 - hw - 8}' y='{line - 26}' width='{hw * 2 + 16}' height='34' rx='12' fill='{c.capc}' stroke='{LN}' stroke-width='{SW}'/>"
                     f"<path d='" + " ".join(f"M{x},{line - 20} v22" for x in range(int(200 - hw + 6), int(200 + hw), 16)) + f"' stroke='{LN}' stroke-width='2' opacity='.35'/>")
        else:
            o.append(f"<path d='M{200 - hw + 10},{line + 2} Q200,{line + 34} {200 + hw + 46},{line + 8} Q{200 + hw + 10},{line - 6} {200 - hw + 10},{line + 2} Z' fill='{c.capc}' stroke='{LN}' stroke-width='{SW}' stroke-linejoin='round'/>"
                     f"<circle cx='200' cy='{t - 10}' r='7' fill='{c.capc}' stroke='{LN}' stroke-width='3'/>")
        return "".join(o)
    if c.hair == "bald":
        return f"<ellipse cx='{200 - 24}' cy='{t + 26}' rx='34' ry='13' fill='#fff' opacity='.45' transform='rotate(-14 176 {t + 26})'/>"
    if c.hair in ("short", "long", "longblond", "receding"):
        cid = c.uid("c")
        wave = " ".join(f"L{x},{line + (10 if (x // 22) % 2 else -2)}" for x in range(int(200 - hw - 20), int(200 + hw + 24), 22))
        if c.hair == "receding":
            o.append(f"<defs><clipPath id='{cid}'><path d='M0,0 H400 V{line + 20} H{200 + hw - 30} V{t + 40} H{200 - hw + 30} V{line + 20} H0 Z'/></clipPath></defs>")
        elif c.hair in ("long", "longblond"):
            o.append(f"<defs><clipPath id='{cid}'><path d='M0,0 H400 V{line + 6} Q300,{line - 24} 210,{line - 40} L200,{line - 28} Q120,{line + 10} 0,{line + 6} Z'/></clipPath></defs>")
        else:
            o.append(f"<defs><clipPath id='{cid}'><path d='M0,0 H400 V{line} {wave} L0,{line} Z'/></clipPath></defs>")
        o.append(f"<path d='{hp}' transform='translate(0,-8)' fill='{hcl}' stroke='{LN}' stroke-width='{SW}' clip-path='url(#{cid})'/>")
        o.append(f"<path d='M{200 - 40},{t + 4} q30,-10 60,0' stroke='#fff' stroke-width='5' fill='none' opacity='.25' stroke-linecap='round'/>")
        return "".join(o)
    if c.hair == "curly":
        import math
        for i in range(15):
            a = math.pi * (1.0 + i / 14)
            x = 200 + math.cos(a) * (hw + 4)
            y = ey - 30 + math.sin(a) * (ey - t + 10)
            o.append(f"<circle cx='{x:.0f}' cy='{y:.0f}' r='{30 + (i % 3) * 4}' fill='{hcl}' stroke='{LN}' stroke-width='{SW}'/>")
        for i in range(5):
            o.append(f"<circle cx='{150 + i * 25}' cy='{t + 8 + (i % 2) * 10}' r='30' fill='{hcl}' stroke='{LN}' stroke-width='{SW}'/>")
        return "".join(o)
    if c.hair == "spiky":
        pts = []
        n = 9
        for i in range(n + 1):
            x = 200 - hw - 8 + (hw * 2 + 16) * i / n
            pts.append(f"{x:.0f},{line + 6}" if i in (0, n) else f"{x:.0f},{t - 44 - (i % 2) * 18 + abs(i - n / 2) * 8:.0f} {x + (hw * 2 + 16) / n / 2:.0f},{t + 4}")
        o.append(f"<polygon points='{' '.join(pts)} {200 + hw + 8},{line + 6}' fill='{hcl}' stroke='{LN}' stroke-width='{SW}' stroke-linejoin='round'/>")
        return "".join(o)
    return ""


def nose(c, ey, sk, sd):
    y0 = ey + 6
    if c.nose == "long":
        return (f"<path d='M204,{y0} C212,{y0 + 30} 232,{y0 + 52} 222,{y0 + 70} C212,{y0 + 82} 196,{y0 + 78} 188,{y0 + 70}' fill='{sk}' stroke='{LN}' stroke-width='{SW}' stroke-linecap='round' stroke-linejoin='round'/>"
                f"<path d='M212,{y0 + 66} q-6,6 -12,2' fill='none' stroke='{LN}' stroke-width='3' stroke-linecap='round'/>")
    if c.nose == "bulb":
        return (f"<path d='M198,{y0} C196,{y0 + 30} 190,{y0 + 46} 196,{y0 + 52}' fill='none' stroke='{LN}' stroke-width='3.5' stroke-linecap='round'/>"
                f"<ellipse cx='206' cy='{y0 + 62}' rx='24' ry='19' fill='{sd}' stroke='{LN}' stroke-width='{SW}'/><ellipse cx='198' cy='{y0 + 56}' rx='7' ry='4' fill='#fff' opacity='.4'/>")
    if c.nose == "hook":
        return (f"<path d='M200,{y0} C220,{y0 + 14} 240,{y0 + 50} 226,{y0 + 76} C214,{y0 + 84} 204,{y0 + 70} 196,{y0 + 74}' fill='{sk}' stroke='{LN}' stroke-width='{SW}' stroke-linecap='round' stroke-linejoin='round'/>")
    return (f"<path d='M202,{y0 + 18} C210,{y0 + 34} 214,{y0 + 46} 204,{y0 + 52} C198,{y0 + 54} 194,{y0 + 50} 192,{y0 + 48}' fill='{sk}' stroke='{LN}' stroke-width='{SW}' stroke-linecap='round' stroke-linejoin='round'/>")


def mouth(c, ey):
    y = ey + 108
    lip = c.lips
    if c.mouth == "flat":
        s = f"<path d='M176,{y} Q200,{y + 3} 224,{y - 2}' fill='none' stroke='{LN}' stroke-width='4.5' stroke-linecap='round'/>"
    elif c.mouth == "smirk":
        s = f"<path d='M174,{y + 2} Q200,{y + 6} 228,{y - 8}' fill='none' stroke='{LN}' stroke-width='4.5' stroke-linecap='round'/><path d='M226,{y - 12} q5,4 4,9' fill='none' stroke='{LN}' stroke-width='3' stroke-linecap='round'/>"
    elif c.mouth == "frown":
        s = f"<path d='M176,{y + 4} Q200,{y - 6} 224,{y + 4}' fill='none' stroke='{LN}' stroke-width='4.5' stroke-linecap='round'/>"
    elif c.mouth == "grin":
        s = (f"<path d='M168,{y - 6} Q200,{y + 36} 234,{y - 8} Q200,{y + 2} 168,{y - 6} Z' fill='#5a1e1e' stroke='{LN}' stroke-width='4' stroke-linejoin='round'/>"
             f"<path d='M174,{y - 4} Q200,{y + 6} 228,{y - 6} L226,{y + 4} Q200,{y + 12} 176,{y + 4} Z' fill='#fff'/>")
    else:  # "o"
        s = f"<ellipse cx='202' cy='{y}' rx='11' ry='14' fill='#5a1e1e' stroke='{LN}' stroke-width='4'/>"
    if lip:
        s = (f"<path d='M176,{y} Q190,{y - 10} 200,{y - 4} Q210,{y - 10} 224,{y} Q200,{y + 16} 176,{y} Z' fill='{lip}' stroke='{LN}' stroke-width='3.5' stroke-linejoin='round'/>"
             f"<path d='M178,{y} Q200,{y + 3} 222,{y}' fill='none' stroke='{LN}' stroke-width='2.5'/>")
    return s


def deck(c):
    return ("<rect x='40' y='392' width='320' height='80' rx='14' fill='#1c1b1f' stroke='" + LN + "' stroke-width='5'/>"
            "<ellipse cx='108' cy='414' rx='46' ry='11' fill='#38363d' stroke='#0d0d0f' stroke-width='3'/><ellipse cx='292' cy='414' rx='46' ry='11' fill='#38363d' stroke='#0d0d0f' stroke-width='3'/>"
            "<circle cx='190' cy='412' r='5' fill='#ff3d7f'/><circle cx='210' cy='412' r='5' fill='#ff3d7f'/>"
            "<text x='200' y='446' text-anchor='middle' font-family='Arial Black,Arial' font-weight='900' font-size='20' letter-spacing='1.5' fill='#fff'>STUDIO 54</text>")


CHARS = {
    "pepa": C(bg="#cfd6da", hair="bald", hw=112, top=70, bot=322, jw=70, glasses="sun", nose="bulb", mouth="frown", stub=True, brows="angry",
              shirt="#1b1b1d", stext="SECURITY", earpiece=True, deck=False),
    "petya": C(bg="#d6d0c8", hair="short", hc="#3d2a1d", beard=True, hw=94, jw=52, lid=.55, nose="long", mouth="smirk",
               shirt="#6d1f2c", jacket="#2b2b2e", stext="PÉŤA", deck=False, look=(4, 2)),
    "denisa": C(bg="#d9cfd6", hair="long", hc="#1d1514", hw=86, top=88, bot=312, jw=34, lid=.45, lashes=True, nose="small",
                lips="#e0457b", earring=True, shirt="#151417", stext="DENISA", deck=False, look=(-4, 2), brows="raised"),
    "martina": C(bg="#d2d7cf", hair="short", hc="#2a1a14", bun="#2a1a14", hw=88, top=92, bot=314, jw=36, glasses="sun", nose="small",
                 lips="#d23b53", tank=True, tattoo=True, shirt="#141316", stext="MARTINA", earring=True, deck=False, mole=True),
    "dj_rio": C(bg="#2fd3f5", skin="tan", hair="curly", hc="#1e1512", hw=92, jw=44, lid=.42, mouth="grin", nose="small", shirt="#ff3f8e", stext="RIO"),
    "dj_richie": C(bg="#7a3cff", hair="short", hc="#5a3a24", glasses="frame", hw=90, jw=40, lid=.5, mouth="smirk", nose="long", shirt="#f4f1ea", stext=""),
    "dj_carl_cross": C(bg="#c6f02e", hair="bald", hw=100, top=74, jw=54, lid=.52, nose="bulb", mouth="grin", stub=True, shirt="#151417", stext="B-DAY", stc="#c6f02e"),
    "dj_yan_lan": C(bg="#ff2f78", hair="bald", beard=True, hc="#5b3a22", hw=102, jw=56, lid=.6, nose="hook", mouth="flat", shirt="#a9cbe8", stext="YAN LAN", stc="#1b1b1d", brows="raised"),
    "djTommy": C(bg="#ff2f78", hair="spiky", hc="#e7c76c", hw=92, jw=46, lid=.48, nose="long", mouth="smirk", stub=True, shirt="#f4f1ea", stext=""),
    "dj_manuel_garcia": C(bg="#27c46b", skin="brown", hair="short", hc="#181210", hw=94, jw=48, lid=.5, nose="bulb", mouth="grin", stub=True, shirt="#f4f1ea", stext=""),
    "dj_terran": C(bg="#efece4", hair="short", hc="#8a6a4c", phones="#2a2a2e", hw=88, top=86, jw=40, lid=.62, nose="small", mouth="flat", shirt="#151417", stext="TERRAN", look=(5, 3)),
    "dj_jose_madeira": C(bg="#ff9a1f", hair="short", hc="#1e1714", cap="cap", capc="#18181b", hw=92, jw=48, lid=.48, nose="long", mouth="smirk", stub=True, shirt="#151417", stext="AIX", brows="raised"),
    "dj_cobra": C(bg="#c6f02e", hair="longblond", hc="#e6c66e", glasses="sun", gtint="#1b3d12", hw=90, jw=42, nose="small", mouth="smirk", shirt="#151417", stext="COBRA", stc="#c6f02e"),
    "dj_jumbo": C(bg="#ffd21f", skin="tan", hair="short", hc="#2a1d16", cap="beanie", capc="#ff4f7b", beard=True, hw=100, jw=54, lid=.5, nose="bulb", mouth="grin", shirt="#151417", stext="JUMBO"),
    "dj_jack_dorman": C(bg="#2fd3f5", hair="short", hc="#2a1d16", cap="cap", capc="#18181b", phones="#ff6fae", glasses="frame", hw=90, jw=42, lid=.46, nose="long", mouth="grin", shirt="#151417", stext="B-DAY", stc="#2fd3f5"),
    "djEnrico": C(bg="#ff2f78", hair="short", hc="#2a1d16", cap="cap", capc="#25304f", hw=94, jw=46, lid=.5, nose="hook", mouth="grin", shirt="#25304f", stext="★ ★ ★", stc="#fff"),
}


def main():
    OUT.mkdir(exist_ok=True)
    cells = []
    for k, c in CHARS.items():
        s = svg(c)
        (OUT / f"{k}.svg").write_text(s, encoding="utf-8")
        cells.append(f"<div style='font:12px sans-serif'><img src='{k}.svg' width='180'><br>{k}</div>")
    (OUT / "_sheet.html").write_text("<body style='margin:0;background:#888;display:flex;flex-wrap:wrap;gap:8px'>" + "".join(cells) + "</body>", encoding="utf-8")
    print(len(CHARS), "postav")


if __name__ == "__main__":
    main()
