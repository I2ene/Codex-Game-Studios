# Evaluation scenarios: gs-qa-plan

Professional scenarios adapted from Donchitos' upstream testing guidance; see
[source attribution](../../../../NOTICE.md). These are evaluation inputs and domain
checks, not executed results. Read `.agents/skills/gs-qa-plan/SKILL.md` and its current procedure first.
Use [evaluation policy](../README.md) and [category rubric](../quality-rubric.md).

Resolve current config and project engine records. Apply review-mode discipline
coverage without claiming automatic delegation: use the parent when needed, label it,
and record actual participants only. Existing human authorization governs writes;
case approvals represent unresolved decisions and never revoke prior authorization.
Historical fixture versions are scenario inputs, not current API verification.
The linked native procedure governs command arguments, output schemas, receipts,
context and mode applicability. Missing inputs remain NOT ASSESSED.

### Case 1: Happy Path — Sprint With Four Typed Stories

**Fixture:**
- `production/sprints/sprint-003.md` is the most recent sprint and references 4
  story files, each with acceptance criteria and a declared Type: Logic,
  Integration, Visual/Feel, UI
- The stories reference GDDs in `design/gdd/`; `engine.name: Godot`
- `qa.level: standard`; `modes.automation: collaborative`

**Input:** `$gs-qa-plan sprint`

**Domain checks:**
- [ ] All 4 stories appear in the plan, each with its declared Type unchanged
- [ ] The classification summary table appears before the plan
- [ ] Logic and Integration rows name test paths under `tests/unit/` and `tests/integration/`
- [ ] The UI row's manual verification is the retained screenshot of each screen touched, not a step-through
- [ ] Preserve the case's unresolved human decisions and declines; perform routine writes already authorized, and ask only for missing decisions or scope.
- [ ] Next steps name `$gs-smoke-check sprint` and `$gs-story-done`

---

### Case 2: Story Without Acceptance Criteria and a Missing Story File

**Fixture:**
- The most recent sprint file references 4 story paths
- One story has no `## Acceptance Criteria` section
- One referenced story path does not exist on disk
- The other 2 stories are complete

**Input:** `$gs-qa-plan sprint`

**Domain checks:**
- [ ] The missing file is reported as MISSING without failing the whole plan
- [ ] The story with no acceptance criteria is full-read and reported as a QA finding
- [ ] That story is not silently dropped from the plan
- [ ] The two complete stories receive normal test assignments

---

### Case 3: Mode Variant — qa.level minimal

**Fixture:**
- Same 4-story sprint as Case 1
- `qa.level: minimal`

**Input:** `$gs-qa-plan sprint`

**Domain checks:**
- [ ] No "Automated Tests Required" section appears
- [ ] The Test Summary's automated-test column is blank
- [ ] The Definition of Done has no test-file or smoke-check rows
- [ ] The Definition of Done still requires the retained screenshot for the Visual/Feel and UI stories, and the signed-off evidence doc for the Visual/Feel story
- [ ] Preserve the case's unresolved human decisions and declines; perform routine writes already authorized, and ask only for missing decisions or scope.

---

### Case 4: No Sprint Plan — NOT ASSESSED

**Fixture:**
- `production/sprints/` contains no files
- No `production/sprint-status.yaml`
- `modes.rigor: standard` (so sprints are expected)

**Input:** `$gs-qa-plan sprint`

**Domain checks:**
- [ ] Verdict is `NOT ASSESSED — no stories in scope`
- [ ] The empty path `production/sprints/` is named
- [ ] `$gs-sprint-plan new` is suggested
- [ ] No plan document with empty tables is produced, and nothing is written

---

### Case 5: Director Gate Check — None

**Fixture:**
- A sprint with typed stories and acceptance criteria
- Any review mode

**Input:** `$gs-qa-plan sprint`

**Domain checks:**
- [ ] No director gate is invoked and no gate skip message appears
- [ ] No subagent is consulted
- [ ] Phases 2–4 run without asking the user anything
- [ ] Exactly one approval prompt precedes the write
