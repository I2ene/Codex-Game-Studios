## Project engine reference contract

When engine facts or APIs matter, explicitly run the native engine-reference command
and read .game-studio/resources/docs/engine-reference-resolution.md. <project-engine-reference> means its resolved
project.root and project.documents. Use actual project version/verification records;
missing records remain unknown. Packaged engine versions are historical background,
never project authority. Confirm current official APIs and actual toolchain before claims.

> Gate definition. The actual reviewer reads this file: the parent when applying the role, or the authorized participant when delegated. Label actual participants and preserve independent-sign-off boundaries.

# TD-CHANGE-IMPACT — Design Change Impact Review

Agent: `technical-director` | Settings: inherited session model/effort/permissions | Domain: Architecture, engine risk, performance

**Trigger**: After the Design Change Impact Report is produced
(`$gs-propagate-design-change` Phase 6), before the resolution workflow begins

**Context to pass**:
- The full Design Change Impact Report from Phase 6 — change summary, every
  affected ADR with its Still Valid / Needs Review / Likely Superseded
  classification, and the recommended actions

**Prompt**:
> "Review this design-change impact assessment before any ADR is revised. Are the
> impact classifications correct — in particular, is any ADR under-classified
> (marked Still Valid when the change actually contradicts its assumptions)? Are
> the recommended actions architecturally sound? Were any cascading effects on
> other ADRs or systems missed — decisions that depend on the ones already
> flagged? Return APPROVE, CONCERNS [the specific ADRs or recommendations to
> revisit], or REJECT [the assessment must be re-analyzed before resolution
> begins — say what was missed]."

**Verdicts**: APPROVE / CONCERNS / REJECT
