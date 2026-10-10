# Úpravy 2026-10-04 večer (podle uživatele): čitelnější písmo, hlášky déle, pomalejší čas + postupný začátek,
# vtipné a neopakující se odpovědi DJů, celistvý rám panelů (TOP 10), úvod: menší sloupec, dva plakáty
# (pátek / sobota v noci), počítadlo malé v levém rohu. Volá se z klub.patch() úplně poslední (po slim).
import re

INK, GOLD, GOLD_D, CREAM = "#121010", "#E2B04E", "#A97A2B", "#F4ECD8"
PB = "'Barlow'"


def rep(s, old, new):
    assert s.count(old) == 1, f"kotva {s.count(old)}×: " + old[:90]
    return s.replace(old, new)


# ─── odpovědi DJů: {d} = jméno DJe; zásobník se neopakuje, dokud se nevystřídá všechno ───
DJ_LINES = {
    "no": [
        "{d}: „Nejdřív se roztanči. Takhle vypadáš jak ve frontě na úřadě.“",
        "{d}: „Podpis? S tímhle výrazem ti podepíšu leda omluvenku do školy.“",
        "{d} si sundal jedno sluchátko: „Cože? … Ne. Nejdřív se zpoť.“",
        "{d}: „Podepisuju jen lidem, co tancujou. Ty jen stojíš a mrkáš jak semafor.“",
        "{d} ukázal na parket, pak na tebe, pak zase na parket. Pochopils.",
        "{d}: „Kámo, tvoje nálada má míň BPM než výtah v paneláku.“",
        "{d}: „Přijď, až budeš vypadat, že tě to baví. Teď vypadáš, že tě sem poslala mamka.“",
        "{d} ti podal fixu, pak si to rozmyslel a vzal ji zpátky: „Ještě ne. Zatanči si.“",
        "{d}: „Vidíš toho týpka v košili? Tomáš. Tancuje od jedný. Buď jako Tomáš.“",
        "{d}: „Podpis jen od nálady 55. Ty máš tak dvanáct. A to počítám i tričko.“",
        "{d}: „Pepa tě nechal projít? Zajímavý. Já tě k pultu zatím nepustím.“",
        "{d}: „Fixa mi došla. Teda… dojde se, až se roztančíš.“",
    ],
    "ok": [
        "{d} ti podepsal kartu a připsal „nebreč u pultu“.",
        "{d} se podepsal tak rozmáchle, že trefil i Kevina.",
        "{d} ti podepsal kartu fixou, která voní jako rok 2004.",
        "{d}: „Podepíšu, ale nikomu neříkej, že jsem tě viděl tancovat.“ Podepsáno!",
        "{d} podepsal kartu jednou rukou a druhou ani nepřestal mixovat. Profík.",
        "{d} podepsal a dal ti pěstičku. Pěstička byla trochu lepkavá. Neřeš to.",
        "{d}: „Pro tebe? Jasně. Pro mamku taky, kdyby se ptala, kde jsi.“ Podpis máš!",
        "{d} ti podepsal kartu a nakreslil k tomu kouli. Vypadá spíš jako brambora.",
        "{d}: „Tohle si zarámuj. Za deset let to bude stát minimálně jedno pivo.“",
    ],
    "shot": [
        "{d} zvedl panáka na tvoje zdraví a málem ho vylil do mixpultu.",
        "{d} hodil panáka do sebe přesně na jedničku. Respekt.",
        "{d}: „Na zdraví! Teda na tvoje. Moje už je pryč.“",
        "{d} postavil panáka obřadně vedle mixpultu. Prej na později. Později je v sedm ráno.",
        "{d} se napil a pustil tak tvrdej drop, že Pepa u dveří zavřel oči.",
        "{d} ťukl panákem o sluchátka. Prej tradice. Nikdo neví čí.",
        "{d}: „Tohle ti nezapomenu.“ Za pět minut zapomněl. Reputace ti ale zůstala.",
        "{d} ti ukázal srdíčko. Pak z něj udělal číslo sedm. Asi chce další.",
    ],
    "req_ok": [
        "Zahrál ji! Parket explodoval. Ty taky. Brečíš štěstím.",
        "{d} ji zamixoval tak, že ji poznal jen pes v šatně. Ale lidi šílí.",
        "{d} ji pustil a celej parket zpívá. Falešně, ale z plných plic.",
        "{d} kývl, chvíli nic, a pak BUM – tvoje písnička. Tomáš ti padl kolem krku.",
        "Zahrál ji! Kevin s Perrym přiběhli ze záchodů, aby to neprošvihli.",
        "{d}: „Tuhle jsem naposledy pouštěl na maturáku.“ Pustil ji a parket se zbláznil.",
    ],
    "req_ko": [
        "{d} kývl, usmál se a nezahraje to. Nikdy.",
        "{d}: „Macarenu? Tady? Chceš, abych přišel o práci?“",
        "{d} si tvoje přání zapsal na papírek. Pak do papírku vysmrkal.",
        "{d} předstíral, že neslyší. Velmi přesvědčivě. Má sluchátka i v očích.",
        "{d}: „Jo, jasně, hned po mixu od Kevina a Perryho.“ To znamená nikdy.",
        "{d} ukázal na ceduli „Nepřijímáme přání“. Tu ceduli tam dal právě teď.",
        "{d}: „Tohle hraju jen na svatbách. A ty nevypadáš jako nevěsta.“",
    ],
    "talk": [
        "{d}: „Víš, co je nejhorší? Když lidi tleskaj do rytmu. Mimo rytmus.“",
        "{d}: „Já vlastně nehraju, já jen zkouším sluchátka. Už čtyři hodiny.“",
        "{d}: „Kevin mi nabízel mix Big Girl. Odmítl jsem. Brečel. Pak jsem brečel já.“",
        "{d}: „Pepa mě dneska nechtěl pustit dovnitř. Na můj vlastní set.“",
        "{d}: „Vidíš tu kouli? Visí tu od roku 2004 a pořád má lepší pohyby než ty.“",
        "{d}: „Mamka si myslí, že dělám v IT. Technicky… mačkám tlačítka.“",
        "{d}: „Ibiza je fajn, ale tady v Hybernský to v sedm ráno teprv začíná.“",
        "{d}: „Psst. Péťa na baru má pro tebe úkol. Když se usměješ, dá ti lepší.“",
        "{d}: „Denisa si pamatuje každej drink, co jsem kdy vypil. Proto se jí bojím.“",
        "{d}: „Tomáš mi přinesl vodu. Už potřetí. Myslím, že mě adoptoval.“",
        "{d}: „Tenhle track jsem dělal v autobuse. Ten hrbol v base je retardér.“",
        "{d}: „Kdyby ses ptal, na co hraju: hlavně na nervy Pepovi.“",
        "{d}: „Podpis ti dám, až budeš mít náladu. Nálada se dělá na parketu, ne tady.“",
    ],
}


