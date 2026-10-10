# Obsah nápovědy „Jak hrát“ (fix7). Čísla odpovídají kódu hry k 2026-10-07 – při změně pravidel aktualizovat.

def _tab(key, label, extra=""):
    return f'<button class="h7-tab {extra}{{{{ hc{key} }}}}" sc-camel-on-click="{{{{ ht{key} }}}}">{label}</button>'


TABS = "".join([
    _tab("Pr", "Základy"), _tab("Loc", "Lokace"), _tab("Dj", "DJové a úkoly"),
    _tab("Body", "Body a konec"), _tab("Inst", "Na plochu", "t-inst "),
])

SEC_PR = """<div class="h7-sec">
  <p>Jsi na afteru ve <b>Studiu 54</b> (Hybernská 38). Máš <b>1 500 Kč</b>, plnou baterku a jeden cíl: <b>vydržet do 14:00</b> a sehnat <b>podpis od všech DJů</b> dnešní noci. Čím víc bodů, tím výš v žebříčku TOP 10.</p>
  <h3>1 · Pepa u dveří</h3>
  <ul>
    <li>Zadej jméno (max. 18 znaků) a dej <b>Start</b>. Vrátný Pepa ti položí <b>4 otázky</b>.</li>
    <li>Za odpovědi sbíráš body: potřebuješ aspoň <b>3</b>. Hloupá odpověď = vyhazov hned.</li>
    <li>Když tě nepustí, můžeš se <b>postavit znovu do fronty</b> – stojí to 20 minut noci.</li>
  </ul>
  <h3>2 · Ukazatele nahoře</h3>
  <ul>
    <li><b>Energie</b> – pomalu ubývá, tanec ji žere rychle. <b>Na nule usneš a hra končí.</b> Doplníš ji vodou, Red Bullem, opláchnutím na WC nebo ve VIP lounge.</li>
    <li><b>Nálada</b> – taky klesá. Čím vyšší, tím rychleji ti naskakují body. <b>Od 55 ti DJ dá podpis.</b></li>
    <li><b>Měchýř</b> – každý drink ho plní. Na 80 % přijde varování, na 100 % hrozí <b>nehoda</b>. Vyprázdníš ho na WC.</li>
    <li><b>Peníze, reputace, body</b> – za peníze nakupuješ, reputace otvírá dveře (VIP, úkoly) a na konci se přičte k bodům.</li>
  </ul>
  <h3>3 · Ovládání</h3>
  <ul>
    <li>Dole přepínáš lokace: <b>Parket · DJ pult · Bar · VIP · WC</b>. Akce v lokaci jsou bubliny – u každé vidíš cenu, čas a účinek.</li>
    <li>Časová osa dole ukazuje, kdo zrovna hraje a kdo přijde.</li>
    <li>Hlášky zavřeš klepnutím. Lišta s Péťou tě vezme rovnou k úkolu.</li>
    <li>Čas se zastaví, když tančíš, hraješ minihru nebo řešíš událost.</li>
  </ul>
  <div class="h7-tip"><b>Tip:</b> Nejdřív se roztanči na parketu, ať máš náladu 55+, a hlídej si čas – každý DJ hraje jen ve svém setu.</div>
</div>"""

SEC_LOC = """<div class="h7-sec">
  <div class="h7-card"><h4>Parket</h4><ul>
    <li><b>Tančit (16 dob)</b> – ťukej na tanečníka (na PC mezerník / Enter), když je hvězda v terči. <b>Perfekt</b> = +3 nálady a 100 bodů, dobře = 40 bodů, minutí = −3 nálady a konec komba. Od komba 4 se body násobí. Potřebuješ aspoň 12 energie.</li>
    <li><b>Koukat na kouli</b> – +5 nálady, 5 min.</li>
    <li><b>Seznámit se</b> – šance na reputaci a náladu, ale může to i pokazit.</li>
  </ul></div>
  <div class="h7-card"><h4>DJ pult</h4><ul>
    <li><b>Požádat o podpis</b> – jde od nálady 55 (nebo po panákovi). +300 bodů a +1 reputace.</li>
    <li><b>Poslat panáka</b> (150 Kč) – DJ ti pak podepíše i s horší náladou.</li>
    <li><b>Přání písničky</b> – 50 : 50, buď +18 nálady, nebo trapas.</li>
    <li><b>Pokecat s DJem</b> – trocha nálady a občas užitečný tip.</li>
  </ul></div>
  <div class="h7-card"><h4>Bar</h4><ul>
    <li><b>Voda</b> 60 Kč (+15 energie) · <b>Red Bull</b> 120 Kč (+30 energie) · <b>Gin tonic</b> 190 Kč (+18 nálady, ale −6 energie). Všechno plní měchýř.</li>
    <li><b>Drby od Martiny</b> – prozradí, kdo hraje dál a kdy.</li>
    <li><b>Denisa · namíchej drink</b> – zapamatuj si suroviny a naklikej je ve správném pořadí. Povede se: +15 nálady, +10 energie, +100 Kč, +250 bodů. Každý další drink je o surovinu delší.</li>
    <li><b>Martina · chyť sklenku</b> – 5 hodů, ťukni „Chyť!“, když je sklenka ve zlaté zóně (bílý střed = perfekt). <b>Hořícího panáka nechytej!</b> 3+ chycené = +1 reputace a +15 energie.</li>
    <li><b>Péťa</b> rozdává úkoly (viz DJové a úkoly).</li>
  </ul></div>
  <div class="h7-card"><h4>VIP</h4><ul>
    <li>Vstup za <b>990 Kč</b>, nebo zdarma <b>ukecáním ochranky</b> – na to potřebuješ reputaci aspoň 4.</li>
    <li>Uvnitř: <b>body za čas ×1,5</b>, <b>lounge</b> (+35 energie), <b>šampaňské</b> 650 Kč (+25 nálady, +2 reputace) a záchod bez fronty.</li>
  </ul></div>
  <div class="h7-card"><h4>WC</h4><ul>
    <li><b>Fronta</b> – 4 až 11 lidí, každý stojí 2 minuty. Vyprázdní měchýř a občas se něco stane.</li>
    <li><b>Opláchnout obličej</b> (+14 energie) a <b>selfie</b> (šance na reputaci).</li>
    <li><b>Kevin a Perry</b> – dej jim dýško a pomoz jim se sluchátky z DJ pultu. Odměna: +500 bodů a <b>klíč od personálního WC</b> = už nikdy fronta.</li>
  </ul></div>
</div>"""

