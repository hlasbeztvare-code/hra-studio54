# Kreslený styl z původních fotek: zachová detaily (lahve, světla, nápisy),
# ploché barvy + inkoustové linky (XDoG) + jemný rastr ve stínech.
import sys
import cv2
import numpy as np


def xdog(gray, sigma=1.1, k=1.6, p=22.0, eps=-0.08, phi=12.0):
    g = gray.astype(np.float32) / 255.0
    g1 = cv2.GaussianBlur(g, (0, 0), sigma)
    g2 = cv2.GaussianBlur(g, (0, 0), sigma * k)
    d = (1 + p) * g1 - p * g2
    e = np.where(d >= eps, 1.0, 1.0 + np.tanh(phi * (d - eps)))
    return np.clip(e, 0, 1)  # 1 = bílá, 0 = linka


def toon(src, dst, k=22):
    img = cv2.imread(src, cv2.IMREAD_COLOR)
    if img is None:
        raise SystemExit(f"Nelze načíst {src}")
    h, w = img.shape[:2]

    # vyhlazení se zachováním detailu
    sm = img
    for _ in range(5):
        sm = cv2.bilateralFilter(sm, 7, 40, 7)
    lines_src = sm.copy()
    sm = cv2.edgePreservingFilter(sm, flags=1, sigma_s=40, sigma_r=0.3)

    # sytější, čistší barvy
    hsv = cv2.cvtColor(sm, cv2.COLOR_BGR2HSV).astype(np.float32)
    hsv[..., 1] = np.clip(hsv[..., 1] * 1.25, 0, 255)
    hsv[..., 2] = np.clip(hsv[..., 2] * 1.05 + 6, 0, 255)
    sm = cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2BGR)

    # plakátové plochy
    lab = cv2.cvtColor(sm, cv2.COLOR_BGR2LAB).reshape(-1, 3).astype(np.float32)
    crit = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 25, 0.5)
    _, lbl, ctr = cv2.kmeans(lab, k, None, crit, 3, cv2.KMEANS_PP_CENTERS)
    lbl = cv2.medianBlur(lbl.reshape(h, w).astype(np.uint8), 3)
    q = cv2.cvtColor(ctr[lbl].astype(np.uint8), cv2.COLOR_LAB2BGR)

    # inkoustové linky
    g = cv2.cvtColor(lines_src, cv2.COLOR_BGR2GRAY)
    ln = xdog(g, sigma=1.4)
    ink = (ln < 0.5).astype(np.uint8) * 255
    gq = cv2.cvtColor(q, cv2.COLOR_BGR2GRAY)
    ink |= cv2.Canny(cv2.GaussianBlur(cv2.cvtColor(lines_src, cv2.COLOR_BGR2GRAY), (5, 5), 0), 70, 170)
    n, cc, st, _ = cv2.connectedComponentsWithStats(ink, 8)
    keep = np.zeros(n, bool)
    keep[1:] = st[1:, cv2.CC_STAT_AREA] >= 40
    ink = np.where(keep[cc], 255, 0).astype(np.uint8)
    ink = cv2.dilate(ink, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3)))
    a = cv2.GaussianBlur(ink, (3, 3), 0).astype(np.float32) / 255.0

    # rastr v tmavých plochách
    out = q.astype(np.float32)
    lum = cv2.cvtColor(q, cv2.COLOR_BGR2GRAY).astype(np.float32) / 255.0
    step = 6
    yy, xx = np.mgrid[0:h, 0:w]
    cy = (yy % step) - step / 2 + 0.5
    cx = ((xx + (yy // step % 2) * step // 2) % step) - step / 2 + 0.5
    dots = (np.sqrt(cx ** 2 + cy ** 2) < 1.3) & (lum < 0.3)
    out[dots] *= 0.6

    out = out * (1 - a[..., None]) + np.array([14, 10, 8], np.float32) * a[..., None]
    out = np.clip(out, 0, 255).astype(np.uint8)
    if not cv2.imwrite(dst, out, [cv2.IMWRITE_WEBP_QUALITY, 90] if dst.endswith(".webp") else []):
        raise SystemExit(f"Nelze zapsat {dst}")
    print("ok", dst)


if __name__ == "__main__":
    toon(sys.argv[1], sys.argv[2], int(sys.argv[3]) if len(sys.argv) > 3 else 40)
