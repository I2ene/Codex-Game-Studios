# Evaluation scenarios: gs-game-designer

Professional scenarios adapted from Donchitos' upstream testing guidance; see
[source attribution](../../../../NOTICE.md). These are evaluation inputs and domain
checks, not executed results. Read `.codex/agents/gs-game-designer.toml` and its current procedure first.
Use [evaluation policy](../README.md) and [category rubric](../quality-rubric.md).

Resolve current config and project engine records. Apply review-mode discipline
coverage without claiming automatic delegation: use the parent when needed, label it,
and record actual participants only. Existing human authorization governs writes;
case approvals represent unresolved decisions and never revoke prior authorization.
Historical fixture versions are scenario inputs, not current API verification.
The linked native procedure governs command arguments, output schemas, receipts,
context and mode applicability. Missing inputs remain NOT ASSESSED.

### Case 1: In-domain request — appropriate output format
**Scenario:** The project's `modes.workflow` is `full`. The user asks game-designer to design a "Stamina-Based Dodge" mechanic: the player has a stamina pool, each dodge costs stamina, stamina regenerates when not dodging, and a dodge grants a short invincibility window.
**Domain checks:** Follows its Question-First workflow — asks what the dodge should make the player feel and how it connects to the pillars, presents 2–4 options with a recommendation, then drafts the GDD in the Design Document Standard with its tunable values exposed as tuning knobs, asking before each write.
**Checklist:**
- [ ] Asks clarifying questions (intended player experience, pillar connection) before proposing a design, and presents 2–4 options with a recommendation that leaves the choice to the user
- [ ] The draft uses the eight Design Document Standard sections: Overview, Player Fantasy, Detailed Rules, Formulas, Edge Cases, Dependencies, Tuning Knobs, Acceptance Criteria
- [ ] Tuning Knobs classify each value (stamina pool, dodge cost, regen rate, invincibility duration) as feel, curve, or gate, and place them in external data files rather than hardcoding them
- [ ] Preserve unresolved human decisions and declines; perform routine writes already authorized and ask only for missing decisions or scope.

---

### Case 2: Out-of-domain request — redirects or escalates
**Scenario:** A team member asks game-designer to write the in-world lore explanation for why the stamina system exists (e.g., the narrative reason characters have stamina limits in the game world).
**Domain checks:** Agent declines to write narrative/lore content and redirects to writer or narrative-director.
**Checklist:**
- [ ] Does not write narrative or lore content
- [ ] Explicitly names `writer` or `narrative-director` as the correct handler
- [ ] Any design intent it adds (e.g., "the stamina system should reinforce the physical realism theme") is framed as input for the narrative team, not written as the lore itself

---

### Case 3: Review findings — specific, verdict left to the review skill
**Scenario:** `$gs-design-review` in full mode spawns game-designer as the adversarial specialist for `design/gdd/environmental-hazards.md`. The spawn prompt reads: "Your job is NOT to validate this design — your job is to find problems. Anchor your review to the Player Fantasy stated in Section B." The Player Fantasy is "the world is dangerous but fair — every hazard is readable and avoidable." The GDD defines three hazard types (fire, acid, electricity) but does not specify what happens when a player is in several hazards at once, what happens when a hazard hits during the dodge invincibility window, or the damage frequency (per-second, per-tick, on-enter).
**Domain checks:** Returns specific findings naming the three undefined edge cases, tied to the stated Player Fantasy, as gaps to fill rather than a rejection of the mechanic. It returns findings, not a verdict — `$gs-design-review` issues the verdict.
**Checklist:**
- [ ] Names each missing edge case: simultaneous multi-hazard exposure, a hazard during dodge invincibility, and the undefined damage frequency
- [ ] Ties at least one gap to the stated Player Fantasy (e.g., an undefined damage frequency makes a hazard's threat unreadable, contradicting "readable and avoidable")
- [ ] Frames the gaps as rules to define in the GDD (what to specify), not as a rejection of the mechanic and not as implementation advice
- [ ] Returns findings to the review, not its own APPROVED / NEEDS REVISION stamp

---

### Case 4: Conflict escalation — correct parent
**Scenario:** systems-designer proposes a damage formula with 6 variables and complex scaling interactions, arguing it produces the best tuning granularity. game-designer believes the formula is too complex for players to intuit and want a simpler 2-variable version.
**Domain checks:** game-designer owns the conceptual rule and player experience intention ("the damage should feel understandable to players"), but defers the formula granularity question to systems-designer. If the disagreement cannot be resolved between them (one wants complex, one wants simple), escalate to creative-director for a player experience ruling.
**Checklist:**
- [ ] Clearly states the player experience intention (intuitive damage, player agency)
- [ ] Defers formula granularity decisions to `systems-designer`
- [ ] Escalates unresolved disagreement to `creative-director` for player experience arbiter ruling
- [ ] Does not unilaterally impose a formula structure on systems-designer

---

### Case 5: Context pass — uses provided context
**Scenario:** The request includes the game's three pillars: "player authorship," "consequence permanence," and "world responsiveness." A new mechanic spec for "permadeath with legacy bonuses" is submitted for the agent's assessment.
**Domain checks:** Assessment evaluates the mechanic against all three provided pillars — how permadeath supports player authorship, how legacy bonuses express or soften consequence permanence, and how the world responds to a player's death. Uses the pillar vocabulary directly, and flags pillar tensions for the user to decide.
**Checklist:**
- [ ] References all three provided pillars by name in the assessment
- [ ] Evaluates the mechanic's contribution to each pillar explicitly
- [ ] Does not generate generic game design advice — every point is tied to one of the provided pillars by name; a framework term (MDA, SDT) may support a point but never replaces the pillar it concerns
- [ ] Flags at least one specific pillar tension (e.g., legacy bonuses softening "consequence permanence") as an issue for the user's decision, not one it resolves silently

---

### Case 6: Section set at `modes.workflow: standard`
**Scenario:** The same "Stamina-Based Dodge" request as Case 1, but the project's `modes.workflow` is `standard`.
**Domain checks:** Drafts the five sections `standard` requires — Overview, Detailed Rules, Edge Cases, Dependencies, Acceptance Criteria — plus Formulas, because the dodge defines numeric rules (stamina cost, regen rate, invincibility duration).
**Checklist:**
- [ ] The draft contains Overview, Detailed Rules, Edge Cases, Dependencies and Acceptance Criteria — Dependencies is not dropped
- [ ] Includes Formulas, because the mechanic defines numeric rules
- [ ] Does not treat Player Fantasy or Tuning Knobs as required sections at this tier
