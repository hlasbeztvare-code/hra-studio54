# Zrychlení načtení: poslední krok řetězce klub.py.
# 1) vyhodí @font-face starých písem (Archivo, JetBrains Mono) – nikde se nepoužívají
# 2) zmenší velké obrázky v src/assets na rozměr, ve kterém se reálně zobrazují (originály -> src/assets-orig/slim/)
# Nepoužitá aktiva (bez odkazu v šabloně) vynechává build.mjs.
import json
import pathlib
import re
import shutil
from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parent.parent
ASSETS = ROOT / "src" / "assets"
ORIG = ROOT / "src" / "assets-orig" / "slim"

# id -> (max šířka, kvalita webp)
TARGET = {
    "heroA": (1600, 74), "heroB": (1600, 74),
    "bgParket": (1600, 74), "bgBar": (1600, 74), "bgVip": (1600, 74),
    "saIntro": (860, 78), "saPepaFig": (380, 86), "logo54": (760, 86),
}
POSTER = (640, 78)
DEAD_FONTS = ("Archivo", "JetBrains Mono")


def strip_fonts(s):
    def keep(m):
        return "" if any(f"'{f}'" in m.group(0) or f'"{f}"' in m.group(0) for f in DEAD_FONTS) else m.group(0)
    return re.sub(r"@font-face\s*\{[^}]*\}", keep, s)


def slim_images():
    ext = {r["id"]: r["uuid"] for r in json.loads((ROOT / "src" / "ext_resources.json").read_text(encoding="utf-8"))}
    index = json.loads((ROOT / "src" / "assets.json").read_text(encoding="utf-8"))
    ORIG.mkdir(parents=True, exist_ok=True)
    saved = 0
    for rid, uuid in ext.items():
        tgt = TARGET.get(rid) or (POSTER if rid.startswith("poster") else None)
        if not tgt or uuid not in index:
            continue
        p = ASSETS / index[uuid]["file"]
        if p.suffix != ".webp" or not p.exists():
            continue
        try:
            im = Image.open(p)
            im.load()
        except Exception as e:  # poškozený soubor nechat být, build ho zabalí jak je
            print("slim: nelze otevřít", rid, e)
            continue
        w, h = im.size
        if w <= tgt[0]:
            continue
        before = p.stat().st_size
        bak = ORIG / p.name
        if not bak.exists():
            shutil.copy2(p, bak)
        im = im.resize((tgt[0], round(h * tgt[0] / w)), Image.LANCZOS)
        im.save(p, "WEBP", quality=tgt[1], method=6)
        saved += before - p.stat().st_size
    print(f"slim: obrázky -{saved // 1024} kB")


def patch(s):
    s = strip_fonts(s)
    slim_images()
    return s
