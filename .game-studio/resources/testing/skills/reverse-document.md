# Evaluation scenarios: gs-reverse-document

Professional scenarios adapted from Donchitos' upstream testing guidance; see
[source attribution](../../../../NOTICE.md). These are evaluation inputs and domain
checks, not executed results. Read `.agents/skills/gs-reverse-document/SKILL.md` and its current procedure first.
Use [evaluation policy](../README.md) and [category rubric](../quality-rubric.md).

Resolve current config and project engine records. Apply review-mode discipline
coverage without claiming automatic delegation: use the parent when needed, label it,
and record actual participants only. Existing human authorization governs writes;
case approvals represent unresolved decisions and never revoke prior authorization.
Historical fixture versions are scenario inputs, not current API verification.
The linked native procedure governs command arguments, output schemas, receipts,
context and mode applicability. Missing inputs remain NOT ASSESSED.

### Case 1: Well-Structured Source at `full` — 8-section GDD produced

**Fixture:**
- `project.yaml` resolves `workflow: full`; no `system_overrides` row for health
- `src/gameplay/health_system.gd` exists (~80 lines) with:
  - `@export var max_health: int = 100`
  - `func take_damage(amount: int)` containing
    `health = clamp(health - amount, 0, max_health)`
  - `signal health_changed(new_value: int)`
  - Docstrings on all public methods
- The user answers every `UNCLEAR INTENT AREAS` question and approves the write

**Input:** `$gs-reverse-document design src/gameplay/health_system.gd`

**Domain checks:**
- [ ] Findings are presented and answered before any draft is shown
- [ ] All 8 GDD sections are present (tier resolved as `full`)
- [ ] The clamp expression appears in Formulas; `max_health = 100` appears as a Tuning Knob
- [ ] The provenance banner appears directly under the title
- [ ] Preserve the case's unresolved human decisions and declines; perform routine writes already authorized, and ask only for missing decisions or scope.
- [ ] Verdict is COMPLETE

---

### Case 2: Unanswered Intent — INTENT UNKNOWN carried into the draft

**Fixture:**
- `project.yaml` resolves `workflow: full`
- `src/gameplay/enemy_ai.gd` exists (~120 lines) with:
  - A patrol/chase/attack state machine
  - Inline constants with use sites: `if distance < 150:`, `speed = 3.5`
  - No arithmetic expression that computes a gameplay value from inputs
  - No comments or docstrings
- The user replies "just draft it" without answering the intent questions, then
  approves the write

**Input:** `$gs-reverse-document design src/gameplay/enemy_ai.gd`

**Domain checks:**
- [ ] `FORMULAS DISCOVERED` reads `none found in the source` (heading kept, not omitted)
- [ ] Each unanswered question appears in the document marked `INTENT UNKNOWN — inferred from implementation, not confirmed`
- [ ] No formula or design intent absent from the code appears in the draft
- [ ] Preserve the case's unresolved human decisions and declines; perform routine writes already authorized, and ask only for missing decisions or scope.
- [ ] Verdict is COMPLETE

---

### Case 3: Architecture Type on Interdependent Files — tier-independent ADR

**Fixture:**
- `project.yaml` resolves `workflow: minimal`
- `src/core/combat/` holds `combat_system.gd` and `damage_resolver.gd`;
  `combat_system.gd` calls `damage_resolver.gd` through an injected reference
- The user answers the architecture questions and approves the write

**Input:** `$gs-reverse-document architecture src/core/combat/`

**Domain checks:**
- [ ] Both files are analyzed, and the combat_system → damage_resolver dependency is documented
- [ ] Output is an ADR at `docs/architecture/`, not `design/gdd/` or a `-brief.md`
- [ ] The `minimal` tier does not change the architecture output
- [ ] Verdict is COMPLETE

---

### Case 4: Thin Source — Sufficiency check stops the run

**Fixture:**
- `src/gameplay/inventory_system.gd` exists with only
  `class_name InventorySystem`, `extends Node` and an empty `_ready()` —
  no mechanics, no formulas, no tuning values (under 20 non-boilerplate lines)

**Input:** `$gs-reverse-document design src/gameplay/inventory_system.gd`

**Domain checks:**
- [ ] The stop message names the path and the three counts (all 0)
- [ ] `$gs-design-system` is suggested — not a fabricated skeleton
- [ ] No write tool is called
- [ ] No verdict is issued (the run stops before Phase 4)

---

### Case 5: Director Gate Check — No gate; declined write is BLOCKED

**Fixture:**
- Same source as Case 1; the user declines at the "May I write" prompt

**Input:** `$gs-reverse-document design src/gameplay/health_system.gd`

**Domain checks:**
- [ ] No director gate is invoked
- [ ] No gate skip messages appear
- [ ] Verdict is BLOCKED (user declined write) — no gate verdict involved

---

### Case 6: Default Tier — a single system becomes a one-page brief

**Fixture:**
- `project.yaml` sets no `modes.rigor` and no `modes.workflow`, so the resolved
  tier is `minimal` — the default; no `system_overrides`
- Same source as Case 1 (`src/gameplay/health_system.gd`)
- The user answers every `UNCLEAR INTENT AREAS` question and approves the write

**Input:** `$gs-reverse-document design src/gameplay/health_system.gd`

**Domain checks:**
- [ ] The output is a brief in the game-brief format, not an 8- or 5-section GDD
- [ ] The path is `design/[system-name]-brief.md`
- [ ] The provenance banner appears under the title
- [ ] Verdict is COMPLETE
