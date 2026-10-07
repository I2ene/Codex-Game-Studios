# Evaluation scenarios: gs-regression-suite

Professional scenarios adapted from Donchitos' upstream testing guidance; see
[source attribution](../../../../NOTICE.md). These are evaluation inputs and domain
checks, not executed results. Read `.agents/skills/gs-regression-suite/SKILL.md` and its current procedure first.
Use [evaluation policy](../README.md) and [category rubric](../quality-rubric.md).

Resolve current config and project engine records. Apply review-mode discipline
coverage without claiming automatic delegation: use the parent when needed, label it,
and record actual participants only. Existing human authorization governs writes;
case approvals represent unresolved decisions and never revoke prior authorization.
Historical fixture versions are scenario inputs, not current API verification.
The linked native procedure governs command arguments, output schemas, receipts,
context and mode applicability. Missing inputs remain NOT ASSESSED.

### Case 1: Audit — Criteria Mapped, Formula Gap Raised to HIGH

**Fixture:**
- `qa.level: standard`; workflow tier `full`; `project.stage: Polish`
- `design/gdd/systems-index.md` lists `combat`; `design/gdd/combat.md` has 4
  acceptance criteria: a damage formula, a hit-stun state transition, a
  knockback rule and a HUD damage-number display
- `tests/unit/combat/` has tests for hit-stun (all cases) and knockback (happy
  path only); nothing tests the damage formula
- `tests/regression-suite.md` exists

**Input:** `$gs-regression-suite audit`

**Domain checks:**
- [ ] Each criterion gets one of COVERED / PARTIAL / MISSING / EXEMPT, matching the fixture
- [ ] The HUD criterion is EXEMPT and excluded from the coverage rate
- [ ] The damage-formula gap is HIGH PRIORITY with a `tests/unit/combat/` path
- [ ] Preserve the case's unresolved human decisions and declines; perform routine writes already authorized, and ask only for missing decisions or scope.
- [ ] Verdict is COMPLETE and `$gs-test-helpers` is suggested

---

### Case 2: Update — Fixed Bug Without a Regression Test

**Fixture:**
- `qa.level: standard`; `project.stage: Polish`
- `production/sprints/sprint-007.md` is the current sprint plan; its one
  `Status: Complete` story is `production/epics/inventory/story-003.md`
- `production/qa/bugs/BUG-0012.md` has `Status: Closed`, system `inventory`
- No test under `tests/unit/inventory/` or `tests/integration/inventory/`
  references BUG-0012 or its failure scenario
- `tests/regression-suite.md` has 6 registered tests

**Input:** `$gs-regression-suite update`

**Domain checks:**
- [ ] BUG-0012 is reported as MISSING REGRESSION TEST
- [ ] The suggested path follows `tests/unit/[system]/[bug-slug]_regression_test.[ext]`
- [ ] No existing manifest entry is removed
- [ ] The next-sprint story recommendation appears because bug regression gaps > 0
- [ ] Verdict is COMPLETE after approval

---

### Case 3: qa.level minimal — Suite Not Generated

**Fixture:**
- `qa.level: minimal`
- GDDs and test files exist

**Input:** `$gs-regression-suite audit`

**Domain checks:**
- [ ] The "not generated at qa.level minimal" message is shown
- [ ] No GDD, test or bug scan runs
- [ ] The smoke-report branch is not entered on account of `qa.level`
- [ ] Preserve the case's unresolved human decisions and declines; perform routine writes already authorized, and ask only for missing decisions or scope.
- [ ] Verdict is NOT ASSESSED — not COMPLETE, and not a stop without a verdict

---

### Case 4: Edge Case — No Test Files, Coverage NOT ASSESSED

**Fixture:**
- `qa.level: standard`; workflow tier `full`; `project.stage: Polish`
- `design/gdd/` holds GDDs with acceptance criteria
- `tests/unit/`, `tests/integration/` and `tests/regression/` contain no files
- The user approves the manifest write

**Input:** `$gs-regression-suite audit`

**Domain checks:**
- [ ] No `0%` (or any percentage) coverage figure is reported
- [ ] Coverage reads `NOT ASSESSED — no test files found`
- [ ] `$gs-test-setup` is named as the producing skill
- [ ] Preserve the case's unresolved human decisions and declines; perform routine writes already authorized, and ask only for missing decisions or scope.
- [ ] Verdict is NOT ASSESSED — never COMPLETE over a coverage figure that was not computed

---

### Case 5: Director Gate Check — None; Report Mode Is Read-Only

**Fixture:**
- `qa.level: standard`; `project.stage: Polish`
- `tests/regression-suite.md`, tests and closed bugs exist
- Any review mode

**Input:** `$gs-regression-suite report`

**Domain checks:**
- [ ] No director gate is invoked and no gate skip message appears
- [ ] No subagent is consulted
- [ ] The status report is shown in conversation
- [ ] Preserve the case's unresolved human decisions and declines; perform routine writes already authorized, and ask only for missing decisions or scope.
