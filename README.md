# Thunderwolf Citadel Gate

**Private work-in-progress.** Pack-first living creation hall for the Boltverse (Phase 1).

## Open locally

Double-click `index.html`, or:

```powershell
Start-Process .\index.html
```

No build step. Pure HTML / CSS / JS + assets.

## What’s included

- Feed-first **Citadel Gate** (pump.fun-style Living Index)
- Gallery of Echoes (Featured) + Explore filters + search
- Publishing Gate submit (localStorage)
- Boltverse cover art, Star Core, hall floor, wolf crest
- Soft parallax + cyan/gold chrome
- **Artifact Identity (Decree #601)** — immutable true names at publish

## Artifact ID (True Name)

```text
artifact_{forger_slug}_{short_hash}
```

- **Slug** — Forger handle at first seal (lowercase, max 20)
- **Hash** — 6-char base36 from `crypto.getRandomValues`
- **Immutable** — ownership/version/remix parent are separate fields

**Static layout & SPA routes**

```text
#/play/{id}          → play session (shareable)
#/artifact/{id}      → Artifact overview
#/relic/{id}         → Relic view
games/{id}/v{n}/index.html
covers/artifacts/{id}.jpg
```

Full algorithm + layout: **[docs/ARTIFACT_IDENTITY.md](docs/ARTIFACT_IDENTITY.md)**

## Vision

Aligned with Pack scaffolding around @StarBoltSprint / SMiR decrees: one place, soul for creators, Wrapper for the whole, everything feeds the Star Core.

## Play live

Public playable hall (GitHub Pages):

**https://starboltsprint.github.io/thunderwolf-citadel-play/?v=skyfilm5**

Private source: `StarBoltSprint/thunderwolf-citadel`  
Public host: `StarBoltSprint/thunderwolf-citadel-play`

## Privacy

The main repository is **private** — only the owner can see it unless collaborators are invited. The **play** repo is the public static host for the live link.
