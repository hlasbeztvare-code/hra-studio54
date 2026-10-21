# PŘEŽIJ AFTER — KOMPLETNÍ REDESIGN A ROZŠÍŘENÍ HERNÍHO SVĚTA STUDIO 54

## 1. HLAVNÍ POKYN

Proveď kompletní vizuální a funkční sjednocení projektu PŘEŽIJ AFTER.

Nejde pouze o redesign webové stránky ani o změnu barev. Cílem je vytvořit jednotný, stylově výrazný a funkčně propojený herní svět inspirovaný vizuální estetikou GTA: San Andreas, který propojí:

- příběhovou hru PŘEŽIJ AFTER;
- stylizované herní postavy a prostředí;
- online hráče a herní komunitu;
- chat, soukromé zprávy a společné mise;
- skutečné Studio 54 Praha a jeho klubové akce;
- dlouhodobou motivaci hráčů vracet se do hry i do klubu.

**Základní myšlenka: Hráč může začít jako člověk, který Studio 54 vůbec nezná, postupně poznat jeho svět, seznámit se s dalšími hráči a nakonec přijít do skutečného klubu.**

Hra musí působit jako jeden ucelený digitální svět. Nesmí být tvořena nesourodými stránkami, různými grafickými styly nebo dodatečně připojenými funkcemi, které vypadají jako samostatné aplikace.

## 2. NEJDŘÍV AUDIT, POTOM ZMĚNY

Než začneš upravovat projekt:

1. Projdi celý existující zdrojový kód, komponenty, styly, assety, herní mechaniky, ukládání dat a API.
2. Identifikuj všechny současné vizuální prvky, postavy, pozadí, ilustrace, ikony, tlačítka, dialogy a herní obrazovky.
3. Zmapuj všechny existující funkce a zjisti, které jsou funkční, částečně funkční nebo pouze vizuálně naznačené.
4. Identifikuj všechny části současného designu, které nejsou kompatibilní s novým výtvarným směrem.
5. Navrhni jednotnou architekturu vzhledu pro celý projekt.
6. Teprve potom proveď kompletní redesign a následně funkční integraci nových komunitních funkcí.

Nevytvářej druhou paralelní aplikaci. Upravuj existující projekt a zachovej funkční části, které lze bezpečně integrovat.

Nespoléhej pouze na screenshoty. Kontroluj také skutečnou implementaci a chování aplikace.

## 3. NOVÝ VIZUÁLNÍ SMĚR

### Inspirace GTA: San Andreas

Celá hra musí získat jednotný komiksový styl inspirovaný ilustracemi, postavami a atmosférou GTA: San Andreas.

Nejde o přesnou kopii GTA ani o použití jeho původních grafických assetů. Vytvoř originální výtvarný směr, který využívá podobné principy:

- výrazné obrysy postav;
- stylizovanou anatomii a siluety;
- dramatické nasvícení;
- výrazné barvy a kontrast;
- ilustrativní městské a klubové prostředí;
- přehledné komiksové dialogy;
- stylizované portréty a herní avatary;
- atmosféru nočního města a undergroundové klubové scény.

Výsledný design musí být vlastní identitou projektu PŘEŽIJ AFTER.

### Odstranění současného vizuálního stylu

Všechny současné postavy a grafické prvky, které neodpovídají novému směru, musí být nahrazeny nebo přepracovány.

To zahrnuje zejména:

- současné realistické nebo nesourodé postavy;
- původní avatary, které neodpovídají nové estetice;
- nejednotné ilustrace;
- nesourodé ikony a grafické prvky;
- původní herní portréty;
- současná pozadí, která narušují jednotný vzhled;
- dialogové a informační panely, které působí jako jiný produkt.

Nestačí přidat nový obrázek na úvodní obrazovku. Redesign musí být konzistentní napříč celou hrou.

**Zachovej obsah, herní logiku a důležité reference, ale sjednoť jejich vizuální podobu.**

### Co musí zůstat vlastní identitou Studia 54

- Originální logo Studio 54.
- Název PŘEŽIJ AFTER.
- Skutečné klubové reference a schválené fotografie.
- Identita DJs a relevantní klubové události.
- Původní herní příběh, dialogy a úkoly.
- Originální Hummer podle dodané reference.
- Specifické postavy vytvořené podle dodaných fotografií.

Reálné osoby stylizuj do nového komiksového směru tak, aby byly rozpoznatelné podle schválených předloh, ale nepůsobily jako cizí fotografie vložené do kreslené hry.

## 4. JEDNOTNÝ DESIGN SYSTEM

Vytvoř jeden společný design system pro všechny obrazovky.

