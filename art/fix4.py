# Expertní kontrola 2026-10-04 (2. kolo): opravy logiky z code review + čitelnost žebříčku.
# Volá se z klub.patch() po fix3.
import re

from fix3 import rep

# Em.dot je DJka – slovesa v odpovědích DJů v ženském rodě (jen celá slova, jen pro FEM)
FEM_VERBS = ["podepsal", "sundal", "ukázal", "podal", "rozmyslel", "vzal", "připsal", "trefil", "nepřestal", "dal",
             "nakreslil", "zvedl", "vylil", "hodil", "postavil", "napil", "pustil", "ťukl", "zapomněl", "udělal",
             "zamixoval", "kývl", "pouštěl", "zapsal", "vysmrkal", "předstíral", "viděl", "Odmítl", "brečel",
             "Zahrál", "nehrál", "dělal", "zkoušel", "přišel"]

FEM_JS = ("const FEM={'Em.dot':1};const femTxt=t=>t.replace(/(^|[^A-Za-zÀ-ž])(" + "|".join(FEM_VERBS) +
          ")(?=$|[^A-Za-zÀ-ž])/g,(m,a,v)=>a+v+'a').replace(/(^|[^A-Za-zÀ-ž])(Brečel)\\. Pak jsem brečela já/,'$1Brečel. Pak jsem brečela já');\n")

PL_SIG = "(r.c?r.c+' '+(r.c===1?'podpis':r.c<5?'podpisy':'podpisů'):'bez podpisu')"


def small_passion(s):
    """malé texty (≤ 20 px) v nadpisovém Passion → čitelný Barlow 800 (Passion je na Windows v malém slitý)"""
    def fix(m):
        st = m.group(1)
        if "Passion CZ" not in st:
            return m.group(0)
        fs = re.search(r"font-size:(\d+(?:\.\d+)?)px", st)
        if not fs or float(fs.group(1)) > 20:
            return m.group(0)
        st = re.sub(r"font-family:'Passion CZ'(,\s*'Barlow')?,\s*sans-serif", "font-family:'Barlow',sans-serif", st)
        st = re.sub(r"font-weight:\d+", "font-weight:800", st) if "font-weight" in st else st + ";font-weight:800"
        return 'style="' + st + '"'
    return re.sub(r'style="([^"]*)"', fix, s)


CSS = """
/* ══ FIX4: žebříček čitelně ══ */
.game-root .gls .cap{padding-left:24px!important;padding-right:24px!important}
.game-root .mg-lb span,.game-root [data-screen-label="Konec"] .gl span{-webkit-text-stroke:0!important;text-shadow:none!important}
"""


