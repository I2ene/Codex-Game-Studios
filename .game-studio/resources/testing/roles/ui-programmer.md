# Evaluation scenarios: gs-ui-programmer

Professional scenarios adapted from Donchitos' upstream testing guidance; see
[source attribution](../../../NOTICE.md). These are evaluation inputs and domain
checks, not executed results. Read `.codex/agents/gs-ui-programmer.toml` and its current procedure first.
Use [evaluation policy](../README.md) and [category rubric](../quality-rubric.md).

Resolve current config and project engine records. Apply review-mode discipline
coverage without claiming automatic delegation: use the parent when needed, label it,
and record actual participants only. Existing human authorization governs writes;
case approvals represent unresolved decisions and never revoke prior authorization.
Historical fixture versions are scenario inputs, not current API verification.
The linked native procedure governs command arguments, output schemas, receipts,
context and mode applicability. Missing inputs remain NOT ASSESSED.

### Case 1: In-domain request — appropriate output
**Input:** The UX spec at `design/ux/inventory-flow.md` defines five slot states: default, hover, selected, empty-slot, locked-slot. Request: "Implement the inventory screen from the UX spec in `design/ux/inventory-flow.md`."
**Domain checks:**
- Reads the UX spec before producing any code
- Produces implementation using the project's configured UI framework (UI Toolkit, UGUI, UMG, or Godot Control nodes)
- Implements every state the spec defines (default, hover, selected, empty-slot, locked-slot) — none dropped, none invented
- Binds inventory data to UI elements via the project's data model, not hardcoded values
- Includes doc comments on public UI API per coding standards

---

### Case 2: Out-of-domain request — redirects correctly
**Input:** "Design the inventory interaction flow — what happens when the player equips, drops, or combines items."
**Domain checks:**
- Does NOT produce interaction flow design or user flow diagrams
- Explicitly states that UX flow design belongs to `ux-designer`
- Redirects the request to `ux-designer`
- Notes that once the flow spec is ready, it can implement it

---

### Case 3: Custom animation coordination
**Input:** "The item selection in the inventory needs a custom bounce animation when selected."
**Domain checks:**
- Recognizes that the bounce's feel (duration, easing curve, overshoot) is UI interaction and visual design, which it implements but does not design
- Checks the UX spec it is implementing for those values first; does NOT invent them if they are absent
- Asks the spec owner — `ux-designer` for interaction timing, `art-director` for visual style — for the missing values
- Once the values are provided, binds the animation to the selection state, skippable and respecting the player's motion preference

---

### Case 4: Ambiguous UX spec — flags back
**Input:** The UX spec states "show item details on selection" but does not define what happens when an empty slot is selected.
**Domain checks:**
- Identifies the ambiguity in the spec (empty slot selection state is undefined)
- Does NOT make an arbitrary implementation decision for the undefined state
- Flags the ambiguity back to `ux-designer` with the specific question: "What should the detail panel show when an empty inventory slot is selected?"
- Any options it offers (e.g., hide the panel / show a placeholder) go to ux-designer as part of the question — none is implemented before the answer

---

### Case 5: Context pass — engine UI toolkit
**Input:** Engine context provided: project uses Godot 4.6 with Control node UI. Request: "Implement a scrollable item list for the inventory."
**Domain checks:**
- Uses Godot's `ScrollContainer` + `VBoxContainer` + `ItemList` (or equivalent) pattern, not Canvas or UGUI
- Does NOT produce Unity UGUI or Unreal UMG code for a Godot project
- Checks the engine version reference (4.6) for any Control node API changes from 4.4/4.5 before using specific APIs
- Produces GDScript or C# code consistent with the project's configured language
