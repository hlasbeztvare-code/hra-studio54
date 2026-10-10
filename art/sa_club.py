# Komiksová fasáda Studia 54 od Pepy/uživatele (art/club_komiks.png, 1536x1024) -> art/sa_intro.webp
# Portrét 1148x2160 (2x 574x1080): fasáda přes šířku, nahoře přechod do noční tmy pod logem, dole do tmy pod kartou.
# Spouštět ručně: python art/sa_club.py
import pathlib
import numpy as np
from PIL import Image

ART = pathlib.Path(__file__).parent
W, H = 1148, 2160
TOP = 560            # kde začíná fasáda (viditelná část scény začíná zhruba na y≈555)
X0, X1 = 110, 1200   # výřez: vchod + neon STUDIO 54
NIGHT = np.array((18, 14, 22), np.float32)


def main():
    src = Image.open(ART / "club_komiks.png").convert("RGB")
    crop = src.crop((X0, 0, X1, src.height))
    fh = round(crop.height * W / crop.width)
    fac = np.asarray(crop.resize((W, fh), Image.LANCZOS), np.float32)

    canvas = np.tile(NIGHT, (H, W, 1))
    y1 = min(H, TOP + fh)
    canvas[TOP:y1] = fac[:y1 - TOP]
    fade = 300
    a = (np.linspace(0, 1, fade) ** 1.3)[:, None, None]
    canvas[TOP:TOP + fade] = canvas[TOP:TOP + fade] * a + NIGHT * (1 - a)
    # dole do tmy
    fb = 260
    a = np.linspace(0, 1, fb)[:, None, None]
    canvas[y1 - fb:y1] = canvas[y1 - fb:y1] * (1 - a * .9) + NIGHT * a * .9
    canvas[y1:] = NIGHT * 1.0

    out = Image.fromarray(np.clip(canvas, 0, 255).astype(np.uint8))
    out.save(ART / "sa_intro.webp", quality=86, method=6)
    out.resize((574, 1080)).save(ART / "sa_intro_preview.png")
    print("sa_intro.webp", out.size, "fasáda", fh)


if __name__ == "__main__":
    main()
