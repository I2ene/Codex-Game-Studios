# Evaluation scenarios: gs-team-polish

Professional scenarios adapted from Donchitos' upstream testing guidance; see
[source attribution](../../../NOTICE.md). These are evaluation inputs and domain
checks, not executed results. Read `.agents/skills/gs-team-polish/SKILL.md` and its current procedure first.
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

### Case 1: Happy Path — Full pipeline completes, READY FOR RELEASE verdict

**Fixture:**
- Resolved config block: `team.size: small`, `automation: collaborative`
- Feature exists and is functionally complete (e.g., `combat` system)
- Performance budgets are defined in `project.yaml` (`performance.target_framerate: 60`, `performance.frame_budget_ms: 16.6`, `performance.draw_call_limit: 2000`, `performance.memory_ceiling_mb: 2048`)
- No frame budget violations exist before polishing begins
- No audio events are missing; VFX assets are complete
- No regressions are introduced by polish changes

**Input:** `$gs-team-polish combat`

**Domain checks:**
- [ ] Active-set line naming `team.size: small` appears before the first agent is consulted
- [ ] performance-analyst is consulted first in Phase 1 before any other agents
- [ ] `host input tool` appears after Phase 1 output and before Phases 2/3/4 launch
- [ ] After assessment, optimization, visual and audio polish are independent; hardening waits for all applicable results
- [ ] engine-programmer is NOT consulted when Phase 1 finds no engine-level root causes
- [ ] performance-analyst edits no code, shader or asset in any phase
- [ ] Implementation files of Phases 2–4 are listed by each agent and asked for in one `host input tool` for the whole set — not once per phase — before any is edited
- [ ] qa-tester (Phase 5) is not launched until the parallel phases complete and user approves
- [ ] Each agent writes to its named `production/polish/[area]-…-[date].md` path without a per-write prompt, and the orchestrator confirms the file exists before treating the phase as done
- [ ] Phase 6 verdict is based on comparison of metrics against defined budgets
- [ ] Summary report includes: before/after performance metrics, visual polish changes, audio polish changes, test results
- [ ] Summary states that nothing reads `production/polish/` yet
- [ ] The parent may write authorized artifacts while applying and labeling the responsible discipline
- [ ] Verdict is READY FOR RELEASE

---

### Case 2: Performance Blocker — Frame budget violation cannot be fully resolved

**Fixture:**
- Resolved config block: `team.size: small`, `automation: collaborative`
- Feature being polished: `particle-storm` VFX system
- Phase 1 identifies a frame budget violation: particle-storm costs 12ms on target hardware (budget is 6ms for this system)
- Phase 1's optimisation list assigns the particle work to technical-artist and an engine-level particle-update hot path to engine-programmer; after both are applied the cost is 9ms — still over the 6ms budget
- Phase 2 cannot fully resolve the violation without a fundamental design change

**Input:** `$gs-team-polish particle-storm`

**Domain checks:**
- [ ] Frame budget violation is flagged in Phase 1 with specific numbers (actual vs. budget)
- [ ] Phase 2 reports the post-optimization metric explicitly (9ms achieved, 3ms still over)
- [ ] Verdict is NEEDS MORE WORK (not READY FOR RELEASE) when a budget violation remains
- [ ] The specific unresolved issue is listed by name with the remaining gap quantified
- [ ] Next Steps references `$gs-sprint-plan update` for scheduling the remaining fix
- [ ] Phases 3 and 4 still run (polish work is not abandoned due to a Phase 2 partial resolution)
- [ ] Phase 5 qa-tester still runs (regression testing is independent of the performance outcome)

---

### Case 3: No Argument — Usage guidance shown

**Fixture:**
- Any project state

**Input:** `$gs-team-polish` (no argument)

**Domain checks:**
- [ ] Skill does NOT consults any agents when no argument is provided
- [ ] Usage message shows the full argument-hint — `$gs-team-polish [feature or area to polish] [--review full|lean|solo]` — and argument examples
- [ ] Skill does NOT attempt to guess a feature from project files
- [ ] No `host input tool` is used — output is direct guidance

---

### Case 4: Engine-Level Bottleneck — engine-programmer consulted conditionally in Phase 2

**Fixture:**
- Resolved config block: `team.size: small`, `automation: collaborative`
- Feature being polished: `open-world` environment streaming
- Phase 1 identifies a performance bottleneck with a root cause in the rendering pipeline: "draw call overhead is caused by the engine's scene tree traversal in the spatial indexer — this is an engine-level issue, not a game code issue"
- Performance budgets are defined; the rendering overhead exceeds target frame budget

**Input:** `$gs-team-polish open-world`

