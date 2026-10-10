# Kolo 7 (2026-10-07): podrobný návod „Jak hrát“ podle aktuální hry + „Ulož si hru na plochu“.
# - nápověda = záložky Pravidla / Lokace / DJové a úkoly / Body / Na plochu, posouvá se překryv (ne .gls – iOS)
# - tlačítko „Uložit na plochu“ v úvodu; Android/Chrome/Edge = nativní instalace (beforeinstallprompt
#   zachytává obálka dist/original.html do window.__bip), iPhone/iPad = návod Sdílet → Přidat na plochu
# - <head> šablony: manifest, apple-touch-icon, apple-mobile-web-app-* (runtime nahrazuje celý dokument)
# Volá se z klub.patch() po fix6.
from fix3 import rep
import help_text

HEAD = """<link rel="manifest" href="/manifest.webmanifest">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-title" content="Přežij after">
<meta name="apple-mobile-web-app-status-bar-style" content="black">
"""

BTN_OLD = """              <button class="sa-btn" sc-camel-on-click="{{ toggleHelp }}"><i class="q">?</i><span>Jak hrát</span></button>
            </div>"""
BTN_NEW = """              <button class="sa-btn" sc-camel-on-click="{{ toggleHelp }}"><i class="q">?</i><span>Jak hrát</span></button>
              <button class="sa-btn in7-home" sc-camel-on-click="{{ openInst }}"><i class="in7-ic"></i><span>Uložit hru na plochu</span></button>
            </div>"""

# celý starý překryv nápovědy (od <sc-if helpOn> po jeho </sc-if>) se nahradí
HELP_START = '<sc-if value="{{ helpOn }}" hint-placeholder-val="{{ false }}">'

