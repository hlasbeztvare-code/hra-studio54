# Doplní do Passion One (Google Fonts) chybějící české znaky č ď ě ň ť ů + verzálky
# složením z vlastních glyfů písma (háček/kroužek/apostrof). Výstup: woff2 pro hru.
import pathlib
from fontTools.ttLib import TTFont
from fontTools.pens.boundsPen import BoundsPen
from fontTools.ttLib.tables._g_l_y_f import GlyphComponent, Glyph

D = pathlib.Path(__file__).with_name("fonts")


def build(src, out):
    f = TTFont(D / src)
    gs, glyf, hmtx = f.getGlyphSet(), f["glyf"], f["hmtx"]

    def bb(n):
        p = BoundsPen(gs); gs[n].draw(p); return p.bounds

    def comp(name, uni, parts, adv=None):
        g = Glyph(); g.numberOfContours = -1; g.components = []
        for gn, dx, dy in parts:
            c = GlyphComponent(); c.glyphName = gn; c.x, c.y = int(round(dx)), int(round(dy)); c.flags = 0
            g.components.append(c)
        if name not in f.getGlyphOrder():
            f.setGlyphOrder(f.getGlyphOrder() + [name])
        glyf[name] = g
        a = adv if adv is not None else hmtx[parts[0][0]][0]
        hmtx[name] = (a, 0)
        for t in f["cmap"].tables:
            if t.isUnicode():
                t.cmap[uni] = name
        glyf[name].recalcBounds(glyf)

    cx = lambda b: (b[0] + b[2]) / 2
    car, ring = bb("caron"), bb("ring")
    # výška háčku nad minuskou / verzálkou podle š / Š
    s, sc, S, Sc = bb("s"), bb("scaron"), bb("S"), bb("Scaron")
    dy_lo = sc[3] - car[3]
    dy_up = Sc[3] - car[3]
    a, ar, A, Ar = bb("a"), bb("aring"), bb("A"), bb("Aring")
    ry_lo, ry_up = ar[3] - ring[3], Ar[3] - ring[3]

    def over(base, mark, mb, dy):
        b = bb(base); return [(base, 0, 0), (mark, cx(b) - cx(mb), dy)]

    for ch, base in (("č", "c"), ("ě", "e"), ("ň", "n")):
        comp(base + "caron", ord(ch), over(base, "caron", car, dy_lo))
    for ch, base in (("Č", "C"), ("Ď", "D"), ("Ě", "E"), ("Ň", "N"), ("Ť", "T")):
        comp(base + "caron", ord(ch), over(base, "caron", car, dy_up))
    comp("uring", ord("ů"), over("u", "ring", ring, ry_lo))
    comp("Uring", ord("Ů"), over("U", "ring", ring, ry_up))
    # ď ť: apostrof vpravo od dříku
    q = bb("quoteright")
    for ch, base in (("ď", "d"), ("ť", "t")):
        b = bb(base); adv = hmtx[base][0]
        x = b[2] - q[0] - 10
        top = b[3] - q[3]
        comp(base + "caron", ord(ch), [(base, 0, 0), ("quoteright", x, top)], adv=int(adv + (q[2] - q[0]) * .55))
    f.flavor = "woff2"
    f.save(D / out)
    print(out, "ok")


if __name__ == "__main__":
    build("PassionOne-Bold.ttf", "passion-cz-700.woff2")
    build("PassionOne-Regular.ttf", "passion-cz-400.woff2")
    build("PassionOne-Black.ttf", "passion-cz-900.woff2")
