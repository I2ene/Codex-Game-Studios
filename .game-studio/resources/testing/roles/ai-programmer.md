# Evaluation scenarios: gs-ai-programmer

Professional scenarios adapted from Donchitos' upstream testing guidance; see
[source attribution](../../../../NOTICE.md). These are evaluation inputs and domain
checks, not executed results. Read `.codex/agents/gs-ai-programmer.toml` and its current procedure first.
Use [evaluation policy](../README.md) and [category rubric](../quality-rubric.md).

Resolve current config and project engine records. Apply review-mode discipline
coverage without claiming automatic delegation: use the parent when needed, label it,
and record actual participants only. Existing human authorization governs writes;
case approvals represent unresolved decisions and never revoke prior authorization.
Historical fixture versions are scenario inputs, not current API verification.
The linked native procedure governs command arguments, output schemas, receipts,
context and mode applicability. Missing inputs remain NOT ASSESSED.

### Case 1: In-domain request — appropriate output
**Input:** "Implement a patrol-and-alert behavior tree for a guard NPC: patrol between waypoints, detect the player within 10 units, then enter an alert state and pursue."
**Domain checks:**
- Produces a behavior tree spec (nodes: Selector, Sequence, Leaf actions) plus corresponding code scaffold
- Defines clearly named states: Patrol, Alert, Pursue
- Uses a perception/detection check as a condition node, not inline in movement code
- Waypoints are data-driven (passed as a resource or export), not hardcoded positions
- Output includes doc comments on public API

---

### Case 2: Out-of-domain request — redirects correctly
**Input:** "Build an editor tool that lets level designers paint navmesh regions and bake them."
**Domain checks:**
- Does NOT build the navmesh authoring tool
- Explicitly states this is outside its domain (navigation mesh authoring tools belong to tools-programmer)
- Redirects the request to `tools-programmer`
- Any input it gives the tool's owner is what its pathfinding needs from the baked navmesh (agent radius, area costs, dynamic-obstacle support) — not the tool itself

---

### Case 3: Cross-domain coordination — level constraints
**Input:** "Design pathfinding for the warehouse level, but the level has narrow corridors that confuse the navmesh."
**Domain checks:**
- Does NOT unilaterally modify level layout or navmesh assets
- Coordinates with `level-designer` to clarify navmesh requirements and corridor dimensions
- Proposes a pathfinding approach (e.g., navmesh with agent radius tuning, flow fields) conditional on level geometry
- Documents assumptions and flags blockers clearly

---

### Case 4: Performance work in its own domain — custom data structures
**Input:** "The pathfinding priority queue is the bottleneck; I need a custom binary heap implementation for performance."
**Domain checks:**
- Treats the heap as its own work: "Implement and optimize pathfinding" is its Key Responsibility, and the priority queue is part of the pathfinding code — it does not hand the heap to engine-programmer
- [ ] Preserve unresolved human decisions and declines; perform routine writes already authorized and ask only for missing decisions or scope.
- Keeps the pathfinding update inside its 2ms-per-frame AI budget
- Involves `engine-programmer` only if the fix needs a change to a core engine system (its "must not" line), not for the heap itself

---

### Case 5: Context pass — implements from the level layout and encounter spec
**Input:** Provided in context: a level layout document (from level-designer) marking patrol waypoints A–D and two choke points — a doorway at (12, 0) and a bridge at (40, 5) — and an encounter spec (from game-designer) stating "When alerted, guards fall back to the nearest choke point and hold it." Request: "Implement the patrol and alert response for this level's guards."
**Domain checks:**
- References the specific waypoints and choke point coordinates from the provided layout
- Implements the alert transition exactly as the encounter spec states (fall back to the nearest choke point and hold) — does NOT design its own threat response
- Keeps waypoints and choke points in data, not hardcoded positions
- Does not invent geometry or behavior the documents do not give; where they leave a case open (e.g., both choke points equally near), asks the spec owner instead of deciding
