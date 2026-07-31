"""Punch transparent center into artifact frame for Hall overlay."""
from PIL import Image
import os

src = r"C:\Users\RM\thunderwolf-citadel\assets\artifact-frame.jpg"
out = r"C:\Users\RM\thunderwolf-citadel\assets\artifact-frame-mask.png"

im = Image.open(src).convert("RGBA")
w, h = im.size
print("size", w, h)
px = im.load()


def near_black(r, g, b, thr=18):
    return r < thr and g < thr and b < thr


# Outer pure black → transparent
for y in range(h):
    for x in range(w):
        r, g, b, a = px[x, y]
        if near_black(r, g, b):
            px[x, y] = (0, 0, 0, 0)

# Inner content window (inside bronze rim) → transparent so HTML shows through
cx0, cx1 = int(w * 0.195), int(w * 0.805)
cy0, cy1 = int(h * 0.165), int(h * 0.835)
feather = max(6, int(min(w, h) * 0.01))

for y in range(cy0, cy1):
    for x in range(cx0, cx1):
        dl = x - cx0
        dr = cx1 - 1 - x
        dt = y - cy0
        db = cy1 - 1 - y
        d = min(dl, dr, dt, db)
        r, g, b, a = px[x, y]
        t = d / feather if feather else 1.0
        if t >= 1.0:
            px[x, y] = (r, g, b, 0)
        else:
            # anti-aliased hole edge
            new_a = int(a * (1.0 - t))
            px[x, y] = (r, g, b, new_a)

im.save(out, "PNG", optimize=True)
print("saved", out, os.path.getsize(out))
