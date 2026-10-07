# Evaluation scenarios: gs-team-narrative

Professional scenarios adapted from Donchitos' upstream testing guidance; see
[source attribution](../../../NOTICE.md). These are evaluation inputs and domain
checks, not executed results. Read `.agents/skills/gs-team-narrative/SKILL.md` and its current procedure first.
Use [evaluation policy](../README.md) and [category rubric](../quality-rubric.md).

Resolve current config and project engine records. Apply review-mode discipline
coverage without claiming automatic delegation: use the parent when needed, label it,
and record actual participants only. Existing human authorization governs writes;
case approvals represent unresolved decisions and never revoke prior authorization.
Historical fixture versions are scenario inputs, not current API verification.
The linked native procedure governs command arguments, output schemas, receipts,
context and mode applicability. Missing inputs remain NOT ASSESSED.

## Execution path variants

Run the relevant success and blocking cases through both paths; preserve each
case's inputs, professional scope, artifact destinations and expected verdict.

**Parent execution path:**
- Fixture: delegation is unavailable or unauthorized; routine task work is authorized.
- [ ] The parent performs each required discipline and labels the work as parent work; it never invents independent participants or sign-off.
- [ ] All required results and blockers are summarized, and dependent phases wait for their prerequisites even when independent work is performed sequentially.

**Authorized delegation path:**
- Fixture: explicit user authorization, an exposed host tool and sufficient capacity for the independent tasks are confirmed.
- [ ] Independent tasks may run concurrently with distinct ownership; do not serialize genuinely independent delegated work when the fixture provides sufficient capacity.
- [ ] Dependent phases wait for all required results; blocks preserve completed work and surface before dependent action.
- [ ] Actual delegated participants are recorded with scope, result, artifacts and blockers; parent contributions remain labeled as parent work.
- [ ] Repeat with capacity below the full roster: queue independent work or apply the parent fallback without inventing concurrency or dropping disciplines.

### Case 1: Happy Path — All five phases complete, narrative doc delivered

**Fixture:**
- Resolved config block: `team.size: studio`, `automation: collaborative`
- A game concept and GDD exist for the target feature (e.g., `design/gdd/faction-intro.md`)
- Character voice profiles exist (e.g., `design/narrative/characters/`)
- Existing lore entries exist for cross-reference (e.g., `design/narrative/lore/`)
- No lore contradictions exist between existing entries and the new content

**Input:** `$gs-team-narrative faction introduction cutscene for the Ironveil faction`

**Domain checks:**
- [ ] Active-set line naming `team.size: studio` appears before the first agent is consulted
- [ ] narrative-director is consulted in Phase 1 before any other agents
- [ ] `host input tool` appears after Phase 1 output and before Phase 2 launch
- [ ] Phase 2 covers world-building, writing and art direction independently before level integration
- [ ] level-designer is not launched until Phase 2 `host input tool` is approved
- [ ] narrative-director is re-consulted in Phase 4 using gate ND-CONSISTENCY — in every review mode, since it is this pipeline's own review and `review_mode` never skips it — and its APPROVE / CONCERNS / REJECT verdict decides whether Phase 5 starts
- [ ] Phase 5 covers writing, localization and canon independently; all results reach the final summary
- [ ] Each agent prompt names its draft path from the skill's path table
- [ ] Preserve the case's unresolved human decisions and declines; perform routine writes already authorized, and ask only for missing decisions or scope.
- [ ] Summary report includes: narrative brief status, lore entries created/updated, dialogue lines written, level narrative integration points, consistency review results
- [ ] Writes follow existing user authorization and named artifact responsibilities, including labeled parent execution
- [ ] Verdict is COMPLETE after delivery

---

### Case 2: Lore Contradiction Found — world-builder finds conflict before writer proceeds

**Fixture:**
- Resolved config block: `team.size: studio`, `automation: collaborative`
- Existing lore entry at `design/narrative/lore/ironveil-history.md` states the Ironveil faction was founded 200 years ago
- The new narrative brief (from Phase 1) states the Ironveil were founded 50 years ago
- The writer has been consulted alongside the world-builder in Phase 2

