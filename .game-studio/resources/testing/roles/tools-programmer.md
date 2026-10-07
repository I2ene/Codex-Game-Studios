# Evaluation scenarios: gs-tools-programmer

Professional scenarios adapted from Donchitos' upstream testing guidance; see
[source attribution](../../../../NOTICE.md). These are evaluation inputs and domain
checks, not executed results. Read `.codex/agents/gs-tools-programmer.toml` and its current procedure first.
Use [evaluation policy](../README.md) and [category rubric](../quality-rubric.md).

Resolve current config and project engine records. Apply review-mode discipline
coverage without claiming automatic delegation: use the parent when needed, label it,
and record actual participants only. Existing human authorization governs writes;
case approvals represent unresolved decisions and never revoke prior authorization.
Historical fixture versions are scenario inputs, not current API verification.
The linked native procedure governs command arguments, output schemas, receipts,
context and mode applicability. Missing inputs remain NOT ASSESSED.

### Case 1: In-domain request — appropriate output
**Input:** "Create a custom editor tool for placing enemy patrol waypoints in the level."
**Domain checks:**
- Produces an editor extension spec and code scaffold for the configured engine (e.g., Godot EditorPlugin, Unity Editor window, Unreal Detail Customization)
- Tool allows designer to click-place waypoints in the scene/viewport
- Waypoints are serialized as engine-native resource (not hardcoded) so level-designer can edit without code
- Includes undo/redo support per editor plugin best practices
- Does NOT modify the AI pathfinding runtime code (that belongs to ai-programmer)

---

### Case 2: Out-of-domain request — redirects correctly
**Input:** "Implement the enemy melee combo system in code."
**Domain checks:**
- Does NOT produce gameplay mechanic code
- Explicitly states that combat system implementation belongs to `gameplay-programmer`
- Redirects the request to `gameplay-programmer`
- Any part it offers is tooling on its side of the line — e.g., a debug overlay that visualizes combo state — never combo logic

---

### Case 3: Runtime data access — coordination required
**Input:** "The waypoint editor must check at edit time that every patrol segment is walkable, but the collision queries that answer this live in the game's runtime code and the editor cannot call them."
**Domain checks:**
- Identifies that the tool needs a runtime query the editor cannot yet call, and that adding one is a change to game runtime code
- Does NOT add the runtime hook itself — delegates it to `engine-programmer` (collision queries are engine-level runtime code) and asks before coordinating ("This will require changes to [other system]. Should I coordinate with that first?")
- Documents the read-only interface the tool needs (inputs, outputs, called from editor context) before implementing the tool
- Reports failing segments as clear, actionable errors rather than silently skipping them

---

### Case 4: Engine version breakage
**Input:** "After the engine upgrade, the waypoint editor tool crashes on startup."
**Domain checks:**
- Checks the engine version reference (`<project-engine-reference>/`) before touching editor plugin APIs, including the pinned version in VERSION.md against the upgraded editor (an `Installed at pin time` of NOT DETERMINED is an unknown gap, not a match)
- Looks for the failing API in the reference's breaking-changes and deprecated-APIs files rather than recalling it from training data; if they do not cover it, says so instead of asserting a cause
- Produces a targeted fix for the breaking change
- Tests the fix on representative data before calling the tool fixed

---

### Case 5: Context pass — art pipeline requirements
**Input:** Art pipeline requirements provided in context: "All texture imports must set compression to VRAM Compressed, generate mipmaps, and tag with a LOD group." Request: "Build an asset import tool that enforces these settings."
**Domain checks:**
- References all three requirements from the context: VRAM compression, mipmap generation, LOD group tagging
- Produces an import tool that validates and applies all three settings on import
- Adds a warning or error report for assets that fail to meet the specified settings
- Treats the three settings as given: does NOT change or add requirements itself — any change it thinks is needed is raised with `technical-artist`, its partner for art pipeline tools
