# Evaluation scenarios: gs-story-done

Professional scenarios adapted from Donchitos' upstream testing guidance; see
[source attribution](../../../NOTICE.md). These are evaluation inputs and domain
checks, not executed results. Read `.agents/skills/gs-story-done/SKILL.md` and its current procedure first.
Use [evaluation policy](../README.md) and [category rubric](../quality-rubric.md).

Resolve current config and project engine records. Apply review-mode discipline
coverage without claiming automatic delegation: use the parent when needed, label it,
and record actual participants only. Existing human authorization governs writes;
case approvals represent unresolved decisions and never revoke prior authorization.
Historical fixture versions are scenario inputs, not current API verification.
The linked native procedure governs command arguments, output schemas, receipts,
context and mode applicability. Missing inputs remain NOT ASSESSED.

### Case 1: Happy Path — All acceptance criteria met, no deviations

**Fixture:**
- `project.yaml` sets `modes.rigor: standard` (→ `workflow: standard`,
  `qa.level: standard`, `review_mode: lean`) and `engine.name: Godot`, so
  `tests/unit/` is the test root
- Story file at `production/epics/core/story-light-pickup.md` with:
  - `Type: Logic` and 3 acceptance criteria, all implemented as described:
    AC-1 "Picking up a light adds it to the inventory", AC-2 "A pickup at the
    carry limit is refused", AC-3 "The picked-up light leaves the world"
  - `TR-light-001`; the story quotes an older wording of the requirement, while
    `tr-registry.yaml` holds the current text, which the implementation matches
  - `ADR: ADR-0003` (Accepted), whose guidance was followed
  - A `## Test Evidence` section naming `tests/unit/light/pickup_test.gd`, which
    exists with one test per criterion — `test_pickup_adds_to_inventory`,
    `test_pickup_refused_at_limit`, `test_pickup_removes_world_light` — so every
    criterion maps to a test
  - `Status: In Progress`
- The `$gs-dev-story` checkpoint in `production/session-state/active.md` names this
  story as **Current task** and carries `Run result: OBSERVED — the light leaves
  the floor and the inventory count rises —
  production/qa/evidence/story-light-pickup/01-pickup.png`; that image exists
- Implementation files listed in the story exist in the code root
- A sprint plan in `production/sprints/` has other READY / NOT STARTED Must Have stories

**Input:** `$gs-story-done production/epics/core/story-light-pickup.md`

**Domain checks:**
- [ ] Requirement text comes from `tr-registry.yaml`, not the story's stale quote — the wording difference produces no deviation
- [ ] Skill reads only the ADR's `## Decision` and `## Consequences` spans, not the whole file
- [ ] Each criterion is listed with its status (`auto-verified` / `confirmed` / `FAILS` / `DEFERRED`) and appears in a Criterion | Test | Status traceability table
- [ ] Test evidence is reported as present, without claiming the tests pass
- [ ] In `lean` mode the skill asks whether `$gs-code-review` was run, and records the answer in the Completion Notes `Code Review:` line
- [ ] Full-mode variant: LP-CODE-REVIEW performed in the parent records `parent assessment (lead-programmer lens); no independent review` consistently in the report, Completion Notes and closing Review line; running a role's gate does not create an independent participant.
- [ ] Full-mode authorized-delegate variant: Reviewed by records the actual participant ID or observed identity together with `role: lead-programmer` and its verdict. A missing or unperformed gate is NOT ASSESSED, never a fabricated approval or identity.
- [ ] The traceability table maps each of AC-1..AC-3 to its test function, with no UNTESTED row
- [ ] The `Run result:` line is read from the checkpoint (whose **Current task** names this story) and noted with its retained path
- [ ] Verdict is COMPLETE — every criterion maps to a test, the run was observed and retained, and no deviations exist
- [ ] No file is edited before the Phase 7 `host input tool`; on "Close the story" the story gets `Status: Complete`, a `Last Updated:` date and a `## Completion Notes` section
- [ ] After completion, skill surfaces the next READY / NOT STARTED Must Have or Should Have story from `production/sprints/` and suggests `$gs-story-readiness [path]`

---

### Case 2: Criteria needing manual or playtest verification

**Input (all subscenarios):** `$gs-story-done production/epics/core/story-light-pickup.md`

**Case 2a — retained animation evidence and genuinely human-only feel:**

**Fixture (2a):**
- Case 1's three implemented criteria and observed run still apply.
- AC-4: "Player sees the correct pickup animation"; no automated test, but a frame is retained at `production/qa/evidence/story-light-pickup/02-pickup-anim.png`.
- AC-5: "Pickup feedback feels satisfying after sustained human play"; this subjective feel has not been playtested and has no automated test.

