## Project engine reference contract

When engine facts or APIs matter, explicitly run the native engine-reference command
and read .game-studio/resources/docs/engine-reference-resolution.md. <project-engine-reference> means its resolved
project.root and project.documents. Use actual project version/verification records;
missing records remain unknown. Packaged engine versions are historical background,
never project authority. Confirm current official APIs and actual toolchain before claims.

> Gate definition. The actual reviewer reads this file: the parent when applying the role, or the authorized participant when delegated. Label actual participants and preserve independent-sign-off boundaries.

# AD-PHASE-GATE — Visual Readiness at Phase Transition

Agent: `art-director` | Responsibility tier: session (inherit) | Domain: Visual identity, art bible, visual production readiness

**Trigger**: At `$gs-gate-check` when `modes.workflow` is `full` — the panel narrows by workflow, and only the full panel includes art-director; spawn in parallel with CD-PHASE-GATE, TD-PHASE-GATE, and PR-PHASE-GATE

**Context to pass**:
- Target phase name and the resolved `workflow` tier
- The target gate's required and recommended artifacts at the resolved tier (from `$gs-gate-check`'s loaded gate file)
- List of all art/visual artifacts present (file paths)
- Visual identity anchor from `design/gdd/game-concept.md` (if present; if there is no `design/gdd/game-concept.md`, the "Art & audio direction" line of `design/game-brief.md`)
- Art bible path if it exists (`design/art/art-bible.md`)

**Prompt**:
> "Review the current project state for [target phase] gate readiness from a visual
> direction perspective, judged against what this gate requires at this tier (the
> required-artifacts list you were given). Is the visual identity established and
> documented at the level this phase requires? Are the visual artifacts this phase
> requires in place? Would visual teams be able to begin their work without
> visual direction gaps that cause costly rework later? Are there visual
> decisions that are being deferred past their latest responsible moment?
> A required artifact passed as "none" is a finding; one passed as "not expected
> before [phase]" or "not required at `workflow: [tier]`" is not a finding.
> Return READY, CONCERNS [specific visual direction gaps that could cause
> production rework], or NOT READY [visual blockers that must exist before this
> phase can succeed — specify what artifact is missing and why it matters at
> this stage]."

**Verdicts**: READY / CONCERNS / NOT READY
