# Evaluation scenarios: gs-start

Professional scenarios adapted from Donchitos' upstream testing guidance; see
[source attribution](../../../NOTICE.md). These are evaluation inputs and domain
checks, not executed results. Read `.agents/skills/gs-start/SKILL.md` and its current procedure first.
Use [evaluation policy](../README.md) and [category rubric](../quality-rubric.md).

Resolve current config and project engine records. Apply review-mode discipline
coverage without claiming automatic delegation: use the parent when needed, label it,
and record actual participants only. Existing human authorization governs writes;
case approvals represent unresolved decisions and never revoke prior authorization.
Historical fixture versions are scenario inputs, not current API verification.
The linked native procedure governs command arguments, output schemas, receipts,
context and mode applicability. Missing inputs remain NOT ASSESSED.

### Case 1: Fresh project — propose minimal rigor, then save only selected settings

**Fixture:** No project YAML, stage mirror, design docs, prototype or source; legacy technical preferences
are placeholders and origin is the user's own. User selects No idea yet, saves Concept/minimal
and selects guided automation.

**Input:** `$gs-start`

**Domain checks:**
- [ ] Read project-state before asking A–D; defer engine choice to setup-engine. Initially offer
  brainstorm open and defer the full path until the rigor is known.
- [ ] Show why Concept and minimal fit; do not ask a second standalone rigor question. Save only
  the selected project.stage, modes.rigor and modes.automation, in one modes block. Do not write
  either legacy mirror or the six derived leaves.
- [ ] Name the minimal four steps and close with the chosen handoff, without auto-starting it in
  this onboarding-only fixture. COMPLETE means oriented, not game work executed.

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
- [ ] Direct the returning contributor to `$gs-help` after reporting the actual brief and
  resolved review mode.

---

### Case 3: Existing Unity work — observed stage and selected state are distinct

**Fixture:** Unity, explicit standard rigor and collaborative automation; source under Assets/Scripts, three
system GDDs, no concept/ADRs. The user selects Existing work and chooses to save the proposed
Systems Design stage.

**Input:** `$gs-start`

**Domain checks:**
- [ ] Find source under Assets, name the observed basis for the stage suggestion and route to
  project-stage-detect and adopt. Do not treat the suggestion as authorization or a passed gate.
- [ ] Write the selected project.stage via native settings and verify the value/provenance. Keep
  existing rigor and automation without asking them again or creating/synchronizing a mirror.
- [ ] Show the applicable standard retrofit path including GDD, ADR and registry checks; end
  COMPLETE after handing off.

---

### Case 4: Template origin is reported without remote mutation

**Fixture:** Fresh project as in Case 1, origin points to the upstream Donchitos template (vary URL casing).
The user describes a small weekend puzzler and agrees to the proposed configuration.

**Input:** `$gs-start`

**Domain checks:**
- [ ] Route to brainstorm with the user's hint and explain the minimal rigor recommendation from
  those words.
- [ ] Report the template-origin issue once and suggest configuring the user's intended
  publishing destination. Do not mutate Git remotes, prescribe pulling template history into a
  consumer, or publish anything.

---

### Case 5: Onboarding has no phase gate

**Fixture:** Fresh project and user choices from Case 1.

**Input:** `$gs-start`

**Domain checks:**
- [ ] Reach COMPLETE after the handoff without invoking a director gate or printing a gate
  verdict or skip.

---

### Case 6: Existing work with unset rigor proposes a grounded value

**Fixture:** Godot, no modes block, GDScript source and four system GDDs without ADRs. User selects Existing
work and describes a commercial game for Steam with one core loop. A: saves suggested
configuration and selects collaborative. B: declines save.

**Input:** `$gs-start`

**Domain checks:**
- [ ] Name stage detection first, then explain the proposed Systems Design and standard rigor
  using project facts and user words. Name settings as the later edit path; defer the standard
  retrofit path until rigor is resolved.
- [ ] A: persist only selected stage, rigor and automation in their proper parents. Keep a
  single modes block with no six derived leaves or new mirrors. B: report values not saved; do
  not write automation or any other config.

---

### Case 7: Extend one existing modes block without changing its override

**Fixture:** Godot and existing `modes.review_mode: lean`, no rigor or automation, no concept/brief. User has
no idea yet, selects the proposed Concept/minimal settings, then chooses guided automation.

**Input:** `$gs-start`

**Domain checks:**
- [ ] Apply only the selected settings under the existing YAML parents. Keep one `modes:` block
  with review_mode lean, rigor minimal and automation guided; never seed the other rigor-derived
  knobs or a legacy mirror.
- [ ] Use existing authorization for routine writes; keep the choice of stage and settings
  distinct from any observed project state.

---

### Case 8: Minimal existing-work path explains where the brief comes from

**Fixture:** Minimal/collaborative Godot; 14 GDScript files implementing an existing game, two GDDs, no
architecture, concept or brief. User chooses existing-work routing. B: four early source files
with no existing game. C: brief exists.

**Input:** `$gs-start`

**Domain checks:**
- [ ] A: recommend stage detection/adoption as applicable and `$gs-reverse-document design src/`
  for the brief. B: recommend `$gs-brainstorm` for the brief. Do not demand GDD/ADR/registry
  retrofit for minimal or treat file count as a completed phase.
- [ ] C: retain the returning-work path instead of rerunning onboarding. No skill is started or
  stage persisted merely because a route is shown.
