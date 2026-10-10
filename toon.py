# Komiksová stylizace fotek pozadí: plné barvy + černé obrysy + rastr + černo-zlatý tón
import sys
import cv2
import numpy as np

def toon(src, dst, k=8, gold_mix=0.8):
    img = cv2.imread(src, cv2.IMREAD_COLOR)
    if img is None:
        raise SystemExit(f"Nelze načíst {src}")
    h, w = img.shape[:2]

    # 1) vyhlazení ploch se zachováním hran
    sm = img.copy()
    for _ in range(4):
        sm = cv2.bilateralFilter(sm, 9, 60, 9)
    sm = cv2.edgePreservingFilter(sm, flags=1, sigma_s=50, sigma_r=0.45)

    # 2) redukce barev (k-means v Lab) → plakátové plochy
    lab = cv2.cvtColor(sm, cv2.COLOR_BGR2LAB).reshape(-1, 3).astype(np.float32)
    crit = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 20, 1.0)
    _, lbl, ctr = cv2.kmeans(lab, k, None, crit, 3, cv2.KMEANS_PP_CENTERS)
    q = ctr[lbl.flatten()].reshape(h, w, 3).astype(np.uint8)
    q = cv2.cvtColor(q, cv2.COLOR_LAB2BGR)

    # 3) černo-zlatá gradientová mapa podle jasu
    lum = cv2.cvtColor(q, cv2.COLOR_BGR2GRAY).astype(np.float32) / 255.0
    lum = np.clip((lum - 0.5) * 1.25 + 0.47, 0, 1) ** 1.15
    stops = np.array([0.0, 0.28, 0.55, 0.8, 1.0], np.float32)
    cols = np.array([  # BGR
        [6, 8, 10],      # skoro černá
        [16, 60, 110],   # bronz
        [24, 130, 200],  # tmavé zlato
        [49, 185, 232],  # zlato #E8B931
        [208, 243, 255], # krém
    ], np.float32)
    gm = np.stack([np.interp(lum, stops, cols[:, c]) for c in range(3)], axis=-1)
    out = (q.astype(np.float32) * (1 - gold_mix) + gm * gold_mix)

    # 4) rastrové tečky (Ben-Day) ve stínech a polotónech
    step = 7
    yy, xx = np.mgrid[0:h, 0:w]
    cy = (yy % step) - step / 2 + 0.5
    cx = ((xx + (yy // step % 2) * step // 2) % step) - step / 2 + 0.5
    dist = np.sqrt(cx ** 2 + cy ** 2)
    radius = (1 - lum) * step * 0.42
    dots = (dist < radius) & (lum < 0.72) & (lum > 0.06)
    out[dots] *= 0.55

    # 5) obrysy – adaptivní práh + Canny, ztloustnuté
    g = cv2.cvtColor(sm, cv2.COLOR_BGR2GRAY)
    g = cv2.medianBlur(g, 7)
    e1 = cv2.adaptiveThreshold(g, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 15, 8)
    e1 = 255 - e1
    e2 = cv2.Canny(cv2.GaussianBlur(g, (5, 5), 0), 40, 110)
    edges = cv2.bitwise_or(e1, e2)
    edges = cv2.morphologyEx(edges, cv2.MORPH_OPEN, np.ones((2, 2), np.uint8))
    n, cc, st, _ = cv2.connectedComponentsWithStats(edges, 8)
    keep = np.zeros(n, bool); keep[1:] = st[1:, cv2.CC_STAT_AREA] >= 40
    edges = np.where(keep[cc], 255, 0).astype(np.uint8)
    edges = cv2.dilate(edges, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3)), iterations=1)
    edges = cv2.GaussianBlur(edges, (3, 3), 0).astype(np.float32) / 255.0
    out = out * (1 - edges[..., None]) + np.array([6, 6, 8], np.float32) * edges[..., None]

    out = np.clip(out, 0, 255).astype(np.uint8)
    ok = cv2.imwrite(dst, out, [cv2.IMWRITE_WEBP_QUALITY, 86])
    if not ok:
        raise SystemExit(f"Nelze zapsat {dst}")
    print("ok", dst)

if __name__ == "__main__":
    toon(sys.argv[1], sys.argv[2])
