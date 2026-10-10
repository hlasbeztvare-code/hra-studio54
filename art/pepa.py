# Pepa u vstupu: těžší a vtipnější otázky (chytáky, lore ze hry), odpovědi se míchají.
# Volá se z klub.patch().

Q0 = r"""{q:'Dobrý ráno. Kam se tak řítíš?',o:[['Dovnitř. Na after.',0,'Řítit se? Tady se neřítí. Tady se stojí ve frontě a mlčí.'],['Nikam. Stojím ve frontě, Pepo.',1,'Správně. Frontu respektuješ. To je první lekce.'],['Za kámošem, je uvnitř.',-1,'„Kámoš je uvnitř“ je nejstarší výmluva od roku 2004. Ven z fronty.']]}"""

POOL = r"""
  {q:'Kolik je dvakrát „ještě jedno a jdem“?',o:[['Dvě.',-1,'Dvě? Ty jsi tu poprvé. Matiku si dodělej v pondělí. Doma.'],['Čtrnáct. Minimálně.',1,'Správně. Jedno „ještě jedno“ je sedm. Znáš místní měnu.'],['Záleží, kdo platí.',0,'Ekonom. Ale tady se počítá v litrech, ne v korunách.']]},
  {q:'Venku je osm ráno a ty máš sluneční brejle. Proč?',o:[['Protože svítí slunce.',0,'V osm ráno v Praze? To jsi naposled viděl v červnu.'],['Aby nebylo poznat, kolik jsem spal.',1,'Upřímnost. Brejle jsou na zakrývání pravdy, ne slunce.'],['Jaký brejle?',-1,'Ty, co máš na čele. Obráceně. Jdi se vyspat.']]},
  {q:'Kdybys stál na mým místě, pustil bys sám sebe?',o:[['Jasně, jsem v pohodě.',0,'To říká každej. Hlavně ti, co nepustím.'],['Asi ne. Ale ty jsi lepší člověk než já.',1,'…Tohle bolelo a zároveň potěšilo. Dobře.'],['Nepouštěl bych nikoho. Klub by byl můj.',-1,'Tak si běž otevřít vlastní. Tady jsem šéf já.']]},
  {q:'Co je těžší: kilo peří, nebo kilo železa?',o:[['Železo.',-1,'Tak si běž zvednout kilo železa. Domů.'],['Váží to stejně.',0,'Správně, ale nudně. Na afteru se počítá i styl.'],['Moje hlava v pondělí ráno.',1,'Odpověď afterkáře. Ta váží nejvíc. Pojď.']]},
  {q:'Kolik schodů vede dolů na parket?',o:[['Netuším. Počítám je až cestou nahoru.',1,'Upřímně. Nahoru jich je dvakrát víc, uvidíš.'],['Dvacet tři.',0,'Tipuješ, ale sebevědomě. To se tu cení napůl.'],['Žádný, jedu výtahem.',-1,'Výtah nemáme. Rozum asi taky ne. Ven.']]},
  {q:'Kámoš je uvnitř, ty venku a máš jeho občanku. Co uděláš?',o:[['Ukážu ti obě a řeknu, že jsme dvojčata.',-1,'On je blonďák s knírem, ty ne. Fronta se ti směje. Domů.'],['Řeknu ti to na rovinu a dám ti ji.',1,'Já nejsem pošťák. Ale nekecáš. Pojď a dej mu ji sám.'],['Nechám si ji. Bude mi dlužit.',0,'Obchodník. Nelíbí se mi to, ale chápu to.']]},
  {q:'Pustím tě, když uhodneš, co mám v kapse.',o:[['Mentolky.',1,'…Jak to víš? To je děsivý. Pojď, než o mně víš víc.'],['Seznam lidí, co nepustíš.',0,'Ten mám v hlavě. V kapse mám něco jinýho. Ale vtipný.'],['Klíče od klubu?',-1,'Klíče má Péťa. Já mám pravomoc. A ty smůlu.']]},
  {q:'Kterej DJ dneska zavírá?',o:[[LINEUP[LINEUP.length-1][1]+'.',1,'Víš, kdo zavírá. Takže plánuješ zůstat. To se mi líbí.'],[LINEUP[0][1]+'.',0,'Ten otvírá. Ty asi nespíš od pátku.'],['Já, když mě pustíš k pultu.',-1,'K pultu nepustím ani tebe, ani tvoje USBčko. Ven.']]},
  {q:'Co uděláš, když tě uvnitř budou dvě holky ignorovat?',o:[['Budu je ignorovat víc.',1,'Psychologická válka. Ty jsi ten typ, co vyhrává.'],['Pošlu jim drink.',0,'Pošlou ho zpátky. Ale aspoň Péťa vydělá.'],['Řeknu jim, že je to tak nefér!',-1,'Kevine, jsi to ty? Převlek ti nepomůže. Ven.']]},
  {q:'Acid nebo pumping? Baleárskej, nebo komerční? Sash, nebo Chicane?',o:[['Pumping. Baleárskej. Sash.',1,'Bez zaváhání. Tragéd by tě nevyhodil. Já taky ne.'],['Ano.',0,'„Ano“ na tři otázky. Politik. Projdeš, ale sleduju tě.'],['Chicane z Lidlu.',-1,'ÁÁÁ, tyhle lháři jsou k hovnu! Ven.']]},
  {q:'Proč vypadáš takhle?',o:[['Neuznávám konvenční styly v oblíkání!',1,'…Respekt. Kevin to říkal taky. Jeho jsem nepustil, tebe jo.'],['Bylo to v akci.',0,'Bylo to v akci, protože to nikdo nechtěl.'],['Mamka mi to vybrala.',-1,'Mamka má vkus. Ty máš zákaz. Domů.']]},
  {q:'Na kolik BPM se tu tancuje?',o:[['126.',1,'Přesně. Buď jsi tu byl, nebo máš metronom v srdci.'],['Na tolik, kolik vydrží srdce.',0,'Romantik. Kardiolog by nesouhlasil.'],['Co je BPM?',-1,'Beats per minute. A ty máš zákaz per today. Domů.']]},
  {q:'Rychle: jak se jmenuje moje zvíře?',o:[['Face Control.',1,'…Kočka. Ale jméno sedí. Drby od Martiny, co? Pojď.'],['Ty nemáš zvíře, Pepo.',0,'Mám. Kočku. Napůl jsi trefil, napůl ne.'],['Rex?',-1,'Rex je komisař. Ty jsi amatér. Ven.']]},
  {q:'Víš vůbec, kde stojíš?',o:[['Hybernská 38.',1,'Bystrej. To se tu cení víc než Rolex.'],['Ve frontě.',0,'Technicky pravda. Prakticky drzost. Projde to.'],['Na Hlaváku, ne?',-1,'Hlavák je o kus dál. Vlak ti jede za dvacet minut. Na něj běž.']]},
  {q:'Kdy jsi naposled spal?',o:[['V pátek. Myslím.',1,'Poctivej afterkář. Respekt.'],['Dneska ráno v tramvaji.',1,'Devítka? Tam spí všichni. I řidič.'],['Spát je pro slabochy.',-1,'Řekl ten, kdo mi právě zívnul do obličeje. Jdi spát.']]},
  {q:'Máš u sebe něco, co bych měl vědět?',o:[['Jen Red Bull a dobrou náladu.',1,'Red Bull je povolenej. Nálada taky. Zatím.'],['Mentolky. Chceš?',1,'…Dám si jednu. Ale nic to mezi náma neznamená.'],['A co bys chtěl vědět?',-1,'Tohle se mi nelíbí. Otoč se a jdi.']]},
  {q:'Co uděláš, když tě uvnitř někdo polije?',o:[['Zasměju se. Je after.',1,'Přesně. Tady se nikdo nepere, tady se tancuje.'],['Poleju ho zpátky.',-1,'A pak tě poleju já. Domů.'],['Nechám ho, ať mi koupí novej.',0,'Rozumný. Ale tady se kupujou hlavně omluvy.']]},
  {q:'Co řekneš, když tě nepustím?',o:[['„To je tak nefér!“',-1,'Znám jednoho Kevina. Taky to říkal. Taky nešel dovnitř.'],['Počkám, až budeš mít pauzu.',0,'Já nemám pauzu. Já jsem pauza.'],['Poděkuju a přijdu příští neděli.',1,'Slušnost. To tu nevídám. Pojď dál.']]},
  {q:'Kdyby ti DJ podal ruku, co řekneš?',o:[['„Mrd dlužím vám!“',1,'Nevím, co to znamená, ale zní to jako heslo. Pojď.'],['„Podepíšeš mi triko?“',0,'Slušně, ale fádně. Podpis se tu získává jinak.'],['„Ukaž, jak se lije vodka do oka.“',-1,'Klub sráčů jsem viděl. Ty ho hraješ. Ven.']]},
  {q:'Kolik stojí voda u baru a kolik stojí moje trpělivost?',o:[['Šedesát korun a víc, než mám.',1,'Přesně. Vodu si koupíš. Trpělivost ne. Pojď.'],['Voda je zadarmo, ne?',-1,'Zadarmo je jen cesta domů. Běž.'],['Nevím. Řekni mi to.',0,'Šedesát. A trpělivost ti právě dochází.']]}"""


def patch(s):
    i = s.index("{q:'Dobrý ráno. Kam jdeš?'")
    j = s.index("]]}", i) + 3
    s = s[:i] + Q0 + s[j:]
    i = s.index("const QPOOL=[")
    j = s.index("const rollQS")
    s = s[:i] + "const QPOOL=[QS[1],QS[2]," + POOL.strip() + "];\n" + s[j:]
    old = "const rollQS=()=>{QS.splice(1,QS.length-2,...shuf(QPOOL).slice(0,2));};"
    assert old in s
    s = s.replace(old, "const shq=a=>a.map(x=>[Math.random(),x]).sort((p,q)=>p[0]-q[0]).map(x=>x[1]);"
                       "const rollQS=()=>{QS.splice(1,QS.length-2,...shq(QPOOL).slice(0,2));QS.forEach(q=>{q.o=shq(q.o);});};rollQS();", 1)
    return s
