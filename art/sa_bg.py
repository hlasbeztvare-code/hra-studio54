# Pozadí intra a Pepy z předlohy uživatele (art/sa_ref.jpg): odstraní zapečené UI (logo, datum, nadpis)
# a vytvoří čisté scény art/sa_intro.webp a art/sa_pepa.webp.
import cv2, numpy as np, pathlib
A = pathlib.Path(__file__).parent
im = cv2.imread(str(A / "sa_ref.jpg"))
L, R = im[19:1774, 0:580].copy(), im[19:1774, 596:1170].copy()


def clean(img, rects, crop_h, fade=160):
    m = np.zeros(img.shape[:2], np.uint8)
    for x0, y0, x1, y1 in rects:
        m[y0:y1, x0:x1] = 255
    # obloha: v každém řádku barva světlých (nebe) pixelů mimo masku → hladký přechod modrá→zlatá
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    sky = np.zeros((img.shape[0], 3)); ok = np.zeros(img.shape[0], bool)
    for y in range(img.shape[0]):
        row = img[y][m[y] == 0]; v = hsv[y][m[y] == 0][:, 2] if len(row) else []
        if len(row) > 20:
            sel = row[v >= np.percentile(v, 70)]
            if len(sel): sky[y] = np.median(sel, axis=0); ok[y] = True
    ys = np.arange(img.shape[0])
    for c in range(3):
        sky[:, c] = np.interp(ys, ys[ok], sky[ok, c])
    sky = cv2.GaussianBlur(sky.reshape(-1, 1, 3).astype(np.float32), (1, 0), sigmaX=1, sigmaY=25).reshape(-1, 3)
    fill = np.repeat(sky[:, None, :], img.shape[1], axis=1)
    fill += np.random.default_rng(5).normal(0, 2.2, fill.shape)
    mm = cv2.GaussianBlur(m, (0, 0), 7).astype(float)[..., None] / 255
    out = (img * (1 - mm) + fill * mm).clip(0, 255).astype(np.uint8)
    out = out[:crop_h]
    # dole plynule do tmavé dlažby
    h = out.shape[0]
    g = np.ones((h, 1, 1)); g[h - fade:, 0, 0] = np.linspace(1, 0, fade) ** 1.4
    dark = np.array([14, 18, 22], float)
    out = (out * g + dark * (1 - g)).astype(np.uint8)
    return out


intro = clean(R, [(12, 40, 395, 222), (378, 66, 566, 296), (24, 218, 196, 336), (54, 306, 514, 472), (54, 460, 218, 508), (188, 444, 518, 570)], 1080)
pepa = clean(L, [(38, 48, 552, 240)], 860, fade=120)