**Domain checks:**
- [ ] engine-programmer is NOT consulted in Phase 2 unless Phase 1 explicitly identifies an engine-level root cause
- [ ] engine-programmer is consulted in Phase 2 when Phase 1 identifies an engine-level root cause
- [ ] Engine-programmer expertise handles the engine fix independently of visual and audio polish; performance-analyst does not implement code changes
- [ ] engine-programmer edits nothing before the one ask for the Phase 2–4 implementation set is answered yes
- [ ] Phases 2, 3 and 4 cover independent concerns; authorized delegation may run concurrently, while parent work is labeled accurately
- [ ] engine-programmer's output includes profiler validation of the fix
- [ ] qa-tester in Phase 5 runs regression tests that cover the engine-level change
- [ ] Verdict correctly reflects whether all metrics including the engine fix now meet budgets

---

### Case 5: Regression Found — Polish change broke an existing feature

**Fixture:**
- Resolved config block: `team.size: small`, `automation: collaborative`
- Feature being polished: `inventory-ui`
- Phases 1–4 complete successfully; performance and polish changes are applied
- Phase 5: qa-tester runs regression tests and finds that a shader optimization applied in Phase 3 broke the item highlight glow effect on hover — an existing feature that was working before the polish pass

**Input:** `$gs-team-polish inventory-ui` (Phase 5 scenario)

**Domain checks:**
- [ ] Regression is surfaced before Phase 6 sign-off
- [ ] The specific broken behavior and the responsible change are both named in the report
- [ ] Preserve the case's unresolved human decisions and declines; perform routine writes already authorized, and ask only for missing decisions or scope.
- [ ] `host input tool` at the Phase 5 → 6 transition presents the regression and qa-tester's proposed resolutions as selectable options
- [ ] Phase 6 lists the regression as a remaining issue with severity
- [ ] Verdict is NEEDS MORE WORK when a regression is present and unresolved
- [ ] Next Steps directs the fix to `$gs-sprint-plan update` and a `$gs-team-polish` re-run — no in-session fix is reported as verified

---

### Case 6: No Budgets Committed — NOT ASSESSED, not READY FOR RELEASE

**Fixture:**
- Resolved config block: `team.size: small`, `automation: collaborative`
- `project.yaml` sets none of `performance.target_framerate`, `performance.frame_budget_ms`, `performance.draw_call_limit` or `performance.memory_ceiling_mb`, and no design doc states a budget for the area
- Feature being polished: `main-menu`; every phase completes, and qa-tester finds no regressions

**Input:** `$gs-team-polish main-menu`

**Domain checks:**
- [ ] Verdict is NOT ASSESSED, not READY FOR RELEASE
- [ ] The report names each unset `performance.*` key as the reason
- [ ] No metric is described as within budget, and no headroom is computed against a placeholder budget
- [ ] Next Steps asks for the budgets and a re-run rather than handing off to `$gs-release-checklist`
- [ ] A regression found in the same run would make the verdict NEEDS MORE WORK instead — the missing budgets do not mask a known problem

---

### Case 7: Default `individual` — the optimisation list is handed to `$gs-dev-story`

**Fixture:**
- Resolved config block: `team.size: individual`, `automation: collaborative`
- Budgets committed in `project.yaml` (as in Case 1)
- Feature being polished: `crafting-menu`; Phase 1 finds a draw-call overrun owned by technical-artist and a script hot path in the crafting logic owned by gameplay-programmer — no engine-level root cause

**Input:** `$gs-team-polish crafting-menu`

**Domain checks:**
- [ ] No agent changes code for the gameplay-programmer item in this run, and performance-analyst changes nothing
- [ ] The report names the optimisation list as handed to `$gs-dev-story`, with the path and each item's owner
- [ ] Verdict is never READY FOR RELEASE at `individual`
- [ ] An over-budget metric the handed-off item targets makes the verdict NEEDS MORE WORK


## Applicable domain checks

- [ ] Before professional work starts, resolve and announce team-size scope, parent coverage and any actual participants. At `team.size: individual`: performance-analyst and technical-artist; inactive implementation owners are handed to `$gs-dev-story` rather than silently added. Name inactive perspectives and unassessed work accurately.
- [ ] Missing named artifacts fail their phase; BLOCKED work surfaces immediately and retains completed results.
- [ ] At individual size omitted audio polish and hardening are named as not run: NOT ASSESSED unless a known problem makes the result NEEDS MORE WORK.
- [ ] READY FOR RELEASE requires all applicable phases and committed metric budgets; NEEDS MORE WORK names severity, measured gap and recommended action. Studio hardening is adversarial; no extra engine-specialist roster is inferred.
