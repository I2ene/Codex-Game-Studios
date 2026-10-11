# Evaluation scenarios: gs-team-qa

Professional scenarios adapted from Donchitos' upstream testing guidance; see
[source attribution](../../../NOTICE.md). These are evaluation inputs and domain
checks, not executed results. Read `.agents/skills/gs-team-qa/SKILL.md` and its current procedure first.
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

### Case 1: Happy Path — All stories pass manual QA, APPROVED verdict

**Fixture:**
- Resolved config block: `team.size: small`, `automation: collaborative`
- `production/sprints/sprint-03.md` lists 4 stories whose story files exist
- Stories are a mix of types: 1 Logic (its unit test exists and passes), 1 Integration (no automated test), 2 Visual/Feel
- All stories have acceptance criteria populated
- The most recent `production/qa/smoke-[date].md` report has verdict PASS
- `production/qa/bugs/` contains no bugs

**Input:** `$gs-team-qa sprint-03`

**Domain checks:**
- [ ] Active-set line naming `team.size: small` appears before the first agent is consulted
- [ ] Phase 1 correctly counts and reports 4 stories with current stage
- [ ] Strategy table in Phase 2 classifies all 4 stories with correct types
- [ ] Smoke check verdict is taken from the existing `production/qa/smoke-*.md` report and its source is shown
- [ ] Preserve the case's unresolved human decisions and declines; perform routine writes already authorized, and ask only for missing decisions or scope.
- [ ] Phase 4 consults a single qa-tester at `team.size: small`, and its prompt names each story's `production/qa/test-cases/` path
- [ ] Sign-off report includes Test Coverage Summary table and Verdict: APPROVED
- [ ] Verdict: COMPLETE appears in final output
- [ ] Next step: "Run `$gs-gate-check` to validate advancement."

---

### Case 2: Smoke Check Fail — QA cycle stops at Phase 2

**Fixture:**
- Resolved config block: `team.size: small`, `automation: collaborative`
- `production/sprints/sprint-04.md` lists 3 stories
- The most recent `production/qa/smoke-[date].md` report has verdict FAIL with 2 listed failures (build unstable on launch, core navigation broken)

**Input:** `$gs-team-qa sprint-04`

**Domain checks:**
- [ ] Smoke check verdict comes from the `production/qa/smoke-*.md` report — qa-lead does not re-derive it or re-interview the user
- [ ] Smoke check FAIL halts the pipeline at Phase 2 — Phases 3, 4, 5, 6 are NOT executed
- [ ] Failure list is shown to the user explicitly (not summarized vaguely)
- [ ] Skill recommends `$gs-smoke-check sprint` and a `$gs-team-qa` re-run as remediation steps
- [ ] No QA plan and no QA sign-off report is written or offered
- [ ] Orchestrator verdict is BLOCKED, not COMPLETE

---

### Case 3: Bug Found — Visual/Feel story fails manual QA, bug report filed

**Fixture:**
- Resolved config block: `team.size: small`, `automation: collaborative`
- `production/sprints/sprint-05.md` lists 2 stories: 1 Logic (its automated test passes), 1 Visual/Feel
- The most recent `production/qa/smoke-[date].md` report has verdict PASS
- The Visual/Feel story's animation timing is visibly wrong (acceptance criterion not met)
- `production/qa/bugs/` already contains `BUG-0001.md` and `BUG-0002.md`

**Input:** `$gs-team-qa sprint-05`

**Domain checks:**
- [ ] FAIL result in Phase 5 triggers `host input tool` to collect the failure description before the bug report is written
- [ ] Bug-report drafting applies qa-tester expertise in the parent or an authorized delegate; the record names who actually performed it
- [ ] Bug report follows `$gs-bug-report`'s naming: `BUG-[NNNN].md` in `production/qa/bugs/`
- [ ] The ID is one past the highest existing bug, zero-padded to four digits (BUG-0003)
- [ ] Phase 6 sign-off report Bugs Found table includes the bug ID, story name, severity, and status
- [ ] Verdict in sign-off report is NOT APPROVED
- [ ] Next step explicitly mentions re-running `$gs-team-qa`
- [ ] Verdict: COMPLETE is still issued by the orchestrator (the QA cycle finished — the sign-off verdict is NOT APPROVED, but the skill completed its pipeline)

