# Program nocí podle plakátů (10. 10. Narozeniny Landchi, 11. 10. Mazerlogy) + postavy ve stylu Lokál TV
# (art/lokal.py) jako obrázky DJů, Pepy a party za barem + tematické události jen pro danou noc (pole nt).
# Volá se z klub.patch() před tidy.patch().
import base64, json, pathlib, shutil, uuid

import lokal

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "src"
ASSETS = SRC / "assets"
UPL = pathlib.Path.home() / ".claude" / "uploads" / "cbdf7a4c-956d-492e-8e0a-a523e132f5ac"
POSTERS = {"20261010": UPL / "73895a7e-image.jpg", "20261011": UPL / "7e2cbb64-image.jpg"}
# pozadí karet v paletě černá–bílá–zlatá
BGS = ["#F2A93B", "#8FBFB6", "#F6EFDC"]

# jméno DJe na plakátu → id postavy v lokal.CHARS (= id v ext_resources) a cesta uploads/…
DJS = {
    "Enrico": ("djEnrico", "uploads/dj-enrico.svg"), "Tommy Rogers": ("djTommy", "uploads/dj-tommy.svg"),
    "Rio": ("dj_rio", "uploads/dj-rio.svg"), "Carl Cross": ("dj_carl_cross", "uploads/dj-carl-cross.svg"),
    "Richie": ("dj_richie", "uploads/dj-richie.svg"), "Jose Madeira": ("dj_jose_madeira", "uploads/dj-jose-madeira.svg"),
    "Yan Lan": ("dj_yan_lan", "uploads/dj-yan-lan.svg"), "Manuel Garcia": ("dj_manuel_garcia", "uploads/dj-manuel-garcia.svg"),
    "Jack Dorman": ("dj_jack_dorman", "uploads/dj-jack-dorman.svg"), "Terran": ("dj_terran", "uploads/dj-terran.svg"),
    "Jumbo": ("dj_jumbo", "uploads/dj-jumbo.svg"), "Cobra": ("dj_cobra", "uploads/dj-cobra.svg"),
    "Mark Evill": ("dj_mark_evill", "uploads/dj-mark-evill.svg"), "Landchi": ("dj_landchi", "uploads/dj-landchi.svg"),
    "Yoppa Parrot": ("dj_yoppa_parrot", "uploads/dj-yoppa-parrot.svg"), "Em.dot": ("dj_em_dot", "uploads/dj-em-dot.svg"),
    "Peet V": ("dj_peet_v", "uploads/dj-peet-v.svg"), "Calvin West": ("dj_calvin_west", "uploads/dj-calvin-west.svg"),
    "Mazer": ("dj_mazer", "uploads/dj-mazer.svg"), "Jerome Levis": ("dj_jerome_levis", "uploads/dj-jerome-levis.svg"),
    "Mike Frost": ("dj_mike_frost", "uploads/dj-mike-frost.svg"),
}

PROGRAM = r"""
  '2026-10-10':{t:'Sobota 10.10. · Narozeniny Landchi',p:'20261010',l:[['02:54','Mark Evill'],['06:00','Landchi'],['07:30','Rio'],['09:00','Yoppa Parrot'],['10:30','Em.dot'],['12:00','Peet V']]},
  '2026-10-11':{t:'Neděle 11.10. · Mazerlogy',p:'20261011',l:[['02:54','Calvin West'],['06:00','Mazer'],['08:00','Jerome Levis'],['10:00','Mike Frost'],['12:00','Terran']]}"""

