# Evaluation scenarios: gs-test-evidence-review

Professional scenarios adapted from Donchitos' upstream testing guidance; see
[source attribution](../../../../NOTICE.md). These are evaluation inputs and domain
checks, not executed results. Read `.agents/skills/gs-test-evidence-review/SKILL.md` and its current procedure first.
Use [evaluation policy](../README.md) and [category rubric](../quality-rubric.md).

Resolve current config and project engine records. Apply review-mode discipline
coverage without claiming automatic delegation: use the parent when needed, label it,
and record actual participants only. Existing human authorization governs writes;
case approvals represent unresolved decisions and never revoke prior authorization.
Historical fixture versions are scenario inputs, not current API verification.
The linked native procedure governs command arguments, output schemas, receipts,
context and mode applicability. Missing inputs remain NOT ASSESSED.

### Case 1: Happy Path — Single Logic story with a strong test

**Fixture:**
- `project.yaml`: `engine.name: godot`, so the unit-test root is `tests/unit/`; `modes.automation` unset (collaborative)
- `production/epics/combat/story-001-damage-calc.md` (slug `damage-calc`): `## Test Evidence` gives Story Type Logic and the path `tests/unit/combat/damage-calc_test.gd`; `## Acceptance Criteria` includes "damage is never below 1" and "critical hits multiply damage by 2.0"
- `tests/unit/combat/damage-calc_test.gd` opens with `# Story: production/epics/combat/story-001-damage-calc.md`, has 4 test functions with 3+ assertions each, named like `test_damage_calc_zero_armor_returns_base_damage` and `test_damage_calc_max_crit_doubles_damage`, and names the GDD's `damage_formula` in a comment

**Input:** `$gs-test-evidence-review production/epics/combat/story-001-damage-calc.md`

**Domain checks:**
- [ ] The test file is located under `tests/unit/combat/` for the Logic story
- [ ] Assertion coverage, edge cases, naming and formula traceability are each reported
- [ ] Story verdict is ADEQUATE
- [ ] Preserve the case's unresolved human decisions and declines; perform routine writes already authorized, and ask only for missing decisions or scope.
- [ ] Run ends with COMPLETE

---

### Case 2: Vacuous and Thin Tests — INCOMPLETE with a BLOCKING item

**Fixture:**
- `project.yaml`: `engine.name: godot`, `modes.rigor: standard` (so `qa.level: standard` — tests are required); no `testing.strict` block
- `production/epics/combat/story-002-crit-roll.md` (slug `crit-roll`): Story Type Logic
- `tests/unit/combat/crit-roll_test.gd` has `func test_1()` with no assertions and `func test_crit_roll_applies_multiplier()` with one assertion

**Input:** `$gs-test-evidence-review production/epics/combat/story-002-crit-roll.md`

**Domain checks:**
- [ ] A test function with zero assertions is flagged BLOCKING
- [ ] `test_1` is flagged as a naming issue
- [ ] Story verdict is INCOMPLETE, not ADEQUATE
- [ ] Output states BLOCKING items must be resolved before `$gs-story-done` and suggests `$gs-test-helpers`
- [ ] Run ends with CONCERNS
- [ ] The test file is not modified
- [ ] Variant — with `testing.strict.logic: false` in `project.yaml`, the zero-assertion finding is ADVISORY, the story is still INCOMPLETE, and the run ends COMPLETE

---

### Case 3: Empty Sprint Scope at Minimal Workflow — NOT ASSESSED, not a clean report

**Fixture:**
- `project.yaml`: `modes.rigor: minimal` (the resolved block shows `workflow: minimal`)
- `production/sprints/` does not exist

**Input:** `$gs-test-evidence-review sprint`

**Domain checks:**
- [ ] Verdict is NOT ASSESSED — no stories in scope
- [ ] Output names which scope was searched and which path was empty
- [ ] At minimal workflow the route is `$gs-test-evidence-review [epic-slug]`, not `$gs-sprint-plan new`
- [ ] No empty report reading "BLOCKING items: 0 / ADVISORY items: 0" is produced

---

### Case 4: Story Type Unknown — Per-story NOT ASSESSED lifts the overall verdict

**Fixture:**
- `project.yaml`: `engine.name: godot`
- `production/epics/combat/` contains `story-001-damage-calc.md` (Logic, test as in Case 1) and `story-003-hit-feedback.md`, whose `## Test Evidence` section states no Story Type and no evidence path
- Full-reading `story-003-hit-feedback.md` does not reveal a type either

**Input:** `$gs-test-evidence-review combat`

**Domain checks:**
- [ ] The untyped story is NOT ASSESSED, not MISSING
- [ ] The NOT ASSESSED reason (type cannot be determined) is stated for that story
- [ ] Overall verdict is NOT ASSESSED, not ADEQUATE
- [ ] The typed story is still reviewed and reported ADEQUATE

