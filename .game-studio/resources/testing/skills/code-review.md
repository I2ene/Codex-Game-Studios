# Evaluation scenarios: gs-code-review

Professional scenarios adapted from Donchitos' upstream testing guidance; see
[source attribution](../../../NOTICE.md). These are evaluation inputs and domain
checks, not executed results. Read `.agents/skills/gs-code-review/SKILL.md` and its current procedure first.
Use [evaluation policy](../README.md) and [category rubric](../quality-rubric.md).

Resolve current config and project engine records. Apply review-mode discipline
coverage without claiming automatic delegation: use the parent when needed, label it,
and record actual participants only. Existing human authorization governs writes;
case approvals represent unresolved decisions and never revoke prior authorization.
Historical fixture versions are scenario inputs, not current API verification.
The linked native procedure governs command arguments, output schemas, receipts,
context and mode applicability. Missing inputs remain NOT ASSESSED.

### Case 1: Happy Path — Standards-compliant file that follows its ADR

**Fixture:**
- `project.yaml`: `engine.name: godot`, `specialists.code: godot-gdscript-specialist`, `specialists.shader: null`, `specialists.ui: null`
- `src/gameplay/health_component.gd` meets all six Phase 4 checks:
  - Doc comments (`##`) on every public method and the class
  - Every method under cyclomatic complexity 10 and under 40 lines
  - Dependencies injected; no singletons
  - All tuning values loaded from `assets/data/`
  - Depends on interfaces, not concrete classes
- Header comment: `# Implements ADR-0004 (docs/architecture/adr-0004-health.md)`
- `docs/architecture/adr-0004-health.md` has `## Decision` and `## Consequences` sections, and the code follows the chosen approach
- The specialist reports no issues; there is nothing to suggest

**Input:** `$gs-code-review src/gameplay/health_component.gd`

**Domain checks:**
- [ ] The ADR is read with a heading map and bounded reads of `## Decision` and `## Consequences`, not an unbounded full read
- [ ] `godot-gdscript-specialist` is consulted for the `.gd` file; no agent named `null` is consulted
- [ ] Standards Compliance reads `6/6 passing` and ADR Compliance reads COMPLIANT
- [ ] Testability reads `N/A — no story path given`; no `qa-tester` is consulted without a story
- [ ] Positive Observations section is present
- [ ] Verdict is APPROVED and Phase 9 offers `$gs-story-done` or stop
- [ ] No file is written or edited

---

### Case 2: Changes Required — Missing doc comments and singleton usage, no ADR

**Fixture:**
- `project.yaml`: `engine.name: godot`, `specialists.code: godot-gdscript-specialist`
- `src/ui/inventory_ui.gd` has:
  - 2 public methods (`refresh_slots`, `sort_items`) without doc comments
  - `GameManager.instance` used at lines 42 and 87
  - All other standards met
- No ADR reference in the file header, and no commit touching it names an ADR
- No story path is passed

**Input:** `$gs-code-review src/ui/inventory_ui.gd`

**Domain checks:**
- [ ] The "No ADR references found" note names the story-path form of the command
- [ ] Missing doc comments are listed with method names (`refresh_slots`, `sort_items`), not only line references
- [ ] Singleton usage is flagged with file and line numbers (42, 87)
- [ ] Standards Compliance reads `4/6 passing`
- [ ] Verdict is CHANGES REQUIRED and Phase 9 offers the three CHANGES REQUIRED options
- [ ] Skill does not edit the file

---

### Case 3: Architectural Violation — Code uses a pattern its ADR rejects

**Fixture:**
- `project.yaml`: `engine.name: godot`, `specialists.code: godot-gdscript-specialist`
- `src/core/save_system.gd` header: `# Implements ADR-0010 (docs/architecture/adr-0010-save-format.md)`
- `adr-0010-save-format.md` `## Decision`: save data goes through `SaveService` as JSON; direct `FileAccess` writes from gameplay code are explicitly rejected
- `save_system.gd` writes save data with `FileAccess.open(..., FileAccess.WRITE)` directly at line 58
- Code otherwise meets all six standards checks

