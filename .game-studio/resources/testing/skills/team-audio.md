# Evaluation scenarios: gs-team-audio

Professional scenarios adapted from Donchitos' upstream testing guidance; see
[source attribution](../../../NOTICE.md). These are evaluation inputs and domain
checks, not executed results. Read `.agents/skills/gs-team-audio/SKILL.md` and its current procedure first.
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

### Case 1: Happy Path — All steps complete, audio design document saved

**Fixture:**
- Resolved config block: `team.size: studio`, `automation: collaborative`
- `engine.name` in `project.yaml` is Godot
- GDD for the target feature exists at `design/gdd/combat.md`
- Sound bible exists at `design/audio/sound-bible.md`
- Existing audio assets are listed in `assets/audio/`
- No accessibility gaps exist in the planned audio event list

**Input:** `$gs-team-audio combat`

**Domain checks:**
- [ ] Active-set line naming `team.size: studio` appears before the first agent is consulted
- [ ] Sound bible is read during context gathering (before Step 1) when it exists
- [ ] audio-director is consulted before sound-designer or accessibility-specialist
- [ ] `host input tool` appears after Step 1 output and before Step 2 launch
- [ ] Step 2 covers sound design and accessibility independently; both results are available before Step 3
- [ ] Step 3 covers technical-art and configured engine expertise independently before gameplay implementation
- [ ] gameplay-programmer is not launched until Step 3 `host input tool` is approved
- [ ] gameplay-programmer writes no code or test file before the one ask for its implementation set is answered yes
- [ ] Preserve the case's unresolved human decisions and declines; perform routine writes already authorized, and ask only for missing decisions or scope.
- [ ] Summary includes audio event count and estimated asset count
- [ ] Verdict is COMPLETE after document delivery

---

### Case 2: Accessibility Gap — Critical gameplay audio event has no visual fallback

**Fixture:**
- Resolved config block: `team.size: studio`, `automation: collaborative`
- GDD for the target feature exists
- Step 1 and Step 2 are in progress
- sound-designer's audio event list includes "EnemyNearbyAlert" — a spatial audio cue that warns the player an enemy is approaching from off-screen
- accessibility-specialist reviews the event list and finds "EnemyNearbyAlert" has no visual fallback (no on-screen indicator, no subtitle, no controller rumble specified)

**Input:** `$gs-team-audio stealth` (Step 2 scenario)

**Domain checks:**
- [ ] Accessibility gap is labeled BLOCKING (not advisory) in the report
- [ ] The specific event name ("EnemyNearbyAlert") and the nature of the gap are stated
- [ ] `host input tool` surfaces the gap before Step 3 is launched
- [ ] At least one resolution option is offered (add visual fallback, add haptic fallback)
- [ ] Step 3 is not launched while the gap is unresolved without explicit user authorization
- [ ] If the user stops, the verdict is `BLOCKED — [reason]` naming the gap and the Step 1–2 outputs are kept in a partial report; if the user carries it forward, the final summary lists it as an open question

---

### Case 3: No Argument — Usage guidance or design doc inference

**Fixture:**
- Any project state

**Input:** `$gs-team-audio` (no argument)

**Domain checks:**
- [ ] Skill does NOT consults any agents when no argument is provided
- [ ] Usage message shows the full argument-hint — `$gs-team-audio [feature or area to design audio for] [--review full|lean|solo]` — and argument examples
- [ ] Skill does NOT attempt to infer a feature from existing design docs without user direction
- [ ] No `host input tool` is used — output is direct guidance

---

### Case 4: Missing Sound Bible — Skill notes the gap and proceeds without it

**Fixture:**
- Resolved config block: `team.size: small`, `automation: collaborative`
- GDD for the target feature exists at `design/gdd/main-menu.md`
- No sound bible exists at `design/audio/sound-bible.md` or `design/gdd/sound-bible.md`
- Engine is configured; other context files are present

**Input:** `$gs-team-audio main menu`

**Domain checks:**
- [ ] Orchestrator checks for the sound bible during context gathering (before Step 1)
- [ ] Missing sound bible is noted explicitly in conversation — not silently ignored
- [ ] Pipeline does NOT halt due to the missing sound bible
- [ ] audio-director is notified that no sound bible exists in its prompt context
- [ ] Use the linked native procedure and explicit runtime command; retired host execution is not required.
- [ ] The skill does not write `design/audio/sound-bible.md` itself in this run
- [ ] Verdict is still COMPLETE if all other steps succeed

---

### Case 5: Engine Not Configured — Engine specialist step skipped and recorded

**Fixture:**
- Resolved config block: `team.size: studio`, `automation: collaborative`
- `engine.name` is unset in `project.yaml`, and `.game-studio/resources/docs/technical-preferences.md` has no Primary engine specialist (shows `[TO BE CONFIGURED]`)
- GDD for the target feature exists
- Sound bible may or may not exist

**Input:** `$gs-team-audio boss encounter`

**Domain checks:**
- [ ] Engine specialist is NOT consulted when no engine is configured
- [ ] Skill does NOT error out due to the missing engine configuration
- [ ] The run output contains `Engine validation: NOT ASSESSED — no engine configured` with the `engine.name` reason — the skip is not silently omitted
- [ ] Engine integration is never described as validated or passed in this run
- [ ] technical-artist is still consulted in Step 3 (skip applies only to the engine specialist)
- [ ] gameplay-programmer still runs in Step 4
- [ ] Verdict is `COMPLETE — engine validation NOT ASSESSED (…)`, never a plain COMPLETE (engine not configured is a graceful case, not a blocker)


## Applicable domain checks

- [ ] Before professional work starts, resolve and announce team-size scope, parent coverage and any actual participants. At `team.size: individual`: sound-designer; audio-director, accessibility-specialist, technical-artist, engine-specialist and gameplay-programmer perspectives are routed through it. Name inactive perspectives and unassessed work accurately.
- [ ] Final document is `design/audio/audio-[feature].md`; missing named step artifacts fail the step rather than counting as completed.
- [ ] BLOCKED results surface immediately, preserve completed outputs in a partial report, and retain the `$gs-dev-story` / `$gs-asset-audit` handoff.
