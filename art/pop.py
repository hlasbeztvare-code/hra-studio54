# Pop-art komiksový skin (podle předlohy „Přežij after“ 4. 10. 2026)
# Vygeneruje SVG dekorace (mráčky, výbuchy, bubliny) a vloží CSS + značky do src/template.html.
import math, random, re, shutil, urllib.parse, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
TPL = ROOT / "src" / "template.html"
INK, Y, Y2, R, O, PAPER = "#0a0806", "#FFD400", "#FFB300", "#E5231B", "#FF7A00", "#FFF7E3"  # klasický komiks


def uri(svg):
    svg = re.sub(r"\s+", " ", svg).strip()
    # runtime hry přepisuje camelCase (viewBox → sc-camel-view-box) i v CSS → velká písmena kódovat, hex malými
    ok = set("abcdefghijklmnopqrstuvwxyz0123456789 =:/,;()'-._")
    return 'url("data:image/svg+xml,' + "".join(c if c in ok else "".join(f"%{b:02x}" for b in c.encode()) for c in svg) + '")'


def burst(cx, cy, rx, ry, n, inner, rnd, rot=0):
    pts = []
    for i in range(n * 2):
        a = rot + math.pi * i / n
        k = 1 if i % 2 == 0 else inner
        k *= 1 + (rnd.random() - .5) * (.22 if i % 2 == 0 else .1)
        pts.append(f"{cx + math.cos(a) * rx * k:.1f},{cy + math.sin(a) * ry * k:.1f}")
    return " ".join(pts)


def boom():  # výbuch za nadpisem
    r = random.Random(54)
    return f"""<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 400 300'>
<defs><pattern id='d' width='9' height='9' patternUnits='userSpaceOnUse'><circle cx='4.5' cy='4.5' r='2.1' fill='{Y}'/></pattern></defs>
<polygon points='{burst(200,150,172,128,17,.62,r,.1)}' fill='{R}' stroke='{INK}' stroke-width='5' stroke-linejoin='round'/>
<polygon points='{burst(200,150,172,128,17,.62,random.Random(54),.1)}' fill='url(#d)' opacity='.55'/>
<polygon points='{burst(200,150,150,108,15,.68,r,.3)}' fill='{O}'/>
<polygon points='{burst(200,150,104,72,13,.72,r,.5)}' fill='#FFF27A'/>
</svg>"""


def startburst():  # paprsky za tlačítkem START
    r = random.Random(7)
    return f"""<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 400 200' preserveAspectRatio='none'>
<polygon points='{burst(200,100,180,86,22,.66,r)}' fill='{Y}' stroke='{INK}' stroke-width='4' stroke-linejoin='round'/>
<polygon points='{burst(200,100,150,70,22,.72,r,.07)}' fill='{R}'/>
</svg>"""


def cloud(seed):  # bílý obláček s rastrem
    r = random.Random(seed)
    cs = []
    for i in range(7):
        a = math.pi * 2 * i / 7 + r.random() * .4
        cs.append((120 + math.cos(a) * 50 * (0.8 + r.random() * .3), 90 + math.sin(a) * 30 * (0.8 + r.random() * .3), 28 + r.random() * 12))
    cs.append((120, 90, 46))
    circ = "".join(f"<circle cx='{x:.0f}' cy='{y:.0f}' r='{rr:.0f}'/>" for x, y, rr in cs)
    return f"""<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 240 180'>
<defs><pattern id='h' width='7' height='7' patternUnits='userSpaceOnUse'><circle cx='3.5' cy='3.5' r='1.7' fill='#9c958a'/></pattern>
<clipPath id='c'>{circ}</clipPath><linearGradient id='g' x1='0' y1='0' x2='.4' y2='1'><stop offset='.45' stop-color='#fff' stop-opacity='0'/><stop offset='1' stop-color='#fff'/></linearGradient>
<mask id='m'><rect width='240' height='180' fill='url(#g)'/></mask></defs>
<g fill='{INK}' stroke='{INK}' stroke-width='9'>{circ}</g><g fill='#fff'>{circ}</g>
<rect width='240' height='180' fill='url(#h)' clip-path='url(#c)' mask='url(#m)'/>
</svg>"""


