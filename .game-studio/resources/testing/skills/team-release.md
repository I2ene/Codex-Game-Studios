# Evaluation scenarios: gs-team-release

Professional scenarios adapted from Donchitos' upstream testing guidance; see
[source attribution](../../../NOTICE.md). These are evaluation inputs and domain
checks, not executed results. Read `.agents/skills/gs-team-release/SKILL.md` and its current procedure first.
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

### Case 1: Happy Path (Single-Player) — All phases complete, version deployed

**Fixture:**
- Resolved config block: `review_mode: full`, `team.size: studio`, `automation: collaborative`
- `project.stage` in `project.yaml` is `Release` (`$gs-gate-check release` has passed)
- Milestone acceptance criteria are all met (producer can confirm)
- `project.yaml` sets `platform.online: false` and `platform.multiplayer: false`; the game collects no player data
- No freeze or platform certification is planned for this release
- All CI builds are clean on `main`
- No open S1/S2 bugs; all strings translated

**Input:** `$gs-team-release v1.0.0`

**Domain checks:**
- [ ] Active-set line naming `team.size: studio` appears before the first agent is consulted
- [ ] Phase 2 cuts no `release/*` branch: the release candidate is the version-bump commit on `main`
- [ ] Phase 3 covers QA and build verification independently; all required quality results precede Phase 4
- [ ] security-engineer is NOT consulted when `platform.online` and `platform.multiplayer` are false and there is no player data, and the Phase 3 output says so by name (e.g. `security-engineer: not consulted — platform.online: false, platform.multiplayer: false, no player data`) — the skip is never silent
- [ ] Each agent is told its own named output file — parallel Phase 3 and Phase 4 agents never share one — and the orchestrator confirms the file exists before treating the phase as done
- [ ] Phase 5 producer collects sign-offs from qa-lead, release-manager, devops-engineer and technical-director before declaring GO
- [ ] Phase 6 deployment only begins after the user picks [A] in the Phase 6 `host input tool`
- [ ] `$gs-changelog` is invoked by release-manager in Phase 6 (not written directly)
- [ ] `$gs-patch-notes v1.0.0` is invoked by release-manager in Phase 6, and community-manager writes the announcement from its output — community-manager is never asked to run `$gs-patch-notes`
- [ ] Phase 7 monitoring plan includes a 48-hour post-release monitoring commitment
- [ ] No stop and no override question at the stage check, because `project.stage` reads `Release`; the skill writes neither `project.stage` nor `production/stage.txt`, and no post-launch stage value is invented
- [ ] Verdict: COMPLETE appears in the final output

---

### Case 2: Go/No-Go: NO — S1 bug found in Phase 3, deployment skipped

**Fixture:**
- Resolved config block: `team.size: small`, `automation: collaborative`, `project.stage: Release`
- The v0.9.0 release candidate is a commit on `main`
- qa-lead discovers a previously unreported S1 crash in the main menu during Phase 3 regression testing
- devops-engineer build is clean and artifacts are ready

**Input:** `$gs-team-release v0.9.0`

**Domain checks:**
- [ ] qa-lead S1 bug finding is surfaced to the user immediately after Phase 3 completes — not suppressed until Phase 5
- [ ] producer's NO-GO decision explicitly references the S1 bug and the quality gate result
- [ ] Phase 6 Deployment is completely skipped when producer declares NO-GO
- [ ] No patch notes or launch announcement are produced on NO-GO — `$gs-patch-notes` is not run and community-manager is NOT consulted
- [ ] The partial report clearly states which phases completed and which were skipped, with reasons
- [ ] Verdict: BLOCKED (not COMPLETE) when deployment is skipped due to NO-GO
- [ ] host input tool offers the user resolution options (fix and re-run / defer / override with rationale)
- [ ] Override path (if chosen) asks for a written justification and embeds it as an "Override Justification" field in the record before any Phase 6 action

---

### Case 3: Security Audit for Online Game — security-engineer is consulted in Phase 3

**Fixture:**
- Resolved config block: `review_mode: full`, `team.size: studio`, `automation: collaborative`, `project.stage: Release`
- `project.yaml` sets `platform.multiplayer: true` and `platform.online: true`; the game stores player account data
- Release candidate exists for v2.1.0
- qa-lead and devops-engineer both return clean sign-offs

**Input:** `$gs-team-release v2.1.0`

**Domain checks:**
- [ ] security-engineer IS consulted in Phase 3 when the game has online features, multiplayer, or player data — this is not skipped
- [ ] network-programmer IS consulted in Phase 3 when the game has multiplayer
- [ ] Phase 3 covers QA, build, security and networking independently, collecting all four results before Phase 4
- [ ] security-engineer audit covers authentication, anti-cheat, and data privacy compliance
- [ ] Phase 5 producer sign-off collection includes security-engineer and network-programmer alongside qa-lead, release-manager, devops-engineer and technical-director
- [ ] Phase 6 deployment does not begin until security-engineer has signed off
- [ ] Skill does NOT treat security-engineer as optional for a game with player data

---

### Case 4: Localization Miss — Untranslated strings reach the go/no-go call

**Fixture:**
- Resolved config block: `team.size: studio`, `automation: collaborative`, `project.stage: Release`
- `project.yaml` sets `platform.online: false` and `platform.multiplayer: false`; no player data
- Release candidate exists for v1.2.0
- Phase 3 (qa-lead, devops-engineer) complete with clean sign-offs
- Phase 4: localization-lead finds 47 untranslated strings in the French locale (a supported language) and returns it as a BLOCKED/CONCERNS item
- producer judges the miss release-blocking and declares NO-GO

