# Evaluation scenarios: gs-sprint-plan

Professional scenarios adapted from Donchitos' upstream testing guidance; see
[source attribution](../../../NOTICE.md). These are evaluation inputs and domain
checks, not executed results. Read `.agents/skills/gs-sprint-plan/SKILL.md` and its current procedure first.
Use [evaluation policy](../README.md) and [category rubric](../quality-rubric.md).

Resolve current config and project engine records. Apply review-mode discipline
coverage without claiming automatic delegation: use the parent when needed, label it,
and record actual participants only. Existing human authorization governs writes;
case approvals represent unresolved decisions and never revoke prior authorization.
Historical fixture versions are scenario inputs, not current API verification.
The linked native procedure governs command arguments, output schemas, receipts,
context and mode applicability. Missing inputs remain NOT ASSESSED.

### Case 1: Happy Path — Ready backlog generates sprint

**Fixture:**
- The injected Existing Sprints listing shows `sprint-001.md` and `sprint-002.md`
- `production/milestones/milestone-02.md` exists
- 5 stories under `production/epics/` across 2 epics have `Status: Ready`
- `project.yaml` sets `modes.review_mode: full` and
  `modes.story_granularity: balanced` (6–10 stories per sprint)
- `production/qa/qa-plan-sprint-003.md` exists
- The producer returns REALISTIC

**Input:** `$gs-sprint-plan new`

**Domain checks:**
- [ ] Allocate sprint-003 after the highest existing sprint-002; write the new plan without replacing sprint-002.
- [ ] Stories come from `production/epics/**/story-*.md` via the status grep, and only `Ready` stories are planned
- [ ] All 5 `Ready` stories are planned — `balanced` allows 6–10, so none is held back
- [ ] Sprint draft is shown before any write prompt or gate invocation
- [ ] PR-SPRINT gate is invoked in full mode after the draft is presented
- [ ] Preserve the case's unresolved human decisions and declines; perform routine writes already authorized, and ask only for missing decisions or scope.
- [ ] Verdict is COMPLETE after both files are written

---

### Case 2: Blocked Path — No stories in the backlog

**Fixture:**
- `production/epics/` contains no story files (`production/epics/**/story-*.md` matches nothing)
- No `--review` flag, no `modes.review_mode` in `project.yaml`, no `production/review-mode.txt`

**Input:** `$gs-sprint-plan new`

**Domain checks:**
- [ ] Verdict is BLOCKED
- [ ] Output contains "No stories found under `production/epics/`" and recommends `$gs-create-stories`
- [ ] No sprint draft is produced from invented work items
- [ ] PR-SPRINT gate is NOT invoked
- [ ] No review-depth question is asked, and no write happens — `project.yaml` gains no `modes.review_mode` and no `production/review-mode.txt` is created

---

### Case 3: Gate returns CONCERNS — Sprint overloaded, revised before write

**Fixture:**
- 8 `Ready` stories estimated at 16 days in total; available capacity is 10 days
- `project.yaml` sets `modes.review_mode: full` and `modes.story_granularity: balanced`
- A QA plan for the sprint exists in `production/qa/`
- The producer returns CONCERNS: the sprint is overloaded

**Input:** `$gs-sprint-plan new`

**Domain checks:**
- [ ] CONCERNS from PR-SPRINT surfaces through `host input tool` ([A] Proceed / [B] Adjust scope / [C] Extend timeline) before any write
- [ ] Preserve the case's unresolved human decisions and declines; perform routine writes already authorized, and ask only for missing decisions or scope.
- [ ] The revised sprint (not the original) is written, and `production/sprint-status.yaml` lists the revised stories
- [ ] Verdict is COMPLETE after revision and write

---

### Case 4: Lean Mode — PR-SPRINT skipped, QA plan check still runs

**Fixture:**
- 4 `Ready` stories under `production/epics/`
- `project.yaml` sets `modes.rigor: standard` and pins no review mode (no
  `modes.review_mode`, no `production/review-mode.txt`, no `--review`), so the
  injected block reads `review_mode: lean (rigor:standard)`