---

### Case 4: No Argument — Skill infers active sprint or asks user

**Fixture (variant A — state files present):**
- `production/session-state/active.md` exists and contains a reference to `sprint-06`
- `production/sprint-status.yaml` exists and identifies `sprint-06` as active
- `production/sprints/sprint-06.md` exists

**Fixture (variant B — no sprint, as at `rigor: minimal`):**
- `production/session-state/active.md` does NOT exist
- `production/sprint-status.yaml` does NOT exist
- No sprint files exist; epics exist under `production/epics/`

**Input:** `$gs-team-qa` (no argument)

**Expected behavior (variant A):**
1. Phase 1: No argument provided; reads `production/session-state/active.md` and `production/sprint-status.yaml`
2. Detects `sprint-06` as the active sprint
3. Proceeds as if `$gs-team-qa sprint-06` was the input; the Phase 1 report line names it: "QA cycle starting for sprint-06. Found [N] stories. Open bugs in scope: [N or none on file]. Current stage: [stage]. Ready to begin QA strategy?"

**Expected behavior (variant B):**
1. Phase 1: No argument provided; attempts to read both state files — both missing; no sprint exists
2. Asks the user which epic to cover, then scopes the run as `feature: [epic-slug]` — it does not invent a sprint

**Domain checks:**
- [ ] Skill does NOT default to a hardcoded sprint name when no argument is provided
- [ ] Skill reads both `production/session-state/active.md` AND `production/sprint-status.yaml` before asking the user (variant A)
- [ ] When no sprint can be inferred, skill asks which epic to cover and uses the `feature: [epic-slug]` form rather than guessing (variant B)
- [ ] The inferred sprint is named in the Phase 1 report line before Phase 2 begins (variant A)
- [ ] Skill does NOT error out when state files are missing — it falls back to asking (variant B)

---

### Case 5: Mixed Results — Some PASS, one FAIL with S1 bug, one BLOCKED

**Fixture:**
- Resolved config block: `team.size: small`, `automation: collaborative`
- `production/sprints/sprint-07.md` lists 4 stories
- The most recent `production/qa/smoke-[date].md` report has verdict PASS
- Story A (Logic): automated test passes — PASS
- Story B (UI): manual QA — PASS WITH NOTES (minor text overflow)
- Story C (Visual/Feel): manual QA — FAIL; tester identifies S1 crash on ability activation
- Story D (Integration): cannot test — BLOCKED (dependency system not yet implemented)
- `production/qa/bugs/` is empty

**Input:** `$gs-team-qa sprint-07`

**Domain checks:**
- [ ] All 4 stories appear in the Phase 6 sign-off report Test Coverage Summary table — none are silently omitted
- [ ] Story D (BLOCKED) is listed in the report with a BLOCKED status and named as lacking executed evidence, not silently dropped
- [ ] S1 bug causes Verdict: NOT APPROVED regardless of the other stories passing, and regardless of Story D being unexecuted
- [ ] PASS WITH NOTES stories do not downgrade to FAIL — they are tracked separately
- [ ] Story B's evidence is its retained screenshots — a UI story needs no lead sign-off to close
- [ ] BUG-0001 severity is listed as S1 in the Bugs Found table
- [ ] Partial results are preserved — the sign-off report is still produced even with failures and blocks
- [ ] Verdict: COMPLETE is issued by the orchestrator (pipeline completed); sign-off verdict is NOT APPROVED

---

### Case 6: `qa.level: minimal` — a Logic story with no test is evidenced by its acceptance-criteria walk

