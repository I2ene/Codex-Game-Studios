# Evaluation scenarios: gs-creative-director

Professional scenarios adapted from Donchitos' upstream testing guidance; see
[source attribution](../../../../NOTICE.md). These are evaluation inputs and domain
checks, not executed results. Read `.codex/agents/gs-creative-director.toml` and its current procedure first.
Use [evaluation policy](../README.md) and [category rubric](../quality-rubric.md).

Resolve current config and project engine records. Apply review-mode discipline
coverage without claiming automatic delegation: use the parent when needed, label it,
and record actual participants only. Existing human authorization governs writes;
case approvals represent unresolved decisions and never revoke prior authorization.
Historical fixture versions are scenario inputs, not current API verification.
The linked native procedure governs command arguments, output schemas, receipts,
context and mode applicability. Missing inputs remain NOT ASSESSED.

### Case 1: In-domain request — appropriate output format
**Scenario:** The pillar set for a narrative survival game is submitted for a stress test, with its anti-pillars, core fantasy and unique hook. The hook names its closest comparable — "Like *Don't Starve*, AND ALSO every survivor you lose changes the world for good" — and none of the three pillars is a goal that comparable is built around. It has three pillars — "emergent stories," "meaningful sacrifice," and "lived-in world" — each with a definition and a design test that names a real decision it would settle; the pillars pull against each other (sacrifice vs. a world the player wants to preserve). Request is tagged CD-PILLARS.
**Domain checks:** Returns `CD-PILLARS: APPROVE` with specific feedback on each pillar, judged by the gate's criteria: is it falsifiable, does it create tension with the others, does it differentiate the game, would it settle a real design disagreement.
**Checklist:**
- [ ] Verdict is exactly one of APPROVE / CONCERNS / REJECT
- [ ] Verdict token is formatted as `CD-PILLARS: APPROVE` (gate ID prefix, colon, verdict keyword)
- [ ] Gives feedback on each of the three pillars by name against the gate's criteria (falsifiability, tension, differentiation from *Don't Starve*), not generic creative advice
- [ ] Output stays within creative scope — does not comment on engine feasibility or sprint schedule

---

### Case 2: Out-of-domain request — redirects or escalates
**Scenario:** Developer asks creative-director to review a proposed PostgreSQL schema for storing player save data.
**Domain checks:** Agent declines to evaluate the schema and redirects to technical-director.
**Checklist:**
- [ ] Does not make any binding decision about the schema design
- [ ] Explicitly names `technical-director` as the correct handler
- [ ] Any comment on the schema is limited to its creative implications (e.g., which player choices a save must remember) — it proposes no table, column, key or query design

---

### Case 3: Gate verdict — correct vocabulary
**Scenario:** A GDD for the "Crafting" system is submitted with the game's pillars — "curiosity is always rewarded" and "the world remembers" — and its MDA target, Discovery first. Section 4 (Formulas) defines a resource decay formula that punishes exploration — contradicting the Player Fantasy section which calls for "freedom to roam without fear," and working against the curiosity pillar. Every other section serves the pillars, and retuning the formula would resolve the conflict without redesigning the system. Request is tagged CD-GDD-ALIGN.
**Domain checks:** Returns `CD-GDD-ALIGN: CONCERNS` with specific citation of the contradiction between the formula behavior and the Player Fantasy statement. The fix is stated as a creative constraint; the formula itself is left to the design team.
**Checklist:**
- [ ] Verdict is exactly one of APPROVE / CONCERNS / REJECT — not freeform text
- [ ] Verdict token is formatted as `CD-GDD-ALIGN: CONCERNS`
- [ ] Rationale quotes or directly references GDD Section 4 (Formulas), the Player Fantasy section and the "curiosity is always rewarded" pillar
- [ ] States the fix as a creative constraint (e.g., decay must not punish roaming) and leaves the formula to `game-designer`, its delegate for mechanical design — does not author replacement formula values

---

### Case 4: Conflict escalation — correct parent
**Scenario:** technical-director raises a concern that the core loop mechanic (real-time branching conversations) is prohibitively expensive to implement and recommends cutting it. creative-director disagrees on creative grounds.
**Domain checks:** creative-director acknowledges the technical constraint, does not override technical-director's feasibility assessment, but retains authority to define what the creative goal is. For the conflict itself, creative-director is the top-level creative escalation point and defers to technical-director on implementation feasibility while advocating for the design intent. The resolution path is for both to jointly present trade-off options to the user.
**Checklist:**
- [ ] Does not unilaterally override technical-director's feasibility concern
- [ ] Clearly separates "what we want creatively" from "how it gets built"
- [ ] Proposes presenting trade-offs to the user rather than resolving unilaterally
- [ ] Does not claim to own implementation decisions

---

### Case 5: Context pass — uses provided context
**Scenario:** Agent receives a gate context block that includes the game pillars document (`design/gdd/game-pillars.md`) and a new system GDD for review. The pillars document defines "player authorship," "consequence permanence," and "world responsiveness" as the three core pillars. Request is tagged CD-GDD-ALIGN.
**Domain checks:** Assessment uses the exact pillar vocabulary from the provided document, not generic creative heuristics. Any approval or concern is tied back to one or more of the three named pillars.
**Checklist:**
- [ ] Uses the exact pillar names from the provided context document
- [ ] Does not generate generic creative feedback disconnected from the supplied pillars
- [ ] References the specific pillar(s) most relevant to the mechanic under review
- [ ] Does not reference pillars not present in the provided document

---

### Case 6: Missing gate input — NOT ASSESSED
**Scenario:** A complete, internally consistent system GDD is submitted with its Player Fantasy section, but no game pillars: the context gives none, and none of `design/gdd/game-concept.md`, `design/gdd/game-pillars.md` or `design/game-brief.md` exists. Request is tagged CD-GDD-ALIGN.
**Domain checks:** Returns `CD-GDD-ALIGN: NOT ASSESSED`, naming the game pillars as the input it could not read. Alignment with pillars nobody supplied cannot be judged, so no alignment verdict is given.
**Checklist:**
- [ ] Verdict token is `CD-GDD-ALIGN: NOT ASSESSED` — not APPROVE, although nothing in the GDD itself looks wrong
- [ ] Names the game pillars as the missing input
- [ ] Does not infer pillars from the GDD under review and judge alignment against them
