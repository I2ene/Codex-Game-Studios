# Evaluation scenarios: gs-milestone-review

Professional scenarios adapted from Donchitos' upstream testing guidance; see
[source attribution](../../../../NOTICE.md). These are evaluation inputs and domain
checks, not executed results. Read `.agents/skills/gs-milestone-review/SKILL.md` and its current procedure first.
Use [evaluation policy](../README.md) and [category rubric](../quality-rubric.md).

Resolve current config and project engine records. Apply review-mode discipline
coverage without claiming automatic delegation: use the parent when needed, label it,
and record actual participants only. Existing human authorization governs writes;
case approvals represent unresolved decisions and never revoke prior authorization.
Historical fixture versions are scenario inputs, not current API verification.
The linked native procedure governs command arguments, output schemas, receipts,
context and mode applicability. Missing inputs remain NOT ASSESSED.

### Case 1: Happy Path — Nearly complete milestone with one deferred feature

**Fixture:**
- `production/milestones/milestone-03.md` exists (milestone-definition template)
  with 8 features in its Feature List
- 7 features have `Status: Complete`
- 1 feature has `Status: Deferred` (deferred to milestone-04)
- `production/sprints/sprint-007.md` through `sprint-009.md` exist with the
  headings `$gs-sprint-plan` writes
- The features' stories exist under `production/epics/`; none is `Blocked`
- `project.yaml` sets `modes.review_mode: full`
- The producer returns ON TRACK

**Input:** `$gs-milestone-review milestone-03`

**Domain checks:**
- [ ] The deferred feature is not listed under Fully Complete and is not counted as complete in the completion percentage (7 of 8)
- [ ] PR-MILESTONE is consulted in full mode before the Go/No-Go recommendation, with completion percentage and blocked story count passed
- [ ] The producer's ON TRACK verdict appears inline in the Go/No-Go section, and no framing `host input tool` is raised (only AT RISK and OFF TRACK raise one)
- [ ] Preserve the case's unresolved human decisions and declines; perform routine writes already authorized, and ask only for missing decisions or scope.
- [ ] Verdict is COMPLETE after the write

---

### Case 2: Blocked Milestone — Producer returns OFF TRACK

**Fixture:**
- `production/milestones/milestone-03.md` lists 5 features
- 2 features have `Status: Complete`
- 3 features have `Status: Blocked`; each has one story under
  `production/epics/[its epic]/` whose file carries `> **Status**: Blocked` and
  a `BLOCKED:` note naming its blocker
- Sprint reports exist in `production/sprints/`; they name no blockers
- `project.yaml` sets `modes.review_mode: full`
- The producer returns OFF TRACK

**Input:** `$gs-milestone-review milestone-03`

**Domain checks:**
- [ ] Each blocked feature is named in the Blocked table with its blocker, taken from its story's `BLOCKED:` note — the sprint reports carry none, so a blocker not read from the story files is invented
- [ ] PR-MILESTONE receives the blocked story count (3), counted from the story files
- [ ] OFF TRACK raises the `host input tool` with Accept NO-GO / Override to CONDITIONAL GO / Stop before the recommendation is generated
- [ ] After [A], the recommendation is NO-GO — the skill does not issue GO against an OFF TRACK verdict
- [ ] Preserve the case's unresolved human decisions and declines; perform routine writes already authorized, and ask only for missing decisions or scope.

---

### Case 3: Full Mode — PR-MILESTONE returns AT RISK over scope drift

**Fixture:**
- `production/milestones/milestone-03.md` lists 6 complete features, 2 of which
  were not in the original definition (added mid-milestone)
- Sprint reports exist in `production/sprints/`
- `project.yaml` sets `modes.review_mode: full`
- The producer returns AT RISK, citing the 2 added features as scope drift and
  listing mitigations

**Input:** `$gs-milestone-review milestone-03`

