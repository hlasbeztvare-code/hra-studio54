# Sjednocení typografie a barev + oprava přetékajících / překrývajících se textů.
# Písma podle předlohy „SUPER KOMIKS“: Luckiest Guy (nadpisy, tlačítka, čísla) + Baloo 2 (texty, popisky).
# Obě mají latin-ext (háčky, čárky). Volá se z klub.patch() jako úplně poslední.
import re

FONT_OLD = "family=Mali:wght@500;700&family=Titan+One&family=Bangers&family=Kalam:wght@700&display=swap"
FONT_NEW = "family=Luckiest+Guy&family=Baloo+2:wght@600;700;800&display=swap"

H = "'Luckiest Guy'"
B = "'Baloo 2'"
# barvy podle předlohy uživatele (GTA západ slunce): jantar, spálená oranž, krém, tyrkys, inkoust
INK, GOLD, GOLD_D, GOLD_L, WHITE = "#121010", "#E2B04E", "#A97A2B", "#F6DA92", "#F4ECD8"
TEAL, TEAL_D = "#A97A2B", "#121010"  # předloha 4. 10.: žádná tyrkysová v UI
R, Y, PAPER = GOLD_D, GOLD, WHITE

# staré UI barvy → nová paleta (ikony ingrediencí a kresby postav se nemění)
REMAP = {
    "FFD400": GOLD, "FFB300": "#C9963D", "FF7A00": GOLD_D, "FFF27A": GOLD_L, "FFF07A": GOLD_L,
    "E5231B": GOLD_D, "FF5A3C": GOLD_D, "FF6A4C": GOLD_D, "FF9F1C": "#C9963D",
    "F5C542": GOLD, "E8B931": GOLD, "FFD45A": GOLD, "FFD23F": GOLD, "F5D06B": GOLD, "D9A520": GOLD_D, "C9971C": GOLD_D,
    "FFE08A": GOLD_L, "FFE9A8": GOLD_L, "FFF1C4": GOLD_L, "FFF3D0": WHITE, "FFF6DC": WHITE,
    "FFF7E3": WHITE, "FFF8E6": WHITE, "FFF8E7": WHITE, "F2F0EB": WHITE,
    "1E88E5": WHITE, "35D0FF": WHITE, "B98BFF": "#C9963D", "8E3FD9": GOLD_D, "3EE6B0": GOLD_L, "12B76A": GOLD,
    "FF4FA3": GOLD,
    "E3B448": GOLD, "B8862B": GOLD_D, "F4DD95": GOLD_L, "FFFDF7": WHITE, "D29E3A": "#C9963D", "0A0806": INK,
}
RGBA = {"229,35,27": "169,122,43", "255,212,0": "226,176,78", "232,185,49": "226,176,78",
        "43,168,224": "244,236,216", "255,90,60": "169,122,43", "255,224,138": "246,218,146", "255,243,208": "244,236,216"}
# chráněné úseky: kreslené ikony (ovoce, chilli…) si nechají přirozené barvy
PROTECT = re.compile(r"\.ce\.ic-[a-z]+\{[^}]*\}|const CREW_IMG=\{.*?\};", re.S)


def _hexre(h):
    enc = "".join(f"(?:{c}|{c.lower()}|%{ord(c):02x})" if c.isalpha() else c for c in h)
    return re.compile(r"(#|%23)" + enc + r"(?![0-9a-zA-Z])")


def _enc(h, pre):  # zachovat kódování data-URI (velká písmena → %xx)
    if pre == "#":
        return h
    return "%23" + "".join(f"%{ord(c):02x}" if c.isupper() else c for c in h[1:])


