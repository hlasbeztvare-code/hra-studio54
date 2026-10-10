# Realistický „graphic novel“ look z původních fotek:
# fotka zůstane reálná, dostane luxusní černo-zlatý filmový grade,
# jemné inkoustové linky a decentní rastr ve stínech → propojení s komiksovým UI.
import sys
import cv2
import numpy as np


def xdog(gray, sigma=0.9, k=1.6, p=18.0, eps=-0.05, phi=12.0):
    g = gray.astype(np.float32) / 255.0
    d = (1 + p) * cv2.GaussianBlur(g, (0, 0), sigma) - p * cv2.GaussianBlur(g, (0, 0), sigma * k)
    return np.clip(np.where(d >= eps, 1.0, 1.0 + np.tanh(phi * (d - eps))), 0, 1)


def lux(src, dst, ink_alpha=0.45, gold=0.55):
    img = cv2.imread(src, cv2.IMREAD_COLOR)
    if img is None:
        raise SystemExit(f"Nelze načíst {src}")
    h, w = img.shape[:2]

    # 1) jemné vyhlazení šumu (detail zůstává)
    base = cv2.bilateralFilter(img, 7, 30, 7)
    f = base.astype(np.float32) / 255.0

    # 2) filmový grade: hlubší černé, S-křivka
    lum = cv2.cvtColor(base, cv2.COLOR_BGR2GRAY).astype(np.float32) / 255.0
    curve = lambda x: np.clip(x * x * (3 - 2 * x) * 1.04 - 0.02, 0, 1)
    lum_c = curve(np.clip((lum - 0.04) * 1.08, 0, 1))

    # 3) luxusní černo-zlatý split-tone (stíny teplá čerň, světla zlato/šampaňské)
    stops = np.array([0.0, 0.25, 0.55, 0.8, 1.0], np.float32)
    cols = np.array([[6, 7, 9], [14, 30, 52], [40, 105, 170], [90, 190, 240], [190, 230, 252]], np.float32)  # BGR
    gm = np.stack([np.interp(lum_c, stops, cols[:, c]) for c in range(3)], -1) / 255.0
    # původní barvy ztlumené, ať zůstane realita (červená, fialová), ale pod zlatým nádechem
    hsv = cv2.cvtColor(base, cv2.COLOR_BGR2HSV).astype(np.float32)
    hsv[..., 1] *= 0.55
    muted = cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2BGR).astype(np.float32) / 255.0
    ratio = (lum_c / np.maximum(lum, 1e-3))[..., None]
    muted = np.clip(muted * np.clip(ratio, 0.4, 1.6), 0, 1)
    out = muted * (1 - gold) + gm * gold

    # 4) bloom ve světlech (luxusní záře)
    hi = np.clip((lum_c - 0.7) / 0.3, 0, 1)[..., None] * out
    bloom = cv2.GaussianBlur(hi, (0, 0), 18)
    out = 1 - (1 - out) * (1 - bloom * 0.35)

    # 5) jemné inkoustové linky (komiksová kresba přes realitu)
    ln = xdog(cv2.cvtColor(base, cv2.COLOR_BGR2GRAY))
    ink = (1 - ln)
    ink = cv2.GaussianBlur(ink, (0, 0), 0.6)
    out = out * (1 - ink[..., None] * ink_alpha)

    # 6) rastr jen v polostínech
    step = 5
    yy, xx = np.mgrid[0:h, 0:w]
    cy = (yy % step) - step / 2 + 0.5
    cx = ((xx + (yy // step % 2) * step // 2) % step) - step / 2 + 0.5
    rad = np.sqrt(cx ** 2 + cy ** 2)
    m = (rad < (1 - lum_c) * 1.6) & (lum_c > 0.12) & (lum_c < 0.5)
    out[m] *= 0.82

    # 7) vinětace
    Y, X = np.ogrid[:h, :w]
    r = np.sqrt(((X - w / 2) / (w / 2)) ** 2 + ((Y - h / 2) / (h / 2)) ** 2)
    out *= np.clip(1.08 - 0.38 * r ** 2, 0.45, 1)[..., None]

    out = np.clip(out * 255, 0, 255).astype(np.uint8)
    params = [cv2.IMWRITE_WEBP_QUALITY, 90] if dst.endswith(".webp") else []
    if not cv2.imwrite(dst, out, params):
        raise SystemExit(f"Nelze zapsat {dst}")
    print("ok", dst)


if __name__ == "__main__":
    lux(sys.argv[1], sys.argv[2])
