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
are placeholders and origin is the user's own. User selects An idea, or none yet (none), saves Concept/minimal
and selects guided automation.

**Input:** `$gs-start`

**Domain checks:**
- [ ] Read project-state before asking A–D with Make me a game first; defer engine choice to setup-engine. Initially offer
  brainstorm open and defer the full path until the rigor is known.
- [ ] Show why Concept and minimal fit; do not ask a second standalone rigor question. Save only
  the selected project.stage and project.goal under one project block, and modes.rigor and modes.automation under one modes block. Do not write
  either legacy mirror or the six derived leaves.
- [ ] Name the minimal path with prototype after brainstorm and before setup-engine and close with the chosen handoff, without auto-starting it in
  this onboarding-only fixture. COMPLETE means oriented, not game work executed.
- [ ] Show the goal on the card as guessed from the person's words (hobby for none, sell for commercial/Steam), with Save/Change/Don't save. Save only an accepted guess or explicit card edit; never seed derived mode leaves or legacy mirrors.

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
- [ ] Direct the returning contributor to `$gs-next-step` after reporting the actual brief and
  resolved review mode.

---

### Case 3: Existing Unity work — observed stage and selected state are distinct

**Fixture:** Unity, project.goal sell, explicit standard rigor and collaborative automation; source under Assets/Scripts, three
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
- [ ] Fixture already sets project.goal sell: keep it as already set, without guessing, asking again or rewriting it.

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
- [ ] Show the goal on the card as guessed from the person's words (hobby for none, sell for commercial/Steam), with Save/Change/Don't save. Save only an accepted guess or explicit card edit; never seed derived mode leaves or legacy mirrors.
- [ ] After saving the commercial/Steam card, project.goal sell is persisted alongside the selected stage and rigor; a declined save changes neither goal nor automation.

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
- [ ] Show the goal on the card as guessed from the person's words (hobby for none, sell for commercial/Steam), with Save/Change/Don't save. Save only an accepted guess or explicit card edit; never seed derived mode leaves or legacy mirrors.

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

---

### Case 9: Make-game onboarding handoff writes no settings

**Fixture:** Fresh project; typed start and user chooses Make me a game. Variant: configured Godot without concept.

**Input:** $gs-start

**Domain checks:**
- [ ] Skip the stage/rigor/goal card, save and automation questions; write no settings. Name prototype as the next step.
- [ ] Godot variant explains the throwaway engine route and optional browser sketch. Model-pin differences never prescribe tool calls or new authorization.

---

### Case 10: An existing plain-language build request continues directly

**Fixture:** User already asks for a sheep-herding game; the system routes through start. Contrast: typed start alone.

**Input:** make me a game where you herd sheep with a dog

**Domain checks:**
- [ ] Use the original request and continue the authorized prototype route without repeating onboarding or inventing intent; preserve required build-card decisions.
- [ ] Do not write onboarding config or issue a competing completion verdict. Typed-start-only remains a handoff request, not automatic build authorization.

---

### Case 11: Clear concept offers build-now only as the appropriate route

**Fixture:** Fresh no-engine project; clear top-down flood-racing concept. Variants: Unity configured, or Godot named in the sentence.

**Input:** $gs-start

**Domain checks:**
- [ ] No-engine options place Build it now first, followed by formalize/jump routes. Choosing it skips settings and names prototype.
- [ ] Known/named engine variants offer formalize, engine setup/continuation and a nonrecommended browser sketch; never silently convert the selected engine.

---

### Case 12: A changed goal on the card overrides its guess

**Fixture:** Cozy farming description initially suggests hobby; user changes goal to selling on Steam, then saves. Variant: stored jam changed to portfolio.

**Input:** $gs-start

**Domain checks:**
- [ ] Show hobby as guessed without a separate goal question. Redisplay sell as user-provided, write nothing before the applicable save choice, then save sell with selected settings.
- [ ] A changed existing goal is saved too; unchanged stored goal is kept. Don't save preserves files, including automation and legacy mirrors.

---

### Case 13: Standard path retains the main route and studio ladder

**Fixture:** Standard rigor; clear river-town trading concept, formalize first; compare existing-work route.

**Input:** $gs-start

**Domain checks:**
- [ ] For new work place make/play/change/Grow before the correctly ordered standard studio path; explain studio fits team, long project or desired paperwork once.
- [ ] Keep every applicable professional step. Existing-work variant retains the studio explanation and its own path without the new-game main-path preface.
