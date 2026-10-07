# Evaluation scenarios: gs-create-epics

Professional scenarios adapted from Donchitos' upstream testing guidance; see
[source attribution](../../../NOTICE.md). These are evaluation inputs and domain
checks, not executed results. Read `.agents/skills/gs-create-epics/SKILL.md` and its current procedure first.
Use [evaluation policy](../README.md) and [category rubric](../quality-rubric.md).

Resolve current config and project engine records. Apply review-mode discipline
coverage without claiming automatic delegation: use the parent when needed, label it,
and record actual participants only. Existing human authorization governs writes;
case approvals represent unresolved decisions and never revoke prior authorization.
Historical fixture versions are scenario inputs, not current API verification.
The linked native procedure governs command arguments, output schemas, receipts,
context and mode applicability. Missing inputs remain NOT ASSESSED.

### Case 1: Happy Path — Two approved GDDs create two epics

**Fixture:**
- `project.yaml`: `engine.name: Godot`, `modes.workflow: full`, `modes.review_mode: lean`
- `design/gdd/systems-index.md` lists 2 Foundation systems
- Both systems have Approved GDDs in `design/gdd/`, each with a `## Summary`
- `docs/architecture/architecture.md` has a module for each system
- Accepted ADRs cover every TR-ID for both systems in `docs/architecture/tr-registry.yaml`;
  the first system has two governing ADRs whose Engine Compatibility rates
  Knowledge Risk LOW and HIGH
- `docs/architecture/control-manifest.md` exists
- No `production/epics/` directory

**Input:** `$gs-create-epics layer: foundation`

**Domain checks:**
- [ ] Preserve the case's unresolved human decisions and declines; perform routine writes already authorized, and ask only for missing decisions or scope.
- [ ] Files land at `production/epics/[epic-slug]/EPIC.md`
- [ ] Each EPIC.md contains Layer, GDD path, Architecture Module, Governing ADRs table, GDD Requirements table, Definition of Done
- [ ] The first epic's Engine Risk is HIGH — the highest among its governing ADRs, not the first or the average
- [ ] The Definition of Done asks Logic and Integration stories for passing tests under `tests/` (the Godot test root) and Visual/Feel and UI stories for retained screenshots in `production/qa/evidence/` — each screen touched for UI, plus a lead sign-off for Visual/Feel
- [ ] "PR-EPIC skipped — Lean mode." appears; no producer is consulted
- [ ] `production/epics/index.md` is created or updated after writing, and only after an ask that named it
- [ ] Verdict is COMPLETE and names `$gs-create-stories [epic-slug]`

---

### Case 2: Failure Path — No system GDDs found

**Fixture:**
- `project.yaml`: `modes.workflow: full`
- `design/gdd/` contains only `game-concept.md` and `systems-index.md` (no
  system GDDs)

**Input:** `$gs-create-epics all`

**Domain checks:**
- [ ] `game-concept.md` and `systems-index.md` are not counted as system GDDs
- [ ] The "No system GDDs found … run `$gs-design-system` first" message is printed
- [ ] Preserve the case's unresolved human decisions and declines; perform routine writes already authorized, and ask only for missing decisions or scope.
- [ ] Verdict is BLOCKED (no eligible systems found), not COMPLETE

---

### Case 3: Director Gate — Full mode consults PR-EPIC before writing

**Fixture:**
- 2 Approved GDDs, architecture, ADRs, TR registry and control manifest as in Case 1
- `project.yaml`: `modes.workflow: full`, `modes.review_mode: full` — the workflow
  is pinned because an unset one resolves to `minimal`, where the skill reads the
  brief instead of the GDDs and the gate never comes into play
- PR-EPIC returns REALISTIC

**Input:** `$gs-create-epics layer: foundation`

**Full mode expected behavior:**
1. Both epics are presented and accepted via "Shall I create Epic: [name]?"
2. `producer` is consulted through available authorized delegation or explicitly labeled parent work with gate PR-EPIC, receiving the epic
   structure summary, the layer, milestone timeline and team capacity
3. On REALISTIC: the per-epic "May I write" asks proceed
4. Epic files are written after approval

**Assertions (full mode):**
- [ ] PR-EPIC is consulted once, after both epics are defined
- [ ] PR-EPIC runs before any "May I write" ask
- [ ] No EPIC.md is written before PR-EPIC resolves

**Fixture (per-run override):**
- Same project, `modes.workflow: full`, `modes.review_mode: full`
- Input: `$gs-create-epics layer: foundation --review lean`