EV_NIGHT = r"""
  {t:'Yabba dabba doo!',nt:'20261010',loc:'parket',d:'Přes parket se valí Landchi v oranžovým Flintstoneově kostýmu s černejma flekama, nafukovacím kyjem nad hlavou a chlupatejma nohama z gumy. Řve: „YABBA DABBA DOO!“ a čeká, kdo odpoví.',o:[['Zařvat „YABBA DABBA DOO!“',{vibe:14,rep:1},'Celej klub řve s váma. Landchi tě poklepal kyjem po hlavě. Pasování na pračlověka. +nálada'],['Uhnout kyji (risk)',{ch:0.5,ok:[{vibe:6},'Kyj proletěl kolem tvý hlavy a trefil Pepu. Pepa se usmál. Poprvé od roku 2004. +nálada'],ko:[{vibe:-6,en:-6},'Nafukovací kyj je překvapivě tvrdej. Vidíš hvězdičky a jednoho brontosaura. −energie']}]]},
  {t:'Dort pro Landchiho',nt:'20261010',loc:'bar',d:'Péťa vytáhl zpod baru narozeninovej dort ve tvaru brontosauřího žebra. „Doneseš ho k pultu? Já nemůžu, točím.“ Cesta vede přes celej parket.',o:[['Nést dort (risk)',{ch:0.5,ok:[{rep:3,vibe:10},'Prošel jsi parketem jak číšník v Ritzu. Landchi brečí štěstím, DJ pult je od šlehačky. +3 reputace'],ko:[{rep:-2,vibe:-6,cash:-100},'Zakopl jsi o chlupatou nohu z kostýmu. Dort přistál na Pepovi. Pepa teď vypadá jako svatební dort. −2 reputace']}],['Ochutnat a říct, že to byl Kevin',{en:12,rep:-1},'Krém je výbornej. Kevin to popírá. Nikdo mu nevěří. Tobě taky ne. −reputace']]},
  {t:'Wilma hledá Freda',nt:'20261010',d:'Holka v bílých šatech a s kostí ve vlasech tě chytla za rameno: „Neviděls Freda? Velkej, oranžovej, má kyj a je mu dneska o rok víc.“',o:[['Ukázat k DJ pultu',{rep:1,vibe:6},'Wilma doběhla k pultu a zařvala: „FREDÍÍÍ!“ Landchi zařval zpátky. Romantika z doby kamenný. +nálada'],['„Já jsem Fred.“',{vibe:4,min:4},'Wilma si tě prohlídla od hlavy k patě: „Málo oranžovej.“ Odešla. Upřímně, měla pravdu.']]},
  {t:'Chlupatá noha',nt:'20261010',loc:'wc',d:'Na zemi u záchodů leží gumová chlupatá noha z kostýmu. Pravá. Kevin s Perrym do ní šťouchají a tvrdí, že je to pravěkej artefakt.',o:[['Vrátit ji Landchimu',{rep:2,min:6},'Landchi si ji nasadil zpátky: „Bez ní jsem jen chlap v oranžovým pyžamu.“ +2 reputace'],['Prodat ji Kevinovi',{cash:150,rep:-1},'Kevin dal 150 Kč za „artefakt na Ibizu“. Perry už ji má na hlavě. +150 Kč, −reputace']]},
  {t:'Hodně štěstí ve frontě',nt:'20261010',loc:'wc',d:'Někdo ve frontě na záchod začal zpívat „Hodně štěstí, zdraví“. Přidává se celá fronta. Landchi tu vůbec není, ale nikoho to nezastaví.',o:[['Zpívat druhej hlas',{vibe:10,min:3},'Fronta zní jako sbor. Paní uklízečka si utírá slzu. Mopem. +nálada'],['Využít zmatek a předběhnout (risk)',{ch:0.45,ok:[{pee:-40,min:1},'Zatímco ostatní zpívali, ty jsi byl uvnitř. Narozeninovej zázrak. −měchýř'],ko:[{rep:-2,min:6},'Fronta přestala zpívat a začala koukat. Na tebe. Celá. Vrátil ses na konec. −2 reputace']}]]},
  {t:'Mark Evill',nt:'20261010',loc:'dj',d:'Mark Evill hraje tak temně, že i barmanky ztlumily světla. Chlápek vedle tebe šeptá: „Říká se, že ten druhej L v Evill je navíc, aby to bylo dvakrát zlý.“',o:[['Headbangovat na house',{vibe:12,en:-6},'Netušíš, jestli se na house headbanguje. Teď už jo. Mark Evill na tebe ukázal. +nálada'],['Zeptat se ho, proč dvě L (risk)',{ch:0.4,ok:[{rep:2},'Mark: „Jedno je na začátek noci, druhý na konec.“ Nedává to smysl a stejně je to nejlepší odpověď. +2 reputace'],ko:[{vibe:-6},'Mark Evill se na tebe podíval tak zle, že jsi zapomněl, jak se jmenuješ. −nálada']}]]},
  {t:'Papoušek',nt:'20261010',d:'Chlápek se zeleným číro opakuje všechno, co řekneš. „Ahoj.“ — „Ahoj.“ „Přestaň.“ — „Přestaň.“ Tvrdí, že je největší fanoušek Yoppa Parrota.',o:[['Naučit ho „Ještě jedno a jdem“',{vibe:10},'Teď to opakuje celou noc. Lidi se přidávají. Nikdo nejde. +nálada'],['Odejít',{min:2},'„Odejít,“ řekl papoušek. A šel za tebou. Až na záchod.']]},
  {t:'Em.dot a tečka',nt:'20261010',late:1,d:'Na zrcadle u baru je rtěnkou napsaný „.“ Barmanka Denisa: „To je podpis Em.dot. Tečka znamená konec věty. Ne konec afteru.“',o:[['Připsat za tečku „ještě jedno“',{vibe:8,rep:1},'Em.dot to viděla a přikreslila smajlíka. Máš autogram, i když jinej, než sis myslel. +nálada'],['Uklidit to',{rep:-1,cash:50},'Péťa ti dal padesátku. Em.dot ti dala pohled, kterej se nedá vyprat. −reputace']]},

  {t:'Krotitel bubnů',nt:'20261011',loc:'parket',d:'Uprostřed parketu sedí chlap v kovbojským klobouku s kozí bradkou a mlátí do bonga, až se třese zrcadlová koule. Josef Rafael. Tančí u toho o sto šest a kývne na tebe: „Zkusíš?“',o:[['Bubnovat s ním (risk)',{ch:0.45,ok:[{vibe:16,rep:2},'Trefil ses do rytmu. Josef zařval „ÓLE!“ a Mazer to pustil do mixu. Jsi v setu. +2 reputace'],ko:[{vibe:-6,rep:-1},'Bubnuješ jak pračka na odstřeďování. Josef ti jemně vzal ruce z bonga a vrátil ti je. −nálada']}],['Tančit kolem bonga',{vibe:10,en:-5},'Tancuješ kolem něj jak kolem táboráku. Josef bubnuje rychleji. Ty taky. Je to závod. +nálada']]},
  {t:'Ztracenej klobouk',nt:'20261011',d:'Na baru leží velkej slaměnej kovbojskej klobouk. Josef Rafael bez něj bubnuje jen na polovic. Všichni to vidí.',o:[['Vrátit ho Josefovi',{rep:2,vibe:6,min:4},'Josef si ho narazil na hlavu a zahrál ti sólo. Jen pro tebe. Na bongo. Zbytek klubu žárlí. +2 reputace'],['Chvíli ho nosit',{vibe:10,rep:-1},'V klobouku vypadáš jak šerif z Hybernský. Holky se otáčejí. Josef taky. Nelíbí se mu to. −reputace']]},
  {t:'Mazerlogy',nt:'20261011',loc:'dj',d:'Mazer hraje tech house tak hutnej, že ti basa přenastavuje tep. Na plakátu stojí „Mazerlogy“. Ptáš se sám sebe, jestli je to obor, a jestli se z toho dělají zkoušky.',o:[['Složit zkoušku z Mazerlogy',{vibe:14,en:-8},'Tancuješ s rukama nad hlavou celých čtyřicet minut. Titul Ing. v Mazerlogy uznávaj jen tady. Stačí to. +nálada'],['Zeptat se, co to znamená (risk)',{ch:0.5,ok:[{rep:2},'Mazer: „To je věda o tom, jak nejít domů.“ Zapsal sis to. Na ruku. Fixou. +2 reputace'],ko:[{vibe:-4},'Mazer ukázal na sluchátka. Neslyší tě. Nikdo tě neslyší. Je to tech house. −nálada']}]]},
  {t:'Calvin West',nt:'20261011',d:'Kluk u šatny se rozhlíží: „Calvin West už hraje? A kde je Calvin East? Myslel jsem, že jsou dva.“',o:[['„East hraje příští týden.“',{vibe:8},'Kluk si to poznamenal do kalendáře. Zklamání přijde za tejden. Dneska je šťastnej. +nálada'],['Vysvětlit mu to',{rep:1,min:4},'Vysvětlil jsi, že je jen jeden. Kluk je smutnej. Ale chytřejší. +reputace']]},
  {t:'Mike Frost',nt:'20261011',late:1,d:'Hraje Mike Frost a někdo pustil klimatizaci na maximum. Na zrcadlech je námraza, Denisa dává led do drinků zadarmo a Pepa poprvé v životě nosí šálu.',o:[['Zahřát se tancem',{vibe:12,en:-8},'Tancuješ, až se z tebe kouří. Doslova, je tu zima. +nálada'],['Schovat se k Josefovu bongu',{en:6,min:5},'Josef bubnuje tak rychle, že od bonga sálá teplo. Je to jediný topení v klubu. +energie']]},
  {t:'Jerome a džíny',nt:'20261011',d:'Ve frontě u baru se dva hádají, jestli má Jerome Levis na sobě džíny Levi’s. Jeden tvrdí, že by to byl střet zájmů. Druhej, že je to marketing.',o:[['Jít se podívat (risk)',{ch:0.5,ok:[{vibe:10,rep:1},'Džíny jsou z Lidlu. Oba prohráli. Ty jsi vyhrál zábavu na zbytek noci. +nálada'],ko:[{rep:-2,min:4},'Pepa tě chytil, jak čumíš DJovi na zadek. Vysvětluj to. Hodně dlouho. −2 reputace']}],['Vsadit se o pivo',{cash:-60,vibe:6},'Prohrál jsi. Nevíš ani jak. Pivo stálo šedesát. Zábava byla zdarma. −60 Kč']]}"""


