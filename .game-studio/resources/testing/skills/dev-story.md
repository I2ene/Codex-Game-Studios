# Evaluation scenarios: gs-dev-story

Professional scenarios adapted from Donchitos' upstream testing guidance; see
[source attribution](../../../NOTICE.md). These are evaluation inputs and domain
checks, not executed results. Read `.agents/skills/gs-dev-story/SKILL.md` and its current procedure first.
Use [evaluation policy](../README.md) and [category rubric](../quality-rubric.md).

Resolve current config and project engine records. Apply review-mode discipline
coverage without claiming automatic delegation: use the parent when needed, label it,
and record actual participants only. Existing human authorization governs writes;
case approvals represent unresolved decisions and never revoke prior authorization.
Historical fixture versions are scenario inputs, not current API verification.
The linked native procedure governs command arguments, output schemas, receipts,
context and mode applicability. Missing inputs remain NOT ASSESSED.

### Case 1: Happy Path — Logic story implemented at full workflow

**Fixture:**
- `project.yaml`: `engine.name: Godot`, `specialists.code: godot-gdscript-specialist`,
  `modes.workflow: full`, `qa.level: standard`
- `production/epics/combat/story-001-damage-calc.md`: `Status: Ready`, Layer Core,
  Type Logic, `Requirement: TR-combat-001`, `ADR Governing Implementation: ADR-0003`,
  an `ADR Version` equal to ADR-0003's `## Last Verified` date, a `Manifest Version`
  equal to the manifest header date, Dependencies None, Test Evidence
  `tests/unit/combat/combat_damage_calc_test.gd`
- `docs/architecture/tr-registry.yaml` has `TR-combat-001`; ADR-0003 exists and is
  Accepted; `docs/architecture/control-manifest.md` exists
- `production/sprint-status.yaml` does not exist

**Input:** `$gs-dev-story production/epics/combat/story-001-damage-calc.md`

**Domain checks:**
- [ ] ADR-0003 is not read in full when its `Last Verified` matches the story's `ADR Version`
- [ ] The In Progress ask names the story file; `Status:` becomes `In Progress` only after it and before any discipline review begins, and the sprint-status-absent line is printed
- [ ] Primary is `gameplay-programmer`; secondary comes from `specialists.code`, not the roster table
- [ ] The ADR guidance is passed inline, not as the ADR path
- [ ] The brief names `tests/unit/combat/combat_damage_calc_test.gd` (`[system]_[feature]_test.gd`) and requires one test per acceptance criterion
- [ ] The parse check's command and exit code are reported, and exactly one `Run result:` line appears
- [ ] Story is NOT marked Complete; the handoff is `$gs-code-review` then `$gs-story-done`
- [ ] The CHECKPOINT block in `active.md` is overwritten, not appended to

---

### Case 2: Failure Path — Referenced ADR is Proposed

**Fixture:**
- `project.yaml`: `modes.workflow: standard`
- Story file with `Status: Ready` and `ADR Governing Implementation: ADR-0005`
- `docs/architecture/adr-0005-*.md` exists with `## Status` Proposed

**Input:** `$gs-dev-story production/epics/[epic-slug]/story-[NNN]-[slug].md`

**Domain checks:**
- [ ] The story header remains Status: Ready while session state records BLOCKED.
- [ ] The Proposed status is read from ADR-0005's `## Status` section, not inferred
- [ ] No programmer or engine-specialist agent is consulted
- [ ] Output names ADR-0005 and recommends `$gs-architecture-decision`
- [ ] Preserve the case's unresolved human decisions and declines; perform routine writes already authorized, and ask only for missing decisions or scope.
- [ ] BLOCKED is recorded in session state, and the checkpoint's **Next step** names `$gs-architecture-decision accept ADR-0005` — not `$gs-story-done`

---

### Case 2b: Failure Path — Proposed ADR at the `full` tier

The `full` column of the file-check table has its own STOP rule, so the
`standard` case above does not exercise it.

**Fixture:**
- `project.yaml`: `modes.workflow: full`
- Story file with `Status: Ready`, `ADR Governing Implementation: ADR-0005` and an
  `ADR Version` older than ADR-0005's `## Last Verified` date
- `docs/architecture/adr-0005-*.md` exists with `## Status` Proposed;
  `docs/architecture/tr-registry.yaml` and the control manifest exist

**Input:** `$gs-dev-story production/epics/[epic-slug]/story-[NNN]-[slug].md`

**Domain checks:**
- [ ] The stop happens at `full`
- [ ] The Status decides before the freshness check: no ADR-version mismatch prompt is shown although the versions differ, and the ADR is not read beyond the one Grep
- [ ] No programmer or engine-specialist agent is consulted, and the story stays `Status: Ready`

