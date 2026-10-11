# Evaluation scenarios: gs-retrospective

Professional scenarios adapted from Donchitos' upstream testing guidance; see
[source attribution](../../../NOTICE.md). These are evaluation inputs and domain
checks, not executed results. Read `.agents/skills/gs-retrospective/SKILL.md` and its current procedure first.
Use [evaluation policy](../README.md) and [category rubric](../quality-rubric.md).

Resolve current config and project engine records. Apply review-mode discipline
coverage without claiming automatic delegation: use the parent when needed, label it,
and record actual participants only. Existing human authorization governs writes;
case approvals represent unresolved decisions and never revoke prior authorization.
Historical fixture versions are scenario inputs, not current API verification.
The linked native procedure governs command arguments, output schemas, receipts,
context and mode applicability. Missing inputs remain NOT ASSESSED.

### Case 1: Happy Path — Sprint with mixed outcomes

**Fixture:**
- `production/sprints/sprint-005.md` exists with 6 stories; no earlier sprint
  plan exists in `production/sprints/`
- `production/sprint-status.yaml` covers sprint 5: 4 stories `done`, 1 `blocked`
  (`blocker: "Waiting on the save-format decision"`), 1 still `backlog`
- `project.yaml` sets `modes.workflow: standard`
- `production/retrospectives/` holds no retrospective at all

**Input:** `$gs-retrospective sprint-005`

**Domain checks:**
- [ ] Retrospective contains What Went Well, What Went Poorly and Action Items for Next Iteration sections
- [ ] Completion metrics come from `production/sprint-status.yaml` (4 of 6 done), not from markdown scanning
- [ ] The blocked story appears under Blockers Encountered with "Waiting on the save-format decision" as its Blocker, and an action item addresses it
- [ ] Velocity Trend reads `NOT ASSESSED — NO DATA` — no Increasing / Stable / Decreasing trend and no earlier-sprint rows are invented from a single sprint
- [ ] Previous Action Items Follow-Up reads `NOT ASSESSED — NO DATA` (no earlier retrospective), not an empty table
- [ ] Preserve the case's unresolved human decisions and declines; perform routine writes already authorized, and ask only for missing decisions or scope.
- [ ] Verdict is COMPLETE after the write, followed by the offer to start `$gs-sprint-plan new`

---

### Case 2: No Sprint Data — Manual input fallback

**Fixture:**
- User calls `$gs-retrospective sprint-009`
- `production/sprints/sprint-009.md` does NOT exist and
  `production/sprint-status.yaml` has no sprint 9
- `project.yaml` sets `modes.workflow: standard`
- No retrospective for sprint-009 exists

**Input:** `$gs-retrospective sprint-009`

**Domain checks:**
- [ ] Skill does not crash or produce an empty document when the sprint file is absent, and states that no sprint data was found for sprint-009
- [ ] `host input tool` offers [A] Provide data manually and [B] Stop — not [C] Look back over the closed stories, which is offered only at `workflow: minimal`
- [ ] Manual input is formatted into the retrospective structure (What Went Well / What Went Poorly / Action Items for Next Iteration)
- [ ] Preserve the case's unresolved human decisions and declines; perform routine writes already authorized, and ask only for missing decisions or scope.

---

### Case 3: Prior Retrospective Exists — Update existing or start fresh

**Fixture:**
- `production/retrospectives/retro-sprint-005-[earlier date].md` already exists
  with content
- `production/sprints/sprint-005.md` exists
- User re-runs `$gs-retrospective sprint-005` and, when asked, selects [B] Start fresh

**Input:** `$gs-retrospective sprint-005`

**Domain checks:**
- [ ] Skill checks for an existing retrospective before loading sprint data
- [ ] User is offered Update existing or Start fresh — the old file is never silently overwritten
- [ ] Preserve the case's unresolved human decisions and declines; perform routine writes already authorized, and ask only for missing decisions or scope.
- [ ] On approval, the old file is kept under an `-archived-[date]` name, not deleted or overwritten
- [ ] Verdict is COMPLETE after the write

---

### Case 4: Edge Case — Unresolved action items from previous retrospective

**Fixture:**
- `production/retrospectives/retro-sprint-004-[date].md` exists with 2 action
  items marked `[ ]` (not done)
- `production/sprints/sprint-005.md` exists; no retrospective for sprint-005 exists
- User runs `$gs-retrospective sprint-005`

**Input:** `$gs-retrospective sprint-005`

**Domain checks:**
- [ ] Skill reads the prior retrospective in `production/retrospectives/` to check its action items
- [ ] Both unresolved items appear in the "Previous Action Items Follow-Up" table
- [ ] Their Status is Not Started or In Progress — not Done
- [ ] The follow-up table is distinct from the newly generated "Action Items for Next Iteration"

---

### Case 5: Gate Compliance — No gate invoked in any mode

**Fixture:**
- `production/sprints/sprint-005.md` exists with complete stories
- `project.yaml` sets `modes.review_mode: full`

**Input:** `$gs-retrospective sprint-005`

**Domain checks:**
- [ ] No director gate is invoked regardless of review mode
- [ ] Output does not contain any gate invocation or gate result notation
- [ ] Preserve the case's unresolved human decisions and declines; perform routine writes already authorized, and ask only for missing decisions or scope.
- [ ] `review_mode` is not among the keys the skill resolves (it resolves `automation`, `workflow`, `qa.level`)

---

### Case 6: Minimal Workflow — Look back over the closed stories

**Fixture:**
- `project.yaml` sets neither `modes.rigor` nor `modes.workflow`, so the injected
  block reads `workflow: minimal (rigor:minimal)`
- `production/sprints/`, `production/milestones/` and
  `production/retrospectives/` do not exist
- 3 stories under `production/epics/core/` have `Status: Complete`; 1 has
  `Status: In Progress`

**Input:** `$gs-retrospective sprint-001`

**Domain checks:**
- [ ] The no-data prompt offers [C] Look back over the closed stories alongside [A] and [B]
- [ ] Choosing [C] continues to Phase 3 from the `Complete` stories — the run does not stop BLOCKED
- [ ] The `In Progress` story is not reported as completed work
- [ ] The sections that need sprint data read `NOT ASSESSED — NO DATA` rather than invented figures
- [ ] Preserve the case's unresolved human decisions and declines; perform routine writes already authorized, and ask only for missing decisions or scope.