def js_str(t):
    return "'" + t.replace("\\", "\\\\").replace("'", "\\'") + "'"


def dj_const():
    body = ",".join(f"{k}:[" + ",".join(js_str(x) for x in v) + "]" for k, v in DJ_LINES.items())
    return "const DJ_SAY={" + body + "};\n"


CSS = f"""
/* ══ FIX3: čitelnost, celistvé panely, úvod ══ */
/* písmo: širší Barlow místo zúženého, drobné popisky bez úzkého Anton */
.game-root .ctag,.game-root .loc-cap>span:first-child,.game-root .hud-meter span,.game-root .hud-chip span,.game-root .hud-tab span:last-child,.game-root .mg-chip,.game-root .dz-hint,.game-root .lbl-c,.game-root .hud-tab span:first-child{{font-family:{PB},sans-serif!important;font-weight:700!important;letter-spacing:.02em!important}}
.game-root .chat>.gb,.game-root .opts>.gb,.game-root .mg-opts>button{{font-family:{PB},sans-serif!important;font-weight:700!important;letter-spacing:0!important}}
.game-root .cap,.game-root p,.game-root .hud-toast,.game-root .gls,.game-root .ev-bub{{font-weight:600!important;-webkit-font-smoothing:antialiased}}
.game-root .hud-toast,.game-root .ev-bub,.game-root .cap,.game-root p{{-webkit-text-stroke:0!important;text-shadow:none!important}}
.game-root .hud-toast{{font-size:max(15px,1em)!important;line-height:1.35!important}}
.game-root .hud-toast:hover{{animation-play-state:paused!important}}
/* panely: jeden čistý rám (dřív se překrýval roztřepený papír + rovný rám + posunutý stín → „rozjetý“) */
.game-root .gls:not(.bubble){{background-image:none!important;background:#16120e!important;border:3px solid {GOLD}!important;border-radius:16px!important;box-shadow:8px 8px 0 {INK}!important;filter:none!important}}
.game-root .gls:not(.bubble)::before{{border-radius:13px!important}}
.game-root .gls:not(.bubble)::after{{display:none!important}}
/* úvod: užší sloupec na velkých obrazovkách */
@media (min-width:900px){{.sa-col{{max-width:410px}}}}
.sa-card{{font-size:clamp(13px,3.5vw,14.5px)!important}}
.sa-brand{{flex:1 1 0!important;min-width:150px!important}}
.game-root .sa-logo{{height:auto!important}}
@media (max-width:520px){{.game-root .hud-tab span{{letter-spacing:0!important}}}}
/* konec hry: statistiky a pořadí stejným čistým rámem, obsah uvnitř rámu */
[data-screen-label="Konec"] .gl:not(button){{background-image:none!important;background:#16120e!important;border:3px solid {GOLD}!important;border-radius:16px!important;box-shadow:8px 8px 0 {INK}!important;filter:none!important;overflow:hidden}}
[data-screen-label="Konec"] .gl:not(button){{padding:16px 18px!important}}
[data-screen-label="Konec"] .cap{{padding:16px 46px!important;box-sizing:border-box}}
/* počítadlo: malé v levém dolním rohu */
.game-root .sa-count{{position:absolute;z-index:40;left:10px;bottom:calc(8px + env(safe-area-inset-bottom));padding:4px 9px;border-radius:8px;background:rgba(10,9,8,.72);color:rgba(244,236,216,.82);font:600 11.5px/1.2 {PB},sans-serif;letter-spacing:.01em;pointer-events:none;white-space:nowrap}}
@media (max-width:899px){{.sa-icol{{padding-bottom:calc(36px + env(safe-area-inset-bottom))!important}}}}
/* plakáty: pátek vlevo, sobota vpravo, menší */
.game-root .ti-poster{{display:none!important}}
@media (min-width:1180px) and (min-height:620px){{
 .game-root .ti-poster{{display:block!important;position:absolute;z-index:1;top:50%;width:min(300px,calc(50% - 290px))!important;left:auto!important;right:auto!important;border:4px solid {INK};border-radius:6px;background:{INK};box-shadow:9px 9px 0 {GOLD_D},9px 9px 0 4px {INK}!important}}
 .game-root .ti-poster img{{display:block!important;width:100%!important;height:auto!important;border-radius:3px}}
 .game-root .ti-poster>span{{position:absolute;left:-18px;top:-22px;z-index:1;font-family:'Passion CZ',sans-serif;text-transform:uppercase;color:{INK};padding:6px 14px 4px;transform:rotate(-7deg)}}
 .game-root .ti-poster::after{{content:"";position:absolute;right:28%;top:-14px;width:84px;height:26px;background:rgba(244,236,216,.75);transform:rotate(4deg);box-shadow:0 1px 0 rgba(0,0,0,.3)}}
 .game-root .ti-poster.ti-p1{{right:calc(50% + 250px)!important;transform:translateY(-50%) rotate(-3deg)!important}}
 .game-root .ti-poster.ti-p2,.game-root .ti-poster.ti-solo{{left:calc(50% + 250px)!important;transform:translateY(-50%) rotate(3deg)!important}}
 .game-root .ti-poster>span{{font-size:17px!important;white-space:nowrap}}
 .game-root .ti-poster.ti-p2>span,.game-root .ti-poster.ti-solo>span{{left:auto!important;right:-18px!important;transform:rotate(6deg)!important}}
}}
@media (min-width:1180px) and (max-height:820px){{.game-root .ti-poster{{width:min(250px,calc(50% - 290px))!important}}}}
"""


