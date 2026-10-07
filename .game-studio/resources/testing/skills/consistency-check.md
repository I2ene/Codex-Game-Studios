# Evaluation scenarios: gs-consistency-check

Professional scenarios adapted from Donchitos' upstream testing guidance; see
[source attribution](../../../../NOTICE.md). These are evaluation inputs and domain
checks, not executed results. Read `.agents/skills/gs-consistency-check/SKILL.md` and its current procedure first.
Use [evaluation policy](../README.md) and [category rubric](../quality-rubric.md).

Resolve current config and project engine records. Apply review-mode discipline
coverage without claiming automatic delegation: use the parent when needed, label it,
and record actual participants only. Existing human authorization governs writes;
case approvals represent unresolved decisions and never revoke prior authorization.
Historical fixture versions are scenario inputs, not current API verification.
The linked native procedure governs command arguments, output schemas, receipts,
context and mode applicability. Missing inputs remain NOT ASSESSED.

### Case 1: Happy Path — Registry and 4 GDDs agree

**Fixture:**
- `modes.workflow` resolves to `full`; `modes.automation` resolves to `collaborative`
- `design/registry/entities.yaml` has 3 entities and 2 constants, each with a `source:` GDD
- `design/gdd/` contains 4 system GDDs plus `game-concept.md`, `systems-index.md` and a `gdd-cross-review-[date].md`
- Every value the GDDs state for a registered name matches the registry

**Input:** `$gs-consistency-check`

**Domain checks:**
- [ ] The in-scope GDD list (4 GDDs, non-system docs excluded) is reported before the scan
- [ ] The scan greps for registered names rather than fully reading each GDD
- [ ] Verdict is PASS when registry and GDDs agree
- [ ] `design/registry/entities.yaml` and `docs/consistency-failures.md` are not written; the only write is the `active.md` breadcrumb
- [ ] The breadcrumb names `docs/consistency-failures.md`, not an invented report file
- [ ] The skill closes with the `host input tool` widget, not plain text

---

### Case 2: Failure Path — A GDD contradicts a registered constant

**Fixture:**
- `modes.workflow` resolves to `full`
- Registry `constants:` has `crit_multiplier` value 1.5, `source: design/gdd/combat.md`, `referenced_by: [combat.md, loot.md]`
- `design/gdd/combat.md` states `crit_multiplier = 1.5`
- `design/gdd/loot.md` states `crit_multiplier = 2.0`
- The registry entry is newer than the last commit to `combat.md` (not stale)

**Input:** `$gs-consistency-check`

**Domain checks:**
- [ ] Verdict is CONFLICTS FOUND (not PASS)
- [ ] The conflict entry names both GDDs and shows both values (1.5 and 2.0)
- [ ] The conflict is classified 🔴 CONFLICT, and the resolution targets the non-source GDD (`loot.md`)
- [ ] Preserve the case's unresolved human decisions and declines; perform routine writes already authorized, and ask only for missing decisions or scope.
- [ ] Skill does NOT auto-resolve the conflict — neither GDD is edited without the user choosing to fix it
- [ ] Final verdict is BLOCKED while the conflict is unresolved

---

### Case 3: Stale Registry — The source GDD changed after the registry entry

**Fixture:**
- `modes.workflow` resolves to `full`
- Registry `entities:` has `goblin` with `health: 40`, `source: design/gdd/combat.md`
- `design/gdd/combat.md` now says goblin health is 50; `git log` shows it changed after the registry entry was written
- No other GDD states a goblin health value

**Input:** `$gs-consistency-check entity:goblin`

**Domain checks:**
- [ ] The finding is classified ⚠️ STALE REGISTRY, distinct from 🔴 CONFLICT
- [ ] Preserve the case's unresolved human decisions and declines; perform routine writes already authorized, and ask only for missing decisions or scope.
- [ ] The approved update sets `revised:` and keeps the old value in a `# was:` comment
- [ ] Verdict after the write is COMPLETE
- [ ] `docs/consistency-failures.md` is not written for a stale-registry finding

---