def star():
    pts = " ".join(f"{50 + math.cos(-math.pi/2 + math.pi*i/5) * (46 if i % 2 == 0 else 20):.1f},{52 + math.sin(-math.pi/2 + math.pi*i/5) * (46 if i % 2 == 0 else 20):.1f}" for i in range(10))
    return f"<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><polygon points='{pts}' fill='{Y}' stroke='{INK}' stroke-width='5' stroke-linejoin='round'/></svg>"


def jag(pts, fill=PAPER):  # zubatá bublina roztažená na prvek, obrys v px (non-scaling)
    p = " ".join(f"{x},{y}" for x, y in pts)
    return f"<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100' preserveAspectRatio='none'><polygon points='{p}' fill='{fill}' stroke='{INK}' stroke-width='4' stroke-linejoin='round' vector-effect='non-scaling-stroke'/></svg>"


def jagburst(seed, n=13):
    r = random.Random(seed)
    pts = []
    for i in range(n * 2):
        a = math.pi * i / n + .2
        k = (49 if i % 2 == 0 else 41) * (1 + (r.random() - .5) * .08)
        pts.append((round(50 + math.cos(a) * k, 1), round(50 + math.sin(a) * k, 1)))
    return pts


CAP = [(5,9),(28,4),(52,8),(76,3),(95,7),(95,30),(100,40),(95,47),(97,78),(93,95),(66,92),(40,97),(9,94),(5,72),(0,62),(5,54),(3,26)]

