# Kolo 5 (2026-10-05): nový úvod na fasádě klubu, ikony místo emoji, opravy rozložení miniher,
# bankomat, nedělní story „Ztráty a nálezy“, vylepšené chytání sklenic, napětí ve hře.
# Volá se z klub.patch() po fix4. Každá náhrada přes rep() = přesně jeden výskyt.
import re

from fix3 import rep
from pop import uri

FASADA = "5f1c2a54-0f05-4e54-9a54-fa5ade154054"

# ─────────────────────────── 1) ÚVOD ───────────────────────────
INTRO = """<div data-screen-label="Intro" class="in5">
      <div class="in5-bg"></div>
      <div class="in5-wrap">
        <div class="in5-head">
          <div class="in5-logo bub"><img data-lsrc="uploads/logo54.webp" alt="Studio 54" class="logo54 in5-logoimg"><span>Hybernská 38 · Praha</span></div>
          <div class="in5-date bub gold"><b class="d">{{ nDay }}</b><b class="big">{{ nDate }}</b><span class="n">{{ nName }}</span><span>start <i>{{ nStart }}</i> · do 14:00</span></div>
        </div>
        <div class="in5-pepa bub say"><b>Pepa · face control</b>„Dobrý ráno. Jméno, a pak uvidíme.“</div>
        <div class="in5-top bub" sc-camel-on-click="{{ openLb }}"><b class="in5-toph"><i></i>Pořadí · TOP 10</b><div class="in5-tl"><sc-for list="{{ lbTop10 }}" as="r" hint-placeholder-count="10"><div class="in5-tr" style="color:{{ r.c }}"><span>{{ r.p }}</span><span>{{ r.n }}</span><span>{{ r.s }}</span></div></sc-for></div></div>
        <div class="in5-right">
          <h1 class="sa-title in5-title"><span data-t="Přežij">Přežij</span><span class="g" data-t="after.">after.</span></h1>
          <p class="in5-card bub say2">1 500 Kč, plná baterka a jeden cíl: vydrž do 14:00 a sežeň podpis od všech DJů. <span>Mamka si myslí, že spíš u kamaráda.</span></p>
          <div class="in5-form bub">
            <span class="in5-lbl">Hráč 1 · zadej jméno</span>
            <input class="gi ti-in sa-in in5-in" value="{{ lbName }}" sc-camel-on-change="{{ lbType }}" sc-camel-on-key-down="{{ startKey }}" maxlength="18" placeholder="Tvoje jméno" autocomplete="nickname" enterkeyhint="go">
            <span class="sa-err">{{ nameErr }}</span>
            <button class="ti-start sa-start in5-start" sc-camel-on-click="{{ start }}"><i></i><span>Start!</span></button>
            <div class="sa-btns in5-btns">
              <button class="sa-btn" sc-camel-on-click="{{ openLb }}"><i class="cup"></i><span>Pořadí</span></button>
              <button class="sa-btn" sc-camel-on-click="{{ toggleHelp }}"><i class="q">?</i><span>Jak hrát</span></button>
            </div>
            <span class="in5-best">{{ bestTxt }}</span>
          </div>
        </div>
        <div class="in5-posters">
          <sc-if value="{{ posterOn }}" hint-placeholder-val="{{ false }}"><div class="in5-pst p1"><span>{{ poster1L }}</span><img data-lsrc="{{ posterSrc }}" alt="Program noci"></div></sc-if>
          <sc-if value="{{ poster2On }}" hint-placeholder-val="{{ false }}"><div class="in5-pst p2"><span>{{ poster2L }}</span><img data-lsrc="{{ poster2Src }}" alt="Program další noci"></div></sc-if>
        </div>
        <sc-if value="{{ statsOn }}" hint-placeholder-val="{{ false }}"><span class="sa-count">{{ statsTxt }}</span></sc-if>
      </div>
      """

