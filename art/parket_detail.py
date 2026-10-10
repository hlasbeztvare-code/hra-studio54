# Parket: barevná a detailní verze (4. 10.) – původní fotka image3 ze studio54.cz,
# jemné komiksové linky místo rozmazání (bilateral/kmeans), ostřejší postavy.
import cv2, numpy as np
src = cv2.imread("art/web/image3.jpg")
img = cv2.resize(src, (1920, 1280), interpolation=cv2.INTER_LANCZOS4)
# doostření (unsharp) + lehce víc saturace a kontrastu
blur = cv2.GaussianBlur(img, (0, 0), 2.2)
img = cv2.addWeighted(img, 1.55, blur, -0.55, 0)
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV).astype(np.float32)
hsv[..., 1] = np.clip(hsv[..., 1] * 1.18, 0, 255)
hsv[..., 2] = np.clip((hsv[..., 2] - 128) * 1.08 + 132, 0, 255)
img = cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2BGR)
# tenké inkoustové obrysy (jen náznak komiksu, postavy zůstávají ostré)
g = cv2.cvtColor(cv2.resize(src, (1920, 1280)), cv2.COLOR_BGR2GRAY)
g = cv2.bilateralFilter(g, 7, 40, 7)
ed = cv2.Canny(g, 60, 140)
ed = cv2.GaussianBlur(ed.astype(np.float32), (0, 0), 0.7) / 255.0
img = (img.astype(np.float32) * (1 - 0.55 * ed[..., None])).clip(0, 255).astype(np.uint8)
cv2.imwrite("src/assets/5c23ba6d-25a4-4810-b4f1-e5a54b0ef638.webp", img, [cv2.IMWRITE_WEBP_QUALITY, 86])
print("ok")
