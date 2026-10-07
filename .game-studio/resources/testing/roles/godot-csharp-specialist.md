# Evaluation scenarios: gs-godot-csharp-specialist

Professional scenarios adapted from Donchitos' upstream testing guidance; see
[source attribution](../../../../NOTICE.md). These are evaluation inputs and domain
checks, not executed results. Read `.codex/agents/gs-godot-csharp-specialist.toml` and its current procedure first.
Use [evaluation policy](../README.md) and [category rubric](../quality-rubric.md).

Resolve current config and project engine records. Apply review-mode discipline
coverage without claiming automatic delegation: use the parent when needed, label it,
and record actual participants only. Existing human authorization governs writes;
case approvals represent unresolved decisions and never revoke prior authorization.
Historical fixture versions are scenario inputs, not current API verification.
The linked native procedure governs command arguments, output schemas, receipts,
context and mode applicability. Missing inputs remain NOT ASSESSED.

### Case 1: In-domain request — appropriate output
**Input:** "Create an export property for enemy health with validation that clamps it between 1 and 1000."
**Domain checks:**
- Produces a C# property with `[Export]` attribute
- Uses a backing field with a property getter/setter that clamps the value in the setter
- Does NOT use a raw `[Export]` public field without validation
- Follows Godot 4 C# naming conventions (PascalCase for properties, fields private with underscore prefix)
- Includes XML doc comment on the property per coding standards

---

### Case 2: Out-of-domain request — redirects correctly
**Input:** "Rewrite this enemy health system in GDScript."
**Domain checks:**
- Does NOT produce GDScript code
- Explicitly states that GDScript authoring belongs to `godot-gdscript-specialist`
- Redirects the request to `godot-gdscript-specialist`
- Any hand-off it offers describes the existing C# system's API (its signals and public methods) for godot-gdscript-specialist to port — it contains no GDScript

---

### Case 3: Async signal awaiting
**Input:** "Wait for an animation to finish before transitioning game state using C# async."
**Domain checks:**
- Produces a proper `async Task` pattern using `ToSignal()` to await a Godot signal
- Uses `await ToSignal(animationPlayer, AnimationPlayer.SignalName.AnimationFinished)`
- Does NOT use `Thread.Sleep()` or `Task.Delay()` as a polling substitute
- Notes that the calling method must be `async` and that fire-and-forget `async void` is only acceptable for event handlers
- Checks `IsInstanceValid(this)` after the `await` before transitioning state — the node may have been freed while waiting
- If the animation might never finish (interrupted, replaced), raises that as an unspecified edge case for the user to decide; any timeout it adds uses `GetTree().CreateTimer()`, never `Task.Delay()`

---

### Case 4: Threading model conflict
**Input:** "This C# code accesses a Godot Node from a background Task thread to update its position."
**Domain checks:**
- Flags this as a race condition risk: Godot nodes are not thread-safe and must only be accessed from the main thread
- Does NOT approve or implement the multi-threaded node access pattern
- Provides the correct pattern: use `CallDeferred()`, `Callable.From().CallDeferred()`, or marshal back to the main thread via a thread-safe queue
- Explains why the code compiles yet is unsafe: the `Task` body runs on a .NET thread-pool thread and nothing in C# stops it touching a Node — the main-thread rule belongs to Godot's scene tree

---

### Case 5: Context pass — Godot 4.6 API correctness
**Input:** Engine version context: Godot 4.6. Request: "Connect a signal using the new typed signal delegate pattern."
**Domain checks:**
- Produces C# signal connection using the typed delegate pattern introduced in Godot 4 C# (`+=` operator on typed signal)
- Checks the 4.6 context to confirm no breaking changes to the signal delegate API in 4.4, 4.5, or 4.6
- Does NOT use the old string-based `Connect("signal_name", callable)` pattern (deprecated in Godot 4 C#)
- Produces code compatible with the project's pinned 4.6 version as documented in VERSION.md
