# Obsah: Klub sráčů (Kevin & Perry Go Large) – vyhazuje paní Jarmilu a dědu Ludvu, přidává události/úkoly/hlášky.
# Spouštět místo pop.py:  python art/klub.py  (nejdřív aplikuje pop skin z template.pre-pop.html, pak obsah)
import pop

TPL = pop.TPL


def obj_span(s, title):
    """najde JS objekt {t:'title',...} a vrátí (start, end) – vyvažuje závorky, přeskakuje '…' řetězce"""
    i = s.index("{t:'" + title + "'")
    d, k = 0, i
    while True:
        c = s[k]
        if c == "'":
            k += 1
            while s[k] != "'":
                k += 2 if s[k] == "\\" else 1
        elif c in "{[(":
            d += 1
        elif c in "}])":
            d -= 1
            if d == 0:
                return i, k + 1
        k += 1


def put(s, title, new):
    a, b = obj_span(s, title)
    return s[:a] + new.strip() + s[b:]


def rep(s, old, new, n=1):
    assert s.count(old) >= 1, "nenalezeno: " + old[:80]
    return s.replace(old, new) if n == 0 else s.replace(old, new, n)


def after(s, anchor, add):
    """vloží text za konec objektu s titulkem anchor"""
    _, b = obj_span(s, anchor)
    return s[:b] + ",\n  " + add.strip() + s[b:]


def arr_append(s, decl, add):
    """přidá prvky na konec pole const X=[...];"""
    i = s.index(decl)
    j = s.index("];", i)
    return s[:j] + "," + add.strip() + s[j:]


# ─── úkoly Péti ───
Q_CANDICE = r'''
{t:'Candice a Gemma',d:'„Vidíš ty dvě u sloupu? Candice a Gemma. Chodí sem každou neděli a ještě nikdy se na nikoho nepodívaly. Lidi místo pití koukaj, jestli se na ně podívaj. Mně padaj tržby. Roztanči se tak, aby se otočily.“',goal:'Ať se Candice a Gemma otočí',n:1,v:s=>s.fl.ludva?1:0,r:{cash:200,rep:2,score:600},rt:'+200 Kč · +2 reputace · +600 bodů',
    act:(s,A,dj,me)=>s.fl.ludva?null:{loc:'parket',a:A('Roztančit se před Candice a Gemmou 💃',s.en<20?'potřeba energie 20+':'risk · čím víc nálady, tím líp · 8 min',()=>me.res({ch:Math.min(0.85,0.2+s.vibe/150),ok:[{vibe:12,rep:1,en:-10,min:8,set:'ludva'},'Udělal jsi „červa“ přes půl parketu. Candice se otočila. Gemma řekla: „Ujde.“ Na Ibize je to jako vyznání lásky.'],ko:[{en:-10,vibe:-6,min:8},'Celou dobu koukaly do telefonu. Pak si udělaly selfie. Ty jsi v pozadí a vypadáš jak Kevin. Zkus to znova s větší náladou.']}),s.en<20)}}'''

Q_VODKA = r'''
{t:'Vodka v oku',d:'„DJ za pultem viděl Klub sráčů a chtěl to zkusit. Nalil si vodku do oka. Teď vidí jen jedním a míchá to, jak kdyby hrál v autobuse. Perry na záchodech má lékárničku. Vyzvedni kapky a doruč je za pult, než pustí Macarenu.“',goal:'Vyzvedni kapky u Perryho na WC a doruč je DJovi',n:1,v:s=>s.fl.zubyOK?1:0,r:{cash:250,rep:2,score:600},rt:'+250 Kč · +2 reputace · +600 bodů',
    act:(s,A,dj,me)=>s.fl.zubyOK?null:!s.fl.zuby?{loc:'wc',a:A('Vyzvednout kapky u Perryho 💧','úkol Péti · 4 min',()=>me.apply({min:4,set:'zuby'},'Perry ti podal kapky: „Vodka do oka? Klasika. My jsme to zkoušeli s Kofolou. Nedoporučuju.“ Kevin: „Mně to nikdo nenabíd. To je tak nefér.“ Utíkej k pultu.'))}:{loc:'dj',a:A('Kápnout DJovi do oka 👁️','úkol Péti · 3 min',()=>me.apply({min:3,vibe:8,set:'zubyOK'},(dj||'DJ')+': „Vidím! Vidím barvy! Vidím… tebe. Jsi frajer.“ Ukázal ti palec a pustil drop, ze kterýho spadla omítka.'))}}'''