def patch(s):
    # 1) událost s indexem 0 nezastavila čas; tanec čas taky zastaví (+12 min se připíše na konci kola)
    s = rep(s, "if(s.phase!=='club'||s.ev||s.mg)return;", "if(s.phase!=='club'||s.ev!=null||s.mg||s.dancing)return;")
    # 2) panák za pult opravdu odemkne podpis (dřív se shot nikdy nenastavil a šlo kupovat donekonečna)
    s = rep(s, "A('Poslat panáka za pult','150 Kč · +reputace',()=>this.buy(150,{rep:1,min:2},this.djSay('shot',dj)+' +reputace'),s.shot||s.cash<150),",
            "A(s.shot?'Panák čeká za pultem ✓':'Poslat panáka za pult',s.shot?'teď si řekni o podpis':'150 Kč · +reputace · podpis i bez nálady',"
            "()=>{if(this.state.cash<150){this.say('Na to nemáš.');return;}if(this.state.shot)return;this.setState(x=>({cash:x.cash-150,rep:x.rep+1,m:x.m+2,shot:true,toast:this.djSay('shot',dj)+' +reputace · teď si řekni o podpis',tk:Date.now()}));},s.shot||s.cash<150||has),")
    # 3) hláška o splněném úkolu / měchýři nepřepíše čerstvou hlášku, připojí se k ní
    s = rep(s, "toast:'✓ Úkol „'+Q.t+'“ splněn.", "toast:(s.toast&&Date.now()-s.tk<2500?s.toast+' · ':'')+'✓ Úkol „'+Q.t+'“ splněn.")
    s = rep(s, "p.peeW=true;p.toast='🚽 Měchýř na '", "p.peeW=true;p.toast=(s.toast&&now-s.tk<2500?s.toast+' · ':'')+'🚽 Měchýř na '")
    # 5) uvítání: nový hráč ví, co dělat (podpis chce náladu 55+, start je 40)
    s = rep(s, "toast:'Jsi uvnitř. Za pultem je '+LINEUP[this.curDj(OPEN+x.wait)][1]+'. Běž pro podpis.'",
            "toast:'Jsi uvnitř! Za pultem je '+LINEUP[Math.max(0,this.curDj(OPEN+x.wait))][1]+'. Na podpis potřebuješ náladu 55+, tak to nejdřív rozjeď na parketu. Péťa na baru má úkoly.'")
    # 6) události o konkrétním DJovi jen když hraje; „Poledne“ až kolem poledne
    s = rep(s, "(!e.nt||e.nt===NIGHT.p);};", "(!e.nt||e.nt===NIGHT.p)&&(!e.from||m>=e.from)&&(!e.dj||LINEUP[Math.max(0,this.curDj(m))][1]===e.dj);};")
    s = rep(s, "{t:'Mark Evill',nt:'20261010',loc:'dj',", "{t:'Mark Evill',nt:'20261010',loc:'dj',dj:'Mark Evill',")
    s = rep(s, "{t:'Mazerlogy',nt:'20261011',loc:'dj',", "{t:'Mazerlogy',nt:'20261011',loc:'dj',dj:'Mazer',")
    s = rep(s, "{t:'Mike Frost',nt:'20261011',late:1,", "{t:'Mike Frost',nt:'20261011',late:1,dj:'Mike Frost',")
    s = rep(s, "{t:'Krotitel bubnů',nt:'20261011',loc:'parket',", "{t:'Krotitel bubnů',nt:'20261011',loc:'parket',dj:'Mazer',")
    s = rep(s, "{t:'Poledne',", "{t:'Poledne',from:700,")
    # 7) Em.dot v ženském rodě
    i = s.index("const DJ_SAY={")
    s = s[:i] + FEM_JS + s[i:]
    s = rep(s, "return DJ_SAY[k][b[k].pop()].split('{d}').join(dj||'DJ');}",
            "const t=DJ_SAY[k][b[k].pop()].split('{d}').join(dj||'DJ');return FEM[dj]?femTxt(t):t;}")
    # 8) časové údaje v textech sedí s hodinami
    s = rep(s, "{t:'Mamka volá',d:'Telefon svítí: MAMKA ❤️. Je neděle, 11:00 a ty máš uvnitř sluneční brýle.'",
            "{t:'Mamka volá',late:1,d:'Telefon svítí: MAMKA ❤️. Je skoro poledne a ty máš uvnitř sluneční brýle.'")
    s = rep(s, "Je 7 ráno. Nikdo normální takhle nepíše.", "V tuhle hodinu nikdo normální nepíše.")
    s = rep(s, "Je 9 ráno a má na sobě", "Je ráno a má na sobě")
    s = rep(s, "V klobouku je 40 Kč a lístek na tramvaj.", "V klobouku je 340 Kč a lístek na tramvaj.")
    # 10) Denisa/Martina v pauze řeknou proč (dřív klik na portrét nedělal nic)
    s = rep(s, "if(s.dancing||s.m<s.mixCd)return;const len",
            "if(s.dancing)return;if(s.m<s.mixCd){this.say('Denisa: „Teď ne, mám frontu. Zkus to v '+hm(s.mixCd)+'.“');return;}const len")
    s = rep(s, "if(s.dancing||s.m<s.catchCd)return;const z",
            "if(s.dancing)return;if(s.m<s.catchCd){this.say('Martina: „Ruce si odpočinou do '+hm(s.catchCd)+'.“');return;}const z")
    # 11/12) nová hra vynuluje žebříček; dvojklik nezdvojí podpis ani odměnu za úkol
    s = rep(s, "lbName:x.lbName,phase:'gate',", "lbName:x.lbName,lbSaved:false,lbMsg:'',phase:'gate',")
    s = rep(s, "this.setState(x=>({cards:[...x.cards,dj],", "this.setState(x=>x.cards.includes(dj)?null:({cards:[...x.cards,dj],")
    s = rep(s, "acceptQuest(){const s=this.state,Q=QUESTS[s.q];", "acceptQuest(){this._clq=null;const s=this.state,Q=QUESTS[s.q];")
    s = rep(s, "const last=s.q+1>=QUESTS.length;", "if(this._clq===s.q+'/'+s.qDone)return;this._clq=s.q+'/'+s.qDone;const last=s.q+1>=QUESTS.length;")
    # žebříček: celé slovo místo „podp.“, čísla čitelným písmem
    s = s.replace("' · '+r.c+' podp.'", "' · '+" + PL_SIG)
    assert "podp.'" not in s
    s = small_passion(s)

    i = s.rindex("</style>")
    return s[:i] + CSS + s[i:]
