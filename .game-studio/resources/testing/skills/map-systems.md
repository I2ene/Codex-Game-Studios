# Evaluation scenarios: gs-map-systems

Professional scenarios adapted from Donchitos' upstream testing guidance; see
[source attribution](../../../NOTICE.md). These are evaluation inputs and domain
checks, not executed results. Read `.agents/skills/gs-map-systems/SKILL.md` and its current procedure first.
Use [evaluation policy](../README.md) and [category rubric](../quality-rubric.md).

Resolve current config and project engine records. Apply review-mode discipline
coverage without claiming automatic delegation: use the parent when needed, label it,
and record actual participants only. Existing human authorization governs writes;
case approvals represent unresolved decisions and never revoke prior authorization.
Historical fixture versions are scenario inputs, not current API verification.
The linked native procedure governs command arguments, output schemas, receipts,
context and mode applicability. Missing inputs remain NOT ASSESSED.

### Case 1: Happy Path — Concept decomposed and index written in full review mode

**Fixture:**
- `project.yaml`: `modes.workflow: standard`, `modes.review_mode: full`
- `design/gdd/game-concept.md` exists with Core Mechanics naming combat and an
  inventory, and an MVP Definition section
- `design/gdd/game-pillars.md` exists with 2 pillars
- No `design/gdd/systems-index.md` exists yet
- TD-SYSTEM-BOUNDARY returns APPROVE, PR-SCOPE returns REALISTIC, CD-SYSTEMS
  returns APPROVE

**Input:** `$gs-map-systems`

**Domain checks:**
- [ ] Implicit systems are inferred and labelled implicit, with the reason given
- [ ] TD-SYSTEM-BOUNDARY consults after the dependency map is approved and before priorities are presented, and is passed the full dependency graph — not a summary
- [ ] PR-SCOPE consults after priorities are approved and before the write ask
- [ ] Preserve the case's unresolved human decisions and declines; perform routine writes already authorized, and ask only for missing decisions or scope.
- [ ] CD-SYSTEMS consults only after the index is written, and receives all four tiers and the high-risk systems — not the MVP list alone
- [ ] The Systems Enumeration table keeps the template's columns (`# / System Name / Category / Priority / Status / Design Doc / Depends On`) — no added column
- [ ] `active.md` is updated and the verdict is COMPLETE

---

### Case 2: Failure Path — No game concept found

**Fixture:**
- `project.yaml`: `modes.workflow: standard`
- Neither `design/gdd/game-concept.md` nor `design/game-brief.md` exists

**Input:** `$gs-map-systems`

**Domain checks:**
- [ ] The "No game concept found" message is printed
- [ ] Skill recommends `$gs-brainstorm` as the next action
- [ ] No systems enumeration is presented and no gate is consulted
- [ ] No `design/gdd/systems-index.md` is created and Verdict COMPLETE is not emitted

---

### Case 3: Director Gate — CD-SYSTEMS returns CONCERNS after the write

**Fixture:**
- Game concept and pillars exist; no index yet
- `project.yaml`: `modes.workflow: standard`, `modes.review_mode: full`
- TD-SYSTEM-BOUNDARY returns APPROVE, PR-SCOPE returns REALISTIC
- CD-SYSTEMS returns CONCERNS: an MVP system implied by the core fantasy is missing
- At the CONCERNS question the user picks `Accept — record them in the index`

**Input:** `$gs-map-systems`

