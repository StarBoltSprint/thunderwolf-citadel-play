# -*- coding: utf-8 -*-
"""Patch Hall feed: Artifacts + Relics same surface."""
from pathlib import Path

p = Path(r"C:\Users\RM\thunderwolf-citadel\index.html")
t = p.read_text(encoding="utf-8")

# ── 1) Toolbar: vessel chips ─────────────────────────────────────────
old_tb = """        <div class="filter-row" id="sortFilters">
          <button type="button" class="chip active" data-sort="new">New</button>
          <button type="button" class="chip" data-sort="rising">Rising</button>
        </div>
        <div class="filter-row" id="typeFilters">
          <button type="button" class="chip active" data-type="all">All</button>"""

new_tb = """        <div class="filter-row" id="sortFilters">
          <button type="button" class="chip active" data-sort="new">New</button>
          <button type="button" class="chip" data-sort="rising">Rising</button>
        </div>
        <div class="filter-row" id="vesselFilters" aria-label="Vessel kind">
          <button type="button" class="chip active" data-vessel="all">All</button>
          <button type="button" class="chip" data-vessel="artifact">Artifacts</button>
          <button type="button" class="chip" data-vessel="relic">Relics</button>
        </div>
        <div class="filter-row" id="typeFilters">
          <button type="button" class="chip active" data-type="all">All types</button>"""

if old_tb not in t:
    raise SystemExit("toolbar block not found")
t = t.replace(old_tb, new_tb, 1)
print("toolbar ok")

# ── 2) Relic modal HTML after detailModal ────────────────────────────
old_detail_end = """  <!-- Play arena -->
  <div class="modal-overlay play-modal" id="playModal\""""

new_detail_end = """  <!-- Relic View — Origin + children in one denser vessel -->
  <div class="modal-overlay" id="relicModal" role="dialog" aria-modal="true" aria-labelledby="relicTitle">
    <div class="modal modal-relic">
      <div class="modal-head">
        <h2 class="modal-title" id="relicTitle">Relic</h2>
        <button type="button" class="close-btn" data-close-relic aria-label="Close">&times;</button>
      </div>
      <div class="relic-hero" id="relicHero"></div>
      <div id="relicContent" class="detail-body"></div>
      <div class="form-actions">
        <button type="button" class="btn btn-ghost" data-close-relic>Close</button>
        <button type="button" class="btn-play" id="relicPlayOrigin">
          <img src="assets/play-wolf.jpg" alt="" width="28" height="28" />
          <span>Play Origin</span>
        </button>
      </div>
    </div>
  </div>

  <!-- Play arena -->
  <div class="modal-overlay play-modal" id="playModal\""""

if old_detail_end not in t:
    raise SystemExit("detail modal end not found")
t = t.replace(old_detail_end, new_detail_end, 1)
print("relic modal ok")