Q_BIGGIRL = r'''
{t:'Mix Big Girl',d:'„Kevin a Perry ze záchodů mi celou noc strkaj kazetu. Prej jejich mix. Jmenuje se Big Girl a je tam hlavně basa a někdo, kdo dejchá do mikrofonu. Vezmi ji, odnes DJovi a ukecej ho, ať to pustí. Když ne, aspoň mi přestanou brečet do kabinky.“',goal:'Vyzvedni mix na WC a ukecej DJe, ať ho pustí',n:1,v:s=>s.fl.bigOK?1:0,r:{cash:300,rep:2,score:700},rt:'+300 Kč · +2 reputace · +700 bodů',
    act:(s,A,dj,me)=>s.fl.bigOK?null:!s.fl.bigA?{loc:'wc',a:A('Vyzvednout mix od Kevina a Perryho 📼','úkol Péti · 3 min',()=>me.apply({min:3,set:'bigA'},'Kevin ti podal kazetu: „Jestli ji poškrábeš, nesnáším tě.“ Perry: „On tě nesnáší i tak. Běž.“'))}:{loc:'dj',a:A('Ukecat DJe, ať pustí Big Girl 📼','risk · čím víc reputace, tím líp · 5 min',()=>me.res({ch:Math.min(0.85,0.3+s.rep/12),ok:[{vibe:15,rep:1,min:5,set:'bigOK'},(dj||'DJ')+' to pustil. Basovej hlas řve „BIG GIRL!“ a celej klub skáče. Kevin s Perrym stojí ve dveřích záchodů a brečí si do ramene.'],ko:[{vibe:-5,min:5},(dj||'DJ')+': „Tohle? Tady je jen pípání a něčí máma volá k obědu.“ Zkus to znova, až tě tu budou víc znát (reputace).']}))}}'''

Q_IBIZA = r'''
{t:'Sbírka na Ibizu',d:'„Kevin a Perry šetřej na Ibizu od roku 2000. Mají 340 Kč a jednu ponožku. Hoď jim tři stovky, ať konečně vypadnou z mýho záchodu. Vrátím ti to. S úrokem. Jsem barman, ne banka, ale dneska jo.“',goal:'Přispěj Kevinovi a Perrymu 300 Kč na WC',n:1,v:s=>s.fl.ibiza?1:0,r:{cash:500,rep:2,score:600},rt:'+500 Kč · +2 reputace · +600 bodů',
    act:(s,A,dj,me)=>s.fl.ibiza?null:{loc:'wc',a:A('Přispět klukům na Ibizu ✈️','300 Kč · úkol Péti',()=>me.buy(300,{min:3,vibe:6,set:'ibiza'},'Perry počítá na prstech: „340 a 300… to je… hodně!“ Kevin: „Nejsem dojatej. Jen mám něco v oku.“ Doufejme, že ne vodku.'),s.cash<300)}}'''

