# Evaluation scenarios: gs-prototype

Professional scenarios adapted from Donchitos' upstream testing guidance; see
[source attribution](../../../NOTICE.md). These are evaluation inputs and domain
checks, not executed results. Read `.agents/skills/gs-prototype/SKILL.md` and its current procedure first.
Use [evaluation policy](../README.md) and [category rubric](../quality-rubric.md).

Resolve current config and project engine records. Apply review-mode discipline
coverage without claiming automatic delegation: use the parent when needed, label it,
and record actual participants only. Existing human authorization governs writes;
case approvals represent unresolved decisions and never revoke prior authorization.
Historical fixture versions are scenario inputs, not current API verification.
The linked native procedure governs command arguments, output schemas, receipts,
context and mode applicability. Missing inputs remain NOT ASSESSED.

### Case 1: Happy Path — Engine Prototype, PROCEED

**Fixture:**
- Explicit standard workflow for the concept prototype handoff (Case 6 covers minimal).
- `design/gdd/game-concept.md` describes a 2D platformer; `project.yaml` has
  `engine.name: Godot` and `engine.language: GDScript`
- `prototypes/` has no `grapple-hook-concept/`
- Review mode: `solo`
- In the debrief the user reports the hypothesis CONFIRMED and answers PROCEED

**Input:** `$gs-prototype grapple-hook traversal`

**Domain checks:**
- [ ] The hypothesis is falsifiable, with a measurable signal
- [ ] Engine is recommended in the path prompt before the user chooses
- [ ] The directory ask names `prototypes/grapple-hook-concept/` and comes before any prototype file is written
- [ ] Every prototype script carries the `PROTOTYPE - NOT FOR PRODUCTION` header as a `#` comment, never `//`; no file is written under the code root
- [ ] REPORT.md is written only after its ask, that ask also names `prototypes/index.md`, and the index gains a row with verdict PROCEED
- [ ] PROCEED next steps include `$gs-map-systems` and `$gs-design-system`

---

### Case 2: PIVOT — Carry-Forward Note Written

**Fixture:**
- A paper prototype of `trade-routes` has just been debriefed
- User answers PIVOT: the route planning was engaging, the upkeep maths was not
- Review mode: `solo`

**Input:** `$gs-prototype trade-routes --path paper`

**Domain checks:**
- [ ] `--path paper` is honoured and produces `rules.md` and `play-log.md`
- [ ] The two carry-forward questions are asked separately
- [ ] Preserve the case's unresolved human decisions and declines; perform routine writes already authorized, and ask only for missing decisions or scope.
- [ ] The note contains a revised hypothesis
- [ ] Next steps offer `$gs-prototype` for the revised concept or `$gs-brainstorm`

---

### Case 3: KILL — Soundness Check and Graveyard Entry

**Fixture:**
- A browser sketch of `procedural-dialogue` inside a configured Godot project has been debriefed
- User answers KILL; the debrief shows testers never understood the core
  action after 2 playtests, no fun moment was observed, and the concept only
  worked when the developer explained it

**Input:** `$gs-prototype procedural-dialogue --path html`

**Domain checks:**
- [ ] The KILL checklist is applied, with the 2+ rule deciding soundness
- [ ] Preserve the case's unresolved human decisions and declines; perform routine writes already authorized, and ask only for missing decisions or scope.
- [ ] The graveyard entry has all four fields and a specific kill reason
- [ ] Next steps route to `$gs-brainstorm`

---

### Case 4: Spike Mode — No Debrief, No Gate, No PROCEED/PIVOT/KILL

**Fixture:**
- Explicit standard workflow with sprint-004 as the current sprint, recorded in the active checkpoint.
- Project is in Production
- Review mode: `full`

**Input:** `$gs-prototype rope-physics --spike`

