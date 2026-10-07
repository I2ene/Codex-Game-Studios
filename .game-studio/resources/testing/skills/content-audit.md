# Evaluation scenarios: gs-content-audit

Professional scenarios adapted from Donchitos' upstream testing guidance; see
[source attribution](../../../NOTICE.md). These are evaluation inputs and domain
checks, not executed results. Read `.agents/skills/gs-content-audit/SKILL.md` and its current procedure first.
Use [evaluation policy](../README.md) and [category rubric](../quality-rubric.md).

Resolve current config and project engine records. Apply review-mode discipline
coverage without claiming automatic delegation: use the parent when needed, label it,
and record actual participants only. Existing human authorization governs writes;
case approvals represent unresolved decisions and never revoke prior authorization.
Historical fixture versions are scenario inputs, not current API verification.
The linked native procedure governs command arguments, output schemas, receipts,
context and mode applicability. Missing inputs remain NOT ASSESSED.

### Case 1: Happy Path — All specified content present

**Fixture:**
- `modes.workflow` resolves to `full`
- `design/gdd/systems-index.md` lists Enemies (MVP) and Items (MVP)
- `design/registry/entities.yaml` has no entries
- `design/gdd/enemies.md` specifies "4 enemy types: Grunt, Sniper, Tank, Boss"
- `design/gdd/items.md` specifies "3 items"
- `assets/data/enemies/` contains `grunt.json`, `sniper.json`, `tank.json`, `boss.json`
- `assets/data/items/` contains 3 item `.json` files

**Input:** `$gs-content-audit`

**Domain checks:**
- [ ] Gap table uses the columns System, Content Type, Specified, Found, Gap, Status
- [ ] Both rows show Specified = Found, Gap 0 and Status COMPLETE
- [ ] Summary line reports 7 specified, 7 found and 0% gap
- [ ] No HIGH PRIORITY flag is raised
- [ ] Preserve the case's unresolved human decisions and declines; perform routine writes already authorized, and ask only for missing decisions or scope.

---

### Case 2: Gaps Found — MVP enemy content barely started

**Fixture:**
- `modes.workflow` resolves to `full`
- `design/gdd/systems-index.md` tags Enemies as MVP
- `design/gdd/enemies.md` specifies "3 enemy types: Grunt, Sniper, Boss"
- `assets/data/enemies/` contains only `grunt.json`

**Input:** `$gs-content-audit enemies`

**Domain checks:**
- [ ] Specified (3), Found (1) and Gap (2) are all shown
- [ ] Status is EARLY for 1 of 3 (33%), not IN PROGRESS or NOT STARTED
- [ ] Enemies is flagged HIGH PRIORITY because it is EARLY and MVP-tagged
- [ ] Skill flags the gap now; it does not assume the content will be added later
- [ ] Next steps point to `$gs-create-stories` for the HIGH PRIORITY gap

---

### Case 3: No Design Inputs — Nothing to audit against

**Fixture:**
- `modes.workflow` resolves to `full`
- `design/gdd/systems-index.md` does not exist
- `design/gdd/` contains no GDDs
- `design/registry/entities.yaml` has no entries

**Input:** `$gs-content-audit`

**Domain checks:**
- [ ] Verdict is `NOT ASSESSED — NO DATA`, not COMPLETE
- [ ] No gap table or overall gap percentage is produced
- [ ] Output names the missing inputs and the skills that produce them
- [ ] Preserve the case's unresolved human decisions and declines; perform routine writes already authorized, and ask only for missing decisions or scope.

---

### Case 3b: No Counts Anywhere — GDDs exist but none gives a count

**Fixture:**
- `modes.workflow` resolves to `full`
- `design/gdd/systems-index.md` lists Core Loop
- `design/gdd/core-loop.md` has a `## Summary` and describes mechanics only — no content count, no named list
- `design/registry/entities.yaml` has no entries

**Input:** `$gs-content-audit`

**Domain checks:**
- [ ] No overall gap percentage is computed and no row is marked COMPLETE
- [ ] Verdict is `NOT ASSESSED — NO DATA`, never COMPLETE over an empty gap table
- [ ] Output says no GDD gives a count and names `$gs-design-system`

