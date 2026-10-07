# Evaluation scenarios: gs-soak-test

Professional scenarios adapted from Donchitos' upstream testing guidance; see
[source attribution](../../../NOTICE.md). These are evaluation inputs and domain
checks, not executed results. Read `.agents/skills/gs-soak-test/SKILL.md` and its current procedure first.
Use [evaluation policy](../README.md) and [category rubric](../quality-rubric.md).

Resolve current config and project engine records. Apply review-mode discipline
coverage without claiming automatic delegation: use the parent when needed, label it,
and record actual participants only. Existing human authorization governs writes;
case approvals represent unresolved decisions and never revoke prior authorization.
Historical fixture versions are scenario inputs, not current API verification.
The linked native procedure governs command arguments, output schemas, receipts,
context and mode applicability. Missing inputs remain NOT ASSESSED.

### Case 1: Happy Path — 2-hour, all-focus soak on Godot

**Fixture:**
- `project.yaml` has `engine.name: Godot` and `performance.target_framerate: 60`
- `design/gdd/game-concept.md` states the intended session length
- The user approves the write

**Input:** `$gs-soak-test 2h all`

**Domain checks:**
- [ ] Checkpoints are exactly T+0, T+20, T+40, T+60, T+80, T+100, T+120
- [ ] Memory thresholds are relative to T+0, and the unit is recorded as displayed (no unit assumed)
- [ ] The Godot tool and counter names are marked NOT SOURCEABLE, not presented as verified, and Pre-Session Setup asks for the tool actually used
- [ ] Memory, stability and balance observation items are all present (focus `all`)
- [ ] Preserve the case's unresolved human decisions and declines; perform routine writes already authorized, and ask only for missing decisions or scope.
- [ ] The skill issues no verdict itself — the protocol's Verdict section is left for the tester

---

### Case 2: No Arguments — Defaults applied

**Fixture:**
- No arguments provided; engine configured

**Input:** `$gs-soak-test`

**Domain checks:**
- [ ] Duration `1h` and focus `all` are used when no argument is given
- [ ] Checkpoints are exactly T+0, T+15, T+30, T+45, T+60
- [ ] The output path ends `-1h.md`
- [ ] Preserve the case's unresolved human decisions and declines; perform routine writes already authorized, and ask only for missing decisions or scope.

---

### Case 3: Narrow Focus on Unreal — 4-hour memory soak

**Fixture:**
- `project.yaml` has `engine.name: Unreal`

**Input:** `$gs-soak-test 4h memory`

**Domain checks:**
- [ ] Checkpoints are exactly T+0, T+30, T+60, T+90, T+120, T+180, T+240
- [ ] The Unreal threshold is a relative > 20% growth, not an absolute size
- [ ] `stat memory` is marked NOT SOURCEABLE, a pointer to confirm rather than a verified command
- [ ] Balance/fatigue items are omitted for focus `memory`
- [ ] Preserve the case's unresolved human decisions and declines; perform routine writes already authorized, and ask only for missing decisions or scope.

---

### Case 4: No Performance Budgets — "not set", never invented

**Fixture:**
- `project.yaml` has `engine.name: Unity` and no `performance` block
- `technical-preferences.md` Performance Budgets are `[TO BE CONFIGURED]`

**Input:** `$gs-soak-test 30m memory`

**Domain checks:**
- [ ] Missing budgets are recorded as "not set", not filled with defaults
- [ ] Checkpoints are exactly T+0, T+10, T+20, T+30
- [ ] The Unity threshold is the unit-free monotonic-growth check
- [ ] Preserve the case's unresolved human decisions and declines; perform routine writes already authorized, and ask only for missing decisions or scope.

---

### Case 5: Director Gate Check — No gate; soak-test is a planning utility

**Fixture:**
- Engine configured; valid duration and focus provided

**Input:** `$gs-soak-test 1h stability`

**Domain checks:**
- [ ] No director gate is invoked
- [ ] No gate skip messages appear
- [ ] The run ends at "Protocol written." with the run steps — no gate verdict, and no soak verdict issued by the skill