**Domain checks:**
- [ ] Keep the spike scope to 2–3 bullets with an approximately four-hour cap; SPIKE-NOTE records the question, YES/NO/PARTIAL result and next action.
- [ ] The intent widget and hypothesis/debrief phases are skipped
- [ ] The spike folder is created only after its ask
- [ ] `SPIKE-NOTE.md` and `active.md` are written only after an ask that names both
- [ ] Output is `SPIKE-NOTE.md` in a `-spike-[date]` folder, not a REPORT.md
- [ ] No CD-PLAYTEST consults or skip note, even though review mode is `full`
- [ ] No PROCEED / PIVOT / KILL verdict is issued
- [ ] The note's next decision includes adding to the current sprint, investigating further or
  abandoning. After the authorized write, the checkpoint returns to sprint-004; Case 7 covers
  minimal.

---

### Case 5: Director Gate — CD-PLAYTEST by Review Mode and Pillars

**Fixture:**
- In a configured non-Web engine project, a concept prototype has been built and REPORT.md written with a PROCEED
  recommendation
- Run A: `--review full`, `design/gdd/game-concept.md` exists with pillars;
  `creative-director` returns REJECT — the core fantasy is not present; the user,
  asked PIVOT or KILL, picks PIVOT
- Run B: `--review full`, neither `game-concept.md` nor `design/game-brief.md` exists
- Run C: `--review lean`

**Input:** `$gs-prototype [concept] --review [mode]`

**Domain checks:**
- [ ] Run A consults `creative-director` for CD-PLAYTEST after REPORT.md is written
- [ ] Run A: the director's verdict is read as one of APPROVE / CONCERNS / REJECT, not as a PROCEED / PIVOT / KILL of its own
- [ ] Run A: after the REJECT, PROCEED is not kept; the user is asked to choose PIVOT or KILL
- [ ] Run A's final recommendation is the user's PIVOT, and REPORT.md records it with the director's reason
- [ ] Run B skips with the "game pillars not yet defined" note instead of consulting without pillars
- [ ] Run C skips with the Lean-mode note
- [ ] No other director gate is consulted

---

### Case 6: NOT ASSESSED (Unplayed) and the `workflow: minimal` PROCEED Route

**Fixture:**
- Configured non-Web engine; Run A: the concept prototype was built this session but nobody has played it yet
- Run B: a PROCEED recommendation, `project.yaml` has `modes.workflow: minimal`

**Input:** `$gs-prototype [concept]`

**Domain checks:**
- [ ] Run A's verdict is NOT ASSESSED, not a guessed PROCEED/PIVOT/KILL
- [ ] Run A's report and `prototypes/index.md` row both read NOT ASSESSED until a playtest happens
- [ ] Run B's recommended path is the `workflow: minimal` route (`$gs-create-stories`, `$gs-dev-story`), not the `standard`/`full` GDD pipeline

---

### Case 7: Minimal spike restores the current story instead of a sprint

**Fixture:** Minimal workflow/full review; brief/build order, no sprints, story-002 In Progress and named in
active checkpoint. User answers YES to rope-physics spike.

**Input:** `$gs-prototype rope-physics --spike`

**Domain checks:**
- [ ] SPIKE-NOTE records question, result and next decision: add to brief/build order,
  investigate further or abandon. Do not offer adding to a current sprint.
- [ ] On authorized write restore checkpoint to story-002, with no sprint reference or creation.
  No CD-PLAYTEST or PROCEED/PIVOT/KILL.
- [ ] Keep the same spike-only scope and approximate four-hour cap as Case 4. No CD-PLAYTEST
  skip note is needed; the gate is inapplicable, not skipped by mode.

---

### Case 8: One-shot build preserves brief, data and evidence boundaries

**Fixture:** No engine/brief/prototypes; browser available; user says you pick then accepts Build it and explicitly authorizes commit/tag.

**Input:** $gs-prototype lighthouse keeper relighting beacons

