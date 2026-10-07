# Evaluation scenarios: gs-architecture-review

Professional scenarios adapted from Donchitos' upstream testing guidance; see
[source attribution](../../../NOTICE.md). These are evaluation inputs and domain
checks, not executed results. Read `.agents/skills/gs-architecture-review/SKILL.md` and its current procedure first.
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

### Case 1: Happy Path — every requirement covered by an Accepted ADR

**Fixture:**
- `project.yaml` sets `modes.workflow: full`, `engine.name: Godot`, `engine.version: 4.6`
- `design/gdd/systems-index.md` plus two system GDDs (`combat.md`, `inventory.md`),
  each with a `## Summary` and technical requirements in its Detailed Rules
- `docs/architecture/adr-0001-*.md` … `adr-0003-*.md`, each with `## Status: Accepted`,
  `## GDD Requirements Addressed`, `## Engine Compatibility` and `## ADR Dependencies`,
  whose `**Depends On**` row is filled in — `None` for `adr-0001`, `ADR-0001` for
  `adr-0002` and `adr-0003` — so `<runtime> dependencies` finds real edges and lists no
  ADR under the native missing-dependency-declaration list; together they cover every requirement; no two contradict
- `docs/architecture/architecture.md` exists and names every system in the index
- No prior `docs/architecture/architecture-review-*.md` report
- Pre-gate items all exist: `tests/unit/`, `tests/integration/` (the Godot test root),
  `.github/workflows/tests.yml`, `design/accessibility-requirements.md`,
  `design/ux/interaction-patterns.md`

**Input:** `$gs-architecture-review`

**Domain checks:**
- [ ] Output reports "Loaded [N] GDDs, [M] ADRs, engine: [name + version]"
- [ ] A Traceability Matrix lists each TR-ID with its GDD, system, requirement, ADR coverage and status; every row is ✅
- [ ] The ADR dependency order comes from `<runtime> dependencies`, not hand-tracing, and puts `adr-0001` first; the native missing-dependency-declaration list is empty, so the acyclic result is a clean graph rather than a structural gap
- [ ] Verdict is PASS only because all requirements are covered by **Accepted** ADRs, no conflicts exist, and engine references agree
- [ ] The actual report has a linked SHA-256 JSON companion covering reviewed ADRs, GDDs and required context
- [ ] Preserve the case's unresolved human decisions and declines; perform routine writes already authorized, and ask only for missing decisions or scope.
- [ ] The closing widget offers `$gs-gate-check pre-production`, because every pre-gate checklist item is ✅

---

### Case 2: Failure Path — Foundation gap plus a cross-ADR ownership conflict

**Fixture:**
- As Case 1, except:
  - `save-system.md` (a Foundation-layer system) requires "Player progress
    persists between sessions" and no ADR addresses it
  - `adr-0002` and `adr-0004` are both Accepted and both claim authority over the
    player's health value

**Input:** `$gs-architecture-review`

**Domain checks:**
- [ ] Verdict is FAIL (a Foundation-layer requirement is uncovered)
- [ ] The gap row names the TR-ID, GDD and requirement, with a suggested `$gs-architecture-decision` command
- [ ] The conflict block names both ADR numbers, a Type (State / Data ownership), what each ADR claims, the Impact, and at least two resolution options
- [ ] Skill does NOT auto-resolve the conflict or edit either ADR
- [ ] If `docs/consistency-failures.md` exists, the Phase 8 `[A]` option names it ("…and append 1 conflict entry to `docs/consistency-failures.md`") and the entry is appended only when the user picks `[A]`; `[B]` (report only) writes the report and nothing else; if the file does not exist, it is not created
- [ ] The closing widget does not offer `$gs-gate-check`; it offers writing the missing ADR via `$gs-architecture-decision [system]`

---

### Case 3: Partial Path — coverage resting on a Proposed ADR

**Fixture:**
- As Case 1, except `adr-0003` (the only ADR covering `TR-inventory-001`) has `## Status: Proposed`
- `adr-0004` (Accepted) has `**Depends On**: ADR-0003` in its `## ADR Dependencies` table

