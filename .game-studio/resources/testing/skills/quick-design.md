# Evaluation scenarios: gs-quick-design

Professional scenarios adapted from Donchitos' upstream testing guidance; see
[source attribution](../../../../NOTICE.md). These are evaluation inputs and domain
checks, not executed results. Read `.agents/skills/gs-quick-design/SKILL.md` and its current procedure first.
Use [evaluation policy](../README.md) and [category rubric](../quality-rubric.md).

Resolve current config and project engine records. Apply review-mode discipline
coverage without claiming automatic delegation: use the parent when needed, label it,
and record actual participants only. Existing human authorization governs writes;
case approvals represent unresolved decisions and never revoke prior authorization.
Historical fixture versions are scenario inputs, not current API verification.
The linked native procedure governs command arguments, output schemas, receipts,
context and mode applicability. Missing inputs remain NOT ASSESSED.

### Case 1: Happy Path — Tweak to an existing system

**Fixture:**
- `design/gdd/movement.md` exists and describes dash invincibility in its Detailed Rules
- `design/gdd/systems-index.md` exists
- `design/quick-specs/dash-cooldown-tuning-[earlier-date].md` tuned the dash cooldown in movement and does not touch invincibility

**Input:** `$gs-quick-design make dash invincible on frame 1`

**Domain checks:**
- [ ] The classification is confirmed via `host input tool` before any context scan or drafting
- [ ] The prior dash-cooldown spec is named in the context report even though it does not conflict
- [ ] The draft uses the Tweak/Addition format, and its Design Delta quotes the current GDD text
- [ ] Preserve the case's unresolved human decisions and declines; perform routine writes already authorized, and ask only for missing decisions or scope.
- [ ] The file path is `design/quick-specs/[kebab-case-title]-[YYYY-MM-DD].md` with today's date
- [ ] The GDD edit is asked for separately, after the quick spec is written, with old vs. new text shown
- [ ] The run ends with the handoff block and verdict `COMPLETE`

---

### Case 2: Failure Path — Scope too large; redirected to $gs-design-system

**Fixture:**
- Scenario (a): the request is "redesign the entire combat system"
- Scenario (b): a Tweak is drafted, and at the approval step the user picks `[C] This grew too large — redirect to $gs-design-system instead`

**Input:** (a) `$gs-quick-design redesign the entire combat system` (b) `$gs-quick-design allow combo to cancel into roll`

**Domain checks:**
- [ ] (a) The scope excess is detected and the skill stops before drafting
- [ ] (a) The verdict line is printed even when the skill stops before the classification widget, not only via `[F]`
- [ ] The message names `$gs-design-system` as the alternative
- [ ] No quick spec file is written
- [ ] The verdict is `REDIRECTED`, not `COMPLETE`

---

### Case 3: Edge Case — Tuning change outside the documented knob range

**Fixture:**
- `design/gdd/player-controller.md` has a Tuning Knobs entry `jump_height` with documented range 3–5
- `assets/data/player.json` holds `jump_height: 5`
- An earlier quick spec, `design/quick-specs/jump-height-tuning-[earlier-date].md`, previously set `jump_height` to 5

**Input:** `$gs-quick-design increase jump height from 5 to 6 units`

**Domain checks:**
- [ ] `assets/data/` is checked for the data file because the change is Tuning
- [ ] The prior quick spec touching `jump_height` is reported, not silently contradicted
- [ ] The draft uses the single-table Tuning format, not the Tweak/Addition sections
- [ ] The Tuning Knob Mapping says the value is outside the documented range and explains the extension

---

### Case 4: Edge Case — No argument and no systems index

**Fixture:**
- No `design/gdd/systems-index.md`
- `design/quick-specs/` may or may not exist

**Input:** `$gs-quick-design` (no argument)

**Domain checks:**
- [ ] With no argument, the skill asks for a description in plain text rather than guessing a change
- [ ] Classification happens only after the user describes the change
- [ ] The missing systems index is noted with the documented line, and the run continues
- [ ] Preserve the case's unresolved human decisions and declines; perform routine writes already authorized, and ask only for missing decisions or scope.

---

### Case 5: No Director Gates — Review mode has no effect

**Fixture:**
- The change is within scope (an Addition: "add a parry window to the block mechanic")
- `design/gdd/combat.md` exists (a GDD written voluntarily at this tier) and describes the block mechanic
- `project.yaml` has `modes.review_mode: full` and `modes.workflow: minimal`

**Input:** `$gs-quick-design add a parry window to the block mechanic`

**Domain checks:**
- [ ] No director gate or other agent is consulted
- [ ] `modes.review_mode: full` does not change the skill's behavior
- [ ] The output explains that quick specs bypass `$gs-design-review` and `$gs-review-all-gdds`, and names `$gs-design-system` for larger changes
- [ ] The handoff points to `$gs-dev-story` directly at `workflow: minimal`

---

### Case 6: Edge Case — No GDD for the system (the default tier)

**Fixture:**
- `project.yaml` has `modes.rigor: minimal`; `design/gdd/` holds no system GDD
- `design/game-brief.md` describes the jump; `production/epics/movement/story-002-jump.md` implements it with a jump height of 5

**Input:** `$gs-quick-design increase jump height from 5 to 6 units`

**Domain checks:**
- [ ] The skill does not stop, and does not redirect to `$gs-design-system`, because there is no GDD
- [ ] The report names the brief and the story it used in place of a GDD
- [ ] The spec's GDD Reference is `design/game-brief.md`
- [ ] Preserve the case's unresolved human decisions and declines; perform routine writes already authorized, and ask only for missing decisions or scope.