INTRO_CSS = """
/* ══ FIX5: úvod = fasáda klubu přes celé pozadí + bubliny ══ */
.game-root .in5{position:absolute;inset:0;z-index:30;overflow:hidden;background:#1a0f0a}
.in5-bg{position:absolute;inset:0;background:url("%(F)s") 16%% 0/cover no-repeat}
.in5-bg::after{content:"";position:absolute;inset:0;background:linear-gradient(90deg,rgba(10,6,4,0) 0,rgba(10,6,4,0) 55%%,rgba(10,6,4,.45) 100%%),linear-gradient(0deg,rgba(10,6,4,.55),rgba(10,6,4,0) 35%%)}
.in5-wrap{position:absolute;inset:0;overflow-x:hidden;overflow-y:auto;-webkit-overflow-scrolling:touch}
:where(.in5) .bub{position:relative}
.in5 .bub{background:#F4ECD8;color:#121010;border:3px solid #121010;border-radius:18px;box-shadow:5px 5px 0 #E2B04E,5px 5px 0 3px #121010}
.in5 .bub.gold{background:#E2B04E}
.in5 .bub.say::after{content:"";position:absolute;left:-17px;top:22px;border:9px solid transparent;border-right:14px solid #121010}
.in5 .bub.say::before{content:"";position:absolute;left:-10px;top:25px;z-index:1;border:6px solid transparent;border-right:10px solid #F4ECD8}
.in5-logo{display:flex;flex-direction:column;align-items:center;gap:2px;padding:8px 14px 7px;width:clamp(150px,15vw,250px);transform:rotate(-2deg)}
.game-root .in5-logoimg{display:block;width:100%%!important;height:auto!important;filter:drop-shadow(2px 2px 0 rgba(0,0,0,.35))}
.in5-logo>span{font:800 11.5px/1.1 'Barlow',sans-serif;letter-spacing:.06em;text-transform:uppercase}
.in5-pepa{max-width:250px;padding:10px 14px;font:700 15px/1.3 'Barlow',sans-serif}
.in5-pepa b{display:block;margin-bottom:3px;font:800 11.5px/1 'Barlow',sans-serif;letter-spacing:.06em;text-transform:uppercase;color:#8a6510}
.in5-right{display:flex;flex-direction:column;align-items:stretch;gap:clamp(10px,1.6vh,16px)}
.in5 .in5-date{display:grid;grid-template-columns:auto auto;column-gap:10px;align-items:end;padding:8px 14px;transform:rotate(2deg);font-family:'Barlow',sans-serif}
.in5-date .d{grid-column:1/3;font:800 13px/1 'Barlow';text-transform:uppercase;letter-spacing:.08em}
.in5 .in5-date .big{grid-row:2/4;font:900 clamp(34px,4vw,48px)/.9 'Passion CZ',sans-serif!important;letter-spacing:.01em}
.in5-date .n{font:800 12.5px/1.15 'Barlow';text-transform:uppercase;max-width:150px}
.in5-date>span{font:700 12px/1.2 'Barlow'}
.in5-date i{font-style:normal;font-weight:800}
.game-root .in5-title{margin:0!important;align-self:center;font-size:clamp(52px,6.2vw,96px)!important;filter:drop-shadow(0 6px 10px rgba(0,0,0,.5))}
.in5-card{margin:0;padding:12px 16px;text-align:center;font:700 15px/1.3 'Barlow',sans-serif}
.in5-card>span{display:block;margin-top:4px;color:#A97A2B;font:900 15px/1.1 'Passion CZ';text-transform:uppercase;letter-spacing:.02em}
.in5 .in5-form{display:flex;flex-direction:column;gap:9px;padding:14px 16px 12px;background:#16120e;color:#F4ECD8;border-color:#E2B04E;box-shadow:5px 5px 0 #121010}
.in5-lbl{align-self:center;padding:4px 12px;background:#E2B04E;color:#121010;border-radius:8px;font:800 12.5px/1 'Barlow',sans-serif;letter-spacing:.06em;text-transform:uppercase}
.game-root .in5-in{margin:0!important;width:100%%!important;box-sizing:border-box}
.game-root .in5-start{margin-top:2px!important}
.game-root .in5-btns{display:grid;grid-template-columns:1fr 1fr;gap:10px}
.in5-best{text-align:center;font:700 13px/1.2 'Barlow',sans-serif;color:#F6DA92}
.in5-form .sa-err:empty{display:none}
.in5-posters{display:flex;gap:18px;align-items:flex-end}
.in5-pst{position:relative;width:clamp(120px,11vw,200px);padding:6px;background:#F4ECD8;border:3px solid #121010;border-radius:10px;box-shadow:5px 5px 0 #E2B04E,5px 5px 0 3px #121010;transform:rotate(-3deg)}
.in5-pst.p2{transform:rotate(3deg)}
.in5-pst img{display:block;width:100%%;aspect-ratio:1086/1536;object-fit:cover;border-radius:5px}
.in5-pst>span{position:absolute;z-index:1;left:50%%;top:-14px;transform:translateX(-50%%) rotate(-2deg);white-space:nowrap;padding:4px 10px;background:#E2B04E;color:#121010;border:2px solid #121010;border-radius:7px;font:800 11.5px/1 'Barlow',sans-serif;letter-spacing:.05em;text-transform:uppercase}
.game-root .in5 .sa-count{left:12px;bottom:calc(10px + env(safe-area-inset-bottom))}
/* desktop / na šířku: dveře vlevo volné, plakáty pod neonem, ovládání vpravo */
@media (min-width:900px) and (min-aspect-ratio:5/4){
 .in5-logo{position:absolute;left:2.2%%;top:3%%}
 .in5-pepa{position:absolute;left:27%%;top:34%%}
 .in5-head{display:contents}
 .in5-date{position:absolute;right:3%%;top:3%%}
 .in5-right{position:absolute;right:3%%;top:calc(3%% + 96px);bottom:3%%;width:clamp(330px,30%%,440px);justify-content:center}
 .in5-posters{position:absolute;left:31%%;bottom:4%%}
}
@media (min-width:900px) and (min-aspect-ratio:5/4) and (max-height:760px){
 .in5-right{gap:8px}
 .game-root .in5-title{font-size:clamp(46px,5vw,70px)!important}
 .in5-card{padding:8px 12px;font-size:13.5px}.in5-card>span{font-size:13.5px}
 .in5-form{gap:7px;padding:10px 14px 9px}
 .in5-pst{width:clamp(110px,9.5vw,150px)}
 .in5-pepa{top:30%%}
}
@media (min-width:900px) and (min-aspect-ratio:5/4) and (max-height:620px){
 .in5-posters,.in5-pepa{display:none}
 .in5 .in5-date{display:none}
 .in5-right{top:3%%}
}
@media (min-width:900px) and (min-aspect-ratio:5/4) and (max-width:1180px){.in5-pepa{display:none}.in5-posters{left:4%%;bottom:calc(4%% + 30px)}}
/* mobil a tablet na výšku: pod sebou, dveře prosvítají uprostřed */
@media (max-width:899.98px),(max-aspect-ratio:5/4){
 .in5-bg{background-position:14%% 50%%}
 .in5-wrap{display:flex;flex-direction:column;align-items:center;padding:14px 16px calc(40px + env(safe-area-inset-bottom))}
 .in5-wrap>*{width:100%%;max-width:460px}
 .in5-head{display:flex;justify-content:space-between;align-items:flex-start;gap:12px}
 .in5-logo{width:44%%;max-width:200px;flex:none}
 .in5 .in5-date{max-width:54%%}
 .in5-pepa{display:none}
 .in5-right{flex:1 0 auto;gap:12px}
 .game-root .in5-title{font-size:clamp(46px,14vw,74px)!important;margin-top:clamp(4px,3vh,40px)!important}
 .in5-card{margin-top:auto}
 .in5-posters{order:-1;display:none}
}
@media (min-width:600px) and (max-aspect-ratio:5/4) and (min-height:1100px){
 .in5-wrap .in5-posters{display:flex;justify-content:center;order:0;margin-top:22px;gap:26px}
 .in5-pst{width:min(176px,30vw)}
}
@media (max-width:899.98px) and (max-height:700px),(max-aspect-ratio:5/4) and (max-height:700px){
 .in5-pst{width:min(160px,34vw)}
 .game-root .in5-title{font-size:clamp(40px,12vw,56px)!important}
 .in5-card{padding:8px 12px;font-size:13px}.in5-card>span{font-size:13px}
 .in5-form{gap:7px;padding:10px 12px 9px}
}
/* telefon na šířku: dva sloupce */
@media (max-height:500px) and (min-aspect-ratio:5/4){
 .in5-head{display:contents}
 .in5-logo{position:absolute;left:2.2%%;top:3%%;width:150px}
 .in5-pepa,.in5-posters,.in5 .in5-date{display:none}
 .in5-right{position:absolute;right:3%%;top:0;padding:10px 0 30px;width:min(420px,55%%);justify-content:flex-start}
 .game-root .in5-title{font-size:44px!important}
}
""" % {"F": FASADA}


