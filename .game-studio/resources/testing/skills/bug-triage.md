# Evaluation scenarios: gs-bug-triage

Professional scenarios adapted from Donchitos' upstream testing guidance; see
[source attribution](../../../NOTICE.md). These are evaluation inputs and domain
checks, not executed results. Read `.agents/skills/gs-bug-triage/SKILL.md` and its current procedure first.
Use [evaluation policy](../README.md) and [category rubric](../quality-rubric.md).

Resolve current config and project engine records. Apply review-mode discipline
coverage without claiming automatic delegation: use the parent when needed, label it,
and record actual participants only. Existing human authorization governs writes;
case approvals represent unresolved decisions and never revoke prior authorization.
Historical fixture versions are scenario inputs, not current API verification.
The linked native procedure governs command arguments, output schemas, receipts,
context and mode applicability. Missing inputs remain NOT ASSESSED.

### Case 1: Happy Path — Sprint mode, 5 bugs grouped by priority

**Fixture:**
- `production/sprints/sprint-004.md` is the newest sprint file and notes spare capacity
- `production/qa/bugs/` contains 5 bug files:
  - `BUG-0001.md` — S1, P1, Audio
  - `BUG-0002.md` — S2, P1, Combat
  - `BUG-0003.md` — S3, P2, UI
  - `BUG-0004.md` — S2, P2, VFX
  - `BUG-0005.md` — S4, P3, Tutorial

**Input:** `$gs-bug-triage`

**Domain checks:**
- [ ] Mode reported as `sprint`
- [ ] BUG-0001 and BUG-0002 are in the "P1 Bugs — Fix This Sprint" table, assigned to the current sprint
- [ ] BUG-0003 and BUG-0004 are in the P2 table; BUG-0005 is in the P3/P4 table
- [ ] Triage Summary counts and the S1/S2 unfixed count (3) are correct
- [ ] Preserve the case's unresolved human decisions and declines; perform routine writes already authorized, and ask only for missing decisions or scope.

---

### Case 2: No Bug Files Found — Stops without a report

**Fixture:**
- `production/qa/bugs/` does not exist
- No `production/qa/bugs.md` and no `production/qa/qa-plan-*.md`

**Input:** `$gs-bug-triage`

**Domain checks:**
- [ ] No triage report file is written when no bug source exists.
- [ ] Output states that no bug files were found in `production/qa/bugs/`
- [ ] Skill stops gracefully rather than erroring
- [ ] No triage tables are produced
- [ ] Preserve the case's unresolved human decisions and declines; perform routine writes already authorized, and ask only for missing decisions or scope.
- [ ] The stop still ends with a verdict: Verdict: COMPLETE — no bug files, nothing to triage

---

### Case 3: Systemic Issues — Deviation check flags a hot spot and a regression

**Fixture:**
- `production/sprints/sprint-004.md` exists
- `production/qa/bugs/` holds 4 bugs: 3 in the Inventory system filed this sprint,
  and 1 filed against `production/epics/core/story-003.md`, whose `Status: Complete`
- The user approves the write when asked

**Input:** `$gs-bug-triage sprint`

**Domain checks:**
- [ ] Inventory is flagged as a potential quality issue (3+ bugs in one system)
- [ ] The bug against the Complete story is flagged as a regression
- [ ] Trend Analysis shows Inventory as the hot spot and "Regressions: 1"
- [ ] Preserve the case's unresolved human decisions and declines; perform routine writes already authorized, and ask only for missing decisions or scope.
- [ ] The post-write message recommends `$gs-smoke-check`, and the verdict is COMPLETE

---

### Case 4: Sprint at Capacity — Overflow flagged, Won't Fix asked, write declined

**Fixture:**
- `production/sprints/sprint-004.md` notes the sprint is at full capacity
- `production/qa/bugs/` holds one S2/P1 bug and one S4 bug judged P4 (cosmetic, out of scope)

**Input:** `$gs-bug-triage sprint`

**Domain checks:**
- [ ] P1 bug carries the `Priority overflow` flag instead of a sprint assignment
- [ ] The Won't Fix question is asked before any bug is dispositioned P4
- [ ] Verdict is BLOCKED when the write is declined
- [ ] `production/qa/bug-triage-[date].md` is not written

---

### Case 5: Director Gate Check — Full mode, no P1 bugs

**Fixture:**
- No sprint file in `production/sprints/`
- `production/qa/bugs/` holds two bugs, S3/P3 and S4/P3

**Input:** `$gs-bug-triage full`

**Domain checks:**
- [ ] "No sprint plan found — assigning to backlog only." is stated
- [ ] Both bugs are dispositioned Backlog
- [ ] "No P1 bugs — build is in good shape for QA hand-off." appears with Verdict COMPLETE
- [ ] No director gate is invoked and no gate skip messages appear