### Barevnost

Používej jednotnou paletu:

- černá a velmi tmavé odstíny jako základ;
- žlutá jako hlavní barva akčních tlačítek a důležitých upozornění;
- fialová a purpurová pro neonové klubové akcenty;
- bílá pro hlavní texty;
- tlumené šedé pro sekundární informace;
- červená pouze pro varování, chyby a nebezpečné herní situace.

Barvy musí být definované jako designové tokeny, nikoli nezávisle nastavované v jednotlivých komponentách.

### Typografie

Zvol jednotnou sadu fontů odpovídající komiksové herní estetice.

- Výrazné titulky a názvy misí.
- Dobře čitelné texty dialogů.
- Jasně odlišené herní statistiky.
- Konzistentní velikosti, tloušťky a řádkování.
- Podpora české diakritiky.

Pokud projekt používá schválený font Passion CZ, zachovej jej pro editovatelné prvky, pokud technická kontrola nepotvrdí problém s jeho použitím.

### Komponenty

Vytvoř sdílené komponenty pro:

- hlavní a sekundární tlačítka;
- herní panely;
- dialogová okna;
- profily hráčů;
- herní avatary;
- notifikace;
- chatovací bubliny;
- karty misí;
- ukazatele statistik;
- odznaky a reputaci;
- seznamy online hráčů;
- herní menu;
- potvrzovací dialogy;
- výsledkové obrazovky.

Všechny komponenty musí používat společné barvy, typografii, rozestupy, okraje, stíny a chování při interakci.

## 5. ÚVODNÍ OBRAZOVKA

Úvodní obrazovka musí být přepracována ve stejném stylu jako zbytek hry.

Zachovej schválený layout a jeho důležité prvky:

- logo Studio 54;
- hlavní název PŘEŽIJ AFTER;
- Pepu a jeho Face Control;
- Hummer podle původní reference;
- výrazné žluté tlačítko START;
- přístup k TOP 10;
- spodní navigaci.

Spodní navigace musí zachovat tyto položky v tomto pořadí:

1. POŘADÍ
2. ULOŽIT NA PLOCHU
3. NÁVŠTĚVY / HRY
4. TVŮJ REKORD
5. JAK HRÁT

Pokud je v projektu závazný schválený grafický návrh úvodní obrazovky, nejprve ověř jeho pravidla. Zachovej jeho schválené rozložení a přepracuj pouze ty prvky, které mají být změněny.

Nepřidávej duplicitní HTML prvky přes texty, loga nebo ilustrace, které jsou již součástí podkladového obrázku.

## 6. HRÁČSKÉ PROFILY A AVATARY

Každý registrovaný hráč musí mít vlastní profil.

Profil obsahuje:

- přezdívku;
- originální stylizovaný avatar;
- herní úroveň;
- reputaci;
- dosažené odznaky;
- herní rekord;
- stav online, pokud jej uživatel povolí;
- volitelnou informaci o zájmu o nadcházející klubovou akci.

Avatary musí používat jednotný komiksový styl. Uživatel si může vybírat z dostupných vzhledů, účesů, oblečení a dalších kosmetických variant.

Nevytvářej kopie současných avatarů v novém skinu bez skutečného sjednocení. Prověř všechny zdroje obrázků a zajisti, aby profil, herní obrazovka, chat i seznam hráčů používaly stejnou identitu konkrétní postavy.

## 7. ONLINE KOMUNITA

Hra se musí změnit z čistě individuálního zážitku na propojenou komunitní platformu.

### Online hráči

Vytvoř přehled online hráčů, kteří dobrovolně povolili zobrazení svého statusu.

U každého hráče zobraz:

- avatar;
- přezdívku;
- online status;
- aktuální herní aktivitu, pokud ji sdílí;
- reputaci nebo úroveň;
- dostupnou akci, například ZOBRAZIT PROFIL nebo POZVAT DO MISE.

Možné stavy:

- Online.
- Právě hraje.
- Plní misi.
- Hledá spoluhráče.
- Chystá se na klubovou akci.
- Offline.

Statusy musí odpovídat skutečným datům. Nevytvářej falešné online uživatele ani simulované počty aktivních hráčů vydávané za skutečnost.

### Hledání spoluhráčů

Hráči mohou:

- pozvat jiného hráče do společné mise;
- přijmout nebo odmítnout pozvání;
- navázat přátelství;
- najít lidi, kteří plní stejnou výzvu;
- vytvořit skupinu;
- domluvit se na společné návštěvě klubu.

Tato funkce musí být přirozenou součástí hry, nikoli oddělenou stránkou s cizím vzhledem.

