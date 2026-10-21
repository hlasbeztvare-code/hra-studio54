# STUDIO 54 — DESIGN LOCK

Permanentní designový kontrakt pro `hra.l-code-dynamics.com`.
Jakákoli další úprava intro obrazovky MUSÍ respektovat pravidla níže.
Pokud úprava pravidlo poruší, nemá být odeslána.

## 0. Výjimka 2026-10-21 (úvod po načtení)

Úvod je interaktivní HTML na všech velikostech okna. Pozadí je fotografie fasády `art/club_foto.jpg` (ve hře uuid `c54a0001-4e54-4a54-8a54-fa5ade154001`), ne komiks `intro_fasada` a ne `intro-mockup.png`. Nahoře je původní logo `uploads/logo54.webp`. Největší nápis je Přežij after. Žluté START je kousek nad svislým středem. Dole jsou čtyři ovládání: Pořadí, Uložit na plochu, rekord (text „Zatím bez rekordu“, dokud hráč nemá `s54g_best`) a Jak hrát. Vlevo dole je vystřižený Pepa (`saPepaFig`) s bublinou, vpravo dodaný bílý Hummer (`hummer-reference.webp`). Panel TOP 10 a plakáty se na úvodu nekreslí. Pořadí dál otevírá žebříček, Jak hrát nápovědu. Po START zůstane vlevo logo a vedle něj datum akce. Klik na datum otevře plakát. Jméno a postava jdou dál v modalu.

## 1. Zdroj pravdy

- `deploy/uploads/intro-mockup.png` je starý návrh. Na úvodní obrazovku se nesmí kreslit jako pozadí ani na desktopu, ani na mobilu.
- Fasáda, logo, Pepa a Hummer jsou samostatné dodané soubory, ne kresba v mockupu.

## 2. Chráněné prvky

Od 2026-10-21 platí sekce 0. Následující tabulka popisuje starý mockup. Na úvodu se tyto věci kreslí HTML prvky a dodanými obrázky, ne průhlednými zónami přes PNG.

| Prvek | Kde v mockupu | HTML akce |
|---|---|---|
| Studio 54 logo top-left | levý horní roh | click → `https://studio54.cz` |
| TOP 10 panel levý | pod logem | click → otevře žebříček (`openLb`) |
| Giant yellow START! comic | střed-dole | click → `openNameForm()` + blink animace |
| Plakáty (Narozeniny Landchi + Mazerlogy) | spodek | neklikatelné, pouze dekorace |
| PŘEŽIJ AFTER headline | střed-horní | pouze vizuál |
| 02:54 mission panel | pravá strana | pouze vizuál |
| SOBOTA 10.10. banner | pravý horní roh | pouze vizuál |
| Pepa + bublina Face Control | levá dolní část | pouze vizuál |
| Blondýnka s Hummerem | střed-pravá | pouze vizuál |
| STUDIO 54 CLUB CAFE neon | horní část | pouze vizuál |

**Žádné duplikáty.** TOP10 i plakáty v HTML jsou na desktopu `display:none !important`.

## 3. Povinná typografie HTML UI

- `'Passion CZ'` (woff2 bundled) = master font pro **všechny** editovatelné HTML prvky:
  - PŘEŽIJ AFTER headline (pokud se někdy přejde na HTML variantu)
  - Spodní ovládací lišta (POŘADÍ · ULOŽIT NA PLOCHU · NÁVŠTĚVY/HRY · TVŮJ REKORD · JAK HRÁT)
  - Modal pro zadání jména hráče
  - Všechny mini-buttons a tlačítka
- `'Allura'` = pouze pro skripturální psaný text (pokud se objeví tetování / podpisové prvky).
- Žádné jiné fonty v UI (bez Impactu, Antonu, Arialu v živém textu — pouze jako fallback).
- Rasterizovaný text uvnitř mockup PNG (TOP10, 02:54, SOBOTA banner, Pepova bublina) **nelze měnit CSS/fontem** — je součástí obrázku.

## 4. Spodní ovládací lišta (`.in5-sub`)

Pořadí přesně:
1. **POŘADÍ** (otevře TOP10)
2. **ULOŽIT NA PLOCHU** (PWA install prompt)
3. **NÁVŠTĚVY / HRY** (živé statistiky — zobrazeno jako číselná dvojice)
4. **TVŮJ REKORD** (localStorage best)
5. **JAK HRÁT** (open tutorial)

Font: Passion CZ. Barva: bílá s černým obrysem pro kontrast nad mockupem. Žádný jiný prvek do lišty nepřidávat.

## 5. Flow jméno hráče

Click START (transparentní zóna přes žlutý comic) →
- přehraje blink animaci (`startBlink` keyframes)
- otevře `.in5-nf-ov` modal
- hráč zadá jméno (Passion CZ input)
- potvrdí → `startGame(name)` → přepnutí do fáze `club`

## 6. Responsive

- Stejná intro scéna na telefonu i na desktopu. Žádný media query nesmí vrátit `intro-mockup.png`.
- Na úzkém telefonu se čtyři spodní ovládání smí zalomit na dva řádky.

## 7. ZAKÁZANÉ MODIFIKACE

- ❌ Překreslovat prvky mockupu v HTML/CSS (vznikají duplikáty).
- ❌ PIL/pixel manipulace mockup PNG bez spolehlivé pixelové reference (šipka, Pepa SECURITY, tetování blondýnky) — opakovaně selhávala; buď se udělá nová AI/Photoshop verze mockupu, nebo se nic nemění.
- ❌ Měnit font rasterizovaného textu uvnitř PNG přes CSS (nefunguje — text je bitmapa).
- ❌ Přidávat další tlačítka do spodní lišty bez explicitního souhlasu.
- ❌ Měnit poměr stran mockupu nebo ho rozbíjet mobilní variantou.
- ❌ Používat Impact/Anton/Arial Black jako primární font v HTML — pouze fallback.

## 8. Deploy

- Build: `node build.mjs` → `dist/index.html` + `deploy/` statiky.
- Deploy: `wrangler deploy` (Cloudflare Workers + static assets z `./deploy`).
- Cache-bust: `BUILD_V = Date.now()` injektováno do všech URL (`?v=__BUILD_V__`).
- Dle paměti uživatele: **úpravy hry nasazovat rovnou**, bez další otázky (sdílené služby jako leaderboard dál se souhlasem).

## 9. Dodatečné prvky (nad rámec mockupu)

Reálné plakáty `poster-20261010.webp` (Narozeniny Landchi) + `poster-20261011.webp` (Mazerlogy) jsou v `deploy/uploads/`. Na desktopu se **nezobrazují** jako HTML overlay (duplikovaly by nakreslené). Na mobilu slouží jako skutečné dekorace místo nakreslených.

## 10. Když něco nejde

Pokud úprava požaduje změnu rasterizovaného obsahu mockupu (šipka pod START, oblečení Pepy, tetování blondýnky, font bannerů/panelů) a není k dispozici:
- nový AI-vygenerovaný mockup se zahrnutou úpravou, nebo
- ruční Photoshop úprava s přesnými souřadnicemi,

úprava se **nedělá** a tento stav se nahlásí uživateli (ne substituovat nepřesnou PIL aproximací — ověřeno 2026-10-09, že PIL pixel operace na obličej/oblečení/šipku bez přesných souřadnic končí katastrofou).
