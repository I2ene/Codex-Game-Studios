# Evaluation scenarios: gs-project-stage-detect

Professional scenarios adapted from Donchitos' upstream testing guidance; see
[source attribution](../../../NOTICE.md). These are evaluation inputs and domain
checks, not executed results. Read `.agents/skills/gs-project-stage-detect/SKILL.md` and its current procedure first.
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

### Case 1: Configured Stage Matches the Artifacts

**Fixture:**
- `project.yaml` has `project.stage: Production` and `engine.name: Godot`
- `src/` has 24 source files; `design/gdd/` has 4 GDDs and `systems-index.md`,
  one GDD per indexed system
- `docs/architecture/` has `architecture.md` and 5 ADRs; `design/art/art-bible.md`
  and the UX specs exist; `tests/unit/` holds tests for each system — no doc type
  the `full` tier flags is missing, so there is no gap to weigh
- `production/sprints/sprint-002.md` exists
- Resolved workflow tier: `full`

**Input:** `$gs-project-stage-detect`

**Domain checks:**
- [ ] `<runtime> artifacts` is run as the first scan step
- [ ] Detected stage is Production, and the heuristic result is reported alongside the configured one
- [ ] Stage Confidence is PASS
- [ ] Preserve the case's unresolved human decisions and declines; perform routine writes already authorized, and ask only for missing decisions or scope.
- [ ] Neither `project.yaml` nor `production/stage.txt` is modified

---

### Case 2: No Configured Stage — Inferred From Artifacts, Role Filter Applied

**Fixture:**
- No `project.stage` in `project.yaml` and no `production/stage.txt`
- `engine.name: Godot`; `src/` has 14 source files
- `design/gdd/` has 3 GDDs; `docs/architecture/` has no ADRs
- Resolved workflow tier: `full`

**Input:** `$gs-project-stage-detect programmer`

**Domain checks:**
- [ ] Inferred stage is Production, based on the 10+ source-file rule
- [ ] Recommendations focus on architecture docs, tests and ADRs for the programmer role
- [ ] The ADR gap is phrased with a clarifying question, not only listed
- [ ] No stage value is written to `project.yaml` or `production/stage.txt`

---

### Case 3: Configured Stage Contradicted by the Artifacts

**Fixture:**
- `project.yaml` has `project.stage: Release`
- `engine.name: Godot`; `src/` has 2 source files; no ADRs, no architecture
  doc, no epics
- Resolved workflow tier: `full`

**Input:** `$gs-project-stage-detect`

**Domain checks:**
- [ ] Output names both the configured stage (Release) and the observed stage (Pre-Production)
- [ ] The disagreement is stated explicitly
- [ ] Stage Confidence is CONCERNS (ambiguous signals), or FAIL if critical gaps are also found — never PASS
- [ ] The configured stage is neither silently overridden nor rewritten in any file

---

### Case 4: Minimal Workflow Tier — Absent Docs Are Not Gaps

**Fixture:**
- Resolved workflow tier: `minimal`
- `project.yaml` has `project.stage: Concept`, as `$gs-start` wrote it — nothing on
  the minimal path runs `$gs-gate-check`, so it has never advanced
- `design/game-brief.md` exists; `engine.name: Godot`; `src/` has 5 source files
- No GDDs, no art bible, no ADRs, no epics, no sprint plans

**Input:** `$gs-project-stage-detect`

**Domain checks:**
- [ ] No absent GDD, art bible, ADR, epic or sprint plan is listed as a gap
- [ ] `$gs-reverse-document` and `$gs-sprint-plan` are not suggested
- [ ] The Production completeness line refers to the brief's build order
- [ ] The configured Concept stage is not reported as a disagreement with the observed stage
- [ ] Preserve the case's unresolved human decisions and declines; perform routine writes already authorized, and ask only for missing decisions or scope.

---

### Case 5: Director Gate Check — None; Declined Write Leaves No File

**Fixture:**
- Any project state
- Any review mode
- User declines the "May I write" ask

**Input:** `$gs-project-stage-detect`

**Domain checks:**
- [ ] No director gate is invoked and no gate skip message appears
- [ ] No subagent is consulted
- [ ] The summary is shown before the write ask
- [ ] After a decline, `production/project-stage-report.md` is not created

---

### Case 6: Unresolved Code Root — NOT ASSESSED, not a greenfield project

**Fixture:**
- No `project.stage`, no `production/stage.txt`
- `project.yaml` has no `engine.name`; `.game-studio/resources/docs/technical-preferences.md`
  reads `[TO BE CONFIGURED]`
- Both `src/` and `Assets/` exist, each holding source files (ambiguous tree)
- `design/gdd/game-concept.md` and `design/gdd/systems-index.md` exist, with a
  GDD for every indexed system; `docs/architecture/` holds the Foundation-layer
  ADRs — nothing the `standard` tier flags is missing
- Resolved workflow tier: `standard`

**Input:** `$gs-project-stage-detect`

**Domain checks:**
- [ ] No source-file count of zero is reported; the Source Code line is `NOT ASSESSED — code root unresolved`
- [ ] The code root is not assumed to be `src/`
- [ ] Stage Confidence is NOT ASSESSED and names the check that did not run — not PASS
- [ ] Preserve the case's unresolved human decisions and declines; perform routine writes already authorized, and ask only for missing decisions or scope.
