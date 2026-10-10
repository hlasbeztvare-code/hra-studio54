# Design podle předlohy uživatele (2026-10-04, styl „San Andreas“ – inspirace, ne kopie GTA):
# ilustrované scény z předlohy, logo z předlohy, písma Passion One (doplněné o č ď ě ň ť ů) + Anton
# + Barlow Semi Condensed, paleta zlatá / krémová / inkoust. Volá se z klub.patch() úplně poslední.
import json, pathlib, re, uuid
from pop import uri

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC, ART = ROOT / "src", ROOT / "art"

INK, GOLD, GOLD_D, GOLD_L, CREAM = "#121010", "#E2B04E", "#A97A2B", "#F6DA92", "#F4ECD8"
PH, PL, PB = "'Passion CZ'", "'Anton'", "'Barlow Semi Condensed'"

FONT_OLD = "family=Luckiest+Guy&family=Baloo+2:wght@600;700;800&display=swap"
FONT_NEW = "family=Anton&family=Barlow+Semi+Condensed:wght@500;600;700;800&display=swap"


def assets():
    idx = json.loads((SRC / "assets.json").read_text(encoding="utf-8"))
    ext = json.loads((SRC / "ext_resources.json").read_text(encoding="utf-8"))
    ids = {e["id"]: e["uuid"] for e in ext}
    out = {}
    for rid, f, ext_, mime in (("saIntro", ART / "sa_intro.webp", "webp", "image/webp"),
                               ("saPepaFig", ART / "sa_pepa_fig.webp", "webp", "image/webp"),
                               ("passion400", ART / "fonts/passion-cz-400.woff2", "woff2", "font/woff2"),
                               ("passion700", ART / "fonts/passion-cz-700.woff2", "woff2", "font/woff2"),
                               ("passion900", ART / "fonts/passion-cz-900.woff2", "woff2", "font/woff2")):
        u = ids.get(rid) or str(uuid.uuid5(uuid.NAMESPACE_URL, "studio54/" + rid))
        (SRC / "assets" / f"{u}.{ext_}").write_bytes(f.read_bytes())
        idx[u] = {"file": f"{u}.{ext_}", "mime": mime}
        if rid not in ids:
            ext.append({"id": rid, "uuid": u}); ids[rid] = u
        out[rid] = u
    (SRC / "assets.json").write_text(json.dumps(idx), encoding="utf-8")
    (SRC / "ext_resources.json").write_text(json.dumps(ext), encoding="utf-8")
    return out


CUP = uri(f"<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 40 40'><path d='M11 5h18v9a9 9 0 0 1-18 0z' fill='{GOLD}' stroke='{INK}' stroke-width='2.5'/>"
          f"<path d='M11 8H5v3a6 6 0 0 0 7 6M29 8h6v3a6 6 0 0 1-7 6' fill='none' stroke='{GOLD}' stroke-width='3'/>"
          f"<path d='M17 22h6l1 8h-8z' fill='{GOLD_D}'/><rect x='11' y='30' width='18' height='6' rx='1.5' fill='{GOLD}' stroke='{INK}' stroke-width='2'/></svg>")

INTRO = """<div class="sa-col sa-icol">
        <div class="sa-top">
          <div class="sa-brand">
            <img data-lsrc="uploads/logo54.webp" alt="Studio 54" class="logo54 sa-logo">
            <div class="sa-city"><b>Studio54</b><b class="g">Praha</b></div>
          </div>
          <div class="sa-date"><b>{{ nDay }}</b><b class="big">{{ nDate }}</b><span>{{ nName }}</span><span>Start <i>{{ nStart }}</i></span><span>Hybernská 38</span></div>
        </div>
        <h1 class="sa-title"><span data-t="Přežij">Přežij</span><span class="g" data-t="after.">after.</span></h1>
        <div class="sa-spacer"></div>
        <div class="sa-bottom">
          <div class="sa-scene sa-scene-i"></div>
          <p class="sa-card">1 500 Kč, plná baterka a jeden cíl: vydrž do 14:00 a sežeň podpis od všech DJů. <span>Mamka si myslí, že spíš u kamaráda.</span></p>
          <span class="sa-label">Hráč 1 · zadej jméno</span>
          <input class="gi ti-in sa-in" value="{{ lbName }}" sc-camel-on-change="{{ lbType }}" sc-camel-on-key-down="{{ startKey }}" maxlength="18" placeholder="Tvoje jméno" autocomplete="nickname" enterkeyhint="go">
          <span class="sa-err">{{ nameErr }}</span>
          <button class="ti-start sa-start" sc-camel-on-click="{{ start }}"><i></i><span>Start!</span></button>
          <div class="sa-btns">
            <button class="sa-btn" sc-camel-on-click="{{ openLb }}"><i class="cup"></i><span>Pořadí</span></button>
            <button class="sa-btn" sc-camel-on-click="{{ toggleHelp }}"><i class="q">?</i><span>Jak hrát</span></button>
          </div>
          <div class="sa-meta"><span>{{ bestTxt }}</span><sc-if value="{{ statsOn }}" hint-placeholder-val="{{ false }}"><span class="ti-stats">{{ statsTxt }}</span></sc-if></div>
        </div>
      </div>
      """

