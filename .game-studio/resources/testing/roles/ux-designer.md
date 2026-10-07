# Evaluation scenarios: gs-ux-designer

Professional scenarios adapted from Donchitos' upstream testing guidance; see
[source attribution](../../../../NOTICE.md). These are evaluation inputs and domain
checks, not executed results. Read `.codex/agents/gs-ux-designer.toml` and its current procedure first.
Use [evaluation policy](../README.md) and [category rubric](../quality-rubric.md).

Resolve current config and project engine records. Apply review-mode discipline
coverage without claiming automatic delegation: use the parent when needed, label it,
and record actual participants only. Existing human authorization governs writes;
case approvals represent unresolved decisions and never revoke prior authorization.
Historical fixture versions are scenario inputs, not current API verification.
The linked native procedure governs command arguments, output schemas, receipts,
context and mode applicability. Missing inputs remain NOT ASSESSED.

### Case 1: In-domain request — appropriate output
**Input:** "Design the inventory management flow for a survival game."
**Domain checks:**
- Before drafting, asks clarifying questions (core player goal, constraints such as input methods and scope, reference games) and presents 2-4 flow options with pros/cons grounded in UX theory (e.g., mental models, progressive disclosure, Fitts's Law), with a recommendation and the final choice deferred to the user
- The drafted flow maps each step and transition: open, browse, select item, sub-actions (equip/drop/combine), close — and names the friction points it removes
- Specifies button assignments and contextual actions for each input method in scope (keyboard/mouse, gamepad, touch if applicable)
- Specifies player feedback for each action (visual, audio, haptic) so the player always knows what happened and why
- Checks the flow against the agent's Accessibility Checklist (keyboard-only, gamepad-only, not reliant on color alone, readable at minimum font size)
- Does NOT produce visual design (colors, icons) or implementation code
- [ ] Preserve unresolved human decisions and declines; perform routine writes already authorized and ask only for missing decisions or scope.

---

### Case 2: Out-of-domain request — redirects correctly
**Input:** "Implement the inventory screen in GDScript with drag-and-drop support."
**Domain checks:**
- Does NOT produce implementation code
- Explicitly states that UI code implementation belongs to `ui-programmer`
- Redirects the request to `ui-programmer`
- Offers the part of the request it does own: the drag-and-drop interaction design (drag affordance, valid/invalid drop feedback, and a non-drag equivalent so the screen stays usable with gamepad only and keyboard only) for ui-programmer to implement against

---

### Case 3: Flow depth conflict — simplification
**Input:** "The lead designer says the current 5-step crafting flow is too deep; maximum 3 steps allowed."
**Domain checks:**
- Presents 2-4 ways to reach a 3-step flow, each with pros/cons and a recommendation, and defers the choice to the user
- For each option, shows which of the 5 steps are merged or removed and what each removed step did for the player, so the usability cost of the collapse is visible
- Does NOT drop a step whose player goal has nowhere else to happen without saying so
- Flags any required use case the 3-step limit cannot serve for user input, and proposes an alternative (e.g., progressive disclosure of advanced options)

---

### Case 4: Accessibility conflict
**Input:** "The onboarding flow uses a timed prompt (auto-advances after 3 seconds) to keep pace, but this conflicts with accessibility requirements for user-controlled timing."
**Domain checks:**
- Identifies the conflict: an auto-advancing prompt takes timing out of the player's control
- Does NOT keep the auto-advance to preserve pace — accessibility requirements are not overridden for aesthetics
- Coordinates with `accessibility-specialist`, which owns the WCAG criterion that applies (SC 2.2.1 Timing Adjustable), to agree on a compliant solution
- Presents alternatives as options with pros/cons — player-advanced prompt, skip or pause control, a setting to disable auto-advance — and shows how each keeps the onboarding's information pacing

---

### Case 5: Context pass — player mental model research
**Input:** Playtest research provided in context: "Players consistently expected the 'Crafting' option to be inside the Inventory screen, not in a separate top-level menu." Request: "Redesign the navigation IA for crafting."
**Domain checks:**
- References the specific player expectation from the research (crafting expected inside inventory)
- Presents IA options with pros/cons and recommends one that places crafting inside the inventory screen (e.g., a tab or panel), deferring the final choice to the user
- Does NOT recommend a design that contradicts the stated player mental model without explicit justification
- The WHY behind the recommendation cites the playtest finding and names it as the players' mental model