---

### Case 3: ADR changed since the story was written
**Fixture:**
- `project.yaml`: `engine.name: Godot`, `modes.workflow: full`
- Story file with `Status: Ready`, Type Logic, `Requirement: TR-combat-002`,
  `ADR Governing Implementation: ADR-0004`, an `ADR Version` older than ADR-0004's
  `## Last Verified` date, a `Manifest Version` equal to the manifest header date,
  Dependencies None
- `docs/architecture/tr-registry.yaml` has `TR-combat-002`; ADR-0004 exists with
  `## Status` Accepted and is under 50KB; `docs/architecture/control-manifest.md`
  exists
- User picks `[A]` at the prompt

**Input:** `$gs-dev-story production/epics/[epic-slug]/story-[NNN]-[slug].md`

**Domain checks:**
- [ ] The mismatch prompt is shown before any discipline review begins
- [ ] All three options ([A] re-read / [B] accept drift / [C] stop) are offered, and [A] names the story edit it makes
- [ ] On [A] the size is checked and a sub-50KB ADR is read in a single `Read`
- [ ] The story's `ADR Version` becomes ADR-0004's `Last Verified` date — not today's date — before the programmer is consulted
- [ ] The programmer brief carries the freshly read Decision guidance inline, not the summary the story held before [A]

**Fixture (Date fallback):**
- As above, but ADR-0004 has no `## Last Verified` section; its `## Date` equals the
  story's `ADR Version` (the value `$gs-create-stories` stamped from it)

**Domain checks (Date fallback):**
- [ ] No mismatch prompt is shown — an ADR stamped from its `## Date` is not treated as stale for lacking `## Last Verified`
- [ ] ADR-0004 is not read beyond the one Grep

---

### Case 4: Edge Case — No argument; reads from session state
**Fixture:**
- No argument is provided
- `production/session-state/active.md` references an active story file
- That story file exists with `Status: In Progress`

**Input:** `$gs-dev-story` (no argument)

**Domain checks:**
- [ ] Skill reads session state when no argument is provided
- [ ] Skill confirms the active story with the user before proceeding
- [ ] Skill does NOT silently assume the active story without confirmation

**Fixture (no active story):**
- No argument is provided
- `production/session-state/active.md` names no active story
- `production/epics/` holds two stories with `Status: Ready` and one `In Progress`

**Domain checks (no active story):**
- [ ] The question is asked instead of guessing a story
- [ ] Only the `Status: Ready` stories are listed

---

### Case 5: Minimal tier, Logic story — tests waived

**Fixture:**
- `project.yaml`: `engine.name: Godot`, `modes.workflow: minimal`, `qa.level: minimal`
- Story Type Logic with `Requirement: Brief MVP feature 1` and ADR fields
  `N/A (minimal — no ADRs)`
- No TR registry, no ADRs, no control manifest
- `<project-engine-reference>/godot/VERSION.md` rates the pinned version HIGH risk

**Input:** `$gs-dev-story production/epics/[slug]/story-001-[slug].md`

**Domain checks:**
- [ ] No STOP or BLOCKED for the absent TR registry, ADR or manifest at `minimal`
- [ ] The `Briefing omits:` line names all three dropped inputs, the ADR included
- [ ] The engine specialist is consulted because VERSION.md rates the risk HIGH
- [ ] The test waiver is stated to the agent and printed in the summary; no tests row or "run your test suite" paragraph appears
- [ ] A `Run result:` line is printed — run-and-observe is not waived
- [ ] The handoff is `$gs-story-done` with no `$gs-code-review` step

---

### Case 5b: Minimal tier, UI story — the screenshot is still required

**Fixture:**
- `project.yaml`: `engine.name: Godot`, `modes.workflow: minimal`, `qa.level: minimal`
- Story Type UI with `Requirement: Brief MVP feature 2` and ADR fields
  `N/A (minimal — no ADRs)`
- No TR registry, no ADRs, no control manifest

**Input:** `$gs-dev-story production/epics/[slug]/story-002-[slug].md`

**Domain checks:**
- [ ] The UI story is not told its evidence is waived — neither in the brief nor as a "Test evidence: waived" line in the summary
- [ ] The screenshot-required line is printed at `qa.level: minimal`
- [ ] `Run result: OBSERVED` names a retained screenshot; a `NOT VERIFIED` result would be reported as a blocker, not a note
- [ ] The handoff is `$gs-story-done` with no `$gs-code-review` step

---

