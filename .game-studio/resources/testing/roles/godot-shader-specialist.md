# Evaluation scenarios: gs-godot-shader-specialist

Professional scenarios adapted from Donchitos' upstream testing guidance; see
[source attribution](../../../../NOTICE.md). These are evaluation inputs and domain
checks, not executed results. Read `.codex/agents/gs-godot-shader-specialist.toml` and its current procedure first.
Use [evaluation policy](../README.md) and [category rubric](../quality-rubric.md).

Resolve current config and project engine records. Apply review-mode discipline
coverage without claiming automatic delegation: use the parent when needed, label it,
and record actual participants only. Existing human authorization governs writes;
case approvals represent unresolved decisions and never revoke prior authorization.
Historical fixture versions are scenario inputs, not current API verification.
The linked native procedure governs command arguments, output schemas, receipts,
context and mode applicability. Missing inputs remain NOT ASSESSED.

### Case 1: In-domain request — appropriate output
**Input:** "Write a dissolve effect shader for enemy death in Godot."
**Domain checks:**
- Produces valid Godot shading language code (not HLSL, not GLSL directly)
- Uses `shader_type spatial;` or `canvas_item` as appropriate
- Defines `uniform float dissolve_amount : hint_range(0.0, 1.0);`
- Samples a noise texture to determine per-pixel dissolve threshold
- Uses `discard;` for pixels below the threshold
- Optionally adds an edge glow using emission near the dissolve boundary
- Code is syntactically correct for Godot's shading language

---

### Case 2: HLSL redirect
**Input:** "Write an HLSL compute shader for this dissolve effect."
**Domain checks:**
- Does NOT produce HLSL code
- States that Godot materials are written in Godot's own shading language (`.gdshader`, a GLSL derivative), not HLSL
- Translates the HLSL intent into the equivalent `.gdshader` approach (noise threshold, `discard`, emission at the dissolve edge)
- If a compute shader was really the intent, flags compute as a separate low-level path (RenderingDevice; unavailable on the Compatibility renderer) and brings in godot-gdextension-specialist for compute-shader offloading

---

### Case 3: Post-cutoff API change — shader texture types (Godot 4.4)
**Input:** "Use `texture()` with a sampler2D to sample the noise texture in the shader."
**Domain checks:**
- [ ] Preserve unresolved human decisions and declines; perform routine writes already authorized and ask only for missing decisions or scope. Preserve the stated artifact obligations for `VERSION.md`, `breaking-changes.md`, `modules/rendering.md`.
- Identifies what the 4.4 change covers: engine-side shader texture parameter/return types moved from `Texture2D` to `Texture` — script and engine API code that handles shader textures, not shading-language syntax
- Uses `uniform sampler2D noise_texture;` with `texture(noise_texture, UV)` — the form its own patterns use; the reference records no change to shading-language sampling syntax
- Does NOT invent a changed sampling syntax for 4.4–4.6, or rewrite `sampler2D` / `texture()` because of the 4.4 row

---

### Case 4: Fragment shader LOD strategy
**Input:** "The fragment shader for the water surface has 8 texture samples and is causing GPU bottlenecks on mid-range hardware."
**Domain checks:**
- Identifies the per-fragment texture sample count as the primary cost driver
- Proposes an LOD strategy:
  - Reduce sample count at distance with a simplified LOD material for distant water, not a per-pixel distance branch in the fragment shader
  - Move UV/scroll math that does not need per-pixel evaluation into the vertex shader and pass it through a `varying`
  - Make sure the water textures are mipmapped (e.g. `filter_linear_mipmap`) so distant samples read smaller mip levels
- Provides the shader code modification implementing the LOD approach
- Does NOT change gameplay behavior of the water system

---

### Case 5: Context pass — Godot 4.6 glow rework
**Input:** Engine version context: Godot 4.6. Request: "Add a bloom/glow post-processing effect to the scene."
**Domain checks:**
- References the VERSION.md note: Godot 4.6 includes a glow rework
- Because `VERSION.md` records `Installed at pin time` as NOT DETERMINED, asks which editor version is installed before tuning for the 4.6 glow behavior
- Produces glow configuration guidance on the `WorldEnvironment` node's `Environment` resource
- States the documented 4.6 change: glow now processes before tonemapping (it was after), with screen blending — so glow intensity/blend tuned on an earlier version will look different and may need re-tuning
- Does NOT invent renamed or removed glow properties that `breaking-changes.md` and `modules/rendering.md` do not document
- Flags any properties that the LLM's training data may have incorrect information about due to the post-cutoff timing
