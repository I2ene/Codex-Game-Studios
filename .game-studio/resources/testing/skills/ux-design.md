# Evaluation scenarios: gs-ux-design

Professional scenarios adapted from Donchitos' upstream testing guidance; see
[source attribution](../../../../NOTICE.md). These are evaluation inputs and domain
checks, not executed results. Read `.agents/skills/gs-ux-design/SKILL.md` and its current procedure first.
Use [evaluation policy](../README.md) and [category rubric](../quality-rubric.md).

Resolve current config and project engine records. Apply review-mode discipline
coverage without claiming automatic delegation: use the parent when needed, label it,
and record actual participants only. Existing human authorization governs writes;
case approvals represent unresolved decisions and never revoke prior authorization.
Historical fixture versions are scenario inputs, not current API verification.
The linked native procedure governs command arguments, output schemas, receipts,
context and mode applicability. Missing inputs remain NOT ASSESSED.

### Case 1: Happy Path — New HUD design

**Fixture:**
- No `design/ux/hud.md`
- `design/gdd/combat.md` and `design/gdd/stamina.md` have `## UI Requirements` sections; `design/gdd/save-system.md` has none
- `project.yaml` has a `platform` block (`targets: [PC]`, `gamepad_support: Full`)
- `design/gdd/game-concept.md` and `design/player-journey.md` exist

**Input:** `$gs-ux-design hud`

**Domain checks:**
- [ ] A GDD without a UI Requirements section is listed and confirmed with the user, not silently excluded
- [ ] `game-concept.md` is not counted as a system GDD, so it is not listed as unmatched
- [ ] Input methods come from the `project.yaml` `platform` block, without asking the user
- [ ] Preserve the case's unresolved human decisions and declines; perform routine writes already authorized, and ask only for missing decisions or scope.
- [ ] The HUD skeleton includes the sections `$gs-ux-review` Phase 3B checks for: HUD Philosophy, Information Architecture, Layout Zones, HUD element specifications, HUD States by Gameplay Context, Information Hierarchy, Visual Budget, Feedback & Notification Systems, Platform Adaptation, Tuning Knobs, Acceptance Criteria
- [ ] Of the three per-mode guidance files only `sections-hud.md` is loaded, and no guide is read whole
- [ ] The handoff names `$gs-ux-review` as required before implementation, and the verdict is `COMPLETE`

---

### Case 2: Existing Document — Retrofit of incomplete sections only

**Fixture:**
- Scenario (a): `design/ux/main-menu.md` exists, built from the UX spec skeleton; Purpose & Player Need, Player Context on Arrival, Navigation Position and Entry & Exit Points have real content; every other section is `[To be designed]`
- Scenario (b): `design/accessibility-requirements.md` exists, built from the accessibility skeleton; Accessibility Tier Definition commits the Standard tier; every other section is `[To be designed]`

**Input:** (a) `$gs-ux-design main-menu` (b) `$gs-ux-design accessibility`

**Domain checks:**
- [ ] The existing file is detected and no skeleton is written
- [ ] The status table and the "incomplete sections only" message are shown before authoring
- [ ] Only Empty or Placeholder sections are authored; complete sections are not overwritten
- [ ] Preserve the case's unresolved human decisions and declines; perform routine writes already authorized, and ask only for missing decisions or scope.
- [ ] (a) The status table rows use the section names of the UX spec skeleton (e.g., `Purpose & Player Need`, `Layout Specification`, `States & Variants`, `Input Method Completeness Checklist`)
- [ ] (b) The status table rows use the accessibility skeleton's section names (e.g., `Accessibility Tier Definition`, `Visual Accessibility`, `Motor Accessibility`), and the file stays at `design/accessibility-requirements.md`

---

### Case 3: Missing Context — No game concept and no player journey

**Fixture:**
- No `design/gdd/game-concept.md` and no `design/game-brief.md`
- No `design/player-journey.md`
- No `design/ux/inventory.md`

**Input:** `$gs-ux-design inventory`

**Domain checks:**
- [ ] The missing concept produces the `$gs-brainstorm` warning, and the skill proceeds only on the user's say-so
- [ ] The missing player journey is noted in the conversation and recorded in Open Questions with the template path
- [ ] The remediation points at the template, never back at `$gs-ux-design`
- [ ] The context summary marks the journey phase as unknown

---

### Case 4: No Argument Provided — Ask instead of failing

**Fixture:**
- No argument
- Neither `design/ux/main-menu.md` nor `design/accessibility-requirements.md` exists, so both scenarios author fresh files
- Scenario (a): the user types "Main Menu"
- Scenario (b): the user picks "The project-wide accessibility requirements"

**Input:** `$gs-ux-design`

**Domain checks:**
- [ ] No usage error; the "What are we designing today?" question is asked with the five options
- [ ] (a) A typed screen name becomes a kebab-case filename under `design/ux/`
- [ ] (b) Accessibility mode writes to `design/accessibility-requirements.md`
- [ ] (b) The tier definition is authored before the other accessibility sections
- [ ] Preserve the case's unresolved human decisions and declines; perform routine writes already authorized, and ask only for missing decisions or scope.

---

### Case 5: No Director Gate — `$gs-ux-review` is the separate review

**Fixture:**
- `project.yaml` has `modes.review_mode: full` and a `platform` block (`targets: [PC, Console]`, `gamepad_support: Full`)
- No `design/ux/settings-menu.md`

**Input:** `$gs-ux-design settings-menu`

**Domain checks:**
- [ ] The skeleton header's Platform Target line names the targets and input methods from the `platform` block
- [ ] No director gate is invoked and no gate skip messages appear
- [ ] `modes.review_mode: full` does not change the skill's behavior
- [ ] Specialist output is presented to the user; agents never write files
- [ ] The verdict is `COMPLETE`, with `$gs-ux-review` named as the validation step
