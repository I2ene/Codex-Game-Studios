# Evaluation scenarios: gs-review-all-gdds

Professional scenarios adapted from Donchitos' upstream testing guidance; see
[source attribution](../../../NOTICE.md). These are evaluation inputs and domain
checks, not executed results. Read `.agents/skills/gs-review-all-gdds/SKILL.md` and its current procedure first.
Use [evaluation policy](../README.md) and [category rubric](../quality-rubric.md).

Resolve current config and project engine records. Apply review-mode discipline
coverage without claiming automatic delegation: use the parent when needed, label it,
and record actual participants only. Existing human authorization governs writes;
case approvals represent unresolved decisions and never revoke prior authorization.
Historical fixture versions are scenario inputs, not current API verification.
The linked native procedure governs command arguments, output schemas, receipts,
context and mode applicability. Missing inputs remain NOT ASSESSED.

### Case 1: Happy Path — Clean GDD set with no conflicts

**Fixture:**
- `project.yaml` sets `modes.workflow: full`
- `design/gdd/` contains `game-concept.md`, `game-pillars.md` (pillars and
  anti-pillars), `systems-index.md`, and three system GDDs — `combat.md`,
  `inventory.md`, `crafting.md` — each with every section Phase 1c loads and a
  filled `## Cross-References` table whose rows all resolve
- All GDDs are consistent: no formula contradictions, no competing ownership,
  no stale references, reciprocal dependencies; every system serves a pillar
- Nothing a design-theory check would warn on either: one primary progression
  loop, at most 4 systems active at once, every resource has both a source and a
  sink, compatible scaling curves, compatible player fantasies

**Input:** `$gs-review-all-gdds`

**Domain checks:**
- [ ] Phase 2 and Phase 3 cover independent concerns, with optional authorized parallel delegation (independent authorized delegated work may run concurrently; parent work is labeled accurately)
- [ ] Sub-agent prompts carry the GDD section content, not just file paths
- [ ] The report states the covered set: `GDDs reviewed: [N] of [M] present` and `Not read: none`, and lists the scenarios walked
- [ ] Verdict is PASS only because there are no blocking issues **and no warnings**, over three readable GDDs — a single warning would make it CONCERNS
- [ ] The report is written only after the user approves, under an ISO-dated name (`gdd-cross-review-YYYY-MM-DD.md`)
- [ ] The closing widget offers `$gs-create-architecture` and `$gs-gate-check` (both allowed on PASS)

---

### Case 2: Failure Path — Conflicting rules between two GDDs

**Fixture:**
- `project.yaml` sets `modes.workflow: full`
- `combat.md` defines a floor: "Minimum damage after armour reduction is 1"
- `status-effects.md` states a mechanic that bypasses it: "Poison ignores armour
  and can reduce damage to 0"
- The two GDDs are otherwise complete and valid; `game-pillars.md` defines the
  pillars and `systems-index.md` lists both systems

**Input:** `$gs-review-all-gdds`

**Domain checks:**
- [ ] Verdict is FAIL (not PASS, CONCERNS or NOT ASSESSED)
- [ ] Both GDD filenames are named in the conflict entry
- [ ] The specific contradicting rules are quoted (not a vague "conflict found")
- [ ] The issue is classified as Blocking (🔴), and both GDDs are in the flagged table with Priority Blocking
- [ ] Skill does NOT decide which GDD is right and does NOT edit either GDD
- [ ] If the user approves the systems-index update, the status is written as exactly `Needs Revision` with no parenthetical
- [ ] The closing widget offers neither `$gs-create-architecture` nor `$gs-gate-check` (verdict is FAIL)

---

### Case 3: Partial Path — Cross-reference to a GDD that does not exist
**Fixture:**
- `project.yaml` sets `modes.workflow: full`
- `design/gdd/` holds `game-pillars.md`, `systems-index.md` and two consistent
  system GDDs, `crafting.md` and `inventory.md`
- `crafting.md`'s `## Cross-References` table has a row whose Target GDD is
  `system-b.md`; no `design/gdd/system-b.md` exists
- `systems-index.md` lists system-b as the next system with Status: Not Started
- Nothing else would warn

**Input:** `$gs-review-all-gdds`

**Domain checks:**
- [ ] The finding names `crafting.md` and the missing `system-b.md`
- [ ] It is reported under Warnings (⚠️), not Blocking — because the systems index lists system-b as planned
- [ ] Verdict is CONCERNS — not FAIL for a reference to planned work, and not an unqualified PASS
- [ ] The closing widget offers `$gs-design-system system-b`, and offers `$gs-create-architecture` but not `$gs-gate-check` (which requires PASS)
- [ ] Skill does NOT skip or silently ignore the missing target

**Case 3b — the target is in neither place:** the same fixture, except
`systems-index.md` has no entry for system-b. Nothing will ever define it.

**Domain checks (3b):**
- [ ] The reference is reported as 🔴 Blocking, and `crafting.md` appears in "GDDs Flagged for Revision" with Priority Blocking
- [ ] Verdict is FAIL, and the closing widget offers neither `$gs-create-architecture` nor `$gs-gate-check`

---

### Case 4: Edge Case — Fewer than two system GDDs

**Fixture:**
- `project.yaml` sets `modes.workflow: full`
- `design/gdd/` contains `systems-index.md` and a single system GDD, `combat.md`

**Input:** `$gs-review-all-gdds`

**Domain checks:**
- [ ] Skill outputs the "requires at least 2 system GDDs" stop message
- [ ] Neither Phase 2 nor Phase 3 sub-agent is consulted
- [ ] No verdict of PASS is produced for the single document
- [ ] No report write is offered and no file is written

---

### Case 5: Director Gate — none consulted, whatever the review mode

**Fixture:**
- `project.yaml` sets `modes.workflow: full`
- `design/gdd/` holds the Case 1 set: concept, pillars, systems index and three
  consistent system GDDs
- 5a: `modes.review_mode: full`; 5b: `modes.review_mode: solo`

**Input:** `$gs-review-all-gdds`

**Domain checks:**
- [ ] No director gate agents (CD-, TD-, PR-, AD-, LP- prefixed gates) are consulted in either mode
- [ ] Review mode changes nothing: under `solo` both game-designer analyses still run through explicitly labeled parent work or authorized delegation
- [ ] Output contains no "Gate: [GATE-ID]" or "[GATE-ID] skipped" entries
- [ ] The skill produces a verdict in both modes
- [ ] Phase 2 and Phase 3 both apply game-designer expertise; record any actual delegated participants and label parent work accurately

---

### Case 6: NOT ASSESSED — fewer than two readable GDDs

**Fixture:**
- `project.yaml` sets `modes.workflow: full`
- `design/gdd/` holds `game-pillars.md`, `systems-index.md` and two system GDDs:
  `combat.md`, complete, and `inventory.md`, which has the template's headings but
  only placeholder text under them

**Input:** `$gs-review-all-gdds`

**Domain checks:**
- [ ] Verdict is NOT ASSESSED — not PASS, although no contradiction was found
- [ ] The report names `inventory.md` as present but not reviewable, and states `GDDs reviewed: 1 of 2 present`
- [ ] A GDD that could not be read at all would be named on the report's `Not read:` line under every verdict, and is a NOT ASSESSED trigger like an empty one
- [ ] The closing widget offers neither `$gs-create-architecture` nor `$gs-gate-check`
