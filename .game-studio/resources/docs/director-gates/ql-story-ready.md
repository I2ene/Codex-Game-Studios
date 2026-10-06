## Project engine reference contract

When engine facts or APIs matter, explicitly run the native engine-reference command
and read .game-studio/resources/docs/engine-reference-resolution.md. <project-engine-reference> means its resolved
project.root and project.documents. Use actual project version/verification records;
missing records remain unknown. Packaged engine versions are historical background,
never project authority. Confirm current official APIs and actual toolchain before claims.

> Gate definition. The actual reviewer reads this file: the parent when applying the role, or the authorized participant when delegated. Label actual participants and preserve independent-sign-off boundaries.

# QL-STORY-READY — QA Lead Story Readiness Check

Agent: `qa-lead` | Responsibility tier: session (inherit)

**Trigger**: Before a story is accepted into a sprint — invoked by `$gs-create-stories`
and `$gs-story-readiness`

**Context to pass**:
- Story file path — or, from `$gs-create-stories` (which runs this gate before any
  story is written), the story inline
- Story type (Logic / Integration / Visual/Feel / UI / Config/Data)
- Acceptance criteria list (verbatim from the story)
- The GDD requirement (TR-ID and text) the story covers

**Prompt**:
> "Review this story's acceptance criteria for testability before it enters the
> sprint. Are all criteria specific enough that a developer would know unambiguously
> when they are done? For Logic-type stories: can every criterion be verified with
> an automated test? For Integration stories: is each criterion observable in a
> controlled test environment? Flag criteria that are too vague to implement
> against, and flag criteria that require a full game build to test (mark these
> DEFERRED, not BLOCKED). Return ADEQUATE (criteria are implementable as written),
> GAPS [specific criteria needing refinement], or INADEQUATE [criteria are too
> vague — story must be revised before sprint inclusion]."

**Verdicts**: ADEQUATE / GAPS / INADEQUATE
