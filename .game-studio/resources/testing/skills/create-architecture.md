# Evaluation scenarios: gs-create-architecture

Professional scenarios adapted from Donchitos' upstream testing guidance; see
[source attribution](../../../NOTICE.md). These are evaluation inputs and domain
checks, not executed results. Read `.agents/skills/gs-create-architecture/SKILL.md` and its current procedure first.
Use [evaluation policy](../README.md) and [category rubric](../quality-rubric.md).

Resolve current config and project engine records. Apply review-mode discipline
coverage without claiming automatic delegation: use the parent when needed, label it,
and record actual participants only. Existing human authorization governs writes;
case approvals represent unresolved decisions and never revoke prior authorization.
Historical fixture versions are scenario inputs, not current API verification.
The linked native procedure governs command arguments, output schemas, receipts,
context and mode applicability. Missing inputs remain NOT ASSESSED.

### Case 1: Happy Path — New architecture document, full mode, reviews approve

**Fixture:**
- `project.yaml` has `engine.name: Godot`, `modes.review_mode: full`, `modes.workflow: full`
- `<project-engine-reference>/godot/` has `VERSION.md`, `breaking-changes.md`, `deprecated-apis.md`, `current-best-practices.md` and `modules/`
- `design/gdd/game-concept.md` and `design/gdd/systems-index.md` exist with real content
- `design/gdd/combat.md` and `design/gdd/inventory.md` follow the GDD template
- `docs/architecture/adr-0001-event-bus.md` exists (`Status: Accepted`)
- No `docs/architecture/architecture.md`
- TD-ARCHITECTURE returns APPROVE; LP-FEASIBILITY returns FEASIBLE

**Input:** `$gs-create-architecture`

**Domain checks:**
- [ ] The baseline uses `TR-[gdd-slug]-[NNN]` IDs and is built from the scanned GDD sections, not whole-file reads
- [ ] The knowledge gap inventory and its three-option `host input tool` come before Phase 1
- [ ] Preserve the case's unresolved human decisions and declines; perform routine writes already authorized, and ask only for missing decisions or scope.
- [ ] The master document is written only after the Phase 7 `host input tool` approval
- [ ] TD-ARCHITECTURE and LP-FEASIBILITY are each consulted as agents (`technical-director`, `lead-programmer`) after the document is written, and both verdicts are collected before Step 3
- [ ] TD-ARCHITECTURE is passed its four context items by name; the parent session does not read the gate file
- [ ] The handoff uses the fixed template headings, with no trailing commentary
- [ ] The handoff names `$gs-gate-check pre-production` — never a `[stage]` placeholder, which while this skill runs would resolve to the gate already passed

---

### Case 2: Review Concerns — LP-FEASIBILITY returns CONCERNS

**Fixture:**
- Same as Case 1, up to Phase 7b
- LP-FEASIBILITY returns CONCERNS: "Save/load path has no owning module for serialisation"
- Scenario (a): TD-ARCHITECTURE returns APPROVE
- Scenario (b): TD-ARCHITECTURE returns NOT ASSESSED, naming a context item it could not read

**Input:** `$gs-create-architecture`

**Domain checks:**
- [ ] The concern text is shown to the user alongside the TD assessment
- [ ] The user is offered Accept / Revise flagged items first / Discuss specific concerns
- [ ] Accepting records `CONCERNS (accepted)`, not `FEASIBLE`
- [ ] A revision records `REVISED after CONCERNS`, and the revised document is written once, after its sections are approved
- [ ] Preserve the case's unresolved human decisions and declines; perform routine writes already authorized, and ask only for missing decisions or scope.
- [ ] (b) A NOT ASSESSED review is recorded with its missing input and never as an approval

---

### Case 3: Lean and Solo Modes — Both reviews skipped, written with user approval only

**Fixture:**
- Same project as Case 1, but scenario (a): `project.yaml` has `modes.review_mode: lean`
- Scenario (b): same project, invoked with `--review solo`

**Input:** (a) `$gs-create-architecture` (b) `$gs-create-architecture --review solo`

