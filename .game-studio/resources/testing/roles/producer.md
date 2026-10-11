# Evaluation scenarios: gs-producer

Professional scenarios adapted from Donchitos' upstream testing guidance; see
[source attribution](../../../NOTICE.md). These are evaluation inputs and domain
checks, not executed results. Read `.codex/agents/gs-producer.toml` and its current procedure first.
Use [evaluation policy](../README.md) and [category rubric](../quality-rubric.md).

Resolve current config and project engine records. Apply review-mode discipline
coverage without claiming automatic delegation: use the parent when needed, label it,
and record actual participants only. Existing human authorization governs writes;
case approvals represent unresolved decisions and never revoke prior authorization.
Historical fixture versions are scenario inputs, not current API verification.
The linked native procedure governs command arguments, output schemas, receipts,
context and mode applicability. Missing inputs remain NOT ASSESSED.

### Case 1: In-domain request — appropriate output format
**Scenario:** A sprint plan is submitted for Sprint 7. The plan commits 9 story points across 4 team members over 2 weeks, with dependencies listed and no story larger than 3 days. Historical velocity from the last 3 sprints averages 11.5 points; no backlog debt is carried in, and the milestone constraints add nothing to this sprint. Request is tagged PR-SPRINT.
**Domain checks:** Returns `PR-SPRINT: REALISTIC` with rationale noting the load sits below historical velocity while keeping the 20% buffer its Sprint Planning Rules require (9 ≤ 80% of 11.5).
**Checklist:**
- [ ] Verdict is exactly one of REALISTIC / CONCERNS / UNREALISTIC
- [ ] Verdict token is formatted as `PR-SPRINT: REALISTIC`
- [ ] Rationale compares the 9 committed points with the 11.5-point velocity and the 20% buffer rule — not a generic "looks achievable"
- [ ] Output stays within production scope — does not comment on whether the stories are well-designed or technically sound

---

### Case 2: Out-of-domain request — redirects or escalates
**Scenario:** Team member asks producer to evaluate whether the game's "weight-based inventory" mechanic feels fun and engaging.
**Domain checks:** Agent declines to evaluate game feel and redirects to game-designer or creative-director.
**Checklist:**
- [ ] Does not make any binding assessment of the mechanic's design quality
- [ ] Explicitly names `game-designer` or `creative-director` as the correct handler
- [ ] Any comment it makes is about production implications only (e.g., which other systems the mechanic depends on) — never whether the mechanic is fun, engaging or well designed

---

### Case 3: Gate verdict — correct vocabulary
**Scenario:** A scope estimate is submitted for a solo developer with a 4-month timeline. The MVP was two systems (movement and combat), estimated at 3 months. The revised MVP adds three more — crafting, weather, and faction reputation — bringing the estimate to exactly 4 months: the whole timeline, with no buffer left for unplanned work. Each of the three could move to the next scope tier without breaking the MVP. Request is tagged PR-SCOPE.
**Domain checks:** Returns `PR-SCOPE: OPTIMISTIC` — the gate's middle verdict, with specific adjustments — because the MVP fits only if nothing goes wrong: names the three added systems and recommends which to move to a later scope tier to restore a buffer. Not UNREALISTIC: the estimate does not exceed the timeline, so neither has to be revised.
**Checklist:**
- [ ] Verdict is exactly one of REALISTIC / OPTIMISTIC / UNREALISTIC (the PR-SCOPE verdicts) — not CONCERNS and not freeform text
- [ ] Verdict token is formatted as `PR-SCOPE: OPTIMISTIC`
- [ ] Rationale names the three specific systems that use up the buffer
- [ ] Does not evaluate whether the systems are good design — only whether they fit the plan

---

