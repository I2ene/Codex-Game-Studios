---
paths:
  - "assets/shaders/**"
  - "**/*.gdshader"
  - "Assets/**/*.{shader,hlsl,cginc,compute,shadergraph}"
  - "Shaders/**"
  - "**/*.{usf,ush}"
---

## Project engine reference contract

When engine facts or APIs matter, explicitly run the native engine-reference command
and read .game-studio/resources/docs/engine-reference-resolution.md. <project-engine-reference> means its resolved
project.root and project.documents. Use actual project version/verification records;
missing records remain unknown. Packaged engine versions are historical background,
never project authority. Confirm current official APIs and actual toolchain before claims.

# Shader Code Standards

All shader files, in every engine, must follow these standards to maintain
visual quality, performance, and cross-platform compatibility.

## Naming Conventions
- File naming: `[type]_[category]_[name].[ext]`
  - `spatial_env_water.gdshader` (Godot)
  - `SG_Env_Water` (Unity Shader Graph)
  - `M_Env_Water` (Unreal Material)
- Use descriptive names that indicate the material purpose
- Prefix with the engine's shader type — Godot `spatial_`, `canvas_`, `particles_`,
  `post_`; Unity `SG_` (Shader Graph); Unreal `M_`, `MI_` (instance), `MF_` (function)

## Code Quality
- All uniforms/parameters must have descriptive names and appropriate hints
- Group related parameters (Godot: `group_uniforms`, Unity: `[Header]`, Unreal: Category)
- Comment non-obvious calculations (especially math-heavy sections)
- No magic numbers — use named constants or documented uniform values
- Include authorship and purpose comment at the top of each shader file

## Performance Requirements
- Document the target platform and complexity budget for each shader
- Use appropriate precision: `half`/`mediump` on mobile where full precision isn't needed
- Minimize texture samples in fragment shaders
- Avoid dynamic branching in fragment shaders — use `step()`, `smoothstep()` and
  `mix()` (Godot, GLSL) or `lerp()` (HLSL: Unity, Unreal)
- No texture reads inside loops
- Two-pass approach for blur effects (horizontal then vertical)

## Cross-Platform
- Test shaders on minimum spec target hardware
- Provide fallback/simplified versions for lower quality tiers
- Document which render pipeline the shader targets (Forward/Deferred, URP/HDRP, Forward+/Mobile/Compatibility)
- Do not mix shaders from different render pipelines in the same directory

## Variant Management
- Minimize shader variants — each variant is a separate compiled shader
- Document all keywords/variants and their purpose
- Use feature stripping where possible to reduce build size
- Log and monitor total variant count per shader