# ── 3) CSS for relic cards + modal ───────────────────────────────────
css_anchor = "    .feed-grid {"
css_insert = """
    /* ── Relic vessels in the same Hall feed ── */
    .tile.is-relic {
      grid-column: span 2;
      --frame-glow: rgba(232, 197, 106, 0.42);
      --frame-filter: saturate(1.12) brightness(1.04) contrast(1.06);
    }
    @media (max-width: 700px) {
      .tile.is-relic { grid-column: span 1; }
    }
    .tile.is-relic .artifact-inner {
      background:
        radial-gradient(ellipse 80% 60% at 50% 30%, rgba(232, 197, 106, 0.08), transparent 55%),
        #0a0c12;
    }
    .tile.is-relic .tile-title {
      color: #ffe9a8 !important;
      text-shadow:
        0 1px 2px rgba(0, 0, 0, 0.95),
        0 0 16px rgba(232, 197, 106, 0.35) !important;
    }
    .tile.is-relic .tile-resonance {
      border-color: rgba(232, 197, 106, 0.55);
      color: #f5e0a8;
      box-shadow: 0 0 16px rgba(232, 197, 106, 0.25);
    }
    .badge-relic {
      background: linear-gradient(135deg, rgba(60, 40, 10, 0.95), rgba(30, 20, 6, 0.95));
      color: #f5e0a8;
      border-color: rgba(232, 197, 106, 0.55);
      box-shadow: 0 0 12px rgba(232, 197, 106, 0.25);
    }
    .badge-origin {
      background: rgba(12, 28, 48, 0.9);
      color: #9eecff;
      border-color: rgba(46, 230, 255, 0.4);
    }
    .relic-lineage {
      display: flex;
      flex-wrap: wrap;
      gap: 0.25rem;
      margin-top: 0.15rem;
    }
    .relic-lineage span {
      font-size: 0.55rem;
      font-weight: 700;
      letter-spacing: 0.04em;
      text-transform: uppercase;
      color: rgba(200, 220, 240, 0.75);
      padding: 0.1rem 0.35rem;
      border-radius: 999px;
      border: 1px solid rgba(46, 230, 255, 0.15);
      background: rgba(0, 0, 0, 0.25);
      max-width: 7rem;
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap;
    }
    .tile.is-relic .play-btn {
      background: linear-gradient(135deg, rgba(40, 28, 8, 0.95), rgba(20, 14, 4, 0.95));
      border-color: rgba(232, 197, 106, 0.5);
      color: #f5e0a8;
    }
    .modal-relic {
      max-width: min(720px, 96vw);
    }
    .relic-hero {
      position: relative;
      aspect-ratio: 16 / 9;
      overflow: hidden;
      border-radius: 12px;
      margin: 0 1rem;
      border: 1px solid rgba(232, 197, 106, 0.35);
      box-shadow: 0 0 28px rgba(232, 197, 106, 0.12);
      background: #060a12;
    }
    .relic-hero img {
      width: 100%;
      height: 100%;
      object-fit: cover;
      display: block;
    }
    .relic-members {
      display: grid;
      gap: 0.55rem;
      margin-top: 0.85rem;
    }
    .relic-member {
      display: grid;
      grid-template-columns: 56px 1fr auto;
      gap: 0.65rem;
      align-items: center;
      padding: 0.5rem 0.6rem;
      border-radius: 12px;
      border: 1px solid rgba(46, 230, 255, 0.14);
      background: rgba(8, 14, 28, 0.75);
      cursor: pointer;
      transition: border-color 0.15s, box-shadow 0.15s, transform 0.15s;
    }
    .relic-member:hover {
      border-color: rgba(232, 197, 106, 0.45);
      box-shadow: 0 0 18px rgba(232, 197, 106, 0.12);
      transform: translateY(-1px);
    }
    .relic-member.is-origin {
      border-color: rgba(232, 197, 106, 0.4);
      background: linear-gradient(135deg, rgba(40, 28, 8, 0.55), rgba(8, 14, 28, 0.85));
    }
    .relic-member__thumb {
      width: 56px;
      height: 56px;
      border-radius: 8px;
      overflow: hidden;
      background: #061018;
    }
    .relic-member__thumb img {
      width: 100%;
      height: 100%;
      object-fit: cover;
      display: block;
    }
    .relic-member__meta b {
      display: block;
      font-size: 0.88rem;
      color: var(--text);
      margin-bottom: 0.15rem;
    }
    .relic-member__meta span {
      font-size: 0.72rem;
      color: var(--text-dim);
    }
    .relic-member__res {
      font-weight: 800;
      font-size: 0.85rem;
      color: var(--mint);
      font-family: var(--font-display);
    }
    #vesselFilters .chip[data-vessel="relic"].active {
      border-color: rgba(232, 197, 106, 0.55);
      color: #f5e0a8;
      box-shadow: 0 0 14px rgba(232, 197, 106, 0.2);
    }

"""
if "tile.is-relic" not in t:
    if css_anchor not in t:
        raise SystemExit("feed-grid css anchor not found")
    t = t.replace(css_anchor, css_insert + css_anchor, 1)
    print("css ok")
else:
    print("css already present")

# ── 4) RELICS data after SEED ────────────────────────────────────────
old_seed_end = """      },
    ];

    /** 6 columns × 10 rows per feed page (pump.fun-style paging) */
    const FEED_COLS = 6;"""

new_seed_end = """      },
    ];

    /**
     * Relics — denser nodes in the SAME Hall feed.
     * vessel: "relic" · originId + childIds form the lineage.
     * Relic Resonance is computed from Origin + children.
     */
    const RELICS = [
      {
        id: "relic-storm-lineage",
        vessel: "relic",
        title: "Storm Orbs Relic",
        description: "The first lightning Mini-Quest grew into a living lineage — sprints, wings, and howls that share the storm.",
        creator: "Forge Hero · SmiR",
        originId: "seed-1",
        childIds: ["seed-7", "seed-3", "seed-4"],
        image: null,
        createdAt: Date.now() - 1000 * 60 * 60 * 5,
        tags: ["storm", "lineage", "relic"],
      },
      {
        id: "relic-silent-seed",
        vessel: "relic",
        title: "Silent Seed Relic",
        description: "From one dormant Guardian seed — codex, crystal ladders, and story branches under ice.",
        creator: "Lore Weaver · Ara",
        originId: "seed-2",
        childIds: ["seed-5", "seed-6", "seed-8"],
        image: null,
        createdAt: Date.now() - 1000 * 60 * 60 * 18,
        tags: ["seed", "guardian", "relic"],
      },
      {
        id: "relic-decree-chain",
        vessel: "relic",
        title: "Decree Chain Relic",
        description: "Official law that grew: torch, sky laws, and the council orb bind as one living decree lineage.",
        creator: "Thread Keeper · SmiR",
        originId: "decree-23",
        childIds: ["decree-24", "decree-25", "decree-26"],
        image: null,
        createdAt: Date.now() - 1000 * 60 * 12,
        tags: ["decree", "law", "relic"],
      },
    ];

    /** 6 columns × 10 rows per feed page (pump.fun-style paging) */
    const FEED_COLS = 6;"""

