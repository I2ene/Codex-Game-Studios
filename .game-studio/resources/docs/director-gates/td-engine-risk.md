## Project engine reference contract

When engine facts or APIs matter, explicitly run the native engine-reference command
and read .game-studio/resources/docs/engine-reference-resolution.md. <project-engine-reference> means its resolved
project.root and project.documents. Use actual project version/verification records;
missing records remain unknown. Packaged engine versions are historical background,
never project authority. Confirm current official APIs and actual toolchain before claims.

> Gate definition. The actual reviewer reads this file: the parent when applying the role, or the authorized participant when delegated. Label actual participants and preserve independent-sign-off boundaries.

# TD-ENGINE-RISK — Engine Version Risk Review

Agent: `technical-director` | Settings: inherited session model/effort/permissions | Domain: Architecture, engine risk, performance

**Trigger**: When making architecture decisions that touch post-cutoff engine APIs,
or before finalizing any engine-specific implementation approach

**Context to pass**:
- The specific API or feature being used
- Engine version and LLM knowledge cutoff (from `<project-engine-reference>/VERSION.md`)
- Relevant excerpt from breaking-changes or deprecated-apis docs

**Prompt**:
> "Review this engine API usage against the version reference. Is this API present
> in [engine version]? Has its signature, behaviour, or namespace changed since the
> LLM knowledge cutoff? Are there known deprecations or post-cutoff alternatives?
> Return APPROVE (safe to use as described), CONCERNS [verify before implementing],
> or REJECT [API has changed — provide corrected approach]."

**Verdicts**: APPROVE / CONCERNS / REJECT
