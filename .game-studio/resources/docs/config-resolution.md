# Configuration resolution

Run `python .game-studio/runtime/studio.py config --root <project-root>` explicitly.
The response contains values, per-leaf sources and notes. There is no injected shell
or per-skill permission grant. Pass the GDD stem as the optional system argument.

Precedence: whitelisted project.local.yaml leaves → project.yaml leaves → legacy
review/stage text → rigor expansion → documented defaults. The runtime uses real YAML,
rejects duplicate keys, malformed input and orphan local files, retains on/off strings,
and reports invalid enums before falling back. It never guesses a neighboring root.

Rigor minimal: minimal workflow/QA, terse docs, coarse stories, solo review, individual.
Standard: standard workflow/QA, balanced docs/stories, lean review, individual.
Full: full workflow/QA, thorough docs, fine stories, full review, studio.
Explicit leaf values outrank rigor. Start writes only rigor and automation preferences;
it does not pin the six derived knobs or write a new review mirror.

Local whitelist: modes.review_mode, modes.automation, modes.automation_always_ask,
team.size, five testing.strict leaves (logic/integration/visual/ui/config),
performance.enforce, features.session_state and features.token_budget_warn_at.
Other local settings are reported and ignored. Unknown optional project leaves are
retained; per-type test requirements remain the calling skill's responsibility.
Per-system tiers override workflow only. False section flags cannot relax full.

Use `$gs-settings` for explicit edits; inspect the generated diff. The runtime does
not migrate old Markdown preferences automatically or choose an engine from examples.
See workflow-modes.md, effects-map.md and native-runtime.md for policy and schema.
