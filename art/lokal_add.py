# Jednorázově rozšíří lokal.py o kostýmy (Flintstone, kovboj, bongo) a DJs nocí 10. a 11. 10. 2026.
import pathlib

p = pathlib.Path(__file__).with_name("lokal.py")
s = p.read_text(encoding="utf-8")
if "neckphones" in s:
    raise SystemExit("už rozšířeno")

s = s.replace("earpiece=False, bun=None, mole=False))",
              "earpiece=False, bun=None, mole=False, spots=None, tie=None, hat=None, goatee=None,\n"
              "                               neckphones=None, bongo=False, club=False))")

old = "    if c.stext and not c.deck:"
new = '''    if c.spots:  # Flintstone: černé fleky na triku
        for x, y, rx, ry, a in [(78, b + 96, 24, 15, -20), (128, b + 128, 15, 11, 15), (318, b + 92, 22, 14, 25), (272, b + 126, 14, 10, -10),
                                (104, b + 58, 12, 8, 5), (334, b + 140, 12, 8, 0), (60, b + 140, 10, 7, 0)]:
            o.append(f"<ellipse cx='{x}' cy='{y}' rx='{rx}' ry='{ry}' fill='{c.spots}' transform='rotate({a} {x} {y})'/>")
    if c.tie:  # kravata přes krk
        o.append(f"<path d='M146,{b + 30} Q200,{b + 66} 254,{b + 30} L244,{b + 48} Q200,{b + 82} 156,{b + 48} Z' fill='{c.tie}' stroke='{LN}' stroke-width='{SW}' stroke-linejoin='round'/>"
                 f"<path d='M192,{b + 66} L172,{b + 130} L200,{b + 146} L228,{b + 130} L208,{b + 66} Z' fill='{c.tie}' stroke='{LN}' stroke-width='{SW}' stroke-linejoin='round'/>")
    if c.neckphones:  # sluchátka kolem krku
        o.append(f"<path d='M140,{b + 20} Q200,{b + 78} 260,{b + 20}' fill='none' stroke='{LN}' stroke-width='16' stroke-linecap='round'/>"
                 f"<path d='M140,{b + 20} Q200,{b + 78} 260,{b + 20}' fill='none' stroke='{c.neckphones}' stroke-width='9' stroke-linecap='round'/>")
        for x in (132, 268):
            o.append(f"<ellipse cx='{x}' cy='{b + 34}' rx='24' ry='30' fill='{c.neckphones}' stroke='{LN}' stroke-width='{SW}'/><ellipse cx='{x}' cy='{b + 34}' rx='12' ry='16' fill='#2a2a2e'/>")
    if c.stext and not c.deck:'''
assert old in s
s = s.replace(old, new, 1)

old = "    if c.deck:\n        o.append(deck(c))"
new = '''    if c.goatee:
        o.append(f"<path d='M184,{ey + 122} Q200,{ey + 160} 216,{ey + 122} Q200,{ey + 132} 184,{ey + 122} Z' fill='{c.goatee}' stroke='{LN}' stroke-width='3'/>"
                 f"<path d='M176,{ey + 96} Q200,{ey + 86} 224,{ey + 96}' fill='none' stroke='{c.goatee}' stroke-width='7' stroke-linecap='round'/>")
    if c.hat:  # kovbojský klobouk
        line = ey - 62
        o.append(f"<path d='M{200 - c.hw - 70},{line + 6} Q200,{line + 44} {200 + c.hw + 70},{line + 6} Q{200 + c.hw + 40},{line - 16} 200,{line - 10} Q{200 - c.hw - 40},{line - 16} {200 - c.hw - 70},{line + 6} Z' fill='{c.hat}' stroke='{LN}' stroke-width='{SW}' stroke-linejoin='round'/>"
                 f"<path d='M{200 - c.hw + 12},{line} C{200 - c.hw + 6},{t - 70} {200 - 30},{t - 50} 200,{t - 34} C{200 + 30},{t - 50} {200 + c.hw - 6},{t - 70} {200 + c.hw - 12},{line} Q200,{line + 14} {200 - c.hw + 12},{line} Z' fill='{c.hat}' stroke='{LN}' stroke-width='{SW}' stroke-linejoin='round'/>"
                 f"<path d='M{200 - c.hw + 10},{line - 14} Q200,{line} {200 + c.hw - 10},{line - 14} L{200 + c.hw - 8},{line - 2} Q200,{line + 12} {200 - c.hw + 8},{line - 2} Z' fill='#2b1e18'/>"
                 + "".join(f"<path d='M{x},{line - 12} l6,10' stroke='#fff' stroke-width='2.5' opacity='.6'/>" for x in range(int(200 - c.hw + 18), int(200 + c.hw - 14), 16)))
    if c.club:  # pravěkej kyj (Flintstone)
        o.append(f"<path d='M318,{t + 40} C352,{t - 10} 392,{t + 6} 380,{t + 60} L344,{b + 120} Q330,{b + 132} 318,{b + 118} Z' fill='#c03a7a' stroke='{LN}' stroke-width='{SW}' stroke-linejoin='round'/>"
                 f"<path d='M346,{t + 20} q16,30 -2,70' fill='none' stroke='#fff' stroke-width='5' opacity='.45' stroke-linecap='round'/>"
                 f"<ellipse cx='326' cy='{b + 96}' rx='22' ry='16' fill='{sk}' stroke='{LN}' stroke-width='{SW}'/>")
    if c.bongo:
        o.append(f"<path d='M110,400 L290,400 L270,470 L130,470 Z' fill='#c9873f' stroke='{LN}' stroke-width='5' stroke-linejoin='round'/>"
                 f"<ellipse cx='200' cy='400' rx='92' ry='18' fill='#f2e6cc' stroke='{LN}' stroke-width='5'/>"
                 f"<path d='M120,420 L280,420 M126,444 L274,444' stroke='{LN}' stroke-width='3' opacity='.5'/>")
    if c.deck:
        o.append(deck(c))'''
