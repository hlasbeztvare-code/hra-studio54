# Tanec 16 dob: místo kruhů komiksový tanečník (pózy podle zásahů) + pás s hvězdami do terče.
# Volá se z klub.patch() (po pop skinu a obsahu).
from pop import uri, INK, Y, R, O, PAPER
from pop_shapes import torn, burstbox, DARK

SKIN, BLUE = "#F6C29A", "#1E88E5"
SH = {"L": (78, 92), "R": (122, 92)}
HIP = {"L": (90, 166), "R": (110, 166)}
# (loket, ruka) pro levou/pravou ruku, (koleno, chodidlo) pro nohy
POSES = [
    dict(la=((58, 62), (64, 24)), ra=((142, 62), (136, 24)), ll=((80, 204), (72, 246)), rl=((120, 204), (128, 246))),   # Sash! ruce nahoru
    dict(la=((58, 112), (42, 134)), ra=((150, 70), (180, 36)), ll=((76, 202), (60, 242)), rl=((124, 206), (126, 248))),  # disco ukazovák
    dict(la=((50, 94), (50, 62)), ra=((150, 94), (150, 126)), ll=((88, 206), (86, 248)), rl=((112, 206), (114, 248))),   # robot
    dict(la=((58, 112), (66, 142)), ra=((146, 106), (166, 128)), ll=((86, 206), (84, 248)), rl=((142, 184), (180, 196))),  # kop
    dict(la=((56, 78), (94, 30)), ra=((144, 78), (106, 30)), ll=((68, 202), (80, 246)), rl=((132, 202), (120, 246))),   # tleskání nad hlavou
    dict(la=((52, 70), (28, 46)), ra=((152, 122), (174, 152)), ll=((82, 208), (58, 236)), rl=((118, 196), (152, 220))),  # zakopnutí
]


def limb(a, b, c, col, w=11, sleeve=None):
    p = f"{a[0]},{a[1]} {b[0]},{b[1]} {c[0]},{c[1]}"
    s = (f"<polyline points='{p}' fill='none' stroke='{INK}' stroke-width='{w + 7}' stroke-linecap='round' stroke-linejoin='round'/>"
         f"<polyline points='{p}' fill='none' stroke='{col}' stroke-width='{w}' stroke-linecap='round' stroke-linejoin='round'/>")
    if sleeve:
        m = (a[0] + (b[0] - a[0]) * .45, a[1] + (b[1] - a[1]) * .45)
        s += f"<line x1='{a[0]}' y1='{a[1]}' x2='{m[0]:.0f}' y2='{m[1]:.0f}' stroke='{sleeve}' stroke-width='{w + 3}' stroke-linecap='round'/>"
    return s


def man(p, fall=False):
    o = ""
    for k in "LR":
        kn, ft = p["ll" if k == "L" else "rl"]
        o += limb(HIP[k], kn, ft, BLUE, 13)
        o += f"<ellipse cx='{ft[0] + (6 if k == 'R' else -6)}' cy='{ft[1]}' rx='15' ry='8' fill='{R}' stroke='{INK}' stroke-width='4'/>"
    o += f"<rect x='76' y='150' width='48' height='24' rx='8' fill='{BLUE}' stroke='{INK}' stroke-width='5'/>"
    o += f"<rect x='70' y='80' width='60' height='82' rx='20' fill='{Y}' stroke='{INK}' stroke-width='5'/>"
    o += f"<text x='100' y='134' text-anchor='middle' font-family='Arial Black,Arial' font-weight='900' font-size='28' fill='{R}' stroke='{INK}' stroke-width='1.5'>54</text>"
    for k in "LR":
        el, hd = p["la" if k == "L" else "ra"]
        o += limb(SH[k], el, hd, SKIN, 10, Y)
        o += f"<circle cx='{hd[0]}' cy='{hd[1]}' r='9' fill='{SKIN}' stroke='{INK}' stroke-width='4'/>"
    hx, hy = (96, 52) if fall else (100, 50)
    o += f"<g transform='rotate({-14 if fall else 0} {hx} {hy})'>"
    o += f"<polygon points='{hx-26},{hy-8} {hx-20},{hy-34} {hx-8},{hy-22} {hx},{hy-40} {hx+8},{hy-22} {hx+22},{hy-34} {hx+26},{hy-8}' fill='{INK}'/>"
    o += f"<circle cx='{hx}' cy='{hy}' r='26' fill='{SKIN}' stroke='{INK}' stroke-width='5'/>"
    o += f"<rect x='{hx-22}' y='{hy-10}' width='44' height='13' rx='5' fill='{INK}'/><line x1='{hx-14}' y1='{hy-6}' x2='{hx-8}' y2='{hy-6}' stroke='#fff' stroke-width='2.5' stroke-linecap='round'/>"
    o += (f"<ellipse cx='{hx}' cy='{hy+14}' rx='6' ry='7' fill='{INK}'/>" if fall else
          f"<path d='M{hx-11},{hy+10} Q{hx},{hy+22} {hx+11},{hy+10}' fill='{R}' stroke='{INK}' stroke-width='4' stroke-linejoin='round'/>")
    o += "</g>"
    if fall:
        o += f"<text x='160' y='40' font-family='Arial Black,Arial' font-weight='900' font-size='34' fill='{R}' stroke='{INK}' stroke-width='2'>?!</text>"
    return uri(f"<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 200 260'>{o}</svg>")