**Fixture:**
- Resolved config block: `team.size: small`, `automation: collaborative`, `qa.level: minimal (rigor:minimal)`
- No sprint files and no `production/sprint-status.yaml`; `production/epics/combat/` holds 2 story files, both `In Review`: story-001 (Logic, no test file anywhere) and story-002 (UI)
- The most recent `production/qa/smoke-[date].md` report has verdict PASS (its automated row WAIVED)
- `production/qa/bugs/` contains no bugs

**Input:** `$gs-team-qa feature: combat`

**Domain checks:**
- [ ] story-001 is never reported as missing its test, and its acceptance-criteria walk is its executed evidence
- [ ] The sign-off verdict is APPROVED, not NOT ASSESSED
- [ ] The UI story still needs its retained screenshot — `qa.level: minimal` waives tests, not the look
- [ ] Entry criteria at `feature:` scope read the story files' Status, not `production/sprint-status.yaml`
- [ ] No next step tells the user to write Logic tests

---

### Case 7: Smoke report NOT ASSESSED — continue with a warning, sign-off NOT ASSESSED

**Fixture:**
- Resolved config block: `team.size: small`, `automation: collaborative`, `qa.level: standard`
- `production/sprints/sprint-008.md` lists 2 stories: 1 Logic (its unit test exists and passes) and 1 Visual/Feel
- The most recent `production/qa/smoke-[date].md` report has verdict NOT ASSESSED — Batch 3 was offered and skipped
- `production/qa/bugs/` contains no bugs

**Input:** `$gs-team-qa sprint-8`

**Domain checks:**
- [ ] The NOT ASSESSED smoke verdict is taken from the report and shown with its source — not read as PASS or UNKNOWN
- [ ] The cycle does not stop at Phase 2 on NOT ASSESSED (only FAIL stops it)
- [ ] The sign-off verdict is NOT ASSESSED even though every story passed
- [ ] The next step names re-running `$gs-smoke-check` before `$gs-team-qa`

---

### Case 8: An open S1 already on file — known before sign-off, and the brief names no verdict

**Fixture:**
- Resolved config block: `team.size: small`, `automation: collaborative`, `qa.level: standard`
- `production/sprints/sprint-009.md` lists 2 stories in the Combat system: 1 Logic (its unit test passes) and 1 UI
- `production/qa/bugs/BUG-0004.md`: System Combat, `**Severity**: S1-Critical`, `**Status**: Open` — filed before this cycle; `BUG-0002.md` (Combat, S2) has `**Status**: Closed`
- The most recent `production/qa/smoke-[date].md` report has verdict PASS

**Input:** `$gs-team-qa sprint-9`

**Domain checks:**
- [ ] BUG-0004 is known from Phase 1 and appears in the Phase 2 strategy — not first discovered at sign-off, and never missed
- [ ] The sign-off verdict is NOT APPROVED although every story passed — never NOT ASSESSED or APPROVED
- [ ] The Phase 6 brief names no verdict and no deciding fact; the qa-lead reaches NOT APPROVED from the rules
- [ ] A closed bug is not counted as open


## Applicable domain checks

- [ ] Before professional work starts, resolve and announce team-size scope, parent coverage and any actual participants. At `team.size: individual`: qa-tester, with qa-lead expertise at the pipeline decision points. Name inactive perspectives and unassessed work accurately.
- [ ] Manual results are recorded only as the tester supplied them; unanswered stories remain unexecuted, and evidence never carries invented or pre-ticked sign-off.
- [ ] Absent smoke evidence is UNKNOWN, with the documented caution; UNKNOWN or NOT ASSESSED smoke prevents approval unless a known S1/S2 or unworked-around failure already requires NOT APPROVED.
- [ ] Each story has a named evidence destination; studio delegation may split stories when capacity permits, while small/individual uses grouped work. The parent path preserves the same story coverage.
- [ ] Sign-off drafting returns the assessment before writing, uses the evidence and verdict rules without a preselected verdict, and preserves all failures/blocks in the summary.
