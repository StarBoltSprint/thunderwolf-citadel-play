# -*- coding: utf-8 -*-
"""
Exact Pack border art, full design preserved, compressed into a TIGHTER rim.
Maps the full decorative band (stone + bronze + lightning + corners)
into a thinner outer rim so style is not lost.
"""
from pathlib import Path
import numpy as np
from PIL import Image

SRC = Path(r"C:\Users\RM\thunderwolf-citadel\assets\artifact-frame-exact.png")
OUT = Path(r"C:\Users\RM\thunderwolf-citadel\assets\artifact-frame-mask.png")

# Target rim thickness as fraction of the short side of the crop
# ~6.2% — a bit tighter than 7.5%, full design still remapped
TARGET_RIM = 0.062

im = Image.open(SRC).convert("RGBA")
a0 = np.array(im)
lum0 = np.maximum(
    np.maximum(a0[:, :, 0].astype(int), a0[:, :, 1].astype(int)),
    a0[:, :, 2].astype(int),
)
h0, w0 = a0.shape[:2]


def side_first(side: str) -> int:
    vals = []
    if side == "L":
        for y in range(int(h0 * 0.2), int(h0 * 0.8), 2):
            for x in range(w0 // 2):
                if lum0[y, x] > 42:
                    vals.append(x)
                    break
    elif side == "R":
        for y in range(int(h0 * 0.2), int(h0 * 0.8), 2):
            for x in range(w0 - 1, w0 // 2, -1):
                if lum0[y, x] > 42:
                    vals.append(x)
                    break
    elif side == "T":
        for x in range(int(w0 * 0.2), int(w0 * 0.8), 2):
            for y in range(h0 // 2):
                if lum0[y, x] > 42:
                    vals.append(y)
                    break
    else:
        for x in range(int(w0 * 0.2), int(w0 * 0.8), 2):
            for y in range(h0 - 1, h0 // 2, -1):
                if lum0[y, x] > 42:
                    vals.append(y)
                    break
    return int(np.median(vals)) if vals else 0


L = max(0, side_first("L") - 1)
R = min(w0 - 1, side_first("R") + 1)
T = max(0, side_first("T") - 1)
B = min(h0 - 1, side_first("B") + 1)
src = np.array(im.crop((L, T, R + 1, B + 1)).convert("RGBA"), dtype=np.float32)
sh, sw = src.shape[:2]

# Natural hole via flood from center on dark non-bronze
rr, gg, bb = src[:, :, 0], src[:, :, 1], src[:, :, 2]
lum = np.maximum(np.maximum(rr, gg), bb)
is_bronze = (rr > 85) & (rr > gg + 5) & (rr > bb + 8) & (gg > 35)
is_hole = ((lum < 36) & (~is_bronze)) | (src[:, :, 3] < 5)

from collections import deque

vis = np.zeros((sh, sw), dtype=bool)
q = deque([(sw // 2, sh // 2)])
vis[sh // 2, sw // 2] = True
while q:
    x, y = q.popleft()
    for nx, ny in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)):
        if 0 <= nx < sw and 0 <= ny < sh and not vis[ny, nx] and is_hole[ny, nx]:
            vis[ny, nx] = True
            q.append((nx, ny))

ys, xs = np.where(vis)
if len(xs) < 100:
    nx0, ny0, nx1, ny1 = int(sw * 0.18), int(sh * 0.16), int(sw * 0.82), int(sh * 0.84)
else:
    nx0, nx1 = int(xs.min()) + 2, int(xs.max()) - 2
    ny0, ny1 = int(ys.min()) + 2, int(ys.max()) - 2

# Natural rim depths (full decorative band)
nat_l, nat_r = max(8, nx0), max(8, sw - nx1)
nat_t, nat_b = max(8, ny0), max(8, sh - ny1)
print(f"source {sw}x{sh} natural rim LTRB {nat_l},{nat_t},{nat_r},{nat_b}")

# Output canvas same aspect, punch tighter hole; remap rim samples from full band
out_w, out_h = sw, sh
tgt = max(22, int(min(out_w, out_h) * TARGET_RIM))
print(f"target rim px={tgt} ({100*tgt/min(out_w,out_h):.1f}%)")

out = np.zeros((out_h, out_w, 4), dtype=np.float32)
yy, xx = np.mgrid[0:out_h, 0:out_w]

# Distance to nearest outer edge
d_left = xx.astype(np.float32)
d_right = (out_w - 1 - xx).astype(np.float32)
d_top = yy.astype(np.float32)
d_bot = (out_h - 1 - yy).astype(np.float32)
d_edge = np.minimum(np.minimum(d_left, d_right), np.minimum(d_top, d_bot))

in_rim = d_edge < tgt
# Normalized position in thin rim [0 outer .. 1 inner]
t = np.clip(d_edge / float(tgt), 0, 1)

# Map to natural rim: sample at depth t * nat_rim along same edge normal
# For each pixel, determine dominant edge and sample source
# Left-dominant
use_l = (d_left <= d_right) & (d_left <= d_top) & (d_left <= d_bot)
use_r = (d_right < d_left) & (d_right <= d_top) & (d_right <= d_bot)
use_t = (d_top < d_left) & (d_top < d_right) & (d_top <= d_bot)
use_b = ~(use_l | use_r | use_t)

sx = xx.astype(np.float32).copy()
sy = yy.astype(np.float32).copy()

# Left edge: sample x = t * nat_l, y proportional
sx = np.where(use_l, t * nat_l, sx)
# Right edge: sample x = sw-1 - t*nat_r
sx = np.where(use_r, (sw - 1) - t * nat_r, sx)
# Top: y = t * nat_t
sy = np.where(use_t, t * nat_t, sy)
# Bottom: y = sh-1 - t*nat_b
sy = np.where(use_b, (sh - 1) - t * nat_b, sy)

# For corners, blend two edges for smoother ornaments
# corner left-top
c_lt = (d_left < tgt) & (d_top < tgt)
c_rt = (d_right < tgt) & (d_top < tgt)
c_lb = (d_left < tgt) & (d_bot < tgt)
c_rb = (d_right < tgt) & (d_bot < tgt)

# corner sample: bilinear of the two edge positions in source
def clamp_xy(x, y):
    return (
        np.clip(x, 0, sw - 1.001),
        np.clip(y, 0, sh - 1.001),
    )


# rebuild corner samples: x from side rim, y from top/bot rim
sx_lt, sy_lt = t * nat_l, t * nat_t
sx_rt, sy_rt = (sw - 1) - t * nat_r, t * nat_t
sx_lb, sy_lb = t * nat_l, (sh - 1) - t * nat_b
sx_rb, sy_rb = (sw - 1) - t * nat_r, (sh - 1) - t * nat_b

# Mix corners by which edge is closer
wl = 1.0 / (d_left + 0.5)
wr = 1.0 / (d_right + 0.5)
wt = 1.0 / (d_top + 0.5)
wb = 1.0 / (d_bot + 0.5)

# left-top corner blend
den = wl + wt
sx = np.where(c_lt, (wl * (t * nat_l) + wt * xx) / den, sx)  # imperfect
# Better corner: sample source at (t*nat_l, t*nat_t) for LT
sx = np.where(c_lt, t * nat_l, sx)
sy = np.where(c_lt, t * nat_t, sy)
sx = np.where(c_rt, (sw - 1) - t * nat_r, sx)
sy = np.where(c_rt, t * nat_t, sy)
sx = np.where(c_lb, t * nat_l, sx)
sy = np.where(c_lb, (sh - 1) - t * nat_b, sy)
sx = np.where(c_rb, (sw - 1) - t * nat_r, sx)
sy = np.where(c_rb, (sh - 1) - t * nat_b, sy)

# Non-corner edges: keep constant along the long axis
# left edge (not corner): x = t*nat_l, y = y
sx = np.where(use_l & ~c_lt & ~c_lb, t * nat_l, sx)
sy = np.where(use_l & ~c_lt & ~c_lb, yy, sy)
sx = np.where(use_r & ~c_rt & ~c_rb, (sw - 1) - t * nat_r, sx)
sy = np.where(use_r & ~c_rt & ~c_rb, yy, sy)
sx = np.where(use_t & ~c_lt & ~c_rt, xx, sx)
sy = np.where(use_t & ~c_lt & ~c_rt, t * nat_t, sy)
sx = np.where(use_b & ~c_lb & ~c_rb, xx, sx)
sy = np.where(use_b & ~c_lb & ~c_rb, (sh - 1) - t * nat_b, sy)

sx, sy = clamp_xy(sx, sy)

# Bilinear sample
x0 = np.floor(sx).astype(np.int32)
y0 = np.floor(sy).astype(np.int32)
x1 = np.clip(x0 + 1, 0, sw - 1)
y1 = np.clip(y0 + 1, 0, sh - 1)
x0 = np.clip(x0, 0, sw - 1)
y0 = np.clip(y0, 0, sh - 1)
fx = (sx - x0).astype(np.float32)[..., None]
fy = (sy - y0).astype(np.float32)[..., None]

Ia = src[y0, x0]
Ib = src[y0, x1]
Ic = src[y1, x0]
Id = src[y1, x1]
sampled = (
    Ia * (1 - fx) * (1 - fy)
    + Ib * fx * (1 - fy)
    + Ic * (1 - fx) * fy
    + Id * fx * fy
)

out[in_rim] = sampled[in_rim]

# Transparent center + outer pure black
out[~in_rim, 3] = 0
# ensure void blacks transparent
black = (out[:, :, 0] < 14) & (out[:, :, 1] < 14) & (out[:, :, 2] < 16)
out[black, 3] = 0

# Soft inner edge of rim
feather = max(2, int(tgt * 0.12))
inner = (d_edge >= tgt - feather) & (d_edge < tgt)
fade = (tgt - d_edge[inner]) / float(feather)
out[inner, 3] = out[inner, 3] * fade

# Slight contrast
m = out[:, :, 3] > 40
rgb = out[:, :, :3]
rgb[m] = np.clip((rgb[m] - 128) * 1.06 + 128, 0, 255)
out[:, :, :3] = rgb

img = Image.fromarray(np.clip(out, 0, 255).astype(np.uint8), "RGBA")
img.save(OUT, "PNG", optimize=True)
print("saved", OUT, OUT.stat().st_size)
inset = 100 * tgt / min(out_w, out_h)
print(f"CSS inset ~ {inset:.2f}%")
print(f"--artifact-inset-t: {100*tgt/out_h:.2f}%;")
print(f"--artifact-inset-x: {100*tgt/out_w:.2f}%;")
print(f"--artifact-inset-b: {100*tgt/out_h:.2f}%;")
for p in [(tgt // 2, out_h // 2), (out_w // 2, tgt // 2), (tgt // 3, tgt // 3), (out_w // 2, out_h // 2)]:
    print(p, img.getpixel(p))
