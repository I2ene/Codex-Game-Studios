# Evaluation scenarios: gs-economy-designer

Professional scenarios adapted from Donchitos' upstream testing guidance; see
[source attribution](../../../../NOTICE.md). These are evaluation inputs and domain
checks, not executed results. Read `.codex/agents/gs-economy-designer.toml` and its current procedure first.
Use [evaluation policy](../README.md) and [category rubric](../quality-rubric.md).

Resolve current config and project engine records. Apply review-mode discipline
coverage without claiming automatic delegation: use the parent when needed, label it,
and record actual participants only. Existing human authorization governs writes;
case approvals represent unresolved decisions and never revoke prior authorization.
Historical fixture versions are scenario inputs, not current API verification.
The linked native procedure governs command arguments, output schemas, receipts,
context and mode applicability. Missing inputs remain NOT ASSESSED.

### Case 1: In-domain request — loot table design for a chest
**Input**: "Design the loot table for a standard treasure chest in our dungeon game."
**Domain checks**:
- Before drafting, asks clarifying questions and presents 2-4 options with a recommendation (Question-First Workflow) — e.g. tier names, whether chests use pity timers or bad-luck protection
- Reads `design/registry/entities.yaml` before authoring and uses registered item values as canonical; a value that differs from a registered entry is flagged as a proposed registry change, not silently used
- Produces the table in its Reward Output Format (output, rate or weight, condition, notes) with distinct rarity tiers — Common, Uncommon, Rare, Epic, Legendary, or project-equivalent — not a single flat list of items
- Tier rates form a complete distribution: percentages sum to 100%, or weights are given with their total
- States the expected acquisition for each tier (attempts on average to receive it) and names the reward-schedule principle behind the table (Reward Psychology)
- [ ] Preserve unresolved human decisions and declines; perform routine writes already authorized and ask only for missing decisions or scope. Preserve the stated artifact obligations for `design/registry/entities.yaml`.

---

### Case 2: Out-of-domain request — seasonal event schedule
**Input**: "Design the schedule for our summer event and fall event. When should they run and how long should each last?"
**Domain checks**:
- Does not produce an event schedule or content cadence plan
- States clearly: "Live ops event scheduling is owned by live-ops-designer; I design the economic structure of rewards within events once the event schedule is defined"
- Offers to produce the reward value design for events once live-ops-designer defines the structure

---

### Case 3: Domain boundary — inflation risk from new currency
**Input**: "We're adding a new 'Prestige Coins' currency earned by completing all seasonal content. Players can spend them in a Prestige Shop."
**Domain checks**:
- Identifies the inflation risk: if Prestige Coins accumulate faster than the shop provides sinks, the shop loses perceived value and players hoard coins without spending
- Flags the specific risk: seasonal content completion is a finite faucet, but if the shop catalog is exhausted before the season ends, late-season coins have no value
- Proposes a sink mechanic: rotating limited-time shop items, consumable items in the Prestige Shop, or a currency conversion option to keep coins draining
- Does NOT approve the design as economically sound without addressing the sink question
- Produces a structured risk assessment: faucet rate (estimated coins/week), sink capacity (estimated coins required to exhaust catalog), surplus projection

---

### Case 4: Mid-game progression curve issue
**Input**: "Players are reporting the mid-game XP grind (levels 20-35) feels like a wall. They need 3x more XP per level but rewards don't increase proportionally."
**Domain checks**:
- Identifies this as a progression curve problem: the XP cost growth rate outpaces the reward growth rate
- Produces a revised XP formula or curve adjustment: either reduce the XP cost multiplier for levels 20-35, increase reward XP in that range, or introduce a catch-up mechanic (bonus XP for completing content significantly below the player's level)
- States the current and proposed curves as formulas with defined variables and evaluates both across the 20–35 range, both ends included (e.g., at levels 20, 25, 30 and 35) — `coding-standards.md` requires design math "defined with variables" and balance values linked to their source formula
- Flags that any curve change affects time-to-level-cap projections — notes the downstream impact on end-game content pacing (its Progression Curve Design models expected player power at each stage)

---

### Case 5: Context pass — balance analysis using current economy data
**Input context**: Current economy data: average player earns 450 Gold/hour, average shop item costs 2,000 Gold, average session length is 40 minutes. Premium items cost 5,000 Gold.
**Input**: "Is our current Gold economy healthy? Should we adjust prices or earn rates?"
**Domain checks**:
- Uses the specific numbers provided: 450 Gold/hour = 300 Gold per 40-minute session; a 2,000 Gold item takes ~4.4 hours (~6.7 sessions) to afford; a 5,000 Gold premium item takes ~11.1 hours (~16.7 sessions)
- Evaluates those acquisition times against its Economic Health Metrics (average currency per hour, item acquisition rate)
- Presents options anchored to the numbers — e.g. raise the earn rate or lower the premium price — with the resulting hours and sessions for each, makes a recommendation, and leaves the choice to the user (Question-First Workflow)
- Does NOT produce generic advice ("prices may be too high") without anchoring to the provided data
