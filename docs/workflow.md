# Game production workflow

Start with `$gs-start`, or use `$gs-adopt` to audit an existing project's artifacts
and actual behavior. `$gs-project-stage-detect` observes what exists; adoption checks
whether that work meets the applicable contracts. `$gs-next-step` recommends the next step.
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

## Main playable route

1. `$gs-prototype` asks one genre-informed round, retains your words and writes the accepted brief.
2. Build the browser playable, run bounded scripted/no-input checks and inspect screenshots against the brief; record assumptions, failures and unassessed items.
3. Play it, ask for changes, tune or share it. Each accepted round keeps a recoverable authorized baseline and preserves unrelated edits.
4. Choose Grow when appropriate, then add one feature per sitting with sampled replay/build/rules/smoke and a keep/revert decision.
5. Use `$gs-cut` to choose scope cuts and polish from actual built facts. Removing implemented code is a separate choice.

No configured engine starts with the browser; an existing non-Web engine keeps
engine/paper prototype paths. `$gs-prototype --spike` tests one mechanic. Stories
are available when requested, or as part of studio mode: `$gs-create-stories`,
`$gs-dev-story`, `$gs-story-done`. A deeper system first needs its applicable design.
Minimal rigor keeps the brief rather than requiring the whole studio artifact ladder;
required evidence and real authorization still apply.

## Studio mode

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

Resume split workflows from the current phase reference rather than re-reading
the full procedure or repeating completed execution. A focused review is evidence
only for the dimensions it covered. A gate cannot advance while any required
check remains unexecuted, even if its aggregate label is CONCERNS.