- No QA plan for this sprint exists in `production/qa/`

**Input:** `$gs-sprint-plan new`

**Domain checks:**
- [ ] PR-SPRINT gate is NOT invoked in lean mode
- [ ] Output contains "PR-SPRINT skipped — Lean mode."
- [ ] The QA plan check still runs in lean mode — the missing QA plan is surfaced explicitly with the [A]/[B] choice, not passed silently
- [ ] Preserve the case's unresolved human decisions and declines; perform routine writes already authorized, and ask only for missing decisions or scope.
- [ ] The resolved `lean` is used without a review-depth question, and the write names only the sprint plan and `production/sprint-status.yaml` — `project.yaml` gains no `modes.review_mode` and no `production/review-mode.txt` is created
- [ ] Verdict is COMPLETE after the write

---

### Case 5: Edge Case — Previous sprint still has open stories

**Fixture:**
- The injected Existing Sprints listing shows `sprint-002.md` as the latest sprint
- `production/sprint-status.yaml` still holds sprint 2; 2 of its stories are not
  `done`: one `in-progress`, and one `ready-for-dev` that was never started (its
  story file says `Status: Ready`)
- 5 other stories have `Status: Ready`
- `project.yaml` sets `modes.review_mode: full` and `modes.story_granularity: balanced`
- A QA plan for the sprint exists in `production/qa/`

**Input:** `$gs-sprint-plan new`

**Domain checks:**
- [ ] Skill reads the previous sprint (sprint-002, identified from the injected listing)
- [ ] The 2 unfinished stories appear in the "Carryover from Previous Sprint" table with Reason and New Estimate — not silently dropped
- [ ] The unstarted sprint-002 story appears only under Carryover — not again in Must Have / Should Have / Nice to Have, although its status is `Ready`
- [ ] The carryover is passed to the PR-SPRINT gate
- [ ] The written `production/sprint-status.yaml` lists the 2 carryover stories with their previous priority and current status (`in-progress`, `ready-for-dev`)

---

### Case 6: Gate returns UNREALISTIC — Stories deferred before the write

**Fixture:**
- The injected Existing Sprints listing shows `sprint-002.md` as the latest sprint
- 9 `Ready` stories estimated at 20 days in total; available capacity is 10 days
- `project.yaml` sets `modes.review_mode: full` and `modes.story_granularity: balanced`
- A QA plan for the sprint exists in `production/qa/`
- The producer returns UNREALISTIC and names 4 stories to defer

**Input:** `$gs-sprint-plan new`

**Domain checks:**
- [ ] UNREALISTIC does not end the run, and the original plan is never written — the selection is revised first
- [ ] The 4 named stories are deferred to Should Have or Nice to Have, not dropped from the plan
- [ ] Preserve the case's unresolved human decisions and declines; perform routine writes already authorized, and ask only for missing decisions or scope.
- [ ] The written `production/sprint-status.yaml` carries the deferred stories as `should-have` or `nice-to-have` with `status: backlog`
- [ ] Verdict is COMPLETE after the write

---

### Case 7: Gate returns NOT ASSESSED — No story estimates

**Fixture:**
- 5 `Ready` stories, none with its `Estimate` filled in
- `project.yaml` sets `modes.review_mode: full` and `modes.story_granularity: balanced`
- A QA plan for the sprint exists in `production/qa/`
- The producer returns NOT ASSESSED — the stories carry no estimates
- Asked for estimates, the user has none yet and goes ahead

**Input:** `$gs-sprint-plan new`

**Domain checks:**
- [ ] The written plan’s header records `PR-SPRINT: NOT ASSESSED — story estimates missing`; the run never stores REALISTIC for that review.
- [ ] The missing input (story estimates) is named in the output
- [ ] NOT ASSESSED is not presented as REALISTIC — nothing says the plan's feasibility was reviewed
- [ ] The CONCERNS options ([A] Proceed / [B] Adjust scope / [C] Extend timeline) are not raised for NOT ASSESSED
- [ ] Preserve the case's unresolved human decisions and declines; perform routine writes already authorized, and ask only for missing decisions or scope.