**Domain checks (2a):**
- [ ] Ask about unverifiable criteria, batching at most four questions; reading behavior code never verifies runtime behavior.
- [ ] Open `02-pickup-anim.png` before describing it. Quote the checkpoint's Run result as the dev-story author's description, not this reviewer's own observation.
- [ ] Only the genuinely human-playtest-only AC-5 is `DEFERRED — requires playtest session`; the observed animation and other criteria retain their actual evidence.
- [ ] COMPLETE WITH NOTES is permitted for these inputs, listing the deferred feel criterion and its human-playtest recommendation.
- [ ] Preserve the explicit close decision before updating the story; no independent participant or sign-off is invented.

**Case 2b — testable persistence has not run:**

**Fixture (2b):**
- Case 1's Logic story and standard QA apply.
- Add "Pickup state persists across a full level run"; the required build/run has not happened, with no covering test execution or retained evidence. The user says "I'll check it when I play".

**Domain checks (2b):**
- [ ] Persistence is testable behavior: mark it UNTESTED, never DEFERRED merely because it needs a full build or a later play session.
- [ ] Apply the actual evidence gate. At the default blocking Logic gate the required evidence gap is BLOCKED; with an explicit advisory gate, the unassessed criterion still keeps the verdict at best NOT ASSESSED, never COMPLETE WITH NOTES.
- [ ] Name the build/test/run and retained evidence needed to settle the criterion; do not manufacture an observed result from code or the user's future intent.
- [ ] Recommend not closing until settled; any explicit override is recorded as such, without converting the missing evidence to a pass.

**Case 2c — observed/manual criterion fails:**

**Fixture (2c):**
- Use 2a, but the user answers `No — fails` for the animation criterion.

**Domain checks (2c):**
- [ ] Mark that criterion FAILS and the verdict BLOCKED, regardless of the separately deferred feel item; do not proceed to close on the reviewer's own initiative.

**Case 2d — claimed animation pass without observation:**

**Fixture (2d):**
- Use 2a, but no image is retained for this story and the checkpoint has no Run result. The user answers `Yes — passes` for the animation.

**Domain checks (2d):**
- [ ] The answer is an assertion, not retained observation. Flag missing evidence at the Logic gate level (blocking by default): BLOCKED, never COMPLETE WITH NOTES solely on that confirmation.
- [ ] Require the actual unresolved close decision before any story write; preserve already-authorized routine work without inventing approval.

---

### Case 3: Blocked Path — GDD deviation detected

**Fixture:**
- `project.yaml` sets `modes.workflow: full`
- The current `tr-registry.yaml` text for the story's TR-ID: "Player can carry max 3 light sources"
- Implementation in the code root has `MAX_CARRIED_LIGHTS = 5` in gameplay code

**Input:** `$gs-story-done production/epics/core/story-light-pickup.md`

**Domain checks:**
- [ ] Skill detects the mismatch between the current requirement text and the implemented value
- [ ] The deviation is reported neutrally as BLOCKING with the GDD/TR reference — the skill does not edit code or the GDD to reconcile it
- [ ] Verdict is BLOCKED, and Phase 7 is not entered unless the user explicitly asks to close anyway
- [ ] Closing a BLOCKED story goes through the Phase 7 `host input tool` regardless of automation mode
- [ ] If closed via "Accept deviations as-is and close anyway", the deviation is recorded in the Completion Notes `Deviations:` line

---

### Case 4: Edge Case — No argument, auto-detect current story

**Fixture:**
- `production/session-state/active.md` names `production/epics/core/story-oxygen-drain.md` as the active story
- That story file exists with `Status: In Progress`

**Input:** `$gs-story-done` (no argument)

**Domain checks:**
- [ ] With no story argument, recovery resolves the configured checkpoint and uses its active story when present
- [ ] The report's `**Story**:` line names the auto-detected story file
- [ ] With several in-progress stories in the sprint, skill asks which one via `host input tool` instead of picking one
- [ ] If no story is found anywhere, skill asks the user to provide a path

---

### Case 5: Director Gate — LP-CODE-REVIEW across review modes
**Fixture:**
- `project.yaml` sets `modes.workflow: full` and `qa.level: standard` (so the
  QA coverage gate is not skipped for `qa.level: minimal`)
- Story file at `production/epics/core/story-light-pickup.md`, `Type: Logic`
- All acceptance criteria verified, no GDD deviations, implementation files exist,
  and Case 1's run evidence (the `Run result: OBSERVED` checkpoint and its retained image)
- Review mode comes from `modes.review_mode` (legacy mirror `production/review-mode.txt`) or `--review`

**Case 5a — full mode:** `$gs-story-done production/epics/core/story-light-pickup.md --review full`

**Domain checks (5a):**
- [ ] Skill uses the resolved review mode before deciding whether to consult LP-CODE-REVIEW
- [ ] LP-CODE-REVIEW is consulted in full mode after the implementation checks, with the four context items
- [ ] A REJECT verdict prevents the story from reaching a COMPLETE verdict until resolved
- [ ] A CONCERNS verdict produces the three-option `host input tool`
- [ ] A NOT ASSESSED answer from either gate is never treated as APPROVE / ADEQUATE: unless the missing input is supplied and the gate re-run, the verdict is NOT ASSESSED, not COMPLETE
- [ ] Skill still asks via the Phase 7 `host input tool` before updating story status, even after APPROVE

