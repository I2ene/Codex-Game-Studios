# Evaluation scenarios: gs-estimate

Professional scenarios adapted from Donchitos' upstream testing guidance; see
[source attribution](../../../../NOTICE.md). These are evaluation inputs and domain
checks, not executed results. Read `.agents/skills/gs-estimate/SKILL.md` and its current procedure first.
Use [evaluation policy](../README.md) and [category rubric](../quality-rubric.md).

Resolve current config and project engine records. Apply review-mode discipline
coverage without claiming automatic delegation: use the parent when needed, label it,
and record actual participants only. Existing human authorization governs writes;
case approvals represent unresolved decisions and never revoke prior authorization.
Historical fixture versions are scenario inputs, not current API verification.
The linked native procedure governs command arguments, output schemas, receipts,
context and mode applicability. Missing inputs remain NOT ASSESSED.

### Case 1: Happy Path — Clear task in a documented system with existing patterns

**Fixture:**
- `project.yaml`: `engine.name: godot`, so the code root is `src/`
- `design/gdd/combat.md` documents melee hit detection
- `src/combat/` holds the melee attack code; similar collision code already exists there
- `production/sprints/sprint-003.md` through `sprint-005.md` record completed combat tasks

**Input:** `$gs-estimate Add hitbox detection to melee attacks`

**Domain checks:**
- [ ] The combat GDD and the sprint history are read before the estimate is produced
- [ ] Effort is given as three day figures (Optimistic, Expected, Pessimistic), not a single number
- [ ] Recommended budget equals the Expected figure, not the Optimistic one
- [ ] Figures are rounded to half days, not hours
- [ ] The closing summary names budget, confidence and the biggest risk
- [ ] No files are written

---

### Case 2: High Uncertainty — New subsystem, no architecture decided

**Fixture:**
- `project.yaml`: `engine.name: godot`
- `src/` holds no source files for an online or matchmaking subsystem
- `design/gdd/online.md` describes the lobby with open "TBD" requirements, and says the networking approach (transport, host model) is not yet decided

**Input:** `$gs-estimate Implement online lobby matchmaking`

**Domain checks:**
- [ ] Confidence is Low when the task has an undecided approach, no existing code and TBD requirements
- [ ] The Risk Factors table names the specific unknowns driving the uncertainty
- [ ] Output recommends a time-boxed `$gs-prototype` spike before committing
- [ ] No files are written

---

### Case 3: No Sprint Velocity Data — Estimate still produced, gap stated

**Fixture:**
- `project.yaml`: `engine.name: godot`; `src/core/` holds the inventory code the save touches
- `design/gdd/save-load.md` documents the save system clearly
- `production/sprints/` is empty — no historical sprints

**Input:** `$gs-estimate Implement save and load of player inventory`

**Domain checks:**
- [ ] Skill does not error or stop when no sprint history exists
- [ ] Estimate is still produced with Optimistic, Expected and Pessimistic figures
- [ ] Output states that no sprint history was available for velocity calibration
- [ ] Any allowance for the missing data is stated as a risk, not hidden in the figures

---

### Case 4: Vague Task — Clarification before estimating

**Fixture:**
- `project.yaml`: `engine.name: godot`
- Project has GDDs and source code under `src/`; sprint history exists

**Input:** `$gs-estimate make combat feel better`

**Domain checks:**
- [ ] Skill asks for clarification for a task that names no concrete change
- [ ] No estimate figures are produced before the clarification is answered
- [ ] `Verdict: COMPLETE` is not printed for an unclarified task
- [ ] No files are written

---

### Case 5: Gate Compliance — No gate; estimates are informational

**Fixture:**
- `project.yaml`: `engine.name: godot`, `modes.review_mode: full`
- Task relates to a documented system with medium complexity; its code is under `src/`

**Input:** `$gs-estimate Add item pickup with inventory stacking`

**Domain checks:**
- [ ] No director gate is invoked regardless of review mode
- [ ] Output is purely informational — no approval or write prompt
- [ ] Next-step recommendation references `$gs-sprint-plan`
- [ ] Estimate does not change based on review mode
