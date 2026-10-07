# Evaluation scenarios: gs-godot-gdextension-specialist

Professional scenarios adapted from Donchitos' upstream testing guidance; see
[source attribution](../../../../NOTICE.md). These are evaluation inputs and domain
checks, not executed results. Read `.codex/agents/gs-godot-gdextension-specialist.toml` and its current procedure first.
Use [evaluation policy](../README.md) and [category rubric](../quality-rubric.md).

Resolve current config and project engine records. Apply review-mode discipline
coverage without claiming automatic delegation: use the parent when needed, label it,
and record actual participants only. Existing human authorization governs writes;
case approvals represent unresolved decisions and never revoke prior authorization.
Historical fixture versions are scenario inputs, not current API verification.
The linked native procedure governs command arguments, output schemas, receipts,
context and mode applicability. Missing inputs remain NOT ASSESSED.

### Case 1: In-domain request — appropriate output
**Input:** "Expose a C++ rigid-body physics simulation library to GDScript via GDExtension."
**Domain checks:**
- Produces a GDExtension binding pattern using godot-cpp:
  - Class inheriting from `godot::Object` or an appropriate Godot base class
  - `GDCLASS` macro registration
  - `_bind_methods()` implementation exposing the physics API to GDScript
  - Module entry point: `initialize_module` in `register_types.cpp` registers the class with `ClassDB::register_class<T>()` at `MODULE_INITIALIZATION_LEVEL_SCENE`, reached from the exported init function named by the manifest's `entry_symbol`
- Notes the `.gdextension` manifest file format required
- Does NOT produce the GDScript usage code (that belongs to gdscript-specialist)

---

### Case 2: Out-of-domain redirect
**Input:** "Write the GDScript that calls the physics simulation from Case 1."
**Domain checks:**
- Does NOT produce GDScript code
- Explicitly states that GDScript authoring belongs to `godot-gdscript-specialist`
- Redirects to `godot-gdscript-specialist`
- Any hand-off it offers is the extension's bound API surface (method names, parameter and return types) — not GDScript that calls it

---

### Case 3: ABI compatibility risk — minor version update
**Input:** "We're upgrading from Godot 4.5 to 4.6. Will our existing GDExtension still work?"
**Domain checks:**
- States the compatibility direction: an extension built for 4.5 should load in 4.6, but not the reverse — so it may keep working, yet it must be re-tested, and rebuilt against 4.6 to use newer APIs
- Directs to check the 4.5→4.6 migration guide for GDExtension API changes
- Recommends rebuilding against the 4.6 godot-cpp headers rather than treating "should load" as tested
- Notes that the `.gdextension` manifest may need a `compatibility_minimum` version update
- Lays out the rebuild as a checklist: rebuild debug and release (`scons ... target=template_debug` / `template_release`, or `cargo build` / `cargo build --release`) for every target platform, update `compatibility_minimum`, then re-test in the 4.6 editor before shipping

---

### Case 4: Memory management — RAII for Godot objects
**Input:** "How should we manage the lifecycle of Godot objects created inside C++ GDExtension code?"
**Domain checks:**
- Produces the RAII-based lifecycle pattern for Godot objects in GDExtension:
  - `Ref<T>` for reference-counted objects (auto-released when Ref goes out of scope)
  - `memnew()` / `memdelete()` for non-reference-counted objects
  - Warning: do NOT use `new`/`delete` for Godot objects — undefined behavior
- Notes object ownership rules: who is responsible for freeing a node added to the scene tree
- Its concrete example (e.g., a `CollisionShape3D` created in C++) applies both rules: the node is created with `memnew()` and handed to the scene tree with `add_child()`, after which the tree frees it (no `memdelete()`); its shape resource is held in a `Ref<>`; `memdelete()` is only for a node that never enters the tree

---

### Case 5: Context pass — Godot 4.6 GDExtension API check
**Input:** Engine version context: Godot 4.6 (upgrading from 4.5). Request: "Check if any GDExtension APIs changed from 4.5 to 4.6."
**Domain checks:**
- References the 4.5→4.6 migration guide from the VERSION.md verified sources list
- Reads the 4.5 → 4.6 table in `<project-engine-reference>/godot/breaking-changes.md` and states explicitly that it has no GDExtension-specific row, with the caveat to verify against the official changelog
- Still surfaces the listed 4.6 changes that reach native code: `Quaternion` now initializes to identity (it was zero)
- Flags the D3D12 default on Windows (4.6 change) as potentially relevant for GDExtension rendering code
- Provides a checklist of what to verify after upgrading
