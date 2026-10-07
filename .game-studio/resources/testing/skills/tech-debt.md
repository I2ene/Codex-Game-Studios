# Evaluation scenarios: gs-tech-debt

Professional scenarios adapted from Donchitos' upstream testing guidance; see
[source attribution](../../../NOTICE.md). These are evaluation inputs and domain
checks, not executed results. Read `.agents/skills/gs-tech-debt/SKILL.md` and its current procedure first.
Use [evaluation policy](../README.md) and [category rubric](../quality-rubric.md).

Resolve current config and project engine records. Apply review-mode discipline
coverage without claiming automatic delegation: use the parent when needed, label it,
and record actual participants only. Existing human authorization governs writes;
case approvals represent unresolved decisions and never revoke prior authorization.
Historical fixture versions are scenario inputs, not current API verification.
The linked native procedure governs command arguments, output schemas, receipts,
context and mode applicability. Missing inputs remain NOT ASSESSED.

### Case 1: Happy Path — Scan appends new findings to an existing register

**Fixture:**
- `project.yaml`: `engine.name: godot`; `modes.automation` unset (collaborative)
- `docs/tech-debt-register.md` is in the skill's Debt Register Format and has 2 `Open` rows:
  - TD-001 — Code Quality, Files `src/core/save_system.gd`: a `# HACK` workaround for a save-path bug. That `HACK` comment is no longer in the file
  - TD-002 — Code Quality, Files `src/gameplay/combat.gd`: the `# TODO` comments in that file
- `src/gameplay/combat.gd` has 2 `# TODO` comments and 1 `# FIXME` comment
- `src/ui/hud.gd` is 620 lines long; 12 source files in `src/` in total

**Input:** `$gs-tech-debt scan`

**Domain checks:**
- [ ] The scan covers the resolved code root `src/` for TODO, FIXME, HACK, `@deprecated`, files >500 lines and functions >50 lines
- [ ] Each finding is assigned one of the six debt categories
- [ ] The number of files scanned is stated with the findings
- [ ] Preserve the case's unresolved human decisions and declines; perform routine writes already authorized, and ask only for missing decisions or scope.
- [ ] The two TODO findings update TD-002 instead of adding a duplicate row
- [ ] TD-001 is proposed as `Resolved [date]` inside the same approval, and is kept in the register rather than deleted
- [ ] New rows take the next IDs (TD-003, TD-004) and carry an `Added` date; the register is updated in place, never replaced
- [ ] Verdict is COMPLETE

---

### Case 2: No Subcommand — Usage and FAIL

**Fixture:**
- `docs/tech-debt-register.md` exists
- `src/` contains source files with TODO comments

**Input:** `$gs-tech-debt`

**Domain checks:**
- [ ] Usage lists the four subcommands
- [ ] No scan is performed and no file is written
- [ ] Verdict is FAIL, stating the subcommand is missing

---

### Case 3: Empty Code Root — NOT ASSESSED, not a clean scan

**Fixture:**
- `project.yaml`: `engine.name: godot`
- `src/` exists but contains no source files
- `docs/tech-debt-register.md` exists with 3 entries

**Input:** `$gs-tech-debt scan`

**Domain checks:**
- [ ] A zero-file scan is reported as NOT ASSESSED — no source files to scan
- [ ] Output does not claim "no debt found" or a clean codebase
- [ ] The register is not written and no write is offered
- [ ] No COMPLETE verdict is emitted

---

### Case 3b: Code Root Unresolved — NOT ASSESSED, nothing scanned on a guess

**Fixture:**
- `project.yaml` has no `engine.name`; `.game-studio/resources/docs/technical-preferences.md` reads `[TO BE CONFIGURED]`
- Both `src/` and `Source/` exist and hold source files, so the tree does not decide the root
- `docs/tech-debt-register.md` exists with 3 entries

**Input:** `$gs-tech-debt scan`

**Domain checks:**
- [ ] Verdict is `NOT ASSESSED — code root unresolved`
- [ ] No debt findings are reported from a guessed root
- [ ] The register is not written and no write is offered

---

### Case 4: Add Mode — User declines the write

**Fixture:**
- `docs/tech-debt-register.md` exists with 4 entries
- `modes.automation` unset (collaborative)

**Input:** `$gs-tech-debt add`

**Domain checks:**
- [ ] Category is collected with `host input tool` offering the six debt categories
- [ ] Effort is collected with `host input tool` offering S / M / L / XL
- [ ] Impact is collected with `host input tool` offering Low / Med / High / Critical, so `prioritize` can score the row
- [ ] The full entry is shown before the append prompt
- [ ] On decline the register is unchanged and the verdict is BLOCKED

---

### Case 4a: Add Mode — Matches an Existing Open Entry

**Fixture:**
- `docs/tech-debt-register.md` exists with an `Open` entry for the same file
  and the same category as the one the user is about to add

**Input:** `$gs-tech-debt add`

**Domain checks:**
- [ ] A new entry with the same file and category as an existing `Open` entry is never appended without first showing the match and asking
- [ ] "Update" edits the matched row rather than adding a new one

---

### Case 4b: Report Mode Without a Register — NOT ASSESSED

**Fixture:**
- `docs/tech-debt-register.md` does not exist

**Input:** `$gs-tech-debt report`

**Domain checks:**
- [ ] Verdict is NOT ASSESSED, not a report of zero items or a "stable" trend
- [ ] The output names `$gs-tech-debt scan` as the way to create the register
- [ ] No file is written

---

### Case 5: Prioritize in Full Review Mode — Scored, re-sorted, approved

**Fixture:**
- `project.yaml`: `modes.review_mode: full`
- `docs/tech-debt-register.md` has 4 entries: TD-001 High/S, TD-002 Low/L, TD-003
  Critical/M, TD-004 Med/— (Effort not yet estimated)

**Input:** `$gs-tech-debt prioritize`

**Domain checks:**
- [ ] Items are scored `impact ÷ effort` from their own columns and re-sorted: TD-001, TD-003, TD-002
- [ ] TD-004 gets no invented score; it is listed as not scored, naming the missing Effort
- [ ] A next-sprint recommendation is given
- [ ] No director gate is invoked in any review mode
- [ ] Preserve the case's unresolved human decisions and declines; perform routine writes already authorized, and ask only for missing decisions or scope.
- [ ] Verdict is COMPLETE
