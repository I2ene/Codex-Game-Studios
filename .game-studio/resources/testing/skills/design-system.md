# Evaluation scenarios: gs-design-system

Professional scenarios adapted from Donchitos' upstream testing guidance; see
[source attribution](../../../NOTICE.md). These are evaluation inputs and domain
checks, not executed results. Read `.agents/skills/gs-design-system/SKILL.md` and its current procedure first.
Use [evaluation policy](../README.md) and [category rubric](../quality-rubric.md).

Resolve current config and project engine records. Apply review-mode discipline
coverage without claiming automatic delegation: use the parent when needed, label it,
and record actual participants only. Existing human authorization governs writes;
case approvals represent unresolved decisions and never revoke prior authorization.
Historical fixture versions are scenario inputs, not current API verification.
The linked native procedure governs command arguments, output schemas, receipts,
context and mode applicability. Missing inputs remain NOT ASSESSED.

### Case 1: Happy Path — New combat GDD, full mode, full workflow

**Fixture:**
- `design/gdd/game-concept.md` and `design/gdd/systems-index.md` exist; `combat` is listed with `Category: Gameplay`
- No `design/gdd/combat.md`
- `project.yaml` has `engine.name: Godot`, `modes.review_mode: full`, `modes.workflow: full`, `modes.automation: collaborative`; `<project-engine-reference>/godot/` has `VERSION.md` and `modules/physics.md` (combat maps to the Physics domain)
- CD-GDD-ALIGN returns APPROVE

**Input:** `$gs-design-system combat`

**Domain checks:**
- [ ] The new skeleton contains all eight required section headers.
- [ ] For the Gameplay category, Visual/Audio and Game Feel are required sections and are not offered as skippable.
- [ ] Preserve the case's unresolved human decisions and declines; perform routine writes already authorized, and ask only for missing decisions or scope.
- [ ] Every section draft is followed in the same response by the "Approve the [Section Name] section?" widget
- [ ] Each section is written individually, immediately after its approval, by an Edit anchored on its heading
- [ ] Section C's specialists come from the routing table's Combat row and are consulted before drafting, using parent work or authorized parallel delegation
- [ ] CD-GDD-ALIGN consults once, after all sections and the Summary are written — not per section
- [ ] The verdict is recorded as `> **Creative Director Review (CD-GDD-ALIGN)**: APPROVED [date]`
- [ ] `$gs-design-review` is directed to a fresh session and never offered inline

---

### Case 2: Retrofit Mode — Fill only the incomplete sections at standard tier

**Fixture:**
- `project.yaml` has `engine.name: Godot`, `modes.workflow: standard`, `modes.review_mode: lean`
- `design/gdd/game-concept.md` and `design/gdd/systems-index.md` exist; `inventory` is listed with `Category: Economy` (engine domain Scripting)
- `<project-engine-reference>/godot/` has `VERSION.md` and `modules/`, but no `modules/scripting.md`
- `design/gdd/inventory.md` exists with Overview, Detailed Design and Formulas fully written; its `## Summary` holds only `[To be designed]`
- `## Edge Cases` and `## Acceptance Criteria` contain only `[To be designed]`; `## Dependencies` has an empty body
- The file has no Player Fantasy or Tuning Knobs section

**Input:** `$gs-design-system retrofit design/gdd/inventory.md`

**Domain checks:**
- [ ] The retrofit block is shown before any change is made
- [ ] Sections the tier does not require are not reported as gaps
- [ ] The skill asks "Shall I fill the 3 missing sections? I will not modify any existing content."
- [ ] The absent `scripting.md` module is named in the output, not skipped silently as if feasibility had been checked
- [ ] No skeleton is created and complete sections are not re-authored or overwritten
- [ ] Each filled section still goes through the per-section approval before its write

---

### Case 3: Director Gate — CD-GDD-ALIGN returns CONCERNS, REJECT or NOT ASSESSED

