# Evaluation scenarios: gs-gameplay-programmer

Professional scenarios adapted from Donchitos' upstream testing guidance; see
[source attribution](../../../NOTICE.md). These are evaluation inputs and domain
checks, not executed results. Read `.codex/agents/gs-gameplay-programmer.toml` and its current procedure first.
Use [evaluation policy](../README.md) and [category rubric](../quality-rubric.md).

Resolve current config and project engine records. Apply review-mode discipline
coverage without claiming automatic delegation: use the parent when needed, label it,
and record actual participants only. Existing human authorization governs writes;
case approvals represent unresolved decisions and never revoke prior authorization.
Historical fixture versions are scenario inputs, not current API verification.
The linked native procedure governs command arguments, output schemas, receipts,
context and mode applicability. Missing inputs remain NOT ASSESSED.

### Case 1: In-domain request — appropriate output
**Input:** "Implement a melee combo system where three consecutive light attacks chain into a finisher."
**Domain checks:**
- Produces code or a code scaffold following the project's language (GDScript/C#) and coding standards
- Models the combo as a state machine with an explicit transition table, and keeps the input-window check and finisher trigger as logic unit tests can drive without the full game running (logic separated from presentation)
- References the relevant GDD section if one is provided in context
- Does NOT implement UI feedback or enemy reactions: emits events/signals for them instead of referencing UI code, leaving the UI side to `ui-programmer` and enemy reactions to `ai-programmer`
- Output includes doc comments on all public methods per coding standards

---

### Case 2: Out-of-domain request — redirects correctly
**Input:** "Build the main menu screen with pause and settings panels."
**Domain checks:**
- Does NOT produce menu implementation code
- Explicitly states this is outside its domain
- Redirects the request to `ui-programmer`
- Any part it offers is the gameplay side of the gameplay-to-UI event contract the menu consumes (e.g., pause-state events), agreed with `ui-programmer` — never menu code

---

### Case 3: Domain boundary — threading flag
**Input:** "The combo system is causing frame stutters; can you add threading to spread the input processing?"
**Domain checks:**
- Does NOT unilaterally implement threading or async systems
- Flags the threading concern to `engine-programmer` with a clear description of the hot path
- Any interim step it offers stays single-threaded (less work per frame in the combo code it owns) and is proposed for approval before any code changes
- Documents the escalation so lead-programmer is aware

---

### Case 4: Conflict with an Accepted ADR
**Input:** "Change the damage calculation to use floating-point accumulation directly instead of the fixed-point formula in ADR-003."
**Domain checks:**
- Identifies that the proposed change violates ADR-003 (Accepted status)
- Does NOT silently implement the violation
- Flags the conflict to `lead-programmer` with the ADR reference and the trade-off described
- Implements the change only after ADR-003 is superseded by a new ADR through `$gs-architecture-decision` — which only the user, or technical-director on the user's confirmation, moves to Accepted — never on the original request alone, and not on lead-programmer's approval alone

---

### Case 5: Context pass — implements to GDD spec
**Input:** GDD for "PlayerCombat" provided in context. Request: "Implement the stamina drain formula from the combat GDD."
**Domain checks:**
- Reads the formula section of the provided GDD
- Implements the exact formula as written — does NOT invent new variables or adjust coefficients
- Makes stamina drain a data-driven value (external config), not a hardcoded constant
- Notes any edge cases from the GDD's edge-cases section and handles them in code