# ─── nové události ───
EV_NEW = r'''
  {t:'Rodiče na kontrole',d:'Na schodech stojí cizí rodiče. Táta v sandálech s ponožkama ukazuje na tebe: „Nejste Kevin?“ Hledají syna, co jim tvrdil, že je na brigádě.',o:[['Ukázat na záchody',{rep:1,vibe:8},'Táta vběhl na WC: „KEVINE!“ Zevnitř se ozvalo: „TO JE TAK NEFÉR!“ Klub tleská. +nálada'],['„Kevin? Neznám.“',{min:3},'Táta si s tebou pro jistotu udělal selfie. Pošle ho mámě. Tvojí. Netušíš jak.']]},
  {t:'Vodka do oka',loc:'dj',d:'Chlápek u pultu tvrdí, že ví, jak to dělaj na Ibize. Vytáhl panáka vodky a míří si s ním do oka.',o:[['Zastavit ho',{rep:2,min:3},'Chytil jsi mu ruku na poslední chvíli. Vodka skončila na Pepovi. Pepa to vzal sportovně. Skoro. +2 reputace'],['Natočit to (risk)',{ch:0.4,ok:[{vibe:10,rep:1},'Video má 200 tisíc zhlédnutí. Chlápek vidí jedním okem, ale je slavnej. +nálada'],ko:[{vibe:-8,rep:-2},'Pepa viděl, že točíš místo pomoci. Teď točí on. Tebou. Ke dveřím. −2 reputace']}]]},
  {t:'Mix v kapse',loc:'dj',d:'V kapse ti chrastí CD s nápisem „MŮJ MIX – HREJ NAHLAS“. Nevíš, kdo ti ho tam dal. DJ je dva metry od tebe.',o:[['Strčit ho DJovi (risk)',{ch:0.45,ok:[{vibe:16,rep:2},'DJ to pustil a klub šílí. Mix je tvůj, i když nevíš, jak. Jsi Kevin, jen bez pupínků. +2 reputace'],ko:[{vibe:-8},'DJ si ho prohlídl a použil ho jako podtácek. Na jeho Red Bullu je teď tvoje jméno. −nálada']}],['Nechat si ho',{},'Doma zjistíš, že je to mix od Kevina a Perryho. Hodina pípání a „Big Girl“. Možná líp.']]},
  {t:'Ignorujou tě',loc:'parket',d:'Candice a Gemma tančí kousek od tebe. Ignorujou tě tak intenzivně, že to musí něco znamenat.',o:[['Ukázat svůj nejlepší krok (risk)',{ch:0.4,ok:[{vibe:14,rep:1},'Candice se otočila a řekla: „Ujde.“ Na Ibize je to jako vyznání lásky. +nálada'],ko:[{vibe:-8},'Pirueta skončila na sloupu. Gemma to natočila. Pro sebe. Do archivu. −nálada']}],['Tancovat dál po svým',{vibe:6},'Nevšímáš si jich. Najednou si všímaj ony tebe. Psychologie, kámo. +nálada']]},
  {t:'Kevin trucuje',loc:'wc',d:'Kevin sedí na schodech u záchodů a kouká do zdi. Mamka mu napsala „Kdy budeš doma, zlatíčko? 😘“ a on to omylem přečetl nahlas před celou frontou.',o:[['Utěšit ho',{rep:1,vibe:4,min:5},'Kevin: „Nejsem smutnej. Jen nesnáším všechny.“ Pak ti dal žvejku. Jste kámoši. +reputace'],['„Zlatíčko!“',{vibe:8,rep:-1},'Fronta řve smíchy. Kevin zabouchl kabinku: „NESNÁŠÍM TĚ!“ Upřímně? Zasloužený. −reputace']]},
  {t:'Big Girl!',d:'DJ pustil track, kde hlubokej hlas opakuje „Big Girl! Big Girl!“. Kevin a Perry vyběhli ze záchodů a tančí, jako by to byla jejich hymna.',o:[['Přidat se ke klukům',{vibe:14,en:-6},'Tancujete ve třech. Perry dělá rukama něco, co se v televizi rozmazává. Pepa zavírá oči. +nálada'],['Dělat, že je neznáš',{rep:1},'Kevin: „Ty se za nás stydíš?! To je tak nefér!“ Pepa ti ale kývl. +reputace']]},
  {t:'Bordel po DJovi',loc:'dj',d:'Předchozí DJ nechal za pultem bordel jak Kevin v pokoji: tři Red Bully, půl pizzy, ponožku a jednu botu.',o:[['Uklidit to',{cash:200,rep:1,min:10,en:-5},'Péťa ti za to dal dvoustovku. Bota tu zůstává. Nikdo neví čí. Asi Perryho. +200 Kč'],['„To není moje bota.“',{vibe:-2},'Péťa: „Tady není nic ničí. Proto to uklízí ten, kdo se dívá.“ Díval ses.']]},
  {t:'Pěna jak na Ibize',loc:'parket',d:'Někdo pustil pěnovač. Po parketu se valí pěna jak na Ibize v roce 2000. Pepa neví, kdo to byl. Pepa to zjistí.',o:[['Skočit do pěny',{vibe:16,en:-8},'Jsi celej bílej a šťastnej. Jako Perry, když poprvé uviděl moře. +16 nálada'],['Nahlásit to Pepovi',{rep:2,vibe:-4},'Pepa to vypnul. Lidi tě nesnáší, Pepa tě má rád. Vyber si. +2 reputace']]},
  {t:'Ibiza pozdravuje',d:'Perry chodí po klubu s kloboukem: „Sbírka na Ibizu! Každá koruna je krok k bazénu!“ V klobouku je 40 Kč a lístek na tramvaj.',o:[['Hodit tam stovku',{cash:-100,rep:1,vibe:6},'Perry tě objal a Kevin řekl, že tě nesnáší o trochu míň. Pokrok. +reputace'],['„Na Ibizu? V říjnu?“',{vibe:-3},'Perry zbledl. Tohle mu nikdo neřekl. Kevin: „Já to věděl. To je tak nefér.“']]},
  {t:'Tragéd tě zkouší',loc:'dj',d:'Za pult se postavil DJ Paul Bulva. Kevin a Perry mu říkaj Tragéd. Zabodl do tebe prst: „Jsi DJ, brácho? House nebo Garage? Acid nebo pumping? Baleárský nebo komerční? Sash, nebo Chicane?“',o:[['Odpovídat sebevědomě (risk)',{ch:0.5,ok:[{rep:2,vibe:8},'„House. Pumping. Baleárský. Sash.“ Tragéd kývl: „Konečně někdo, kdo není k hovnu.“ Dal ti panáka. Do ruky, ne do oka. +2 reputace'],ko:[{rep:-1,vibe:-8},'Na „Sash, nebo Chicane?“ jsi řekl „Chicane z Lidlu“. Tragéd: „ÁÁÁ, tyhle lháři jsou k hovnu!“ Smál se celej pult. −reputace']}],['„Já jsem tu jen pro vodu.“',{min:2},'Tragéd ztratil zájem dřív, než jsi dořekl „vodu“. Upřímnost tě zachránila.']]},
  {t:'Jsem zašprclej!',loc:'parket',d:'Kolem tebe právě protančily Candice a Gemma. Perry vedle tebe zbledl, pak zrudl a zašeptal: „Jsem zašprclej!“',o:[['„Já taky. Jdem se zchladit.“',{en:12,min:6,pee:-20},'Strčili jste hlavy pod kohoutek na WC. Perry: „Lepší než moře.“ Kevin z kabinky: „To je tak nefér, že jste mě nevzali!“ +energie'],['Tancovat dál, jako by nic',{vibe:8,rep:1},'Perry odběhl ke klimatizaci a stál tam dvacet minut s rukama nahoře. Ty jsi zatím zapůsobil. +nálada']]},
  {t:'Paní Pettersonová',d:'Do klubu přišla Kevinova máma, paní Pettersonová, zkontrolovat, jestli Kevin nepije. Perry si k ní přisedl a hlubokým hlasem pronesl: „Paní Pettersonová, vy rošťando…“',o:[['Odtáhnout Perryho',{rep:2,min:3},'Odtáhl jsi ho za límec. Kevin ti děkuje pohledem. Paní Pettersonová trochu zklamaně dopila gin. +2 reputace'],['Přidat se: „Sukni mou pozvednout!“',{vibe:12,rep:-2},'Paní Pettersonová se zasmála. Kevin se zhroutil na schodech. Pepa vás oba vyvedl na pět minut na čerstvej vzduch. +nálada, −2 reputace']]},
  {t:'Zrzavej chlup na mýdle',loc:'wc',d:'Na mýdle u umyvadla je zrzavej chlup. Kevin to uviděl a řve na celej suterén: „Tohle je nejhorší den mýho života! Já jsem adoptovanej!“ Utekl. Do kabinky č. 3.',o:[['Umejt si ruce i tak',{en:4,vibe:-4},'Čistý ruce, špinavá duše. Kevin z kabinky: „Jak můžeš?!“'],['Vyšetřit to s Pepou',{rep:1,min:3},'Pepa si chlup prohlídl proti světlu. „Péťa.“ Případ uzavřen. Péťa to popírá. +reputace']]},
  {t:'Neuznávám konvenční styly',d:'Kevin a Perry se převlékli do svítících neonových overalů. Pepa je chtěl vyhodit, ale Kevin na něj vystartoval: „Neuznávám konvenční styly v oblíkání!“',o:[['Pochválit jim outfit',{vibe:8,rep:1},'Perry: „Mrd dlužím vám!“ Nikdo neví, co to znamená. Za hodinu to říká celej klub. +nálada'],['Půjčit si svítící brejle',{vibe:12,en:-4},'Svítíš jak semafor na Hlaváku. Lidi se s tebou fotí jako s památkou. +nálada']]},
  {t:'Pěknej párek',d:'Pepa u vchodu zastavil Kevina a Perryho, co se vraceli z pauzy. Prohlídl si je od hlavy k patě a řekl jen: „Pěknej párek čůráků.“ Kevin kouká na tebe: „Řekni mu, že jsme s tebou!“',o:[['„Jsou se mnou.“',{rep:-1,vibe:10},'Pepa je pustil. Kevin ti řekl, že tě nesnáší o tři procenta míň. +nálada, −reputace'],['„Neznám je.“',{rep:1},'Kevin: „To je tak nefér!“ Za pět minut lezou dovnitř oknem na záchodech. Jako vždycky. +reputace']]},
  {t:'Trapnej táta',late:1,d:'Ve dveřích stojí táta jednoho kluka. Přišel ho vyzvednout a začal tančit tátovskej tanec. U toho tleská mimo rytmus. Jeho syn se schovává za tebe.',o:[['Krýt kluka',{rep:2,min:4},'Postavil ses před něj jak zeď. Táta odtancoval k baru a objednal si „něco, co pijou mladí“. Kluk ti dluží život. +2 reputace'],['Tančit s tátou',{vibe:12,rep:-1},'Táta tě naučil krok „sekačka na trávník“. Klub ho přijal. Syn emigruje. +nálada']]}'''