**Fixture:**
- `design/gdd/game-concept.md` (pillars include "Fearless Exploration") and `design/gdd/systems-index.md` exist; `stamina` is listed with `Category: Gameplay`
- `project.yaml` has `modes.review_mode: full` and `modes.workflow: full`
- All eight sections, Player Fantasy included, and the Summary are written for `design/gdd/stamina.md`
- Scenario (a): CD-GDD-ALIGN returns CONCERNS: "Detailed Design's stamina drain undercuts the 'Fearless Exploration' pillar"
- Scenario (b): CD-GDD-ALIGN returns REJECT: "stamina exhaustion strands the player mid-exploration, which the 'Fearless Exploration' pillar rules out"
- Scenario (c): CD-GDD-ALIGN returns NOT ASSESSED — no MDA aesthetics target was available to check the GDD against

**Input:** `$gs-design-system stamina` (reaching Step 5a-bis)

**Domain checks:**
- [ ] CD-GDD-ALIGN receives the completed GDD path, the pillars, the MDA target and the Player Fantasy section
- [ ] (a) CONCERNS are shown to the user with the three standard options, not auto-accepted
- [ ] A revised section re-runs its section cycle and is re-approved before it is written
- [ ] The Status header records `REVISED [date]` or `CONCERNS (accepted) [date]` to match the user's choice
- [ ] (b) After a REJECT, no later step (5b registry, 5d systems index) runs until the flagged section has been revised
- [ ] (c) NOT ASSESSED is never recorded or reported as an approval

---

### Case 4: Lean and Solo Modes — Gate skipped once; specialist consults follow their own checks

**Fixture:**
- `design/gdd/game-concept.md` and `design/gdd/systems-index.md` exist; the system is `stamina` (`Category: Gameplay`); no `design/gdd/stamina.md`
- `project.yaml` has `engine.name: Godot` and `modes.workflow: full`
- Section D's stamina formula has no knobs that interact; the stamina bar is feedback the player reads to play
- Scenario (a): `modes.review_mode: lean`
- Scenario (b): `modes.review_mode: solo`

**Input:** `$gs-design-system stamina`

**Domain checks:**
- [ ] (a) In lean mode Sections B, C, E and G are drafted without their specialists, while Sections D and H and Visual/Audio still consults theirs
- [ ] (a) Each lean-skipped consults prints a "not consulted — Lean mode" note naming its agent — none is skipped silently
- [ ] (a) The CD-GDD-ALIGN skip note appears once, at Step 5a-bis
- [ ] (b) In solo mode no agent is consulted, and each skipped specialist leaves a "not consulted — Solo mode" note
- [ ] (b) The skip note reads "CD-GDD-ALIGN skipped — Solo mode."
- [ ] Per-section user approval is required in both modes

---

### Case 5: Missing Input and Declined Skeleton

**Fixture:**
- `project.yaml` has `modes.workflow: standard` in every scenario — the systems index is required at this tier, so pointing at `$gs-map-systems` is correct
- Scenario (a): no argument; `design/gdd/systems-index.md` lists `stamina` as the highest-priority "Not Started" system (MVP, Core layer)
- Scenario (b): no argument; no systems index
- Scenario (c): `$gs-design-system stamina` with concept and index present; the user declines the skeleton

**Input:** (a) `$gs-design-system` (b) `$gs-design-system` (c) `$gs-design-system stamina`

**Domain checks:**
- [ ] (a) The next system is proposed from the systems index with the three options
- [ ] (b) The usage message and the `$gs-map-systems` pointer are printed; nothing is written
- [ ] (c) Declining the skeleton produces the BLOCKED verdict and stops before Section A
- [ ] Preserve the case's unresolved human decisions and declines; perform routine writes already authorized, and ask only for missing decisions or scope.

---

### Case 6: Minimal Project, One System Raised by `system_overrides`

**Fixture:**
- `project.yaml` has `modes.workflow: minimal`, `modes.review_mode: solo` and `workflow_overrides.system_overrides.combat: standard`
- `design/game-brief.md` exists; its MVP features describe combat (a damage rule and a stagger threshold), and its build order lists combat first
- No `design/gdd/game-concept.md`, no `design/gdd/systems-index.md`, no `design/gdd/combat.md`

**Input:** `$gs-design-system combat`

**Domain checks:**
- [ ] The run reads the brief and does not stop for the missing concept or systems index
- [ ] The required section set is `standard`'s (the effective tier) — not the project tier's
- [ ] Category, Layer and Priority are derived from the brief and marked inferred in the Quick reference
- [ ] No systems index is created; §5d reports nothing to update
