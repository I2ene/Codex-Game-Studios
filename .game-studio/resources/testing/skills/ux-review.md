# Evaluation scenarios: gs-ux-review

Professional scenarios adapted from Donchitos' upstream testing guidance; see
[source attribution](../../../NOTICE.md). These are evaluation inputs and domain
checks, not executed results. Read `.agents/skills/gs-ux-review/SKILL.md` and its current procedure first.
Use [evaluation policy](../README.md) and [category rubric](../quality-rubric.md).

Resolve current config and project engine records. Apply review-mode discipline
coverage without claiming automatic delegation: use the parent when needed, label it,
and record actual participants only. Existing human authorization governs writes;
case approvals represent unresolved decisions and never revoke prior authorization.
Historical fixture versions are scenario inputs, not current API verification.
The linked native procedure governs command arguments, output schemas, receipts,
context and mode applicability. Missing inputs remain NOT ASSESSED.

### Case 1: Happy Path — Complete UX spec, APPROVED

**Fixture:**
- `design/ux/inventory.md` follows `.game-studio/resources/docs/templates/ux-spec.md`: header with Status, Author, Platform Target (PC, Console), Related GDDs (`design/gdd/inventory.md`), Accessibility Tier and `> **Template**: UX Spec`; every section populated, including States & Variants (loading, empty, populated, error), keyboard and d-pad navigation with focus order, an Input Method Completeness Checklist block for keyboard/mouse and for gamepad with every item ticked, and at least 5 testable acceptance criteria
- `design/accessibility-requirements.md` commits the Standard tier
- `design/ux/interaction-patterns.md` exists, and every interactive component in the spec names a pattern from it
- `project.yaml` `platform` block: `targets: [PC, Console]`, `gamepad_support: Full`
- `design/gdd/inventory.md` UI Requirements are all addressed by the spec

**Input:** `$gs-ux-review design/ux/inventory.md`

**Domain checks:**
- [ ] Input method coverage is checked against the `project.yaml` platform block, not only the spec header
- [ ] The UX spec checklist (Phase 3A) is used, including States & Variants, Interaction Map coverage and the Input Method Completeness Checklist item
- [ ] Every review dimension has something to check against — the committed tier, the pattern library, the referenced GDD — so none is NOT ASSESSED
- [ ] Accessibility is checked against the tier committed in `design/accessibility-requirements.md`
- [ ] Verdict is APPROVED with the `$gs-team-ui` handoff
- [ ] No files are written

---

### Case 2: Empty Accessibility Section — NEEDS REVISION

**Fixture:**
- Same as Case 1, but the spec's Accessibility section is empty
- `design/accessibility-requirements.md` commits the Standard tier

**Input:** `$gs-ux-review design/ux/inventory.md`

**Domain checks:**
- [ ] NEEDS REVISION is returned (not APPROVED or MAJOR REVISION NEEDED)
- [ ] Findings name the section and give a specific fix
- [ ] The handoff is to fix the issues and re-run `$gs-ux-review`
- [ ] The skill offers help but does not auto-fix, and no files are written

---

### Case 3: Incomplete States — NEEDS REVISION outranks NOT ASSESSED

**Fixture:**
- `design/ux/settings-menu.md` follows the UX spec template, carries `> **Template**: UX Spec`, and is otherwise complete
- Its States & Variants section documents only the populated state — no loading, empty or error state; the screen fetches its data asynchronously
- `design/ux/interaction-patterns.md` exists and the spec's components name patterns from it
- No `design/accessibility-requirements.md`, so there is no committed tier

**Input:** `$gs-ux-review design/ux/settings-menu.md`

**Domain checks:**
- [ ] NEEDS REVISION is returned, not NOT ASSESSED — NOT ASSESSED ranks below the revision verdicts
- [ ] The not-assessed Accessibility dimension is still named in the report
- [ ] The missing loading, empty and error states are each named in the output
- [ ] MAJOR REVISION NEEDED is not returned for this fixable gap
- [ ] The handoff is to re-run `$gs-ux-review` after the fix

---

### Case 4: Nothing to Assess Against — NOT ASSESSED

**Fixture:**
- Scenario (a): `design/ux/inventory-screen.md` does not exist
- Scenario (b): `design/ux/inventory.md` is complete (as in Case 1), but `design/accessibility-requirements.md` does not exist; the spec header states "Accessibility Tier: Standard"

**Input:** (a) `$gs-ux-review design/ux/inventory-screen.md` (b) `$gs-ux-review design/ux/inventory.md`

**Domain checks:**
- [ ] In variant (b), carry the spec header’s Standard tier forward as an assumption, never as the project’s committed accessibility tier.
- [ ] (a) A missing spec yields NOT ASSESSED naming the path, with no checklist output
- [ ] (b) Accessibility is reported NOT ASSESSED, not COMPLIANT, when no tier is committed
- [ ] (b) `$gs-ux-design accessibility` is recommended
- [ ] The report does not recommend handing off to `$gs-team-ui` on a NOT ASSESSED result
- [ ] No files are written

---

### Case 5: `all` Argument and No Director Gate

**Fixture:**
- `design/ux/` contains `hud.md` (written by `$gs-ux-design hud`, header line `> **Template**: HUD Design`), `inventory.md` (written by `$gs-ux-design inventory`, `> **Template**: UX Spec`) and `pause-menu.md` (hand-written from `.game-studio/resources/docs/templates/ux-spec.md`, with no Template line)
- `project.yaml` has `modes.review_mode: full`

**Input:** `$gs-ux-review all`

**Domain checks:**
- [ ] The `all` run covers every file under `design/ux/`, presents a file / verdict / primary issue summary first, then a full report for each file.
- [ ] Preserve the case's unresolved human decisions and declines; perform routine writes already authorized, and ask only for missing decisions or scope.
- [ ] Each document's checklist comes from its Template line (HUD vs UX spec)
- [ ] A file without a Template line is classified by name, and the report says which checklist was assumed
- [ ] No director gate is invoked and no gate skip messages appear
- [ ] Every verdict comes from the skill's four-verdict set