**Input:** `$gs-team-release v1.2.0`

**Domain checks:**
- [ ] Phase 4 applies localization-lead expertise in the parent or an authorized delegate when that discipline is in scope
- [ ] The localization finding is presented at the Phase 4 → 5 transition via `host input tool` before the go/no-go runs
- [ ] The producer's NO-GO rationale names the untranslated-strings issue
- [ ] The resolution options include re-running the affected phase — the skill does not require restarting from Phase 1
- [ ] If the user overrides, the written justification is embedded in the record before any Phase 6 action
- [ ] A missing translation remains a release blocker or explicit recorded override; do not fabricate translations or evidence to unblock it
- [ ] Verdict is BLOCKED and Phase 6 does not run on NO-GO

---

### Case 5: No Argument — Skill infers version or asks

In both variants `project.stage` is `Release`.

**Fixture (variant A — milestone data present):**
- `production/milestones/` exists with a milestone file; most recent milestone is "v1.1.0 — Gold"
- `production/session-state/active.md` references a version or milestone

**Fixture (variant B — no discoverable version):**
- `production/milestones/` does not exist
- `production/session-state/active.md` does not reference a version
- No git tags are present from which to infer a version

**Input:** `$gs-team-release` (no argument)

**Expected behavior (variant A):**
1. Argument check: no version provided; reads `production/session-state/active.md` and the most recent milestone file in `production/milestones/`
2. Infers v1.1.0 as the target version; reports "No version argument provided — inferred v1.1.0 from milestone data. Proceeding."
3. Confirms with host input tool before beginning Phase 1: "Releasing v1.1.0. Is this correct?"
4. Proceeds as if `$gs-team-release v1.1.0` was the input

**Expected behavior (variant B):**
1. Argument check: no version provided; reads available state files — no version discoverable
2. Uses host input tool: "What version number should be released? (e.g., v1.0.0)"
3. Waits for user input before proceeding

**Domain checks:**
- [ ] Skill does NOT default to a hardcoded version string when no argument is provided
- [ ] Skill reads `production/session-state/active.md` and milestone files before asking (variant A)
- [ ] Inferred version is confirmed with the user via host input tool before proceeding (variant A)
- [ ] When no version is discoverable, host input tool is used — skill does not guess (variant B)
- [ ] Skill does NOT error out when milestone files are absent — it falls back to asking (variant B)

---

### Case 6: Stage Still Polish — Stops Before Phase 1, Nothing consult

**Fixture:**
- Resolved config block: `review_mode: full`, `team.size: studio`, `automation: autonomous`, `project.stage: Polish`
- `$gs-gate-check release` has not been run; a release candidate exists for v1.0.0

**Input:** `$gs-team-release v1.0.0`

**Expected behavior (variant A — the user stops):**
1. Phase 0 resolves `project.stage: Polish`; the stage check stops before Phase 1: "The release readiness gate has not passed (project.stage: Polish) — run `$gs-gate-check release` first."
2. `host input tool` offers `[A] Stop — I'll run $gs-gate-check release (recommended)` / `[B] Proceed anyway — override the stage check` — asked even though `automation` is `autonomous`
3. User picks `[A]`: no agent is consulted, no file is written, nothing is tagged or deployed
4. Verdict: BLOCKED — release gate not passed

**Expected behavior (variant B — the user overrides):**
1. Same stop and question; user picks `[B]` and, asked why, answers "cert window closes Friday"
2. The run continues to Phase 1 with the override in the producer's brief
3. The go/no-go record (`production/releases/go-no-go-v1.0.0.md`) and the final report carry `Stage override: project.stage was Polish — release gate not passed; the user chose to proceed: cert window closes Friday`
4. `project.stage` still reads `Polish` at the end of the run

**Domain checks:**
- [ ] No delegated work starts before the stage-check question is answered
- [ ] The stop message names `$gs-gate-check release` as the step to run first
- [ ] The question is asked in `autonomous` mode — the override is never taken automatically
- [ ] On `[A]` the verdict is BLOCKED and no agent is consulted at all (not even release-manager)
- [ ] On `[B]` the override and its reason appear in the go/no-go record and in the final report
- [ ] The skill writes neither `project.stage` nor `production/stage.txt` in either variant


## Applicable domain checks

- [ ] Before professional work starts, resolve and announce team-size scope, parent coverage and any actual participants. At `team.size: individual`: release-manager, with other release perspectives routed through it. Name inactive perspectives and unassessed work accurately.
- [ ] Missing named artifacts fail their phase. Each parallel participant has a distinct destination, and every required sign-off is collected before a go/no-go decision.
- [ ] Unknown online/multiplayer/player-data scope is resolved rather than assumed false; skipped security/network work is named with reasons.
- [ ] Lean/solo omits the technical-director sign-off explicitly; a NOT ASSESSED director result is never counted as approval.
- [ ] A stabilization release branch accepts fixes only, propagated to main. Tagging, publication and deployment require applicable explicit user authorization; no path or role supplies it.
- [ ] A NO-GO without an explicit recorded override blocks deployment and preserves the partial report. A staging-only choice holds production; COMPLETE requires the deployment scope actually authorized and executed.
