# Kolo 6 (2026-10-07): responzivita mobil + tablet.
# - hláška na mobilu už neschovává horní lištu (body, energie, peníze) – sedí pod ní
# - telefon: kompaktní lišta (čas + 3 čipy v 1. řádku, ukazatele ve 2.), čipy štítek nad hodnotou
# - panely nejsou scroll kontejnery s filtrem (iOS pak zdvojuje text) – posouvá se .hud-mid
# - záložky a citace v papírových bublinách nepřetékají, tablet na výšku = 2 sloupce
# - „Otoč telefon“ se neukáže při psaní jména (Android klávesnice zmenší výšku)
# Volá se z klub.patch() po fix5. CSS jde na konec posledního <style>.

CSS = """
/* ══ FIX6: responzivita mobil + tablet ══ */
/* panely: filtr + overflow:auto na jednom prvku = iOS kreslí text dvakrát → posouvá se jen .hud-mid */
.game-root .panel-loc,.game-root .panel-dj{overflow:visible!important;max-height:none!important}
.game-root .hud-mid{overscroll-behavior:contain;scrollbar-width:thin}
/* citace v papírové bublině (úkoly, minihry, události): zubatý okraj nesmí ukousnout text */
.game-root .gls .cap{padding-left:max(20px,calc(3.5% + 12px))!important;padding-right:max(20px,calc(3.5% + 12px))!important}
.game-root .loc-cap{padding-left:max(16px,calc(3% + 10px))!important;padding-right:max(16px,calc(3% + 10px))!important}
/* telefon na ležato: hlášku neukazovat, když je to jen klávesnice (výška se zmenší) */
@media (orientation:landscape) and (max-height:500px) and (pointer:coarse) and (max-aspect-ratio:13/9){.game-root::after{display:none!important}}
.game-root:has(input:focus)::after{display:none!important}

@media (max-width:899px){
 /* hláška pod lištou, lišta zůstává vidět */
 .game-root:has(.hud-toast) .hud-top{visibility:visible!important}
 .game-root.game-root .hud-toast{top:calc(var(--ht,140px) + 6px)!important;min-height:0!important;padding:9px 46px 9px 16px!important;box-shadow:4px 4px 0 #A97A2B,0 10px 24px rgba(0,0,0,.45)!important}
 /* čipy: štítek nad hodnotou */
 .game-root .hud-chip{flex-direction:column!important;align-items:flex-start!important;justify-content:center!important;gap:1px!important;padding:4px 6px 3px 7px!important;min-width:0!important;overflow:hidden}
 .game-root.game-root .hud-top .hud-chip .hud-chip-k,.game-root.game-root .hud-top .hud-chip .hud-chip-k span{font:800 9.5px/1.15 'Barlow',sans-serif!important;letter-spacing:0!important;text-transform:uppercase!important;white-space:nowrap!important}
 .game-root .hud-chip-k{display:flex!important;align-items:center;gap:3px;max-width:100%;overflow:hidden}
 .game-root .hud-chip-k::before{font-size:11px!important;flex:none}
 .game-root.game-root .hud-top .hud-chip>span:last-child{font-size:16px!important;line-height:1.05!important;white-space:nowrap!important;max-width:100%}
 /* záložky lokací */
 .game-root .hud-tabs{gap:5px!important}
 .game-root.game-root .hud-tab{min-height:38px!important;min-width:0!important;padding-left:2px!important;padding-right:2px!important;justify-content:center!important;overflow:hidden}
 .game-root .hud-tab span:first-child{font-size:clamp(11px,3.2vw,14px)!important;letter-spacing:0!important;white-space:nowrap!important;text-align:center}
 /* papírové panely: okraj roste s šířkou (rám je kreslený v %) */
 .game-root .panel-loc,.game-root .panel-dj{padding:30px max(22px,calc(4% + 12px)) 28px!important}
 /* úvod */
 .in5 .in5-date{min-width:0}
 .in5-date .big{white-space:nowrap}
 .in5-date .n{font-size:clamp(11px,3.3vw,15px)!important;hyphens:none;overflow-wrap:normal}
 .in5-tl>.in5-tr:only-child{grid-column:1/-1}
}

/* úzký telefon: karta s datem pod sebe, ať se nic nevylévá */
@media (max-width:399px){
 .in5 .in5-date{grid-template-columns:minmax(0,1fr)!important;row-gap:2px}
 .in5-date .d{grid-column:1!important}
 .in5 .in5-date .big{grid-row:auto!important;font-size:clamp(26px,8.6vw,34px)!important}
 .in5-date .n{max-width:none!important}
}
/* telefon: lišta ve dvou řádcích – [čas | peníze | reputace | body] + [energie | nálada | měchýř] */
@media (max-width:599px){
 .game-root .hud-top{display:grid!important;grid-template-columns:repeat(12,minmax(0,1fr))!important;gap:6px!important;align-items:stretch}
 .game-root .hud-stats{display:contents!important}
 .game-root .hud-id{grid-column:span 3;order:0;display:flex!important;flex-direction:column;align-items:flex-start;justify-content:center;gap:2px!important;min-width:0}
 .game-root .hud-id .logo54{display:none!important}
 .game-root .hud-clock{font-size:19px!important;padding:2px 7px 0!important}
 .game-root .hud-left{margin:0!important;font-size:9.5px!important;letter-spacing:.02em!important;white-space:nowrap}
 .game-root .hud-chip{grid-column:span 3!important;order:1}
 .game-root .hud-meter{grid-column:span 4!important;order:2}
}
/* úzký telefon: u čipů jen ikonka + hodnota */
@media (max-width:379px){
 .game-root.game-root .hud-top .hud-chip .hud-chip-k span{font-size:0!important}
 .game-root.game-root .hud-top .hud-chip .hud-chip-k::before{font-size:12px!important}
 .game-root.game-root .hud-top .hud-chip>span:last-child{font-size:13px!important;letter-spacing:-.01em!important}
 .game-root.game-root .hud-top .hud-chip{padding-left:5px!important;padding-right:4px!important}
 .game-root.game-root .hud-tab span:first-child{font-size:10.5px!important}
 .game-root .hud-tabs{gap:4px!important}
}

/* tablet na výšku: místo a lokace vedle sebe */
@media (min-width:700px) and (max-width:899px){
 .game-root .panel-loc{flex:1 1 360px!important}
 .game-root .panel-dj{flex:1 1 250px!important;max-width:330px!important}
}
"""


def patch(s):
    i = s.rindex("</style>")
    return s[:i] + CSS + s[i:]