PEPA = """<div data-screen-label="Pepa" class="sa-root sa-proot" style="position:absolute;inset:0;z-index:30">
      <div class="sa-col sa-pcol">
        <img data-lsrc="uploads/logo54.webp" alt="Studio 54" class="logo54 sa-logo sa-plogo">
        <div class="sa-spacer"></div>
        <div class="sa-bottom">
          <div class="sa-pfig" style="transform:{{ pepaTf }}"></div>
          <div class="sa-qcard">
            <div class="sa-qh"><span>Pepa · face control</span><span>{{ gateStep }}</span></div>
            <div class="sa-q">„{{ gateLine }}“</div>
            <div class="opts sa-opts">
              <sc-for list="{{ gateOpts }}" as="o" hint-placeholder-count="3">
                <button class="sa-opt" sc-camel-on-click="{{ o.go }}"><span>{{ o.t }}</span></button>
              </sc-for>
            </div>
          </div>
          <div class="sa-tip">{{ queueTxt }}</div>
        </div>
      </div>
    </div>"""


def css(u):
    sI, sF = f'url("{u["saIntro"]}")', f'url("{u["saPepaFig"]}")'
    ol = lambda w, c=INK: f"-webkit-text-stroke:{w} {c};paint-order:stroke fill"
    return f"""
/* ══ DESIGN PODLE PŘEDLOHY (San Andreas styl) ══ */
@font-face{{font-family:'Passion CZ';font-weight:400;font-display:swap;src:url("{u['passion400']}") format('woff2')}}
@font-face{{font-family:'Passion CZ';font-weight:700;font-display:swap;src:url("{u['passion700']}") format('woff2')}}
@font-face{{font-family:'Passion CZ';font-weight:900;font-display:swap;src:url("{u['passion900']}") format('woff2')}}
.game-root{{font-family:{PB},sans-serif}}
.game-root [style*="Passion"],.game-root .cx,.game-root .ti-logo,.game-root .djc-n,.game-root .hud-mark,.game-root .hud-clock{{font-weight:700!important}}
.game-root .cx{{font-weight:900!important;letter-spacing:.01em!important}}
.game-root .cap,.game-root p,.game-root .hud-toast,.game-root .gls,.game-root .ev-bub{{font-family:{PB},sans-serif!important;font-weight:600!important}}
.game-root .chat>.gb,.game-root .opts>.gb,.game-root .mg-opts>button{{font-family:{PH},sans-serif!important;font-weight:700!important;letter-spacing:.005em}}
.game-root .ctag,.game-root .loc-cap>span:first-child,.game-root .hud-meter span,.game-root .hud-chip span,.game-root .hud-tab span:last-child,.game-root .mg-chip,.game-root .dz-hint,.game-root .lbl-c,.game-root .hud-tab span:first-child{{font-family:{PL},sans-serif!important;font-weight:400!important;letter-spacing:.03em!important}}
.game-root .hud-tab span:first-child{{text-transform:uppercase}}

/* ── společné: sloupec jako telefon, na desktopu rozmazaná scéna po stranách ── */
[data-screen-label="Intro"],[data-screen-label="Pepa"]{{background:{INK}!important;-webkit-backdrop-filter:none!important;backdrop-filter:none!important;overflow:hidden}}
[data-screen-label="Intro"]::before,[data-screen-label="Pepa"]::before{{content:"";position:absolute;inset:-60px;background:{sI} center 70%/cover no-repeat;filter:blur(22px) brightness(.42) saturate(1.1)}}
[data-screen-label="Intro"]>.ti-sun,[data-screen-label="Intro"]>.ti-dots,[data-screen-label="Intro"]>.pop-cloud,[data-screen-label="Intro"]>.pop-star{{display:none!important}}
.sa-col{{position:absolute;top:0;bottom:0;left:0;right:0;margin:0 auto;width:100%;max-width:460px;box-sizing:border-box;display:flex;flex-direction:column;overflow-x:hidden;overflow-y:auto;padding:14px 16px calc(16px + env(safe-area-inset-bottom));background:#16120e;isolation:isolate}}
@media (min-width:600px){{.sa-col{{box-shadow:0 0 0 3px {INK},0 0 60px rgba(0,0,0,.7)}}}}
.sa-spacer{{flex:1 1 auto;min-height:12px}}
.sa-bottom{{position:relative;z-index:1;display:flex;flex-direction:column;gap:10px}}
.sa-scene{{position:absolute;z-index:-1;left:-16px;right:-16px;pointer-events:none;background:center bottom/100% 100% no-repeat}}
.sa-scene-i{{bottom:calc(100% - 190px);aspect-ratio:574/1080;background-image:{sI}}}
[data-screen-label="Pepa"] .sa-col.sa-pcol{{background:linear-gradient(180deg,rgba(14,12,10,.2),rgba(14,12,10,.55) 70%,#16120e),{sI} center 40%/cover no-repeat,#16120e!important}}
[data-screen-label="Pepa"] .sa-pcol::before,[data-screen-label="Pepa"] .sa-pcol::after{{display:none!important}}
.sa-pfig{{position:relative;z-index:0;align-self:center;height:clamp(130px,25vh,230px);aspect-ratio:538/740;margin-bottom:-16px;background:{sF} center bottom/contain no-repeat;filter:drop-shadow(6px 6px 0 rgba(0,0,0,.45));transition:transform .4s cubic-bezier(.3,1.6,.5,1)}}
.sa-col>*:not(.sa-bottom){{position:relative;z-index:2}}
.sa-logo{{display:block;width:100%;height:auto!important;max-width:270px;filter:drop-shadow(0 5px 6px rgba(0,0,0,.45))!important;background:none!important;box-shadow:none!important;padding:0!important}}

/* ── intro ── */
.sa-top{{display:flex;justify-content:space-between;align-items:flex-start;gap:8px}}
.sa-brand{{flex:1 1 auto;min-width:0;display:flex;flex-direction:column;gap:6px}}
.sa-city{{display:flex;flex-direction:column;margin-left:6px;transform:rotate(-3deg);transform-origin:left}}
.sa-city>b{{font:400 clamp(20px,6vw,28px)/.98 {PL};text-transform:uppercase;color:{CREAM};{ol('.16em')};text-shadow:3px 3px 0 {INK};letter-spacing:.01em}}
.sa-city>b.g,.sa-title .g{{color:{GOLD}}}
.sa-date{{flex:0 0 auto;display:flex;flex-direction:column;align-items:flex-end;text-align:right;font-family:{PL};text-transform:uppercase;color:{CREAM};{ol('.2em')};line-height:1.02}}
.sa-date>b{{font-weight:400;font-size:clamp(19px,5.4vw,25px);letter-spacing:.02em}}
.sa-date>b.big{{font-size:clamp(34px,9.6vw,46px);line-height:.95}}
.sa-date>span{{font-size:clamp(11px,3.2vw,14px);letter-spacing:.02em}}
.sa-date i{{font-style:normal;color:{GOLD}}}
.sa-title{{margin:clamp(6px,2vh,22px) 0 0;display:flex;flex-direction:column;align-items:center;font:900 clamp(50px,16vw,84px)/.84 {PH};text-transform:uppercase;letter-spacing:.005em;transform:rotate(-4deg) skewX(-7deg)}}
.sa-title span{{position:relative;display:block;color:transparent;background:linear-gradient(180deg,#fffaf0 0%,{CREAM} 50%,#cfc3a6 52%,#e9dfc6 100%);-webkit-background-clip:text;background-clip:text}}
.sa-title span.g{{margin-left:.9em;background-image:linear-gradient(180deg,{GOLD_L} 0%,{GOLD} 50%,#c8932f 52%,{GOLD} 100%)}}
.sa-title span::before{{content:attr(data-t);position:absolute;inset:0;z-index:-1;color:{INK};-webkit-text-stroke:.1em {INK};text-shadow:.03em .035em 0 {INK},.06em .07em 0 {INK},.085em .1em 0 {INK}}}
.sa-card{{margin:0 4px!important;padding:11px 15px 10px!important;background:{CREAM};color:{INK}!important;text-align:center;font:700 clamp(13px,3.7vw,15px)/1.22 {PB}!important;transform:rotate(-2deg);clip-path:polygon(0 4%,6% 0,14% 3%,23% 0,33% 2%,44% 0,55% 3%,66% 0,77% 2%,88% 0,100% 3%,99% 30%,100% 62%,98% 100%,88% 97%,76% 100%,64% 97%,52% 100%,40% 97%,28% 100%,16% 97%,5% 100%,0 96%,1% 60%,0 30%);filter:drop-shadow(0 5px 0 {INK})}}
.sa-card span{{display:block;margin-top:4px;font:400 clamp(13px,3.8vw,16px)/1.1 {PL};text-transform:uppercase;color:#a8761f;letter-spacing:.02em}}
.sa-label{{position:relative;z-index:0;align-self:center;padding:6px 26px 5px;font:400 clamp(14px,3.9vw,17px)/1 {PL};text-transform:uppercase;letter-spacing:.03em;color:{GOLD}}}
.sa-label::before{{content:"";position:absolute;inset:0;z-index:-1;background:{INK};border:2px solid {GOLD};box-shadow:0 0 0 2px {INK};transform:skewX(-14deg)}}
.game-root .sa-in{{all:unset;box-sizing:border-box;width:100%;height:46px;padding:0 14px;text-align:center;background:{CREAM}!important;color:{INK}!important;border:3px solid {INK}!important;border-radius:14px!important;box-shadow:0 0 0 3px {GOLD},0 0 0 6px {INK},0 6px 0 6px {INK}!important;font:700 20px/1 {PH}!important;text-transform:uppercase;letter-spacing:.02em}}
.game-root .sa-in::placeholder{{font:700 18px/1 {PH}!important;color:#8d826c!important;text-transform:none}}
.sa-err{{min-height:0;text-align:center;font:700 15px/1.2 {PB};color:#ffb36b;text-shadow:1px 1px 0 {INK}}}
.sa-err:empty{{display:none}}
.sa-start{{all:unset;box-sizing:border-box;cursor:pointer;margin-top:8px;height:clamp(56px,8vh,68px);display:flex;align-items:center;justify-content:center;gap:clamp(12px,3.4vw,18px);border-radius:18px;background:linear-gradient(180deg,#f8e2a0 0%,{GOLD} 46%,#c99434 54%,#ddb055 100%);border:4px solid {INK};box-shadow:inset 0 3px 0 rgba(255,255,255,.65),inset 0 -5px 0 rgba(90,55,0,.25),0 0 0 3px {GOLD},0 0 0 6px {INK},0 8px 0 6px {INK};transition:transform .12s}}
.sa-start:active{{transform:translateY(4px)}}
.sa-start i{{position:relative;width:clamp(36px,9.6vw,44px);aspect-ratio:1;border-radius:10px;background:#1b1a18;box-shadow:inset 0 2px 0 rgba(255,255,255,.18)}}
.sa-start i::after{{content:"";position:absolute;left:36%;top:26%;border-style:solid;border-width:.62em 0 .62em 1em;border-color:transparent transparent transparent #fff;font-size:clamp(13px,3.5vw,16px)}}
.sa-start span{{font:900 clamp(34px,10vw,46px)/1 {PH};text-transform:uppercase;color:{INK};letter-spacing:.01em;margin-top:.05em}}
.sa-btns{{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-top:10px}}
.sa-btn{{all:unset;box-sizing:border-box;cursor:pointer;height:clamp(42px,6vh,48px);display:flex;align-items:center;justify-content:center;gap:10px;border-radius:14px;background:#141312;border:3px solid {GOLD};box-shadow:0 0 0 2px {INK},0 5px 0 2px {INK};color:{CREAM};font:400 clamp(15px,4.2vw,18px)/1 {PL};text-transform:uppercase;letter-spacing:.03em}}
.sa-btn i{{display:block;font-style:normal}}
.sa-btn i.cup{{width:24px;height:24px;background:{CUP} center/contain no-repeat}}
.sa-btn i.q{{font:900 24px/1 {PH};color:{GOLD};margin-top:2px}}
.sa-meta{{display:flex;flex-wrap:wrap;justify-content:center;align-items:center;gap:4px 10px;margin-top:4px;font:600 13px/1.2 {PB};color:rgba(244,236,216,.75)}}
.game-root .sa-meta .ti-stats{{all:unset;font:600 13px/1.2 {PB};color:rgba(244,236,216,.75)}}

/* ── Pepa ── */
.sa-pcol .sa-plogo{{align-self:center;max-width:min(56%,250px)}}
.sa-qcard{{position:relative;z-index:1;margin-top:8px;padding:13px 13px 15px;background:{CREAM};border:3px solid {INK};border-radius:8px 10px 6px 9px;box-shadow:0 6px 0 {INK}}}
.sa-qcard::before,.sa-qcard::after{{content:"";position:absolute;left:44%;bottom:100%;border-style:solid;border-width:0 0 30px 22px;border-color:transparent transparent {INK} transparent}}
.sa-qcard::after{{left:calc(44% + 4px);border-width:0 0 24px 15px;border-color:transparent transparent {CREAM} transparent;margin-bottom:-3px}}
.sa-qh{{display:flex;justify-content:space-between;gap:10px;font:400 clamp(11px,3.2vw,14px)/1 {PL};text-transform:uppercase;letter-spacing:.03em;color:#6c614f}}
.sa-q{{margin:9px 0 12px;font:700 clamp(20px,5.8vw,28px)/1 {PH};text-transform:uppercase;color:{INK};text-wrap:balance;letter-spacing:.005em}}
.sa-opts{{display:flex;flex-direction:column;gap:10px;counter-reset:o}}
.game-root .sa-opt{{all:unset;box-sizing:border-box;cursor:pointer;position:relative;display:grid;grid-template-columns:auto minmax(0,1fr) 22px;align-items:center;gap:12px;min-height:52px;padding:6px 12px 6px 8px;background:#fbf6ea;border:3px solid {INK};border-radius:14px;box-shadow:4px 5px 0 #b98a35,4px 5px 0 3px {INK};font:700 clamp(15px,4.3vw,18px)/1.08 {PH};color:{INK};counter-increment:o;transition:transform .1s,background .15s}}
.game-root .sa-opt::before{{content:counter(o,upper-alpha);display:grid;place-items:center;width:36px;height:36px;border-radius:50%;background:radial-gradient(circle at 40% 30%,{GOLD_L},{GOLD} 55%,#b88430);border:3px solid {INK};font:900 20px/1 {PH};color:{INK}}}
.game-root .sa-opt>span{{text-align:left!important;justify-self:start!important;margin:0!important;width:auto!important}}
.game-root .sa-opt::after{{content:"";justify-self:end;border-style:solid;border-width:9px 0 9px 12px;border-color:transparent transparent transparent {INK};opacity:0}}
.sa-opt:hover,.sa-opt:focus-visible{{background:linear-gradient(180deg,#f6dc95,{GOLD} 60%,#d4a043)}}
.sa-opt:hover::after,.sa-opt:focus-visible::after{{opacity:1}}
.sa-opt:active{{transform:translate(2px,3px)}}
.sa-tip{{margin-top:14px;padding:10px 14px;border-radius:12px;background:rgba(14,13,12,.86);border:1px solid rgba(244,236,216,.1);color:{CREAM};font:600 clamp(13px,3.7vw,15px)/1.3 {PB}}}

/* ── malé a nízké telefony ── */
@media (max-height:700px){{
 .sa-col{{padding-top:10px}}
 .sa-logo{{max-width:210px}}
 .sa-title{{font-size:clamp(44px,13.5vw,66px)}}
 .sa-bottom{{gap:8px}}
 .sa-card{{padding:9px 13px 8px!important;font-size:13px!important}}
 .sa-card span{{font-size:13px}}
 .game-root .sa-in{{height:42px;font-size:18px!important}}
 .sa-start{{height:52px;margin-top:6px}}
 .sa-start span{{font-size:32px}}
 .sa-btns{{margin-top:6px}}
 .sa-btn{{height:40px}}
 .sa-q{{font-size:19px;margin:7px 0 9px}}
 .sa-pfig{{height:clamp(90px,18vh,150px)}}
 .game-root .sa-opt{{min-height:46px;font-size:15px}}
 .game-root .sa-opt::before{{width:32px;height:32px;font-size:18px}}
 .sa-tip{{margin-top:10px;padding:8px 12px;font-size:13px}}
}}
@media (max-width:359px){{
 .sa-date>b.big{{font-size:30px}}
 .sa-city>b{{font-size:19px}}
 .sa-btn{{font-size:14px;gap:6px}}
}}
.game-root .ti-poster{{right:auto!important;left:calc(50% + 260px)!important;width:min(calc(50vw - 360px),calc(min(60vh,640px) * .71))!important}}
@media (max-width:1499px){{.game-root .ti-poster{{display:none!important}}}}
@media (max-width:359px){{.sa-date>b.big{{font-size:28px}}.sa-date>b{{font-size:17px}}.sa-date>span{{font-size:11px}}}}
/* telefon na ležato: intro i Pepa se scrollují ve sloupci */
@media (orientation:landscape) and (max-height:500px){{.sa-scene{{display:none}}}}
/* komiksové nadpisy (.cx): Passion One je úzké – tenčí obrys a víc prostoru, ať se písmena neslévají */
.game-root .cx{{-webkit-text-stroke-width:.045em!important;letter-spacing:.035em!important;text-shadow:.05em .06em 0 #121010!important}}
.game-root .ev-bub .cx{{color:#121010!important;-webkit-text-stroke:0!important;letter-spacing:.02em!important;text-shadow:.05em .05em 0 #E2B04E!important}}
/* zobák bubliny u Pepy mimo nápis SECURITY */
.sa-qcard::before{{left:24%}}.sa-qcard::after{{left:calc(24% + 4px)}}
/* iPhone Safari: filtr (komiksový stín) na POSUVNÉM panelu kreslí stín i pod každý text → posouvá se překryv, panel ne */
.game-root div:has(> .gls:not(.bubble)){{align-items:flex-start!important}}
.game-root .gls:not(.bubble){{max-height:none!important;overflow:visible!important;margin-top:auto!important;margin-bottom:auto!important;flex-shrink:0;padding-bottom:calc(clamp(18px,4vw,28px) + 20px)!important}}
"""


def patch(s):
    u = assets()
    # písma: Luckiest Guy → Passion CZ, Baloo 2 → Barlow Semi Condensed (mimo zabudované @font-face)
    assert FONT_OLD in s
    s = s.replace(FONT_OLD, FONT_NEW)
    parts = re.split(r"(@font-face\s*\{[^}]*\})", s)
    for k in range(0, len(parts), 2):
        parts[k] = re.sub(r"(['\"])Luckiest Guy\1", PH, parts[k])
        parts[k] = re.sub(r"(['\"])Baloo 2\1", PB, parts[k])
    s = "".join(parts)
    # intro
    a = s.index('<div style="position:absolute;inset:0;overflow:auto;display:flex;flex-direction:column;align-items:center;justify-content:space-between;gap:clamp(10px,2vh,24px);padding:clamp(12px,2.6vh,28px) clamp(16px,4vw,40px)">')
    b = s.index('<sc-if value="{{ helpOn }}"', a)
    s = s[:a] + INTRO + s[b:]
    # Pepa
    c = s.index('<div data-screen-label="Pepa"')
    d = s.index('\n  </sc-if>', c)
    s = s[:c] + PEPA + s[d:]
    i = s.rindex("</style>")
    return s[:i] + css(u) + s[i:]