## 8. CHAT A ZPRÁVY

Vytvoř chatovací systém, který vizuálně odpovídá novému designu.

### Typy komunikace

**Soukromý chat**

Zprávy mezi hráči, kteří mají komunikaci povolenou. Uživatelé mohou žádosti o zprávy přijímat, odmítat a blokovat.

**Skupinový chat**

Komunikace mezi hráči v jedné skupině nebo společné misi.

**Mise chat**

Kontextový chat pro hráče, kteří společně plní konkrétní úkol.

**Klubová komunita**

Prostor pro komunikaci kolem akcí, DJs a společných herních událostí. Moderování musí být dostupné oprávněným správcům.

Chat musí obsahovat seznam konverzací, přehled nových zpráv, čas odeslání, základní notifikace a stavy načtení.

Zprávy musí být skutečně ukládány a doručovány prostřednictvím backendu. Nestačí pouze vytvořit statické grafické okno.

Pokud současná infrastruktura nemá backend pro zprávy, navrhni jeho bezpečnou implementaci a jasně popiš potřebné změny.

## 9. SPOLEČNÉ MISE A PŘÍBĚH

Herní příběh zůstává hlavním základem projektu.

Zachovej:

- Face Control s Pepou;
- vstupní peníze a baterii telefonu;
- statistiky energie, nálady, měchýře, peněz a reputace;
- parket, DJ pult, bar, VIP a WC;
- rytmickou minihru;
- časové sloty DJs a sbírání podpisů;
- osmnáct úkolů od Péti;
- události s Kevinem a Perrym;
- příběhová rozhodnutí;
- konec hry a hodnocení;
- rekordy a TOP 10.

Nad tento základ přidej možnost společných misí, pokud to jejich mechanika umožňuje.

Příklady:

- najít dva další hráče pro splnění výzvy;
- společně dokončit taneční úkol;
- vytvořit tým pro speciální klubovou misi;
- odemknout týmový odznak;
- připravit se na konkrétní klubovou akci.

Neslučuj všechny úkoly do jednoho generického systému. Zachovej jejich osobitost, dialogy a návaznost na příběh.

## 10. PROPOJENÍ S REÁLNÝM STUDIEM 54

Studio 54 musí být přirozenou součástí herního světa.

Vytvoř sekci KLUBOVÉ AKCE, která může zobrazovat:

- nadcházející události;
- program DJs;
- datum a čas;
- speciální mise spojené s akcí;
- možnost označit, že hráč má zájem přijít;
- dobrovolné skupiny hráčů, kteří se na akci chystají.

Každá akce může mít vlastní tematický vizuál, ale musí vycházet ze společného design systemu.

Po skončení akce lze přidat vzpomínkovou nebo hodnoticí misi, digitální odznak či jinou herní odměnu.

Pokud má být potvrzována skutečná účast, použij transparentní způsob, například dobrovolné ověření QR kódem. Nezaměňuj pouhý zájem o akci za skutečnou návštěvu.

Nezobrazuj neověřené informace o programu. Klubová data musí pocházet z dostupného a udržovatelného zdroje.

## 11. CESTA NOVÉHO HRÁČE

Navrhni celý proces tak, aby fungoval i pro člověka, který Studio 54 nikdy nenavštívil.

1. Uživatel objeví hru přes sociální sítě, web nebo QR kód.
2. Vytvoří si účet a herní postavu.
3. Projde úvodním příběhem a Face Controlem.
4. Seznámí se s herními mechanikami.
5. Dokončí první misi.
6. Objeví další online hráče.
7. Najde spoluhráče a naváže kontakt.
8. Zjistí, jaké akce se ve Studiu 54 konají.
9. Může se přidat ke skupině hráčů, kteří se na akci chystají.
10. Navštíví skutečný klub a následně pokračuje ve hře.

Hráče nikdy nenuť ke sdílení osobních údajů ani k návštěvě klubu. Nabídni mu jasné možnosti a motivaci, ne nátlak.

## 12. TECHNICKÁ IMPLEMENTACE

Před implementací zkontroluj současný stack a přizpůsob řešení skutečnému stavu projektu.

Pokud projekt již obsahuje funkční ukládání, žebříček nebo backendové API, nejprve ověř, zda je možné je rozšířit.

Zachovej kompatibilitu s existujícími daty a mechanismy, zejména:

- `s54g_best`
- `s54g_name`
- `s54g_look`
- `s54g_pid`

Zachovej existující integraci žebříčku, pokud je funkční:

`https://s54-leaderboard.hlancaric.workers.dev`

