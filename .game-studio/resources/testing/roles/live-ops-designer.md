# Evaluation scenarios: gs-live-ops-designer

Professional scenarios adapted from Donchitos' upstream testing guidance; see
[source attribution](../../../../NOTICE.md). These are evaluation inputs and domain
checks, not executed results. Read `.codex/agents/gs-live-ops-designer.toml` and its current procedure first.
Use [evaluation policy](../README.md) and [category rubric](../quality-rubric.md).

Resolve current config and project engine records. Apply review-mode discipline
coverage without claiming automatic delegation: use the parent when needed, label it,
and record actual participants only. Existing human authorization governs writes;
case approvals represent unresolved decisions and never revoke prior authorization.
Historical fixture versions are scenario inputs, not current API verification.
The linked native procedure governs command arguments, output schemas, receipts,
context and mode applicability. Missing inputs remain NOT ASSESSED.

### Case 1: In-domain request — summer event design
**Input**: "Design a summer event for our game. It should run for 3 weeks and give players reasons to log in daily."
**Domain checks**:
- Before drafting, asks clarifying questions and presents 2-4 options with a recommendation (Question-First Workflow)
- The event brief carries every field its Event Design requires: start date, end date, mechanics, rewards, success criteria — plus a fallback plan if the event breaks (disable, extend, compensate)
- Includes daily login retention hooks (e.g., daily challenges, login streaks, time-limited rewards) — the request's "reasons to log in daily" — paced across the full 3 weeks, not front-loaded into the first days (e.g., weekly milestones, or the weekly challenges its Weekly cadence tier names)
- Names reward categories (cosmetic, functional, currency) but does NOT assign specific reward values or currency amounts — those are left to economy-designer ("exact values assigned by economy-designer")
- [ ] Preserve unresolved human decisions and declines; perform routine writes already authorized and ask only for missing decisions or scope.

---

### Case 2: Out-of-domain request — reward value calculation
**Input**: "How much premium currency should we give out in this event? What's the fair value of each cosmetic reward tier?"
**Domain checks**:
- Does not produce currency amounts or reward valuation
- Says reward values and currency amounts are economy-designer's to assign, and that its part is defining which rewards exist and how they are structured
- Offers to produce the reward structure (tiers, unlock gates, rarity distribution, reward categories) so economy-designer has something concrete to value

---

### Case 3: Domain boundary — predatory monetization concern
**Input**: "Let's design the battle pass so that players need to spend premium currency on top of the pass price to complete all tiers within the season."
**Domain checks**:
- Flags this design as predatory — pay-to-complete gating is named in its Escalation Paths
- Does NOT produce a design that requires additional purchases after a battle pass purchase without flagging it ("do NOT implement it silently")
- Offers at least one compliant option alongside the flag (Question-First step 2 presents 2-4 options): a pass completable by a buyer playing at a reasonable daily pace, using the catch-up mechanics its Battle Pass Design calls for
- [ ] Preserve unresolved human decisions and declines; perform routine writes already authorized and ask only for missing decisions or scope. Preserve the stated artifact obligations for `design/live-ops/ethics-policy.md`.
- Does not refuse to continue entirely — offers the ethical alternative and awaits direction

---

### Case 4: Conflict — event schedule vs. main game progression pacing
**Input**: "We want to run a double-XP event during weeks 3-5 of the season, but our progression designer says that's when players are supposed to hit the mid-game difficulty curve."
**Domain checks**:
- Identifies the conflict: a double-XP event during the mid-game difficulty curve compresses the intended progression pacing
- Does NOT unilaterally move or cancel either element
- Escalates to creative-director: a live-ops schedule that forces players off a designed progression curve is the "Cross-domain design conflict" its Escalation Paths names
- Presents both positions — the event's retention value and the intended progression experience — and lets creative-director adjudicate; any resolution it suggests (shift the event timing, scope the boost to non-core progression) is offered as an option for the director, not applied

---

### Case 5: Context pass — designing to address a player retention drop-off
**Input context**: Analytics show a 40% player drop-off at Day 7, attributed to players completing the tutorial but finding no mid-term goal to pursue.
**Input**: "Design a live ops feature to address the Day 7 drop-off."
**Domain checks**:
- Designs for the Day 7 cohort named in the data — not a generic retention feature — and does not re-ask for the drop-off data it was given
- The feature is visible and active at or before Day 7 and supplies the missing mid-term goal (a visible progression track with rewards spaced beyond Day 7)
- Defines success against the D7 retention point its Retention Mechanics already tracks (with D14 to confirm the effect holds), not a generic engagement metric
- Does NOT design a feature for Day 1 retention or Day 30 monetization when the data points to Day 7
- Leaves specific reward values to economy-designer
