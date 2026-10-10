# Čistý kreslený styl (à la Lokál TV) z původních fotek: zachované barvy a kompozice,
# ploché barevné plochy, tlusté černé obrysy, jemné stínování.
import sys
import cv2
import numpy as np


def toon(src, dst, k=14):
    img = cv2.imread(src, cv2.IMREAD_COLOR)
    if img is None:
        raise SystemExit(f"Nelze načíst {src}")
    h, w = img.shape[:2]

    # 1) silné vyhlazení – zmizí šum, textura koberce a světelné skvrny, hrany zůstanou
    sm = cv2.pyrMeanShiftFiltering(img, 14, 38, maxLevel=2)
    for _ in range(3):
        sm = cv2.bilateralFilter(sm, 9, 50, 9)
    sm = cv2.edgePreservingFilter(sm, flags=1, sigma_s=80, sigma_r=0.5)

    # 2) živější barvy (kreslený look), mírně jasnější
    hsv = cv2.cvtColor(sm, cv2.COLOR_BGR2HSV).astype(np.float32)
    hsv[..., 1] = np.clip(hsv[..., 1] * 1.35, 0, 255)
    hsv[..., 2] = np.clip(hsv[..., 2] * 1.06 + 8, 0, 255)
    sm = cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2BGR)

    # 3) plakátové plochy – k-means v Lab
    lab = cv2.cvtColor(sm, cv2.COLOR_BGR2LAB).reshape(-1, 3).astype(np.float32)
    crit = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 25, 0.5)
    _, lbl, ctr = cv2.kmeans(lab, k, None, crit, 4, cv2.KMEANS_PP_CENTERS)
    lbl = lbl.reshape(h, w).astype(np.uint8)
    lbl = cv2.medianBlur(lbl, 7)  # pryč s drobnými ostrůvky
    lbl = cv2.medianBlur(lbl, 5)
    q = cv2.cvtColor(ctr[lbl].astype(np.uint8), cv2.COLOR_LAB2BGR)

    # 4) obrysy – hranice ploch + strukturní hrany z vyhlazeného obrazu
    gx = cv2.Sobel(lbl.astype(np.float32), cv2.CV_32F, 1, 0, ksize=1)
    gy = cv2.Sobel(lbl.astype(np.float32), cv2.CV_32F, 0, 1, ksize=1)
    reg = ((np.abs(gx) + np.abs(gy)) > 0).astype(np.uint8) * 255
    # jen hranice mezi plochami s výrazným rozdílem jasu
    L = cv2.cvtColor(q, cv2.COLOR_BGR2GRAY)
    lg = cv2.morphologyEx(L, cv2.MORPH_GRADIENT, np.ones((3, 3), np.uint8))
    reg = np.where(lg > 22, reg, 0).astype(np.uint8)

    g = cv2.cvtColor(sm, cv2.COLOR_BGR2GRAY)
    can = cv2.Canny(cv2.GaussianBlur(g, (5, 5), 0), 60, 150)
    edges = cv2.bitwise_or(reg, can)
    n, cc, st, _ = cv2.connectedComponentsWithStats(edges, 8)
    keep = np.zeros(n, bool)
    keep[1:] = st[1:, cv2.CC_STAT_AREA] >= 60
    edges = np.where(keep[cc], 255, 0).astype(np.uint8)
    edges = cv2.dilate(edges, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3)), iterations=1)
    edges = cv2.GaussianBlur(edges, (3, 3), 0).astype(np.float32) / 255.0

    # 5) jemné komiksové stínování: tmavé plochy dostanou husté tečky
    out = q.astype(np.float32)
    lum = L.astype(np.float32) / 255.0
    step = 6
    yy, xx = np.mgrid[0:h, 0:w]
    cy = (yy % step) - step / 2 + 0.5
    cx = ((xx + (yy // step % 2) * step // 2) % step) - step / 2 + 0.5
    dots = (np.sqrt(cx ** 2 + cy ** 2) < 1.4) & (lum < 0.32)
    out[dots] *= 0.6

    out = out * (1 - edges[..., None]) + np.array([12, 10, 8], np.float32) * edges[..., None]
    out = np.clip(out, 0, 255).astype(np.uint8)
    if not cv2.imwrite(dst, out, [cv2.IMWRITE_WEBP_QUALITY, 90] if dst.endswith(".webp") else []):
        raise SystemExit(f"Nelze zapsat {dst}")
    print("ok", dst)


if __name__ == "__main__":
    toon(sys.argv[1], sys.argv[2], int(sys.argv[3]) if len(sys.argv) > 3 else 14)
