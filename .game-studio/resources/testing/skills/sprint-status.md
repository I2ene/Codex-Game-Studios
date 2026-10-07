# Evaluation scenarios: gs-sprint-status

Professional scenarios adapted from Donchitos' upstream testing guidance; see
[source attribution](../../../../NOTICE.md). These are evaluation inputs and domain
checks, not executed results. Read `.agents/skills/gs-sprint-status/SKILL.md` and its current procedure first.
Use [evaluation policy](../README.md) and [category rubric](../quality-rubric.md).

Resolve current config and project engine records. Apply review-mode discipline
coverage without claiming automatic delegation: use the parent when needed, label it,
and record actual participants only. Existing human authorization governs writes;
case approvals represent unresolved decisions and never revoke prior authorization.
Historical fixture versions are scenario inputs, not current API verification.
`<runtime>` abbreviates `<runtime-python> <project-root>/.game-studio/runtime/studio.py`;
append `--root <project-root>` and use the current command's `--help`.
The linked native procedure governs command arguments, output schemas, receipts,
context and mode applicability. Missing inputs remain NOT ASSESSED.

### Case 1: Happy Path — Mixed sprint, At Risk with a blocked Must Have

**Fixture:**
- `production/sprints/sprint-004.md` is the most recently modified sprint file
- `production/sprint-status.yaml` covers sprint 4: it started 13 days ago and
  ends 7 days from today (65% of time consumed)
- The yaml lists 6 stories:
  - 3 with `status: done`
  - 2 with `status: in-progress`, both last updated within the past 2 days
  - 1 with `status: blocked`, `priority: must-have`,
    `blocker: "Waiting on physics ADR acceptance"`

**Input:** `$gs-sprint-status`

**Domain checks:**
- [ ] Output includes "Progress: 3/6 tasks (50%)" and a status table listing all 6 stories
- [ ] The blocked story is named with "Waiting on physics ADR acceptance" in its Blocker column
- [ ] Burndown is At Risk (50% complete vs 65% time consumed — 15 points behind)
- [ ] The SPRINT AT RISK critical flag appears at the top, recommending `$gs-sprint-plan update`
- [ ] Skill does not write any files

---

### Case 2: All Stories Complete — On Track with completion flag

**Fixture:**
- `production/sprints/sprint-004.md` is the most recently modified sprint file
- `production/sprint-status.yaml` covers sprint 4: it started 5 days ago and ends
  5 days from today (50% of time consumed)
- All 5 stories have `status: done` (3 `must-have`, 2 `should-have`)

**Input:** `$gs-sprint-status`

**Domain checks:**
- [ ] Burndown is On Track
- [ ] The completion flag "All Must Haves complete. Team can pull from Should Have backlog." appears at the top
- [ ] Output shows "Progress: 5/5 tasks (100%)"
- [ ] Output makes at most one recommendation (or "Sprint is on track — no action needed.")
- [ ] No files are written

---

### Case 3: No Sprint Files — Guidance to run $gs-sprint-plan

**Fixture:**
- `production/sprints/` directory is absent
- `project.yaml` sets `modes.workflow: standard`

**Input:** `$gs-sprint-status`

**Domain checks:**
- [ ] Skill does not error or crash when no sprint file exists
- [ ] Output states "No sprint files found" and recommends `$gs-sprint-plan new`
- [ ] Skill stops there — no burndown verdict and no status table are emitted
- [ ] The `workflow: minimal` build-order report is not used at `standard`

---

### Case 4: Edge Case — Stale In Progress Story (flagged)

**Fixture:**
- `production/sprints/sprint-004.md` is the most recently modified sprint file
- `production/sprint-status.yaml` covers sprint 4: 10-day sprint, 5 days elapsed
  (50% of time consumed); 4 stories — 2 `done`, 2 `in-progress` (50% complete)
- `production/epics/combat/story-003-dash.md` (in progress) has
  `> **Last Updated**: [6 days before today]`
- `production/epics/combat/story-004-parry.md` (in progress) has
  `> **Last Updated**: [3 days before today]`
- No stories are Blocked

**Input:** `$gs-sprint-status`

**Domain checks:**
- [ ] Dates come from the story files' `Last Updated` field via a single grep, not from `active.md` or a read per story
- [ ] story-003 (6 days) is flagged STALE by name in Attention Needed; story-004 (3 days) is not flagged
- [ ] Burndown is At Risk despite 50% complete against 50% time consumed, and the escalation reason gives the stale count (1) and story-003's own age (6 days) as separate figures
- [ ] Output does not conflate "stale" with "Blocked" — story-003 keeps its IN PROGRESS status with a STALE note

---

### Case 5: Gate Compliance — Read-only; no gate invocation

**Fixture:**
- `production/sprints/sprint-004.md` exists and `production/sprint-status.yaml`
  lists 4 stories (2 `done`, 2 `in-progress`) with sprint dates
- `project.yaml` sets `modes.review_mode: full`

**Input:** `$gs-sprint-status`

**Domain checks:**
- [ ] No director gate is invoked in any review mode
- [ ] Preserve the case's unresolved human decisions and declines; perform routine writes already authorized, and ask only for missing decisions or scope.
- [ ] Skill completes and returns a Burndown verdict without user interaction
- [ ] `review_mode` is not among the keys the skill resolves (it resolves `story_granularity` and `workflow`)

---

### Case 6: Default Minimal Workflow — Build-order progress, no sprint files

**Fixture:**
- `production/sprints/` does not exist
- `project.yaml` sets neither `modes.rigor` nor `modes.workflow`, so the injected
  block reads `workflow: minimal (rigor:minimal)`
- The injected `<runtime> stories` list reads:
  ```
  IN_REVIEW    production/epics/core/story-003-dash.md
  IN_PROGRESS  production/epics/core/story-002-jump.md
  TODO         production/epics/core/story-004-parry.md  (Ready)
  COMPLETE     1 of 4
  ```

**Input:** `$gs-sprint-status`

**Domain checks:**
- [ ] Output does not say "No sprint files found" and does not recommend `$gs-sprint-plan new`
- [ ] Output shows "Build order: 1 of 4 stories complete" — the `In Review` story is not counted as complete
- [ ] Next is story-003, the first line of the list, with `$gs-story-done` and its path — the story files are not re-ranked into file order
- [ ] No burndown verdict is emitted and no file is written

---

### Case 7: Minimal Workflow — Every unfinished story Blocked or Draft

**Fixture:**
- `production/sprints/` does not exist; the injected block reads
  `workflow: minimal (rigor:minimal)`
- The injected `<runtime> stories` list reads:
  ```
  BLOCKED      production/epics/core/story-003-dash.md  (Blocked)
  OTHER        production/epics/core/story-004-parry.md  (Draft)
  COMPLETE     2 of 4
  ```
- story-003's file carries the note `BLOCKED: waiting on the dash animation`

**Input:** `$gs-sprint-status`

**Domain checks:**
- [ ] Output never says the build order is done — no "Build order done" line, no three ways on
- [ ] No story is presented as Next — neither the Blocked story-003 nor the Draft story-004
- [ ] story-003 is named with its blocker, "waiting on the dash animation", from its `BLOCKED:` note
- [ ] story-004 is named with its status as written, `Draft`
- [ ] Output makes exactly one recommendation, and no file is written
