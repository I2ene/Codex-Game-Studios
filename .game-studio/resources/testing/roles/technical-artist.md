# Evaluation scenarios: gs-technical-artist

Professional scenarios adapted from Donchitos' upstream testing guidance; see
[source attribution](../../../NOTICE.md). These are evaluation inputs and domain
checks, not executed results. Read `.codex/agents/gs-technical-artist.toml` and its current procedure first.
Use [evaluation policy](../README.md) and [category rubric](../quality-rubric.md).

Resolve current config and project engine records. Apply review-mode discipline
coverage without claiming automatic delegation: use the parent when needed, label it,
and record actual participants only. Existing human authorization governs writes;
case approvals represent unresolved decisions and never revoke prior authorization.
Historical fixture versions are scenario inputs, not current API verification.
The linked native procedure governs command arguments, output schemas, receipts,
context and mode applicability. Missing inputs remain NOT ASSESSED.

### Case 1: In-domain request — appropriate output
**Input:** "Create a dissolve effect shader for enemy death sequences."
**Domain checks:**
- [ ] Preserve unresolved human decisions and declines; perform routine writes already authorized and ask only for missing decisions or scope.
- Produces shader code or a Shader Graph node spec appropriate to the configured engine (Godot shading language / Unity Shader Graph / Unreal Material Blueprint)
- Exposes the dissolve driver as a documented shader parameter (e.g., a `dissolve_amount` uniform, 0.0–1.0, thresholding a noise texture) and documents each parameter's visual effect
- States the effect's performance budget (e.g., texture samples, shader instruction count)
- Leaves the look of the effect (edge color, glow) to art-director rather than deciding it
- Output is engine-version-aware (checks version reference if post-cutoff APIs are needed)

---

### Case 2: Out-of-domain request — redirects correctly
**Input:** "Define the art bible color palette: primary, secondary, and accent colors for the UI."
**Domain checks:**
- Does NOT produce color palette decisions or art direction documents
- Explicitly states that art style decisions belong to `art-director`
- Redirects the request to `art-director`
- Any follow-up it offers is implementation on its side — e.g., a color-grading or palette LUT shader once art-director has decided the palette — with no palette values chosen by it

---

### Case 3: Performance warning — GPU particle count
**Input:** "The VFX system is triggering a GPU particle count warning at 50,000 particles in the explosion pool."
**Domain checks:**
- Produces an optimization spec addressing the specific warning
- Proposes concrete strategies: particle budget caps per emitter, LOD-based particle reduction, GPU instancing, or switching to mesh-based VFX for distant effects
- Sets an explicit particle-count budget for the explosion effect and states the visual-quality cost of each strategy (e.g., as documented quality tiers)
- Flags any visible change to the explosion's look for art-director rather than deciding it
- Does NOT change gameplay behavior of the explosion (delegates any gameplay impact to gameplay-programmer)

---

### Case 4: Engine version compatibility
**Input:** "Use the new texture sampler API for the water shader."
**Domain checks:**
- Checks the engine version reference (e.g., `<project-engine-reference>/godot/VERSION.md`) before suggesting any API
- Flags if the requested API is post-cutoff (e.g., Godot 4.4+ texture type changes)
- Provides the correct syntax for the project's pinned engine version
- If uncertain about post-cutoff behavior, explicitly states the uncertainty and directs to verified docs

---

### Case 5: Context pass — uses performance budget
**Input:** Performance budget provided in context: 2ms GPU budget for the forest, max 200 draw calls per frame. Request: "Optimize the forest rendering system."
**Domain checks:**
- Treats the 2ms GPU budget and 200 draw call limit from the provided context as the budgets it enforces — no other numbers substituted
- Proposes rendering optimizations (LOD, occlusion, batching, atlasing), each tied to the budget it targets (e.g., "batching reduces draw calls from 340 to ~180, within the 200 limit")
- Calls out any optimization that helps one budget at the other's expense (e.g., merged meshes cut draw calls but can defeat occlusion and raise GPU time past 2ms) instead of presenting it as a free win
- [ ] Preserve unresolved human decisions and declines; perform routine writes already authorized and ask only for missing decisions or scope.