CSS = f"""
/* ══ POP-ART KOMIKS (předloha 4. 10.) ══ */
:root{{--py:{Y};--py2:{Y2};--pr:{R};--po:{O};--pp:{PAPER}}}
/* úvod: paprsky, rastr, výbuch, mráčky */
[data-screen-label="Intro"]{{background:{INK}!important;-webkit-backdrop-filter:none!important;backdrop-filter:none!important}}
.ti-sun{{top:42%!important;background:repeating-conic-gradient(from 2deg,transparent 0 31deg,{R} 31deg 33.5deg),repeating-conic-gradient(from 0deg,{Y} 0 4.5deg,transparent 4.5deg 13deg),repeating-conic-gradient(from 5deg,{Y2} 0 3deg,transparent 3deg 17deg)!important;-webkit-mask:none!important;mask:none!important;animation-duration:140s!important}}
.ti-dots{{background:radial-gradient({Y} 1.7px,transparent 2.2px) 0 0/10px 10px!important;opacity:.55}}
.ti-dots::after{{content:"";position:absolute;inset:0;background:radial-gradient({INK} 1.9px,transparent 2.4px) 5px 5px/10px 10px;-webkit-mask:radial-gradient(ellipse at 50% 42%,transparent 30%,#000 75%);mask:radial-gradient(ellipse at 50% 42%,transparent 30%,#000 75%)}}
.ti-dots::before{{content:"";position:absolute;inset:0;background:radial-gradient(ellipse 46% 40% at 50% 46%,rgba(10,8,6,.78),rgba(10,8,6,0) 100%)}}
.pop-cloud,.pop-star{{position:absolute;pointer-events:none;background:center/contain no-repeat;z-index:0}}
.pop-cloud{{width:clamp(96px,22vw,230px);aspect-ratio:4/3}}
.pc1{{background-image:{uri(cloud(1))};left:-3%;top:24%}}
.pc2{{background-image:{uri(cloud(2))};right:-3%;top:36%;transform:scaleX(-1)}}
.pc3{{background-image:{uri(cloud(3))};left:-2%;top:62%}}
.pc4{{background-image:{uri(cloud(4))};right:-2%;top:68%;transform:scaleX(-1)}}
.pop-star{{width:clamp(34px,7vw,70px);aspect-ratio:1;background-image:{uri(star())}}}
.ps1{{left:7%;top:37%;transform:rotate(-12deg)}}.ps2{{right:12%;top:21%;transform:rotate(14deg) scale(.7)}}
@media (min-width:1400px) and (min-height:700px){{.pc2,.pc4,.ps2{{display:none}}}}
/* horní rohy: zubaté bubliny */
.ti-top{{width:100%;display:grid;grid-template-columns:1fr auto 1fr;align-items:start;gap:8px}}
.pop-jag{{position:relative;isolation:isolate;color:{INK};font-family:'Titan One','Mali',sans-serif;text-transform:uppercase;line-height:1.02}}
.pop-jag::before{{content:"";position:absolute;inset:0;z-index:-1;background:center/100% 100% no-repeat;filter:drop-shadow(4px 5px 0 {INK})}}
.pop-jag .r{{color:{R}}}
.ti-tl,.ti-tr{{display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:clamp(18px,3vw,30px) clamp(18px,3.2vw,34px);min-width:clamp(118px,15vw,190px)}}
.ti-tl{{justify-self:start;transform:rotate(-6deg);font-size:clamp(17px,2vw,26px)}}
.ti-tl::before{{background-image:{uri(jag(jagburst(11)))}}}
.ti-tl .r{{font-size:1.08em}}
.ti-tl .ti-hi{{margin-top:5px;font:700 clamp(10px,.95vw,12px)/1.15 'Mali',sans-serif;letter-spacing:.02em;color:#5a4a1a;max-width:150px}}
.ti-tr{{justify-self:end;transform:rotate(5deg);font-size:clamp(11px,1.15vw,14px)}}
.ti-tr::before{{background-image:{uri(jag(jagburst(23,15)))}}}
.ti-tr b{{font-size:1.6em;font-weight:400}}.ti-tr .r{{font-size:2.5em;line-height:.95}}
.ti-tr span{{max-width:150px}}.ti-tr i{{font-style:normal;color:{R}}}
.ti-top .ti-lg{{align-self:center;margin-top:clamp(4px,1.2vh,14px)}}
/* nadpis + výbuch */
.ti-head{{position:relative;isolation:isolate;padding:.2em .5em}}
.ti-head::before{{content:"";position:absolute;inset:-14% -10%;z-index:-1;background:{uri(boom())} center/100% 100% no-repeat;animation:popBoom 3.2s ease-in-out infinite}}
@keyframes popBoom{{0%,100%{{transform:scale(1) rotate(0)}}50%{{transform:scale(1.04) rotate(1.5deg)}}}}
.ti-logo{{color:#fff!important;-webkit-text-stroke:.11em {INK}!important;paint-order:stroke fill;text-shadow:.03em .035em 0 {R},.06em .07em 0 {R},.085em .1em 0 {INK},.1em .12em 0 {INK}!important;letter-spacing:.02em}}
.ti-neon{{color:{Y}!important;-webkit-text-stroke-color:{INK}!important}}
/* popis = zubatá krémová bublina */
[data-screen-label="Intro"] .cap{{position:relative;isolation:isolate;background:transparent!important;border:0!important;box-shadow:none!important;padding:clamp(16px,2.4vh,24px) clamp(22px,4vw,40px)!important;color:{INK}!important;transform:rotate(-2deg)!important}}
[data-screen-label="Intro"] .cap::before{{content:"";position:absolute;inset:0;z-index:-1;background:{uri(jag(CAP))} center/100% 100% no-repeat;filter:drop-shadow(5px 6px 0 {INK})}}
.cap .r{{display:block;margin-top:2px;color:{R};font-family:'Titan One','Mali',sans-serif;font-weight:400;text-transform:uppercase;letter-spacing:.01em}}
/* jméno + start */
.ti-pl{{align-self:center;padding:5px 18px 4px;border:3px solid {INK};border-radius:999px;background:radial-gradient(rgba(10,8,6,.18) 1.2px,transparent 1.7px) 0 0/6px 6px,{Y};color:{INK}!important;font-family:'Titan One','Mali',sans-serif!important;font-weight:400!important;font-size:15px!important;box-shadow:3px 3px 0 {INK};transform:rotate(-1deg)}}
.ti-in{{border-radius:999px!important;border:4px solid {INK}!important;background:{PAPER}!important;color:{INK}!important;font-family:'Titan One','Mali',sans-serif!important;font-weight:400!important;text-transform:uppercase;box-shadow:5px 5px 0 {INK}!important}}
.ti-in::placeholder{{color:#8d8577!important;text-transform:none;font-family:'Mali',sans-serif}}
.ti-in:focus{{box-shadow:5px 5px 0 {R}!important}}
.ti-startw{{position:relative;isolation:isolate;display:flex;justify-content:center;padding:clamp(10px,2vh,22px) clamp(24px,5vw,56px)}}
.ti-startw::before{{content:"";position:absolute;inset:0 -6%;z-index:-1;background:{uri(startburst())} center/100% 100% no-repeat;animation:popBoom 2.4s ease-in-out infinite}}
.ti-start{{background:linear-gradient(180deg,#FFF07A 0%,{Y} 42%,{Y2} 100%)!important;border:4px solid {INK}!important;box-shadow:inset 0 3px 0 rgba(255,255,255,.65),inset 0 -5px 0 rgba(170,90,0,.35),6px 7px 0 {INK}!important;color:{INK}!important;text-shadow:2px 2px 0 rgba(255,255,255,.7)}}
.ti-start>span:first-child{{color:{R};-webkit-text-stroke:3px {INK};paint-order:stroke fill;text-shadow:none;font-size:.75em!important}}
.ti-blink{{color:#fff!important;text-shadow:2px 2px 0 {INK},-1px -1px 0 {INK}}}
[data-screen-label="Intro"] .gb{{background:{INK}!important;color:#fff!important;border:3px solid {INK}!important;box-shadow:inset 0 0 0 3px {Y},4px 4px 0 {INK}!important}}
[data-screen-label="Intro"] .gb:hover{{background:{Y}!important;color:{INK}!important;box-shadow:inset 0 0 0 3px {INK},6px 6px 0 {INK}!important}}
.ti-best{{color:#fff!important;text-shadow:2px 2px 0 {INK},-1px -1px 0 {INK},1px -1px 0 {INK},-1px 1px 0 {INK}}}
.ti-poster{{box-shadow:9px 9px 0 {R},9px 9px 0 4px {INK}!important}}
.ti-poster>span{{background:{Y}!important}}
@media (max-width:640px){{
 .ti-top{{grid-template-columns:1fr 1fr;grid-template-areas:"l r" "logo logo";row-gap:0}}
 .ti-tl{{grid-area:l}}.ti-tr{{grid-area:r}}.ti-top .ti-lg{{grid-area:logo;justify-self:center;margin-top:-22px;position:relative;z-index:1}}
 .ti-tl{{font-size:17px;padding:20px 16px;min-width:0}}.ti-tr{{font-size:10.5px;padding:18px 14px;min-width:0}}
 .pop-cloud{{width:clamp(90px,30vw,140px)}}
}}
@media (max-height:760px){{.ti-tl,.ti-tr{{padding:14px 16px}}.ti-tr .r{{font-size:2em}}.ti-startw{{padding:8px 24px}}}}
@media (max-height:480px){{.ti-top{{display:none}}}}
@media (prefers-reduced-motion:reduce){{.ti-head::before,.ti-startw::before{{animation:none}}}}

/* ve hře: žluté rastrové lišty, černé panely, pop titulky */
.page-frame{{border:6px solid {INK}!important;box-shadow:inset 0 0 0 4px {Y},inset 0 0 0 7px {INK}!important}}
.aur{{opacity:.75!important;mix-blend-mode:normal!important;animation:none!important;inset:0!important;background:radial-gradient({INK} 1.5px,transparent 2px) 0 0/8px 8px!important;-webkit-mask:radial-gradient(ellipse at 50% 50%,transparent 58%,#000 100%);mask:radial-gradient(ellipse at 50% 50%,transparent 58%,#000 100%)}}
.hud-top,.hud-bot{{background:radial-gradient(rgba(10,8,6,.2) 1.3px,transparent 1.8px) 0 0/8px 8px,linear-gradient(180deg,#FFE04A,{Y} 55%,{Y2})!important;border:3px solid {INK}!important;box-shadow:6px 6px 0 {R},6px 6px 0 3px {INK}!important}}
.hud-left{{color:{INK}!important}}
.hud-clock{{background:{INK}!important;color:{Y}!important;border-color:{INK}!important;box-shadow:3px 3px 0 {R}!important}}
.hud-id .logo54{{background:{INK};padding:3px 8px;border-radius:10px;box-shadow:2px 2px 0 {R};filter:none}}
.hud-chip{{background:{PAPER}!important}}
.hud-stats>.hud-chip:last-child{{background:{R}!important}}
.hud-stats>.hud-chip:last-child>span{{color:#fff!important}}
.hud-stats>.hud-chip:last-child::after{{background:{R}!important}}
.gl,.gls{{background:radial-gradient(rgba(255,212,0,.13) 1.3px,transparent 1.8px) 0 0/8px 8px,linear-gradient(180deg,#16110a,#0a0806)!important;box-shadow:0 0 0 3px {Y},9px 9px 0 3px {INK}!important}}
.gls{{box-shadow:0 0 0 3px {Y},10px 10px 0 3px {R},10px 10px 0 6px {INK}!important}}
.panel-loc{{box-shadow:0 0 0 3px var(--acc),9px 9px 0 3px {INK}!important}}
.cx{{color:#fff!important;-webkit-text-stroke:6px {INK}!important;paint-order:stroke fill;text-shadow:3px 3px 0 {R},6px 6px 0 {INK}!important}}
.panel-loc .cx{{-webkit-text-stroke-color:{INK}!important;text-shadow:3px 3px 0 var(--acc),6px 6px 0 {INK}!important}}
.cx-y{{color:{Y}!important}}
.ev-bub .cx{{color:#fff!important;-webkit-text-stroke:6px {INK}!important;text-shadow:3px 3px 0 {R},5px 5px 0 {INK}!important}}
.ctag{{background:{R}!important;color:#fff!important;border:3px solid {INK}!important;font-family:'Titan One','Mali',sans-serif!important;font-weight:400!important;box-shadow:3px 3px 0 {INK}!important}}
.loc-cap{{background:radial-gradient(rgba(10,8,6,.12) 1.2px,transparent 1.7px) 0 0/6px 6px,{Y}!important}}
.panel-dj>div:first-child>span:first-child{{background:{Y}!important}}
.gp{{background:linear-gradient(180deg,#FFF07A 0%,{Y} 45%,{Y2} 100%)!important;border:3px solid {INK}!important;box-shadow:inset 0 2px 0 rgba(255,255,255,.6),5px 5px 0 {INK}!important}}
.gp:hover{{background:linear-gradient(180deg,#FFF6A8 0%,#FFE03A 45%,{Y} 100%)!important}}
.gls.bubble{{background:{PAPER}!important;box-shadow:0 0 0 3px {INK},9px 9px 0 3px {R},9px 9px 0 6px {INK}!important}}
.bubble::after,.ev-bub::after{{border-top-color:{PAPER}}}
.ev-bub::after{{border-color:{PAPER} transparent transparent transparent!important}}
.hud-toast{{background:{PAPER}!important;box-shadow:5px 5px 0 {R},5px 5px 0 3px {INK}!important}}
/* překryvy (událost, minihra, nápověda, konec) = dramatické paprsky */
div:has(> .ev-bub),div:has(> .gls:not(.bubble)),[data-screen-label="Konec"]{{background:radial-gradient(closest-side,rgba(10,8,6,.55),rgba(10,8,6,.9)),repeating-conic-gradient(from 0deg at 50% 50%,{Y} 0 4deg,transparent 4deg 12deg),{INK}!important}}
[data-screen-label="Konec"] h1.cx{{-webkit-text-stroke-width:.09em!important;text-shadow:.04em .05em 0 {R},.07em .09em 0 {INK}!important}}
[data-screen-label="Pepa"]>div:first-child{{background:radial-gradient(circle at 50% 30%,rgba(0,0,0,.1) 0,rgba(0,0,0,.85) 70%),radial-gradient(rgba(255,212,0,.16) 1.4px,transparent 2px) 0 0/9px 9px!important}}

/* doladění */
.ti-head::before{{inset:-34% -22%}}
.ti-head{{padding:.1em .4em}}
.ti-startw{{padding:clamp(8px,1.6vh,16px) clamp(30px,6vw,64px)}}
.ti-startw::before{{inset:-34% -4%}}
.ti-blink{{display:none!important}}
.ti-tr{{padding:clamp(22px,3.2vw,34px) clamp(24px,3.4vw,40px);min-width:clamp(150px,17vw,220px)}}
@media (max-width:640px){{.ti-tr{{padding:24px 18px;min-width:168px;font-size:10px}}.ti-tl{{padding:22px 18px}}}}
div:has(> .ev-bub),div:has(> .gls:not(.bubble)),[data-screen-label="Konec"]{{background:radial-gradient(closest-side,rgba(10,8,6,.05),rgba(10,8,6,.3)),radial-gradient(rgba(10,8,6,.45) 1.6px,transparent 2.1px) 0 0/9px 9px,repeating-conic-gradient(from 2deg at 50% 50%,transparent 0 31deg,{R} 31deg 33.5deg),repeating-conic-gradient(from 0deg at 50% 50%,{Y} 0 4.5deg,{INK} 4.5deg 13deg)!important}}
[data-screen-label="Pepa"]{{background:repeating-conic-gradient(from 2deg at 50% 32%,transparent 0 31deg,{R} 31deg 33.5deg),repeating-conic-gradient(from 0deg at 50% 32%,{Y} 0 4.5deg,{INK} 4.5deg 13deg)!important}}
[data-screen-label="Pepa"]>div:first-child{{background:radial-gradient(ellipse 40% 34% at 50% 32%,rgba(10,8,6,.05),rgba(10,8,6,.35) 100%),radial-gradient(rgba(10,8,6,.45) 1.6px,transparent 2.1px) 0 0/9px 9px!important}}
@media (min-width:700px){{.ti-logo{{font-size:clamp(46px,calc(min(11vw,9.6vh) / var(--z)),150px)!important}}.ti-startw{{padding-top:6px;padding-bottom:6px}}.ti-start{{padding-top:clamp(12px,1.8vh,20px)!important;padding-bottom:clamp(12px,1.8vh,20px)!important}}}}
@media (max-width:899px){{.hud-line .hud-mark.now{{color:{INK}!important;text-shadow:none!important}}}}

/* klasické komiksové barvy všude (přání 4. 10.): žlutá · červená · modrá · černá · bílá */
.loc-parket{{--acc:{R}}}.loc-dj{{--acc:#1E88E5}}.loc-bar{{--acc:{O}}}.loc-vip{{--acc:#8E3FD9}}.loc-wc{{--acc:#12B76A}}
.tab-parket{{--tc:{R}}}.tab-dj{{--tc:#1E88E5}}.tab-bar{{--tc:{O}}}.tab-vip{{--tc:#8E3FD9}}.tab-wc{{--tc:#12B76A}}
.hud-stats>.hud-meter:nth-child(1){{--mc:{Y}}}.hud-stats>.hud-meter:nth-child(2){{--mc:{R}}}.hud-stats>.hud-meter:nth-child(3){{--mc:#1E88E5}}
.hud-stats>.hud-meter:nth-child(1) .hud-bar>div{{background-color:{Y}!important}}
.hud-stats>.hud-meter:nth-child(2) .hud-bar>div{{background-color:{R}!important}}
.hud-stats>.hud-meter:nth-child(3) .hud-bar>div{{background-color:#1E88E5!important}}
.djc-now{{box-shadow:0 0 0 3px {R},6px 6px 0 2px #000}}
.djc-own{{background:radial-gradient(rgba(10,8,6,.12) 1px,transparent 1.5px) 0 0/6px 6px,linear-gradient(160deg,#FFF07A,{Y} 60%,{Y2})}}
.djc-st{{background:{Y}}}.djc-now .djc-st{{background:{R};color:#fff}}
.mg-opts>button[style*="E8B931"]{{--bb:{Y}}}
"""

