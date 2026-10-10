# Komiksová písma (Bangers na popisky, Kalam na text) + kreslené ikony místo emoji (ingredience, výsledky, úkoly).
# Volá se z klub.patch() jako poslední.
from pop import uri, INK, Y, R, O, PAPER

S = f"stroke='{INK}' stroke-width='3.5' stroke-linejoin='round' stroke-linecap='round'"


def sv(body):
    return uri(f"<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'>{body}</svg>")


def slice_(outer, inner, seg):
    o = f"<circle cx='32' cy='32' r='26' fill='{outer}' {S}/><circle cx='32' cy='32' r='20' fill='{inner}'/>"
    o += "".join(f"<line x1='32' y1='32' x2='{32 + 18 * c:.1f}' y2='{32 + 18 * s:.1f}' stroke='{seg}' stroke-width='2.5'/>"
                 for c, s in [(1, 0), (.707, .707), (0, 1), (-.707, .707), (-1, 0), (-.707, -.707), (0, -1), (.707, -.707)])
    return o + f"<circle cx='32' cy='32' r='3' fill='{seg}'/><path d='M14,24 q4,-8 12,-11' fill='none' stroke='#fff' stroke-width='3' stroke-linecap='round' opacity='.7'/>"


def bottle(body, label, txt, tc=INK):
    return (f"<rect x='27' y='5' width='10' height='9' rx='2' fill='#2b2b2e' {S}/><path d='M27,14 h10 v6 q9,4 9,14 v22 q0,4 -4,4 h-20 q-4,0 -4,-4 v-22 q0,-10 9,-14 Z' fill='{body}' {S}/>"
            f"<rect x='19' y='34' width='26' height='13' rx='2' fill='{label}' stroke='{INK}' stroke-width='2.5'/>"
            f"<text x='32' y='44' text-anchor='middle' font-family='Arial Black,Arial' font-weight='900' font-size='9' fill='{tc}'>{txt}</text>"
            f"<line x1='22' y1='24' x2='22' y2='31' stroke='#fff' stroke-width='3' stroke-linecap='round' opacity='.7'/>")