def patch(s):
    # 1) písmo: Barlow Semi Condensed → Barlow (mimo @font-face), načíst Barlow z Google Fonts
    s = rep(s, "family=Anton&family=Barlow+Semi+Condensed:wght@500;600;700;800&display=swap",
            "family=Anton&family=Barlow:wght@500;600;700;800&display=swap")
    parts = re.split(r"(@font-face\s*\{[^}]*\})", s)
    for k in range(0, len(parts), 2):
        parts[k] = parts[k].replace("'Barlow Semi Condensed'", PB)
    s = "".join(parts)
    # drobné písmo o kousek větší
    s = re.sub(r"font-size:(10|11|12)px", lambda m: "font-size:" + {"10": "11.5", "11": "12", "12": "13"}[m.group(1)] + "px", s)

    # 2) hlášky: déle na obrazovce (10–30 s podle délky), zavření klepnutím zůstává
    s = rep(s, "toastDur:Math.min(16,Math.max(6.5,3.5+String(s.toast||'').length/11)).toFixed(1)+'s'",
            "toastDur:Math.min(30,Math.max(10,5+String(s.toast||'').length/8)).toFixed(1)+'s'")
    s = rep(s, "@keyframes popR{0%{transform:translate(-50%,-8px);opacity:0}4%,93%{",
            "@keyframes popR{0%{transform:translate(-50%,-8px);opacity:0}2%,96%{")
    s = rep(s, "@keyframes popM{0%{transform:translateY(-8px);opacity:0}4%,93%{",
            "@keyframes popM{0%{transform:translateY(-8px);opacity:0}2%,96%{")

    # 3) čas: pomalejší hodiny, max. krok 1 s (návrat ze záložky neposune noc), klidný začátek a řidší události
    s = rep(s, "const SP={'pomalu':1100,'normálně':650,'rychle':320};", "const SP={'pomalu':1600,'normálně':1100,'rychle':650};")
    s = rep(s, "const s=this.state,now=Date.now(),dt=now-(this.lt||now);this.lt=now;",
            "const s=this.state,now=Date.now(),dt=Math.min(1000,now-(this.lt||now));this.lt=now;")
    s = rep(s, "p.nextEv=m+28+Math.random()*34;", "p.nextEv=m+45+Math.random()*40;")
    s = rep(s, "phase:'club',m:OPEN+x.wait,toast:", "phase:'club',m:OPEN+x.wait,nextEv:OPEN+x.wait+70,toast:")

    # 4) DJ: neopakující se vtipné odpovědi + nová akce „Pokecat s DJem“
    i = s.index("const SP={")
    s = s[:i] + dj_const() + s[i:]
    s = rep(s, "  say(t){",
            "  djSay(k,dj){const b=this.djB||(this.djB={});if(!b[k]||!b[k].length)b[k]=shuf(DJ_SAY[k].map((_,i)=>i));return DJ_SAY[k][b[k].pop()].split('{d}').join(dj||'DJ');}\n  say(t){")
    s = rep(s, "this.apply({min:3},dj+': „Nejdřív se roztanči. Takhle vypadáš jak ve frontě na úřadě.“');",
            "this.apply({min:3},this.djSay('no',dj));")
    s = rep(s, "toast:dj+' ti podepsal kartu! ('+(x.cards.length+1)+'/'+LINEUP.length+')'",
            "toast:this.djSay('ok',dj)+' ✍️ Podpis '+(x.cards.length+1)+'/'+LINEUP.length")
    s = rep(s, "this.buy(150,{rep:1,min:2},dj+' zvedl panáka na tvoje zdraví a málem ho vylil do mixpultu.')",
            "this.buy(150,{rep:1,min:2},this.djSay('shot',dj)+' +reputace')")
    s = rep(s, "this.apply({vibe:18,min:5},'Zahrál ji! Parket explodoval. Ty taky. Brečíš štěstím. +18 nálada'):this.apply({vibe:-4,min:5},dj+' kývl, usmál se a nezahraje to. Nikdy.'))",
            "this.apply({vibe:18,min:5},this.djSay('req_ok',dj)+' +18 nálada'):this.apply({vibe:-4,min:5},this.djSay('req_ko',dj)+' −4 nálada')),\n"
            "        A('Pokecat s DJem','+3 nálada · 3 min',()=>this.apply({vibe:3,min:3},this.djSay('talk',dj)))")

    # 5) úvod: počítadlo bez emoji do levého rohu, pod tlačítky jen rekord
    s = rep(s, "statsTxt:t?'👀 '+f(t.visits)+' '+pl(t.visits,'návštěva','návštěvy','návštěv')+' · 🎮 '+f(t.plays)+' '+pl(t.plays,'odehraná hra','odehrané hry','odehraných her'):''",
            "statsTxt:t?f(t.visits)+' '+pl(t.visits,'návštěva','návštěvy','návštěv')+' · '+f(t.plays)+' '+pl(t.plays,'hra','hry','her'):''")
    s = rep(s, '<sc-if value="{{ statsOn }}" hint-placeholder-val="{{ false }}"><span class="ti-stats">{{ statsTxt }}</span></sc-if></div>', "</div>")
    s = rep(s, '<div class="sa-col sa-icol">',
            '<sc-if value="{{ statsOn }}" hint-placeholder-val="{{ false }}"><span class="sa-count">{{ statsTxt }}</span></sc-if>\n      <div class="sa-col sa-icol">')

    # 6) plakáty: tato noc + následující, popisek podle dne, kdy noc začíná (pátek / sobota v noci)
    s = rep(s, '<sc-if value="{{ posterOn }}" hint-placeholder-val="{{ false }}"><div class="ti-poster"><span>Dnes v klubu</span><img data-lsrc="{{ posterSrc }}" alt="Program dnešní noci"></div></sc-if>',
            '<sc-if value="{{ posterOn }}" hint-placeholder-val="{{ false }}"><div class="{{ poster1Cls }}"><span>{{ poster1L }}</span><img data-lsrc="{{ posterSrc }}" alt="Program noci"></div></sc-if>'
            '<sc-if value="{{ poster2On }}" hint-placeholder-val="{{ false }}"><div class="ti-poster ti-p2"><span>{{ poster2L }}</span><img data-lsrc="{{ poster2Src }}" alt="Program další noci"></div></sc-if>')
    s = rep(s, "posterSrc:NIGHT.p?'uploads/poster-'+NIGHT.p+'.webp':'',",
            "posterSrc:NIGHT.p?'uploads/poster-'+NIGHT.p+'.webp':'',poster2On:!!(NIGHT2&&NIGHT2.p),poster2Src:NIGHT2&&NIGHT2.p?'uploads/poster-'+NIGHT2.p+'.webp':'',"
            "poster1L:nightLbl(NIGHT),poster2L:NIGHT2?nightLbl(NIGHT2):'',poster1Cls:'ti-poster '+(NIGHT2&&NIGHT2.p?'ti-p1':'ti-solo'),")
    s = rep(s, "const LINEUP=NIGHT.l;",
            "const NIGHT2=(()=>{const ks=Object.keys(PROGRAM).sort(),k=ks.find(x=>PROGRAM[x]===NIGHT);const n=ks[ks.indexOf(k)+1];return n?Object.assign({k:n},PROGRAM[n]):null;})();\n"
            "const nightLbl=N=>{const k=N.k||Object.keys(PROGRAM).find(x=>PROGRAM[x]===N);if(!k)return 'V klubu';const d=new Date(k+'T12:00:00');d.setDate(d.getDate()-1);"
            "return ['Neděle','Pondělí','Úterý','Středa','Čtvrtek','Pátek','Sobota'][d.getDay()]+' v noci';};\n"
            "const LINEUP=NIGHT.l;")

    # TOP 10 i na konci hry (dřív nápis top 20)
    s = rep(s, "lbScope:LB_API&&!s.lbErr?'Všichni hráči · top 20':'Toto zařízení · top 20',", "lbScope:LB_API&&!s.lbErr?'Všichni hráči · top 10':'Toto zařízení · top 10',")

    i = s.rindex("</style>")
    return s[:i] + CSS + s[i:]