QP_NEW = r'''
  {q:'Jsi tu s kámošem?',o:[['Jo, s Perrym.',1,'Perry je na záchodech. Myje. Šetří na Ibizu. Pozdravuj ho.'],['Ne, sám. Jako vlk.',1,'Vlk v roláku. V říjnu. Dobře, vlku, běž.'],['Mamka mě sem hodila autem.',-1,'Mamka. Ať tě zase vyzvedne. Teď.']]},
  {q:'Co řekneš, když tě nepustím?',o:[['„To je tak nefér!“',0,'Znám jednoho Kevina. Taky to říkal. Taky nešel dovnitř.'],['Počkám, až budeš mít pauzu.',-1,'Já nemám pauzu. Já jsem pauza.'],['Poděkuju a přijdu příští neděli.',1,'Slušnost. To tu nevídám. Pojď dál.']]},
  {q:'Máš vlastní mix?',o:[['Jo, jmenuje se Big Girl.',1,'…Ten znám. Kevin mi ho pouští každou neděli. Pojď.'],['Mám playlist na Spotify.',0,'Playlist má i moje babička. Jsou tam Kabáti.'],['Jsem DJ. Jen to ještě nikdo neví.',1,'Tak to jsi tu správně. Tady nikdo neví nic o nikom.']]},
  {q:'Co uděláš, když tě DJ pozve za pult?',o:[['Na nic nesahám, jen kývu.',1,'Profík. Takových je málo.'],['Naleju si vodku do oka.',-1,'Klub sráčů jsem viděl taky. Nedělej to. Jdi domů.'],['Pustím Macarenu.',-1,'Ven. Okamžitě. A nevracej se.']]},
  {q:'Jsi DJ, brácho? House nebo Garage?',o:[['House.',1,'Acid nebo pumping? …Dělám si srandu. Pojď.'],['Garage. Mám tam kolo.',0,'Kolo nech venku. Tebe tam nechám chvíli taky.'],['Sash, nebo Chicane?',-1,'Odpovídáš otázkou? Tyhle lháři jsou k hovnu. Ven.']]},
  {q:'Proč vypadáš takhle?',o:[['Neuznávám konvenční styly v oblíkání!',1,'…Respekt. Kevin to říkal taky. Jeho jsem nepustil. Tebe jo.'],['Bylo to v akci.',0,'Bylo to v akci, protože to nikdo nechtěl.'],['Mamka mi to vybrala.',-1,'Mamka má vkus. Ty máš zákaz. Domů.']]},
  {q:'Kdyby ti DJ podal ruku, co řekneš?',o:[['„Mrd dlužím vám!“',1,'Nevím, co to znamená. Ale zní to jako heslo. Pojď.'],['„Podepíšeš mi triko?“',1,'Slušně. Dneska podepisujou všichni.'],['„Ukaž, jak se lije vodka do oka.“',-1,'Klub sráčů jsem viděl. Ty ho hraješ. Ven.']]}'''