TOP10_JS = ("lbTop10:(()=>{const l=lbView(s.lb).slice(0,10);if(!l.length)return [{p:'—',n:'Zatím nikdo. Buď první.',s:'',c:'#8d857d'}];"
            "return l.map((r,i)=>({p:String(i+1).padStart(2,'0'),n:r.n,s:String(r.s),c:r.t===s.lbMe?'#FF9F1C':(i<3?'#F6DA92':'#F4ECD8')}));})(), ")

TOP10_CSS = """
/* ══ FIX5: TOP 10 + počítadlo návštěv a her na úvodu ══ */
.in5 .in5-top{background:#16120e;color:#F4ECD8;border-color:#E2B04E;box-shadow:5px 5px 0 #121010;padding:9px 12px 8px;cursor:pointer;transform:rotate(-1deg)}
.in5-toph{display:flex;align-items:center;justify-content:center;gap:7px;margin-bottom:5px;font:800 12.5px/1 'Barlow',sans-serif;letter-spacing:.07em;text-transform:uppercase;color:#E2B04E}
.in5-toph>i{width:16px;height:16px;flex:none;background:url("%(CUP)s") center/contain no-repeat}
.in5-tl{display:grid;grid-template-columns:minmax(0,1fr)}
.in5-tr{display:grid;grid-template-columns:24px minmax(0,1fr) auto;gap:8px;align-items:center;padding:3px 0;border-top:1px solid rgba(255,255,255,.08);font:700 13.5px/1.25 'Barlow',sans-serif}
.in5-tr>span:nth-child(1){font-weight:800;font-size:11.5px;opacity:.75}
.in5-tr>span:nth-child(2){overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.in5-tr>span:nth-child(3){font-weight:800;font-variant-numeric:tabular-nums}
.game-root .in5 .sa-count{z-index:41;padding:5px 11px;border:2px solid #E2B04E;border-radius:9px;background:rgba(18,16,16,.88);color:#F6DA92;font:800 12.5px/1.2 'Barlow',sans-serif;letter-spacing:.02em}
@media (min-width:900px) and (min-aspect-ratio:5/4){
 .in5-top{position:absolute;left:2.2%%;top:calc(3%% + min(15vw,250px)*.5 + 48px);width:clamp(230px,19%%,300px)}
}
@media (min-width:900px) and (min-aspect-ratio:5/4) and (max-height:760px){
 .in5-tr{padding:2px 0;font-size:12.5px}
 .in5-top{top:calc(3%% + min(15vw,250px)*.5 + 40px)}
}
@media (min-width:900px) and (min-aspect-ratio:5/4) and (max-height:620px){.in5-tr:nth-child(n+6){display:none}}
@media (min-width:900px) and (min-aspect-ratio:5/4) and (max-width:1180px){.in5-posters{left:calc(2.2%% + clamp(230px,19%%,300px) + 34px)}}
@media (max-width:899.98px),(max-aspect-ratio:5/4){
 .in5-right{display:contents}
 .in5-wrap{gap:12px}
 .in5-head{order:0}.in5-title{order:1}.in5-top{order:2}.in5-card{order:3}.in5-form{order:4}.in5-wrap .in5-posters{order:5}
 .in5-wrap .in5-top{width:100%%;max-width:460px;box-sizing:border-box;transform:none;padding:7px 10px 6px}
 .in5-tl{grid-template-columns:1fr 1fr;grid-template-rows:repeat(5,auto);grid-auto-flow:column;column-gap:14px}
 .in5-tr{grid-template-columns:20px minmax(0,1fr) auto;gap:6px;padding:2px 0;font-size:12.5px}
 .in5-tr>span:nth-child(1){font-size:10.5px}
 .in5-toph{margin-bottom:3px;font-size:11.5px}
 .in5-right>.in5-card,.in5-right>.in5-form{width:100%%;max-width:460px;box-sizing:border-box}
 .in5-wrap{padding-bottom:calc(14px + env(safe-area-inset-bottom))}
 .game-root .in5 .sa-count{position:static;order:6;align-self:center;width:auto;max-width:none;flex:none}
}
@media (max-width:899.98px) and (max-height:740px),(max-aspect-ratio:5/4) and (max-height:740px){
 .in5-tl{grid-template-rows:repeat(3,auto)}.in5-tr:nth-child(n+7){display:none}
 .in5-wrap{gap:9px}
 .game-root .in5-title{margin-top:2px!important}
}
@media (max-width:899.98px) and (max-height:680px),(max-aspect-ratio:5/4) and (max-height:680px){
 .in5-tl{grid-template-rows:repeat(2,auto)}.in5-tr:nth-child(n+5){display:none}
}
@media (max-height:500px) and (min-aspect-ratio:5/4){
 .in5-right{display:flex}
 .in5-wrap .in5-top{position:absolute;left:2.2%%;top:calc(3%% + 94px);width:min(300px,38%%);transform:none}
 .in5 .in5-logo{width:124px}
 .game-root .in5 .sa-count{position:absolute;bottom:calc(8px + env(safe-area-inset-bottom))}
 .in5-tl{grid-template-columns:minmax(0,1fr);grid-template-rows:none;grid-auto-flow:row}
 .in5-tr{padding:1px 0;font-size:12px}
 .in5-wrap .in5-tl>.in5-tr{display:grid}
}
@media (max-height:340px) and (min-aspect-ratio:5/4){.in5-wrap .in5-tl>.in5-tr:nth-child(n+6){display:none}}
"""


