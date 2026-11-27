# Configuration resolution

Run `python .game-studio/runtime/studio.py config --root <project-root>` explicitly.
The response contains values, per-leaf sources and notes. There is no injected shell
or per-skill permission grant. Pass the GDD stem as the optional system argument.

Precedence: whitelisted project.local.yaml leaves → project.yaml leaves → legacy
review/stage text → rigor expansion → documented defaults. The runtime uses real YAML,
diagnoses duplicate keys, rejects malformed input and orphan local files, retains on/off strings,
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

Use `$gs-project-settings` for explicit edits; inspect the generated diff. The runtime does
not migrate old Markdown preferences automatically or choose an engine from examples.
See workflow-modes.md, effects-map.md and native-runtime.md for policy and schema.

Read-only resolution reports duplicate keys with source line numbers and merges
mapping blocks, using later values for overlapping leaves. This is inspection
and repair evidence. Fix duplicates before writing configuration or executing
commands; a dotted-path collision with nested settings is rejected.
Use the project's actual tool commands and keep local overrides whitelisted.

`engine_row` is an opt-in derived result of the native config command. Its engine
folders and suggested run/build/test/smoke commands come from the shared
`.game-studio/resources/engines/engines.tsv`. Explicit consumer command argv wins;
table strings are never executed implicitly. Nested shared engine roots outrank
compatible shared top-level roots. Invalid overrides remain invalid, not defaults.
Web uses lead-programmer expertise. `project.goal` is shared and optional: start
shows the inferred goal and saves it only on the accepted assumptions card; cut
writes a changed goal only when the user chooses that change.
