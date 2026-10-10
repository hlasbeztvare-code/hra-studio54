# Minihry na baru: Martina (chytání sklenky) + Denisa (pamatování drinku) – komiksová grafika, chytáky, víc vtipu.
# Volá se z klub.patch().
from pop import uri, INK, Y, R, O, PAPER
from pop_shapes import torn, burstbox, DARK

COCKTAIL = uri(f"<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 60 70'>"
               f"<line x1='40' y1='4' x2='33' y2='22' stroke='{INK}' stroke-width='2.5'/><circle cx='40' cy='9' r='5' fill='#5DBB3F' stroke='{INK}' stroke-width='2.5'/>"
               f"<polygon points='5,10 55,10 30,38' fill='#fff' stroke='{INK}' stroke-width='3.5' stroke-linejoin='round'/>"
               f"<polygon points='11,14 49,14 30,34' fill='#FF4F9A'/><line x1='14' y1='16' x2='22' y2='16' stroke='#fff' stroke-width='2.5' stroke-linecap='round'/>"
               f"<line x1='30' y1='38' x2='30' y2='60' stroke='{INK}' stroke-width='4'/><ellipse cx='30' cy='62' rx='14' ry='4.5' fill='#fff' stroke='{INK}' stroke-width='3'/></svg>")
FIRE = uri(f"<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 60 70'>"
           f"<path d='M30,2 C42,14 46,22 40,32 L20,32 C13,22 20,12 26,8 C26,14 28,16 30,2 Z' fill='{R}' stroke='{INK}' stroke-width='3' stroke-linejoin='round'/>"
           f"<path d='M30,14 C36,20 37,26 34,32 L25,32 C22,26 26,20 30,14 Z' fill='{Y}'/>"
           f"<polygon points='15,32 45,32 41,64 19,64' fill='{O}' stroke='{INK}' stroke-width='3.5' stroke-linejoin='round'/>"
           f"<line x1='20' y1='38' x2='22' y2='56' stroke='#fff' stroke-width='2.5' stroke-linecap='round'/></svg>")