def _svg(key, bg):
    c = lokal.CHARS[key]
    old = c.bg
    c.bg = bg
    c.n = 0
    try:
        return lokal.svg(c)
    finally:
        c.bg = old


def assets():
    """Zapíše SVG postav a plakáty do src/assets a zaregistruje je (idempotentní)."""
    idx = json.loads((SRC / "assets.json").read_text(encoding="utf-8"))
    ext = json.loads((SRC / "ext_resources.json").read_text(encoding="utf-8"))
    ids = {e["id"]: e["uuid"] for e in ext}
    bak = SRC / "assets-orig" / "prelokal"
    bak.mkdir(parents=True, exist_ok=True)

    def put(rid, data, ext_, mime):
        u = ids.get(rid) or str(uuid.uuid5(uuid.NAMESPACE_URL, "studio54/" + rid))
        f = ASSETS / f"{u}.{ext_}"
        if rid in ids and f.exists() and not (bak / f.name).exists():
            shutil.copy2(f, bak / f.name)
        f.write_bytes(data)
        idx[u] = {"file": f.name, "mime": mime}
        if rid not in ids:
            ext.append({"id": rid, "uuid": u})
            ids[rid] = u

    for i, (name, (rid, _)) in enumerate(DJS.items()):
        put(rid, _svg(rid, BGS[i % 3]).encode(), "svg", "image/svg+xml")
    put("pepa", _svg("pepa", "none").encode(), "svg", "image/svg+xml")
    from PIL import Image
    import io
    # komiksové logo (art/logo.html → art/logo54_comic.png, vykresleno playwrightem)
    lg = pathlib.Path(__file__).with_name("logo54_gta.png")  # logo z předlohy uživatele (vyříznuté)
    im = Image.open(lg).convert("RGBA")
    x0, y0, x1, y1 = im.getbbox()
    im = im.crop((max(0, x0 - 6), max(0, y0 - 6), min(im.width, x1 + 6), min(im.height, y1 + 6)))
    im.thumbnail((1100, 440), Image.LANCZOS)
    b = io.BytesIO()
    im.save(b, "WEBP", quality=90, method=6)
    put("logo54", b.getvalue(), "webp", "image/webp")
    for d, src in POSTERS.items():
        if not src.exists():
            raise FileNotFoundError(src)
        im = Image.open(src).convert("RGB")
        im.thumbnail((900, 1300))
        b = io.BytesIO()
        im.save(b, "WEBP", quality=84, method=6)
        put("poster" + d, b.getvalue(), "webp", "image/webp")
    (SRC / "assets.json").write_text(json.dumps(idx), encoding="utf-8")
    (SRC / "ext_resources.json").write_text(json.dumps(ext), encoding="utf-8")