def intro(s):
    i = s.index('<div data-screen-label="Intro"')
    j = s.index('<sc-if value="{{ helpOn }}"', i)
    s = s[:i] + INTRO + s[j:]
    s = rep(s, "lbTop5:(()=>{", TOP10_JS + "lbTop5:(()=>{")
    return s


# ─────────────────────────── 2) IKONY MÍSTO EMOJI ───────────────────────────
def ico(body, col):
    return uri(f"<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='{col}' "
               f"stroke-width='2.2' stroke-linecap='round' stroke-linejoin='round'>{body}</svg>")


G, K = "#E2B04E", "#121010"
SV = {
    "ball": "<circle cx='12' cy='12' r='8.5'/><path d='M3.5 12h17M12 3.5v17M5.5 7h13M5.5 17h13M8 4.5c-2 5-2 10 0 15M16 4.5c2 5 2 10 0 15'/>",
    "head": "<path d='M4 15v-3a8 8 0 0 1 16 0v3'/><rect x='3' y='14' width='4.5' height='6.5' rx='1.5'/><rect x='16.5' y='14' width='4.5' height='6.5' rx='1.5'/>",
    "glass": "<path d='M4 4h16l-8 9z'/><path d='M12 13v7M8 20.5h8'/><path d='M16 4l2.5-2'/>",
    "crown": "<path d='M3.5 18.5h17M4 16l-1-9 5 4 4-6 4 6 5-4-1 9z'/>",
    "wc": "<path d='M6 3.5h7v6H6z'/><path d='M4.5 9.5h15c0 4.5-3 7-7.5 7S4.5 14 4.5 9.5z'/><path d='M9 16.5l-1 4h8l-1-4'/>",
    "bolt": "<path d='M13.5 2.5L5 13.5h6l-1 8 8.5-11h-6z' fill='#COL'/>",
    "flame": "<path d='M12 21.5c4 0 6.5-2.6 6.5-6.3 0-3.7-3-6-3.8-9.7-1.9 1.4-3 3.4-3 5.3C10.6 9.3 9.4 8 9 6.5 6.8 8.5 5.5 11.5 5.5 15.2c0 3.7 2.5 6.3 6.5 6.3z' fill='#COL'/>",
    "drop": "<path d='M12 2.8c3.4 4.6 6 7.8 6 11.2a6 6 0 0 1-12 0c0-3.4 2.6-6.6 6-11.2z' fill='#COL'/>",
    "cash": "<rect x='2.5' y='6' width='19' height='12' rx='2'/><circle cx='12' cy='12' r='2.8'/><path d='M6 9.5v5M18 9.5v5'/>",
    "star": "<path d='M12 3l2.7 5.6 6.1.9-4.4 4.3 1 6.1L12 17l-5.4 2.9 1-6.1-4.4-4.3 6.1-.9z' fill='#COL'/>",
    "cup": "<path d='M7 3.5h10v5a5 5 0 0 1-10 0z'/><path d='M7 5.5H3.5c0 3 1.5 4.5 3.8 4.6M17 5.5h3.5c0 3-1.5 4.5-3.8 4.6M12 13.5v4M8 20.5h8M9.5 17.5h5'/>",
}