CSS = f"""
/* ══ MINIHRY NA BARU ══ */
.mc-bar{{position:relative;height:132px;overflow:hidden;background:{torn(131, DARK, Y)} center/100% 100% no-repeat;filter:drop-shadow(5px 6px 0 {R})}}
.mc-bar::before{{content:'';position:absolute;left:4%;right:4%;top:10%;height:40%;background:radial-gradient(rgba(255,212,0,.22) 1.4px,transparent 2px) 0 0/8px 8px}}
.mc-bar::after{{content:'';position:absolute;left:3%;right:3%;bottom:10%;height:26px;border:3px solid {INK};border-radius:6px;background:repeating-linear-gradient(90deg,#8B4A1C 0 38px,#A65A24 38px 40px),#8B4A1C;box-shadow:inset 0 5px 0 rgba(255,255,255,.25)}}
.mc-zone{{position:absolute;top:8%;bottom:8%;z-index:1;background:rgba(255,212,0,.28);border-left:3px dashed {Y};border-right:3px dashed {Y}}}
.mc-zone b{{position:absolute;left:50%;top:2px;transform:translateX(-50%);font:12px 'Titan One',sans-serif;color:{Y};text-shadow:1px 1px 0 {INK};letter-spacing:.06em}}
.mc-perf{{position:absolute;top:24%;bottom:8%;z-index:1;background:rgba(229,35,27,.55);box-shadow:0 0 0 2px {INK}}}
.mc-glass{{position:absolute;top:30px;left:0;z-index:2;width:52px;height:60px;margin-top:0;background:center/contain no-repeat;pointer-events:none;filter:drop-shadow(3px 3px 0 rgba(10,8,6,.6));will-change:transform,left}}
.mc-cocktail{{background-image:{COCKTAIL}}}
.mc-fire{{background-image:{FIRE};animation:mcfl .18s steps(2) infinite}}
@keyframes mcfl{{50%{{filter:drop-shadow(0 0 10px {O}) drop-shadow(3px 3px 0 rgba(10,8,6,.6))}}}}
.mc-btn{{font-family:'Titan One','Mali',sans-serif!important;display:flex!important;align-items:center!important;justify-content:center!important;min-height:80px;font-size:34px!important;text-transform:uppercase;touch-action:manipulation;-webkit-user-select:none;user-select:none;color:{INK}!important}}
.mc-btn:active{{transform:translate(3px,3px) scale(.98)!important}}
/* společné: štítky výsledků */
.game-root .mg-catch .mg-chip,.game-root .mg-mix .mg-chip{{background:{PAPER}!important;border:3px solid {INK}!important;border-radius:14px 22px 10px 24px / 20px 12px 22px 14px!important;color:{INK}!important;font-family:'Titan One','Mali',sans-serif;font-weight:400!important;box-shadow:3px 3px 0 {INK};animation:mgin .3s backwards}}
.game-root .mg-mix .mg-chip:nth-child(odd),.game-root .mg-catch .mg-chip:nth-child(odd){{transform:rotate(-2deg)}}
.game-root .mg-mix .mg-chip:nth-child(even),.game-root .mg-catch .mg-chip:nth-child(even){{transform:rotate(2deg)}}
""" + "".join(f".game-root .mg-mix .mg-chip:nth-child({k}),.game-root .mg-catch .mg-chip:nth-child({k}){{animation-delay:{(k - 1) * .09:.2f}s}}\n" for k in range(1, 9)) + f"""
@keyframes mgin{{from{{opacity:0;scale:.3}}}}
.game-root .mg-catch .mg-chips,.game-root .mg-mix .mg-chips{{justify-content:center;gap:10px!important}}
/* Denisa: recept na tabuli, suroviny jako samolepky, sklenice se plní */
.game-root .mg-mix .mg-chips{{padding:20px 18px;background:{torn(132, "#1d3b2a", Y)} center/100% 100% no-repeat;filter:drop-shadow(4px 5px 0 {INK})}}
.game-root .mg-mix .mg-chip{{font-size:15px!important;padding:8px 12px!important}}
.game-root .mg-mix .mg-chip span:first-child{{font-size:26px!important}}
.game-root .mg-mix .mg-grid{{gap:10px!important}}
.game-root .mg-mix .mg-grid .gb{{--bb:{PAPER};background:{PAPER}!important;border:3px solid {INK}!important;box-shadow:3px 4px 0 {INK}!important;min-height:76px!important;border-radius:20px 12px 22px 10px / 12px 22px 10px 20px!important}}
.game-root .mg-mix .mg-grid .gb:nth-child(3n){{transform:rotate(1.5deg)}}
.game-root .mg-mix .mg-grid .gb:nth-child(3n+1){{transform:rotate(-1.5deg)}}
.game-root .mg-mix .mg-grid .gb:hover{{background:{Y}!important;transform:translate(-2px,-2px)!important;box-shadow:5px 6px 0 {INK}!important}}
.game-root .mg-mix .mg-grid .gb:active{{transform:translate(2px,2px) scale(.95)!important;box-shadow:1px 1px 0 {INK}!important}}
.game-root .mg-mix .mg-grid .gb span:first-child{{font-size:34px!important}}
.game-root .mg-mix .mg-grid .gb span:last-child{{color:{INK}!important;font-family:'Titan One','Mali',sans-serif!important;font-weight:400!important}}
.mg-shaker{{align-self:center;display:flex;align-items:flex-end;gap:14px}}
.mg-cup{{position:relative;width:62px;height:82px;border:4px solid {INK};border-top:0;border-radius:0 0 16px 16px;background:rgba(255,255,255,.75);overflow:hidden;box-shadow:4px 4px 0 {R}}}
.mg-liq{{position:absolute;left:0;right:0;bottom:0;background:radial-gradient(rgba(255,255,255,.55) 1.6px,transparent 2.2px) 0 0/9px 11px,linear-gradient({O},{R});transition:height .35s cubic-bezier(.2,1.5,.5,1)}}
.mg-cup::after{{content:'';position:absolute;left:8px;top:6px;bottom:8px;width:5px;border-radius:3px;background:rgba(255,255,255,.7)}}
.mg-shaker b{{font:18px 'Titan One',sans-serif;color:{INK};padding:6px 12px;background:{torn(133, Y)} center/100% 100% no-repeat;filter:drop-shadow(2px 2px 0 {INK});transform:rotate(-3deg)}}
"""

CATCH_MARKUP = '''<div class="mc-bar">
            <div class="mc-zone" style="left:{{ mgZoneL }};width:{{ mgZoneW }}"><b>CHYŤ</b></div>
            <div class="mc-perf" style="left:{{ mgPerfL }};width:{{ mgPerfW }}"></div>
            <span ref="{{ glassRef }}" class="{{ mgGlassK }}"></span>
          </div>
          <button class="gp mc-btn" sc-camel-on-pointer-down="{{ catchTap }}" style="all:unset;cursor:pointer;border-radius:20px">Chyť!</button>'''

