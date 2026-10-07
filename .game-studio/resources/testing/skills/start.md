# Evaluation scenarios: gs-start

Professional scenarios adapted from Donchitos' upstream testing guidance; see
[source attribution](../../../../NOTICE.md). These are evaluation inputs and domain
checks, not executed results. Read `.agents/skills/gs-start/SKILL.md` and its current procedure first.
Use [evaluation policy](../README.md) and [category rubric](../quality-rubric.md).

Resolve current config and project engine records. Apply review-mode discipline
coverage without claiming automatic delegation: use the parent when needed, label it,
and record actual participants only. Existing human authorization governs writes;
case approvals represent unresolved decisions and never revoke prior authorization.
Historical fixture versions are scenario inputs, not current API verification.
The linked native procedure governs command arguments, output schemas, receipts,
context and mode applicability. Missing inputs remain NOT ASSESSED.

### Case 1: Happy Path — Fresh repo, Path A, minimal rigor

**Fixture:**
- No `project.yaml`, no `production/stage.txt`; `technical-preferences.md`
  holds only placeholders
- No design docs, prototypes or source code; `origin` is the user's own repo
- The user picks `A) No idea yet`, approves the `project.yaml` write, then picks
  `Jam / prototype / first game`, then `Guided`

**Input:** `$gs-start`

**Domain checks:**
- [ ] Phase 2 offers exactly the four A–D options and no engine choice
- [ ] Preserve the case's unresolved human decisions and declines; perform routine writes already authorized, and ask only for missing decisions or scope.
- [ ] `project.stage` and `production/stage.txt` are both `Concept`
- [ ] `project.yaml` ends up holding only `project.stage`, `modes.rigor` and `modes.automation` from `$gs-start` — none of the six rigor-fronted knobs — and `production/review-mode.txt` is not written
- [ ] The recommended rigor option is listed first with ` (Recommended)`
- [ ] Phase 4 prints the minimal 4-step path
- [ ] The next skill is not auto-run; Verdict is COMPLETE

---

### Case 2: Returning User — Onboarding skipped

**Fixture:**
- `project.yaml` has `engine.name: Godot` and `modes.rigor: minimal`; no explicit `modes.review_mode`
- `design/game-brief.md` exists

**Input:** `$gs-start`

**Domain checks:**
- [ ] The A–D starting-point question is not asked
- [ ] The message names the configured engine (Godot) and the brief path
- [ ] Review mode is reported as `solo`, resolved from rigor
- [ ] No write is made to `project.yaml` or `production/stage.txt`

---

### Case 3: Existing Work on Unity — Path D2, stage and rigor already set

**Fixture:**
- `project.yaml` has `engine.name: Unity`, `modes.rigor: standard` and
  `modes.automation: collaborative`
- C# scripts exist under `Assets/Scripts/`; `design/gdd/` holds 3 system GDDs;
  no `design/gdd/game-concept.md`, no `docs/architecture/`
- The user picks `D) Existing work` and approves the `project.yaml` write

**Input:** `$gs-start`

**Domain checks:**
- [ ] Source files are found under `Assets/`, not reported as absent
- [ ] `$gs-project-stage-detect` and `$gs-adopt` are recommended for D2
- [ ] Preserve the case's unresolved human decisions and declines; perform routine writes already authorized, and ask only for missing decisions or scope.
- [ ] The rigor and automation questions are skipped because both keys are set
- [ ] The D2 retrofit path is printed in Phase 4, including the GDD, ADR and registry retrofit steps
- [ ] Verdict is COMPLETE

---

### Case 4: Clone Still Wired to the Template Repo — remote note, never run

**Fixture:**
- Fresh project as in Case 1
- `.git/config` has `[remote "origin"]` with url
  `https://github.com/I2ene/Codex-Game-Studios.git`
- The user picks `B) Vague idea` with the hint "a small weekend puzzler"

**Input:** `$gs-start`

**Domain checks:**
- [ ] The template-origin note appears exactly once, after the path
- [ ] The current procedure's suggested origin-remediation commands are presented without execution
- [ ] No git command is executed (read of `.git/config` only)
- [ ] The minimal rigor option is the recommended one for the described scope

---

### Case 5: Director Gate Check — No gate; start is a utility setup skill

**Fixture:**
- Fresh project and answers as in Case 1 (`A) No idea yet`, the write approved,
  `Jam / prototype / first game`, `Guided`)

**Input:** `$gs-start`

**Domain checks:**
- [ ] No director gate is invoked during the skill execution
- [ ] No gate skip messages appear (gates are absent, not suppressed)
- [ ] Skill reaches COMPLETE without any gate verdict

---

### Case 6: Path D2 With Rigor Unset — the retrofit path waits for the answer

**Fixture:**
- `project.yaml` has `engine.name: Godot` and no `modes` block
- `src/` holds GDScript files; `design/gdd/` holds 4 system GDDs; no
  `docs/architecture/`
- The user picks `D) Existing work`, approves the `project.yaml` write, then
  picks `Several systems that affect each other` and `Collaborative`

**Input:** `$gs-start`

**Domain checks:**
- [ ] No tiered D2 path is printed before Phase 3d has the rigor
- [ ] The rigor question is asked because the key is unset
- [ ] Phase 4's D2 path matches the chosen `standard`, with the GDD, ADR and registry retrofit steps
- [ ] None of the six rigor-fronted knobs is written — only `modes.rigor` and `modes.automation` are added