### Case 4: Conflict escalation — correct parent
**Scenario:** game-designer wants to add a late-breaking mechanic (dynamic weather affecting all gameplay systems) that technical-director warns will require 3 additional sprints. game-designer and technical-director are in disagreement about whether to proceed.
**Domain checks:** Producer does not take a side on whether the mechanic is worth adding (design decision) or feasible (technical decision). Producer quantifies the production impact (3 sprints of delay, milestone slip risk), presents the trade-off to the user, and follows coordination-rules.md rule 3: game-designer and technical-director share no parent, and whether the mechanic is worth its cost is a design conflict, so it goes to creative-director, the arbiter of scope questions where creative intent and production capacity collide.
**Checklist:**
- [ ] Quantifies the production impact in concrete terms (sprint count, milestone date slip)
- [ ] Does not make a binding design or technical decision
- [ ] Surfaces the conflict to the user with the scope implications clearly stated
- [ ] Escalates the conflict to `creative-director` per coordination-rules.md rule 3 (no shared parent; a design conflict) — not to technical-director, and not straight to the user as if no escalation target existed

---

### Case 5: Context pass — uses provided context
**Scenario:** Agent receives a gate context block that includes the current milestone deadline (8 weeks away, two-week sprints) and velocity data from the last 4 sprints (8, 10, 9, 11 points). A sprint plan is submitted with 14 story points in five stories: Player movement (3), Jump buffering (2, depends on Player movement), Enemy patrol AI (5), Pause menu (2) and Save slots (2). Request is tagged PR-SPRINT.
**Domain checks:** Assessment uses the provided velocity data to show 14 points is well over the ~9.5-point average (and further over it once the 20% buffer is kept), returns `PR-SPRINT: UNREALISTIC` naming stories to defer, and references the 8-week milestone window to assess what the overrun does to the milestone.
**Checklist:**
- [ ] Uses the specific velocity figures from the provided context (not generic estimates)
- [ ] References the 8-week deadline in the capacity assessment
- [ ] Calculates or estimates remaining sprint count within the milestone window (four two-week sprints), as its duty to flag milestone risk at least 2 sprints ahead requires
- [ ] Names the stories to defer from the five supplied, by title, and never keeps Jump buffering while deferring Player movement, which it depends on
- [ ] Does not give generic scope advice disconnected from the supplied deadline and velocity data

---

### Case 6: Missing gate input — NOT ASSESSED
**Scenario:** A sprint plan is submitted with five stories — titles, estimates and dependencies, correctly ordered — and the milestone constraints, but no team capacity: the context gives none, and `production/sprints/` holds no earlier sprint to derive a velocity from. Request is tagged PR-SPRINT.
**Domain checks:** Returns `PR-SPRINT: NOT ASSESSED`, naming team capacity as the input it could not read. Whether a story load is realistic depends on the capacity it is measured against, so no feasibility verdict is given.
**Checklist:**
- [ ] Verdict token is `PR-SPRINT: NOT ASSESSED` — not REALISTIC, and not UNREALISTIC by assumption
- [ ] Names team capacity as the missing input
- [ ] Does not invent a capacity or velocity figure to judge the load against

---

### Case 7: Phase gate at `minimal` — the brief's Build order is the plan
**Scenario:** `$gs-gate-check production` at `workflow: minimal` runs the panel with `review_mode: lean` set explicitly, so the producer is spawned alone for PR-PHASE-GATE. The context gives the target phase (Production), the tier, and the gate's required artifacts at that tier: a filled `design/game-brief.md` with its Build order, and stories under `production/epics/`. Both are present — the Build order lists four MVP features, the first three independent and the fourth depending on the first, and there is one story per feature in that order, none Blocked. `team.size` is `individual`; the brief states a six-week target for the MVP. The sprint plan and sprint capacity are passed as "not required at `workflow: minimal`".
**Domain checks:** Returns `PR-PHASE-GATE: READY` — the Build order is the plan at this tier, its dependency is ordered, and four stories fit a solo developer's six weeks. The absent sprint plan and velocity are not findings.
**Checklist:**
- [ ] Verdict is exactly one of READY / CONCERNS / NOT READY (the PR-PHASE-GATE verdicts), formatted as `PR-PHASE-GATE: READY`
- [ ] Judges the Build order as the plan, and checks its dependency order (the fourth feature after the first)
- [ ] Does not raise the missing sprint plan or velocity as a concern, and does not answer NOT ASSESSED for them — they were passed as "not required at `workflow: minimal`"
- [ ] Does not invent a sprint capacity to judge the load against
