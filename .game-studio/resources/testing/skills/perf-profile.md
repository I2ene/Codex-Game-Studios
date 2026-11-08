# Evaluation scenarios: gs-perf-profile

Professional scenarios adapted from Donchitos' upstream testing guidance; see
[source attribution](../../../NOTICE.md). These are evaluation inputs and domain
checks, not executed results. Read `.agents/skills/gs-perf-profile/SKILL.md` and its current procedure first.
Use [evaluation policy](../README.md) and [category rubric](../quality-rubric.md).

Resolve current config and project engine records. Apply review-mode discipline
coverage without claiming automatic delegation: use the parent when needed, label it,
and record actual participants only. Existing human authorization governs writes;
case approvals represent unresolved decisions and never revoke prior authorization.
Historical fixture versions are scenario inputs, not current API verification.
The linked native procedure governs command arguments, output schemas, receipts,
context and mode applicability. Missing inputs remain NOT ASSESSED.

### Case 1: Happy Path — Budgets committed, combat hotspots found

**Fixture:**
- `project.yaml`: `engine.name: godot`, `performance.target_framerate: 60`,
  `performance.frame_budget_ms: 16.6`, `performance.draw_call_limit: 200`,
  `performance.memory_ceiling_mb: 2048`; `performance.enforce` unset (resolves
  to `warn`); `modes.automation` unset (collaborative)
- No config key, design doc or `AGENTS.md` section states a load-time target
- `src/gameplay/combat/enemy_manager.gd` has a `_process()` that loops over every
  enemy and, inside that loop, over every active projectile, and casts a ray per
  enemy every frame
- Reworking the nested loop into a spatial partition is a multi-day change

**Input:** `$gs-perf-profile combat`

**Domain checks:**
- [ ] Budgets come from the four `performance.*` keys read with `get_effective_yaml_key`, not from design docs or a hardcoded 16.67 ms
- [ ] The nested loop and the per-frame raycast are reported as hotspots with a `file:line` location
- [ ] Each optimization recommendation states location, expected gain, risk and approach
- [ ] The frame time, memory and draw call rows carry an OK / WARNING / OVER status; the Load time row is `NOT ASSESSED`, not OK
- [ ] No headroom is claimed for load time; the summary says `no budget set — headroom not assessed`
- [ ] Preserve the case's unresolved human decisions and declines; perform routine writes already authorized, and ask only for missing decisions or scope.
- [ ] The M/L-effort hotspot triggers the Phase 5 choice (implement / `$gs-scope-check` / defer to Polish / `$gs-architecture-decision`)
- [ ] Verdict is COMPLETE

---

### Case 2: No Committed Budget — Budget rows are NOT ASSESSED

**Fixture:**
- `project.yaml` has `engine.name: godot` and no `performance` block
- No design doc and no `AGENTS.md` section states a frame-rate, memory, load-time or draw-call target
- `src/` contains gameplay scripts with `_process()` functions

**Input:** `$gs-perf-profile full`

**Domain checks:**
- [ ] No budget row shows OK, WARNING or OVER; each is `NOT ASSESSED`
- [ ] The `[16.67ms]` placeholder is never used as a budget, and no headroom figure is claimed
- [ ] Hotspot analysis still runs and is reported
- [ ] The `NOT ASSESSED` rows are kept in the report offered for writing, not edited out

---

### Case 3: Nothing to Profile — Whole verdict NOT ASSESSED — NO DATA

**Fixture:**
- Fresh project: `project.yaml` has `engine.name: godot` and no `performance` block, and the code root `src/` is absent
- No design docs exist
- No profiler output exists anywhere

**Input:** `$gs-perf-profile full`

**Domain checks:**
- [ ] Each input is recorded as FOUND or ABSENT, not assumed present
- [ ] The whole verdict is `NOT ASSESSED — NO DATA`, not COMPLETE
- [ ] Output names each missing input and which skill produces it
- [ ] Preserve the case's unresolved human decisions and declines; perform routine writes already authorized, and ask only for missing decisions or scope.

---

### Case 4: Local Enforcement Override `block` — Violations are blockers

**Fixture:**
- `project.yaml`: `engine.name: godot`, `performance.enforce: warn`, `performance.draw_call_limit: 200`, the other three budgets set
- `project.local.yaml`: `performance.enforce: block`, so the resolved block at the top of the skill shows `block`
- `src/levels/forest/forest_builder.gd` instantiates 600 individual foliage `MeshInstance3D` nodes, each with its own material and no instancing
- `modes.automation` unset (collaborative)

**Input:** `$gs-perf-profile forest`

**Domain checks:**
- [ ] The local `block` applies, not the committed `warn` — `performance.enforce` comes from the resolved block
- [ ] The Draw calls row is OVER against the 200 budget
- [ ] The report states the violation is a blocker and that `$gs-gate-check` will FAIL the Polish gate on it
- [ ] Preserve the case's unresolved human decisions and declines; perform routine writes already authorized, and ask only for missing decisions or scope.

---

### Case 5: Enforcement Level `off` in Full Review Mode — Informational only, no gates

**Fixture:**
- Explicit standard workflow; this fixture exercises sprint scheduling rather than the minimal route in Case 6.
- `project.yaml`: `engine.name: godot`, `modes.review_mode: full`, `performance.enforce: off`, all four budgets set
- `src/` contains a `_process()` whose estimated frame cost exceeds `performance.frame_budget_ms`

**Input:** `$gs-perf-profile full`

**Domain checks:**
- [ ] No director gate is invoked in any review mode
- [ ] The estimated frame time still appears in the budget table
- [ ] The over-budget metric is not raised as a violation finding or a fix recommendation
- [ ] Preserve the case's unresolved human decisions and declines; perform routine writes already authorized, and ask only for missing decisions or scope.
- [ ] Next steps name `$gs-architecture-decision`, `$gs-scope-check` and `$gs-sprint-plan update`

---

### Case 6: Accepted optimization follows workflow

**Fixture:** As Case 1, with the nested-loop optimization rated M/L and the operator choosing to implement
it. Run A: minimal workflow; Run B: explicit standard.

**Input:** `$gs-perf-profile combat`

**Domain checks:**
- [ ] A: the implementation option and scheduling handoff name the brief's build order; neither
  schedules a sprint.
- [ ] B: offer to fix now or schedule via `$gs-sprint-plan update`, without the minimal
  build-order wording.
- [ ] Preserve the scope-check, Polish deferral and ADR alternatives. Both runs end COMPLETE
  with the same performance evidence limits.

---

### Case 7: Subdirectory invocation resolves root budgets

**Fixture:** Start in `src/gameplay/`. Root config sets Godot and target 60 fps, 16.6 ms frame, 200 draw
calls and 2048 MB. `src/gameplay/combat/enemy_manager.gd` has a nested loop in `_process()`.

**Input:** `$gs-perf-profile combat`

**Domain checks:**
- [ ] Resolve the actual project root and effective config there. The budgets table shows the
  four committed values; working directory alone never makes them unset or NOT ASSESSED.
- [ ] Find the nested loop with a file and line. Estimated code cost is not an executed timing
  measurement.
