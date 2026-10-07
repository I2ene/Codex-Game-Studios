# Evaluation scenarios: gs-help

Professional scenarios adapted from Donchitos' upstream testing guidance; see
[source attribution](../../../NOTICE.md). These are evaluation inputs and domain
checks, not executed results. Read `.agents/skills/gs-help/SKILL.md` and its current procedure first.
Use [evaluation policy](../README.md) and [category rubric](../quality-rubric.md).

Resolve current config and project engine records. Apply review-mode discipline
coverage without claiming automatic delegation: use the parent when needed, label it,
and record actual participants only. Existing human authorization governs writes;
case approvals represent unresolved decisions and never revoke prior authorization.
Historical fixture versions are scenario inputs, not current API verification.
The linked native procedure governs command arguments, output schemas, receipts,
context and mode applicability. Missing inputs remain NOT ASSESSED.

### Case 1: Happy Path — Production stage with active sprint

**Fixture:**
- `project.yaml` sets `project.stage: Production` and `modes.rigor: standard`
  (so `workflow` resolves to `standard`)
- `production/sprints/sprint-004.md` exists
- `production/sprint-status.yaml` lists one story `status: in-progress`, two
  `status: ready-for-dev`, three `status: done`, and one `status: blocked` with a
  `blocker` field
- `production/session-state/active.md` has a STATUS block naming the in-progress story

**Input:** `$gs-help`

**Domain checks:**
- [ ] Heading reads `## Where You Are: Production`
- [ ] `production/sprint-status.yaml` is read; the in-progress story is surfaced as currently active
- [ ] The blocked story appears with its `blocker` field
- [ ] Exactly one `→ Next up (REQUIRED)` step is shown (not a list of all skills)
- [ ] The in-progress story from `active.md` is surfaced at the top ("It looks like you were working on …")
- [ ] Verdict is COMPLETE
- [ ] No files are written

---

### Case 2: Concept Stage — engine configured, no concept document

**Fixture:**
- `project.yaml` sets `project.stage: Concept`, `modes.rigor: full`, and
  `engine.name: "Godot"` (`full`, because at `standard` the art bible is
  required only when visual-asset stories exist — `.game-studio/resources/docs/workflow-modes.md`
  — and a Concept-stage project has no stories to decide it by)
- No `design/gdd/game-concept.md`, no `design/art/art-bible.md`, no
  `design/gdd/systems-index.md`, no sprint files

**Input:** `$gs-help`

**Domain checks:**
- [ ] Heading reads `## Where You Are: Concept`
- [ ] Engine Setup is shown under `✓ Done` (not reported missing)
- [ ] `→ Next up` is Game Concept Document via `$gs-brainstorm`
- [ ] `$gs-art-bible` and `$gs-map-systems` appear under "Coming up after that", in that order
- [ ] No Production-stage skill (e.g. `$gs-dev-story`, `$gs-sprint-plan`) is suggested
- [ ] Verdict is COMPLETE

---

### Case 3: No stage recorded — phase inferred from artifacts

**Fixture:**
- `project.yaml` sets `modes.rigor: standard` and has no `project.stage`
- No `production/stage.txt`
- `design/gdd/game-concept.md` and `design/gdd/systems-index.md` exist
- No `docs/architecture/adr-*.md`, no `production/epics/**/story-*.md`, code root empty

**Input:** `$gs-help`

**Domain checks:**
- [ ] Skill does not stop or error when no stage is recorded
- [ ] Inferred phase is Systems Design (heading `## Where You Are: Systems Design`), not Concept
- [ ] `→ Next up` is System GDDs via `$gs-design-system`
- [ ] The skill asks the user whether any system GDD is already done (MANUAL step), rather than reporting System GDDs as done or as not started
- [ ] The "Need more detail?" escalation block (`$gs-project-stage-detect`, `$gs-gate-check`, `$gs-start`) is NOT shown
- [ ] Verdict is COMPLETE

---

### Case 4: Argument — user names the step they finished and says they are unsure

**Fixture:**
- `project.yaml` sets `project.stage: Systems Design` and `modes.rigor: standard`
- `design/gdd/systems-index.md` lists two MVP systems, both `Status: Approved`,
  and both system GDDs exist
- No `design/gdd/gdd-cross-review-*.md`
- The catalog's `design-review` step has no artifact check (`NO_CHECK`)

**Input:** `$gs-help just finished design-review, not sure what's next`

**Domain checks:**
- [ ] Per-System Design Review is treated as done because the user named it
- [ ] `→ Next up` is Cross-GDD Review via `$gs-review-all-gdds`
- [ ] Escalation block lists `$gs-project-stage-detect`, `$gs-gate-check` and `$gs-start`
- [ ] No `$gs-settings` rigor-change line appears
- [ ] Verdict is COMPLETE

---

### Case 5: Director Gate Check — minimal path, no gate and no gate-check route

**Fixture:**
- `project.yaml` has `engine.name: "Godot"` and no `modes` block (`modes.rigor`
  defaults to `minimal`, so `workflow` resolves to `minimal`)
- `design/game-brief.md` exists
- `production/epics/core/story-001.md` is `Status: Complete`,
  `story-002.md` is `Status: In Progress`, `story-003.md` is `Status: Ready`
- Neither `active.md` (its CHECKPOINT names story-002 as the current task, with
  **Next step:** `$gs-dev-story` on it) nor the git log (no commit mentions
  story-002) says story-002's implementation is written

**Input:** `$gs-help`

**Domain checks:**
- [ ] Heading reads `Minimal path — 1 of 3 stories complete`
- [ ] `active.md`'s checkpoint is read before the next step is chosen (Step 3 runs at `minimal`)
- [ ] `→ Next up` is story-002 via `$gs-dev-story`, not story-003
- [ ] No `$gs-gate-check` line and no "Approaching … gate" line appear
- [ ] Game concept, art bible, systems map and GDDs are not listed as next steps
- [ ] No director gate is invoked and no gate IDs appear in output
- [ ] No write tool is called
- [ ] Verdict is COMPLETE

---

### Case 6: Minimal path — the checkpoint says the work is written

**Fixture:**
- As Case 5, except `active.md`'s CHECKPOINT reads
  **Next step:** `$gs-story-done production/epics/core/story-002.md` (what
  `$gs-dev-story` writes when it finishes a story)

**Input:** `$gs-help`

**Domain checks:**
- [ ] `→ Next up` is story-002 via `$gs-story-done`, not `$gs-dev-story`
- [ ] story-002 is not counted or listed as complete
- [ ] Verdict is COMPLETE

---

### Case 7: Minimal path — only a blocked story and an unknown status remain

**Fixture:**
- As Case 5, except `story-002.md` is `Status: Blocked` (its file says it waits
  on the art for the player sprite) and `story-003.md` is `Status: Draft`

**Input:** `$gs-help I'm stuck`

**Domain checks:**
- [ ] story-002 is named with its blocker; story-003 is named with status `Draft`
- [ ] Neither story is recommended to `$gs-dev-story` or `$gs-story-done`
- [ ] The output does not say the build order is done
- [ ] Heading reads `Minimal path — 1 of 3 stories complete`
- [ ] The escalation block appears and has no `$gs-gate-check` line
- [ ] Verdict is COMPLETE


## Applicable domain checks

- [ ] Recommend the next skill without automatically running it.