**Input:** `$gs-architecture-review`

**Domain checks:**
- [ ] Skill reads each ADR's `## Status` before marking coverage; a Proposed ADR never yields ✅
- [ ] Verdict is CONCERNS (not PASS) when coverage rests on a Proposed ADR
- [ ] Output names `$gs-architecture-decision accept ADR-0003` as the route to clear it
- [ ] The unresolved dependency on a Proposed ADR is flagged

---

### Case 4: Edge Case — missing architecture document; malformed ADRs

**Case 4a — no master architecture document:**
- As Case 1, but `docs/architecture/architecture.md` does not exist

**Assertions (4a):**
- [ ] The report states `Architecture document coverage: NOT ASSESSED — no docs/architecture/architecture.md` as a named line item, rather than showing no Phase 6 findings
- [ ] The overall verdict is NOT ASSESSED, not PASS: Phase 6 is part of the `full` scope and did not run, even though every requirement is covered (a CONCERNS or FAIL finding elsewhere would still outrank it)

**Case 4b — ADRs present but none has a scannable section:**
- As Case 1 (`modes.workflow: full` — at the default `minimal` tier, a `project.yaml` with no `modes` block,
  the skill does not apply), except the three `docs/architecture/adr-*.md` files
  carry none of the six headings the Phase 1b scan looks for: `## Status`,
  `## Decision`, `## GDD Requirements Addressed`, `## Engine Compatibility`,
  `## ADR Dependencies`, `## Performance Implications`

**Assertions (4b):**
- [ ] Skill reports "[N] ADRs found, none carries a scannable section — run `$gs-architecture-decision retrofit [file]` on each" (subcommand first — with the path first, `$gs-architecture-decision` would start authoring a new ADR instead)
- [ ] Skill does NOT report zero coverage or a design failure — it is a format failure
- [ ] Rows whose ADR has no `## Status` are `❓ Not assessed`, and the verdict is not PASS — nor FAIL on coverage grounds, since coverage is unknown rather than absent

**Domain checks:**
- [ ] The report states `Architecture document coverage: NOT ASSESSED — no docs/architecture/architecture.md` as a named line item, rather than showing no Phase 6 findings
- [ ] The overall verdict is NOT ASSESSED, not PASS: Phase 6 is part of the `full` scope and did not run, even though every requirement is covered (a CONCERNS or FAIL finding elsewhere would still outrank it)
- [ ] Skill reports "[N] ADRs found, none carries a scannable section — run `$gs-architecture-decision retrofit [file]` on each" (subcommand first — with the path first, `$gs-architecture-decision` would start authoring a new ADR instead)
- [ ] Skill does NOT report zero coverage or a design failure — it is a format failure
- [ ] Rows whose ADR has no `## Status` are `❓ Not assessed`, and the verdict is not PASS — nor FAIL on coverage grounds, since coverage is unknown rather than absent

---

### Case 5: Engine specialist consultation — configured vs unconfigured engine
**Case 5a — engine configured:** Case 1 fixture (`engine.name: Godot`)

**Domain checks (5a):**
- [ ] The specialist is resolved from `engine.name` (Godot → `godot-specialist`)
- [ ] It is consulted after the engine audit, with the audit findings in its prompt
- [ ] Output includes an `### Engine Specialist Findings` section
- [ ] No director gate (TD-ARCHITECTURE, LP-FEASIBILITY or any other gate ID) is consulted or mentioned

**Case 5b — no engine configured:** as Case 1, except `engine.name` is unset in `project.yaml` and `technical-preferences.md` is still `[TO BE CONFIGURED]`

**Domain checks (5b):**
- [ ] No engine specialist is consulted
- [ ] Output records `Engine validation: NOT ASSESSED — no engine configured` rather than omitting the step
- [ ] The verdict is NOT ASSESSED, not PASS — the engine audit is part of the `full` scope and had no pinned engine to check against, even though every requirement is covered

---


## Applicable domain checks

- [ ] Reuse existing TR-registry IDs; never renumber or delete entries. Deprecation is an explicit human decision.