SEC_DJ = """<div class="h7-sec">
  <h3>DJové</h3>
  <ul>
    <li>Každou noc hraje 5–6 DJů podle skutečného programu klubu. Kdo a kdy, vidíš na časové ose a v panelu <b>Podpisy DJů</b>.</li>
    <li>Od každého DJe máš jen <b>jeden podpis</b> a jen <b>během jeho setu</b>. Když set skončí, karta se přeškrtne <b>Zmeškáno</b>.</li>
    <li>Podpis = +300 bodů hned a dalších <b>+600 bodů na konci</b>. Všechny podpisy jsou cesta k Legendě.</li>
  </ul>
  <h3>Péťa a úkoly</h3>
  <ul>
    <li>Péťa na baru má <b>18 úkolů</b>, jdou postupně. Vezmeš si úkol („Beru to“) nebo ho odložíš („Teď ne“).</li>
    <li>Splněný úkol si vyzvedni u Péti – peníze, energie, reputace a hodně bodů. Vzdát úkol stojí 1 reputaci.</li>
    <li>Příklady: <b>Zahřívačka</b> (6 perfektních dob), <b>Rychlé ruce</b> (3 perfektní chyty), <b>Hospodský kvíz</b>, <b>Mistr baru</b>.</li>
    <li>Kdo dá všech 18, dostane <b>Kartu štamgasta</b>.</li>
  </ul>
  <h3>Události</h3>
  <ul>
    <li>Asi hodinu po vstupu a pak každých 45–85 minut se něco semele – vybereš ze dvou možností.</li>
    <li>Volby označené <b>(risk)</b> můžou dopadnout skvěle, nebo pěkně blbě.</li>
  </ul>
</div>"""

SEC_BODY = """<div class="h7-sec">
  <h3>Jak se počítá skóre</h3>
  <ul>
    <li>Body ti naskakují <b>průběžně podle nálady</b> (ve VIP ×1,5) a za tanec, minihry, podpisy a úkoly.</li>
    <li><b>Na konci:</b> body + <b>600 za každý podpis</b> + <b>150 za každý bod reputace</b>. Ztracená bunda v šatně = −300.</li>
    <li>Tituly: do 3 000 <b>Turista s mapou</b> · do 7 000 <b>Afterák v zácviku</b> · do 12 000 <b>Štamgast</b> · víc = <b>Legenda Hybernské</b>.</li>
    <li>Výsledek se sám uloží do <b>žebříčku TOP 10</b> pod tvým jménem (počítá se tvůj nejlepší).</li>
  </ul>
  <h3>Jak hra končí</h3>
  <ul>
    <li><b>Ve 14:00 se zavírá</b> – vydržel jsi celý after.</li>
    <li><b>Energie na nule</b> – usnul jsi.</li>
    <li>Některé volby v událostech tě pošlou domů dřív (třeba „něco na povzbuzení“ na záchodech, nebo snídaně s partou po 11:40).</li>
    <li>Po konci můžeš hned hrát znovu – Pepa se ptá pokaždé jinak.</li>
  </ul>
</div>"""

