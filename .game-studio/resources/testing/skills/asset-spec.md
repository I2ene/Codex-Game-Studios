# Evaluation scenarios: gs-asset-spec

Professional scenarios adapted from Donchitos' upstream testing guidance; see
[source attribution](../../../NOTICE.md). These are evaluation inputs and domain
checks, not executed results. Read `.agents/skills/gs-asset-spec/SKILL.md` and its current procedure first.
Use [evaluation policy](../README.md) and [category rubric](../quality-rubric.md).

Resolve current config and project engine records. Apply review-mode discipline
coverage without claiming automatic delegation: use the parent when needed, label it,
and record actual participants only. Existing human authorization governs writes;
case approvals represent unresolved decisions and never revoke prior authorization.
Historical fixture versions are scenario inputs, not current API verification.
The linked native procedure governs command arguments, output schemas, receipts,
context and mode applicability. Missing inputs remain NOT ASSESSED.

### Case 1: Happy Path — Character spec in lean mode

**Fixture:**
- `project.yaml` sets `modes.rigor: standard` (review mode resolves to `lean`) and
  has `performance.*` and `naming.*` values
- `design/art/art-bible.md` exists with Shape Language, Color System and Section 8 Asset Standards
- `design/narrative/characters/goblin-enemy.md` exists with a visual description
- No `design/assets/asset-manifest.md`

**Input:** `$gs-asset-spec character:goblin-enemy`

**Domain checks:**
- [ ] Asset list is confirmed with `host input tool` before any spec is generated
- [ ] Only `art-director` is consulted (no `technical-artist` in lean mode)
- [ ] The output names `technical-artist` as skipped and says technical constraints were not validated
- [ ] Each asset block has the field table, Art Bible Anchors (by section), a Generation Prompt and `Status: Needed`
- [ ] Preserve the case's unresolved human decisions and declines; perform routine writes already authorized, and ask only for missing decisions or scope.
- [ ] Manifest is created with a Progress Summary and IDs starting at `ASSET-001`
- [ ] Phase 6 offers `$gs-asset-audit` among the next steps

---

### Case 2: No Art Bible — Skill stops before speccing

**Fixture:**
- `project.yaml` sets `modes.rigor: standard`
- `design/gdd/combat.md` exists with a Visual/Audio Requirements section
- `design/art/art-bible.md` does NOT exist
- `design/game-brief.md` does NOT exist

**Input:** `$gs-asset-spec system:combat`

**Domain checks:**
- [ ] The "No art bible found. Run `$gs-art-bible` first" message is shown
- [ ] No asset list is presented and no delegated participant is required
- [ ] No spec file or manifest is written
- [ ] Specs are not generated with invented style rules

---

### Case 3: Manifest Already Exists — IDs continue and shared assets are reused

**Fixture:**
- `project.yaml` sets `modes.rigor: standard`; art bible exists
- `design/assets/asset-manifest.md` exists; the highest ID is `ASSET-014`, and
  `ASSET-012` (Generic Hit Spark) is specced for the Combat system in
  `design/assets/specs/combat-assets.md`
- `design/gdd/tower-defense.md` Visual/Audio section lists a hit spark and a tower-build VFX

**Input:** `$gs-asset-spec system:tower-defense`

**Domain checks:**
- [ ] Append the Tower Defense context to the existing manifest, preserving all previous asset/context entries; update the Progress Summary.
- [ ] The hit spark references `ASSET-012`; no duplicate hit-spark spec is created
- [ ] The new asset's ID is `ASSET-015` (project-wide sequence, not restarted per target)
- [ ] Preserve the case's unresolved human decisions and declines; perform routine writes already authorized, and ask only for missing decisions or scope.
- [ ] Progress Summary counts are updated

---

### Case 4: Several Assets in One Target — One file, per-asset revision before write

**Fixture:**
- `project.yaml` sets `modes.rigor: standard`; art bible exists; no manifest
- `design/gdd/combat.md` Visual/Audio section names a hit-spark VFX, a floating
  damage number (UI) and a hit sound (audio)

**Input:** `$gs-asset-spec system:combat`

**Domain checks:**
- [ ] Preserve the case's unresolved human decisions and declines; perform routine writes already authorized, and ask only for missing decisions or scope.
- [ ] The audio asset has no image generation prompt
- [ ] The minor revision does not re-consults `art-director`
- [ ] All three `ASSET-NNN` blocks are in `design/assets/specs/combat-assets.md`

---

### Case 5: Director Gate Check — Solo default, brief instead of art bible

**Fixture:**
- `project.yaml` has no `modes` block (review mode resolves to `solo` via `modes.rigor: minimal`)
- `design/game-brief.md` exists with an Art & audio direction line
- No `design/art/art-bible.md`
- No character profile for `hero` in `design/narrative/` or `design/assets/entity-inventory.md`

**Input:** `$gs-asset-spec character:hero`

**Domain checks:**
- [ ] Skill continues without an art bible and says the specs are anchored to the brief
- [ ] Missing profile triggers the "Describe it briefly" question rather than a failure
- [ ] No `art-director` or `technical-artist` is consulted
- [ ] Both skipped agents are named in the output, which says technical constraints were not validated
- [ ] If the spec is written, its header names `design/game-brief.md` as the art direction (no `> **Art Bible**:` line), each asset carries a `**Brief anchor:**` line instead of Art Bible Anchors, and no Art Bible section or §8 tier is cited
- [ ] No gate IDs appear — the skip note names agents, not gates

---

### Case 6: Re-run on an Existing Spec — Updated in place, not overwritten

**Fixture:**
- `project.yaml` sets `modes.rigor: standard`; art bible exists
- `design/assets/specs/goblin-enemy-assets.md` exists with `ASSET-001` to
  `ASSET-004` (idle, walk and attack sprites; portrait); the manifest's highest ID
  is `ASSET-009`
- `design/narrative/characters/goblin-enemy.md` has since gained a charge-attack
  ability

**Input:** `$gs-asset-spec character:goblin-enemy`

**Domain checks:**
- [ ] The existing spec file is detected and read before the asset list is proposed
- [ ] Preserve the case's unresolved human decisions and declines; perform routine writes already authorized, and ask only for missing decisions or scope.
- [ ] Existing blocks and IDs are preserved; the file is not overwritten wholesale
- [ ] New assets continue the project-wide ID sequence (`ASSET-010`, `ASSET-011`)


## Applicable domain checks

- [ ] Surface conflicting discipline recommendations to the user before choosing a direction; do not silently select a winner.
