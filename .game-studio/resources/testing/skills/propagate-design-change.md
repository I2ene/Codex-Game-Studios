# Evaluation scenarios: gs-propagate-design-change

Professional scenarios adapted from Donchitos' upstream testing guidance; see
[source attribution](../../../../NOTICE.md). These are evaluation inputs and domain
checks, not executed results. Read `.agents/skills/gs-propagate-design-change/SKILL.md` and its current procedure first.
Use [evaluation policy](../README.md) and [category rubric](../quality-rubric.md).

Resolve current config and project engine records. Apply review-mode discipline
coverage without claiming automatic delegation: use the parent when needed, label it,
and record actual participants only. Existing human authorization governs writes;
case approvals represent unresolved decisions and never revoke prior authorization.
Historical fixture versions are scenario inputs, not current API verification.
The linked native procedure governs command arguments, output schemas, receipts,
context and mode applicability. Missing inputs remain NOT ASSESSED.

### Case 1: Happy Path — GDD formula change affects one of two referencing ADRs

**Fixture:**
- `project.yaml`: `modes.workflow: full`, `modes.review_mode: lean`
- `design/gdd/combat.md` has an uncommitted edit to a damage formula in its
  Formulas section
- `docs/architecture/` has 4 ADRs; ADR-0003 and ADR-0005 list `combat.md` in
  `## GDD Requirements Addressed`; ADR-0003's decision assumed the old formula,
  ADR-0005's decision does not depend on it
- `docs/architecture/requirements-traceability.md` exists

**Input:** `$gs-propagate-design-change design/gdd/combat.md`

**Domain checks:**
- [ ] What changed is taken from `git diff`, not from reading two whole documents
- [ ] Only the 2 referencing ADRs are full-read; the other 2 are not described as verified unaffected
- [ ] The full impact report is shown before any resolution ask or write
- [ ] A resolution ask is made per Needs Review / Likely Superseded ADR, one at a time
- [ ] Each file change (ADR status, traceability index, impact report) has its own ask
- [ ] "TD-CHANGE-IMPACT skipped — Lean mode." appears
- [ ] Verdict is COMPLETE after the impact report is written

---

### Case 2: Zero matches — "no impact" versus "cannot trace"

**Fixture (tables present):**
- `project.yaml`: `modes.workflow: full`
- `design/gdd/combat.md` has an uncommitted edit
- 3 ADRs, each with a `## GDD Requirements Addressed` section, none naming
  `combat.md` in the table or in prose

**Input (both fixtures):** `$gs-propagate-design-change design/gdd/combat.md`

**Expected behavior (tables present):**
1. Both scans return 0 with N = 3
2. The files-with-matches check for `## GDD Requirements Addressed` is non-empty
3. Reports "No ADR references combat.md — no architecture impact."

**Fixture (tables absent):**
- Same GDD edit; 3 ADRs, none containing a `## GDD Requirements Addressed` section
  and none naming `combat.md`

**Expected behavior (tables absent):**
1. Both scans return 0 with N = 3; the section check is also empty
2. Reports "3 ADRs found, none contains a 'GDD Requirements Addressed' section —
   traceability cannot be computed (a `gate-pre-production` blocker). Run
   `$gs-architecture-decision retrofit [adr]`."

**Domain checks:**
- [ ] With tables present, the "no architecture impact" message is printed
- [ ] With tables absent, the skill does NOT report "no impact" — it reports that traceability cannot be computed and names `$gs-architecture-decision retrofit [adr]`, the form that skill parses
- [ ] No per-ADR resolution ask and no ADR edit happens in either fixture
- [ ] Skill does NOT error or crash when no references are found

---

### Case 3: Edge Case — Empty diff on a GDD with history

**Fixture:**
- `project.yaml`: `modes.workflow: full`
- `design/gdd/combat.md` is committed, has no uncommitted changes, and was not
  touched by the last commit

**Input:** `$gs-propagate-design-change design/gdd/combat.md`

