# -*- coding: utf-8 -*-
from pathlib import Path

p = Path(r"C:\Users\RM\thunderwolf-citadel\index.html")
t = p.read_text(encoding="utf-8")

old_media = """    .tile-media {
      position: relative;
      flex: 1 1 auto;
      min-height: 0;
      width: 100%;
      margin: 0;
      aspect-ratio: auto;
      overflow: hidden;
      background:
        radial-gradient(ellipse 75% 65% at 50% 42%, rgba(30, 50, 90, 0.45), #060a14 78%),
        url("assets/artifact-stone-tex.jpg") center / cover no-repeat;
      border-radius: 0;
      border: none;
      box-shadow:
        inset 0 0 36px rgba(46, 230, 255, 0.12),
        inset 0 0 50px rgba(0, 0, 0, 0.45);
    }"""

new_media = """    .tile-media {
      position: relative;
      flex: 1 1 74%;
      min-height: 62%;
      width: 100%;
      margin: 0;
      aspect-ratio: auto;
      overflow: hidden;
      background:
        radial-gradient(ellipse 75% 65% at 50% 42%, rgba(30, 50, 90, 0.45), #060a14 78%),
        url("assets/artifact-stone-tex.jpg") center / cover no-repeat;
      border-radius: 0;
      border: none;
      box-shadow:
        inset 0 0 20px rgba(46, 230, 255, 0.1),
        inset 0 0 32px rgba(0, 0, 0, 0.35);
    }"""

if old_media not in t:
    raise SystemExit("media block not found")
t = t.replace(old_media, new_media, 1)
print("media ok")

old_div = """    .artifact-divider {
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 0.35rem;
      margin: 0;
      padding: 0.2rem 0.4rem;
      flex: 0 0 auto;
      color: var(--cyan-soft);
      font-size: 0.72rem;
      line-height: 1;
      text-shadow: 0 0 10px rgba(46, 230, 255, 0.65);
      z-index: 2;
      background: linear-gradient(180deg, rgba(6, 10, 18, 0.2), rgba(8, 12, 20, 0.55));
    }"""

new_div = """    .artifact-divider {
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 0.25rem;
      margin: 0;
      padding: 0.06rem 0.25rem;
      flex: 0 0 auto;
      color: var(--cyan-soft);
      font-size: 0.5rem;
      line-height: 1;
      text-shadow: 0 0 10px rgba(46, 230, 255, 0.65);
      z-index: 2;
      background: linear-gradient(180deg, rgba(6, 10, 18, 0.12), rgba(8, 12, 20, 0.35));
    }"""

if old_div not in t:
    raise SystemExit("divider not found")
t = t.replace(old_div, new_div, 1)
print("divider ok")

# Inject compact plaque rules once
marker = "    /* Compact plaque — maximize hologram */"
if marker not in t:
    inject = """
    /* Compact plaque — maximize hologram */
    .tile .artifact-lore-row { display: none !important; }
    .tile .artifact-kicker { display: none !important; }
    .tile .tile-body {
      padding: 0.18rem 0.4rem 0.25rem !important;
      gap: 0.08rem !important;
      flex: 0 0 auto !important;
      max-height: 28%;
    }
    .tile .tile-title {
      font-size: clamp(0.66rem, 1.05vw, 0.8rem) !important;
      -webkit-line-clamp: 1 !important;
      line-height: 1.2 !important;
    }
    .tile .tile-footer {
      padding-top: 0.1rem !important;
      margin-top: 0.06rem !important;
    }
    .tile .tile-meta {
      margin-top: 0.04rem !important;
    }
    .tile .artifact-divider::before,
    .tile .artifact-divider::after {
      height: 1px !important;
    }

"""
    anchor = "    .tile-body {\n      /* Carved lower plate"
    if anchor not in t:
        # fallback: after tile-media img absolute
        anchor = "    .tile-media img {\n      position: absolute;"
        if anchor not in t:
            raise SystemExit("inject anchor not found")
    t = t.replace(anchor, inject + anchor, 1)
    print("compact inject ok")
else:
    print("compact already present")

p.write_text(t, encoding="utf-8")
print("done", len(t))
