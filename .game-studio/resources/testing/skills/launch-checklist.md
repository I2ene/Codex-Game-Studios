# Evaluation scenarios: gs-launch-checklist

Professional scenarios adapted from Donchitos' upstream testing guidance; see
[source attribution](../../../../NOTICE.md). These are evaluation inputs and domain
checks, not executed results. Read `.agents/skills/gs-launch-checklist/SKILL.md` and its current procedure first.
Use [evaluation policy](../README.md) and [category rubric](../quality-rubric.md).

Resolve current config and project engine records. Apply review-mode discipline
coverage without claiming automatic delegation: use the parent when needed, label it,
and record actual participants only. Existing human authorization governs writes;
case approvals represent unresolved decisions and never revoke prior authorization.
Historical fixture versions are scenario inputs, not current API verification.
The linked native procedure governs command arguments, output schemas, receipts,
context and mode applicability. Missing inputs remain NOT ASSESSED.

### Case 1: Happy Path — Steam project, clean scans, every section confirmed, READY

**Fixture:**
- `project.yaml`: `project.stage: Release`, `modes.rigor: standard`, `platform.cert_tier: steam`,
  engine Godot (code root `src/`); a single-player game with no servers
- `src/` has 40 source files with no TODO/FIXME/HACK, no debug output, no placeholder or hardcoded dev values
- `assets/` exists with final assets
- `production/releases/` does not exist yet
- In Phase 4b the user answers `Yes — all of them` for every section, except the
  Infrastructure question, where `Some differ` gives each Servers item N/A and
  every Analytics and Monitoring item yes

**Input:** `$gs-launch-checklist 2026-11-01`

**Domain checks:**
- [ ] Every Phase 3 scan line shows its denominator (`scanned [N] files, [M] hits`)
- [ ] No console (TRC/Lotcheck) or itch.io items appear
- [ ] The soak-test item does not require a soak longer than `$gs-soak-test` offers
- [ ] Phase 4b asks at most one question per section, and no Phase 3 count is asked about
- [ ] Overall Status is READY — every item is ticked on evidence or on a Phase 4b answer, or marked N/A
- [ ] The summary gives total, blocking, conditional and not-assessed counts
- [ ] Preserve the case's unresolved human decisions and declines; perform routine writes already authorized, and ask only for missing decisions or scope.
- [ ] Next steps name `$gs-team-release` and do not offer `$gs-gate-check`

---

### Case 2: Blocking Findings — FIXMEs and debug output

**Fixture:**
- As Case 1, but `src/` contains 3 `FIXME` comments and one `print()` debug call in production code
- `src/` also has one `HACK` comment whose justification is documented beside it

**Input:** `$gs-launch-checklist 2026-11-01`

**Domain checks:**
- [ ] FIXME count is 3, with file locations
- [ ] The debug `print()` is reported and its item is not ticked
- [ ] Blocking Items lists the FIXMEs and the debug output
- [ ] The documented HACK is under Conditional Items, not Blocking Items
- [ ] Overall Status is NOT READY (not READY, CONDITIONAL or NOT ASSESSED)

---

### Case 3: Cert Tier Unset — Ask, do not emit every track

**Fixture:**
- `project.yaml`: `project.stage: Release`, `modes.rigor: standard`, no `platform.cert_tier`
- Config block shows `platform.cert_tier: (unset -- ask which platforms are in scope)`

**Input:** `$gs-launch-checklist 2026-11-01`

**Domain checks:**
- [ ] Skill asks which platforms are in scope
- [ ] Console, Steam and itch.io blocks are never all emitted together
- [ ] Without an answer, the section reads `NOT ASSESSED — cert tier unknown`
- [ ] The "omitted — cert_tier is 'none'" line does not appear

---

### Case 4: Nothing to Scan — `[?]` items, not green ticks

**Fixture:**
- `project.yaml`: `project.stage: Release`, `platform.cert_tier: itch`, engine Godot
- `src/` exists but is empty; no `assets/` directory

**Input:** `$gs-launch-checklist 2026-11-01`

**Domain checks:**
- [ ] No scan with no input is reported as zero hits
- [ ] "All placeholder art replaced with final assets" is `- [?]`, not ticked and not `- [ ]`
- [ ] The `[?]` legend appears
- [ ] No Steamworks or console items appear
- [ ] Overall Status is NOT ASSESSED and names the `[?]` scans (code and placeholder-asset scans); it is not READY or CONDITIONAL

---

### Case 5: Director Gate Check — Dry run, cert tier `none`

**Fixture:**
- `project.yaml`: `project.stage: Release`, `platform.cert_tier: none`
- Code root with source files

**Input:** `$gs-launch-checklist dry-run`

**Domain checks:**
- [ ] The "omitted — cert_tier is 'none'" line appears and no certification rows are emitted
- [ ] No Phase 4b question is asked in dry-run, the skip is stated, and the Overall Status is NOT ASSESSED
- [ ] Preserve the case's unresolved human decisions and declines; perform routine writes already authorized, and ask only for missing decisions or scope.
- [ ] No director gate is invoked and no gate skip messages appear
- [ ] Next steps name `$gs-team-release` and do not offer `$gs-gate-check`

---

### Case 6: Stage Still Polish — Answers Make It CONDITIONAL, or NOT ASSESSED

**Fixture:**
- As Case 1, but `project.stage: Polish` and `modes.rigor: full` (`workflow: full`)
- Variant A: in Phase 4b the Marketing items all get yes except "Press/influencer
  review keys distributed", answered `not yet` — the user says the keys go out on
  launch morning and the producer accepts the risk; every other section is `Yes —
  all of them` (Servers N/A as in Case 1)
- Variant B: as Variant A, but the user leaves the Legal question unanswered

**Input:** `$gs-launch-checklist 2026-11-01`

**Domain checks:**
- [ ] A `not yet` answer is never ticked; with an accepted risk it is listed under Conditional Items
- [ ] Variant A's Overall Status is CONDITIONAL
- [ ] Variant B's Overall Status is NOT ASSESSED and names the unanswered Legal items
- [ ] No "documented exception" is offered for an S2 or S3 at `workflow: full`
- [ ] Next steps name `$gs-gate-check release` before `$gs-team-release`
