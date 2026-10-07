# Evaluation scenarios: gs-playtest-report

Professional scenarios adapted from Donchitos' upstream testing guidance; see
[source attribution](../../../NOTICE.md). These are evaluation inputs and domain
checks, not executed results. Read `.agents/skills/gs-playtest-report/SKILL.md` and its current procedure first.
Use [evaluation policy](../README.md) and [category rubric](../quality-rubric.md).

Resolve current config and project engine records. Apply review-mode discipline
coverage without claiming automatic delegation: use the parent when needed, label it,
and record actual participants only. Existing human authorization governs writes;
case approvals represent unresolved decisions and never revoke prior authorization.
Historical fixture versions are scenario inputs, not current API verification.
The linked native procedure governs command arguments, output schemas, receipts,
context and mode applicability. Missing inputs remain NOT ASSESSED.

### Case 1: Happy Path — Analyze Notes, Findings Routed by Bucket

**Fixture:**
- `production/qa/notes/session-01.md` holds one tester's notes: "framerate
  drops every time the forest area loads", "I could not work out how to open
  the first door", and "the second boss hits far too hard"
- `design/gdd/` holds the tutorial and combat GDDs; the tutorial GDD says the
  first door teaches the interact key
- Review mode: `solo`

**Input:** `$gs-playtest-report analyze production/qa/notes/session-01.md`

**Domain checks:**
- [ ] The framerate drop appears in the Bugs Encountered table, not under Gameplay Flow
- [ ] Findings are presented in the four buckets (design, balance, bug, polish)
- [ ] Each bucket is routed to its named skill (`$gs-propagate-design-change`, `$gs-balance-check`, `$gs-bug-report`)
- [ ] Preserve the case's unresolved human decisions and declines; perform routine writes already authorized, and ask only for missing decisions or scope.
- [ ] Verdict is COMPLETE

---

### Case 2: New Mode — Blank Template Output

**Fixture:**
- Any project state

**Input:** `$gs-playtest-report new`

**Domain checks:**
- [ ] Output contains the headings Session Info, Test Focus, First Impressions, Gameplay Flow, Bugs Encountered, Feature-Specific Feedback, Quantitative Data, Overall Assessment and Top 3 Priorities
- [ ] Placeholders (e.g. `[Date]`, `[Name/ID]`) are left unfilled
- [ ] No notes file is read and no findings are fabricated
- [ ] Preserve the case's unresolved human decisions and declines; perform routine writes already authorized, and ask only for missing decisions or scope.
- [ ] Verdict is COMPLETE

---

### Case 3: Observation Conflicts With Design Intent

**Fixture:**
- `design/gdd/crafting.md` states crafting is a core loop players engage with
  every session
- `production/qa/notes/session-02.md` records that the tester never opened the
  crafting menu in 40 minutes
- Review mode: `solo`

**Input:** `$gs-playtest-report analyze production/qa/notes/session-02.md`

**Domain checks:**
- [ ] The crafting observation is explicitly flagged as conflicting with the GDD's intent
- [ ] It is categorised as a design change, not a polish item
- [ ] `$gs-propagate-design-change` is suggested on the affected GDD
- [ ] Verdict is COMPLETE after the write

---

### Case 4: Edge Case — Full Review Mode With No Pillars Available

**Fixture:**
- Review mode: `full`
- Neither `design/gdd/game-concept.md` nor `design/game-brief.md` exists
- `production/qa/notes/session-03.md` holds playtest notes

**Input:** `$gs-playtest-report analyze production/qa/notes/session-03.md`

**Domain checks:**
- [ ] CD-PLAYTEST is consulted (review mode is `full`)
- [ ] The gate prompt says no pillars are available instead of passing none silently
- [ ] Pillars are not invented by the skill
- [ ] Preserve the case's unresolved human decisions and declines; perform routine writes already authorized, and ask only for missing decisions or scope.

---

### Case 5: Director Gate — CD-PLAYTEST by Review Mode

**Fixture:**
- `design/gdd/game-concept.md` exists with pillars
- `production/qa/notes/session-04.md` holds playtest notes
- Run three times: `--review full`, `--review lean`, `--review solo`
- In the full run, `creative-director` returns CONCERNS

**Input:** `$gs-playtest-report analyze production/qa/notes/session-04.md --review [mode]`

**Domain checks:**
- [ ] In full mode, CD-PLAYTEST consults `creative-director` before the report is saved
- [ ] On CONCERNS, the report gains a `## Creative Director Assessment` section with the verdict and feedback
- [ ] In lean mode, the skip note names CD-PLAYTEST and Lean mode
- [ ] In solo mode, the skip note names CD-PLAYTEST and Solo mode
- [ ] No other director gate is consulted in any mode
