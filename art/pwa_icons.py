# Ikony pro „Přidat na plochu“ (manifest + apple-touch-icon): fasáda klubu + logo Studio 54
from pathlib import Path
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "src" / "pwa"
OUT.mkdir(parents=True, exist_ok=True)
logo = Image.open(ROOT / "art" / "logo54_gta.png").convert("RGBA")
bg = Image.open(ROOT / "art" / "sa_intro.webp").convert("RGB")


def make(size, safe):
    """safe = podíl plochy, kam se vejde logo (maskable ikony ořezávají okraje)."""
    w, h = bg.size
    side = min(w, h)
    crop = bg.crop((0, 600, side, 600 + side)).resize((size, size), Image.LANCZOS)
    crop = ImageEnhance.Brightness(crop.filter(ImageFilter.GaussianBlur(size / 160))).enhance(0.55)
    im = crop.convert("RGBA")
    # zlatý rámeček
    d = ImageDraw.Draw(im)
    b = max(2, size // 40)
    inset = int(size * (1 - safe) / 2) + b
    d.rounded_rectangle((inset, inset, size - inset, size - inset), radius=size // 8, outline=(226, 176, 78, 255), width=b)
    lw = int(size * safe * 0.86)
    lg = logo.resize((lw, int(logo.height * lw / logo.width)), Image.LANCZOS)
    sh = Image.new("RGBA", lg.size, (0, 0, 0, 0))
    sh.putalpha(lg.getchannel("A").point(lambda a: int(a * 0.6)))
    sh = sh.filter(ImageFilter.GaussianBlur(size / 90))
    x, y = (size - lw) // 2, (size - lg.height) // 2
    im.alpha_composite(sh, (x + size // 80, y + size // 60))
    im.alpha_composite(lg, (x, y))
    return im.convert("RGB")


for name, size, safe in [("icon-192.png", 192, 0.92), ("icon-512.png", 512, 0.92),
                         ("icon-maskable-512.png", 512, 0.72), ("apple-touch-icon.png", 180, 0.92)]:
    make(size, safe).save(OUT / name, optimize=True)
    print(name)