def svg(k, col):
    return ico(SV[k].replace("#COL", col), col)


ICON_CSS = """
/* ══ FIX5: vlastní ikony místo obecných emoji ══ */
.game-root .hud-tabs>.hud-tab::before{content:""!important;background:#121010 center/17px 17px no-repeat!important}
.game-root .hud-tabs>.hud-tab:nth-child(1)::before{background-image:%(ball)s!important}
.game-root .hud-tabs>.hud-tab:nth-child(2)::before{background-image:%(head)s!important}
.game-root .hud-tabs>.hud-tab:nth-child(3)::before{background-image:%(glass)s!important}
.game-root .hud-tabs>.hud-tab:nth-child(4)::before{background-image:%(crown)s!important}
.game-root .hud-tabs>.hud-tab:nth-child(5)::before{background-image:%(wc)s!important}
.game-root .hud-stats .hud-mk::before,.game-root .hud-stats .hud-chip-k::before{content:""!important;display:inline-block;width:1.15em;height:1.15em;margin-right:.3em;vertical-align:-.2em;background:center/contain no-repeat}
.game-root .hud-stats>.hud-meter:nth-child(1) .hud-mk::before{background-image:%(bolt)s}
.game-root .hud-stats>.hud-meter:nth-child(2) .hud-mk::before{background-image:%(flame)s}
.game-root .hud-stats>.hud-meter:nth-child(3) .hud-mk::before{background-image:%(drop)s}
.game-root .hud-stats>.hud-chip:nth-last-child(3) .hud-chip-k::before{background-image:%(cash)s}
.game-root .hud-stats>.hud-chip:nth-last-child(2) .hud-chip-k::before{background-image:%(star)s}
.game-root .hud-stats>.hud-chip:nth-last-child(1) .hud-chip-k::before{background-image:%(cup)s}
""" % {"ball": svg("ball", G), "head": svg("head", G), "glass": svg("glass", G), "crown": svg("crown", G), "wc": svg("wc", G),
       "bolt": svg("bolt", "#F6DA92"), "flame": svg("flame", "#FF7A3D"), "drop": svg("drop", "#5CC8FF"),
       "cash": svg("cash", K), "star": svg("star", K), "cup": svg("cup", K)}