def recolor(s):
    pats = [(_hexre(k), v) for k, v in REMAP.items()]
    out, last = [], 0
    for m in list(PROTECT.finditer(s)) + [None]:
        seg = s[last:m.start() if m else len(s)]
        for rx, v in pats:
            seg = rx.sub(lambda x: _enc(v, x.group(1)), seg)
        for a, b in RGBA.items():
            seg = re.sub(r"rgba?\(\s*" + a.replace(",", r"\s*,\s*"), lambda x: x.group(0).split("(")[0] + "(" + b, seg)
        out.append(seg)
        if m:
            out.append(m.group(0)); last = m.end()
    return "".join(out)

# 3D komiksový nadpis: černý obrys + bílý a černý stín (jako „SUPER“)
SUPER = (f"-webkit-text-stroke:.085em {INK}!important;paint-order:stroke fill!important;"
         f"text-shadow:.045em .055em 0 #fff,.085em .1em 0 {INK}!important")

CSS = f"""
/* ══ SJEDNOCENÍ: písma, barvy, žádné přetékání ══ */
.game-root{{font-family:{B},sans-serif;font-synthesis:none;-webkit-font-smoothing:antialiased;text-rendering:optimizeLegibility}}
.game-root [style*="Luckiest"],.game-root .cx,.game-root .ti-logo{{font-weight:400!important;font-synthesis:none}}
.game-root [style*="Luckiest"],.game-root .djc-n,.game-root .hud-mark,.game-root .ti-in{{text-transform:uppercase}}
.game-root .pop-jag.ti-tl .ti-hi,.game-root .ti-tl .ti-hi{{white-space:normal!important;display:block!important;max-width:94px!important;margin:2px auto 0!important;font-size:10px!important;line-height:1.1!important;text-align:center!important}}
.game-root [style*="Baloo"]{{font-weight:700}}
/* nadpisy */
.game-root .cx{{font-family:{H},sans-serif!important;color:{GOLD}!important;{SUPER};line-height:1.14!important;letter-spacing:.02em!important;padding-top:.1em}}
.game-root .ti-logo{{font-family:{H},sans-serif!important;color:{WHITE}!important;{SUPER};line-height:1!important}}
.game-root .ti-neon{{color:{Y}!important;-webkit-text-stroke-color:{INK}!important}}
/* běžný text: Baloo 2, čitelně */
.game-root .cap,.game-root p,.game-root .hud-toast,.game-root .chat>.gb,.game-root .opts>.gb,.game-root .mg-opts>button,.game-root .gls,.game-root .ev-bub{{font-family:{B},sans-serif!important;font-weight:700!important;line-height:1.32!important}}
/* malé popisky (dřív Bangers): Baloo 2 ExtraBold verzálky */
.game-root .ctag,.game-root .loc-cap>span:first-child,.game-root .hud-meter span,.game-root .hud-chip span,.game-root .hud-tab span:last-child,.game-root .mg-chip,.game-root .dz-hint,.game-root .mc-zone b,.game-root .dz-target::after,.game-root .ti-pl,.game-root .ti-best,.game-root .ti-hi,.game-root .pop-jag span,.game-root .gb span:last-child>span,.game-root .lbl-c{{font-family:{B},sans-serif!important;font-weight:800!important;letter-spacing:.03em!important;line-height:1.15!important}}
/* žádné šedé texty – jen inkoust, červená, žlutá, bílá */
.game-root [style*="#5a5a6a"],.game-root [style*="#4a4a58"],.game-root [style*="#5a4a1a"]{{color:{INK}!important;opacity:1!important}}
.game-root .ti-hi{{color:{R}!important}}
/* štítky a tlačítka v paletě */
.game-root .ctag{{color:{INK}!important;background:{TEAL}!important}}
.game-root .gb,.game-root .gb *{{font-weight:800!important}}
.game-root .mc-perf{{background:rgba(246,239,220,.85)!important}}
.game-root .ti-in::placeholder{{font-family:{B},sans-serif!important;font-weight:700!important;color:#8a8170!important}}
/* plakátky na intru: řádky se nesmí překrývat */
.game-root .ti-poster,.game-root .ti-poster *,.game-root .pop-jag,.game-root .pop-jag *{{line-height:1.12!important}}
.game-root .pop-jag .ti-hi{{white-space:normal!important;max-width:150px;text-align:center}}
/* úkol dole: zalomit na 2 řádky místo „…“ */
.game-root .hud-quest .gl>span{{white-space:normal!important;overflow:visible!important;text-overflow:clip!important;line-height:1.15!important;font-size:12px!important;display:block}}
.game-root .hud-quest .gl{{height:auto!important;min-height:44px}}
/* tanec: nápověda se zalamuje a nevyjede z rámečku */
.game-root .dz-hint{{white-space:normal!important;text-align:center!important;max-width:100%!important;box-sizing:border-box;line-height:1.2!important}}
.game-root .dz{{max-width:calc(100vw - 24px)}}
/* menu tabů: název DJe se nesmí useknout */
.game-root .hud-tab span:last-child{{white-space:normal!important;overflow:visible!important;text-overflow:clip!important;line-height:1.05!important}}
/* ČERNÉ POZADÍ: intro, lišty, překryvy – zlatá jen na akcentech */
.game-root [data-screen-label="Intro"]{{background:{INK}!important}}
.game-root .ti-sun{{background:repeating-conic-gradient(from 0deg,rgba(242,169,59,.10) 0 4.5deg,transparent 4.5deg 13deg)!important;opacity:1!important}}
.game-root .ti-dots{{background:radial-gradient(rgba(242,169,59,.16) 1.6px,transparent 2.1px) 0 0/10px 10px!important;opacity:1!important}}
.game-root .ti-dots::after{{display:none}}
.game-root .hud-top,.game-root .hud-bot{{background:radial-gradient(rgba(242,169,59,.10) 1.3px,transparent 1.8px) 0 0/8px 8px,{INK}!important;border:3px solid {GOLD}!important;box-shadow:5px 5px 0 {GOLD_D}!important}}
.game-root div:has(> .ev-bub),.game-root div:has(> .gls:not(.bubble)),.game-root [data-screen-label="Konec"]{{background:radial-gradient(closest-side,rgba(18,16,16,.7),rgba(18,16,16,.96)),repeating-conic-gradient(from 0deg at 50% 50%,rgba(242,169,59,.35) 0 4deg,transparent 4deg 12deg),{INK}!important}}
/* tyrkysová „obloha“ jako druhý akcent */
.game-root .hud-top,.game-root .hud-bot{{box-shadow:5px 5px 0 {TEAL_D}!important}}
.game-root .tab-parket{{--tc:{GOLD}}}.game-root .tab-dj{{--tc:{TEAL}}}.game-root .tab-bar{{--tc:{GOLD_D}}}.game-root .tab-vip{{--tc:{GOLD_L}}}.game-root .tab-wc{{--tc:{TEAL}}}
.game-root .ti-pl{{background:{TEAL}!important;color:{WHITE}!important}}
.game-root [data-screen-label="Intro"] .gb{{box-shadow:inset 0 0 0 3px {TEAL},4px 4px 0 {TEAL_D}!important}}
.game-root .hud-meter{{box-shadow:3px 3px 0 {TEAL_D}!important}}
.game-root .gl,.game-root .gls:not(.bubble){{box-shadow:0 0 0 3px {GOLD},9px 9px 0 3px {TEAL_D}!important}}
.game-root .hud-mark.now{{color:{GOLD}!important;background:{INK}!important;border-color:{GOLD}!important}}
@media (max-width:899px){{
 /* hláška na mobilu: zabere místo horní lišty (ta se na chvíli schová), hru nezakrývá */
 .game-root .hud-toast{{top:10px!important;bottom:auto!important;left:10px!important;right:10px!important;min-height:64px;box-sizing:border-box;padding:10px 38px!important;background-image:none!important;background:{PAPER}!important;border:3px solid {INK}!important;border-radius:14px!important;filter:none!important;box-shadow:4px 4px 0 {R}!important;font-size:14px!important;line-height:1.25!important;display:flex;align-items:center;justify-content:center;text-align:center;animation-name:popM!important}}
 .game-root:has(.hud-toast) .hud-top{{visibility:hidden}}
 /* štítky čipů na mobilu jen jako ikonka, ať se nepřekrývají s částkou */
 .game-root .hud-chip-k{{font-size:0!important;letter-spacing:0!important}}
 .game-root .hud-chip-k::before{{font-size:14px!important}}
 .game-root .hud-chip>span:last-child{{white-space:nowrap!important}}
 /* papírové panely: menší okraje, víc místa na text */
 .game-root .panel-loc,.game-root .panel-dj{{padding:34px 26px 30px!important}}
 .game-root .hud-tab span:first-child{{font-size:14px!important;white-space:nowrap!important;letter-spacing:0!important}}
}}
@media (max-width:380px){{
 .game-root .panel-loc,.game-root .panel-dj{{padding:30px 20px 26px!important}}
 .game-root .hud-tab span:first-child{{font-size:12.5px!important}}
 .game-root .hud-tabs{{gap:5px!important}}
 .game-root .hud-tab{{padding-left:2px!important;padding-right:2px!important}}
}}
/* nízké telefony: kompaktní lišty, ať zbyde místo na hru */
@media (max-width:899px) and (max-height:740px){{
 .game-root .logo54{{height:26px!important}}
 .game-root .hud-clock{{font-size:19px!important}}
 .game-root .hud-meter{{padding:3px 7px 4px!important}}
 .game-root .hud-chip{{padding:2px 6px!important}}
 .game-root .hud-chip span:last-child{{font-size:15px!important}}
 .game-root .hud-quest>*{{min-height:36px!important;padding-top:3px!important;padding-bottom:3px!important}}
 .game-root .hud-quest img{{height:26px!important;width:23px!important}}
 .game-root .hud-tab{{min-height:0!important;padding-top:5px!important;padding-bottom:4px!important}}
 .game-root .hud-bot{{gap:5px!important;padding-top:6px!important;padding-bottom:6px!important}}
}}
/* telefon na ležato: hra je dělaná na výšku */
@media (orientation:landscape) and (max-height:500px) and (pointer:coarse){{
 .game-root::after{{content:"Otoč telefon na výšku ↻";position:fixed;inset:0;z-index:99999;display:flex;align-items:center;justify-content:center;padding:24px;text-align:center;background:{INK};color:{GOLD};font:28px/1.2 {H},sans-serif;letter-spacing:.03em}}
}}
}}
"""