CATCH_JS = r"""  mkZone(r){const df=this.df,hw=Math.max(0.045,(0.12-r*0.016)/Math.sqrt(df));return {c:0.18+Math.random()*0.64,hw,per:Math.max(540,(1450-r*190)/df),fake:r>=1&&Math.random()<0.3};}
  cpos(t,per){if(t<0)return 0;const f=(t%per)/per;return f<0.5?f*2:2-f*2;}
  startCatch(){const s=this.state;if(s.dancing||s.m<s.catchCd)return;const z=this.mkZone(0);this.c={t0:performance.now()+800,res:[],z};this.setState({mg:{type:'catch',ph:'play',res:[],z,fb:'Martina se napřahuje…',q:-1}});}
  frameCatch(){const g=this.state.mg;if(!g||g.type!=='catch'||g.ph!=='play'||!this.c)return;const el=this.glassRef.current;if(!el)return;const t=performance.now()-this.c.t0,z=this.c.z,h=z.per/2,f=t<0?0:(t%h)/h;
    el.style.left=(this.cpos(t,z.per)*100).toFixed(2)+'%';el.style.transform='translate(-50%,'+(-Math.sin(Math.PI*f)*24).toFixed(1)+'px) rotate('+(z.fake?0:Math.round(t*0.4)%360)+'deg)';
    if(z.fake&&t>z.per*1.6)this.catchRes(2,pick(CATCH_FAKE_OK));}
  catchTap(e){if(e&&e.preventDefault)e.preventDefault();const g=this.state.mg;if(!g||g.type!=='catch'||g.ph!=='play'||!this.c)return;
    const t=performance.now()-this.c.t0;if(t<0)return;const z=this.c.z;if(z.fake){this.catchRes(0,pick(CATCH_FAKE_BAD));return;}
    const d=Math.abs(this.cpos(t,z.per)-z.c),q=d<=z.hw*0.35?2:d<=z.hw?1:0;this.catchRes(q,pick(CATCH_FB[q]));}
  catchRes(q,fb){const g=this.state.mg;if(!g||!this.c)return;const res=[...this.c.res,q];
    if(res.length>=5){const per=res.filter(x=>x===2).length,hit=res.filter(x=>x>0).length;this.c=null;
      const txt=hit===5&&per>=3?'Martina: „Ty bys mohl dělat flair bartendera. Nebo žonglovat v cirkuse.“':hit>=3?'Martina ti hodila plechovku Red Bullu. Tu jsi chytil taky. Energie zdarma.':hit>=1?'Martina: „No… aspoň sis nerozbil nos.“':'Pět rozbitých sklenic. Péťa ti je strhne z výplaty, kterou ani nemáš. −100 Kč';
      this.setState(x=>({mg:Object.assign({},g,{ph:'done',res,fb,q,per,hit,txt}),catchOK:x.catchOK+per,catchCd:x.m+25}));return;}
    const nz=this.mkZone(res.length);this.c={t0:performance.now()+700,res,z:nz};this.setState({mg:Object.assign({},g,{res,z:nz,fb,q})});}
"""

CONSTS = r"""
const CATCH_FAKE_OK=['Hořící panák jsi nechal letět. Trefil Pepu. Pepa nic neřekl. To je horší.','Hořící panák proletěl kolem. Martina: „Reflexy dobrý, mozek taky.“','Nechytils to. Správně. Péťa teď hasí bar Red Bullem.'],CATCH_FAKE_BAD=['Chytil jsi hořící panák. Au. AU. Martina: „Tys neviděl ten oheň?“','Hořící panák v ruce. Obočí máš teď jen jedno.','Chytil jsi oheň. Kevin z WC: „To je tak nefér, já to chtěl zkusit!“'];"""