CSS = """
/* ══ FIX7: nápověda + uložení na plochu ══ */
.game-root .in7-home{grid-column:1/-1;height:40px!important;border-style:dashed!important;font-size:14px!important;background:#1d1912!important}
.game-root .in7-ic{width:18px;height:18px;flex:none;background:url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' view%42ox='0 0 24 24' fill='none' stroke='%23E2B04E' stroke-width='2.4' stroke-linecap='round' stroke-linejoin='round'%3e%3crect x='5' y='2' width='14' height='20' rx='3'/%3e%3cpath d='M12 7v8M8.5 11.5 12 15l3.5-3.5'/%3e%3c/svg%3e") center/contain no-repeat}
@media (display-mode:standalone),(display-mode:fullscreen){.game-root .in7-home,.game-root .h7-tab.t-inst{display:none!important}}
.h7-ov{position:absolute;inset:0;z-index:40;background:rgba(0,0,0,.6);-webkit-backdrop-filter:blur(8px);backdrop-filter:blur(8px);overflow-y:auto;-webkit-overflow-scrolling:touch;overscroll-behavior:contain;padding:max(14px,env(safe-area-inset-top)) 12px max(18px,env(safe-area-inset-bottom))}
.h7-box{position:relative;box-sizing:border-box;width:min(640px,100%);margin:0 auto;padding:18px clamp(14px,4vw,26px) 20px;background:#141210;color:#F4ECD8;border:3px solid #E2B04E;border-radius:22px;box-shadow:0 0 0 3px #121010,7px 8px 0 #A97A2B}
.h7-head{display:flex;align-items:center;justify-content:space-between;gap:10px;margin-bottom:12px}
.h7-head b{font:30px/1 'Passion CZ',sans-serif;letter-spacing:.02em;color:#E2B04E;text-transform:uppercase}
.h7-x{all:unset;cursor:pointer;flex:none;width:40px;height:40px;display:grid;place-items:center;border-radius:12px;background:#E2B04E;color:#121010;font:800 22px/1 'Barlow',sans-serif;box-shadow:3px 3px 0 #000}
.h7-tabs{display:flex;flex-wrap:wrap;gap:6px;margin-bottom:14px}
.h7-tab{all:unset;cursor:pointer;padding:8px 12px;border-radius:12px;border:2px solid #E2B04E;background:#1d1912;font:800 13px/1 'Barlow',sans-serif;text-transform:uppercase;letter-spacing:.03em;color:#F4ECD8}
.h7-tab.on{background:#E2B04E;color:#121010}
.h7-sec{display:flex;flex-direction:column;gap:10px}
.h7-sec h3{margin:8px 0 0;font:22px/1.05 'Passion CZ',sans-serif;letter-spacing:.02em;text-transform:uppercase;color:#E2B04E}
.h7-sec p{margin:0;font:600 15.5px/1.45 'Barlow',sans-serif!important;color:#F4ECD8}
.h7-sec ul,.h7-sec ol{margin:0;padding-left:20px;display:flex;flex-direction:column;gap:6px;font:600 15.5px/1.42 'Barlow',sans-serif}
.h7-sec li::marker{color:#E2B04E;font-weight:800}
.h7-sec b{color:#F6DA92;font-weight:800}
.h7-card{padding:12px 14px;border-radius:14px;background:#1f1a13;border:2px solid rgba(226,176,78,.45)}
.h7-card>h4{margin:0 0 6px;font:800 14px/1.1 'Barlow',sans-serif;letter-spacing:.05em;text-transform:uppercase;color:#E2B04E}
.h7-tip{padding:10px 14px;border-radius:14px;background:#E2B04E;color:#121010!important;font:700 15px/1.4 'Barlow',sans-serif!important}
.h7-tip b{color:#121010!important}
.h7-go{all:unset;cursor:pointer;align-self:center;margin-top:14px;padding:14px 28px;border-radius:999px;background:#E2B04E;color:#121010;font:800 16px/1 'Barlow',sans-serif;text-transform:uppercase;box-shadow:0 0 0 3px #121010,4px 5px 0 #000}
.h7-inst{all:unset;cursor:pointer;display:flex;align-items:center;justify-content:center;gap:10px;padding:14px 20px;border-radius:14px;background:#E2B04E;color:#121010;font:800 17px/1 'Barlow',sans-serif;text-transform:uppercase;box-shadow:0 0 0 3px #121010,4px 5px 0 #000}
.h7-os{display:flex;flex-direction:column;gap:10px}
.h7-os>.h7-card{order:2}
.h7-os.os-ios>.c-ios,.h7-os.os-and>.c-and,.h7-os.os-pc>.c-pc{order:1;border-color:#E2B04E;box-shadow:inset 0 0 0 1px #E2B04E}
.h7-os.os-ios>.c-ios>h4::after,.h7-os.os-and>.c-and>h4::after,.h7-os.os-pc>.c-pc>h4::after{content:" · tvoje zařízení";color:#F6DA92}
.h7-sym{display:inline-block;padding:0 6px;border-radius:6px;background:#2a241a;border:1px solid rgba(226,176,78,.5);font-weight:800;white-space:nowrap}
@media (max-width:420px){.h7-head b{font-size:25px}.h7-tab{padding:7px 9px;font-size:12px}.h7-sec p,.h7-sec ul,.h7-sec ol{font-size:15px!important}}
"""


def patch(s):
    s = rep(s, '<title>Studio 54 · Přežij after</title>\n', '<title>Studio 54 · Přežij after</title>\n' + HEAD)
    s = rep(s, BTN_OLD, BTN_NEW)
    # starý překryv nápovědy → nový
    i = s.index(HELP_START)
    assert s.count(HELP_START) == 1
    j = s.index("</sc-if>", i) + len("</sc-if>")
    s = s[:i] + help_text.OVERLAY + s[j:]
    # logika: záložky nápovědy, otevření rovnou na „Na plochu“, instalace
    s = rep(s, "helpOn:!!s.help, toggleHelp:()=>this.setState(x=>({help:!x.help})),", help_text.RENDER)
    # VIP násobí jen body za čas, ne všechno
    s = rep(s, "'Jsi uvnitř · body ×1,5'", "'Jsi uvnitř · body za čas ×1,5'")
    s = rep(s, "Všechno tady se počítá jedna a půl krát.", "Body, co ti tu nabíhají za čas, se počítají jedna a půl krát.")
    i = s.rindex("</style>")
    return s[:i] + CSS + s[i:]