Při změnách nesmí dojít ke ztrátě rekordů nebo rozbití kompatibility s existujícími výsledky.

Pokud je nutné přidat autentizaci, uživatelské profily, přátele, chat, skupiny nebo online statusy, navrhni potřebnou databázovou strukturu, API, autorizaci a ochranu proti zneužití.

Nikdy neukládej přihlašovací údaje ani citlivá data do veřejně dostupného frontendu.

Pokud nová funkce vyžaduje server, databázi nebo externí službu, nepředstírej, že je hotová, dokud není skutečně implementována a otestována.

## 13. RESPONZIVITA A POUŽITELNOST

Hra musí fungovat na mobilu i desktopu.

Na mobilu musí být:

- pohodlné ovládání jednou rukou;
- čitelné dialogy;
- dostatečně velká tlačítka;
- přehledný chat;
- snadný přístup k online hráčům;
- žádné překrývání herních prvků;
- zachovaný herní styl i na menších displejích.

Na desktopu může být rozhraní prostorově bohatší, ale musí zůstat součástí stejného design systemu.

Otestuj iPhone Safari, Android Chrome a běžné desktopové prohlížeče.

## 14. BEZPEČNOST A MODERACE

Protože projekt propojuje lidi, musí obsahovat:

- blokování hráčů;
- nahlašování nevhodného obsahu;
- ochranu proti spamu;
- oprávnění pro skupiny a správce;
- kontrolu přístupu k soukromým zprávám;
- možnost skrýt online status;
- ochranu osobních údajů;
- omezení automatizovaného zneužívání API.

Přesnou polohu hráče nikdy nezobrazuj ostatním bez výslovného souhlasu. Pro seznamování a domlouvání klubových návštěv používej dobrovolně sdílené informace.

## 15. ZÁKAZ POLOVIČATÉHO REDESIGNU

Nedělej pouze kosmetické změny.

Neponechávej staré postavy v novém rozhraní, pokud narušují jednotný styl.

Nekombinuj realistické fotografie, nesourodé avatary, náhodné ikony a komiksové ilustrace bez jasného výtvarného pravidla.

Nevytvářej nefunkční tlačítka ani statické makety funkcí, které mají být skutečně interaktivní.

Nevymazávej existující funkce jen proto, že se obtížně začleňují do nového designu. Nejdříve navrhni jejich náhradu nebo integraci.

Nevymýšlej obsah, který není podložený projektem nebo schváleným zadáním.

Nepoužívej původní grafické assety GTA bez příslušných práv. Inspiruj se výtvarnými principy a vytvářej originální grafiku.

## 16. TESTOVÁNÍ A PŘEDÁNÍ

Po implementaci:

1. Zkontroluj všechny obrazovky a herní stavy.
2. Ověř jednotný vizuální styl postav, pozadí, dialogů, tlačítek a ikon.
3. Otestuj registraci a přihlášení.
4. Otestuj profily a avatary.
5. Otestuj online statusy a jejich aktualizaci.
6. Otestuj soukromé zprávy, skupinový chat a blokování.
7. Otestuj pozvánky a společné mise.
8. Otestuj klubové akce.
9. Ověř zachování rekordů a ukládání dat.
10. Otestuj mobilní i desktopové zobrazení.
11. Zkontroluj chyby v konzoli, přístupnost a výkon.
12. Sepiš přehled hotových funkcí, nedokončených částí a nutných externích nastavení.

Pokud některá část nemůže být dokončena kvůli chybějícímu backendu, přístupům nebo externí službě, jasně uveď přesnou překážku a další nutný krok.

## 17. PRODUKČNÍ OMEZENÍ

Neprováděj automatické nasazení do produkce bez výslovného souhlasu.

Nespouštěj produkční deploy ani příkazy Wrangler bez výslovného povolení.

Před nasazením musí být připravený funkční build, testy, kontrola datové kompatibility a přehled změn.

## 18. FINÁLNÍ VIZE

PŘEŽIJ AFTER má být originální herní svět Studia 54 s jednotnou komiksovou estetikou inspirovanou GTA: San Andreas.

Hráč se stává součástí příběhu, vytváří si postavu, plní úkoly, sbírá reputaci, potkává další hráče, komunikuje s nimi, vytváří skupiny a objevuje skutečné klubové akce.

Hra má propojit digitální zábavu se skutečným společenským zážitkem.

**Nejde jen o to přežít afterparty. Jde o to poznat lidi, stát se součástí komunity a objevit Studio 54.**

Výsledkem musí být jeden konzistentní, funkční a dlouhodobě rozvíjitelný produkt, nikoli pouze vizuálně upravená úvodní obrazovka.
