# Čistý kreslený styl (Lokál TV) z původních fotek:
# 1) potlačení světelných skvrn (disco koule) a šumu, 2) plakátové plochy,
# 3) sloučení drobných ostrůvků do sousedů → velké čisté plochy,
# 4) tlusté obrysy po hranách ploch + jemné kresebné linky detailů.
import sys
import cv2
import numpy as np


def xdog(gray, sigma=1.2, k=1.6, p=20.0, eps=-0.06, phi=10.0):
    g = gray.astype(np.float32) / 255.0
    d = (1 + p) * cv2.GaussianBlur(g, (0, 0), sigma) - p * cv2.GaussianBlur(g, (0, 0), sigma * k)
    return np.clip(np.where(d >= eps, 1.0, 1.0 + np.tanh(phi * (d - eps))), 0, 1)


def merge_small(lbl, min_area):
    """Ostrůvky menší než min_area přebarví podle nejbližšího velkého souseda."""
    small = np.zeros(lbl.shape, bool)
    for v in np.unique(lbl):
        n, cc, st, _ = cv2.connectedComponentsWithStats((lbl == v).astype(np.uint8), connectivity=4)
        tiny = np.where(st[:, cv2.CC_STAT_AREA] < min_area)[0]
        tiny = tiny[tiny > 0]
        if tiny.size:
            small |= np.isin(cc, tiny)
    if not small.any():
        return lbl
    src = (~small).astype(np.uint8)
    _, idx = cv2.distanceTransformWithLabels(1 - src, cv2.DIST_L2, 5, labelType=cv2.DIST_LABEL_PIXEL)
    ys, xs = np.nonzero(src)
    lut_v = np.zeros(idx.max() + 1, lbl.dtype)
    # DIST_LABEL_PIXEL: každý nulový pixel (= velká plocha) má vlastní index v pořadí skenování
    zero_idx = idx[src.astype(bool)]
    lut_v[zero_idx] = lbl[ys, xs]
    out = lbl.copy()
    out[small] = lut_v[idx[small]]
    return out


def toon(src, dst, k=20, min_area=700):
    img = cv2.imread(src, cv2.IMREAD_COLOR)
    if img is None:
        raise SystemExit(f"Nelze načíst {src}")
    h, w = img.shape[:2]

    base = img
    for _ in range(4):
        base = cv2.bilateralFilter(base, 7, 40, 7)

    # potlačení malých světlých skvrn v jasu (white top-hat)
    lab = cv2.cvtColor(base, cv2.COLOR_BGR2LAB)
    L = lab[..., 0]
    th = cv2.morphologyEx(L, cv2.MORPH_TOPHAT, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (31, 31)))
    th = np.where(th > 18, th, 0).astype(np.uint8)
    lab[..., 0] = cv2.subtract(L, (th * 0.85).astype(np.uint8))
    flat = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)
    flat = cv2.pyrMeanShiftFiltering(flat, 10, 26, maxLevel=1)

    # sytější barvy
    hsv = cv2.cvtColor(flat, cv2.COLOR_BGR2HSV).astype(np.float32)
    hsv[..., 1] = np.clip(hsv[..., 1] * 1.3, 0, 255)
    hsv[..., 2] = np.clip(hsv[..., 2] * 1.08 + 8, 0, 255)
    flat = cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2BGR)

    # plakátové plochy + sloučení ostrůvků
    data = cv2.cvtColor(flat, cv2.COLOR_BGR2LAB).reshape(-1, 3).astype(np.float32)
    crit = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 25, 0.5)
    _, lbl, ctr = cv2.kmeans(data, k, None, crit, 3, cv2.KMEANS_PP_CENTERS)
    lbl = cv2.medianBlur(lbl.reshape(h, w).astype(np.uint8), 5)
    lbl = merge_small(lbl, min_area)
    lbl = cv2.medianBlur(lbl, 5)
    q = cv2.cvtColor(ctr[lbl].astype(np.uint8), cv2.COLOR_LAB2BGR)

    # tlusté obrysy po hranách ploch (jen kde je výrazný rozdíl)
    gq = cv2.cvtColor(q, cv2.COLOR_BGR2GRAY)
    grad = cv2.morphologyEx(gq, cv2.MORPH_GRADIENT, np.ones((3, 3), np.uint8))
    bold = (grad > 26).astype(np.uint8) * 255
    bold = cv2.dilate(bold, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2, 2)))

    # jemné linky detailů (lahve, světla, nápisy)
    fine = (xdog(cv2.cvtColor(base, cv2.COLOR_BGR2GRAY)) < 0.45).astype(np.uint8) * 255
    n, cc, st, _ = cv2.connectedComponentsWithStats(fine, 8)
    keep = np.zeros(n, bool)
    keep[1:] = st[1:, cv2.CC_STAT_AREA] >= 50
    fine = np.where(keep[cc], 255, 0).astype(np.uint8)

    ink = cv2.GaussianBlur(cv2.bitwise_or(bold, fine), (3, 3), 0).astype(np.float32) / 255.0

    # jemný rastr ve stínech
    out = q.astype(np.float32)
    lum = gq.astype(np.float32) / 255.0
    step = 6
    yy, xx = np.mgrid[0:h, 0:w]
    cy = (yy % step) - step / 2 + 0.5
    cx = ((xx + (yy // step % 2) * step // 2) % step) - step / 2 + 0.5
    out[(np.sqrt(cx ** 2 + cy ** 2) < 1.3) & (lum < 0.3)] *= 0.62

    out = out * (1 - ink[..., None]) + np.array([16, 12, 10], np.float32) * ink[..., None]
    out = np.clip(out, 0, 255).astype(np.uint8)
    if not cv2.imwrite(dst, out, [cv2.IMWRITE_WEBP_QUALITY, 90] if dst.endswith(".webp") else []):
        raise SystemExit(f"Nelze zapsat {dst}")
    print("ok", dst)


if __name__ == "__main__":
    toon(sys.argv[1], sys.argv[2])