**Override expected behavior:**
1. `--review lean` overrides the resolved `full`
2. PR-EPIC is skipped — noted in output
3. "May I write" asks proceed directly

**Assertions (override):**
- [ ] "PR-EPIC skipped — Lean mode." appears in output
- [ ] No producer agent is consulted and the write asks follow the epic definitions directly

**Domain checks:**
- [ ] PR-EPIC is consulted once, after both epics are defined
- [ ] Preserve the case's unresolved human decisions and declines; perform routine writes already authorized, and ask only for missing decisions or scope.
- [ ] "PR-EPIC skipped — Lean mode." appears in output
- [ ] No producer agent is consulted and the write asks follow the epic definitions directly

---

### Case 4: Edge Case — Untraced requirements at full workflow

**Fixture:**
- `project.yaml`: `modes.workflow: full`, `modes.review_mode: solo`
- One Approved Foundation GDD whose system has 5 TR-IDs in `tr-registry.yaml`;
  Accepted ADRs cover 3 of them (2 untraced)

**Input:** `$gs-create-epics [system-name]`

**Domain checks:**
- [ ] Coverage count and the 2 untraced TR-IDs are shown before the create ask
- [ ] The untraced-requirements warning names `$gs-architecture-decision` and says what actually happens downstream: the stories are written `Ready` with no governing ADR — it does not claim they will be Blocked
- [ ] Option `[C] Pause — I need to write ADRs first` is offered
- [ ] The written EPIC.md marks the untraced rows `❌ No ADR` (not silently dropped)

---

### Case 5: Director Gate — PR-EPIC returns CONCERNS

**Fixture:**
- 2 Approved GDDs, architecture, ADRs, TR registry and control manifest as in Case 1
- `project.yaml`: `modes.workflow: full`, `modes.review_mode: full`
- PR-EPIC returns CONCERNS (one epic's scope is too large)

**Input:** `$gs-create-epics layer: foundation`

**Domain checks:**
- [ ] Preserve the case's unresolved human decisions and declines; perform routine writes already authorized, and ask only for missing decisions or scope.
- [ ] Skill does NOT write epics while the gate is unresolved
- [ ] All three options ([A] proceed / [B] revise / [C] stop) are offered
- [ ] Choosing [B] re-presents the revised epics and re-runs PR-EPIC before any write ask
- [ ] Choosing [C] ends with Verdict: BLOCKED and no files written

---

### Case 6: Edge Case — An EPIC.md already exists for one system

**Fixture:**
- As Case 1 (`modes.workflow: full`, `modes.review_mode: lean`)
- `production/epics/[first-slug]/EPIC.md` already exists, with
  `**Stories**: 3 stories` in its header and a 3-row `## Stories` table;
  `production/epics/index.md` has its row with `3 stories`
- The second system has no EPIC.md

**Input:** `$gs-create-epics layer: foundation`

**Domain checks:**
- [ ] The existing file is detected before any write, and update / skip is offered — it is not overwritten
- [ ] After the update, the `**Stories**` header line and all 3 `## Stories` rows are unchanged
- [ ] The index has no duplicate row for the first epic and does not reset it to `Not yet created`
- [ ] Preserve the case's unresolved human decisions and declines; perform routine writes already authorized, and ask only for missing decisions or scope.

---

### Case 7: Standard tier — GDDs without `## Summary`, one untraced non-critical requirement

**Fixture:**
- `project.yaml`: `modes.workflow: standard`, `modes.review_mode: solo`
- `design/gdd/systems-index.md` lists one Foundation and one Core system; both
  GDDs predate `## Summary` (the Summary scan matches none of them)
- `docs/architecture/architecture.md` has a module for each system, and
  `docs/architecture/tr-registry.yaml` holds both systems' TR-IDs
- The Foundation system's TR-IDs are covered by an Accepted Foundation-layer ADR;
  one of the Core system's TR-IDs has no ADR
- `docs/architecture/control-manifest.md` does not exist

**Input:** `$gs-create-epics all`

**Domain checks:**
- [ ] A zero-match Summary scan is reported as such and both systems stay in scope — it is not read as "nothing in scope"
- [ ] The missing control manifest does not stop the run at `standard`
- [ ] The untraced non-critical requirement is listed, but the ⚠️ warning is not emitted
- [ ] Preserve the case's unresolved human decisions and declines; perform routine writes already authorized, and ask only for missing decisions or scope.