if "RELICS =" not in t:
    if old_seed_end not in t:
        raise SystemExit("SEED end not found")
    t = t.replace(old_seed_end, new_seed_end, 1)
    print("RELICS data ok")
else:
    print("RELICS already present")

# ── 5) state.vessel ──────────────────────────────────────────────────
old_state = """    let state = {
      sort: "new",
      type: "all",
      query: "",
      page: 1,"""
new_state = """    let state = {
      sort: "new",
      type: "all",
      vessel: "all",
      query: "",
      page: 1,"""
if "vessel: \"all\"" not in t and "vessel: 'all'" not in t:
    if old_state not in t:
        raise SystemExit("state block not found")
    t = t.replace(old_state, new_state, 1)
    print("state ok")
else:
    print("state vessel already")

# ── 6) Core JS helpers + allItems + filtered ─────────────────────────
old_all = """    function allItems() {
      const map = new Map();
      [...SEED, ...loadUserItems()].forEach((i) => map.set(i.id, ensureEngagement(i)));
      return [...map.values()];
    }"""

new_all = """    function isRelic(item) {
      return !!(item && (item.vessel === "relic" || item.type === "relic"));
    }

    function isArtifact(item) {
      return !!item && !isRelic(item);
    }

    function findItemById(id) {
      return allItems().find((i) => i.id === id) || null;
    }

    /** Members of a Relic: Origin first, then children (as live Artifacts). */
    function relicMembers(relic) {
      if (!relic) return [];
      const byId = new Map(allItemsRaw().map((i) => [i.id, i]));
      const ids = [relic.originId, ...(relic.childIds || [])].filter(Boolean);
      const seen = new Set();
      const out = [];
      ids.forEach((id) => {
        if (seen.has(id)) return;
        seen.add(id);
        const m = byId.get(id);
        if (m && !isRelic(m)) out.push(m);
      });
      return out;
    }

    /** Relic Resonance — denser lineage sorts higher in the same Hall ranking. */
    function computeRelicResonance(relic) {
      const members = relicMembers(relic);
      if (!members.length) return relic.resonance || 70;
      const avg = members.reduce((s, m) => s + (m.resonance || 0), 0) / members.length;
      const bonus = Math.min(18, members.length * 3);
      return Math.min(99, Math.round(avg + bonus));
    }

    function computeRelicHowls(relic) {
      return relicMembers(relic).reduce((s, m) => s + (m.howls || 0), 0);
    }

    function hydrateRelic(relic) {
      const members = relicMembers(relic);
      const origin = members.find((m) => m.id === relic.originId) || members[0] || null;
      const image = relic.image || (origin && origin.image) || "";
      const resonance = computeRelicResonance(relic);
      const howls = computeRelicHowls(relic);
      const views = members.reduce((s, m) => s + (m.views || 0), 0);
      return ensureEngagement({
        ...relic,
        vessel: "relic",
        type: "relic",
        title: relic.title,
        description: relic.description,
        creator: relic.creator || (origin && origin.creator) || "Pack",
        image,
        resonance,
        howls,
        views,
        plays: members.reduce((s, m) => s + (m.plays || 0), 0),
        featured: !!relic.featured || members.some((m) => m.featured),
        canon: relic.canon || (origin && origin.canon) || "community",
        createdAt: relic.createdAt || (origin && origin.createdAt) || Date.now(),
        memberCount: members.length,
        originTitle: origin ? origin.title : "Unknown Origin",
        tags: relic.tags || [],
      });
    }

    /** Artifacts only (no Relic vessels). */
    function allItemsRaw() {
      const map = new Map();
      [...SEED, ...loadUserItems()].forEach((i) => {
        if (isRelic(i)) return;
        map.set(i.id, ensureEngagement({ ...i, vessel: i.vessel || "artifact" }));
      });
      return [...map.values()];
    }

    function allItems() {
      const artifacts = allItemsRaw();
      const relics = (typeof RELICS !== "undefined" ? RELICS : []).map(hydrateRelic);
      const map = new Map();
      artifacts.forEach((i) => map.set(i.id, i));
      relics.forEach((i) => map.set(i.id, i));
      return [...map.values()];
    }"""