ICONS = {
    "ic-limetka": sv(slice_("#5DAA2E", "#CDEB7A", "#F4FCD8")),
    "ic-pomeranc": sv(slice_("#F07800", "#FFC04D", "#FFF1C7")),
    "ic-okurka": sv(f"<circle cx='32' cy='32' r='26' fill='#2F7D27' {S}/><circle cx='32' cy='32' r='21' fill='#CFE8A0'/>"
                    + "".join(f"<ellipse cx='{32 + 9 * c:.1f}' cy='{32 + 9 * s:.1f}' rx='2.2' ry='3.6' fill='#8DBF5A' transform='rotate({a} {32 + 9 * c:.1f} {32 + 9 * s:.1f})'/>"
                              for a, c, s in [(0, 0, -1), (60, .87, -.5), (120, .87, .5), (0, 0, 1), (60, -.87, .5), (120, -.87, -.5)])),
    "ic-led": sv(f"<polygon points='12,22 32,11 52,22 32,33' fill='#E6F7FF' {S}/><polygon points='12,22 32,33 32,55 12,44' fill='#9ED8F5' {S}/>"
                 f"<polygon points='32,33 52,22 52,44 32,55' fill='#5DB6E8' {S}/><path d='M18,27 v10 M24,21 l8,-4' stroke='#fff' stroke-width='3' stroke-linecap='round'/>"),
    "ic-mata": sv(f"<path d='M30,58 C28,44 30,34 34,26' fill='none' {S}/><path d='M33,28 C20,30 8,20 10,8 C24,6 34,16 33,28 Z' fill='#3DAA4A' {S}/>"
                  f"<path d='M33,30 C44,22 58,26 58,38 C46,44 36,40 33,30 Z' fill='#56C25B' {S}/><path d='M31,26 L16,12 M36,31 L52,36' stroke='#1F6E2A' stroke-width='2' stroke-linecap='round'/>"),
    "ic-gin": sv(bottle("#D3F1FF", "#fff", "GIN")),
    "ic-rum": sv(bottle("#8B4A1C", Y, "RUM")),
    "ic-visen": sv(f"<path d='M22,40 C24,24 30,14 40,8 M42,40 C40,26 40,16 40,8' fill='none' stroke='#3B7A2A' stroke-width='3.5' stroke-linecap='round'/>"
                   f"<path d='M40,8 C48,4 56,8 56,14 C48,16 42,14 40,8 Z' fill='#56C25B' {S}/>"
                   f"<circle cx='20' cy='46' r='12' fill='#D7263D' {S}/><circle cx='44' cy='46' r='12' fill='#B5162C' {S}/>"
                   f"<circle cx='16' cy='42' r='3' fill='#fff' opacity='.75'/><circle cx='40' cy='42' r='3' fill='#fff' opacity='.75'/>"),
    "ic-tonic": sv(f"<rect x='18' y='10' width='28' height='46' rx='6' fill='#EEF5F9' {S}/><ellipse cx='32' cy='11' rx='13' ry='4' fill='#C9D4DB' {S}/>"
                   f"<rect x='18' y='26' width='28' height='16' fill='#1E88E5' stroke='{INK}' stroke-width='2.5'/>"
                   f"<text x='32' y='38' text-anchor='middle' font-family='Arial Black,Arial' font-weight='900' font-size='8' fill='#fff'>TONIC</text>"
                   f"<line x1='23' y1='16' x2='23' y2='22' stroke='#fff' stroke-width='3' stroke-linecap='round'/>"),
    "ic-chilli": sv(f"<path d='M44,14 C54,26 50,46 28,56 C20,59 12,56 16,52 C34,44 38,30 34,18 Z' fill='#E5231B' {S}/>"
                    f"<path d='M34,18 C36,10 42,8 46,12 L44,16 Z' fill='#3B9A3A' {S}/><path d='M46,12 q4,-6 0,-10' fill='none' stroke='#3B7A2A' stroke-width='3.5' stroke-linecap='round'/>"
                    f"<path d='M40,24 q2,10 -4,18' fill='none' stroke='#fff' stroke-width='3' stroke-linecap='round' opacity='.6'/>"),
    "ic-oliva": sv(f"<line x1='8' y1='56' x2='54' y2='8' stroke='#C79A5A' stroke-width='4' stroke-linecap='round'/><line x1='8' y1='56' x2='54' y2='8' stroke='{INK}' stroke-width='1.2'/>"
                   f"<ellipse cx='30' cy='34' rx='17' ry='13' fill='#7A9A2E' {S} transform='rotate(-40 30 34)'/><circle cx='34' cy='30' r='5.5' fill='#E5231B' stroke='{INK}' stroke-width='2.5'/>"
                   f"<path d='M20,36 q0,-8 6,-12' fill='none' stroke='#fff' stroke-width='3' stroke-linecap='round' opacity='.6'/>"),
    "ic-med": sv(f"<rect x='16' y='8' width='32' height='10' rx='3' fill='#8B4A1C' {S}/><path d='M14,18 h36 v34 q0,6 -6,6 h-24 q-6,0 -6,-6 Z' fill='#F5B400' {S}/>"
                 f"<path d='M14,22 q6,8 10,0 q4,10 8,0 q5,8 9,0 q4,6 9,0' fill='#FFD54A' stroke='{INK}' stroke-width='2.5'/>"
                 f"<rect x='20' y='34' width='24' height='12' rx='2' fill='{PAPER}' stroke='{INK}' stroke-width='2.5'/><text x='32' y='43.5' text-anchor='middle' font-family='Arial Black,Arial' font-weight='900' font-size='8.5' fill='{INK}'>MED</text>"),
    "ic-koktejl": sv(f"<line x1='42' y1='4' x2='35' y2='20' stroke='{INK}' stroke-width='2.5'/><circle cx='42' cy='9' r='5' fill='#5DBB3F' stroke='{INK}' stroke-width='2.5'/>"
                     f"<polygon points='7,12 57,12 32,38' fill='#fff' {S}/><polygon points='13,16 51,16 32,34' fill='#FF4F9A'/>"
                     f"<line x1='32' y1='38' x2='32' y2='56' stroke='{INK}' stroke-width='4'/><ellipse cx='32' cy='58' rx='13' ry='4' fill='#fff' stroke='{INK}' stroke-width='3'/>"),
    "ic-boom": sv(f"<polygon points='32,2 38,18 54,8 46,24 62,30 46,36 56,52 38,44 32,62 26,44 8,52 18,36 2,30 18,24 10,8 26,18' fill='{R}' {S}/>"
                  f"<polygon points='32,14 36,24 46,20 40,30 48,34 38,36 40,46 32,40 24,46 26,36 16,34 24,30 18,20 28,24' fill='{Y}'/>"),
    "ic-ruka": sv(f"<path d='M18,58 C12,48 10,38 12,30 C13,26 18,26 19,30 L21,36 L20,14 C20,9 27,9 27,14 L28,30 L28,9 C28,4 35,4 35,9 L35,30 L36,12 C36,7 43,7 43,12 L43,32 L45,20 C45,15 52,16 51,21 L49,40 C48,50 44,56 40,60 Z' fill='#F3CBA8' {S}/>"
                  f"<path d='M10,8 l-6,-4 M14,4 l-2,-4 M52,6 l6,-4' stroke='{INK}' stroke-width='3' stroke-linecap='round'/>"),
    "ic-star": sv(f"<polygon points='32,4 40,23 60,24 44,37 50,58 32,46 14,58 20,37 4,24 24,23' fill='{Y}' {S}/><path d='M24,26 l5,-1' stroke='#fff' stroke-width='3' stroke-linecap='round'/>"),
    "ic-q": sv(f"<circle cx='32' cy='32' r='26' fill='{PAPER}' {S}/><text x='32' y='45' text-anchor='middle' font-family='Arial Black,Arial' font-weight='900' font-size='36' fill='{R}' stroke='{INK}' stroke-width='1.5'>?</text>"),
    "ic-cil": sv(f"<circle cx='32' cy='32' r='27' fill='{R}' {S}/><circle cx='32' cy='32' r='19' fill='#fff' {S}/><circle cx='32' cy='32' r='11' fill='{R}' {S}/><circle cx='32' cy='32' r='4' fill='{Y}'/>"),
    "ic-dar": sv(f"<rect x='8' y='26' width='48' height='32' rx='3' fill='{R}' {S}/><rect x='5' y='18' width='54' height='12' rx='3' fill='#FF4F4F' {S}/>"
                 f"<rect x='28' y='18' width='8' height='40' fill='{Y}' stroke='{INK}' stroke-width='2.5'/><path d='M32,18 C22,4 10,10 18,18 Z M32,18 C42,4 54,10 46,18 Z' fill='{Y}' {S}/>"),
}
EMOJI = {"🍋": "ic-limetka", "🧊": "ic-led", "🌿": "ic-mata", "🍸": "ic-koktejl", "🥃": "ic-rum", "🍊": "ic-pomeranc", "🍒": "ic-visen", "🥤": "ic-tonic",
         "🌶️": "ic-chilli", "🥒": "ic-okurka", "🫒": "ic-oliva", "🍯": "ic-med", "💥": "ic-boom", "✋": "ic-ruka", "⭐": "ic-star", "❔": "ic-q", "🎯": "ic-cil", "🎁": "ic-dar"}
