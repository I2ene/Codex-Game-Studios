## Project engine reference contract

When engine facts or APIs matter, explicitly run the native engine-reference command
and read .game-studio/resources/docs/engine-reference-resolution.md. <project-engine-reference> means its resolved
project.root and project.documents. Use actual project version/verification records;
missing records remain unknown. Packaged engine versions are historical background,
never project authority. Confirm current official APIs and actual toolchain before claims.

> Gate definition. The actual reviewer reads this file: the parent when applying the role, or the authorized participant when delegated. Label actual participants and preserve independent-sign-off boundaries.

# TD-MANIFEST — Control Manifest Review

Agent: `technical-director` | Settings: inherited session model/effort/permissions | Domain: Architecture, engine risk, performance

**Trigger**: After control-manifest rules are extracted and previewed
(`$gs-create-control-manifest` Phase 4), before the manifest file is written

**Context to pass**:
- The Control Manifest Preview from Phase 4 (rule counts per layer, full extracted rule list)
- The list of ADRs covered
- Engine version
- Any rules sourced from `technical-preferences.md` or engine reference docs

**Prompt**:
> "Review this control manifest before it is written. Are all mandatory ADR
> patterns captured and accurately stated? Are the forbidden approaches complete
> and correctly attributed to their source ADR? Were any rules added that lack a
> source ADR or preference document — that is, invented rather than extracted?
> Are the performance guardrails consistent with the constraints the ADRs
> actually set? Return APPROVE, CONCERNS [list the specific rules to revise], or
> REJECT [rules that are wrong or unsourced and must be fixed before the manifest
> is written]."

**Verdicts**: APPROVE / CONCERNS / REJECT