if "function hydrateRelic" not in t:
    if old_all not in t:
        raise SystemExit("allItems not found")
    t = t.replace(old_all, new_all, 1)
    print("allItems/relic helpers ok")
else:
    print("helpers already")

old_filtered = """    function filtered() {
      let list = allItems();
      if (state.type !== "all") list = list.filter((i) => i.type === state.type);
      if (state.sort === "featured") {
        const topIds = new Set(featuredItems().map((i) => i.id));
        list = list.filter((i) => topIds.has(i.id));
      }
      const q = state.query.trim().toLowerCase();
      if (q) {
        list = list.filter((i) => {
          const blob = [
            i.title,
            i.creator,
            i.description,
            typeLabel(i.type),
            typeShort(i.type),
            ...(i.tags || []),
          ].join(" ").toLowerCase();
          return blob.includes(q);
        });
      }
      if (state.sort === "rising") list = [...list].sort((a, b) => risingScore(b) - risingScore(a));
      else if (state.sort === "new") list = [...list].sort((a, b) => b.createdAt - a.createdAt);
      else list = [...list].sort((a, b) => b.resonance - a.resonance);
      return list;
    }"""

new_filtered = """    function filtered() {
      let list = allItems();
      /* Vessel kind: All | Artifacts | Relics (same Hall, filter only) */
      if (state.vessel === "artifact") list = list.filter(isArtifact);
      else if (state.vessel === "relic") list = list.filter(isRelic);
      /* Type chip — Artifacts by type; Relics if any member matches type */
      if (state.type !== "all") {
        list = list.filter((i) => {
          if (isRelic(i)) {
            return relicMembers(i).some((m) => m.type === state.type);
          }
          return i.type === state.type;
        });
      }
      if (state.sort === "featured") {
        const topIds = new Set(featuredItems().map((i) => i.id));
        list = list.filter((i) => topIds.has(i.id) || (isRelic(i) && i.featured));
      }
      const q = state.query.trim().toLowerCase();
      if (q) {
        list = list.filter((i) => {
          const blob = [
            i.title,
            i.creator,
            i.description,
            isRelic(i) ? "relic" : typeLabel(i.type),
            isRelic(i) ? "RELIC" : typeShort(i.type),
            i.originTitle || "",
            ...(i.tags || []),
          ].join(" ").toLowerCase();
          return blob.includes(q);
        });
      }
      if (state.sort === "rising") list = [...list].sort((a, b) => risingScore(b) - risingScore(a));
      else if (state.sort === "new") list = [...list].sort((a, b) => b.createdAt - a.createdAt);
      else list = [...list].sort((a, b) => b.resonance - a.resonance);
      return list;
    }"""

if "state.vessel === \"artifact\"" not in t:
    if old_filtered not in t:
        raise SystemExit("filtered not found")
    t = t.replace(old_filtered, new_filtered, 1)
    print("filtered ok")
else:
    print("filtered already")

# TYPE_META entry for relic - find TYPE_META
if '"relic"' not in t.split("TYPE_META")[1][:800] if "TYPE_META" in t else True:
    # inject into TYPE_META if pattern exists
    meta_mark = '      "remix":'
    # try common pattern
    for mark in [
        '      remix:',
        '      "remix":',
        "      remix:            {",
    ]:
        pass
    # Search for remix in TYPE_META
    import re
    m = re.search(r'(remix:\s*\{[^}]+\},?)', t)
    if m and "relic:" not in t[m.start() : m.start() + 200]:
        insert = m.group(1) + '\n      relic:             { label: "Relic",            emoji: "🏛️", short: "RELIC" },'
        # careful - might break if already has trailing
        t = t.replace(m.group(1), insert, 1)
        print("TYPE_META relic ok")
    else:
        print("TYPE_META skip or already")

# ── 7) renderFeed: dual card template ────────────────────────────────
# Replace the map callback body to branch on relic

old_map_start = """      feed.innerHTML = pageItems.map((item) => {
        const tier = borderTier(item);
        const tierName = borderTierLabel(tier);
        const flags = tileStateClasses(item, { trendingIds, myIdentity });
        const extraBadges = tileStateBadges(item, flags);
        const locked = !!item.locked;
        return `
          <article class="tile artifact ${borderClass(item)} ${isActivelyFeatured(item) ? "is-featured" : ""} ${flags.className}" data-id="${item.id}" role="listitem" title="${escapeAttr(flags.title || ("Artifact · " + tierName))}">"""