def patch(s):
    assets()
    # žebříček: jen TOP 10, průběžné pořadí se obnovuje častěji (worker beze změny)
    assert s.count("lbView(s.lb).slice(0,20)") == 2
    s = s.replace("lbView(s.lb).slice(0,20)", "lbView(s.lb).slice(0,10)")
    s = s.replace("mgT:'Síň slávy'", "mgT:'TOP 10'")
    s = s.replace("rk<=20?'Top 20! Mamka", "rk<=10?'Top 10! Mamka")
    old_iv = "if(document.visibilityState==='visible')this.lbLoad();},45000);"
    assert old_iv in s
    s = s.replace(old_iv, "if(document.visibilityState==='visible')this.lbLoad();},20000);")
    # program nocí + výběr: dnešní, jinak nejbližší další, jinak poslední
    old = "'2026-10-04':{t:'Neděle 4.10. · Across the House',p:'20261004',l:[['02:54','Manuel Garcia'],['06:00','Jack Dorman'],['08:00','Terran'],['10:00','Jumbo'],['12:00','Cobra']]}"
    assert old in s
    s = s.replace(old, old + "," + PROGRAM, 1)
    old = "return PROGRAM[k]||(d.getDay()===0?PROGRAM['2026-10-04']:PROGRAM['2026-10-03']);"
    assert old in s
    s = s.replace(old, "const ks=Object.keys(PROGRAM).sort();return PROGRAM[k]||PROGRAM[ks.find(x=>x>=k)||ks[ks.length-1]];", 1)
    # portréty DJů
    i = s.index("const PORT={")
    j = s.index("};", i) + 2
    s = s[:i] + "const PORT={" + ",".join(f"'{n}':'{u}'" for n, (_, u) in DJS.items()) + ",'Esoj Ariedam':'uploads/dj-jose-madeira.svg'};" + s[j:]
    # mapování uploads/… → id zdroje
    old = '"uploads/poster-20261004.webp":"poster20261004",'
    assert old in s
    add = '"uploads/poster-20261010.webp":"poster20261010","uploads/poster-20261011.webp":"poster20261011",' + "".join(
        f'"{u}":"{rid}",' for n, (rid, u) in DJS.items() if f'"{u}"' not in s)
    s = s.replace(old, old + add, 1)
    # parta za barem v novém stylu
    i = s.index("const CREW_IMG={")
    j = s.index("};", i) + 2
    crew = {k: "data:image/svg+xml;base64," + base64.b64encode(_svg(k, BGS[n]).encode()).decode() for n, k in enumerate(("petya", "denisa", "martina"))}
    s = s[:i] + "const CREW_IMG={" + ",".join(f"{k}:'{v}'" for k, v in crew.items()) + "};" + s[j:]
    # události jen pro konkrétní noc
    old = "&&(!e.need||(s.fl||{})[e.need]);};"
    assert old in s
    s = s.replace(old, "&&(!e.need||(s.fl||{})[e.need])&&(!e.nt||e.nt===NIGHT.p);};", 1)
    i = s.index("const EV=[") + len("const EV=[")
    s = s[:i] + EV_NIGHT.strip() + ",\n  " + s[i:]
    return s