**Domain checks:**
- [ ] Neither `technical-director` nor `lead-programmer` is consulted, and no TD-ARCHITECTURE review is applied in lean or solo mode
- [ ] The skip note names both gates and the mode
- [ ] (b) The `--review solo` argument overrides the resolved `review_mode` for the run
- [ ] The document is written on user approval alone, and completion is not blocked
- [ ] Document Status records both reviews as skipped in that mode (after its ask), so the document says why it has no sign-off
- [ ] The Phase 8 handoff is still printed

---

### Case 3b: Review Rejects — Accept Is Not Offered

**Fixture:**
- Same project as Case 1 in `full` mode; `technical-director` returns
  `TD-ARCHITECTURE: REJECT` (a Core system depends on a Presentation-layer module);
  `lead-programmer` returns `LP-FEASIBILITY: FEASIBLE`

**Input:** `$gs-create-architecture`

**Domain checks:**
- [ ] `technical-director` and `lead-programmer` calls are issued before either result is awaited
- [ ] `Accept — proceed to handoff` is not an option while a REJECT stands
- [ ] The revised document is written once, after the re-drafted sections are approved — not section by section
- [ ] Document Status never shows TD-ARCHITECTURE as APPROVE for this run; the handoff line says `REVISED after REJECT`

---

### Case 4: Edge Case — Systems index missing or empty

**Fixture:**
- Engine configured; `design/gdd/game-concept.md` exists
- Scenario (a): `modes.workflow: standard`, no `design/gdd/systems-index.md`
- Scenario (b): `modes.workflow: standard`, `design/gdd/systems-index.md` exists but contains only template placeholders
- Scenario (c): `modes.workflow: minimal`, no systems index, no game concept, `design/game-brief.md` exists

**Input:** `$gs-create-architecture`

**Domain checks:**
- [ ] (a) The skill stops with the `$gs-map-systems` message and writes nothing
- [ ] (b) A present-but-placeholder systems index is treated as absent
- [ ] (c) At `minimal` the skill says the index is not required and proceeds from the game brief
- [ ] At `standard` (a, b), no run continues past Phase 0b with a missing design file; at `minimal` (c) the brief stands in for both, and the run stops only if it is absent too

---

### Case 5: ADR Audit — Proposed ADRs and uncovered requirements

**Fixture:**
- Same as Case 1, plus `docs/architecture/adr-0002-save-format.md` with `Status: Proposed`
- Also `design/gdd/crafting.md`, written before the GDD template, with none of the scanned section headings
- Baseline requirement `TR-combat-002` (combo state machine) is not covered by any ADR's GDD Requirements Addressed section or decision text

**Input:** `$gs-create-architecture`

**Domain checks:**
- [ ] `crafting.md`, which matched no scanned section, is full-read and reported, and contributes TR-IDs to the baseline
- [ ] ADR statuses come from the header scan and ADR-0002 is reported as Proposed
- [ ] `TR-combat-002` is marked as a GAP and becomes a Required New ADR naming the TR-ID it covers
- [ ] Required New ADRs are grouped by layer, Foundation first
- [ ] "Gate-Check Readiness" lists ADR-0002 under "Accept ADRs"
- [ ] "Run These ADRs Next" lists no more than three entries

---

### Case 6: Existing Architecture Document — Update in place, never overwritten unasked

**Fixture:**
- Same project as Case 1, but `project.yaml` has `modes.review_mode: lean`
- Scenario (a): `docs/architecture/architecture.md` exists at `Version: 2` with every section written; the user picks `[A] Update chosen sections in place` and chooses Data Flow
- Scenario (b): no `docs/architecture/architecture.md`; the input is `$gs-create-architecture layers`

**Input:** (a) `$gs-create-architecture` (b) `$gs-create-architecture layers`

**Domain checks:**
- [ ] (a) The existing document is detected before any authoring, and replacing it is only ever the user's explicit `[B]` choice
- [ ] (a) Only the chosen section is re-authored and written; the other sections are left as they were
- [ ] (a) The version is raised, not reset to v1.0
- [ ] (b) A focus-area run with no document writes nothing and offers the full walkthrough