# We'll replace a larger chunk including the whole return template and click handler

old_render_chunk = """      feed.innerHTML = pageItems.map((item) => {
        const tier = borderTier(item);
        const tierName = borderTierLabel(tier);
        const flags = tileStateClasses(item, { trendingIds, myIdentity });
        const extraBadges = tileStateBadges(item, flags);
        const locked = !!item.locked;
        return `
          <article class="tile artifact ${borderClass(item)} ${isActivelyFeatured(item) ? "is-featured" : ""} ${flags.className}" data-id="${item.id}" role="listitem" title="${escapeAttr(flags.title || ("Artifact · " + tierName))}">
            <div class="artifact-inner">
              <div class="tile-media artifact-holo">
                ${mediaHtml(item)}
                <div class="tile-badge-row">
                  ${typeBadgeHtml(item)}
                  ${canonBadges(item)}
                  ${extraBadges}
                </div>
                <div class="tile-resonance">${item.resonance}</div>
              </div>
              <div class="artifact-divider" aria-hidden="true">⚡</div>
              <div class="tile-body">
                <div class="artifact-kicker">Artifact</div>
                <div class="tile-title" title="${escapeAttr(item.title)}">${escapeHtml(item.title)}</div>
                <div class="artifact-lore-row">
                  <div class="artifact-facts">
                    Rarity: <b>${escapeHtml(tierName)}</b><br />
                    Type: <b>${escapeHtml((TYPE_META[item.type] && TYPE_META[item.type].label) || item.type)}</b>
                  </div>
                  <div class="artifact-seal" title="Citadel seal" aria-hidden="true">🐺</div>
                </div>
                <div class="tile-meta tile-meta-clean">
                  <div class="tile-creator" title="Creator · ${escapeAttr(item.creator)}">
                    <span class="creator-by">by</span>
                    <span class="creator">
                      <span class="creator-ico" aria-hidden="true">✦</span>
                      <span class="creator-name">${escapeHtml(item.creator)}</span>
                    </span>
                  </div>
                  <button type="button" class="play-btn" data-play="${item.id}" title="${locked ? "Coming soon" : "Play"}" ${locked ? "disabled" : ""}>
                    <img src="assets/play-wolf.jpg" alt="" width="18" height="18" />
                    ${locked ? "Soon" : "Play"}
                  </button>
                </div>
              </div>
            </div>
            <div class="artifact-frame" aria-hidden="true"></div>
          </article>`;
      }).join("");

      feed.querySelectorAll(".tile").forEach((el) => {
        el.addEventListener("click", (e) => {
          if (e.target.closest("[data-play]") || e.target.closest("[data-howl]")) return;
          const id = el.dataset.id;
          const item = allItems().find((i) => i.id === id);
          if (item?.locked) {
            toast("Coming soon · fog still holds this spark");
            return;
          }
          openCardWithBeauty(el, id);
        });
      });
      feed.querySelectorAll("[data-play]").forEach((btn) => {
        btn.addEventListener("click", (e) => {
          e.stopPropagation();
          const id = btn.dataset.play;
          const tile = btn.closest(".tile");
          flashPlayEnergy(btn, tile);
          pulseTilePress(tile, () => launchPlay(id));
        });
      });"""

new_render_chunk = """      feed.innerHTML = pageItems.map((item) => {
        if (isRelic(item)) return relicCardHtml(item, { trendingIds, myIdentity });
        return artifactCardHtml(item, { trendingIds, myIdentity });
      }).join("");

      feed.querySelectorAll(".tile").forEach((el) => {
        el.addEventListener("click", (e) => {
          if (e.target.closest("[data-play]") || e.target.closest("[data-howl]") || e.target.closest("[data-open-relic]")) return;
          const id = el.dataset.id;
          const item = allItems().find((i) => i.id === id);
          if (item?.locked) {
            toast("Coming soon · fog still holds this spark");
            return;
          }
          if (isRelic(item)) {
            openCardWithBeauty(el, id, { relic: true });
            return;
          }
          openCardWithBeauty(el, id);
        });
      });
      feed.querySelectorAll("[data-open-relic]").forEach((btn) => {
        btn.addEventListener("click", (e) => {
          e.stopPropagation();
          const id = btn.dataset.openRelic;
          const tile = btn.closest(".tile");
          openCardWithBeauty(tile, id, { relic: true });
        });
      });
      feed.querySelectorAll("[data-play]").forEach((btn) => {
        btn.addEventListener("click", (e) => {
          e.stopPropagation();
          const id = btn.dataset.play;
          const tile = btn.closest(".tile");
          flashPlayEnergy(btn, tile);
          pulseTilePress(tile, () => launchPlay(id));
        });
      });"""

