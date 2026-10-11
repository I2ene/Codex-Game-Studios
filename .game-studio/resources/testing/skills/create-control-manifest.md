# Evaluation scenarios: gs-create-control-manifest

Professional scenarios adapted from Donchitos' upstream testing guidance; see
[source attribution](../../../NOTICE.md). These are evaluation inputs and domain
checks, not executed results. Read `.agents/skills/gs-create-control-manifest/SKILL.md` and its current procedure first.
Use [evaluation policy](../README.md) and [category rubric](../quality-rubric.md).

Resolve current config and project engine records. Apply review-mode discipline
coverage without claiming automatic delegation: use the parent when needed, label it,
and record actual participants only. Existing human authorization governs writes;
case approvals represent unresolved decisions and never revoke prior authorization.
Historical fixture versions are scenario inputs, not current API verification.
The linked native procedure governs command arguments, output schemas, receipts,
context and mode applicability. Missing inputs remain NOT ASSESSED.

### Case 1: Happy Path — 4 Accepted ADRs create a correct manifest

**Fixture:**
- `docs/architecture/` contains `adr-0001-*.md` … `adr-0004-*.md`, each with a
  `## Status` section reading `Accepted`
- Each ADR has `## Decision` (with "must"/"always" statements) and
  `## Alternatives Considered` (with rejected alternatives)
- No existing `docs/architecture/control-manifest.md`
- Review mode resolves to `solo`

**Input:** `$gs-create-control-manifest`

**Domain checks:**
- [ ] All 4 Accepted ADRs are listed under `ADRs Covered` in the manifest header
- [ ] Each layer section has `### Required Patterns` and `### Forbidden Approaches`
- [ ] Every rule carries its source — `— source: [ADR-NNNN]` for a layer rule; a global rule names its `project.yaml` / `technical-preferences.md` key or engine-reference file (e.g. `deprecated-apis.md`)
- [ ] Preserve the case's unresolved human decisions and declines; perform routine writes already authorized, and ask only for missing decisions or scope.
- [ ] "TD-MANIFEST skipped — Solo mode." appears; no technical-director is consulted
- [ ] Verdict is COMPLETE after writing

---

### Case 2: Failure Path — No ADRs found

**Fixture:**
- `docs/architecture/` directory exists but contains no `adr-*.md` files

**Input:** `$gs-create-control-manifest`

**Domain checks:**
- [ ] The "No ADRs found" message is printed
- [ ] Skill recommends `$gs-architecture-decision` as the next action
- [ ] Preserve the case's unresolved human decisions and declines; perform routine writes already authorized, and ask only for missing decisions or scope.
- [ ] Verdict COMPLETE is NOT emitted (the skill stops at Phase 1)

---

### Case 3: Mixed ADR Statuses — Only Accepted ADRs included

**Fixture:**
- `docs/architecture/` contains 5 ADRs: 3 with `## Status` Accepted, 2 with
  `## Status` Proposed (ADR-0004, ADR-0005)

**Input:** `$gs-create-control-manifest`

**Domain checks:**
- [ ] Status is resolved with the `^## Status` Grep before any ADR section is read
- [ ] The preview's `ADRs covered` and the manifest's `ADRs Covered` list exactly the 3 Accepted ADRs
- [ ] Both excluded ADRs are named, with their status, in the preview the user sees before approving — the skill does not silently omit them
- [ ] No rule in the manifest is sourced from either Proposed ADR
- [ ] The "none Accepted — proceed with Proposed or stop?" ask is NOT shown for this fixture

---

### Case 4: Edge Case — Regenerating an existing manifest

**Fixture:**
- `docs/architecture/control-manifest.md` already exists with
  `Manifest Version` and `Last Updated` both dated last week
- `docs/architecture/` contains Accepted ADRs, one of them accepted since then
- `production/epics/` already holds epics with stories, so the first-run
  `$gs-create-epics` next step does not apply

**Input:** `$gs-create-control-manifest update`

**Domain checks:**
- [ ] Preserve the case's unresolved human decisions and declines; perform routine writes already authorized, and ask only for missing decisions or scope.
- [ ] The newly accepted ADR appears in `ADRs Covered`
- [ ] `Manifest Version` equals `Last Updated` and is the generation date (not a v1→v2 counter)
- [ ] The regeneration next-step ("Updated. Recommend notifying the team…") is shown instead of the first-run `$gs-create-epics` handoff

---

### Case 5: Director Gate — TD-MANIFEST in full review mode returns REJECT

**Fixture:**
- 4 Accepted ADRs exist
- Review mode resolves to `full`
- TD-MANIFEST returns REJECT, naming one rule that has no source ADR

**Input:** `$gs-create-control-manifest`

**Domain checks:**
- [ ] TD-MANIFEST is consulted only after the Phase 4 summary is accepted
- [ ] The gate receives the rule list, ADRs covered and engine version
- [ ] On REJECT no manifest file is written
- [ ] The flagged rule is revised and the summary re-presented before any write ask
- [ ] No "TD-MANIFEST skipped" note appears in `full` mode

---

### Case 6: Edge Case — No Accepted ADR, and ADRs with no `## Status`

**Fixture (none Accepted):**
- `docs/architecture/` contains 3 ADRs, each with `## Status` Proposed

**Fixture (malformed):**
- `docs/architecture/` contains 3 ADRs, none with a `## Status` section

**Input (both fixtures):** `$gs-create-control-manifest`

**Expected behavior (none Accepted):**
1. N = 3; the `^## Status` Grep matches 3, none reading Accepted
2. Reports "3 ADRs found, none Accepted. A manifest built from Proposed ADRs would
   encode decisions that may still change." and asks whether to proceed with the
   Proposed ADRs or stop

**Expected behavior (malformed):**
1. N = 3; the `^## Status` Grep matches nothing
2. Reports "3 ADRs found, none has a `## Status` section — acceptance cannot be
   determined. Run `$gs-architecture-decision retrofit [file]` on each." and stops

**Domain checks:**
- [ ] None Accepted: the ask is shown and no empty manifest is written
- [ ] Malformed: the run stops — the ADRs are not treated as Accepted and no manifest is written
- [ ] Malformed: the retrofit command reads `$gs-architecture-decision retrofit [file]` — the form that skill parses
- [ ] Preserve the case's unresolved human decisions and declines; perform routine writes already authorized, and ask only for missing decisions or scope.
