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
- An HTML prototype of `procedural-dialogue` has been debriefed
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
- Project is in Production
- Review mode: `full`

**Input:** `$gs-prototype rope-physics --spike`

**Domain checks:**
- [ ] The intent widget and hypothesis/debrief phases are skipped
- [ ] The spike folder is created only after its ask
- [ ] `SPIKE-NOTE.md` and `active.md` are written only after an ask that names both
- [ ] Output is `SPIKE-NOTE.md` in a `-spike-[date]` folder, not a REPORT.md
- [ ] No CD-PLAYTEST consults or skip note, even though review mode is `full`
- [ ] No PROCEED / PIVOT / KILL verdict is issued

---

### Case 5: Director Gate — CD-PLAYTEST by Review Mode and Pillars

**Fixture:**
- A concept prototype has been built and REPORT.md written with a PROCEED
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
- Run A: the prototype was built this session but nobody has played it yet
- Run B: a PROCEED recommendation, `project.yaml` has `modes.workflow: minimal`

**Input:** `$gs-prototype [concept]`

**Domain checks:**
- [ ] Run A's verdict is NOT ASSESSED, not a guessed PROCEED/PIVOT/KILL
- [ ] Run A's report and `prototypes/index.md` row both read NOT ASSESSED until a playtest happens
- [ ] Run B's recommended path is the `workflow: minimal` route (`$gs-create-stories`, `$gs-dev-story`), not the `standard`/`full` GDD pipeline