### Case 6: Unity — code under `Assets/`, capture script asked for

**Fixture:**
- `project.yaml`: `engine.name: Unity`, `specialists.code: unity-specialist`,
  `specialists.ui: unity-ui-specialist`, `commands.smoke` and `commands.run` set,
  `modes.workflow: minimal`, `qa.level: minimal`
- Story Type UI (an inventory screen) with `Requirement: Brief MVP feature 3` and
  ADR fields `N/A (minimal — no ADRs)`
- The project has `Assets/` and no `src/`; no `ScreenshotOnArg.cs` exists under `Assets/`
- `<project-engine-reference>/unity/VERSION.md` rates the pinned version HIGH risk

**Input:** `$gs-dev-story production/epics/[slug]/story-003-[slug].md`

**Domain checks:**
- [ ] No file is written under `src/` — the Godot row is not a default
- [ ] Both specialists come from the `specialists` block, not the roster table
- [ ] `ScreenshotOnArg.cs` is written only after its ask, at `Assets/Scripts/`, exactly as run-and-observe.md gives it
- [ ] If the user declines that ask, the result is `Run result: NOT VERIFIED — ScreenshotOnArg.cs not written`, not an observation
- [ ] Verification names `commands.smoke` and its exit code

---

### Case 7: Engine unset — the code root is unresolved, nothing is written

**Fixture:**
- `project.yaml` has no `engine` block; `.game-studio/resources/docs/technical-preferences.md`
  reads `Engine: [TO BE CONFIGURED]`
- The project has none of `src/`, `Assets/` or `Source/`
- `modes.workflow: minimal`; the story is Type Logic

**Input:** `$gs-dev-story production/epics/[slug]/story-001-[slug].md`

**Domain checks:**
- [ ] No file is created under `src/` or any other guessed root
- [ ] The output names the unresolved code root as the reason nothing was written
- [ ] "Implementation Complete" is not printed

---

### Case 8: Dependency marked Complete through option [C]

**Fixture:**
- `project.yaml`: `engine.name: Godot`, `modes.workflow: minimal`, `qa.level: minimal`
- `story-003` lists `story-002` under Dependencies; `story-002` has
  `Status: In Progress`
- At the dependency prompt the user picks `[C]`, then approves the update

**Input:** `$gs-dev-story production/epics/[slug]/story-003-[slug].md`

**Domain checks:**
- [ ] On [C], dependency story-002 becomes Complete and only its Status field changes before work continues on story-003.
- [ ] The dependency prompt comes before any discipline review begins
- [ ] Preserve the case's unresolved human decisions and declines; perform routine writes already authorized, and ask only for missing decisions or scope.
- [ ] story-003 itself is not marked Complete — it is set In Progress, after its own ask
- [ ] Had the user picked `[B]`, story-003 would be BLOCKED in session state and no agent consulted

---

### Case 9: The agent stops early — INCOMPLETE, and the checkpoint says resume

**Fixture:**
- `project.yaml`: `engine.name: Godot`, `modes.workflow: minimal`, `qa.level: minimal`
- Story Type Logic, `Status: Ready`, ADR fields `N/A (minimal — no ADRs)`
- The programmer agent reports that it hit its turn limit after adding
  `src/combat/damage.gd`, which calls a helper it never defined

**Input:** `$gs-dev-story production/epics/[slug]/story-001-[slug].md`

**Domain checks:**
- [ ] No "Implementation Complete" and no `Status:` change past `In Progress`
- [ ] The checkpoint's **Next step** is `$gs-dev-story [story-path]` to resume — never `$gs-story-done`, which `$gs-help` reads as "the work is written"

---

### Case 10: `full` tier, a story with no governing ADR (`ADR: N/A`)

**Fixture:**
- `project.yaml`: `engine.name: Godot`, `modes.workflow: full`
- Story `Status: Ready`, Type Logic, `ADR Governing Implementation: N/A — no
  architectural pattern required` (what `$gs-create-stories` writes for a
  requirement `$gs-create-epics` flagged as untraced)
- `docs/architecture/tr-registry.yaml` has the story's TR-ID; the control manifest exists

**Input:** `$gs-dev-story production/epics/[slug]/story-004-[slug].md`

**Domain checks:**
- [ ] No STOP and no BLOCKED for the `N/A` ADR field at `full`
- [ ] No ADR file is looked up for `N/A`
- [ ] Variant — the story names `ADR-0006`, whose `## Status` reads `Superseded by ADR-0009`: the story is BLOCKED at every tier, naming ADR-0009 and saying to edit its ADR field (`$gs-create-stories` never rewrites an existing story)