**Domain checks:**
- [ ] CD-SYSTEMS is consulted only after the index is written, not before the write ask
- [ ] The CONCERNS go to the user as a choice — the index is not edited before the user picks
- [ ] Only the Accept choice, which names the edit, leads to the note being written; it sits directly beneath the `## Priority Tiers` table and names the MVP tier
- [ ] Had the user picked `Revise the system set`, the affected systems would be reworked with the user and the re-write of the index asked again
- [ ] CONCERNS do not trigger a full re-decomposition (that path is REJECT's)
- [ ] Verdict is COMPLETE

---

### Case 4: Edge Case — Systems index already exists

**Fixture:**
- `project.yaml`: `modes.workflow: standard`
- `design/gdd/game-concept.md` exists
- `design/gdd/systems-index.md` already exists with 8 systems, 3 of them designed

**Input:** `$gs-map-systems`

**Domain checks:**
- [ ] Skill detects and reads the existing index before proceeding
- [ ] The system count with designed / not-started split is presented
- [ ] All three options are offered — the index is not auto-overwritten
- [ ] Skill does NOT re-run a full decomposition from scratch without the user choosing to

---

### Case 5: Director Gate — Lean and solo modes skip all three gates, noted

**Fixture (lean mode):**
- Game concept exists
- `project.yaml`: `modes.workflow: standard`, `modes.review_mode: lean`

**Lean mode expected behavior:**
1. Systems, dependencies and priorities are presented and approved as in Case 1
2. Notes "TD-SYSTEM-BOUNDARY skipped — Lean mode." and "PR-SCOPE skipped — Lean
   mode." at their phases
3. "May I write" is asked; the index is written after approval
4. Notes "CD-SYSTEMS skipped — Lean mode."
5. Session state is updated and Verdict: COMPLETE is printed

**Assertions (lean mode):**
- [ ] All three skip notes appear, each at its own phase
- [ ] No director agent is consulted
- [ ] The "May I write" ask still precedes the write
- [ ] `active.md` is updated and Verdict: COMPLETE is printed even though CD-SYSTEMS was skipped

**Fixture (solo mode):**
- Same concept, `project.yaml`: `modes.workflow: standard`, `modes.review_mode: full`
- Input: `$gs-map-systems --review solo`

**Solo mode expected behavior:**
1. `--review solo` overrides the resolved `full`
2. The same three gates are skipped, noted with "Solo mode."

**Assertions (solo mode):**
- [ ] All three skip notes carry the "Solo mode." label
- [ ] Behavior is otherwise identical to lean mode for this skill

**Domain checks:**
- [ ] All three skip notes appear, each at its own phase
- [ ] No director agent is consulted
- [ ] Preserve the case's unresolved human decisions and declines; perform routine writes already authorized, and ask only for missing decisions or scope.
- [ ] `active.md` is updated and Verdict: COMPLETE is printed even though CD-SYSTEMS was skipped
- [ ] All three skip notes carry the "Solo mode." label
- [ ] Behavior is otherwise identical to lean mode for this skill

---

### Case 6: Guided mode — a new index is still asked for; an update is not

**Fixture (new index):**
- `project.yaml`: `modes.workflow: standard`, `modes.review_mode: solo`,
  `modes.automation: guided`
- Game concept exists; no `design/gdd/systems-index.md`

**Fixture (update):**
- Same, but `design/gdd/systems-index.md` exists and the user chose "Update the
  index with new systems"

**Input (both fixtures):** `$gs-map-systems`

**Domain checks:**
- [ ] Preserve the case's unresolved human decisions and declines; perform routine writes already authorized, and ask only for missing decisions or scope.
- [ ] Update at `guided`: no write ask; the summary and destination are shown before the write and the result is reported after it

---

### Case 7: Director Gate — TD-SYSTEM-BOUNDARY returns REJECT

**Fixture:**
- `project.yaml`: `modes.workflow: standard`, `modes.review_mode: full`
- Game concept and pillars exist; no index yet
- TD-SYSTEM-BOUNDARY returns REJECT: two systems share one responsibility and
  must be merged

**Input:** `$gs-map-systems`

**Domain checks:**
- [ ] Priority assignment does not start while the REJECT is unresolved
- [ ] The revised boundaries are shown to the user before priorities are presented
- [ ] Preserve the case's unresolved human decisions and declines; perform routine writes already authorized, and ask only for missing decisions or scope.
- [ ] The REJECT is not recorded as a note and passed over — that handling is CONCERNS'