# texty: obecné emoji pryč (kreslené ikony surovin v IC_EM/ING zůstávají – vykreslují se jako vlastní ikony)
EMO_TXT = [(" 💧'", "'"), (" 📼'", "'"), (" 📸'", "'"), (" 👁️'", "'"), (" ✈️'", "'"), (" 💃'", "'"),
           (" 🥂'", "!'"), ("' ✍️ Podpis '", "' · Podpis '"), (" Máš sluchátka! 🎧 Utíkej", " Máš sluchátka! Utíkej"),
           (" · 🔑',", " · klíč od personálního WC',"), (" 🔑'", "'"), ("MAMKA ❤️", "MAMKA"),
           ("'Típnout a poslat 👍'", "'Típnout a poslat palec nahoru'"), ("jak se máš? 🙂“", "jak se máš? :)“"),
           ("zlatíčko? 😘“", "zlatíčko? Pusinky.“"), ("'🚽 Měchýř na '", "'Měchýř na '"),
           ("p:i===0?'🥇':i===1?'🥈':i===2?'🥉':String(i+1).padStart(2,'0')", "p:String(i+1).padStart(2,'0')"),
           ("p:['🥇','🥈','🥉'][i]||String(i+1).padStart(2,'0')", "p:String(i+1).padStart(2,'0')"),
           ("DZ_IC=['👐','🕺','💃','🤘']", "DZ_IC=['1','2','3','4']")]