---

### Case 5: Visual/Feel Evidence Without a Retained Screenshot, Full Review Mode — No gates

**Fixture:**
- `project.yaml`: `engine.name: godot`, `modes.review_mode: full`
- `production/epics/combat/story-004-hit-flash.md` (slug `hit-flash`): Story Type Visual/Feel
- `production/qa/evidence/hit-flash-evidence.md` references every acceptance criterion, has every sign-off filled, and is dated after the sprint start
- No `*.png`, `*.jpg` or `*.gif` for this story exists in `production/qa/evidence/`

**Input:** `$gs-test-evidence-review production/epics/combat/story-004-hit-flash.md`

**Domain checks:**
- [ ] A Visual/Feel evidence doc with no retained image is INCOMPLETE, even with complete sign-offs
- [ ] The missing screenshot is listed as a BLOCKING issue
- [ ] No director gate is invoked in any review mode
- [ ] The evidence document is not modified

---

### Case 6: UI Story Closed by Its Screenshots — No Sign-Off Required

**Fixture:**
- `project.yaml`: `engine.name: godot`
- `production/epics/ui/story-007-inventory-screen.md` (slug `inventory-screen`): Story Type UI; its
  `## Test Evidence` names `production/qa/evidence/inventory-screen-populated.png` and
  `production/qa/evidence/inventory-screen-empty.png` — one per screen state it touches
- Both images exist and are dated after the sprint start
- No `inventory-screen-evidence.md`, no sign-off record and no walkthrough log exist

**Input:** `$gs-test-evidence-review production/epics/ui/story-007-inventory-screen.md`

**Domain checks:**
- [ ] The story's stated evidence paths are checked first, and both images are found
- [ ] The missing sign-off does not make the story INCOMPLETE — a UI story needs none
- [ ] No walkthrough log is demanded
- [ ] Story verdict is ADEQUATE

---

### Case 7: Unity Logic Story — Evidence at the Stated Engine Path

**Fixture:**
- `project.yaml`: `engine.name: unity`
- `production/epics/inventory/story-003-stack-merge.md`: Story Type Logic; its
  `## Test Evidence` names `Assets/Tests/EditMode/InventoryTests.cs`
- That file exists and holds one `[Test]` per acceptance criterion (4 in all), each with 3 or more `Assert.That` calls, named in the `[Scenario]_[Expected]` form (`MergeStacks_FullStack_SpillsToNewSlot`), with the empty-stack and max-stack cases covered
- The inventory GDD has no Formulas section, so formula traceability does not apply
- Nothing named `stack-merge_test.*` exists anywhere, and `tests/unit/` does not exist

**Input:** `$gs-test-evidence-review production/epics/inventory/story-003-stack-merge.md`

**Domain checks:**
- [ ] The test is found at the stated Unity path — the story is not reported MISSING
- [ ] The review does not require a `[story-slug]_test.*` name or a `tests/unit/` location

---

### Case 8: No Test for a Logic Story — MISSING, and it outranks NOT ASSESSED

**Fixture:**
- `project.yaml`: `engine.name: godot`, `modes.rigor: standard` (so `qa.level: standard` — a Logic story's test is required)
- `production/epics/combat/` contains `story-003-hit-feedback.md` (no Story Type, as in Case 4) and `story-005-knockback.md`: Story Type Logic, no evidence path stated
- No test exists for it: `tests/unit/combat/` does not exist, and no other test file names the slug `knockback` or references the story

**Input:** `$gs-test-evidence-review combat`

**Domain checks:**
- [ ] The Logic story with no test file is MISSING, not NOT ASSESSED
- [ ] The untyped story is NOT ASSESSED, not MISSING — the two are kept apart
- [ ] Overall verdict is MISSING, not NOT ASSESSED
- [ ] The missing test is listed as BLOCKING and the run ends with CONCERNS

---

### Case 9: `qa.level: minimal` — a Logic Story With No Test Is WAIVED; a UI Screenshot Is Not

**Fixture:**
- `project.yaml`: `engine.name: godot`, no `modes` block (so `qa.level: minimal` — tests are waived)
- `production/epics/combat/` contains `story-005-knockback.md` (Logic, no test anywhere, as in Case 8) and `story-008-pause-menu.md` (UI, no retained image for it in `production/qa/evidence/`)

**Input:** `$gs-test-evidence-review combat`

**Domain checks:**
- [ ] The Logic story with no test is WAIVED (qa.level: minimal), not MISSING, and is not listed as BLOCKING
- [ ] The UI story with no screenshot is still MISSING and BLOCKING at `qa.level: minimal`
- [ ] The waived story is named as waived in the report, not dropped from it
- [ ] Variant: an all-waived scope reads WAIVED, with no "must be resolved before `$gs-story-done`" prompt