**Domain checks:**
- [ ] Both diffs are tried, working tree first, then the last commit
- [ ] The "no uncommitted or last-commit changes" report is printed
- [ ] The user is asked which revision to propagate
- [ ] The empty diff is NOT reported as "no impact"

---

### Case 4: Edge Case — No argument provided

**Fixture:**
- Multiple GDDs exist in `design/gdd/`

**Input:** `$gs-propagate-design-change` (no argument)

**Domain checks:**
- [ ] Skill outputs the usage message when no argument is given
- [ ] The usage example shows the `design/gdd/[system].md` path format
- [ ] No `git diff` or ADR scan is performed without a target GDD
- [ ] Skill does NOT silently pick a GDD without user input

---

### Case 5: Director Gate — TD-CHANGE-IMPACT returns CONCERNS in full mode

**Fixture:**
- `project.yaml`: `modes.workflow: full`, `modes.review_mode: full`
- A GDD edit that leaves one referencing ADR classified Needs Review
- TD-CHANGE-IMPACT returns CONCERNS: a second ADR was under-classified

**Input:** `$gs-propagate-design-change design/gdd/[system].md`

**Domain checks:**
- [ ] TD-CHANGE-IMPACT is consulted after the impact report is shown and before any resolution ask
- [ ] The gate receives the full report (change summary, classifications, recommended actions)
- [ ] The CONCERNS name the flagged ADR and all three options are offered
- [ ] No ADR, traceability or report file is written before the CONCERNS are answered
- [ ] No "TD-CHANGE-IMPACT skipped" note appears in `full` mode

---

### Case 6: Workflow tiers — `minimal` stops before the cascade; `standard` narrows it

**Fixture (minimal):**
- `project.yaml` sets no `modes` keys — `modes.rigor` defaults to `minimal`, so
  the workflow resolves to `minimal`
- `design/gdd/loot.md` has an uncommitted edit

**Fixture (standard):**
- `project.yaml`: `modes.workflow: standard`, `modes.review_mode: solo`
- `design/gdd/loot.md` has an uncommitted edit
- 4 ADRs, by their Engine Compatibility `Layer`: ADR-0001 (Foundation, event bus,
  no mention of `loot.md`), ADR-0002 (Foundation, save system, lists `loot.md` in
  `## GDD Requirements Addressed`), ADR-0006 (Feature, loot tables, names `loot.md`
  in prose only), ADR-0007 (Feature, enemy AI, no mention)

**Input (both fixtures):** `$gs-propagate-design-change design/gdd/loot.md`

**Expected behavior (minimal):**
1. The diff and Change Summary run as usual
2. At the ADR step: "No ADR cascade at minimal workflow — design change recorded;
   no architecture impact analysis." and the skill stops

**Expected behavior (standard):**
1. The in-scope set is the Foundation ADRs plus any ADR referencing `loot.md`:
   ADR-0001, ADR-0002 and ADR-0006, so N = 3; ADR-0007 is out of scope
2. Reports "Loaded 3 ADRs by scan. 2 reference loot.md (1 via requirements table,
   1 via prose reference only)."
3. Full-reads only ADR-0002 and ADR-0006; notes "TD-CHANGE-IMPACT skipped — Solo mode."

**Domain checks:**
- [ ] Minimal: no ADR is globbed or read, no gate is consulted or noted, and no write ask is made
- [ ] Standard: ADR-0007 is not counted or read, and neither it nor ADR-0001 is described as verified unaffected
- [ ] Standard: the prose-only reference in ADR-0006 is caught by the basename grep
- [ ] Standard: the Foundation ADRs are found from the `**Layer**` rows (`Grep pattern="\*\*Layer\*\*" glob="docs/architecture/adr-*.md"`), not guessed from titles
- [ ] Variant — ADR-0007 has no `**Layer**` row: it is treated as critical (when in doubt, critical) and joins the in-scope set, so N = 4