if "function artifactCardHtml" not in t:
    if old_render_chunk not in t:
        raise SystemExit("renderFeed chunk not found")
    t = t.replace(old_render_chunk, new_render_chunk, 1)
    print("renderFeed ok")
else:
    print("renderFeed already")

# Insert card HTML builders before renderFeed
builders = r'''
    function artifactCardHtml(item, ctx = {}) {
      const tier = borderTier(item);
      const tierName = borderTierLabel(tier);
      const flags = tileStateClasses(item, ctx);
      const extraBadges = tileStateBadges(item, flags);
      const locked = !!item.locked;
      return `
          <article class="tile artifact ${borderClass(item)} ${isActivelyFeatured(item) ? "is-featured" : ""} ${flags.className}" data-id="${item.id}" data-vessel="artifact" role="listitem" title="${escapeAttr(flags.title || ("Artifact · " + tierName))}">
            <div class="artifact-inner">
              <div class="tile-media artifact-holo">
                ${mediaHtml(item)}
                <div class="tile-badge-row">
                  ${typeBadgeHtml(item)}
                  ${canonBadges(item)}
                  ${extraBadges}
                </div>
                <div class="tile-resonance" title="Resonance">${item.resonance}</div>
              </div>
              <div class="artifact-divider" aria-hidden="true">⚡</div>
              <div class="tile-body">
                <div class="tile-title" title="${escapeAttr(item.title)}">${escapeHtml(item.title)}</div>
                <div class="tile-meta tile-meta-clean">
                  <div class="tile-creator" title="Creator · ${escapeAttr(item.creator)}">
                    <span class="creator-by">by</span>
                    <span class="creator">
                      <span class="creator-ico" aria-hidden="true">✦</span>
                      <span class="creator-name">${escapeHtml(item.creator)}</span>
                    </span>
                  </div>
                  <button type="button" class="play-btn" data-play="${item.id}" title="${locked ? "Coming soon" : "Play"}" ${locked ? "disabled" : ""}>
                    <img src="assets/play-wolf.jpg" alt="" width="18" height="18" />
                    ${locked ? "Soon" : "Play"}
                  </button>
                </div>
              </div>
            </div>
            <div class="artifact-frame" aria-hidden="true"></div>
          </article>`;
    }

    function relicCardHtml(item, ctx = {}) {
      const members = relicMembers(item);
      const origin = members.find((m) => m.id === item.originId) || members[0];
      const locked = !!item.locked;
      const lineage = members.slice(0, 4).map((m) =>
        `<span title="${escapeAttr(m.title)}">${escapeHtml(m.title)}</span>`
      ).join("");
      const more = members.length > 4 ? `<span>+${members.length - 4}</span>` : "";
      return `
          <article class="tile artifact is-relic ${borderClass(item)} ${item.featured ? "is-featured" : ""}" data-id="${item.id}" data-vessel="relic" role="listitem" title="${escapeAttr("Relic · " + item.title)}">
            <div class="artifact-inner">
              <div class="tile-media artifact-holo">
                ${mediaHtml(item)}
                <div class="tile-badge-row">
                  <span class="badge badge-relic">Relic</span>
                  <span class="badge badge-origin">Origin</span>
                  ${item.featured ? '<span class="badge badge-featured">Featured</span>' : ""}
                </div>
                <div class="tile-resonance" title="Relic Resonance">${item.resonance}</div>
              </div>
              <div class="artifact-divider" aria-hidden="true">⚡</div>
              <div class="tile-body">
                <div class="tile-title" title="${escapeAttr(item.title)}">${escapeHtml(item.title)}</div>
                <div class="relic-lineage" aria-label="Lineage">
                  ${lineage}${more}
                </div>
                <div class="tile-meta tile-meta-clean">
                  <div class="tile-creator" title="Origin · ${escapeAttr(item.originTitle || "")}">
                    <span class="creator-by">${members.length} linked</span>
                    <span class="creator">
                      <span class="creator-ico" aria-hidden="true">✦</span>
                      <span class="creator-name">${escapeHtml(item.creator)}</span>
                    </span>
                  </div>
                  <button type="button" class="play-btn" data-open-relic="${item.id}" title="Open Relic">
                    <img src="assets/play-wolf.jpg" alt="" width="18" height="18" />
                    Open
                  </button>
                </div>
              </div>
            </div>
            <div class="artifact-frame" aria-hidden="true"></div>
          </article>`;
    }

'''

