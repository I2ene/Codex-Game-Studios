# Evaluation scenarios: gs-bug-report

Professional scenarios adapted from Donchitos' upstream testing guidance; see
[source attribution](../../../NOTICE.md). These are evaluation inputs and domain
checks, not executed results. Read `.agents/skills/gs-bug-report/SKILL.md` and its current procedure first.
Use [evaluation policy](../README.md) and [category rubric](../quality-rubric.md).

Resolve current config and project engine records. Apply review-mode discipline
coverage without claiming automatic delegation: use the parent when needed, label it,
and record actual participants only. Existing human authorization governs writes;
case approvals represent unresolved decisions and never revoke prior authorization.
Historical fixture versions are scenario inputs, not current API verification.
The linked native procedure governs command arguments, output schemas, receipts,
context and mode applicability. Missing inputs remain NOT ASSESSED.

### Case 1: Happy Path — User describes a crash, full report produced

**Fixture:**
- `production/qa/bugs/` does not exist yet
- The code root contains a boss-arena scene script

**Input:** `$gs-bug-report The game crashes to desktop every time the player enters the boss arena — progress is blocked`

**Domain checks:**
- [ ] Report contains Title, ID, Severity, Priority, Status, Category, System, Build, Reproduction Steps, Expected Result and Actual Result
- [ ] Severity uses the S1–S4 scale (`S1-Critical` here) and Priority uses the P1–P4 labels
- [ ] "Likely affected files" is filled from the codebase search
- [ ] Preserve the case's unresolved human decisions and declines; perform routine writes already authorized, and ask only for missing decisions or scope.
- [ ] Variant — with `BUG-0001.md` and `BUG-0003.md` already present, the new ID is
- [ ] Verdict is COMPLETE after the write
- [ ] `$gs-hotfix [BUG-ID]` is suggested because severity is S1

---

### Case 2: No Argument — Asks for a description before drafting

**Fixture:**
- No existing bug reports

**Input:** `$gs-bug-report`

**Domain checks:**
- [ ] Skill asks for a description instead of drafting from nothing
- [ ] Preserve the case's unresolved human decisions and declines; perform routine writes already authorized, and ask only for missing decisions or scope.
- [ ] Verdict is COMPLETE only after the file is written

---

### Case 3: Close Mode — Bug not yet verified is refused

**Fixture:**
- `production/qa/bugs/BUG-0007.md` exists with `**Status**: Open`

**Input:** `$gs-bug-report close BUG-0007`

**Domain checks:**
- [ ] The "must be Verified Fixed before it can be closed" message is shown
- [ ] `$gs-bug-report verify BUG-0007` is named as the next step
- [ ] No Closure Record is written and `BUG-0007.md` is not edited
- [ ] Preserve the case's unresolved human decisions and declines; perform routine writes already authorized, and ask only for missing decisions or scope.

---

### Case 4: Multi-System Bug — One report, primary and related systems

**Fixture:**
- No existing reports
- The code root has a save manager and a level-complete UI screen

**Input:** `$gs-bug-report After finishing a level, the save system freezes and the UI doesn't show the completion screen`

**Domain checks:**
- [ ] A single report is created (not one per system)
- [ ] `System` is the save system, the one whose code must change; the UI is under Related systems
- [ ] Likely affected files cover both systems
- [ ] Verdict is COMPLETE

---

### Case 5: Director Gate Check — Analyze Mode, no gate

**Fixture:**
- `src/save/save_manager.gd` exists and contains an unguarded null dereference and an unclosed file handle
- `production/qa/bugs/` holds `BUG-0011.md` (the highest existing number)

**Input:** `$gs-bug-report analyze src/save/save_manager.gd`

**Domain checks:**
- [ ] One report per potential bug, each with a trigger scenario and recommended fix
- [ ] The two reports get different, consecutive IDs (`BUG-0012`, `BUG-0013`) — never the same ID twice
- [ ] Preserve the case's unresolved human decisions and declines; perform routine writes already authorized, and ask only for missing decisions or scope.
- [ ] No director gate is invoked and no gate skip messages appear
- [ ] If the user declines, Verdict is BLOCKED and nothing is written

---

### Case 6: Verify Mode — older three-digit file found by its number, CANNOT VERIFY

**Fixture:**
- `production/qa/bugs/` holds a bug file for bug 42 written in the older form:
  a three-digit number followed by a slug (`-save-corruption.md`), with
  `**Status**: Fixed — Pending Verification`
- The bug's root-cause code path is gone from `src/save/`, but no test in
  `tests/` covers the save system, and the reproduction needs a console suspend
  that no automated check can drive

**Input:** `$gs-bug-report verify BUG-0042`

**Domain checks:**
- [ ] The older three-digit file is found by its number; the skill does not report "No bug BUG-0042"
- [ ] The manual-play question is asked, with the three answers, before a verdict is given
- [ ] Verdict is CANNOT VERIFY, not VERIFIED FIXED — the changed code path is not taken as a pass, and "Not played yet" is not a pass
- [ ] Playing the reproduction steps is named as what would settle it
- [ ] Preserve the case's unresolved human decisions and declines; perform routine writes already authorized, and ask only for missing decisions or scope.
- [ ] Close is not offered while the verdict is CANNOT VERIFY

---

### Case 7: Verify then Close — no test covers the bug, the user's play settles it

**Fixture:**
- `project.yaml` has no `modes` block (so `qa.level: minimal` — tests are waived)
  and no `commands` block
- `production/qa/bugs/BUG-0005.md`: Category `UI`, System `HUD`, "health bar does
  not update after healing", `**Status**: Fixed — Pending Verification`
- No test in the engine's test root covers the HUD

**Input:** `$gs-bug-report verify BUG-0005`, then `$gs-bug-report close BUG-0005`

**Domain checks:**
- [ ] No test command is written from memory; the unset `commands.test` is named
- [ ] The manual-play question is asked with the three answers and the build is recorded as the user gave it
- [ ] Verdict is VERIFIED FIXED, recorded as manual (`[user], manual, build 0.3.1`) — a bug no test covers can reach Verified Fixed
- [ ] Preserve the case's unresolved human decisions and declines; perform routine writes already authorized, and ask only for missing decisions or scope.
- [ ] The Closure Record's Regression test reads "Manual verification"
- [ ] Variant — answering `[Still occurs]` gives STILL PRESENT (the bug is reopened and `$gs-hotfix [BUG-ID]` suggested); answering `[Not played yet]` gives CANNOT VERIFY