def patch(s):
    def rep(old, new, cnt=1):
        nonlocal s
        assert old in s, "minig: nenalezeno " + old[:70]
        s = s.replace(old, new, cnt)

    # obsah: víc surovin, nové drinky a hlášky
    i = s.index("const ING=[")
    j = s.index("];", i) + 2
    s = s[:i] + ("const ING=[['🍋','Limetka'],['🧊','Led'],['🌿','Máta'],['🍸','Gin'],['🥃','Rum'],['🍊','Pomeranč'],['🍒','Višeň'],['🥤','Tonic'],"
                 "['🌶️','Chilli'],['🥒','Okurka'],['🫒','Oliva'],['🍯','Med']];") + s[j:]
    rep("'Pondělí neexistuje','Ještě jedno a jdem'];", "'Pondělí neexistuje','Ještě jedno a jdem','Vodka do oka','Big Girl Spritz','Zašprclej Colada','Tragédův tonic','Mrd dlužím vám'];")
    rep("Ty: „To bylo mojito?“ Denisa: „Už ne.“'];", "Ty: „To bylo mojito?“ Denisa: „Už ne.“','Denisa ochutnala: „Tohle by pil jen Tragéd. Do oka.“','„Med a chilli? Tos viděl v nějakým filmu? Ve špatným?“'];")
    rep("Martina: „To nebylo těžký.“'];", "Martina: „To nebylo těžký.“','„Pumping. Baleárskej. Perfektní.“ Denisa ti to poprvé za noc nenaúčtovala.'];")
    rep("'Martina: „Ty máš ruce z másla, nebo z Hery?“'],", "'Martina: „Ty máš ruce z másla, nebo z Hery?“','Sklenka ti proletěla mezi prsty jak Kevinovi holky.'],")
    rep("'Ninja. Martina se zamyslela, jestli tě nevzít na Ninja Warriora.']];", "'Ninja. Martina se zamyslela, jestli tě nevzít na Ninja Warriora.','Chytils to za stopku. Perry z WC tleská.']];" + CONSTS)

    # Martina – nová grafika + hořící panák (nechytat)
    i = s.index('<div class="gl" style="position:relative;height:84px;border-radius:16px;overflow:hidden">')
    j = s.index("Chyť!</button>", i) + len("Chyť!</button>")
    s = s[:i] + CATCH_MARKUP + s[j:]
    i = s.index("  mkZone(r){")
    j = s.index("this.setState({mg:Object.assign({},g,{res,z:nz,fb,q})});}", i) + len("this.setState({mg:Object.assign({},g,{res,z:nz,fb,q})});}")
    s = s[:i] + CATCH_JS.rstrip("\n") + s[j:]
    rep("mgD:'Sklenka letí po baru. Ťukni na CHYŤ, když je v zelené zóně. Růžový střed = perfekt.',mgCatch:true,",
        "mgD:'Martina hází po baru. Ťukni na CHYŤ, když je sklenka ve žluté zóně, červenej střed = perfekt. Hořící panák NECHYTEJ!',mgCatch:true,mgGlassK:'mc-glass '+(z.fake?'mc-fire':'mc-cocktail'),")

    # Denisa – tabule, samolepky, plnící se sklenice, zamíchaná mřížka, kratší ukázka
    rep("{type:'mix',ph:'show',rec,inp:[],name:pick(DRINKS)}", "{type:'mix',ph:'show',rec,inp:[],name:pick(DRINKS),ord:shuf(ING.map((_,i)=>i))}")
    rep("this.mgT=setTimeout(()=>this.mixGo(),1600+len*700);", "this.mgT=setTimeout(()=>this.mixGo(),1400+len*650);")
    rep("else if(g.ph==='input')Object.assign(v,{mgD:'Naklikej suroviny ve správném pořadí. '",
        "else if(g.ph==='input')Object.assign(v,{mgIsMixIn:true,mgFill:Math.round(g.inp.length/g.rec.length*100)+'%',mgD:'Naklikej suroviny ve správném pořadí. Denisa je mezitím přeházela, protože může. '")
    rep("mgGrid:ING.map(([e,l],i)=>({e,l,go:()=>this.mixTap(i)}))", "mgGrid:(g.ord||ING.map((_,i)=>i)).map(i=>({e:ING[i][0],l:ING[i][1],go:()=>this.mixTap(i)}))")

    # props + třídy v markupu
    rep("mgCatch:false,mgOpts:[],", "mgCatch:false,mgType:g?g.type:'',mgIsMixIn:false,mgFill:'0%',mgGlassK:'mc-glass mc-cocktail',mgOpts:[],")
    i = s.index('<sc-if value="{{ mgOn }}"')
    k = s.index('<div class="gls" style="width:min(520px,100%)', i)
    s = s[:k] + '<div class="gls mg-{{ mgType }}"' + s[k + len('<div class="gls"'):]
    rep('<sc-if value="{{ mgHasChips }}" hint-placeholder-val="{{ false }}"><div style="display:flex;flex-wrap:wrap;gap:6px">',
        '<sc-if value="{{ mgIsMixIn }}" hint-placeholder-val="{{ false }}"><div class="mg-shaker"><div class="mg-cup"><div class="mg-liq" style="height:{{ mgFill }}"></div></div><b>{{ mgFill }}</b></div></sc-if>\n'
        '        <sc-if value="{{ mgHasChips }}" hint-placeholder-val="{{ false }}"><div class="mg-chips" style="display:flex;flex-wrap:wrap;gap:6px">')
    rep('<span style="display:flex;align-items:center;gap:6px;padding:8px 10px;border-radius:10px;background:{{ c.bg }}',
        '<span class="mg-chip" style="display:flex;align-items:center;gap:6px;padding:8px 10px;border-radius:10px;background:{{ c.bg }}')
    rep('<div style="display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:8px">',
        '<div class="mg-grid" style="display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:8px">')

    i = s.index("</style>\n</helmet>")
    return s[:i] + CSS + s[i:]
