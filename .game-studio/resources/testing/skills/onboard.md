# Evaluation scenarios: gs-onboard

Professional scenarios adapted from Donchitos' upstream testing guidance; see
[source attribution](../../../NOTICE.md). These are evaluation inputs and domain
checks, not executed results. Read `.agents/skills/gs-onboard/SKILL.md` and its current procedure first.
Use [evaluation policy](../README.md) and [category rubric](../quality-rubric.md).

Resolve current config and project engine records. Apply review-mode discipline
coverage without claiming automatic delegation: use the parent when needed, label it,
and record actual participants only. Existing human authorization governs writes;
case approvals represent unresolved decisions and never revoke prior authorization.
Historical fixture versions are scenario inputs, not current API verification.
The linked native procedure governs command arguments, output schemas, receipts,
context and mode applicability. Missing inputs remain NOT ASSESSED.

### Case 1: Happy Path — Programmer Role on a Godot Project

**Fixture:**
- `AGENTS.md` exists
- `project.yaml` has `engine.name: Godot`, so the code root is `src/`
- `src/` holds game code; `.codex/agents/gs-gameplay-programmer.toml` exists
- `production/sprints/sprint-005.md` exists; git log has recent commits
- `modes.automation` is unset (defaults to `collaborative`)

**Input:** `$gs-onboard gameplay-programmer`

**Domain checks:**
- [ ] The agent definition for the named role is read
- [ ] The code root `src/` is scanned for this programmer role
- [ ] The explanation covers the role, current task, architecture, naming standards, relevant scripts and review responsibilities without requiring a retired fixed report template
- [ ] Preserve the case's unresolved human decisions and declines; perform routine writes already authorized, and ask only for missing decisions or scope.
- [ ] The completion summary distinguishes explained context from executed work and recommends a relevant next step such as `$gs-sprint-status` or `$gs-help`

---

### Case 2: Designer Role — Scans design/, Not the Code Root

**Fixture:**
- `AGENTS.md` exists; `.codex/agents/gs-game-designer.toml` exists
- `design/gdd/` holds three system GDDs
- `src/` also holds code

**Input:** `$gs-onboard game-designer`

**Domain checks:**
- [ ] `design/` is the area scanned for this role
- [ ] The existing GDDs are named in the document's current-state section
- [ ] Preserve the case's unresolved human decisions and declines; perform routine writes already authorized, and ask only for missing decisions or scope.
- [ ] Verdict is COMPLETE

---

### Case 3: Every Input Absent — Report Gaps Without Inventing Project State

**Fixture:**
- `AGENTS.md` does not exist
- `.codex/agents/` does not exist, so no agent definition can be read
- `tests/` does not exist; the directory is not a git repository

**Input:** `$gs-onboard qa-tester`

**Domain checks:**
- [ ] Unavailable framework instructions and role profiles are reported as context gaps; identify an installation gap only when the requested installed capability actually requires those files. Do not attribute them to a game-authoring skill or suppress useful authorized onboarding that the parent can perform.
- [ ] Inputs are recorded as FOUND or ABSENT before any report is produced
- [ ] Unavailable project facts and unexecuted verification are NOT ASSESSED — NO DATA; no complete project assessment or successful task execution is invented
- [ ] The missing inputs are named; `tests/` points to `$gs-test-setup`
- [ ] Use the linked native procedure and explicit runtime command; retired host execution is not required.
- [ ] Preserve the case's unresolved human decisions and declines; perform routine writes already authorized, and ask only for missing decisions or scope.

---

### Case 4: Edge Case — Programmer Role With an Unresolved Code Root

**Fixture:**
- `AGENTS.md` exists; `.codex/agents/gs-gameplay-programmer.toml` exists
- `project.yaml` has no `engine.name`, technical-preferences has
  `[TO BE CONFIGURED]`, and both `src/` and `Assets/` exist (ambiguous tree)

**Input:** `$gs-onboard gameplay-programmer`

**Domain checks:**
- [ ] The code root is not assumed to be `src/`
- [ ] Architecture/key-file content is marked `NOT ASSESSED — code root unresolved`, not `NO DATA`
- [ ] Sections with found inputs are still generated
- [ ] Preserve the case's unresolved human decisions and declines; perform routine writes already authorized, and ask only for missing decisions or scope.

---

### Case 5: Director Gate Check — None; No Agents consult

**Fixture:**
- Any project state with `AGENTS.md` present
- Any review mode

**Input:** `$gs-onboard producer`

**Domain checks:**
- [ ] No director gate is invoked and no gate skip message appears
- [ ] No delegation is required; producer expertise can be applied and labeled by the parent
- [ ] `production/` is the area scanned for this role
- [ ] Report what was explained or executed; do not require a file write or a redundant approval for already authorized onboarding work
