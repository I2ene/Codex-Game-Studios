# Evaluation scenarios: gs-unity-specialist

Professional scenarios adapted from Donchitos' upstream testing guidance; see
[source attribution](../../../../NOTICE.md). These are evaluation inputs and domain
checks, not executed results. Read `.codex/agents/gs-unity-specialist.toml` and its current procedure first.
Use [evaluation policy](../README.md) and [category rubric](../quality-rubric.md).

Resolve current config and project engine records. Apply review-mode discipline
coverage without claiming automatic delegation: use the parent when needed, label it,
and record actual participants only. Existing human authorization governs writes;
case approvals represent unresolved decisions and never revoke prior authorization.
Historical fixture versions are scenario inputs, not current API verification.
The linked native procedure governs command arguments, output schemas, receipts,
context and mode applicability. Missing inputs remain NOT ASSESSED.

### Case 1: In-domain request — appropriate output
**Input:** "Should I use MonoBehaviour or ScriptableObject for storing enemy configuration data?"
**Domain checks:**
- Produces a pattern decision tree covering:
  - MonoBehaviour: for runtime behavior, needs to be attached to a GameObject, has Update() lifecycle
  - ScriptableObject: for pure data/configuration, exists as an asset, shared across instances, no scene dependency
- Recommends ScriptableObject for enemy configuration data (stateless, reusable, designer-friendly)
- Notes that MonoBehaviour can reference the ScriptableObject for runtime use
- Provides a concrete example of what the ScriptableObject class definition looks like (does not produce full code — refers to engine-programmer or gameplay-programmer for implementation)

---

### Case 2: Wrong-engine redirect
**Input:** "Set up a Node scene tree with signals for this enemy system."
**Domain checks:**
- Does NOT produce Godot Node/signal code
- Identifies node trees and signals as Godot concepts
- Confirms the project's engine from `engine.name` in `project.yaml` rather than guessing; if it is not Unity, says it is the wrong specialist for this project instead of translating
- If `engine.name` is unset, says no engine is configured and asks which engine the project uses — it does not assume Unity
- In a Unity project, maps the concepts: node tree → GameObject hierarchy with composed MonoBehaviours; signal → C# event or UnityEvent (consistent with its own rule to use events instead of `SendMessage()` / `Find()`)
- Does not hand the request to a Godot specialist — its Agent grant covers only the four Unity sub-specialists

---

### Case 3: Unity version API flag
**Input:** "Use the new Unity 6 GPU resident drawer for batch rendering."
**Domain checks:**
- Checks `<project-engine-reference>/unity/VERSION.md` and `<project-engine-reference>/unity/modules/rendering.md` before answering, not training data (the version file places Unity 6 past the model's knowledge cutoff)
- States what the reference documents: GPU Resident Drawer is a Unity 6+ feature enabled in the URP Asset (Rendering > GPU Resident Drawer), so it requires an SRP project
- Flags the installed-version gap: when `Installed at pin time` in the version file is not determined, asks which editor version is installed before recommending the feature
- Does NOT assume the installed editor is Unity 6 because the reference is pinned to it
- Proposes the URP Asset change and asks before editing it; routes render pipeline customization beyond the setting to `unity-shader-specialist`

---

### Case 4: DOTS vs. MonoBehaviour conflict
**Input:** "The combat system uses MonoBehaviour for state management, but we want to add a DOTS-based projectile system. Can they coexist?"
**Domain checks:**
- Recognizes this as a hybrid architecture scenario
- Explains the coexistence mechanism at architecture level, as `<project-engine-reference>/unity/plugins/dots-entities.md` documents it: authoring MonoBehaviours baked into entities by a `Baker<T>`, projectile data held in `IComponentData`, processed by an `ISystem`
- Notes the performance and complexity trade-offs of mixing the two patterns
- Recommends escalating the architecture decision to `lead-programmer` or `technical-director`
- Defers to `unity-dots-specialist` for the DOTS-side implementation details

---

### Case 5: Context pass — Unity version
**Input:** Project context provided: Unity 6.3 LTS, keyboard/mouse and gamepad targets. Request: "Configure the new Input System for this project."
**Domain checks:**
- Applies the Unity 6.3 LTS context from `<project-engine-reference>/unity/modules/input.md`: the Input System package (`com.unity.inputsystem`) with Active Input Handling set to the new system
- Does NOT produce legacy Input Manager code (`Input.GetKeyDown()`, `Input.GetAxis()`) — the engine reference lists these as deprecated
- Defines actions in an `.inputactions` asset, uses the Player Input component or a generated C# class, and prefers action callbacks (`performed`, `canceled`) over polling in `Update()`
- Sets up keyboard+mouse and gamepad control schemes with automatic switching
- Routes UI navigation and input-prompt work to `unity-ui-specialist`
- [ ] Preserve unresolved human decisions and declines; perform routine writes already authorized and ask only for missing decisions or scope.
