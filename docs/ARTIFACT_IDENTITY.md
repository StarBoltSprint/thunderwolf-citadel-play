# Artifact Identity — Decree #601

**True Name of the Vessel**  
Implemented in `index.html` (`mintArtifactId`, `artifactPathsFor`, …).

---

## Core format

```text
artifact_{forger_slug}_{short_hash}
```

Examples:

- `artifact_smir_7k9x2p`
- `artifact_pathrunner_a3f8q1`
- `artifact_citadel_b2m4n7`

| Part | Purpose | Rules |
|------|---------|--------|
| `artifact_` | Namespace prefix | Always present |
| `{forger_slug}` | Original creator identity | Lowercase `[a-z0-9_]`, max **20** chars, from Forger profile at first publish |
| `{short_hash}` | Collision-proof uniqueness | **6** base36 chars by default (`0-9a-z`); may widen on extreme collision |

The ID is **immutable**. Ownership is a separate field (`owner_id`).

---

## Exact hash algorithm

### 1. Forger slug (`forgerSlugFromIdentity`)

1. Trim, lowercase.
2. Strip leading `@`.
3. Unicode NFKD; strip combining marks.
4. Replace non `[a-z0-9]` runs with `_`; collapse `_`.
5. Truncate to 20 characters; trim trailing `_`.
6. Empty / reserved `artifact` / `draft` → `forger`.

### 2. Short hash (`randomBase36(6)`)

1. Allocate `Uint8Array(6)`.
2. Fill with **`crypto.getRandomValues`** (CSPRNG).
3. Map each byte: `BASE36[byte % 36]` where  
   `BASE36 = "0123456789abcdefghijklmnopqrstuvwxyz"`.
4. Concatenate → 6-character string.

Bias from `byte % 36` is acceptable for 6-char display IDs (not a password).

### 3. Assembly + uniqueness (`mintArtifactId`)

1. `id = "artifact_" + forger_slug + "_" + short_hash`
2. Check against Hall registry (seed + user + relics).
3. On collision, mint a new hash (up to 32 tries at length 6, then length 8).
4. Last resort: mix time + entropy (still frozen once assigned).

### 4. Drafts

```text
draft_{uuid_hex_or_entropy}
```

Temporary only. Converted to a real `artifact_*` at **Pass the Gate**.

### 5. Remixes

Always a **new** `mintArtifactId`.  
Set `parent_id` to the parent’s Artifact ID (true name).  
`link_type`: e.g. `remix_of` | `sequel_of` | `expansion_of`.

---

## Versioning (not part of the ID)

| Field | Meaning |
|--------|---------|
| `id` | Never changes |
| `version` | Starts at `1`; increments on package update |
| Package folder | `games/{id}/v{version}/` |

---

## URL & static folder layout

Safe for **GitHub Pages** and any static host (relative paths, no query required for packages).

### Play & vessel routes (SPA — live in Gate)

| Style | Path | Behavior |
|--------|------|----------|
| **Play** | `#/play/{id}` | Opens play session for that vessel id |
| **Artifact detail** | `#/artifact/{id}` | Opens Artifact overview |
| **Relic detail** | `#/relic/{id}` | Opens Relic view |
| Clean path (host rewrite optional) | `/play/{id}/` | Static-host package style |

Helpers: `artifactPlayHash(id)`, `artifactDetailHash(id)`, `relicDetailHash(id)`, `artifactPlayPath(id)`, `parseCitadelHash()`, `applyCitadelRoute()`.

**Law:** Constellation nodes, Build near, pulse ledger, and play all key by the same `id` string (sealed `artifact_…` or legacy `seed-…`). Routes never invent a second identity.

Examples:

```text
index.html#/play/seed-1
index.html#/play/artifact_smir_7k9x2p
index.html#/artifact/vid-11
index.html#/relic/relic-silent-seed
```

### Game package (static files)

```text
games/
  {artifact_id}/
    v1/
      index.html          ← playable entry
      assets/             ← optional
    v2/
      index.html
    v3/
      index.html
```

| Helper | Returns |
|--------|---------|
| `artifactPackageRoot(id)` | `games/{id}/` |
| `artifactPackagePath(id, version)` | `games/{id}/v{n}/` |
| `artifactPackageEntry(id, version)` | `games/{id}/v{n}/index.html` |

### Covers (optional convention)

```text
covers/artifacts/{artifact_id}.jpg
```

Helper: `artifactCoverPath(id)`.

### Full path bag

```js
artifactPathsFor(id, version)
// → { play_hash, play_path, package_root, package_path, package_entry, cover_path, version }
```

### Example

```text
ID:       artifact_smir_7k9x2p
version:  3

Play:     #/play/artifact_smir_7k9x2p
Package:  games/artifact_smir_7k9x2p/v3/index.html
Cover:    covers/artifacts/artifact_smir_7k9x2p.jpg
```

---

## Fields written at publish (Gate)

| Field | Source |
|--------|--------|
| `id` | `mintArtifactId` |
| `version` | `1` |
| `owner_id` | current Forger slug |
| `original_forger_id` | same slug at seal (never changes) |
| `short_hash` | minted hash |
| `parent_id` | forge draft parent if any |
| `link_type` | draft link type / `remix_of` |
| `remix_policy` | default `open` |
| `status` | `live` |
| `package_path` / `play_path` / `play_hash` | layout helpers |

## Catalog migration v1 (live)

At boot, `buildCatalogIdentityMigration()` rewrites every migratable seed/demo id:

| Legacy pattern | New form |
|----------------|----------|
| `seed-*`, `vid-*`, `howl-*`, `decree-*`, `hall-*`, `user-*` | `artifact_{slug}_{hash6}` |
| `relic-*` | `relic_{slug}_{hash6}` |

- **Hash is deterministic** (`deterministicBase36("artifact:seed-1")`) so every browser gets the **same** sealed names.
- Each vessel keeps `legacy_id` for dual-read.
- Relic `originId` / `childIds` are remapped to canon ids.
- localStorage (pulse, howls, seen, overrides, forge draft) is dual-keyed via `migrateBrowserIdentityStorage()`.
- `findItemById`, pulse ledger, and game URL resolve accept **legacy or canon**.

Routes still work either way:

```text
#/play/seed-1
#/play/artifact_citadel_xxxxxx
```

(both resolve if the map knows the alias)

---

## Design law

> The Artifact ID is the vessel’s true name.  
> It is given once, at the moment the Publishing Gate opens.  
> It never lies, never changes hands, and never forgets its parent.

— Decree #601 · Thread Keeper · SMiR · Thunderwolf Citadel  
Powered by xAI & YOU
