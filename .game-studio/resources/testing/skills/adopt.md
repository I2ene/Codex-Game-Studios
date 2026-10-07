# Evaluation scenarios: gs-adopt

Professional scenarios adapted from Donchitos' upstream testing guidance; see
[source attribution](../../../NOTICE.md). These are evaluation inputs and domain
checks, not executed results. Read `.agents/skills/gs-adopt/SKILL.md` and its current procedure first.
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

### Case 1: Happy Path — All GDDs compliant, no BLOCKING or HIGH gaps

**Fixture:**
- `project.yaml` sets `modes.rigor: full`, `project.stage`, and `engine.name`,
  `engine.version`, `engine.language`, `engine.rendering`, `engine.physics`
- `design/gdd/` contains 3 GDD files; each has all 8 required sections with content
  and a valid `> **Status**:` field
- `docs/architecture/adr-0001.md` exists with `## Status`, `## ADR Dependencies`,
  `## Engine Compatibility`, `## GDD Requirements Addressed` and `## Performance Implications`
- `docs/architecture/tr-registry.yaml` and `docs/architecture/control-manifest.md` exist
- `<project-engine-reference>/[engine]/VERSION.md` exists

**Input:** `$gs-adopt`

**Domain checks:**
- [ ] Skill reads silently before presenting any output
- [ ] "Scanning project artifacts..." appears before the silent read phase
- [ ] `<runtime> gdd-structure` is invoked with an explicit path per GDD (not bare)
- [ ] Gap counts show `BLOCKING: 0` and `HIGH: 0`, and the project is reported template-compatible
- [ ] Preserve the case's unresolved human decisions and declines; perform routine writes already authorized, and ask only for missing decisions or scope.
- [ ] Adoption plan file is written to `docs/adoption-plan-[date].md`
- [ ] `modes.review_mode` is not written to `project.yaml` and `production/review-mode.txt` is not created — the review mode is reported, never pinned
- [ ] Phase 7 asks "No blocking gaps — this project is template-compatible. What next?" via `host input tool`

---

### Case 2: Non-Compliant Documents — GDDs missing sections, BLOCKING and HIGH gaps

**Fixture:**
- `project.yaml` sets `modes.rigor: full` and configures the engine
- `design/gdd/` contains 2 GDD files:
  - `combat.md` — missing `## Acceptance Criteria` and `## Formulas` sections
  - `movement.md` — all 8 sections present
- One ADR (`adr-0001.md`) is missing `## Status` section
- `docs/architecture/tr-registry.yaml` does not exist

**Input:** `$gs-adopt`

**Domain checks:**
- [ ] BLOCKING gaps are listed as explicit file-name bullets in the Gap Preview
- [ ] HIGH and MEDIUM shown as counts in Gap Preview
- [ ] Migration plan items are in BLOCKING-first order
- [ ] Each plan item includes the fix command or manual steps
- [ ] Preserve the case's unresolved human decisions and declines; perform routine writes already authorized, and ask only for missing decisions or scope.
- [ ] Phase 7 offers to immediately retrofit the first BLOCKING item

---

### Case 3: Mixed State — Some docs compliant, some not, partial report

**Fixture:**
- `project.yaml` sets `modes.rigor: full` and configures engine, naming and performance
- 4 GDD files: 2 fully compliant, 2 with gaps (one missing Tuning Knobs, one missing Formulas)
- ADRs: 3 files — 2 compliant, 1 missing `## ADR Dependencies`
- Stories: 5 files — 3 have TR-ID references, 2 do not
- Infrastructure: all critical files present

**Input:** `$gs-adopt`

**Domain checks:**
- [ ] Summary shows GDD and ADR tallies as `N (X fully compliant, Y with gaps)` and `Stories audited: 5`
- [ ] Summary shows `BLOCKING: 0` and the Gap Preview lists no BLOCKING bullets
- [ ] The 2 stories without TR-IDs are counted as MEDIUM gaps
- [ ] Existing story compatibility note is included in the plan
- [ ] HIGH gap precedes MEDIUM gaps; MEDIUM GDD gaps precede MEDIUM story gaps
- [ ] Preserve the case's unresolved human decisions and declines; perform routine writes already authorized, and ask only for missing decisions or scope.

---

### Case 4: No Artifacts Found — Fresh project, guidance to run $gs-start

**Fixture:**
- Repository has no files in `design/gdd/`, `docs/architecture/`, `production/epics/`
- No `project.stage` in `project.yaml` and no `production/stage.txt`
- No source code: none of `src/`, `Assets/` or `Source/` exists
- No game-concept.md, no game-brief.md, no systems-index.md

**Input:** `$gs-adopt`

**Domain checks:**
- [ ] `host input tool` is used (not a plain text message) when no artifacts are found
- [ ] `$gs-start` is presented as a named option
- [ ] Skill stops after the question — no audit phases run
- [ ] No adoption plan file is written

---

### Case 5: Director Gate Check — No gate; minimal tier scopes the audit to the brief

**Fixture:**
- `project.yaml` configures the engine and has no `modes` block (`workflow`
  resolves to `minimal`)
- `design/game-brief.md` exists
- `design/gdd/combat.md` exists and is missing `## Acceptance Criteria`

**Input:** `$gs-adopt`

**Domain checks:**
- [ ] `design/game-brief.md` is audited
- [ ] Absent ADRs and UX specs are not reported as gaps
- [ ] `combat.md`'s missing Acceptance Criteria is not counted in the HIGH total
- [ ] The plan prescribes none of `$gs-architecture-review`, `$gs-create-control-manifest`, `$gs-sprint-plan` or `$gs-gate-check` — none is on the minimal path
- [ ] No director gate is invoked and no gate skip messages appear
- [ ] Skill reaches plan-writing or cancellation without any gate verdict

---

### Case 6: v1.0 Project — Converter run, never hand-migrated

**Fixture:**
- No `project.yaml` at the repo root
- `production/stage.txt` reads `Production`; `.game-studio/resources/docs/technical-preferences.md`
  has `- **Engine**: Godot 4.6` and a filled naming section
- `design/gdd/` holds GDDs; no `production/migration-report.md`

**Input:** `$gs-adopt`

**Domain checks:**
- [ ] `--dry-run` runs before any real migration, and its output is reported
- [ ] `project.yaml` is written only by the converter, after the ask naming `project.yaml` and `production/migration-report.md` is approved
- [ ] `--finalize` is not run before the user has read `production/migration-report.md`
- [ ] The migration is a BLOCKING item, first in the plan
- [ ] No legacy file is deleted during the run