NOTE_C = [R, Y, BLUE, O]
CSS = f"""
/* ══ TANEC 16 DOB – komiksový tanečník + pás ══ */
.dz{{display:flex;flex-direction:column;align-items:center;gap:10px;cursor:pointer;touch-action:manipulation;-webkit-user-select:none;user-select:none;-webkit-tap-highlight-color:transparent}}
.dz-stage{{position:relative;width:220px;height:232px}}
.dz-stage::before{{content:'';position:absolute;left:-30px;top:-14px;width:280px;height:260px;background:{burstbox(21, Y)} center/100% 100% no-repeat;opacity:.95;filter:drop-shadow(5px 6px 0 {R});animation:dzspin 14s linear infinite;z-index:0}}
@keyframes dzspin{{to{{transform:rotate(360deg)}}}}
.dz-man{{position:absolute;left:25px;top:6px;width:170px;height:221px;background:center/contain no-repeat;transform-origin:50% 100%;z-index:1;filter:drop-shadow(4px 5px 0 rgba(10,8,6,.55))}}
""" + "".join(f".dz-p{i}{{background-image:{man(p, i == 5)}}}\n" for i, p in enumerate(POSES)) + f"""
.dz-fb{{position:absolute;right:-74px;top:-6px;z-index:2;min-width:96px;padding:26px 22px;text-align:center;background:{burstbox(22, PAPER)} center/100% 100% no-repeat;font-family:'Titan One','Mali',sans-serif;font-size:19px;line-height:1;text-transform:uppercase;filter:drop-shadow(4px 4px 0 {INK});transform:rotate(9deg);animation:dzpop .32s cubic-bezier(.2,1.6,.5,1)}}
@keyframes dzpop{{from{{transform:rotate(9deg) scale(.4)}}to{{transform:rotate(9deg) scale(1)}}}}
.dz-move{{max-width:min(420px,86vw);min-height:20px;padding:9px 18px 7px;background:{torn(123, Y)} center/100% 100% no-repeat;color:{INK};font-family:'Titan One','Mali',sans-serif;font-size:16px;text-align:center;text-transform:uppercase;filter:drop-shadow(3px 4px 0 {INK});transform:rotate(-1.5deg);animation:dzpop2 .3s ease-out}}
@keyframes dzpop2{{from{{transform:rotate(-1.5deg) scale(.85)}}}}
.dz-lane{{position:relative;width:min(440px,88vw);height:70px;background:{torn(124, DARK, Y)} center/100% 100% no-repeat;filter:drop-shadow(5px 6px 0 {R})}}
.dz-target{{position:absolute;left:20px;top:50%;width:52px;height:52px;margin-top:-26px;border:4px dashed {Y};border-radius:50%;box-shadow:0 0 0 3px {INK},inset 0 0 0 3px {INK}}}
.dz-target::after{{content:'ŤUK';position:absolute;left:50%;top:-16px;transform:translateX(-50%);font:12px 'Titan One',sans-serif;color:{Y};text-shadow:1px 1px 0 {INK}}}
.dz-notes{{position:absolute;inset:0;overflow:hidden;pointer-events:none}}
.dz-n{{position:absolute;left:0;top:50%;width:46px;height:46px;margin-top:-23px;display:flex;align-items:center;justify-content:center;font-style:normal;font-size:19px;background:center/100% 100% no-repeat;will-change:transform;transition:opacity .25s}}
""" + "".join(f".dz-n{k}{{background-image:{burstbox(40 + k, c)}}}\n" for k, c in enumerate(NOTE_C)) + """
.dz-n.q0{opacity:.15;filter:grayscale(1)}
.dz-n.q1,.dz-n.q2{opacity:0}
.dz-hint{padding:8px 16px!important;font-family:'Mali',sans-serif;font-weight:700;font-size:12px;letter-spacing:.05em;text-transform:uppercase;white-space:nowrap}
@media (max-height:760px){.dz-stage{transform:scale(.82);margin:-20px 0 -24px}}
"""

MARKUP = '''<div class="dz" sc-camel-on-pointer-down="{{ hit }}">
          <div class="dz-stage"><div ref="{{ ringRef }}" class="dz-man dz-p0"></div><div key="{{ fbKey }}" class="dz-fb" style="color:{{ fbc }}">{{ fb }}</div></div>
          <div key="{{ fbKey }}" class="dz-move">{{ moveTxt }}</div>
          <div class="dz-lane"><div class="dz-target"></div><div ref="{{ laneRef }}" class="dz-notes"></div></div>
          <span class="gl dz-hint">{{ beatTxt }} · {{ comboTxt }} · ťukni, až je hvězda v terči</span>
        </div>'''