**Domain checks:**
- [ ] The producer's AT RISK assessment, including its scope-drift finding, is shown inline in the Go/No-Go section — not suppressed
- [ ] AT RISK raises the `host input tool` with CONDITIONAL GO / NO-GO / GO before the file is written
- [ ] After [A], the recommendation is CONDITIONAL GO and its Conditions list carries the producer's conditions
- [ ] Preserve the case's unresolved human decisions and declines; perform routine writes already authorized, and ask only for missing decisions or scope.

---

### Case 4: Edge Case — No milestone definition and no sprint data

**Fixture:**
- `production/milestones/` does not exist
- `production/sprints/` does not exist
- `production/risk-register/` does not exist
- No source files exist under the code root
- No story files, no `production/sprint-status.yaml` and no `production/qa/bugs/`
- `project.yaml` sets `modes.review_mode: full`

**Input:** `$gs-milestone-review current`

**Domain checks:**
- [ ] Skill does not crash and does not fill the review template with estimated values
- [ ] Verdict is `NOT ASSESSED — NO DATA` — not GO and not COMPLETE
- [ ] Output names the missing inputs and where each comes from (`$gs-sprint-plan` for sprint reports; the milestone-definition template for milestones)
- [ ] Preserve the case's unresolved human decisions and declines; perform routine writes already authorized, and ask only for missing decisions or scope.

---

### Case 5: Lean/Solo Mode — PR-MILESTONE gate skipped

**Fixture:**
- `production/milestones/milestone-03.md` lists 5 features, all `Status: Complete`
- Sprint reports exist in `production/sprints/`
- `production/qa/bugs/` does not exist — no bug has been filed with `$gs-bug-report`
- `project.yaml` sets `modes.review_mode: solo`

**Input:** `$gs-milestone-review milestone-03`

**Domain checks:**
- [ ] PR-MILESTONE gate is NOT invoked in solo mode
- [ ] Output contains "PR-MILESTONE skipped — Solo mode."
- [ ] The Go/No-Go section carries no producer verdict (no ON TRACK / AT RISK / OFF TRACK attributed to the producer)
- [ ] The Quality Metrics bug lines read `NOT ASSESSED — NO DATA` — not "0" — while the sections that have inputs are still produced
- [ ] User approval is still required before the write
- [ ] Verdict is COMPLETE after the write

---

### Case 6: Lean Mode from Rigor — PR-MILESTONE skipped with the Lean note

**Fixture:**
- `production/milestones/milestone-03.md` lists 4 features, all `Status: Complete`
- Sprint reports exist in `production/sprints/`
- `project.yaml` sets `modes.rigor: standard` and pins no review mode, so the
  injected block reads `review_mode: lean (rigor:standard)`

**Input:** `$gs-milestone-review milestone-03`

**Domain checks:**
- [ ] PR-MILESTONE gate is NOT invoked in lean mode
- [ ] Output contains "PR-MILESTONE skipped — Lean mode." — not the Solo note
- [ ] The Go/No-Go section carries no producer verdict
- [ ] User approval is still required before the write, and the verdict is COMPLETE after it

---

### Case 7: Gate returns NOT ASSESSED — Never GO

**Fixture:**
- `production/milestones/milestone-03.md` lists 5 features, all `Status: Complete`,
  but gives no Target Date
- Sprint reports exist in `production/sprints/`; the stories exist under
  `production/epics/` and none is `Blocked`
- `project.yaml` sets `modes.review_mode: full`
- The producer returns NOT ASSESSED — no target date to judge against
- Asked for the date, the user has none to give

**Input:** `$gs-milestone-review milestone-03`

**Domain checks:**
- [ ] The Go/No-Go recommendation is NOT ASSESSED — never GO — although every feature is Complete
- [ ] The missing target date is named in the Go/No-Go section
- [ ] The AT RISK and OFF TRACK framing questions are not raised for NOT ASSESSED
- [ ] Preserve the case's unresolved human decisions and declines; perform routine writes already authorized, and ask only for missing decisions or scope.