def patch(s):
    assert FONT_OLD in s, "font link"
    s = s.replace(FONT_OLD, FONT_NEW)
    # inline font-family: nadpisová písma → Luckiest Guy, ostatní → Baloo 2
    # zabudované @font-face starých písem nechat být (jinak se pod jménem Baloo 2 načte JetBrains Mono)
    parts = re.split(r"(@font-face\s*\{[^}]*\})", s)
    for k in range(0, len(parts), 2):
        t = re.sub(r"(['\"])Titan One\1", H, parts[k])
        for f in ("Bangers", "Kalam", "Mali", "Archivo", "JetBrains Mono"):
            t = re.sub(rf"(['\"]){f}\1", B, t)
        parts[k] = t.replace(f"{B},{B},{B}", B).replace(f"{B},{B}", B)
    s = "".join(parts)
    # během tance panely úplně schovat (ne průsvitné přes tanečníka)
    old = "panelsOp:s.dancing?0.15:1"
    assert old in s
    s = s.replace(old, "panelsOp:s.dancing?0:1")
    old = "žluté zóně, červenej střed = pe"
    assert old in s
    s = s.replace("ve žluté zóně, červenej střed = perfekt", "ve zlaté zóně, bílej střed = perfekt")
    s = recolor(s)
    i = s.rindex("</style>")
    return s[:i] + CSS + s[i:]
