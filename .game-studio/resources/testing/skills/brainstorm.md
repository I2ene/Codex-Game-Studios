# Evaluation scenarios: gs-brainstorm

Professional scenarios adapted from Donchitos' upstream testing guidance; see
[source attribution](../../../NOTICE.md). These are evaluation inputs and domain
checks, not executed results. Read `.agents/skills/gs-brainstorm/SKILL.md` and its current procedure first.
Use [evaluation policy](../README.md) and [category rubric](../quality-rubric.md).

Resolve current config and project engine records. Apply review-mode discipline
coverage without claiming automatic delegation: use the parent when needed, label it,
and record actual participants only. Existing human authorization governs writes;
case approvals represent unresolved decisions and never revoke prior authorization.
Historical fixture versions are scenario inputs, not current API verification.
The linked native procedure governs command arguments, output schemas, receipts,
context and mode applicability. Missing inputs remain NOT ASSESSED.

### Case 1: Happy Path — Full mode, 3 concepts, gates at their three points

**Fixture:**
- `project.yaml` sets `modes.rigor: full` (`workflow` → `full`, `review_mode` → `full`)
- No existing `design/gdd/game-concept.md`
- CD-PILLARS returns APPROVE; TD-FEASIBILITY returns VIABLE and PR-SCOPE returns REALISTIC (each gate's own verdict words)

**Input:** `$gs-brainstorm`

**Domain checks:**
- [ ] Exactly 3 concept options are presented
- [ ] CD-PILLARS and AD-CONCEPT-VISUAL cover the applicable disciplines, with optional authorized parallel delegation
- [ ] TD-FEASIBILITY consults before scope tiers are defined; PR-SCOPE after
- [ ] Preserve the case's unresolved human decisions and declines; perform routine writes already authorized, and ask only for missing decisions or scope.
- [ ] The concept document includes a Visual Identity Anchor section
- [ ] Next-step handoff lists `$gs-map-systems`
- [ ] Verdict is COMPLETE

---

### Case 2: Failure Path — CD-PILLARS returns REJECT

**Fixture:**
- `project.yaml` sets `modes.rigor: full`
- Pillars and anti-pillars have been agreed with the user
- CD-PILLARS returns REJECT: "The pillars do not carry weight — none forces a design choice"
- AD-CONCEPT-VISUAL returns 3 named visual directions

**Input:** `$gs-brainstorm`

**Domain checks:**
- [ ] CD-PILLARS feedback is shown to the user
- [ ] User is offered `Revise [specific pillar]` and `Discuss further` (and may `Lock in as-is`)
- [ ] The first question after the REJECT has no Visual anchor tab
- [ ] Visual anchor selection is not requested until the pillar issue is resolved
- [ ] `design/gdd/game-concept.md` is not written at this point

---

### Case 3: Lean Mode — All 4 gates skipped with named notes

**Fixture:**
- `project.yaml` sets `modes.rigor: standard` (`workflow` → `standard`, `review_mode` → `lean`)
- No existing game concept

**Input:** `$gs-brainstorm`

**Domain checks:**
- [ ] All 4 skip notes appear, each naming its gate and "Lean mode"
- [ ] No delegated participant is required for any director
- [ ] Preserve the case's unresolved human decisions and declines; perform routine writes already authorized, and ask only for missing decisions or scope.
- [ ] Verdict is COMPLETE

---

### Case 4: Solo Default — Minimal tier runs the Lean Brief flow

**Fixture:**
- `project.yaml` has `engine.name` set and no `modes` block (`modes.rigor`
  defaults to `minimal`: `workflow` → `minimal`, `review_mode` → `solo`)
- No `design/game-brief.md`, no `design/gdd/game-concept.md`

**Input:** `$gs-brainstorm roguelike`

**Domain checks:**
- [ ] Output file is `design/game-brief.md`; `design/gdd/game-concept.md` is not written
- [ ] 2–3 one-line concepts are proposed (not the full 9-field concept cards)
- [ ] No director agent is consulted
- [ ] Next steps list `$gs-create-stories` and `$gs-dev-story`, not `$gs-map-systems` or `$gs-setup-engine`
- [ ] Verdict is COMPLETE

---

### Case 5: Director Gate — PR-SCOPE returns UNREALISTIC

**Fixture:**
- `project.yaml` sets `modes.rigor: full`
- Concept, pillars and scope tiers are defined
- PR-SCOPE returns UNREALISTIC: "The MVP would take 18+ months for a solo developer"
- The user cuts the MVP to the adjusted tiers the skill offers, then answers
  `[A] Yes — write it` to the write ask

**Input:** `$gs-brainstorm`

**Domain checks:**
- [ ] Preserve the case's unresolved human decisions and declines; perform routine writes already authorized, and ask only for missing decisions or scope.
- [ ] Skill offers to adjust the MVP definition or scope tiers
- [ ] Skill does NOT discard or auto-reject the concept — the user decides
- [ ] The concept is written only after the user approves the write
- [ ] "Estimated Scope" in the written concept matches the Scope Tiers timeline (e.g. "Large (X–Y months, solo)")

---

### Case 6: Solo Review on the Full Flow — All 4 gates skipped with Solo-mode notes

**Fixture:**
- `project.yaml` sets `modes.rigor: standard` (`workflow` → `standard`)
- No existing game concept

**Input:** `$gs-brainstorm --review solo`

**Domain checks:**
- [ ] All 4 skip notes appear, each naming its gate and "Solo mode" (not "Lean mode")
- [ ] No delegated participant is required for any director
- [ ] Preserve the case's unresolved human decisions and declines; perform routine writes already authorized, and ask only for missing decisions or scope.
- [ ] Verdict is COMPLETE
