# Evaluation scenarios: gs-prototyper

Professional scenarios adapted from Donchitos' upstream testing guidance; see
[source attribution](../../../NOTICE.md). These are evaluation inputs and domain
checks, not executed results. Read `.codex/agents/gs-prototyper.toml` and its current procedure first.
Use [evaluation policy](../README.md) and [category rubric](../quality-rubric.md).

Resolve current config and project engine records. Apply review-mode discipline
coverage without claiming automatic delegation: use the parent when needed, label it,
and record actual participants only. Existing human authorization governs writes;
case approvals represent unresolved decisions and never revoke prior authorization.
Historical fixture versions are scenario inputs, not current API verification.
The linked native procedure governs command arguments, output schemas, receipts,
context and mode applicability. Missing inputs remain NOT ASSESSED.

### Case 1: In-domain request — prototype a card-drawing mechanic
**Input**: "Prototype a card-drawing mechanic in 2 hours. The core question: does drawing 3 cards per turn with hand-size limit of 7 feel good? I need something to test in a playtest today."
**Domain checks**:
- States the falsifiable hypothesis ("If the player draws 3 cards per turn with a hand limit of 7, they will feel [Y] — evidenced by [Z]") and the riskiest assumption before building
- Recommends a prototype path with rationale — a card mechanic where timing precision is not the question points to the HTML or Paper path, not the Engine path
- Proposes scope in 3–5 bullets (deck, draw N, hand limit 7, a minimal state display) and gets confirmation before building
- Output goes to `prototypes/card-draw-concept/` (e.g., a single self-contained `prototype.html` that opens by double-click, or `rules.md` + `play-log.md` on the Paper path); every code file starts with the `PROTOTYPE - NOT FOR PRODUCTION` header naming the question and date
- Code prioritizes speed over correctness: no unit tests, no doc comments required, global state is acceptable; no menus or polish
- Does NOT implement production patterns (dependency injection, signals, data-driven config) unless they take less time than not using them
- [ ] Preserve unresolved human decisions and declines; perform routine writes already authorized and ask only for missing decisions or scope.

---

### Case 2: Out-of-domain request — production-grade implementation
**Input**: "The card mechanic prototype worked great. Now write the production implementation of the card system for src/gameplay/cards/."
**Domain checks**:
- Does not write production code to `src/`
- States clearly that prototype code is throwaway: production implementation of a validated mechanic is written from scratch to proper standards, and the prototype is reference only
- Points to the prototype's `REPORT.md` (hypothesis, result, recommendation, tuning values discovered, lessons learned) as what carries into production — offering to write it if it does not exist yet — so the knowledge transfers, not the code
- Routes production architecture questions to `lead-programmer`
- Does NOT copy the prototype code into src/ or suggest it as a starting point without warning about its non-production quality

---

### Case 3: Prototype validates the mechanic — recommendation output
**Input**: "The card-draw prototype playtested well. Three sessions all enjoyed drawing 3 cards/turn with hand limit 7. No confusion observed. What's next?"
**Domain checks**:
- [ ] Preserve unresolved human decisions and declines; perform routine writes already authorized and ask only for missing decisions or scope. Preserve the stated artifact obligations for `prototypes/card-draw-concept/REPORT.md`.
- Report includes: the hypothesis tested, riskiest assumption, Result as specific observations (3 sessions, no confusion observed), playtester count and a hypothesis verdict of CONFIRMED, **Recommendation: PROCEED** with that evidence, the tuning values to preserve (3 cards/turn, hand limit 7), and lessons learned
- Updates `prototypes/index.md` after the report is written
- Presents PROCEED as a recommendation — the decision belongs to the user / creative-director, not the prototyper
- Does NOT begin writing production code; the next step it points to is design work (GDDs), not implementation
- Output is structured as a decision-ready recommendation, not a narrative summary

---

### Case 4: Prototype reveals the mechanic is unworkable — abandonment note
**Input**: "The prototype for the physics-based lock-picking mechanic is done. After 4 playtest sessions, all testers found it frustrating — too much precision required, not fun. One tester rage-quit."
**Domain checks**:
- [ ] Preserve unresolved human decisions and declines; perform routine writes already authorized and ask only for missing decisions or scope. Preserve the stated artifact obligations for `prototypes/lock-picking-physics-concept/REPORT.md`.
- Report includes: the hypothesis tested, a hypothesis verdict of REFUTED, and specific reasons as observations (precision barrier too high, negative emotional response across all 4 sessions, rage-quit incident as evidence)
- **Recommendation: KILL** for the physics-based approach — or PIVOT only with a concrete pivot direction and what to keep (e.g., a simplified key-tumbler or rhythm-based mechanic); never PROCEED
- Does NOT recommend persisting with the prototype mechanic because of sunk cost — the verdict is based on evidence, not effort invested
- Does NOT mark the result as inconclusive — after 4 sessions with consistent negative responses, the evidence supports a decision

---

### Case 5: Context pass — using the project's engine scripting language
**Input context**: Project uses Godot 4.6 with GDScript (`engine.name` and `engine.language` in `project.yaml`); the user has chosen the Engine path.
**Input**: "Prototype a basic grid movement system — player clicks a tile and the character moves to it."
**Domain checks**:
- Produces the prototype in GDScript — not Python, C#, or pseudocode
- Uses Godot 4.6 node types appropriate for a grid: TileMapLayer (not TileMap, which `<project-engine-reference>/godot/deprecated-apis.md` lists as deprecated since 4.3) or a custom grid manager node, CharacterBody2D or Node2D for the player
- Does NOT apply production coding standards (no required test coverage, no doc comments, global state acceptable)
- Writes the output to `prototypes/grid-movement-concept/` not to `src/`
- After writing, hands control back: asks the user to run the project and paste any errors or describe what they observe, rather than assuming it worked
- If a Godot 4.6 API is uncertain, flags the specific API with a note to verify against the Godot 4.6 docs — `<project-engine-reference>/godot/VERSION.md` reaches the agent through `AGENTS.md`'s import, and its Knowledge Gap Warning says to cross-reference that directory before suggesting Godot API calls