**Domain checks:**
- [ ] Match only relevant genre sheets; ask one round for unanswered choices with defaults, no repeated questions. Card contains full brief, Look/First minute/Challenge, guessed/provisional/effort/engine/writes; no file before Build it.
- [ ] Write source words exactly, unchecked Features and empty Keep. Build in isolated prototype folder with tuning config, seeded rng, offline assets/vendor provenance; tune panel is opt-in.
- [ ] Retain all four small-check rows (boots, shot, brief words, emoji/outlines), the play screenshot and check-run/1 record. Respect explicitly requested visual choices; a failed row stays visible. Run finite scripted checks without a robot player or fabricated human review. Retain viewed screenshots and named brief-line outcomes, mark actually built Features in both briefs.
- [ ] Commit/tag only agreed files under actual explicit authorization. Handover states Not yet played by a person and starts the applicable debrief. Do not pin the host model or effort.

- [ ] Features and named-system coverage are assessed line by line as pass, missing, broken or not assessed; do not equate a file existing with a working promise. Autonomous skips questions only within already authorized scope; no-question-tool falls back to plain text.

---

### Case 9: Frozen-screen repair is bounded and failures remain visible

**Fixture:** As one-shot case, first build stops changing after start while scripted keys continue. Variant: no supported browser.

**Input:** $gs-prototype lighthouse keeper, then Build it

**Domain checks:**
- [ ] Run the small check and keep self-check rows/play screenshot. Fix once and recheck once; any remaining issue appears as Still broken, never a hidden pass.
- [ ] No autonomous reviewer or robot player establishes fun. No-browser rows are individually NOT ASSESSED with reasons; later requested changes use only their relevant light check.

- [ ] A check refuses a third run in the same repair round. Retain each outcome so a later requested change does not erase the earlier failure.

---

### Case 10: An engine preference is visible before a browser sketch is accepted

**Fixture:** No configured engine; at the card the user says Godot is installed and asks whether to use it.

**Input:** $gs-prototype lighthouse keeper

**Domain checks:**
- [ ] Explain Web now/Godot after play on the Engine and Next lines, and wait for acceptance of that concrete browser build. Do not setup/switch engines silently.
- [ ] Keep missing promised pieces under Still to do. A browser sketch within an existing non-Web project returns to applicable concept-prototype debrief/review, not automatic Grow.

---

### Case 11: 3D and persistence checks retain actual results

**Fixture:** Accepted 3D marble run remembering best time; browser available.

**Input:** $gs-prototype a 3D marble run that remembers best time

**Domain checks:**
- [ ] Record actual WebGL renderer and saved storage key, screenshots and check-run/1 record. Unsupported sound/other rows are not assessed with reasons, never not-applicable or pass.
- [ ] state.staged is set only for explicitly sourced staged-failure intent. Legitimate deterministic clock/manual/render hooks may aid observation but cannot change gameplay outcomes to make checks pass.

---

### Case 12: Named-game intent is clarified without copying protected expression

**Fixture:** No engine or brief. User asks for a Pac-Man clone and same UI with explicit controls/rules. Variants: named-game reference with new ghost perspective; new label on same-copy request; an existing brainstorm brief.

**Input:** $gs-prototype a maze-chase game

**Domain checks:**
- [ ] Ask only the unresolved original-in-genre versus own-twist choice, then build the accepted original direction. Preserve Avoid naming the referenced game's name/art/characters/UI; do not silently discard the user's gameplay requirements.
- [ ] A reference alone needs no copy question; relabeling alone does not resolve exact-copy intent. Existing brief requires no repeated questions and Writes names only the prototype folder.

---

## Applicable domain checks

- [ ] On the engine/paper route, if the concept is too vague to form a falsifiable hypothesis, stop before building and obtain the missing scope.

- [ ] Retain route selection through resume: explicit engine/paper and spike select their procedures; HTML in a configured non-Web project is a browser sketch returning to Phases 6–9; the no-engine/Web one-shot uses its own handover without REPORT.md/index or concept gate.