CONSTS = r"""
const DZ_MOVES=['Sash! Ruce nahoru!','Kevinův trucovací krok','Perry na Ibize','Sekačka na trávník','Robot z Hlaváku','Hledání lístku od šatny','Baleárskej pumping','Zašprclej twist','Tátovskej tanec (ironicky)','Pepa kývl. Fakt kývl.','Moonwalk po rozlitým ginu','Candice se otočila!','Ruce jak na horský dráze','Péťa přestal točit pivo'],DZ_OK=['Ujde.','Skoro jako Perry','Rytmus cítíš. Trochu.','Gemma koukla. Možná.','Ještě jedno a jdem'],DZ_MISS=['Zakopl jsi o Perryho','Kevin: „To je tak nefér!“','Pepa se dívá…','Tragéd: „Lháři k hovnu!“','Rozlil jsi gin. Svůj.','Tancuješ jak na firemním večírku'],DZ_START=['Tragéd pouští beat…','House nebo Garage? Tancuj!','Kevin a Perry se dívají'],DZ_IC=['👐','🕺','💃','🤘'];"""

FRAME_OLD = "const r=this.ringRef.current;if(r){const f=((t%P)+P)%P/P,sc=1+1.6*(1-f);r.style.transform='scale('+sc.toFixed(3)+')';r.style.opacity=(0.25+0.75*f).toFixed(2);}"
FRAME_NEW = ("const r=this.ringRef.current;if(r){const f=((t%P)+P)%P/P,b=Math.max(0,1-f*3.5),ps=s.pose==null?0:s.pose;r.className='dz-man dz-p'+(ps<0?5:ps);"
             "r.style.transform=(ps<0?'rotate(-9deg) ':'')+'translateY('+(-b*12).toFixed(1)+'px) scale('+(1+b*.05).toFixed(3)+','+(1-b*.06).toFixed(3)+')';}"
             "const L=this.laneRef.current;if(L){if(L.childElementCount!==BEATS)L.innerHTML=Array.from({length:BEATS},(_,k)=>'<i class=\"dz-n dz-n'+(k%4)+'\">'+DZ_IC[k%4]+'</i>').join('');"
             "const W=L.clientWidth,TX=46,SP=(W-TX)/3.2;for(let k=0;k<BEATS;k++){const el=L.children[k],q=this.d.q[k],dt=((k+1)*P-t)/P;"
             "el.className='dz-n dz-n'+(k%4)+(q!=null?' q'+q:'');el.style.transform='translateX('+(TX-23+dt*SP).toFixed(1)+'px) rotate('+(dt*40).toFixed(0)+'deg)';el.style.visibility=dt>3.4||dt<-1?'hidden':'visible';}}")


def patch(s):
    def rep(old, new):
        nonlocal s
        assert old in s, "dance: nenalezeno " + old[:70]
        s = s.replace(old, new, 1)

    i = s.index('<button class="gl" sc-camel-on-pointer-down="{{ hit }}"')
    j = s.index("klikni, když se kruhy potkají</span>", i) + len("klikni, když se kruhy potkají</span>")
    s = s[:i] + MARKUP + s[j:]
    rep("const CLOSE=840, P=60000/126*2, BEATS=16;", "const CLOSE=840, P=60000/126*2, BEATS=16;" + CONSTS)
    rep("this.setState({dancing:true,combo:0,beat:0,fb:'Připrav se',fbc:'#F2F0EB'});}",
        "this.d.q={};this.setState({dancing:true,combo:0,beat:0,fb:'Jdem!',fbc:'#0a0806',pose:0,dmove:pick(DZ_START)});}")
    rep("this.d.j.add(k);this.judge(dl<P*0.1?2:dl<P*0.24?1:0);}",
        "this.d.j.add(k);const q=dl<P*0.1?2:dl<P*0.24?1:0;this.d.q[k]=q;this.judge(q);}")
    rep("if(!this.d.j.has(k)&&t>(k+1)*P+P*0.3){this.d.j.add(k);this.judge(0);}",
        "if(!this.d.j.has(k)&&t>(k+1)*P+P*0.3){this.d.j.add(k);this.d.q[k]=0;this.judge(0);}")
    rep("fb:['MIMO','DOBŘE','PERFEKT'][q],fbc:['#BDB7B0','#FFE08A','#E8B931'][q],",
        "fb:['ÁÁÁ!','DOBŘE!','PERFEKT!'][q],fbc:['#E5231B','#0a0806','#0a0806'][q],pose:q?(((s.pose==null||s.pose<0)?0:s.pose)+1+Math.floor(Math.random()*3))%5:-1,dmove:q===2?pick(DZ_MOVES):q===1?pick(DZ_OK):pick(DZ_MISS),")
    rep(FRAME_OLD, FRAME_NEW)
    rep("ringRef=React.createRef();", "ringRef=React.createRef(); laneRef=React.createRef();")
    rep("ringRef:this.ringRef,", "ringRef:this.ringRef, laneRef:this.laneRef, moveTxt:s.dmove||'', fbKey:String(s.beat)+String(s.fb),")
    i = s.index("</style>\n</helmet>")
    return s[:i] + CSS + s[i:]