def emoji(s):
    for a, b in EMO_TXT:
        n = s.count(a)
        assert n >= 1, a
        s = s.replace(a, b)
    return s


# ─────────────────────────── 3) ROZLOŽENÍ ───────────────────────────
LAYOUT_CSS = """
/* ══ FIX5: kostky surovin, čipy, minihry a portréty bez přetékání ══ */
.game-root .mg-mix .mg-grid{gap:8px!important}
.game-root .mg-mix .mg-grid .gb{min-height:64px!important;padding:6px 2px!important;overflow:hidden;box-sizing:border-box}
.game-root .mg-mix .mg-grid .gb span:first-child{font-size:28px!important}
.game-root .mg-mix .mg-grid .gb span:last-child{display:block;max-width:100%;font:800 11.5px/1.1 'Barlow',sans-serif!important;letter-spacing:.02em!important;text-transform:uppercase;color:#121010!important;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.game-root .mg-chip{font:700 14px/1.15 'Barlow',sans-serif!important;padding:6px 10px!important}
.game-root .mg-chip>span:first-child{font-size:18px!important}
.game-root .mg-chips{justify-content:center}
.game-root .gls[class*="mg-"]{gap:12px!important}
@media (max-height:820px){
 .game-root .gls[class*="mg-"]{padding:16px 18px!important;gap:9px!important}
 .game-root .gls[class*="mg-"] .glow-img{width:58px!important}
 .game-root .gls[class*="mg-"] .cx{font-size:clamp(22px,5vw,30px)!important}
 .game-root .gls[class*="mg-"] .cap{font-size:14.5px!important;padding:8px 14px!important}
 .game-root .mg-mix .mg-grid .gb{min-height:54px!important}
 .game-root .mg-mix .mg-grid .gb span:first-child{font-size:24px!important}
 .game-root .mg-shaker{transform:scale(.8);margin:-8px 0}
}
/* DJ portrét na mobilu nesmí zabrat celou obrazovku */
.game-root img.dj-port{width:min(100%,calc(34vh * 400 / 460))!important;margin:0 auto!important}
@media (max-width:899px){.game-root img.dj-port{width:min(100%,calc(28vh * 400 / 460))!important}}
"""


def patch_part1(s):
    s = intro(s)
    s = emoji(s)
    s = rep(s, '<img class="glow-img" data-lsrc="{{ locImg }}"', '<img class="glow-img dj-port" data-lsrc="{{ locImg }}"')
    i = s.rindex("</style>")
    return s[:i] + INTRO_CSS + TOP10_CSS % {"CUP": svg("cup", G)} + ICON_CSS + LAYOUT_CSS + s[i:]


def patch(s):
    s = patch_part1(s)
    return s