### Case 4: Edge Case — Empty registry, no GDDs

**Fixture:**
- `modes.workflow` resolves to `full`
- `design/registry/entities.yaml` is the shipped stub with no entries
- `design/gdd/` is empty

**Input:** `$gs-consistency-check`

**Domain checks:**
- [ ] Skill outputs the empty-registry message naming `$gs-design-system`
- [ ] Use the linked native procedure and explicit runtime command; retired host execution is not required.
- [ ] No file is written, including `production/session-state/active.md`
- [ ] Skill does NOT crash or produce a partial report

---

### Case 4b: Edge Case — Registry populated, but no GDD in scope

**Fixture:**
- `modes.workflow` resolves to `full`
- `design/registry/entities.yaml` has 3 entities, each with a `source:` GDD
- `design/gdd/gdd-cross-review-[date].md` exists, and no system GDD has changed since it

**Input:** `$gs-consistency-check since-last-review`

**Domain checks:**
- [ ] Verdict is NOT ASSESSED, never PASS — nothing was compared
- [ ] The output names the filter that produced the empty scope
- [ ] No GDD is scanned and no conflict log entry is written

---

### Case 4c: Edge Case — Named entity is not in the registry

**Fixture:**
- `modes.workflow` resolves to `full`
- `design/registry/entities.yaml` has entities `goblin` and `orc_warlord`
- `design/gdd/` contains 3 system GDDs; one mentions a `goblin_shaman`

**Input:** `$gs-consistency-check entity:goblin_shaman`

**Domain checks:**
- [ ] Verdict is NOT ASSESSED naming the unregistered entity — never PASS
- [ ] The closest registered names are listed
- [ ] No GDD is scanned and nothing is written

---

### Case 5: Director Gate — No gate consulted in full review mode

**Fixture:**
- `project.yaml`: `modes.review_mode: full`, `modes.workflow: full`
- `design/registry/entities.yaml` has entries
- `design/gdd/` contains ≥2 GDDs

**Input:** `$gs-consistency-check`

**Domain checks:**
- [ ] No director gate agents are consulted (no CD-, TD-, PR-, AD- prefixed gates)
- [ ] The skill does not resolve or read the review mode — its config block asks only for `automation`, `workflow` and `system_overrides`
- [ ] Output contains no "Gate: [GATE-ID]" or gate-skipped entries
- [ ] Review mode `full` has no effect on this skill's behavior

---

### Case 6: Standard Workflow — Only the required GDD sections are compared

**Fixture:**
- `modes.workflow` resolves to `standard`
- Registry `constants:` has `crit_multiplier` value 1.5, `source: design/gdd/combat.md`
- `design/gdd/combat.md` `## Detailed Design` states `crit_multiplier = 1.5`
- `design/gdd/loot.md` states `crit_multiplier = 2.0` only in its `## Tuning Knobs` section, which `standard` does not require; no required section of `loot.md` states a value for it

**Input:** `$gs-consistency-check`

**Domain checks:**
- [ ] The Tuning Knobs value is not reported as a 🔴 CONFLICT at `standard`
- [ ] The report states the required-sections-only scope and names the mention it did not check — the narrower scan is not silent
- [ ] Verdict is PASS

---

### Case 6b: Standard Workflow — A per-system override makes one GDD `full`

**Fixture:**
- `modes.workflow` resolves to `standard`; `project.yaml` has
  `workflow_overrides.system_overrides.loot: full`
- Registry `constants:` has `crit_multiplier` value 1.5, `source: design/gdd/combat.md`
- `design/gdd/combat.md` `## Detailed Design` states `crit_multiplier = 1.5`
- `design/gdd/loot.md` states `crit_multiplier = 2.0` only in its `## Tuning Knobs` section

**Input:** `$gs-consistency-check`

**Domain checks:**
- [ ] The Tuning Knobs value in `loot.md` is compared, because its effective tier is `full` — the project tier alone would have skipped it (Case 6)
- [ ] The report names the GDD whose effective tier differs from the project's
- [ ] Verdict is CONFLICTS FOUND, not PASS
