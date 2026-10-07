# Evaluation scenarios: gs-writer

Professional scenarios adapted from Donchitos' upstream testing guidance; see
[source attribution](../../../../NOTICE.md). These are evaluation inputs and domain
checks, not executed results. Read `.codex/agents/gs-writer.toml` and its current procedure first.
Use [evaluation policy](../README.md) and [category rubric](../quality-rubric.md).

Resolve current config and project engine records. Apply review-mode discipline
coverage without claiming automatic delegation: use the parent when needed, label it,
and record actual participants only. Existing human authorization governs writes;
case approvals represent unresolved decisions and never revoke prior authorization.
Historical fixture versions are scenario inputs, not current API verification.
The linked native procedure governs command arguments, output schemas, receipts,
context and mode applicability. Missing inputs remain NOT ASSESSED.

### Case 1: In-domain request — NPC merchant dialogue
**Input**: "Write dialogue for Mira, a traveling merchant NPC. She sells general supplies. Players can ask her about her wares, the road ahead, and rumors."
**Domain checks**:
- Looks for Mira's voice profile (voice profiles are defined by narrative-director); if none is provided, says so and asks, or proposes a provisional voice for approval — it does not decide her character arc
- Produces a dialogue tree with at least three top-level conversation options: [Wares], [The Road Ahead], [Rumors], and at least one follow-up branch (tree structure, not flat responses)
- Every line has a speaker tag and a context note, and branch conditions carry condition/state annotations in a consistent format
- No line exceeds 120 characters; any variable insertion uses a named placeholder (e.g., `{player_name}`)
- Road and rumor content does not contradict established world-building
- [ ] Preserve unresolved human decisions and declines; perform routine writes already authorized and ask only for missing decisions or scope.

---

### Case 2: Out-of-domain request — world history design
**Input**: "Design the history of the world — when the first kingdom was founded, what the great wars were, and why magic was banned."
**Domain checks**:
- Does not produce world history, lore architecture, or world rules
- States clearly: "World history, lore, and world rules are owned by world-builder; once the history is established, I can write in-game texts, books, and dialogue that reference those events"
- Does not produce even partial world history as a "placeholder"

---

### Case 3: Dialogue contradicts established lore — flag to narrative-director
**Input**: "Write Mira's dialogue line where she mentions that dragons have been extinct for 200 years." [Context includes existing lore: dragons are alive and revered in the northern provinces, not extinct.]
**Domain checks**:
- Identifies the contradiction: established lore states dragons are alive and revered; dialogue stating they're extinct directly conflicts
- Does NOT write the requested line as given
- Flags the inconsistency to narrative-director: "Mira's dialogue as requested contradicts established lore (dragons are alive per world-builder's document); requires narrative-director resolution before I can write this line"
- Offers the user a lore-consistent alternative line (e.g., Mira expresses awe about a dragon sighting in the north) to use while the conflict is resolved

---

### Case 4: Item description references an undesigned mechanic
**Input**: "Write a description for the 'Berserker's Chalice' — a consumable that triggers the Berserker state when drunk."
**Domain checks**:
- Identifies the dependency gap: "Berserker state" is not defined in any provided game design document
- Flags the missing dependency: "This description references a 'Berserker state' mechanic that has no GDD entry — I cannot write accurate flavor text for a mechanic whose rules are undefined, as the description may create incorrect player expectations"
- Does NOT write a description that invents mechanic details (duration, effects) that may conflict with the eventual design
- Raises the missing definition with game-designer (its coordinator for mechanical clarity in text) and asks the user how to proceed: (a) a vague, non-mechanical description that creates no false expectations, flagged as temporary; or (b) wait for game-designer to define the Berserker state first

---

### Case 5: Context pass — character voice guide
**Input context**: Character voice guide for Mira: She speaks in short, energetic sentences. Uses merchant slang ("a fine bargain," "coin well spent"). Drops pronouns occasionally ("Good wares, these."). Never uses contractions — always "I will" not "I'll". Warm but slightly mercenary.
**Input**: "Write Mira's response when a player asks if she has healing potions."
**Domain checks**:
- Short, energetic sentences — no long monologues
- Uses merchant slang: "a fine bargain," "coin well spent," or similar
- Drops pronouns where natural: "Fine stock, these potions."
- No contractions: "I will" not "I'll," "do not" not "don't"
- Warm tone with a mercenary undertone: she's happy to help because you're a paying customer
- Does NOT produce dialogue that violates any voice guide rule — check each rule explicitly
