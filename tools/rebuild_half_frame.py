# -*- coding: utf-8 -*-
"""
Thin artifact rim (~5.3%): OUTER half bronze fittings, INNER half stone + lightning.
Same total border width — dual material like stele / Stormcaller refs.
"""
from pathlib import Path
import numpy as np
from PIL import Image

src = Path(r"C:\Users\RM\thunderwolf-citadel\assets\artifact-frame.jpg")
stone_src = Path(r"C:\Users\RM\thunderwolf-citadel\assets\artifact-stone-tex.jpg")
out = Path(r"C:\Users\RM\thunderwolf-citadel\assets\artifact-frame-mask.png")

im = Image.open(src).convert("RGBA")
arr0 = np.array(im)
r, g, b = arr0[:, :, 0].astype(int), arr0[:, :, 1].astype(int), arr0[:, :, 2].astype(int)
h0, w0 = arr0.shape[:2]


def is_bronze(rr, gg, bb):
    return (
        (rr > 100 and rr > gg + 10 and rr > bb + 15 and gg > 50 and gg < 185 and bb < 125)
        or (rr > 155 and gg > 105 and bb < 145 and rr > gg and (rr - bb) > 40)
    )


lefts, rights, tops, bots = [], [], [], []
for y in range(int(h0 * 0.15), int(h0 * 0.85)):
    for x in range(0, w0 // 3):
        if is_bronze(r[y, x], g[y, x], b[y, x]):
            lefts.append(x)
            break
    for x in range(w0 - 1, w0 * 2 // 3, -1):
        if is_bronze(r[y, x], g[y, x], b[y, x]):
            rights.append(x)
            break
for x in range(int(w0 * 0.15), int(w0 * 0.85)):
    for y in range(int(h0 * 0.15), int(h0 * 0.85)):
        pass
for x in range(int(w0 * 0.15), int(w0 * 0.85)):
    for y in range(0, h0 // 3):
        if is_bronze(r[y, x], g[y, x], b[y, x]):
            tops.append(y)
            break
    for y in range(h0 - 1, h0 * 2 // 3, -1):
        if is_bronze(r[y, x], g[y, x], b[y, x]):
            bots.append(y)
            break

L = max(0, int(np.median(lefts)) - 2)
T = max(0, int(np.median(tops)) - 2)
R = min(w0 - 1, int(np.median(rights)) + 2)
B = min(h0 - 1, int(np.median(bots)) + 2)

crop = im.crop((L, T, R + 1, B + 1)).convert("RGBA")
w, h = crop.size
frame = np.array(crop, dtype=np.float32).copy()

# Stone texture for inner half of rim
if stone_src.exists():
    stone = Image.open(stone_src).convert("RGB").resize((w, h), Image.Resampling.LANCZOS)
    stone_a = np.array(stone, dtype=np.float32)
else:
    stone_a = np.stack(
        [
            np.full((h, w), 55, np.float32),
            np.full((h, w), 58, np.float32),
            np.full((h, w), 62, np.float32),
        ],
        axis=-1,
    )

# Procedural cyan/gold lightning cracks (thin veins)
yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
# a few diagonal crack fields
crack = (
    np.sin((xx * 0.11 + yy * 0.19) * 1.7) * np.sin((xx * 0.07 - yy * 0.13) * 2.3)
    + np.sin((xx * 0.21 - yy * 0.05) * 3.1) * 0.55
)
crack = (crack - crack.min()) / (crack.max() - crack.min() + 1e-6)
vein = (crack > 0.72).astype(np.float32)
vein = vein * (0.55 + 0.45 * crack)
# gold vs cyan by region
gold_m = ((xx + yy) % 97 > 48).astype(np.float32)
cyan_m = 1.0 - gold_m

# Rim geometry
rim = max(34, int(min(w, h) * 0.054))
half = rim // 2  # outer bronze | inner stone
print("rim", rim, "half", half, "pct", round(100 * rim / w, 2), "size", w, h)

dist_from_edge = np.minimum(np.minimum(xx, w - 1 - xx), np.minimum(yy, h - 1 - yy))
in_rim = dist_from_edge < rim
outer_half = dist_from_edge < half  # bronze fittings zone
inner_half = in_rim & ~outer_half  # stone + lightning zone

# Soft blend between halves
blend = np.clip((dist_from_edge - (half - 2)) / 5.0, 0, 1)  # 0 outer → 1 inner
blend = blend * in_rim.astype(np.float32)

# Build composite RGB in rim
bronze_rgb = frame[:, :, :3].copy()
# enrich bronze slightly
br_boost = bronze_rgb.copy()
br_boost[:, :, 0] = np.clip(br_boost[:, :, 0] * 1.05 + 6, 0, 255)
br_boost[:, :, 1] = np.clip(br_boost[:, :, 1] * 1.02 + 2, 0, 255)

stone_rgb = stone_a.copy()
stone_rgb = stone_rgb * 0.72 + np.array([28, 32, 38], dtype=np.float32)  # darker citadel stone
# add lightning veins on stone
stone_rgb[:, :, 0] = np.clip(stone_rgb[:, :, 0] + vein * gold_m * 160 + vein * cyan_m * 30, 0, 255)
stone_rgb[:, :, 1] = np.clip(stone_rgb[:, :, 1] + vein * gold_m * 110 + vein * cyan_m * 180, 0, 255)
stone_rgb[:, :, 2] = np.clip(stone_rgb[:, :, 2] + vein * gold_m * 40 + vein * cyan_m * 220, 0, 255)

# Mix: outer stays bronze from art, inner becomes stone+lightning (blend soft)
for c in range(3):
    frame[:, :, c] = np.where(
        in_rim,
        br_boost[:, :, c] * (1.0 - blend) + stone_rgb[:, :, c] * blend,
        frame[:, :, c],
    )

# Keep original bronze ornaments stronger on very outer 30% of rim (corners/rails)
outer_w = np.clip(1.0 - dist_from_edge / max(half, 1), 0, 1) * in_rim.astype(np.float32)
for c in range(3):
    frame[:, :, c] = frame[:, :, c] * (1.0 - outer_w * 0.35) + br_boost[:, :, c] * (outer_w * 0.35)

# Alpha: transparent black + punch hole
near_black = (frame[:, :, 0] < 18) & (frame[:, :, 1] < 18) & (frame[:, :, 2] < 18)
frame[:, :, 3] = np.where(near_black, 0, frame[:, :, 3])

cx0, cy0, cx1, cy1 = rim, rim, w - rim, h - rim
inside = (xx >= cx0) & (xx < cx1) & (yy >= cy0) & (yy < cy1)
d = np.minimum(
    np.minimum(xx - cx0, cx1 - 1 - xx),
    np.minimum(yy - cy0, cy1 - 1 - yy),
)
feather = max(2, int(min(w, h) * 0.004))
alpha = frame[:, :, 3].copy()
alpha[inside & (d >= feather)] = 0
edge = inside & (d < feather)
t = d[edge] / feather
alpha[edge] = alpha[edge] * (1.0 - t)
frame[:, :, 3] = alpha

out_im = Image.fromarray(np.clip(frame, 0, 255).astype(np.uint8), "RGBA")
out_im.save(out, "PNG", optimize=True)
print("saved", out.stat().st_size)
print("CSS inset", round(100 * (rim - 2) / w, 2))
for x in [3, half // 2, half + 2, rim - 4]:
    print("x", x, out_im.getpixel((int(x), h // 2)))