Q_TRAGED = r'''
{t:'Zkouška u Tragéda',d:'„Na pult přišel Paul Bulva. Kluci mu říkaj Tragéd. Kdo neprojde jeho zkouškou ‚House nebo Garage‘, nesmí k pultu ani s vodou. Projdi to a Kevin s Perrym ti budou do smrti nosit tašky. Hlavně ať neřekneš Chicane.“',goal:'Projdi DJ zkouškou u Tragéda za pultem',n:1,v:s=>s.fl.tragedOK?1:0,r:{cash:250,rep:2,score:700},rt:'+250 Kč · +2 reputace · +700 bodů',
    act:(s,A,dj,me)=>s.fl.tragedOK?null:{loc:'dj',a:A('Projít zkouškou u Tragéda 🎧','risk · nálada i reputace pomáhají · 5 min',()=>me.res({ch:Math.min(0.85,0.25+s.vibe/150+s.rep/30),ok:[{vibe:10,rep:1,min:5,set:'tragedOK'},'„House. Pumping. Baleárský. Sash.“ Tragéd kývl: „Konečně někdo, kdo není k hovnu.“ Kevin a Perry za tebou stojí a nedýchají.'],ko:[{vibe:-6,min:5},'Na „Sash, nebo Chicane?“ jsi řekl „Chicane z Lidlu“. Tragéd: „ÁÁÁ, tyhle lháři jsou k hovnu!“ Zkus to znova, až budeš víc v náladě.']}))}}'''


