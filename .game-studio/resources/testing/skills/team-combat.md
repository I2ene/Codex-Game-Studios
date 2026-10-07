# Evaluation scenarios: gs-team-combat

Professional scenarios adapted from Donchitos' upstream testing guidance; see
[source attribution](../../../NOTICE.md). These are evaluation inputs and domain
checks, not executed results. Read `.agents/skills/gs-team-combat/SKILL.md` and its current procedure first.
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

### Case 1: Happy Path — All agents succeed, full pipeline runs to completion

**Fixture:**
- Resolved config block: `team.size: small`, `automation: collaborative`, `workflow: full`
- `design/gdd/game-concept.md` exists and is populated
- `engine.name` in `project.yaml` is Godot
- No existing GDD for the requested combat feature
- The feature involves NPC reactions (enemies parry and riposte), so AI work is flagged

**Input:** `$gs-team-combat parry and riposte system`

**Domain checks:**
- [ ] Active-set line naming `team.size: small` appears before the first agent is consulted
- [ ] `host input tool` called at each phase transition (at minimum before Phase 3 and before Phase 5)
- [ ] The pre-Phase 3 gate offers [A] Proceed / [B] Revise / [C] Stop, and no implementation agent is consulted unless [A] is chosen
- [ ] Phase 3 covers gameplay, flagged AI, VFX and sound disciplines independently; integration waits for all required results
- [ ] Engine specialist runs in Phase 2 before Phase 3 begins (output incorporated into architecture)
- [ ] Each agent prompt names its destination from the path table; no sub-agent writes under `design/`
- [ ] No implementation file (code root, `assets/`) is written before one ask covering the whole Phase 3 set
- [ ] Preserve the case's unresolved human decisions and declines; perform routine writes already authorized, and ask only for missing decisions or scope.
- [ ] Verdict COMPLETE present in final report
- [ ] Next steps include `$gs-code-review`, `$gs-balance-check`, `$gs-team-polish`
- [ ] Design doc covers all 8 required GDD sections

---

### Case 2: Blocked Agent — One subagent returns BLOCKED mid-pipeline

**Fixture:**
- Resolved config block: `team.size: small`, `automation: collaborative`
- `design/gdd/parry-riposte.md` exists (Phase 1 already complete)
- ai-programmer agent returns BLOCKED because no AI system architecture ADR exists (ADR status is Proposed)

**Input:** `$gs-team-combat parry and riposte system`

**Domain checks:**
- [ ] BLOCKED surface message appears before any dependent phase continues
- [ ] `host input tool` offers at minimum three options: skip / retry / stop
- [ ] Partial report produced — completed agents' work is not discarded
- [ ] Overall verdict is BLOCKED (not COMPLETE) when any agent is unresolved
- [ ] Blocked reason references the ADR and suggests `$gs-architecture-decision`
- [ ] Orchestrator does not silently proceed past the blocked dependency

---

### Case 3: No Argument — Clear usage guidance shown

**Fixture:**
- Any project state

**Input:** `$gs-team-combat` (no argument)

**Domain checks:**
- [ ] Skill does NOT consults any specialist disciplines when no argument is given
- [ ] Usage message shows the full argument-hint: `$gs-team-combat [combat feature description] [--review full|lean|solo]`
- [ ] Error message includes at least one example of a valid invocation
- [ ] No file reads beyond what is needed to detect the missing argument
- [ ] Verdict is NOT shown (pipeline never runs)

---

### Case 4: Parallel Phase Validation — Phase 3 independent disciplines

**Fixture:**
- Resolved config block: `team.size: small`, `automation: collaborative`
- `design/gdd/parry-riposte.md` exists, is complete, and flags enemy AI reactions
- Architecture sketch has been approved with option [A]
- Engine specialist has validated architecture

**Input:** `$gs-team-combat parry and riposte system` (resuming from Phase 2 complete)

**Domain checks:**
- [ ] The four independent disciplines share the approved architecture as input; no result is made an artificial prerequisite of another
- [ ] Phase 4 does not begin until all four Phase 3 agents have returned results
- [ ] Skill does not pass one Phase 3 agent's output as input to another Phase 3 agent (they are independent)
- [ ] All four Phase 3 agent results referenced in the Phase 4 integration step

---

### Case 5: Architecture Phase Engine Routing — Engine specialist resolved from config

**Fixture (variant A — engine configured):**
- Resolved config block: `team.size: small`, `automation: collaborative`
- `engine.name` in `project.yaml` is Godot; engine version pinned in `<project-engine-reference>/godot/VERSION.md`
- Architecture sketch produced by gameplay-programmer is available, and the orchestrator has read it

**Fixture (variant B — no engine configured):**
- As variant A, except `engine.name` is unset in `project.yaml` and `.game-studio/resources/docs/technical-preferences.md` has no Primary engine specialist (shows `[TO BE CONFIGURED]`)

**Input:** `$gs-team-combat parry and riposte system`

**Expected behavior (variant A):**
1. Phase 2 — gameplay-programmer produces architecture sketch
2. Skill derives the primary engine specialist from `engine.name` (Godot → `godot-specialist`); `technical-preferences.md` is consulted only if `engine.name` is absent
3. Engine specialist is consulted with a distilled brief of the architecture sketch (not a path to a document the orchestrator has already read) and asked the three Phase 2 questions: idiomatic class/node structure, engine-native systems to prefer, APIs deprecated or changed in the pinned engine version
4. Engine specialist writes its notes to `docs/architecture/parry-riposte-engine-notes.md`; the orchestrator checks the file exists before treating the step as done
5. Orchestrator incorporates engine notes into the architecture before presenting Phase 2 results to user
6. `host input tool` architecture gate includes engine specialist's notes alongside the architecture sketch

**Expected behavior (variant B):**
1. Phase 2 — gameplay-programmer produces architecture sketch
2. No engine specialist is consulted and no engine-notes file is expected
3. The run output records `Engine validation: NOT ASSESSED — no engine configured (engine.name unset in project.yaml)`
4. The architecture gate still runs; it presents the sketch without describing it as engine-validated
5. When the run completes, the verdict is `COMPLETE — engine validation NOT ASSESSED (no engine configured)`

**Domain checks:**
- [ ] Engine specialist agent type is derived from `engine.name` (falling back to `technical-preferences.md`) — not hardcoded (variant A)
- [ ] Because the orchestrator has already read the sketch, the engine specialist's brief carries the relevant sketch content inline rather than the sketch's path (variant A)
- [ ] Engine specialist checks for deprecated or changed APIs against the pinned engine version (variant A)
- [ ] Engine specialist output is incorporated before Phase 3 begins (not skipped or appended separately) (variant A)
- [ ] The engine specialist is not consulted and the run output records `Engine validation: NOT ASSESSED — no engine configured` — the skip is never silent (variant B)
- [ ] The architecture is never described as engine-validated when no specialist ran (variant B)
- [ ] When the run completes, its verdict reads `COMPLETE — engine validation NOT ASSESSED ([reason])` — never a plain COMPLETE (variant B)


## Applicable domain checks

- [ ] Before professional work starts, resolve and announce team-size scope, parent coverage and any actual participants. At `team.size: individual`: gameplay-programmer; AI work is escalated only when flagged, and other perspectives are routed through the responsible discipline. Name inactive perspectives and unassessed work accurately.
- [ ] Missing named artifacts fail the phase; a partial report preserves completed work and distinguishes COMPLETE, NEEDS WORK and BLOCKED.
- [ ] At studio size the adversarial QA pass looks for failures; subsystem expertise may be applied by the parent or authorized delegates without claiming a tools grant.
