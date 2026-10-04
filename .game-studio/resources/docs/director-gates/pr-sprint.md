## Project engine reference contract

When engine facts or APIs matter, explicitly run the native engine-reference command
and read .game-studio/resources/docs/engine-reference-resolution.md. <project-engine-reference> means its resolved
project.root and project.documents. Use actual project version/verification records;
missing records remain unknown. Packaged engine versions are historical background,
never project authority. Confirm current official APIs and actual toolchain before claims.

> Gate definition. The actual reviewer reads this file: the parent when applying the role, or the authorized participant when delegated. Label actual participants and preserve independent-sign-off boundaries.

# PR-SPRINT — Sprint Feasibility Review

Agent: `producer` | Settings: inherited session model/effort/permissions | Domain: Scope, timeline, dependencies, production risk

**Trigger**: Before finalising a sprint plan (`$gs-sprint-plan`), and after any
mid-sprint scope change

**Context to pass**:
- Proposed sprint story list (titles, estimates, dependencies)
- Team capacity (hours available)
- Current sprint backlog debt (if any)
- Milestone constraints

**Prompt**:
> "Review this sprint plan for feasibility. Is the story load realistic for the
> available capacity? Are stories correctly ordered by dependency? Are there hidden
> dependencies between stories that could block the sprint mid-way? Are any stories
> underestimated given their technical complexity? Return REALISTIC (plan is
> achievable), CONCERNS [specific risks], or UNREALISTIC [sprint must be
> descoped — identify which stories to defer]."

**Verdicts**: REALISTIC / CONCERNS / UNREALISTIC
