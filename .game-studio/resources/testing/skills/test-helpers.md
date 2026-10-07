# Evaluation scenarios: gs-test-helpers

Professional scenarios adapted from Donchitos' upstream testing guidance; see
[source attribution](../../../../NOTICE.md). These are evaluation inputs and domain
checks, not executed results. Read `.agents/skills/gs-test-helpers/SKILL.md` and its current procedure first.
Use [evaluation policy](../README.md) and [category rubric](../quality-rubric.md).

Resolve current config and project engine records. Apply review-mode discipline
coverage without claiming automatic delegation: use the parent when needed, label it,
and record actual participants only. Existing human authorization governs writes;
case approvals represent unresolved decisions and never revoke prior authorization.
Historical fixture versions are scenario inputs, not current API verification.
The linked native procedure governs command arguments, output schemas, receipts,
context and mode applicability. Missing inputs remain NOT ASSESSED.

### Case 1: Happy Path — Player helper generated for Godot/GDScript

**Fixture:**
- `project.yaml` has `engine.name: Godot`, `engine.language: GDScript`,
  `testing.framework: gdUnit4`; `addons/gdUnit4/` is installed, so its
  assertion API can be confirmed from the project
- `tests/unit/player/player_movement_test.gd` exists
- `design/gdd/player.md` has a Formulas section bounding health to 0–100
- No existing files in `tests/helpers/`; the user approves the write

**Input:** `$gs-test-helpers player`

**Domain checks:**
- [ ] Generated helper is GDScript at `tests/helpers/player_factory.gd`
- [ ] Bound constants trace to the GDD's Formulas section (not invented values)
- [ ] Helper extends `RefCounted`, not the test-suite base class, and uses no Autoload/singleton
- [ ] No bare `assert()` and no unresolved `FAIL_IF` reaches the file
- [ ] Verdict is COMPLETE

---

### Case 2: Engine Not Configured — Stops with $gs-setup-engine

**Fixture:**
- `project.yaml` has no `engine` block; `technical-preferences.md` shows
  `[TO BE CONFIGURED]` for Engine

**Input:** `$gs-test-helpers player`

**Domain checks:**
- [ ] The message states the engine is not configured
- [ ] `$gs-setup-engine` is named as the prerequisite
- [ ] No write tool is called
- [ ] Verdict is not COMPLETE (nothing was created)

---

### Case 3: Helper Already Exists — Skipped, never overwritten

**Fixture:**
- Godot/GDScript/gdUnit4 configured as in Case 1
- `tests/helpers/game_assertions.gd` already exists with hand-written additions
- `tests/helpers/game_factory.gd` and `tests/helpers/scene_runner_helper.gd` do
  not exist; the user approves the write

**Input:** `$gs-test-helpers scaffold`

**Domain checks:**
- [ ] `scaffold` mode generates no `[system]_factory` helper
- [ ] The existing `game_assertions.gd` is left byte-for-byte unchanged
- [ ] The skip message names the existing file and how to regenerate it
- [ ] Only the two missing files are written; Verdict is COMPLETE

---

### Case 4: Framework Assertion API Unconfirmed — No helper generated

**Fixture:**
- `project.yaml` has `engine.name: Godot`, `engine.language: GDScript`;
  `testing.framework` is absent and `technical-preferences.md` shows no Framework
- No `addons/gdUnit4/` and no existing test files to learn the API from

**Input:** `$gs-test-helpers scaffold`

**Domain checks:**
- [ ] The skill states it cannot confirm the framework's assertion API
- [ ] No helper file is written
- [ ] No guessed assertion form (and no `FAIL_IF` placeholder) is presented as ready to write
- [ ] Verdict is not COMPLETE

---

### Case 5: Director Gate Check — No gate; test-helpers is a scaffolding utility

**Fixture:**
- Engine and framework configured as in Case 1, no existing helpers

**Input:** `$gs-test-helpers player`

**Domain checks:**
- [ ] No director gate is invoked
- [ ] No gate skip messages appear
- [ ] Verdict is COMPLETE without any gate check

---

### Case 6: Unity — Helpers under the engine's test root

**Fixture:**
- `project.yaml` has `engine.name: Unity`, `engine.language: C#`,
  `testing.framework: NUnit`; `com.unity.test-framework` is in
  `Packages/manifest.json`, so NUnit's assertion API can be confirmed from the
  installed package
- `$gs-test-setup` has created `Assets/Tests/EditMode/EditModeTests.asmdef`
- No helpers exist yet; the user approves the write

**Input:** `$gs-test-helpers scaffold`

**Domain checks:**
- [ ] Helpers are written under `Assets/Tests/EditMode/Helpers/`
- [ ] Nothing is written under `tests/helpers/` — outside `Assets/`, Unity never compiles it
- [ ] Preserve the case's unresolved human decisions and declines; perform routine writes already authorized, and ask only for missing decisions or scope.
- [ ] Verdict is COMPLETE