**Input:** `$gs-team-narrative ironveil faction introduction cutscene`

**Domain checks:**
- [ ] Contradiction is surfaced before Phase 3 begins
- [ ] Orchestrator does not silently resolve the contradiction by picking one version
- [ ] `host input tool` presents at least 3 options including "stop and resolve first"
- [ ] Writer's draft output is preserved in the partial report, not discarded
- [ ] Phase 3 (level-designer) is not launched until the user resolves the contradiction or explicitly chooses to skip world-builder
- [ ] Verdict is BLOCKED (not COMPLETE) if the user stops to resolve the contradiction

---

### Case 3: No Argument — Usage guidance shown

**Fixture:**
- Any project state

**Input:** `$gs-team-narrative` (no argument)

**Domain checks:**
- [ ] Skill does NOT consults any agents when no argument is provided
- [ ] Usage message shows the full argument-hint — `$gs-team-narrative [narrative content description] [--review full|lean|solo]` — and an argument example
- [ ] Skill does NOT attempt to guess or infer a narrative topic from project files
- [ ] No `host input tool` is used — output is direct guidance

---

### Case 4: Localization Compliance — localization-lead blocks on a non-translatable string

**Fixture:**
- Resolved config block: `team.size: studio`, `automation: collaborative`
- Phases 1–4 complete successfully
- Phase 5 begins; writer and world-builder complete without issues
- localization-lead finds a dialogue line that uses a hardcoded formatted date string (e.g., `"On March 12th, Year 3"`) that cannot survive locale-specific translation without a locale-aware formatter, and returns it as a BLOCKED item in its return contract

**Input:** `$gs-team-narrative ironveil faction introduction cutscene` (Phase 5 scenario)

**Domain checks:**
- [ ] Phase 5 includes localization expertise alongside writing and world-building, without assuming delegated participants
- [ ] Hardcoded date format is identified as a localization blocker (not silently passed)
- [ ] The specific string key and reason are included in the surfaced BLOCKED message
- [ ] `host input tool` offers skip-and-note-gap, retry, and stop options
- [ ] If the user proceeds without fixing, the final report names the unfixed string key; if the user stops, the verdict is BLOCKED
- [ ] Preserve the case's unresolved human decisions and declines; perform routine writes already authorized, and ask only for missing decisions or scope.

---

### Case 5: Writer Blocked — Missing character voice profiles

**Fixture:**
- Resolved config block: `team.size: studio`, `automation: collaborative`
- Phase 1 narrative-director produces a narrative brief referencing two characters: Commander Varek and Advisor Selene
- No character voice profiles exist in `design/narrative/characters/` for either character
- Phase 2 begins; world-builder and art-director proceed normally

**Input:** `$gs-team-narrative ironveil surrender negotiation scene`

**Domain checks:**
- [ ] Writer block is surfaced before Phase 3 begins
- [ ] world-builder's completed lore output is preserved in the partial report
- [ ] Missing prerequisite (voice profiles) is named specifically (character names and expected file path)
- [ ] `host input tool` offers at least one option to resolve the missing prerequisite
- [ ] Orchestrator does not fabricate voice profiles or invent character voices
- [ ] Phase 3 is not launched while writer is BLOCKED without explicit user authorization


## Applicable domain checks

- [ ] Before professional work starts, resolve and announce team-size scope, parent coverage and any actual participants. At `team.size: individual`: writer; other perspectives are routed through it, and ND-CONSISTENCY is not presented as an independent director gate. Name inactive perspectives and unassessed work accurately.
- [ ] At individual size record the writer consistency self-check separately from ND-CONSISTENCY; no independent director approval is implied.
- [ ] An ND-CONSISTENCY NOT ASSESSED result names the missing input and is re-run only after supplying it, or carried into both the report and `COMPLETE — consistency NOT ASSESSED ([input])`.
- [ ] Missing named artifacts fail their phase; completed work survives in the partial report.