def hair(img):
    """Pepa není plešatej: krátké tmavé vlasy (komiksově, s obrysem a leskem)."""
    h, w = img.shape[:2]
    yy, xx = np.mgrid[0:h, 0:w].astype(float)
    cx, cy, rx, ry = 298, 461, 81, 90
    ell = ((xx - cx) / rx) ** 2 + ((yy - cy) / ry) ** 2 <= 1 + 0.035 * np.sin(np.arctan2(yy - cy, xx - cx) * 38)
    line = 413 + ((xx - cx) / 70) ** 2 * 20 + 3.5 * np.sin(xx / 4.2) * (np.abs(xx - cx) < 74)
    m = (ell & (yy < line) & (yy > 300)).astype(np.uint8) * 255
    m = cv2.GaussianBlur(m, (0, 0), 1.2)
    base = np.zeros_like(img); base[:] = (24, 30, 42)  # BGR tmavě hnědá
    rng = np.random.default_rng(3)
    tex = base.astype(float)
    for _ in range(260):  # tahy štětce (strniště)
        x = rng.uniform(cx - rx, cx + rx); y = rng.uniform(cy - ry, 440)
        cv2.line(tex, (int(x), int(y)), (int(x + rng.uniform(-3, 3)), int(y + rng.uniform(4, 9))), (12, 15, 20), 1, cv2.LINE_AA)
    for _ in range(140):  # světlejší pramínky
        x = rng.uniform(cx - rx + 8, cx + rx - 8); y = rng.uniform(cy - ry + 6, 425)
        cv2.line(tex, (int(x), int(y)), (int(x + rng.uniform(-4, 4)), int(y + rng.uniform(5, 10))), (44, 54, 70), 1, cv2.LINE_AA)
    for i in range(7):  # lesk jako tahy
        x0 = cx - 46 + i * 9
        cv2.line(tex, (x0, cy - 78 + abs(i - 3) * 2), (x0 + 6, cy - 68 + abs(i - 3) * 2), (52, 62, 78), 1, cv2.LINE_AA)
    tex = cv2.GaussianBlur(tex, (0, 0), .6)
    a = m.astype(float)[..., None] / 255
    out = (img * (1 - a) + tex * a).astype(np.uint8)
    cs, _ = cv2.findContours((m > 128).astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    cv2.drawContours(out, cs, -1, (14, 12, 12), 3, cv2.LINE_AA)
    return out


# pepa = hair(pepa)  # Pepa je a zůstane plešatej (uživatel 2026-10-04)
for name, img in (("sa_intro", intro), ("sa_pepa", pepa)):
    cv2.imwrite(str(A / f"{name}.webp"), img, [cv2.IMWRITE_WEBP_QUALITY, 86])
    print(name, img.shape)


# ── Pepa podle portrétu od uživatele (art/pepa_ref.png): plešatej, oblečenej v černém triku SECURITY ──
def dress(img):
    from PIL import Image, ImageDraw, ImageFont, ImageFilter
    S = 2  # kreslit ve 2× kvůli hladkým hranám
    h, w = img.shape[:2]
    base = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB)).resize((w * S, h * S), Image.LANCZOS)
    P = lambda pts: [(x * S, y * S) for x, y in pts]
    # výstřih (U) od levé strany krku přes hrudní kost k pravé
    collar = [(205 + t * 435, 860 + 150 * np.sin(np.pi * t) + (20 * t)) for t in np.linspace(0, 1, 40)]
    shirt = [(0, 868), (175, 786)] + collar + [(700, 862), (765, 884), (832, 938), (872, 1012), (890, 1100), (904, 1250), (948, 1439), (0, 1439)]
    lay = Image.new("RGBA", base.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    d.polygon(P(shirt), fill=(26, 25, 27, 255))
    # záhyby a světlo na rameni
    for pts, col, wd in (([(40, 1000), (160, 1130), (210, 1300)], (44, 43, 46, 255), 26),
                         ([(760, 960), (820, 1060), (850, 1200)], (52, 51, 55, 255), 30),
                         ([(330, 1250), (420, 1330), (520, 1335), (610, 1270)], (18, 17, 19, 255), 16),
                         ([(120, 860), (200, 900)], (60, 59, 63, 255), 14)):
        d.line(P(pts), fill=col, width=wd * S, joint="curve")
    # žebrovaný lem výstřihu
    inner = [(x, y + 26) for x, y in collar]
    d.polygon(P(collar + inner[::-1]), fill=(40, 39, 42, 255))
    for i in range(0, 40, 2):
        d.line(P([collar[i], inner[i]]), fill=(20, 19, 21, 255), width=2 * S)
    # SECURITY přes hruď
    f = ImageFont.truetype(str(A / "fonts/Anton-Regular.ttf"), 112 * S)
    txt = Image.new("RGBA", base.size, (0, 0, 0, 0)); td = ImageDraw.Draw(txt)
    td.text((450 * S, 1175 * S), "SECURITY", font=f, fill=(233, 228, 214, 255), anchor="mm")
    txt = txt.rotate(4, center=(450 * S, 1175 * S), resample=Image.BICUBIC)
    lay = Image.alpha_composite(lay, txt)
    out = Image.alpha_composite(base.convert("RGBA"), lay)
    # inkoustový obrys trika
    o = ImageDraw.Draw(out)
    o.line(P(shirt[:-2]), fill=(10, 9, 9, 255), width=8 * S, joint="curve")
    o.line(P(inner), fill=(10, 9, 9, 255), width=4 * S, joint="curve")
    out = out.convert("RGB").resize((w, h), Image.LANCZOS)
    return cv2.cvtColor(np.array(out), cv2.COLOR_RGB2BGR)


pepa = dress(cv2.imread(str(A / "pepa_ref.png")))
cv2.imwrite(str(A / "sa_pepa.webp"), pepa, [cv2.IMWRITE_WEBP_QUALITY, 86])
print("sa_pepa (portrét)", pepa.shape)


# ── malá postavička Pepy: výřez z oblečeného portrétu + černý komiksový obrys ──
def figure(img):
    h, w = img.shape[:2]
    m = np.full((h, w), cv2.GC_PR_BGD, np.uint8)
    cv2.ellipse(m, (390, 520), (300, 440), 0, 0, 360, cv2.GC_PR_FGD, -1)
    cv2.fillPoly(m, [np.array([(0, 870), (180, 780), (640, 860), (770, 880), (840, 940), (890, 1100), (950, 1439), (0, 1439)])], cv2.GC_PR_FGD)
    cv2.ellipse(m, (400, 520), (220, 360), 0, 0, 360, cv2.GC_FGD, -1)
    cv2.fillPoly(m, [np.array([(40, 960), (700, 960), (820, 1100), (860, 1439), (40, 1439)])], cv2.GC_FGD)
    m[:60, :] = cv2.GC_BGD; m[:, 1000:] = cv2.GC_BGD; m[:700, 760:] = cv2.GC_BGD; m[:420, :90] = cv2.GC_BGD
    bgm, fgm = np.zeros((1, 65)), np.zeros((1, 65))
    cv2.grabCut(img, m, None, bgm, fgm, 6, cv2.GC_INIT_WITH_MASK)
    a = np.where((m == 1) | (m == 3), 255, 0).astype("uint8")
    n, l, st, _ = cv2.connectedComponentsWithStats(a); k = 1 + np.argmax(st[1:, 4]); a = np.where(l == k, 255, 0).astype("uint8")
    ff = a.copy(); cv2.floodFill(ff, None, (w - 1, 0), 128); a[ff == 0] = 255
    a = cv2.morphologyEx(a, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9, 9)))
    pad = 24
    img = cv2.copyMakeBorder(img, pad, 0, pad, pad, cv2.BORDER_CONSTANT)
    a = cv2.copyMakeBorder(a, pad, 0, pad, pad, cv2.BORDER_CONSTANT)
    ring = cv2.dilate(a, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (19, 19)))
    out = img.copy(); out[(ring > 0) & (a < 128)] = (10, 9, 9)
    alpha = cv2.GaussianBlur(ring, (3, 3), 0)
    rgba = np.dstack([out, alpha])
    x, y, bw, bh = cv2.boundingRect((alpha > 10).astype("uint8"))
    rgba = rgba[y:y + bh, x:x + bw]
    rgba = cv2.resize(rgba, (int(bw * .55), int(bh * .55)), interpolation=cv2.INTER_AREA)
    cv2.imwrite(str(A / "sa_pepa_fig.webp"), rgba, [cv2.IMWRITE_WEBP_QUALITY, 88])
    print("sa_pepa_fig", rgba.shape)


figure(pepa)
