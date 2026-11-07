# Your Path

Here's your path at rigor `[value]`. Every skill still runs at any rigor; rigor changes
what's required, not what's allowed.

**`minimal`: 4 steps to running code**
1. `$gs-setup-engine`: choose and configure the engine
2. `$gs-brainstorm`: write the one-page `design/game-brief.md`
3. `$gs-create-stories`: turn the brief's MVP list into stories (no epics or sprint plan needed)
4. `$gs-dev-story`: the first line of game code

**`standard`**
- Concept: `$gs-setup-engine` → `$gs-brainstorm` → `$gs-prototype` → `$gs-art-bible` → `$gs-gate-check`
- Systems Design: `$gs-map-systems` → `$gs-design-system` (once per system) → `$gs-review-all-gdds` →
  `$gs-gate-check`
- Architecture: `$gs-create-architecture` → `$gs-architecture-decision` (once per decision) →
  `$gs-create-control-manifest` → `$gs-architecture-review` → `$gs-test-setup` → `$gs-ux-design`
  (accessibility and interaction patterns) → `$gs-gate-check`
- Pre-Production: `$gs-ux-design` (HUD and key screens) → `$gs-create-epics` → `$gs-create-stories` →
  `$gs-sprint-plan` → `$gs-gate-check`
- Production: `$gs-dev-story`

Each `$gs-gate-check` moves the project one stage, and only when it passes.

**`full`:** everything in `standard`, plus `$gs-vertical-slice` and `$gs-playtest-report` in
Pre-Production and `$gs-design-review` after each GDD.

**Path D with existing work** (stage `Systems Design` or later, or code on disk) gets this instead.
Print only the steps that apply, and for the brief only the one source that applies. At `minimal`:
1. `$gs-project-stage-detect`: what stage the project is at and what is missing
2. `$gs-adopt`: whether the existing files are in the format the skills read
3. `$gs-setup-engine`: only when no engine is set; leave it out when `engine` names one
4. The brief, only if `concept` is absent: `$gs-reverse-document design [code_root]` when the code
   root holds 10 or more source files (it writes the brief from the game), and then do not mention
   `$gs-brainstorm` at all; `$gs-brainstorm` only when it holds fewer

At `standard` and `full`, steps 1 to 3, then `$gs-design-system retrofit [path]`,
`$gs-architecture-decision retrofit [path]`, `$gs-architecture-review` and `$gs-gate-check`.

`minimal` is the documented floor, not a lesser mode. Its trade: no GDDs, so design
problems show up in code.
