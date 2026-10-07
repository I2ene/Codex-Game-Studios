# Game production workflow

Start with `$gs-start`, or use `$gs-adopt` to audit an existing project's artifacts
and actual behavior. `$gs-project-stage-detect` observes what exists; adoption checks
whether that work meets the applicable contracts. `$gs-help` recommends the next step.
Keep game records in the game repository, separate from this framework source.

## Rigor and collaboration

`modes.rigor` defaults to `minimal`. It derives workflow, documentation density,
QA, story granularity, review mode and team size unless a leaf is explicitly set.
Choose standard/full for the corresponding project risks and professional artifacts.
A per-system override can raise a system's workflow tier. Read
[workflow modes](../.game-studio/resources/docs/workflow-modes.md) for exact applicability.
Rigor changes requirements; it does not remove access to any skill or discipline.

Collaboration and automation settings express preferences for unresolved decisions.
Existing human authorization and native permissions still govern actions. Keep the
user's vision, scope and budget explicit. Present material options and draft sections
when decisions remain open; do not repeat approval prompts for already authorized work.
See [automation modes](../.game-studio/resources/docs/automation-modes.md).

## Minimal route

1. `$gs-setup-engine` records the actual toolchain when applicable.
2. `$gs-brainstorm` writes a one-page `design/game-brief.md`, including a build order.
3. `$gs-create-stories` turns that build order into implementable stories.
4. `$gs-dev-story` and `$gs-story-done` implement and close each story with its required evidence.

This route does not require an epic, sprint or phase gate. A UI or visual story still
needs the evidence its contract requires. Use additional QA, design or architecture
workflows when the task needs them; raise rigor as the project grows.

## Seven phases

| Phase | Work and typical artifacts | Main skills |
|---|---|---|
| Concept | Player fantasy, pillars, core loop, visual identity, prototype, systems map | `$gs-brainstorm`, `$gs-prototype`, `$gs-art-bible`, `$gs-map-systems` |
| Systems Design | System GDDs, formulas, tuning, dependencies, UX/art/audio/narrative records | `$gs-design-system`, `$gs-design-review`, `$gs-review-all-gdds`, `$gs-ux-design` |
| Technical Setup | Verified engine reference, architecture, ADRs, requirements and control manifest | `$gs-setup-engine`, `$gs-create-architecture`, `$gs-architecture-decision`, `$gs-architecture-review` |
| Pre-Production | Epics, traceable stories, test strategy, vertical slice | `$gs-create-control-manifest`, `$gs-create-epics`, `$gs-create-stories`, `$gs-vertical-slice` |
| Production | Ordered implementation, code review, tests, content and sprint progress | `$gs-story-readiness`, `$gs-dev-story`, `$gs-code-review`, `$gs-story-done`, `$gs-sprint-plan` |
| Polish | Playtests, balance, assets, accessibility, security, performance and regression evidence | `$gs-team-polish`, `$gs-team-qa`, `$gs-balance-check`, `$gs-perf-profile`, `$gs-smoke-check` |
| Release | Build verification, certification, launch readiness, deployment and support | `$gs-release-checklist`, `$gs-launch-checklist`, `$gs-team-release` |

At standard/full, GDD requirements become TR records; architecture and ADRs govern
implementation; epics/stories carry those references into code and tests. Contracts
live alongside the [skills](../.agents/skills/). Templates live under
[resources](../.game-studio/resources/docs/templates/). Use `$gs-consistency-check`
and `$gs-propagate-design-change` when a design changes so downstream work stays aligned.

`$gs-gate-check` evaluates applicable transitions against the target gate, actual
artifacts, quality checks and the review mode's discipline panel. It does not infer
quality from file presence, manufacture missing evidence or silently advance stages.
Strictest verdicts and missing-input handling remain in the gate contracts. A skipped
or parent-applied discipline review must be reported accurately.

## Ongoing operations

Sprint and milestone reviews connect delivery progress to risk and scope. Live
operations include `$gs-team-live-ops`, patch notes, localization, retrospectives,
hotfixes and day-one patches. Preserve rollback plans and real test/release receipts.
Optional checkpoints help resume work; they are records, not new authorization.

Roles may be applied by the current agent or delegated with available tools and
human authorization. Parent work is not independent sign-off. Engine references,
playtests, visual capture and builds need the consumer's real tools and inputs.
See [validation boundaries](validation.md) before interpreting a result as readiness.