assert old in s
s = s.replace(old, new, 1)

old = '    "djEnrico": C('
new = '''    # 10. 10. Narozeniny Landchi
    "dj_mark_evill": C(bg="#F4DD95", hair="spiky", hc="#141216", hw=90, jw=42, lid=.6, nose="hook", mouth="smirk", brows="angry", stub=True, shirt="#141316", stext="EVILL", stc="#E3B448", earring=True),
    "dj_landchi": C(bg="#E3B448", hair="short", hc="#3a261a", beard=True, hw=110, top=76, bot=324, jw=66, lid=.42, nose="bulb", mouth="grin", shirt="#f26a1b",
                    spots="#1b1512", tie="#9fc3d6", club=True, deck=False, stext="", look=(2, 3)),
    "dj_yoppa_parrot": C(bg="#efe6d2", skin="tan", hair="spiky", hc="#2fa84f", hw=88, jw=40, lid=.44, nose="hook", mouth="grin", glasses="sun", gtint="#d23b53", shirt="#151417", stext="YOPPA", stc="#2fa84f"),
    "dj_em_dot": C(bg="#E3B448", hair="long", hc="#141216", hw=84, top=88, bot=312, jw=34, lid=.48, lashes=True, nose="small", lips="#b23a48", earring=True, shirt="#151417", stext="EM.DOT", stc="#E3B448", look=(-3, 2)),
    "dj_peet_v": C(bg="#F4DD95", hair="receding", hc="#5a3a24", hw=96, jw=50, lid=.55, nose="long", mouth="flat", glasses="frame", stub=True, shirt="#f4f1ea", stext="PEET V", stc="#151417"),
    # 11. 10. Mazerlogy
    "dj_calvin_west": C(bg="#efe6d2", skin="brown", hair="bald", hw=96, top=74, jw=50, lid=.5, nose="bulb", mouth="smirk", beard=True, hc="#181210", shirt="#151417", stext="WEST", stc="#E3B448"),
    "dj_mazer": C(bg="#E3B448", hair="short", hc="#2a1d16", hw=86, top=84, jw=38, lid=.58, nose="long", mouth="flat", brows="angry", neckphones="#f4f1ea", shirt="#1d1f33", stext="MAZER", stc="#E3B448", look=(0, 3)),
    "dj_jerome_levis": C(bg="#F4DD95", skin="tan", hair="curly", hc="#1e1512", hw=90, jw=44, lid=.5, nose="hook", mouth="grin", stub=True, shirt="#f4f1ea", stext="JEROME", stc="#151417"),
    "dj_mike_frost": C(bg="#efe6d2", hair="short", hc="#d9d4c8", hw=92, jw=46, lid=.55, nose="small", mouth="smirk", glasses="sun", gtint="#2a6f9a", shirt="#151417", stext="FROST", stc="#bfe3f5"),
    "josef_rafael": C(bg="#E3B448", skin="tan", hair="short", hc="#1e1512", hat="#d8bf8a", goatee="#1e1512", hw=94, jw=46, lid=.5, nose="hook", mouth="grin", shirt="#9a9a9a", bongo=True, deck=False, stext=""),
    "djEnrico": C('''
assert old in s
s = s.replace(old, new, 1)
p.write_text(s, encoding="utf-8")
print("ok")
