# Evaluation scenarios: gs-godot-gdscript-specialist

Professional scenarios adapted from Donchitos' upstream testing guidance; see
[source attribution](../../../../NOTICE.md). These are evaluation inputs and domain
checks, not executed results. Read `.codex/agents/gs-godot-gdscript-specialist.toml` and its current procedure first.
Use [evaluation policy](../README.md) and [category rubric](../quality-rubric.md).

Resolve current config and project engine records. Apply review-mode discipline
coverage without claiming automatic delegation: use the parent when needed, label it,
and record actual participants only. Existing human authorization governs writes;
case approvals represent unresolved decisions and never revoke prior authorization.
Historical fixture versions are scenario inputs, not current API verification.
The linked native procedure governs command arguments, output schemas, receipts,
context and mode applicability. Missing inputs remain NOT ASSESSED.

### Case 1: In-domain request — appropriate output
**Input:** "Review this GDScript file for type annotation coverage."
**Domain checks:**
- Reads the provided GDScript file
- Flags every variable, parameter, and return type that is missing a static type annotation
- Produces a list of specific line-by-line findings: `var speed = 5.0` → `var speed: float = 5.0`
- Notes the performance and tooling benefits of static typing in Godot 4
- Does NOT rewrite the entire file unprompted — produces a findings list for the developer to apply

---

### Case 2: Out-of-domain request — redirects correctly
**Input:** "Write a vertex shader to distort the mesh in world space."
**Domain checks:**
- Does NOT produce shader code in GDScript or in Godot's shading language
- Explicitly states that shader authoring belongs to `godot-shader-specialist`
- Redirects the request to `godot-shader-specialist`
- Any help it offers stays on the script side its redirect line says it owns (`set_shader_parameter()`, material assignment) — it writes no shader code

---

### Case 3: Async loading with coroutines
**Input:** "Load a scene asynchronously and wait for it to finish before spawning it."
**Domain checks:**
- Produces an `await` + `ResourceLoader.load_threaded_request` pattern for Godot 4
- Uses static typing throughout (`var scene: PackedScene`)
- Handles the completion check with `ResourceLoader.load_threaded_get_status()`, awaiting between polls rather than blocking the frame
- Checks `is_instance_valid(self)` after the await before spawning — the node may have been freed while the scene loaded
- Notes error handling for failed loads
- Does NOT use deprecated Godot 3 `yield()` syntax

---

### Case 4: Performance issue — typed array recommendation
**Input:** "The entity update loop is slow; it iterates an untyped Array of 1,000 nodes every frame."
**Domain checks:**
- Identifies that an untyped `Array` foregoes GDScript compiler optimizations
- Recommends converting to a typed array (`Array[Node]` or the specific type) so the compiler can use typed code paths
- Produces the typed array refactor as the immediate fix
- Notes that if profiling still shows the loop as a bottleneck, the next step is moving the hot path to GDExtension (C++/Rust) with godot-gdextension-specialist, per its GDScript/GDExtension boundary
- Does NOT recommend moving the loop, or the codebase, out of GDScript without profiler evidence

---

### Case 5: Context pass — Godot 4.6 with post-cutoff features
**Input:** Engine version context provided: Godot 4.6. Request: "Create an abstract base class for all enemy types using @abstract."
**Domain checks:**
- Identifies `@abstract` as a Godot 4.5+ feature (post-cutoff)
- Notes this in the output: feature introduced in 4.5, confirmed against `<project-engine-reference>/godot/breaking-changes.md` (4.4 → 4.5 table)
- Produces the GDScript class using `@abstract` on the class and its abstract methods, following the reference docs (`current-best-practices.md`) rather than training data
- Flags that `VERSION.md` records `Installed at pin time` as NOT DETERMINED — the installed editor must be 4.5 or later for `@abstract` to parse
- Uses static typing for all method signatures in the abstract class
