# Evaluation scenarios: gs-vertical-slice

Professional scenarios adapted from Donchitos' upstream testing guidance; see
[source attribution](../../../NOTICE.md). These are evaluation inputs and domain
checks, not executed results. Read `.agents/skills/gs-vertical-slice/SKILL.md` and its current procedure first.
Use [evaluation policy](../README.md) and [category rubric](../quality-rubric.md).

Resolve current config and project engine records. Apply review-mode discipline
coverage without claiming automatic delegation: use the parent when needed, label it,
and record actual participants only. Existing human authorization governs writes;
case approvals represent unresolved decisions and never revoke prior authorization.
Historical fixture versions are scenario inputs, not current API verification.
The linked native procedure governs command arguments, output schemas, receipts,
context and mode applicability. Missing inputs remain NOT ASSESSED.

### Case 1: Happy Path — slice built, played unaided, PROCEED

**Fixture:**
- `project.yaml`: `engine.name: Godot`, `engine.language: GDScript`,
  `modes.review_mode: solo`
- `design/gdd/game-concept.md` (core fantasy, pillars), `design/gdd/systems-index.md`,
  `docs/architecture/architecture.md` and `docs/architecture/control-manifest.md`
  exist; `prototypes/` has no `ember-trail-vertical-slice/`
- In the debrief the player finished the loop unaided, reached the first meaningful
  action in 40 seconds, felt the core fantasy and hit no fun blocker; the user
  answers PROCEED

**Input:** `$gs-vertical-slice`

**Domain checks:**
- [ ] The validation question has both a player-experience and a build-feasibility part
- [ ] Preserve the case's unresolved human decisions and declines; perform routine writes already authorized, and ask only for missing decisions or scope.
- [ ] The directory ask comes before any slice file; each GDScript file's header is a `#` comment, never `//`
- [ ] The debrief questions are asked one at a time, after the from-scratch playthrough
- [ ] REPORT.md and the `prototypes/index.md` row are written only after one ask naming both; the row records PROCEED
- [ ] The formal stage step is `$gs-gate-check production` (Pre-Production → Production), not `$gs-gate-check pre-production`

---

### Case 2: Failure Path — a built slice with a NO cannot PROCEED

**Fixture:**
- As Case 1, but in the debrief the player needed the developer to explain the
  core action (question 1: no)
- The user answers PROCEED anyway, then picks PIVOT when asked

**Input:** `$gs-vertical-slice`

**Domain checks:**
- [ ] PROCEED is not written to REPORT.md or `prototypes/index.md` while a validation item is NO
- [ ] The user, not the skill, chooses between PIVOT and KILL
- [ ] The report names the failed validation item
- [ ] PIVOT-NOTE.md is written only after its ask, with what worked, what failed and what the next slice should prove

---

### Case 3: Mode Variant — CD-PLAYTEST in full, skipped in lean and solo

**Fixture:**
- A slice has been debriefed with a PROCEED recommendation and REPORT.md written
- Run A: `modes.review_mode: full`; CD-PLAYTEST returns APPROVE
- Run B: `modes.review_mode: lean`
- Run C: `modes.review_mode: full`, input `$gs-vertical-slice --review solo`

**Domain checks:**
- [ ] Run A consults CD-PLAYTEST only after REPORT.md exists, with the three inputs
- [ ] Run A's APPROVE keeps the recommendation and triggers no REPORT.md update ask
- [ ] Runs B and C consults no director and print their skip notes
- [ ] No other director gate is consulted in any run

---

### Case 4: Edge Case — the slice is built but nobody has played it

**Fixture:**
- The loop became demonstrable, but the user cannot play it through from scratch
  this session
- `modes.review_mode: full`

**Input:** `$gs-vertical-slice`

**Domain checks:**
- [ ] The verdict is NOT ASSESSED — never PROCEED — and its reason is stated
- [ ] NOT ASSESSED is ranked above PROCEED and below PIVOT and KILL
- [ ] CD-PLAYTEST is not consulted for an unplayed slice, and the skip is announced
- [ ] PROCEED's next steps are not offered

---

### Case 5: Director Gate — CD-PLAYTEST returns REJECT, CONCERNS or NOT ASSESSED

**Fixture:**
- A slice has been debriefed with a PROCEED recommendation and REPORT.md written;
  `modes.review_mode: full`; `design/gdd/game-concept.md` holds the pillars
- Run A: CD-PLAYTEST returns REJECT — the core fantasy is not present. Asked PIVOT
  or KILL, the user picks KILL; no playtest session showed an emotional high
  point, and this is the third slice attempt on the concept
- Run B: CD-PLAYTEST returns CONCERNS — the resolution beat undercuts a pillar; the
  user picks `Accept with noted concerns`
- Run C: CD-PLAYTEST returns NOT ASSESSED — the pillars were missing from the
  context it received

**Input:** `$gs-vertical-slice`

**Domain checks:**
- [ ] The director's answer is read as APPROVE / CONCERNS / REJECT / NOT ASSESSED — never as a PROCEED / PIVOT / KILL of its own
- [ ] Run A: PROCEED is not kept after the REJECT; the user chooses PIVOT or KILL, and the director's reason is in REPORT.md
- [ ] Run A: the GRAVEYARD.md entry is appended only after its ask, with a specific kill reason
- [ ] Run B: the user decides; the recommendation changes only if the user revises it
- [ ] Run C: NOT ASSESSED is not treated as APPROVE
- [ ] Every REPORT.md / `prototypes/index.md` update follows an ask naming both
