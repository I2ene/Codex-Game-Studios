# Evaluation scenarios: gs-ue-umg-specialist

Professional scenarios adapted from Donchitos' upstream testing guidance; see
[source attribution](../../../../NOTICE.md). These are evaluation inputs and domain
checks, not executed results. Read `.codex/agents/gs-ue-umg-specialist.toml` and its current procedure first.
Use [evaluation policy](../README.md) and [category rubric](../quality-rubric.md).

Resolve current config and project engine records. Apply review-mode discipline
coverage without claiming automatic delegation: use the parent when needed, label it,
and record actual participants only. Existing human authorization governs writes;
case approvals represent unresolved decisions and never revoke prior authorization.
Historical fixture versions are scenario inputs, not current API verification.
The linked native procedure governs command arguments, output schemas, receipts,
context and mode applicability. Missing inputs remain NOT ASSESSED.

### Case 1: In-domain request — inventory widget with data binding
**Input**: "Create an inventory widget that shows a grid of item slots. Each slot should display item icon, quantity, and rarity color. It needs to update when the inventory changes."
**Domain checks**:
- Produces a UMG widget structure: a parent WBP_Inventory containing a UniformGridPanel or TileView, with a child WBP_InventorySlot widget per item
- Describes data binding approach: either Event Dispatchers on an Inventory Component triggering a refresh, or a TileView fed UObject-based item data (not raw structs); it names the entry widget's list-entry interface (`IUserObjectListEntry`) and marks it unverified against `<project-engine-reference>/unreal/`, which does not document it
- Specifies how rarity color is driven: a WidgetStyle asset or a data table lookup, not hardcoded color values
- Output includes the widget hierarchy, binding pattern, and the refresh trigger mechanism

---

### Case 2: Out-of-domain request — UX flow design
**Input**: "Design the full navigation flow for our inventory system — how the player opens it, transitions to character stats, and exits to the pause menu."
**Domain checks**:
- Does not produce a navigation flow or screen transition architecture
- Names ux-designer, its coordination partner for interaction design, as the owner of the flow, and offers to build the screens on its layered architecture (Menu Layer, `UCommonActivatableWidgetStack`) once the flow is defined
- Does not make UX decisions (back button behavior, transition animations, modal vs. fullscreen) without a UX spec — it asks for the spec or lists these as open questions instead

---

### Case 3: Domain boundary — CommonUI input action mismatch
**Input**: "Our inventory widget isn't responding to the controller Back button. We're using CommonUI."
**Domain checks**:
- Identifies the likely causes: the widget's Back binding does not point at the Back row of the project's `CommonInputActionDataBase` data table, or the widget is not the activated, focused screen on its stack
- Explains the CommonUI input routing model: screens derive from `UCommonActivatableWidget` and bind UI actions to data-table rows; only the focused, activated widget consumes input and unfocused widgets ignore it
- Provides the fix: verify the Back binding's data-table row and that the widget is pushed onto (and active on) its activatable-widget stack
- Distinguishes this from a hardware input binding issue (which would be Enhanced Input territory)

---

### Case 4: Widget performance issue — many widget instances per frame
**Input**: "Our leaderboard widget creates 500 individual WBP_LeaderboardRow instances at once. The game hitches for 300ms when opening the leaderboard."
**Domain checks**:
- Identifies the root cause: 500 widget instantiations in a single frame causes a construction hitch
- Recommends switching to ListView or TileView with virtualization — only visible rows are constructed
- Explains the ListView data requirement: each row's data is a UObject-based entry item, not a raw struct; it names the row widget's list-entry interface (`IUserObjectListEntry`) and marks it unverified against `<project-engine-reference>/unreal/`
- If ListView is not appropriate, recommends pooling: pre-instantiate a fixed number of rows and recycle them with new data
- Output is a concrete recommendation with the specific UMG component to use, not a vague "optimize it"

---

### Case 5: Context pass — CommonUI setup already configured
**Input context**: Project uses CommonUI; its `CommonInputActionDataBase` data table defines these input action rows: Confirm, Back, Pause, Secondary.
**Input**: "Add a 'Sort Inventory' button to the inventory widget that works with CommonUI."
**Domain checks**:
- Uses the existing Secondary row (or recommends adding a new Sort row if Secondary is already allocated on this screen)
- Does NOT invent a new input action without noting that it must be added as a row to the project's CommonUI input action data table
- Uses a `UCommonButtonBase` for the button and CommonUI's input routing — not a non-CommonUI binding (e.g., raw key press in Event Graph or `APlayerController::InputComponent`)
- References the provided action rows explicitly in the recommendation
