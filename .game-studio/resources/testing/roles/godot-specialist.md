# Evaluation scenarios: gs-godot-specialist

Professional scenarios adapted from Donchitos' upstream testing guidance; see
[source attribution](../../../../NOTICE.md). These are evaluation inputs and domain
checks, not executed results. Read `.codex/agents/gs-godot-specialist.toml` and its current procedure first.
Use [evaluation policy](../README.md) and [category rubric](../quality-rubric.md).

Resolve current config and project engine records. Apply review-mode discipline
coverage without claiming automatic delegation: use the parent when needed, label it,
and record actual participants only. Existing human authorization governs writes;
case approvals represent unresolved decisions and never revoke prior authorization.
Historical fixture versions are scenario inputs, not current API verification.
The linked native procedure governs command arguments, output schemas, receipts,
context and mode applicability. Missing inputs remain NOT ASSESSED.

### Case 1: In-domain request — appropriate output
**Input:** "When should I use signals vs. direct method calls in Godot?"
**Domain checks:**
- Produces a pattern decision guide with rationale:
  - Signals: decoupled communication, parent-to-child ignorance, event-driven UI updates, one-to-many notification
  - Direct calls: tightly-coupled systems where the caller needs a return value, or performance-critical hot paths
- Illustrates each side with a concrete Godot case (e.g., a child health component emitting a typed `health_changed` signal that its parent or the HUD listens to; a parent calling a method on a child it owns)
- Does NOT produce raw code for both patterns — refers to gdscript-specialist or csharp-specialist for implementation
- Notes the "call down, signal up" convention: a child does not call its parent's methods directly — it emits a signal — so each scene stays self-contained with no implicit dependency on its parent

---

### Case 2: Wrong-engine redirect
**Input:** "Write a MonoBehaviour that runs on Start() and subscribes to a UnityEvent."
**Domain checks:**
- Does NOT produce Unity MonoBehaviour code
- Clearly identifies that this is a Unity pattern, not a Godot pattern
- Maps the concepts to Godot: `_ready()` instead of `Start()`, and a typed Godot `signal` connected in `_ready()` instead of a UnityEvent
- Grounds the answer in the project's engine pin (`<project-engine-reference>/godot/VERSION.md`, Godot 4.6) rather than asking which engine the project uses
- Routes the actual node script to godot-gdscript-specialist or godot-csharp-specialist rather than writing it itself
- Variant: with `engine.name: Unity` in `project.yaml`, it says it is the wrong specialist for this project instead of mapping the concepts

---

### Case 3: Post-cutoff API risk
**Input:** "Use the new Godot 4.5 @abstract annotation to define an abstract base class."
**Domain checks:**
- Identifies that `@abstract` is a post-cutoff feature (introduced in Godot 4.5, after LLM knowledge cutoff)
- Flags the version risk: LLM knowledge of this annotation may be incomplete or incorrect, so the reference docs take precedence
- Confirms the feature against the version reference before answering — `<project-engine-reference>/godot/breaking-changes.md` lists the `@abstract` decorator in its 4.4 → 4.5 table
- Flags the installed-version gap: `VERSION.md` records `Installed at pin time` as NOT DETERMINED, so the installed editor must be confirmed as 4.5 or later before `@abstract` code will parse
- Routes the class authoring to godot-gdscript-specialist rather than writing the class itself

---

### Case 4: Language selection for a hot path
**Input:** "The physics query loop runs every frame for 500 objects. Should we use GDScript or C# for this?"
**Domain checks:**
- Provides a balanced analysis:
  - GDScript: simpler, team familiar, but slower for tight loops
  - C#: faster for CPU-intensive loops, requires .NET runtime, team needs C# knowledge
- Does NOT make the final decision unilaterally — presents the trade-off for the user to decide
- Flags that bringing C#/.NET (or a GDExtension module) into the project is a major tech choice that needs `technical-director` sign-off, not a call it makes alone
- Notes that GDExtension (C++) is a third option for extreme performance cases and recommends escalating if C# is insufficient

---

### Case 5: Context pass — engine version 4.6
**Input:** Engine version context provided: Godot 4.6, Jolt as default physics. Request: "Set up a RigidBody3D for the player character."
**Domain checks:**
- Reads the 4.6 context and the physics module reference (`<project-engine-reference>/godot/modules/physics.md`) rather than relying on LLM training data alone
- States what the reference documents: Jolt is the default 3D engine for new projects, but existing projects keep their setting — so it checks Project Settings → Physics → 3D → Physics Engine before assuming Jolt
- Carries over the documented Jolt differences that apply: collision margins may behave differently, and Jolt emits runtime warnings for properties it does not support (e.g. HingeJoint3D `damp`)
- Does NOT invent RigidBody3D property changes between GodotPhysics and Jolt — the reference documents none, and it says so