if "function relicCardHtml" not in t:
    anchor = "    function renderFeed() {"
    if anchor not in t:
        raise SystemExit("renderFeed anchor not found for builders")
    t = t.replace(anchor, builders + anchor, 1)
    print("card builders ok")
else:
    print("builders already")

# ── 8) openCardWithBeauty + openRelicView ────────────────────────────
old_beauty = """    function openCardWithBeauty(tileEl, id) {
      if (!id) return;
      if (prefersReducedMotion() || !tileEl) {
        openDetail(id);
        return;
      }"""

new_beauty = """    function openCardWithBeauty(tileEl, id, opts = {}) {
      if (!id) return;
      const go = () => {
        if (opts.relic || isRelic(findItemById(id))) openRelicView(id);
        else openDetail(id);
      };
      if (prefersReducedMotion() || !tileEl) {
        go();
        return;
      }"""

if "opts = {}" not in t.split("function openCardWithBeauty")[1][:200]:
    if old_beauty not in t:
        raise SystemExit("openCardWithBeauty not found")
    t = t.replace(old_beauty, new_beauty, 1)
    # also replace openDetail(id) at end of timeout
    t = t.replace(
        """      window.setTimeout(() => {
        fx.remove();
        borderRun.remove();
        tileEl.classList.remove("is-opening");
        openDetail(id);
      }, 880);
    }
    function flashPlayEnergy(btn, tile) {""",
        """      window.setTimeout(() => {
        fx.remove();
        borderRun.remove();
        tileEl.classList.remove("is-opening");
        go();
      }, 880);
    }
    function flashPlayEnergy(btn, tile) {""",
        1,
    )
    print("openCardWithBeauty ok")
else:
    print("openCardWithBeauty already")

relic_view_fn = r'''
    function closeRelicView() {
      document.getElementById("relicModal")?.classList.remove("open");
    }

    function openRelicView(id) {
      const relic = allItems().find((i) => i.id === id && isRelic(i));
      if (!relic) {
        openDetail(id);
        return;
      }
      recordView(id);
      markCardSeen(id);
      const members = relicMembers(relic);
      const origin = members.find((m) => m.id === relic.originId) || members[0];

      document.getElementById("relicTitle").textContent = relic.title;
      const hero = document.getElementById("relicHero");
      hero.innerHTML = mediaHtml(relic);

      const rows = members.map((m) => {
        const isOrigin = m.id === relic.originId;
        return `
          <div class="relic-member ${isOrigin ? "is-origin" : ""}" data-relic-play="${m.id}" role="button" tabindex="0">
            <div class="relic-member__thumb">${mediaHtml(m)}</div>
            <div class="relic-member__meta">
              <b>${escapeHtml(m.title)}${isOrigin ? " · Origin" : ""}</b>
              <span>${escapeHtml(typeLabel(m.type))} · by ${escapeHtml(m.creator)}</span>
            </div>
            <div class="relic-member__res" title="Artifact Resonance">${m.resonance}</div>
          </div>`;
      }).join("");

      document.getElementById("relicContent").innerHTML = `
        <div class="detail-tags">
          <span class="badge badge-relic">Relic</span>
          <span class="badge badge-origin">${members.length} Artifacts</span>
          ${relic.featured ? '<span class="badge badge-featured">Featured</span>' : ""}
        </div>
        <p>${escapeHtml(relic.description || "A living lineage of Artifacts that grew into a Relic of the Hall.")}</p>
        <div class="detail-meta-grid">
          <div><b>Relic Resonance</b>${relic.resonance}</div>
          <div><b>Linked</b>${members.length}</div>
          <div><b>Origin</b>${escapeHtml(relic.originTitle || (origin && origin.title) || "—")}</div>
          <div><b>Keeper</b>${escapeHtml(relic.creator)}</div>
          <div><b>Howls (sum)</b>${formatCount(relic.howls)}</div>
          <div><b>Views (sum)</b>${formatCount(relic.views)}</div>
        </div>
        <h3 style="margin:1rem 0 0.35rem;font-size:0.95rem;color:var(--gold-soft)">Lineage</h3>
        <p style="font-size:0.78rem;color:var(--text-dim);margin:0 0 0.5rem">Tap any Artifact to play. Origin is marked.</p>
        <div class="relic-members">${rows || "<p>No linked Artifacts yet.</p>"}</div>
        <p style="font-size:0.78rem;color:var(--text-dim);margin-top:0.85rem">Relics rise inside the Hall — denser nodes in the same feed, not a second world.</p>
      `;

      document.getElementById("relicContent").querySelectorAll("[data-relic-play]").forEach((row) => {
        row.addEventListener("click", () => {
          const mid = row.dataset.relicPlay;
          closeRelicView();
          launchPlay(mid);
        });
        row.addEventListener("keydown", (e) => {
          if (e.key === "Enter" || e.key === " ") {
            e.preventDefault();
            row.click();
          }
        });
      });

      const originId = relic.originId || (origin && origin.id);
      const playBtn = document.getElementById("relicPlayOrigin");
      if (playBtn) {
        playBtn.onclick = () => {
          if (!originId) return;
          closeRelicView();
          flashPlayEnergy(playBtn, hero);
          window.setTimeout(() => launchPlay(originId), prefersReducedMotion() ? 0 : 120);
        };
        playBtn.disabled = !originId;
      }

      const modal = document.getElementById("relicModal");
      modal.classList.remove("open");
      void modal.offsetWidth;
      modal.classList.add("open");
    }

'''

