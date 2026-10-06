## Project engine reference contract

When engine facts or APIs matter, explicitly run the native engine-reference command
and read .game-studio/resources/docs/engine-reference-resolution.md. <project-engine-reference> means its resolved
project.root and project.documents. Use actual project version/verification records;
missing records remain unknown. Packaged engine versions are historical background,
never project authority. Confirm current official APIs and actual toolchain before claims.

> Gate definition. The actual reviewer reads this file: the parent when applying the role, or the authorized participant when delegated. Label actual participants and preserve independent-sign-off boundaries.

# CD-SYSTEMS — Systems Decomposition Vision Check

Agent: `creative-director` | Settings: inherited session model/effort/permissions | Domain: Vision, pillars, player experience

**Trigger**: After the systems index is written by `$gs-map-systems` — validates the
complete system set before GDD authoring begins

**Context to pass**:
- Systems index path (`design/gdd/systems-index.md`)
- Game pillars and core fantasy (from `design/gdd/game-concept.md`; if there is no `design/gdd/game-concept.md`, the pitch and "what they feel" line of `design/game-brief.md`, which has no pillars)
- Priority tier assignments (MVP / Vertical Slice / Alpha / Full Vision)
- Any high-risk or bottleneck systems identified in the dependency map

**Prompt**:
> "Review this systems decomposition against the game's design pillars. Does the
> full set of MVP-tier systems collectively deliver the core fantasy? Are there
> systems whose mechanics don't serve any stated pillar — indicating they may be
> scope creep? Are there pillar-critical player experiences that have no system
> assigned to deliver them? Are any systems missing that the core loop requires?
> Return APPROVE (systems serve the vision), CONCERNS [specific gaps or
> misalignments with their pillar implications], or REJECT [fundamental gaps —
> the decomposition misses critical design intent and must be revised before GDD
> authoring begins]."

**Verdicts**: APPROVE / CONCERNS / REJECT
