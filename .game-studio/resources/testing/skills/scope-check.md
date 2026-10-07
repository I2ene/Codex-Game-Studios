# Evaluation scenarios: gs-scope-check

Professional scenarios adapted from Donchitos' upstream testing guidance; see
[source attribution](../../../../NOTICE.md). These are evaluation inputs and domain
checks, not executed results. Read `.agents/skills/gs-scope-check/SKILL.md` and its current procedure first.
Use [evaluation policy](../README.md) and [category rubric](../quality-rubric.md).

Resolve current config and project engine records. Apply review-mode discipline
coverage without claiming automatic delegation: use the parent when needed, label it,
and record actual participants only. Existing human authorization governs writes;
case approvals represent unresolved decisions and never revoke prior authorization.
Historical fixture versions are scenario inputs, not current API verification.
The linked native procedure governs command arguments, output schemas, receipts,
context and mode applicability. Missing inputs remain NOT ASSESSED.

### Case 1: Happy Path — Multi-word feature on track

**Fixture:**
- `design/gdd/inventory-crafting-system.md` enumerates 20 scope items
- `src/gameplay/inventory/` and `src/gameplay/crafting/` implement all 20, plus one addition (item sorting) found in a recent commit
- No items were dropped

**Input:** `$gs-scope-check inventory crafting system`

**Domain checks:**
- [ ] The baseline is located from the full multi-word argument, not its first word
- [ ] The addition is named in the Scope Additions table with source, when, justified and effort columns
- [ ] Bloat Score shows original, current, added and removed counts and the net percentage
- [ ] Verdict is PASS for a net change ≤10%
- [ ] No files are written

---

### Case 2: Significant Creep — Sprint gained unplanned items

**Fixture:**
- `production/sprints/sprint-003.md` lists 8 planned stories
- Commits since the sprint start add an online leaderboard, an achievement system and a photo mode, none of which appear in the sprint plan
- No planned stories were dropped

**Input:** `$gs-scope-check sprint-3`

**Domain checks:**
- [ ] Each unplanned addition is named explicitly in the Scope Additions table
- [ ] Verdict is FAIL for a net change between 25% and 50%
- [ ] Output recommends escalating to the producer and references `$gs-sprint-plan update` or `$gs-estimate`
- [ ] Skill does not edit the sprint plan or remove stories — findings are advisory

---

### Case 3: Baseline Missing — Report the missing file and stop

**Fixture:**
- No `design/gdd/crafting.md` and no file in `design/` matches "crafting"
- `src/gameplay/crafting/` contains implemented code

**Input:** `$gs-scope-check crafting`

**Domain checks:**
- [ ] Output names the baseline file it looked for and did not find
- [ ] Skill stops at Phase 1 — no Phase 3 comparison report is rendered
- [ ] No percentage and no PASS verdict are produced without a baseline
- [ ] No files are written

---

### Case 4: Empty Baseline — NOT ASSESSED, not 0%

**Fixture:**
- `design/gdd/dialogue.md` exists but contains only section headings and `[TO BE CONFIGURED]` placeholders — no scope items
- `src/narrative/dialogue/` contains implemented code

**Input:** `$gs-scope-check dialogue`

**Domain checks:**
- [ ] Verdict is NOT ASSESSED, never PASS, when the baseline has no items
- [ ] No computed percentage appears anywhere in the report
- [ ] Output says which side was unusable and what would fix it (populate the baseline document)
- [ ] Skill does not offer a re-run against the same inputs

---

### Case 4b: Unreadable Current State — NOT ASSESSED, not −100%

**Fixture:**
- `production/sprints/sprint-004.md` lists 6 planned stories
- No source files relate to those stories, `git log` shows no commits since the sprint start, and nothing is marked in progress

**Input:** `$gs-scope-check sprint-4`

**Domain checks:**
- [ ] Verdict is NOT ASSESSED, never PASS
- [ ] No −100% (or any percentage) appears in the report
- [ ] Output names the current state as the side that could not be read
- [ ] Skill does not offer a re-run against the same inputs

---

### Case 5: Minor Creep in Full Review Mode — CONCERNS, no gates

**Fixture:**
- `project.yaml` has `modes.review_mode: full`
- `production/milestones/alpha.md` enumerates 10 scope items
- Current state has all 10 plus two additions (a settings menu rework and an extra enemy type)

**Input:** `$gs-scope-check alpha`

**Domain checks:**
- [ ] Verdict is CONCERNS for a net change between 10% and 25%
- [ ] No director gate is invoked in any review mode
- [ ] Output offers to identify the additions with the best cut ratio and references `$gs-sprint-plan update`
- [ ] No files are written