def patch():
    pop.patch()
    s = TPL.read_text(encoding="utf-8")

    # ── WC: paní Jarmila → Kevin a Perry (brigádníci, šetří na Ibizu); kachna Kvido → sluchátka z bazaru ──
    s = rep(s, "zrcadlo, které pamatuje víc než Péťa, a u talířku paní Jarmila. Tady se rodí legendy. A fronty.",
            "zrcadlo, které pamatuje víc než Péťa, a u talířku Kevin a Perry – dva brigádníci, co si šetří na Ibizu. Tady se rodí legendy. A fronty.")
    s = rep(s, "Personální záchod. Teplá voda, ručník, voňavka. Paní Jarmila tě má ráda.",
            "Personální záchod. Teplá voda, ručník, voňavka a Perryho schovaný sušenky.")
    s = rep(s, "A('Paní Jarmila · dát dýško','20 Kč · něco se děje'", "A('Kevin a Perry · dát dýško','20 Kč · něco se děje'")
    s = rep(s, "this.say('Ani dvacku nemáš? Paní Jarmila se zklamaně dívá.')", "this.say('Ani dvacku nemáš? Kevin: „To je tak nefér!“')")
    s = rep(s, "toast:'Paní Jarmila: „Někdo mi ukrad Kvida. Gumovou kachnu. Sedí na talířku od roku 2004. Prej ji viděli u DJ pultu. Přines mi ho a nebudeš litovat.“'",
            "toast:'Kevin: „Někdo nám šlohnul DJ sluchátka! Z bazaru, za devadesát! Bez nich nebudem DJové na Ibize. To je tak nefér!“ Perry: „Prej jsou u DJ pultu.“'")
    s = rep(s, "A('Paní Jarmila · hledá Kvida','gumová kachna · zkus DJ pult',()=>this.say('Paní Jarmila: „Kvido. Žlutej. Jedno oko mu chybí. Ptej se u DJ pultu.“'))",
            "A('Kevin a Perry · hledají sluchátka','zkus DJ pult',()=>this.say('Perry: „Sluchátka. Růžový, jedno ucho drží izolepa. Ptej se u DJ pultu.“ Kevin: „Nesnáším vás. Všechny.“'))")
    s = rep(s, "A('Vrátit Kvida paní Jarmile 🦆'", "A('Vrátit sluchátka Kevinovi a Perrymu 🎧'")
    s = rep(s, "toast:'Paní Jarmila se rozbrečela. „Tady máš klíč od personálního. Bez fronty. Napořád. Nikomu ani slovo.“",
            "toast:'Kevin a Perry řvou jak na Ibize. Perry ti strčil klíč od personálního: „Bez fronty. Napořád. Jsme kámoši, jo?“ Kevin: „Nejsme. Ale jo.“")
    s = rep(s, "A('Pokecat s paní Jarmilou','20 Kč · drby ze záchodů'", "A('Pokecat s Kevinem a Perrym','20 Kč · drby ze záchodů'")
    s = rep(s, "'Paní Jarmila: '+pick(JARM)", "pick(JARM)")
    s = rep(s, "A('Zeptat se na kachnu Kvida','úkol paní Jarmily',()=>this.setState(x=>({jarm:2,m:x.m+4,rep:x.rep+1,toast:(dj||'DJ')+': „Kvido? Ten mi dělá maskota na pultu. Vrať ho paní Jarmile, mám ji rád.“ Máš Kvida! 🦆 Utíkej na WC.'",
            "A('Zeptat se na sluchátka Kevina a Perryho','úkol z WC',()=>this.setState(x=>({jarm:2,m:x.m+4,rep:x.rep+1,toast:(dj||'DJ')+': „Tyhle? Myslel jsem, že jsou z Lidlu. Vrať je klukům, ať jednou dojedou na Ibizu.“ Máš sluchátka! 🎧 Utíkej na WC.'")
    s = rep(s, "Fronta žere čas a paní Jarmila ví o všem.", "Fronta žere čas a Kevin s Perrym vědí o všem.")
    i = s.index("const JARM=[")
    j = s.index("];", i) + 2
    s = s[:i] + ("const JARM=['Perry: „Šetříme na Ibizu. Zatím máme 340 Kč a jednu ponožku.“',"
                 "'Kevin: „Táta mi ráno řekl, že mě má rád. Před kámošema! To je tak nefér!“',"
                 "'Perry: „Až budem DJové, budem mít vlastní bazén. A holky. A druhej bazén.“',"
                 "'Kevin: „Pepa nás nepustí na parket. Prej vypadáme jak dva sráči. Co je to za argument?!“',"
                 "'Perry: „Jednou jsme viděli DJe, co si nalil vodku do oka. Nejlepší den našeho života.“',"
                 "'Kevin: „Já nejsem naštvanej. Já jen nesnáším všechny a všechno. To je rozdíl.“',"
                 "'Perry: „Denisa se na mě dneska podívala. Teda na zeď za mnou. Ale já tam stál.“'];") + s[j:]

    # ── drobné zmínky Jarmila / Ludva v událostech ──
    for old, new in [
        ("Paní Jarmila tě vyhnala koštětem až ke schodům.", "Holky tě vyhnaly kabelkama až ke schodům."),
        ("['Zavolat paní Jarmilu',{rep:-1,vibe:-4,min:4},'Přišla s rolí a s pohledem, kterej nezapomeneš do smrti. „Dvacet let to dělám, chlapče.“']",
         "['Zavolat Perryho',{rep:-1,vibe:-4,min:4},'Přinesl roli a zašeptal: „Tohle nikomu neříkej. Já budu jednou DJ na Ibize.“ Pak ti ji hodil přes dveře. Do mísy.']"),
        ("vycouval do dámských. Paní Jarmila mlčí. Zatím.", "vycouval do dámských. Holky mlčí. Zatím."),
        ("Jinak by tu hrál Ludva z kazeťáku.", "Jinak by tu hrál Kevin z kazeťáku."),
        ("vrazil do Ludvy. Ludva se ani nehnul.", "vrazil do Pepy. Pepa se ani nehnul."),
        ("Paní Jarmila diriguje mopem.", "Perry diriguje štětkou."),
        ("Ukázal jsi mu kouli, Ludvu a paní Jarmilu.", "Ukázal jsi mu kouli, Pepu a Kevina s Perrym."),
        ("Předběhl jsi celou frontu a paní Jarmila to viděla.", "Předběhl jsi celou frontu. Kevin řval „to je tak nefér!“."),
        ("Paní Jarmila ti půjčila tepláky ze ztrát a nálezů.", "Perry ti půjčil tepláky ze ztrát a nálezů."),
        ("Paní Jarmila to viděla a mlčí. Zatím.", "Perry to viděl a mlčí. Za dýško."),
        ("Omlouval ses Ludvovi.", "Omlouval ses Pepovi."),
        ("Na fotce jsou tři lidi, sloup a Ludva.", "Na fotce jsou tři lidi, sloup a Kevin, co dělá rohy."),
        ("Ludva je na ní taky. Ludva je na každý fotce.", "Kevin s Perrym dělaj vzadu rohy. Jsou na každý fotce."),
        ("kdo ukradl Kvida,", "kdo šlohnul Kevinovi sluchátka,"),
        ("Asi zase paní Jarmila. Zajdi za ní, dej jí dýško a zjisti, co se děje. Ona ti to řekne. Mně nic neřekne, mě nemá ráda od roku 2011.",
         "Asi zase Kevin a Perry, naši brigádníci. Zajdi za nima, dej jim dýško a zjisti, co se děje. Mně nic neřeknou, prej jsem „trapnej starej chlap“. Je mi 29."),
        ("goal:'Promluv si s paní Jarmilou na WC'", "goal:'Promluv si s Kevinem a Perrym na WC'"),
    ]:
        s = rep(s, old, new)

    # Ludva → Kevinova kšiltovka, battle → Kevin a Perry
    s = put(s, "Děda Ludva vyzývá", r'''{t:'Kevin a Perry vyzývají',d:'Kevin a Perry vylezli ze záchodů a vyzvali tě na taneční battle. Mají nacvičenou choreografii z pokoje před zrcadlem. Perry má čelenku.',o:[['Přijmout battle (risk)',{ch:0.45,ok:[{vibe:16,rep:2,en:-8},'Kolem vás kruh, celej klub řve. Kevin: „To je tak nefér!“ Perry ti podal ruku: „Naučíš nás to?“ +2 reputace'],ko:[{vibe:-10,rep:-1,en:-10},'Perry udělal špagát. Kevin udělal hvězdu. Ty jsi zakopl o Perryho čelenku. −reputace']}],['Uznat porážku',{rep:1},'Kevin: „Jasně, že jsme lepší.“ Perry ti dal mentolku a pozval tě na Ibizu. Až budou mít víc než 340 Kč. +reputace']]}''')
    s = rep(s, "Uvnitř fixou: „Kdo mě najde, ten má štěstí. Ludva.“", "Uvnitř fixou: „KEVIN – IBIZA. NESAHAT. FAKT.“")
    s = rep(s, "Sedí jak ulitá. Cítíš se o 50 let starší a o 50 % lepší tanečník.", "Sedí jak ulitá. Cítíš se jako DJ na Ibize. Teda jako kluk, co chce bejt DJ na Ibize.")
    s = put(s, "Ludva chce kšiltovku", r'''{t:'Kevin chce kšiltovku',need:'cap',d:'Kevin tě zastavil uprostřed parketu a zírá na kšiltovku na tvý hlavě. „To je moje! Moje šťastná DJ kšiltovka! To je tak nefér!“',o:[['Vrátit ji',{rep:2,vibe:6},'Kevin tě objal, pak se zastyděl a řekl, že tě nesnáší. U Kevina je to nejvyšší forma díků. +2 reputace'],['„Kdo najde, ten má.“ (risk)',{ch:0.3,ok:[{vibe:12},'Kevin: „Fajn! Nech si ji! Stejně jsem ji nechtěl!“ A šel trucovat na WC. Kšiltovka je tvoje. +nálada'],ko:[{rep:-2,vibe:-8,min:10},'Kevin zavolal Pepu. Pepa zavolal Kevinovu mámu. Mamka přijela. Do klubu. V županu. −2 reputace']}]]}''')

    # ── úkoly ──
    s = put(s, "Ludvova výzva", Q_CANDICE)
    s = put(s, "Zubatá záhada", Q_VODKA)
    s = after(s, "Inspekce záchodů", Q_BIGGIRL)
    s = after(s, "Vodka v oku", Q_IBIZA)
    s = after(s, "Mix Big Girl", Q_TRAGED)

    # ── nové události, Pepovy otázky, drby, kvíz, Péťa ──
    i = s.index("const PEE_EV=")
    j = s.rindex("{t:'Nehoda na obzoru'", 0, i)
    s = s[:j] + EV_NEW.strip() + ",\n  " + s[j:]
    s = arr_append(s, "const DRBY=[",
                   "'Kevin a Perry ze záchodů šetřej na Ibizu od roku 2000. Mají 340 Kč.',"
                   "'Jeden DJ si tu prej nalil vodku do oka. Pepa mu pak nalil vodu do druhýho. Pro rovnováhu.',"
                   "'Pepa viděl Klub sráčů čtyřicetkrát. Na vrátnýho z Amnesie kouká jako na učitele.',"
                   "'Candice a Gemma sem choděj každou neděli a ještě nikdy s nikým nepromluvily. Je to jejich koníček.',"
                   "'Kevin tvrdí, že je adoptovanej. Kvůli zrzavýmu chlupu na mýdle. Doma.',"
                   "'Perry říká Kevinově mámě „vy rošťando“. Kevin to nese hodně špatně.',"
                   "'DJovi Paulu Bulvovi kluci říkaj Tragéd. Na Ibize prej na lodi… radši se neptej. Kevin od tý doby neplave.'")
    s = arr_append(s, "const WC_Q=[",
                   "\n  [{vibe:5},'Z vedlejší kabinky slyšíš Kevina do telefonu: „Mami, já jsem v knihovně!“ Fronta zadržuje smích. +nálada'],"
                   "\n  [{vibe:4},'Na zdi kabinky fixou: „Já bych š…, až bych pukal! – K.“ Pod tím jiným písmem: „Nepukneš. – P.“ +nálada']")
    s = arr_append(s, "const QUIZ=[",
                   "\n  {q:'Co nedělat s vodkou?',a:[['Lít si ji do oka',1],['Pít ji s Red Bullem',0],['Dávat ji Pepovi',0]]},"
                   "\n  {q:'Jak se jmenuje mix Kevina a Perryho?',a:[['Big Girl',1],['Small Boy',0],['Mamka volá',0]]},"
                   "\n  {q:'Co říká Kevin, když mu něco nevyjde?',a:[['To je tak nefér!',1],['Díky, mami',0],['Ještě jedno a jdem',0]]},"
                   "\n  {q:'Co křičí Tragéd na falešný DJe?',a:[['Tyhle lháři jsou k hovnu!',1],['Mrd dlužím vám!',0],['Jsem zašprclej!',0]]},"
                   "\n  {q:'Co znamená „Mrd dlužím vám“?',a:[['Díky moc',1],['Dlužím ti peníze',0],['Nikdo neví, ale zní to dobře',0]]}")
    s = arr_append(s, "const PETYA_DONE=[", "'„Mrd dlužím vám! Teda… díky moc. Kevin mě to naučil.“'")
    s = arr_append(s, "const PETYA_DONE=[", "'„Tohle nedal ani Kevin s Perrym. A ti šetřej na Ibizu od roku 2000.“'")
    s = arr_append(s, "const PETYA_QUIT=[", "'„To je tak nefér? Ne, Kevine. To je fér.“'")

    for w in ("Jarmil", "Ludv", "Kvid"):
        assert w not in s, "zbylo: " + w
    import dance, pepa, minig, comic, tidy, nights, sa, slim, fix3, fix4, fix5, fix6, fix7
    s = dance.patch(s)
    s = minig.patch(s)
    s = comic.patch(s)
    s = pepa.patch(s)
    s = nights.patch(s)
    s = tidy.patch(s)
    s = sa.patch(s)
    s = slim.patch(s)
    s = fix3.patch(s)
    s = fix4.patch(s)
    s = fix5.patch(s)
    s = fix6.patch(s)
    s = fix7.patch(s)
    TPL.write_text(s, encoding="utf-8")
    print("Klub sráčů: hotovo")


if __name__ == "__main__":
    patch()
