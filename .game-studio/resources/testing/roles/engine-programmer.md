# Evaluation scenarios: gs-engine-programmer

Professional scenarios adapted from Donchitos' upstream testing guidance; see
[source attribution](../../../NOTICE.md). These are evaluation inputs and domain
checks, not executed results. Read `.codex/agents/gs-engine-programmer.toml` and its current procedure first.
Use [evaluation policy](../README.md) and [category rubric](../quality-rubric.md).

Resolve current config and project engine records. Apply review-mode discipline
coverage without claiming automatic delegation: use the parent when needed, label it,
and record actual participants only. Existing human authorization governs writes;
case approvals represent unresolved decisions and never revoke prior authorization.
Historical fixture versions are scenario inputs, not current API verification.
The linked native procedure governs command arguments, output schemas, receipts,
context and mode applicability. Missing inputs remain NOT ASSESSED.

### Case 1: In-domain request — appropriate output
**Input:** "Implement a custom object pool for projectiles to avoid per-frame allocation."
**Domain checks:**
- Produces an engine-level object pool implementation with acquire/release interface
- Pool is typed to the projectile object type, uses pre-allocated fixed-size storage
- Provides thread-safety notes (or clearly marks as single-threaded-only with rationale)
- Includes doc comments on the public API per coding standards
- Output is compatible with the project's configured engine and language

---

### Case 2: Out-of-domain request — redirects correctly
**Input:** "Add a wall-jump ability to the player controller."
**Domain checks:**
- Does NOT produce the wall-jump gameplay code
- Explicitly states that gameplay features belong to `gameplay-programmer`
- Redirects the request to `gameplay-programmer`
- If it offers an engine-level query the ability can call (e.g., wall contact and surface normal), that API does not depend on gameplay code (strict dependency direction)

---

### Case 3: Memory leak diagnosis
**Input:** "Memory usage grows by ~50MB per level load and never releases. We suspect the resource loading system."
**Domain checks:**
- Diagnoses by measurement before changing code: memory baseline, repeated load/unload cycles, numbers documented (profile before and after)
- Audits the resource loading/caching and object lifecycle code it owns for references that are never released, naming likely causes (orphaned resource handles, circular references, a cache that never evicts)
- Produces a concrete fix for the identified leak pattern
- Provides a test to verify the fix (memory baseline before load, measure after unload, confirm return to baseline)

---

### Case 4: Cross-domain coordination — shared system optimization
**Input:** "I need to optimize the physics broadphase, but the gameplay system is tightly coupled to the physics query API."
**Domain checks:**
- Does NOT unilaterally change the physics query API surface (would break gameplay-programmer's code)
- Coordinates with `lead-programmer` to plan the change safely
- Proposes a migration path: new optimized API alongside old API, with a deprecation period
- Documents the coordination requirement before proceeding

---

### Case 5: Context pass — checks engine version reference
**Input:** Engine version reference (Godot 4.6) provided in context. Request: "Set up the default physics engine for the project."
**Domain checks:**
- Reads the engine version reference and notes Godot 4.6 change: Jolt physics is now the default
- Produces configuration guidance that accounts for the Jolt-as-default change (4.6 migration note)
- Flags the GodotPhysics3D→Jolt differences `<project-engine-reference>/godot/modules/physics.md` documents — HingeJoint3D `damp` is unsupported under Jolt, collision margins may behave differently, Jolt warns at runtime about unsupported properties — and that existing projects keep their current engine setting; says the reference lists no other API differences rather than inventing any
- Does NOT suggest deprecated or pre-4.6 physics setup steps without noting they apply to older versions