---

### Case 4: Edge Case — A pre-Summary GDD describes content without a count

**Fixture:**
- `modes.workflow` resolves to `full`
- `design/gdd/systems-index.md` lists Enemies and Quests
- `design/gdd/enemies.md` has a `## Summary` and specifies "3 enemy types: Grunt, Sniper, Boss"; `assets/data/enemies/` has all 3
- `design/gdd/quests.md` has no `## Summary` section and says the game has "a handful of side quests" with no number or named list
- User answers yes to the report write

**Input:** `$gs-content-audit`

**Domain checks:**
- [ ] `quests.md` is full-read because it lacks `## Summary`, even though the content-count grep did not match it
- [ ] The Quests content is recorded as "Unspecified", never given an estimated count
- [ ] The Unspecified Content Counts section of the report names `quests.md`
- [ ] The Enemies row is still audited normally (Specified 3, Found 3, COMPLETE)
- [ ] The report carries the approximation caveat

---

### Case 5: Gate Compliance — No gate; optional report requires approval

**Fixture:**
- `project.yaml`: `modes.workflow: full`, `modes.review_mode: full`
- GDDs specify 10 content items; 9 are found in the implementation directories

**Input:** `$gs-content-audit`

**Domain checks:**
- [ ] No director gate is invoked in any review mode
- [ ] Gap table is presented without auto-writing any file
- [ ] The report write is offered for `docs/content-audit-[YYYY-MM-DD].md` but not forced
- [ ] Skill does not modify any asset files

---

### Case 6: Standard Workflow — Only counts in the required sections are audited

**Fixture:**
- `modes.workflow` resolves to `standard`
- `design/gdd/systems-index.md` lists Enemies (MVP)
- `design/gdd/enemies.md` `## Detailed Design` specifies "3 enemy types: Grunt, Sniper, Boss"; its `## Tuning Knobs` section mentions "2 elite variants"
- `assets/data/enemies/` contains `grunt.json`, `sniper.json`, `boss.json`

**Input:** `$gs-content-audit`

**Domain checks:**
- [ ] The Detailed Design count is audited and the Enemies row is COMPLETE
- [ ] The Tuning Knobs count is not in the gap table or the totals
- [ ] The output names the Tuning Knobs count as not audited at `standard` rather than dropping it silently

---

### Case 7: Minimal Workflow — No systems index to audit against

**Fixture:**
- `project.yaml`: `modes.rigor: minimal` (`workflow` resolves to `minimal`)
- `design/game-brief.md` exists; `design/gdd/systems-index.md` does not

**Input:** `$gs-content-audit`

**Domain checks:**
- [ ] Verdict is `NOT ASSESSED — NO DATA`, not COMPLETE
- [ ] Output names `design/gdd/systems-index.md` as missing and `$gs-map-systems` as the skill that produces it
- [ ] No gap percentage is computed and no file is written

---

### Case 8: Code Root Unresolved — The level count is not taken

**Fixture:**
- `modes.workflow` resolves to `full`
- `project.yaml` has no `engine.name`; `.game-studio/resources/docs/technical-preferences.md` reads `[TO BE CONFIGURED]`; both `src/` and `Source/` exist, so the tree does not decide the root
- `design/gdd/systems-index.md` lists Levels (MVP) and Enemies (MVP)
- `design/gdd/levels.md` specifies "6 levels"; `design/gdd/enemies.md` specifies "3 enemy types: Grunt, Sniper, Boss"
- `assets/data/enemies/` contains 3 enemy files; no scene files exist under `assets/`

**Input:** `$gs-content-audit`

**Domain checks:**
- [ ] The Levels row reads `NOT ASSESSED — code root unresolved`, never Found 0 or NOT STARTED
- [ ] The summary totals leave Levels out and say so
- [ ] Verdict is NOT ASSESSED, not COMPLETE


## Applicable domain checks

- [ ] On Unity, content discovery also scans `Assets/` without requiring a `data/` segment (including `Assets/**/Items/**` and `*Item*.asset`); present Unity items, abilities, quests and dialogue are not reported NOT STARTED by an `assets/data/`-only scan.