# Gin v ING má 🍸 – v mřížce/receptu ho chceme jako lahev; koktejl jen u Martiny
ING_IC = ["ic-limetka", "ic-led", "ic-mata", "ic-gin", "ic-rum", "ic-pomeranc", "ic-visen", "ic-tonic", "ic-chilli", "ic-okurka", "ic-oliva", "ic-med"]

CSS = ("\n/* ══ KOMIKSOVÁ PÍSMA + KRESLENÉ IKONY ══ */\n"
       ".game-root{font-family:'Kalam','Mali',sans-serif}\n"
       ".game-root .cap,.game-root p,.game-root .hud-toast,.game-root .chat>.gb,.game-root .opts>.gb,.game-root .mg-opts>button,.game-root .gls,.game-root .ev-bub{font-family:'Kalam','Mali',sans-serif!important;font-weight:700!important}\n"
       ".game-root .cap,.game-root p{line-height:1.3!important}\n"
       ".game-root .ctag,.game-root .loc-cap>span:first-child,.game-root .hud-meter span,.game-root .hud-chip span,.game-root .hud-tab span:last-child,.game-root .mg-chip,.game-root .dz-hint,.game-root .mc-zone b,.game-root .dz-target::after,.game-root .ti-pl,.game-root .ti-best,.game-root .ti-hi,.game-root .pop-jag span,.game-root .gb span:last-child>span,.game-root .lbl-c{font-family:'Bangers','Mali',sans-serif!important;font-weight:400!important;letter-spacing:.06em!important}\n"
       ".game-root .mg-chip{font-size:17px!important}\n"
       ".game-root .ce.ic{display:inline-block;flex:none;width:30px;height:30px;font-size:0!important;color:transparent!important;background:center/contain no-repeat;filter:drop-shadow(2px 2px 0 rgba(10,8,6,.35))}\n"
       ".game-root .mg-mix .mg-chip .ce.ic{width:36px;height:36px}\n"
       ".game-root .mg-grid .ce.ic{width:46px;height:46px}\n"
       ".game-root .mg-grid .gb:hover .ce.ic{transform:rotate(-8deg) scale(1.1)}\n"
       + "".join(f".game-root .ce.{k}{{background-image:{v}}}\n" for k, v in ICONS.items()))