INTRO_DECO = '<div class="pop-cloud pc1"></div><div class="pop-cloud pc2"></div><div class="pop-cloud pc3"></div><div class="pop-cloud pc4"></div><div class="pop-star ps1"></div><div class="pop-star ps2"></div>'


def patch():
    s = TPL.read_text(encoding="utf-8")
    bak = TPL.with_name("template.pre-pop.html")
    if "POP-ART KOMIKS" in s:
        s = bak.read_text(encoding="utf-8")
    else:
        shutil.copy(TPL, bak)
    rep = []
    from pop_shapes import SHAPES
    s = s.replace("</style>\n</helmet>", CSS + SHAPES + "</style>\n</helmet>", 1)
    old = '<div style="display:flex;flex-direction:column;gap:6px;padding:18px 22px;border-radius:20px;background:var(--yel)'
    assert old in s; s = s.replace(old, old.replace('<div style', '<div class="pop-rank" style'), 1)
    old = '<div class="ti-sun"></div><div class="ti-dots"></div>'
    assert old in s; s = s.replace(old, old + INTRO_DECO, 1)
    # horní řádek → dvě zubaté bubliny + logo uprostřed
    i = s.index('<div style="width:100%;display:flex;justify-content:space-between;align-items:center;gap:10px 20px;flex-wrap:wrap;font-family:\'Mali\'')
    j = s.index("</div>", i) + 6
    s = s[:i] + ('<div class="ti-top">\n'
        '          <div class="pop-jag ti-tl"><span>Studio54</span><span class="r">Praha</span><span class="ti-hi">Hi-score {{ hiScore }} · {{ hiName }}</span></div>\n'
        '          <img data-lsrc="uploads/logo54.webp" alt="Studio 54" class="logo54 ti-lg" style="height:clamp(52px,min(16vw,9.5vh),110px);width:auto">\n'
        '          <div class="pop-jag ti-tr"><b>{{ nDay }}</b><b class="r">{{ nDate }}</b><span>{{ nName }}</span><span>Start <i>{{ nStart }}</i></span><span>Hybernská 38</span></div>\n'
        '        </div>') + s[j:]
    old = '\n          <img data-lsrc="uploads/logo54.webp" alt="Studio 54" class="logo54 ti-lg" style="height:clamp(52px,min(16vw,9.5vh),110px);width:auto">\n          <h1 class="ti-logo">Přežij<br><span class="ti-neon">after.</span></h1>'
    assert old in s
    s = s.replace(old, '\n          <div class="ti-head"><h1 class="ti-logo">Přežij<br><span class="ti-neon">after.</span></h1></div>', 1)
    old = "sežeň podpis od všech DJů. Mamka si myslí, že spíš u kamaráda.</p>"
    assert old in s; s = s.replace(old, 'sežeň podpis od všech DJů. <span class="r">Mamka si myslí, že spíš u kamaráda.</span></p>', 1)
    old = '<span style="font-family:\'Mali\',\'Mali\',\'Archivo\',sans-serif;font-weight:700;font-size:13px;font-weight:700;letter-spacing:.06em;text-transform:uppercase;color:var(--yel)">Hráč 1'
    assert old in s; s = s.replace(old, old.replace("<span style", '<span class="ti-pl" style'), 1)
    m = re.search(r'\n\s*<button class="gp ti-start".*?</button>', s)
    s = s[:m.start()] + '\n          <div class="ti-startw">' + m.group(0).strip() + '</div>' + s[m.end():]
    old = '<span style="padding:12px 4px;font-family:\'Mali\',\'Mali\',\'Archivo\',sans-serif;font-weight:700;font-size:14px;font-weight:700;color:#D6D1C9">{{ bestTxt }}</span>'
    assert old in s; s = s.replace(old, old.replace("<span style", '<span class="ti-best" style'), 1)
    old = "nightTxt:NIGHT.t+' · start '+hm(OPEN)+' · Hybernská 38',"
    assert old in s
    s = s.replace(old, old + " ...(()=>{const m=/^(\\S+)\\s+(\\d+\\.\\d+\\.)\\s*(.*?)\\s*·\\s*(.*)$/.exec(NIGHT.t)||[];return {nDay:m[1]||'Dnes',nDate:m[2]||'',nName:(m[4]||NIGHT.t).replace(/\\s*×.*$/,''),nStart:hm(OPEN)};})(),", 1)
    TPL.write_text(s, encoding="utf-8")
    print("hotovo, CSS", len(CSS), "B")


if __name__ == "__main__":
    patch()
