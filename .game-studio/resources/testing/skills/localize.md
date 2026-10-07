# Evaluation scenarios: gs-localize

Professional scenarios adapted from Donchitos' upstream testing guidance; see
[source attribution](../../../../NOTICE.md). These are evaluation inputs and domain
checks, not executed results. Read `.agents/skills/gs-localize/SKILL.md` and its current procedure first.
Use [evaluation policy](../README.md) and [category rubric](../quality-rubric.md).

Resolve current config and project engine records. Apply review-mode discipline
coverage without claiming automatic delegation: use the parent when needed, label it,
and record actual participants only. Existing human authorization governs writes;
case approvals represent unresolved decisions and never revoke prior authorization.
Historical fixture versions are scenario inputs, not current API verification.
The linked native procedure governs command arguments, output schemas, receipts,
context and mode applicability. Missing inputs remain NOT ASSESSED.

### Case 1: Extract — New Strings Keyed and Appended After Approval

**Fixture:**
- `project.yaml` has `engine.name: Godot`, so the code root is `src/`
- `src/ui/hud.gd` wraps three strings in `tr()` that have no entry in
  `assets/data/strings/strings-en.json`
- No `production/localization/freeze-status.md` exists

**Input:** `$gs-localize extract`

**Domain checks:**
- [ ] Proposed keys follow `[category].[subcategory].[description]`
- [ ] Every new entry includes a `context` field
- [ ] Preserve the case's unresolved human decisions and declines; perform routine writes already authorized, and ask only for missing decisions or scope.
- [ ] Only the three new entries are written — existing entries are not rewritten
- [ ] Verdict is COMPLETE

---

### Case 2: No Subcommand — Usage and FAIL

**Fixture:**
- Any project state

**Input:** `$gs-localize`

**Domain checks:**
- [ ] Usage listing the available modes is printed
- [ ] Verdict is FAIL with the reason "missing required subcommand"
- [ ] No scan, extract or validation work is performed
- [ ] Preserve the case's unresolved human decisions and declines; perform routine writes already authorized, and ask only for missing decisions or scope.

---

### Case 3: Validate — Gaps Reported by Locale, Nothing Written

**Fixture:**
- `assets/data/strings/` holds `strings-en.json`, `strings-fr.json` and
  `strings-de.json`
- `strings-de.json` lacks 4 keys present in the English source
- One French entry omits the `{playerName}` placeholder its English source has

**Input:** `$gs-localize validate`

**Domain checks:**
- [ ] The 4 missing keys are named and attributed to the `de` locale
- [ ] The placeholder mismatch is reported against the `fr` locale and its key
- [ ] Output is grouped by locale and severity
- [ ] Preserve the case's unresolved human decisions and declines; perform routine writes already authorized, and ask only for missing decisions or scope.

---

### Case 4: Status With No String Table — NOT ASSESSED

**Fixture:**
- `assets/data/strings/` does not exist

**Input:** `$gs-localize status`

**Domain checks:**
- [ ] Output is `NOT ASSESSED — no string table found`
- [ ] No coverage matrix with zero counts is produced
- [ ] The source locale is not reported as `100%` coverage
- [ ] No file is written (status is read-only)

---

### Case 5: Director Gate Check — None; Cultural Review Uses localization-lead

**Fixture:**
- `assets/data/strings/strings-en.json` exists with player-facing strings
- Any review mode

**Input:** `$gs-localize cultural-review`

**Domain checks:**
- [ ] `localization-lead` is the only agent consulted
- [ ] No director gate (creative, technical, producer, art) is invoked and no gate skip message appears
- [ ] Each finding carries BLOCKING, ADVISORY or NOTE severity
- [ ] Preserve the case's unresolved human decisions and declines; perform routine writes already authorized, and ask only for missing decisions or scope.

---

### Case 6: Scan With an Unresolved Code Root — NOT ASSESSED, never "no hardcoded strings"

**Fixture:**
- `project.yaml` has no `engine.name`; `.game-studio/resources/docs/technical-preferences.md`
  reads `[TO BE CONFIGURED]`
- Both `src/` and `Assets/` exist and hold UI code with hardcoded strings
  (ambiguous tree)

**Input:** `$gs-localize scan`

**Domain checks:**
- [ ] Output reads `NOT ASSESSED — code root unresolved` for the code search
- [ ] No "no hardcoded strings" or zero-hit result is reported
- [ ] The code root is not assumed to be `src/`
- [ ] Preserve the case's unresolved human decisions and declines; perform routine writes already authorized, and ask only for missing decisions or scope.

---

### Case 7: QA on a Locale Nobody Has Played — NOT ASSESSED

**Fixture:**
- `assets/data/strings/strings-en.json` and `strings-fr.json` exist and validate
  cleanly
- No one has played the French build: there are no in-game observations for the
  functional, overflow, contextual-accuracy or VO checks

**Input:** `$gs-localize qa`

**Domain checks:**
- [ ] The French Status is NOT ASSESSED, with the unrun checks named
- [ ] No PASS or PASS WITH CONDITIONS is issued for an unplayed locale
- [ ] Preserve the case's unresolved human decisions and declines; perform routine writes already authorized, and ask only for missing decisions or scope.
- [ ] The report does not present the locale as cleared for the Polish → Release gate
