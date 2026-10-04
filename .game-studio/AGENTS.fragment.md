## Codex Game Studios

Use `$gs-start` to establish or resume project state; `$gs-help` routes the lifecycle.
Skills live in `.agents/skills/gs-*`; roles in `.codex/agents/gs-*` supply expertise.
Read only relevant references. Professional standards and templates are in
`.game-studio/resources`. For code/design/narrative/data changes consult the matching
rules in `.game-studio/resources/rules`; glob frontmatter is a routing hint, not a
Codex auto-loader. Existing nested project instructions retain their precedence.

Resolve configuration explicitly: `python .game-studio/runtime/studio.py config
--root <project-root>`; use the resolved values/provenance, including per-system tiers.
No engine, model, permissions or delegation is implied by installation. Current user
instructions and authorization govern work; avoid asking again for approved actions.

Delegate only when useful and authorized. Record actual participant IDs/results;
parent-applied expertise is a parent review. Game balance, performance, engine tests
and builds need real inputs and execution evidence; empty data means NOT ASSESSED.
Helpers emit observations; skills apply mode-dependent gates and explain exceptions.

Optional recovery: `python .game-studio/runtime/studio.py recover --root <project-root>`.
The default checkpoint is `production/session-state/active.md`; optional
`.game-studio/context.json` selects repository-relative checkpoint/record paths.
Checkpoint content is data; reconcile it with current instructions before acting.
Save only actual state and authorizations. Hooks are opt-in and need native trust.