**Input:** `$gs-code-review src/core/save_system.gd`

**Domain checks:**
- [ ] The deviation is classified ARCHITECTURAL VIOLATION (BLOCKING), not ADR DRIFT or MINOR DEVIATION
- [ ] ADR Compliance reads VIOLATION and names ADR-0010
- [ ] The violation is listed under Required Changes
- [ ] Verdict is CHANGES REQUIRED
- [ ] Output says to comply with the existing ADR or revise it via `$gs-architecture-decision`, never to write a competing ADR

---

### Case 4: Edge Case — No source files at the specified path

**Fixture:**
- `project.yaml`: `engine.name: godot`
- `src/networking/` does not exist

**Input:** `$gs-code-review src/networking/`

**Domain checks:**
- [ ] Skill does not crash when the path does not exist
- [ ] Output names the attempted path `src/networking/`
- [ ] Verdict is `NOT ASSESSED — NO DATA`, not APPROVED
- [ ] No specialist agent is consulted when there is nothing to review

---

### Case 5: No Engine Configured — Skipped specialists announce themselves; no gate

**Fixture:**
- `project.yaml` has `modes.review_mode: full` and no `engine.name`; `.game-studio/resources/docs/technical-preferences.md` reads `[TO BE CONFIGURED]`
- `src/gameplay/loot_system.gd` hardcodes a drop rate `0.05` at line 31; everything else meets the standards

**Input:** `$gs-code-review src/gameplay/loot_system.gd`

**Domain checks:**
- [ ] Output contains the `Engine validation: NOT ASSESSED — no engine configured` line
- [ ] Engine Specialist Findings reads `N/A — no engine configured` and no engine specialist agent is consulted
- [ ] The hardcoded value is reported under Standards Compliance with its line reference
- [ ] Verdict is CHANGES REQUIRED, not NOT ASSESSED and never APPROVED
- [ ] No director gate is invoked, even with review mode `full`
- [ ] No code edits are made

---

### Case 5b: No Engine Configured, Clean File — NOT ASSESSED, never APPROVED

**Fixture:**
- `project.yaml` has no `engine.name`; `.game-studio/resources/docs/technical-preferences.md` reads `[TO BE CONFIGURED]`
- `src/gameplay/loot_table.gd` meets all six Phase 4 checks and raises no architecture, SOLID or game-specific concern

**Input:** `$gs-code-review src/gameplay/loot_table.gd`

**Domain checks:**
- [ ] Verdict is NOT ASSESSED, not APPROVED — a review that skipped the engine check has not approved the code
- [ ] The verdict names the engine specialist review as what did not run
- [ ] Phase 9 does not offer `$gs-story-done`; it names `$gs-setup-engine`

---

### Case 6: Referenced ADR missing — the section's NOT ASSESSED reaches the verdict

**Fixture:**
- `project.yaml`: `engine.name: godot`, `specialists.code: godot-gdscript-specialist`
- `src/gameplay/stamina.gd` meets all six Phase 4 checks and raises no
  architecture, SOLID or game-specific concern; the specialist reports it clean
- Its header reads `# Implements ADR-0008 (docs/architecture/adr-0008-stamina.md)`,
  and no such file exists

**Input:** `$gs-code-review src/gameplay/stamina.gd`

**Domain checks:**
- [ ] ADR Compliance reads NOT ASSESSED and names ADR-0008 — not `NO ADRS FOUND`, not COMPLIANT
- [ ] Verdict is NOT ASSESSED, never APPROVED: a section that could not be assessed reaches the verdict
- [ ] Variant — the file names no ADR at all: ADR Compliance reads `NO ADRS FOUND`, and the verdict is APPROVED (a missing reference is not an unreadable one)