**Case 5b — lean mode:** `--review lean`

**Domain checks (5b):**
- [ ] LP-CODE-REVIEW does NOT consult
- [ ] Skill asks "Did you run `$gs-code-review` on the implemented files?" with the three listed options; all three proceed
- [ ] "QL-TEST-COVERAGE skipped — Lean mode." is noted

**Case 5c — solo mode:** `--review solo`

**Domain checks (5c):**
- [ ] Neither LP-CODE-REVIEW nor QL-TEST-COVERAGE consult, and no code-review question is asked
- [ ] Output notes "LP-CODE-REVIEW skipped — Solo mode." and "QL-TEST-COVERAGE skipped — Solo mode."
- [ ] Skill still requires the Phase 7 `host input tool` before marking the story Complete

---

### Case 6: UI story at `minimal`, no sprint plan — the screenshot closes it

**Fixture:**
- `project.yaml` sets `modes.rigor: minimal` (→ `workflow: minimal`,
  `qa.level: minimal`, `review_mode: solo`); there is no sprint plan in
  `production/sprints/` — the brief's build order is the plan
- `production/epics/mvp/` holds `story-001-*.md` (`Status: Complete`), this story
  `story-002-shop-panel.md` (`Status: In Progress`) and `story-003-*.md` (`Status: Ready`)
- `story-002-shop-panel.md` has `Type: UI` and two criteria: "The shop panel shows
  all 6 item slots inside the frame at 1280x720" and "Each slot shows its price"
- `production/qa/evidence/story-002-shop-panel/01-shop-open.png` exists and shows
  both; the checkpoint carries `Run result: OBSERVED` with that path; there is no
  evidence doc and no sign-off

**Input:** `$gs-story-done production/epics/mvp/story-002-shop-panel.md`

**Domain checks:**
- [ ] The UI screenshot check runs at `qa.level: minimal` and is satisfied by the retained image alone — no evidence doc or sign-off is required for a UI story
- [ ] Verdict is COMPLETE, not BLOCKED for a missing sign-off
- [ ] Phase 8 names `story-003` and recommends `$gs-dev-story` directly — no `$gs-story-readiness` line at `minimal`, and no Sprint Close-Out Sequence
- [ ] Use the linked native procedure and explicit runtime command; retired host execution is not required.
- [ ] Variant — `production/epics/combat/story-001-arena.md` reads `**Status:** In Review`: it is Next Up (the script lists `IN_REVIEW` first, across every epic folder), and the Next Up line recommends `$gs-story-done [path]` to close it, not `$gs-dev-story`
- [ ] Variant — no image under `production/qa/evidence/` and no `Run result:` line: the UI gate is still BLOCKING at `qa.level: minimal`, so the verdict is BLOCKED
- [ ] Variant — `story-003` is `Blocked`, naming its blocker, and no other story is unfinished: Phase 8 prints no Next Up, names `story-003` with its blocker, suggests clearing it, and never says the build order is done

---

### Case 7: NOT ASSESSED — a criterion nobody could evaluate

**Fixture:**
- As Case 1, plus a fourth criterion, AC-4: "The pickup code is robust" — it
  names no observable outcome, so no test, run or playtest could settle it

**Input:** `$gs-story-done production/epics/core/story-light-pickup.md`

**Domain checks:**
- [ ] Verdict is NOT ASSESSED — not COMPLETE or COMPLETE WITH NOTES, and not BLOCKED (nothing is known to fail)
- [ ] Output names AC-4, why it cannot be evaluated, and what would make it checkable
- [ ] Phase 7 is entered only if the user explicitly asks to close anyway; it then always prompts (`scope_changes`), and the Completion Notes record AC-4 as never evaluated
- [ ] Variant — AC-4 is a checkable criterion that the user answers `Not tested yet`: it is UNTESTED in the traceability table and the verdict is NOT ASSESSED, naming what would settle it
- [ ] Variant — another criterion also FAILS: the verdict is BLOCKED (BLOCKED is evaluated before NOT ASSESSED)

---

### Case 8: Read only references needed by the completion branch

**Fixture:** As Case 1: standard/lean Godot Logic story with three covered criteria and retained execution
evidence, no sprint/status file and no advisory deviations. Variant: full review, sprint has
another story and there is an advisory deviation; user chooses to close and log debt.

**Input:** `$gs-story-done production/epics/core/story-light-pickup.md`

**Domain checks:**
- [ ] Lean case offers the appropriate code review without loading the branch-only
  `review-gates.md`, `sprint-next.md` or `tech-debt-row.md`. Required common procedure still
  applies.
- [ ] Variant reads each actual branch reference before that work: review brief before the
  review, debt row before logging, sprint-next before Next Up. Preserve review/QA/automation
  settings and unresolved closure decisions; do not add duplicate authorization prompts.

---

## Applicable domain checks

- [ ] Only the “Close and log advisory deviations as tech debt” choice appends debt entries; append rows in the tech-debt register table with an Added date, never free-form bullets.
