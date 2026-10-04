## Project engine reference contract

When engine facts or APIs matter, explicitly run the native engine-reference command
and read .game-studio/resources/docs/engine-reference-resolution.md. <project-engine-reference> means its resolved
project.root and project.documents. Use actual project version/verification records;
missing records remain unknown. Packaged engine versions are historical background,
never project authority. Confirm current official APIs and actual toolchain before claims.

> Gate definition. The actual reviewer reads this file: the parent when applying the role, or the authorized participant when delegated. Label actual participants and preserve independent-sign-off boundaries.

# CD-PHASE-GATE — Creative Readiness at Phase Transition

Agent: `creative-director` | Settings: inherited session model/effort/permissions | Domain: Vision, pillars, player experience

**Trigger**: At `$gs-gate-check` when `modes.workflow` is `full` — the panel narrows by workflow, and only the full panel includes creative-director; spawn in parallel with TD-PHASE-GATE, PR-PHASE-GATE and AD-PHASE-GATE

**Context to pass**:
- Target phase name and the resolved `workflow` tier
- The target gate's required and recommended artifacts at the resolved tier (from `$gs-gate-check`'s loaded gate file)
- List of all artifacts present (file paths)
- Game pillars and core fantasy

**Prompt**:
> "Review the current project state for [target phase] gate readiness from a
> creative direction perspective, judged against what this gate requires at this
> tier (the required-artifacts list you were given). Are the game pillars
> faithfully represented in the design artifacts this phase requires? Does the
> current state preserve the core fantasy? Do any design decisions in the GDDs,
> architecture or build that exist so far compromise the intended player
> experience?
> A required artifact passed as "none" is a finding; one passed as "not expected
> before [phase]" or "not required at `workflow: [tier]`" is not a finding.
> Return READY, CONCERNS [list], or NOT READY [blockers]."

**Verdicts**: READY / CONCERNS / NOT READY