SEC_INST = """<div class="h7-sec">
  <p>Ulož si hru na plochu mobilu jako aplikaci – spustíš ji jedním klepnutím a poběží <b>přes celou obrazovku</b> bez lišty prohlížeče.</p>
  <sc-if value="{{ canInst }}" hint-placeholder-val="{{ false }}"><button class="h7-inst" sc-camel-on-click="{{ doInst }}">Nainstalovat hru</button></sc-if>
  <div class="h7-os {{ osCls }}">
    <div class="h7-card c-ios"><h4>iPhone a iPad</h4><ol>
      <li>Otevři hru v <b>Safari</b> (v iOS 16.4+ jde i Chrome).</li>
      <li>Klepni na <span class="h7-sym">Sdílet ⬆</span> – čtvereček se šipkou dole (na iPadu nahoře).</li>
      <li>Sjeď níž a vyber <span class="h7-sym">Přidat na plochu</span>.</li>
      <li>Klepni na <b>Přidat</b>. Hra je na ploše jako „Přežij after“.</li>
    </ol></div>
    <div class="h7-card c-and"><h4>Android</h4><ol>
      <li><b>Chrome:</b> nahoře vpravo <span class="h7-sym">⋮</span> → <span class="h7-sym">Přidat na plochu</span> nebo <span class="h7-sym">Instalovat aplikaci</span> → <b>Instalovat</b>.</li>
      <li><b>Samsung Internet:</b> dole <span class="h7-sym">☰</span> → <span class="h7-sym">Přidat stránku na</span> → <b>Domovská obrazovka</b>.</li>
      <li><b>Firefox:</b> <span class="h7-sym">⋮</span> → <span class="h7-sym">Přidat na plochu</span> (nebo <b>Instalovat</b>).</li>
      <li><b>Edge / Opera:</b> menu → <span class="h7-sym">Přidat na telefon / plochu</span>.</li>
    </ol></div>
    <div class="h7-card c-pc"><h4>Počítač</h4><ol>
      <li><b>Chrome / Edge:</b> ikonka <span class="h7-sym">⊕ Instalovat</span> vpravo v adresním řádku, nebo menu → <b>Uložit a sdílet → Instalovat stránku jako aplikaci</b>.</li>
      <li><b>Safari na Macu:</b> Soubor → <b>Přidat do Docku</b>.</li>
    </ol></div>
  </div>
</div>"""

OVERLAY = f"""<sc-if value="{{{{ helpOn }}}}" hint-placeholder-val="{{{{ false }}}}">
        <div class="h7-ov">
          <div class="h7-box">
            <div class="h7-head"><b>Jak hrát</b><button class="h7-x" sc-camel-on-click="{{{{ toggleHelp }}}}" aria-label="Zavřít">✕</button></div>
            <div class="h7-tabs">{TABS}</div>
            <sc-if value="{{{{ hPr }}}}" hint-placeholder-val="{{{{ true }}}}">{SEC_PR}</sc-if>
            <sc-if value="{{{{ hLoc }}}}" hint-placeholder-val="{{{{ false }}}}">{SEC_LOC}</sc-if>
            <sc-if value="{{{{ hDj }}}}" hint-placeholder-val="{{{{ false }}}}">{SEC_DJ}</sc-if>
            <sc-if value="{{{{ hBody }}}}" hint-placeholder-val="{{{{ false }}}}">{SEC_BODY}</sc-if>
            <sc-if value="{{{{ hInst }}}}" hint-placeholder-val="{{{{ false }}}}">{SEC_INST}</sc-if>
            <div style="display:flex;justify-content:center"><button class="h7-go" sc-camel-on-click="{{{{ toggleHelp }}}}">Jasný, jdu na to</button></div>
          </div>
        </div>
      </sc-if>"""

# render: záložky (hPr…hInst + hc*/ht*), otevření rovnou na „Na plochu“, nativní instalace (Android/Chrome/Edge)
_K = ["Pr", "Loc", "Dj", "Body", "Inst"]
RENDER = (
    "helpOn:!!s.help, toggleHelp:()=>this.setState(x=>({help:!x.help,hTab:'Pr'})), "
    "openInst:()=>this.setState({help:true,hTab:'Inst'}), "
    + "".join(f"h{k}:(s.hTab||'Pr')==='{k}', hc{k}:(s.hTab||'Pr')==='{k}'?'on':'', ht{k}:()=>this.setState({{hTab:'{k}'}}), " for k in _K)
    + "canInst:!!(typeof window!=='undefined'&&window.__bip), "
    "doInst:()=>{const p=window.__bip;if(!p)return;try{p.prompt();Promise.resolve(p.userChoice).then(r=>{if(r&&r.outcome==='accepted')window.__bip=null;this.setState({instT:Date.now()});}).catch(()=>{});}catch(e){window.__bip=null;this.setState({instT:Date.now()});}}, "
    "osCls:(()=>{try{const u=navigator.userAgent||'';if(/iPhone|iPad|iPod/.test(u)||(/Macintosh/.test(u)&&navigator.maxTouchPoints>1))return 'os-ios';if(/Android/.test(u))return 'os-and';}catch(e){}return 'os-pc';})(),"
)
