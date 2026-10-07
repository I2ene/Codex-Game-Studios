# Evaluation scenarios: gs-world-builder

Professional scenarios adapted from Donchitos' upstream testing guidance; see
[source attribution](../../../../NOTICE.md). These are evaluation inputs and domain
checks, not executed results. Read `.codex/agents/gs-world-builder.toml` and its current procedure first.
Use [evaluation policy](../README.md) and [category rubric](../quality-rubric.md).

Resolve current config and project engine records. Apply review-mode discipline
coverage without claiming automatic delegation: use the parent when needed, label it,
and record actual participants only. Existing human authorization governs writes;
case approvals represent unresolved decisions and never revoke prior authorization.
Historical fixture versions are scenario inputs, not current API verification.
The linked native procedure governs command arguments, output schemas, receipts,
context and mode applicability. Missing inputs remain NOT ASSESSED.

### Case 1: In-domain request — faction culture and government design
**Input**: "Design the Ironveil Merchant Consortium — a powerful trading faction in our world. I need their culture, government structure, and internal motivations."
**Domain checks**:
- Before drafting, asks clarifying questions and presents 2-4 options for the government model (e.g., council of founding houses, elected chair, shareholder-weighted vote) with pros/cons and a recommendation, deferring the choice to the user
- Produces a faction profile with: motivations (what they want and why), power structure (how decisions are made, who holds power, succession or appointment), relationships to other factions (allies, rivals, neutral parties), territories, player-facing personality, and cultural details (customs, beliefs, daily life)
- The faction is internally consistent: a merchant consortium's government is driven by economic logic, not feudal or religious logic, unless a deliberate hybrid is specified
- The entry carries the Lore Document Standard fields: Canon Level, Visible To Player, Cross-References, Contradictions Check, Source
- [ ] Preserve unresolved human decisions and declines; perform routine writes already authorized and ask only for missing decisions or scope.

---

### Case 2: Out-of-domain request — dialogue writing
**Input**: "Write the dialogue for a Ironveil Consortium merchant NPC that the player meets at the city gates."
**Domain checks**:
- Does not produce NPC dialogue
- States that dialogue writing is owned by `writer`, and that its own part is the world and faction context that informs the dialogue — the faction's culture, tone and speaking style
- Offers to produce the faction's cultural details — customs, beliefs, language fragments, daily life — that writer would need to write consistent dialogue

---

### Case 3: New lore entry contradicts established history — conflict flagging
**Input**: "Add a lore entry stating the Ironveil Consortium was founded 50 years ago by a single merchant family." [Context includes existing lore: the Consortium has existed for 300 years and was founded as a collective by 12 rival trading houses.]
**Domain checks**:
- Identifies the contradiction: existing lore states 300-year history and a founding coalition of 12 houses; the new entry claims 50 years and a single founding family
- Does NOT write the new entry as requested
- Flags the conflict: states both versions, identifies which is established and which is the proposed change
- Proposes resolution options: (a) the new entry is wrong and should be corrected; (b) the existing lore should be updated if the new version is the intended canon; (c) there is an in-world explanation (the current family claims founding credit despite the collective origin — a deliberate unreliable narrator, with the truth documented separately)
- Does not apply option (b) on its own: changing established canon requires narrative-director approval

---

### Case 4: World rule has gameplay implications — coordination with game-designer
**Input**: "I want to establish a world rule: magic users who cast spells near iron ore are weakened. Iron disrupts arcane energy."
**Domain checks**:
- Produces the world rule as a lore entry: the metaphysical explanation, how it is understood in-world, historical implications
- Identifies the gameplay implication: this world rule has direct mechanical consequences (players near iron ore deposits are debuffed, level design must account for iron placement)
- Flags the coordination requirement: "This world rule has gameplay mechanics implications — game-designer needs to define how this translates into player-facing mechanics; proceeding with the lore without the mechanics definition risks inconsistency"
- Does NOT unilaterally design the game mechanic — describes the lore rule and the mechanical territory it implies, then defers to game-designer

---

### Case 5: Context pass — using established world documents
**Input context**: Existing world document states: the world uses a dual-sun system, one sun is the source of arcane energy (the White Sun), and arcane magic ceases to function during the 3-day lunar eclipse period (the Darkening).
**Input**: "Add a lore entry about the Mages' College and how they prepare for the Darkening."
**Domain checks**:
- Uses the established dual-sun cosmology: references the White Sun as the source of arcane energy
- Uses the established Darkening event: 3-day eclipse, magic ceases
- Does NOT invent a different eclipse mechanism, duration, or name
- Produces a lore entry where the Mages' College's Darkening preparations are consistent with the established rules: they cannot cast during the Darkening, so preparations are practical (stockpiling non-magical supplies, scheduling, shutting down ongoing magical processes)
- Does not contradict any established fact from the context document