if "function openRelicView" not in t:
    t = t.replace("    function openDetail(id, opts = {}) {", relic_view_fn + "    function openDetail(id, opts = {}) {", 1)
    print("openRelicView ok")
else:
    print("openRelicView already")

# openDetail: if relic, redirect
old_od = """    function openDetail(id, opts = {}) {
      const item = allItems().find((i) => i.id === id);
      if (!item) return;
      if (item.locked) {
        toast("Coming soon · fog still holds this spark");
        return;
      }"""
new_od = """    function openDetail(id, opts = {}) {
      const item = allItems().find((i) => i.id === id);
      if (!item) return;
      if (isRelic(item) && !opts.forceArtifact) {
        openRelicView(id);
        return;
      }
      if (item.locked) {
        toast("Coming soon · fog still holds this spark");
        return;
      }"""
if "forceArtifact" not in t:
    if old_od not in t:
        raise SystemExit("openDetail start not found")
    t = t.replace(old_od, new_od, 1)
    print("openDetail redirect ok")

# ── 9) Event listeners for vessel filters + close relic ──────────────
old_type_listener = """    document.getElementById("typeFilters").addEventListener("click", (e) => {
      const btn = e.target.closest("[data-type]");
      if (!btn) return;
      state.type = btn.dataset.type;
      resetFeedPage();
      document.querySelectorAll("#typeFilters .chip").forEach((c) => c.classList.toggle("active", c === btn));
      render();
    });"""

new_type_listener = """    document.getElementById("vesselFilters")?.addEventListener("click", (e) => {
      const btn = e.target.closest("[data-vessel]");
      if (!btn) return;
      state.vessel = btn.dataset.vessel;
      resetFeedPage();
      document.querySelectorAll("#vesselFilters .chip").forEach((c) => c.classList.toggle("active", c === btn));
      render();
    });

    document.getElementById("typeFilters").addEventListener("click", (e) => {
      const btn = e.target.closest("[data-type]");
      if (!btn) return;
      state.type = btn.dataset.type;
      resetFeedPage();
      document.querySelectorAll("#typeFilters .chip").forEach((c) => c.classList.toggle("active", c === btn));
      render();
    });

    document.querySelectorAll("[data-close-relic]").forEach((el) => {
      el.addEventListener("click", closeRelicView);
    });
    document.getElementById("relicModal")?.addEventListener("click", (e) => {
      if (e.target.id === "relicModal") closeRelicView();
    });"""

if "vesselFilters" not in t.split("typeFilters").addEventListener if False else t:
    pass
if 'getElementById("vesselFilters")' not in t:
    if old_type_listener not in t:
        raise SystemExit("typeFilters listener not found")
    t = t.replace(old_type_listener, new_type_listener, 1)
    print("listeners ok")
else:
    print("listeners already")

# Escape key: also close relic - find keydown Escape
if "closeRelicView" in t and "Escape" in t:
    # try add to existing escape handler
    if "relicModal" not in t[t.find("Escape") : t.find("Escape") + 400]:
        esc_old = 'if (e.key === "Escape")'
        # find first Escape handler that closes modals
        idx = t.find('if (e.key === "Escape")')
        if idx > 0:
            # insert closeRelicView near start of block
            chunk = t[idx:idx+300]
            if "closeRelicView" not in chunk:
                t = t.replace(
                    'if (e.key === "Escape") {',
                    'if (e.key === "Escape") {\n        closeRelicView();',
                    1,
                )
                print("escape ok")

p.write_text(t, encoding="utf-8")
print("DONE", len(t))
