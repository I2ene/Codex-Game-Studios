# Evaluation scenarios: gs-unreal-specialist

Professional scenarios adapted from Donchitos' upstream testing guidance; see
[source attribution](../../../NOTICE.md). These are evaluation inputs and domain
checks, not executed results. Read `.codex/agents/gs-unreal-specialist.toml` and its current procedure first.
Use [evaluation policy](../README.md) and [category rubric](../quality-rubric.md).

Resolve current config and project engine records. Apply review-mode discipline
coverage without claiming automatic delegation: use the parent when needed, label it,
and record actual participants only. Existing human authorization governs writes;
case approvals represent unresolved decisions and never revoke prior authorization.
Historical fixture versions are scenario inputs, not current API verification.
The linked native procedure governs command arguments, output schemas, receipts,
context and mode applicability. Missing inputs remain NOT ASSESSED.

### Case 1: In-domain request — Blueprint vs C++ decision criteria
**Input**: "Should I implement our combo attack system in Blueprint or C++?"
**Domain checks**:
- Applies its stated default: C++ for the combo system's framework, Blueprint for content and prototyping
- Routes the combat logic through GAS (combo attacks as Gameplay Abilities, combo state as Gameplay Tags, montage flow via Ability Tasks) and names ue-gas-specialist for the GAS design rather than implementing it itself
- Recommends Blueprint for designer-tunable values (exposed with `EditAnywhere` / `BlueprintReadWrite`, data-only Blueprints for combo variations, `BlueprintNativeEvent` where designers override behavior)
- Cites its ~20-nodes-per-function threshold as the point where Blueprint combo logic belongs in C++
- Does NOT render a final verdict without knowing project context — asks clarifying questions if context is absent
- Presents the split as a proposed class structure with its trade-offs, not a freeform opinion

---

### Case 2: Out-of-domain request — Unity C# code
**Input**: "Write me a C# MonoBehaviour that handles player health and fires a Unity event on death."
**Domain checks**:
- Does not produce Unity C# code
- Confirms the project's engine from `engine.name` in `project.yaml` before answering: with Unreal configured, states that the project is built in Unreal Engine 5; with it unset, asks which engine the project uses rather than assuming
- With Unreal configured, maps the request to the Unreal equivalent its own standards prescribe: health as an Attribute Set attribute changed only through Gameplay Effects when GAS is in use, otherwise a C++ `UActorComponent` exposing a death event to Blueprint
- Does not redirect to unity-specialist — that agent serves Unity projects only, and the role uses the project's Unreal expertise; native tools and permissions inherit

---

### Case 3: Domain boundary — UE5.4 API requirement
**Input**: "I need to use the new Motion Matching API introduced in UE5.4."
**Domain checks**:
- Flags that UE5.4 is past the model's training coverage (`<project-engine-reference>/unreal/VERSION.md` lists 5.4 as a post-cutoff, HIGH-risk version)
- Checks `<project-engine-reference>/unreal/` before trusting any API suggestion
- States that no file under `<project-engine-reference>/unreal/` documents Motion Matching, and labels any class or node names it offers as unverified against the pinned version
- Does NOT silently produce stale or incorrect API signatures without a caveat

---

### Case 4: Conflict — Blueprint spaghetti in a core system
**Input**: "Our replication logic is entirely in a deeply nested Blueprint event graph with 300+ nodes and no functions. It's becoming unmaintainable."
**Domain checks**:
- Identifies this as a Blueprint architecture problem, not a minor style issue
- Recommends migrating core replication logic to C++ ActorComponent or GameplayAbility system
- Notes the coordination required: changes to replication architecture must involve lead-programmer
- Does NOT unilaterally declare "migrate to C++" without surfacing the scope of the refactor to the user
- Produces a concrete migration recommendation, not a vague suggestion

---

### Case 5: Context pass — version-appropriate API suggestions
**Input context**: Project engine-reference file states Unreal Engine 5.3.
**Input**: "How do I set up Enhanced Input actions for a new character?"
**Domain checks**:
- Uses UE5.3-era Enhanced Input API (InputMappingContext, UEnhancedInputComponent::BindAction)
- Does NOT reference APIs introduced after UE5.3 without flagging them as potentially unavailable
- References the project's stated engine version in its response
- Provides concrete, version-anchored code or Blueprint node names