def patch(s):
    def rep(old, new):
        nonlocal s
        assert old in s, "comic: nenalezeno " + old[:70]
        s = s.replace(old, new, 1)

    rep("family=Mali:wght@500;700&family=Titan+One&display=swap", "family=Mali:wght@500;700&family=Titan+One&family=Bangers&family=Kalam:wght@700&display=swap")
    rep("C=(e,l,on,bad)=>({e,l,", "C=(e,l,on,bad)=>({e,l,ek:IC_EM[e]?'ce ic '+IC_EM[e]:'ce',")
    rep("mgGrid:(g.ord||ING.map((_,i)=>i)).map(i=>({e:ING[i][0],l:ING[i][1],", "mgGrid:(g.ord||ING.map((_,i)=>i)).map(i=>({e:ING[i][0],l:ING[i][1],ek:'ce ic '+ING_IC[i],")
    # recept/výsledek: Gin jako lahev (ne koktejl)
    rep("mgChips:R.map(([e,l],k)=>C(e,(k+1)+'. '+l,1))", "mgChips:g.rec.map((i,k)=>Object.assign(C(ING[i][0],(k+1)+'. '+ING[i][1],1),{ek:'ce ic '+ING_IC[i]}))")
    rep("C(ING[g.inp[k]][0],ING[g.inp[k]][1],1)", "Object.assign(C(ING[g.inp[k]][0],ING[g.inp[k]][1],1),{ek:'ce ic '+ING_IC[g.inp[k]]})")
    rep("mgChips:R.map(([e,l],k)=>C(e,l,g.inp[k]===g.rec[k],k<g.inp.length&&g.inp[k]!==g.rec[k]))",
        "mgChips:g.rec.map((i,k)=>Object.assign(C(ING[i][0],ING[i][1],g.inp[k]===g.rec[k],k<g.inp.length&&g.inp[k]!==g.rec[k]),{ek:'ce ic '+ING_IC[i]}))")
    rep('<span style="font-size:20px;line-height:1">{{ c.e }}</span>', '<span class="{{ c.ek }}" style="font-size:20px;line-height:1">{{ c.e }}</span>')
    rep('<span style="font-size:30px;line-height:1">{{ g.e }}</span>', '<span class="{{ g.ek }}" style="font-size:30px;line-height:1">{{ g.e }}</span>')
    rep("const ING=[", "const IC_EM=" + repr(EMOJI).replace("'", '"') + ",ING_IC=" + repr(ING_IC).replace("'", '"') + ";\nconst ING=[")
    i = s.index("</style>\n</helmet>")
    return s[:i] + CSS + s[i:]
