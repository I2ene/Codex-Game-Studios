# Evaluation scenarios: gs-test-setup

Professional scenarios adapted from Donchitos' upstream testing guidance; see
[source attribution](../../../NOTICE.md). These are evaluation inputs and domain
checks, not executed results. Read `.agents/skills/gs-test-setup/SKILL.md` and its current procedure first.
Use [evaluation policy](../README.md) and [category rubric](../quality-rubric.md).

Resolve current config and project engine records. Apply review-mode discipline
coverage without claiming automatic delegation: use the parent when needed, label it,
and record actual participants only. Existing human authorization governs writes;
case approvals represent unresolved decisions and never revoke prior authorization.
Historical fixture versions are scenario inputs, not current API verification.
The linked native procedure governs command arguments, output schemas, receipts,
context and mode applicability. Missing inputs remain NOT ASSESSED.

### Case 1: Happy Path — Godot project, scaffolds GdUnit4 test structure

**Fixture:**
- `project.yaml` has `engine.name: Godot`
- `tests/` does not exist; `addons/gdUnit4/` is not installed; no CI workflow
- The user approves the plan

**Input:** `$gs-test-setup`

**Domain checks:**
- [ ] Godot CI uses the project-installed gdUnit4 package rather than silently replacing it with latest, and configures the permissions required by its result publisher using the verified action/runtime syntax.
- [ ] `tests/unit/`, `tests/integration/`, `tests/smoke/` and `production/qa/evidence/` all exist afterwards (each holds a written file)
- [ ] No custom runner script is written (the old hand-written runner loaded a file gdUnit4 never shipped and failed every run)
- [ ] The test command matches the coding-standards.md CI command
- [ ] Approval is asked before any file is created
- [ ] Verdict is COMPLETE

---

### Case 2: Unity Project — Scaffolds Unity Test Runner with asmdef

**Fixture:**
- `project.yaml` has `engine.name: Unity`
- `Packages/manifest.json` lists `com.unity.test-framework`
- No `Assets/Tests/`; the user approves the plan

**Input:** `$gs-test-setup`

**Domain checks:**
- [ ] Document the `UNITY_LICENSE` secret prerequisite for Unity CI.
- [ ] Tests are under `Assets/Tests/`, never `tests/` or a top-level `Tests/` (neither is compiled: 0 tests, "Passed")
- [ ] `.asmdef` files are generated
- [ ] EditMode and PlayMode runner config is present, in CI and as two local runs with separate results files
- [ ] The gate note names the Unity test root
- [ ] Verdict is COMPLETE

---

### Case 3: Infrastructure Already Exists — Early exit, nothing re-initialized

**Fixture:**
- Godot project; `tests/unit/`, `tests/integration/`, `.github/workflows/tests.yml`
  and `addons/gdUnit4/bin/GdUnitCmdTool.gd` all exist
- No `force` argument

**Input:** `$gs-test-setup`

**Domain checks:**
- [ ] Skill does NOT re-initialize when the infrastructure exists
- [ ] The message points to `$gs-test-setup force`
- [ ] No existing file is modified and no new file is written

---

### Case 4: No Engine Configured — Redirects to $gs-setup-engine

**Fixture:**
- `project.yaml` has no `engine.name`; `technical-preferences.md` shows
  `[TO BE CONFIGURED]` for Engine

**Input:** `$gs-test-setup`

**Domain checks:**
- [ ] Error message explicitly states engine is not configured
- [ ] `$gs-setup-engine` is suggested as the next step
- [ ] No write tool is called
- [ ] Verdict is not COMPLETE (blocked state)

---

### Case 5: Director Gate Check — No gate; test-setup is a scaffolding utility

**Fixture:**
- Engine configured, tests/ does not exist

**Input:** `$gs-test-setup`

**Domain checks:**
- [ ] No director gate is invoked
- [ ] No gate skip messages appear
- [ ] Verdict is COMPLETE without any gate check


## Applicable domain checks

- [ ] `force` bypasses the early exit only to create missing scaffold files; every existing test or infrastructure file remains unchanged.
