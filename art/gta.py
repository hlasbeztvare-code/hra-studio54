# GTA styl (loading-screen art) z reálných fotek klubu:
# malířsky vyhlazené plochy, cel-shading ve 3–4 tónech, tvrdé kontury,
# sytý kontrast a teplý černo-zlatý grade.
import sys
import cv2
import numpy as np

OUT_SIZE = (2560, 1707)  # ostré i na 4K (cover přes 3840 px stačí s mírným zvětšením)


def xdog(gray, sigma=1.0, k=1.6, p=24.0, eps=-0.04, phi=14.0):
    g = gray.astype(np.float32) / 255.0
    d = (1 + p) * cv2.GaussianBlur(g, (0, 0), sigma) - p * cv2.GaussianBlur(g, (0, 0), sigma * k)
    return np.clip(np.where(d >= eps, 1.0, 1.0 + np.tanh(phi * (d - eps))), 0, 1)


def gta(src, dst, scale=2.0, levels=5, gold=0.28):
    img = cv2.imread(src, cv2.IMREAD_COLOR)
    if img is None:
        raise SystemExit(f"Nelze načíst {src}")
    h0, w0 = img.shape[:2]
    # práce ve 2× rozlišení → jemnější a čistší kontury
    img = cv2.resize(img, (int(w0 * scale), int(h0 * scale)), interpolation=cv2.INTER_CUBIC)

    # 1) malířské vyhlazení (pleť, oblečení a stěny jako tahy štětcem)
    paint = img
    for _ in range(3):
        paint = cv2.bilateralFilter(paint, 9, 45, 9)
    paint = cv2.edgePreservingFilter(paint, flags=1, sigma_s=60, sigma_r=0.38)
    paint = cv2.detailEnhance(paint, sigma_s=8, sigma_r=0.12)

    # 2) cel-shading: kvantovaný jas s měkkým přechodem
    lab = cv2.cvtColor(paint, cv2.COLOR_BGR2LAB).astype(np.float32)
    L = lab[..., 0] / 255.0
    Lc = np.clip(np.power(L, 0.72), 0, 1)
    Lc = np.clip((Lc - 0.5) * 1.3 + 0.52, 0, 1)          # zvednuté stíny + kontrast
    q = np.round(Lc * (levels - 1)) / (levels - 1)
    soft = cv2.GaussianBlur(q, (0, 0), 1.2)
    lab[..., 0] = np.clip((soft * 0.7 + Lc * 0.3) * 255, 0, 255)
    # sytější barvy (GTA je výrazné)
    lab[..., 1] = 128 + (lab[..., 1] - 128) * 1.35
    lab[..., 2] = 128 + (lab[..., 2] - 128) * 1.35
    out = cv2.cvtColor(np.clip(lab, 0, 255).astype(np.uint8), cv2.COLOR_LAB2BGR).astype(np.float32) / 255.0

    # 3) teplý černo-zlatý grade (propojení s UI)
    lum = cv2.cvtColor((out * 255).astype(np.uint8), cv2.COLOR_BGR2GRAY).astype(np.float32) / 255.0
    stops = np.array([0.0, 0.3, 0.6, 0.85, 1.0], np.float32)
    cols = np.array([[8, 8, 12], [20, 40, 70], [50, 120, 190], [110, 200, 245], [200, 238, 255]], np.float32)
    gm = np.stack([np.interp(lum, stops, cols[:, c]) for c in range(3)], -1) / 255.0
    out = out * (1 - gold) + gm * gold

    # 4) tvrdé kontury: XDoG z vyhlazeného obrazu + silné hrany
    gray = cv2.cvtColor(paint, cv2.COLOR_BGR2GRAY)
    gray = cv2.equalizeHist(gray)
    ink = 1 - xdog(gray, sigma=1.7, p=30.0)
    can = cv2.Canny(cv2.GaussianBlur(gray, (5, 5), 0), 70, 170).astype(np.float32) / 255.0
    ink = np.maximum(ink, cv2.GaussianBlur(can, (3, 3), 0) * 0.9)
    m = (ink > 0.35).astype(np.uint8)
    n, cc, st, _ = cv2.connectedComponentsWithStats(m, 8)
    keep = np.zeros(n, bool)
    keep[1:] = st[1:, cv2.CC_STAT_AREA] >= 60
    ink = ink * keep[cc]
    ink = cv2.dilate(ink, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3)))
    out = out * (1 - np.clip(ink * 0.9, 0, 1)[..., None]) + np.array([0.03, 0.025, 0.02]) * np.clip(ink * 0.9, 0, 1)[..., None]

    # 5) lehká vinětace
    hh, ww = out.shape[:2]
    Y, X = np.ogrid[:hh, :ww]
    r = np.sqrt(((X - ww / 2) / (ww / 2)) ** 2 + ((Y - hh / 2) / (hh / 2)) ** 2)
    out *= np.clip(1.06 - 0.3 * r ** 2, 0.5, 1)[..., None]

    out = np.clip(out * 255, 0, 255).astype(np.uint8)
    out = cv2.resize(out, OUT_SIZE, interpolation=cv2.INTER_AREA)
    params = [cv2.IMWRITE_WEBP_QUALITY, 90] if dst.endswith(".webp") else []
    if not cv2.imwrite(dst, out, params):
        raise SystemExit(f"Nelze zapsat {dst}")
    print("ok", dst)


if __name__ == "__main__":
    gta(sys.argv[1], sys.argv[2])
