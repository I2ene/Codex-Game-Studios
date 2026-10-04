## Project engine reference contract

When engine facts or APIs matter, explicitly run the native engine-reference command
and read .game-studio/resources/docs/engine-reference-resolution.md. <project-engine-reference> means its resolved
project.root and project.documents. Use actual project version/verification records;
missing records remain unknown. Packaged engine versions are historical background,
never project authority. Confirm current official APIs and actual toolchain before claims.

> Gate definition. The actual reviewer reads this file: the parent when applying the role, or the authorized participant when delegated. Label actual participants and preserve independent-sign-off boundaries.

# PR-PHASE-GATE — Production Readiness at Phase Transition

Agent: `producer` | Settings: inherited session model/effort/permissions | Domain: Scope, timeline, dependencies, production risk

**Trigger**: At every `$gs-gate-check` director panel — producer is on the panel at every `modes.workflow`; spawn in parallel with the rest of it (alone at `minimal`, with TD-PHASE-GATE at `standard`, with TD-PHASE-GATE, CD-PHASE-GATE and AD-PHASE-GATE at `full`)

**Context to pass**:
- Target phase name and the resolved `workflow` tier
- The target gate's required and recommended artifacts at the resolved tier (from `$gs-gate-check`'s loaded gate file)
- Sprint and milestone artifacts present — at `minimal`, the Build order in `design/game-brief.md` is the plan (that tier has no sprint plan)
- Team size (`team.size`) and sprint capacity (from the current sprint plan, if one exists)
- Current blocked story count

**Prompt**:
> "Review the current project state for [target phase] gate readiness from a
> production perspective, judged against what this gate requires at this tier
> (the required-artifacts list you were given). Is the scope realistic for the
> stated timeline and team size? Is the work of [target phase] planned to the
> depth this gate requires — from the Production gate on, a sprint plan at
> `standard`/`full` and the brief's Build order at `minimal`; before it, no
> sprint plan is expected — and are its dependencies ordered so the team can
> execute it in sequence? What milestone or schedule risks could derail the start
> of [target phase] (its first two sprints, where the tier plans in sprints)?
> A required artifact passed as "none" is a finding; one passed as "not expected
> before [phase]" or "not required at `workflow: [tier]`" is not a finding.
> Return READY, CONCERNS [list], or NOT READY [blockers]."

**Verdicts**: READY / CONCERNS / NOT READY
