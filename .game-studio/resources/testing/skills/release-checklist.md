# Evaluation scenarios: gs-release-checklist

Professional scenarios adapted from Donchitos' upstream testing guidance; see
[source attribution](../../../../NOTICE.md). These are evaluation inputs and domain
checks, not executed results. Read `.agents/skills/gs-release-checklist/SKILL.md` and its current procedure first.
Use [evaluation policy](../README.md) and [category rubric](../quality-rubric.md).

Resolve current config and project engine records. Apply review-mode discipline
coverage without claiming automatic delegation: use the parent when needed, label it,
and record actual participants only. Existing human authorization governs writes;
case approvals represent unresolved decisions and never revoke prior authorization.
Historical fixture versions are scenario inputs, not current API verification.
The linked native procedure governs command arguments, output schemas, receipts,
context and mode applicability. Missing inputs remain NOT ASSESSED.

### Case 1: Happy Path — PC Build on the Steam Tier

**Fixture:**
- `platform.cert_tier: steam`; `project.stage: Polish`; `engine.name: Godot`
- `src/` has 40 source files containing 3 TODO, 1 FIXME and 0 HACK comments
- `production/milestones/` holds the current milestone
- `production/qa/bugs/` holds `BUG-0003.md` (S1, `**Status**: Closed`) and
  `BUG-0004.md` (S4, `**Status**: Open`); `modes.rigor` is unset (`workflow: minimal`)
- CI test output exists

**Input:** `$gs-release-checklist pc`

**Domain checks:**
- [ ] TODO/FIXME/HACK counts are reported with the number of files scanned
- [ ] Only the PC device block appears
- [ ] Certification contains Steamworks rows and no itch.io or console certification rows
- [ ] Go / No-Go is READY or NOT READY — never NOT ASSESSED, since every section in this fixture could be assessed
- [ ] The Quality Gates bug line is counted from `production/qa/bugs/` (0 open S1, S2 or S3); the closed S1 and the open S4 fail nothing
- [ ] Preserve the case's unresolved human decisions and declines; perform routine writes already authorized, and ask only for missing decisions or scope.

---

### Case 2: Device Argument and Certification Tier Are Separate Axes

**Fixture:**
- `platform.cert_tier: itch`
- Source files exist in the code root

**Input:** `$gs-release-checklist console`

**Domain checks:**
- [ ] The Console device block is present
- [ ] The only certification block is itch.io
- [ ] No console certification rows (TRC/Lotcheck, first-party submission) appear
- [ ] No Steamworks rows appear

---

### Case 3: cert_tier none vs Unset — Different Output

**Fixture:**
- Run A: `platform.cert_tier: none`
- Run B: `platform.cert_tier` absent (resolved block shows it as unset) and the
  user cannot say which platforms are in scope

**Input:** `$gs-release-checklist` (no argument → device blocks for `all`)

**Domain checks:**
- [ ] Run A shows the "omitted — cert_tier is 'none'" line and no certification rows
- [ ] Run B asks which platforms are in scope
- [ ] Run B's certification section is `NOT ASSESSED — cert tier unknown`, not the `none` line
- [ ] Neither run emits itch.io, Steamworks and console certification together

---

### Case 4: Edge Case — Nothing to Scan, No Test Output

**Fixture:**
- `platform.cert_tier: steam`
- No `engine.name`, no legacy engine value, and none of `src/`, `Assets/`,
  `Source/` exists (code root unresolved)
- No test output directories or CI logs
- `production/qa/bugs/` holds one bug, `BUG-0002.md` (S2, `**Status**: Closed`)

**Input:** `$gs-release-checklist pc`

**Domain checks:**
- [ ] No bare `0` count is reported for TODO/FIXME/HACK
- [ ] Codebase Health is `NOT ASSESSED — code root unresolved`
- [ ] The test-results NOT ASSESSED line is present
- [ ] Go / No-Go is never READY: it is NOT ASSESSED naming both unassessed sections,
- [ ] Preserve the case's unresolved human decisions and declines; perform routine writes already authorized, and ask only for missing decisions or scope.

---

### Case 5: Director Gate Check — None; Sign-Offs Are Listed, Not consult

**Fixture:**
- `platform.cert_tier: console`; source files present
- Any review mode

**Input:** `$gs-release-checklist all`

**Domain checks:**
- [ ] No director gate is invoked and no gate skip message appears
- [ ] No subagent is consulted, although sign-offs are listed
- [ ] The console certification block is the only certification block
- [ ] Next steps name `$gs-gate-check` and `$gs-team-release`

---

### Case 6: A Known Blocker Outranks an Unassessed Section

**Fixture:**
- `platform.cert_tier: steam`; `project.stage: Polish`
- No `engine.name`, no legacy engine value, and none of `src/`, `Assets/`,
  `Source/` exists (code root unresolved)
- CI test output exists
- `production/qa/bugs/BUG-0007.md` is an S1 (Critical) bug with `**Status**: Open`

**Input:** `$gs-release-checklist pc`

**Domain checks:**
- [ ] Go / No-Go is NOT READY — not NOT ASSESSED
- [ ] The S1 bug is listed in the Rationale as a blocking item
- [ ] Codebase Health still shows `NOT ASSESSED — code root unresolved`

---

### Case 7: Bug Thresholds Follow the Workflow Tier

**Fixture:**
- `platform.cert_tier: steam`; source files present; CI test output exists
- Run A: `modes.rigor: standard` (`workflow: standard`); `production/qa/bugs/BUG-0012.md`
  is an S2 (High) bug with `**Status**: Open`, and no other bug is open
- Run B: `modes.rigor: full` (`workflow: full`); `production/qa/bugs/BUG-0013.md`
  is an S3 (Medium) bug with `**Status**: Open`, and no other bug is open

**Input:** `$gs-release-checklist pc`

**Domain checks:**
- [ ] Run A's Go / No-Go is not NOT READY because of the S2, and the S2 appears in the Rationale as a risk
- [ ] Run B's Go / No-Go is NOT READY, naming BUG-0013 as a blocking item
- [ ] Neither run offers a "documented exception" for the S3 at `workflow: full`

---

### Case 8: No Bug Records — NOT ASSESSED, Not Zero

**Fixture:**
- `platform.cert_tier: steam`; source files present; CI test output exists
- `production/qa/bugs/` does not exist

**Input:** `$gs-release-checklist pc`

**Domain checks:**
- [ ] No bare `0` bug count and no ticked "Zero open S1 (Critical) bugs" item
- [ ] `NOT ASSESSED — no bug records` appears
- [ ] Go / No-Go is not READY
