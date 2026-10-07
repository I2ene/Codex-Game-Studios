# Evaluation scenarios: gs-day-one-patch

Professional scenarios adapted from Donchitos' upstream testing guidance; see
[source attribution](../../../NOTICE.md). These are evaluation inputs and domain
checks, not executed results. Read `.agents/skills/gs-day-one-patch/SKILL.md` and its current procedure first.
Use [evaluation policy](../README.md) and [category rubric](../quality-rubric.md).

Resolve current config and project engine records. Apply review-mode discipline
coverage without claiming automatic delegation: use the parent when needed, label it,
and record actual participants only. Existing human authorization governs writes;
case approvals represent unresolved decisions and never revoke prior authorization.
Historical fixture versions are scenario inputs, not current API verification.
The linked native procedure governs command arguments, output schemas, receipts,
context and mode applicability. Missing inputs remain NOT ASSESSED.

### Case 1: Happy Path — Scope, rollback plan first, fixes, patch record

**Fixture:**
- `project.yaml` has `project.stage: Release`
- The most recent file in `production/gate-checks/` records a release-gate PASS
- `production/qa/bugs/` holds three Open bugs:
  - `BUG-0010` — S2, P1, code fix estimated at 2 hours
  - `BUG-0011` — S3, a one-value config/data fix
  - `BUG-0012` — S2, fix requires an architecture change

**Input:** `$gs-day-one-patch`

**Domain checks:**
- [ ] BUG-0012 is deferred to 1.1 because it needs an architecture change
- [ ] Scope is approved via `host input tool` before any work
- [ ] The rollback plan is written before any fix is attempted
- [ ] Preserve the case's unresolved human decisions and declines; perform routine writes already authorized, and ask only for missing decisions or scope.
- [ ] BUG-0011 is fixed without consulting `lead-programmer`
- [ ] Next steps include `$gs-patch-notes`

---

### Case 2: Critical Bug That Cannot Be Fixed Safely — Accepted risk, rollback trigger

**Fixture:**
- Release stage; release-gate PASS on record
- `production/qa/bugs/` holds `BUG-0020` — S1 (save-file data loss) whose fix needs
  an architecture change — and `BUG-0021` — S2, P1, 1-hour fix

**Input:** `$gs-day-one-patch`

**Domain checks:**
- [ ] BUG-0020 appears in the deferred table with its reason (architecture change)
- [ ] BUG-0021 is still patched — the S1 does not block the rest of the patch
- [ ] The "S1 bugs remain open" warning is shown after the record is written
- [ ] The warning points to the rollback plan's trigger conditions

---

### Case 3: No Release-Gate Record — NOT ASSESSED, not assumed

**Fixture:**
- `project.yaml` has `project.stage: Release`
- `production/gate-checks/` is empty (no release-gate record)
- Open bugs exist in `production/qa/bugs/`

**Input:** `$gs-day-one-patch`

**Domain checks:**
- [ ] `Release gate: NOT ASSESSED — no gate-check record found` is reported
- [ ] `project.stage: Release` alone is not treated as proof the gate passed
- [ ] User is offered `$gs-gate-check` first or a full QA pass
- [ ] No rollback plan, fix or patch record is produced before the user answers

---

### Case 4: Nothing Worth Patching — User selects "No day-one patch needed"

**Fixture:**
- Release stage; release-gate PASS on record
- `production/qa/bugs/` holds only two S4 cosmetic bugs that need code changes

**Input:** `$gs-day-one-patch`

**Domain checks:**
- [ ] Both S4 bugs are listed as deferred, not included
- [ ] On `[C]`, "No day-one patch required. Proceed to `$gs-launch-checklist`." is shown
- [ ] Skill stops without writing any file
- [ ] No `release-manager`, `lead-programmer` or `qa-lead` is consulted

---

### Case 5: Director Gate Check — Patch QA NOT ASSESSED is not a pass

**Fixture:**
- `project.yaml`: `modes.rigor: standard` (so a project with no game tests gets NOT ASSESSED, not WAIVED)
- Release stage; release-gate PASS on record; one included S2/P1 fix implemented
- `qa-lead` chooses a targeted smoke check; `$gs-smoke-check` returns
  `NOT ASSESSED — no game tests found`

**Input:** `$gs-day-one-patch`

**Domain checks:**
- [ ] NOT ASSESSED does not let the patch proceed as if it passed
- [ ] The fix is either re-verified with a real result or deferred to 1.1
- [ ] No creative-director, technical-director, producer or art-director is consulted
- [ ] Any written record states the QA verdict and what was not assessed
