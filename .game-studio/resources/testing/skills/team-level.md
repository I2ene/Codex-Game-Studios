# Evaluation scenarios: gs-team-level

Professional scenarios adapted from Donchitos' upstream testing guidance; see
[source attribution](../../../../NOTICE.md). These are evaluation inputs and domain
checks, not executed results. Read `.agents/skills/gs-team-level/SKILL.md` and its current procedure first.
Use [evaluation policy](../README.md) and [category rubric](../quality-rubric.md).

Resolve current config and project engine records. Apply review-mode discipline
coverage without claiming automatic delegation: use the parent when needed, label it,
and record actual participants only. Existing human authorization governs writes;
case approvals represent unresolved decisions and never revoke prior authorization.
Historical fixture versions are scenario inputs, not current API verification.
The linked native procedure governs command arguments, output schemas, receipts,
context and mode applicability. Missing inputs remain NOT ASSESSED.

### Case 1: Happy Path — All team members produce outputs, document compiled and saved

**Fixture:**
- Resolved config block: `team.size: studio`, `automation: collaborative`
- `design/gdd/game-concept.md` exists and is populated
- `design/gdd/game-pillars.md` exists
- `design/levels/` directory exists (may contain other level docs)
- `design/narrative/` directory exists with relevant narrative docs
- World-building docs for the forest region exist

**Input:** `$gs-team-level forest dungeon`

**Domain checks:**
- [ ] Active-set line naming `team.size: studio` appears before the first agent is consulted
- [ ] All five sources read during context gathering before any discipline review begins
- [ ] narrative-director, world-builder and art-director discipline reviews cover independent concerns, with authorized parallel delegation when available in Step 1, and all three complete before Step 2
- [ ] The level-designer brief carries the art-director's Step 1 visual targets as constraints
- [ ] `host input tool` called at each step gate (minimum: after Step 1, Step 2, Step 3, Step 4)
- [ ] Step 4 agents (art-director, accessibility-specialist) launched simultaneously
- [ ] Preserve the case's unresolved human decisions and declines; perform routine writes already authorized, and ask only for missing decisions or scope.
- [ ] Level doc saved to `design/levels/forest-dungeon.md` (slugified from argument)
- [ ] Verdict COMPLETE in final summary report
- [ ] Next steps include `$gs-design-review`, `$gs-dev-story`, `$gs-qa-plan`
- [ ] Summary report includes: area overview, encounter count, estimated asset list, narrative beats

---

### Case 2: Blocked Agent (world-builder) — Partial report produced with gap noted

**Fixture:**
- Resolved config block: `team.size: studio`, `automation: collaborative`
- `design/gdd/game-concept.md` exists
- World-building docs for the forest region do NOT exist
- world-builder agent returns BLOCKED: "No world-building docs found for the forest region — cannot provide lore context"

**Input:** `$gs-team-level forest dungeon`

**Domain checks:**
- [ ] BLOCKED surface message appears immediately when world-builder fails — before Step 2 begins without user input
- [ ] `host input tool` offers at minimum three options (skip / retry / stop)
- [ ] Partial report produced — narrative-director's and art-director's completed work is not discarded
- [ ] The missing world-building context is named as a gap in the final report
- [ ] Overall verdict is BLOCKED (not COMPLETE) when world-builder remains unresolved
- [ ] Use the linked native procedure and explicit runtime command; retired host execution is not required.

---

### Case 3: No Argument — Usage guidance shown

**Fixture:**
- Any project state

**Input:** `$gs-team-level` (no argument)

**Domain checks:**
- [ ] Skill does NOT consults any specialist disciplines when no argument is given
- [ ] Usage message shows the full argument-hint: `$gs-team-level [level name or area to design] [--review full|lean|solo]`
- [ ] At least one example of a valid invocation is shown
- [ ] No GDD or level files read before failing
- [ ] Verdict is NOT shown (pipeline never starts)

---

### Case 4: Accessibility Review Gate — Blocking concern surfaces before sign-off

**Fixture:**
- Resolved config block: `team.size: studio`, `automation: collaborative`
- Steps 1–3 complete successfully
- `design/accessibility-requirements.md` committed tier: Standard
- accessibility-specialist (Step 4, parallel) flags a BLOCKING concern: the critical path through the forest dungeon requires players to distinguish between two environmental hazards (toxic pools vs. shallow water) using color alone — no shape, icon, or audio cue differentiates them

**Input:** `$gs-team-level forest dungeon`

**Domain checks:**
- [ ] BLOCKING accessibility concern is not treated as advisory — it is surfaced as a blocker
- [ ] `host input tool` presents the specific concern text (not just "accessibility issue found")
- [ ] Step 5 (qa-tester) does NOT begin without user acknowledging the BLOCKING concern
- [ ] Revision path offered: level-designer + art-director can be sent back before proceeding
- [ ] Final report includes the accessibility concern and its resolution status
- [ ] art-director's completed output is NOT discarded when accessibility-specialist blocks

---

### Case 5: Circular Level Reference — Adjacent area dependency flagged

**Fixture:**
- Resolved config block: `automation: collaborative` (any `team.size` — level-designer is active at every size)
- Steps 1–3 in progress
- level-designer (Step 2) produces a layout that specifies entry/exit points connecting to "the crystal caves" (an adjacent area)
- `design/levels/crystal-caves.md` does NOT exist — the crystal caves area has not been designed yet

**Input:** `$gs-team-level forest dungeon`

**Domain checks:**
- [ ] Skill detects the missing adjacent area by checking `design/levels/` — does not assume it will be created later
- [ ] Skill does NOT fabricate crystal caves content (lore, layout, connections) to resolve the reference
- [ ] `host input tool` offers a "design crystal caves first" option referencing `$gs-team-level`
- [ ] If user proceeds with placeholder, level doc explicitly marks the west exit as UNRESOLVED
- [ ] Summary report includes an open cross-level dependencies section listing unresolved references
- [ ] Circular or forward references do not cause the skill to loop or crash
